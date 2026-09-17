"""What Is a GIS? — Day 1 (Introduction to Geomatics and to GIS).

Rendered by tools/build_quiz.py to docs/quizzes/what-is-gis/index.html.
"""

SLUG = "what-is-gis"
TITLE = "What Is a GIS?"
DAY = 1
WEEK = 1
TOPIC = "Introduction to Geomatics and to GIS"
DESCRIPTION = "CCE 114 first-day self-check: what a GIS is and is not, the three vector feature types and the attribute table behind them, and how this course works."

BLURB = """Eight questions in three parts: what a GIS <strong>is</strong> and is not, the
      <strong>features</strong> and the table behind them, and how this <strong>course</strong>
      works."""

CLOSING = """\
        <strong style="color: var(--text);">Before Tuesday:</strong><br>
        Install <strong>QGIS</strong> &mdash; free, from qgis.org/download<br>
        Do the assigned reading in <em>GIS Fundamentals</em><br>
        Take the open-book quiz on Learning Suite<br>
        <em>Lab 1 assumes QGIS is already working on your own machine.</em>"""

MESSAGES = [
    "Every one, on the first day. Now go install QGIS.",
    "Solid. Read the explanations on the ones you missed — none of this is meant to be known in advance.",
    "This is day one, so nothing here was supposed to be obvious. Read the explanations and run it again.",
]

QUESTIONS = [
    dict(
        section="Part 1 — What a GIS is",
        prompt="What is a GIS?",
        setup="",
        options=[
            "A collection of maps",
            "A database",
            "Hardware, software, and data working together",
            "All of the above",
        ],
        correct=3,
        explanation="A GIS is all of these at once: computer hardware and software that integrate spatial features, attribute data, and the analysis tools that work on them. A map is one thing a GIS can produce, not the thing itself.",
    ),
    dict(
        section="Part 1 — What a GIS is",
        prompt="Which of these would you NOT use a GIS for?",
        setup="",
        options=[
            "Deciding where to put an airport",
            "Mapping flooding after a hurricane in North Carolina",
            "Designing a high-rise building",
            "Managing a city's water and sewer infrastructure",
        ],
        correct=2,
        explanation="Designing the building itself is CAD and BIM work, not GIS. A GIS still has plenty to say about the site around it — where to put it, what it floods, what it connects to — so the line is about the design work, not the project.",
    ),
    dict(
        section="Part 1 — What a GIS is",
        prompt="Which GIS software does this course use?",
        setup="",
        options=[
            "ArcGIS Pro",
            "QGIS",
            "Civil 3D",
            "AutoCAD",
        ],
        correct=1,
        explanation="QGIS: free, open source, and it runs on both Mac and Windows, so you install it on your own machine and keep it after you graduate. If you guessed ArcGIS Pro, that is the software CCE 414 uses; Civil 3D and AutoCAD are design tools, not GIS.",
    ),
    dict(
        section="Part 2 — Features and the table behind them",
        prompt="Utah city boundaries, the road network, and city centers. Which feature type is each?",
        setup="",
        options=[
            "Polygon, polyline, point",
            "Polyline, polygon, point",
            "Polygon, point, polyline",
            "They are all polygons at different scales",
        ],
        correct=0,
        explanation="A city boundary encloses an area, so it is a polygon. A road has length but no area, so it is a polyline. A city center is a single location, so it is a point. Those three are the vector feature types you will meet all semester.",
    ),
    dict(
        section="Part 2 — Features and the table behind them",
        prompt="How is an attribute table organized?",
        setup="",
        options=[
            "One row per layer, one column per feature",
            "One row per feature, one column per attribute",
            "One row per attribute, one column per feature",
            "One row per map, one column per layer",
        ],
        correct=1,
        explanation="Every feature on the map owns exactly one row. Select a row and the feature lights up on the map; click the feature and its row is the one highlighted. That link is what makes it a GIS rather than a drawing.",
    ),
    dict(
        section="Part 2 — Features and the table behind them",
        prompt="Is a river a polyline or a polygon?",
        setup="",
        options=[
            "Always a polyline — rivers flow in one direction",
            "Always a polygon — rivers have width",
            "It depends on the scale you are working at",
            "Neither; a river is a raster",
        ],
        correct=2,
        explanation="On a map of the state, a river is a line and its width is beneath the resolution of the map. On a map of one reach for a flood study, the banks matter and it is a polygon. The feature type follows the question you are asking, not the object.",
    ),
    dict(
        section="Part 3 — How this course works",
        prompt="What does your grade come from?",
        setup="",
        options=[
            "A midterm and a final exam",
            "Weekly readings with open-book quizzes, weekly hands-on labs, and in-class discussion, attendance, and participation",
            "Lab reports only",
            "A single semester project",
        ],
        correct=1,
        explanation="Three things, every week: read and take the open-book quiz, do the lab, and show up and take part. Attendance and participation are worth 25 points across the semester, and you mark your attendance each week.",
    ),
    dict(
        section="Part 3 — How this course works",
        prompt="Which of these follows the course's AI policy?",
        setup="You are encouraged to use AI tools — responsibly.",
        options=[
            "Have AI produce the maps and the analysis, then check them yourself",
            "Ask AI how to do something in QGIS or to explain a concept, do the GIS work yourself, and say so if AI helped with the writing",
            "Avoid AI entirely; it is not permitted in this course",
            "Use AI however you like — there is nothing to report",
        ],
        correct=1,
        explanation="Use AI to learn, not to produce. Build your own maps, run your own analysis, and solve the problems with your own brain — then report it whenever AI helped with your writing or with working a problem out. The full policy is on the course site.",
    ),
]
