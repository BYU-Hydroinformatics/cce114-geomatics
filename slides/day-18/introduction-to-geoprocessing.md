---
marp: true
theme: cce114
paginate: true
footer: "CCE 114 · Day 18 — Introduction to Geoprocessing"
---

<!-- _class: lead -->
<!-- _paginate: skip -->

![bg right:45% w:90%](images/gp-title-overlay.png)

![w:110](images/byu-medallion.svg)

# Solving Spatial Problems with Geoprocessing

CCE 114 Geomatics
Civil & Construction Engineering
Brigham Young University
Dr. Dan Ames and Dr. James Halgren

<!-- Tuesday concept lecture, Week 10. Today is the vocabulary and the logic of geoprocessing: what the common tools do and how you chain them together. Thursday runs the same ideas as a hands-on QGIS session, and Lab 9 (The Yellowstone Disaster) is the graded version. -->

<!-- stamp:begin -->
<!-- _footer: '<span>CCE 114 · Day 18 — Introduction to Geoprocessing<span class="updated">Last Updated: 2026-10-28</span></span><span>© 2026 Daniel P. Ames · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a></span>' -->
<!-- stamp:end -->

---

# Today's Goals

![bg right:32% w:92%](images/gp-buffer-vector.png)

By the end of class you should be able to:

- Say what **geoprocessing** is: input data in, a tool, new data out
- Explain what **reclassify**, **buffer**, **clip** and **difference** do, the four tools Lab 9 is built on
- **Reproject** a layer before you buffer it, and say why
- Tell **select by attribute** from **select by location**, and select from extract
- Match each overlay tool to the question it answers: in **both**, in **either**, or in one **but not** the other
- Chain tools into a **workflow**, and find them in the QGIS **Processing Toolbox**

<!-- Set expectations. This is the concepts day. The tools are simple one at a time; the skill we are after is choosing the right one and putting them in the right order. -->

---

# Where We Are So Far…

<div class="columns">
<div>

- Basic GIS data types
- Cartography
- Coordinate systems and map projections
- Creating data
  - Survey / GPS
  - Discover and download

</div>
<div style="text-align:center;">

![w:400 center](images/gp-map-library.jpg)

<p style="font-size:1.5em;font-weight:700;color:#002e5d;line-height:1.25;">But what can you<br>do with it?</p>

</div>
</div>

<!-- Everything so far has been about getting data into the GIS and drawing it correctly. Ten weeks of building a map library. Today we finally ask the payoff question: now that you have the data, what can you actually compute with it? -->

---

<!-- _class: lead -->

![bg right:50%](images/gp-divider-analyze.jpg)

# Map it. Query it. **Analyze it.**

## Geoprocessing is the third one

<!-- The source deck used three logos here: "Map it", "query-it" and "Analyze It". Making a map is display. Querying is asking about what is already in the table. Geoprocessing is analysis: it makes brand new data that did not exist before you ran the tool. -->

<!-- Anime-style cartoon generated with gpt-image-2.5-flare, October 2026; prompt in tools/divider-images/week10.json. -->

---

<!-- _class: lead -->

![bg right:50%](images/gp-divider-approach.jpg)

# Part 1

## Common spatial analysis tools

<!-- Anime-style cartoon generated with gpt-image-2.5-flare, October 2026; prompt in tools/divider-images/gap-fill-2026-10.json. -->

---

# Reclassify: Continuous Values to Classes

![w:1100 center](images/gp-reclassify-wind.png)

Windspeed values 1–7 become two classes: **low** (< 4) and **high** (≥ 4).

<!-- Reclassify takes one input layer and a rule table and writes a new layer. Nothing moves; only the values change. It throws information away on purpose, because "high wind" is the thing you can act on and "4.7 m/s" is not. In QGIS: Processing Toolbox ▸ Raster analysis ▸ Reclassify by table. Lab 9 opens with exactly this tool. -->

---

# Reclassify: Population Density

![w:1100 center](images/gp-reclassify-pop.png)

Census population density becomes **sparse** and **dense**, using a threshold of 10 people per unit area.

<!-- Same tool, different data. Ask the class where the threshold came from. Somebody chose 10. Every reclassification embeds a judgement call, and it belongs in your metadata and your map's text box. -->

---

# Buffer: A Zone of Influence

![h:400 center](images/gp-buffer-vector.png)

A buffer takes **points, lines or polygons** and returns **polygons**: everything within a given distance of the input. Tick **Dissolve result** to merge overlapping buffers into one polygon.

<!-- Buffer is the workhorse. Points give circles, lines give ribbons, polygons give fattened polygons. Two things to stress: the output is always polygons, and the distance is in the units of the layer's CRS, so a layer in degrees has to be reprojected first. Dissolve: overlapping buffers stay as separate features unless you tick "Dissolve result", which merges them into one. Lab 9 Part 2 buffers the geysers by 1 km with Dissolve ticked, and Part 3 buffers Fish Creek Road the same way. In QGIS: Vector ▸ Geoprocessing Tools ▸ Buffer, or Processing Toolbox ▸ Vector geometry ▸ Buffer. -->

---

# Reproject Before You Buffer

![w:1000 center](images/gp-reproject-units.png)

Buffer measures distance in the **layer's** units, not the map's. A layer in latitude and longitude buffers in **degrees**. Run **Reproject Layer** to a CRS in meters first.

<!-- This is the step students skip, and it is the first step of Lab 9 Part 3: the roads arrive in EPSG:4269 (degrees) and get reprojected to EPSG:26912, UTM zone 12N, in meters. Setting the project CRS does not fix it; the Buffer dialog follows the layer, and warns "Distance is in geographic degrees" when it is wrong. Checked in QGIS 3.44.13: buffering a point layer in EPSG:4326 by 10 produces a buffer 10 degrees wide. In QGIS: Vector ▸ Data Management Tools ▸ Reproject Layer, or Processing Toolbox ▸ Vector general ▸ Reproject layer. -->

---

# Select by Attribute: Ask the Table

![h:400 center](images/gp-select-by-expression-qgis.png)

A query on the **table**, not the map: `"NAME" = 'UTAH'` picks Utah County out by name.

<!-- QGIS 3.44 Select by Expression on the UGRC counties: a database WHERE clause that happens to select shapes. Lab 9 Part 3 uses the same idea on the roads ("name" = 'FISH CREEK'), then buffers only the selected feature. Processing Toolbox ▸ Vector selection ▸ Select by attribute does the same job from the Toolbox. -->

---

# Select by Location: Ask the Geometry

![h:380 center](images/gp-select-by-location-qgis.png)

Which schools **intersect** the selected county? **Select** only highlights them; **Extract** by attribute or by location writes them to a new layer, which is usually what the next tool needs.

<!-- QGIS 3.44 Select by Location (Vector ▸ Research Tools), selecting the PreK-12 schools that intersect the selected Utah County feature; point out the Selected features only checkbox. Lab 9 ends Part 3 with Extract by attribute, saving Fish Creek Road as its own layer for the map. Both Extract tools are in Processing Toolbox ▸ Vector selection. -->
---

# Clip: A Cookie Cutter

![bg right:40% w:94%](images/gp-cookie-cutter.jpg)

- Cuts the **input** layer to the outline of a second layer
- Keeps the input's geometry and **only the input's attributes**
- The second layer is just a shape to cut with

**The question it answers:** *what part of this is inside that outline?*

<!-- Lab 9 Part 3 clips the national park boundaries to the state of Idaho, which is where QGIS throws its invalid-geometry error on purpose; Fix Geometries (Processing Toolbox ▸ Vector geometry) on the input, then run Clip again. Clip lives in Vector ▸ Geoprocessing Tools and in Processing Toolbox ▸ Vector overlay. -->

---

# Difference: In This but Not That

Cut the catchment out of the counties layer: keep only the parts of the counties that are **not** inside it.

**The question it answers:** *what is in the counties but not in the catchment?*

ArcGIS calls this tool **Erase**; QGIS calls it **Difference**.

![w:950 center](images/gp-difference-counties.png)

<!-- The counties layer comes out with a hole in it exactly the shape of the catchment. In QGIS this tool is called Difference, not Erase: Processing Toolbox ▸ Vector overlay ▸ Difference. Lab 9 Part 3 uses it to cut the ground crew's 5 km road buffer out of the park polygon, leaving the helicopter search area. -->

---

# Intersection: In Both

Lab 9 does not need it, but the Walmart problem in Week 12 does. Intersect the catchments with the counties: every output polygon knows **which county** and **which catchment** it belongs to.

**The question it answers:** *what is in a county and in a catchment, and which ones?*

![h:330 center](images/gp-intersection-counties.png)

<!-- Point at the output: each numbered piece is one county and one catchment, and the table underneath has both names on that row. That is what makes Intersection useful for "how much of this is in that" questions. -->

---

# Clip vs. Intersection

![bg right:36% w:94%](images/gp-cookie-cutter.jpg)

<div class="columns">
<div>

**Clip** — a cookie cutter

- Keeps the geometry of the **input** layer
- Keeps only the **input's** attributes
- The overlay layer is just a shape to cut with

</div>
<div>

**Intersection** — a true overlay

- Keeps the geometry of the **overlap**
- Keeps the attributes of **both** layers
- Use it when you need to know what came from where

</div>
</div>

Same picture, different table. Ask yourself: *do I need the second layer's attributes, or just its outline?*

<!-- This is the distinction students get wrong most often, and it is worth two minutes. If you only want "the roads inside the park", clip. If you want "the roads inside the park, tagged with which park", use Intersection. Both live in Processing Toolbox ▸ Vector overlay. -->

---

# Union: In Either

Union the circle with the counties: **nothing** is thrown away, but every polygon is split wherever the other layer's boundary crosses it.

**The question it answers:** *what is in the circle or in a county, and which of the two?*

![h:340 center](images/gp-union-counties.png)

<!-- Walk the legend: green pieces are in both layers, blue are county only, and the orange sliver is circle only, the part of the circle that hangs off the edge of the state. Nothing was deleted; the layers were merged and the boundaries were cut into each other. -->

---

# Three Overlay Tools, Three Questions

![w:1050 center](images/gp-overlay-summary.png)

<p style="text-align:center;font-size:0.8em;">If you have met logic before: that is AND, OR and NOT.</p>

<!-- The payoff slide for Part 1. Read the three questions out loud and have the class name the tool. The AND/OR/NOT line is for students who have seen logic in a math or programming class; do not dwell on it, but the reading quiz does ask which tool goes with which word. Everything in Part 2 is these, plus reclassify, buffer and clip, run in the right order. -->

---

# Finding the Tools in QGIS

<div class="columns" style="font-size:0.85em;">
<div>

![w:280 center](images/gp-toolbox-search.jpg)

Open the **Processing Toolbox**
*(View ▸ Panels ▸ Processing Toolbox)*, then type the tool name in the search box.

The old ArcGIS name is on the left; what QGIS calls it is on the right.

</div>
<div>

| ArcGIS | QGIS |
| --- | --- |
| ArcToolbox | **Processing Toolbox** |
| Reclassify | Reclassify by Table *(Raster analysis)* |
| Buffer, Dissolve | Buffer, Dissolve *(Vector geometry)* |
| Project | **Reproject Layer** *(Vector general)* |
| Select Layer By Attribute | Select by Attribute *(Vector selection)* |
| Select Layer By Location | Select by Location *(Vector selection)* |
| Table Select | **Extract by Attribute** *(Vector selection)* |
| Clip | Clip *(Vector overlay)* |
| Repair Geometry | **Fix Geometries** *(Vector geometry)* |
| **Erase** | **Difference** *(Vector overlay)* |
| Intersect | **Intersection** *(Vector overlay)* |
| Union | Union *(Vector overlay)* |

</div>
</div>

<!-- Added for the QGIS version of the course. The rows run in the order Lab 9 uses them, with Intersection and Union last. Gotchas worth saying out loud: Erase is called Difference, Intersect is called Intersection, and Fix Geometries is only in the Toolbox, not on the Vector menu (checked in QGIS 3.44.13). Also mention that "Select by location" only highlights features, while "Extract by location" writes them to a new layer, which is usually what you actually want. -->

---

<!-- _class: lead -->

![bg right:50%](images/gp-divider-workflow.jpg)

# Part 2

## Geoprocessing workflows

<!-- Anime-style cartoon generated with gpt-image-2.5-flare, October 2026; prompt in tools/divider-images/week10.json. -->

---

# Geoprocessing Workflows

![h:330 center](images/gp-workflow-generic.jpg)

One tool rarely answers a real question. The **output of one tool becomes the input of the next**.

<!-- Rectangles are layers, ovals are operations. Every intermediate layer is real data you can open, inspect and throw away. Encourage students to save the intermediate layers to files rather than leaving them as temporary scratch layers, which is exactly what Lab 9 warns about. -->

---

<!-- _class: activity -->

# Find All U.S. Cities Within 10 km of a Major River

<div class="columns">
<div>

**What input data do we need?**

![w:330 center](images/gp-us-cities.png)

![w:330 center](images/gp-us-rivers.png)

</div>
<div>

**What tools do we need?**

- **Select** — get just the "major" rivers
- **Reproject** — into a CRS in meters
- **Buffer** — a 10 km zone around them
- **Intersection** — the cities inside that zone

**What is the workflow?**

Sketch the boxes and ovals before you look at the next slide.

</div>
</div>

<!-- Give the class three or four minutes in pairs to draw the flowchart on paper. The hard part is not knowing the tools, it is ordering them and noticing that the cities layer does not enter until the last step. Watch for groups who buffer all the rivers before selecting: it works, but it takes far longer to run. The diagram on the next slide was drawn before the Reproject step was added; say it out loud: reproject the rivers and the cities before the buffer, exactly as Thursday does. -->

---

![bg contain](images/gp-cities-rivers-workflow.jpg)

<!-- The answer. Rivers (polyline) go into Select Major Rivers, producing Major Rivers (polyline). Those go into Buffer the Rivers, producing River Areas (polygon). Those, plus the Cities (point) layer, go into Intersect, producing Cities Near Rivers (point). Three tools, two intermediate layers, one answer. Point out that the data model changes at every step: polyline, polyline, polygon, point. -->

---

# Lab 9: The Yellowstone Disaster

![bg right:42% w:92%](images/gp-yellowstone-flood-layout.jpg)

- **Unprecedented climate change and natural disasters have destabilized Yellowstone.** The Park Service has asked you to find the areas that need attention first
- Three scenarios, eight tools, **no data provided** — you find it on the National Map yourself
- Not as far-fetched as it sounds: in June 2022 record flooding closed every park entrance and forced about 10,000 visitors out in a single day

<!-- Lab 9 is the graded version of today's lecture. The scenario is deliberately over the top, but every step is a real geoprocessing workflow, and the 2022 flood really did happen (nps.gov/articles/000/yell-flooding.htm). Emphasize the "no data provided" part: finding and vetting the data is half the assignment. -->

---

# Yellowstone: Set the Scene

<div class="columns">
<div>

![w:380 center](images/gp-yellowstone-scene.jpg)

Before you start the lab, watch the clip:

<p style="font-size:1.05em;"><a href="https://www.youtube.com/watch?v=JGEgTXsGOPk&t=346s" target="_blank"><strong>▶ Yellowstone movie clip</strong></a></p>

<p style="font-size:0.75em;"><a href="https://www.youtube.com/watch?v=JGEgTXsGOPk&t=346s" target="_blank">youtube.com/watch?v=JGEgTXsGOPk&amp;t=346s</a><br>(starts at 5:46)</p>

</div>
<div>

Then ask the engineer's version of the question:

- Who is **inside** the hazard zone?
- How far is **far enough**?
- Which roads still get you **out**?

Every one of those is a reclassify, a buffer, a clip or a difference.

</div>
</div>

<!-- Play the clip as the hook, then immediately turn it into geoprocessing questions so it does not feel like a break from class. Opens in a new tab; nothing is embedded. TODO: confirm the clip title and the stop point before class. -->

---

# Three Scenarios, One Toolbox

<div class="imggrid" style="grid-template-columns: 1.35fr 1fr 0.55fr;">

![h:250](images/gp-yellowstone-flood-layout.jpg)

![h:250](images/gp-yellowstone-geyser-buffer.jpg)

![h:250](images/gp-yellowstone-search-area.jpg)

</div>

<div class="columns" style="grid-template-columns:1fr 1fr 1fr;font-size:0.78em;align-items:start;">
<div><strong>1. Floods</strong><br>What is lower than the lake?<br><em>Reclassify by table</em></div>
<div><strong>2. Noxious gas</strong><br>What is within 1 km of the geysers?<br><em>Buffer + Dissolve</em></div>
<div><strong>3. Search and rescue</strong><br>What is in the park, in Idaho, and more than 5 km from the road?<br><em>Reproject, Select by attribute, Buffer, Clip, Fix Geometries, Difference, Extract by attribute</em></div>
</div>

<!-- Walk the three parts in one minute each so nobody is surprised on Saturday. Part 3 is the long one and the one where QGIS throws an "invalid geometry" error on purpose; the fix is the Fix Geometries tool. Full instructions and the rubric are on the assignments page. -->

---

<!-- _class: activity -->

# Thursday: hands-on in QGIS

![bg right:36% w:94%](images/gp-thursday-qgis.jpg)

- We build the **cities near rivers** analysis for real, in QGIS: select, reproject, buffer, intersect
- Then a dress rehearsal for Lab 9 Part 3: **Difference**, and **Fix Geometries** when QGIS complains
- Every tool's output is a layer you save to disk and feed to the next one
- The U.S. cities and rivers data is posted on **Learning Suite**
- **In-class activity — Cities Near Rivers:** upload a screenshot of your map showing all U.S. cities within 10 km of a major river, and record completion on Learning Suite

<!-- Preview of Thursday. The activity is a screenshot upload, so nobody leaves without a finished map. The next slide is the version of the workflow diagram to walk through before they start. -->

---

![bg contain](images/gp-cities-rivers-diagram.png)

<!-- The Thursday workflow, annotated. Green boxes are tools, blue ellipses are layers, and every layer is labelled with its file type and its data model: rivers come in as polyline shapefiles, Select keeps a subset of polylines, Buffer turns those into polygons, and Intersect combines the polygons with the cities points to give points back out. That bookkeeping is what students lose track of once they have five layers in the panel. Note this example buffers by 1 mile; Thursday's activity uses 10 km. It also predates the Reproject step; Thursday reprojects both layers first. -->

---

<!-- _class: activity -->

# Final Thoughts

<div class="columns" style="grid-template-columns: 1.7fr 1fr; font-size: 0.74em;">
<div>

**Quiz: Which Tool Answers the Question?** Eight questions on your phone: from a **question** to a tool, what each **tool** puts out, and **chaining** the tools. **Scan the code**, or open the link under it.

- Not graded, and every answer explains itself
- Good practice for this week's open-book quiz

**Before next class**

- Read **Chapter 9, *Basic Spatial Analysis***, in *GIS Fundamentals* (Bolstad & Manson)
- Finish **Quiz 8: Geoprocessing and Spatial Data Analysis** (open book, on Learning Suite) by Saturday
- Start [**Lab 9: The Yellowstone Disaster**](https://byu-hydroinformatics.github.io/cce114-geomatics/assignments/lab-09/) — due Saturday, 11:59 pm
- The **Community and Professional Map Experience** is due Wednesday
- Questions? Office hours: [calendly.com/dan-ames/office-hours](https://calendly.com/dan-ames/office-hours)

</div>
<div>

![w:300 center](images/gp-quiz-geoprocessing-qr.png)

<span style="font-size: 0.45em; color: #4a5568;">byu-hydroinformatics.github.io/cce114-geomatics/quizzes/geoprocessing/</span>

</div>
</div>

<!-- Lab 9 is long and involves three large downloads, one of them nearly 200 MB. Tell students to start it before Thursday so they arrive with questions. -->

<!-- Conversion notes (2026-09-02): source deck "Introduction to geoprocessing.pptx" (2021, 27 slides), plus "example cities near rivers workflow diagram.pptx" for the Thursday preview slide (rendered at 200 dpi from shapes). No slides were dropped for content; source slide 3 (the "Map it / query-it / Analyze It" logo slide) became a text-only section break because the three vendor logos added nothing at slide size. Source slide 5 (the Esri "geographic approach" table image) was rebuilt as HTML so the ArcGIS/ArcMap wording could be changed to QGIS. Seven slides are new: "Clip vs. Intersect", "Finding the Tools in QGIS", the three Yellowstone/Lab 9 slides, and the two Thursday preview slides. 36 slides total. ArcGIS screenshots that still need a QGIS re-shoot: gp-attribute-table-arcmap.jpg (attribute table), gp-select-by-query-arcmap.jpg + gp-select-by-query-sql.png (select by attribute), gp-select-by-location-arcmap.jpg (select by location) — all four are ArcMap 10.x and are flagged in their speaker notes. TODO: confirm the title of the Yellowstone movie clip and where to stop playing it. The three Yellowstone images are reused from docs/assignments/lab-09/images. -->

<!-- Update 2026-09-02: ArcGIS-era screenshots replaced with QGIS 3.44 captures made by tools/qgis_reshoot_screens.py: gp-attribute-table-qgis.png, gp-select-by-expression-qgis.png, gp-select-by-location-qgis.png replace the four ArcMap screenshots. -->

<!-- Update 2026-10-28 (figures): the reclassify, buffer, difference, intersection and union figures came from Bolstad's GIS Fundamentals and the Esri tool help. All were replaced with original synthetic figures drawn by tools/draw_geoprocessing_figures.py; no real places or data are shown. -->

<!-- Update 2026-10-28: at Dan's request the whole "geographic approach" section (its divider, the five-step table, the four worked-example steps, and the attribute-table, Select by Expression and Select by Location slides) was removed. The compass-girl divider art moved to the former Part 2 divider, replacing the blue-and-orange overlay twins, and the parts were renumbered 1 and 2. Same day, also at Dan's request: the Boolean framing was replaced with plain questions. The two A/B/C Venn drills were cut; Difference, Intersection and Union are now titled by the question each answers (in this but not that, in both, in either); and the Venn summary slide became "Three Overlay Tools, Three Questions", built from the three county overlay maps, with AND/OR/NOT kept as one line so the reading quiz still matches. -->

<!-- Update 2026-10-28 (Week 10 alignment): Part 1 now runs in Lab 9's order. Added "Reproject Before You Buffer" (new synthetic figure), "Select: by Attribute or by Location" (restoring the two QGIS 3.44 captures cut earlier the same day) and "Clip: A Cookie Cutter". The two simple Intersect/Union diagram slides were dropped as duplicates of the county versions. The tools table now follows Lab 9 and adds Reproject Layer, Select by Attribute, Extract by Attribute and Fix Geometries. The cities-near-rivers chain is Select, Reproject, Buffer, Intersection everywhere: this deck, the Thursday run sheet and the self-check quiz. Lab 9 uses eight tools, not seven. -->

<!-- Five minutes, in pairs, then a show of hands on the two worth arguing about: clip against Intersection, and the order of the cities-near-rivers chain. Both come back on Thursday and in Lab 9. If the room has no signal, put the URL on the board. -->
