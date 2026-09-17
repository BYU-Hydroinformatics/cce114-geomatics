#!/usr/bin/env bash
# Re-shoot every figure on docs/handson/week-03.md (the Week 3 symbology walkthrough).
#
#   ./tools/reshoot_week03.sh ~/week03work
#
# The argument is a folder holding the UNZIPPED "United States Shapefiles.zip" from the Week 3
# Thursday entry on Learning Suite, so that "$1/United States/Shapefiles/states.shp" exists.
# Keep it outside ~/Desktop, ~/Documents and ~/Downloads: QGIS cannot read there on macOS.
#
# Two passes, because the two kinds of capture need different hosts:
#   * dialogs   -- QGIS's bundled Python, headless, no window, no focus stealing
#   * windows   -- QGIS launched with --code so it can grab its own main window and the
#                  Print Layout designer
# One shot per process in both: several dialogs in one process crashes partway through.
#
# Like the Lab 3/4 and Lab 5/6 re-shoots, this needs the Mac in LIGHT appearance. Qt follows the
# macOS session appearance and it cannot be set from a script, so the run refuses in dark mode
# rather than producing dark figures no Clyde 234 machine would ever show.
set -euo pipefail
cd "$(dirname "$0")/.."

DATA="${1:-$HOME/week03work}"
OUT="docs/handson/images"

if [[ "$(defaults read -g AppleInterfaceStyle 2>/dev/null || echo Light)" == "Dark" ]]; then
  echo "Mac is in Dark appearance. Set System Settings > Appearance to Light and re-run." >&2
  exit 1
fi
if [[ ! -f "$DATA/United States/Shapefiles/states.shp" ]]; then
  echo "No states.shp under '$DATA/United States/Shapefiles'." >&2
  echo "Unzip 'United States Shapefiles.zip' there first." >&2
  exit 1
fi

QGIS=/Applications/QGIS.app
export PYTHONHOME="$QGIS/Contents/Frameworks" \
       PROJ_LIB="$QGIS/Contents/Resources/qgis/proj" \
       GDAL_DATA="$QGIS/Contents/Resources/qgis/gdal" \
       QT_PLUGIN_PATH="$QGIS/Contents/PlugIns"

echo "==> dialogs (headless)"
for s in single-symbol-states states-categorized states-graduated cities-graduated-size \
         labels-states labels-cities-expression select-by-expression field-calculator; do
  WEEK03_DATA="$DATA" WEEK03_OUT="$OUT" SHOT="$s" \
    "$QGIS/Contents/MacOS/python3.12" tools/qgis_week03_dialog_shots.py
done

echo "==> main window and print layout (QGIS grabs itself)"
for s in map-single-symbols map-graduated map-labels attribute-table \
         layout-designer layout-export; do
  WEEK03_DATA="$DATA" WEEK03_OUT="$OUT" SHOT="$s" \
    "$QGIS/Contents/MacOS/QGIS" --nologo --code tools/qgis_week03_window_shots.py \
    2>&1 | grep '^\[week03\]' || true
done

echo "==> normalising to the repo's 2000 px ceiling"
for f in "$OUT"/w3-*.png; do
  w=$(sips -g pixelWidth "$f" | awk '/pixelWidth/{print $2}')
  if [[ "$w" -gt 2000 ]]; then sips -Z 2000 "$f" --out "$f" >/dev/null; fi
done

echo "==> done. Figures in $OUT:"
ls -1 "$OUT"/w3-*.png | wc -l
