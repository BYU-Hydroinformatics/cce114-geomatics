"""Check that the Day 13 live-demo web services still load in QGIS 3.44.

Run before Week 7 Thursday with QGIS's own Python (PYTHONHOME must be set for that interpreter
only; see tools/reshoot_lab0304.sh):

    env PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
        PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
        GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
        QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns QT_QPA_PLATFORM=offscreen \
        /Applications/QGIS.app/Contents/MacOS/python3.12 tools/check_demo_services.py

Each line reports whether the layer loads, how many features fall along the Wasatch Front (for
the vector services), and how long it took. On 2026-10-15 every service below passed: the MRDS
WFS returned 1,408 sites in about 5 s and the USGS OGC API 4,992 monitoring locations in about
10 s. Rejected that day: the NHD WMS (84 s, blank render), the USFWS wetlands WMS (blank), and
USGS active mines (no features in the view); nowCOAST's WFS carries only marine layers.
"""
import os, time
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from qgis.core import (Qgis, QgsApplication, QgsCoordinateReferenceSystem, QgsCoordinateTransform,
                       QgsFeatureRequest, QgsProject, QgsRasterLayer, QgsRectangle, QgsVectorLayer)

WASATCH = QgsRectangle(-112.2, 40.0, -111.4, 40.8)   # lon/lat, EPSG:4326

WMS = {
    "USGS 3DEP hillshade": ("https://elevation.nationalmap.gov/arcgis/services/3DEPElevation/ImageServer/WMSServer",
                            "3DEPElevation:Hillshade Gray"),
    "USGS Topo basemap": ("https://basemap.nationalmap.gov/arcgis/services/USGSTopo/MapServer/WMSServer", "0"),
    "NEXRAD radar (Iowa State)": ("https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0q.cgi", "nexrad-n0q-900913"),
}
VECTOR = {
    "USGS MRDS (WFS)": ("WFS", "pagingEnabled='true' restrictToRequestBBOX='1' srsname='EPSG:4326' "
                               "typename='ms:mrds-high' url='https://mrdata.usgs.gov/services/mrds' version='auto'"),
    "USGS gages (OGC API - Features)": ("OAPIF", "pagingEnabled='true' restrictToRequestBBOX='1' "
                               "typename='monitoring-locations' url='https://api.waterdata.usgs.gov/ogcapi/v0' "
                               "version='OGC_API_FEATURES'"),
}

app = QgsApplication([], False)
app.initQgis()
print("QGIS", Qgis.version())
for name, (url, layer) in WMS.items():
    t = time.time()
    lyr = QgsRasterLayer(f"crs=EPSG:3857&format=image/png&layers={layer}&styles&url={url}", name, "wms")
    print(f"{'OK  ' if lyr.isValid() else 'FAIL'} {name}  {time.time() - t:.1f}s")
for name, (provider, uri) in VECTOR.items():
    t = time.time()
    lyr = QgsVectorLayer(uri, name, provider)
    if not lyr.isValid():
        print(f"FAIL {name}")
        continue
    box = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:4326"), lyr.crs(),
                                 QgsProject.instance()).transformBoundingBox(WASATCH)
    n = sum(1 for _ in lyr.getFeatures(QgsFeatureRequest().setFilterRect(box)))
    print(f"{'OK  ' if n else 'FAIL'} {name}  {n} features along the Wasatch Front  {time.time() - t:.1f}s")
app.exitQgis()
