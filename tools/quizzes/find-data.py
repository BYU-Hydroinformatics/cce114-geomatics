"""Who Already Has This Data? — Day 12 (Finding Spatial Data and Web Services).

Rendered by tools/build_quiz.py to docs/quizzes/find-data/index.html. Everything here comes
from slides/day-12/finding-spatial-data-and-web-services.md; the same ground is walked again
in Lab 6, so this doubles as a warm-up for the lab.
"""

SLUG = "find-data"
TITLE = "Who Already Has This Data?"
DAY = 12
WEEK = 7
TOPIC = "Finding Spatial Data and Web Services"
DESCRIPTION = ("CCE 114 in-class self-check: where public spatial data lives, whether a web "
               "service hands you a picture or the actual features, and how to connect QGIS to "
               "Utah's data without downloading anything.")

BLURB = """Eight questions in three parts: <strong>where the data comes from</strong> and who
      made it, whether a service hands you a <strong>picture or the features</strong>, and how
      Utah's data gets <strong>into QGIS</strong> without a download."""

CLOSING = """\
        <strong style="color: var(--text);">For Thursday:</strong><br>
        Data Source Manager &rsaquo; <strong>ArcGIS REST Server</strong> &rsaquo; New &rsaquo; paste the URL &rsaquo; Connect<br>
        Find layers with the <strong>search box</strong> &mdash; the names are database names<br>
        Three or more live layers, styled, with every map element from Lab 2<br>
        <em>A picture if you only need to look at it; the features if you need to analyze it.</em>"""

MESSAGES = [
    "Every one. Now go find something nobody told you existed.",
    "Solid. Reread the ones you missed — picture against features is what Thursday and Lab 6 turn on.",
    "Worth a second run. Every question here is a step in Lab 6, so these explanations are the cheap version of that lab.",
]

QUESTIONS = [
    dict(
        section="Part 1 — Where the data comes from",
        prompt="You need culvert locations for a drainage study. What is the fastest way to find them?",
        setup="",
        options=[
            "Search data.gov for “culverts”",
            "Ask who would care about culverts for their own job — a department of transportation — and go to that agency's site",
            "Digitize them yourself from aerial imagery",
            "Search “culvert shapefile download” and work through the results",
        ],
        correct=1,
        explanation="Data is created by whoever needs it for their own job: parcels come from the "
                    "county assessor because taxes depend on them, streamflow from the USGS "
                    "because someone has to run the gages. Searching for the agency beats "
                    "searching for the data — soils means USDA, floodplains mean FEMA, culverts "
                    "mean a DOT.",
    ),
    dict(
        section="Part 1 — Where the data comes from",
        prompt="data.gov indexes over 550,000 datasets, with a Geospatial category. What happens when you click one?",
        setup="",
        options=[
            "The file downloads from data.gov's own servers",
            "You get a web service URL you can paste straight into QGIS",
            "You are sent out to the agency that publishes it, and you deal with whatever download page they built",
            "You get a preview map, and the download needs a free account",
        ],
        correct=2,
        explanation="data.gov is a catalog, not a warehouse: it indexes datasets that live on "
                    "agency servers and links out to them. That makes it very good for discovery "
                    "and sometimes frustrating for download, because you land on whatever the "
                    "agency happened to build.",
    ),
    dict(
        section="Part 1 — Where the data comes from",
        prompt="A search for Utah county parcels returns page after page of companies selling you parcel data. What fixes it fastest?",
        setup="",
        options=[
            "Add the word “free”",
            "Add “site:.gov” or “site:.us”",
            "Look for the parcels in a mapping app instead",
            "Add the word “repository”",
        ],
        correct=1,
        explanation="Restricting the search to .gov or .us cuts out every reseller repackaging "
                    "public data you already paid for. The companion trick from the same slide: "
                    "add a format word — shapefile, raster, geojson — and you often land on the "
                    "download page instead of somebody's web map.",
    ),
    dict(
        section="Part 2 — A picture, or the actual features?",
        prompt="The hillshade shown in class came back from the USGS 3DEP elevation service as a WMS layer. What did the service actually send?",
        setup="",
        options=[
            "The elevation value of every cell in the area you asked for",
            "A picture the server drew, and nothing else",
            "Contour features carrying elevation attributes",
            "A link to download the source elevation model",
        ],
        correct=1,
        explanation="Web Map Service means the server does the drawing and sends back an image — a "
                    "PNG, in that case. You can look at it; you cannot query the features "
                    "underneath, because none came. WMTS is the same bargain with the tiles drawn "
                    "in advance, and XYZ tiles are the looser, wildly popular version of WMTS: all "
                    "pictures, all fast, which is exactly what a basemap needs to be.",
    ),
    dict(
        section="Part 2 — A picture, or the actual features?",
        prompt="You need to buffer a stream network by 100 meters. Which service do you connect to?",
        setup="",
        options=[
            "WMS",
            "WMTS",
            "WFS, or an ArcGIS feature service",
            "XYZ tiles",
        ],
        correct=2,
        explanation="A buffer is a geometry operation, so you need the geometry — real vector "
                    "features with their attributes, not a rendered image of them. A feature "
                    "service is slower to draw than a picture, and worth it the moment you have "
                    "to select, query, or analyze. WFS has a successor, OGC API - Features, which "
                    "is the same idea rebuilt on plain URLs and GeoJSON.",
    ),
    dict(
        section="Part 2 — A picture, or the actual features?",
        prompt="You want the actual elevation numbers for a study area, to work with them rather than look at a shaded image of them. Which service?",
        setup="",
        options=[
            "WMS",
            "WFS",
            "WCS",
            "XYZ tiles",
        ],
        correct=2,
        explanation="Web Coverage Service is to rasters what WFS is to vectors: it hands back cell "
                    "values instead of a picture of them. WFS is the tempting miss — the instinct "
                    "is right, raw ingredients rather than a cooked meal — but WFS carries vector "
                    "features, and elevation is a raster coverage.",
    ),
    dict(
        section="Part 3 — Utah's data, into QGIS",
        prompt="You found QuaternaryFaults in the SGID Index and want it live in QGIS. Which entry in the Data Source Manager, and how do you find the layer among 891 of them?",
        setup="The SGID is the State Geographic Information Datasource, the catalog behind UGRC — the state GIS office that older documents still call the AGRC.",
        options=[
            "WFS, then scroll the list",
            "ArcGIS REST Server, then use the search box — layer names are the database names, like QuaternaryFaults",
            "WMS, then scroll the list looking for “Quaternary Faults”",
            "XYZ tiles, then paste the layer URL directly",
        ],
        correct=1,
        explanation="UGRC serves its data from Esri infrastructure, so the connection type is "
                    "ArcGIS REST Server: New, name the connection, paste the endpoint URL, OK, "
                    "then Connect. After that, search a fragment — “fault”, “bound”, “oil” — "
                    "because the names are database names with no spaces and your eyes will not "
                    "beat the search box. The connection is saved in your QGIS profile, so you set "
                    "it up once.",
    ),
    dict(
        section="Part 3 — Utah's data, into QGIS",
        prompt="Your layout is built entirely on live web services, and it is due tomorrow. What is the professional move?",
        setup="",
        options=[
            "Nothing — a public agency service is as dependable as a file on your own disk",
            "Download a local copy of the layers you cannot afford to lose, and cite the source on the map",
            "Convert every layer to WMS so the map draws faster",
            "Keep a screenshot of the map canvas as a backup",
        ],
        correct=1,
        explanation="A live service is a dependency: servers go down, go slow, or change their "
                    "URL, and every web layer is blank when you are offline. On a real project you "
                    "decide deliberately which layers stay live, because they change, and which "
                    "you cache locally, because you cannot afford them to vanish the night before "
                    "a submittal. Two more things before you call it finished: check the CRS, "
                    "since services usually publish in Web Mercator and QGIS reprojects on the "
                    "fly, and credit the agency on the layout.",
    ),
]
