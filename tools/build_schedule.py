#!/usr/bin/env python3
"""Generate the week-by-week schedule page and one placeholder page per lecture day.

The course runs every Fall (Sep-Dec) and Winter (Jan-Apr). Everything here is expressed
as week numbers and weekdays, never calendar dates, so the site does not need a rewrite
each semester: Tuesdays are concept lectures (Dr. Ames), Thursdays are demos and hands-on
work (Dr. Halgren). Day numbers count class meetings from the first one.

Edit the DAYS and WEEKS tables below, then run:  python3 tools/build_schedule.py
It rewrites docs/schedule.md, docs/lectures/README.md, docs/lectures/day-NN.md and the
Lectures section of mkdocs.yml. Hand edits to the generated day pages are preserved below
the "<!-- notes -->" marker if you add one; everything above it is regenerated.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
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
         slides=[("The Global Positioning System, Part 1", f"{SITE}/slides/day-06/gps-part-1.html"),
                 ("The Global Positioning System, Part 2", f"{SITE}/slides/day-07/gps-part-2.html")],
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
    dict(n=28, week=15, kind="other", title="Final Exam",
         topics=["Remaining final project presentations",
                 "The final exam is given in class in the regular classroom; see Learning Suite for the exact time",
                 "Practical, hands-on exam in QGIS; AI tools are not permitted"]),
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
    15: dict(theme="Final Exam", due=["Final Exam (in class)", "Course evaluation (extra credit)"]),
}

LABS = {1: "Getting Started with GIS", 2: "Map Symbology and Layouts", 3: "GPS Data Collection and Importing Into QGIS",
        4: "Changing, Editing, and Fixing GIS Data", 5: "Working with Raster Data", 6: "Spatial Data Web Services",
        7: "Projections and Coordinate Systems", 8: "Metadata", 9: "The Yellowstone Disaster",
        10: "Domes for Mozambique", 11: "Walmart Site Selection"}

KIND_LABEL = {"concepts": "Tuesday · Concepts lecture (Dr. Ames)",
              "hands-on": "Thursday · Demo and hands-on (Dr. Halgren)",
              "other": "Class session"}


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


def day_page(d: dict) -> str:
    out = [f"# Day {d['n']}: {d['title']}", "",
           f"**Week {d['week']}** · {KIND_LABEL[d['kind']]}", ""]
    if d.get("note"):
        out += [f"> [!NOTE]", f"> {d['note']}", ""]
    out += ["## Topics", ""] + [f"- {t}" for t in d["topics"]] + [""]
    if d.get("handson"):
        out += ["## Hands-on guide", "",
                f"[Week {d['week']} Thursday run sheet](../hands-on/{d['handson']}.md): the plan Dr. Halgren follows, "
                "with the demo steps, the graded activity, and the common snags.", ""]
    if d.get("slides"):
        out += ["## Slides", ""] + [f"- [{t}]({u})" for t, u in d["slides"]] + [""]
    else:
        out += ["## Slides", "", "*Slides for this day are not on the site yet. They will be added as the semester goes.*", ""]
    if d.get("data") or d.get("links"):
        out += ["## Materials", ""]
        for t, u in d.get("data", []):
            out.append(f"- {t}: [download]({u})" if u else f"- {t} (posted on Learning Suite)")
        for t, u in d.get("links", []):
            out.append(f"- [{t}]({u})")
        out.append("")
    if d.get("activity"):
        out += ["## In-class activity", "", d["activity"] + ". Record your completion on Learning Suite.", ""]
    if d.get("reading"):
        out += ["## Reading", "", d["reading"], ""]
    due = WEEKS[d["week"]]["due"]
    if due:
        out += [f"## Due this week (Saturday, 11:59 pm unless noted)", ""] + [f"- {lab_link(x, '../')}" for x in due] + [""]
    return "\n".join(out)


def schedule_page() -> str:
    out = ["# Schedule", "",
           "CCE 114 is taught every **Fall** (September to December) and **Winter** (January to April).",
           "The sequence below is the same each semester; only the calendar dates change, so this page",
           "uses week numbers and weekdays. Exact due dates are on Learning Suite.", "",
           "Each week has two class meetings:", "",
           "- **Tuesday: concepts.** A lecture from the [slides](lectures/README.md) with discussion and short activities (Dr. Ames).",
           "- **Thursday: demo and hands-on.** Working in QGIS on the week's topic (Dr. Halgren).", "",
           "Reading quizzes open on Tuesday and close **Saturday at 11:59 pm**; lab reports are also due **Saturday at 11:59 pm**.", "",
           "| Week | Theme | Tuesday (concepts) | Thursday (hands-on) | Due this week |",
           "| --- | --- | --- | --- | --- |"]
    for w, info in WEEKS.items():
        days = [d for d in DAYS if d["week"] == w]
        tue = days[0] if days else None
        thu = days[1] if len(days) > 1 else None
        if w == 1:
            tue, thu = None, days[0]
        cell = lambda d: f"[Day {d['n']}: {d['title']}](lectures/day-{d['n']:02d}.md)" if d else "—"
        due = "<br>".join(lab_link(x, "") for x in info["due"]) or "—"
        out.append(f"| {w} | {info['theme']} | {cell(tue)} | {cell(thu)} | {due} |")
    out += ["", "Holidays and reading days shift between semesters; Week 13 and Week 15 absorb them.", ""]
    return "\n".join(out)


def lectures_index() -> str:
    out = ["# Lectures", "",
           "Lecture slides are interactive web presentations. Navigate with the arrow keys (or swipe);",
           "press <kbd>F</kbd> for fullscreen and <kbd>P</kbd> for presenter view with speaker notes.", "",
           "Each week, **Tuesday** is a concepts lecture from these slides (Dr. Ames) and **Thursday** is",
           "a demo and hands-on session in QGIS (Dr. Halgren). Days are numbered from the first class",
           "meeting of the semester; see the [schedule](../schedule.md) for the week-by-week view.", "",
           "**Week 1 meets only once, on Thursday** (Day 1: course introduction). The Tuesday/Thursday",
           "rhythm starts in Week 2.", ""]
    for w, info in WEEKS.items():
        out += [f"## Week {w}: {info['theme']}", ""]
        for d in DAYS:
            if d["week"] != w:
                continue
            tag = {"concepts": "Tue", "hands-on": "Thu", "other": ""}[d["kind"]]
            tag = f"{tag} · " if tag else ""
            line = f"- {tag}[Day {d['n']}: {d['title']}](day-{d['n']:02d}.md)"
            if d.get("slides"):
                line += " — slides: " + ", ".join(f"[{t}]({u})" for t, u in d["slides"])
            if d.get("handson"):
                line += f" — [hands-on guide](../hands-on/{d['handson']}.md)"
            out.append(line)
        out.append("")
    out += ["## Data", "",
            f"- [UtahCountyData.zip]({SITE}/lectures/data/UtahCountyData.zip) (38 MB): county boundary, major roads,",
            "  and cellular tower shapefiles plus a DEM, used in Week 2.", ""]
    return "\n".join(out)


def update_nav(mkdocs_yml: Path) -> None:
    text = mkdocs_yml.read_text()
    lines = ["  - Lectures:", "      - Overview: lectures/README.md"]
    for w, info in WEEKS.items():
        lines.append(f"      - \"Week {w} — {info['theme']}\":")
        for d in DAYS:
            if d["week"] == w:
                lines.append(f"          - \"Day {d['n']} — {d['title']}\": lectures/day-{d['n']:02d}.md")
    block = "\n".join(lines) + "\n"
    new = re.sub(r"  - Lectures:.*?(?=\n  - [A-Z]|\Z)", block.rstrip("\n"), text, flags=re.S)
    mkdocs_yml.write_text(new)


def main() -> None:
    (DOCS / "schedule.md").write_text(schedule_page())
    (DOCS / "lectures" / "README.md").write_text(lectures_index())
    for d in DAYS:
        path = DOCS / "lectures" / f"day-{d['n']:02d}.md"
        body = day_page(d)
        if path.exists() and "<!-- notes -->" in path.read_text():
            keep = path.read_text().split("<!-- notes -->", 1)[1]
            body = body + "\n<!-- notes -->" + keep
        path.write_text(body)
    update_nav(ROOT / "mkdocs.yml")
    print(f"wrote schedule.md, lectures/README.md, {len(DAYS)} day pages, and the mkdocs nav")


if __name__ == "__main__":
    main()
