# Day 2 demo screenshots: rebuild the "Utah County in QGIS" project and have QGIS 3.44 grab
# its own main window. Runs INSIDE QGIS at launch, from a terminal:
#
#   cd <scratch dir>; curl -LO https://github.com/BYU-Hydroinformatics/cce114-geomatics/releases/download/course-data-2026/UtahCountyData.zip
#   unzip UtahCountyData.zip -d ucd
#   DEMO_DIR="$PWD" SHOT=all-five /Applications/QGIS.app/Contents/MacOS/QGIS --nologo \
#       --code /path/to/qgis_day02_demo_shots.py
#
# SHOT is one of all-five, raster, polygon, polyline, point (which layers are checked).
# Output: $DEMO_DIR/day02out/dm-demo-<SHOT>.png at 2x (2880x1406 for a 1440x703 window); the
# deck images are that resized to 2000 px wide. QGIS quits itself when done (about 15 s).
#
# Layer order is the point of this script: Cellular Towers, Major Roads, Utah County Boundary,
# Elevation (m) top to bottom, so the raster draws underneath the vector layers.
# Gotchas: QGIS execs --code files, so __file__ is undefined (hence DEMO_DIR); the project CRS
# gets reset to the default after layers are added, so it is re-asserted before zooming; grab
# only after mapCanvasRefreshed or the canvas comes out blank; QWidget.grab drops the title bar.
import os, sys, traceback
from qgis.core import (QgsProject, QgsVectorLayer, QgsRasterLayer, QgsCoordinateReferenceSystem,
                       QgsSingleBandPseudoColorRenderer, QgsColorRampShader, QgsRasterShader,
                       QgsGradientColorRamp, QgsGradientStop, QgsRasterBandStats, QgsSymbol,
                       QgsMarkerSymbol, QgsLineSymbol, QgsFillSymbol, QgsUnitTypes)
from qgis.PyQt.QtCore import QTimer, Qt
from qgis.PyQt.QtGui import QColor
from qgis.utils import iface

# QGIS runs --code files with exec(open(f).read()), so __file__ is not defined: take the dir from env
SCR = os.environ['DEMO_DIR']
UCD = os.path.join(SCR, 'ucd', 'UtahCountyData')
OUT = os.path.join(SCR, 'day02out'); os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, 'log.txt')
SHOT = os.environ.get('SHOT', 'all-five')   # which view to stage

def log(*a):
    with open(LOG, 'a') as f: f.write(' '.join(str(x) for x in a) + '\n')

def build():
    p = QgsProject.instance(); p.clear()
    # add bottom-up: each new layer goes on top of the tree
    dem = QgsRasterLayer(os.path.join(UCD, 'UtahCountyDEM.tif'), 'Elevation (m)')
    bnd = QgsVectorLayer(os.path.join(UCD, 'UtahCountyBoundary.shp'), 'Utah County Boundary', 'ogr')
    rds = QgsVectorLayer(os.path.join(UCD, 'UtahCountyMajorRoads.shp'), 'Major Roads', 'ogr')
    twr = QgsVectorLayer(os.path.join(UCD, 'UtahCountyCellularTowers.shp'), 'Cellular Towers', 'ogr')
    for l in (dem, bnd, rds, twr):
        log('layer', l.name(), l.isValid()); p.addMapLayer(l)
    crs = QgsCoordinateReferenceSystem('EPSG:26912'); p.setCrs(crs); iface.mapCanvas().setDestinationCrs(crs)
    log('crs', p.crs().authid(), iface.mapCanvas().mapSettings().destinationCrs().authid(), 'dem', dem.crs().authid(), 'bnd', bnd.crs().authid())

    # Elevation: green -> tan -> white hypsometric ramp over the band's real min/max
    stats = dem.dataProvider().bandStatistics(1, QgsRasterBandStats.Min | QgsRasterBandStats.Max)
    lo, hi = stats.minimumValue, stats.maximumValue; log('dem range', lo, hi)
    ramp = QgsGradientColorRamp(QColor('#2f6b3d'), QColor('#ffffff'),
                                stops=[QgsGradientStop(0.35, QColor('#9cbf76')),
                                       QgsGradientStop(0.62, QColor('#d3b98c')),
                                       QgsGradientStop(0.85, QColor('#e9dcc3'))])
    fcn = QgsColorRampShader(lo, hi, ramp, QgsColorRampShader.Interpolated)
    fcn.classifyColorRamp(classes=8, band=1, input=dem.dataProvider())
    shader = QgsRasterShader(); shader.setRasterShaderFunction(fcn)
    dem.setRenderer(QgsSingleBandPseudoColorRenderer(dem.dataProvider(), 1, shader))

    bnd.setRenderer(bnd.renderer().clone())
    fill = QgsFillSymbol.createSimple({'color': '228,240,228,95', 'outline_color': '#2f5c44',
                                       'outline_width': '1.1', 'outline_width_unit': 'MM'})
    bnd.renderer().setSymbol(fill)
    rds.renderer().setSymbol(QgsLineSymbol.createSimple({'color': '#3b6fd1', 'width': '0.55', 'width_unit': 'MM'}))
    twr.renderer().setSymbol(QgsMarkerSymbol.createSimple({'name': 'circle', 'color': '#e2762c',
                                                            'outline_color': '#5a2d0c', 'outline_width': '0.3',
                                                            'size': '2.8', 'size_unit': 'MM'}))
    for l in (dem, bnd, rds, twr):
        l.triggerRepaint(); iface.layerTreeView().refreshLayerSymbology(l.id())
    root = p.layerTreeRoot()
    vis = {'all-five': {dem, bnd, rds, twr}, 'raster': {dem}, 'polygon': {bnd},
           'polyline': {bnd, rds}, 'point': {bnd, twr}}[SHOT]
    for l in (dem, bnd, rds, twr):
        root.findLayer(l.id()).setItemVisibilityChecked(l in vis)
    iface.setActiveLayer(dem)

    # window chrome: only the Layers panel, sized like the earlier demo shots
    mw = iface.mainWindow()
    from qgis.PyQt.QtWidgets import QDockWidget
    layers_dock = None
    for d in mw.findChildren(QDockWidget):
        d.setVisible(d.objectName() == 'Layers')
        if d.objectName() == 'Layers': layers_dock = d
    mw.resize(1440, 703)
    if layers_dock: mw.resizeDocks([layers_dock], [250], Qt.Horizontal)
    c = iface.mapCanvas(); c.setExtent(bnd.extent()); c.refresh()
    def on_refreshed():
        c.mapCanvasRefreshed.disconnect(on_refreshed)
        log('rendered; canvas', c.width(), c.height(), 'scale', c.scale(), 'crs', c.mapSettings().destinationCrs().authid())
        QTimer.singleShot(1000, shoot)
    def settle():
        crs = QgsCoordinateReferenceSystem('EPSG:26912'); p.setCrs(crs); c.setDestinationCrs(crs)
        log('settle crs', p.crs().authid(), c.mapSettings().destinationCrs().authid())
        c.mapCanvasRefreshed.connect(on_refreshed)
        c.setExtent(bnd.extent()); c.zoomByFactor(1.12); c.refresh()
    QTimer.singleShot(2500, settle)

def shoot():
    try:
        mw = iface.mainWindow(); pm = mw.grab()
        path = os.path.join(OUT, f'dm-demo-{SHOT}.png'); pm.save(path)
        log('saved', path, pm.width(), pm.height(), 'scale', iface.mapCanvas().scale())
    except Exception:
        log(traceback.format_exc())
    QgsProject.instance().setDirty(False)
    QTimer.singleShot(500, iface.mainWindow().close)

def start():
    try:
        build()
    except Exception:
        log(traceback.format_exc()); QTimer.singleShot(500, iface.mainWindow().close); return

def _guard():
    try:
        start()
    except Exception:
        log(traceback.format_exc()); iface.mainWindow().close()

QTimer.singleShot(1500, _guard)
