# Standalone capture of Layer Properties > Symbology for Lab 1 (QGIS 3.44 LTR, no running QGIS needed).
#
# Unlike tools/qgis_reshoot_screens.py this does NOT run inside the QGIS Python console; it drives
# QGIS's bundled Python directly, so it works from a terminal:
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_lab01_symbology_shot.py
#
# Needs Utah_Quaternary_Faults.geojson next to the script (UGRC feature service
# services1.arcgis.com/99lidPhWCzftIe9K .../QuaternaryFaults, paged 2000 at a time). Writes
# out/sym-grab.png at 2x with native macOS chrome (QWidget.grab; QWidget.render drops button
# frames). The default symbol library is imported from symbology-style.xml so the style list is
# what a fresh install shows. Red annotation boxes were added afterwards with PIL; the dialog
# window title bar is not part of the grab. Keep script and output outside ~/Desktop, ~/Documents,
# ~/Downloads (QGIS cannot read there on macOS).
import os, sys
from qgis.core import QgsApplication, QgsVectorLayer, QgsProject, QgsStyle
from qgis.gui import QgsGui, QgsMapCanvas, QgsMessageBar, QgsVectorLayerProperties
from qgis.PyQt.QtCore import QTimer, QSize
from qgis.PyQt.QtGui import QImage, QPainter
from qgis.PyQt.QtWidgets import QWidget

SCR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCR, 'out')
os.makedirs(OUT, exist_ok=True)
QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], True)
app.initQgis()
QgsGui.editorWidgetRegistry().initEditors()
st = QgsStyle.defaultStyle()
if st.symbolCount()==0:
    ok=st.importXml(QgsApplication.defaultStylePath()); print('importXml', ok)
print('symbols', st.symbolCount(), 'favs', len(st.symbolsOfFavorite(QgsStyle.SymbolEntity)))

lyr = QgsVectorLayer(os.path.join(SCR, 'Utah_Quaternary_Faults.geojson'), 'Utah_Quaternary_Faults', 'ogr')
assert lyr.isValid(), 'layer invalid'
QgsProject.instance().addMapLayer(lyr)
canvas = QgsMapCanvas(); canvas.setLayers([lyr]); canvas.zoomToFullExtent()
bar = QgsMessageBar()
dlg = QgsVectorLayerProperties(canvas, bar, lyr)
dlg.setCurrentPage('mOptsPage_Style')
dlg.resize(1000, 880)
dlg.show()

def shoot():
    app.processEvents()
    pm = dlg.grab(); pm.save(os.path.join(OUT, 'sym-grab.png')); print('grab', pm.width(), pm.height())
    print('title:', dlg.windowTitle(), 'size', dlg.size(), 'hint', dlg.sizeHint())
    app.quit()

QTimer.singleShot(2500, shoot)
app.exec_()
