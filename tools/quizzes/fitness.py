"""Fit for Your Use? — Day 17 (Metadata, Thursday).

Rendered by tools/build_quiz.py to docs/quizzes/fitness/index.html. Everything here comes
from slides/day-17/metadata-standards.md: the metadata standards, where metadata lives in a
download, and reading a record against the fitness-for-use checklist. Written 2026-10-26,
when the second half of the Day 16 deck moved to Thursday; three of its questions came over
from tools/quizzes/metadata.py with it.
"""

SLUG = "fitness"
TITLE = "Fit for Your Use?"
DAY = 17
WEEK = 9
TOPIC = "Metadata Standards"
DESCRIPTION = ("CCE 114 in-class self-check: the FGDC and ISO 19115 metadata standards, where "
               "the metadata lives in a download, and reading a record to decide whether the "
               "data are fit for your use.")

BLURB = """Eight questions in two parts: the <strong>standards</strong> and where the record
      actually <strong>lives</strong>, and reading a record well enough to decide whether the
      data are <strong>fit for your use</strong>."""

CLOSING = """\
        <strong style="color: var(--text);">Before you build anything on a download:</strong><br>
        Unzip the whole thing &mdash; opening only the <strong>.shp</strong> throws the metadata away<br>
        The coordinate system is in the <strong>.prj</strong>, not the <strong>.xml</strong><br>
        In QGIS, <strong>Save metadata to file</strong>, or it lives only in the project<br>
        <em>Anything the metadata does not tell you is a risk you are carrying into your design.</em>"""

MESSAGES = [
    "Every one. Lab 8 is the same work on real Utah layers, so it should go quickly.",
    "Solid. Reread the explanations you missed — the fitness-for-use ones are what Lab 8 grades.",
    "Worth a second run. The checklist is short, and it is the habit this week is trying to build.",
]

QUESTIONS = [
    dict(
        section="Part 1 — The standards, and where the record lives",
        prompt="Why have a metadata standard at all, instead of letting every agency write whatever fields it likes?",
        setup="",
        options=[
            "So the files are smaller",
            "So the field names and expected content are fixed, which makes records searchable and portable between agencies and software",
            "So only certified professionals can write metadata",
            "So the metadata can be stored inside the shapefile",
        ],
        correct=1,
        explanation="A card catalog is only useful because every card has the same fields in the "
                    "same places. A standard says what has to be there; a style or profile says "
                    "how one organization fills it in.",
    ),
    dict(
        section="Part 1 — The standards, and where the record lives",
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
        section="Part 1 — The standards, and where the record lives",
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
        section="Part 1 — The standards, and where the record lives",
        prompt="You fill in every page of Layer Properties > Metadata in QGIS, click OK, and email a colleague the shapefile. What metadata do they get?",
        setup="",
        options=[
            "Everything you wrote — QGIS stores it in the .dbf",
            "None of it — unless you saved it to a .qmd file beside the layer, it lives only in your project file",
            "Everything, because QGIS writes an FGDC .xml automatically",
            "Only the title and abstract",
        ],
        correct=1,
        explanation="A QGIS layer's metadata lives in a .qmd sidecar file or inside the project "
                    "file. Clicking OK saves it to the project, which your colleague does not have. "
                    "Use Save metadata to file, or for a GeoPackage, save it into the .gpkg so it "
                    "travels inside the file.",
    ),
    dict(
        section="Part 2 — Reading a record, and deciding",
        prompt="A dataset's page says it was updated in 2024, but the Metadata Reference section of its FGDC record says the metadata was written in 1998. What should you conclude?",
        setup="",
        options=[
            "Nothing — the metadata date does not matter",
            "It is a warning sign: the record may describe an older version of the data, so check before you trust it",
            "The dataset must actually be from 1998",
            "The FGDC record is invalid and should be deleted",
        ],
        correct=1,
        explanation="Section 7, Metadata Reference, records who wrote the metadata and when. It "
                    "matters more than it looks: a record much older than the data it describes "
                    "may not describe the data you downloaded.",
    ),
    dict(
        section="Part 2 — Reading a record, and deciding",
        prompt="A dataset passes every item on the checklist for your project: scale, date, coordinate system, completeness, lineage and attributes. Which item is left that could still stop you from using it?",
        setup="",
        options=[
            "File format",
            "Constraints — the license, any use restrictions, and any required credit",
            "The number of features",
            "Whether it opens in QGIS",
        ],
        correct=1,
        explanation="Constraints are item seven on the checklist, and they are easy to skip "
                    "because nothing about the data itself is wrong. Read the license before you "
                    "build a deliverable on someone else's work.",
    ),
    dict(
        section="Part 2 — Reading a record, and deciding",
        prompt="You find a dataset on data.gov that looks right, but its page gives no lineage and no contact. What is the right move?",
        setup="",
        options=[
            "Use it — federal data is always reliable",
            "Treat each unanswered question as a risk: find a better-documented source, or confirm the missing pieces before you design against it",
            "Assume the lineage is the same as a similar UGRC layer",
            "Ignore it, because data.gov data cannot be used in engineering",
        ],
        correct=1,
        explanation="data.gov holds a huge range of datasets with wildly varying metadata quality, "
                    "which makes it good practice at deciding what you cannot trust. Anything you "
                    "cannot answer from the metadata is a risk you are carrying into your design.",
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
