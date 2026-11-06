"""What Goes Where? — Day 20 (Geoplanning: Site Layout and Design).

Rendered by tools/build_quiz.py to docs/quizzes/layout/index.html. Everything here comes from
slides/day-20/geoplanning.md, the Tuesday lecture behind Lab 10 (Domes for Mozambique). The
numbers in the buffer questions are deliberately not the Lab 10 numbers, so the lab still asks
students to apply the rule themselves.
"""

SLUG = "layout"
TITLE = "What Goes Where?"
DAY = 20
WEEK = 11
TOPIC = "Geoplanning: Site Layout and Design"
DESCRIPTION = ("CCE 114 in-class self-check: telling the program from the constraints, turning "
               "each constraint into a layer, and the buffer arithmetic behind footprints, roads, "
               "and setbacks.")

BLURB = """Eight questions in three parts: the <strong>program</strong> and the
      <strong>constraints</strong>, turning a plan into <strong>layers and tools</strong>, and the
      <strong>buffer arithmetic</strong> that trips people up in Lab 10."""

CLOSING = """\
        <strong style="color: var(--text);">Before you lay out a site:</strong><br>
        Map the <strong>constraints first</strong>, then fit the program into what is left<br>
        Work in a <strong>projected CRS in meters</strong> before any buffer<br>
        A buffer distance is a <strong>radius</strong>: half the diameter, half the width<br>
        <em>GIS lays out the concept. The engineering design comes after.</em>"""

MESSAGES = [
    "Every one. You are ready to lay out the Lab 10 site.",
    "Solid. Reread the explanations you missed, especially the buffer ones, before Lab 10.",
    "Worth a second run. The buffer questions are exactly what Lab 10 asks you to do.",
]

QUESTIONS = [
    dict(
        section="Part 1 — Program and constraints",
        prompt="In site design, what is the program?",
        setup="",
        options=[
            "The list of things the site has to hold: buildings, roads, open space, and their sizes",
            "The GIS software used to draw the plan",
            "The list of places on the site where nothing can be built",
            "The order in which the geoprocessing tools are run",
        ],
        correct=0,
        explanation="The program is what has to fit: in Lab 10, 80 homes, a church, a mosque, a "
                    "school, a market, and a recreation area. The places where nothing can go are "
                    "the constraints. A site plan is the program fitted inside the constraints.",
    ),
    dict(
        section="Part 1 — Program and constraints",
        prompt="Which of these is a constraint rather than part of the program?",
        setup="",
        options=[
            "A school 20 meters across",
            "A market of at least 4,000 m²",
            "A 25 m flood setback along a canal",
            "Eighty homes",
        ],
        correct=2,
        explanation="The setback says where things cannot go. The school, the market, and the homes "
                    "are things that must be placed. Constraints get mapped first, because the "
                    "program can only use the land they leave.",
    ),
    dict(
        section="Part 1 — Program and constraints",
        prompt="Why map the constraints before placing anything?",
        setup="",
        options=[
            "QGIS will not let you add points until a polygon layer exists",
            "The program only fits in the land the constraints leave behind, so you need to know where that is first",
            "Constraints are always smaller than the program, so they are faster to draw",
            "So the legend lists them first",
        ],
        correct=1,
        explanation="Placing homes and then discovering half of them sit in the flood band means "
                    "starting over. Site minus constraints is the buildable area, and the buildable "
                    "area is where the design happens.",
    ),
    dict(
        section="Part 2 — From plan to layers",
        prompt="You want to show the land left for building after removing the flood setbacks and the protected tree buffers. Which operation does that?",
        setup="You have the site boundary as one polygon layer and the merged setbacks as another.",
        options=[
            "Intersection of the site and the setbacks",
            "Union of the site and the setbacks",
            "Difference: the site minus the setbacks",
            "Clip the setbacks to the site",
        ],
        correct=2,
        explanation="Difference keeps the part of the site outside the setbacks, which is exactly "
                    "the buildable area. Intersection and Clip would return the setbacks inside the "
                    "site: the land you cannot use, which is the opposite of what you want.",
    ),
    dict(
        section="Part 2 — From plan to layers",
        prompt="Before running a buffer in meters on the Mozambique site, what has to be true?",
        setup="",
        options=[
            "The layer has an attribute field for the distance",
            "The layers are in a projected CRS whose units are meters, such as a UTM zone",
            "The basemap is turned off",
            "The layer is saved as a shapefile",
        ],
        correct=1,
        explanation="A buffer distance is measured in the layer's units. In WGS 84 those are "
                    "degrees, and a \"25\" buffer would reach thousands of kilometers. That is why Lab 10 "
                    "starts by setting a UTM CRS for Mozambique: the Week 8 lesson put to work.",
    ),
    dict(
        section="Part 3 — Buffer arithmetic",
        prompt="A water tank is 10 m across. You placed its center as a point. What buffer distance draws its footprint?",
        setup="",
        options=["10 m", "5 m", "20 m", "2.5 m"],
        correct=1,
        explanation="A buffer extends the same distance in every direction from the point, so the "
                    "distance is the radius. Ten meters across means 5 m. Buffering by 10 m draws a "
                    "tank 20 m across, four times the area you meant.",
    ),
    dict(
        section="Part 3 — Buffer arithmetic",
        prompt="A lane is 8 m wide and you digitized its centerline. What buffer distance draws the lane?",
        setup="",
        options=["8 m", "16 m", "4 m", "2 m"],
        correct=2,
        explanation="The buffer goes out on both sides of the line, so half the width on each side: "
                    "4 m. The same rule as the tank: a buffer distance is always measured from the "
                    "feature outward.",
    ),
    dict(
        section="Part 3 — Buffer arithmetic",
        prompt="What does the GIS layout give you, and what still comes after it?",
        setup="",
        options=[
            "It is the final construction drawing; nothing comes after",
            "A concept plan that fits the program inside the constraints; grading, drainage, and detailed engineering design come after, usually in CAD",
            "Only a pretty map; the real layout is done by hand",
            "The cost estimate; the layout comes after",
        ],
        correct=1,
        explanation="GIS is where you test whether the program fits and where it should go. The "
                    "engineering design that gets built, with grades, pipe sizes, and dimensions, "
                    "is drawn next in CAD and civil design software, starting from that layout.",
    ),
]
