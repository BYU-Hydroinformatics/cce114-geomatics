# CCE 114 Geomatics on GitHub: status and handoff

*Written 2026-09-02, at the end of the first full build-out day. For Dan Ames, Dr. Halgren, the
TAs, and any future Claude session. The short version: the course site is complete enough to
teach from for Fall 2026; what remains is polish, a few instructor confirmations, and the
per-semester date pass.*

## What this is

The course now lives in one GitHub repository, **BYU-Hydroinformatics/cce114-geomatics**, and is
published as a website at **https://byu-hydroinformatics.github.io/cce114-geomatics/**. Every push
to `main` rebuilds and redeploys the site in about a minute (GitHub Actions, `.github/workflows/pages.yml`).
The site is the student-facing source of truth. The Google Docs and PowerPoints in the Drive
folder (`ames-sync/Work/Teaching/CCE 114 Geomatics`) are now an archive; edits go to the repo only.

Learning Suite still holds what changes every semester: dates, quizzes, submissions, grades,
attendance, and TA contact details. The site deliberately links to Learning Suite for those rather
than repeating them.

## What is done

**Labs (done before this session).** All eleven lab assignments were converted from Google Docs
to Markdown with images, one folder per lab under `docs/assignments/`. Lab 4's screenshots that
contradicted the text were re-shot in QGIS 3.44 today; the other labs' images were upscaled from
the original documents and are readable, though older QGIS versions show in some of them.

**Course structure (today).** The Fall 2026 Learning Suite syllabus was turned into
semester-agnostic pages:

- `docs/course.md`: description, instructors, prerequisites, textbook, learning outcomes, how the course works
- `docs/schedule.md`: 15 weeks, each with a Tuesday concepts day and a Thursday hands-on day, plus what is due
- `docs/lectures/day-NN.md`: 29 lecture-day pages with topics, slides, materials, activities, reading, and due items
- `docs/policies/`: grading, attendance and participation, exams, university policies, plus the existing AI policy
- `docs/assignments/deliverables.md` (quizzes, in-class activities, experiences) and `docs/assignments/final-project.md`

Everything is expressed in week numbers and weekdays, never calendar dates, so the same site
serves Fall (September to December) and Winter (January to April). The weekly rhythm is
**Tuesday: concepts lecture (Dr. Ames), Thursday: demo and hands-on in QGIS (Dr. Halgren)**;
Week 1 meets only on Thursday.

**Lecture slides (today).** Sixteen Marp web slide decks covering fourteen class days, built
from the PowerPoints, each with speaker notes (press P in the deck), Today's Goals, a Thursday
preview, and Before Next Class slides, and with software wording updated from ArcGIS to QGIS:

| Day | Deck | Day | Deck |
| --- | --- | --- | --- |
| 1 | Course Introduction; Introduction to GIS | 14 | Geodesy, Projections, and Coordinate Systems |
| 2 | GIS Data Models & File Formats | 16 | Spatial Metadata |
| 4 | Maps, Symbology, and Cartography | 18 | Introduction to Geoprocessing |
| 6 | GPS, Part 1 | 21 | Introduction to CCE 414 |
| 7 | GPS, Part 2 | 22 | Project Site Selection (Walmart) |
| 8 | Working with Vector Data | 23 | Final Mapping Project; Concepts Review |
| 10 | Raster Analysis and Map Algebra | | |
| 12 | Finding Spatial Data and Web Services | | |

All ArcMap screenshots in those decks were replaced with QGIS 3.44 captures today, except in the
Day 21 deck, which describes CCE 414 and keeps its ArcGIS 10 screenshots on purpose.

**Thursday hands-on run sheets and Tuesday activities (2026-09-02, evening).** `docs/hands-on/` holds one
run sheet per Thursday for Weeks 2 to 12 (goal, prep checklist, 50-minute plan, QGIS 3.44 walkthrough,
the graded upload, common snags) plus `tuesday-activities.md`, which collects Dr. Ames's lecture
activities with their setup and the full metadata-melodrama script. `docs/assignments/web-mapping-with-ai.md`
is the spec for the Web Mapping with AI Experience (kicked off Week 11 Thursday). Structural decisions
made with Dan that day: both GPS decks are given on Tuesday of Week 4 and Thursday is field collection
plus the CSV import; Week 11 became "Geoplanning and Georeferencing" (Tuesday: georeference a pencil sketch
of your neighborhood; Thursday: a real scan with GCPs and residuals) because no georeferencing lecture or
lab existed; the CCE 414 intro moved to Tuesday of Week 14, followed by project work; final project
presentations are Thursday of Week 14 and Tuesday of Week 15. Thursday day pages link their run sheet
through the `handson=` key in `tools/build_schedule.py`. Graded in-class activities are one per class
meeting, 5 points each; new ones are First Map: Utah County (Week 2 Thu), DEM Profile (Week 6 Thu),
Playing with Projections (Week 8 Thu), AGRC Metadata (Week 9 Thu), and Georeference Your Neighborhood
Sketch (Week 11 Tue).

**Data.** `docs/lectures/data/UtahCountyData.zip` (38 MB: county boundary, major roads, cellular
towers, DEM) is published for the Day 2 demo and Thursday sessions. Lab 4 ships a GeoPackage
fallback in its folder.

## How things are generated

Two files are the source of truth for structure; edit them rather than their outputs.

- **`tools/build_schedule.py`** holds the DAYS and WEEKS tables. Running
  `python3 tools/build_schedule.py` regenerates `docs/schedule.md`, `docs/lectures/README.md`, all
  29 day pages, and the Lectures section of `mkdocs.yml`. To add a slide deck to a day, add it to
  that day's `slides=` list and rerun. Hand-written text survives on a day page only below a
  `<!-- notes -->` marker.
- **`mkdocs.yml`** holds the rest of the navigation (labs, policies, course pages).

Slide decks are plain Markdown in `slides/day-NN/`, one folder per day with an `images/`
subfolder, built by marp-cli in the workflow. `slides/theme/cce114.css` is the shared theme.

## How to work on it

- **Local preview of the site:** `pip install mkdocs-material mkdocs-github-admonitions-plugin`
  then `mkdocs serve`. Note that `mkdocs serve` mounts the site under `/cce114-geomatics/`.
- **Local preview of a deck:** `npx -y @marp-team/marp-cli@latest --no-stdin --theme slides/theme/cce114.css --html slides/day-NN/deck.md -o /tmp/deck.html`.
  For PNG renders add `--allow-local-files --images png`. Without `--no-stdin` marp hangs.
- **Converting another PowerPoint:** follow `tools/slide-conversion-guide.md`, using
  `tools/pptx_extract.py` to dump text, notes, media, and contact sheets. Today's decks were each
  produced by a Claude sub-agent following that guide in about ten minutes.
- **Screenshots from QGIS:** two in-app drivers show the pattern. `tools/qgis_lab04_dialog_shots.py`
  captures dialogs; `tools/qgis_reshoot_screens.py` also builds Print Layouts, a terrain pair, and
  a Model Designer view. Paste the `exec(...)` line into the QGIS Python console. Captures are
  native 2x and need no screen-recording permission. QGIS cannot read or write under `~/Desktop`,
  `~/Documents`, or `~/Downloads` on macOS, so keep working folders elsewhere.
- **Git:** the repo identity is set locally (Dan Ames, dpames@gmail.com). Small separate git
  commands work best with the Claude permission classifier.

## Each semester

1. Update dates on Learning Suite (the site has none).
2. Read `docs/schedule.md` against the Learning Suite calendar and fix any week where a
   holiday moves a session; Week 13 and Week 15 absorb the usual ones.
3. Check every deck's Before Next Class slide reads correctly for the current lab and quiz.
4. Update TA information on Learning Suite; the site does not list TAs.
5. If QGIS LTR moves past 3.44 on the lab machines, re-shoot dialog screenshots with the
   drivers above.

## What still needs a person

Collected from the conversion notes at the end of each deck (search for `Conversion notes` and
`TODO`) and from `tools/image-improvements-handoff.md`:

- **Final exam day (open, asked 2026-09-02):** Learning Suite lists the final exam in class on Tue Dec 8,
  11:00 to 2:00, and Dec 8 now also carries remaining final project presentations. Confirm the
  university-scheduled final slot for a TTh 1:00 pm class (finals run Dec 12 to 17), then fix the LS
  schedule entry, the Final Exam assignment date, and Day 28 in `tools/build_schedule.py`.
- **Day 21:** confirm what software CCE 414 uses now and whether its lab list is current; then
  decide whether to keep the ArcGIS 10 screenshots.
- **Day 7:** the Air Force One activity distances are from the 2021 classroom; re-measure.
- **Day 6:** the worked signal-delay example keeps the source's numbers, which are not GPS-scale;
  a sanity-check callout was added. Decide whether to change the example.
- **Day 12 and Day 23:** class sign-up and scavenger-hunt Google links were dead and are marked
  TODO; create new sheets if you want them back.
- **Day 4:** the two-part "which elements are required" poll has no answer key in the source.
- **Day 20 (Geoplanning):** no source deck exists, so there are no slides.
- **Surveying:** three archived Surveying decks are not in the current schedule and were not converted.
- **Quiz readings** on the deliverables page cite 6th-edition page ranges; the required text is
  now the 7th edition, and the mapping is noted as pending.
- **Final project:** the site page is a placeholder that points to the Mapping Term Project
  document on Learning Suite; converting that document into the page is the natural next step.
- **Lab images:** Labs 5 and 9 have known content issues in old screenshots (raster.utah.gov
  wizard, a 10 km vs 5 km annotation); see `tools/image-improvements-handoff.md`.
- **Repository size:** the repo is about 190 MB because of images and the data zip. Fine for now;
  further datasets should go to GitHub Releases or Git LFS.

## Where the source material is

- Drive folder: `ames-sync/Work/Teaching/CCE 114 Geomatics/` with `Lectures/Archived/` (the
  PowerPoints), `Lectures/Day 1/` and `Day 2/` (the newest decks), `Learning Suite Syllabus/`
  (the Fall 2026 syllabus PDF), and `Assignments/` (lab Google Docs and data).
- UGRC data used for the QGIS example maps: county boundaries, cities and towns, municipal
  boundaries, and PreK-12 schools, fetched from `https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services`
  as GeoJSON (commands in `tools/image-improvements-handoff.md`).
