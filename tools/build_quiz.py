#!/usr/bin/env python3
"""Render the end-of-lecture self-check quizzes.

Every Tuesday deck ends with a scannable quiz: a self-contained page on the course site,
reached in class from a QR code on the last slide and from the week page afterwards. The
pages are all the same page with different questions, so they are generated rather than
copied — one data file per quiz under `tools/quizzes/`, one shared template.

    python3 tools/build_quiz.py                 # rebuild every quiz
    python3 tools/build_quiz.py map-elements    # rebuild one

Output is `docs/quizzes/<slug>/index.html`: a shell that loads the shared engine,
`docs/quizzes/assets/quiz.css` and `docs/quizzes/assets/quiz.js`, and carries its own
questions as a JSON block. MkDocs copies all of it through untouched. Styling and behaviour
live in those two shared files — change them once and every quiz follows.

To add a quiz to a deck:

 1. Write `tools/quizzes/<slug>.py` — copy the nearest existing one. Six to eight questions,
    sized to what the deck actually teaches, in two or three named parts. Every question
    needs an `explanation`: the explanation is the teaching, the score is not.
 2. `python3 tools/build_quiz.py <slug>`
 3. `python3 tools/make_quiz_qr.py <slug> slides/day-NN/images/<prefix>-quiz-<slug>-qr.png`
 4. Add the activity slide as the deck's LAST slide, after "Before Next Class", with the QR
    at `w:400` on the right and the URL in small text on the left as a fallback for a room
    with no signal.
 5. Add the quiz to `PRACTICE` in `tools/build_schedule.py` and re-run it, so the week page
    links it for anyone who misses the scan.
 6. Render the deck to PNG and decode the QR out of the rendered slide, not just the source
    image; play the quiz through at phone width.

Keep the slug short: it decides the QR's density, and the code is read from the back row.
"""
import hashlib
import html
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tools" / "quiz_template.html"
DATA_DIR = ROOT / "tools" / "quizzes"
OUT_DIR = ROOT / "docs" / "quizzes"
ASSETS = OUT_DIR / "assets"

REQUIRED = ["SLUG", "TITLE", "DAY", "WEEK", "TOPIC", "BLURB", "DESCRIPTION",
            "CLOSING", "MESSAGES", "QUESTIONS"]


def load(path: Path) -> dict:
    """Exec one quiz data file and return its module namespace."""
    ns: dict = {}
    exec(compile(path.read_text(), str(path), "exec"), ns)
    missing = [k for k in REQUIRED if k not in ns]
    if missing:
        raise SystemExit(f"{path.name}: missing {', '.join(missing)}")
    return ns


def check(ns: dict, path: Path) -> None:
    """The mistakes that are easy to make in a data file and invisible in the rendered page."""
    qs = ns["QUESTIONS"]
    if not 4 <= len(qs) <= 10:
        raise SystemExit(f"{path.name}: {len(qs)} questions — the house size is six to eight")
    for i, q in enumerate(qs, start=1):
        where = f"{path.name} question {i}"
        for field in ("section", "prompt", "options", "correct", "explanation"):
            if field not in q:
                raise SystemExit(f"{where}: missing '{field}'")
        if not (isinstance(q["correct"], int) and 0 <= q["correct"] < len(q["options"])):
            raise SystemExit(f"{where}: 'correct' is not an index into 'options'")
        if len(set(q["options"])) != len(q["options"]):
            raise SystemExit(f"{where}: duplicate options")
        if len(q["options"]) < 2:
            raise SystemExit(f"{where}: a question needs at least two options")
        if len(q["options"]) > 6:
            raise SystemExit(f"{where}: more than six options (the letters run A-F)")
        if not q["explanation"].strip():
            raise SystemExit(f"{where}: empty explanation — the explanation is the teaching")
    if len(ns["MESSAGES"]) != 3:
        raise SystemExit(f"{path.name}: MESSAGES needs three entries (top, middle, low)")


# Options whose meaning depends on where they sit. These are pinned to the end and never
# shuffled; everything above them is.
TRAILING = re.compile(r"^(all|none|both|neither) of (the )?(above|these)\b", re.I)


def balance(qs: list, slug: str) -> None:
    """Spread the correct answer across the letters, in place.

    Left alone, a written-in-order quiz tends to put the answer in the same slot again and
    again — six of the first eleven had it in one letter five times out of eight, which
    rewards guessing and teaches nothing. Each question's options are permuted with a seed
    made from the quiz and the question, so the order is stable across rebuilds (a student
    who reloads sees the same page) but unrelated between questions.
    """
    targets = [i % 4 for i in range(len(qs))]
    random.Random(f"{slug}-positions").shuffle(targets)
    for n, (q, want) in enumerate(zip(qs, targets)):
        opts = q["options"]
        pinned = [o for o in opts if TRAILING.match(o)]
        movable = [o for o in opts if o not in pinned]
        answer = opts[q["correct"]]
        if answer in pinned:            # "none of the above" as the answer: leave it alone
            continue
        rest = [o for o in movable if o != answer]
        random.Random(f"{slug}-{n}").shuffle(rest)
        want = min(want, len(movable) - 1)
        new = rest[:want] + [answer] + rest[want:] + pinned
        q["options"] = new
        q["correct"] = new.index(answer)


def asset_version() -> str:
    """A short hash of the shared stylesheet and script, stamped onto their URLs.

    The assets have no version in their names, so without this a browser that cached
    quiz.css keeps serving the old one after a fix ships — which is exactly what happened
    the first time the engine changed under a page that was already open."""
    h = hashlib.sha256()
    for name in ("quiz.css", "quiz.js"):
        h.update((ASSETS / name).read_bytes())
    return h.hexdigest()[:8]


def render(ns: dict) -> str:
    """Fill the shell. The questions travel as a JSON block that docs/quizzes/assets/quiz.js
    reads — the page carries no logic and no styling of its own."""
    t = TEMPLATE.read_text()
    qs = ns["QUESTIONS"]

    balance(qs, ns["SLUG"])

    data = {
        "messages": list(ns["MESSAGES"]),
        "questions": [
            {"section": q["section"], "prompt": q["prompt"], "setup": q.get("setup", ""),
             "options": list(q["options"]), "correct": q["correct"],
             "explanation": q["explanation"]}
            for q in qs
        ],
    }
    # "</script>" inside a question would end the JSON block early; nothing in the data
    # files needs it, but escaping the slash costs nothing and removes the trap.
    payload = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")

    values = {
        "TITLE": html.escape(ns["TITLE"]),
        "DESCRIPTION": html.escape(ns["DESCRIPTION"]),
        "DAY": str(ns["DAY"]),
        "TOPIC": ns["TOPIC"],
        "BLURB": ns["BLURB"].strip(),
        "N": str(len(qs)),
        "WEEK": str(ns["WEEK"]),
        "WEEK2": f"{ns['WEEK']:02d}",
        "CLOSING": ns["CLOSING"].rstrip("\n"),
        "DATA": payload,
        "ASSETV": asset_version(),
    }
    for key, val in values.items():
        t = t.replace(f"%%{key}%%", val)
    if "%%" in t:
        raise SystemExit("template still has an unfilled placeholder")
    return t


def main() -> None:
    wanted = sys.argv[1:]
    files = sorted(DATA_DIR.glob("*.py"))
    if wanted:
        files = [f for f in files if f.stem in wanted]
        unknown = set(wanted) - {f.stem for f in files}
        if unknown:
            raise SystemExit(f"no quiz data file for: {', '.join(sorted(unknown))}")
    if not files:
        raise SystemExit(f"no quiz data files in {DATA_DIR}")

    for path in files:
        ns = load(path)
        check(ns, path)
        out = OUT_DIR / ns["SLUG"] / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(ns))
        print(f"{out.relative_to(ROOT)}  —  {len(ns['QUESTIONS'])} questions, "
              f"Day {ns['DAY']}, Week {ns['WEEK']}")


if __name__ == "__main__":
    main()
