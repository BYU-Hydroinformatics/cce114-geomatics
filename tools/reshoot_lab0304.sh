#!/bin/bash
# Re-shoot every Lab 3 and Lab 4 figure from scratch, in one command.
#
#   IMPORTANT: put the Mac in LIGHT appearance first.
#   Qt takes its palette from the macOS session appearance, and in dark mode every dialog comes
#   out dark, which no Clyde 234 lab machine shows and which does not match Labs 1 and 2. There
#   is no way to force it from a script: `defaults write -g AppleInterfaceStyle` does not reach
#   the running GUI session, and the AppleScript route needs an automation prompt.
#   System Settings > Appearance > Light, then run this.
#
#   ./tools/reshoot_lab0304.sh <work dir>
#
# <work dir> needs the demo data built by the commands in tools/lab0304-improvement-plan.md:
# points.csv, pts_corrected.shp, campus.shp, campus_area.shp, temple_footprint.shp,
# parking_lot.shp and SF_Waterways.gpkg. Keep it outside ~/Desktop, ~/Documents and ~/Downloads.
set -euo pipefail

WORK="${1:?usage: reshoot_lab0304.sh <work dir>}"
OUT="$WORK/out"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$OUT"

if [ "$(defaults read -g AppleInterfaceStyle 2>/dev/null || true)" = "Dark" ]; then
  echo "macOS is in dark appearance. Switch to Light in System Settings first, or the figures" >&2
  echo "will not match Labs 1 and 2. Aborting." >&2
  exit 1
fi

QGIS=/Applications/QGIS.app/Contents/MacOS/QGIS
# A throwaway QGIS profile, so the figures use QGIS's default light UI theme no matter what theme
# the maintainer's own profile is set to, and so nothing about their setup is touched.
PROFILE=lab34shots
PY=/Applications/QGIS.app/Contents/MacOS/python3.12
# PYTHONHOME must be set for QGIS's own interpreter and must NOT leak into the system python3,
# which crashes with "No module named 'encodings'" if it inherits it. So set it per call.
QENV="PYTHONHOME=/Applications/QGIS.app/Contents/Frameworks \
PROJ_LIB=/Applications/QGIS.app/Contents/Resources/qgis/proj \
GDAL_DATA=/Applications/QGIS.app/Contents/Resources/qgis/gdal \
QT_PLUGIN_PATH=/Applications/QGIS.app/Contents/PlugIns"
export LAB34_DATA="$WORK" LAB34_OUT="$OUT"

echo "== dialogs =="
for s in $(python3 "$REPO/tools/qgis_lab0304_dialog_shots.py" --list); do
  env $QENV SHOT="$s" "$PY" "$REPO/tools/qgis_lab0304_dialog_shots.py" 2>/dev/null \
    | grep -E "x [0-9]+$" || echo "  $s FAILED"
done

echo "== windows, canvas and layouts =="
for s in $(python3 "$REPO/tools/qgis_lab0304_window_shots.py" --list); do
  SHOT="$s" "$QGIS" --nologo --profile "$PROFILE" --code \
    "$REPO/tools/qgis_lab0304_window_shots.py" >/dev/null 2>&1 || true
  echo "  $s done"
done
grep -E "saved|MISSING|EXCEPTION" "$OUT/window-shots-34.log" || true

echo "== annotations, written straight into the labs' images folders =="
python3 "$REPO/tools/lab0304_annotate.py" "$OUT" "$REPO"

echo
echo "Now: python3 -m mkdocs build --strict, read both pages, then commit."
