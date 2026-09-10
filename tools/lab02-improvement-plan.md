# Lab 2 review and improvement plan

*Written 2026-09-09 by Claude, in session with Dan. Compares Lab 2 against Lab 1 and against a
full run-through of Lab 2's own steps in QGIS 3.44.13 LTR with live UGRC data downloaded the same
day. Every claim below marked "verified" was observed in that run; the log is reproduced at the
end of this file.*

## The short version

Lab 2 is pedagogically sound and its data still works, but it is the least finished lab in the
course. It carries the fewest instructional screenshots per step of any lab, it is the only lab
with placeholder alt text, its rubric is a single 30-point cell, and it has no written component
at all. The run-through also surfaced four things in the instructions that are wrong or missing
against today's data and today's QGIS.

Nothing here is a blocker for teaching it. The work splits into a two-hour text pass and a
half-day screenshot pass.

## Part 1: How Lab 2 differs from Lab 1

### Structure

| | Lab 1 | Lab 2 |
| --- | --- | --- |
| Instructions heading | "Step by Step Instructions" | "Instructions" |
| Subsection headings | "Step 1: Download Data from UGRC", numbered and active-voice | "Data and Map Setup", "Point Symbology", topic nouns |
| Header block | title, course, semester, italic byline | same plus a stray "Brigham Young University" line, byline not italic |
| Background figures | numbered and captioned ("Figure 1.", "Figure 2.") | no figure numbers, no captions |
| QGIS version | pinned: "Long Term Version 3.44 (LTR)" | vague: "the latest Long Term Version" |
| Rubric | three rows, each with its own point pool | one row worth all 30 points, eight criteria crammed into one cell |
| Deliverables | screenshot, three written questions, an article write-up | map layout and a city name only |
| Steps | 34 | 64 |

The numbered-step rewrite Lab 1 got on 2026-09-08 has not reached Lab 2. `HANDOFF.md` already
tracks that as an open item for Labs 2 to 11; Lab 2 is the natural first one to do, because it is
the next lab students meet.

There are no inbound anchor links to any Lab 2 heading, so headings can be renamed freely. Only
plain page links exist, in `mkdocs.yml`, `docs/schedule.md`, `docs/assignments/README.md`,
`docs/index.md`, `docs/weeks/week-03.md`, and the Day 4 deck.

### Images

Lab 2 has fifteen image references, but eight of them are 24-to-34-pixel toolbar icons and one is
the shared title hero. That leaves **seven instructional screenshots for sixty-four steps** — the
lowest density in the course, and four of the seven are under 630 pixels wide.

| Lab | Steps | Images | Placeholder alt text |
| --- | --- | --- | --- |
| Lab 1 | 34 | 10 | 0 |
| **Lab 2** | **64** | **15** | **11** |
| Lab 3 | 53 | 22 | 0 |
| Lab 4 | 45 | 27 | 0 |
| Lab 5 | 60 | 22 | 0 |

Lab 2 is also **the only lab in the course still using placeholder alt text** — eleven references
read `![image1]`, `![image2]`, `![anchored1]` and so on. Every other lab was given descriptive alt
text; Lab 2 was missed.

Current sizes:

| File | Pixels | What it shows | Verdict |
| --- | --- | --- | --- |
| `image1.png` | 243 × 120 | Layers panel with four layers | too small, and layer names disagree with the text |
| `image2.png` | 625 × 467 | Full window after symbology | panel text illegible; pre-3.44 chrome |
| `image3.png` | 627 × 473 | Full window after labels | same |
| `image11.png` | 597 × 454 | The finished PDF | same, plus content problems below |
| `anchored1.png` | 1860 × 1400 | Layout with neatline, Items panel | upscaled, soft; keeps its pink callout |
| `anchored2.png` | 1055 × 780 | Legend Item Properties | smallest of the three; keeps red boxes and two red notes |
| `anchored3.png` | 2140 × 1480 | Title label Item Properties | best of the set; keeps two red arrow callouts |
| `image4`–`image10` | 24–34 px | Toolbar icons | 1×, from an older QGIS |

Steps with no screenshot at all, where Lab 1 would have one: the CRS dialog (3–4), the point
symbol layer stack and SVG marker (11–14), the whole categorized-roads sequence (17–21), the whole
graduated-population sequence (23–28), Layer Rendering opacity (28), the Labels tab and buffer
(30–33), Show Grid (37), and the north arrow and scale bar properties (46–48).

Three content problems are baked into existing images rather than the text:

1. `image11.png` and `anchored3.png` both show the title **"Title Text - An interesting title"** —
   which the lab's own Important Points section names as exactly what not to do — over the byline
   "Dr. Dan Ames" and the date 06/24/24. The example contradicts the instruction.
2. `anchored2.png` shows a legend with **ten population classes**, while step 26 tells students to
   set Classes to 5.
3. `image1.png` shows layers named Municipalities, Roads and AirportLocations, while the
   surrounding steps say `municipal_boundaries`, `roads` and `airport_locations`. There is a NOTE
   covering this, but the screenshot could simply match the steps instead.

### Level of effort

Lab 2 asks for roughly twice the clicking of Lab 1 (64 steps against 34, plus an entire print
layout) for the same 30 points, and unlike every other lab it asks for **no writing at all**. A
student can finish it without articulating a single idea. Because the rubric is one undivided
cell, a TA also cannot award partial credit for understanding, and a student self-evaluating has
to hold eight criteria against one number.

## Part 2: What the run-through found

Downloaded fresh on 2026-09-09 from the UGRC open data portal and loaded into QGIS 3.44.13 LTR.
The lab's whole sequence — CRS, three layers, three kinds of symbology, labels, print layout,
PDF export — completes with no errors. Field names in the instructions are all still correct.

Verified as still true:

- `CARTOCODE` exists on Roads and is a **text** field, so Classify lists 1, 10, 11 … 18, 2, 3 —
  exactly as step 19 warns.
- The shapefile download truncates `POPLASTESTIMATE` to **`POPLASTEST`**, exactly as step 24's
  parenthetical warns. `NAME` is present and untruncated.
- Utah Roads is genuinely large: the shapefile zip is 115 MB and unzips to about 960 MB across
  413,311 features. The step 6 warning is well earned.
- The airport link in step 7 still resolves, and the airports dataset is 138 points.
- A valid answer to the problem statement exists, and comfortably. Ten municipalities contain an
  airport, have a cartocode 1–5 highway crossing them, and have a population under 3,000 —
  Duchesne, Fillmore, Wendover, Delta, Parowan, Junction, Bluff, Dutch John, Fairfield and
  Toquerville among them.

Five problems found:

**1. Fifty-five of the 138 "airports" are heliports.** The dataset's `LAN_FA_TY` field splits into
83 AIRPORT and 55 HELIPORT. Most of the heliports are hospital pads — Timpanogos Regional,
Alta View, McKay-Dee — and one is a television station. A student can satisfy "there must be an
airport within the city limits" with a hospital helipad and never know. This is worth turning into
a teaching moment rather than a footnote: the lab already claims "use symbology to represent data
attributes" as a learning objective, and categorizing airports on `LAN_FA_TY` serves that
objective better than the current free-choice SVG marker does.

**2. Eight municipalities have a population of zero, and one of them is Logan.** `POPLASTEST` is 0
for Plain City, Spring City, Erda, Lake Point, Magna City, Logan, Ogden Valley City and Spring
Lake. Logan is a city of roughly fifty thousand with an airport and highways through it. Under the
lab's graduated symbology it lands in the lowest, "smallest town" class and looks like a perfect
answer. This is the single most likely way for a diligent student to get the wrong answer.

**3. Graduated legend labels default to four decimal places.** Straight out of QGIS 3.44 the class
labels read `0.0000 - 357.0000` and `16502.0000 - 204657.0000`. Dan's own example screenshot shows
clean integers, so he fixed the precision and it never made it into the written steps. The rubric
asks for a professional presentation; the instructions should say where the precision setting is.

**4. Unchecking road categories 6–18 does not remove them from the legend.** Verified: with the
layout legend on its default auto-update, the roads entry lists all eighteen categories, including
the hidden ones, plus five separate rows all reading "Highway" from step 21's renaming. Step 43
tells students to remove the basemap from the legend and nothing else, so the intended result is
not reachable by following the steps as written. Two fixes were tested and both work:

   - **Delete** categories 6–18 with the red minus rather than unchecking them, and
   - select categories 1–5 and use **Merge Categories**, which yields exactly one legend row
     reading "Highway". Verified: the merged category renders precisely the cartocode 1–5
     features and the legend shows one row.

**5. Step 35's colour advice no longer matches the data.** The step says to look for "one of the
two lower population categories (one of the greens, in this example)". With current populations
and five quantile classes the breaks fall at 357, 892, 3,229 and 16,502, so Duchesne at 1,623 and
Fillmore at 2,643 sit in the **middle** class, not the lowest two. The advice should describe the
population range to look for, not the colour, which depends on a ramp the student chose.

## Part 3: The plan

### A. Text pass (about two hours, no QGIS needed)

1. Renumber the instruction headings the way Lab 1 was renumbered: "Step by Step Instructions"
   with "Step 1: Set Up the Project and Download Data", "Step 2: Symbolize the Airports", and so
   on. No inbound anchors to break.
2. Fix the header block: drop the stray "Brigham Young University" line, italicise the byline to
   match Labs 1, 3 and 4.
3. Pin the QGIS version to "Long Term Version 3.44 (LTR)" as Lab 1 does.
4. Give every image descriptive alt text. Lab 2 is the last lab still on placeholders.
5. Number and caption the background figures, as Lab 1 does.
6. Split the rubric into rows so each criterion carries its own points, mirroring Lab 1's shape.
7. Add a short written component — two or three questions worth roughly 8 of the 30 points, with
   the rubric rebalanced. Candidates that fall straight out of what the lab already does: why
   EPSG:26912 rather than the default for a Utah map; what graduated symbology communicates that
   categorized cannot; why a legend is expected to be exhaustive.
8. Fold step 7 into step 6. Utah Airports is now browsable in the SGID Transportation category at
   `gis.utah.gov/products/sgid/transportation/airports`, which points at the same dataset on the
   main portal, so students no longer need the separate emergency-management hub link.
9. Add the four corrections from the run-through: the heliport caveat, the zero-population caveat
   with Logan named, the legend-label precision setting, and delete-and-merge instead of uncheck
   for the road categories.
10. Reword step 35 to describe a population range rather than "one of the greens".

### B. Screenshot pass (about half a day, QGIS 3.44.13 is installed and the data is downloaded)

Follow the pattern already proven in this repo: a standalone script driving QGIS's bundled Python,
grabbing dialogs at native 2× with `QWidget.grab()`, red annotation boxes added afterwards with
PIL. `tools/qgis_lab01_symbology_shot.py` is the working model. Keep every existing filename so no
Markdown reference changes, except where a new step needs a new file.

Replace, at 2× and in 3.44 chrome:

| File | New content |
| --- | --- |
| `image1.png` | Layers panel at a readable size, layer names matching the steps |
| `image2.png` | Full window after symbology |
| `image3.png` | Full window after labels |
| `image11.png` | The finished PDF, with a **descriptive** title, a generic student byline and no stale date |
| `anchored1.png` | Layout with neatline and Items panel; re-add the pink callout |
| `anchored2.png` | Legend Item Properties, showing **five** classes; re-add the red boxes and both notes |
| `anchored3.png` | Title label Item Properties; re-add both red arrow callouts |
| `image4`–`image10` | The seven toolbar icons re-grabbed at 2× from 3.44 |

Add, all currently missing:

- Project CRS dialog with 26912 filtered and NAD83 / UTM zone 12N selected (steps 3–4)
- Airport symbology with the two-layer symbol stack and the SVG marker browser (steps 11–14)
- Roads symbology after Classify, showing the 1, 10, 11 … ordering (steps 17–19)
- Roads symbology after delete-and-merge, one row reading "Highway" (steps 20–21)
- Municipalities graduated on POPLASTEST, five classes, with the label-precision control visible
  (steps 23–27)
- Layer Rendering expanded with the opacity slider (step 28)
- Labels tab: Single Labels on NAME with Draw text buffer checked (steps 30–33)
- North arrow and scale bar Item Properties (steps 46–48)

One risk worth naming: the full-window map shots need the Google Satellite Hybrid XYZ basemap, so
tiles must load during the capture. If headless tile loading proves unreliable, fall back to the
documented workflow where Dan drives QGIS and Claude does everything else.

### C. Decision Dan needs to make

**The semester line.** Lab 2's header reads "Winter 2026" — but so does the header of **all eleven
labs**, so this is a course-wide edit, not a Lab 2 one. The rest of the site is deliberately
semester-agnostic: `HANDOFF.md` records that everything is expressed in week numbers and weekdays
"so the same site serves Fall and Winter". The lab headers are the one place that breaks the rule.
Recommendation: **drop the semester from all eleven lab headers** and keep the instructor line, so
the labs stop going stale every January. The alternative is a find-and-replace to "Fall 2026" and
the same chore every semester.

---

## Appendix: run-through log

QGIS 3.44.13 LTR, 2026-09-09, live UGRC downloads.

```
STEP 3-4 CRS valid: True | NAD83 / UTM zone 12N
STEP 8 layer Municipalities valid True n 261 geom Polygon
STEP 8 layer Roads valid True n 413311 geom Line
STEP 8 layer AirportLocations valid True n 138 geom Point
STEP 18 CARTOCODE field index: 1 type: String
STEP 19 Classify -> 18 categories, list order: ['1','10','11','12','13','14','15','16','17','18','2','3','4','5','6','7','8','9']
STEP 24 population field present: POPLASTEST
STEP 25-27 quantile breaks (5 classes):
             0 - 357
           357 - 892
           892 - 3229
          3229 - 16502
         16502 - 204657
STEP 28 layer opacity: 0.45
STEP 31-33 labels on: True field: NAME buffer: True
CHECK municipalities with POPLASTEST = 0: ['Plain City','Spring City','Erda','Lake Point','Magna City','Logan','Ogden Valley City','Spring Lake']
CHECK airport points: total 138 HELIPORT 55 AIRPORT 83
STEP 36 default page: 297 x 210 mm
STEP 55-57 PDF export result: 0 (success), 249675 bytes

default graduated label precision: 4  ->  '0.0000 - 357.0000'
legend with categories 6-18 unchecked still lists: Highway, 10, 11, 12, 13, 14, 15, 16, 17, 18,
    Highway, Highway, Highway, Highway, 6, 7, 8, 9
after Merge Categories on 1-5: legend lists exactly one row, 'Highway'
```

Towns satisfying all three criteria (airport point inside the boundary, a cartocode 1–5 highway
crossing it, population under 3,000):

```
     pop  city            highway segments  airport
     149  Dutch John              8         DUTCH JOHN
     156  Fairfield              12         WEST DESERT AIRPARK
     211  Junction               31         JUNCTION
     243  Bluff                  37         BLUFF
    1135  Wendover               26         WENDOVER
    1623  Duchesne               28         DUCHESNE MUNI
    1960  Toquerville            17         DIAMOND 'G' RANCH
    2643  Fillmore               67         FILLMORE MUNI
```

**Gotcha for whoever scripts the captures:** driving QGIS with `--code` and quitting via
`iface.actionExit()` pops the "Do you want to save?" dialog and hangs the run unless the project
has just been written to disk. Write the project, or set the dirty flag false inside the timer
callback immediately before exiting.
