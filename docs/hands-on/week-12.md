# Week 12 Thursday: Workflow Walkthrough, Final Project Kickoff, Exam 2 Kahoot

**Day 23 · Thursday · Live demo and hands-on in QGIS (Dr. Halgren)** · feeds [Lab 11](../assignments/lab-11/README.md) and the [Final Project](../assignments/final-project.md) · ends with the Exam 2 Kahoot

## At a glance

| | |
| --- | --- |
| **Goal** | Students see the Walmart site-selection workflow as a diagram and then as a Model Designer model, choose a county and a site-selection problem for their final project, and review for Concepts Exam 2. |
| **Why this week** | Tuesday Dr. Ames presented site selection as a process of elimination. Lab 11 asks for a workflow diagram and a GeoPackage-based analysis; the final project is the same pattern on a county and problem of their choosing. Concepts Exam 2 closes in the Testing Center Saturday. |
| **Students bring** | Laptop with QGIS 3.44. A phone for Kahoot. A group of two or three for the final project. |
| **Graded item** | None. The final project is the deliverable (due Saturday of Week 14). |
| **Feeds** | Lab 11: Walmart Site Selection, due Saturday. Final Project. Concepts Exam 2. |

## Before class

- [ ] The two decks open: [Final Mapping Project](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-23/final-project.html) and [Concepts Review](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-23/concepts-review.html). Press P for speaker notes.
- [ ] The class Google Sheet open at the **Mapping Final Projects** tab (group members, chosen county, site-selection problem, data they will need). Clear old rows. Only one or two groups per county, and not Utah County.
- [ ] A Model Designer model of the Lab 11 chain built in advance (buffer, clip, intersect, select) saved as `walmart.model3`, so the demo is a walk-through and not a build.
- [ ] The Exam 2 Kahoot from the Learning Suite **Kahoot** page (*Exam 2 Review*, or one of the *CCE 114 Exam 2* variants) at the lobby screen.
- [ ] The "Some Examples" workflow diagram slides from the Week 12 Thursday entry on Learning Suite.

## Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | Workflow diagrams: the examples, then the Lab 11 diagram, box by box |
| 0:10 | Model Designer: open the model, run it, change one parameter, rerun |
| 0:20 | Final project: the five problem options, what a good county looks like, groups fill the sheet |
| 0:32 | Kahoot: Exam 2 review |
| 0:46 | Lab 11 and final project pointers; exam closes Saturday |

## Walkthrough

### 1. Diagrams first

Show two or three of the example workflow diagrams. Then draw the Lab 11 one: Walmart points, roads, population or land-use layers in; buffers and selections in the middle; a suitable-sites layer out. Name the shape convention (blue ellipses are layers, green boxes are tools, every layer labelled with its geometry) because the final project report requires the diagram and graders look for it.

Say the elimination logic out loud: start with everything, remove what fails each criterion, what is left is the answer. Show the "all suitable areas" layer as its own output, not just pins, because the final project rubric asks for it.

### 2. Model Designer

1. **Processing > Model Designer**, open `walmart.model3`. The canvas is the diagram, executable. Inputs on the left, algorithms in the middle, outputs on the right.
2. Run it from the toolbar. Fill the inputs with the Lab 11 layers. The outputs appear in the Layers panel.
3. Double-click the buffer algorithm, change the distance, run again. The whole chain reruns in seconds. That is the point of a model: the analysis is reproducible and the parameters are arguments.
4. Show **Export as Python** briefly. The same chain as a script; CCE 414 lives here.

### 3. Final project kickoff

1. Walk the [final project page](../assignments/final-project.md) and the option slides in the Final Mapping Project deck: five site-selection problems, any Utah county except Utah County, groups of two or three.
2. What a good county looks like: enough data on UGRC (parcels, roads, zoning, hazards), a real constraint (floodplain, slope, distance to a highway), a problem you can describe in one sentence.
3. Groups fill the **Mapping Final Projects** tab now: members, county, problem, and a first list of data. Circulate; the group that leaves without a county is the group that falls behind. Aim for every group registered before Kahoot starts.
4. Timeline: work sessions Tuesday of Week 13 (Thanksgiving week, no Thursday) and Tuesday of Week 14 with Dr. Ames after his CCE 414 intro; presentations Thursday of Week 14 and Tuesday of Week 15; the report is due Saturday of Week 14.

## Kahoot (14 minutes)

Run the Exam 2 review. Reread the questions most people miss. Exam 2 covers everything since Exam 1: projections and coordinate systems, metadata, geoprocessing, site selection. The book is not available in the Testing Center.

## Common snags

- **Model Designer will not run: "Missing parameter."** An input is unconnected. Hover the red exclamation on the algorithm box.
- **The model output is a temporary layer.** Right-click the output box and set a destination, or save the layer afterwards.
- **Groups pick Utah County anyway.** It is excluded because Lab 11 and the examples use it; the point is to transfer the method.
- **A group's problem has no data.** Send them to the UGRC SGID browser during lab hour; if the key layer does not exist, change the problem, not the county.

## Links

- [Day 23 lecture page](../lectures/day-23.md)
- [Lab 11: Walmart Site Selection](../assignments/lab-11/README.md)
- [Final Project](../assignments/final-project.md)
- [Exams](../policies/exams.md)
- Tuesday's deck: [Project Site Selection: the Walmart Problem](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-22/walmart-site-selection.html)
