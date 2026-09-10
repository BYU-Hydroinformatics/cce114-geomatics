"""Build every demo layer the Lab 3 and Lab 4 figures need, from scratch, on any machine.

Everything here comes from a source the labs themselves cite, so the figures cannot drift away
from what the labs tell students to do:

  points.csv            the five geocache coordinates Lab 3 publishes, converted to EPSG:26912
                        and nudged a few metres, standing in for handheld GPS error
  pts_corrected.shp     the same five at their published positions, plus the "favorite" point
                        Lab 3 step 28 has students add
  campus.shp            BYU main campus, read from tools/lab0304-data/byu-campus.geojson,
                        which measures 1,444,296 m2 (357 acres)
  campus_area.shp       the same polygon with the area field Lab 3 step 42 calculates
  SF_Waterways.gpkg     Lab 4's own SGID query, reprojected to EPSG:26912 (98 features)
  temple_footprint.shp  a rectangle at the announced Spanish Fork temple site, 29,708 sq ft,
                        inside Lab 4's 25,000-35,000 target
  parking_lot.shp       a U-shape around it, 69,750 sq ft, inside Lab 4's 60,000-80,000 target

Run it with QGIS's bundled Python so GDAL and PROJ are on hand:

    export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
           PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
           GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal
    /Applications/QGIS.app/Contents/MacOS/python3.12 tools/lab0304_make_demo_data.py <work dir>

Needs the network for one fetch, the UGRC waterways query. The campus polygon is committed rather
than re-fetched from Overpass, which rate-limits and answered 504 during the session that wrote
this. Keep the work directory outside ~/Desktop, ~/Documents and ~/Downloads: QGIS cannot read or
write there on macOS.
"""
import json
import math
import os
import random
import sys
import urllib.request

from osgeo import ogr, osr

ogr.UseExceptions()

# The Spanish Fork Utah Temple site, from resolving the Google Maps link printed in Lab 4.
TEMPLE_LATLON = (40.1069876, -111.614298)

SGID_QUERY = (
    'https://services1.arcgis.com/99lidPhWCzftIe9K/arcgis/rest/services/UtahStreamsNHD/'
    'FeatureServer/0/query?where=FType+IN+(336,460)'
    '&geometry=-111.68,40.06,-111.56,40.15&geometryType=esriGeometryEnvelope&inSR=4326'
    '&spatialRel=esriSpatialRelIntersects&outFields=GNIS_Name,FType_Text,FCode_Text&f=geojson'
)
CAMPUS_GEOJSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'lab0304-data', 'byu-campus.geojson')


def wgs84_to_utm12n():
    src = osr.SpatialReference()
    src.ImportFromEPSG(4326)
    src.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    dst = osr.SpatialReference()
    dst.ImportFromEPSG(26912)
    dst.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    return osr.CoordinateTransformation(src, dst), dst


def fetch(url, path, data=None):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print('  cached  %s' % os.path.basename(path))
        return
    # Overpass answers 406 to requests with no User-Agent.
    req = urllib.request.Request(url, data=data.encode() if data else None,
                                 headers={'User-Agent': 'cce114-geomatics lab figure builder'})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, 'wb') as f:
        f.write(r.read())
    print('  fetched %s (%d bytes)' % (os.path.basename(path), os.path.getsize(path)))


def shapefile(path, name, srs, geom_type, fields, rows):
    drv = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(path):
        drv.DeleteDataSource(path)
    ds = drv.CreateDataSource(path)
    lyr = ds.CreateLayer(name, srs, geom_type)
    for fname, ftype, *rest in fields:
        fd = ogr.FieldDefn(fname, ftype)
        if rest:
            fd.SetWidth(rest[0])
            fd.SetPrecision(rest[1])
        lyr.CreateField(fd)
    for attrs, geom in rows:
        f = ogr.Feature(lyr.GetLayerDefn())
        for k, v in attrs.items():
            if v is not None:
                f.SetField(k, v)
        f.SetGeometry(geom)
        lyr.CreateFeature(f)
    ds = None
    print('  wrote   %s (%d features)' % (os.path.basename(path), len(rows)))


def main(work):
    os.makedirs(work, exist_ok=True)
    ct, utm = wgs84_to_utm12n()

    print('Lab 3 points, from the geocache coordinates Lab 3 publishes')

    def dms(d, m, s):
        return d + m / 60 + s / 3600

    geo = [('Statue_JSB', dms(40, 14, 52.00), -dms(111, 38, 55.36)),
           ('Statue_Maeser', dms(40, 14, 53.75), -dms(111, 38, 59.34)),
           ('Vent', dms(40, 14, 49.73), -dms(111, 39, 3.05)),
           ('Drain_Cover', dms(40, 14, 56.30), -dms(111, 38, 54.70)),
           ('Walkway', dms(40, 14, 59.03), -dms(111, 38, 57.34))]
    pts = [(n,) + ct.TransformPoint(lon, lat)[:2] for n, lat, lon in geo]

    random.seed(114)  # fixed, so re-running gives byte-identical demo data
    with open(os.path.join(work, 'points.csv'), 'w') as f:
        f.write('name,x,y\n')
        for n, x, y in pts:
            f.write('%s,%.2f,%.2f\n' % (n, x + random.uniform(-6, 6), y + random.uniform(-6, 6)))
    print('  wrote   points.csv (%d rows)' % len(pts))

    rows = [({'name': n, 'x': x, 'y': y}, _pt(x, y)) for n, x, y in pts]
    rows.append(({'name': 'favorite'}, _pt(444700.0, 4455480.0)))
    shapefile(os.path.join(work, 'pts_corrected.shp'), 'pts_corrected', utm, ogr.wkbPoint,
              [('name', ogr.OFTString), ('x', ogr.OFTReal), ('y', ogr.OFTReal)], rows)

    print('BYU main campus, from tools/lab0304-data/byu-campus.geojson')
    fc = json.load(open(CAMPUS_GEOJSON))
    campus = ogr.CreateGeometryFromJson(json.dumps(fc['features'][0]['geometry']))
    campus.Transform(ct)
    acres = campus.GetArea() / 4046.8564224
    print('  campus area %.0f m2 = %.0f acres  (Lab 3 says about 1.4 million m2, ~350 acres)' %
          (campus.GetArea(), acres))
    if not 330 <= acres <= 380:
        print('  WARNING: outside the range Lab 3 tells students to expect; check the relation')
    shapefile(os.path.join(work, 'campus.shp'), 'campus', utm, ogr.wkbPolygon,
              [('id', ogr.OFTInteger)], [({'id': 1}, campus)])
    shapefile(os.path.join(work, 'campus_area.shp'), 'campus', utm, ogr.wkbPolygon,
              [('id', ogr.OFTInteger), ('area', ogr.OFTReal, 20, 3)],
              [({'id': 1, 'area': campus.GetArea()}, campus)])

    print("Lab 4 waterways, from the SGID address printed in Lab 4")
    gj = os.path.join(work, 'sf_waterways.geojson')
    fetch(SGID_QUERY, gj)
    feats = json.load(open(gj)).get('features', [])
    print('  %d features (Lab 4 says 98)' % len(feats))
    gpkg = os.path.join(work, 'SF_Waterways.gpkg')
    if os.path.exists(gpkg):
        os.remove(gpkg)
    drv = ogr.GetDriverByName('GPKG')
    out = drv.CreateDataSource(gpkg)
    lyr = out.CreateLayer('Waterways', utm, ogr.wkbUnknown)
    for name in ('GNIS_Name', 'FType_Text', 'FCode_Text'):
        lyr.CreateField(ogr.FieldDefn(name, ogr.OFTString))
    for feat in feats:
        g = ogr.CreateGeometryFromJson(json.dumps(feat['geometry']))
        g.Transform(ct)
        f = ogr.Feature(lyr.GetLayerDefn())
        for name in ('GNIS_Name', 'FType_Text', 'FCode_Text'):
            f.SetField(name, feat['properties'].get(name))
        f.SetGeometry(g)
        lyr.CreateFeature(f)
    out = None
    print('  wrote   SF_Waterways.gpkg')

    print('Lab 4 footprints, at the announced temple site')
    tx, ty = ct.TransformPoint(TEMPLE_LATLON[1], TEMPLE_LATLON[0])[:2]
    print('  temple site EPSG:26912  X %.0f  Y %.0f' % (tx, ty))
    temple = _rect(tx, ty, 46.0, 60.0)
    sqft = temple.GetArea() * 10.7639
    print('  temple footprint %.0f sq ft (Lab 4 target 25,000-35,000)' % sqft)
    shapefile(os.path.join(work, 'temple_footprint.shp'), 'Temple_Footprint', utm, ogr.wkbPolygon,
              [('id', ogr.OFTInteger), ('Name', ogr.OFTString), ('area', ogr.OFTReal, 20, 2)],
              [({'id': 1, 'Name': 'Spanish Fork Utah Temple', 'area': sqft}, temple)])
    lot = _rect(tx, ty, 88.0, 105.0).Difference(temple)
    print('  parking lot      %.0f sq ft (Lab 4 target 60,000-80,000)' % (lot.GetArea() * 10.7639))
    shapefile(os.path.join(work, 'parking_lot.shp'), 'Parking_Lot', utm, ogr.wkbPolygon,
              [('id', ogr.OFTInteger), ('Name', ogr.OFTString)],
              [({'id': 1, 'Name': 'Parking Lot'}, lot)])

    print('\nDone. Now put the Mac in Light appearance and run:')
    print('    ./tools/reshoot_lab0304.sh %s' % work)


def _pt(x, y):
    g = ogr.Geometry(ogr.wkbPoint)
    g.AddPoint(x, y)
    return g


def _rect(cx, cy, w, h):
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2),
                   (-w / 2, -h / 2)):
        ring.AddPoint(cx + dx, cy + dy)
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(ring)
    return poly


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
