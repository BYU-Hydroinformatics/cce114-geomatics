"""A Picture, or the Features? — Day 13 (Web Services).

Rendered by tools/build_quiz.py to docs/quizzes/services/index.html. Everything here comes
from slides/day-13/web-services.md, the Thursday lecture of Week 7. Five of the questions
came from the find-data quiz, which covered both days until Week 7's Thursday became a
lecture on 2026-10-09; the same ground is walked again in Lab 6.
"""

SLUG = "services"
TITLE = "A Picture, or the Features?"
DAY = 13
WEEK = 7
TOPIC = "Web Services"
DESCRIPTION = ("CCE 114 in-class self-check: whether a web service hands you a picture or the "
               "actual features, what QGIS asks a server, and connecting QGIS to Utah's data "
               "without downloading anything.")

BLURB = """Seven questions in three parts: whether a service hands you a <strong>picture or
      the features</strong>, what QGIS is really doing when it talks to a <strong>URL</strong>,
      and how Utah's data gets <strong>into QGIS</strong> without a download."""

CLOSING = """\
        <strong style="color: var(--text);">For Lab 6, Step 3:</strong><br>
        Data Source Manager &rsaquo; <strong>ArcGIS REST Server</strong> &rsaquo; New &rsaquo; paste the URL &rsaquo; Connect<br>
        Find layers with the <strong>search box</strong> &mdash; the names are database names<br>
        Three live layers, styled, with every required map element<br>
        <em>A picture if you only need to look at it; the features if you need to analyze it.</em>"""

MESSAGES = [
    "Every one. Lab 6 should feel like a formality.",
    "Solid. Reread the ones you missed — picture against features is what Lab 6 turns on.",
    "Worth a second run. Every question here is a step in Lab 6, so these explanations are the cheap version of that lab.",
]

QUESTIONS = [
    dict(
        section='Part 1 — A picture, or the features?',
        prompt='The hillshade shown in class came back from the USGS 3DEP elevation service as a WMS layer. What did the service actually send?',
        setup='',
        options=[
            'The elevation value of every cell in the area you asked for',
            'A picture the server drew, and nothing else',
            'Contour features carrying elevation attributes',
            'A link to download the source elevation model',
        ],
        correct=1,
        explanation='Web Map Service means the server does the drawing and sends back an image — a PNG, in that case. You can look at it; you cannot query the features underneath, because none came. WMTS is the same bargain with the tiles drawn in advance, and XYZ tiles are the looser, wildly popular version of WMTS: all pictures, all fast, which is exactly what a basemap needs to be.',
    ),
    dict(
        section='Part 1 — A picture, or the features?',
        prompt='You need to buffer a stream network by 100 meters. Which service do you connect to?',
        setup='',
        options=[
            'WMS',
            'WMTS',
            'WFS, or an ArcGIS feature service',
            'XYZ tiles',
        ],
        correct=2,
        explanation='A buffer is a geometry operation, so you need the geometry — real vector features with their attributes, not a rendered image of them. A feature service is slower to draw than a picture, and worth it the moment you have to select, query, or analyze. WFS has a successor, OGC API - Features, which is the same idea rebuilt on plain URLs and GeoJSON.',
    ),
    dict(
        section='Part 1 — A picture, or the features?',
        prompt='You want the actual elevation numbers for a study area, to work with them rather than look at a shaded image of them. Which service?',
        setup='',
        options=[
            'WMS',
            'WFS',
            'WCS',
            'XYZ tiles',
        ],
        correct=2,
        explanation='Web Coverage Service is to rasters what WFS is to vectors: it hands back cell values instead of a picture of them. WFS is the tempting miss — the instinct is right, raw ingredients rather than a cooked meal — but WFS carries vector features, and elevation is a raster coverage.',
    ),
    dict(
        section='Part 1 — A picture, or the features?',
        prompt='Your Lab 6 map needs a satellite basemap behind three data layers. Which kind of service suits the basemap?',
        setup='',
        options=[
            'WFS',
            'WCS',
            'XYZ tiles or WMTS',
            'An ArcGIS feature service',
        ],
        correct=2,
        explanation='A basemap only has to look right, so a picture is all you need, and pre-drawn tiles are the fastest picture there is. XYZ tiles are how Google, OpenStreetMap, and almost every basemap works; WMTS is the OGC standard for the same idea. Save the feature services for the layers you will query or analyze.',
    ),
    dict(
        section='Part 2 — A service is just a URL',
        prompt='You click Connect on a new WMS or WFS connection in QGIS. What does QGIS ask the server first?',
        setup='',
        options=[
            'For a copy of every feature it holds',
            'GetCapabilities — what layers do you have?',
            'For a password',
            "For the layer's metadata record in XML",
        ],
        correct=1,
        explanation='Every OGC service answers a GetCapabilities request with a list of its layers, and that list is what fills the connection tree in the Data Source Manager. After that, QGIS is just building URLs — a GetMap for a picture, a query for features — and drawing whatever comes back. Paste one of those URLs into a browser and you see exactly what QGIS sees.',
    ),
    dict(
        section="Part 3 — Utah's data, into QGIS",
        prompt='You found QuaternaryFaults in the SGID Index and want it live in QGIS. Which entry in the Data Source Manager, and how do you find the layer among more than 900 of them?',
        setup='The SGID is the State Geographic Information Datasource, the catalog behind UGRC — the state GIS office that older documents still call the AGRC.',
        options=[
            'WFS, then scroll the list',
            'ArcGIS REST Server, then use the search box — layer names are the database names, like QuaternaryFaults',
            'WMS, then scroll the list looking for “Quaternary Faults”',
            'XYZ tiles, then paste the layer URL directly',
        ],
        correct=1,
        explanation='UGRC serves its data from Esri infrastructure, so the connection type is ArcGIS REST Server: New, name the connection, paste the endpoint URL, OK, then Connect. After that, search a fragment — “fault”, “bound”, “oil” — because the names are database names with no spaces and your eyes will not beat the search box. The connection is saved in your QGIS profile, so you set it up once.',
    ),
    dict(
        section="Part 3 — Utah's data, into QGIS",
        prompt='Your layout is built entirely on live web services, and it is due tomorrow. What is the professional move?',
        setup='',
        options=[
            'Nothing — a public agency service is as dependable as a file on your own disk',
            'Download a local copy of the layers you cannot afford to lose, and cite the source on the map',
            'Convert every layer to WMS so the map draws faster',
            'Keep a screenshot of the map canvas as a backup',
        ],
        correct=1,
        explanation='A live service is a dependency: servers go down, go slow, or change their URL, and every web layer is blank when you are offline. On a real project you decide deliberately which layers stay live, because they change, and which you cache locally, because you cannot afford them to vanish the night before a submittal. Two more things before you call it finished: check the CRS, since services usually publish in Web Mercator and QGIS reprojects on the fly, and credit the agency on the layout.',
    ),
]
