# qgis_lab04_dialog_shots.py
#
# Stages the Lab 4 dialogs inside a running QGIS and saves them as native-resolution
# (Retina 2x) PNGs using QWidget.grab(), so no screen-recording permission or GUI clicking
# is needed. Produces: crs-dialog.png (annotated), crs-dialog-plain.png,
# street-lights-dialog.png (-> anchored3), database-row.png (-> anchored2, crop the
# bottom sliver), temple-dialog.png (-> anchored5).
#
# How to run (QGIS 3.44 on macOS):
#   1. Set OUT below (or the QGIS_SHOTS_OUT env var) to a writable folder that is NOT under
#      ~/Desktop, ~/Documents or ~/Downloads (macOS privacy protection blocks QGIS there),
#      and put a Lab4.qgz project with a Google Satellite XYZ layer in it.
#   2. Open QGIS, Plugins > Python Console, and run:
#        exec(open('/path/to/qgis_lab04_dialog_shots.py').read())
#   3. Wait ~25 s. Progress and errors go to OUT/drive.log.
#
# The same pattern (find_dialog + findChild by objectName + grab) works for any QGIS dialog;
# use dlg.findChildren(QWidget) and log objectName()s to discover widget names.
import os, traceback
from qgis.PyQt.QtCore import QTimer, Qt, QRect, QPoint
from qgis.PyQt.QtGui import QPainter, QPen, QColor
from qgis.PyQt.QtWidgets import (QApplication, QAction, QDialog, QLineEdit, QComboBox, QLabel,
                                 QListWidget, QWidget, QTreeView, QAbstractButton, QPushButton)
from qgis.core import QgsProject, QgsCoordinateReferenceSystem
from qgis.gui import QgsFileWidget, QgsProjectionSelectionWidget
from qgis.utils import iface

OUT = os.environ.get('QGIS_SHOTS_OUT', os.path.expanduser('~/cce114-shots'))
LAB = '/Users/danames/Desktop/Lab 4'
LOG = os.path.join(OUT, 'drive.log')
PROJECT = os.path.join(OUT, 'Lab4.qgz')
RED = QColor(220, 30, 30)

def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')

def find_dialog(sub):
    for w in QApplication.topLevelWidgets():
        if isinstance(w, QDialog) and w.isVisible() and sub in w.windowTitle():
            return w
    return None

def rect_in(dlg, w, local=None):
    """Geometry of widget w (or a local rect inside w) in dlg coordinates."""
    r = local if local is not None else w.rect()
    tl = w.mapTo(dlg, r.topLeft()); return QRect(tl, r.size())

def annotate(pm, rects, dpr):
    p = QPainter(pm); p.setRenderHint(QPainter.Antialiasing)
    p.setPen(QPen(RED, 3)); p.setBrush(Qt.NoBrush)
    for r in rects:
        p.drawRect(r.adjusted(-4, -4, 4, 4))
    p.end()

def save(pm, name):
    path = os.path.join(OUT, name); pm.save(path)
    log('saved', name, pm.width(), pm.height(), 'dpr', pm.devicePixelRatio())

def combo_select(cb, sub):
    for i in range(cb.count()):
        if sub.lower() in cb.itemText(i).lower():
            cb.setCurrentIndex(i); return cb.itemText(i)
    return None

def step(delay, fn, *args):
    def wrapped():
        try: fn(*args)
        except Exception: log('ERROR in', fn.__name__, traceback.format_exc())
    QTimer.singleShot(delay, wrapped)

# ---- CRS dialog ----
def open_props():
    try:
        QgsCoordinateReferenceSystem.clearRecentCoordinateReferenceSystems(); log('cleared recent CRS list')
    except Exception as e:
        log('could not clear recent CRS:', e)
    QgsProject.instance().setCrs(QgsCoordinateReferenceSystem('EPSG:3857'))
    log('opening project properties')
    iface.actionProjectProperties().trigger()

def config_crs():
    dlg = find_dialog('Project Properties')
    lw = dlg.findChild(QListWidget, 'mOptionsListWidget')
    lw.setCurrentItem(lw.findItems('CRS', Qt.MatchExactly)[0])
    dlg.findChild(QLineEdit, 'leSearch').setText('26912')

def select_crs():
    dlg = find_dialog('Project Properties')
    for tv in dlg.findChildren(QTreeView):
        m = tv.model()
        if m is None: continue
        idxs = m.match(m.index(0, 0), Qt.DisplayRole, 'NAD83 / UTM zone 12N', 1, Qt.MatchExactly | Qt.MatchRecursive)
        if idxs:
            tv.setCurrentIndex(idxs[0]); tv.scrollTo(idxs[0]); tv.setFocus()
            log('selected row in', tv.objectName())

def grab_crs():
    dlg = find_dialog('Project Properties')
    pm = dlg.grab(); dpr = pm.devicePixelRatio()
    rects = []
    le = dlg.findChild(QLineEdit, 'leSearch')
    lbl = [l for l in dlg.findChildren(QLabel) if l.text() == 'Filter' and l.isVisible()]
    r = rect_in(dlg, le)
    if lbl: r = r.united(rect_in(dlg, lbl[0]))
    rects.append(r)
    for tv in dlg.findChildren(QTreeView):
        if tv.objectName() == 'lstCoordinateSystems':
            idx = tv.currentIndex(); vr = tv.visualRect(idx)
            full = QRect(0, vr.top(), tv.viewport().width(), vr.height())
            rects.append(rect_in(dlg, tv.viewport(), full))
    ok = [b for b in dlg.findChildren(QPushButton) if b.text() == 'OK']
    if ok: rects.append(rect_in(dlg, ok[0]))
    log('annotation rects', [(r.x(), r.y(), r.width(), r.height()) for r in rects])
    save(pm, 'crs-dialog-plain.png')
    annotate(pm, rects, dpr); save(pm, 'crs-dialog.png')
    dlg.reject()
    QgsProject.instance().setCrs(QgsCoordinateReferenceSystem('EPSG:26912'))
    log('project crs', QgsProject.instance().crs().authid())

# ---- New GeoPackage Layer dialog ----
def open_gpkg():
    acts = [a for a in iface.mainWindow().findChildren(QAction) if 'geopackage layer' in a.text().replace('&', '').lower()]
    acts[0].trigger()

def config_gpkg(fname, table, geom, fields):
    dlg = find_dialog('New GeoPackage Layer')
    dlg.findChild(QgsFileWidget).setFilePath(os.path.join(LAB, fname))
    dlg.findChild(QLineEdit, 'mTableNameEdit').setText(table)
    log('geom ->', combo_select(dlg.findChild(QComboBox, 'mGeometryTypeBox'), geom))
    sel = [c for c in dlg.findChildren(QWidget) if c.objectName() == 'mCrsSelector'][0]
    log('crs selector type', type(sel).__name__, hasattr(sel, 'setCrs'))
    if hasattr(sel, 'setCrs'): sel.setCrs(QgsProject.instance().crs())
    cb = sel.findChild(QComboBox)
    log('crs combo items', [cb.itemText(i) for i in range(cb.count())])
    if not cb.currentText().startswith('Project CRS'):
        for i in range(cb.count()):
            if cb.itemText(i).startswith('Project CRS'): cb.setCurrentIndex(i); break
    log('crs combo ->', cb.currentText())
    name = dlg.findChild(QLineEdit, 'mFieldNameEdit'); typ = dlg.findChild(QComboBox, 'mFieldTypeBox')
    add = dlg.findChild(QAbstractButton, 'mAddAttributeButton')
    for n, t in fields:
        name.setText(n); log('field', n, combo_select(typ, t)); add.click()
    name.setText(''); combo_select(typ, 'text')

def grab_gpkg(fname, crop_name=None):
    dlg = find_dialog('New GeoPackage Layer')
    pm = dlg.grab(); dpr = pm.devicePixelRatio(); save(pm, fname)
    if crop_name:
        fw = dlg.findChild(QgsFileWidget)
        lbl = dlg.findChild(QLabel, 'mFileNameLabel')
        r = rect_in(dlg, fw).united(rect_in(dlg, lbl)).adjusted(-10, -8, 10, 8)
        crop = pm.copy(QRect(int(r.x()*dpr), int(r.y()*dpr), int(r.width()*dpr), int(r.height()*dpr)))
        crop.setDevicePixelRatio(dpr); save(crop, crop_name)
    dlg.reject()

def main():
    log('main start; project =', QgsProject.instance().fileName())
    if not QgsProject.instance().fileName():
        iface.addProject(PROJECT); log('loaded project')
    step(1000, open_props)
    step(3500, config_crs)
    step(4500, select_crs)
    step(6000, grab_crs)
    step(8000, open_gpkg)
    step(10000, config_gpkg, 'Street_Lights.gpkg', 'Street_Lights', 'Point',
         [('ID', 'integer (32'), ('Fixture_Type', 'text'), ('Voltage', 'integer (32')])
    step(12000, grab_gpkg, 'street-lights-dialog.png', 'database-row.png')
    step(14000, open_gpkg)
    step(16000, config_gpkg, 'Temple_Footprint.gpkg', 'Temple_Footprint', 'Polygon', [('Name', 'text')])
    step(18000, grab_gpkg, 'temple-dialog.png')
    step(19000, log, 'DONE')

log('drive.py loaded')
step(3000, main)
