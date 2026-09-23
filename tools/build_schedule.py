#!/usr/bin/env python3
"""Generate the week-by-week schedule page, one page per week, and the pages they link to.

The course runs every Fall (Sep-Dec) and Winter (Jan-Apr). Everything here is expressed
as week numbers and weekdays, never calendar dates, so the site does not need a rewrite
each semester: Tuesdays are concept lectures, Thursdays are demos and hands-on work in
QGIS. Day numbers count class meetings from the first one.

Edit the DAYS and WEEKS tables below, then run:  python3 tools/build_schedule.py
It rewrites docs/schedule.md, docs/weeks/week-NN.md (one per week), docs/handson/ (one page
per Thursday session plus an index), docs/activities/ (one page per Tuesday activity guide),
and the Schedule section of mkdocs.yml.

Every week page has the same shape: an optional "Also this week" callout for exams,
experiences and final-project deadlines, then four cards in a fixed order, each with its own
icon: Presentation Slides, In-Class Practice, Lab Assignment, Reading Quiz. A card with
nothing in it says so ("No lab this week") rather than vanishing. Week pages are fully
generated; nothing hand-written survives on them.

Two kinds of linked page keep a hand-written zone that survives a rerun, below a marker:
docs/handson/week-NN.md below "<!-- runsheet -->" (the Thursday run sheet) and
docs/activities/week-NN.md below "<!-- notes -->" (the fuller write-up of a Tuesday in-class
activity: setup, how to run it, what goes on Learning Suite). Content below a marker must use
"### " or deeper headings.
"""
import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
WEEKS_DIR = DOCS / "weeks"
HANDSON_DIR = DOCS / "handson"
ACTIVITIES_DIR = DOCS / "activities"
SITE = "https://byu-hydroinformatics.github.io/cce114-geomatics"

# ---------------------------------------------------------------------------------------
# Class meetings. kind: "concepts" (Tuesday), "hands-on" (Thursday), or "other".
# slides: list of (title, url). data: list of (title, url). activity: in-class activity.
# ---------------------------------------------------------------------------------------
DAYS = [
    dict(n=1, week=1, kind="concepts", title="Course Introduction and Introduction to GIS",
         topics=["Welcome, introductions, syllabus overview, course expectations and policies",
                 "What geomatics is: surveying, GPS, GIS, remote sensing, mapping",
                 "What a GIS is: points, polylines, polygons, attribute tables",
                 "Software for the course: QGIS (free, open source)"],
         slides=[("Course Introduction", f"{SITE}/slides/day-01/course-introduction.html"),
                 ("Introduction to GIS", f"{SITE}/slides/day-01/intro-to-gis.html")],
         activity="Spatial identity getting-to-know-you activity; class activity sheet on uses of GIS in civil and construction engineering",
         reading="GIS Fundamentals (Bolstad & Manson), Chapter 1",
         note="The first class meeting of the semester. In Fall it falls on a Thursday; the Tuesday/Thursday rhythm starts the following week."),
    dict(n=2, week=2, kind="concepts", title="GIS Data Models, Part 1",
         topics=["Model = abstraction of reality", "Data model vs. file format",
                 "Vector data models: point, polyline, polygon", "Raster and TIN data models",
                 "Encoding a state boundary with numbers: Cartesian, polar, TIN, raster"],
         slides=[("GIS Data Models & File Formats", f"{SITE}/slides/day-02/gis-data-models.html")],
         data=[("UtahCountyData.zip", "https://github.com/BYU-Hydroinformatics/cce114-geomatics/releases/download/course-data-2026/UtahCountyData.zip")],
         activity="Polygon data model activity: encode a state boundary using only numbers",
         reading="GIS Fundamentals, Chapter 2 (Data Models)"),
    dict(n=3, week=2, kind="hands-on", title="GIS Data Models, Part 2: Creating and Editing GIS Data", handson="week-02",
         topics=["Raster and image data models, continued", "Make a map in QGIS using each data type",
                 "Live demo of creating and editing vector data in QGIS"],
         data=[("UtahCountyData.zip", "https://github.com/BYU-Hydroinformatics/cce114-geomatics/releases/download/course-data-2026/UtahCountyData.zip")],
         activity="First Map: Utah County: build a QGIS project with a basemap, the four Utah County layers, and your own point layer, and upload a screenshot"),
    dict(n=4, week=3, kind="concepts", title="Maps, Symbology, and Cartography, Part 1",
         slides=[("Maps, Symbology, and Cartography", f"{SITE}/slides/day-04/maps-and-cartography.html")],
         topics=["Map design fundamentals", "Symbology for points, lines, and polygons",
                 "Labels, legends, scale bars, and layout elements"],
         reading="GIS Fundamentals, Chapter 4 (Maps, Data Entry, and Editing) map design sections"),
    dict(n=5, week=3, kind="hands-on", title="Maps, Symbology, and Cartography, Part 2", handson="week-03",
         topics=["Follow along: make a map of the United States",
                 "Practice point, line, and polygon symbology", "Explore the attribute table", "Add labels"],
         data=[("United States shapefiles (same zip as the one on Learning Suite)",
                "data/united-states-shapefiles.zip")],
         activity="Playing with Symbology: make a colorful map in QGIS and upload a screenshot"),
    dict(n=6, week=4, kind="concepts", title="The Global Positioning System",
         slides=[("The Global Positioning System", f"{SITE}/slides/day-06/gps-part-1.html"),
                 ("GPS extended slides: trilateration build, error budget, meters demo (reference)", f"{SITE}/slides/day-07/gps-part-2.html")],
         topics=["How GPS and GNSS positioning work", "Trilateration: where is Air Force One?",
                 "Latitude and longitude, precision, and error",
                 "Converting from latitude/longitude to meters, and why it is not straightforward"],
         activity="Find Air Force One, then Where Am I: trilaterate Prague on paper from three signal delays and upload a photo of your solution",
         reading="GIS Fundamentals, Chapter 5 (GNSS and Coordinate Surveying)"),
    dict(n=7, week=4, kind="hands-on", title="Campus Field Trip", handson="week-04",
         handson_heading="Week 4 Hands-On Campus Field Trip",
         topics=["Collect phone GPS readings on campus",
                 "Import them into QGIS and convert to UTM meters",
                 "Compare readings from the same site"],
         activity="GPS Class Activity: enter three campus positions in the shared sheet and record the site names on Learning Suite"),
    dict(n=8, week=5, kind="concepts", title="Working with Vector Data, Part 1",
         slides=[("Working with Vector Data", f"{SITE}/slides/day-08/working-with-vector-data.html")],
         topics=["Creating vector data", "Digitizing and editing", "Attribute tables and schemas", "Saving to disk: GeoPackage and shapefile"],
         reading="GIS Fundamentals, Chapter 4 (Maps, Data Entry, and Editing)"),
    dict(n=9, week=5, kind="hands-on", title="Working with Vector Data, Part 2", handson="week-05",
         topics=["Hands-on practice creating, digitizing, and editing vector layers", "Snapping and topology"],
         activity="Creating and Editing Vector Data: digitize your home with snapped lines and upload a screenshot or PDF"),
    dict(n=10, week=6, kind="concepts", title="Working with Raster Data, Part 1",
         slides=[("Raster Analysis and Map Algebra", f"{SITE}/slides/day-10/raster-analysis-and-map-algebra.html")],
         topics=["Raster data structure: cells, resolution, extent, no-data", "Raster analysis and map algebra",
                 "Digital elevation models and derived surfaces"],
         activity="Engineering Paper Raster Analysis: work a map algebra problem by hand and upload a photo",
         reading="GIS Fundamentals, Chapter 2 raster sections and Chapter 10 (Raster Analysis)"),
    dict(n=11, week=6, kind="hands-on", title="Working with Raster Data, Part 2", handson="week-06",
         activity="DEM Profile: upload a screenshot of a pseudocolor DEM with an elevation profile",
         topics=["Load a GeoTIFF in QGIS and read the Information and Source tabs (data type, rows and columns, cell size, units, projection)",
                 "Raster symbology: render types, singleband pseudocolor, color ramps, classification",
                 "Elevation surfaces and cross-section profiles (View > Elevation Profile, or the Profile Tool plugin)",
                 "Exam 1 review Kahoot in the last fifteen minutes"]),
    dict(n=12, week=7, kind="concepts", title="Finding Spatial Data and Web Services",
         slides=[("Finding Spatial Data and Web Services", f"{SITE}/slides/day-12/finding-spatial-data-and-web-services.html")],
         topics=["Where spatial data comes from: government repositories and data portals",
                 "Online data sources and servers at the Utah Geospatial Resource Center (UGRC)",
                 "Web map services: WMS, WMTS, ArcGIS REST, XYZ tiles"],
         reading="GIS Fundamentals, Chapter 7 (Digital Data)"),
    dict(n=13, week=7, kind="hands-on", title="Getting Data through Web Mapping Services", handson="week-07",
         topics=["Connect QGIS to online services", "Build a layout from live web layers"],
         activity="Build a map using three or more layers from the Utah ArcGIS REST services and upload a nice layout",
         note="Concepts Exam 1 is taken in the Testing Center this week."),
    dict(n=14, week=8, kind="concepts", title="Geodesy, Projections, and Coordinate Systems, Part 1",
         slides=[("Geodesy, Projections, and Coordinate Systems", f"{SITE}/slides/day-14/coordinate-systems-and-projections.html")],
         topics=["The shape of the Earth: geoid, ellipsoid, datums", "Map projections and distortion",
                 "Geographic vs. projected coordinate systems; UTM and state plane"],
         links=[("XKCD on projections", "https://xkcd.com/977/"), ("The True Size", "https://www.thetruesize.com/"),
                ("Projection transitions (Jason Davies)", "https://www.jasondavies.com/maps/transition/")],
         reading="GIS Fundamentals, Chapter 3 (Geodesy, Datums, Map Projections, and Coordinate Systems)"),
    dict(n=15, week=8, kind="hands-on", title="Geodesy, Projections, and Coordinate Systems, Part 2", handson="week-08",
         topics=["Explore projections in QGIS: project CRS, layer CRS, on-the-fly reprojection",
                 "Reproject a layer for real and compare measured lengths and areas",
                 "Choosing a projection for an engineering problem"],
         activity="Playing with Projections: upload a screenshot of the same data in two different projections"),
    dict(n=16, week=9, kind="concepts", title="Metadata, Part 1",
         slides=[("Spatial Metadata", f"{SITE}/slides/day-16/metadata.html")],
         topics=["What metadata is and why it matters", "Metadata standards and styles", "Reading metadata to judge whether data is fit for use"],
         links=[("A brief metadata melodrama", "http://t.ly/rPYx")],
         activity="What I learned about metadata: write down a couple of things you learned today"),
    dict(n=17, week=9, kind="hands-on", title="Metadata, Part 2", handson="week-09",
         topics=["Creating and editing metadata in QGIS", "Finding and evaluating datasets on gis.utah.gov and data.gov"],
         activity="AGRC Metadata: evaluate one published dataset and fill a row of the AGRC Metadata tab in the class sheet"),
    dict(n=18, week=10, kind="concepts", title="Geoprocessing, Part 1",
         slides=[("Introduction to Geoprocessing", f"{SITE}/slides/day-18/introduction-to-geoprocessing.html")],
         topics=["Introduction to geoprocessing and spatial analysis", "Buffer, clip, intersect, select by location",
                 "Introduction to the Yellowstone Disaster scenario"],
         links=[("Yellowstone movie clip", "https://www.youtube.com/watch?v=JGEgTXsGOPk&t=346s")],
         reading="GIS Fundamentals, Chapter 9 (Basic Spatial Analysis)"),
    dict(n=19, week=10, kind="hands-on", title="Geoprocessing, Part 2", handson="week-10",
         topics=["Cities near rivers analysis in QGIS", "Chaining tools into a workflow"],
         data=[("United States data for the cities-near-rivers analysis", "")],
         activity="Cities Near Rivers: upload a screenshot of your map showing all U.S. cities within 10 km of a major river"),
    dict(n=20, week=11, kind="concepts", title="Geoplanning and Georeferencing",
         topics=["Introduction to geoplanning", "Domes for the World and the Mozambique project",
                 "Georeferencing: attaching real-world coordinates to an image that has none"],
         activity="Georeference Your Neighborhood Sketch: draw your neighborhood in pencil, photograph it, email it to yourself, and georeference it in QGIS"),
    dict(n=21, week=11, kind="hands-on", title="Georeferencing in QGIS and the Web Mapping with AI Kickoff", handson="week-11",
         topics=["Georeference a scanned historic map: ground control points, transformation types, residuals",
                 "What a site plan for the Domes for Mozambique project needs from georeferencing",
                 "Web Mapping with AI Experience kickoff: from a QGIS layer to a public web map with an AI assistant"],
         links=[("Web Mapping with AI Experience", "../assignments/web-mapping-with-ai.md")]),
    dict(n=22, week=12, kind="concepts", title="Project Site Selection, Part 1",
         slides=[("Project Site Selection: the Walmart Problem", f"{SITE}/slides/day-22/walmart-site-selection.html")],
         topics=["Site selection as a process of elimination", "Geoprocessing site selection example: Walmart"],
         links=[("Walmart open data", "https://walmart-open-data-walmarttech.opendata.arcgis.com/")]),
    dict(n=23, week=12, kind="hands-on", title="Project Site Selection, Part 2", handson="week-12",
         slides=[("Final Mapping Project", f"{SITE}/slides/day-23/final-project.html"), ("Concepts Review", f"{SITE}/slides/day-23/concepts-review.html")],
         topics=["Review workflow diagrams and the Lab 11 model", "Final mapping project kickoff: choose a county and a problem", "Exam 2 review Kahoot"],
         note="Concepts Exam 2 is taken in the Testing Center this week."),
    dict(n=24, week=13, kind="other", title="Final Project Work Session",
         topics=["No formal lecture; come work on your final project with help from the instructors and TAs"]),
    dict(n=25, week=13, kind="other", title="Final Project Work Session or Holiday",
         topics=["In Fall this is Thanksgiving and there is no class; in Winter it is a work session"]),
    dict(n=26, week=14, kind="other", title="Introduction to CCE 414 and Final Project Work Session",
         slides=[("Introduction to CCE 414", f"{SITE}/slides/day-21/intro-to-cce-414.html")],
         topics=["A short introduction to CCE 414: Engineering Applications of GIS, the follow-on course",
                 "Then work on your final project in class, and into the lab hour, with the instructor's help"],
         links=[("Prior-year recording of the CCE 414 introduction", "https://youtu.be/RIzy0JRB8VI")]),
    dict(n=27, week=14, kind="other", title="Final Project Presentations",
         topics=["Groups present their final mapping projects; presentations continue on Tuesday of Week 15"]),
    dict(n=28, week=15, kind="other", title="Final Project Presentations, Part 2, and Exam Review",
         topics=["Remaining final project presentations",
                 "Final exam review; the exam itself is given during finals week in the university-scheduled slot for this class, in the regular classroom (exact date and time on Learning Suite)",
                 "The final is a practical, hands-on exam in QGIS; AI tools are not permitted"]),
    dict(n=29, week=15, kind="other", title="Last Day of Class",
         topics=["Final exam study session or wrap-up; in some semesters this is a university reading day with no class"]),
]

# What is due each week. quiz: (number, title); lab: number; both due Saturday 11:59 pm.
# also: everything else (exams, experiences, final project), with its timing in parentheses;
# shown in the "Also this week" callout above the four cards.
WEEKS = {
    1: dict(theme="Introduction"),
    2: dict(theme="GIS Data Models", quiz=(1, "Intro to GIS & Map Design Fundamentals"), lab=1),
    3: dict(theme="Maps, Symbology, and Cartography", quiz=(2, "Spatial Data Models and File Types"), lab=2),
    4: dict(theme="The Global Positioning System", quiz=(3, "GPS, Part 1"), lab=3),
    5: dict(theme="Working with Vector Data", quiz=(4, "GPS, Part 2"), lab=4),
    6: dict(theme="Working with Raster Data", quiz=(5, "Getting Started with Raster Data"), lab=5,
            also=["BYU Belonging Map (Wednesday)"]),
    7: dict(theme="Finding Spatial Data and Web Services", lab=6,
            also=["Concepts Exam 1 (Testing Center, midweek)"]),
    8: dict(theme="Geodesy, Projections, and Coordinate Systems", quiz=(6, "Map Projections and Coordinate Systems"), lab=7),
    9: dict(theme="Metadata", quiz=(7, "Metadata"), lab=8),
    10: dict(theme="Geoprocessing", quiz=(8, "Geoprocessing and Spatial Data Analysis"), lab=9,
             also=["Community and Professional Map Experience (Wednesday)"]),
    11: dict(theme="Geoplanning and Georeferencing", lab=10),
    12: dict(theme="Project Site Selection", lab=11, also=["Concepts Exam 2 (Testing Center)"]),
    13: dict(theme="Final Project"),
    14: dict(theme="Final Project", also=["Web Mapping with AI Experience (Wednesday)",
                                          "Final project presentations (Thursday)", "Final Project (Saturday)"]),
    15: dict(theme="Presentations and Exam Review", also=["Final Exam (finals week, university-scheduled slot)",
                                                          "Course evaluation (extra credit)"]),
}


def due_items(w: int) -> list:
    """Everything due in week w as display strings, for the schedule overview's Due column."""
    info = WEEKS[w]
    items = [f"Quiz {info['quiz'][0]}: {info['quiz'][1]}"] if info.get("quiz") else []
    items += [f"Lab {info['lab']}"] if info.get("lab") else []
    return items + info.get("also", [])

LABS = {1: "Getting Started with GIS", 2: "Map Symbology and Layouts", 3: "GPS Data Collection and Importing Into QGIS",
        4: "Changing, Editing, and Fixing GIS Data", 5: "Working with Raster Data", 6: "Spatial Data Web Services",
        7: "Projections and Coordinate Systems", 8: "Metadata", 9: "The Yellowstone Disaster",
        10: "Domes for Mozambique", 11: "Walmart Site Selection"}

# Session types. Each has a badge label and a CSS modifier class; docs/stylesheets/extra.css
# renders them as colored pills. Instructors are deliberately not named here: who teaches which
# day changes between semesters (CLAUDE.md rule 7).
KIND_LABEL = {"concepts": "Lecture", "hands-on": "Hands-On Practice", "other": "Class Session"}
KIND_CLASS = {"concepts": "badge-lecture", "hands-on": "badge-handson", "other": "badge-session"}
# Emoji were tried here and render inconsistently in the theme's font stack (the mouse glyph
# does not render at all on the lab machines), so session type is carried by the CSS badges.
# The week-page card icons are different: pymdownx.emoji inlines them as SVG, so they do not
# depend on any font.


def badge(kind: str) -> str:
    """An inline attribute-list span; attr_list turns it into <strong class="badge ...">."""
    return f"**{KIND_LABEL[kind]}**{{ .badge .{KIND_CLASS[kind]} }}"

# Thursday sessions get the run sheet's applied title instead of the lecture-generator's
# academic title, since the two are now the same page. Keyed by day number.
THURSDAY_TITLE = {
    3: "First Map in QGIS",
    5: "Symbology, Labels, and a First Layout",
    7: "Campus Field Trip",
    9: "Digitize Your Home with Snapping and the Vertex Tool",
    11: "Raster Data in QGIS and an Elevation Profile",
    13: "Web Services in QGIS",
    15: "Playing with Projections",
    17: "Writing and Evaluating Metadata",
    19: "Cities Near Rivers",
    21: "Georeferencing in QGIS, and the Web Mapping with AI Kickoff",
    23: "Workflow Walkthrough, Final Project Kickoff, Exam 2 Kahoot",
}

# Tuesday activities with a fuller write-up (setup, how to run it, what goes on Learning Suite),
# each on its own page at docs/activities/week-NN.md, below a "<!-- notes -->" marker. Keyed by
# day number; the value is the page title. The write-ups used to sit inline on the week pages.
ACTIVITY_GUIDES = {
    2: "State Boundary Data Model",
    6: "Find Air Force One, and Where Am I?",
    10: "Engineering Paper Raster Analysis",
    12: "Data Source Scavenger Hunt",
    14: "Globe Activity: The Great Circle",
    16: "A Brief Metadata Melodrama",
    20: "Georeference Your Neighborhood Sketch",
}

# The four cards every week page carries, in order: (key, heading, icon, text when empty).
# Icons are Material Design icons inlined as SVG by pymdownx.emoji; colors are in extra.css.
CARDS = [
    ("slides",   "Presentation Slides", "material-presentation-play",      "No slides this week."),
    ("practice", "In-Class Practice",   "material-account-group",          "No in-class practice this week."),
    ("lab",      "Lab Assignment",      "material-flask",                  "No lab this week."),
    ("quiz",     "Reading Quiz",        "material-book-open-page-variant", "No reading quiz this week."),
]


# Self-check quizzes, keyed by week. Each is a self-contained page at
# docs/quizzes/<slug>/index.html that MkDocs copies through untouched, reached in class by
# the QR code on that week's deck and from the week page afterward by anyone who missed the
# scan. Nothing is graded and nothing is handed in.
PRACTICE = {
    1: [("what-is-gis", "What Is a GIS?",
         "What a GIS is and is not, the three vector feature types and the attribute table "
         "behind them, and how this course works.")],
    2: [("data-models", "Model, Format, or Reality?",
         "Telling a data model from reality and from the file format it is stored in, naming "
         "vector, raster, and TIN, and what each one costs.")],
    3: [("map-elements", "Does This Map Work?",
         "The required map elements, what makes a map ugly, and what a map does to the reader "
         "looking at it.")],
    4: [("gps", "How Does It Know Where You Are?",
         "How a receiver turns a radio signal into a position, what the digits of a coordinate are "
         "worth, and where GPS error comes from.")],
    5: [("vector", "Who Drew That Line?",
         "Choosing a geometry type, digitizing at a scale the data can support, and what a field's "
         "type costs you later.")],
    6: [("raster", "Where Should the Water Park Go?",
         "What a grid of cells really holds, map algebra one cell at a time, and what a DEM gives "
         "you for free.")],
    7: [("find-data", "Who Already Has This Data?",
         "Where spatial data actually comes from, the difference between a picture of the data and "
         "the features themselves, and getting Utah's data into QGIS.")],
    8: [("projections", "Why Is Greenland So Big?",
         "What every flat map gives up, how a projection is fitted to the ground, and the "
         "difference between declaring a CRS and reprojecting into one.")],
    9: [("metadata", "Would You Drink It?",
         "What a dataset with no documentation costs you, and how to read a metadata record and "
         "decide whether to trust the data.")],
    10: [("geoprocessing", "Which Tool Answers the Question?",
          "Turning a question into a selection, what each overlay tool puts out, and the order to "
          "chain them in.")],
    12: [("siting", "Where Would You Put It?",
          "Reading a stated requirement as an operation, chaining the operations, and knowing what "
          "the surviving polygons do and do not tell you.")],
}


# The Learning Suite "In Class Activity" name for each hands-on day, used in the hands-on
# index. Taken from the "Graded item" row of each run sheet; None where Thursday has no item.
ACTIVITY_NAME = {3: "First Map: Utah County", 5: "Playing with Symbology", 7: "GPS Class Activity",
                 9: "Creating and Editing Vector Data", 11: "DEM Profile",
                 13: "Getting Data through Web Mapping Services", 15: "Playing with Projections",
                 17: "AGRC Metadata", 19: "Cities Near Rivers", 21: None, 23: None}


def lab_link(text: str, prefix: str) -> str:
    m = re.match(r"Lab (\d+)$", text)
    if m:
        n = int(m.group(1))
        return f"[Lab {n}: {LABS[n]}]({prefix}assignments/lab-{n:02d}/README.md)"
    if text.startswith("Quiz"):
        return f"[{text}]({prefix}assignments/deliverables.md#reading-quizzes)"
    if "Exam" in text:
        return f"[{text}]({prefix}policies/exams.md)"
    if "Final Project" in text:
        return f"[{text}]({prefix}assignments/final-project.md)"
    if "Web Mapping" in text:
        return f"[{text}]({prefix}assignments/web-mapping-with-ai.md)"
    if "presentations" in text:
        return f"[{text}]({prefix}assignments/final-project.md)"
    if "Experience" in text or "Belonging" in text:
        return f"[{text}]({prefix}assignments/deliverables.md#experiences)"
    if "evaluation" in text:
        return f"[{text}]({prefix}policies/grading.md)"
    return text


def week_reading(w: int) -> str:
    """The assigned reading for a week, gathered from that week's class meetings."""
    seen = []
    for d, _ in week_sessions(w):
        if d.get("reading") and d["reading"] not in seen:
            seen.append(d["reading"])
    return "; ".join(seen)


def slug(text: str) -> str:
    """Mirror python-markdown's default toc slugify so links can target a heading."""
    import unicodedata
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def session_heading(d: dict, weekday: Optional[str]) -> str:
    return f"{weekday} — {session_title(d)}" if weekday else f"Day {d['n']} — {session_title(d)}"


def week_sessions(w: int) -> list:
    """(day, weekday) pairs for a week; a single-meeting week has weekday None."""
    days = [d for d in DAYS if d["week"] == w]
    weekdays = [None] if len(days) == 1 else ["Tuesday", "Thursday"]
    return list(zip(days, weekdays))


def session_title(d: dict) -> str:
    return THURSDAY_TITLE.get(d["n"], d["title"]) if d["kind"] == "hands-on" else d["title"]


def preserved_after(existing_text: str, marker: str) -> Optional[str]:
    """Hand-written content directly below `marker`, up to (not including) the next
    top-level "## " session heading. Content pasted below a marker must use "### " or
    deeper so it is not mistaken for the start of the next session."""
    if marker not in existing_text:
        return None
    rest = existing_text[existing_text.index(marker) + len(marker):]
    end = re.search(r"\n## ", rest)
    return (rest[:end.start()] if end else rest).strip("\n")


def handson_callout(d: dict) -> list:
    """The prominent link from a week page out to that Thursday's hands-on page."""
    w = d["week"]
    return ['<div class="handson-cta" markdown="1">', "",
            "**Hands-On Practice**{ .handson-cta__eyebrow }", "",
            f"**{session_title(d)}**{{ .handson-cta__title }}", "",
            "This session has its own step-by-step guide: what you need, an overview, the "
            "click-by-click QGIS walkthrough, what to hand in, and the snags that usually "
            "come up.", "",
            f"[Open the Week {w} hands-on guide \u2192](../handson/week-{w:02d}.md)"
            "{ .handson-cta__button }", "",
            "</div>", ""]


def handson_day(w: int) -> Optional[dict]:
    """The hands-on meeting of week w, if it has one."""
    for d in DAYS:
        if d["week"] == w and d["kind"] == "hands-on":
            return d
    return None


def handson_page(d: dict, existing_text: str) -> str:
    """A standalone page for one Thursday hands-on session.

    Everything above the "<!-- runsheet -->" marker is regenerated on every run. The run sheet
    itself (at a glance, practice run, before class, the plan, the walkthrough, the graded
    upload, common snags) is hand-written below the marker and is never touched, so it must
    start at "### " or deeper."""
    w, info = d["week"], WEEKS[d["week"]]
    heading = d.get("handson_heading", f"Week {w} Hands-On — {session_title(d)}")
    out = [f"# {heading}", "",
           f"{badge('hands-on')} · *Day {d['n']} · Thursday of "
           f"[Week {w} — {info['theme']}](../weeks/week-{w:02d}.md)*", ""]
    if d.get("note"):
        out += ["> [!NOTE]", f"> {d['note']}", ""]
    out += ["### Topics", ""] + [f"- {x}" for x in d["topics"]] + [""]
    if d.get("slides"):
        out += ["### Slides", ""] + [f"- [{a}]({b})" for a, b in d["slides"]] + [""]
    if d.get("data") or d.get("links"):
        out += ["### Materials", ""]
        for a, b in d.get("data", []):
            out.append(f"- {a}: [download]({b})" if b else f"- {a} (posted on Learning Suite)")
        for a, b in d.get("links", []):
            out.append(f"- [{a}]({b})")
        out.append("")
    # The graded item is not repeated here: every run sheet's "At a glance" table names it.
    out.append("<!-- runsheet -->")
    preserved = preserved_after(existing_text, "<!-- runsheet -->")
    out.append(preserved if preserved else "")
    return "\n".join(out).rstrip("\n") + "\n"


def handson_index() -> str:
    out = ["# Hands-On Practice", "",
           "Every Thursday of Weeks 2 through 12 is a working session in QGIS 3.44. Each one has "
           "its own page below: what the session is for, what to have ready, a practice run you "
           "can do on your own beforehand, a minute-by-minute plan, the click-by-click "
           "walkthrough, the graded upload, and the snags that usually come up.", "",
           "Weeks 1, 13, 14 and 15 have no hands-on session. Week 1 meets once, Week 13 is a work "
           "session or holiday, and Weeks 14 and 15 are final project presentations.", "",
           "| Week | Session | Feeds | Graded activity |",
           "| --- | --- | --- | --- |"]
    for w in WEEKS:
        d = handson_day(w)
        if not d:
            continue
        lab = LABS.get(w - 1)
        lab_cell = f"[Lab {w - 1}](../assignments/lab-{w - 1:02d}/README.md)" if lab else "—"
        act = ACTIVITY_NAME.get(d["n"]) or "—"
        out.append(f"| {w} | [{session_title(d)}](week-{w:02d}.md) | {lab_cell} | {act} |")
    out += ["", "> [!TIP]", "> Each page is written so that someone who has never run the session "
            "can rehearse it alone in about twenty minutes before class.", ""]
    return "\n".join(out)


def activity_page(w: int, d: dict, existing_text: str) -> str:
    """A standalone page for one Tuesday in-class activity. Everything above "<!-- notes -->" is
    regenerated; the write-up below it is hand-written and never touched."""
    out = [f"# Week {w} Activity — {ACTIVITY_GUIDES[d['n']]}", "",
           f"{badge('concepts')} · *Day {d['n']} · Tuesday of "
           f"[Week {w} — {WEEKS[w]['theme']}](../weeks/week-{w:02d}.md)*", ""]
    if d.get("activity"):
        out += [f"**Graded in-class activity.** {d['activity']}. Record your completion on Learning Suite.", ""]
    else:
        out += ["Not graded.", ""]
    out.append("<!-- notes -->")
    preserved = preserved_after(existing_text, "<!-- notes -->")
    out.append(preserved if preserved else "")
    return "\n".join(out).rstrip("\n") + "\n"


def when_label(d: dict, weekday: Optional[str]) -> str:
    return f"**{weekday}**" if weekday else f"**Day {d['n']}**"


def week_page(w: int) -> str:
    """Four cards — slides, in-class practice, lab, reading quiz — under an optional callout."""
    info = WEEKS[w]
    sessions = week_sessions(w)
    body = {k: [] for k, *_ in CARDS}

    # Presentation Slides: every deck this week, Tuesday's with its topics as the description.
    materials = []
    for d, weekday in sessions:
        when = when_label(d, weekday)
        topics = "; ".join(d.get("topics", [])) if d["kind"] == "concepts" else ""
        for i, (title, url) in enumerate(d.get("slides", [])):
            desc = f" — {topics}" if topics and i == 0 else ""
            body["slides"].append(f"- {when} — [{title}]({url}){desc}")
        if d["kind"] == "concepts" and not d.get("slides"):
            body["slides"].append(f"- {when} — {d['title']} (slides not posted yet) — {topics}")
        if d["kind"] == "concepts":
            materials += [f"[{a}]({b})" if b else f"{a} (on Learning Suite)" for a, b in d.get("data", [])]
            materials += [f"[{a}]({b})" for a, b in d.get("links", [])]
    if any(d.get("slides") for d, _ in sessions):
        body["slides"] += ["", "Press <kbd>F</kbd> for fullscreen and <kbd>P</kbd> for presenter view with speaker notes."]
    if materials:
        body["slides"] += ["", "**Materials:** " + " · ".join(materials)]

    # In-Class Practice: Tuesday's activity, Thursday's hands-on guide, or what happens in class.
    for d, weekday in sessions:
        when = when_label(d, weekday)
        guide = f"../activities/week-{w:02d}.md" if d["n"] in ACTIVITY_GUIDES else None
        if d["kind"] == "hands-on":
            if body["practice"]:
                body["practice"].append("")
            body["practice"] += handson_callout(d)
        elif d["kind"] == "concepts" and d.get("activity"):
            line = f"- {when} — {d['activity']}. Record your completion on Learning Suite."
            body["practice"].append(line + (f" [Activity guide]({guide})" if guide else ""))
        elif d["kind"] == "concepts" and guide:
            body["practice"].append(f"- {when} — [{ACTIVITY_GUIDES[d['n']]}]({guide}) (not graded).")
        elif d["kind"] == "other":
            body["practice"].append(f"- {when} — **{d['title']}.** " + " ".join(
                x if x.endswith(".") else x + "." for x in d.get("topics", [])))
    if w in PRACTICE:
        if body["practice"]:
            body["practice"].append("")
        body["practice"] += ["Self-check quizzes — not graded; open them on a phone or laptop as often as you like:", ""]
        body["practice"] += [f"- [{title}](../quizzes/{s}/index.html) — {desc}" for s, title, desc in PRACTICE[w]]

    # Lab Assignment.
    if info.get("lab"):
        n = info["lab"]
        body["lab"] += [f"[Lab {n} — {LABS[n]}](../assignments/lab-{n:02d}/README.md)", "",
                        "Due **Saturday at 11:59 pm** on Learning Suite."]

    # Reading Quiz: this week's reading, and the quiz due this week.
    reading = week_reading(w)
    if reading:
        body["quiz"].append(f"**This week's reading:** {reading}.")
    if info.get("quiz"):
        n, title = info["quiz"]
        if body["quiz"]:
            body["quiz"].append("")
        body["quiz"].append(f"**Quiz {n} — {title}** on Learning Suite: open book. Due **Saturday at 11:59 pm**. "
                            "See [Reading Quizzes](../assignments/deliverables.md#reading-quizzes).")
    elif reading:
        body["quiz"] += ["", "*No quiz due this week.*"]

    out = [f"# Week {w} — {info['theme']}", ""]
    # Anchors for the old per-session headings, which Learning Suite and the schedule link to.
    out += [" ".join(f'<span id="{slug(session_heading(d, wd))}"></span>' for d, wd in sessions), ""]

    also = [f"- {lab_link(x, '../')}" for x in info.get("also", [])]
    also += [f"- {d['note']}" for d, _ in sessions if d.get("note") and d["kind"] != "hands-on"]
    if also:
        out += ["> [!IMPORTANT] Also this week"] + [f"> {x}" for x in also] + [""]

    for key, heading, icon, empty in CARDS:
        out += [f'<div class="week-card week-card--{key}" markdown>', "", f"## :{icon}: {heading}", ""]
        out += body[key] or [f"*{empty}*"]
        out += ["", "</div>", ""]
    out += ["> [!NOTE]", "> If you see a discrepancy between Learning Suite and this page, please let us know so "
            "we can rectify it.", ""]
    return "\n".join(out)


def schedule_page() -> str:
    out = ["# Schedule", "",
           "CCE 114 is taught every **Fall** (September to December) and **Winter** (January to April).",
           "The sequence below is the same each semester; only the calendar dates change, so this page",
           "uses week numbers and weekdays. Exact due dates are on Learning Suite.", "",
           "Each week has two class meetings, presented together on that week's page:", "",
           f"- {badge('concepts')} **Tuesday.** Concepts, discussion, and a short in-class "
           "activity.",
           f"- {badge('hands-on')} **Thursday.** Working in QGIS on the week's topic. Every "
           "session has its own step-by-step guide under [Hands-On Practice](handson/README.md), "
           "written so it can be rehearsed alone beforehand.", "",
           "Reading quizzes open on Tuesday and close **Saturday at 11:59 pm**; lab reports are also due **Saturday at 11:59 pm**.", "",
           "| Week | Tuesday (lecture) | Thursday (hands-on practice) | Due this week |",
           "| --- | --- | --- | --- |"]
    for w, info in WEEKS.items():
        page = f"weeks/week-{w:02d}.md"
        cells = {"Tuesday": "—", "Thursday": "—"}
        for d, weekday in week_sessions(w):
            # A hands-on session links straight to its own guide; everything else links to the
            # session heading on the week page, which is what Learning Suite points at.
            target = (f"handson/week-{w:02d}.md" if d["kind"] == "hands-on"
                      else f"{page}#{slug(session_heading(d, weekday))}")
            link = f"[{session_title(d)}]({target})"
            cells[weekday or "Thursday"] = link   # Week 1 meets only on Thursday
        due = "<br>".join(lab_link(x, "") for x in due_items(w)) or "—"
        out.append(f"| [Week {w}: {info['theme']}]({page}) | {cells['Tuesday']} | {cells['Thursday']} | {due} |")
    out += ["", "Holidays and reading days shift between semesters; Week 13 and Week 15 absorb them.", ""]
    return "\n".join(out)


def update_nav(mkdocs_yml: Path) -> None:
    text = mkdocs_yml.read_text()
    # schedule.md keeps its URL so existing Learning Suite links still resolve, so the
    # overview is a labeled first child of the Schedule section rather than its index.
    lines = ["  - Schedule:", "      - Overview: schedule.md"]
    for w, info in WEEKS.items():
        lines.append(f"      - \"Week {w} — {info['theme']}\": weeks/week-{w:02d}.md")
    block = "\n".join(lines) + "\n"
    text, n = re.subn(r"  - Schedule:\n(?:      .*\n)*", block, text)
    if n != 1:
        raise SystemExit("mkdocs.yml: expected exactly one '  - Schedule:' nav block")

    mkdocs_yml.write_text(text)


def main() -> None:
    (DOCS / "schedule.md").write_text(schedule_page())
    WEEKS_DIR.mkdir(exist_ok=True)
    for w in WEEKS:
        path = WEEKS_DIR / f"week-{w:02d}.md"
        path.write_text(week_page(w))
    ACTIVITIES_DIR.mkdir(exist_ok=True)
    for d in DAYS:
        if d["n"] in ACTIVITY_GUIDES:
            path = ACTIVITIES_DIR / f"week-{d['week']:02d}.md"
            existing = path.read_text() if path.exists() else ""
            path.write_text(activity_page(d["week"], d, existing))
    HANDSON_DIR.mkdir(exist_ok=True)
    (HANDSON_DIR / "README.md").write_text(handson_index())
    n_handson = 0
    for w in WEEKS:
        d = handson_day(w)
        if not d:
            continue
        path = HANDSON_DIR / f"week-{w:02d}.md"
        existing = path.read_text() if path.exists() else ""
        path.write_text(handson_page(d, existing))
        n_handson += 1
    update_nav(ROOT / "mkdocs.yml")
    print(f"wrote schedule.md, {len(WEEKS)} week pages, {n_handson} hands-on pages "
          f"plus their index, {len(ACTIVITY_GUIDES)} activity guides, and the Schedule nav")


if __name__ == "__main__":
    main()
