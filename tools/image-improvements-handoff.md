# Handoff: CCE 114 lab image improvements

*Written 2026-09-02 by Claude (session with Dan). Self-contained brief for a future
session. Start by reading this whole file; the memory index also points here.*

## Context

The CCE 114 Geomatics course lives at **BYU-Hydroinformatics/cce114-geomatics**
(local clone `~/Code/cce114-geomatics`), published via MkDocs + GitHub Actions to
https://byu-hydroinformatics.github.io/cce114-geomatics/ — every push to `main`
redeploys in ~1 minute. Labs are `docs/assignments/lab-NN/README.md` with images in
`docs/assignments/lab-NN/images/`. **The site is the student-facing source of truth;
the Google Docs are an archive** — image fixes go to the repo only.

What's already done (don't redo): all images recovered from Google-Drawing crops were
re-cropped at 2× from 300-dpi PDF renders (`tools/upscale_crops.py`, FFT-correlation
matching; Google PDF exports are nondeterministic so exact pixel matching fails).
**The remaining quality ceiling is the source material itself** — the fix now is
re-shooting screenshots, not more pipeline work.

## Environment facts

- Lab machines (Clyde 234) run **QGIS 3.44.11 LTR** — screenshots must show 3.44 UI.
- Dan's Mac has QGIS **4.2.1** at `/Applications/QGIS-final-4_2_1.app` (its
  `qgis_process`/GDAL work headless with
  `PROJ_LIB=.../Contents/Resources/qgis/proj GDAL_DATA=.../Contents/Resources/gdal`).
- So either install QGIS 3.44 LTR side-by-side on the Mac (macOS dmg from
  qgis.org/download — LTR and latest coexist fine) or capture on a lab machine.
- **Best workflow (found 2026-09-02): QGIS captures its own dialogs.** Run
  `tools/qgis_lab04_dialog_shots.py` from the QGIS Python console (instructions in the file
  header). It opens each dialog via `iface` actions, fills widgets by `objectName`, and saves
  `QWidget.grab()` PNGs at native Retina 2x — no screen-recording permission, no clicking,
  no focus stealing. Gotchas: QGIS cannot read/write under ~/Desktop, ~/Documents or
  ~/Downloads (macOS privacy), so keep scripts and output elsewhere; the profile
  `python/startup.py` hook did not fire in 3.44, so paste the `exec(...)` line into the
  console instead; `grab()` omits the macOS title bar. Lab 4's four dialog shots were
  redone this way.
- Fallback workflow for map-canvas shots: **Dan drives QGIS, Claude does everything around it** —
  tell him exactly what to set up on screen per shot (layers, zoom, dialog, which
  annotations), he screenshots (⌘⇧4/⌘⇧5; Retina gives 2× natively), drops files
  somewhere agreed, and Claude renames to the existing `images/` filenames (keep
  filenames — the markdown references don't change), verifies each with the Read
  tool, commits, pushes, checks the live page. Full GUI automation of QGIS was
  considered and is not worth the fiddle.
- Replacing a file in place is the whole update; alt text in the README should be
  checked/updated if the new shot differs meaningfully.

## Priority list (from the review/conversion agents' findings)

**Lab 4 — DONE 2026-09-02 for items 1–3** (`anchored5`, `anchored2`, `anchored3`,
`crs-dialog` re-shot from QGIS 3.44 at 2x; README wording updated: the dialog row is now
"File name" not "Database", field types are "Integer"/"Text", CRS left on Project CRS).
Remaining:
4. `anchored10–12, anchored14` are small culvert photos (~250 px, native resolution) —
   replace with better-resolution culvert photos (any source Dan likes) or leave.
5. Data for staging shots: `docs/assignments/lab-04/data/SF_Waterways.gpkg` (98
   waterways, EPSG:26912) is in the repo; the lab's own steps describe the rest.

**Lab 9:** the screenshots near "Retrieving the Shapefiles" show the NPS download
page from its shapefile era (dataset is now geodatabase-only; the *text* is already
fixed). Also `anchored9.png` has a content bug baked into the drawing: the red note
says "10km buffer" but the lab uses **5 km** — re-shoot or edit the annotation.

**Lab 5:** raster.utah.gov wizard screenshots predate the current UI (text already
updated: yellow Download button, "Step 2/3/4" panels — screenshots should match).
Also both example-layout images contain Dan's red markup annotations (struck
"Slope"/"DEM" labels) inside the drawings — re-export clean layouts.

**Lab 1–2 (lower priority):** UGRC website screenshots still match the live site's
labels (verified Aug 2026) but predate its current look; QGIS window chrome in older
shots shows pre-3.44 styling. Refresh opportunistically.

**While in the neighborhood (not images):** Lab 7 step 31's five spoiler answers are
Claude reconstructions (marked with an HTML comment) — Dan should compare with his
Google Doc's dropdown wording; nobody has yet.

## Verification loop

After replacing images: `git add -A && git commit && git push` (small separate
commands — the permission classifier sometimes blocks long compound git commands),
then `gh run watch` the pages.yml workflow and spot-check
`https://byu-hydroinformatics.github.io/cce114-geomatics/assignments/lab-NN/` plus a
direct image URL. Local preview if wanted: `pip install mkdocs-material
mkdocs-github-admonitions-plugin && mkdocs serve` from the repo root.

## Lecture deck follow-ups (added 2026-09-02, after converting Days 4-23)

Every deck under `slides/day-NN/` ends with a `<!-- Conversion notes -->` comment. The items
that need a person, collected from those notes:

**ArcGIS/ArcMap screenshots to re-shoot in QGIS 3.44** (keep the filenames; the markdown
references don't change):
- Day 4: `mc-major-cities-icon-map.jpg` (student layout made in ArcMap; a QGIS Print Layout example would replace it).
- Day 10: `ras-dem-3d-arcview.jpg` (ArcView 3D surface with streams; use a QGIS 3D view or slope/hillshade pair).
- Day 14: `crs-arcgis-transformation-dialog.png` (ArcMap datum transformation dialog; replace with Project Properties > CRS); also find a QGIS way to show Tissot indicatrices.
- Day 16: `md-qgis-metadata-panel.jpg` is QGIS but from a 2.x release; re-shoot Layer Properties > Metadata in 3.44.
- Day 18: `gp-attribute-table-arcmap.jpg`, `gp-select-by-query-arcmap.jpg`, `gp-select-by-query-sql.png`, `gp-select-by-location-arcmap.jpg`.
- Day 22: `ws-udot-routes-table.png`, `ws-select-i15.png`, `ws-model-builder.png` (attribute table, Select by Expression, Graphical Modeler).
- Day 23: `fp-example-map.jpg` (past student's ArcMap final map; a QGIS example would be better).
- Day 21: thirteen ArcGIS 10 screenshots are kept on purpose because the deck describes CCE 414; confirm which software CCE 414 uses now before deciding.

**Instructor confirmations left as TODO comments in the decks:** Day 7 Air Force One room
distances (re-measure for the actual classroom); Day 6 worked example keeps the source's
non-GPS-scale numbers with a sanity-check callout; Day 12 and Day 23 class sign-up/scavenger
sheet links (old Google links were dead); Day 4 poll answer key; Day 23 exam window; and the
"due Saturday" lines on every Before Next Class slide should match Learning Suite each semester.

**Not converted:** Day 20 Geoplanning (no source deck exists) and the Surveying decks (not in
the current schedule).
