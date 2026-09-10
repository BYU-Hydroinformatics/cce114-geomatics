# Lab 3 and Lab 4 main-window, map-canvas and Print Layout screenshots, captured by QGIS 3.44
# grabbing itself. Runs INSIDE QGIS at launch, one shot per process:
#
#   for s in $(python3 tools/qgis_lab0304_window_shots.py --list); do
#     LAB34_DATA=<data dir> LAB34_OUT=<out dir> SHOT=$s \
#       /Applications/QGIS.app/Contents/MacOS/QGIS --nologo --code tools/qgis_lab0304_window_shots.py
#   done
#
# Gotchas are the same ones tools/qgis_lab02_window_shots.py documents: __file__ is undefined under
# --code, the XYZ basemap needs time to fetch tiles, QGIS resets the canvas CRS after layers are
# added so EPSG:26912 has to be re-asserted right before the extent, and quitting via
# iface.actionExit() hangs on the unsaved-project prompt unless the project has just been written.
import os
import sys
import time
import json
import traceback

if '--list' in sys.argv:
    print('lab3-toolbar-icons lab3-digitizing-toolbar lab3-campus-polygon lab3-example-layout '
          'lab4-data-source-manager lab4-snapping-toolbar lab4-toolbar-icons '
          'lab4-temple-site lab4-footprints lab4-canal-before lab4-canal-after')
    raise SystemExit

from qgis.core import (QgsProject, QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem,
                       QgsRectangle, QgsMarkerSymbol, QgsLineSymbol, QgsFillSymbol,
                       QgsSingleSymbolRenderer, QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLabel,
                       QgsLayoutItemLegend, QgsLayoutItemScaleBar, QgsLayoutItemPicture,
                       QgsLayoutItemShape, QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes,
                       QgsLayoutExporter, QgsApplication, QgsPalLayerSettings, QgsTextFormat,
                       QgsTextBufferSettings, QgsVectorLayerSimpleLabeling, QgsLayerTreeLayer)
from qgis.PyQt.QtCore import QTimer
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtWidgets import QApplication, QToolBar, QToolButton, QWidget, QDockWidget
from qgis.utils import iface

DATA = os.environ['LAB34_DATA']
OUT = os.environ['LAB34_OUT']
SHOT = os.environ.get('SHOT', '')
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, 'window-shots-34.log')

CRS = QgsCoordinateReferenceSystem('EPSG:26912')
# BYU main campus, and the Spanish Fork temple site, both EPSG:26912 metres.
CAMPUS = QgsRectangle(444100, 4454900, 445500, 4456100)
TEMPLE = QgsRectangle(447350, 4439540, 447950, 4440090)
CANAL = QgsRectangle(447150, 4439600, 447600, 4440000)


def log(*a):
    with open(LOG, 'a') as f:
        f.write('[%s] %s\n' % (SHOT, ' '.join(str(x) for x in a)))


def basemap():
    url = 'https://mt1.google.com/vt/lyrs%3Dy%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D'
    l = QgsRasterLayer('type=xyz&url=' + url + '&zmax=22&zmin=0', 'Google Satellite Hybrid', 'wms')
    log('basemap valid', l.isValid())
    return l


def settle(seconds):
    end = time.time() + seconds
    while time.time() < end:
        QApplication.processEvents()
        time.sleep(0.05)


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


def add(path, name, provider='ogr'):
    l = QgsVectorLayer(os.path.join(DATA, path), name, provider)
    log('layer', name, l.isValid(), l.featureCount())
    QgsProject.instance().addMapLayer(l)
    return l


def toolbar_icons(pairs, prefix):
    """Grab named toolbar buttons by their action text or tooltip, at native 2x."""
    win = iface.mainWindow()
    buttons = []
    for tb in win.findChildren(QToolBar):
        for b in tb.findChildren(QToolButton):
            a = b.defaultAction()
            txt = (a.text() if a is not None else '') or ''
            buttons.append((txt.replace('&', '').strip().lower(), b.toolTip().strip().lower(), b))
    log('toolbar actions:', sorted({t for t, _, _ in buttons if t})[:60])
    for needle, out_name in pairs:
        hit = (next((b for t, tip, b in buttons if t == needle), None)
               or next((b for t, tip, b in buttons if needle in t), None)
               or next((b for t, tip, b in buttons if needle in tip), None))
        if hit is None:
            log('MISSING', needle)
            continue
        pm = hit.grab()
        pm.save(os.path.join(OUT, prefix + out_name + '.png'))
        log('  ', prefix + out_name, pm.width(), 'x', pm.height())


def finish():
    p = QgsProject.instance()
    p.write(os.path.join(OUT, 'lab34-shots.qgz'))
    p.setDirty(False)
    QTimer.singleShot(400, lambda: iface.actionExit().trigger())


def main():
    p = QgsProject.instance()
    p.clear()
    p.setCrs(CRS)

    if SHOT == 'lab3-toolbar-icons':
        # Only one layer is active at a time, and the Add Point / Add Polygon buttons appear only
        # while a layer of that geometry is active, so capture in two passes.
        pts = add('pts_corrected.shp', 'pts_corrected')
        camp = add('campus.shp', 'campus')
        iface.setActiveLayer(pts)
        pts.startEditing()
        settle(4)
        toolbar_icons([('add point feature', 'add-point-feature'),
                       ('move feature', 'move-feature'),
                       ('open field calculator', 'field-calculator'),
                       ('open data source manager', 'data-source-manager'),
                       ('new shapefile layer', 'new-shapefile-layer'),
                       ('toggle editing', 'toggle-editing'),
                       ('save layer edits', 'save-layer-edits')], 'lab3-icon-')
        pts.rollBack()
        iface.setActiveLayer(camp)
        camp.startEditing()
        settle(4)
        toolbar_icons([('add polygon feature', 'add-polygon-feature')], 'lab3-icon-')
        camp.rollBack()

    elif SHOT == 'lab3-digitizing-toolbar':
        lyr = add('pts_corrected.shp', 'pts_corrected')
        iface.setActiveLayer(lyr)
        lyr.startEditing()
        settle(4)
        tb = next((t for t in iface.mainWindow().findChildren(QToolBar)
                   if t.objectName() == 'mDigitizeToolBar'), None)
        grab(tb if tb is not None else iface.mainWindow(), 'lab3-digitizing-toolbar')
        lyr.rollBack()

    elif SHOT == 'lab3-campus-polygon':
        p.addMapLayer(basemap())
        camp = add('campus.shp', 'campus')
        camp.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
            {'color': 'transparent', 'outline_color': '#ffd400', 'outline_width': '0.9'})))
        zoom(CAMPUS)
        grab(iface.mainWindow(), 'lab3-campus-polygon')

    elif SHOT == 'lab3-example-layout':
        p.addMapLayer(basemap())
        camp = add('campus_area.shp', 'campus')
        camp.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
            {'color': 'transparent', 'outline_color': '#ffd400', 'outline_width': '0.9'})))
        pts = add('points.csv', 'points', 'delimitedtext') if os.path.exists(
            os.path.join(DATA, 'points.csv')) else None
        cor = add('pts_corrected.shp', 'pts_corrected')
        cor.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
            {'name': 'circle', 'color': '#1a7f37', 'outline_color': '#ffffff', 'size': '3'})))
        zoom(CAMPUS)
        area = next(camp.getFeatures()).attribute('area')
        acres = area / 4046.8564224
        lay = layout(p, [cor, camp] + ([pts] if pts else []),
                     CAMPUS, 'BYU Campus GPS Survey',
                     'Campus area: %.0f acres' % acres)
        exp = QgsLayoutExporter(lay)
        s = QgsLayoutExporter.ImageExportSettings()
        s.dpi = 160
        log('layout export', exp.exportToImage(os.path.join(OUT, 'lab3-example-layout.png'), s),
            'area %.0f m2 = %.0f acres' % (area, acres))

    elif SHOT == 'lab4-data-source-manager':
        settle(4)
        # There is no iface.actionDataSourceManager() in 3.44; find the action by its text.
        act = next((a for a in iface.mainWindow().findChildren(type(iface.actionExit()))
                    if 'data source manager' in (a.text() or '').replace('&', '').lower()), None)
        if act is None:
            log('MISSING Data Source Manager action')
            finish()
            return
        act.trigger()
        settle(6)
        dlg = next((w for w in QApplication.topLevelWidgets()
                    if w.isVisible() and 'DataSourceManager' in w.objectName()), None)
        if dlg is None:
            log('MISSING data source manager dialog')
        else:
            dlg.resize(1180, 900)
            settle(2)
            grab(dlg, 'lab4-data-source-manager')

    elif SHOT == 'lab4-snapping-toolbar':
        add('SF_Waterways.gpkg', 'Waterways')
        settle(4)
        tb = next((t for t in iface.mainWindow().findChildren(QToolBar)
                   if t.objectName() == 'mSnappingToolBar'), None)
        if tb is None:
            log('MISSING snapping toolbar; names:',
                [t.objectName() for t in iface.mainWindow().findChildren(QToolBar)])
        else:
            tb.setVisible(True)
            settle(2)
            grab(tb, 'lab4-snapping-toolbar')

    elif SHOT == 'lab4-toolbar-icons':
        add('SF_Waterways.gpkg', 'Waterways')
        settle(4)
        toolbar_icons([('toggle editing', 'toggle-editing'),
                       ('save layer edits', 'save-layer-edits'),
                       ('add point feature', 'add-point-feature'),
                       ('vertex tool', 'vertex-tool'),
                       ('add polygon feature', 'add-polygon-feature')], 'lab4-icon-')

    elif SHOT in ('lab4-temple-site', 'lab4-footprints', 'lab4-canal-before', 'lab4-canal-after'):
        p.addMapLayer(basemap())
        if SHOT in ('lab4-canal-before', 'lab4-canal-after'):
            w = add('SF_Waterways.gpkg', 'Waterways')
            w.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
                {'color': '#1e90ff', 'width': '0.9'})))
            zoom(CANAL)
        elif SHOT == 'lab4-footprints':
            lot = add('parking_lot.shp', 'Parking_Lot')
            lot.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
                {'color': '164,110,200,120', 'outline_color': '#6b3fa0', 'outline_width': '0.6'})))
            tem = add('temple_footprint.shp', 'Temple_Footprint')
            tem.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
                {'color': '255,214,0,140', 'outline_color': '#c8a200', 'outline_width': '0.6'})))
            zoom(TEMPLE)
        else:
            zoom(TEMPLE)
        grab(iface.mainWindow(), SHOT)

    else:
        log('unknown SHOT')


def layout(p, layers, extent, title, note):
    lay = QgsPrintLayout(p)
    lay.initializeDefaults()
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
    na = QgsLayoutItemPicture(lay)
    na.setPicturePath(os.path.join(QgsApplication.svgPaths()[0], 'arrows', 'NorthArrow_02.svg'))
    na.attemptMove(QgsLayoutPoint(166, 158, QgsUnitTypes.LayoutMillimeters))
    na.attemptResize(QgsLayoutSize(14, 14, QgsUnitTypes.LayoutMillimeters))
    lay.addLayoutItem(na)
    sb = QgsLayoutItemScaleBar(lay)
    sb.setStyle('Single Box')
    sb.setLinkedMap(m)
    sb.setUnits(QgsUnitTypes.DistanceMeters)
    sb.setUnitLabel('m')
    sb.setUnitsPerSegment(100)
    sb.setNumberOfSegments(4)
    sb.update()
    sb.attemptMove(QgsLayoutPoint(112, 176, QgsUnitTypes.LayoutMillimeters))
    lay.addLayoutItem(sb)
    t = QgsLayoutItemLabel(lay)
    t.setText(title)
    f = QFont('Helvetica', 24)
    f.setBold(True)
    t.setFont(f)
    t.attemptMove(QgsLayoutPoint(14, 10, QgsUnitTypes.LayoutMillimeters))
    t.attemptResize(QgsLayoutSize(168, 14, QgsUnitTypes.LayoutMillimeters))
    lay.addLayoutItem(t)
    c = QgsLayoutItemLabel(lay)
    c.setText('Your Name\nYour Section\nLab 3\n\n' + note +
              '\n\nBasemap: Google Satellite\nData: your GPS survey\nProjection: EPSG:26912')
    c.setFont(QFont('Helvetica', 11))
    c.attemptMove(QgsLayoutPoint(190, 110, QgsUnitTypes.LayoutMillimeters))
    c.attemptResize(QgsLayoutSize(95, 70, QgsUnitTypes.LayoutMillimeters))
    lay.addLayoutItem(c)
    p.layoutManager().addLayout(lay)
    return lay


try:
    main()
except Exception:
    log('EXCEPTION\n' + traceback.format_exc())
finish()
