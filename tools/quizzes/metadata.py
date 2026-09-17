"""Would You Drink It? — Day 16 (Metadata).

Rendered by tools/build_quiz.py to docs/quizzes/metadata/index.html. Everything here comes
from slides/day-16/metadata.md; the Thursday session and Lab 8 do the hands-on version of
the same material, so this works as preparation for either.
"""

SLUG = "metadata"
TITLE = "Would You Drink It?"
DAY = 16
WEEK = 9
TOPIC = "Metadata"
DESCRIPTION = ("CCE 114 in-class self-check: why an undocumented dataset is a risk, what a "
               "metadata record has to tell you, where the answers live in a download, and how "
               "to judge whether data are fit for your use.")

BLURB = """Eight questions in two parts: why an undocumented dataset is a
      <strong>risk</strong>, and how to read a record well enough to decide whether the data are
      <strong>fit for your use</strong>."""

CLOSING = """\
        <strong style="color: var(--text);">Before you build anything on a download:</strong><br>
        Six questions &mdash; <strong>what, where, when, why, how, who</strong><br>
        The coordinate system is in the <strong>.prj</strong>, not the <strong>.xml</strong><br>
        Unzip the whole thing &mdash; opening only the <strong>.shp</strong> throws the metadata away<br>
        <em>Almost nothing goes wrong because the data were wrong. It goes wrong because they
        were right data, wrong job.</em>"""

MESSAGES = [
    "Every one. Now go read a real record on gis.utah.gov and find what it does not tell you.",
    "Solid. Reread the explanations you missed — the fitness-for-use ones are what Lab 8 grades.",
    "Worth a second run. Metadata is the cheapest hour in this course and the most expensive one to skip.",
]

QUESTIONS = [
    dict(
        section="Part 1 — What is missing, and what it costs",
        prompt="A colleague sends you roads_final_v3 — just the .shp, .shx and .dbf. It opens in QGIS and the lines look like roads. Why is that not enough to design against?",
        setup="",
        options=[
            "It is enough — the geometry is what matters, and it draws correctly",
            "Nothing in the folder says when the roads were collected, at what scale, from what source, or what the columns mean — and with no .prj, not even the coordinate system",
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
            "The metadata record was written in the wrong standard",
        ],
        correct=1,
        explanation="The numbers were not wrong, they were undocumented. Units, datums and "
                    "coordinate systems are exactly the kind of thing that is obvious to the "
                    "person who made the file and invisible to everyone else. Your freeway "
                    "alignment has the same failure mode, for a lot less money.",
    ),
    dict(
        section="Part 1 — What is missing, and what it costs",
        prompt="On a bottle, the ingredients list tells you what is actually inside. What is the equivalent on a dataset?",
        setup="",
        options=[
            "The definition of every attribute column, including what its codes mean",
            "The number of features in the layer",
            "The file size and format",
            "The bounding coordinates",
        ],
        correct=0,
        explanation="In an FGDC record this is the Entity and Attribute section, and it is the one "
                    "nobody fills in and everybody needs. \"What do the columns mean?\" is the "
                    "single most common gap in real-world metadata — a column called TYPE holding "
                    "codes with no key is a column you cannot use.",
    ),
    dict(
        section="Part 1 — What is missing, and what it costs",
        prompt="You can answer what, where, when and who for a layer, but nothing tells you how it was made. What have you lost?",
        setup="",
        options=[
            "The lineage — the collection method and the processing steps that came after, which is what lets you decide whether to trust the numbers",
            "The license and use constraints",
            "The extent of the data",
            "The revision schedule",
        ],
        correct=0,
        explanation="\"How\" is the lineage, and it lives in the Data Quality section of an FGDC "
                    "record. Without it you cannot tell whether a line came from a survey, a "
                    "scanned paper map, or somebody tracing imagery at the wrong zoom — and those "
                    "three deserve very different amounts of trust.",
    ),
    dict(
        section="Part 2 — Reading a record, and deciding",
        prompt="You unzip the Utah County Boundaries download, open the .xml in a browser and read the whole thing. You still do not know the coordinate system. Where should you look?",
        setup="The folder holds the usual shapefile pieces plus the metadata file.",
        options=[
            "The .dbf, which stores the projection alongside the attributes",
            "The .prj file sitting in the same folder",
            "The .shx index file",
            "Nowhere — you have to email the agency for it",
        ],
        correct=1,
        explanation="This one catches almost everyone: the coordinate system lives in its own "
                    "sidecar file, separate from the rest of the metadata, and it is the file QGIS "
                    "actually reads when it assigns the layer a CRS. While you are in the .xml, "
                    "Ctrl+F for \"metd\" gives you the metadata date and \"bounding\" gives you "
                    "the extent.",
    ),
    dict(
        section="Part 2 — Reading a record, and deciding",
        prompt="You spend the morning reading an FGDC record from a Utah download, then open Layer Properties > Metadata in QGIS to document a layer of your own. Was the morning wasted?",
        setup="",
        options=[
            "Yes — FGDC and ISO 19115 are unrelated standards that ask different questions",
            "No — both ask the same six questions with different tag names, and QGIS follows the ISO 19115 model, which is why its panel has identification, extent, access, fields and history",
            "Yes — QGIS imports an FGDC .xml directly, so there was no reason to read it by hand",
            "No, but only because ISO 19115 has replaced FGDC, so Utah downloads are ISO now",
        ],
        correct=1,
        explanation="FGDC CSDGM is the U.S. federal standard, and most Utah and federal downloads "
                    "you open this semester still carry one. QGIS chose ISO, which is a large part "
                    "of why an FGDC .xml does not simply import — so you read one standard and "
                    "write the other, and the six questions carry across unchanged.",
    ),
    dict(
        section="Part 2 — Reading a record, and deciding",
        prompt="A statewide roads layer documents its source scale as 1:100,000. You zoom to a street corner in QGIS and the centerline still draws as a crisp, sharp line. Can you place a curb from it?",
        setup="",
        options=[
            "Yes — vector data have no resolution limit, so you can zoom as far as you like",
            "No — the source scale limits what the data can represent, and zooming in cannot add detail that was never captured",
            "Yes, once you reproject the layer to UTM meters",
            "Only after converting it to a raster with a finer cell size",
        ],
        correct=1,
        explanation="The tempting part is true: the line really does stay sharp at any zoom, "
                    "because it is drawn from coordinates rather than pixels. Nothing on screen "
                    "warns you it was digitized for a statewide overview. Scale and resolution sit "
                    "at the top of the fitness-for-use checklist for exactly this reason — the "
                    "display will never tell you.",
    ),
    dict(
        section="Part 2 — Reading a record, and deciding",
        prompt="You are laying out a new road west of Lehi and need building footprints. Dataset A: collected 2013, 1:24,000, no lineage, no contact. Dataset B: collected 2024 from 6-inch imagery, lineage documented, county GIS contact listed. Which do you use?",
        setup="",
        options=[
            "A",
            "B",
            "Either — both are building footprints",
            "Neither, until you check something else",
        ],
        correct=3,
        explanation="B is plainly the better record, which is exactly why it is the tempting "
                    "answer. But nothing above tells you either dataset's coordinate system or its "
                    "use constraints, and a 2024 footprint layer digitized for planning is still "
                    "not a survey. The habit to build is asking what the metadata did not tell you.",
    ),
]
