"""Which Tool Answers the Question? — Day 18 (Introduction to Geoprocessing).

Rendered by tools/build_quiz.py to docs/quizzes/geoprocessing/index.html. Everything here
comes from slides/day-18/introduction-to-geoprocessing.md and its speaker notes; the tool
names are the QGIS ones, which is what the Processing Toolbox will show on Thursday.
"""

SLUG = "geoprocessing"
TITLE = "Which Tool Answers the Question?"
DAY = 18
WEEK = 10
TOPIC = "Introduction to Geoprocessing"
DESCRIPTION = ("CCE 114 in-class self-check: turning a question into an operation on geometry, "
               "what each geoprocessing tool puts out, and the order to run them in.")

BLURB = """Eight questions in three parts: turning a <strong>question</strong> into an operation
      on geometry, what each <strong>tool</strong> actually puts out, and how the tools
      <strong>chain</strong> into a workflow."""

CLOSING = """\
        <strong style="color: var(--text);">For Thursday and Lab 9:</strong><br>
        Check the <strong>CRS</strong> before you buffer &mdash; meters, not degrees<br>
        <strong>Clip</strong> for the outline; <strong>Intersection</strong> when you need both tables<br>
        AND &middot; OR &middot; NOT &rarr; Intersection &middot; Union &middot; Difference<br>
        <em>Save every intermediate layer to a file. A temporary scratch layer is gone when you close QGIS.</em>"""

MESSAGES = [
    "Every one. Now go build the chain in QGIS.",
    "Solid. Reread the explanations on the ones you missed — clip against intersect is the one that costs points in Lab 9.",
    "Worth a second run. Choosing the tool is the whole skill; running it is three clicks.",
]

QUESTIONS = [
    dict(
        section="Part 1 — From a question to a selection",
        prompt="You download a road layer and go straight to buffering it by 5 km. Which step of the geographic approach did you skip, and what does it usually cost you?",
        setup="Ask · Acquire · Examine · Analyze · Act.",
        options=[
            "Ask — you never framed the question in terms of location",
            "Acquire — there was a better dataset on the portal",
            "Examine — you never looked at the coordinate system, and a layer in degrees cannot be buffered by kilometers",
            "Act — you skipped the map layout at the end",
        ],
        correct=2,
        explanation="Examine is the step everybody wants to skip, and it is the one that wastes "
                    "the afternoon: read the metadata, open the attribute table, check the extents "
                    "and the currency, and check the CRS. Lab 9 makes you reproject a road layer "
                    "for exactly this reason.",
    ),
    dict(
        section="Part 1 — From a question to a selection",
        prompt="“How many schools are in Utah County?” You have a statewide schools point layer and a counties polygon layer. Which pair of operations answers it?",
        setup="",
        options=[
            "Select by attribute on the counties (\"NAME\" = 'UTAH'), then select by location on the schools",
            "Select by attribute on both layers",
            "Select by location on the counties, then select by attribute on the schools",
            "Buffer the county, then reclassify the schools",
        ],
        correct=0,
        explanation="An attribute query knows nothing about geography — it is a database WHERE "
                    "clause that happens to select shapes, and it is the right way to pick the "
                    "county out by name. The little word “in” is the spatial half, and that is "
                    "select by location, with a relationship of within or intersects. Translating "
                    "that preposition into an operation on geometry is the whole analysis. One "
                    "warning for the next step: select by location only highlights features, so "
                    "when you need them as a layer, reach for Extract by Location instead.",
    ),
    dict(
        section="Part 2 — What each tool puts out",
        prompt="You buffer a river polyline layer by 10 km. What geometry comes out, and what are the distance units?",
        setup="",
        options=[
            "Polylines, offset by the distance in the layer's CRS units",
            "Polygons, and the distance is always in meters",
            "Polygons, and the distance is in the units of the layer's CRS",
            "Polygons, and the distance is always in degrees",
        ],
        correct=2,
        explanation="Buffer always returns polygons, whatever goes in: points give circles, lines "
                    "give ribbons, polygons come out fattened. The distance is read in whatever "
                    "the layer's coordinate system measures in, so a layer in geographic "
                    "coordinates has to be reprojected before the number 10,000 means anything.",
    ),
    dict(
        section="Part 2 — What each tool puts out",
        prompt="You want the roads inside a national park, and you need to know which park each road belongs to. Clip or Intersection?",
        setup="",
        options=[
            "Clip — it is the standard tool for trimming one layer to another",
            "Intersection — it keeps the attributes of both layers, so each output road carries the park's name",
            "Union — it keeps everything, so the park names are in there somewhere",
            "Select by location — it tags the roads with the park they fall in",
        ],
        correct=1,
        explanation="Clip and intersect give you the same picture and a different table. Clip is a "
                    "cookie cutter: it keeps the input's geometry and the input's attributes, and "
                    "the overlay is only a shape to cut with. If you wanted just “the roads inside "
                    "the park,” clip is right. The moment you need to know what came from where, "
                    "you need intersect — so ask which one you are after before you pick.",
    ),
    dict(
        section="Part 2 — What each tool puts out",
        prompt="You run Union on a counties layer and a circular study-area polygon. What is in the output layer?",
        setup="",
        options=[
            "Only the parts of the counties that fall inside the circle",
            "Only the parts of the counties that fall outside the circle",
            "Everything — the overlap and both remainders, with every feature cut wherever the other layer's boundary crossed it",
            "The counties exactly as they were, with one extra attribute column",
        ],
        correct=2,
        explanation="Union is the greedy one: no geometry is thrown away. The first option "
                    "describes intersect and the second describes difference, which is why they "
                    "are tempting. Expect empty cells in the output table wherever a feature only "
                    "existed in one of the two inputs — that is not a bug, it is what OR looks "
                    "like in a table.",
    ),
    dict(
        section="Part 3 — Chaining the tools",
        prompt="AND, OR and NOT. Which set of tools are they?",
        setup="",
        options=[
            "AND is union, OR is intersect, NOT is clip",
            "AND is intersect, OR is union, NOT is erase — which QGIS calls Difference",
            "AND is clip, OR is union, NOT is difference",
            "AND is intersect, OR is difference, NOT is union",
        ],
        correct=1,
        explanation="If you remember one slide from today, this is a good candidate: the three "
                    "overlay tools are Boolean operations with geometry attached. Watch the names "
                    "in the Processing Toolbox — under Vector overlay, QGIS calls intersect "
                    "Intersection and calls erase Difference. Clip is not one of the three; it is "
                    "a cookie cutter, not a Boolean overlay.",
    ),
    dict(
        section="Part 3 — Chaining the tools",
        prompt="Find all U.S. cities within 10 km of a major river. Which order runs it?",
        setup="You have a national rivers polyline layer and a cities point layer.",
        options=[
            "Buffer every river by 10 km, then select the major ones, then intersect with the cities",
            "Select the major rivers, buffer those by 10 km, then intersect the buffer with the cities",
            "Intersect the cities with the rivers, then buffer the result by 10 km",
            "Clip the cities with the rivers, then select the major ones",
        ],
        correct=1,
        explanation="Select, buffer, intersect — and notice the cities layer does not enter until "
                    "the last step. The first option gets the same answer and takes far longer, "
                    "because you compute a buffer around every creek in the country and then throw "
                    "most of them away. Watch the data model change down the chain: polyline, "
                    "polyline, polygon, point.",
    ),
    dict(
        section="Part 3 — Chaining the tools",
        prompt="The search area is everything inside the park, inside Idaho, and more than 5 km from a road. You already have the park-in-Idaho polygon and a 5 km buffer around the roads. What is the last step?",
        setup="This is the search-and-rescue scenario from Lab 9.",
        options=[
            "Intersection of the park polygon with the road buffer",
            "Clip the park polygon with the road buffer",
            "Difference — cut the road buffer out of the park polygon",
            "Union of the park polygon and the road buffer",
        ],
        correct=2,
        explanation="“More than 5 km from a road” is NOT, so it is Difference: the park polygon "
                    "comes out with holes in it the shape of the buffer, and what is left is the "
                    "helicopter's search area. Intersection and clip both hand you the exact "
                    "opposite — the ground crew's ribbon along the roads. If QGIS stops with an "
                    "invalid geometry error partway through this chain, run Fix Geometries and "
                    "carry on.",
    ),
]
