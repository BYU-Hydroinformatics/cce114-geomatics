# Day 22: how Intersection and Union bring both attribute tables into the output.
#
# Builds two tiny synthetic layers in QGIS 3.44 (the same shapes as ws-intersect-simple.png: two
# side-by-side county rectangles and one round catchment across their shared edge), runs the real
# native:intersection and native:union on them, and writes every output feature's attributes and
# geometry to tools/day22-attribute-demo.json. The slide tables and the small maps drawn by
# tools/draw_day22_attribute_figures.py come from that file, so the rows on the slide are what
# QGIS actually produced, not a guess at it. With SHOT=dialog it instead opens the Intersection
# dialog with the two layers chosen and grabs it, plus the rectangles of the field pickers.
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   SHOT=run    /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_day22_attribute_demo.py
#   SHOT=dialog DAY22_OUT=<out dir> /Applications/QGIS.app/Contents/MacOS/python3.12 tools/qgis_day22_attribute_demo.py
#
# The names are invented on purpose (no real county or catchment), like every figure drawn by
# tools/draw_geoprocessing_figures.py. The Mac must be in Light appearance for the dialog shot.
import json
import os
import sys

sys.path.append('/Applications/QGIS.app/Contents/Resources/qgis/python/plugins')

from qgis.core import (Qgis, QgsApplication, QgsVectorLayer, QgsProject, QgsFeature, QgsGeometry,
                       QgsPointXY, QgsCoordinateReferenceSystem)
from qgis.PyQt.QtGui import QTransform
from qgis.gui import QgsGui
from qgis.PyQt.QtCore import QTimer
from qgis.PyQt.QtWidgets import QWidget, QComboBox

SHOT = os.environ.get('SHOT', 'run')
HERE = os.path.dirname(os.path.abspath(__file__))
JSON_OUT = os.path.join(HERE, 'day22-attribute-demo.json')

QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], True)
app.initQgis()
QgsGui.editorWidgetRegistry().initEditors()
KEEP = []

# Same geometry as simple_inputs() in draw_geoprocessing_figures.py, in kilometers.
K = 1000.0
COUNTIES = [(1, 'West County', 'POLYGON((0 1, 2 1, 2 3.6, 0 3.6, 0 1))'),
            (2, 'East County', 'POLYGON((2 1, 4 1, 4 3.6, 2 3.6, 2 1))')]
CATCHMENTS = [('C1', 'Catchment A', (2.0, 1.1, 1.25))]


def scaled(wkt):
    g = QgsGeometry.fromWkt(wkt)
    g.transform(QTransform.fromScale(K, K))
    return g


def build():
    proj = QgsProject.instance()
    proj.setCrs(QgsCoordinateReferenceSystem('EPSG:26912'))
    c = QgsVectorLayer('Polygon?crs=EPSG:26912&field=county_id:integer&field=county:string(20)',
                       'Counties', 'memory')
    feats = []
    for cid, name, wkt in COUNTIES:
        f = QgsFeature(c.fields())
        f.setAttributes([cid, name])
        f.setGeometry(scaled(wkt))
        feats.append(f)
    c.dataProvider().addFeatures(feats)
    w = QgsVectorLayer('Polygon?crs=EPSG:26912&field=catch_id:string(5)&field=catchment:string(20)',
                       'Catchments', 'memory')
    feats = []
    for wid, name, (x, y, r) in CATCHMENTS:
        f = QgsFeature(w.fields())
        f.setAttributes([wid, name])
        f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x * K, y * K)).buffer(r * K, 48))
        feats.append(f)
    w.dataProvider().addFeatures(feats)
    for lyr in (c, w):
        assert lyr.isValid() and lyr.featureCount() > 0
        proj.addMapLayer(lyr)
        KEEP.append(lyr)
    return c, w


def dump(layer):
    names = [f.name() for f in layer.fields()]
    rows = []
    for f in layer.getFeatures():
        g = QgsGeometry(f.geometry())
        g.transform(QTransform.fromScale(1 / K, 1 / K))
        rows.append({'attrs': [None if (v is None or str(v) == 'NULL') else v for v in f.attributes()],
                     'wkt': g.asWkt(4), 'area_km2': round(f.geometry().area() / 1e6, 3)})
    return {'fields': names, 'rows': rows}


def run():
    from processing.core.Processing import Processing
    import processing
    Processing.initialize()
    c, w = build()
    out = {'qgis': Qgis.version(), 'counties': dump(c), 'catchments': dump(w)}
    for key, alg in (('intersection', 'native:intersection'), ('union', 'native:union')):
        res = processing.run(alg, {'INPUT': c, 'OVERLAY': w, 'OUTPUT': 'memory:'})
        out[key] = dump(res['OUTPUT'])
        print(key, out[key]['fields'], [r['attrs'] for r in out[key]['rows']])
    with open(JSON_OUT, 'w') as f:
        json.dump(out, f, indent=1)
    print('wrote', JSON_OUT)
    sys.stdout.flush()
    os._exit(0)


def dialog():
    from processing.core.Processing import Processing
    from processing.gui.AlgorithmDialog import AlgorithmDialog
    from qgis.gui import QgsProcessingMapLayerComboBox
    Processing.initialize()
    c, w = build()
    out_dir = os.environ['DAY22_OUT']
    os.makedirs(out_dir, exist_ok=True)
    alg = QgsApplication.processingRegistry().algorithmById('native:intersection')
    d = AlgorithmDialog(alg.create(), False, None)
    KEEP.append(d)
    d.resize(1000, 760)
    d.show()
    app.processEvents()
    from qgis.PyQt.QtWidgets import QLabel
    # sip hands the layer pickers back as plain QComboBox; cast them to set a layer.
    import sip
    from qgis.gui import QgsMapLayerComboBox
    combos = [sip.cast(x, QgsMapLayerComboBox) for x in d.findChildren(QComboBox) if x.isVisible()]
    assert len(combos) >= 2, 'expected input and overlay layer pickers'
    combos[0].setLayer(c)
    combos[1].setLayer(w)
    app.processEvents()
    if os.environ.get('EXPAND'):
        # open Advanced Parameters, only to confirm where the overlay prefix lives
        from qgis.PyQt.QtWidgets import QToolButton
        d.findChild(QToolButton, 'collapseButton').click()
        app.processEvents()
    scale = d.devicePixelRatioF()

    def rect(wdg):
        tl = wdg.mapTo(d, wdg.rect().topLeft())
        return [round(tl.x() * scale), round(tl.y() * scale),
                round(wdg.width() * scale), round(wdg.height() * scale)]

    # A parameter's label sits directly above its widget in the panel's layout, so each field
    # picker's box runs from the top of its label to the bottom of the next widget below it.
    labels = {x.text(): x for x in d.findChildren(QLabel) if x.isVisible() and x.text()}
    if os.environ.get('LIST'):
        for t, x in labels.items():
            print('L', repr(t), rect(x), flush=True)
    rects = {'INPUT': rect(combos[0]), 'OVERLAY': rect(combos[1])}
    for key, start_txt in (('INPUT_FIELDS', 'Input fields to keep'),
                           ('OVERLAY_FIELDS', 'Overlay fields to keep'),
                           ('OVERLAY_FIELDS_PREFIX', 'Overlay fields prefix')):
        hit = [x for t, x in labels.items() if t.startswith(start_txt)]
        if not hit:
            print('  (no label %s)' % start_txt, flush=True)
            continue
        lab = hit[0]
        parent = lab.parentWidget()
        below = [x for x in parent.findChildren(QWidget, options=__import__('qgis.PyQt.QtCore', fromlist=['Qt']).Qt.FindDirectChildrenOnly)
                 if x.isVisible() and x is not lab and x.geometry().top() >= lab.geometry().bottom() - 2]
        below.sort(key=lambda x: x.geometry().top())
        lr = rect(lab)
        if below:
            br = rect(below[0])
            rects[key] = [min(lr[0], br[0]), lr[1], max(lr[0] + lr[2], br[0] + br[2]) - min(lr[0], br[0]), br[1] + br[3] - lr[1]]
        else:
            rects[key] = lr
    pm = d.grab()
    pm.save(os.path.join(out_dir, 'intersection-dialog.png'))
    with open(os.path.join(out_dir, 'intersection-dialog.json'), 'w') as f:
        json.dump(rects, f, indent=1)
    print('dialog %d x %d rects %s' % (pm.width(), pm.height(), rects))
    sys.stdout.flush()
    os._exit(0)


def guarded():
    # Exit without Qt teardown even on an error: a traceback that falls back into the event loop
    # leaves QGIS to segfault on exit, and macOS then shows a "QGIS quit unexpectedly" dialog.
    try:
        (run if SHOT == 'run' else dialog)()
    except Exception:
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)


QTimer.singleShot(1200, guarded)
app.exec_()
