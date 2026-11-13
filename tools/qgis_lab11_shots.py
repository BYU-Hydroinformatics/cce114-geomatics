# Lab 11 Processing dialog figures, captured from QGIS 3.44 LTR's own dialogs (no window manager,
# no screen-recording permission). One dialog per process: SHOT picks extract-attr (step 20,
# images/anchored4.png), reproject (step 25, images/reproject-layer.png) or buffer (step 25,
# images/buffer-dialog.png).
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   for s in extract-attr reproject buffer; do SHOT=$s LAB11_GPKG=/Users/Shared/Lab11/UtahCounty.gpkg \
#     LAB11_OUT=<out dir> /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_lab11_shots.py; done
#
# LAB11_GPKG is a GeoPackage from running the lab's steps on the data students get (UGRC downloads
# and the REST layers, all EPSG:3857): tables walmart_clip (step 13's Clip output) and MajorRoads.
# Keep it outside ~/Desktop, ~/Documents and ~/Downloads, which QGIS cannot read on macOS. The Mac
# must be in Light appearance (see tools/lab0304-improvement-plan.md).
import os
import sys
sys.path.append('/Applications/QGIS.app/Contents/Resources/qgis/python/plugins')
from qgis.core import QgsApplication, QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem
from qgis.gui import QgsGui
from qgis.PyQt.QtCore import QTimer, QEventLoop
from qgis.PyQt.QtWidgets import QComboBox, QDoubleSpinBox, QCheckBox, QAbstractSpinBox

G = os.environ['LAB11_GPKG']
OUT = os.environ['LAB11_OUT']
SHOT = os.environ['SHOT']
os.makedirs(OUT, exist_ok=True)
QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], True)
app.initQgis()
QgsGui.editorWidgetRegistry().initEditors()
KEEP = []


def dest(table):
    return f"ogr:dbname='{G}' table=\"{table}\" (geom)"


def settle(ms=1500):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()


def main():
    from processing.core.Processing import Processing
    from processing.gui.AlgorithmDialog import AlgorithmDialog
    Processing.initialize()
    proj = QgsProject.instance()
    proj.setCrs(QgsCoordinateReferenceSystem('EPSG:26912'), True)

    def layer(table, name):
        lyr = QgsVectorLayer(f'{G}|layername={table}', name, 'ogr')
        assert lyr.isValid(), table
        proj.addMapLayer(lyr)
        KEEP.append(lyr)
        return lyr

    if SHOT == 'extract-attr':
        lyr = layer('walmart_clip', 'Clipped')
        alg, params, name = 'native:extractbyattribute', {
            'INPUT': lyr, 'FIELD': 'businessunit_banner_description', 'OPERATOR': 1,
            'VALUE': "Sam's Club", 'OUTPUT': dest('CurrentLocations')}, 'anchored4.png'
    elif SHOT == 'reproject':
        lyr = layer('MajorRoads', 'MajorRoads')
        alg, params, name = 'native:reprojectlayer', {
            'INPUT': lyr, 'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:26912'),
            'OUTPUT': dest('MajorRoads_UTM')}, 'reproject-layer.png'
    else:
        lyr = layer('MajorRoads_UTM', 'MajorRoads_UTM')
        alg, params, name = 'native:buffer', {
            'INPUT': lyr, 'DISTANCE': 3218.69, 'SEGMENTS': 12, 'DISSOLVE': True,
            'OUTPUT': dest('MajorRoadsBuffer')}, 'buffer-dialog.png'

    a = QgsApplication.processingRegistry().algorithmById(alg)
    d = AlgorithmDialog(a.create(), False, None)
    KEEP.append(d)
    d.resize(1100, 820 if SHOT == 'buffer' else 640)
    d.show()
    settle(600)
    d.mainWidget().setParameters(params)
    settle()
    if SHOT == 'buffer':
        # Show the distance the way step 25 tells students to enter it: 2, with the unit set to miles.
        for cb in d.findChildren(QComboBox):
            idx = [cb.itemText(i) for i in range(cb.count())]
            if 'miles' in idx:
                cb.setCurrentIndex(idx.index('miles'))
                for sb in d.findChildren(QDoubleSpinBox):
                    if abs(sb.value() - 3218.69) < 0.01 or abs(sb.value() - 2.0) < 0.01:
                        sb.setValue(2.0)
                break
        settle(400)
    pm = d.grab()
    pm.save(os.path.join(OUT, name))
    print(name, pm.width(), pm.height(), flush=True)
    sys.stdout.flush()
    os._exit(0)


QTimer.singleShot(1200, main)
app.exec_()
