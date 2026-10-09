"""Who Already Has This Data? — Day 12 (Finding Spatial Data).

Rendered by tools/build_quiz.py to docs/quizzes/find-data/index.html. Everything here comes
from slides/day-12/finding-spatial-data.md. Until 2026-10-09 this quiz also covered web
services; those questions moved to tools/quizzes/services.py with the Thursday deck.
"""

SLUG = "find-data"
TITLE = "Who Already Has This Data?"
DAY = 12
WEEK = 7
TOPIC = "Finding Spatial Data"
DESCRIPTION = ("CCE 114 in-class self-check: who makes public spatial data, the national "
               "sources worth knowing, and finding Utah's data at the UGRC.")

BLURB = """Eight questions in three parts: <strong>where the data comes from</strong> and who
      made it, the <strong>national</strong> front doors, and <strong>Utah's</strong> data at
      the UGRC."""

CLOSING = """\
        <strong style="color: var(--text);">For Lab 6, Steps 1 and 2:</strong><br>
        Start at <strong>gis.utah.gov/products/sgid</strong> &rsaquo; browse the categories or search the index<br>
        Pick <strong>three datasets</strong> and one question they answer together<br>
        Note each one's type, source agency, and how you can get it<br>
        <em>Don't search for the data; search for the agency whose job depends on it.</em>"""

MESSAGES = [
    "Every one. Now go find something nobody told you existed.",
    "Solid. Reread the ones you missed — knowing who makes the data is most of finding it.",
    "Worth a second run. Lab 6 starts with exactly this kind of hunting, so these explanations are the cheap version of its first two steps.",
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
        section="Part 2 — The national front doors",
        prompt="You need satellite scenes showing a reservoir shrinking from the 1980s to today. Where do you go?",
        setup="",
        options=[
            "The National Map Downloader",
            "USGS EarthExplorer",
            "data.gov",
            "USDA Web Soil Survey",
        ],
        correct=1,
        explanation="EarthExplorer is the USGS front door for satellite and aerial imagery: Landsat "
                    "back to 1972, Sentinel, aerial photography. You set an area, a date range, and "
                    "a cloud-cover limit, then download scenes; it needs a free account. The time "
                    "dimension is the point — it is how you show a reservoir shrinking or a city "
                    "sprawling. The National Map Downloader is the place for elevation, "
                    "hydrography, boundaries, and topo maps.",
    ),
    dict(
        section="Part 2 — The national front doors",
        prompt="A client asks whether their site sits in a mapped floodplain. Whose data answers that?",
        setup="",
        options=[
            "USDA's Web Soil Survey",
            "FEMA's Flood Map Service Center",
            "Census TIGER/Line",
            "OpenStreetMap",
        ],
        correct=1,
        explanation="Floodplains mean FEMA: its Flood Map Service Center publishes the flood "
                    "insurance rate maps. It is the same rule as Part 1 — go to the agency whose "
                    "job depends on the data. Soils are USDA's, boundaries and roads are the "
                    "Census Bureau's TIGER/Line, and OpenStreetMap is crowdsourced.",
    ),
    dict(
        section="Part 3 — Utah's data",
        prompt="A report from a few years ago credits its maps to the “AGRC”. Where do you find that data today?",
        setup="",
        options=[
            "Nowhere — the AGRC was shut down",
            "At the UGRC, gis.utah.gov: the same office, renamed",
            "Only by emailing the report's authors",
            "On data.gov, which absorbed the state portals",
        ],
        correct=1,
        explanation="The Automated Geographic Reference Center is now the Utah Geospatial Resource "
                    "Center, UGRC: the same state GIS office under a new name. Half the material "
                    "online still says AGRC. Its catalog is the SGID, the State Geographic "
                    "Information Datasource, and nearly everything in it is free and public.",
    ),
    dict(
        section="Part 3 — Utah's data",
        prompt="Every result in the SGID Index lists its source agency — DWR, UDOT, UGS, and so on. Why should you care?",
        setup="",
        options=[
            "The source decides which file format you get",
            "It tells you who made the data, which tells you how far to trust it",
            "Only data from UGRC itself can be used in QGIS",
            "It decides whether the dataset is free",
        ],
        correct=1,
        explanation="Knowing who stewards a dataset tells you why it exists and how much to trust "
                    "it: wildlife habitat from the Division of Wildlife Resources, roads from UDOT, "
                    "geology from the Utah Geological Survey. That is the whole idea behind the "
                    "metadata week later in the course.",
    ),
    dict(
        section="Part 3 — Utah's data",
        prompt="Your survey crew will spend three days in a canyon with no cell signal. The SGID offers each layer as a download and as a web service. Which do you take?",
        setup="",
        options=[
            "The web service — it is always current",
            "The download — a file on your disk works offline",
            "Either; QGIS caches web services automatically",
            "Neither; take screenshots of the map",
        ],
        correct=1,
        explanation="A download is yours forever and works offline, but it is frozen the moment "
                    "you take it. A web service is always current and there is nothing to store, "
                    "but it needs a network and a server that is up. No signal settles it. "
                    "Thursday is about the other column: when the service is the better choice.",
    ),
]
