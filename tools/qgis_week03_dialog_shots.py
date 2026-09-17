# Week 3 hands-on dialog screenshots (QGIS 3.44 LTR), captured without a running QGIS session.
#
# Same approach as tools/qgis_lab02_dialog_shots.py: drives QGIS's bundled Python from a
# terminal, so no window opens and no screen-recording permission is needed. Each dialog is
# staged by setting the renderer/labeling on the layer first, then opening the dialog the
# walkthrough step talks about, and grabbing it with QWidget.grab() at native Retina 2x.
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   for s in single-symbol-states states-categorized states-graduated cities-graduated-size \
#            labels-states labels-cities-expression select-by-expression field-calculator; do
#     WEEK03_DATA=~/week03work WEEK03_OUT=docs/handson/images SHOT=$s \
#       /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_week03_dialog_shots.py
#   done
#
# One shot per process on purpose: opening and closing several property dialogs in a single
# headless process crashes partway through.
#
# WEEK03_DATA is the unzipped "United States Shapefiles.zip" from the Week 3 Thursday entry on
# Learning Suite. Keep it outside ~/Desktop, ~/Documents and ~/Downloads: QGIS cannot read there
# on macOS. Field names are the real ones in that zip, checked against the .dbf on 2026-09-17:
# states carry STATE_NAME / SUB_REGION / POP1990, cities CITY_NAME / POP1990, roads ADMN_CLASS.
# The data is unprojected EPSG:4326 and its population is the 1990 census, which is what
# students see, so nothing here reprojects or substitutes newer numbers.
import os, sys, json
from qgis.core import (QgsApplication, QgsVectorLayer, QgsProject, QgsStyle,
                       QgsMarkerSymbol, QgsLineSymbol, QgsFillSymbol,
                       QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsSingleSymbolRenderer,
                       QgsGraduatedSymbolRenderer, QgsCoordinateReferenceSystem,
                       QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings,
                       QgsVectorLayerSimpleLabeling, QgsClassificationJenks,
                       QgsRendererRangeLabelFormat)
from qgis.gui import (QgsGui, QgsMapCanvas, QgsMessageBar, QgsVectorLayerProperties,
                      QgsCollapsibleGroupBoxBasic, QgsFieldExpressionWidget,
                      QgsExpressionBuilderDialog, QgsExpressionSelectionDialog,
                      QgsExpressionBuilderWidget)
from qgis.PyQt.QtCore import QTimer, QEventLoop
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtWidgets import (QWidget, QGroupBox, QPushButton, QComboBox, QApplication,
                                 QListWidget)
import sip

DATA = os.path.expanduser(os.environ.get('WEEK03_DATA', '~/week03work'))
OUT = os.environ.get('WEEK03_OUT')
assert OUT, 'set WEEK03_OUT'
os.makedirs(OUT, exist_ok=True)
SHP = os.path.join(DATA, 'United States', 'Shapefiles')

QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], True)
app.initQgis()
QgsGui.editorWidgetRegistry().initEditors()
st = QgsStyle.defaultStyle()
if st.symbolCount() == 0:
    st.importXml(QgsApplication.defaultStylePath())

proj = QgsProject.instance()
# The shapefiles are WGS 84 and students do not reproject them, so the figures keep that CRS.
proj.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))

def load(fn, name):
    l = QgsVectorLayer(os.path.join(SHP, fn), name, 'ogr')
    assert l.isValid(), 'invalid layer: ' + fn
    proj.addMapLayer(l)
    return l

states = load('states.shp', 'states')
cities = load('cities.shp', 'cities')
roads = load('roads.shp', 'roads')

# Qt parents are not owned by the dialogs, so anything the dialog borrows must outlive it or
# grab() segfaults with no traceback.
KEEP = []

def props(layer, page, w=1240, h=900, prep=None):
    canvas = QgsMapCanvas()
    canvas.setLayers([layer])
    canvas.zoomToFullExtent()
    bar = QgsMessageBar()
    KEEP.extend([canvas, bar])
    dlg = QgsVectorLayerProperties(canvas, bar, layer)
    KEEP.append(dlg)
    dlg.setCurrentPage(page)
    dlg.resize(w, h)
    dlg.show()
    app.processEvents()
    if prep:
        prep(dlg)
    app.processEvents()
    return dlg

def settle(ms=1800):
    """Let queued work finish. The expression preview loads its sample feature asynchronously,
    so a bare processEvents() grabs the dialog before the preview has evaluated."""
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec_()
    app.processEvents()

def save(dlg, name):
    app.processEvents()
    pm = dlg.grab()
    path = os.path.join(OUT, name + '.png')
    pm.save(path)
    print('%-32s %d x %d  -> %s' % (name, pm.width(), pm.height(), path))

def set_field(dlg, button_name, field):
    """Set the Value field on the symbology page by driving the real widget."""
    btn = dlg.findChild(QPushButton, button_name)
    assert btn is not None, 'button not found: ' + button_name
    page = btn.parent()
    fw = sip.cast(page.findChild(QWidget, 'mExpressionWidget'), QgsFieldExpressionWidget)
    fw.setField(field)
    app.processEvents()
    assert fw.currentField()[0] == field, 'field not set: %r' % (fw.currentField(),)
    return btn

def pick_renderer(dlg, label):
    cbo = dlg.findChild(QComboBox, 'cboRenderers')
    for i in range(cbo.count()):
        if cbo.itemText(i) == label:
            cbo.setCurrentIndex(i)
            break
    else:
        raise AssertionError('renderer not in dropdown: ' + label)
    app.processEvents()

# ------------------------------------------------------------ 1. Single symbols
def shot_single_symbol():
    states.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {'color': '#dbe7d4', 'outline_color': '#6f7d68', 'outline_width': '0.26'})))
    save(props(states, 'mOptsPage_Style', h=820), 'w3-single-symbol-states')

# ------------------------------------------------- 2. Categorized on SUB_REGION
def shot_categorized():
    # Drive the dropdown and press Classify for real, so the shot shows exactly what the button
    # produces -- including the "all other values" row QGIS adds and the walkthrough mentions.
    states.setRenderer(QgsSingleSymbolRenderer(QgsFillSymbol.createSimple(
        {'color': '#cccccc', 'outline_color': '#ffffff', 'outline_width': '0.26'})))
    def prep(d):
        pick_renderer(d, 'Categorized')
        btn = set_field(d, 'btnAddCategories', 'SUB_REGION')
        btn.click()
        app.processEvents()
    save(props(states, 'mOptsPage_Style', h=920, prep=prep), 'w3-states-categorized')

# -------------------------------------------- 3. Graduated on POP1990, Jenks x5
def jenks_renderer():
    ramp = QgsStyle.defaultStyle().colorRamp('Blues')
    r = QgsGraduatedSymbolRenderer('POP1990')
    method = QgsClassificationJenks()
    method.setLabelPrecision(0)
    method.setLabelTrimTrailingZeroes(True)
    r.setClassificationMethod(method)
    r.setSourceSymbol(QgsFillSymbol.createSimple(
        {'color': '#cccccc', 'outline_color': '#ffffff', 'outline_width': '0.2'}))
    r.updateClasses(states, 5)
    r.setLabelFormat(QgsRendererRangeLabelFormat('%1 - %2', 0), True)
    r.updateColorRamp(ramp.clone())
    return r

def shot_graduated():
    states.setRenderer(jenks_renderer())
    # Wider than the rest: below about 1700 the Legend format row clips its own
    # Precision label down to "ecision (".
    save(props(states, 'mOptsPage_Style', w=1760, h=860), 'w3-states-graduated')

# ------------------------------------- 4. Cities graduated by SIZE, not colour
def shot_cities_size():
    r = QgsGraduatedSymbolRenderer('POP1990')
    method = QgsClassificationJenks()
    method.setLabelPrecision(0)
    method.setLabelTrimTrailingZeroes(True)
    r.setClassificationMethod(method)
    r.setSourceSymbol(QgsMarkerSymbol.createSimple(
        {'name': 'circle', 'color': '#c0392b', 'outline_color': '#ffffff',
         'outline_width': '0.2', 'size': '2'}))
    r.setGraduatedMethod(QgsGraduatedSymbolRenderer.GraduatedSize)
    r.updateClasses(cities, 5)
    r.setSymbolSizes(1.0, 6.0)
    r.setLabelFormat(QgsRendererRangeLabelFormat('%1 - %2', 0), True)
    cities.setRenderer(r)
    save(props(cities, 'mOptsPage_Style', w=1760, h=880), 'w3-cities-graduated-size')

# ---------------------------------------------------- 5. Labels tab on states
def state_labels():
    ls = QgsPalLayerSettings()
    ls.fieldName = 'STATE_NAME'
    ls.enabled = True
    tf = QgsTextFormat()
    tf.setFont(QFont('Helvetica', 8))
    tf.setSize(8)
    buf = QgsTextBufferSettings()
    buf.setEnabled(True)
    buf.setSize(1.0)
    buf.setColor(QColor('white'))
    tf.setBuffer(buf)
    ls.setFormat(tf)
    return QgsVectorLayerSimpleLabeling(ls)

def shot_labels_states():
    states.setLabeling(state_labels())
    states.setLabelsEnabled(True)
    def prep(d):
        for w in d.findChildren(QListWidget, 'mLabelingOptionsListWidget'):
            for i in range(w.count()):
                if 'buffer' in w.item(i).text().lower():
                    w.setCurrentRow(i)
                    break
            break
    save(props(states, 'mOptsPage_Labels', h=940, prep=prep), 'w3-labels-states')

# ------------------------------- 6. The CASE WHEN expression in the builder
def shot_label_expression():
    expr = 'CASE WHEN "POP1990" > 500000 THEN "CITY_NAME" END'
    d = QgsExpressionBuilderDialog(cities, expr)
    KEEP.append(d)
    d.resize(1180, 760)
    d.show()
    settle()
    save(d, 'w3-labels-cities-expression')

# ------------------------------------------ 7. Select Features by Expression
def shot_select_by_expression():
    d = QgsExpressionSelectionDialog(cities)
    KEEP.append(d)
    d.setExpressionText('"POP1990" > 1000000')
    d.resize(1100, 700)
    d.show()
    settle()
    save(d, 'w3-select-by-expression')

# --------------------------------------------------------- 8. Field Calculator
def shot_field_calculator():
    from qgis.gui import QgsFieldCalculator
    cities.startEditing()
    d = QgsFieldCalculator(cities)
    KEEP.append(d)
    d.resize(1180, 780)
    d.show()
    app.processEvents()
    # Fill in what step 3 of section 5 asks for: a new decimal field pop_k = POP1990 / 1000.
    for le_name, value in (('mOutputFieldNameLineEdit', 'pop_k'),):
        w = d.findChild(QWidget, le_name)
        if w is not None and hasattr(w, 'setText'):
            w.setText(value)
    for cb in d.findChildren(QComboBox, 'mOutputFieldTypeComboBox'):
        for i in range(cb.count()):
            if 'decimal' in cb.itemText(i).lower():
                cb.setCurrentIndex(i)
                break
        break
    # sip returns the builder as a plain QWidget with none of its own methods; cast it first.
    eb = d.findChild(QWidget, 'builder')
    assert eb is not None, 'expression builder not found'
    sip.cast(eb, QgsExpressionBuilderWidget).setExpressionText('"POP1990" / 1000')
    settle()
    save(d, 'w3-field-calculator')

SHOTS = {
    'single-symbol-states': shot_single_symbol,
    'states-categorized': shot_categorized,
    'states-graduated': shot_graduated,
    'cities-graduated-size': shot_cities_size,
    'labels-states': shot_labels_states,
    'labels-cities-expression': shot_label_expression,
    'select-by-expression': shot_select_by_expression,
    'field-calculator': shot_field_calculator,
}

def main():
    want = os.environ.get('SHOT')
    assert want in SHOTS, 'set SHOT to one of: ' + ', '.join(SHOTS)
    try:
        SHOTS[want]()
    except Exception:
        import traceback; traceback.print_exc()
        sys.stdout.flush()
        os._exit(1)
    sys.stdout.flush()
    # Skip Qt teardown: exitQgis()/normal exit segfaults on this build and pops the macOS
    # crash reporter once per shot.
    os._exit(0)

QTimer.singleShot(1200, main)
app.exec_()
