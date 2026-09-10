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
- `docs/schedule.md`: the 15-week overview table, linking to the weekly pages below
- `docs/weeks/week-NN.md`: 15 weekly lesson-plan pages (restructured 2026-09-09, see below), each with
  the Tuesday concepts session and the Thursday hands-on session together
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

**Thursday hands-on run sheets and Tuesday activities (2026-09-02, evening).** Originally built as
`docs/hands-on/`, one run sheet per Thursday for Weeks 2 to 12 (goal, prep checklist, 50-minute plan,
QGIS 3.44 walkthrough, the graded upload, common snags) plus `tuesday-activities.md`, collecting
Dr. Ames's lecture activities with their setup and the full metadata-melodrama script. On
2026-09-09 this content was folded into the Tuesday/Thursday sections of each `docs/weeks/week-NN.md`
page (see "Restructuring" below) — the `docs/hands-on/` tree no longer exists; the same content lives
under the `<!-- tuesday-notes -->` and `<!-- thursday-notes -->` markers on the relevant week pages.
`docs/assignments/web-mapping-with-ai.md` is the spec for the Web Mapping with AI Experience (kicked
off Week 11 Thursday). Structural decisions made with Dan that day: both GPS decks are given on
Tuesday of Week 4 and Thursday is field collection plus the CSV import; Week 11 became "Geoplanning
and Georeferencing" (Tuesday: georeference a pencil sketch of your neighborhood; Thursday: a real
scan with GCPs and residuals) because no georeferencing lecture or lab existed; the CCE 414 intro
moved to Tuesday of Week 14, followed by project work; final project presentations are Thursday of
Week 14 and Tuesday of Week 15. Graded in-class activities are one per class meeting, 5 points each;
new ones are First Map: Utah County (Week 2 Thu), DEM Profile (Week 6 Thu), Playing with Projections
(Week 8 Thu), AGRC Metadata (Week 9 Thu), and Georeference Your Neighborhood Sketch (Week 11 Tue).

**Restructuring to one page per week (2026-09-09).** The site originally spread each week across
three menus: `docs/lectures/day-NN.md` (Tuesday, generated), `docs/hands-on/week-NN.md` (Thursday,
hand-written), and `docs/hands-on/tuesday-activities.md` (a separate Tuesday-activity index) — three
places for the same 15 weeks, and a sidebar of about 90 links. At Dan's request this became one page
per week, `docs/weeks/week-NN.md`, so the nav is simply Week 1 through Week 15 under a **Schedule**
tab, and Learning Suite can point at one URL per week. Thursday sessions
now head with the run sheet's applied title (e.g. "First Map in QGIS") rather than the lecture
generator's academic title, since both sessions share a page. `tools/build_schedule.py` was rewritten
to emit `docs/weeks/week-NN.md` instead of one page per day; see rule 3 in `CLAUDE.md` for the two
marker names.

**Learning Suite links: done 2026-09-09.** The restructure broke every direct link on Learning
Suite. All 43 on the Schedule page (26 `lectures/day-NN`, 11 `hands-on/week-NN`, 6
`hands-on/tuesday-activities#...`) and 5 more inside In Class Activity descriptions on the
Assignments page now point at `weeks/week-NN` with the right Tuesday or Thursday anchor. Every
target and anchor was checked against the live site. Slide and lab links were unaffected. If the
week pages are ever retitled, those anchors go stale, because the `##` heading text is the slug.

**Top tabs and the schedule table (2026-09-10).** Even with one page per week the left sidebar was
still one 48-link column (Schedule, Assignments, Policies all expanded), with Assignments below the
fold on every page. `mkdocs.yml` now uses Material's `navigation.tabs` plus `navigation.indexes`
instead of `navigation.sections`: each top-level section is a tab across the top and the sidebar
shows only the active section; `assignments/README.md` is its section's own page (Material only
allows `index.md` or `README.md` there, so `schedule.md` stays a labeled "Overview" child to keep
its URL). The schedule table got its Tuesday and Thursday columns back, each cell linking to the
session heading on the week page (`weeks/week-NN.md#tuesday-...` / `#thursday-...`); the generator
computes those slugs with the same rule python-markdown uses, so they stay in step with the
headings. The generator's nav rewrite also now replaces the whole existing `- Schedule:` block and
fails loudly if it cannot find it (the previous pattern matched only the pre-restructure file, so a
rerun left the nav untouched).

**Data.** `docs/lectures/data/UtahCountyData.zip` (38 MB: county boundary, major roads, cellular
towers, DEM) is published for the Day 2 demo and Thursday sessions. Lab 4 ships a GeoPackage
fallback in its folder.

## How things are generated

Two files are the source of truth for structure; edit them rather than their outputs.

- **`tools/build_schedule.py`** holds the DAYS and WEEKS tables. Running
  `python3 tools/build_schedule.py` regenerates `docs/schedule.md`, all 15 `docs/weeks/week-NN.md`
  pages, and the Schedule section of `mkdocs.yml`. To add a slide deck to a day, add it to that
  day's `slides=` list and rerun. Hand-written text survives on a week page only below a
  `<!-- tuesday-notes -->` or `<!-- thursday-notes -->` marker (see rule 3 in `CLAUDE.md`).
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

- **Final exam day (resolved 2026-09-02):** the university slot for Fall 2026 is Thu Dec 17, 11:00 am to
  2:00 pm, 234 CB. The site now says finals week generically; Dec 8 is presentations part 2 and review.
  Learning Suite's Dec 8 entry, a new Dec 17 entry, and the Final Exam assignment date were updated the
  same night (see the session notes); re-check each semester.
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
- **Lab headings (Labs 5 to 11):** Labs 1 to 4 now use "Step by Step Instructions" with numbered,
  active-voice subsection headings and one continuous step sequence. Do the same for the other seven.
  Check for inbound anchor links before renaming a heading; Labs 1 to 4 had none.
- **Labs 3 and 4: done 2026-09-10.** Renumbered into one continuous step sequence each, semester
  dropped from both headers, Lab 4's deliverables and rubric restructured, four data corrections
  made (the largest: Lab 4 required ten culverts where only nine road crossings exist within a
  kilometer of the temple site), and **23 figures re-shot in QGIS 3.44 at 2x**. Re-running the
  figures later is four commands, and the scripts rebuild their own demo data from sources the labs
  cite:

  ```bash
  export PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
         PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
         GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal
  /Applications/QGIS.app/Contents/MacOS/python3.12 tools/lab0304_make_demo_data.py ~/lab34work
  ./tools/reshoot_lab0304.sh ~/lab34work        # needs the Mac in LIGHT appearance
  python3 -m mkdocs build --strict
  ```

  Two things control how light the figures come out. QGIS's own UI theme is handled by the script,
  which runs the in-app captures under a throwaway `--profile lab34shots` so they use the default
  light theme whatever the maintainer's profile is set to. The macOS session appearance is **not**
  scriptable and must be set to Light by hand; `reshoot_lab0304.sh` refuses to run in dark mode.
  `tools/lab0304-improvement-plan.md` has the capture-to-figure mapping and the short list of
  figures still made by hand (context menus, a tooltip, and Lab 4's two annotated aerial views).
- **Labs 5 and 6: done 2026-09-10.** Semester dropped from both headers, Lab 6's QGIS version
  pinned, both renumbered under active-voice step headings (Lab 5 runs 1 to 56, Lab 6 1 to 23), and
  **eleven Lab 5 figures re-shot in QGIS 3.44**. That clears the oldest item in
  `tools/image-improvements-handoff.md`: the two Lab 5 example layouts carried Dan's red
  strike-through markup ("Slope" struck out on the elevation layout, "DEM" on the slope layout) and
  are now clean exports. Lab 5 step 12 also promised a figure it never had; it has one now.

  Verified against live data rather than assumed: each DEM tile really is a 4,000 x 4,000 grid of
  5 m cells, so the lab's "roughly 96 million elevation values" across six tiles is right; the UGRC
  REST service really does carry 892 datasets, matching Lab 6's "nearly 900"; and the DEM reads
  about 1,330 m over Utah Lake against a published 1,368 m, so Lab 5's warning that the number will
  disagree now names the size of the gap.

  Rebuild and re-shoot with `tools/lab0506_make_demo_data.py` then `tools/qgis_lab0506_shots.py`
  (about 145 MB of downloads); the commands are printed at the end of the data builder. Same two
  appearance rules as Labs 3 and 4: the script's `--profile lab56shots` handles QGIS's own theme,
  and the Mac has to be in Light appearance by hand.

- **Labs 7 and 8: done 2026-09-10.** Semester dropped from both headers, both renumbered under
  active-voice step headings (Lab 7 runs 1 to 31, Lab 8 1 to 19), and **Lab 8 got its first
  figures**: five captures of the QGIS Metadata tabs its steps walk through. The lab used to say in
  its own text "There are also no QGIS screenshots for this lab yet". Script:
  `tools/qgis_lab08_metadata_shots.py`.

  Two corrections worth knowing about:

  - **Lab 7's five spoiler answers were Claude reconstructions**, flagged in
    `tools/image-improvements-handoff.md` for someone to check against Dan's Google Doc. They are
    now checked against Natural Earth country polygons measured in an equal-area projection.
    Four were right. One was not: it claimed India is "nearly four times" Greenland, where the real
    ratio is about 1.4. All five now carry the numbers, and the review markers are gone.
  - **Lab 8's metadata hints had drifted from the files students download.** The Utah County
    Boundaries XML no longer has a `metd` tag the Part 1 hint tells students to search for; it uses
    `pubdate` and `ModDate`. Question 1 told students that UGRC downloads no longer carry `ModDate`
    and to search `metd` instead, which is exactly backwards for Utah Buildings, where `ModDate` is
    2021-08-10 and there is no `metd`. Question 6 asserted the Major Lakes XML "has no contact
    section at all", which it does have. And question 4 expects Major Lakes and Roads to differ in
    CRS; both currently ship as Web Mercator, so the question now says that finding a match is a
    good answer too. Lab 8's Lehi transportation plan link was also a 404 and now points at the
    live PDF, with Lehi's Studies and Master Plans page named as the stable fallback.

- **Lab 4 culvert photos** (`anchored10`, `anchored11`, `anchored12`, `anchored14`) are 225 to 369 px
  wide. They are photographs, not QGIS captures, so no script replaces them; they need images Dan is
  happy to license.
- **Lab 2 (done 2026-09-09):** rebuilt end to end. All fifteen figures re-shot in QGIS 3.44 at 2x
  and eight steps that had no figure got one, descriptive alt text throughout, the rubric split into
  four rows, and three short written questions added. A run-through with live UGRC data also turned
  up four instruction bugs, now fixed: 55 of the 138 "airports" are heliports, eight municipalities
  (including Logan) have a population of 0, graduated legend labels default to four decimal places,
  and unchecking road categories does not remove them from a layout legend. The review and the
  method are in `tools/lab02-improvement-plan.md`; the capture scripts are
  `tools/qgis_lab02_dialog_shots.py`, `tools/qgis_lab02_window_shots.py`, and
  `tools/lab02_annotate.py`. **The same run-through is worth doing on Labs 3 to 11** — every one of
  those four bugs was invisible from reading the text.
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
