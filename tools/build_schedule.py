#!/usr/bin/env python3
"""Generate the week-by-week schedule page and one page per week of the course.

The course runs every Fall (Sep-Dec) and Winter (Jan-Apr). Everything here is expressed
as week numbers and weekdays, never calendar dates, so the site does not need a rewrite
each semester: Tuesdays are concept lectures (Dr. Ames), Thursdays are demos and hands-on
work (Dr. Halgren). Day numbers count class meetings from the first one.

Edit the DAYS and WEEKS tables below, then run:  python3 tools/build_schedule.py
It rewrites docs/schedule.md, docs/weeks/week-NN.md (one per week), and the Schedule
section of mkdocs.yml.

Each week page has two generated parts (topics, slides, materials, one-line activity
blurb, reading, due list) rebuilt from the tables below every run, plus up to two
hand-written zones that survive a rerun: everything below a "<!-- tuesday-notes -->"
marker (the fuller write-up of that week's in-class activity) and everything below a
"<!-- thursday-notes -->" marker (the instructor run sheet: at-a-glance, prep, the
50-minute plan, the walkthrough, the graded upload, and common snags). Add a marker by
hand to a week page to start a preserved zone; re-running the script never touches
content below a marker that is already there.
"""
import re
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
WEEKS_DIR = DOCS / "weeks"
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
         data=[("UtahCountyData.zip", f"{SITE}/lectures/data/UtahCountyData.zip")],
         activity="Polygon data model activity: encode a state boundary using only numbers",
         reading="GIS Fundamentals, Chapter 2 (Data Models)"),
    dict(n=3, week=2, kind="hands-on", title="GIS Data Models, Part 2: Creating and Editing GIS Data", handson="week-02",
         topics=["Raster and image data models, continued", "Make a map in QGIS using each data type",
                 "Live demo of creating and editing vector data in QGIS"],
         data=[("UtahCountyData.zip", f"{SITE}/lectures/data/UtahCountyData.zip")],
         activity="State Boundary Vector Data Model activity (trade coordinate lists with a neighbor and guess the state)"),
    dict(n=4, week=3, kind="concepts", title="Maps, Symbology, and Cartography, Part 1",
         slides=[("Maps, Symbology, and Cartography", f"{SITE}/slides/day-04/maps-and-cartography.html")],
         topics=["Map design fundamentals", "Symbology for points, lines, and polygons",
                 "Labels, legends, scale bars, and layout elements"],
         reading="GIS Fundamentals, Chapter 4 (Maps, Data Entry, and Editing) map design sections"),
    dict(n=5, week=3, kind="hands-on", title="Maps, Symbology, and Cartography, Part 2", handson="week-03",
         topics=["Follow along: make a map of the United States",
                 "Practice point, line, and polygon symbology", "Explore the attribute table", "Add labels"],
         data=[("United States shapefiles", "")],
         activity="Playing with Symbology: make a colorful map in QGIS and upload a screenshot"),
    dict(n=6, week=4, kind="concepts", title="The Global Positioning System",
         slides=[("The Global Positioning System", f"{SITE}/slides/day-06/gps-part-1.html"),
                 ("GPS extended slides: trilateration build, error budget, meters demo (reference)", f"{SITE}/slides/day-07/gps-part-2.html")],
         topics=["How GPS and GNSS positioning work", "Trilateration: where is Air Force One?",
                 "Latitude and longitude, precision, and error",
                 "Converting from latitude/longitude to meters, and why it is not straightforward"],
         activity="Find Air Force One, then Where Am I: trilaterate Prague on paper from three signal delays and upload a photo of your solution",
         reading="GIS Fundamentals, Chapter 5 (GNSS and Coordinate Surveying)"),
    dict(n=7, week=4, kind="hands-on", title="GPS Field Data Collection and Importing Into QGIS", handson="week-04",
         topics=["Twenty minutes on campus collecting positions with your phone",
                 "Importing the class points into QGIS from a CSV, assigning the CRS, and reprojecting to UTM",
                 "Seeing GPS error as the scatter between students at the same site"],
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
                 "Then work on your final project in class, and into the lab hour, with Dr. Ames' help"],
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

# Saturday deadlines and other items by week (all times 11:59 pm unless noted).
WEEKS = {
    1: dict(theme="Introduction", due=[]),
    2: dict(theme="GIS Data Models", due=["Quiz 1: Intro to GIS & Map Design Fundamentals", "Lab 1"]),
    3: dict(theme="Maps, Symbology, and Cartography", due=["Quiz 2: Spatial Data Models and File Types", "Lab 2"]),
    4: dict(theme="The Global Positioning System", due=["Quiz 3: GPS, Part 1", "Lab 3"]),
    5: dict(theme="Working with Vector Data", due=["Quiz 4: GPS, Part 2", "Lab 4"]),
    6: dict(theme="Working with Raster Data", due=["Quiz 5: Getting Started with Raster Data", "Lab 5", "BYU Belonging Map (Wednesday)"]),
    7: dict(theme="Finding Spatial Data and Web Services", due=["Lab 6", "Concepts Exam 1 (Testing Center, midweek)"]),
    8: dict(theme="Geodesy, Projections, and Coordinate Systems", due=["Quiz 6: Map Projections and Coordinate Systems", "Lab 7"]),
    9: dict(theme="Metadata", due=["Quiz 7: Metadata", "Lab 8"]),
    10: dict(theme="Geoprocessing", due=["Quiz 8: Geoprocessing and Spatial Data Analysis", "Lab 9", "Community and Professional Map Experience (Wednesday)"]),
    11: dict(theme="Geoplanning and Georeferencing", due=["Lab 10"]),
    12: dict(theme="Project Site Selection", due=["Lab 11", "Concepts Exam 2 (Testing Center)"]),
    13: dict(theme="Final Project", due=[]),
    14: dict(theme="Final Project", due=["Web Mapping with AI Experience (Wednesday)", "Final project presentations (Thursday)", "Final Project (Saturday)"]),
    15: dict(theme="Presentations and Exam Review", due=["Final Exam (finals week, university-scheduled slot)", "Course evaluation (extra credit)"]),
}

LABS = {1: "Getting Started with GIS", 2: "Map Symbology and Layouts", 3: "GPS Data Collection and Importing Into QGIS",
        4: "Changing, Editing, and Fixing GIS Data", 5: "Working with Raster Data", 6: "Spatial Data Web Services",
        7: "Projections and Coordinate Systems", 8: "Metadata", 9: "The Yellowstone Disaster",
        10: "Domes for Mozambique", 11: "Walmart Site Selection"}

KIND_LABEL = {"concepts": "Concepts lecture (Dr. Ames)",
              "hands-on": "Demo and hands-on (Dr. Halgren)",
              "other": "Class session"}

# Thursday sessions get the run sheet's applied title instead of the lecture-generator's
# academic title, since the two are now the same page. Keyed by day number.
THURSDAY_TITLE = {
    3: "First Map in QGIS",
    5: "Symbology, Labels, and a First Layout",
    7: "GPS Field Collection and Importing the Class Data",
    9: "Digitize Your Home with Snapping and the Vertex Tool",
    11: "Raster Data in QGIS and an Elevation Profile",
    13: "Web Services in QGIS",
    15: "Playing with Projections",
    17: "Writing and Evaluating Metadata",
    19: "Cities Near Rivers",
    21: "Georeferencing in QGIS, and the Web Mapping with AI Kickoff",
    23: "Workflow Walkthrough, Final Project Kickoff, Exam 2 Kahoot",
}

# Days whose Tuesday in-class activity has a fuller write-up preserved under a
# "<!-- tuesday-notes -->" marker (migrated once from the old tuesday-activities.md).
TUESDAY_NOTES_DAYS = {2, 6, 10, 12, 14, 16, 20}


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


def session_title(d: dict) -> str:
    return THURSDAY_TITLE.get(d["n"], d["title"]) if d["kind"] == "hands-on" else d["title"]


def session_generated_body(d: dict, skip_topics_and_activity: bool = False) -> list[str]:
    """The part of a session that is always rebuilt from the tables."""
    out = [f"*Day {d['n']} · {KIND_LABEL[d['kind']]}*", ""]
    if d.get("note"):
        out += ["> [!NOTE]", f"> {d['note']}", ""]
    if not skip_topics_and_activity:
        out += ["### Topics", ""] + [f"- {t}" for t in d["topics"]] + [""]
    if d.get("slides"):
        out += ["### Slides", ""] + [f"- [{t}]({u})" for t, u in d["slides"]] + [""]
    elif not skip_topics_and_activity:
        out += ["### Slides", "", "*Slides for this day are not on the site yet. They will be added as the semester goes.*", ""]
    if d.get("data") or d.get("links"):
        out += ["### Materials", ""]
        for t, u in d.get("data", []):
            out.append(f"- {t}: [download]({u})" if u else f"- {t} (posted on Learning Suite)")
        for t, u in d.get("links", []):
            out.append(f"- [{t}]({u})")
        out.append("")
    if not skip_topics_and_activity and d.get("activity"):
        out += ["### In-class activity", "", d["activity"] + ". Record your completion on Learning Suite.", ""]
    if d.get("reading"):
        out += ["### Reading", "", d["reading"], ""]
    return out


def preserved_after(existing_text: str, marker: str) -> Optional[str]:
    """Hand-written content directly below `marker`, up to (not including) the next
    top-level "## " session heading. Content pasted below a marker must use "### " or
    deeper so it is not mistaken for the start of the next session."""
    if marker not in existing_text:
        return None
    rest = existing_text[existing_text.index(marker) + len(marker):]
    end = re.search(r"\n## ", rest)
    return (rest[:end.start()] if end else rest).strip("\n")


def session_section(d: dict, weekday: Optional[str], existing_text: str) -> list:
    heading = f"## {weekday} — {session_title(d)}" if weekday else f"## Day {d['n']} — {session_title(d)}"
    out = [heading, ""]
    marker = None
    if d["kind"] == "hands-on":
        marker = "<!-- thursday-notes -->"
        out += session_generated_body(d, skip_topics_and_activity=True)
    elif d["kind"] in ("concepts", "other") and d["n"] in TUESDAY_NOTES_DAYS:
        marker = "<!-- tuesday-notes -->"
        out += session_generated_body(d)
    else:
        out += session_generated_body(d)
    if marker:
        out.append(marker)
        preserved = preserved_after(existing_text, marker)
        out.append(preserved if preserved else "")
        out.append("")
    return out


def week_page(w: int, existing_text: str) -> str:
    info = WEEKS[w]
    days = [d for d in DAYS if d["week"] == w]
    out = [f"# Week {w} — {info['theme']}", ""]
    due = info["due"]
    if due:
        out += ["**Due this week (Saturday, 11:59 pm unless noted):**", ""] + [f"- {lab_link(x, '../')}" for x in due] + [""]
    weekdays = [None] if len(days) == 1 else ["Tuesday", "Thursday"]
    for d, weekday in zip(days, weekdays):
        out += session_section(d, weekday, existing_text)
    return "\n".join(out).rstrip("\n") + "\n"


def schedule_page() -> str:
    out = ["# Schedule", "",
           "CCE 114 is taught every **Fall** (September to December) and **Winter** (January to April).",
           "The sequence below is the same each semester; only the calendar dates change, so this page",
           "uses week numbers and weekdays. Exact due dates are on Learning Suite.", "",
           "Each week has two class meetings, presented together on that week's page:", "",
           "- **Tuesday: concepts.** A lecture with discussion and short activities (Dr. Ames).",
           "- **Thursday: demo and hands-on.** Working in QGIS on the week's topic (Dr. Halgren).", "",
           "Reading quizzes open on Tuesday and close **Saturday at 11:59 pm**; lab reports are also due **Saturday at 11:59 pm**.", "",
           "| Week | Theme | Due this week |",
           "| --- | --- | --- |"]
    for w, info in WEEKS.items():
        due = "<br>".join(lab_link(x, "") for x in info["due"]) or "—"
        out.append(f"| [Week {w}: {info['theme']}](weeks/week-{w:02d}.md) | {info['theme']} | {due} |")
    out += ["", "Holidays and reading days shift between semesters; Week 13 and Week 15 absorb them.", ""]
    return "\n".join(out)


def update_nav(mkdocs_yml: Path) -> None:
    text = mkdocs_yml.read_text()
    lines = ["  - Schedule:", "      - Overview: schedule.md"]
    for w, info in WEEKS.items():
        lines.append(f"      - \"Week {w} — {info['theme']}\": weeks/week-{w:02d}.md")
    block = "\n".join(lines) + "\n"
    text = re.sub(r"  - Schedule: schedule\.md\n", block, text)
    text = re.sub(r"  - Thursday Hands-On:.*?(?=\n  - [A-Z])", "", text, flags=re.S)
    text = re.sub(r"  - Lectures:.*?(?=\n  - [A-Z]|\Z)", "", text, flags=re.S)
    mkdocs_yml.write_text(text)


def main() -> None:
    (DOCS / "schedule.md").write_text(schedule_page())
    WEEKS_DIR.mkdir(exist_ok=True)
    for w in WEEKS:
        path = WEEKS_DIR / f"week-{w:02d}.md"
        existing = path.read_text() if path.exists() else ""
        path.write_text(week_page(w, existing))
    update_nav(ROOT / "mkdocs.yml")
    print(f"wrote schedule.md, {len(WEEKS)} week pages, and the mkdocs nav")


if __name__ == "__main__":
    main()
