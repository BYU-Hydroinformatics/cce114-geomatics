# Runs the Lab 11 Walmart site-selection analysis (steps 12 to 28) with QGIS 3.44 processing, the
# same algorithms and settings the lab gives students, so the Day 22 deck can show a real result.
# Writes every intermediate and PotentialCustomers to $LAB11_OUT/UtahCounty.gpkg.
#
#   export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
#          PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
#          GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
#          QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns
#   LAB11_IN=<work dir>/ws.gpkg LAB11_OUT=<out dir> \
#     /Applications/QGIS.app/Contents/MacOS/python3.12 tools/lab11_run_analysis.py
#
# LAB11_IN is the GeoPackage built by the commands in the header of tools/qgis_day22_shots.py,
# which also adds `roads` (UGRC Utah Roads) and `census_blocks_2020_area` (every 2020 block whose
# bounding box touches the Utah County area, standing in for the statewide download).
#
# Where the lab leaves a choice to the student, this takes the plain reading and says so:
# step 18 and step 27 use the "intersect" predicate; step 28 uses "are disjoint".
import os
import sys

IN = os.environ['LAB11_IN']
OUT = os.environ['LAB11_OUT']
os.makedirs(OUT, exist_ok=True)
GPKG = os.path.join(OUT, 'UtahCounty.gpkg')
if os.path.exists(GPKG):
    os.remove(GPKG)

from qgis.core import (QgsApplication, QgsProject, QgsCoordinateReferenceSystem, QgsVectorLayer,
                       QgsProcessingContext, QgsProcessingFeedback)

QgsApplication.setPrefixPath('/Applications/QGIS.app', True)
app = QgsApplication([], False)
app.initQgis()
sys.path.append('/Applications/QGIS.app/Contents/Resources/qgis/python/plugins')
import processing
from processing.core.Processing import Processing
Processing.initialize()

project = QgsProject.instance()
project.setCrs(QgsCoordinateReferenceSystem('EPSG:26912'))  # step 3
project.setEllipsoid('EPSG:7019')  # GRS 1980, QGIS's default for an EPSG:26912 project
context = QgsProcessingContext()
context.setProject(project)
context.setEllipsoid('EPSG:7019')
feedback = QgsProcessingFeedback()


def src(table):
    return f'{IN}|layername={table}'


def run(alg, params, table):
    params = dict(params, OUTPUT=f'ogr:dbname=\'{GPKG}\' table="{table}" (geom)')
    out = processing.run(alg, params, context=context, feedback=feedback)['OUTPUT']
    lyr = QgsVectorLayer(f'{GPKG}|layername={table}', table, 'ogr')
    print(f'{table:28s} {lyr.featureCount():>7d}  {alg}', flush=True)
    return f'{GPKG}|layername={table}'


# Step 9: Extract by Attribute, NAME = UTAH, from the county boundaries.
county = run('native:extractbyattribute',
             {'INPUT': src('counties'), 'FIELD': 'name', 'OPERATOR': 0, 'VALUE': 'UTAH'}, 'UtahCounty')
# Steps 12 and 13: Vector overlay > Clip, roads and Walmart locations to Utah County.
roads = run('native:clip', {'INPUT': src('roads'), 'OVERLAY': county}, 'roads_clipped')
stores = run('native:clip', {'INPUT': src('walmarts_all'), 'OVERLAY': county}, 'walmarts_clipped')
# Steps 14 and 15: CARTOCODE 1 to 5, matched one value at a time because the field is text.
major = run('native:extractbyexpression',
            {'INPUT': roads, 'EXPRESSION': "\"cartocode\" IN ('1', '2', '3', '4', '5')"}, 'MajorRoads')
# Step 17: Fix Geometries on the census blocks.
fixed = run('native:fixgeometries', {'INPUT': src('census_blocks_2020_area')}, 'blocks_fixed')
# Step 18: Extract by Location, blocks that intersect Utah County.
blocks = run('native:extractbylocation', {'INPUT': fixed, 'PREDICATE': [0], 'INTERSECT': county},
             'CensusBlocks')
# Step 20: Extract by Attribute, everything that is not a Sam's Club.
current = run('native:extractbyattribute',
              {'INPUT': stores, 'FIELD': 'businessunit_banner_description', 'OPERATOR': 1,
               'VALUE': "Sam's Club"}, 'CurrentLocations')
# Step 22: Field Calculator, Density = PP_TOTAL / $area * 2589988 (people per square mile).
dens = run('native:fieldcalculator',
           {'INPUT': blocks, 'FIELD_NAME': 'Density', 'FIELD_TYPE': 0, 'FIELD_LENGTH': 20,
            'FIELD_PRECISION': 6, 'FORMULA': '"pp_total" / $area * 2589988'}, 'CensusBlocksDensity')
# Step 24: Extract by Attribute, Density > 5000.
dense = run('native:extractbyattribute',
            {'INPUT': dens, 'FIELD': 'Density', 'OPERATOR': 2, 'VALUE': '5000'}, 'HighDensity')
# Steps 25 and 26: 2-mile buffers, 12 segments, dissolved.
buf = {'DISTANCE': 3218.69, 'SEGMENTS': 12, 'END_CAP_STYLE': 0, 'JOIN_STYLE': 0,
       'MITER_LIMIT': 2, 'DISSOLVE': True}
road_buf = run('native:buffer', dict(buf, INPUT=major), 'MajorRoadsBuffer')
store_buf = run('native:buffer', dict(buf, INPUT=current), 'WalmartBuffer')
# Step 27: dense blocks that intersect the road buffer.
near = run('native:extractbylocation', {'INPUT': dense, 'PREDICATE': [0], 'INTERSECT': road_buf},
           'DenseNearRoads')
# Step 28: of those, the ones disjoint from the Walmart buffer.
run('native:extractbylocation', {'INPUT': near, 'PREDICATE': [2], 'INTERSECT': store_buf},
    'PotentialCustomers')

os._exit(0)
