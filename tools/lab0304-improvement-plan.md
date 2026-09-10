# Labs 3 and 4: handoff for the screenshot re-shoot

*Updated 2026-09-10. The text, structure and data corrections for both labs are **done, committed
and live**. Only the figures remain, and they are blocked on one thing: the Mac has to be in Light
appearance. This file is written so a session on a different machine can finish the job without
anything from the machine the work started on.*

## Start here

Four commands on a Mac in **Light** appearance, with QGIS 3.44 LTR installed at
`/Applications/QGIS.app`:

```bash
git clone https://github.com/BYU-Hydroinformatics/cce114-geomatics.git && cd cce114-geomatics
export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
       PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
       GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal
/Applications/QGIS.app/Contents/MacOS/python3.12 tools/lab0304_make_demo_data.py ~/lab34work
./tools/reshoot_lab0304.sh ~/lab34work
```

That builds the demo data, captures every figure, annotates them, and writes each one straight into
`docs/assignments/lab-03/images/` or `lab-04/images/` under the filename the Markdown already
references. Then `python3 -m mkdocs build --strict`, read both pages, and commit.

`~/lab34work` must not be under `~/Desktop`, `~/Documents` or `~/Downloads` — QGIS cannot read or
write there on macOS. Anywhere else is fine.

## Why Light appearance, and why it is not automated

Qt takes its palette from the macOS session appearance. In dark mode every capture comes out dark,
which no Clyde 234 lab machine displays and which does not match Labs 1 and 2. There is no scripted
way around it, and all three obvious routes were tried and failed:

- forcing a light palette onto the native macOS style paints text fields as solid black boxes;
- `defaults write -g AppleInterfaceStyle` changes the stored preference but never reaches the
  running GUI session, even after `killall cfprefsd` and
  `notifyutil -p AppleInterfaceThemeChangedNotification`;
- the AppleScript route through System Events hangs on a one-time automation prompt that a person
  has to approve at the keyboard.

`reshoot_lab0304.sh` refuses to run in dark mode rather than producing a set nobody can use.

## What each script does

| Script | What |
| --- | --- |
| `tools/lab0304_make_demo_data.py` | Builds every demo layer from sources the labs themselves cite. Prints a self-check against each number the labs claim. |
| `tools/qgis_lab0304_dialog_shots.py` | Nine dialogs, from QGIS's bundled Python, no QGIS window. `--list` prints the shot names. |
| `tools/qgis_lab0304_window_shots.py` | Twelve main-window, canvas and Print Layout shots plus the toolbar icons, from inside QGIS via `--code`. `--list` prints the names. |
| `tools/lab0304_annotate.py` | Draws the red boxes from the widget rectangles the capture scripts save, caps width at 2000 px, writes to final filenames. |
| `tools/reshoot_lab0304.sh` | Runs all of the above in order. |
| `tools/lab0304-data/byu-campus.geojson` | The BYU main campus polygon, committed so the build does not depend on Overpass, which rate-limited and returned 504 during this work. |

The demo data is all derived, never invented: Lab 3's points are the five geocache coordinates Lab 3
publishes, converted to EPSG:26912; the campus polygon is the OpenStreetMap campus relation's main
outer way; Lab 4's waterways come from the SGID address printed in Lab 4; the temple footprint and
parking lot are rectangles at the announced site sized into Lab 4's own target ranges. The builder
prints each of these against the labs' stated figures so a mismatch is loud:

```
  campus area 1444296 m2 = 357 acres  (Lab 3 says about 1.4 million m2, ~350 acres)
  98 features (Lab 4 says 98)
  temple footprint 29708 sq ft (Lab 4 target 25,000-35,000)
  parking lot      69750 sq ft (Lab 4 target 60,000-80,000)
```

## Which capture becomes which figure

`tools/lab0304_annotate.py` holds this mapping in `TARGETS`; it is repeated here for a human. The
final names are the ones the Markdown already uses, so **no Markdown edits are needed** for these.

| Capture | Becomes |
| --- | --- |
| `lab3-delimited-text` | lab-03 `dsm-delimited-text.png` |
| `lab3-save-features-as` | lab-03 `anchored4.png` |
| `lab3-digitizing-toolbar` | lab-03 `digitizing-toolbar.png` |
| `lab3-feature-attributes` | lab-03 `feature-attributes.png` |
| `lab3-new-shapefile-dialog` | lab-03 `new-shapefile-dialog.png` |
| `lab3-campus-polygon` | lab-03 `anchored6.png` |
| `lab3-field-calculator` | lab-03 `anchored7.png` |
| `lab3-attribute-table` | lab-03 `anchored8.png` |
| `lab3-example-layout` | lab-03 `example-layout.png` |
| `lab3-icon-data-source-manager` / `-move-feature` / `-add-point-feature` / `-add-polygon-feature` / `-field-calculator` | lab-03 `image2.png` / `image3.png` / `image4.png` / `image5.png` / `image6.png` |
| `lab4-new-geopackage-point` | lab-04 `anchored3.png` |
| `lab4-new-geopackage-polygon` | lab-04 `anchored5.png` |
| `lab4-snapping-toolbar` | lab-04 `anchored6.png` |
| `lab4-temple-site` | lab-04 `anchored4.png` |
| `lab4-footprints` | lab-04 `image7.png` |
| `lab4-field-calculator` | lab-04 `image5.png` |
| `lab4-field-calculator-update` | lab-04 `image6.png` |
| `lab4-icon-toggle-editing` | lab-04 `image2.png` and `image3.png` |
| `lab4-icon-save-layer-edits` | lab-04 `image4.png` |

### Three judgment calls left open on purpose

1. **`lab3-icon-new-shapefile-layer` is not mapped.** The capture is a 66 px button; the existing
   `new-shapefile-button.png` is a wide toolbar strip whose alt text says "toolbar with the New
   Shapefile Layer button highlighted". Swapping one for the other would make the alt text wrong.
   Decide which the step wants, then either map it and reword the alt text, or re-shoot the strip.
2. **`lab4-data-source-manager` writes `dsm-vector-protocol.png`, which nothing references yet.**
   Lab 4 step 34, the HTTP protocol paste, has no figure at all and would be clearer with one. To
   use it, add this line under step 34:
   `![Data Source Manager Vector tab with Source Type set to Protocol HTTP(S) and the SGID address pasted into the URI box](images/dsm-vector-protocol.png)`
3. **Five figures cannot be scripted** and are left as they are: Lab 3's `select-transformation.png`
   and `panels-toolbars.png`, and Lab 4's `image1.png`, `anchored8.png` and `anchored16.png`. They
   are context menus, a menu bar and a tooltip, none of which QGIS will hand to a script. Capture
   them by hand with ⌘⇧4 (Retina gives 2x) if they are worth redoing.

## Already open before this work, still open

- **Lab 4's culvert photographs** (`anchored10`, `anchored11`, `anchored12`, `anchored14`) are 225
  to 369 px wide. They are photographs, not QGIS captures, so no script replaces them. They need
  images Dan is happy to license.
- **Labs 5 to 11** have had none of this treatment. Every problem worth finding in Labs 2, 3 and 4
  came out of running the steps, not reading them.

## What was already fixed, so nobody redoes it

Text, structure and data corrections for both labs are committed and live. In short: the semester is
gone from both headers; Lab 3 pins QGIS 3.44 LTR; both labs run one continuous 1-to-46 step sequence
under numbered active-voice headings, replacing Lab 3's two restarting Parts and Lab 4's four
restarting Phases; Lab 4's deliverables became a numbered list and its rubric four rows.

Four data corrections, all found by running the labs rather than reading them:

- **Lab 4 required ten culverts where nine exist.** Within a kilometre of the temple site the East
  Bench Canal crosses exactly nine roads, and nothing else in the download comes within two
  kilometres. Following the canal out to two kilometres gives seventeen. The lab now says so.
- Lab 4 now states what the SGID query returns (98 features, 57 streams and 41 canals) so a student
  can tell whether the long address pasted cleanly.
- Lab 3's campus-area guidance is grounded at 357 acres with a 330-to-380 range, and its rubric line
  now says "within 10% of about 350 acres" instead of within 10% of nothing in particular.
- A 314 px screenshot of a spreadsheet sitting directly above a Markdown table saying the same thing
  was removed from Lab 3.

Checked and deliberately left alone: Lab 3's coordinate converter is up, its published geocache
coordinates convert into the sanity band it tells students to expect, and Lab 4's claim that the
canal runs a few hundred metres west of the site is right at 384 m.
