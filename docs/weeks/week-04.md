# Week 4 — The Global Positioning System

**Due this week (Saturday, 11:59 pm unless noted):**

- [Quiz 3: GPS, Part 1](../assignments/deliverables.md#reading-quizzes)
- [Lab 3: GPS Data Collection and Importing Into QGIS](../assignments/lab-03/README.md)

## Tuesday — The Global Positioning System

**Lecture**{ .badge .badge-lecture } · *Day 6*

### Topics

- How GPS and GNSS positioning work
- Trilateration: where is Air Force One?
- Latitude and longitude, precision, and error
- Converting from latitude/longitude to meters, and why it is not straightforward

### Slides

- [The Global Positioning System](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-06/gps-part-1.html)
- [GPS extended slides: trilateration build, error budget, meters demo (reference)](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-07/gps-part-2.html)

### In-class activity

Find Air Force One, then Where Am I: trilaterate Prague on paper from three signal delays and upload a photo of your solution. Record your completion on Learning Suite.

### Reading

GIS Fundamentals, Chapter 5 (GNSS and Coordinate Surveying)

<!-- tuesday-notes -->
*In the [Global Positioning System](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-06/gps-part-1.html) deck, "Warm-up: find Air Force One." The deck opens with the two activities and then gives the short GPS explanation.*

**Setup, before class.** Tape a printed photo of Air Force One somewhere in the room, not in plain sight. Mark three fixed points in the room as satellites 1, 2, and 3 (a corner of the lectern, a door frame, a window sill; label them with sticky notes). Measure the straight-line distance from each satellite to the photo with a tape and type the three numbers into the blanks on the slide (the 2021 room's were 169, 216, and 151 inches; re-measure for 234 CB).

**Run.** Show the slide, give five minutes, let them use string, a tape, or their arms. Whoever finds it says how. The point: three ranges from three known points fix a position. That is trilateration, and it is the whole GPS idea before the math.

*Same deck, "Activity: Where Am I?" and "The answer: Prague"; the QGIS version by Harrison Stewart is in the Teaching folder under In class activities.*

**Setup.** Printed maps of Europe with a scale bar, one per student, or let them use a web map with the measure tool. Compasses or string.

**Run.**

1. The story: lost in Europe, three radio stations announce the time, each arrives late by the travel time. Amsterdam 2.37 × 10⁻³ s, Paris 2.95 × 10⁻³ s, London 3.45 × 10⁻³ s.
2. Distance is delay × speed of light (299,792,458 m/s): about 710 km, 884 km, and 1,034 km.
3. Draw the three circles on the map. They meet at Prague.
4. Students write their name and the solution on the paper, photograph it, and upload it to *In Class Activity: Where Am I* on Learning Suite.

Fifteen minutes. Circulate and check that they converted seconds to kilometers before drawing; the usual mistake is a circle in meters on a map scaled in kilometers.

## Thursday — GPS Field Collection and Importing the Class Data

**Hands-On Practice**{ .badge .badge-handson } · *Day 7*

### Topics

- Twenty minutes on campus collecting positions with your phone
- Importing the class points into QGIS from a CSV, assigning the CRS, and reprojecting to UTM
- Seeing GPS error as the scatter between students at the same site

### In-class activity

GPS Class Activity: enter three campus positions in the shared sheet and record the site names on Learning Suite. Record your completion on Learning Suite.

<div class="handson-cta" markdown="1">

**Hands-On Practice**{ .handson-cta__eyebrow }

**GPS Field Collection and Importing the Class Data**{ .handson-cta__title }

This session has its own step-by-step guide: what to have ready, a practice run to do beforehand, the 50-minute plan, the click-by-click QGIS walkthrough, the graded upload, and the snags that usually come up.

[Open the Week 4 hands-on guide →](../handson/week-04.md){ .handson-cta__button }

</div>
