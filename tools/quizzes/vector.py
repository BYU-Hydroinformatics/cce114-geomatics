"""Who Drew That Line? — Day 8 (Working with Vector Data).

Rendered by tools/build_quiz.py to docs/quizzes/vector/index.html. Everything here comes from
slides/day-08/working-with-vector-data.md, so it works as a self-check straight after that
lecture and as a warm-up before the Thursday digitizing session and Lab 4.
"""

SLUG = "vector"
TITLE = "Who Drew That Line?"
DAY = 8
WEEK = 5
TOPIC = "Working with Vector Data"
DESCRIPTION = ("CCE 114 in-class self-check: the three decisions a new vector layer needs, what "
               "digitizing really is, and the attribute and saving habits that keep a layer "
               "usable.")

BLURB = """Eight questions in three parts: the decisions you make <strong>before you draw
      anything</strong>, turning what you can see into <strong>coordinates</strong>, and the
      <strong>table and the save</strong> that decide whether the work survives."""

CLOSING = """\
        <strong style="color: var(--text);">For Thursday:</strong><br>
        One geometry type per layer &mdash; decide it before you click <strong>OK</strong><br>
        Turn <strong>snapping</strong> on before you draw, not after forty features<br>
        <strong>Save Layer Edits</strong> is a different command from saving the project<br>
        <em>Every dataset was drawn by somebody, at some scale, for some purpose.</em>"""

MESSAGES = [
    "Every one. Now go draw your own house and see if the theory holds.",
    "Solid. Read the explanations on the ones you missed — the saving question is the one that costs people an afternoon.",
    "Worth a second run. Most of the ways to lose an afternoon are on this quiz, and they are all avoidable.",
]

QUESTIONS = [
    dict(
        section="Part 1 — Before you draw anything",
        prompt="You are mapping campus utilities: fire hydrants, and the water mains that run between them. How many layers?",
        setup="",
        options=[
            "One layer, with a Type field that says “hydrant” or “main”",
            "Two layers — one of points, one of lines",
            "One layer, because hydrants and mains are the same utility system",
            "Three: hydrants, mains, and the junctions between them",
        ],
        correct=1,
        explanation="A layer holds one geometry type, and hydrants are points while mains are "
                    "lines. A single “utilities” layer is tempting because they belong to one "
                    "system, but picture the attribute table: half the columns would be empty for "
                    "every row, because pipe diameter means nothing to a hydrant.",
    ),
    dict(
        section="Part 1 — Before you draw anything",
        prompt="You create a layer in a different CRS from the project CRS. What do you see on screen?",
        setup="Our labs use EPSG:26912, NAD83 / UTM zone 12N.",
        options=[
            "The layer refuses to load until you fix the CRS",
            "The layer draws in the wrong part of the world, so the mistake is obvious",
            "Everything draws correctly, because QGIS reprojects on the fly — the surprise comes later, in areas and lengths",
            "The layer draws, but the attribute table is empty",
        ],
        correct=2,
        explanation="On-the-fly reprojection is a kindness that hides the mistake. Nothing looks "
                    "wrong; the trouble shows up when you measure something and the number is not "
                    "what you expected. Match the layer CRS to the project CRS, and make sure the "
                    "project CRS matches the map you are making.",
    ),
    dict(
        section="Part 1 — Before you draw anything",
        prompt="In the New GeoPackage Layer dialog you type a field name, choose Text, and click OK. What did you just create?",
        setup="",
        options=[
            "A layer with that field, ready to fill in",
            "A layer with that field, but with the wrong type",
            "A layer with no such field — the name was never added to the fields list",
            "Nothing; the dialog will not accept OK until the field is added",
        ],
        correct=2,
        explanation="The name and type sit in the New Field box until you click Add to Fields "
                    "List, and only what is in the list becomes a column. This is one of the most "
                    "common mistakes in Lab 4, and the dialog gives you no warning at all — you "
                    "find out when you go to type a value and there is nowhere to put it.",
    ),
    dict(
        section="Part 2 — Turning what you can see into coordinates",
        prompt="How many vertices does a road need?",
        setup="You are tracing a curving road from imagery.",
        options=[
            "As few as possible",
            "As many as possible",
            "Enough that the line matches the imagery at the scale you will use it",
            "One every 10 meters, evenly spaced",
        ],
        correct=2,
        explanation="More vertices is not more accurate; it is only more data, and it costs you "
                    "file size, drawing speed, and every analysis downstream. A straight road "
                    "needs two. A cul-de-sac needs many — or one true arc, if you digitize it "
                    "with the curve tool.",
    ),
    dict(
        section="Part 2 — Turning what you can see into coordinates",
        prompt="You load the SGID canal lines over high-resolution imagery and they sit well off the real channel. What is going on?",
        setup="",
        options=[
            "The canal lines are in the wrong coordinate system",
            "They were digitized years ago from much smaller-scale maps, and you are using them at a scale they were never made for",
            "The imagery is misregistered, so the canals are right and the photo is wrong",
            "The canals have physically moved since the data were collected",
        ],
        correct=1,
        explanation="Source scale limits the product. A line traced from a 1:100,000 map does not "
                    "become accurate by being loaded into a project drawn at 1:1,000. The data "
                    "are not wrong — they are being asked a question they were never built to "
                    "answer, which is exactly the fix Lab 4 asks you to make.",
    ),
    dict(
        section="Part 2 — Turning what you can see into coordinates",
        prompt="A culvert point sits 30 cm from the waterway line instead of on it. Is that a problem?",
        setup="",
        options=[
            "No — 30 cm is well inside the accuracy of the imagery",
            "No — anything that looks joined on screen will be treated as joined",
            "Yes — the point will not join to the line, so a hydrologic model routes the water over the road instead of under it",
            "Yes, but only if the two layers are in different coordinate systems",
        ],
        correct=2,
        explanation="Topology is about how features relate — connected, adjacent, contained — and "
                    "near is not connected. Water does not flow across a 30 cm gap in a model, "
                    "and the design storm comes out wrong. Turn snapping on before you draw; Lab "
                    "4 uses a 12-pixel tolerance, and pixels follow the zoom while map units do "
                    "not.",
    ),
    dict(
        section="Part 3 — The table, and the save",
        prompt="A student builds a Buildings layer with height stored as Text, “42 ft”. What is the cost?",
        setup="",
        options=[
            "None — the value is still there and a reader can see it",
            "Only that it takes more disk space than a number would",
            "You cannot sum, average, sort numerically, or graduate the symbology by it without parsing the text first",
            "QGIS will refuse to draw the layer until the field is fixed",
        ],
        correct=2,
        explanation="If you might ever want to add, average, or sort a value numerically, do not "
                    "store it as text — “42 ft” has to be taken apart before it can be used as a "
                    "number. The same goes for a year, which is better still as a Date when you "
                    "know the day. And an ID is a label, not a quantity, so integer is right for "
                    "it as long as nobody averages it.",
    ),
    dict(
        section="Part 3 — The table, and the save",
        prompt="You digitize for an hour, press Ctrl+S to save the project, and close QGIS. What is on disk?",
        setup="",
        options=[
            "Everything — saving the project saves the layers inside it",
            "The project file, which records where your layers are and how they are drawn; your features are saved only if you also saved the layer edits",
            "Nothing, because the project was never saved to a new file",
            "The features, but not the styling",
        ],
        correct=1,
        explanation="Editing puts changes in an edit buffer, and only Save Layer Edits writes that "
                    "buffer to the file. The .qgz stores pointers and symbology, not features. "
                    "Two separate habits: save layer edits often, and save the project often — "
                    "and remember a temporary scratch layer never had a file at all.",
    ),
]
