---
marp: true
theme: cce114
paginate: true
footer: "CCE 114 · Day 2 — GIS Data Models & File Formats"
---

<!-- _class: lead -->
<!-- _paginate: skip -->

![bg right:45% w:95%](images/dm-demo-all-five.png)

# GIS Data Models & File Formats

CCE 114 Geomatics
Dr. Dan Ames and Dr. James Halgren

<!-- Tuesday concept lecture. Thursday is the hands-on session, where students build and edit these layers themselves in QGIS. -->

---

# Today's Goals

![bg right:32% w:85%](images/dm-vector-diagram.jpg)

- By the end of class you should be able to:
  - Explain what a *model* is, and why a map is one
  - Tell a **data model** from a **file format**
  - Name the five things every GIS is built from
  - Encode the same shape three ways: **vector**, **raster**, **TIN**
  - Pick the right data model for a dataset, and say why
- Thursday, in the hands-on session, you build and edit these layers yourself in QGIS

<!-- Set expectations. This is the concepts day; the hands-on work happens Thursday. Reading is Bolstad & Manson chapter 2, Data Models, which this lecture follows closely. -->

---

# See it first, then name it

<div class="columns">
<div>

- We start in QGIS with real **Utah County** data, the same software you installed for Lab 1
- You will see, on screen, the five things every GIS is built from:
  - a **point**, a **polyline**, a **polygon**, an **attribute table**, and a **raster**
- Then we back up and ask the harder question: what is a "model," and why is a map one?
- Everything after that refers back to what you saw

</div>
<div>

![w:600 center](images/dm-five-things-panel.png)

</div>
</div>

<!-- Set up the hour: we look before we name things. Have UtahCountyData.zip already unzipped on the presentation machine if you plan to show it live; otherwise the next six slides are the same walkthrough as screenshots. -->

---

# A Quick Look: Utah County in QGIS

- Download and unzip [UtahCountyData.zip](https://byu-hydroinformatics.github.io/cce114-geomatics/lectures/data/UtahCountyData.zip), then drag each layer into QGIS:
  - **UtahCountyBoundary**: one polygon. Where does the county end?
  - **UtahCountyMajorRoads**: polylines. Length, but no area.
  - **UtahCountyCellularTowers**: points. A location, nothing more.
  - Open the towers **attribute table**: one row per tower, one column per fact
  - **UtahCountyDEM.tif**: a raster. Every cell holds an elevation.
- Click a feature with **Identify**. Ask each time: *what did the computer have to store?*

<!-- Keep this to about five minutes as a look, not a tutorial; students do the full version Thursday in the Thursday hands-on session. Drag layers in one at a time and ask the same question after each: what did the computer have to store to draw that? The next six slides are backups of every step in case the projector or QGIS misbehaves. -->

---

# Polygon: county boundary

![h:470 center](images/dm-demo-polygon.png)

<!-- One feature. The computer stored an ordered list of coordinate pairs that closes back on itself. -->

---

# Polyline: major roads

![h:470 center](images/dm-demo-polyline.png)

<!-- Ordered lists of coordinate pairs that do not close. Length, but no area. -->

---

# Point: cellular towers

![h:470 center](images/dm-demo-point.png)

<!-- One coordinate pair per tower. Ask what a point cannot tell you: size, shape, orientation. -->

---

# Attribute table: one row per feature

![h:470 center](images/dm-demo-attribute-table.png)

<!-- One row per tower, one column per fact. Select a row and the tower lights up on the map: the geometry and the attributes are linked by that row. -->

---

# Raster: elevation, one value per cell

![h:470 center](images/dm-demo-raster.png)

<!-- A regular grid. Every cell holds a number, here elevation in meters. There are no features to click on, just cells. -->

---

# All five together

![h:470 center](images/dm-demo-all-five.png)

<!-- This is the payoff view. Points, polylines, polygons, a table, and a raster in one project. -->

---

# The five things you just saw

![h:480 center](images/dm-five-things-panel.png)

<!-- Leave this slide up while you move into the abstract material. Every later section, the airplane, the river, Colorado, can point back at these five panels. -->

---

<!-- _class: quiz -->

# Data Models

![bg right:38% w:90%](images/dm-vector-diagram.jpg)

What are the **geometry characteristics** of each of these feature types?

- Points
- Polylines
- Polygons

<!-- Ask them to picture the cellular towers layer from the demo. What did QGIS actually have to store for each tower? Just a coordinate pair. -->

---

# Data Models

![bg right:38% w:90%](images/dm-vector-diagram.jpg)

- **Point** data model: `(x, y)`
- **Polyline** data model: `(x0,y0), (x1,y1), (x2,y2), …`
- **Polygon** data model: `(x0,y0), (x1,y1), (x2,y2), … (x0,y0)`
- How can you store this data?
- What is the file format?

<!-- Roads = an ordered list of coordinate pairs. Boundary = the same, but the last pair repeats the first to close the ring. Point back at the demo screenshots if anyone needs to see it again. -->

---

# Data Model vs. File Format

<div class="columns">
<div>

- **Data Model** = the *conceptual* organization of the data
- **File Format** = how data are *stored* on the computer

![w:300 center](images/dm-file-format-icons.jpg)

</div>
<div>

![w:420 center](images/dm-data-model-brain.jpg)

</div>
</div>

<!-- The demo file names make this concrete: UtahCountyMajorRoads.shp is the file format; "polyline" is the data model. The same roads could be stored as .gpkg or .geojson and still be polylines. -->

---

# What is a model?

<div style="background:#e8792b;color:#fff;border-radius:12px;padding:1.2em 1.5em;margin:0.6em auto;max-width:860px;text-align:center;">
<div style="font-size:1.9em;font-weight:700;line-height:1.3;">Model = Abstraction of Reality</div>
<div style="display:flex;justify-content:space-between;margin-top:0.9em;font-size:0.8em;">
<span style="background:#fff;color:#22262e;padding:0.2em 0.6em;border-radius:6px;">Concept, Idea, Notion, Generalization</span>
<span style="background:#fff;color:#22262e;padding:0.2em 0.6em;border-radius:6px;">Reality</span>
</div>
</div>

<!-- Refer straight back to the demo: they have already seen a point, a polyline, a polygon, a table and a raster on screen. Now ask what those five things have in common: each is a simplification of Utah County, not Utah County itself. -->

---

<!-- _class: lead -->

# Consider a model airplane

---

# Vultee P-66 Vanguard

![h:460 center](images/dm-vultee-p66.jpg)

<!-- The Vultee P-66 Vanguard was a United States Army Air Forces fighter aircraft. It was initially ordered by Sweden, but by the time the aircraft were ready for delivery in 1941, the United States would not allow them to be exported, designating them as P-66s and retaining them for defensive and training purposes. Eventually, a large number were sent to China where they were pressed into service as combat aircraft with indifferent results. But it is still a cool looking airplane that is interesting to consider from a "modeling" point of view. -->

---

# The real thing: Vultee factory footage

<a href="https://youtu.be/g0lePaHC2aI" target="_blank">

![h:430 center](images/dm-video-factory.png)

</a>

<p style="text-align:center;font-size:0.7em;margin-top:0;"><a href="https://youtu.be/g0lePaHC2aI" target="_blank">youtu.be/g0lePaHC2aI</a></p>

<!-- Vultee airplane factory video. Click the thumbnail to open it in a new tab. -->

---

# Models of the Vanguard

<div class="imggrid" style="grid-template-columns: repeat(3, 1fr);">

![h:210](images/dm-model-plane-1.jpg)

![h:210](images/dm-model-plane-2.jpg)

![h:210](images/dm-model-plane-3.jpg)

![h:170](images/dm-model-plane-4.jpg)

![h:170](images/dm-model-plane-5.jpg)

</div>

<!-- What information can you gain from each model of the Vanguard P-66? What is left out? -->

---

<!-- _class: quiz -->

# Which is the best model, and why?

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1em;text-align:center;align-items:end;">
<div><a href="https://youtu.be/74PdV0MteS8?t=47s" target="_blank"><img src="images/dm-video-model-flying.png" style="height:230px;"></a><br><strong>A</strong> (video)</div>
<div><img src="images/dm-best-model-b.jpg" style="height:230px;"><br><strong>B</strong></div>
<div><img src="images/dm-best-model-c.jpg" style="height:230px;"><br><strong>C</strong></div>
</div>

<p style="text-align:center;margin-top:0.6em;"><strong>D</strong> — It depends</p>

<!-- Answer is D. A flying model tells you about aerodynamics, the display model about proportions and paint, the toy about almost nothing. The best model depends on the question you are asking. Option A links to a video of a model airplane flying. -->

---

![bg contain](images/dm-blueprint.png)

<!-- How is this a "model" of a Vanguard P-66 airplane? Is it an abstraction of reality? Could it be considered a model? What information can you gain from this model that the photos and toys cannot give you? -->

---

<!-- _class: lead -->

# What "models" can we use to represent a river?

---

<!-- _class: quiz -->

# Is this a data model, or reality?

<div class="columns">
<div>

<a href="https://youtu.be/wSWY0Mq3zFU" target="_blank">

![w:500](images/dm-video-lochsa-raft.png)

</a>

</div>
<div>

<ol type="A">
<li>Data model</li>
<li>Reality</li>
<li>Neither</li>
</ol>

<p style="font-size:0.7em;"><a href="https://youtu.be/wSWY0Mq3zFU" target="_blank">youtu.be/wSWY0Mq3zFU</a></p>

</div>
</div>

<!-- This is a rafting ride on the Lochsa River in Idaho on Memorial Day weekend 2013 (May 28, 2013). Is this video "reality" or a "model"? It is a video of reality, but it is actually a model: a representation of reality. -->

---

<!-- _class: quiz -->

# What is this?

![bg right:55% fit](images/dm-lochsa-photo.jpg)

<ol type="A">
<li>Raster data model</li>
<li>Vector data model</li>
<li>Triangulated data model</li>
<li>Reality</li>
<li>None of the above</li>
</ol>

<!-- This is the Lochsa River in northern Idaho. A photo is a raster: a grid of pixels, each holding a color. -->

---

<!-- _class: quiz -->

# What is this?

![bg right:45% fit](images/dm-lochsa-map.jpg)

Lochsa River, northern Idaho

<ol type="A">
<li>Raster data model</li>
<li>Vector data model</li>
<li>Triangulated data model</li>
<li>Reality</li>
<li>None of the above</li>
</ol>

<!-- Watershed boundaries and stream lines: vector polygons and polylines. -->

---

<!-- _class: quiz -->

# Which data model best represents the Lochsa River?

<div class="columns" style="grid-template-columns: 1fr 2fr;">
<div>

<ol type="A">
<li>The photo</li>
<li>The video</li>
<li>The map</li>
<li>The time series table</li>
<li>The graph</li>
</ol>

</div>
<div>

<div style="display:flex;gap:0.6em;align-items:flex-start;justify-content:center;">
<img src="images/dm-lochsa-table.png" style="height:330px;">
<img src="images/dm-lochsa-graph.png" style="height:330px;">
</div>

</div>
</div>

<!-- Here is another representation of the streamflow in the Lochsa River at the same time: the USGS gage table and hydrograph. Which "model" gives you more information, the video or the plot? What kind of information is provided in both? What is not communicated in each? -->

---

<!-- _class: lead -->

# Part 2

## Encoding the world with numbers: vector, raster, TIN

---

<!-- _class: lead -->

# Consider a U.S. State

---

![bg contain](images/dm-colorado-outline.png)

<!-- Look at this state outline. Anyone know which state it is? Right, Colorado. How did you know? Spatial reasoning based on the shape and the location of Denver.

How can we represent this state shape using the fewest bytes of memory possible? Let's digitize the corners. I have to measure them from some point of origin; for this example I measured distances from an origin at the exact center of the image. We also need to know the units. Here the units are inches, so we would need to scale them up to kilometers to make this "geolocatable". -->

---

# "I'll Sue Ya" (Weird Al Yankovic)

<div class="columns">
<div>

<a href="https://youtu.be/MeXQBHLIPcw?t=2m6s" target="_blank">

![w:520](images/dm-weird-al.jpg)

</a>

</div>
<div>

- Weird Al sues the state of Colorado for looking a little too much like Wyoming
- Play from 2:06 to about 2:30
- <a href="https://youtu.be/MeXQBHLIPcw?t=2m6s" target="_blank">youtu.be/MeXQBHLIPcw?t=2m6s</a>

</div>
</div>

<!-- We are going to look at the state of Colorado. Play the audio from 2:06 to 2:30 and stop there; some later scenes are a little dodgy to show in class. -->

---

<!-- _class: activity -->

# Polygon Data Model Activity

<div class="columns">
<div>

- Choose a state
- Look at the state and figure out a good way to represent it using **ONLY numbers**
- Think about the data encoding models from the book: **raster**, **vector**, **TIN**
- Feel free to invent your own
- **RULE:** no symbols, colors, or letters. Just numbers…

</div>
<div>

**Discussion:** Which data model did you use to encode your state?

<ol type="A">
<li>Vector</li>
<li>Raster</li>
<li>Triangulated (TIN)</li>
<li>Other</li>
</ol>

</div>
</div>

<!-- Give students five minutes in pairs. Have a few groups show their encoding on the board before revealing the next slides. -->

---

![bg contain](images/dm-colorado-cartesian.png)

<!-- Given just these coordinates, we can come up with a numeric representation of the shape. Why are there five rows in the table? Because we need to "close" the polygon. This is typical of spatial data representation in most data models.

It takes 8 bytes (64 bits) of memory to hold a single double-precision real number, so how much memory is required to store this polygon? 80 bytes.

How accurate is this representation of Colorado? Not very. The red lines are straight and the black lines are curved. But isn't Colorado a rectangle? The data are projected. We learn about projection systems and distortion in a later week. -->

---

![bg contain](images/dm-colorado-polar.png)

<!-- Here is another way to represent the geometry of the state. What method is this? A polar (radial) coordinate system: we assume one point at an origin and measure the distance and angle to each of the other points in sequential order. L is the length and theta is the angle measured from due east. -->

---

![bg contain](images/dm-colorado-tin.png)

<!-- Another way: triangles. In what case would this be a very efficient method for representing data? You can use triangles to represent 3D objects like an elevation surface really efficiently, because it uses fewer triangles in large flat areas and more triangles in rough, highly varying areas. For a video game, for example, it is most efficient to represent objects and terrain as triangles with textured images on the faces. -->

---

# Triangulated Irregular Network (TIN)

![h:460 center](images/dm-tin-dolphin.png)

<!-- A mesh of triangles. Big triangles where the surface is flat, small ones where it curves. -->

---

# TIN: more triangles where it matters

<div class="columns">
<div>

![h:400 center](images/dm-tin-face.png)

</div>
<div>

![h:400 center](images/dm-tin-hands.png)

</div>
</div>

<!-- The three hands are the same shape at 25,000, 5,000 and 500 vertices. Ask which one you would choose for a video game versus a surgical simulator. -->

---

# TIN terrain

![h:470 center](images/dm-tin-terrain.jpg)

<!-- Terrain as a TIN: exactly how game engines and many engineering surface models store elevation. -->

---

![bg contain](images/dm-colorado-raster.png)

<!-- Another way to represent Colorado: a raster. A raster is a regularly spaced grid of values. The raster has to be completely filled in, so you need to specify which value means "no data". Here 0 means no data and 1 marks the state.

What is good about it? Fast, easy to fill in. What is bad? Pixelated borders and a lot of memory. How many bytes? 360 here. Is this a "better" data model? Does the additional storage result in more accuracy? No. -->

---

![bg contain](images/dm-colorado-raster-fine.png)

<!-- What do you think of the higher-resolution raster? Does it make sense to represent a polygon with a raster data model? No? Then what kind of data would it make sense to represent with a raster? -->

---

# Each pixel is a number

<div class="columns">
<div>

![w:520 center](images/dm-pixels-eye.png)

</div>
<div>

![w:460 center](images/dm-pixels-hex.png)

</div>
</div>

Each pixel (raster cell) is stored as a hexadecimal number that tells the screen which color to display.

<!-- Digital photos are raster images. Each pixel has a different value from the one next to it, representing a different color. Raster works really well for digital photos. -->

---

<!-- _class: quiz -->

# Which data model for air temperature?

![bg right:55% fit](images/dm-temperature-map.jpg)

- Point?
- Line?
- Polygon?
- Raster?

<!-- Raster. Each cell contains a temperature value; the colors are drawn by the GIS software based on the value. Temperature is continuous: it has a value everywhere, which is exactly what a raster stores. -->

---

# Raster: tsunami wave heights

![h:470 center](images/dm-tsunami.jpg)

<!-- Predicted wave heights and propagation times for the 2011 Fukushima earthquake, from NOAA. Another continuous surface: every cell of ocean has a value. -->

---

![bg](images/dm-valley-photo.jpg)

<!-- How about terrain? Ask students what they would need to store to describe this valley to a computer, then go to the next slide. -->

---

<!-- _class: quiz -->

# What data model represents the terrain here?

![bg right:52% fit](images/dm-terrain-wireframe.jpg)

<ol type="A">
<li>Vector</li>
<li>Raster</li>
<li>Triangulated (TIN)</li>
<li>Other</li>
</ol>

<!-- Raster: a regular grid of elevation values drawn as a wireframe surface. Compare with the TIN terrain slide: the grid here is regular, the TIN was not. -->

---

# When to use each data model

<div class="columns">
<div>

- **Vector**
  - Fewer distinct values
  - Discrete features
- **Raster**
  - Highly variable
  - Continuous surfaces
- **TIN**
  - 3D rendering
  - High data compression

</div>
<div>

![w:460 center](images/dm-vector-diagram.jpg)

![h:230 center](images/dm-tin-terrain.jpg)

</div>
</div>

<!-- The summary slide. Discrete things you can count (towers, roads, parcels) are vector. Things that vary everywhere (elevation, temperature, imagery) are raster. TINs are a compact way to store surfaces for 3D work. -->

---

<!-- _class: activity -->

# Thursday: hands-on in QGIS

![bg right:40% w:90%](images/dm-demo-point.png)

- Create a map in QGIS with the [Utah County data](https://byu-hydroinformatics.github.io/cce114-geomatics/lectures/data/UtahCountyData.zip)
- Create a new **vector layer**, choosing the right geometry type
- Use the editing toolbar to add points and edit vertices
- Note the vocabulary: a *vector layer* is a **feature class** in a geodatabase, or a **shapefile** in a folder

<!-- Preview of Thursday. The Thursday session students create and edit vector layers with the data from today's demo. -->

---

# Before Next Class

- Read Chapter 2, *Data Models*, in *GIS Fundamentals* (Bolstad & Manson)
- Take the open-book quiz on Learning Suite
- Bring your laptop with QGIS installed on Thursday, and download [UtahCountyData.zip](https://byu-hydroinformatics.github.io/cce114-geomatics/lectures/data/UtahCountyData.zip) beforehand
- Current lab: see the [Assignments page](https://byu-hydroinformatics.github.io/cce114-geomatics/assignments/)
- Questions? Office hours: [calendly.com/dan-ames/office-hours](https://calendly.com/dan-ames/office-hours)

<!-- Fill in the quiz due date and the current lab before class. -->
