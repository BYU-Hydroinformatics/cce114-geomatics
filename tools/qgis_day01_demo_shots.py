# Day 1 demo screenshots: rebuild the "Utah County in QGIS" project used by the Day 1
# Intro to GIS deck and have QGIS 3.44 LTR grab its own window. Runs INSIDE QGIS at launch,
# from a terminal — no clicking, no screen-recording permission, no focus stealing:
#
#   cd <scratch dir>
#   curl -LO https://github.com/BYU-Hydroinformatics/cce114-geomatics/releases/download/course-data-2026/UtahCountyData.zip
#   unzip UtahCountyData.zip -d ucd
#   B=https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services
#   for svc in UtahMunicipalBoundaries CitiesTownsLocations; do
#     curl -s "$B/$svc/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=26912&f=geojson&resultRecordCount=2000" -o $svc.geojson
#   done
#   DEMO_DIR="$PWD" SHOT=polygons /Applications/QGIS.app/Contents/MacOS/QGIS --nologo \
#       --code /path/to/qgis_day01_demo_shots.py
#
# SHOT is one of polygons, polylines, points, all-layers, attribute-table, buffer.
# Output: $DEMO_DIR/day01out/gis-<SHOT>.png at 2x (3200x1642 for a 1600x829 window). QGIS quits
# itself when done, about 20 s per shot.
#
# Status, 2026-09-17: written to re-shoot the deck's demo screenshots in 3.44 after a presenter
# note claimed they were QGIS 4.2. They are not — the Processing Toolbox group list, toolbars and
# status bar in the deck's existing shots match 3.44.14 exactly, apart from a GRASS provider that
# is enabled on whichever machine took them. The note was corrected and the images were left
# alone. This script is kept because it is the reproducible way to re-shoot them when they do go
# stale. The four map shots (polygons, polylines, points, all-layers) are verified; the
# attribute-table and buffer shots do not work yet — see the note on each in stage().
#
# The four layers and their order match the deck's Layers panel, top to bottom: Utah County
# (outline only), Utah Cities, Roads, City Centers. Roads come from the course data zip, so
# they stop at the county line — that is the layer students actually open in Lab 1.
#
# Gotchas, all learned the hard way and all still true:
#  - QGIS execs --code files, so __file__ is undefined; the scratch dir comes from DEMO_DIR.
#  - The project CRS resets to the default after layers are added, so it is re-asserted late.
#  - Grab only after mapCanvasRefreshed or the canvas comes out blank.
#  - QWidget.grab drops the title bar, which is what we want.
#  - QGIS cannot read or write under ~/Desktop, ~/Documents or ~/Downloads on macOS.
import os, traceback
from qgis.core import (QgsProject, QgsVectorLayer, QgsCoordinateReferenceSystem,
                       QgsFillSymbol, QgsLineSymbol, QgsMarkerSymbol)
from qgis.PyQt.QtCore import QTimer, Qt
from qgis.utils import iface

SCR = os.environ['DEMO_DIR']
UCD = os.path.join(SCR, 'ucd', 'UtahCountyData')
OUT = os.path.join(SCR, 'day01out'); os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, 'log.txt')
SHOT = os.environ.get('SHOT', 'all-layers')

W, H = 1600, 829          # window size; the grab comes back at 2x on a Retina display
PANEL = 250               # Layers panel width, matching the deck's existing shots


def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')


def build():
    p = QgsProject.instance(); p.clear()
    # Added bottom-up: each new layer lands on top of the tree, so this ends as
    # Utah County / Utah Cities / Roads / City Centers from the top down.
    ctr = QgsVectorLayer(os.path.join(SCR, 'CitiesTownsLocations.geojson'), 'City Centers', 'ogr')
    rds = QgsVectorLayer(os.path.join(UCD, 'UtahCountyMajorRoads.shp'), 'Roads', 'ogr')
    cty = QgsVectorLayer(os.path.join(SCR, 'UtahMunicipalBoundaries.geojson'), 'Utah Cities', 'ogr')
    bnd = QgsVectorLayer(os.path.join(UCD, 'UtahCountyBoundary.shp'), 'Utah County', 'ogr')
    for l in (ctr, rds, cty, bnd):
        log('layer', l.name(), l.isValid(), l.featureCount() if l.isValid() else '-')
        p.addMapLayer(l)

    crs = QgsCoordinateReferenceSystem('EPSG:26912')
    p.setCrs(crs); iface.mapCanvas().setDestinationCrs(crs)

    bnd.renderer().setSymbol(QgsFillSymbol.createSimple(
        {'color': '255,255,255,0', 'outline_color': '#6b6b6b',
         'outline_width': '0.5', 'outline_width_unit': 'MM'}))
    cty.renderer().setSymbol(QgsFillSymbol.createSimple(
        {'color': '#9ccc8a', 'outline_color': '#4f7a42',
         'outline_width': '0.25', 'outline_width_unit': 'MM'}))
    rds.renderer().setSymbol(QgsLineSymbol.createSimple(
        {'color': '#3b6fd1', 'width': '0.4', 'width_unit': 'MM'}))
    ctr.renderer().setSymbol(QgsMarkerSymbol.createSimple(
        {'name': 'circle', 'color': '#e2762c', 'outline_color': '#8a4a12',
         'outline_width': '0.25', 'size': '2.6', 'size_unit': 'MM'}))
    for l in (ctr, rds, cty, bnd):
        l.triggerRepaint(); iface.layerTreeView().refreshLayerSymbology(l.id())

    # Which layers are checked, per shot. The deck walks one feature type at a time.
    vis = {'polygons':        {bnd, cty},
           'polylines':       {bnd, rds},
           'points':          {bnd, ctr},
           'all-layers':      {bnd, cty, rds, ctr},
           'attribute-table': {bnd, cty},
           'buffer':          {bnd, rds}}[SHOT]
    root = p.layerTreeRoot()
    for l in (ctr, rds, cty, bnd):
        root.findLayer(l.id()).setItemVisibilityChecked(l in vis)
    iface.setActiveLayer(cty)

    mw = iface.mainWindow()
    from qgis.PyQt.QtWidgets import QDockWidget
    layers_dock = None
    for d in mw.findChildren(QDockWidget):
        keep = d.objectName() == 'Layers' or (SHOT == 'buffer' and d.objectName() == 'ProcessingToolbox')
        d.setVisible(keep)
        if d.objectName() == 'Layers':
            layers_dock = d
    mw.resize(W, H)
    if layers_dock:
        mw.resizeDocks([layers_dock], [PANEL], Qt.Horizontal)

    c = iface.mapCanvas()

    def on_refreshed():
        c.mapCanvasRefreshed.disconnect(on_refreshed)
        log('rendered; canvas', c.width(), c.height(), 'scale', c.scale())
        QTimer.singleShot(1200, stage)

    def settle():
        crs2 = QgsCoordinateReferenceSystem('EPSG:26912')
        p.setCrs(crs2); c.setDestinationCrs(crs2)
        c.mapCanvasRefreshed.connect(on_refreshed)
        # Frame it the way the deck's existing shots are framed: the county extent with a
        # little air around it, which brings in the south end of Salt Lake County for context.
        c.setExtent(bnd.extent()); c.zoomByFactor(1.30); c.refresh()

    QTimer.singleShot(2500, settle)
    globals()['_cty'] = cty


def stage():
    """Open whatever this shot needs on top of the map, then shoot."""
    try:
        if SHOT == 'attribute-table':
            # NOT WORKING YET. A free-floating attribute table opens at 617x331 and ignores
            # resize() because it has not been mapped when stage() runs, so the grab is too
            # small to read. Setting qgis/dockAttributeTable at this point is too late — the
            # table does not appear in the grab at all. Next thing to try: set the setting
            # before the main window is built, or find the dock by objectName after showing it
            # and force it visible.
            from qgis.core import QgsSettings
            QgsSettings().setValue('qgis/dockAttributeTable', True)
            iface.showAttributeTable(globals()['_cty'])
            QTimer.singleShot(2000, lambda: shoot(None))
            return
        if SHOT == 'buffer':
            # PARTLY WORKING. The Processing Toolbox panel comes out right; the Buffer dialog
            # itself is a separate top-level window and does not appear in the main window's
            # grab. Either grab the dialog separately once it is mapped, or drop the dialog and
            # keep the toolbox panel alone.
            import processing
            dlg = processing.createAlgorithmDialog('native:buffer', {
                'INPUT': globals()['_cty'], 'DISTANCE': 10.0, 'SEGMENTS': 5})
            dlg.show()
            QTimer.singleShot(1800, lambda: shoot(None))
            return
    except Exception:
        log(traceback.format_exc())
    shoot(None)


def shoot(widget):
    try:
        w = widget if widget is not None else iface.mainWindow()
        pm = w.grab()
        path = os.path.join(OUT, f'gis-{SHOT}.png')
        pm.save(path)
        log('saved', path, pm.width(), pm.height(), 'scale', iface.mapCanvas().scale())
    except Exception:
        log(traceback.format_exc())
    QgsProject.instance().setDirty(False)
    QTimer.singleShot(600, iface.mainWindow().close)


def _guard():
    try:
        build()
    except Exception:
        log(traceback.format_exc())
        iface.mainWindow().close()


QTimer.singleShot(1500, _guard)
