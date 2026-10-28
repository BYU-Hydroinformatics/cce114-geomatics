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
# Open SGID is UGRC's PostGIS mirror of the same SGID layer Lab 11 links to; countyfp20 '049'
# gives 10,092 blocks summing to 659,399 people, the check figure the lab quotes. The Walmart
# layer is the Walmart Open Data Hub service the lab links to ("Walmart Store Status Public
# Data", services1.arcgis.com/WyIdBuoLrhwRHOSA/.../STORE_STATUS_PUBLIC_VIEW). Sam's Club is left
# out, as Lab 11 step 20 has students do. Keep both directories outside ~/Desktop, ~/Documents
# and ~/Downloads: QGIS cannot read or write there on macOS.
import os
from qgis.core import (QgsApplication, QgsProject, QgsVectorLayer, QgsCoordinateReferenceSystem,
                       QgsFillSymbol, QgsMarkerSymbol, QgsRuleBasedRenderer, QgsSingleSymbolRenderer,
                       QgsPrintLayout, QgsLayoutItem, QgsLayoutItemMap, QgsLayoutItemLegend,
                       QgsLayoutItemScaleBar, QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes,
                       QgsLayoutExporter, QgsRectangle, QgsLegendStyle, QgsTextFormat,
                       QgsScaleBarSettings, QgsPalLayerSettings, QgsVectorLayerSimpleLabeling,
                       QgsTextBufferSettings)
from qgis.PyQt.QtCore import QRectF
from qgis.PyQt.QtGui import QColor, QFont

GPKG = os.environ['DAY22_GPKG']
OUT = os.environ['DAY22_OUT']
SHOTS = [os.environ['SHOT']] if os.environ.get('SHOT') else ['census-blocks', 'utah-county',
                                                              'current-walmarts']
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


def county_extent(margin):
    ext = county.extent()
    ext.grow(margin)
    # Match the page aspect so the county sits centered with even margins.
    aspect = W / H
    if ext.width() / ext.height() < aspect:
        pad = (ext.height() * aspect - ext.width()) / 2
        return QgsRectangle(ext.xMinimum() - pad, ext.yMinimum(), ext.xMaximum() + pad, ext.yMaximum())
    pad = (ext.width() / aspect - ext.height()) / 2
    return QgsRectangle(ext.xMinimum(), ext.yMinimum() - pad, ext.xMaximum(), ext.yMaximum() + pad)


def render(name, layers, legend_layers, margin, bar_y):
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.pageCollection().page(0).setPageSize(QgsLayoutSize(W, H, QgsUnitTypes.LayoutMillimeters))

    m = QgsLayoutItemMap(layout)
    layout.addLayoutItem(m)
    m.attemptSetSceneRect(QRectF(0, 0, W, H))  # attemptMove+attemptResize leaves a map at 0x0
    m.setFrameEnabled(False)
    m.setCrs(crs)
    m.setLayers(layers)
    m.setExtent(county_extent(margin))

    # Top right is outside Utah County (Wasatch County side), so nothing important is covered.
    # Anchor by the upper-right corner: a legend's size is not settled until it is drawn.
    if legend_layers:
        legend = QgsLayoutItemLegend(layout)
        layout.addLayoutItem(legend)
        legend.setLinkedMap(m)
        legend.setAutoUpdateModel(False)
        legend.setTitle('')
        tree = legend.model().rootGroup()
        tree.removeAllChildren()
        for lyr in legend_layers:
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
        legend.attemptMove(QgsLayoutPoint(W - 4, 4, QgsUnitTypes.LayoutMillimeters))

    bar = QgsLayoutItemScaleBar(layout)
    layout.addLayoutItem(bar)
    bar.setLinkedMap(m)
    bar.setStyle('Single Box')
    bar.setUnits(QgsUnitTypes.DistanceMiles)
    bar.setUnitLabel('mi')
    bar.setUnitsPerSegment(5)
    bar.setSegmentSizeMode(QgsScaleBarSettings.SegmentSizeFixed)
    bar.setNumberOfSegments(2)
    bar.setNumberOfSegmentsLeft(0)
    bar.setTextFormat(FMT)
    bar.setBackgroundEnabled(True)
    bar.setBackgroundColor(QColor(255, 255, 255, 235))
    bar.update()
    bar.setReferencePoint(QgsLayoutItem.UpperRight)
    bar.attemptMove(QgsLayoutPoint(W - 4, bar_y, QgsUnitTypes.LayoutMillimeters))

    png = os.path.join(OUT, f'ws-{name}.png')
    settings = QgsLayoutExporter.ImageExportSettings()
    settings.dpi = 200
    print('export', name, QgsLayoutExporter(layout).exportToImage(png, settings), flush=True)


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

# app.exitQgis() segfaults on teardown; everything is written by now.
os._exit(0)
