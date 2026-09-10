# Lab 3 and Lab 4 dialog screenshots (QGIS 3.44 LTR), captured without a running QGIS session.
#
# Same pattern as tools/qgis_lab02_dialog_shots.py: drive QGIS's bundled Python from a terminal,
# stage each dialog the way the lab step describes, and grab it with QWidget.grab() at native
# Retina 2x. One shot per process, because opening and closing several property dialogs in one
# headless process crashes partway through.
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   for s in $(python3 tools/qgis_lab0304_dialog_shots.py --list); do
#     LAB34_DATA=<data dir> LAB34_OUT=<out dir> SHOT=$s \
#       /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_lab0304_dialog_shots.py
#   done
#
# LAB34_DATA holds points.csv, pts_corrected.shp, campus.shp and SF_Waterways.gpkg, built by the
# commands in tools/lab0304-improvement-plan.md. Keep both directories outside ~/Desktop,
# ~/Documents and ~/Downloads: QGIS cannot read or write there on macOS. Red annotation boxes are
# added afterwards by tools/lab0304_annotate.py, from the widget rectangles saved next to each PNG.
import json
import os
import sys

# The Data Source Manager and the Snapping toolbar are not exposed to Python outside a running
# QGIS in 3.44, so those two live in tools/qgis_lab0304_window_shots.py instead.
SHOTS = ['lab3-save-features-as', 'lab3-new-shapefile-dialog',
         'lab3-feature-attributes', 'lab3-field-calculator', 'lab3-attribute-table',
         'lab4-new-geopackage-point', 'lab4-new-geopackage-polygon',
         'lab4-field-calculator', 'lab4-field-calculator-update']

if '--list' in sys.argv:
    print(' '.join(SHOTS))
    raise SystemExit

from qgis.core import (QgsApplication, QgsVectorLayer, QgsProject, QgsStyle, QgsField,
                       QgsCoordinateReferenceSystem, QgsFeature, QgsGeometry, QgsPointXY,
                       QgsVectorLayerUtils, QgsSnappingConfig, QgsTolerance, QgsVectorLayerCache)
from qgis.gui import (QgsGui, QgsMapCanvas, QgsMessageBar, QgsAttributeDialog,
                      QgsAttributeEditorContext, QgsFieldCalculator, QgsAttributeTableView)
from qgis.PyQt.QtCore import QTimer, QVariant, Qt
from qgis.PyQt.QtWidgets import (QWidget, QLineEdit, QComboBox, QPushButton, QCheckBox,
                                 QToolButton, QApplication, QDialog, QVBoxLayout)
import sip

# Shown in the File name box of the layer-creation dialogs; nothing is written there.
DISPLAY_DIR = os.environ.get('LAB34_DISPLAY_DIR', '/Users/student/CCE114/Lab4')
DATA = os.environ.get('LAB34_DATA')
OUT = os.environ.get('LAB34_OUT')
SHOT = os.environ.get('SHOT')
assert DATA and OUT and SHOT, 'set LAB34_DATA, LAB34_OUT and SHOT'
os.makedirs(OUT, exist_ok=True)

QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], True)
app.initQgis()
QgsGui.editorWidgetRegistry().initEditors()
st = QgsStyle.defaultStyle()
if st.symbolCount() == 0:
    st.importXml(QgsApplication.defaultStylePath())

CRS = QgsCoordinateReferenceSystem('EPSG:26912')
proj = QgsProject.instance()
proj.setCrs(CRS)

# QGIS dialogs do not take ownership of the canvas or message bar they are handed, so anything
# passed in has to outlive the dialog or the process segfaults on grab().
KEEP = []


def canvas_for(layer):
    c = QgsMapCanvas()
    c.setDestinationCrs(CRS)
    c.setLayers([layer])
    c.zoomToFullExtent()
    KEEP.append(c)
    return c


def load(path, name, provider='ogr'):
    l = QgsVectorLayer(os.path.join(DATA, path), name, provider)
    assert l.isValid(), 'invalid layer: ' + path
    proj.addMapLayer(l)
    KEEP.append(l)
    return l


def rects(widget, wanted):
    out = {}
    scale = widget.devicePixelRatioF()
    for key, obj in (wanted or {}).items():
        w = widget.findChild(QWidget, obj)
        if w is None or not w.isVisible():
            print('  (no visible widget %s for %s)' % (obj, key))
            continue
        tl = w.mapTo(widget, w.rect().topLeft())
        out[key] = [round(tl.x() * scale), round(tl.y() * scale),
                    round(w.width() * scale), round(w.height() * scale)]
    return out


def save(dlg, name, wanted=None):
    app.processEvents()
    pm = dlg.grab()
    pm.save(os.path.join(OUT, name + '.png'))
    if wanted:
        with open(os.path.join(OUT, name + '.json'), 'w') as f:
            json.dump(rects(dlg, wanted), f, indent=1)
    print('%-32s %d x %d' % (name, pm.width(), pm.height()))


def show(dlg, w, h):
    KEEP.append(dlg)
    dlg.resize(w, h)
    dlg.show()
    app.processEvents()
    return dlg


def set_file(parent, obj, path):
    """Set a QgsFileWidget's path. sip returns it as a plain QWidget, so cast first."""
    from qgis.gui import QgsFileWidget
    w = parent.findChild(QWidget, obj)
    if w is None:
        print('  (no file widget %s)' % obj)
        return
    sip.cast(w, QgsFileWidget).setFilePath(path)


def set_crs(parent, obj, crs):
    """Set a QgsProjectionSelectionWidget, which also comes back as a plain QWidget."""
    from qgis.gui import QgsProjectionSelectionWidget
    w = parent.findChild(QWidget, obj)
    if w is None:
        print('  (no crs widget %s)' % obj)
        return
    sip.cast(w, QgsProjectionSelectionWidget).setCrs(crs)


def set_expression(dlg, text):
    """Type an expression into the Field Calculator.

    The editor is a QScintilla widget, not a QTextEdit, so it has setText and not setPlainText,
    and QgsExpressionBuilderWidget does not come back from findChildren as itself.
    """
    from qgis.PyQt.Qsci import QsciScintilla
    for w in dlg.findChildren(QsciScintilla):
        if w.isVisible():
            w.setText(text)
            app.processEvents()
            got = w.text().strip()
            if got != text:
                print('  (expression did not stick: %r)' % got)
            return
    print('  (no expression editor found)')


def set_combo(parent, obj, needle):
    cb = parent.findChild(QComboBox, obj)
    if cb is None:
        print('  (no combo %s)' % obj)
        return
    for i in range(cb.count()):
        if needle.lower() in cb.itemText(i).lower():
            cb.setCurrentIndex(i)
            return
    print('  (no item like %r in %s)' % (needle, obj))


# ------------------------------------------------------------ Lab 3, Part 2 step 11-12
def lab3_save_features_as():
    from qgis.gui import QgsVectorLayerSaveAsDialog
    lyr = load('pts_corrected.shp', 'points')
    d = QgsVectorLayerSaveAsDialog(lyr)
    show(d, 1000, 860)
    save(d, 'lab3-save-features-as', {'format': 'mFormatComboBox', 'crs': 'mCrsSelector',
                                      'filename': 'mFilename'})


# ------------------------------------------------------------ Lab 3, Part 2 step 23-24
def lab3_new_shapefile_dialog():
    from qgis.gui import QgsNewVectorLayerDialog
    d = QgsNewVectorLayerDialog()
    show(d, 940, 820)
    set_file(d, 'mFileName', os.path.join(DISPLAY_DIR, 'campus.shp'))
    set_combo(d, 'mGeometryTypeBox', 'Polygon')
    set_crs(d, 'mCrsSelector', CRS)
    app.processEvents()
    save(d, 'lab3-new-shapefile-dialog', {'geometry': 'mGeometryTypeBox', 'crs': 'mCrsSelector',
                                          'filename': 'mFileName'})


# ------------------------------------------------------------ Lab 3, Part 2 step 19
def lab3_feature_attributes():
    lyr = load('pts_corrected.shp', 'pts_corrected')
    feat = QgsVectorLayerUtils.createFeature(lyr)
    feat.setAttribute('name', 'favorite')
    feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(444700, 4455480)))
    ctx = QgsAttributeEditorContext()
    ctx.setMapCanvas(canvas_for(lyr))
    d = QgsAttributeDialog(lyr, feat, False, None, True, ctx)
    show(d, 700, 460)
    save(d, 'lab3-feature-attributes', {})


# ------------------------------------------------------------ Lab 3, Part 2 step 30-31
def lab3_field_calculator():
    lyr = load('campus.shp', 'campus')
    d = QgsFieldCalculator(lyr)
    show(d, 1120, 900)
    for le in d.findChildren(QLineEdit):
        if le.objectName() == 'mOutputFieldNameLineEdit':
            le.setText('area')
    set_combo(d, 'mOutputFieldTypeComboBox', 'Decimal')
    set_expression(d, '$area')
    # The expression editor is the QScintilla widget QGIS names txtPython inside this dialog.
    save(d, 'lab3-field-calculator', {'name': 'mOutputFieldNameLineEdit',
                                      'type': 'mOutputFieldTypeComboBox',
                                      'expression': 'txtPython'})


# ------------------------------------------------------------ Lab 3, Part 2 step 33-34
def lab3_attribute_table():
    from qgis.gui import QgsAttributeTableModel, QgsAttributeTableFilterModel
    lyr = load('campus_area.shp', 'campus')
    cache = QgsVectorLayerCache(lyr, 1000)
    canvas = canvas_for(lyr)
    model = QgsAttributeTableModel(cache)
    model.loadLayer()
    fmodel = QgsAttributeTableFilterModel(canvas, model)
    view = QgsAttributeTableView()
    view.setModel(fmodel)
    KEEP.extend([cache, model, fmodel, view])
    holder = QDialog()
    holder.setWindowTitle('campus — Features Total: 1, Filtered: 1, Selected: 0')
    lay = QVBoxLayout(holder)
    lay.addWidget(view)
    show(holder, 900, 300)
    save(holder, 'lab3-attribute-table', {})


# ------------------------------------------------------------ Lab 4 Phase 1 steps 5-9
def _new_gpkg(name, geometry, fields, out_name, w=980, h=1080):
    from qgis.gui import QgsNewGeoPackageLayerDialog
    d = QgsNewGeoPackageLayerDialog()
    show(d, w, h)
    # A short, plausible path reads better in a figure than the capture machine's scratch dir.
    set_file(d, 'mFileName', os.path.join(DISPLAY_DIR, name + '.gpkg'))
    for obj in ('mTableNameEdit', 'mLayerIdentifierEdit'):
        le = d.findChild(QLineEdit, obj)
        if le is not None:
            le.setText(name)
    set_combo(d, 'mGeometryTypeBox', geometry)
    set_crs(d, 'mCrsSelector', CRS)
    app.processEvents()
    # Fill the schema the way step 9 describes: type each field, pick its type, then click
    # "Add to Fields List". The button is a QToolButton, not a QPushButton.
    add = d.findChild(QToolButton, 'mAddAttributeButton')
    for fname, ftype in fields:
        fe = d.findChild(QLineEdit, 'mFieldNameEdit')
        if fe is None or add is None:
            print('  (cannot reach the field editor)')
            break
        fe.setText(fname)
        set_combo(d, 'mFieldTypeBox', ftype)
        app.processEvents()
        add.click()
        app.processEvents()
    tree = d.findChild(QWidget, 'mAttributeView')
    n = tree.topLevelItemCount() if hasattr(tree, 'topLevelItemCount') else -1
    print('  fields added to the list: %d of %d' % (n, len(fields)))
    save(d, out_name, {'geometry': 'mGeometryTypeBox', 'filename': 'mFileName',
                       'fields': 'mAttributeView', 'add': 'mAddAttributeButton',
                       'crs': 'mCrsSelector', 'tablename': 'mTableNameEdit'})


def lab4_new_geopackage_point():
    _new_gpkg('Street_Lights', 'Point',
              [('ID', 'Integer'), ('Fixture_Type', 'Text'), ('Voltage', 'Integer')],
              'lab4-new-geopackage-point')


def lab4_new_geopackage_polygon():
    _new_gpkg('Temple_Footprint', 'Polygon', [('Name', 'Text')],
              'lab4-new-geopackage-polygon')


# ------------------------------------------------------------ Lab 4 Phase 2 steps 16-18, 21
def _lab4_calc(update_existing, out_name):
    lyr = load('temple_footprint.shp', 'Temple_Footprint')
    d = QgsFieldCalculator(lyr)
    show(d, 1120, 940)
    cb = d.findChild(QCheckBox, 'mUpdateExistingGroupBox') or d.findChild(QWidget, 'mUpdateExistingGroupBox')
    if update_existing and cb is not None and hasattr(cb, 'setChecked'):
        cb.setChecked(True)
        app.processEvents()
        set_combo(d, 'mExistingFieldComboBox', 'area')
    else:
        for le in d.findChildren(QLineEdit):
            if le.objectName() == 'mOutputFieldNameLineEdit':
                le.setText('area')
        set_combo(d, 'mOutputFieldTypeComboBox', 'Decimal')
    set_expression(d, '$area * 10.7639')
    save(d, out_name, {'name': 'mOutputFieldNameLineEdit', 'type': 'mOutputFieldTypeComboBox',
                       'expression': 'txtPython', 'update': 'mUpdateExistingGroupBox',
                       'existing': 'mExistingFieldComboBox'})


def lab4_field_calculator():
    _lab4_calc(False, 'lab4-field-calculator')


def lab4_field_calculator_update():
    _lab4_calc(True, 'lab4-field-calculator-update')


FUNCS = {
    'lab3-save-features-as': lab3_save_features_as,
    'lab3-new-shapefile-dialog': lab3_new_shapefile_dialog,
    'lab3-feature-attributes': lab3_feature_attributes,
    'lab3-field-calculator': lab3_field_calculator,
    'lab3-attribute-table': lab3_attribute_table,
    'lab4-new-geopackage-point': lab4_new_geopackage_point,
    'lab4-new-geopackage-polygon': lab4_new_geopackage_polygon,
    'lab4-field-calculator': lab4_field_calculator,
    'lab4-field-calculator-update': lab4_field_calculator_update,
}


def main():
    assert SHOT in FUNCS, 'SHOT must be one of: ' + ', '.join(FUNCS)
    FUNCS[SHOT]()
    app.quit()


QTimer.singleShot(1200, main)
app.exec_()
