# Tuesday Lecture Activities

The Tuesday concepts lectures (Dr. Ames) each carry a short activity that keeps the hour live.
This page collects them in one place with the setup each one needs, so nothing depends on
memory. The Thursday hands-on sessions are on the [Thursday Hands-On](README.md) pages.

| Week | Activity | Graded on Learning Suite | Time |
| --- | --- | --- | --- |
| 1 | Getting to know you; uses of GIS in civil and construction engineering (class activity sheet) | no | 10 min |
| 2 | [State boundary in numbers](#week-2-state-boundary-in-numbers) | *State Boundary Vector Data Model Activity* (5) | 12 min |
| 4 | [Find Air Force One](#week-4-find-air-force-one), then [Where Am I: trilaterate Prague](#week-4-where-am-i-trilaterate-prague) | *Where Am I* (5) | 5 + 15 min |
| 6 | [Engineering paper raster analysis](#week-6-engineering-paper-raster-analysis) | *Engineering Paper Raster Analysis* (5) | 25 min |
| 7 | [Data source scavenger hunt](#week-7-data-source-scavenger-hunt) | no | 10 min |
| 8 | [Globe and string: the great circle](#week-8-globe-and-string-the-great-circle) | no | 8 min |
| 9 | [The metadata melodrama](#week-9-the-metadata-melodrama), then [What I learned about metadata](#week-9-what-i-learned-about-metadata) | *What I learned about metadata* (5) | 8 + 5 min |
| 11 | [Georeference your neighborhood sketch](#week-11-georeference-your-neighborhood-sketch) | *Georeference Your Neighborhood Sketch* (5) | 25 min |

Everything else on Tuesdays is discussion and the quiz-style slides built into the decks.

## Week 2: State boundary in numbers

*In the [GIS Data Models](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-02/gis-data-models.html) deck, "Polygon Data Model Activity."*

**Setup.** Blank paper. Optionally a stack of printed state outlines with no names, one per pair.

**Run.**

1. Each pair picks a state (or is handed one). Their job: represent the state using **only numbers**. No letters, symbols, or colors.
2. Five minutes. Most pairs invent a vertex list in some coordinate system they made up; some draw a grid and fill cells; a few triangulate. Those are vector, raster, and TIN, and they just reinvented them.
3. Pairs trade papers with a neighboring pair who does not know the state and try to identify it from the numbers alone.
4. Ask which model each pair used, and what they had to agree on for the trade to work (the origin, the units, the order of the numbers). That is a coordinate system, and it is Week 8's topic.

**Learning Suite.** Students record the state they encoded and whether the other pair identified it, on *In Class Activity: State Boundary Vector Data Model Activity*.

## Week 4: Find Air Force One

*In the [Global Positioning System](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-06/gps-part-1.html) deck, "Warm-up: find Air Force One." The deck opens with the two activities and then gives the short GPS explanation.*

**Setup, before class.** Tape a printed photo of Air Force One somewhere in the room, not in plain sight. Mark three fixed points in the room as satellites 1, 2, and 3 (a corner of the lectern, a door frame, a window sill; label them with sticky notes). Measure the straight-line distance from each satellite to the photo with a tape and type the three numbers into the blanks on the slide (the 2021 room's were 169, 216, and 151 inches; re-measure for 234 CB).

**Run.** Show the slide, give five minutes, let them use string, a tape, or their arms. Whoever finds it says how. The point: three ranges from three known points fix a position. That is trilateration, and it is the whole GPS idea before the math.

## Week 4: Where Am I: trilaterate Prague

*Same deck, "Activity: Where Am I?" and "The answer: Prague"; the QGIS version by Harrison Stewart is in the Teaching folder under In class activities.*

**Setup.** Printed maps of Europe with a scale bar, one per student, or let them use a web map with the measure tool. Compasses or string.

**Run.**

1. The story: lost in Europe, three radio stations announce the time, each arrives late by the travel time. Amsterdam 2.37 × 10⁻³ s, Paris 2.95 × 10⁻³ s, London 3.45 × 10⁻³ s.
2. Distance is delay × speed of light (299,792,458 m/s): about 710 km, 884 km, and 1,034 km.
3. Draw the three circles on the map. They meet at Prague.
4. Students write their name and the solution on the paper, photograph it, and upload it to *In Class Activity: Where Am I* on Learning Suite.

Fifteen minutes. Circulate and check that they converted seconds to kilometers before drawing; the usual mistake is a circle in meters on a map scaled in kilometers.

## Week 6: Engineering paper raster analysis

*In the [Raster Analysis and Map Algebra](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-10/raster-analysis-and-map-algebra.html) deck, the eight activity slides after the title.*

**Setup.** A sheet of engineering paper per student, pencils. The slides carry the problem: a Utah suitability analysis done by hand, one raster per criterion, combined with map algebra.

**Run.** Students rip the sheet into quarters, fill every cell of each quarter with a number for one criterion (the deck walks them through it), then combine the quarters cell by cell into the final raster. Insist on no blank cells; a raster is completely filled in. Twenty-five minutes. They photograph the result and upload it to *In Class Activity: Engineering Paper Raster Analysis*.

## Week 7: Data source scavenger hunt

*In the [Finding Spatial Data and Web Services](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-12/finding-spatial-data-and-web-services.html) deck, "Data Source Scavenger Hunt."*

**Setup.** The **Data Source Scavenger Hunt** tab of the class Google Sheet (columns: name, U.S. state, repository URL, then a checklist of dataset types). Clear last semester's rows.

**Run.** Groups of two or three pick a state or country someone is connected to. Five minutes to find its statewide GIS portal, a transportation dataset, and a water dataset, and to note the URL, format, and license for each in the sheet. Five minutes of reporting out: one surprise per group. Not graded.

## Week 8: Globe and string: the great circle

*In the [Geodesy, Projections, and Coordinate Systems](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-14/coordinate-systems-and-projections.html) deck, "Globe Activity: The Great Circle."*

**Setup.** Globes, one per three students, and string. Borrow globes a week ahead; the department and the library map collection have them.

**Run.** Before anyone touches a globe, each group writes down which states and countries a flight from Salt Lake City to a European city they choose will pass over. Then they stretch the string on the globe and check. The straight line on a flat map runs over Iowa and Maine; the string runs over Hudson Bay and Greenland. The rest of the lecture explains why. Eight minutes; not graded.

## Week 9: The metadata melodrama

*In the [Spatial Metadata](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-16/metadata.html) deck, "A brief metadata melodrama." The script is below; the original is "Metadata Football Data.docx" in the Lectures/Archived folder.*

**Setup.** Nine volunteers, each handed one role card printed from the script. Props are optional; a cape for Data helps.

**Cast.** Data; the villains Unreliability and Irrelevance; the six heroes What, Where, When, Why, How, Who.

**Run.** Read in order. Data reads the opening line, the villains attack, the heroes arrive one at a time, and Data closes. Eight minutes including applause.

**Script.**

**Data:** Hello, my name is Data. I am not a robot on Star Trek. I am an important bit of spatial information about the world. I can be very useful for solving engineering and science problems. Oh no! Who is that? I hope it isn't my old nemesis, Unreliability!

**Unreliability:** It is I! (evil laugh) Unreliability! And I am here to destroy your value, Data! Since you have no metadata, I am going to make you worthless and meaningless to future users. Sure, maybe that one person who created you will still love you and care about you, but no one else! Because they have no clue what you are, they will dare not use you for anything! (another evil laugh)

**Data:** Woe is me! Will no one come to my rescue?

**What:** Have no fear, Data! I am here to save you! I am the metadata element of "What"! I will describe what you are. I'll be like a citation or bibliography for you! No one will ever have to wonder what you are again!

**Where:** Have no fear, Data! I am here to save you too! I am the metadata element of "Where"! I will tell the world what part of the world you represent! I will give them your latitude (pause for cheer from the audience), your longitude (pause for cheer). I will give them (wait for it) your projection information!

**When:** Have no fear, Data! I am here to save you too! I am the metadata element of "When"! I will tell the world when you were created! I will tell the world what date or time you represent! No one will ever again falsely accuse you of being older or younger than you are! No early retirement center for you, Data! I love you, Data! (gets down on one knee) When, Data? When will you love me back?

**Data:** I feel so happy now to be protected by What, Where, and When! Yay! But wait, who is that coming to attack now? Oh dear, could it be? No! (scream) It's Irrelevance!

**Irrelevance:** Ha ha ha ha (evil screeching laugh). It's too late for you, Data! I am Irrelevance! Some people call me "So what!" I am here to destroy you once and for all! You are nothing to me! There is no reason for your existence! I will make sure the world knows you have no purpose! We don't even know how you were created or by whom! For all you know... (Darth Vader voice) I AM YOUR FATHER!

**Why:** Have no fear, Data! I am here to save you! I am the metadata element of "Why"! I will tell the world why you were created! Your life will now have real meaning! If the world knows why you were created then they can better use you for your intended purpose! No longer will people be trying to misuse you for weird and inappropriate purposes! I am awesome! (small dance) (beats chest) (chanting: Why! Why! Why! Why!)

**How:** Have no fear, Data! I am here to save you! I am the metadata element of "How"! I will tell the world how you were created! Were you collected by GPS? Satellite? A guy with a yardstick? You will never have to wonder again! I am all-knowledgeable. (shouting) I will tell you how!

**Who:** Have no fear, Data! I am here to save you! I am the metadata element of "Who"! I will tell the world who created you! No longer will you wonder who brought you into being! The world will know! The world must know! I am about to tell you right now! The words are about to come out of my mouth! Here it comes! I am about to say it! Your... creator... was...

**Data:** Well, that was strange, but I feel so much safer and happier now! I have meaning! I have purpose! I... AM... DATA! (shouting)

## Week 9: What I learned about metadata

*Same deck, "In-class activity: What I learned about metadata."*

Five minutes after the melodrama. Students write down a couple of things they learned, one of which they will actually check the next time they download data, and enter them on *In Class Activity: What I learned about metadata*. Collect two or three answers out loud.

## Week 11: Georeference your neighborhood sketch

*New in Fall 2026, paired with the Tuesday georeferencing presentation. Thursday of the same week, Dr. Halgren runs the [advanced version](week-11.md) with a real scanned map.*

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
