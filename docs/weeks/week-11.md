# Week 11 — Geoplanning and Georeferencing

**Due this week (Saturday, 11:59 pm unless noted):**

- [Lab 10: Domes for Mozambique](../assignments/lab-10/README.md)

## Tuesday — Geoplanning and Georeferencing

**Lecture**{ .badge .badge-lecture } · *Day 20*

### Topics

- Introduction to geoplanning
- Domes for the World and the Mozambique project
- Georeferencing: attaching real-world coordinates to an image that has none

### Slides

*Slides for this day are not on the site yet. They will be added as the semester goes.*

### In-class activity

Georeference Your Neighborhood Sketch: draw your neighborhood in pencil, photograph it, email it to yourself, and georeference it in QGIS. Record your completion on Learning Suite.

<!-- tuesday-notes -->
*New in Fall 2026, paired with the Tuesday georeferencing presentation. Thursday of the same week, Dr. Halgren runs the advanced version with a real scanned map in this page's Thursday section.*

**Setup.** Pencils and paper. Every student needs a laptop with QGIS 3.44 today, so announce it the Thursday before. The Google satellite XYZ basemap connection from Week 2.

**Run.**

1. **Draw** (7 minutes). On paper, in pencil, draw the neighborhood around your home or apartment from memory: your building, the streets on all four sides, and at least four things you could find on a satellite image (intersections, a park corner, a church, a parking lot). Label nothing; north up.
2. **Photograph** it with your phone and **email it to yourself**. Save the image to your laptop in a folder without spaces in the path.
3. **QGIS.** Open a project with the satellite basemap, set the project CRS to EPSG:26912, and zoom to your neighborhood.
4. **Layer > Georeferencer...** Open Raster, choose the photo. **Add Point** on an intersection in the sketch, then **From Map Canvas** and click the same intersection on the satellite image. Repeat for four points spread to the corners of the sketch.
5. **Settings > Transformation Settings**: Transformation type **Helmert** (it can rotate and scale a hand drawing but will not warp it), Resampling Nearest neighbor, Target CRS EPSG:26912, an output file next to the photo, tick **Load in project when done**. Then **Start Georeferencing**.
6. The sketch lands on the satellite image. Set its opacity to 50 percent. Which of your streets are in the right place? Which are not? Try **Polynomial 1** and compare; with six or more points, try **Polynomial 2** and notice it starts bending the drawing to fit.
7. Take a screenshot with the sketch over the imagery and upload it to *In Class Activity: Georeference Your Neighborhood Sketch* on Learning Suite.

Twenty-five minutes. What they learn: a drawing has no coordinates until you give it some, four good control points are worth more than ten bad ones, and memory is a poor surveying instrument.

## Thursday — Georeferencing in QGIS, and the Web Mapping with AI Kickoff

**Hands-On Practice**{ .badge .badge-handson } · *Day 21*

### Topics

- Georeference a scanned historic map: ground control points, transformation types, residuals
- What a site plan for the Domes for Mozambique project needs from georeferencing
- Web Mapping with AI Experience kickoff: from a QGIS layer to a public web map with an AI assistant

### Materials

- [Web Mapping with AI Experience](../assignments/web-mapping-with-ai.md)

> [!TIP]
> 🖱️ **Hands-On Practice: Georeferencing in QGIS, and the Web Mapping with AI Kickoff**
>
> This session has its own step-by-step guide: what to have ready, a practice run you can do beforehand, the 50-minute plan, the click-by-click QGIS walkthrough, the graded upload, and the snags that usually come up.
>
> **[Open the Week 11 hands-on guide &rarr;](../handson/week-11.md)**
