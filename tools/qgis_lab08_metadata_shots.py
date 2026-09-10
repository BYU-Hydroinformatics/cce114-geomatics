# Lab 8 metadata screenshots (QGIS 3.44 LTR), captured without a running QGIS session.
#
# Lab 8 shipped with no figures at all beyond the title banner, and said so in the text: "There are
# also no QGIS screenshots for this lab yet". Its steps walk through five tabs of the Layer
# Properties Metadata panel, which is exactly the kind of thing a script can stage reliably.
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   for s in $(python3 tools/qgis_lab08_metadata_shots.py --list); do
#     LAB08_DATA=<dir with a polygon layer> LAB08_OUT=<out dir> SHOT=$s \
#       /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_lab08_metadata_shots.py
#   done
#
# One shot per process: several property dialogs in one headless process crash partway through.
# The Mac must be in Light appearance, for the reason tools/lab0304-improvement-plan.md explains.
import json
import os
import sys

SHOTS = ['identification', 'access', 'extent', 'contact', 'history']

if '--list' in sys.argv:
    print(' '.join(SHOTS))
    raise SystemExit

from qgis.core import (QgsApplication, QgsVectorLayer, QgsProject, QgsStyle,
                       QgsCoordinateReferenceSystem, QgsLayerMetadata, QgsBox3d, QgsDateTimeRange,
                       QgsAbstractMetadataBase)
from qgis.gui import QgsGui, QgsMapCanvas, QgsMessageBar, QgsVectorLayerProperties
from qgis.PyQt.QtCore import QTimer, QDateTime, QDate, QTime
from qgis.PyQt.QtWidgets import QWidget, QTabWidget, QApplication

DATA = os.environ.get('LAB08_DATA')
OUT = os.environ.get('LAB08_OUT')
SHOT = os.environ.get('SHOT')
assert DATA and OUT and SHOT, 'set LAB08_DATA, LAB08_OUT and SHOT'
os.makedirs(OUT, exist_ok=True)

QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], True)
app.initQgis()
QgsGui.editorWidgetRegistry().initEditors()
if QgsStyle.defaultStyle().symbolCount() == 0:
    QgsStyle.defaultStyle().importXml(QgsApplication.defaultStylePath())

CRS = QgsCoordinateReferenceSystem('EPSG:26912')
QgsProject.instance().setCrs(CRS)
KEEP = []          # dialogs do not own the canvas or message bar handed to them


def metadata_for(layer):
    """Fill in the metadata Lab 8 steps 11 to 15 have students type."""
    md = layer.metadata()
    md.setTitle('Lehi Project Wetland Boundaries')
    md.setAbstract('Wetland boundary polygon mapped by the project survey crew with a handheld '
                   'GNSS receiver, collected to identify wetlands that the proposed 1900 South '
                   'freeway alignment should avoid.')
    md.setLicenses(['Creative Commons Attribution 4.0'])
    md.setCrs(CRS)
    contact = QgsAbstractMetadataBase.Contact()
    contact.name = 'Your Name'
    contact.organization = 'Transportation Firm'
    contact.email = 'you@example.com'
    contact.role = 'Point of contact'
    md.setContacts([contact])
    created = QgsAbstractMetadataBase.Link()
    md.addHistoryItem('Created 2024-10-28 by the project survey crew')
    md.addHistoryItem('Published ' + QDate.currentDate().toString('yyyy-MM-dd'))
    layer.setMetadata(md)
    return layer


def main():
    path = os.path.join(DATA, 'Lehi_wetlands01.shp')
    lyr = QgsVectorLayer(path, 'Lehi_wetlands01', 'ogr')
    assert lyr.isValid(), 'invalid layer: ' + path
    QgsProject.instance().addMapLayer(lyr)
    metadata_for(lyr)

    canvas = QgsMapCanvas()
    canvas.setDestinationCrs(CRS)
    canvas.setLayers([lyr])
    canvas.zoomToFullExtent()
    bar = QgsMessageBar()
    KEEP.extend([canvas, bar, lyr])
    dlg = QgsVectorLayerProperties(canvas, bar, lyr)
    KEEP.append(dlg)
    dlg.setCurrentPage('mOptsPage_Metadata')
    dlg.resize(1180, 860)
    dlg.show()
    app.processEvents()

    # The Metadata page carries its own QTabWidget (Identification, Categories, Keywords, Access,
    # Extent, Contact, Links, History, Validation), not a list down the side like the outer page.
    picked = False
    for tw in dlg.findChildren(QTabWidget):
        names = [tw.tabText(i).strip().lower() for i in range(tw.count())]
        if 'identification' not in names:
            continue
        for i, n in enumerate(names):
            if n.startswith(SHOT):
                tw.setCurrentIndex(i)
                picked = True
                break
        if picked:
            break
    if not picked:
        print('  (no metadata tab called %r)' % SHOT)
    app.processEvents()

    pm = dlg.grab()
    name = 'metadata-' + SHOT
    pm.save(os.path.join(OUT, name + '.png'))
    print('%-28s %d x %d' % (name, pm.width(), pm.height()))
    app.quit()


QTimer.singleShot(1200, main)
app.exec_()
