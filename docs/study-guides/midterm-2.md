# Midterm 2 Study Guide

**Midterm 2** (Concepts Exam 2) is a closed-book, concept-based exam in the **Testing Center**. It is
given in **Week 12** and covers **Weeks 7–12**: finding spatial data and web services; geodesy,
projections and coordinate systems; metadata; geoprocessing; geoplanning and georeferencing; and
project site selection. The earlier material comes back only where these topics build on it. The
exact Testing Center window is on Learning Suite. Go early in the window rather than on the last
afternoon.

**Conditions.** Paper and pencil, closed book and closed notes, with no computer, phone or other
device. **Bring a calculator**: any calculator that is not a phone is allowed. You have **3 hours**,
which is plenty. Most students finish in about half that.

**What the exam looks like.** About **60 questions**, all multiple choice or true/false, each with
one best answer. They are grouped by topic, in the order the course taught them. A **"Using QGIS"**
section near the end shows screenshots from Labs 6–9 and the lecture slides (a connection dialog, a
metadata page, a reclassify table, a buffer, a geoprocessing dialog, a Model Designer workflow) and
asks what a setting does or what a tool produces. You mark your answers on the **Testing Center's
answer sheet**, and only the answer sheet is scored. Work in the booklet as you go, and leave time
at the end to copy every letter onto the sheet.

**What is not on this exam.** **Lab 11** (Walmart Site Selection) is due the same week as the exam,
so no question depends on having finished it. The **Week 12 Tuesday lecture** on site selection is
on the exam, though. The final project and the Web Mapping with AI Experience are not on it.

## How to study for this exam

- **Take your Learning Suite reading quizzes again** (Quizzes 6–8). The same ideas come back on the
  exam, this time without the book.
- **Retake the self-check quizzes** linked under each week below. Many exam questions test the same
  ideas in different words.
- **Come to the Week 12 Thursday review**, or go through the [Concepts Review](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-23/concepts-review.html)
  slides yourself before you test. If you take the exam before Thursday, do the slides first.
- **Know what each geoprocessing tool gives back.** For Select by Expression, Select by Location,
  Buffer, Dissolve, Clip, Intersection, Union, Difference, Reproject Layer and Reclassify, say what
  goes in, what comes out, what geometry the output has, and whose attributes it keeps. Then say
  which tool answers a question asked in plain words.
- **Draw the workflows.** Sketch the cities-near-rivers and Walmart workflows as flowcharts, and say
  why the order of the steps matters and where reprojecting has to happen.
- **Go back through Labs 6–9 with QGIS's dialogs in mind.** Be able to say what each setting you
  changed did, and why a step was needed.
- **Read every option before you choose.** If the answer seems obvious, it probably is. The exam is
  not trying to trick you, but a wrong option that looks right at first glance is often a mistake
  students really make.

**How to use the weekly lists.** Each week lists what you should be able to do. Turn every line into
a question and answer it out loud without notes. If you cannot, open that week's slides (press
<kbd>P</kbd> for the speaker notes, which carry the explanations) and the self-check quiz.

## Week 7 — Finding Spatial Data and Web Services

*Slides:* [Finding Spatial Data](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-12/finding-spatial-data.html), [Web Services](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-13/web-services.html). *Self-check:* [Who Already Has This Data?](../quizzes/find-data/index.html), [A Picture, or the Features?](../quizzes/services/index.html). *Lab:* [Lab 6](../assignments/lab-06/README.md). *Week page:* [Week 7](../weeks/week-07.md).

- Name the national sources of spatial data (data.gov, The National Map, EarthExplorer) and say what you would go to each for
- Say what the **Utah Geospatial Resource Center (UGRC)** and the **SGID** are
- Define a **GIS web service**, and say when to use one instead of downloading a file, and when a download is better
- Tell services that send **a picture** (WMS, WMTS, XYZ tiles) from services that send **the features** (WFS, ArcGIS feature services), and say what you can and cannot do with each, such as selecting, measuring or buffering
- Say what an ArcGIS **REST services directory** is, and what a FeatureServer or MapServer address gives you in QGIS
- For Lab 6: which Data Source Manager entry connects QGIS to UGRC, where the layers you added actually live, and the backup method if a layer will not add

## Week 8 — Geodesy, Projections, and Coordinate Systems

*Reading:* Chapter 3 (Geodesy, Datums, Map Projections, and Coordinate Systems). *Slides:* [Geodesy, Projections, and Coordinate Systems](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-14/coordinate-systems-and-projections.html). *Self-check:* [Why Is Greenland So Big?](../quizzes/projections/index.html). *Hands-on:* [Playing with Projections](../handson/week-08.md). *Lab:* [Lab 7](../assignments/lab-07/README.md). *Week page:* [Week 8](../weeks/week-08.md).

- Describe the shape of the Earth: the **geoid**, the **ellipsoid**, and a **datum**; say what Ferguson's *Square and Stationary Earth* map was
- Say what a **map projection** is for, and why every projection distorts something
- Say what a **conformal**, an **equal-area** and an **equidistant** projection each preserves
- Explain why **Mercator** makes Greenland look huge, and what a **Tissot indicatrix** shows
- Say what **Web Mercator** (EPSG:3857) is good for and what it must never be used for
- Tell a **geographic** coordinate system (degrees) from a **projected** one (meters or feet), and say what QGIS's measurement setting does to an area computed in EPSG:4326
- Explain **UTM**: the zones, the zone Utah is in, and where UTM distorts most; say why Idaho uses its own **IDTM** ("Tater Mercator")
- Say when **State Plane** is the right choice, and pick a projection for a state shaped like Tennessee
- Explain the difference between **Set CRS** and **Reproject Layer**, and what goes wrong when you use the wrong one
- For Lab 7: what the four-projection layout showed, why the same X and Y numbers land in different places in two UTM zones, and how your eye compared with The True Size

## Week 9 — Metadata

*Reading:* Chapter 7 (Digital Data). *Slides:* [Spatial Metadata](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-16/metadata.html), [Metadata Standards and Fitness for Use](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-17/metadata-standards.html). *Self-check:* [Would You Drink It?](../quizzes/metadata/index.html), [Fit for Your Use?](../quizzes/fitness/index.html). *Hands-on:* [Writing and Evaluating Metadata](../handson/week-09.md). *Lab:* [Lab 8](../assignments/lab-08/README.md). *Week page:* [Week 9](../weeks/week-09.md).

- Define **metadata**, and name the six questions every metadata record answers
- Say what metadata typically includes, and recognize something it does not
- Explain **fitness for use**: why the right data can be wrong for a job, and why a complex dataset should not be trusted for every purpose just because it exists
- Retell the lessons of the Metadata Melodrama, the beverage label, and the **Mars Climate Orbiter**
- Name the two metadata standards from class, **FGDC CSDGM** and **ISO 19115**, and say which one UGRC's `.xml` files follow and which one QGIS's metadata tabs follow
- Fill in QGIS metadata under Layer Properties > Metadata, and say what has to happen for it to travel with the data
- For Lab 8: how UGRC's metadata arrived with the download, where you found the coordinate reference system, and how you answered the project team's questions from the metadata

## Week 10 — Geoprocessing

*Reading:* Chapter 9 (Basic Spatial Analysis). *Slides:* [Introduction to Geoprocessing](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-18/introduction-to-geoprocessing.html). *Self-check:* [Which Tool Answers the Question?](../quizzes/geoprocessing/index.html). *Hands-on:* [Cities Near Rivers](../handson/week-10.md). *Lab:* [Lab 9](../assignments/lab-09/README.md). *Week page:* [Week 10](../weeks/week-10.md).

- Define **geoprocessing**, and explain why the **order of steps** can change the result
- Use **Select by Expression** to pick features by an attribute, and **Select by Location** to pick them by where they are
- Say what **Buffer** produces from a point, a line and a polygon, and what the **dissolve** option changes
- Say what **Dissolve** does on its own
- Tell **Clip** (a cookie cutter) from **Intersection**, and say which attributes each keeps
- Say what **Union** and **Difference** do, and match Intersection, Union and Difference to the Boolean AND, OR and NOT
- Explain why a layer must be **reprojected** to meters before you buffer it by a distance
- Read a **Reclassify** table and give the output value for a given input
- Use the **Field Calculator** to compute a new value, such as a density, from existing fields
- Lay out the **cities near rivers** workflow as a flowchart, step by step
- For Lab 9: how the flood-risk map came from the lake level, why the roads were reprojected before buffering, and how Difference found the helicopter search area

## Week 11 — Geoplanning and Georeferencing

*Slides:* [Geoplanning: What Goes Where?](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-20/geoplanning.html). *Self-check:* [What Goes Where?](../quizzes/layout/index.html). *Hands-on:* [Georeferencing in QGIS](../handson/week-11.md). *Lab:* [Lab 10](../assignments/lab-10/README.md). *Week page:* [Week 11](../weeks/week-11.md).

- Tell the three scales of geoplanning apart: **site selection**, **site layout**, and **site design**
- Say how a project's **program** and its **constraints** each become a GIS layer, as in the Paper Site Plan activity
- Define **georeferencing**, and say what a **ground control point** (GCP) is
- Read **residuals** and the **RMS error**, and say what a large residual on one point most likely means
- Choose a **transformation type** (Polynomial 1, Helmert, Thin Plate Spline) for a scan, and say why a zero error can be a warning sign rather than good news
- For Lab 10: why the project needed a CRS that fits Mozambique, and how the flood hazard zone and canals constrained where the community could go

## Week 12 — Project Site Selection

*Slides:* [Project Site Selection: the Walmart Problem](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-22/walmart-site-selection.html), [Concepts Review](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-23/concepts-review.html). *Self-check:* [Where Would You Put It?](../quizzes/siting/index.html). *Week page:* [Week 12](../weeks/week-12.md).

- Explain site selection as a **process of elimination**
- Say which tool finds all the area **near** something, such as a school or a highway, and how to get one clean corridor instead of a chain of overlapping circles
- Say what happens to the **attribute tables** of both inputs when you run an Intersection or a Union
- Walk through the **Walmart** workflow: the criteria, the population-density step, and which tool removes the area near existing stores
- Read a workflow in the QGIS **Model Designer** and name the tool at each step
