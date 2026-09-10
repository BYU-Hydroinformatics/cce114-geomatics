# Lab 2 main-window and Print Layout screenshots, captured by QGIS 3.44 grabbing itself.
#
# Runs INSIDE QGIS at launch, from a terminal, one shot per process:
#
#   for s in layers-panel map-after-symbology map-with-labels layout-neatline \
#            layout-legend-properties layout-north-arrow-scalebar layout-title-label \
#            finished-layout toolbar-icons; do
#     LAB02_DATA=<data dir> LAB02_OUT=<out dir> SHOT=$s \
#       /Applications/QGIS.app/Contents/MacOS/QGIS --nologo --code tools/qgis_lab02_window_shots.py
#   done
#
# LAB02_DATA holds the three UGRC shapefile downloads, reprojected once to EPSG:26912 with
# ogr2ogr. The downloads arrive in Web Mercator, and reprojecting 413,311 road centrelines to the
# lab's UTM zone 12N on every canvas refresh stalls the capture for tens of minutes. Reprojecting
# ahead of time changes nothing a student would see on screen: same features, same symbology, same
# CRS in the status bar. Everything else the lab asks for is built from the layers themselves, so
# the shots and the written steps cannot drift apart.
#
# Gotchas, all learned the hard way:
#   * QGIS execs --code files, so __file__ is undefined; the paths come from the environment.
#   * The Google Satellite Hybrid XYZ layer needs the network, and the canvas has to be given
#     time to fetch tiles before the grab or the basemap comes out blank.
#   * Quitting with iface.actionExit() pops "Do you want to save?" and hangs the run unless the
#     project has just been written, so write it first and clear the dirty flag.
#   * QGIS resets the canvas CRS to its default after layers are added, so EPSG:26912 has to be
#     re-asserted right before the extent is set or the shot lands on the wrong part of the map.
#   * QWidget.grab() omits the macOS title bar.
#   * QGIS cannot read or write under ~/Desktop, ~/Documents or ~/Downloads on macOS.
import os, time, json, traceback
from qgis.core import (QgsProject, QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem,
                       QgsRectangle, QgsStyle, QgsMarkerSymbol, QgsLineSymbol, QgsFillSymbol,
                       QgsSvgMarkerSymbolLayer, QgsSingleSymbolRenderer, QgsApplication,
                       QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsClassificationQuantile,
                       QgsGraduatedSymbolRenderer, QgsPalLayerSettings, QgsTextFormat,
                       QgsTextBufferSettings, QgsVectorLayerSimpleLabeling, QgsPrintLayout,
                       QgsLayoutItemMap, QgsLayoutItemLabel, QgsLayoutItemLegend, QgsLayoutPoint,
                       QgsLayoutItemScaleBar, QgsLayoutItemPicture, QgsLayoutItemShape,
                       QgsLayoutSize, QgsUnitTypes, QgsLayoutExporter, QgsLayerTreeLayer)
from qgis.PyQt.QtCore import QTimer, Qt, QUrl, QSize
from qgis.PyQt.QtGui import QColor, QFont, QImage, QPainter
from qgis.PyQt.QtWidgets import (QApplication, QToolBar, QToolButton, QWidget,
                                 QDockWidget, QScrollArea)
from qgis.utils import iface

DATA = os.environ['LAB02_DATA']
OUT = os.environ['LAB02_OUT']
SHOT = os.environ.get('SHOT', 'map-after-symbology')
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, 'window-shots.log')

def log(*a):
    with open(LOG, 'a') as f:
        f.write('[%s] %s\n' % (SHOT, ' '.join(str(x) for x in a)))

HWY = ('1', '2', '3', '4', '5')
# Utah Valley, the wide view the symbology and label shots use (EPSG:26912 metres).
VALLEY = QgsRectangle(400000, 4425000, 465000, 4478000)
# Heber Valley, deliberately not an answer to the problem statement: the layout examples use it.
HEBER = QgsRectangle(447000, 4462000, 470000, 4482000)

def basemap():
    url = 'https://mt1.google.com/vt/lyrs%3Dy%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D'
    uri = 'type=xyz&url=' + url + '&zmax=22&zmin=0'
    l = QgsRasterLayer(uri, 'Google Satellite Hybrid', 'wms')
    log('basemap valid', l.isValid())
    return l

def build(styled=True):
    p = QgsProject.instance()
    p.clear()
    crs = QgsCoordinateReferenceSystem('EPSG:26912')
    p.setCrs(crs)
    iface.mapCanvas().setDestinationCrs(crs)

    # Added bottom-up: each new layer lands on top, giving the lab's intended stack of
    # airports, roads, municipalities, basemap.
    bm = basemap()
    p.addMapLayer(bm)
    mun = QgsVectorLayer(os.path.join(DATA, 'municipal', 'Municipalities.shp'),
                         'Municipal Boundaries', 'ogr')
    rds = QgsVectorLayer(os.path.join(DATA, 'roads', 'Roads.shp'), 'Roads', 'ogr')
    apt = QgsVectorLayer(os.path.join(DATA, 'airports', 'AirportLocations.shp'), 'Airports', 'ogr')
    for l in (mun, rds, apt):
        log('layer', l.name(), l.isValid(), l.featureCount())
        p.addMapLayer(l)

    if not styled:
        # Step 9 comes before any symbology, so that shot wants QGIS's random default colours.
        return p, mun, rds, apt, bm

    # airports: circle plus a plane SVG on top, the two-layer symbol of steps 12-14
    sym = QgsMarkerSymbol.createSimple(
        {'name': 'circle', 'color': '#1a7f37', 'outline_color': '#ffffff',
         'outline_width': '0.4', 'size': '3.4'})
    plane = os.path.join(QgsApplication.svgPaths()[0], 'gpsicons', 'plane.svg')
    if os.path.exists(plane):
        sl = QgsSvgMarkerSymbolLayer(plane)
        sl.setSize(2.2)
        sl.setFillColor(QColor('#ffffff'))
        sym.appendSymbolLayer(sl)
    apt.setRenderer(QgsSingleSymbolRenderer(sym))

    # roads: cartocodes 1-5 merged into one Highway category, every other category and the
    # "all other values" row deleted, which is the end state of steps 19 to 21
    hwy = QgsRendererCategory(list(HWY),
                              QgsLineSymbol.createSimple({'color': '#ffe14d', 'width': '0.75'}),
                              'Highway')
    rds.setRenderer(QgsCategorizedSymbolRenderer('CARTOCODE', [hwy]))

    # municipalities: graduated on population, green for the small towns (steps 23-28)
    ramp = QgsStyle.defaultStyle().colorRamp('RdYlGn')
    ramp.invert()
    g = QgsGraduatedSymbolRenderer('POPLASTEST')
    method = QgsClassificationQuantile()
    method.setLabelPrecision(0)
    method.setLabelTrimTrailingZeroes(True)
    g.setClassificationMethod(method)
    g.setSourceSymbol(QgsFillSymbol.createSimple(
        {'color': '#cccccc', 'outline_color': '#ffffff', 'outline_width': '0.3'}))
    g.updateClasses(mun, 5)
    g.updateColorRamp(ramp.clone())
    mun.setRenderer(g)
    mun.setOpacity(0.45)
    return p, mun, rds, apt, bm

def add_labels(mun):
    ls = QgsPalLayerSettings()
    ls.fieldName = 'NAME'
    ls.enabled = True
    tf = QgsTextFormat()
    tf.setFont(QFont('Helvetica', 10))
    tf.setSize(10)
    buf = QgsTextBufferSettings()
    buf.setEnabled(True)
    buf.setSize(1.0)
    buf.setColor(QColor('white'))
    tf.setBuffer(buf)
    ls.setFormat(tf)
    mun.setLabeling(QgsVectorLayerSimpleLabeling(ls))
    mun.setLabelsEnabled(True)

def settle(seconds):
    """Spin the event loop so XYZ tiles arrive and the canvas finishes rendering."""
    end = time.time() + seconds
    while time.time() < end:
        QApplication.processEvents()
        time.sleep(0.05)

def zoom(extent, seconds=14):
    """Point the canvas at an EPSG:26912 extent and wait for it to draw.

    Adding layers queues a deferred full-extent zoom and resets the canvas CRS to the project
    default, and both land after the first event-loop spin. So settle first, then assert the CRS
    and the extent, then settle again and assert the extent once more before the grab.
    """
    c = iface.mapCanvas()
    crs = QgsCoordinateReferenceSystem('EPSG:26912')
    settle(3)
    QgsProject.instance().setCrs(crs)
    c.setDestinationCrs(crs)
    settle(1)
    c.setExtent(extent)
    c.refresh()
    settle(seconds)
    c.setExtent(extent)
    c.refresh()
    settle(6)
    log('canvas crs', c.mapSettings().destinationCrs().authid(),
        'extent', c.extent().toString(0), 'scale %.0f' % c.scale())

def grab(widget, name, wanted=None):
    """Grab a widget, and record where named children sit inside the pixmap.

    tools/lab02_annotate.py draws the red boxes and callouts from that JSON, so the annotations
    follow the widgets instead of being pinned to hand-measured pixel positions.
    """
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

def make_layout(p, layers, extent, with_legend=False, with_furniture=False, with_title=False):
    lay = QgsPrintLayout(p)
    lay.initializeDefaults()
    lay.setName('Lab 2')
    page = lay.pageCollection().page(0)
    pw, ph = page.pageSize().width(), page.pageSize().height()

    m = QgsLayoutItemMap(lay)
    m.attemptMove(QgsLayoutPoint(14, 28, QgsUnitTypes.LayoutMillimeters))
    m.attemptResize(QgsLayoutSize(168, 160, QgsUnitTypes.LayoutMillimeters))
    m.setLayers(layers)
    m.zoomToExtent(extent)
    lay.addLayoutItem(m)

    sh = QgsLayoutItemShape(lay)
    sh.setShapeType(QgsLayoutItemShape.Rectangle)
    sh.attemptMove(QgsLayoutPoint(7, 7, QgsUnitTypes.LayoutMillimeters))
    sh.attemptResize(QgsLayoutSize(pw - 14, ph - 14, QgsUnitTypes.LayoutMillimeters))
    sh.setSymbol(QgsFillSymbol.createSimple(
        {'color': 'transparent', 'outline_color': '#000000', 'outline_width': '0.5'}))
    lay.addLayoutItem(sh)

    lg = None
    if with_legend:
        lg = QgsLayoutItemLegend(lay)
        lg.setTitle('Legend')
        lg.setLinkedMap(m)
        lg.setAutoUpdateModel(False)
        for node in list(lg.model().rootGroup().children()):
            if isinstance(node, QgsLayerTreeLayer) and node.layer() is not None \
                    and node.layer().name().startswith('Google'):
                lg.model().rootGroup().removeChildNode(node)
        lg.attemptMove(QgsLayoutPoint(190, 30, QgsUnitTypes.LayoutMillimeters))
        lay.addLayoutItem(lg)

    na = sb = None
    if with_furniture:
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
        sb.setUnitsPerSegment(2)
        sb.setNumberOfSegments(4)
        sb.update()
        sb.attemptMove(QgsLayoutPoint(112, 176, QgsUnitTypes.LayoutMillimeters))
        lay.addLayoutItem(sb)

    ttl = None
    if with_title:
        ttl = QgsLayoutItemLabel(lay)
        ttl.setText('Filming Site Selection: Heber Valley')
        f = QFont('Helvetica', 24)
        f.setBold(True)
        ttl.setFont(f)
        ttl.attemptMove(QgsLayoutPoint(14, 10, QgsUnitTypes.LayoutMillimeters))
        ttl.attemptResize(QgsLayoutSize(168, 14, QgsUnitTypes.LayoutMillimeters))
        lay.addLayoutItem(ttl)
        cit = QgsLayoutItemLabel(lay)
        cit.setText('Your Name\nYour Section\nLab 2\n\n'
                    'Basemap: Google Satellite\nData: UGRC\nProjection: EPSG:26912')
        cit.setFont(QFont('Helvetica', 11))
        cit.attemptMove(QgsLayoutPoint(190, 120, QgsUnitTypes.LayoutMillimeters))
        cit.attemptResize(QgsLayoutSize(90, 50, QgsUnitTypes.LayoutMillimeters))
        lay.addLayoutItem(cit)

    p.layoutManager().addLayout(lay)
    return lay, m, sh, lg, na, sb, ttl

def designer(lay, select=None, panel=None, scroll=0.0, also=None):
    """Open the Print Layout designer, optionally selecting an item and fronting a panel.

    Selecting an item does not front the Item Properties dock on its own, and the layout steps
    are all about that dock, so raise it by name.
    """
    d = iface.openLayoutDesigner(lay)
    win = d.window()
    win.resize(1500, 1020)
    win.show()
    settle(10)
    if select is not None:
        lay.setSelectedItem(select)
        settle(3)
    if panel:
        for dock in win.findChildren(QDockWidget):
            if dock.windowTitle().strip().lower() == panel.lower():
                dock.raise_()
                dock.show()
                break
        else:
            log('panel not found:', panel,
                '| have:', [x.windowTitle() for x in win.findChildren(QDockWidget)])
        settle(3)
        if scroll:
            for sa in dock.findChildren(QScrollArea):
                b = sa.verticalScrollBar()
                if b.maximum() > 0:
                    b.setValue(int(b.maximum() * scroll))
            settle(2)
    # Front a second panel afterwards, in the other tab stack. raise_() only: calling show() on
    # an already-visible tabified dock moves it into the other stack.
    for extra in (also or []):
        for x in win.findChildren(QDockWidget):
            if x.windowTitle().strip().lower() == extra.lower():
                x.raise_()
                break
        settle(1)
    # An Undo History panel listing the script's own steps has no business in a lab figure.
    lay.undoStack().stack().clear()
    settle(1)
    return d, win

def finish():
    p = QgsProject.instance()
    p.write(os.path.join(OUT, 'lab02-shots.qgz'))
    p.setDirty(False)
    QTimer.singleShot(400, lambda: iface.actionExit().trigger())

def main():
    p, mun, rds, apt, bm = build(styled=SHOT != 'layers-panel')

    if SHOT == 'layers-panel':
        zoom(VALLEY)
        panel = iface.mainWindow().findChild(QWidget, 'Layers')
        grab(panel if panel is not None else iface.layerTreeView(), 'layers-panel')

    elif SHOT == 'map-after-symbology':
        zoom(VALLEY)
        grab(iface.mainWindow(), 'map-after-symbology')

    elif SHOT == 'map-with-labels':
        add_labels(mun)
        zoom(VALLEY)
        grab(iface.mainWindow(), 'map-with-labels')

    elif SHOT == 'layout-neatline':
        add_labels(mun)
        zoom(HEBER, 10)
        lay, m, sh, _, _, _, _ = make_layout(p, [apt, rds, mun, bm], HEBER)
        d, win = designer(lay, select=sh, panel='Items')
        shape_btn = next((b for tb in win.findChildren(QToolBar)
                          for b in tb.findChildren(QToolButton)
                          if b.toolTip().strip().lower() == 'add shape'), None)
        if shape_btn is not None:
            shape_btn.setObjectName('lab02ShapeButton')
        items_dock = next((x for x in win.findChildren(QDockWidget)
                           if x.windowTitle().strip() == 'Items'), None)
        if items_dock is not None:
            items_dock.setObjectName('lab02ItemsDock')
        grab(win, 'layout-neatline',
             {'items-panel': 'lab02ItemsDock', 'shape-tool': 'lab02ShapeButton'})

    elif SHOT == 'layout-legend-properties':
        add_labels(mun)
        zoom(HEBER, 10)
        lay, m, sh, lg, _, _, _ = make_layout(p, [apt, rds, mun, bm], HEBER, with_legend=True)
        d, win = designer(lay, select=lg, panel='Item Properties', scroll=0.32)
        if os.environ.get('DUMP'):
            for dock in win.findChildren(QDockWidget):
                if dock.windowTitle().strip() == 'Item Properties':
                    for ch in dock.findChildren(QWidget):
                        if ch.objectName() and not ch.objectName().startswith('qt_') \
                                and ch.isVisible():
                            log('  IP %-30s %s' % (type(ch).__name__, ch.objectName()))
        grab(win, 'layout-legend-properties',
             {'auto-update': 'mCheckBoxAutoUpdate', 'item-tree': 'mItemTreeView',
              'remove': 'mRemoveToolButton', 'edit': 'mEditPushButton'})

    elif SHOT == 'layout-north-arrow-scalebar':
        add_labels(mun)
        zoom(HEBER, 10)
        lay, m, sh, lg, na, sb, _ = make_layout(p, [apt, rds, mun, bm], HEBER,
                                                with_legend=True, with_furniture=True)
        d, win = designer(lay, select=sb, panel='Item Properties')
        grab(win, 'layout-north-arrow-scalebar', {})

    elif SHOT == 'layout-title-label':
        add_labels(mun)
        zoom(HEBER, 10)
        lay, m, sh, lg, na, sb, ttl = make_layout(p, [apt, rds, mun, bm], HEBER,
                                                  with_legend=True, with_furniture=True,
                                                  with_title=True)
        d, win = designer(lay, select=ttl, panel='Item Properties')
        if os.environ.get('DUMP'):
            for dock in win.findChildren(QDockWidget):
                if dock.windowTitle().strip() == 'Item Properties':
                    for ch in dock.findChildren(QWidget):
                        if ch.objectName() and not ch.objectName().startswith('qt_') \
                                and ch.isVisible():
                            log('  IP %-30s %s' % (type(ch).__name__, ch.objectName()))
        grab(win, 'layout-title-label',
             {'text': 'mTextEdit', 'font': 'mFontButton', 'appearance': 'mAppearanceGroup'})

    elif SHOT == 'finished-layout':
        add_labels(mun)
        zoom(HEBER, 10)
        lay, m, sh, lg, na, sb, ttl = make_layout(p, [apt, rds, mun, bm], HEBER,
                                                  with_legend=True, with_furniture=True,
                                                  with_title=True)
        settle(6)
        exp = QgsLayoutExporter(lay)
        s = QgsLayoutExporter.ImageExportSettings()
        s.dpi = 160
        r = exp.exportToImage(os.path.join(OUT, 'finished-layout.png'), s)
        log('export image result', r)
        log('export pdf result',
            exp.exportToPdf(os.path.join(OUT, 'finished-layout.pdf'),
                            QgsLayoutExporter.PdfExportSettings()))

    elif SHOT == 'toolbar-icons':
        # The item tools in the layout Toolbox are built from the layout item registry and their
        # QActions carry no objectName, so match on the action text instead.
        lay, m, sh, _, _, _, _ = make_layout(p, [mun], HEBER)
        d, win = designer(lay)
        wanted = [('add map', 'icon-add-map'),
                  ('move content', 'icon-move-item-content'),
                  ('add legend', 'icon-add-legend'),
                  ('add north arrow', 'icon-add-north-arrow'),
                  ('add scale bar', 'icon-add-scalebar'),
                  ('add label', 'icon-add-label')]
        buttons = []
        for tb in win.findChildren(QToolBar):
            for btn in tb.findChildren(QToolButton):
                act = btn.defaultAction()
                if act is not None and act.text():
                    buttons.append((act.text().replace('&', '').strip().lower(), btn, act.text()))
        log('toolbar actions:', sorted(set(b[2] for b in buttons)))
        for needle, out_name in wanted:
            hit = next((b for b in buttons if b[0] == needle), None) or \
                  next((b for b in buttons if needle in b[0]), None)
            if hit is None:
                log('MISSING', needle)
                continue
            pm = hit[1].grab()
            pm.save(os.path.join(OUT, out_name + '.png'))
            log('  ', out_name, 'from', repr(hit[2]), pm.width(), 'x', pm.height())

        # The shape tool is a grouped tool button: it carries no action text until it has been
        # used once, so identify it by its tooltip.
        shape_btn = None
        for tb in win.findChildren(QToolBar):
            for btn in tb.findChildren(QToolButton):
                if btn.toolTip().strip().lower() == 'add shape':
                    shape_btn = btn
                    break
            if shape_btn:
                break
        if shape_btn is None:
            log('MISSING add shape')
        else:
            pm = shape_btn.grab()
            pm.save(os.path.join(OUT, 'icon-add-shape.png'))
            log('   icon-add-shape', pm.width(), 'x', pm.height())

    else:
        log('unknown SHOT')

try:
    main()
except Exception:
    log('EXCEPTION\n' + traceback.format_exc())
finish()
