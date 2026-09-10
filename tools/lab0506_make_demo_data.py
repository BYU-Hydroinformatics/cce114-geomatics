"""Build the Lab 5 demo data: the six UGRC DEM tiles, the merged raster, slope, and city points.

Everything comes from the sources Lab 5 itself sends students to, so the figures cannot drift away
from the lab. The tile list comes from UGRC's own auto-correlated DEM index, the same layer behind
the raster.utah.gov wizard the lab walks through.

    export PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
           GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal
    /Applications/QGIS.app/Contents/MacOS/python3.12 tools/lab0506_make_demo_data.py <work dir>

About 145 MB of downloads and 1.4 GB unzipped. Keep the work directory outside ~/Desktop,
~/Documents and ~/Downloads: QGIS cannot read or write there on macOS.
"""
import os
import subprocess
import sys
import urllib.request
import zipfile

M = '/Applications/QGIS.app/Contents/MacOS'
# The six 5-metre tiles covering Utah Lake and Provo/Orem/Spanish Fork, which is what Lab 5 step 5
# asks students to pick off the map. Each is a 4,000 x 4,000 grid of 5 m cells.
TILES = ['12TVK400600', '12TVK200600', '12TVK400400',
         '12TVK200400', '12SVK400200', '12SVK200200']
BASE = 'https://storage.googleapis.com/state-of-utah-sgid-downloads/auto-correlated-dems/5-meter/'
CITIES = ('https://services1.arcgis.com/99lidPhWCzftIe9K/arcgis/rest/services/'
          'CitiesTownsLocations/FeatureServer/0/query?where=1%3D1&outFields=NAME'
          '&outSR=26912&f=geojson&resultRecordCount=2000')


def run(*args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print('  FAILED:', ' '.join(args[:2]), r.stderr.strip()[:200])
    return r.returncode == 0


def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print('  cached  %s' % os.path.basename(path))
        return
    req = urllib.request.Request(url, headers={'User-Agent': 'cce114-geomatics lab figure builder'})
    with urllib.request.urlopen(req, timeout=600) as r, open(path, 'wb') as f:
        f.write(r.read())
    print('  fetched %s (%.0f MB)' % (os.path.basename(path), os.path.getsize(path) / 1e6))


def main(work):
    os.makedirs(work, exist_ok=True)
    print('Six 5-metre auto-correlated DEM tiles, the ones Lab 5 has students pick')
    for t in TILES:
        z = os.path.join(work, t + '.zip')
        fetch(BASE + t + '.zip', z)
        if not os.path.exists(os.path.join(work, t + '.asc')):
            with zipfile.ZipFile(z) as zf:
                zf.extractall(work)
    asc = sorted(f for f in os.listdir(work) if f.endswith('.asc'))
    print('  %d .asc tiles' % len(asc))
    head = open(os.path.join(work, asc[0])).readline().split()
    with open(os.path.join(work, asc[0])) as f:
        rows, cols = f.readline().split()[1], f.readline().split()[1]
    print('  each tile is %s x %s cells (Lab 5 says 4,000 x 4,000)' % (cols, rows))

    merged = os.path.join(work, 'merged_dem.tif')
    if not os.path.exists(merged):
        print('Merging, the way Lab 5 step 17 does with the GDAL Merge tool')
        run(M + '/gdal_merge', '-q', '-o', merged, '-a_nodata', '-9999', '-of', 'GTiff',
            *[os.path.join(work, f) for f in asc])
        # the .asc tiles carry no .prj, so state the CRS they are already in
        run(M + '/gdal_edit', '-a_srs', 'EPSG:26912', merged)
    slope = os.path.join(work, 'slope.tif')
    if not os.path.exists(slope):
        print('Slope, the way Lab 5 step 49 does with the Slope tool')
        run(M + '/gdaldem', 'slope', merged, slope, '-compute_edges')

    gj = os.path.join(work, 'cities.geojson')
    fetch(CITIES, gj)
    if not os.path.exists(os.path.join(work, 'cities.shp')):
        run(M + '/ogr2ogr', '-f', 'ESRI Shapefile', os.path.join(work, 'cities.shp'), gj)
    print('\nDone. Now, with the Mac in Light appearance:')
    print('    for s in $(python3 tools/qgis_lab0506_shots.py --list); do \\')
    print('      LAB56_DATA=%s LAB56_OUT=%s/out SHOT=$s \\' % (work, work))
    print('        /Applications/QGIS.app/Contents/MacOS/QGIS --nologo --profile lab56shots \\')
    print('          --code tools/qgis_lab0506_shots.py; done')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
