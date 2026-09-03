# Working in this repository

This is the course site for **CCE 114 Geomatics** at BYU (Dr. Dan Ames and Dr. James Halgren),
published to https://byu-hydroinformatics.github.io/cce114-geomatics/. Every push to `main`
rebuilds the MkDocs site and every Marp slide deck and redeploys in about a minute.

## What this repo is for

> [!IMPORTANT]
> **The site is the student-facing source of truth. The Google Docs are an archive.**
> Corrections — text, images, links — go into this repository. Do not "fix" a lab by editing the
> Google Doc and expecting it to reach students; it will not.

The course used to be distributed as Google Docs and PowerPoint attachments. It now lives here as
Markdown and web slides, so material is linkable, diffable, and reviewable, and a correction ships
in one commit.

## Current state

Unlike the sibling repo, this migration is largely **done** — the site is complete enough to teach
from. All 11 labs are migrated, 29 lecture-day pages exist, 16 Marp decks cover 14 class days, and
the schedule and policy pages are written.

Two status documents, and you should read the relevant one before starting:

- [`HANDOFF.md`](HANDOFF.md) — **read this first.** Overall status of the course site, the
  generators, the per-semester checklist, and the open items awaiting an instructor decision.
- [`tools/image-improvements-handoff.md`](tools/image-improvements-handoff.md) — read before
  touching any image. It records what has already been done (do not redo it), the priority list,
  and the capture workflows that were found to work.

## Hard rules

1. **This course uses QGIS, not ArcGIS.** The sibling repo
   [ce414-gis-applications](https://github.com/BYU-Hydroinformatics/ce414-gis-applications) is the
   applications course and uses ArcGIS Pro. Do not carry its wording or screenshots across.
2. **Screenshots must show QGIS 3.44 LTR** — that is what the Clyde 234 lab machines run. Dan's Mac
   also has QGIS 4.2.1; captures from 4.2.1 will not match what students see. Check the version
   before you shoot.
3. **`tools/build_schedule.py` generates four things.** It rewrites `docs/schedule.md`,
   `docs/lectures/README.md`, every `docs/lectures/day-NN.md`, and the Lectures section of
   `mkdocs.yml`. **Never hand-edit those files** — edit the `DAYS` and `WEEKS` tables in the script
   and re-run it. Hand-written notes survive only *below* a `<!-- notes -->` marker in a day page;
   everything above it is regenerated and your edit will vanish.
4. **Never fabricate a screenshot.** Captures come from a real QGIS session. If an image is needed
   and does not exist, leave a `<!-- TODO -->` and say so in your report.
5. **Never invent a field name, tool setting, coordinate system, or data figure.** If you cannot
   verify it in QGIS, write it as something to verify rather than as fact.
6. **Do not reproduce copyrighted material** — song lyrics, long textbook passages — even when a
   source slide has them. Keep the reference, describe it in a line.
7. **Never name a professor when pointing at the other class day.** Instructors change between
   semesters. Write "Thursday: hands-on in QGIS", never "Thursday with Dr. X." The title-slide
   byline is the one place names belong.
8. **American English throughout** — meters, kilometers, center, color, catalog, gray. Journal and
   product names keep their own spelling.
9. **Nearly every slide carries a graphic**, section-divider (`lead`) slides excepted. If a slide
   has none, generate one with the OpenAI image skill and save it in the deck's `images/` folder.
   Do not add decoration for its own sake.

Rules 7 to 9 come from `tools/slide-conversion-guide.md`, which is the authority when writing or
converting a deck. Read it before you touch slide content.

## How screenshots get made

Two workflows, both documented in full in `tools/image-improvements-handoff.md`:

- **QGIS captures itself.** Two scripts run from the QGIS Python console and save PNGs at native
  Retina 2x, with no screen-recording permission, no clicking, and no focus stealing:
  `tools/qgis_lab04_dialog_shots.py` for the Lab 4 dialogs, and `tools/qgis_reshoot_screens.py`
  for the lecture-deck screenshots that used to be ArcMap captures (attribute tables, Select by
  Expression, Select by Location, Layer Properties, Model Designer, hillshade/slope, and Print
  Layout maps). Note QGIS cannot read or write under `~/Desktop`, `~/Documents` or `~/Downloads`
  on macOS, so keep scripts and output elsewhere.
- **Map canvas: Dan drives, you do everything else.** Tell him exactly what to put on screen per
  shot — layers, zoom, dialog, annotations. He captures (⌘⇧4 gives 2× on Retina) and drops the
  files somewhere agreed; you rename them to the **existing** `images/` filenames so the Markdown
  references do not change, verify each one by reading it, then commit and check the live page.

Full GUI automation of QGIS was evaluated and judged not worth the fiddle. Don't re-litigate it.

## Layout

| Path | What |
| --- | --- |
| `docs/assignments/lab-NN/` | One folder per lab: `README.md` + `images/` |
| `docs/lectures/` | One page per class day — **generated**, see rule 3 |
| `docs/policies/` | Grading, attendance, exams, AI use, university policies |
| `slides/day-NN/` | Marp deck source + its own `images/` |
| `slides/theme/cce114.css` | The deck theme. Do not edit it for a one-off; use inline styles |
| `tools/` | Conversion pipeline and the image-improvements handoff |

## How to build and check

```bash
pip install mkdocs-material mkdocs-github-admonitions-plugin
mkdocs build --strict          # must pass; --strict catches broken nav and links
mkdocs serve                   # local preview at :8000
```

A deck:

```bash
npx -y @marp-team/marp-cli@latest --no-stdin --theme slides/theme/cce114.css --html \
  slides/day-NN/<slug>.md -o /tmp/check.html
```

`--no-stdin` matters — without it marp hangs waiting on stdin. To render slides as images for
visual QA add `--allow-local-files --images png`; without `--allow-local-files` every image
renders as a broken icon.

**Always look at what you produced.** Render the page or deck and read it before calling it done.
Most defects in this material are visual — an image that overflows the slide, a figure orphaned
from its caption, a screenshot too small to read at presentation size.

## Conventions

- Nothing references an image outside its own folder.
- GitHub-style admonitions (`> [!NOTE]`, `> [!WARNING]`) — the `gh-admonitions` plugin renders them.
- Schedule in **week numbers, not calendar dates**, so the site survives being re-offered.
- Images: nothing wider than about 2000 px; keep a deck's `images/` folder under ~15 MB; JPEG for
  photographs, PNG for anything with text.
- Do not commit built output: `site/`, `_site/`, or deck `.html`.
- Converting a PowerPoint? `tools/slide-conversion-guide.md` is the authority. Follow it exactly so
  every deck behaves the same.

## Git

Commit logically-grouped work with a message that says what changed and why. Pushing to `main`
publishes to students within a minute, so do not push unasked. If you are a subagent converting a
single deck or fixing one lab's images, leave the work in the working tree and report back; the
maintainer commits.

When you finish, say plainly what you changed, what you verified versus what you assumed, what you
flagged, and what you deliberately did not do.
