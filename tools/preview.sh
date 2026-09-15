#!/usr/bin/env bash
# Local preview of the whole course site, decks included, before pushing.
#
#   tools/preview.sh              # site + every deck
#   tools/preview.sh day-02       # site + just that deck (much faster to start)
#   tools/preview.sh day-02 day-14
#
# Then open http://localhost:8000/ . Editing anything under docs/ reloads the page;
# editing a deck under slides/ re-renders it, and a browser refresh shows it.
#
# Why this exists rather than a bare `mkdocs serve`:
#
#   * mkdocs alone does not build the Marp decks, so half the course is missing.
#   * The week and hands-on pages link to decks by absolute published URL, so a
#     deck link in a local preview would take you to the live site instead of
#     your edits. tools/preview_hooks.py rewrites those links to local ones.
#   * Decks must be rendered with the same flags CI uses. --html in particular:
#     without it Marp strips `style` attributes and every inline-styled slide
#     renders wrong, so a local check would pass on a deck that ships broken.
#
# Everything this writes (.venv-preview/, docs/slides/) is gitignored.

set -euo pipefail
cd "$(dirname "$0")/.."

VENV=".venv-preview"
DECK_OUT="docs/slides"
THEME="slides/theme/cce114.css"
MARP=(npx -y @marp-team/marp-cli@latest --no-stdin --html --theme "$THEME")

# --- python side: mkdocs in a throwaway venv -------------------------------
if [[ ! -x "$VENV/bin/mkdocs" ]]; then
  echo "==> first run: installing mkdocs into $VENV (about a minute)"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --quiet --upgrade pip
  "$VENV/bin/pip" install --quiet mkdocs-material mkdocs-github-admonitions-plugin
fi

# --- which decks -----------------------------------------------------------
if (( $# )); then
  days=("$@")
else
  days=()
  for d in slides/day-*/; do days+=("$(basename "$d")"); done
fi

echo "==> rendering ${#days[@]} deck(s) into $DECK_OUT"
for day in "${days[@]}"; do
  src_dir="slides/$day"
  [[ -d "$src_dir" ]] || { echo "no such deck: $src_dir" >&2; exit 1; }
  mkdir -p "$DECK_OUT/$day"
  for md in "$src_dir"/*.md; do
    [[ -e "$md" ]] || continue
    "${MARP[@]}" "$md" -o "$DECK_OUT/$day/$(basename "${md%.md}").html"
  done
  # Deck HTML references images/ relatively, and mkdocs does not follow symlinks,
  # so the images have to be real files under docs/. rsync keeps it incremental.
  if [[ -d "$src_dir/images" ]]; then
    rsync -a --delete "$src_dir/images/" "$DECK_OUT/$day/images/"
  fi
done

pids=()
cleanup() {
  for p in "${pids[@]:-}"; do kill "$p" 2>/dev/null || true; done
  wait 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# --- watch the decks -------------------------------------------------------
# One watcher per deck file. Marp's --watch rebuilds on save; the rebuilt HTML
# lands under docs/, which also nudges mkdocs to reload.
for day in "${days[@]}"; do
  for md in "slides/$day"/*.md; do
    [[ -e "$md" ]] || continue
    "${MARP[@]}" --watch "$md" -o "$DECK_OUT/$day/$(basename "${md%.md}").html" \
      >/dev/null 2>&1 &
    pids+=($!)
  done
done

# --- serve -----------------------------------------------------------------
# Not --strict: a work-in-progress tree often has a link that is not wired up yet,
# and you still want to look at the page. Run `mkdocs build --strict` before pushing.
"$VENV/bin/mkdocs" serve -f mkdocs.preview.yml &
pids+=($!)

wait
