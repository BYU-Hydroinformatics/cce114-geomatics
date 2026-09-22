# Week 4 — The Global Positioning System

**Due this week.** Quizzes and lab reports are due **Saturday at 11:59 pm**;
anything on another day says so.

| What | Details |
| --- | --- |
| Reading | GIS Fundamentals, Chapter 5 (GNSS and Coordinate Surveying) |
| Quiz 3 | [GPS, Part 1](../assignments/deliverables.md#reading-quizzes) — open book, on Learning Suite |
| Lab 3 | [GPS Data Collection and Importing Into QGIS](../assignments/lab-03/README.md) |

## Practice

Not graded, and nothing to hand in — open it on a phone or a laptop as often as you like.

- [How Does It Know Where You Are?](../quizzes/gps/index.html) — How a receiver turns a radio signal into a position, what the digits of a coordinate are worth, and where GPS error comes from.

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

<!-- tuesday-notes -->
*In the [Global Positioning System](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-06/gps-part-1.html) deck, "Warm-up: find Air Force One." The deck opens with the two activities and then gives the short GPS explanation.*

**Setup, before class.** Tape a printed photo of Air Force One somewhere in the room, not in plain sight. Mark three fixed points in the room as satellites 1, 2, and 3 and label them with sticky notes. In Clyde 234 the three used are the north projector, the south projector, and the camera lens at the front. Measure the straight-line distance from each satellite to the photo with a tape and type the three numbers into the slide (Fall 2026: 88, 175, and 167 inches; the 2021 room's were 169, 216, and 151). Re-measure whenever the room or the hiding place changes.

**Run.** Show the slide and call up two or three volunteers to do the measuring — string, a tape, or their arms — while the rest of the class calls out where the arcs cross. No clock; let it run as long as it takes. Whoever finds it says how. The point: three ranges from three known points fix a position. That is trilateration, and it is the whole GPS idea before the math.

*Same deck, "In-Class Activity" and "The answer: Prague"; the QGIS version by Harrison Stewart is in the Teaching folder under In class activities.*

**Setup.** Printed maps of Europe with a scale bar, one per student — print them beforehand rather than counting on a web map. Compasses or string.

**Run.**

1. The story: lost in Europe, three radio stations announce the time, each arrives late by the travel time. Amsterdam 2.37 × 10⁻³ s, Paris 2.95 × 10⁻³ s, London 3.45 × 10⁻³ s.
2. Distance is delay × speed of light (299,792,458 m/s): about 710 km, 884 km, and 1,034 km.
3. Draw the three circles on the map. They meet at Prague.
4. Students write their name and the solution on the paper, photograph it, and upload it to *In Class Activity: Where Am I* on Learning Suite.

Fifteen minutes. Circulate and check that they converted seconds to kilometers before drawing; the usual mistake is a circle in meters on a map scaled in kilometers.

## Thursday — Campus Field Trip

**Hands-On Practice**{ .badge .badge-handson } · *Day 7*

<div class="handson-cta" markdown="1">

**Hands-On Practice**{ .handson-cta__eyebrow }

**Campus Field Trip**{ .handson-cta__title }

This session has its own step-by-step guide: what you need, an overview, the click-by-click QGIS walkthrough, what to hand in, and the snags that usually come up.

[Open the Week 4 hands-on guide →](../handson/week-04.md){ .handson-cta__button }

</div>
