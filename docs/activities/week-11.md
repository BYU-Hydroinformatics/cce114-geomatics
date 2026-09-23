# Week 11 Activity — Georeference Your Neighborhood Sketch

**Lecture**{ .badge .badge-lecture } · *Day 20 · Tuesday of [Week 11 — Geoplanning and Georeferencing](../weeks/week-11.md)*

**Graded in-class activity.** Georeference Your Neighborhood Sketch: draw your neighborhood in pencil, photograph it, email it to yourself, and georeference it in QGIS. Record your completion on Learning Suite.

<!-- notes -->
*New in Fall 2026, paired with the Tuesday georeferencing presentation. Thursday of the same week, the hands-on session runs the advanced version with a real scanned map; see the [Week 11 hands-on guide](../handson/week-11.md).*

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
