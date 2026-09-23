# Week 4 Activity — Find Air Force One, and Where Am I?

**Lecture**{ .badge .badge-lecture } · *Day 6 · Tuesday of [Week 4 — The Global Positioning System](../weeks/week-04.md)*

**Graded in-class activity.** Find Air Force One, then Where Am I: trilaterate Prague on paper from three signal delays and upload a photo of your solution. Record your completion on Learning Suite.

<!-- notes -->
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
