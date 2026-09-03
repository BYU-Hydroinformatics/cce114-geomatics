# Week 8 Thursday: Playing with Projections

**Day 15 · Thursday · Live demo and hands-on in QGIS (Dr. Halgren)** · feeds [Lab 7](../assignments/lab-07/README.md)

## At a glance

| | |
| --- | --- |
| **Goal** | Students see the difference between the project CRS and a layer's CRS, watch on-the-fly reprojection, reproject a layer for real, and measure how length and area change with the projection. |
| **Why this week** | Tuesday was geodesy, datums, projections, and the globe-and-string activity. Lab 7 uses a Tissot indicatrix layer, a state boundary, and a set of mystery points in an unknown CRS. Today is the toolkit for all of it. |
| **Students bring** | Laptop with QGIS 3.44. The **Lab 7 data** from Learning Suite (Tissot indicatrix and state boundary shapefiles, mystery points CSV), unzipped. |
| **Graded item** | *In Class Activity: Playing with Projections* (5 points). Upload a screenshot of the same data in two different projections. |
| **Feeds** | Lab 7: Projections and Coordinate Systems. Due Saturday. |

## Before class

- [ ] QGIS open with the Tissot indicatrix layer (or the Week 3 US states) loaded in a project whose CRS is **EPSG:4326**.
- [ ] Four CRS codes on a slide or sticky note: **4326** (WGS 84, degrees), **3857** (Web Mercator), **5070** (NAD83 CONUS Albers, equal area), **26912** (NAD83 UTM 12N), and **3566** (NAD83 Utah Central, US feet).
- [ ] **Project > Properties > General**: measurements set to **Ellipsoidal**, so the Measure tool gives true ground distances regardless of the projection.
- [ ] Learning Suite open to the *Playing with Projections* activity.

## Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | Project CRS: change it four times and watch the Tissot circles |
| 0:11 | Layer CRS: what does not change; on-the-fly reprojection with a second layer |
| 0:18 | Reproject for real: Export with a new CRS; compare $area and $length before and after |
| 0:27 | Choose a projection for an engineering problem, and justify it |
| 0:32 | Students: two projections, screenshot, upload |
| 0:44 | Lab 7 pointer: mystery points and how to identify an unknown CRS |

## Walkthrough

### 1. The project CRS is a lens

1. Click the CRS badge at bottom right (or **Project > Properties > CRS**). Filter `3857`, select WGS 84 / Pseudo-Mercator, OK. Greenland balloons; the Tissot circles stay circles but grow toward the poles: conformal, not equal area.
2. Filter `5070`, NAD83 / Conus Albers. The circles become ellipses but all the same area: equal area, not conformal. Say which is which and why a map of "acres burned" must be one of them.
3. Filter `26912`, UTM zone 12N. Utah looks right; the far east coast is smeared. Every projection is a local agreement.
4. Back to `4326`. Point at the status bar: coordinates are now degrees, and the map is stretched horizontally because a degree of longitude is drawn as wide as a degree of latitude.

Nothing about the data changed. The project CRS is only how the screen draws it.

### 2. The layer CRS is a fact about the file

1. Right-click the layer > **Properties > Source**. The **Assigned CRS** is what the coordinates in the file mean. Changing it here does not move the data; it changes what QGIS believes about it. Lie to it and the layer flies to the wrong place. That is the mystery-points lesson in Lab 7.
2. Add the Utah County boundary from Week 2 (stored in EPSG:26912) on top of the 4326 layer. They line up. That is on-the-fly reprojection: QGIS converts every layer to the project CRS for drawing, every frame.

### 3. Reproject for real, and measure

1. Right-click the state boundary > **Export > Save Features As...**, GeoPackage, CRS **EPSG:5070**. Add the result. Now two copies exist with different numbers inside.
2. Open the attribute table of each, **Field Calculator**, new decimal field `area_km2`, expression `$area / 1000000`. With ellipsoidal measurement on, both agree, because `$area` is computed on the ellipsoid. Now switch **Project > Properties > General** to **Planimetric** and recompute: the 4326 copy gives nonsense (square degrees) and the 5070 copy gives an honest planar area. This is the single most common projection mistake in student projects.
3. Use the **Measure Line** tool across the state in each project CRS. Ellipsoidal on: the same answer every time. Ellipsoidal off: it depends on the projection.

### 4. Choose a projection for a job

Put three problems on the screen and have the room pick and defend a CRS for each:

- A county road-resurfacing quantity takeoff (lengths in feet): **Utah Central State Plane, EPSG:3566**.
- A Utah Lake watershed area comparison: **UTM 12N, EPSG:26912**, or an Albers if the area crosses zones.
- A web map that must overlay Google tiles: **EPSG:3857**, and do the measuring somewhere else.

## Student activity

Students load the Tissot indicatrix layer (or the US states), set the project CRS to two different projections, and take one screenshot that shows both, side by side or as two screenshots combined, with the CRS badge visible in each. Upload to **In Class Activity: Playing with Projections**. Full credit for two clearly different projections named in the upload.

## Lab 7 pointer

Lab 7's mystery points CSV has coordinates with no CRS given. The method: look at the magnitude of the numbers (degrees are small, UTM eastings are six digits, State Plane feet are seven), try a candidate CRS in the delimited-text import, and check whether the points land where the accompanying description says. Show one wrong guess so they know what wrong looks like.

## Common snags

- **A layer disappears when the project CRS changes.** It is off the edge of the projection's valid area, or its assigned CRS is wrong. Zoom to Layer.
- **`$area` is a tiny decimal.** Project measurements are planimetric and the layer is in degrees. Switch to ellipsoidal, or reproject.
- **Export keeps the old CRS.** The CRS dropdown in Save Features As was left on "Layer CRS." Choose the target explicitly.
- **The CRS search finds nothing.** They typed the name with a typo; search by the EPSG number.
- **Utah Central comes in meters, not feet.** There are two: EPSG:3566 is US feet, EPSG:26912-style meter versions exist too. Read the CRS description.

## Links

- [Day 15 lecture page](../lectures/day-15.md)
- [Lab 7: Projections and Coordinate Systems](../assignments/lab-07/README.md)
- Tuesday's deck: [Geodesy, Projections, and Coordinate Systems](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-14/coordinate-systems-and-projections.html)
- [The True Size](https://www.thetruesize.com/) and [projection transitions](https://www.jasondavies.com/maps/transition/) for the opening minute
