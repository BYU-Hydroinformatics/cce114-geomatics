"""Rebuild Week 4 synthetic practice data and genuine QGIS 3.44 screenshots.
Run in an isolated QGIS profile (never uses or closes a user's project):
WEEK04_REPO="$PWD" /Applications/QGIS.app/Contents/MacOS/QGIS --nologo \
  --profiles-path /tmp/cce114-week04/profiles --profile screenshots \
  --code "$PWD/tools/qgis_week04_shots.py"
All example positions are synthetic, NOT field observations or surveyed landmarks.
"""
import os, csv, time, traceback, json
from pathlib import Path
from qgis.core import *
from qgis.gui import QgsVectorLayerSaveAsDialog, QgsProjectionSelectionWidget, QgsFieldCalculator, QgsExpressionBuilderWidget
from qgis.PyQt.QtCore import QTimer, QVariant, Qt, QUrl
from qgis.PyQt.QtGui import QColor, QFont, QPalette
from qgis.PyQt.QtWidgets import QApplication, QWidget, QDockWidget, QListWidget, QLineEdit, QComboBox, QCheckBox, QStyleFactory
from qgis.utils import iface
import sip
ROOT = Path(os.environ['WEEK04_REPO'])
DATA = ROOT / 'docs/handson/data/week-04'
OUT = ROOT / 'docs/handson/images'
WORK = Path('/tmp/cce114-week04')
for directory in (DATA, OUT, WORK): directory.mkdir(parents=True, exist_ok=True)
KEEP = []
def settle(n=1):
    end=time.time()+n
    while time.time()<end:
        QApplication.processEvents(); time.sleep(.05)
def shot(w,name):
    for widget in QApplication.allWidgets():
        widget.setPalette(QApplication.palette())
    settle(1)
    pm=w.grab()
    if pm.width()>2000: pm=pm.scaledToWidth(2000, Qt.SmoothTransformation)
    assert pm.save(str(OUT/('w4-'+name+'.png')))
    print('SHOT',name,pm.width(),pm.height(),flush=True)
def combo(d,name,text):
    w=d.findChild(QComboBox,name); assert w is not None, name
    i=w.findText(text,Qt.MatchContains); assert i>=0,(name,text)
    w.setCurrentIndex(i)
def crs_widget(d,name,crs):
    w=d.findChild(QWidget,name); assert w is not None,name
    sip.cast(w,QgsProjectionSelectionWidget).setCrs(crs)
def labels(layer,field):
    s=QgsPalLayerSettings(); s.fieldName=field
    t=QgsTextFormat(); t.setFont(QFont('Arial',11)); t.setSize(11)
    b=QgsTextBufferSettings(); b.setEnabled(True); b.setSize(1); b.setColor(QColor('white')); t.setBuffer(b)
    s.setFormat(t); layer.setLabeling(QgsVectorLayerSimpleLabeling(s)); layer.setLabelsEnabled(True)
def main():
    exit_code = 1
    try:
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        pal=QPalette()
        for role,color in [(QPalette.Window,'#f0f0f0'),(QPalette.WindowText,'#202020'),(QPalette.Base,'#ffffff'),(QPalette.AlternateBase,'#f6f6f6'),(QPalette.Text,'#202020'),(QPalette.Button,'#eeeeee'),(QPalette.ButtonText,'#202020'),(QPalette.Highlight,'#cce5ff'),(QPalette.HighlightedText,'#101010'),(QPalette.ToolTipBase,'#ffffff'),(QPalette.ToolTipText,'#202020')]: pal.setColor(role,QColor(color))
        QApplication.instance().setStyleSheet('')
        QApplication.setPalette(pal)
        assert Qgis.QGIS_VERSION.startswith('3.44'), Qgis.QGIS_VERSION
        p=QgsProject.instance(); p.clear()
        wgs=QgsCoordinateReferenceSystem('EPSG:4326'); utm=QgsCoordinateReferenceSystem('EPSG:26912')
        p.setCrs(utm); p.setEllipsoid('NONE')
        back=QgsCoordinateTransform(utm,wgs,p)
        # Three illustrative campus clusters, each with three simulated receivers.
        rows=[]
        for site,e,n in [('Demo_A',444700,4455300),('Demo_B',444900,4455500),('Demo_C',444600,4455700)]:
            for receiver,dx,dy in [('A',0,0),('B',6,8),('C',-4,3)]:
                pt=back.transform(QgsPointXY(e+dx,n+dy))
                rows.append([receiver,site,f'{pt.y():.8f}',f'{pt.x():.8f}'])
        csvpath=DATA/'practice_gps.csv'
        with csvpath.open('w',newline='') as f:
            wr=csv.writer(f); wr.writerow(['name','site','lat','lon']); wr.writerows(rows)
        uri=QUrl.fromLocalFile(str(csvpath)).toString()+'?type=csv&xField=lon&yField=lat&crs=EPSG:4326&detectTypes=yes'
        raw=QgsVectorLayer(uri,'practice_gps — degrees','delimitedtext'); assert raw.isValid() and raw.featureCount()==9
        p.addMapLayer(raw)
        opts=QgsVectorFileWriter.SaveVectorOptions(); opts.driverName='GPKG'; opts.layerName='practice_utm'
        opts.ct=QgsCoordinateTransform(wgs,utm,p)
        gpkg=WORK/'practice_gps.gpkg'
        if gpkg.exists(): gpkg.unlink()
        result=QgsVectorFileWriter.writeAsVectorFormatV3(raw,str(gpkg),p.transformContext(),opts)
        assert result[0]==QgsVectorFileWriter.NoError,result
        pts=QgsVectorLayer(str(gpkg)+'|layername=practice_utm','practice_utm — meters','ogr'); assert pts.isValid()
        p.addMapLayer(pts)
        cats=[]
        for site,color in [('Demo_A','#ea6d35'),('Demo_B','#148477'),('Demo_C','#7754a6')]:
            cats.append(QgsRendererCategory(site,QgsMarkerSymbol.createSimple({'name':'circle','color':color,'outline_color':'white','outline_width':'0.4','size':'4'}),site))
        pts.setRenderer(QgsCategorizedSymbolRenderer('site',cats)); labels(pts,'site')
        p.layerTreeRoot().findLayer(raw.id()).setItemVisibilityChecked(False)
        iface.setActiveLayer(pts)
        for dock in iface.mainWindow().findChildren(QDockWidget):
            if dock.windowTitle().lower()!='layers': dock.hide()
        iface.mainWindow().resize(1250,800)
        # Import dialog, using the actual CSV and actual QGIS controls.
        act=next(a for a in iface.mainWindow().findChildren(type(iface.actionExit())) if 'data source manager' in a.text().replace('&','').lower())
        act.trigger(); settle(2)
        d=next(w for w in QApplication.topLevelWidgets() if w.isVisible() and 'DataSourceManager' in w.objectName())
        d.resize(1080,850)
        for lw in d.findChildren(QListWidget):
            hit=next((i for i in range(lw.count()) if 'delimited' in lw.item(i).text().lower()),None)
            if hit is not None: lw.setCurrentRow(hit); break
        settle(1)
        from qgis.gui import QgsFileWidget
        fw=next(w for w in d.findChildren(QWidget) if w.objectName()=='mFileWidget' and w.isVisible())
        sip.cast(fw,QgsFileWidget).setFilePath(str(csvpath)); settle(2)
        from qgis.gui import QgsCollapsibleGroupBox
        for name in ('recordOptionsGroupBox','geometryDefinitionGroupBox'):
            sip.cast(d.findChild(QWidget,name),QgsCollapsibleGroupBox).setCollapsed(False)
        settle()
        # Record object names for reproducible staging if QGIS changes its widget names.
        (WORK/'import-widgets.txt').write_text('\n'.join(f'{w.metaObject().className()} {w.objectName()}' for w in d.findChildren(QWidget) if w.isVisible()))
        for cb in d.findChildren(QComboBox):
            if cb.objectName()=='cmbXField': combo(d,cb.objectName(),'lon')
            if cb.objectName()=='cmbYField': combo(d,cb.objectName(),'lat')
        for w in d.findChildren(QWidget):
            if 'ProjectionSelectionWidget' in w.metaObject().className(): sip.cast(w,QgsProjectionSelectionWidget).setCrs(wgs)
        shot(d,'import'); d.close(); settle()
        d=QgsVectorLayerSaveAsDialog(raw); KEEP.append(d); d.resize(1000,760); d.show(); settle()
        combo(d,'mFormatComboBox','GeoPackage')
        fw=d.findChild(QWidget,'mFilename'); assert fw is not None
        sip.cast(fw,QgsFileWidget).setFilePath(str(WORK/'practice_gps.gpkg'))
        ln=d.findChild(QWidget,'leLayername'); assert ln is not None
        ln.setText('practice_utm')
        crs_widget(d,'mCrsSelector',utm)
        shot(d,'export'); d.reject()
        pts.startEditing()
        d=QgsFieldCalculator(pts); KEEP.append(d); d.resize(1080,740); d.show(); settle()
        d.findChild(QLineEdit,'mOutputFieldNameLineEdit').setText('easting')
        combo(d,'mOutputFieldTypeComboBox','Decimal')
        eb=sip.cast(d.findChild(QWidget,'builder'),QgsExpressionBuilderWidget); eb.setExpressionText('$x')
        from qgis.PyQt.QtWidgets import QSpinBox
        for spin in d.findChildren(QSpinBox):
            if 'precision' in spin.objectName().lower(): spin.setValue(2)
            if 'width' in spin.objectName().lower(): spin.setValue(12)
        shot(d,'calculator'); d.reject(); pts.rollBack()
        pts.startEditing()
        pts.addAttribute(QgsField('easting',QVariant.Double)); pts.addAttribute(QgsField('northing',QVariant.Double)); pts.updateFields()
        results=[]
        for f in pts.getFeatures():
            pt=f.geometry().asPoint()
            pts.changeAttributeValue(f.id(),pts.fields().indexFromName('easting'),round(pt.x(),2))
            pts.changeAttributeValue(f.id(),pts.fields().indexFromName('northing'),round(pt.y(),2))
            results.append({'name':f['name'],'site':f['site'],'easting':round(pt.x(),2),'northing':round(pt.y(),2)})
        assert pts.commitChanges()
        (WORK/'verified.json').write_text(json.dumps({'qgis':Qgis.QGIS_VERSION,'rows':results},indent=2))
        cfg=pts.attributeTableConfig(); cfg.setSortExpression('"site" || "name"'); cfg.setSortOrder(Qt.AscendingOrder); pts.setAttributeTableConfig(cfg)
        d=iface.showAttributeTable(pts); d.window().resize(1220,500); settle(2); shot(d.window(),'table'); d.close()
        # Real QGIS map canvas, deliberately offline so the practice works without web tiles.
        c=iface.mapCanvas(); c.setCanvasColor(QColor('#f3f7f4')); p.setCrs(utm); c.setDestinationCrs(utm)
        c.setExtent(QgsRectangle(444500,4455200,445500,4455800)); c.refresh(); settle(3)
        c.setExtent(QgsRectangle(444500,4455200,445500,4455800)); c.refresh(); settle(2)
        shot(iface.mainWindow(),'overview')
        labels(pts,'name'); pts.setSubsetString('"site" = \'Demo_A\'')
        c.setExtent(QgsRectangle(444685,4455288,444720,4455320)); c.refresh(); settle(2)
        shot(iface.mainWindow(),'scatter')
        pts.setSubsetString(''); labels(pts,'site')
        p.setFilePathStorage(Qgis.FilePathType.Relative)
        # Downloadable checkpoint, using a relative CSV and GeoPackage in one ZIP.
        import shutil, zipfile
        pack=WORK/'practice'; pack.mkdir(exist_ok=True)
        shutil.copy2(csvpath,pack/'practice_gps.csv'); shutil.copy2(gpkg,pack/'practice_gps.gpkg')
        raw.setDataSource(QUrl.fromLocalFile(str(pack/'practice_gps.csv')).toString()+'?type=csv&xField=lon&yField=lat&crs=EPSG:4326&detectTypes=yes',raw.name(),'delimitedtext')
        pts.setDataSource(str(pack/'practice_gps.gpkg')+'|layername=practice_utm',pts.name(),'ogr')
        c.setExtent(QgsRectangle(444500,4455200,445500,4455800))
        p.setTitle('Week 4 — SYNTHETIC GPS practice'); p.write(str(pack/'week04-practice.qgz'))
        with zipfile.ZipFile(DATA/'week04-practice.zip','w',zipfile.ZIP_DEFLATED) as z:
            z.write(DATA/'README.md','README.md')
            for f in pack.iterdir():
                if f.suffix in ('.csv','.gpkg','.qgz'): z.write(f,f.name)
        print('COMPLETE',flush=True)
        exit_code = 0
    except Exception:
        traceback.print_exc()
    finally:
        QgsProject.instance().setDirty(False)
        QTimer.singleShot(500,lambda: os._exit(exit_code))
QTimer.singleShot(2500,main)
