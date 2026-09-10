# Lab 2 dialog screenshots (QGIS 3.44 LTR), captured without a running QGIS session.
#
# Drives QGIS's bundled Python from a terminal, the same way tools/qgis_lab01_symbology_shot.py
# does, so no QGIS window opens and no screen-recording permission is needed. Each dialog is
# staged by setting the renderer/labeling on the layer first, then opening Layer Properties on
# the page that the lab step talks about, and grabbing it with QWidget.grab() at native Retina 2x.
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   for s in crs-dialog point-symbology point-svg-marker roads-categorized \
#            roads-merged-highway municipalities-graduated layer-rendering-opacity labels-tab; do
#     LAB02_DATA=<data dir> LAB02_OUT=<out dir> SHOT=$s \
#       /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_lab02_dialog_shots.py
#   done
#
# One shot per process on purpose: opening and closing several property dialogs in a single
# headless process crashes partway through.
#
# LAB02_DATA holds the three UGRC shapefile downloads (Municipalities, AirportLocations, Roads).
# Keep both directories outside ~/Desktop, ~/Documents and ~/Downloads: QGIS cannot read or write
# there on macOS. Red annotation boxes are added afterwards by tools/lab02_annotate.py.
# QWidget.grab() does not include the macOS title bar, which is why these shots have none.
import os, sys, json
from qgis.core import (QgsApplication, QgsVectorLayer, QgsProject, QgsStyle, QgsSymbol,
                       QgsMarkerSymbol, QgsLineSymbol, QgsFillSymbol, QgsSvgMarkerSymbolLayer,
                       QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsSingleSymbolRenderer,
                       QgsGraduatedSymbolRenderer, QgsCoordinateReferenceSystem,
                       QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings,
                       QgsVectorLayerSimpleLabeling, QgsClassificationQuantile)
from qgis.gui import (QgsGui, QgsMapCanvas, QgsMessageBar, QgsVectorLayerProperties,
                      QgsProjectionSelectionDialog, QgsCollapsibleGroupBoxBasic,
                      QgsFieldExpressionWidget)
from qgis.PyQt.QtCore import QTimer, Qt
from qgis.PyQt.QtGui import QColor, QFont
from qgis.PyQt.QtWidgets import (QWidget, QLineEdit, QGroupBox, QTreeView, QScrollArea,
                                 QPushButton, QComboBox, QApplication)
import sip

DATA = os.environ.get('LAB02_DATA')
OUT = os.environ.get('LAB02_OUT')
assert DATA and OUT, 'set LAB02_DATA and LAB02_OUT'
os.makedirs(OUT, exist_ok=True)

QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], True)
app.initQgis()
QgsGui.editorWidgetRegistry().initEditors()
st = QgsStyle.defaultStyle()
if st.symbolCount() == 0:
    st.importXml(QgsApplication.defaultStylePath())

proj = QgsProject.instance()
proj.setCrs(QgsCoordinateReferenceSystem('EPSG:26912'))

def load(sub, fn, name):
    l = QgsVectorLayer(os.path.join(DATA, sub, fn), name, 'ogr')
    assert l.isValid(), 'invalid layer: ' + fn
    proj.addMapLayer(l)
    return l

apt = load('airports', 'AirportLocations.shp', 'Airports')
rds = load('roads', 'Roads.shp', 'Roads')
mun = load('municipal', 'Municipalities.shp', 'Municipalities')
HWY = ('1', '2', '3', '4', '5')

def uncollapse(w, *object_names):
    """Expand a collapsible group box by objectName.

    sip hands these back as plain QGroupBox wrappers, which have no setCollapsed, so cast to
    QgsCollapsibleGroupBoxBasic first.
    """
    for n in object_names:
        gb = w.findChild(QGroupBox, n)
        if gb is None:
            print('  (no group box named %s)' % n)
            continue
        sip.cast(gb, QgsCollapsibleGroupBoxBasic).setCollapsed(False)

# QgsVectorLayerProperties does not take ownership of the canvas or the message bar, so both
# must outlive the dialog. Letting them fall out of scope segfaults the process on grab().
KEEP = []
FILTER_NAME = []

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

def rects(dlg, wanted):
    """Record where named widgets sit inside the grabbed pixmap.

    tools/lab02_annotate.py draws the red boxes from this, so the annotations cannot drift when
    a dialog is re-captured at a different size.
    """
    out = {}
    scale = dlg.devicePixelRatioF()
    for key, obj in wanted.items():
        w = dlg.findChild(QWidget, obj)
        if w is None or not w.isVisible():
            print('  (no visible widget %s for %s)' % (obj, key))
            continue
        tl = w.mapTo(dlg, w.rect().topLeft())
        out[key] = [round(tl.x() * scale), round(tl.y() * scale),
                    round(w.width() * scale), round(w.height() * scale)]
    return out

def save(dlg, name, wanted=None):
    app.processEvents()
    pm = dlg.grab()
    path = os.path.join(OUT, name + '.png')
    pm.save(path)
    if wanted:
        with open(os.path.join(OUT, name + '.json'), 'w') as f:
            json.dump(rects(dlg, wanted), f, indent=1)
    print('%-34s %d x %d' % (name, pm.width(), pm.height()))

# ---------------------------------------------------------------- steps 3-4: project CRS
def shot_crs():
    d = QgsProjectionSelectionDialog()
    KEEP.append(d)
    d.setCrs(QgsCoordinateReferenceSystem('EPSG:26912'))
    d.resize(900, 720)
    d.show()
    app.processEvents()
    for le in d.findChildren(QLineEdit):
        if 'filter' in le.objectName().lower() or 'search' in le.objectName().lower():
            le.setText('26912')
            FILTER_NAME.append(le.objectName())
            break
    app.processEvents()
    save(d, 'crs-dialog', {'filter': FILTER_NAME[0]} if FILTER_NAME else None)

# ---------------------------------------------------------- steps 11-14: point symbology
def airport_symbol(with_svg):
    sym = QgsMarkerSymbol.createSimple(
        {'name': 'circle', 'color': '#1a7f37', 'outline_color': '#ffffff',
         'outline_width': '0.4', 'size': '3.4'})
    if with_svg:
        plane = None
        for root in QgsApplication.svgPaths():
            cand = os.path.join(root, 'gpsicons', 'plane.svg')
            if os.path.exists(cand):
                plane = cand
                break
        if plane:
            sl = QgsSvgMarkerSymbolLayer(plane)
            sl.setSize(2.2)
            sl.setFillColor(QColor('#ffffff'))
            sym.appendSymbolLayer(sl)
    return sym

def shot_point_simple():
    apt.setRenderer(QgsSingleSymbolRenderer(airport_symbol(False)))
    save(props(apt, 'mOptsPage_Style', h=820), 'point-symbology',
         {'add-layer': 'btnAddLayer', 'symbol-tree': 'layersTree'})

def shot_point_svg():
    apt.setRenderer(QgsSingleSymbolRenderer(airport_symbol(True)))
    def prep(d):
        # Select the SVG Marker row so the dialog shows the SVG image browser, which is what
        # step 13 asks students to look at.
        for tv in d.findChildren(QTreeView):
            if tv.objectName() != 'layersTree':
                continue
            tv.expandAll()
            m = tv.model()
            if m is None or m.rowCount() == 0:
                continue
            top = m.index(0, 0)
            if m.rowCount(top):
                tv.setCurrentIndex(m.index(0, 0, top))
            break
        # Scroll the properties pane to the bottom so the SVG image browser is on screen.
        app.processEvents()
        for sa in d.findChildren(QScrollArea):
            b = sa.verticalScrollBar()
            if b.maximum() > 0:
                b.setValue(b.maximum())
    save(props(apt, 'mOptsPage_Style', h=900, prep=prep), 'point-svg-marker',
         {'symbol-tree': 'layersTree'})

# ------------------------------------------------------- steps 17-21: categorized roads
def shot_roads_classified():
    # Drive the real widget rather than building the renderer by hand: switch the dropdown to
    # Categorized, set the field, then press Classify. That way the shot shows exactly what the
    # button produces, including QGIS's own "all other values" row and its category ordering.
    rds.setRenderer(QgsSingleSymbolRenderer(
        QgsLineSymbol.createSimple({'color': '#8f8f8f', 'width': '0.26'})))

    def prep(d):
        cbo = d.findChild(QComboBox, 'cboRenderers')
        for i in range(cbo.count()):
            if cbo.itemText(i) == 'Categorized':
                cbo.setCurrentIndex(i)
                break
        app.processEvents()
        # The Value selector comes back from sip as a plain QWidget named mExpressionWidget, so
        # find it inside the categorized page and cast it before setting the field.
        btn = d.findChild(QPushButton, 'btnAddCategories')
        assert btn is not None, 'Classify button not found'
        cat = btn.parent()
        fw = sip.cast(cat.findChild(QWidget, 'mExpressionWidget'), QgsFieldExpressionWidget)
        fw.setField('CARTOCODE')
        app.processEvents()
        assert fw.currentField()[0] == 'CARTOCODE', 'field not set: %r' % (fw.currentField(),)
        btn.click()
        app.processEvents()

    save(props(rds, 'mOptsPage_Style', h=920, prep=prep), 'roads-categorized',
         {'value': 'mExpressionWidget', 'classify': 'btnAddCategories',
          'categories': 'viewCategories', 'delete': 'btnDeleteCategories'})

def shot_roads_merged():
    s = QgsLineSymbol.createSimple({'color': '#ffef3f', 'width': '0.75'})
    # The end state of steps 19 to 21: everything except cartocodes 1-5 deleted, including the
    # "all other values" row Classify leaves behind, and 1-5 merged into a single Highway
    # category. With no catch-all category the other roads simply do not draw.
    merged = QgsRendererCategory(list(HWY), s, 'Highway')
    rds.setRenderer(QgsCategorizedSymbolRenderer('CARTOCODE', [merged]))
    save(props(rds, 'mOptsPage_Style', h=700), 'roads-merged-highway',
         {'categories': 'viewCategories'})

# ------------------------------------------------ steps 23-28: graduated municipalities
def graduated():
    # Green for the small towns, as the lab's narrative describes, so the ramp is inverted.
    ramp = QgsStyle.defaultStyle().colorRamp('RdYlGn')
    ramp.invert()
    r = QgsGraduatedSymbolRenderer('POPLASTEST')
    method = QgsClassificationQuantile()
    method.setLabelPrecision(0)
    method.setLabelTrimTrailingZeroes(True)
    r.setClassificationMethod(method)
    r.setSourceSymbol(QgsFillSymbol.createSimple(
        {'color': '#cccccc', 'outline_color': '#ffffff', 'outline_width': '0.26'}))
    r.updateClasses(mun, 5)
    r.updateColorRamp(ramp.clone())
    return r

def shot_graduated():
    mun.setRenderer(graduated())
    # Wider than the other shots: at 1240 the Legend format row squeezes the word
    # "Precision" down to "ecision (".
    save(props(mun, 'mOptsPage_Style', w=1500, h=860), 'municipalities-graduated',
         {'value': 'mExpressionWidget', 'classify': 'btnAddCategories',
          'precision': 'spinPrecision', 'classes': 'spinGraduatedClasses',
          'mode': 'cboGraduatedMode'})

def shot_opacity():
    mun.setRenderer(graduated())
    mun.setOpacity(0.45)
    def prep(d):
        uncollapse(d, 'mLayerRenderingGroupBox')
    save(props(mun, 'mOptsPage_Style', h=940, prep=prep), 'layer-rendering-opacity',
         {'opacity': 'mOpacityWidget'})

# ------------------------------------------------------------ steps 30-33: labels
def shot_labels():
    ls = QgsPalLayerSettings()
    ls.fieldName = 'NAME'
    ls.enabled = True
    tf = QgsTextFormat()
    f = QFont('Helvetica', 10)
    tf.setFont(f)
    tf.setSize(10)
    buf = QgsTextBufferSettings()
    buf.setEnabled(True)
    buf.setSize(1.0)
    buf.setColor(QColor('white'))
    tf.setBuffer(buf)
    ls.setFormat(tf)
    mun.setLabeling(QgsVectorLayerSimpleLabeling(ls))
    mun.setLabelsEnabled(True)
    def prep(d):
        for w in d.findChildren(QWidget):
            if w.objectName() == 'mLabelingOptionsListWidget' and hasattr(w, 'setCurrentRow'):
                for i in range(w.count()):
                    if 'buffer' in w.item(i).text().lower():
                        w.setCurrentRow(i)
                        break
    save(props(mun, 'mOptsPage_Labels', h=940, prep=prep), 'labels-tab',
         {'mode': 'mLabelModeComboBox', 'sections': 'mLabelingOptionsListWidget'})

SHOTS = {
    'crs-dialog': shot_crs,
    'point-symbology': shot_point_simple,
    'point-svg-marker': shot_point_svg,
    'roads-categorized': shot_roads_classified,
    'roads-merged-highway': shot_roads_merged,
    'municipalities-graduated': shot_graduated,
    'layer-rendering-opacity': shot_opacity,
    'labels-tab': shot_labels,
}

def main():
    # One shot per process: Qt dialogs in this headless setup are not reliable to open and
    # close in sequence, so the caller loops over SHOT values instead.
    want = os.environ.get('SHOT')
    assert want in SHOTS, 'set SHOT to one of: ' + ', '.join(SHOTS)
    SHOTS[want]()
    app.quit()

QTimer.singleShot(1200, main)
app.exec_()
