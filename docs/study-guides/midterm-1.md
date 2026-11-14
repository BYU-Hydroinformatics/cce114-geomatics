# Midterm 1 Study Guide

**Midterm 1** (Concepts Exam 1) is a closed-book, concept-based exam in the **Testing Center**. It is
given midweek in **Week 7** and covers **Weeks 1–6**: introduction to GIS, data models, maps and
symbology, GPS, vector data, and raster data. The exact Testing Center window is on Learning Suite.
Go early in the window rather than on the last afternoon.

**Conditions.** Paper and pencil, closed book and closed notes, with no computer, phone or other
device. **Bring a calculator**: any calculator that is not a phone is allowed. You have **3 hours**,
which is plenty. Most students finish in about half that.

**What the exam looks like.** About **65 questions**, all multiple choice or true/false, each with
one best answer. They are grouped by topic, in roughly the order the course taught them. A
**"Using QGIS"** section near the end shows screenshots from the labs and hands-on sessions (dialog
boxes, toolbar buttons, settings) and asks what a setting does or what a tool produces. A group of
questions asks you to convert and compare **latitude and longitude** by hand. You mark your answers
on the **Testing Center's answer sheet**, and only the answer sheet is scored. Work in the booklet
as you go, and leave time at the end to copy every letter onto the sheet.

**What is not on this exam.** Week 7 (finding spatial data and web services) is on
[Midterm 2](midterm-2.md), not this one. Map projections and coordinate systems are Week 8 and also
belong to Midterm 2, although you should already know what EPSG:4326 and UTM zone 12N are from
Labs 3 and 4.

## How to study for this exam

- **Take your Learning Suite reading quizzes again** (Quizzes 1–5). The same ideas come back on the
  exam, this time without the book.
- **Retake the self-check quizzes** linked under each week below. Many exam questions test the same
  ideas in different words.
- **Practice the degree conversions until they are automatic.** Decimal degrees to degrees and
  minutes, degrees-minutes-seconds to decimal degrees and back, and how many minutes and seconds
  are in a degree. Know which latitudes and longitudes cannot exist, which lines sit at 0°, how to
  find the difference in longitude between two places on opposite sides of the Prime Meridian
  (draw a sketch), and roughly how far a small fraction of a degree of latitude is on the ground.
- **Go back through your labs with QGIS's dialogs in mind.** For each of Labs 1–5, be able to say
  what each setting you changed did. The screenshot questions use the same dialogs: the Identify
  tool, the editing toolbar, snapping options, the New Layer dialog, the Field Calculator, Add
  Delimited Text Layer, Save Features As, Graduated symbology, label buffers, and the Slope tool.
- **Read every option before you choose.** If the answer seems obvious, it probably is. The exam is
  not trying to trick you, but a wrong option that looks right at first glance is often a mistake
  students really make.
- **Pace yourself.** About 65 questions in 3 hours is close to three minutes each, with time left
  over to fill in the answer sheet.

**How to use the weekly lists.** Each week lists what you should be able to do. Turn every line into
a question and answer it out loud without notes. If you cannot, open that week's slides (press
<kbd>P</kbd> for the speaker notes, which carry the explanations) and the self-check quiz.

## Week 1 — Introduction to GIS

*Reading:* Bolstad & Manson, *GIS Fundamentals*, Chapter 1. *Slides:* [Course Introduction](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-01/course-introduction.html), [Introduction to GIS](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-01/intro-to-gis.html). *Self-check:* [What Is a GIS?](../quizzes/what-is-gis/index.html). *Week page:* [Week 1](../weeks/week-01.md).

- Say what **GIS** stands for, and what a GIS does: store, organize, maintain, analyze and share spatial data
- Say what makes something a GIS and not just a map on a screen: **spatial data plus attributes plus analysis**
- Name the civil and construction engineering disciplines that use GIS, with an example from each
- Name common uses of GIS, and recognize something that is not a GIS use
- Read a **map scale** (1:10 versus 1:100) and say which shows more detail, and why
- Say what **open source** means for QGIS, and that QGIS is one of many GIS packages
- Explain why "the best way to get data" depends on the job: download, digitize, collect with GPS, or extract from imagery

## Week 2 — GIS Data Models

*Reading:* Chapter 2 (Data Models). *Slides:* [GIS Data Models & File Formats](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-02/gis-data-models.html). *Self-check:* [Model, Format, or Reality?](../quizzes/data-models/index.html). *Lab:* [Lab 1](../assignments/lab-01/README.md). *Week page:* [Week 2](../weeks/week-02.md).

- Define a **model** as an abstraction of reality, and tell a model of the Provo River from the river itself
- Describe the **vector** data model (points, polylines, polygons) and the **raster** and **TIN** models
- Choose the best data model for a feature: a subdivision, a trail, a campground's toilets, a parking lot, air temperature, elevation
- Say whether a feature can be a point, a line or a polygon **at every map scale**, and why most real features cannot
- Explain "**raster is faster, but vector is correcter**"
- Separate a **data model** from a **file format**, and pick a sensible format for a kind of data (for example, which one holds elevation)
- For Lab 1: how you downloaded the data, built the map, and changed the symbology

## Week 3 — Maps, Symbology, and Cartography

*Reading:* Chapter 4, map design sections. *Slides:* [Maps, Symbology, and Cartography](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-04/maps-and-cartography.html). *Self-check:* [Does This Map Work?](../quizzes/map-elements/index.html). *Hands-on:* [Symbology, Labels, and a First Layout](../handson/week-03.md). *Lab:* [Lab 2](../assignments/lab-02/README.md). *Week page:* [Week 3](../weeks/week-03.md).

- Name the components of a map: data area, neat line, inset, title, legend, scale bar, north arrow, labels
- Say what a **choropleth** map is, and what QGIS calls that renderer
- Say what decides a feature's color in **Single symbol**, **Categorized** and **Graduated** symbology
- Say what a label **text buffer** (halo) does and why you would turn it on
- Tell the jobs of **map design** from the jobs of a **file format**
- Explain why engineers need maps that are clear and readable, not just accurate data
- For Lab 2: how you symbolized points, lines and polygons, labeled the cities, and built the layout

## Week 4 — The Global Positioning System

*Reading:* Chapter 5 (GNSS and Coordinate Surveying). *Slides:* [The Global Positioning System](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-06/gps-part-1.html), [GPS extended slides](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-07/gps-part-2.html). *Self-check:* [How Does It Know Where You Are?](../quizzes/gps/index.html). *Hands-on:* [Campus Field Trip](../handson/week-04.md). *Lab:* [Lab 3](../assignments/lab-03/README.md). *Week page:* [Week 4](../weeks/week-04.md).

- Name the three parts of any GNSS: the **satellites**, the **control stations**, and the **users**
- Explain **trilateration**: what the set of possible positions looks like with one, two, three and four satellites, and why the fourth one is needed
- Say what a receiver measures by lining up the satellite's **pseudo-random (PRN) code**, and how a signal delay becomes a distance
- Explain how a phone gets precise timing without an atomic clock of its own, and what (if anything) the phone sends to the satellites
- List real sources of GPS error (atmosphere, surroundings, satellite geometry or **PDOP**, user error) and spot one that is not
- Explain **differential GPS**: what the base station knows, and how its error corrects the rover
- Say what **Selective Availability** was, and that it was turned off
- Read and write positions in **decimal degrees**, **degrees-minutes-seconds**, and degrees with decimal minutes; convert between them
- Say why a degree of longitude is a poor distance measure, and roughly how far one degree of latitude, and a small fraction of one, is on the ground
- For Lab 3 and the field trip: how phone readings became points in QGIS (which setting gives their CRS), how you converted them to UTM meters, and how the Field Calculator measured your campus polygon

## Week 5 — Working with Vector Data

*Reading:* Chapter 4 (Maps, Data Entry, and Editing). *Slides:* [Working with Vector Data](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-08/working-with-vector-data.html). *Self-check:* [Who Drew That Line?](../quizzes/vector/index.html). *Hands-on:* [Digitize Your Home](../handson/week-05.md). *Lab:* [Lab 4](../assignments/lab-04/README.md). *Week page:* [Week 5](../weeks/week-05.md).

- Create a new vector layer and say which of its properties **cannot be changed** once you click OK
- Add attribute fields, choose the right **field type** (text, integer, decimal, date) for a value, and say which control actually adds the field
- Digitize and edit features, and say which button **saves your edits** to disk
- Explain **snapping**: what undershoots and overshoots are, and what the snapping tolerance in pixels controls
- Explain why digitized data is **only as accurate as its source map**, whatever scale you later draw it at
- Say why GeoPackage and shapefile are both used, and what saving to disk means for each
- For Lab 4: how you set up the point, line and polygon layers, why snapping mattered, and how you corrected the waterways

## Week 6 — Working with Raster Data

*Reading:* Chapter 2 raster sections and Chapter 10 (Raster Analysis). *Slides:* [Raster Analysis and Map Algebra](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-10/raster-analysis-and-map-algebra.html). *Self-check:* [Where Should the Water Park Go?](../quizzes/raster/index.html). *Hands-on:* [Raster Data in QGIS and an Elevation Profile](../handson/week-06.md). *Lab:* [Lab 5](../assignments/lab-05/README.md). *Week page:* [Week 6](../weeks/week-06.md).

- Describe the raster structure: a regular grid of square **cells**, each holding one value; **resolution**, **extent** and **NoData**
- Say what a **DEM** is, and what kind of problem raster data suits best
- Define **map algebra** and work a small map algebra problem by hand, as in the engineering-paper activity
- Read a raster's properties in QGIS: data type, rows and columns, cell size, units, CRS
- Symbolize a DEM with **singleband pseudocolor** and draw an elevation profile
- Say what the **Identify** tool returns when you click a raster cell
- For Lab 5: why the tiles were merged, how you read elevations off the DEM, and what each cell of the **Slope** output holds, and in what units

## Week 6 Thursday — the review

The last fifteen minutes of the Week 6 hands-on session are an **Exam 1 review Kahoot**. Come to it.
It is the best preview of the exam's style you will get.
