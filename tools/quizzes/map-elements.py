"""Does This Map Work? — Day 4 (Maps, Symbology, and Cartography).

Rendered by tools/build_quiz.py to docs/quizzes/map-elements/index.html.
"""

SLUG = "map-elements"
TITLE = "Does This Map Work?"
DAY = 4
WEEK = 3
TOPIC = "Maps, Symbology, and Cartography"
DESCRIPTION = "CCE 114 in-class self-check: the required map elements, what makes a map ugly, and what a map does to the reader who looks at it."

BLURB = """Twelve questions in three parts: the <strong>elements</strong> every map you turn in must carry,
      what makes a map <strong>ugly</strong>, and what a map <strong>does to the reader</strong> looking at it."""

CLOSING = """\
        <strong style="color: var(--text);">The checklist, one more time:</strong><br>
        Title &middot; Legend &middot; Scale bar &middot; North arrow<br>
        Neat line &middot; Metadata &middot; Legible text &middot; Distinct colors<br>
        <em>If a reader has to ask you a question to use the map, the map is not finished.</em>"""

MESSAGES = [
    "Every one. Bring that eye to Lab 2.",
    "Solid. Reread the explanations on the ones you missed — they are the ones that cost points on a layout.",
    "Worth a second run. The checklist below is what Lab 2 and every lab after it is graded against.",
]

QUESTIONS = [
    dict(
        section="Part 1 — What goes in every map",
        prompt="Which of these is NOT required on a technical map you turn in for this course?",
        setup="",
        options=[
            "Title",
            "North arrow",
            "Metadata",
            "Legend",
            "None of the above",
        ],
        correct=4,
        explanation="All four belong on a technical map, so the answer is “none of the above.” The course does not grade aesthetics, but it does grade whether the map is readable and complete.",
    ),
    dict(
        section="Part 1 — What goes in every map",
        prompt="What belongs in the metadata block on a map layout?",
        setup="",
        options=[
            "The full attribute table of every layer on the map",
            "Who made it, when, from what data, and in what coordinate system",
            "The file path to your QGIS project",
            "A paragraph describing your analysis and conclusions",
        ],
        correct=1,
        explanation="On a layout, “metadata” means a short credit block: author, date, data source, and projection. It is what lets a reader judge whether to trust the map, and reproduce it if they want to.",
    ),
    dict(
        section="Part 1 — What goes in every map",
        prompt="What is a neat line?",
        setup="",
        options=[
            "The border that frames the map",
            "The outline of the study-area polygon",
            "The divider between the map and the legend",
            "The line style used for roads and streams",
        ],
        correct=0,
        explanation="A neat line is the frame around the map. It tells the reader where the map stops and the page begins — which matters most when the data run right to the edge.",
    ),
    dict(
        section="Part 1 — What goes in every map",
        prompt="Which is the best title for a map figure in an engineering report?",
        setup="",
        options=[
            "Figure 3",
            "Utah County",
            "Flood Hazard Zones, Utah County, Utah (FEMA NFHL, 2024)",
            "Final Map — Lab 2",
        ],
        correct=2,
        explanation="A title answers “what is this a map of?” — subject, place, and when. “Utah County” names the place but not the subject; “Figure 3” and “Final Map” name neither.",
    ),
    dict(
        section="Part 1 — What goes in every map",
        prompt="In QGIS, where do you assemble the title, legend, scale bar, and north arrow?",
        setup="You have your layers styled the way you want them in the map canvas.",
        options=[
            "Layer Properties › Symbology",
            "The Print Layout",
            "The attribute table",
            "Project › Properties",
        ],
        correct=1,
        explanation="Symbology decides how the data look; the Print Layout is where the map becomes a figure. Layout elements — map frame, title, legend, scale bar, north arrow, and a spatial reference block — are all added there.",
    ),
    dict(
        section="Part 1 — What goes in every map",
        prompt="A U.S. map with Alaska and Hawaii in inset boxes carries three scale bars. Why three?",
        setup="This is the soft-drink map from class — “pop,” “coke,” or “soda” by county.",
        options=[
            "One in miles, one in kilometers, one in degrees",
            "For visual balance across the bottom of the layout",
            "The insets are drawn at different scales than the lower 48, so a single scale bar would be wrong for two of the three frames",
            "The projection changes across the map, so distance cannot be shown with one bar",
        ],
        correct=2,
        explanation="Each inset is its own map frame at its own scale. One scale bar can only describe one frame, so an honest layout gives each frame its own.",
    ),
    dict(
        section="Part 2 — Ugly maps",
        prompt="The West Virginia hot-dog-slaw map has a title and a legend. What is it missing?",
        setup="Counties shaded by whether a hot dog with “everything” comes with coleslaw.",
        options=[
            "A scale bar, a north arrow, and a metadata block",
            "Nothing — a title and a legend are enough for a thematic map",
            "A legible title and distinct colors",
            "A neat line and a graticule",
        ],
        correct=0,
        explanation="It does the hard part — a clear subject and a legend that explains the shading — and then skips the scale bar, the north arrow, and any statement of who made it, from what, and when. That last omission is the one that would sink it in a report.",
    ),
    dict(
        section="Part 2 — Ugly maps",
        prompt="You inherit a map with twelve layers switched on, a full-color street basemap under everything, labels colliding, and no obvious subject. What do you fix first?",
        setup="",
        options=[
            "Increase the label font size",
            "Switch to a different color ramp",
            "Add the missing north arrow",
            "Decide what the map is for, then turn off everything that does not serve it",
        ],
        correct=3,
        explanation="Clutter is not a styling problem, it is a scoping problem. Ask what the map is for and who is reading it; the color, type, and layout decisions only have right answers once that is settled.",
    ),
    dict(
        section="Part 2 — Ugly maps",
        prompt="A student symbolizes each city with a detailed photo icon. At county scale the icons collide and every label has to be pushed away on a leader line. What went wrong?",
        setup="This is a real student map from a previous semester.",
        options=[
            "The layer is in the wrong coordinate system",
            "The marker carries more detail than the map scale can show — symbol size and complexity have to suit the scale",
            "Cities should always be symbolized as polygons",
            "Labels should have been turned off",
        ],
        correct=1,
        explanation="A symbol has to be readable at the scale it is printed. A simple marker sized by population says more at county scale than a photograph does, and it leaves room for the labels.",
    ),
    dict(
        section="Part 3 — What the map does to the reader",
        prompt="A county map of the 2012 presidential vote looks overwhelmingly red. What does that actually tell you?",
        setup="",
        options=[
            "Most voters voted Republican",
            "Most counties voted Republican — and counties are not people",
            "The map is mislabeled",
            "Turnout was higher in Republican counties",
        ],
        correct=1,
        explanation="The eye adds up area, but people vote. The smaller red‑shaded counties on the companion map hold more people than all the gray ones combined. Any choropleth of a person-based quantity has this problem; cartograms, dot-density maps, and normalizing by population are the usual fixes.",
    ),
    dict(
        section="Part 3 — What the map does to the reader",
        prompt="A map of January minimum temperatures, 1981–2010 compared with 1971–2000, shows Minnesota in deep red. What is the red showing?",
        setup="",
        options=[
            "Minnesota is hot in January",
            "Minnesota is the warmest part of the map",
            "The change in January minimums — Minnesota is going from extremely cold to slightly less extremely cold",
            "Missing data for that part of the country",
        ],
        correct=2,
        explanation="The quantity is a difference, not a temperature, and a red-means-hot ramp on a difference map makes the argument before the reader gets to the legend. The ramp is a claim; choose it as deliberately as you choose the data.",
    ),
    dict(
        section="Part 3 — What the map does to the reader",
        prompt="“Camp 3” on a USGS quad map is really Camp David. Elsewhere, a block of imagery over part of Girona, Spain, is blacked out entirely. What is the difference?",
        setup="Two ways a map can keep a secret.",
        options=[
            "Both are omission",
            "Both are obfuscation",
            "The first is obfuscation — drawn, but labeled so you cannot tell what it is; the second is omission — removed outright",
            "The first is a scale problem; the second is a resolution problem",
        ],
        correct=2,
        explanation="Obfuscation leaves the feature on the map and hides what it is. Omission takes it off. Both are editorial decisions, and both are worth asking about on any map you did not make yourself — what did the mapmaker decide to leave out?",
    ),
]
