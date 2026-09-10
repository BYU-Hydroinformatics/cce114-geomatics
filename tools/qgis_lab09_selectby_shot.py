# Lab 9's Select by Attribute figure, re-captured so its callout can be redrawn.
#
# The figure in the repository (anchored9.png) carries a red callout that says "We need a 10km
# buffer" twice, but Lab 9 step 41 buffers Fish Creek Road by 5 kilometers. The wrong number has
# been flagged in tools/image-improvements-handoff.md since 2026-09-02. This re-shoots the dialog;
# tools/lab09_annotate.py draws the corrected callout.
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   LAB09_DATA=<dir with idaho_road_reproj.shp> LAB09_OUT=<out dir> \
#     /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_lab09_selectby_shot.py
#
# The Mac must be in Light appearance; see tools/lab0304-improvement-plan.md for why that cannot
# be scripted.
import json
import os
import sys

# The processing framework ships as a bundled plugin, which is not on sys.path in a bare
# QgsApplication the way it is inside the running QGIS app.
sys.path.append('/Applications/QGIS.app/Contents/Resources/qgis/python/plugins')

from qgis.core import (QgsApplication, QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem)
from qgis.gui import QgsGui
from qgis.PyQt.QtCore import QTimer
from qgis.PyQt.QtWidgets import QWidget, QComboBox

DATA = os.environ['LAB09_DATA']
OUT = os.environ['LAB09_OUT']
os.makedirs(OUT, exist_ok=True)

QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], True)
app.initQgis()
QgsGui.editorWidgetRegistry().initEditors()
KEEP = []


def main():
    from processing.core.Processing import Processing
    from processing.gui.AlgorithmDialog import AlgorithmDialog
    Processing.initialize()
    proj = QgsProject.instance()
    proj.setCrs(QgsCoordinateReferenceSystem('EPSG:26912'))
    lyr = QgsVectorLayer(os.path.join(DATA, 'idaho_road_reproj.shp'), 'idaho_road_reproj', 'ogr')
    assert lyr.isValid(), 'roads layer invalid'
    proj.addMapLayer(lyr)
    KEEP.append(lyr)

    alg = QgsApplication.processingRegistry().algorithmById('qgis:selectbyattribute')
    assert alg is not None, 'Select by attribute algorithm not found'
    d = AlgorithmDialog(alg.create(), False, None)
    KEEP.append(d)
    d.resize(1000, 700)
    d.show()
    app.processEvents()

    # point the Selection attribute at "name", which is what Lab 9 step 39 uses
    for cb in d.findChildren(QComboBox):
        for i in range(cb.count()):
            if cb.itemText(i).strip().lower() == 'name':
                cb.setCurrentIndex(i)
                break
    app.processEvents()

    wanted = {'input': 'INPUT', 'attribute': 'FIELD', 'value': 'VALUE'}
    rects = {}
    scale = d.devicePixelRatioF()
    for key, obj in wanted.items():
        w = d.findChild(QWidget, obj)
        if w is None or not w.isVisible():
            print('  (no visible widget %s)' % obj)
            continue
        tl = w.mapTo(d, w.rect().topLeft())
        rects[key] = [round(tl.x() * scale), round(tl.y() * scale),
                      round(w.width() * scale), round(w.height() * scale)]
    pm = d.grab()
    pm.save(os.path.join(OUT, 'lab09-select-by-attribute.png'))
    with open(os.path.join(OUT, 'lab09-select-by-attribute.json'), 'w') as f:
        json.dump(rects, f, indent=1)
    print('lab09-select-by-attribute  %d x %d  rects: %s' % (pm.width(), pm.height(), sorted(rects)))
    app.quit()


QTimer.singleShot(1200, main)
app.exec_()
