# Day 22 Walmart deck map figures (slides/day-22/images/), rendered by QGIS 3.44 LTR from its
# bundled Python as Print Layout exports, with no QGIS window and no screen-recording permission.
# They replace ArcMap-era captures: ws-census-blocks showed the 2010 blocks, and Lab 11 now has
# students download UGRC's "Census 2020 Blocks"; ws-current-walmarts showed a store list that has
# since grown. SHOT picks one of: census-blocks, utah-county, current-walmarts (default: all).
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   DAY22_GPKG=<work dir>/ws.gpkg DAY22_OUT=<out dir> \
#     /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_day22_shots.py
#
# ws.gpkg is built with the ogr2ogr that ships in /Applications/QGIS.app/Contents/MacOS:
#   PG="PG:host=opensgid.agrc.utah.gov port=5432 dbname=opensgid user=agrc password=agrc sslmode=disable"
#   ogr2ogr -f GPKG ws.gpkg "$PG" -nln utah_county \
#     -sql "select name, shape from boundaries.county_boundaries where name='UTAH'"
#   ogr2ogr -f GPKG -update ws.gpkg "$PG" -nln counties \
#     -sql "select name, shape from boundaries.county_boundaries"
#   ogr2ogr -f GPKG -update ws.gpkg "$PG" -nln census_blocks_2020 \
#     -sql "select * from demographic.census_blocks_2020 where countyfp20='049'"
#   ogr2ogr -f GPKG -update ws.gpkg "<Walmart FeatureServer/0>/query?where=1%3D1&outFields=*&f=json" \
#     -nln walmarts_all -t_srs EPSG:26912
#   ogr2ogr -f GPKG -update ws.gpkg ws.gpkg -nln walmarts_utah_county -dialect sqlite \
#     -sql "select w.* from walmarts_all w, utah_county c where st_intersects(w.geom, c.shape)"
#   ENV="st_makeenvelope(380000,4385000,530000,4510000,26912)"   # Utah County and surroundings
#   ogr2ogr -f GPKG -update ws.gpkg "$PG" -nln udot_routes \
#     -sql "select * from transportation.udot_routes_alrs where shape && $ENV"
#   ogr2ogr -f GPKG -update ws.gpkg "$PG" -nln roads \
#     -sql "select xid, cartocode, fullname, dot_hwynam, dot_rtname, shape from transportation.roads where shape && $ENV"
#   ogr2ogr -f GPKG -update ws.gpkg "$PG" -nln census_blocks_2020_area \
#     -sql "select * from demographic.census_blocks_2020 where shape && $ENV"
# buffer-i15 and final-map also need DAY22_LAB11, the UtahCounty.gpkg that
# tools/lab11_run_analysis.py writes from ws.gpkg; final-map fetches Google Satellite tiles.
# Open SGID is UGRC's PostGIS mirror of the same SGID layer Lab 11 links to; countyfp20 '049'
# gives 10,092 blocks summing to 659,399 people, the check figure the lab quotes. The Walmart
# layer is the Walmart Open Data Hub service the lab links to ("Walmart Store Status Public
# Data", services1.arcgis.com/WyIdBuoLrhwRHOSA/.../STORE_STATUS_PUBLIC_VIEW). Sam's Club is left
# out, as Lab 11 step 20 has students do. Keep both directories outside ~/Desktop, ~/Documents
# and ~/Downloads: QGIS cannot read or write there on macOS.
import os
import sys
from qgis.core import (QgsApplication, QgsProject, QgsVectorLayer, QgsCoordinateReferenceSystem,
                       QgsFillSymbol, QgsMarkerSymbol, QgsRuleBasedRenderer, QgsSingleSymbolRenderer,
                       QgsPrintLayout, QgsLayoutItem, QgsLayoutItemMap, QgsLayoutItemLegend,
                       QgsLayoutItemScaleBar, QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes,
                       QgsLayoutExporter, QgsRectangle, QgsLegendStyle, QgsTextFormat,
                       QgsScaleBarSettings, QgsPalLayerSettings, QgsVectorLayerSimpleLabeling,
                       QgsTextBufferSettings, QgsLayoutItemLabel, QgsLineSymbol, QgsRasterLayer,
                       QgsLayoutItemMapOverview)
from qgis.PyQt.QtCore import QRectF, Qt
from qgis.PyQt.QtGui import QColor, QFont

GPKG = os.environ['DAY22_GPKG']
OUT = os.environ['DAY22_OUT']
LAB11 = os.environ.get('DAY22_LAB11', '')  # UtahCounty.gpkg from tools/lab11_run_analysis.py
SHOTS = [os.environ['SHOT']] if os.environ.get('SHOT') else ['census-blocks', 'utah-county',
                                                              'current-walmarts', 'udot-routes',
                                                              'buffer-i15', 'final-map']
# Close-ups on the final map: the two biggest clusters of candidate blocks, EPSG:26912 centers.
# Checked against UGRC municipal boundaries: 319 of the 332 blocks in the first are in Orem, 162 of
# 164 in the second are in Eagle Mountain.
INSETS = [('Orem', (442000, 4462000)), ('Eagle Mountain', (416500, 4467000))]
INSET_HALF = 2600
os.makedirs(OUT, exist_ok=True)

QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], False)
app.initQgis()

project = QgsProject.instance()
crs = QgsCoordinateReferenceSystem('EPSG:26912')
project.setCrs(crs)

# Page roughly the shape of Utah County; 254 mm at 200 dpi = 2000 px wide.
W, H = 254.0, 200.0
FMT = QgsTextFormat()
FMT.setFont(QFont('Helvetica', 13))
FMT.setSize(13)


def gpkg_layer(table, name):
    lyr = QgsVectorLayer(f'{GPKG}|layername={table}', name, 'ogr')
    assert lyr.isValid(), table
    project.addMapLayer(lyr)
    return lyr


def fill(**props):
    return QgsSingleSymbolRenderer(QgsFillSymbol.createSimple({k: str(v) for k, v in props.items()}))


counties = gpkg_layer('counties', 'Utah counties')
county = gpkg_layer('utah_county', 'Utah County')
blocks = gpkg_layer('census_blocks_2020', 'Census 2020 Blocks')
stores = gpkg_layer('walmarts_utah_county', 'Existing Walmart stores')
stores.setSubsetString("businessunit_banner_description <> 'Sam''s Club'")
print('stores', sum(1 for _ in stores.getFeatures()), flush=True)

# Light fill, thin gray outlines; water-only blocks (Utah Lake) in pale blue so the lake reads.
outline = '#8a8a8a'
land = QgsFillSymbol.createSimple({'color': '#f6f2e4', 'outline_color': outline, 'outline_width': '0.07'})
water = QgsFillSymbol.createSimple({'color': '#cfe2f1', 'outline_color': outline, 'outline_width': '0.07'})
root = QgsRuleBasedRenderer.Rule(None)
root.appendChild(QgsRuleBasedRenderer.Rule(land, filterExp='"aland20" > 0', label='Land block'))
root.appendChild(QgsRuleBasedRenderer.Rule(water, filterExp='"aland20" = 0',
                                           label='Water block (Utah Lake)'))
blocks.setRenderer(QgsRuleBasedRenderer(root))

stores.setRenderer(QgsSingleSymbolRenderer(QgsMarkerSymbol.createSimple(
    {'name': 'circle', 'color': '#f07f13', 'outline_color': '#202020', 'outline_width': '0.35',
     'size': '3.6'})))

# Neighboring counties in light gray with their names, for context.
counties.setRenderer(fill(color='#fbfbfb', outline_color='#9a9a9a', outline_width=0.35))
pal = QgsPalLayerSettings()
# Utah County itself goes unlabeled: the slide title names it, and the label would sit on a store.
pal.fieldName = "CASE WHEN \"name\" <> 'UTAH' THEN title(lower(\"name\")) END"
pal.isExpression = True
pal.fitInPolygonOnly = True  # otherwise Juab's label lands in Utah County's southwest tail
lfmt = QgsTextFormat()
lfmt.setFont(QFont('Helvetica', 12))
lfmt.setSize(12)
lfmt.setColor(QColor('#707070'))
buf = QgsTextBufferSettings()
buf.setEnabled(True)
buf.setSize(1)
lfmt.setBuffer(buf)
pal.setFormat(lfmt)
counties.setLabeling(QgsVectorLayerSimpleLabeling(pal))
counties.setLabelsEnabled(True)


def fit(ext, w, h, margin=0):
    """Grow a rectangle by margin, then to the w:h aspect, so it is centered with even padding."""
    ext = QgsRectangle(ext)
    ext.grow(margin)
    if ext.width() / ext.height() < w / h:
        pad = (ext.height() * w / h - ext.width()) / 2
        return QgsRectangle(ext.xMinimum() - pad, ext.yMinimum(), ext.xMaximum() + pad, ext.yMaximum())
    pad = (ext.width() * h / w - ext.height()) / 2
    return QgsRectangle(ext.xMinimum(), ext.yMinimum() - pad, ext.xMaximum(), ext.yMaximum() + pad)


def new_layout(w, h):
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.pageCollection().page(0).setPageSize(QgsLayoutSize(w, h, QgsUnitTypes.LayoutMillimeters))
    return layout


def add_map(layout, x, y, w, h, layers, ext, frame=False):
    m = QgsLayoutItemMap(layout)
    layout.addLayoutItem(m)
    m.attemptSetSceneRect(QRectF(x, y, w, h))  # attemptMove+attemptResize leaves a map at 0x0
    m.setFrameEnabled(frame)
    m.setCrs(crs)
    m.setLayers(layers)
    m.setExtent(fit(ext, w, h))
    return m


def add_legend(layout, m, layers, x, y):
    # Anchored by the upper-right corner: a legend's size is not settled until it is drawn.
    legend = QgsLayoutItemLegend(layout)
    layout.addLayoutItem(legend)
    legend.setLinkedMap(m)
    legend.setAutoUpdateModel(False)
    legend.setTitle('')
    tree = legend.model().rootGroup()
    tree.removeAllChildren()
    for lyr in layers:
        tree.addLayer(lyr)
    for style in (QgsLegendStyle.SymbolLabel, QgsLegendStyle.Subgroup, QgsLegendStyle.Group):
        legend.rstyle(style).setTextFormat(FMT)
    legend.setSymbolWidth(7)
    legend.setSymbolHeight(5)
    legend.setBackgroundEnabled(True)
    legend.setBackgroundColor(QColor(255, 255, 255, 235))
    legend.setFrameEnabled(True)
    legend.adjustBoxSize()
    legend.setReferencePoint(QgsLayoutItem.UpperRight)
    legend.attemptMove(QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters))
    return legend


def add_scalebar(layout, m, x, y, per_segment=5, fmt=FMT):
    bar = QgsLayoutItemScaleBar(layout)
    layout.addLayoutItem(bar)
    bar.setLinkedMap(m)
    bar.setStyle('Single Box')
    bar.setUnits(QgsUnitTypes.DistanceMiles)
    bar.setUnitLabel('mi')
    bar.setUnitsPerSegment(per_segment)
    bar.setSegmentSizeMode(QgsScaleBarSettings.SegmentSizeFixed)
    bar.setNumberOfSegments(2)
    bar.setNumberOfSegmentsLeft(0)
    bar.setTextFormat(fmt)
    bar.setBackgroundEnabled(True)
    bar.setBackgroundColor(QColor(255, 255, 255, 235))
    bar.update()
    bar.setReferencePoint(QgsLayoutItem.UpperRight)
    bar.attemptMove(QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters))
    return bar


def add_label(layout, text, x, y, w, h, size=15, bold=False):
    lab = QgsLayoutItemLabel(layout)
    layout.addLayoutItem(lab)
    lab.setText(text)
    f = QgsTextFormat()
    font = QFont('Helvetica', size)
    font.setBold(bold)
    f.setFont(font)
    f.setSize(size)
    lab.setTextFormat(f)
    lab.setHAlign(Qt.AlignHCenter)
    lab.attemptSetSceneRect(QRectF(x, y, w, h))
    return lab


def export(layout, name, dpi=200):
    png = os.path.join(OUT, f'ws-{name}.png')
    settings = QgsLayoutExporter.ImageExportSettings()
    settings.dpi = dpi
    print('export', name, QgsLayoutExporter(layout).exportToImage(png, settings), flush=True)


def render(name, layers, legend_layers, margin, bar_y):
    """One map of Utah County filling a W x H page, legend and scale bar at the top right."""
    layout = new_layout(W, H)
    ext = QgsRectangle(county.extent())
    ext.grow(margin)
    m = add_map(layout, 0, 0, W, H, layers, ext)
    # Top right is outside Utah County (Wasatch County side), so nothing important is covered.
    if legend_layers:
        add_legend(layout, m, legend_layers, W - 4, 4)
    add_scalebar(layout, m, W - 4, bar_y)
    export(layout, name)


def lab11_layer(table, name):
    lyr = QgsVectorLayer(f'{LAB11}|layername={table}', name, 'ogr')
    assert lyr.isValid(), table
    project.addMapLayer(lyr)
    return lyr


def line(color, width, **extra):
    return QgsSingleSymbolRenderer(QgsLineSymbol.createSimple(
        dict({'line_color': color, 'line_width': str(width)}, **{k: str(v) for k, v in extra.items()})))


def run_alg(alg, params):
    global processing
    if 'processing' not in globals():
        sys.path.append('/Applications/QGIS.app/Contents/Resources/qgis/python/plugins')
        import processing
        from processing.core.Processing import Processing
        Processing.initialize()
    return processing.run(alg, dict(params, OUTPUT='memory:'))['OUTPUT']


def shot_udot_routes():
    # Every UDOT route (mainlines and ramps) in and around the county, before any narrowing.
    routes = gpkg_layer('udot_routes', 'UDOT routes')
    routes.setRenderer(line('#6a2c91', 0.35))
    county.setRenderer(highlight)
    render('udot-routes', [routes, county, counties], [], 9000, 6)


def shot_buffer_i15():
    # Lab 11's 2-mile buffer on I-15 inside Utah County, with Dissolve result off and then on.
    roads = lab11_layer('roads_clipped', 'Utah Roads, clipped')
    i15 = run_alg('native:extractbyexpression', {'INPUT': roads, 'EXPRESSION': '"dot_hwynam" = \'I-15\''})
    print('I-15 features', i15.featureCount(), flush=True)
    i15.setName('I-15')
    i15.setRenderer(line('#b8412f', 0.6))
    panels = []
    for dissolve in (False, True):
        b = run_alg('native:buffer', {'INPUT': i15, 'DISTANCE': 3218.69, 'SEGMENTS': 12, 'END_CAP_STYLE': 0,
                                      'JOIN_STYLE': 0, 'MITER_LIMIT': 2, 'DISSOLVE': dissolve})
        print('buffer dissolve', dissolve, b.featureCount(), flush=True)
        b.setRenderer(fill(color='92,190,172,70', outline_color='#2f6f64', outline_width=0.12))
        project.addMapLayer(b)
        panels.append(b)
    project.addMapLayer(i15)
    county.setRenderer(fill(color='#f6f2e4', outline_color='#3a3a3a', outline_width=0.5))

    pw, ph, gap, top = 125.0, 170.0, 4.0, 14.0
    layout = new_layout(2 * pw + gap, ph + top)
    ext = QgsRectangle(panels[1].extent())
    ext.grow(1500)
    titles = ('Dissolve result: unchecked', 'Dissolve result: checked')
    for i, (b, title) in enumerate(zip(panels, titles)):
        x = i * (pw + gap)
        add_label(layout, title, x, 2, pw, 10, size=16, bold=True)
        m = add_map(layout, x, top, pw, ph, [i15, b, county, counties], ext, frame=True)
    add_scalebar(layout, m, 2 * pw + gap - 3, top + 3)
    export(layout, 'buffer-i15')


def shot_final_map():
    # The candidate set from running Lab 11 as written (tools/lab11_run_analysis.py), laid out the
    # way the lab's map asks: the whole county, plus close-ups of the two biggest clusters.
    major = lab11_layer('MajorRoads', 'Major roads (CARTOCODE 1-5)')
    current = lab11_layer('CurrentLocations', 'Existing Walmart stores')
    cand = lab11_layer('PotentialCustomers', 'Requirements met')
    major.setRenderer(line('#7d7d7d', 0.25))
    current.setRenderer(stores.renderer().clone())
    cand.setRenderer(fill(color='#d81b8c', outline_color='#d81b8c', outline_width=0.05))
    county.setRenderer(fill(style='no', outline_color='#3a3a3a', outline_width=0.5))
    sat = QgsRasterLayer('type=xyz&url=https://mt1.google.com/vt/lyrs%3Ds%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D'
                         '&zmax=19&zmin=0', 'Google Satellite', 'wms')
    assert sat.isValid()
    project.addMapLayer(sat)
    inset_cand = cand.clone()
    inset_cand.setName('Requirements met')
    inset_cand.setRenderer(fill(color='216,27,140,120', outline_color='#ff4fc0', outline_width=0.2))
    project.addMapLayer(inset_cand)

    pw, ph = 190.0, 244.0
    layout = new_layout(pw, ph)
    add_label(layout, 'Possible Walmart locations in Utah County', 0, 3, pw, 12, size=20, bold=True)
    main_ext = QgsRectangle(county.extent())
    main_ext.grow(1500)
    main = add_map(layout, 5, 17, pw - 10, 140, [current, cand, major, county, blocks], main_ext,
                   frame=True)
    add_legend(layout, main, [cand, current, major], pw - 7, 20)
    add_scalebar(layout, main, pw - 7, 140)

    iw, ih, iy = 88.0, 66.0, 168.0
    for i, (title, center) in enumerate(INSETS):
        x = 5 + i * (iw + 4)
        add_label(layout, title, x, iy - 9, iw, 8, size=14, bold=True)
        cx, cy = center
        m = add_map(layout, x, iy, iw, ih, [current, inset_cand, sat],
                    QgsRectangle(cx - INSET_HALF, cy - INSET_HALF, cx + INSET_HALF, cy + INSET_HALF),
                    frame=True)
        small = QgsTextFormat()
        small.setFont(QFont('Helvetica', 11))
        small.setSize(11)
        add_scalebar(layout, m, x + iw - 2, iy + ih - 13, per_segment=0.5, fmt=small)
        # Locator box for this inset on the county map.
        ov = QgsLayoutItemMapOverview(title, main)
        main.overviews().addOverview(ov)
        ov.setLinkedMap(m)
        ov.setFrameSymbol(QgsFillSymbol.createSimple(
            {'style': 'no', 'outline_color': '#111111', 'outline_width': '0.5'}))
    credit = add_label(layout, 'Inset imagery: Google Satellite, as in Lab 11 step 2. '
                       'Data: UGRC Census 2020 Blocks and Utah Roads; Walmart Open Data.',
                       5, iy + ih + 1.5, pw - 10, 6, size=9)
    export(layout, 'final-map')


highlight = fill(color='#f6f2e4', outline_color='#3a3a3a', outline_width=0.6)
no_fill = fill(style='no', outline_color='#3a3a3a', outline_width=0.5)
for shot in SHOTS:
    if shot == 'census-blocks':
        county.setRenderer(no_fill)
        render(shot, [stores, county, blocks], [stores, blocks], 2500, 46)
    elif shot == 'utah-county':
        # The whole county, everything still in play, among its statewide neighbors.
        county.setRenderer(highlight)
        render(shot, [county, counties], [], 9000, 6)
    elif shot == 'current-walmarts':
        county.setRenderer(highlight)
        render(shot, [stores, county, counties], [], 9000, 6)
    elif shot == 'udot-routes':
        shot_udot_routes()
    elif shot == 'buffer-i15':
        shot_buffer_i15()
    elif shot == 'final-map':
        shot_final_map()

# app.exitQgis() segfaults on teardown; everything is written by now.
os._exit(0)
