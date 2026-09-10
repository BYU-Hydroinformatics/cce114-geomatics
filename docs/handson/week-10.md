# Week 10 Hands-On — Cities Near Rivers

**Hands-On Practice**{ .badge .badge-handson } · *Day 19 · Thursday of [Week 10 — Geoprocessing](../weeks/week-10.md)*

### Topics

- Cities near rivers analysis in QGIS
- Chaining tools into a workflow

### Materials

- United States data for the cities-near-rivers analysis (posted on Learning Suite)

### Graded in-class activity

Cities Near Rivers: upload a screenshot of your map showing all U.S. cities within 10 km of a major river. Students record completion on Learning Suite.

<!-- runsheet -->
**Feeds** [Lab 9](../assignments/lab-09/README.md).

### At a glance

| | |
| --- | --- |
| **Goal** | Students run a real geoprocessing chain, buffer, then select by location or clip, to find every U.S. city within 10 km of a major river, and see the same chain as a workflow diagram. |
| **Why this week** | Tuesday introduced geoprocessing and the Yellowstone Disaster scenario. Lab 9 is three chained analyses (floods, gas plume, search and rescue) using buffer, clip, intersect, and select by location. Today is one such chain, end to end. |
| **Students bring** | Laptop with QGIS 3.44 and **United States.zip** from the Week 10 Thursday entry on Learning Suite, unzipped (cities, rivers, states). |
| **Graded item** | *In Class Activity: Cities Near Rivers* (5 points). Upload a screenshot showing all U.S. cities within 10 km of a major river. |
| **Feeds** | Lab 9: The Yellowstone Disaster. Due Saturday. Quiz 8 closes Saturday. |

### Practice run before class

> [!TIP]
> Twenty minutes. This is the cleanest geoprocessing session of the semester, and the whole class
> hangs on getting the buffer units right.

**What you need.** QGIS 3.44 LTR and **United States.zip** from Learning Suite, holding the states,
the cities and the major rivers. Unzip it and set the project CRS to **EPSG:5070**, NAD83 CONUS
Albers, before you load anything.

<!-- TODO: publish United States.zip on this site the way UtahCountyData.zip is published, so this
session can be rehearsed without hunting through Learning Suite. -->

**Do this, in order.**

1. Sketch the workflow on paper first: rivers into **Buffer** gives river zones; river zones plus
   cities into **Select by Location** gives cities near rivers. Draw it before you click anything,
   because that habit is what Lab 11 and the final project are graded on.
2. **Vector > Geoprocessing Tools > Buffer**. Input rivers, distance **10 kilometers** chosen from
   the unit dropdown rather than typed as 10000, segments 16, **Dissolve result** ticked, output
   saved into `week10.gpkg` as `river_zones` rather than left temporary. Run.
3. Style the buffer semi-transparent blue and zoom to the Mississippi to see the corridor.
4. **Vector > Research Tools > Select by Location**. Select from cities, where features
   **intersect**, comparing to `river_zones`. Read the count in the status bar; that number is the
   answer to the question.
5. Right-click cities > **Export > Save Selected Features As...** into `week10.gpkg` as
   `cities_near_rivers`. Style them red against gray.
6. Get the same answer two more ways: **Clip** cities by `river_zones`, and **Join Attributes by
   Location** so every city carries the zone it falls in.
7. Open **Processing > History**, find one of those runs, and copy it as a Python command.

**You are ready when** the buffer is a believable 10 km corridor rather than a blob or a hairline,
and your three methods agree on the count.

**The one that bites.** A buffer distance entered while the project is in degrees produces either a
continent-sized blob or an invisible hairline. Set EPSG:5070 first and use the unit dropdown.

### Before class

- [ ] United States.zip unzipped and the three layers loaded on the projector machine, project CRS set to **EPSG:5070** (NAD83 CONUS Albers) so buffers are in meters and honest across the country.
- [ ] The **Processing Toolbox** panel open (Processing > Toolbox).
- [ ] The workflow diagram from the Day 18 deck (the annotated buffer, select, output chain) on a slide.
- [ ] Learning Suite open to the *Cities Near Rivers* activity.

### Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | The question, then the diagram: rivers, buffer, cities, select, count |
| 0:08 | Buffer the rivers 10 km, dissolved |
| 0:14 | Select by Location: cities within the buffer; count; save selection as a layer |
| 0:21 | The same answer two other ways: Clip, and Join Attributes by Location; the Processing history |
| 0:28 | Students: run it, style it, screenshot, upload |
| 0:42 | Lab 9 pointer: three chains, one invalid-geometry trap |

### Walkthrough

#### 1. Draw it before you click it

Put the question on the screen: **which cities are within 10 km of a major river?** Then the diagram: rivers (line) into **Buffer 10 km** gives river zones (polygon); river zones and cities (point) into **Select by Location** gives cities near rivers (point). Every geoprocessing problem in this course, including the final project, is a diagram like this first. Lab 11 formalizes it.

Check the project CRS badge: EPSG:5070. Say why: a 10 km buffer in a degrees CRS is not 10 km.

#### 2. Buffer

1. **Vector > Geoprocessing Tools > Buffer**. Input: rivers. Distance **10 kilometers** (change the unit dropdown; do not type 10000 in degrees). Segments 16. Tick **Dissolve result** so overlapping buffers merge into one polygon. Output: save to `week10.gpkg` as `river_zones` rather than a temporary layer. Run.
2. Style it as a semi-transparent blue. Zoom to the Mississippi to show the corridor.

#### 3. Select by Location

1. **Vector > Research Tools > Select by Location**. Select features from: cities. Where the features: **intersect** (or *are within*). By comparing to: `river_zones`. Run.
2. The status bar shows the count selected. Say the number; it is the answer.
3. Right-click cities > **Export > Save Selected Features As...** to `week10.gpkg` as `cities_near_rivers`. Style them red, the rest gray. That is the screenshot.

#### 4. Same answer, other tools

- **Vector > Geoprocessing Tools > Clip**: input cities, overlay `river_zones`. The output is a new layer of just the cities inside, geometry unchanged for points.
- **Processing Toolbox > Join Attributes by Location**: cities joined to `river_zones`, so every city gets a field saying which river zone it is in, and cities with no match keep null. Filter on that field.
- **Processing > History** shows every run with its parameters. Copy one as a Python command to show that the click was really a function call. Model Designer, in two weeks, chains these boxes for you.

### Student activity

Students run the buffer and the select on their own laptops, save the selected cities as a layer, style near-river cities distinctly from the rest, and take a screenshot of the whole country with the buffer visible. Upload it to **In Class Activity: Cities Near Rivers**. Full credit for a map that shows the buffer and the selected cities.

### Lab 9 pointer

Lab 9 is the Yellowstone Disaster: floods (buffer rivers, clip, intersect with towns), a noxious gas plume (buffer a point, select by location), and search and rescue (a chain of three). Part 3 throws an "invalid geometry" error on purpose; the fix is **Vector > Geometry Tools > Fix Geometries** before the overlay. Say that now so nobody spends Friday night on it.

### Common snags

- **Buffer is a giant blob or a hairline.** The distance unit was degrees. Set the project CRS to 5070 and use the unit dropdown.
- **Select by Location selects zero.** Cities and buffer are in different CRSs and one has no CRS assigned, or they picked "are within" against an undissolved buffer with holes. Use intersect.
- **The output layer is temporary and vanishes.** They left the output as a scratch layer. Save to the GeoPackage.
- **Invalid geometry error on Clip.** Run Fix Geometries on the input first, exactly as in Lab 9.
- **Everything is slow.** Statewide-detail rivers are heavy. Use the major rivers layer, not the full hydrography.
