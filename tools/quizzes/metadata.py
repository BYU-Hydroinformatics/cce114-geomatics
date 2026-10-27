"""Would You Drink It? — Day 16 (Metadata, Tuesday).

Rendered by tools/build_quiz.py to docs/quizzes/metadata/index.html. Everything here comes
from slides/day-16/metadata.md: why undocumented data is a risk, the six questions, and
right data, wrong job. The standards, where metadata lives in a download, and the
fitness-for-use checklist moved to Thursday's deck on 2026-10-26 and have their own quiz,
tools/quizzes/fitness.py.
"""

SLUG = "metadata"
TITLE = "Would You Drink It?"
DAY = 16
WEEK = 9
TOPIC = "Metadata"
DESCRIPTION = ("CCE 114 in-class self-check: why an undocumented dataset is a risk, the six "
               "questions every metadata record answers, and why good data can still be the "
               "wrong data for your job.")

BLURB = """Nine questions in two parts: why an undocumented dataset is a
      <strong>risk</strong>, the <strong>six questions</strong> every record has to answer
      before you trust the data, and <strong>right data, wrong job</strong>."""

CLOSING = """\
        <strong style="color: var(--text);">Before you build anything on a download:</strong><br>
        Six questions &mdash; <strong>what, where, when, why, how, who</strong><br>
        Undocumented is not the same as wrong &mdash; but you cannot tell the difference<br>
        <em>Almost nothing goes wrong because the data were wrong. It goes wrong because they
        were right data, wrong job.</em>"""

MESSAGES = [
    "Every one. Thursday you write a record yourself in QGIS.",
    "Solid. Reread the explanations you missed — the six questions are what Lab 8 grades.",
    "Worth a second run. Metadata is the cheapest hour in this course and the most expensive one to skip.",
]

QUESTIONS = [
    dict(
        section="Part 1 — What is missing, and what it costs",
        prompt="You can get vector data three ways: collect it in the field with differential GPS, digitize it yourself, or download someone else's. Which one leaves you most in need of metadata?",
        setup="",
        options=[
            "Differential GPS, because the corrections have to be recorded",
            "Digitizing, because hand-drawn lines are the least accurate",
            "Downloading, because it is a stranger's work and you were not there when it was made",
            "All three equally",
        ],
        correct=2,
        explanation="The three run from most to least personally connected to the data. When you "
                    "survey or digitize, you carry the knowledge of how the data were "
                    "made in your head. The moment you download somebody else's file, that "
                    "knowledge has to travel with the file, and metadata is how it travels. That "
                    "is the \"what is it?\" question from the start of class.",
    ),
    dict(
        section="Part 1 — What is missing, and what it costs",
        prompt="A colleague sends you roads_final_v3 — just the .shp, .shx and .dbf. It opens in QGIS and the lines look like roads. Why is that not enough to design against?",
        setup="",
        options=[
            "It is enough — the geometry is what matters, and it draws correctly",
            "Nothing in the folder says when the roads were collected, at what scale, from what source, or what the columns mean",
            "Shapefiles are not an acceptable format for engineering work",
            "QGIS cannot measure distances on a layer that has no metadata",
        ],
        correct=1,
        explanation="This is the unlabeled brown bottle from class. The liquid may be perfectly "
                    "good; you have no way to decide, and \"it looks right on screen\" is not a "
                    "check. A file that draws correctly and a file you can defend in a report are "
                    "two different things.",
    ),
    dict(
        section="Part 1 — What is missing, and what it costs",
        prompt="NASA lost the $125 million Mars Climate Orbiter in 1999. What actually went wrong?",
        setup="",
        options=[
            "The ground software computed the thruster numbers incorrectly",
            "The numbers were correct, but nobody wrote down the units — the ground software delivered English units and the onboard software expected metric",
            "The two teams used different coordinate systems for the spacecraft's position",
            "A sensor failed and sent no data at all",
        ],
        correct=1,
        explanation="The numbers were not wrong, they were undocumented. Units, datums and "
                    "coordinate systems are exactly the kind of thing that is obvious to the "
                    "person who made the file and invisible to everyone else. Your freeway "
                    "alignment has the same failure mode, for a lot less money.",
    ),
    dict(
        section="Part 1 — What is missing, and what it costs",
        prompt="The usual reasons for skipping metadata are \"no time,\" \"the project is over,\" and \"I know what it means.\" Who pays for that choice?",
        setup="",
        options=[
            "Nobody — if the creator understands the data, the data are fine",
            "The agency that hosts the file",
            "The next engineer to use the data, who is often you six months later",
            "Only people who use different software",
        ],
        correct=2,
        explanation="This is the panda's problem in the video: a file nobody can interpret. "
                    "\"I know what it means\" is true on the day you make the file and stops being "
                    "true surprisingly fast, even for you.",
    ),
    dict(
        section="Part 2 — The six questions, and the wrong job",
        prompt="On a bottle, the ingredients list tells you what is actually inside. What is the equivalent on a dataset?",
        setup="",
        options=[
            "The definition of every attribute column, including what its codes mean",
            "The number of features in the layer",
            "The file size and format",
            "The area the data cover",
        ],
        correct=0,
        explanation="\"What do the attribute columns mean?\" is part of the What question, and it "
                    "is the single most common gap in real-world metadata. A column called TYPE "
                    "holding codes with no key is a column you cannot use.",
    ),
    dict(
        section="Part 2 — The six questions, and the wrong job",
        prompt="You can answer what, where, when and who for a layer, but nothing tells you how it was made. What have you lost?",
        setup="",
        options=[
            "The lineage — the collection method and the processing steps that came after, which is what lets you decide whether to trust the numbers",
            "The license and use constraints",
            "The area the data cover",
            "The revision schedule",
        ],
        correct=0,
        explanation="\"How\" is the lineage. Without it you cannot tell whether a line came from "
                    "a survey, a scanned paper map, or somebody tracing imagery at the wrong zoom — "
                    "and those three deserve very different amounts of trust.",
    ),
    dict(
        section="Part 2 — The six questions, and the wrong job",
        prompt="Which of the six questions do professionals usually read first, because it tells them whether data made for a statewide overview map can be trusted for a site-scale design?",
        setup="",
        options=[
            "Who",
            "When",
            "Why — the purpose the data were created for",
            "Where",
        ],
        correct=2,
        explanation="\"Why\" is the field students skip and professionals read first. Data "
                    "collected for one purpose are not automatically valid for another, and the "
                    "purpose statement is where you find out what the data were built to do.",
    ),
    dict(
        section="Part 2 — The six questions, and the wrong job",
        prompt="A statewide roads layer was made at 1:100,000. You zoom to a street corner in QGIS and the centerline still draws as a crisp, sharp line. Can you place a curb from it?",
        setup="",
        options=[
            "Yes — vector data have no resolution limit, so you can zoom as far as you like",
            "No — the scale it was made at limits what it can represent, and zooming in cannot add detail that was never captured",
            "Yes, once you reproject the layer to UTM meters",
            "Only after converting it to a raster with a finer cell size",
        ],
        correct=1,
        explanation="The tempting part is true: the line really does stay sharp at any zoom, "
                    "because it is drawn from coordinates rather than pixels. Nothing on screen "
                    "warns you it was made for a statewide overview. The data are not wrong; it is "
                    "right data, wrong job, and only the metadata tells you so.",
    ),
    dict(
        section="Part 2 — The six questions, and the wrong job",
        prompt="A land-cover raster's metadata says the imagery behind it was collected in 2011. You want to map the subdivision that was built last year. Which of the six questions just saved you, and what did it tell you?",
        setup="",
        options=[
            "Where — the raster does not cover the subdivision",
            "When — the data predate the subdivision, so it cannot be in them",
            "Who — the agency that made it does not map subdivisions",
            "How — satellites cannot see houses",
        ],
        correct=1,
        explanation="\"When\" covers when the data were collected and last updated. Nothing is "
                    "wrong with a 2011 land-cover raster; it simply cannot show anything built "
                    "after 2011. Right data, wrong job, and the date in the record is how you "
                    "find out before you design against it.",
    ),
]
