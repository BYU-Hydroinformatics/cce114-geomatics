# Week 3 hands-on main-window and Print Layout screenshots, captured by QGIS 3.44 grabbing itself.
#
# Runs INSIDE QGIS at launch, from a terminal, one shot per process:
#
#   for s in map-single-symbols map-graduated map-labels attribute-table \
#            layout-designer layout-export; do
#     WEEK03_DATA=~/week03work WEEK03_OUT=docs/handson/images SHOT=$s \
#       /Applications/QGIS.app/Contents/MacOS/QGIS --nologo --code tools/qgis_week03_window_shots.py
#   done
#
# Companion to tools/qgis_week03_dialog_shots.py, which does the headless dialog captures.
# Field names are the real ones in "United States Shapefiles.zip" (states: STATE_NAME,
# SUB_REGION, POP1990; cities: CITY_NAME, POP1990; roads: ADMN_CLASS), checked against the .dbf.
# The data is EPSG:4326 and is left that way, because that is what students see when they load it.
#
# Gotchas, inherited from tools/qgis_lab02_window_shots.py and all still live:
#   * QGIS execs --code files, so __file__ is undefined; paths come from the environment.
#   * Adding layers resets the canvas CRS to the project default and queues a deferred
#     full-extent zoom; both land after the first event-loop spin, so settle, set the extent,
#     settle, and set it again before grabbing.
#   * Quitting with iface.actionExit() pops "Do you want to save?" and hangs unless the project
#     has just been written, so write it and clear the dirty flag first.
#   * QWidget.grab() omits the macOS title bar.
#   * QGIS cannot read or write under ~/Desktop, ~/Documents or ~/Downloads on macOS.
import os, time, json, traceback
from qgis.core import (QgsProject, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsRectangle,
                       QgsStyle, QgsMarkerSymbol, QgsLineSymbol, QgsFillSymbol,
                       QgsSingleSymbolRenderer, QgsGraduatedSymbolRenderer,
                       QgsCategorizedSymbolRenderer, QgsRendererCategory,
                       QgsClassificationJenks, QgsRendererRangeLabelFormat,
                       QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings,
                       QgsVectorLayerSimpleLabeling, QgsPrintLayout, QgsLayoutItemMap,
                       QgsLayoutItemLabel, QgsLayoutItemLegend, QgsLayoutPoint, QgsLayoutSize,
                       QgsLayoutItemScaleBar, QgsLayoutItemPicture, QgsLayoutExporter,
                       QgsUnitTypes, QgsApplication, QgsFeatureRequest)
from qgis.PyQt.QtCore import QTimer, Qt, QRectF
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtWidgets import QApplication, QWidget, QDockWidget
from qgis.utils import iface

DATA = os.path.expanduser(os.environ['WEEK03_DATA'])
OUT = os.path.abspath(os.environ['WEEK03_OUT'])
SHOT = os.environ['SHOT']
SHP = os.path.join(DATA, 'United States', 'Shapefiles')
os.makedirs(OUT, exist_ok=True)

# The lower 48 in lat/long. states.shp has no Alaska or Hawaii, so this IS its full extent.
LOWER48 = QgsRectangle(-127.0, 23.0, -65.5, 50.5)
CRS = QgsCoordinateReferenceSystem('EPSG:4326')

def log(*a):
    print('[week03]', *a, flush=True)

def settle(seconds):
    end = time.time() + seconds
    while time.time() < end:
        QApplication.processEvents()
        time.sleep(0.05)

def load(fn, name):
    l = QgsVectorLayer(os.path.join(SHP, fn), name, 'ogr')
    assert l.isValid(), 'invalid layer: ' + fn
    QgsProject.instance().addMapLayer(l)
    return l

def style_single(states, cities, roads):
    states.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {'color': '#dbe7d4', 'outline_color': '#6f7d68', 'outline_width': '0.26'})))
    roads.setRenderer(QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
        {'color': '#2f6fa8', 'width': '0.6'})))
    cities.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
        {'name': 'circle', 'color': '#c0392b', 'outline_color': '#ffffff',
         'outline_width': '0.2', 'size': '2'})))

def style_graduated(states):
    ramp = QgsStyle.defaultStyle().colorRamp('Blues')
    r = QgsGraduatedSymbolRenderer('POP1990')
    m = QgsClassificationJenks(); m.setLabelPrecision(0); m.setLabelTrimTrailingZeroes(True)
    r.setClassificationMethod(m)
    r.setSourceSymbol(QgsFillSymbol.createSimple(
        {'color': '#cccccc', 'outline_color': '#ffffff', 'outline_width': '0.2'}))
    r.updateClasses(states, 5)
    r.setLabelFormat(QgsRendererRangeLabelFormat('%1 - %2', 0), True)
    r.updateColorRamp(ramp.clone())
    states.setRenderer(r)

def style_cities_by_size(cities):
    r = QgsGraduatedSymbolRenderer('POP1990')
    m = QgsClassificationJenks(); m.setLabelPrecision(0); m.setLabelTrimTrailingZeroes(True)
    r.setClassificationMethod(m)
    r.setSourceSymbol(QgsMarkerSymbol.createSimple(
        {'name': 'circle', 'color': '#c0392b', 'outline_color': '#ffffff',
         'outline_width': '0.2', 'size': '2'}))
    r.setGraduatedMethod(QgsGraduatedSymbolRenderer.GraduatedSize)
    r.updateClasses(cities, 5)
    r.setSymbolSizes(1.0, 6.0)
    cities.setRenderer(r)

def style_roads_categorized(roads):
    colors = {'Interstate': '#d94801', 'US Highway': '#fd8d3c', 'State Highway': '#fdd0a2'}
    cats = [QgsRendererCategory(k, QgsLineSymbol.createSimple(
        {'color': v, 'width': '0.55' if k == 'Interstate' else '0.35'}), k)
        for k, v in colors.items()]
    roads.setRenderer(QgsCategorizedSymbolRenderer('ADMN_CLASS', cats))

def label(layer, expr, size, is_expression=False):
    ls = QgsPalLayerSettings()
    ls.fieldName = expr
    ls.isExpression = is_expression
    ls.enabled = True
    tf = QgsTextFormat()
    tf.setFont(QFont('Helvetica', size))
    tf.setSize(size)
    buf = QgsTextBufferSettings(); buf.setEnabled(True); buf.setSize(1.0)
    buf.setColor(QColor('white')); tf.setBuffer(buf)
    ls.setFormat(tf)
    layer.setLabeling(QgsVectorLayerSimpleLabeling(ls))
    layer.setLabelsEnabled(True)

def zoom(extent=LOWER48, seconds=8):
    # QGIS opens at whatever size it last had, which on a fresh profile is short and wide and
    # letterboxes the map. Fix the window size so every figure has the same frame.
    mw = iface.mainWindow()
    # Browser and Processing Toolbox between them take well over half the width and nothing in
    # this session uses either. Hiding them lets the canvas approach the lower 48's own 2.2:1
    # shape, so the map fills the figure instead of floating in padding. The Layers panel stays:
    # these figures are partly about it.
    for dock in mw.findChildren(QDockWidget):
        if dock.windowTitle().strip().lower() not in ('layers',):
            dock.hide()
    mw.resize(1900, 820)
    settle(2)
    c = iface.mapCanvas()
    settle(3)
    QgsProject.instance().setCrs(CRS)
    c.setDestinationCrs(CRS)
    settle(1)
    # setExtent() grows the requested rectangle to the canvas aspect ratio, so a canvas that is
    # taller than the lower 48 pads with empty ocean. Grow the rectangle to the canvas aspect
    # ourselves first, so the padding is split evenly and stays small.
    cw, ch = c.width(), c.height()
    want = QgsRectangle(extent)
    if cw and ch:
        target = cw / float(ch)
        have = want.width() / want.height()
        if have < target:
            pad = (want.height() * target - want.width()) / 2.0
            want.setXMinimum(want.xMinimum() - pad); want.setXMaximum(want.xMaximum() + pad)
        else:
            pad = (want.width() / target - want.height()) / 2.0
            want.setYMinimum(want.yMinimum() - pad); want.setYMaximum(want.yMaximum() + pad)
    c.setExtent(want); c.refresh()
    settle(seconds)
    c.setExtent(want); c.refresh()
    settle(4)
    log('canvas', cw, 'x', ch, 'crs', c.mapSettings().destinationCrs().authid(),
        'extent', c.extent().toString(1))

def grab(widget, name):
    QApplication.processEvents()
    pm = widget.grab()
    path = os.path.join(OUT, 'w3-' + name + '.png')
    pm.save(path)
    log('saved', name, pm.width(), 'x', pm.height())

def make_layout(p, title):
    """A layout carrying the six required elements, laid out so nothing overlaps.

    The page is sized to the map rather than the other way round: an A4 landscape default leaves
    roughly a third of the sheet empty under a lower-48 map, and the scale bar then lands on top
    of the credit line.
    """
    lay = QgsPrintLayout(p)
    lay.initializeDefaults()
    lay.setName('Week 3')

    PW, PH = 297.0, 152.0           # mm; chosen so the map fills the sheet
    page = lay.pageCollection().page(0)
    page.setPageSize(QgsLayoutSize(PW, PH, QgsUnitTypes.LayoutMillimeters))

    MAP_X, MAP_Y, MAP_W = 10.0, 22.0, 200.0
    MAP_H = MAP_W * (LOWER48.height() / LOWER48.width())   # keep the map's own aspect

    m = QgsLayoutItemMap(lay)
    lay.addLayoutItem(m)
    # attemptMove + attemptResize leave a map item at 0 x 0 here, which renders nothing and
    # takes its linked scale bar down with it. attemptSetSceneRect sets both at once and sticks.
    m.attemptSetSceneRect(QRectF(MAP_X, MAP_Y, MAP_W, MAP_H))
    m.setCrs(CRS)
    m.setExtent(LOWER48)
    m.setFrameEnabled(True)
    m.refresh()

    t = QgsLayoutItemLabel(lay)
    lay.addLayoutItem(t)
    t.setText(title)
    f = QFont('Helvetica', 22); f.setBold(True)
    t.setFont(f)
    t.attemptMove(QgsLayoutPoint(MAP_X, 6, QgsUnitTypes.LayoutMillimeters))
    t.attemptResize(QgsLayoutSize(PW - 2 * MAP_X, 12, QgsUnitTypes.LayoutMillimeters))

    leg = QgsLayoutItemLegend(lay)
    leg.setLinkedMap(m)
    # Section 6 step 2 is explicitly about unticking Auto update before renaming entries.
    leg.setAutoUpdateModel(False)
    leg.setTitle('Legend')
    lay.addLayoutItem(leg)
    leg.attemptMove(QgsLayoutPoint(MAP_X + MAP_W + 4, MAP_Y, QgsUnitTypes.LayoutMillimeters))
    leg.adjustBoxSize()

    sb = QgsLayoutItemScaleBar(lay)
    sb.setLinkedMap(m)
    sb.setStyle('Single Box')
    # Default units come out as metres, so a continental map reads "1,000,000 m".
    sb.setUnits(QgsUnitTypes.DistanceKilometers)
    sb.setUnitLabel('km')
    sb.setUnitsPerSegment(500)
    sb.setNumberOfSegments(2)
    sb.setNumberOfSegmentsLeft(0)
    sb.update()
    lay.addLayoutItem(sb)
    sb.attemptMove(QgsLayoutPoint(MAP_X, MAP_Y + MAP_H + 6, QgsUnitTypes.LayoutMillimeters))

    na = QgsLayoutItemPicture(lay)
    lay.addLayoutItem(na)
    arrow = None
    for root in QgsApplication.svgPaths():
        for cand in ('arrows/NorthArrow_02.svg', 'arrows/NorthArrow_01.svg'):
            q = os.path.join(root, cand)
            if os.path.exists(q):
                arrow = q; break
        if arrow:
            break
    if arrow:
        na.setPicturePath(arrow)
    na.attemptResize(QgsLayoutSize(13, 13, QgsUnitTypes.LayoutMillimeters))
    na.attemptMove(QgsLayoutPoint(MAP_X + MAP_W - 16, MAP_Y + MAP_H + 4,
                                  QgsUnitTypes.LayoutMillimeters))

    cred = QgsLayoutItemLabel(lay)
    lay.addLayoutItem(cred)
    cred.setText('Author: CCE 114 student   |   Data: United States Shapefiles (1990 census)   '
                 '|   Projection: WGS 84 (EPSG:4326)')
    cred.setFont(QFont('Helvetica', 7))
    # Below the scale bar, not on it.
    cred.attemptMove(QgsLayoutPoint(MAP_X, PH - 10, QgsUnitTypes.LayoutMillimeters))
    cred.attemptResize(QgsLayoutSize(PW - 2 * MAP_X, 6, QgsUnitTypes.LayoutMillimeters))
    return lay

def finish():
    p = QgsProject.instance()
    # Written only so actionExit() does not stop on the unsaved-project prompt.
    p.write(os.path.join(DATA, 'week03-shots.qgz'))
    p.setDirty(False)
    QTimer.singleShot(400, lambda: iface.actionExit().trigger())

def main():
    try:
        p = QgsProject.instance()
        p.setCrs(CRS)
        states = load('states.shp', 'states')
        cities = load('cities.shp', 'cities')
        roads = load('roads.shp', 'roads')
        style_single(states, cities, roads)

        if SHOT == 'map-single-symbols':
            zoom()
            grab(iface.mainWindow(), 'map-single-symbols')

        elif SHOT == 'map-graduated':
            style_graduated(states)
            style_roads_categorized(roads)
            style_cities_by_size(cities)
            zoom()
            grab(iface.mainWindow(), 'map-graduated')

        elif SHOT == 'map-labels':
            style_graduated(states)
            style_cities_by_size(cities)
            label(states, 'STATE_NAME', 8)
            label(cities, 'CASE WHEN "POP1990" > 500000 THEN "CITY_NAME" END', 9,
                  is_expression=True)
            zoom(seconds=10)
            grab(iface.mainWindow(), 'map-labels')

        elif SHOT == 'attribute-table':
            zoom(seconds=4)
            # Select the eight cities over a million so the map highlight and the table
            # selection are the same eight rows section 5 talks about.
            ids = [f.id() for f in cities.getFeatures(
                QgsFeatureRequest().setFilterExpression('"POP1990" > 1000000'))]
            cities.selectByIds(ids)
            log('selected', len(ids), 'cities over 1,000,000')
            # Section 5 step 1 is "click a column header to sort", and step 2 is the selection.
            # In file order the table opens on small Washington towns and the selected rows are
            # thousands of rows down, so the figure would show neither. Sort POP1990 descending
            # and the eight selected cities are the top eight rows, highlighted.
            cfg = cities.attributeTableConfig()
            cfg.setSortExpression('"POP1990"')
            cfg.setSortOrder(Qt.DescendingOrder)
            cities.setAttributeTableConfig(cfg)
            d = iface.showAttributeTable(cities)
            settle(4)
            w = d.window()
            w.resize(1400, 760)
            settle(3)
            grab(w, 'attribute-table')

        elif SHOT in ('layout-designer', 'layout-export'):
            style_graduated(states)
            style_roads_categorized(roads)
            style_cities_by_size(cities)
            label(states, 'STATE_NAME', 8)
            zoom(seconds=8)
            lay = make_layout(p, 'Population by State, 1990')
            p.layoutManager().addLayout(lay)
            settle(3)
            if SHOT == 'layout-export':
                exp = QgsLayoutExporter(lay)
                s = QgsLayoutExporter.ImageExportSettings()
                s.dpi = 150
                res = exp.exportToImage(os.path.join(OUT, 'w3-layout-export.png'), s)
                log('export result', res)
            else:
                d = iface.openLayoutDesigner(lay)
                win = d.window()
                win.resize(1500, 1020)
                win.show()
                settle(8)
                for dock in win.findChildren(QDockWidget):
                    if dock.windowTitle().strip().lower() == 'items':
                        dock.raise_(); break
                lay.undoStack().stack().clear()
                settle(3)
                grab(win, 'layout-designer')
        else:
            raise SystemExit('unknown SHOT: ' + SHOT)
    except Exception:
        traceback.print_exc()
    finish()

QTimer.singleShot(2500, main)
