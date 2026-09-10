# Lab 5 and Lab 6 figures, captured by QGIS 3.44 grabbing itself. Runs INSIDE QGIS via --code,
# one shot per process, under a throwaway profile so the UI is QGIS's default light theme:
#
#   for s in $(python3 tools/qgis_lab0506_shots.py --list); do
#     LAB56_DATA=<work dir> LAB56_OUT=<out dir> SHOT=$s \
#       /Applications/QGIS.app/Contents/MacOS/QGIS --nologo --profile lab56shots \
#         --code tools/qgis_lab0506_shots.py
#   done
#
# <work dir> needs merged_dem.tif and slope.tif, built by tools/lab0506_make_demo_data.py from
# the six UGRC 5-metre auto-correlated DEM tiles the lab has students download.
#
# The two layout figures are the point of this script: the ones in the repository carry Dan's red
# strike-through markup ("Slope" struck out on the elevation layout, "DEM" on the slope layout),
# which has been flagged in tools/image-improvements-handoff.md since 2026-09-02.
#
# Same gotchas as the Lab 3/4 script: __file__ is undefined under --code, XYZ tiles need time to
# arrive, QGIS resets the canvas CRS after layers are added so EPSG:26912 must be re-asserted right
# before the extent, and iface.actionExit() hangs unless the project has just been written.
import os
import sys
import time
import json
import traceback

SHOTS = ['lab5-tiles-added', 'lab5-processing-toolbox', 'lab5-merge-dialog', 'lab5-pseudocolor',
         'lab5-hillshade-combined', 'lab5-identify-y', 'lab5-slope-dialog', 'lab5-slope-map',
         'lab5-export-dialog', 'lab5-elevation-layout', 'lab5-slope-layout', 'lab5-toolbar-icons',
         'lab6-rest-connection', 'lab6-styled-map', 'lab6-layout']

if '--list' in sys.argv:
    print(' '.join(SHOTS))
    raise SystemExit

from qgis.core import (QgsProject, QgsRasterLayer, QgsVectorLayer, QgsCoordinateReferenceSystem,
                       QgsRectangle, QgsStyle, QgsHillshadeRenderer, QgsColorRampShader,
                       QgsRasterShader, QgsSingleBandPseudoColorRenderer, QgsRasterBandStats,
                       QgsSingleBandGrayRenderer, QgsContrastEnhancement, QgsPrintLayout,
                       QgsLayoutItemMap, QgsLayoutItemLabel, QgsLayoutItemLegend, QgsLayoutPoint,
                       QgsLayoutItemScaleBar, QgsLayoutItemPicture, QgsLayoutItemShape,
                       QgsLayoutSize, QgsUnitTypes, QgsLayoutExporter, QgsApplication,
                       QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings,
                       QgsVectorLayerSimpleLabeling, QgsLayerTreeLayer, QgsNullSymbolRenderer)
from qgis.PyQt.QtCore import QTimer
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtWidgets import QApplication, QToolBar, QToolButton, QWidget, QDockWidget
from qgis.utils import iface

DATA = os.environ['LAB56_DATA']
OUT = os.environ['LAB56_OUT']
SHOT = os.environ.get('SHOT', '')
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, 'lab0506-shots.log')

CRS = QgsCoordinateReferenceSystem('EPSG:26912')
# Utah Valley: Utah Lake, Provo, Orem and Spanish Fork, in EPSG:26912 metres.
VALLEY = QgsRectangle(420000, 4425000, 465000, 4470000)
# The Y on Y Mountain, for the Identify step.
Y_HILL = QgsRectangle(444800, 4456600, 447000, 4458400)


def log(*a):
    with open(LOG, 'a') as f:
        f.write('[%s] %s\n' % (SHOT, ' '.join(str(x) for x in a)))


def settle(seconds):
    end = time.time() + seconds
    while time.time() < end:
        QApplication.processEvents()
        time.sleep(0.05)


def basemap():
    url = 'https://mt1.google.com/vt/lyrs%3Ds%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D'
    return QgsRasterLayer('type=xyz&url=' + url + '&zmax=22&zmin=0', 'Google Satellite', 'wms')


def zoom(extent, seconds=14):
    c = iface.mapCanvas()
    settle(3)
    QgsProject.instance().setCrs(CRS)
    c.setDestinationCrs(CRS)
    settle(1)
    c.setExtent(extent)
    c.refresh()
    settle(seconds)
    c.setExtent(extent)
    c.refresh()
    settle(6)
    log('canvas', c.mapSettings().destinationCrs().authid(), c.extent().toString(0))


def grab(widget, name, wanted=None):
    QApplication.processEvents()
    pm = widget.grab()
    pm.save(os.path.join(OUT, name + '.png'))
    if wanted:
        scale = widget.devicePixelRatioF()
        out = {}
        for key, obj in wanted.items():
            w = widget.findChild(QWidget, obj)
            if w is None or not w.isVisible():
                log('  (no visible widget %s for %s)' % (obj, key))
                continue
            tl = w.mapTo(widget, w.rect().topLeft())
            out[key] = [round(tl.x() * scale), round(tl.y() * scale),
                        round(w.width() * scale), round(w.height() * scale)]
        with open(os.path.join(OUT, name + '.json'), 'w') as f:
            json.dump(out, f, indent=1)
    log('saved', name, pm.width(), 'x', pm.height())


def dem(name='Elevation (m)'):
    r = QgsRasterLayer(os.path.join(DATA, 'merged_dem.tif'), name)
    log('dem valid', r.isValid())
    return r


def pseudocolor(layer, opacity=1.0):
    """The green-to-red singleband pseudocolor of Lab 5 steps 22 to 23."""
    st = layer.dataProvider().bandStatistics(1, QgsRasterBandStats.Min | QgsRasterBandStats.Max)
    # Round to whole metres, or the legend shows the raw float band range, 1,327.599976 and
    # 3,579.100098, which is not something to put on a finished map.
    lo, hi = float(int(st.minimumValue)), float(int(st.maximumValue) + 1)
    ramp = QgsStyle.defaultStyle().colorRamp('Spectral')
    ramp.invert()
    shader_fn = QgsColorRampShader(lo, hi)
    shader_fn.setColorRampType(QgsColorRampShader.Interpolated)
    shader_fn.setSourceColorRamp(ramp)
    # classifyColorRamp will not take None for the extent or the feedback in 3.44, so build the
    # class list directly from the band's own min and max.
    items = []
    for i in range(21):
        v = lo + (hi - lo) * i / 20.0
        items.append(QgsColorRampShader.ColorRampItem(v, ramp.color(i / 20.0), '%.0f' % v))
    shader_fn.setColorRampItemList(items)
    shader = QgsRasterShader()
    shader.setRasterShaderFunction(shader_fn)
    layer.setRenderer(QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, shader))
    layer.setOpacity(opacity)
    return layer


def hillshade(layer):
    r = QgsHillshadeRenderer(layer.dataProvider(), 1, 315.0, 45.0)
    layer.setRenderer(r)
    return layer


def cities():
    p = os.path.join(DATA, 'cities.shp')
    if not os.path.exists(p):
        log('no cities.shp; skipping labels')
        return None
    lyr = QgsVectorLayer(p, 'Cities and Towns', 'ogr')
    lyr.setRenderer(QgsNullSymbolRenderer())          # step 31: "No Symbols"
    field = next((f.name() for f in lyr.fields() if f.name().upper() in ('NAME', 'CITY')), None)
    ls = QgsPalLayerSettings()
    ls.fieldName = field
    ls.enabled = True
    tf = QgsTextFormat()
    tf.setFont(QFont('Helvetica', 10))
    tf.setSize(10)
    buf = QgsTextBufferSettings()
    buf.setEnabled(True)
    buf.setSize(1.2)
    buf.setColor(QColor('white'))
    tf.setBuffer(buf)
    ls.setFormat(tf)
    lyr.setLabeling(QgsVectorLayerSimpleLabeling(ls))
    lyr.setLabelsEnabled(True)
    log('cities field', field, lyr.featureCount())
    return lyr


def layout(p, layers, extent, title, legend_title=None):
    lay = QgsPrintLayout(p)
    lay.initializeDefaults()
    page = lay.pageCollection().page(0)
    pw, ph = page.pageSize().width(), page.pageSize().height()
    m = QgsLayoutItemMap(lay)
    m.attemptMove(QgsLayoutPoint(14, 30, QgsUnitTypes.LayoutMillimeters))
    m.attemptResize(QgsLayoutSize(168, 158, QgsUnitTypes.LayoutMillimeters))
    m.setLayers(layers)
    m.zoomToExtent(extent)
    lay.addLayoutItem(m)
    sh = QgsLayoutItemShape(lay)
    sh.setShapeType(QgsLayoutItemShape.Rectangle)
    sh.attemptMove(QgsLayoutPoint(7, 7, QgsUnitTypes.LayoutMillimeters))
    sh.attemptResize(QgsLayoutSize(pw - 14, ph - 14, QgsUnitTypes.LayoutMillimeters))
    sh.setSymbol(__import__('qgis.core', fromlist=['QgsFillSymbol']).QgsFillSymbol.createSimple(
        {'color': 'transparent', 'outline_color': '#000000', 'outline_width': '0.5'}))
    lay.addLayoutItem(sh)
    lg = QgsLayoutItemLegend(lay)
    lg.setTitle('Legend')
    lg.setLinkedMap(m)
    lg.setAutoUpdateModel(False)
    for node in list(lg.model().rootGroup().children()):
        if isinstance(node, QgsLayerTreeLayer) and node.layer() is not None \
                and node.layer().name().startswith('Google'):
            lg.model().rootGroup().removeChildNode(node)
    if legend_title:
        for node in lg.model().rootGroup().children():
            if isinstance(node, QgsLayerTreeLayer) and node.layer() is not None \
                    and node.layer().name().lower().startswith('slope'):
                node.setName(legend_title)
    lg.attemptMove(QgsLayoutPoint(190, 32, QgsUnitTypes.LayoutMillimeters))
    lay.addLayoutItem(lg)
    na = QgsLayoutItemPicture(lay)
    na.setPicturePath(os.path.join(QgsApplication.svgPaths()[0], 'arrows', 'NorthArrow_02.svg'))
    na.attemptMove(QgsLayoutPoint(166, 158, QgsUnitTypes.LayoutMillimeters))
    na.attemptResize(QgsLayoutSize(14, 14, QgsUnitTypes.LayoutMillimeters))
    lay.addLayoutItem(na)
    sb = QgsLayoutItemScaleBar(lay)
    sb.setStyle('Single Box')
    sb.setLinkedMap(m)
    sb.setUnits(QgsUnitTypes.DistanceKilometers)
    sb.setUnitLabel('km')
    sb.setUnitsPerSegment(5)
    sb.setNumberOfSegments(4)
    sb.update()
    sb.attemptMove(QgsLayoutPoint(110, 176, QgsUnitTypes.LayoutMillimeters))
    lay.addLayoutItem(sb)
    t = QgsLayoutItemLabel(lay)
    t.setText(title)
    f = QFont('Helvetica', 22)
    f.setBold(True)
    t.setFont(f)
    t.attemptMove(QgsLayoutPoint(14, 12, QgsUnitTypes.LayoutMillimeters))
    t.attemptResize(QgsLayoutSize(180, 14, QgsUnitTypes.LayoutMillimeters))
    lay.addLayoutItem(t)
    c = QgsLayoutItemLabel(lay)
    c.setText('Your Name\nYour Section\nLab 5\n\nBasemap: Google Satellite\n'
              'Data: UGRC 5 m auto-correlated DEM\nProjection: EPSG:26912')
    c.setFont(QFont('Helvetica', 10))
    c.attemptMove(QgsLayoutPoint(190, 120, QgsUnitTypes.LayoutMillimeters))
    c.attemptResize(QgsLayoutSize(95, 60, QgsUnitTypes.LayoutMillimeters))
    lay.addLayoutItem(c)
    p.layoutManager().addLayout(lay)
    return lay


def export_layout(lay, name, dpi=150):
    exp = QgsLayoutExporter(lay)
    s = QgsLayoutExporter.ImageExportSettings()
    s.dpi = dpi
    log('export', name, exp.exportToImage(os.path.join(OUT, name + '.png'), s))


def toolbar_icons(pairs, prefix):
    win = iface.mainWindow()
    buttons = []
    for tb in win.findChildren(QToolBar):
        for b in tb.findChildren(QToolButton):
            a = b.defaultAction()
            txt = (a.text() if a is not None else '') or ''
            buttons.append((txt.replace('&', '').strip().lower(), b.toolTip().strip().lower(), b))
    for needle, out_name in pairs:
        hit = (next((b for t, _, b in buttons if t == needle), None)
               or next((b for t, _, b in buttons if needle in t), None)
               or next((b for _, tip, b in buttons if needle in tip), None))
        if hit is None:
            log('MISSING', needle)
            continue
        pm = hit.grab()
        pm.save(os.path.join(OUT, prefix + out_name + '.png'))
        log('  ', prefix + out_name, pm.width(), 'x', pm.height())


def open_toolbox():
    for a in iface.mainWindow().findChildren(type(iface.actionExit())):
        if 'toolbox' in (a.text() or '').replace('&', '').lower():
            a.trigger()
            settle(3)
            return next((d for d in iface.mainWindow().findChildren(QDockWidget)
                         if 'toolbox' in d.windowTitle().lower()), None)
    return None


def finish():
    p = QgsProject.instance()
    p.write(os.path.join(OUT, 'lab56-shots.qgz'))
    p.setDirty(False)
    QTimer.singleShot(400, lambda: iface.actionExit().trigger())


def main():
    p = QgsProject.instance()
    p.clear()
    p.setCrs(CRS)

    if SHOT == 'lab5-tiles-added':
        # Step 12: the six tiles added but not yet merged, over the basemap.
        p.addMapLayer(basemap())
        n = 0
        for f in sorted(os.listdir(DATA)):
            if f.endswith('.asc'):
                r = QgsRasterLayer(os.path.join(DATA, f), f[:-4])
                if r.isValid():
                    r.setCrs(CRS)
                    p.addMapLayer(r)
                    n += 1
        log('tiles added', n)
        zoom(VALLEY)
        grab(iface.mainWindow(), 'lab5-tiles-added')

    elif SHOT == 'lab5-processing-toolbox':
        p.addMapLayer(dem())
        settle(3)
        dock = open_toolbox()
        if dock is None:
            log('MISSING processing toolbox')
        else:
            from qgis.PyQt.QtWidgets import QLineEdit
            for le in dock.findChildren(QLineEdit):
                if le.isVisible():
                    le.setText('merge raster')
                    break
            settle(4)
            grab(dock, 'lab5-processing-toolbox')

    elif SHOT in ('lab5-merge-dialog', 'lab5-slope-dialog'):
        import processing
        from processing.core.Processing import Processing
        Processing.initialize()
        p.addMapLayer(dem())
        settle(3)
        alg = 'gdal:merge' if SHOT == 'lab5-merge-dialog' else 'native:slope'
        from processing.gui.AlgorithmDialog import AlgorithmDialog
        a = QgsApplication.processingRegistry().algorithmById(alg)
        if a is None:
            log('MISSING algorithm', alg)
        else:
            d = AlgorithmDialog(a.create(), False, iface.mainWindow())
            d.resize(1000, 760)
            d.show()
            settle(4)
            grab(d, SHOT)

    elif SHOT in ('lab5-pseudocolor', 'lab5-hillshade-combined', 'lab5-slope-map'):
        p.addMapLayer(basemap())
        if SHOT == 'lab5-slope-map':
            s = QgsRasterLayer(os.path.join(DATA, 'slope.tif'), 'Slope (degrees)')
            s.setCrs(CRS)
            p.addMapLayer(s)
        else:
            if SHOT == 'lab5-hillshade-combined':
                p.addMapLayer(hillshade(dem('Hillshade')))
            p.addMapLayer(pseudocolor(dem(), 0.55 if SHOT == 'lab5-hillshade-combined' else 1.0))
        zoom(VALLEY)
        grab(iface.mainWindow(), SHOT)

    elif SHOT == 'lab5-identify-y':
        p.addMapLayer(basemap())
        p.addMapLayer(pseudocolor(dem(), 0.55))
        zoom(Y_HILL)
        grab(iface.mainWindow(), 'lab5-identify-y')

    elif SHOT == 'lab5-export-dialog':
        s = QgsRasterLayer(os.path.join(DATA, 'slope.tif'), 'Slope (degrees)')
        s.setCrs(CRS)
        p.addMapLayer(s)
        settle(2)
        from qgis.gui import QgsRasterLayerSaveAsDialog
        d = QgsRasterLayerSaveAsDialog(s, s.dataProvider(), s.extent(), s.crs(), s.crs(),
                                       iface.mainWindow())
        d.resize(980, 900)
        d.show()
        settle(3)
        grab(d, 'lab5-export-dialog')

    elif SHOT in ('lab5-elevation-layout', 'lab5-slope-layout'):
        bm = basemap()
        p.addMapLayer(bm)
        cty = cities()
        if cty:
            p.addMapLayer(cty)
        if SHOT == 'lab5-elevation-layout':
            hs = hillshade(dem('Hillshade'))
            pc = pseudocolor(dem('Elevation (m)'), 0.55)
            p.addMapLayer(hs)
            p.addMapLayer(pc)
            layers = ([cty] if cty else []) + [pc, hs, bm]
            title = 'Utah Valley Elevation'
            legend_title = None
        else:
            s = QgsRasterLayer(os.path.join(DATA, 'slope.tif'), 'Slope (degrees)')
            s.setCrs(CRS)
            p.addMapLayer(s)
            layers = ([cty] if cty else []) + [s, bm]
            title = 'Utah Valley Slope'
            legend_title = 'Slope (degrees)'
        zoom(VALLEY)
        lay = layout(p, layers, VALLEY, title, legend_title)
        settle(6)
        export_layout(lay, SHOT)

    elif SHOT == 'lab5-toolbar-icons':
        p.addMapLayer(dem())
        settle(4)
        toolbar_icons([('identify features', 'identify'),
                       ('open data source manager', 'data-source-manager'),
                       ('refresh', 'refresh')], 'lab5-icon-')

    else:
        log('unknown or not-yet-implemented SHOT')


try:
    main()
except Exception:
    log('EXCEPTION\n' + traceback.format_exc())
finish()
