"""Model, Format, or Reality? — Day 2 (GIS Data Models and File Formats).

Rendered by tools/build_quiz.py to docs/quizzes/data-models/index.html.
"""

SLUG = "data-models"
TITLE = "Model, Format, or Reality?"
DAY = 2
WEEK = 2
TOPIC = "GIS Data Models and File Formats"
DESCRIPTION = "CCE 114 in-class self-check: model versus reality versus file format, naming the vector, raster, and TIN data models, and what each one costs."

BLURB = """Eight questions in three parts: telling a <strong>model</strong> from reality and from the
      <strong>file format</strong> it is stored in, naming the model you are looking at, and what
      each one <strong>costs</strong> you."""

CLOSING = """\
        <strong style="color: var(--text);">The summary, one more time:</strong><br>
        <strong>Vector</strong> &mdash; discrete features, few distinct values<br>
        <strong>Raster</strong> &mdash; continuous surfaces, highly variable<br>
        <strong>TIN</strong> &mdash; 3D surfaces, high compression<br>
        <em>The data model should follow the phenomenon, not your habits.</em>"""

MESSAGES = [
    "Every one. That is Chapter 2 in twelve questions.",
    "Solid. Reread the explanations on the ones you missed — the model-versus-format distinction comes back all semester.",
    "Worth a second run, then reread Chapter 2. The summary below is the short version.",
]

QUESTIONS = [
    dict(
        section="Part 1 — Model, format, or reality",
        prompt="A video shot from a raft running the Lochsa River at spring runoff. Data model, or reality?",
        setup="",
        options=[
            "Reality — it is a recording of the actual river",
            "A model — a video is a representation of reality, not the river itself",
            "Neither",
            "A data model only once it is loaded into QGIS",
        ],
        correct=1,
        explanation="A model is an abstraction of reality. The video is a flat, silent, two-minute stand-in for a river that is none of those things — it drops depth, temperature, discharge, and everything upstream and downstream of the raft. Every representation leaves something out; the question is always what.",
    ),
    dict(
        section="Part 1 — Model, format, or reality",
        prompt="In UtahCountyMajorRoads.shp, which part is the data model and which is the file format?",
        setup="",
        options=[
            "“Shapefile” is the data model; “polyline” is the file format",
            "“Polyline” is the data model; “shapefile” is the file format",
            "Both are file formats",
            "Both are data models",
        ],
        correct=1,
        explanation="The data model is the conceptual organization — what has to be stored. A road is a polyline: an ordered list of coordinate pairs. The shapefile is one of many ways to write those numbers to disk.",
    ),
    dict(
        section="Part 1 — Model, format, or reality",
        prompt="A classmate emails you one file, UtahCountyMajorRoads.shp, and nothing else. What happens when you open it?",
        setup="A shapefile is really a set of files that travel together.",
        options=[
            "Nothing opens — .shp on its own is unreadable",
            "The roads draw, but the attribute table is gone and the layer may not know its coordinate system",
            "Everything works; the other files are backups",
            "The roads draw as points instead of lines",
        ],
        correct=1,
        explanation="The .shp holds the geometry, the .dbf the attribute table, the .shx the index, and the .prj the coordinate system. Lose the .dbf and the lines still draw with nothing attached to them. This is the everyday argument for GeoPackage, where one file carries the lot.",
    ),
    dict(
        section="Part 2 — Name the data model",
        prompt="A photograph of the Lochsa River. Which data model is it?",
        setup="",
        options=[
            "Raster",
            "Vector",
            "Triangulated (TIN)",
            "Reality — a photo is not a model",
        ],
        correct=0,
        explanation="A photo is a grid of pixels, each holding a color as a number. That is a raster, and it is also a model: a flat grid of color values standing in for a river.",
    ),
    dict(
        section="Part 2 — Name the data model",
        prompt="A map of the same river showing the watershed boundary and the stream network. Which data model?",
        setup="",
        options=[
            "Raster",
            "Vector — a polygon for the watershed, polylines for the streams",
            "Triangulated (TIN)",
            "Point",
        ],
        correct=1,
        explanation="Discrete features with boundaries you can draw are vector. The watershed closes on itself, so it is a polygon; each stream is an ordered list of coordinate pairs, so it is a polyline.",
    ),
    dict(
        section="Part 2 — Name the data model",
        prompt="Terrain drawn as a wireframe surface, where the mesh is a regular grid of equally spaced elevation values. Raster or TIN?",
        setup="",
        options=[
            "TIN — any 3D surface mesh is a TIN",
            "Raster — the grid is regular, one elevation value per cell",
            "Vector — the wireframe is made of lines",
            "Neither; a surface is not a data model",
        ],
        correct=1,
        explanation="Regularity is the tell. A raster is an evenly spaced grid, so every cell is the same size whether the ground there is a cliff or a parking lot. A TIN is irregular on purpose: small triangles where the surface bends, large ones where it does not.",
    ),
    dict(
        section="Part 3 — Choosing a model, and what it costs",
        prompt="Colorado as a polygon takes about 80 bytes. The same state as a raster took about 360. Is the raster the better model?",
        setup="Double-precision numbers are 8 bytes each.",
        options=[
            "Yes — more storage means more detail",
            "Yes — rasters are always more accurate than vectors",
            "No — it costs four times as much and gives a blockier boundary, because the phenomenon is a boundary, not a surface",
            "It depends on which format you save it in",
        ],
        correct=2,
        explanation="The extra bytes bought pixelated edges, not accuracy. Storage is not precision, and a finer grid only makes both numbers worse. A state boundary is a discrete line, so the vector model fits it.",
    ),
    dict(
        section="Part 3 — Choosing a model, and what it costs",
        prompt="Air temperature across the state, mapped as a smooth field of color. Which data model, and why?",
        setup="",
        options=[
            "Point — temperature is measured at weather stations",
            "Polygon — each colored zone is an area",
            "Raster — temperature has a value everywhere, which is exactly what a grid of cells stores",
            "TIN — it is a continuous surface",
        ],
        correct=2,
        explanation="Temperature is continuous: there is a value at every location, not just where someone put a thermometer. Continuous and highly variable is the raster case; discrete, countable things are the vector case; and a TIN is the compact way to carry a surface for 3D work.",
    ),
]
