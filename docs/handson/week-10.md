# Week 10 Hands-On — Cities Near Rivers

**Hands-On Practice**{ .badge .badge-handson } · *Day 19 · Thursday of [Week 10 — Geoprocessing](../weeks/week-10.md)*

### Topics

- Cities near rivers in QGIS: select, reproject, buffer, intersect
- Lab 9 rehearsal: Difference and Fix Geometries

### Materials

- United States data for the cities-near-rivers analysis (posted on Learning Suite)

<!-- runsheet -->
**Feeds** [Lab 9](../assignments/lab-09/README.md).

### At a glance

| | |
| --- | --- |
| **Goal** | Students run Tuesday's chain for real, select, reproject, buffer, intersect, to find every U.S. city within 10 km of a major river, then rehearse the Difference and Fix Geometries steps that Lab 9 Part 3 depends on. |
| **Why this week** | Tuesday taught the Lab 9 toolkit in the lab's order. Lab 9 is three scenarios: floods (Reclassify by table), a noxious gas plume (Buffer with Dissolve), and search and rescue (Reproject, Select by attribute, Buffer, Clip, Fix Geometries, Difference, Extract by attribute). Today practices everything in Part 3 except Clip on smaller data, so the lab is the second time, not the first. |
| **Students bring** | Laptop with QGIS 3.44 and **United States.zip** from the Week 10 Thursday entry on Learning Suite, unzipped (cities, rivers, states). |
| **Graded item** | *In Class Activity: Cities Near Rivers* (5 points). Upload a screenshot showing all U.S. cities within 10 km of a major river. |
| **Feeds** | Lab 9: The Yellowstone Disaster. Due Saturday. Quiz 8 closes Saturday. |

### Practice run before class

> [!TIP]
> Twenty-five minutes. The whole class hangs on getting the buffer units right, and the fix is
> reprojecting the layers, not changing the project CRS.

**What you need.** QGIS 3.44 LTR and **United States.zip** from Learning Suite, holding the states,
the cities and the major rivers.

<!-- TODO: publish United States.zip on this site the way UtahCountyData.zip is published, so this
session can be rehearsed without hunting through Learning Suite. -->

<!-- TODO: confirm in the zip whether the rivers layer is already major rivers only, and if not,
which field ranks them. Step 3 below is written for either case. -->

**Do this, in order.**

1. Sketch the workflow on paper first: rivers into **Select** gives major rivers; major rivers into
   **Buffer** gives river zones; river zones plus cities into **Intersection** gives cities near
   rivers. Draw it before you click anything, because that habit is what Lab 11 and the final
   project are graded on.
2. **Vector > Data Management Tools > Reproject Layer**. Reproject the rivers, the cities and the
   states to **EPSG:5070**, NAD83 CONUS Albers, saving each into `week10.gpkg`. Buffer measures in
   the *layer's* units, so this is the step that makes 10 km mean 10 km. Setting the project CRS
   does not.
3. Open the rivers attribute table. If it holds every river, **Select by Attribute** on the field
   that ranks them and **Extract by Attribute** the major ones into `major_rivers`. If the layer is
   already major rivers only, say so and skip this step.
4. **Vector > Geoprocessing Tools > Buffer**. Input the reprojected major rivers, distance **10
   kilometers** from the unit dropdown, segments 32, **Dissolve result** ticked, output saved into
   `week10.gpkg` as `river_zones`. If the dialog warns "Distance is in geographic degrees", the
   input was not reprojected; go back to step 2.
5. **Vector > Geoprocessing Tools > Intersection**. Input the reprojected cities, overlay
   `river_zones`, output `cities_near_rivers`. Right-click the new layer > **Show Feature Count**;
   that number is the answer.
6. Cross-check: **Vector > Research Tools > Select by Location**, cities that **intersect**
   `river_zones`. The status bar count should match step 5.
7. Lab 9 rehearsal: **Vector > Geoprocessing Tools > Difference**, input the reprojected states,
   overlay `river_zones`, output `far_from_rivers`: all the land more than 10 km from a major
   river. That is the same move as Lab 9's helicopter search area. If QGIS stops on an invalid
   geometry, run **Processing Toolbox > Vector geometry > Fix geometries** on the input and run
   Difference again. (Fix Geometries is not on the Vector menu in QGIS 3.44.)

**You are ready when** the buffer is a believable 10 km corridor rather than a blob or a hairline,
steps 5 and 6 agree on the count, and `far_from_rivers` has holes along every major river.

**The one that bites.** A buffer of a layer still in degrees produces either a continent-sized blob
or an invisible hairline. Reproject the layer first; the project CRS has no effect on Buffer.

### Before class

- [ ] United States.zip unzipped, and the cities, rivers and states already reprojected to **EPSG:5070** in `week10.gpkg` on the projector machine, so the demo can start from the buffer if time runs short.
- [ ] The **Processing Toolbox** panel open (Processing > Toolbox).
- [ ] The workflow diagram from the Day 18 deck (select, buffer, intersect) on a slide.
- [ ] Learning Suite open to the *Cities Near Rivers* activity.

### Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | The question, then the diagram: rivers, select, reproject, buffer, intersect with cities, count |
| 0:08 | Reproject the three layers; show the degrees warning on Buffer before and after |
| 0:13 | Select the major rivers if needed; buffer 10 km, dissolved |
| 0:19 | Intersection: cities near rivers; count; cross-check with Select by Location |
| 0:25 | Students: run it, style it, screenshot, upload |
| 0:38 | Lab 9 rehearsal: Difference, states minus river zones; Fix Geometries if it errors |
| 0:46 | Lab 9 pointer: what each of the three parts uses |

### Walkthrough

#### 1. Draw it before you click it

Put the question on the screen: **which cities are within 10 km of a major river?** Then the diagram: rivers (line) into **Select** gives major rivers (line); those into **Buffer 10 km** give river zones (polygon); river zones and cities (point) into **Intersection** give cities near rivers (point). It is the same chain as the Day 18 deck and the self-check quiz. Every geoprocessing problem in this course, including the final project, is a diagram like this first. Lab 11 formalizes it.

#### 2. Reproject first

1. Open **Buffer** on the raw rivers layer and point at the warning: *Distance is in geographic degrees*. Cancel.
2. **Vector > Data Management Tools > Reproject Layer**: rivers, cities and states to EPSG:5070, each saved to `week10.gpkg`.
3. Open Buffer again on the reprojected rivers: the warning is gone and the unit dropdown offers kilometers. Say it plainly: the tool follows the layer, not the project. Lab 9 Part 3 starts with exactly this step.

#### 3. Select and buffer

1. If the rivers layer holds more than the major rivers, **Select by Attribute** on the ranking field, then **Extract by Attribute** to save them as `major_rivers`. Select only highlights; Extract makes the layer the next tool needs.
2. **Vector > Geoprocessing Tools > Buffer**. Distance **10 kilometers**, segments 32, **Dissolve result** ticked so overlapping buffers merge into one polygon. Output `river_zones` in the GeoPackage. Style it semi-transparent blue and zoom to the Mississippi.

#### 4. Intersection, and a cross-check

1. **Vector > Geoprocessing Tools > Intersection**: input cities, overlay `river_zones`, output `cities_near_rivers`. Points in, points out, now carrying the river zone's attributes too. Style them red, the rest gray. That is the screenshot.
2. Right-click > **Show Feature Count** and say the number.
3. **Vector > Research Tools > Select by Location** on the cities against `river_zones` should select the same number. Two tools, one answer.

#### 5. Lab 9 rehearsal: Difference and Fix Geometries

1. **Vector > Geoprocessing Tools > Difference**: input states, overlay `river_zones`. The output is every state with a hole wherever a river zone was: land more than 10 km from a major river. Lab 9's search area is built the same way, with the park in place of the states and a road buffer in place of the river zones.
2. If QGIS stops on an invalid geometry, that is the Lab 9 trap arriving early. **Processing Toolbox > Vector geometry > Fix geometries** on the input layer, then run Difference on the fixed layer.

### Student activity

Students run the reproject, select, buffer and intersection on their own laptops, style near-river cities distinctly from the rest, and take a screenshot of the whole country with the buffer visible. Upload it to **In Class Activity: Cities Near Rivers**. Full credit for a map that shows the buffer and the cities near rivers. Students who finish early run the Difference rehearsal.

### Lab 9 pointer

Lab 9 is the Yellowstone Disaster, in three parts:

- **Floods:** Reclassify by table on a 1/3 arc-second DEM, splitting at the lake's elevation.
- **Noxious gas:** create the geyser points, then Buffer 1 km with Dissolve.
- **Search and rescue:** Reproject the roads to UTM, Select by attribute to find Fish Creek Road, Buffer the selection 5 km, Clip the park to Idaho, Fix Geometries when Clip complains, Difference to cut the road buffer out of the park, and Extract by attribute to save the road as its own layer.

Clip throws an "invalid geometry" error on purpose; today's rehearsal is the fix. Say that now so nobody spends Friday night on it.

### Common snags

- **Buffer is a giant blob or a hairline.** The layer is still in degrees. Reproject it to 5070; changing the project CRS does not help.
- **Intersection or Select by Location finds zero.** The cities and the buffer are in different CRSs, or one was never reprojected. Reproject both, then run it again.
- **The output layer is temporary and vanishes.** They left the output as a scratch layer. Save to the GeoPackage.
- **Invalid geometry error on Difference or Clip.** Fix geometries on the input first (Processing Toolbox > Vector geometry), exactly as in Lab 9.
- **Everything is slow.** Statewide-detail rivers are heavy. Use the major rivers, and select before you buffer, never after.
