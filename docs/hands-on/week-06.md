# Week 6 Thursday: Raster Data in QGIS and an Elevation Profile

**Day 11 · Thursday · Live demo and hands-on in QGIS (Dr. Halgren)** · feeds [Lab 5](../assignments/lab-05/README.md) · ends with the Exam 1 Kahoot

## At a glance

| | |
| --- | --- |
| **Goal** | Students read a raster's properties, style a DEM three ways, pull an elevation profile across a valley, and run one raster analysis tool. |
| **Why this week** | Tuesday students did raster analysis by hand on engineering paper. Today the same ideas run on a real DEM. Lab 5 merges DEM tiles, styles them, reads elevations, and computes slope. Concepts Exam 1 closes in the Testing Center next Wednesday, so the last 15 minutes are the review Kahoot. |
| **Students bring** | Laptop with QGIS 3.44 and the Utah County DEM from [UtahCountyData.zip](https://byu-hydroinformatics.github.io/cce114-geomatics/lectures/data/UtahCountyData.zip) (they downloaded it in Week 2). A phone for Kahoot. |
| **Graded item** | *In Class Activity: DEM Profile* (5 points). Upload a screenshot showing a pseudocolor DEM with an elevation profile. |
| **Feeds** | Lab 5: Working with Raster Data. Due Saturday. |

## Before class

- [ ] QGIS open with the DEM loaded and the county boundary on top as an outline.
- [ ] The Exam 1 Kahoot from the Learning Suite **Kahoot** content page (*Geomatics Exam 1 Prep*) open in a second browser tab and started to the lobby screen.
- [ ] Learning Suite open to the *DEM Profile* activity.

## Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | Layer Properties: Information and Source; what the numbers mean |
| 0:09 | Symbology: singleband gray, pseudocolor with classes, hillshade |
| 0:17 | Identify a cell; Elevation tab; View > Elevation Profile across Utah Lake to the Wasatch |
| 0:25 | Raster > Analysis > Slope, and the Raster Calculator in one line |
| 0:30 | Students: pseudocolor plus a profile; screenshot; upload |
| 0:35 | Kahoot: Exam 1 prep |
| 0:48 | Lab 5 pointer; exam closes Wednesday |

## Walkthrough

### 1. What is in the file

Right-click the DEM > **Properties > Information**. Read out loud and ask what each means:

- **Dimensions**: columns by rows. The whole raster is that many numbers and nothing else.
- **Pixel size**: the cell size, in the layer's units. With EPSG:26912 that is metres; this is a 10 m or 30 m DEM.
- **CRS** and **Extent**: where the grid sits and how big it is.
- **Data type** (Float32 or Int16) and **No-data value**: a no-data cell is not zero. Zero is an elevation.

The **Source** tab shows the file path and lets you rename the layer. Renaming changes nothing on disk.

### 2. Three ways to see one grid

1. **Symbology > Render type: Singleband gray**. Min and max stretch. Dark is low.
2. **Singleband pseudocolor**. Pick a terrain color ramp, **Mode: Equal Interval**, 8 classes, **Classify**, Apply. Then try **Continuous**. Say what "pseudo" means: the cells are elevations, not colors; the ramp is a lookup table you chose.
3. **Hillshade**. Azimuth 315, altitude 45. Duplicate the layer, keep one as pseudocolor with 60 percent opacity on top of the hillshade. That pair is how most published relief maps are built.

### 3. Reading elevations

1. **Identify Features** on the DEM: one band, one value, in metres.
2. **Properties > Elevation**: set **Represents Elevation Surface**. Apply.
3. **View > Elevation Profile**. Click the **Capture Curve** tool, draw a line from Utah Lake east across Provo to the Wasatch, right-click to finish. The profile appears below the map. Ask where campus is on it, and what the vertical exaggeration is doing.
4. If the profile panel misbehaves on someone's laptop, the **Profile Tool** plugin (Plugins > Manage and Install) does the same job.

### 4. One analysis, two ways

1. **Raster > Analysis > Slope**. Input the DEM; leave the Z factor at 1 because the CRS is in metres. Run. Style the result pseudocolor. Lab 5 asks for exactly this.
2. **Raster > Raster Calculator**: expression `"dem@1" > 1500` produces a 1/0 raster of everything above 1500 m. Tuesday's engineering-paper reclass was this, done by hand.

## Student activity

Students style the DEM as singleband pseudocolor with at least five classes, draw an elevation profile across the county, and take one screenshot that shows the map and the profile panel together. Upload it to **In Class Activity: DEM Profile** on Learning Suite. Full credit for pseudocolor plus a profile.

## Kahoot (15 minutes)

Start the *Geomatics Exam 1 Prep* Kahoot from the Learning Suite Kahoot page. Students join with the PIN on their phones. Read the questions that get the most wrong answers twice; those are the ones to review before Wednesday. Remind them the Testing Center closes early on some days and the exam is closed book.

## Common snags

- **The DEM draws as a flat gray square.** Min and max are not set. Symbology > Min/Max Value Settings > **Cumulative count cut**, Apply.
- **"Represents Elevation Surface" is missing.** They are on an older QGIS. The Profile Tool plugin covers it.
- **Slope output is all zero or all 90.** Z factor or units problem: the DEM is in EPSG:4326 (degrees) so a metre rise looks enormous. Reproject the DEM to EPSG:26912 first with **Raster > Projections > Warp (Reproject)**.
- **Raster Calculator says the expression is invalid.** Layer names with spaces or hyphens need the quotes exactly as the dialog inserts them; double-click the layer in the list instead of typing.
- **Kahoot PIN will not join.** Refresh the lobby; the BYU network sometimes blocks the first attempt.

## Links

- [Day 11 lecture page](../lectures/day-11.md)
- [Lab 5: Working with Raster Data](../assignments/lab-05/README.md)
- [Exams](../policies/exams.md)
- Tuesday's deck: [Raster Analysis and Map Algebra](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-10/raster-analysis-and-map-algebra.html)
