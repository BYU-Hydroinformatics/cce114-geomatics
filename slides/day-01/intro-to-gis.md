---
marp: true
theme: cce114
paginate: true
footer: "CCE 114 · Day 1 — Introduction to GIS"
---

<!-- _class: lead -->
<!-- _paginate: skip -->

![bg right:42% w:90%](images/gis-map-layers-illustration.png)

# Introduction to Geographic Information Systems

CCE 114 Geomatics
Dr. Dan Ames and Dr. James Halgren

---

# Today's Goals

![bg right:32% w:80%](images/gis-feature-type-icons.png)

- By the end of class you should be able to:
  - Say what a GIS is — and what it is not
  - Identify the three vector feature types: points, polylines, polygons
  - Explain how an attribute table connects to features on a map
  - Name two ways a civil or environmental engineer uses GIS
- Software for this course: **QGIS** — free, open source, runs on Mac and Windows

<!-- Set expectations for the hour. Note the software change: this course now uses QGIS, not ArcGIS Pro. QGIS is free and cross-platform, so students install it themselves rather than relying on a lab license. -->

---

<!-- _class: quiz -->

# What is GIS?

![bg right:35% w:85%](images/gis-components-illustration.png)

<ol type="A">
<li>Geographic Information System</li>
<li>Maps</li>
<li>A database</li>
<li>Hardware, software, and data</li>
<li>All of the above</li>
</ol>

<!-- Pre-assessment — take a show of hands before revealing. Answer is E: a GIS is all of these together. Don't correct wrong answers yet; slide 8 does the real definition. -->

---

<!-- _class: quiz -->

# Which would you NOT use GIS&nbsp;for?

![bg right:35% w:85%](images/gis-map-and-building.png)

<ol type="A">
<li>Determining where to place an airport</li>
<li>Flooding after a hurricane in North Carolina</li>
<li>Designing a high rise building</li>
<li>Managing the city's infrastructure</li>
<li>Traveling to a friend's house with your smart phone</li>
</ol>

<!-- Answer is C, designing a high rise building — that's a CAD/BIM task. Worth acknowledging GIS still gets used for siting and context around a high rise, so the distinction is about the design work itself, not the project. -->

---

<!-- _class: quiz -->

# What is the name of the GIS software we will use in this class?

![bg right:35% w:90%](images/gis-qgis-laptop.png)

<ol type="A">
<li>Civil 3D</li>
<li>GRASS</li>
<li>QGIS</li>
<li>ArcGIS Pro</li>
<li>AutoCAD</li>
</ol>

<!-- Answer is C: QGIS. Most students will guess ArcGIS Pro if they've heard of GIS before, or Civil 3D from other CCE courses — that's the teachable moment. Mention it's free, open source, and theirs to keep after graduation. -->

---

<!-- _class: activity -->

# What is your "Spatial Identity"?

<div class="columns">
<div>

- Where were you born?
- Where did you grow up?
- Where have you travelled/served a mission?
- Where do you want to travel?
- What is your favorite foreign food?
- Where would be the best marriage proposal location?

</div>
<div>

<div style="background:#4a90c2;color:#fff;padding:0.6em 0.9em;border-radius:8px;text-align:center;font-weight:600;margin-bottom:0.5em;">How do these places contribute to who you are as a person?</div>

![w:420 center](images/gis-machu-picchu.jpg)

</div>
</div>

<!-- People are spatially oriented by nature. We think about where we've been, where we're at and where we're going all the time. This contributes to our "spatial identity" and is a major part of who we are as individuals. Let's play a little getting to know you game by answering these questions. -->

---

<!-- _class: activity -->

# A "Getting to Know You" Activity

![bg right:55% fit](images/gis-world-map.png)

- How does your spatial identity contribute to who you are as a person?
- Take a minute to get to know the other students in the class and to understand their spatial identity and how it is similar/differs from yours.

<!-- Let's see what your answers look like spatially… Imagine this map projected onto the floor of our classroom with Greenland near the whiteboard and Australia at the back of the room. Now go stand in the places that match your answers to these questions: Where are your primary ancestors from? Where were you born? Where would you go on vacation this year if money was no object?

As you go to different parts of the room/world, take a minute to get to know the other students in the class and to understand their spatial identity and how it is similar/differs from yours. -->

---

# What is a Geographic Information System?

<div class="columns">
<div>

- Computer software and hardware for integrating
  - Spatial features
  - Attribute data
  - Analysis tools

![w:420](images/gis-us-states-map.png)

</div>
<div>

![w:540 center](images/gis-state-gpa-table.png)

</div>
</div>

<!-- Spatial features (the state polygons) link to attribute data (the GPA table) — each state on the map has a row in the table. -->

---

# Polygon Features

![h:470 center](images/gis-qgis-polygons.png)

<!-- This is QGIS 4.2 — what students will see when they install it. Point at the Layers panel on the left: the checkbox controls visibility, and the order controls what draws on top. Polygons here are Utah city boundaries. -->

---

# Polyline Features

![h:470 center](images/gis-qgis-polylines.png)

<!-- Same project, roads layer turned on instead. Polylines have length but no area. Ask: is a river a polyline or a polygon? (Depends on scale — good discussion.) -->

---

# Point Features

![h:470 center](images/gis-qgis-points.png)

<!-- Points are city centers derived from the city polygons. Ask what a point loses compared to a polygon — area, shape, boundary. -->

---

# Attribute Table

![h:470 center](images/gis-attribute-table.png)

<!-- One row per feature, one column per attribute. Point out Shape_Leng and Shape_Area: QGIS carries geometry-derived fields too. Select a row in the live demo to show the map/table link. -->

---

# Bringing It All Together…

![bg right:58% fit](images/gis-qgis-all-layers.png)

- Do you see points? Polylines? Polygons?
- Do you see the attribute table?
- QGIS live demo…

<!-- All three feature types plus the attribute table. This is the payoff slide — everything they'll do in Lab 1 is visible here. -->

---

# Analysis Tools

![h:470 center](images/gis-processing-toolbox.png)

<!-- Processing Toolbox is the QGIS equivalent of ArcToolbox. Buffer is the classic first tool: it answers 'what is within X distance of this feature?' Don't run it here — save it for the live demo. -->

---

# Live Demo — QGIS

![bg right:32% w:88%](images/gis-live-demo-illustration.png)

- Add the layers — counties, roads, cities
- Toggle each layer on and off in the Layers panel
- Identify a feature: click it and read its attributes
- Open the attribute table — select a row, watch it light up on the map
- Change the symbology: color, outline, point size
- Run one tool: Processing Toolbox → Vector geometry → Buffer
- Follow along on your own laptop if you already have QGIS installed.

<!-- Keep this to about ten minutes. If the projector or QGIS misbehaves, the screenshots on slides 9-14 cover the same ground. -->

---

# Why is Spatial Information Important to Civil/Environmental/Construction Engineers?

<div class="imggrid" style="grid-template-columns: repeat(3, 1fr);">

![h:200](images/gis-parcel-map.jpg)

![h:200 center](images/gis-salmon-watershed.jpg)

![h:200](images/gis-tceq-regions.png)

![h:180](images/gis-river-land-tirol.png)

![h:180 center](images/gis-mangrove-biomass.png)

</div>

<!-- Examples left to right: land parcels (surveying/land development), Middle Fork Salmon River watershed (hydrology), TCEQ service regions (environmental regulation), River Land Tirol river network (water resources mapping), mangrove standing biomass from remote sensing (environmental monitoring). -->

---

<!-- _class: activity -->

# Activity

<div class="columns">
<div>

- Explore uses of GIS in Civil and Construction Engineering. Add what you find to the **class activity sheet** — scan the code or use the link on Learning Suite.

</div>
<div>

![w:260 center](images/gis-activity-qr.png)

<p style="text-align:center;font-size:0.7em;margin-top:0;"><strong>Class activity sheet</strong></p>

</div>
</div>

<div style="display:flex;gap:0.6em;justify-content:center;align-items:center;margin-top:0.4em;">

![h:130](images/gis-tceq-regions.png) ![h:130](images/gis-parcel-map.jpg) ![h:130](images/gis-salmon-watershed.jpg) ![h:130](images/gis-river-land-tirol.png) ![h:130](images/gis-mangrove-biomass.png)

</div>

<!-- Give students a few minutes to search for real GIS applications in civil and construction engineering and add them to the shared activity sheet. -->

---

# Before Next Class

![bg right:35% w:88%](images/gis-before-next-class.png)

- Read the assigned pages in *GIS Fundamentals* (Bolstad & Manson, 7th ed.)
- Take the open-book quiz on Learning Suite — due Friday at midnight
- Install QGIS on your own computer (free: [qgis.org/download](https://qgis.org/download))
- [Lab 1](https://byu-hydroinformatics.github.io/cce114-geomatics/assignments/lab-01/) is assigned Tuesday and due Saturday night
- Questions? Office hours: [calendly.com/dan-ames/office-hours](https://calendly.com/dan-ames/office-hours)

<!-- Emphasise installing QGIS before Tuesday — Lab 1 assumes it's working on their own machine. -->
