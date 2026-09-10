# Labs 3 and 4: review, run-through findings, and the screenshot re-run

*Written 2026-09-10 by Claude, in session with Dan. Same treatment Lab 2 got: compare against
Lab 1, run the lab's own steps against live data, fix what is wrong, re-shoot the figures. The
text work is done and committed. The figures are blocked on one thing only, described at the
bottom.*

## What was wrong, and is now fixed

**Both labs.** The header said "Winter 2026"; the semester is gone, as it is in Lab 2. Lab 3 did
not pin the QGIS version; it now says 3.44 LTR like the others.

**Step numbering.** Lab 3 restarted its numbering at 1 in Part 2, so there were two step 1s
through two step 9s; it now runs 1 to 46 without a break, under active-voice headings ("Step 3:
Import Your GPS Data into QGIS"). Lab 4 was worse: four Phases, each restarting, giving three
step 1s. It now runs 1 to 46 under six numbered headings. The Part 1 and Part 2 framing survives
where it is genuinely useful — in Lab 3's deliverables, which really do split into group fieldwork
and individual QGIS work — but now says which step numbers each covers.

**Lab 4's deliverables and rubric.** Deliverables were bullets; they are a numbered list like every
other lab. The rubric was two cells holding nine criteria between them; it is four rows that a TA
can actually mark and a student can self-evaluate against.

**A redundant figure.** Lab 3 step 10 showed a 314-pixel-wide screenshot of a spreadsheet directly
above a Markdown table saying the same thing. The table stays, the screenshot is gone.

## What the run-through found

Checked on 2026-09-10 against live sources.

**Both labs' data sources still work.** The West Virginia coordinate converter Lab 3 sends students
to is up. Lab 4's SGID query returns exactly the 98 features the text claims — 57 streams and
rivers, 41 canals and ditches — including the Spanish Fork River, the East Bench Canal and the
Mapleton Lateral.

**Lab 3's numbers check out.** Converting the five geocache coordinates the lab publishes gives X
444,645 to 444,843 and Y 4,455,392 to 4,455,677, inside the sanity band the lab tells students to
expect. A polygon traced along the roads that ring main campus measures 1,444,296 square meters,
or **357 acres**, against the lab's "approximately 1.4 million" and "close to 350 acres". Both
correct. The lab now also gives a range, 330 to 380 acres, and says what being outside it means.

**Lab 4 asked for ten culverts where nine exist.** This is the real find. Within one kilometer of
the temple site the East Bench Canal crosses exactly **nine** roads, and no other waterway in the
download comes within two kilometers. A student who keeps the map tight on the site, which is what
the lab tells them to do, cannot reach the required ten. Following the canal out to about two
kilometers gives seventeen crossings. The lab now says so explicitly, and names the canal as the
one to work along.

**Lab 4's canal direction is right.** The text says the East Bench Canal "runs a few hundred meters
west of the temple site". Resolving the lab's own Google Maps link puts the site at 40.10699,
-111.61430, and the nearest point on the canal is 384 m to the west. Confirmed, not changed.

## The screenshots

Both capture scripts are written, debugged and committed, and they produce correct content:

- `tools/qgis_lab0304_dialog_shots.py` — nine dialogs (Save Features As, New Shapefile Layer,
  Feature Attributes, both Field Calculators, both New GeoPackage Layer dialogs, the attribute
  table). Verified: the GeoPackage dialog fills its Fields List with ID, Fixture_Type and Voltage
  and sets the CRS to EPSG:26912, exactly as Lab 4 step 6 describes.
- `tools/qgis_lab0304_window_shots.py` — eleven main-window, canvas and layout shots, plus the
  eight toolbar icons at 2x. Verified: all eight icons grab, the Data Source Manager and Snapping
  toolbar open, the aerial views land on the right coordinates.
- `tools/reshoot_lab0304.sh` — runs all of it in one command.

**They have not been shipped, because of the Mac's appearance setting.** Qt takes its palette from
the macOS session appearance. The Mac was in dark mode during this session, so every capture came
out dark — which no Clyde 234 lab machine displays and which would not match Labs 1 and 2. There
is no scripted way around it:

- forcing a light palette on the native macOS style renders text fields as solid black boxes;
- `defaults write -g AppleInterfaceStyle` changes the stored preference but does not reach the
  running GUI session, even after restarting `cfprefsd` and posting the theme-change notification;
- the AppleScript route through System Events needs a one-time automation prompt that has to be
  approved by a person at the keyboard.

Qt's Fusion style with a light palette does render cleanly and is a usable fallback, but its window
chrome does not match the rest of the course.

**To finish:** set System Settings > Appearance to Light, then

```bash
./tools/reshoot_lab0304.sh /path/to/work-dir
```

The work directory needs the demo data. All of it is derived from sources the labs themselves cite:

```bash
# Lab 4 waterways, straight from the address printed in the lab
curl -o sf.geojson "https://services1.arcgis.com/99lidPhWCzftIe9K/arcgis/rest/services/UtahStreamsNHD/FeatureServer/0/query?where=FType+IN+(336,460)&geometry=-111.68,40.06,-111.56,40.15&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=GNIS_Name,FType_Text,FCode_Text&f=geojson"
ogr2ogr -f GPKG -t_srs EPSG:26912 -nln Waterways SF_Waterways.gpkg sf.geojson
```

The Lab 3 demo points come from the five geocache coordinates the lab publishes, converted to
EPSG:26912; the campus polygon comes from the OpenStreetMap campus relation's main outer way; the
temple footprint and parking lot are rectangles at the announced site sized into the lab's own
target ranges (29,708 and 69,750 square feet). The exact scripts are in the session scratch
directory; regenerating them is a few lines of GDAL either way.

## Still open

- **Lab 4's culvert photographs** (`anchored10`, `anchored11`, `anchored12`, `anchored14`) are
  225 to 369 pixels wide. They are photographs, not QGIS captures, so no script can replace them.
  They need images Dan is happy to license.
- **Labs 5 to 11** have had none of this treatment. Every problem worth finding in Labs 2, 3 and 4
  came out of running the steps, not reading them.
