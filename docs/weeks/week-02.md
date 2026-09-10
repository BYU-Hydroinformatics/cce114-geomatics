# Week 2 — GIS Data Models

**Due this week (Saturday, 11:59 pm unless noted):**

- [Quiz 1: Intro to GIS & Map Design Fundamentals](../assignments/deliverables.md#reading-quizzes)
- [Lab 1: Getting Started with GIS](../assignments/lab-01/README.md)

## Tuesday — GIS Data Models, Part 1

**Lecture**{ .badge .badge-lecture } · *Day 2*

### Topics

- Model = abstraction of reality
- Data model vs. file format
- Vector data models: point, polyline, polygon
- Raster and TIN data models
- Encoding a state boundary with numbers: Cartesian, polar, TIN, raster

### Slides

- [GIS Data Models & File Formats](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-02/gis-data-models.html)

### Materials

- UtahCountyData.zip: [download](https://github.com/BYU-Hydroinformatics/cce114-geomatics/releases/download/course-data-2026/UtahCountyData.zip)

### In-class activity

Polygon data model activity: encode a state boundary using only numbers. Record your completion on Learning Suite.

### Reading

GIS Fundamentals, Chapter 2 (Data Models)

<!-- tuesday-notes -->
*In the [GIS Data Models](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-02/gis-data-models.html) deck, "Polygon Data Model Activity."*

**Setup.** Blank paper. Optionally a stack of printed state outlines with no names, one per pair.

**Run.**

1. Each pair picks a state (or is handed one). Their job: represent the state using **only numbers**. No letters, symbols, or colors.
2. Five minutes. Most pairs invent a vertex list in some coordinate system they made up; some draw a grid and fill cells; a few triangulate. Those are vector, raster, and TIN, and they just reinvented them.
3. Pairs trade papers with a neighboring pair who does not know the state and try to identify it from the numbers alone.
4. Ask which model each pair used, and what they had to agree on for the trade to work (the origin, the units, the order of the numbers). That is a coordinate system, and it is Week 8's topic.

**Learning Suite.** Students record the state they encoded and whether the other pair identified it, on *In Class Activity: State Boundary Vector Data Model Activity*.

## Thursday — First Map in QGIS

**Hands-On Practice**{ .badge .badge-handson } · *Day 3*

### Topics

- Raster and image data models, continued
- Make a map in QGIS using each data type
- Live demo of creating and editing vector data in QGIS

### Materials

- UtahCountyData.zip: [download](https://github.com/BYU-Hydroinformatics/cce114-geomatics/releases/download/course-data-2026/UtahCountyData.zip)

### In-class activity

First Map: Utah County: build a QGIS project with a basemap, the four Utah County layers, and your own point layer, and upload a screenshot. Record your completion on Learning Suite.

<div class="handson-cta" markdown="1">

**Hands-On Practice**{ .handson-cta__eyebrow }

**First Map in QGIS**{ .handson-cta__title }

This session has its own step-by-step guide: what to have ready, a practice run to do beforehand, the 50-minute plan, the click-by-click QGIS walkthrough, the graded upload, and the snags that usually come up.

[Open the Week 2 hands-on guide →](../handson/week-02.md){ .handson-cta__button }

</div>
