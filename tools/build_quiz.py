#!/usr/bin/env python3
"""Render the end-of-lecture self-check quizzes.

Every Tuesday deck ends with a scannable quiz: a self-contained page on the course site,
reached in class from a QR code on the last slide and from the week page afterwards. The
pages are all the same page with different questions, so they are generated rather than
copied — one data file per quiz under `tools/quizzes/`, one shared template.

    python3 tools/build_quiz.py                 # rebuild every quiz
    python3 tools/build_quiz.py map-elements    # rebuild one

Output is `docs/quizzes/<slug>/index.html`, which MkDocs copies through untouched.

To add a quiz to a deck:

 1. Write `tools/quizzes/<slug>.py` — copy the nearest existing one. Twelve questions in
    three parts reads well in about five minutes; every question needs an `explanation`,
    because the explanation is the teaching and the score is not.
 2. `python3 tools/build_quiz.py <slug>`
 3. `python3 tools/make_quiz_qr.py <slug> slides/day-NN/images/<prefix>-quiz-<slug>-qr.png`
 4. Add the activity slide to the deck, with the QR at `w:400` on the right and the URL in
    small text on the left as a fallback for a room with no signal.
 5. Add the quiz to `PRACTICE` in `tools/build_schedule.py` and re-run it, so the week page
    links it for anyone who misses the scan.
 6. Render the deck to PNG and decode the QR out of the rendered slide, not just the source
    image; play the quiz through at phone width.

Keep the slug short: it decides the QR's density, and the code is read from the back row.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "tools" / "quiz_template.html"
DATA_DIR = ROOT / "tools" / "quizzes"
OUT_DIR = ROOT / "docs" / "quizzes"

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
    if not qs:
        raise SystemExit(f"{path.name}: no questions")
    for i, q in enumerate(qs, start=1):
        where = f"{path.name} question {i}"
        for field in ("section", "prompt", "options", "correct", "explanation"):
            if field not in q:
                raise SystemExit(f"{where}: missing '{field}'")
        if not (isinstance(q["correct"], int) and 0 <= q["correct"] < len(q["options"])):
            raise SystemExit(f"{where}: 'correct' is not an index into 'options'")
        if len(set(q["options"])) != len(q["options"]):
            raise SystemExit(f"{where}: duplicate options")
        if len(q["options"]) > 6:
            raise SystemExit(f"{where}: more than six options (the letters run A-F)")
        if not q["explanation"].strip():
            raise SystemExit(f"{where}: empty explanation — the explanation is the teaching")
    if len(ns["MESSAGES"]) != 3:
        raise SystemExit(f"{path.name}: MESSAGES needs three entries (top, middle, low)")


def render(ns: dict) -> str:
    t = TEMPLATE.read_text()
    qs = ns["QUESTIONS"]

    # json.dumps gives valid JavaScript for these values and escapes the quotes and
    # backslashes that a hand-written explanation will eventually contain.
    lines = ["  const questions = ["]
    for q in qs:
        lines.append("    {")
        for field in ("section", "prompt", "setup"):
            lines.append(f"      {field}: {json.dumps(q.get(field, ''), ensure_ascii=False)},")
        lines.append("      options: [")
        for opt in q["options"]:
            lines.append(f"        {json.dumps(opt, ensure_ascii=False)},")
        lines.append("      ],")
        lines.append(f"      correct: {q['correct']},")
        lines.append(f"      explanation: {json.dumps(q['explanation'], ensure_ascii=False)}")
        lines.append("    },")
    lines.append("  ];")
    questions = "\n".join(lines)

    top, mid, low = ns["MESSAGES"]
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
        "MSG_TOP": json.dumps(top, ensure_ascii=False),
        "MSG_MID": json.dumps(mid, ensure_ascii=False),
        "MSG_LOW": json.dumps(low, ensure_ascii=False),
        "QUESTIONS": questions,
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
