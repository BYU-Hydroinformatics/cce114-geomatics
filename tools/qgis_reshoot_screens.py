# qgis_reshoot_screens.py
#
# Re-creates the lecture-deck screenshots that used to be ArcMap captures, inside a running
# QGIS 3.44: attribute tables, Select by Expression, Select by Location, Layer Properties >
# Metadata, the Model Designer, a hillshade/slope pair, and two Print Layout example maps.
# Widgets are captured with QWidget.render() at 2x (Retina) so no screen-recording permission
# is needed; layouts are exported with QgsLayoutExporter.
#
# Inputs: the UtahCountyData folder (docs/lectures/data/UtahCountyData.zip, unzipped) and four
# GeoJSON downloads from UGRC (county boundaries, cities and towns, municipal boundaries,
# PreK-12 schools; see the curl commands in tools/image-improvements-handoff.md). Set the
# OUT / UCD / UGRC paths below to writable folders outside ~/Desktop, ~/Documents, ~/Downloads.
#
# Run from the QGIS Python console:
#   exec(open('/path/to/tools/qgis_reshoot_screens.py').read())
# Outputs and a log land in OUT. The main() sequence at the bottom was trimmed during the
# 2026-09-02 session; restore the full list of steps (all functions above) to regenerate everything.
import os, traceback
from qgis.PyQt.QtCore import QTimer, Qt, QSize, QRectF
from qgis.PyQt.QtGui import QColor, QFont, QImage, QPainter
from qgis.PyQt.QtWidgets import QApplication, QDialog, QWidget, QComboBox, QLineEdit, QTextEdit, QPlainTextEdit
from qgis.core import (QgsProject, QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem, QgsRectangle,
                       QgsLayerMetadata, QgsBox3d, QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLabel,
                       QgsLayoutItemLegend, QgsLayoutItemScaleBar, QgsLayoutItemPicture, QgsLayoutItemShape,
                       QgsLayoutPoint, QgsLayoutSize, QgsUnitTypes, QgsLayoutExporter, QgsLayerTreeLayer,
                       QgsMarkerSymbol, QgsLineSymbol, QgsFillSymbol, QgsGraduatedSymbolRenderer, QgsRendererRange,
                       QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsPalLayerSettings, QgsTextFormat,
                       QgsVectorLayerSimpleLabeling, QgsTextBufferSettings, QgsMapSettings, QgsMapRendererParallelJob,
                       QgsSingleBandPseudoColorRenderer, QgsColorRampShader, QgsRasterShader, QgsStyle,
                       QgsProcessingModelAlgorithm, QgsProcessingModelChildAlgorithm, QgsProcessingModelParameter,
                       QgsProcessingModelChildParameterSource, QgsProcessingModelOutput,
                       QgsProcessingParameterFeatureSource, QgsProcessingParameterNumber, QgsApplication,
                       QgsLayoutItemMapGrid, QgsLayoutItemPage, QgsLayoutFrame)
from qgis.gui import QgsExpressionBuilderWidget
from qgis.utils import iface
import processing

OUT = '/private/tmp/claude-503/-Users-danames-ames-sync-Work-Teaching-CCE-114-Geomatics/7cbb146e-5554-4d0a-a87c-2a239010dc3a/scratchpad/reshoot/out'
UCD = '/private/tmp/claude-503/-Users-danames-ames-sync-Work-Teaching-CCE-114-Geomatics/7cbb146e-5554-4d0a-a87c-2a239010dc3a/scratchpad/ucd/UtahCountyData'
UGRC = '/private/tmp/claude-503/-Users-danames-ames-sync-Work-Teaching-CCE-114-Geomatics/7cbb146e-5554-4d0a-a87c-2a239010dc3a/scratchpad/ugrc'
LOG = os.path.join(OUT, 'reshoot.log')
os.makedirs(OUT, exist_ok=True)
L = {}  # layers by key
NAVY = '#002e5d'


def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')


def find_dialog(sub):
    for w in QApplication.topLevelWidgets():
        if w.isVisible() and sub.lower() in w.windowTitle().lower() and w is not iface.mainWindow():
            return w
    return None


def grab(w, name):
    img = QImage(w.size() * 2, QImage.Format_ARGB32_Premultiplied); img.setDevicePixelRatio(2.0); img.fill(QColor('white'))
    w.render(img); path = os.path.join(OUT, name); img.save(path)
    log('saved', name, img.width(), img.height())


def step(delay, fn, *args):
    def wrapped():
        try:
            fn(*args)
        except Exception:
            log('ERROR in', fn.__name__, traceback.format_exc())
    QTimer.singleShot(delay, wrapped)


def close_dialogs(*subs):
    for s in subs:
        d = find_dialog(s)
        if d:
            d.close()


# ------------------------------------------------------------------ setup
def setup():
    p = QgsProject.instance(); p.clear()
    p.setCrs(QgsCoordinateReferenceSystem('EPSG:26912'))
    def add(key, uri, name, provider='ogr'):
        lyr = QgsVectorLayer(uri, name, provider) if provider == 'ogr' else QgsRasterLayer(uri, name)
        log('layer', name, lyr.isValid(), lyr.featureCount() if lyr.isValid() and provider == 'ogr' else '')
        p.addMapLayer(lyr); L[key] = lyr; return lyr
    add('counties', f'{UGRC}/Utah_County_Boundaries.geojson', 'Utah Counties')
    add('cities', f'{UGRC}/CitiesTownsLocations.geojson', 'Cities and Towns')
    add('munis', f'{UGRC}/UtahMunicipalBoundaries.geojson', 'Municipal Boundaries')
    if os.path.exists(f'{UGRC}/Schools.geojson'):
        add('schools', f'{UGRC}/Schools.geojson', 'Schools (PreK-12)')
    add('roads', f'{UCD}/UtahCountyMajorRoads.shp', 'UtahCountyMajorRoads')
    add('towers', f'{UCD}/UtahCountyCellularTowers.shp', 'UtahCountyCellularTowers')
    add('boundary', f'{UCD}/UtahCountyBoundary.shp', 'UtahCountyBoundary')
    add('dem', f'{UCD}/UtahCountyDEM.tif', 'UtahCountyDEM', 'gdal')
    # basic styling so screenshots look intentional
    L['counties'].renderer().symbol().setColor(QColor('#f3efe6'))
    L['counties'].renderer().symbol().symbolLayer(0).setStrokeColor(QColor('#7a7a7a'))
    L['boundary'].renderer().symbol().setColor(QColor(0, 0, 0, 0))
    L['boundary'].renderer().symbol().symbolLayer(0).setStrokeColor(QColor(NAVY)); L['boundary'].renderer().symbol().symbolLayer(0).setStrokeWidth(0.8)
    L['roads'].renderer().symbol().setColor(QColor('#b8412f')); L['roads'].renderer().symbol().setWidth(0.5)
    L['towers'].renderer().symbol().setColor(QColor('#e08a1e')); L['towers'].renderer().symbol().setSize(2.6)
    if 'schools' in L:
        L['schools'].renderer().symbol().setColor(QColor('#3b7dd8')); L['schools'].renderer().symbol().setSize(1.8)
    for k in ('cities', 'munis'):
        QgsProject.instance().layerTreeRoot().findLayer(L[k].id()).setItemVisibilityChecked(False)
    iface.mapCanvas().setExtent(L['boundary'].extent()); iface.mapCanvas().refresh()
    iface.mainWindow().resize(1400, 900)
    log('setup done')


# ------------------------------------------------------------------ Day 18: attribute table (counties, Utah selected)
def table_action(dlg, *names):
    from qgis.PyQt.QtWidgets import QAction
    for n in names:
        a = dlg.findChild(QAction, n)
        if a is not None:
            a.trigger(); log('triggered', n); return True
    log('no action among', names, [a.objectName() for a in dlg.findChildren(QAction) if a.objectName()][:40])
    return False


def counties_table():
    lyr = L['counties']; lyr.selectByExpression('"NAME" = \'UTAH\'')
    iface.setActiveLayer(lyr)
    dlg = iface.showAttributeTable(lyr); L['_table'] = dlg
    QTimer.singleShot(600, lambda: (dlg.resize(1250, 640), table_action(dlg, 'mActionSelectedToTop')))
    log('counties table', dlg)


def grab_counties_table():
    d = L['_table']; grab(d, 'gp-attribute-table-qgis.png'); d.close()


# ------------------------------------------------------------------ Select by Expression dialogs
def open_select_expr(layer_key, expr, size=(1000, 720)):
    iface.setActiveLayer(L[layer_key]); L[layer_key].removeSelection()
    from qgis.PyQt.QtWidgets import QAction
    act = iface.mainWindow().findChild(QAction, 'mActionSelectByExpression')
    if act is None:
        act = [a for a in iface.mainWindow().findChildren(QAction) if 'by expression' in a.text().lower()][0]
    act.trigger()
    def fill():
        import sip
        from qgis.gui import QgsExpressionSelectionDialog
        d = find_dialog('Select by Expression'); d.resize(*size)
        try:
            d2 = sip.cast(d, QgsExpressionSelectionDialog); d2.setExpressionText(expr); log('set via dialog cast')
        except Exception as e:
            log('cast failed', e)
            w = d.findChild(QgsExpressionBuilderWidget); w.setExpressionText(expr)
        w = d.findChild(QgsExpressionBuilderWidget)
        log('select expr dialog', d.windowTitle(), 'text now:', w.expressionText() if w else None)
    QTimer.singleShot(800, fill)


def grab_select_expr(name):
    d = find_dialog('Select by Expression'); grab(d, name); d.close()


# ------------------------------------------------------------------ Select by Location dialog
def open_select_location():
    src = L.get('schools', L['towers'])
    L['counties'].selectByExpression('"NAME" = \'UTAH\'')
    from qgis.core import QgsProcessingFeatureSourceDefinition
    dlg = processing.createAlgorithmDialog('native:selectbylocation', {
        'INPUT': src, 'PREDICATE': [0], 'INTERSECT': QgsProcessingFeatureSourceDefinition(L['counties'].id(), True), 'METHOD': 0})
    dlg.show(); dlg.resize(900, 640); log('select location dialog', dlg.windowTitle())
    L['_sel_loc_dlg'] = dlg


def grab_select_location():
    d = L['_sel_loc_dlg']; grab(d, 'gp-select-by-location-qgis.png'); d.close()


# ------------------------------------------------------------------ Day 22: roads table + I-15 selection
def roads_table():
    lyr = L['roads']; lyr.selectByExpression('"HWYNAME" = \'I-15\'')
    iface.setActiveLayer(lyr); dlg = iface.showAttributeTable(lyr); L['_table'] = dlg
    QTimer.singleShot(600, lambda: (dlg.resize(1250, 640), table_action(dlg, 'mActionSelectedFilter', 'mActionSelectedToTop')))
    log('roads table', dlg)


def grab_roads_table():
    d = L['_table']; grab(d, 'ws-roads-attribute-table-qgis.png'); d.close()


# ------------------------------------------------------------------ Day 16: Layer Properties > Metadata
def metadata_props():
    lyr = L['counties']
    md = lyr.metadata()
    md.setIdentifier('utah-county-boundaries'); md.setTitle('Utah County Boundaries')
    md.setType('dataset'); md.setLanguage('EN')
    md.setAbstract('Boundaries of the 29 counties of Utah, maintained by the Utah Geospatial Resource Center (UGRC) '
                   'as part of the State Geographic Information Datastore (SGID). Downloaded for CCE 114 Geomatics.')
    md.setKeywords({'gmd:topicCategory': ['boundaries'], 'keywords': ['Utah', 'counties', 'SGID', 'UGRC']})
    md.setLicenses(['Public domain (State of Utah)'])
    md.setCrs(lyr.crs())
    lyr.setMetadata(md)
    iface.showLayerProperties(lyr, 'mOptsPage_Metadata')
    def fix():
        d = find_dialog('Layer Properties'); d.resize(1000, 760); log('layer props', d.windowTitle())
    QTimer.singleShot(800, fix)


def grab_metadata_props():
    d = find_dialog('Layer Properties'); grab(d, 'md-qgis-metadata-panel-344.png'); d.close()


# ------------------------------------------------------------------ Day 22: Graphical Modeler
def open_modeler():
    m = QgsProcessingModelAlgorithm('Walmart site selection', 'CCE 114')
    def param(name, desc, x, y):
        pd = QgsProcessingParameterFeatureSource(name, desc)
        mp = QgsProcessingModelParameter(name); mp.setPosition(QPointF(x, y))
        m.addModelParameter(pd, mp)
    from qgis.PyQt.QtCore import QPointF
    param('blocks', 'Census blocks', 260, 60); param('roads', 'UDOT routes', 560, 60); param('walmarts', 'Existing Walmarts', 860, 60)
    def child(cid, alg, x, y, sources, extra=None, out=None):
        c = QgsProcessingModelChildAlgorithm(alg); c.setChildId(cid); c.setDescription(cid.replace('_', ' ').title())
        c.setPosition(QPointF(x, y))
        for k, v in sources.items():
            if isinstance(v, tuple):
                c.addParameterSources(k, [QgsProcessingModelChildParameterSource.fromChildOutput(*v)])
            elif isinstance(v, str) and v in ('blocks', 'roads', 'walmarts'):
                c.addParameterSources(k, [QgsProcessingModelChildParameterSource.fromModelParameter(v)])
            else:
                c.addParameterSources(k, [QgsProcessingModelChildParameterSource.fromStaticValue(v)])
        if out:
            o = QgsProcessingModelOutput(out, out); o.setChildId(cid); o.setChildOutputName('OUTPUT'); o.setPosition(QPointF(x, y + 110))
            c.setModelOutputs({out: o})
        m.addChildAlgorithm(c); return cid
    child('density', 'native:fieldcalculator', 260, 180, {'INPUT': 'blocks', 'FIELD_NAME': 'density', 'FIELD_TYPE': 0, 'FORMULA': '"POP" / ($area / 1000000)'})
    child('dense_blocks', 'native:extractbyexpression', 260, 300, {'INPUT': ('density', 'OUTPUT'), 'EXPRESSION': '"density" > 1000'})
    child('i15', 'native:extractbyexpression', 560, 180, {'INPUT': 'roads', 'EXPRESSION': '"HWYNAME" = \'I-15\''})
    child('dissolve', 'native:dissolve', 560, 300, {'INPUT': ('i15', 'OUTPUT')})
    child('road_buffer', 'native:buffer', 560, 420, {'INPUT': ('dissolve', 'OUTPUT'), 'DISTANCE': 3000, 'DISSOLVE': True})
    child('walmart_buffer', 'native:buffer', 860, 180, {'INPUT': 'walmarts', 'DISTANCE': 8000, 'DISSOLVE': True})
    child('near_roads', 'native:intersection', 400, 540, {'INPUT': ('dense_blocks', 'OUTPUT'), 'OVERLAY': ('road_buffer', 'OUTPUT')})
    child('candidates', 'native:difference', 630, 660, {'INPUT': ('near_roads', 'OUTPUT'), 'OVERLAY': ('walmart_buffer', 'OUTPUT')}, out='Possible Walmart locations')
    from processing.modeler.ModelerDialog import ModelerDialog
    dlg = ModelerDialog.create(m); dlg.show(); dlg.resize(1500, 920)
    L['_modeler'] = dlg; log('modeler open', dlg.windowTitle())


def grab_modeler():
    d = L['_modeler']; grab(d, 'ws-graphical-modeler-qgis.png'); d.close()


# ------------------------------------------------------------------ Day 10: hillshade + slope renders
def terrain():
    hs = processing.run('gdal:hillshade', {'INPUT': L['dem'], 'BAND': 1, 'Z_FACTOR': 1, 'AZIMUTH': 315, 'ALTITUDE': 45, 'OUTPUT': os.path.join(OUT, 'hillshade.tif')})['OUTPUT']
    sl = processing.run('gdal:slope', {'INPUT': L['dem'], 'BAND': 1, 'AS_PERCENT': False, 'OUTPUT': os.path.join(OUT, 'slope.tif')})['OUTPUT']
    ct = processing.run('gdal:contour', {'INPUT': L['dem'], 'BAND': 1, 'INTERVAL': 200, 'FIELD_NAME': 'ELEV', 'OUTPUT': os.path.join(OUT, 'contours.gpkg')})['OUTPUT']
    hsl = QgsRasterLayer(hs, 'Hillshade'); sll = QgsRasterLayer(sl, 'Slope (degrees)'); ctl = QgsVectorLayer(ct, 'Contours (200 m)', 'ogr')
    ctl.renderer().symbol().setColor(QColor('#6b3e1e')); ctl.renderer().symbol().setWidth(0.25)
    # slope colour ramp
    shader = QgsRasterShader(); fn = QgsColorRampShader(); fn.setColorRampType(QgsColorRampShader.Interpolated)
    fn.setColorRampItemList([QgsColorRampShader.ColorRampItem(0, QColor('#ffffcc'), '0'), QgsColorRampShader.ColorRampItem(15, QColor('#fd8d3c'), '15'),
                             QgsColorRampShader.ColorRampItem(30, QColor('#bd0026'), '30'), QgsColorRampShader.ColorRampItem(60, QColor('#3b0012'), '60')])
    shader.setRasterShaderFunction(fn); sll.setRenderer(QgsSingleBandPseudoColorRenderer(sll.dataProvider(), 1, shader))
    for lyr in (hsl, sll, ctl):
        QgsProject.instance().addMapLayer(lyr, False)
    L['hillshade'], L['slope'], L['contours'] = hsl, sll, ctl
    ext = L['dem'].extent()
    # zoom to the Provo / Wasatch front third of the DEM for a dramatic view
    cx, cy = ext.center().x(), ext.center().y(); w, h = ext.width() * 0.45, ext.height() * 0.45
    view = QgsRectangle(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
    for name, layers in (('ras-hillshade-contours.png', [ctl, hsl]), ('ras-slope.png', [sll])):
        ms = QgsMapSettings(); ms.setLayers(layers); ms.setExtent(view); ms.setOutputSize(QSize(1200, 1000))
        ms.setDestinationCrs(QgsCoordinateReferenceSystem('EPSG:26912')); ms.setBackgroundColor(QColor('white'))
        job = QgsMapRendererParallelJob(ms); job.start(); job.waitForFinished()
        job.renderedImage().save(os.path.join(OUT, name)); log('rendered', name)


# ------------------------------------------------------------------ layouts (Day 4, Day 23)
def add_label(layout, text, x, y, w, h, size=12, bold=False, align=Qt.AlignLeft, color='#22262e'):
    lab = QgsLayoutItemLabel(layout); lab.setText(text)
    f = QFont('Helvetica'); f.setPointSizeF(size); f.setBold(bold); lab.setFont(f); lab.setFontColor(QColor(color)); lab.setHAlign(align)
    lab.attemptMove(QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters)); lab.attemptResize(QgsLayoutSize(w, h, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(lab); return lab


def add_frame(layout, x, y, w, h, width=0.6):
    sh = QgsLayoutItemShape(layout); sh.setShapeType(QgsLayoutItemShape.Rectangle)
    sym = QgsFillSymbol.createSimple({'color': '0,0,0,0', 'outline_color': NAVY, 'outline_width': str(width)}); sh.setSymbol(sym)
    sh.attemptMove(QgsLayoutPoint(x, y, QgsUnitTypes.LayoutMillimeters)); sh.attemptResize(QgsLayoutSize(w, h, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(sh); return sh


def add_furniture(layout, mapitem, legend_layers, legend_title, x_right, scale_y, north_y, legend_y, src_text, src_y):
    lg = QgsLayoutItemLegend(layout); lg.setTitle(legend_title); lg.setAutoUpdateModel(False)
    root = lg.model().rootGroup()
    for n in list(root.children()):
        root.removeChildNode(n)
    for lyr in legend_layers:
        root.addLayer(lyr)
    lg.setLinkedMap(mapitem); lg.setSymbolHeight(4); lg.setSymbolWidth(6)
    lg.attemptMove(QgsLayoutPoint(x_right, legend_y, QgsUnitTypes.LayoutMillimeters)); layout.addLayoutItem(lg)
    sb = QgsLayoutItemScaleBar(layout); sb.setLinkedMap(mapitem); sb.setStyle('Single Box'); sb.setUnits(QgsUnitTypes.DistanceKilometers)
    sb.setUnitsPerSegment(10); sb.setUnitLabel('km'); sb.setNumberOfSegments(2); sb.setNumberOfSegmentsLeft(0); sb.setHeight(3)
    sb.attemptMove(QgsLayoutPoint(x_right, scale_y, QgsUnitTypes.LayoutMillimeters)); layout.addLayoutItem(sb)
    na = QgsLayoutItemPicture(layout); na.setPicturePath(os.path.join(QgsApplication.pkgDataPath(), 'svg', 'arrows', 'NorthArrow_02.svg'))
    na.attemptMove(QgsLayoutPoint(x_right + 62, scale_y - 6, QgsUnitTypes.LayoutMillimeters)); na.attemptResize(QgsLayoutSize(12, 16, QgsUnitTypes.LayoutMillimeters))
    layout.addLayoutItem(na)
    add_label(layout, src_text, x_right, src_y, 78, 40, size=7.5)


def export(layout, name, dpi=200):
    ex = QgsLayoutExporter(layout); s = QgsLayoutExporter.ImageExportSettings(); s.dpi = dpi
    r = ex.exportToImage(os.path.join(OUT, name), s); log('layout export', name, r)


def layout_cities():
    counties = L['counties']; cities = L['cities']; munis = L['munis']
    counties.setSubsetString("\"NAME\" IN ('SALT LAKE','UTAH')")
    munis.setSubsetString("\"COUNTYNBR\" IN ('18','25')")
    cities.setSubsetString("\"COUNTY\" IN ('Salt Lake','Utah') AND \"POPULATION\" >= 20000")
    munis.renderer().symbol().setColor(QColor('#e3ecd8')); munis.renderer().symbol().symbolLayer(0).setStrokeColor(QColor('#b7c9a3'))
    # graduated star markers by population: "point symbols can be anything"
    ranges = []
    for lo, hi, size, label in ((20000, 60000, 3.5, '20,000 - 60,000'), (60000, 120000, 5.5, '60,000 - 120,000'), (120000, 400000, 8, 'over 120,000')):
        sym = QgsMarkerSymbol.createSimple({'name': 'star', 'color': '#e08a1e', 'outline_color': NAVY, 'outline_width': '0.3', 'size': str(size)})
        ranges.append(QgsRendererRange(lo, hi, sym, label))
    cities.setRenderer(QgsGraduatedSymbolRenderer('POPULATION', ranges))
    pal = QgsPalLayerSettings(); pal.fieldName = 'NAME'; pal.placement = QgsPalLayerSettings.OrderedPositionsAroundPoint
    tf = QgsTextFormat(); tf.setFont(QFont('Helvetica', 8)); tf.setSize(8); buf = QgsTextBufferSettings(); buf.setEnabled(True); buf.setSize(0.8); tf.setBuffer(buf)
    pal.setFormat(tf); cities.setLabeling(QgsVectorLayerSimpleLabeling(pal)); cities.setLabelsEnabled(True)
    root = QgsProject.instance().layerTreeRoot()
    for k in ('cities', 'munis', 'counties'):
        root.findLayer(L[k].id()).setItemVisibilityChecked(True)
    lay = QgsPrintLayout(QgsProject.instance()); lay.initializeDefaults(); lay.setName('cities')
    pc = lay.pageCollection(); pc.page(0).setPageSize('A4', QgsLayoutItemPage.Landscape)
    add_frame(lay, 6, 6, 285, 198, 0.8)   # neat line
    add_label(lay, 'Major Cities of Salt Lake and Utah Counties', 12, 10, 273, 12, size=18, bold=True, align=Qt.AlignHCenter, color=NAVY)
    add_label(lay, 'Cities with more than 20,000 residents, symbol size by population', 12, 21, 273, 7, size=10, align=Qt.AlignHCenter, color='#555')
    ext = counties.extent(); ext.scale(1.06); aspect = ext.width() / ext.height()
    mh = 165.0; mw = mh * aspect
    m = QgsLayoutItemMap(lay); m.setRect(0, 0, 10, 10); m.setLayers([cities, munis, counties])
    m.attemptMove(QgsLayoutPoint(12, 30, QgsUnitTypes.LayoutMillimeters)); m.attemptResize(QgsLayoutSize(mw, mh, QgsUnitTypes.LayoutMillimeters))
    m.setExtent(ext); m.setFrameEnabled(True); m.setBackgroundColor(QColor('#f7fbff'))
    lay.addLayoutItem(m)
    xr = 12 + mw + 12
    add_furniture(lay, m, [cities, munis, counties], 'Legend', xr, 150, 150, 32,
                  'Projection: NAD83 / UTM zone 12N (EPSG:26912)\nData: Utah Geospatial Resource Center (UGRC) SGID,\ncities and towns, municipal and county boundaries\nMap: CCE 114 Geomatics, Brigham Young University', 176)
    export(lay, 'mc-major-cities-qgis-layout.png')
    counties.setSubsetString(''); munis.setSubsetString(''); cities.setSubsetString('')


def layout_sites():
    roads0, towers0, boundary = L['roads'], L['towers'], L['boundary']
    t26 = processing.run('native:reprojectlayer', {'INPUT': towers0, 'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:26912'), 'OUTPUT': 'memory:'})['OUTPUT']
    towers = processing.run('native:clip', {'INPUT': t26, 'OVERLAY': boundary, 'OUTPUT': 'memory:'})['OUTPUT']
    towers.setName('Cellular towers'); QgsProject.instance().addMapLayer(towers, False)
    roads = processing.run('native:clip', {'INPUT': roads0, 'OVERLAY': boundary, 'OUTPUT': 'memory:'})['OUTPUT']
    roads.setName('Major roads'); roads.renderer().symbol().setColor(QColor('#b8412f')); roads.renderer().symbol().setWidth(0.45)
    QgsProject.instance().addMapLayer(roads, False)
    buf = processing.run('native:buffer', {'INPUT': roads, 'DISTANCE': 1000, 'DISSOLVE': True, 'OUTPUT': 'memory:'})['OUTPUT']
    buf.setName('Within 1 km of a major road')
    buf.renderer().symbol().setColor(QColor(59, 125, 216, 70)); buf.renderer().symbol().symbolLayer(0).setStrokeColor(QColor(59, 125, 216, 0))
    QgsProject.instance().addMapLayer(buf, False)
    log('crs check', towers.crs().authid(), buf.crs().authid(), roads.crs().authid(), towers.featureCount(), 'towers in county')
    inside = processing.run('native:selectbylocation', {'INPUT': towers, 'PREDICATE': [0], 'INTERSECT': buf, 'METHOD': 0})
    ids = set(towers.selectedFeatureIds()); towers.removeSelection(); log('candidates', len(ids))
    cats = []
    for val, color, label in ((1, '#1a9641', 'Candidate site (within 1 km)'), (0, '#9e9e9e', 'Other tower')):
        sym = QgsMarkerSymbol.createSimple({'name': 'circle', 'color': color, 'outline_color': '#333', 'outline_width': '0.25', 'size': '2.8' if val else '2'})
        cats.append(QgsRendererCategory(val, sym, label))
    expr = 'CASE WHEN $id IN (' + ','.join(str(i) for i in ids) + ') THEN 1 ELSE 0 END'
    towers.setRenderer(QgsCategorizedSymbolRenderer(expr, cats))
    lay = QgsPrintLayout(QgsProject.instance()); lay.initializeDefaults(); lay.setName('sites')
    lay.pageCollection().page(0).setPageSize('A4', QgsLayoutItemPage.Landscape)
    add_frame(lay, 6, 6, 285, 198, 0.8)
    add_label(lay, 'Candidate Cell Tower Sites Within 1 km of a Major Road', 12, 10, 273, 12, size=18, bold=True, align=Qt.AlignHCenter, color=NAVY)
    add_label(lay, 'Utah County, Utah — example site-selection result for the CCE 114 final mapping project', 12, 21, 273, 7, size=10, align=Qt.AlignHCenter, color='#555')
    m = QgsLayoutItemMap(lay); m.setRect(0, 0, 10, 10); m.setLayers([towers, roads, buf, boundary])
    m.attemptMove(QgsLayoutPoint(12, 30, QgsUnitTypes.LayoutMillimeters)); m.attemptResize(QgsLayoutSize(195, 168, QgsUnitTypes.LayoutMillimeters))
    ext = boundary.extent(); ext.scale(1.03); m.setExtent(ext); m.setFrameEnabled(True); m.setBackgroundColor(QColor('#f7fbff'))
    lay.addLayoutItem(m)
    boundary.setName('Utah County boundary')
    add_furniture(lay, m, [towers, buf, roads, boundary], 'Legend', 212, 150, 150, 32,
                  f'{len(ids)} of {towers.featureCount()} towers fall within 1 km of a major road.\n\nProjection: NAD83 / UTM zone 12N (EPSG:26912)\nData: UGRC SGID roads and county boundary;\nFCC cellular tower registrations\nMap: CCE 114 Geomatics, Brigham Young University', 176)
    export(lay, 'fp-example-map-qgis.png')


# ------------------------------------------------------------------ sequence
def main():
    log('main start (rerun)')
    step(500, setup)
    step(4000, layout_sites)
    step(14000, log, 'DONE')


log('reshoot.py loaded')
step(1500, main)
