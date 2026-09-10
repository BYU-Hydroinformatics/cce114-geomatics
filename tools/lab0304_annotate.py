"""Turn the raw Lab 3 and Lab 4 captures into the finished figures, at their final filenames.

Reuses the drawing helpers from tools/lab02_annotate.py, adds the red boxes each lab step needs
from the widget rectangles the capture scripts saved next to every PNG, caps the width at the
repository's 2000 px limit, and writes each figure straight into the lab's images/ folder under
the name the Markdown already references. Nothing to rename afterwards.

    python3 tools/lab0304_annotate.py <shots dir> [repo root]

Shots whose source capture is missing are skipped and listed, so a partial capture run still
produces whatever it can. TARGETS below is the whole mapping from capture name to final file; it
is also reproduced in tools/lab0304-improvement-plan.md for a human to read.
"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lab02_annotate import RED, PAD, LINE, font, box, note, arrow, MAX_WIDTH  # noqa: E402

# capture name -> (lab folder, final file name, annotate function or None)
# The final names are the ones Lab 3 and Lab 4 already reference, so the Markdown does not change.
# Deliberately NOT mapped, because the capture and the existing figure mean different things:
#   lab3-icon-new-shapefile-layer  is a 66 px button; new-shapefile-button.png is a toolbar strip
#     whose alt text says "toolbar with the New Shapefile Layer button highlighted". Swapping one
#     for the other would make the alt text wrong. Decide which the step wants first.
TARGETS = [
    # ---- Lab 3
    ('lab3-delimited-text',        'lab-03', 'dsm-delimited-text.png',      'lab3_dsm'),
    ('lab3-save-features-as',      'lab-03', 'anchored4.png',               'lab3_save_as'),
    ('lab3-digitizing-toolbar',    'lab-03', 'digitizing-toolbar.png',      None),
    ('lab3-feature-attributes',    'lab-03', 'feature-attributes.png',      None),
    ('lab3-new-shapefile-dialog',  'lab-03', 'new-shapefile-dialog.png',    'lab3_new_shp'),
    ('lab3-campus-polygon',        'lab-03', 'anchored6.png',               None),
    ('lab3-field-calculator',      'lab-03', 'anchored7.png',               'lab3_calc'),
    ('lab3-attribute-table',       'lab-03', 'anchored8.png',               None),
    ('lab3-example-layout',        'lab-03', 'example-layout.png',          None),
    ('lab3-icon-data-source-manager', 'lab-03', 'image2.png',               None),
    ('lab3-icon-move-feature',     'lab-03', 'image3.png',                  None),
    ('lab3-icon-add-point-feature', 'lab-03', 'image4.png',                 None),
    ('lab3-icon-add-polygon-feature', 'lab-03', 'image5.png',               None),
    ('lab3-icon-field-calculator', 'lab-03', 'image6.png',                  None),
    # ---- Lab 4
    ('lab4-new-geopackage-point',  'lab-04', 'anchored3.png',               'lab4_gpkg'),
    ('lab4-new-geopackage-polygon', 'lab-04', 'anchored5.png',              'lab4_gpkg'),
    ('lab4-snapping-toolbar',      'lab-04', 'anchored6.png',               None),
    ('lab4-temple-site',           'lab-04', 'anchored4.png',               None),
    ('lab4-footprints',            'lab-04', 'image7.png',                  None),
    ('lab4-field-calculator',      'lab-04', 'image5.png',                  'lab4_calc'),
    ('lab4-field-calculator-update', 'lab-04', 'image6.png',                'lab4_calc'),
    ('lab4-icon-toggle-editing',   'lab-04', 'image2.png',                  None),
    ('lab4-icon-toggle-editing',   'lab-04', 'image3.png',                  None),
    ('lab4-icon-save-layer-edits', 'lab-04', 'image4.png',                  None),
    # Not referenced by Lab 4 yet. It is a good figure for step 34, the HTTP protocol paste,
    # which currently has none; see tools/lab0304-improvement-plan.md for the snippet to add.
    ('lab4-data-source-manager',   'lab-04', 'dsm-vector-protocol.png',     None),
]

# Figures that are mostly satellite imagery keep their .png name but are written as JPEG-quality
# PNG only if small; these are re-encoded as JPEG under the same stem when the lab reference is
# updated. Left as PNG here so the existing Markdown keeps working.
PHOTOGRAPHIC = {'lab3-campus-polygon', 'lab3-example-layout', 'lab4-temple-site', 'lab4-footprints'}


def _f(sz):
    return font(sz)


def lab3_dsm(d, r):
    if 'crs' in r:
        box(d, r['crs'])
        note(d, (r['crs'][0], r['crs'][1] + r['crs'][3] + 34),
             ['Set this to EPSG:26912 before you click Add'], _f(28))


def lab3_save_as(d, r):
    for k in ('format', 'crs', 'filename'):
        if k in r:
            box(d, r[k])


def lab3_new_shp(d, r):
    for k in ('geometry', 'crs', 'filename'):
        if k in r:
            box(d, r[k])


def lab3_calc(d, r):
    for k in ('name', 'type', 'expression'):
        if k in r:
            box(d, r[k])


def lab4_gpkg(d, r):
    for k in ('filename', 'geometry', 'crs', 'fields'):
        if k in r:
            box(d, r[k])
    if 'add' in r:
        box(d, r['add'])
        x, y, w, h = r['add']
        note(d, (x - 40, y + h + 40), ['Click this after each field,', 'or it is not added'],
             _f(28), anchor='rt')


def lab4_calc(d, r):
    for k in ('name', 'type', 'expression', 'update', 'existing'):
        if k in r:
            box(d, r[k])


FUNCS = {n: f for n, f in globals().items() if n.startswith(('lab3_', 'lab4_'))}


def main(src, repo):
    import json
    from PIL import ImageDraw
    made, missing = [], []
    for capture, lab, final, fn in TARGETS:
        p = os.path.join(src, capture + '.png')
        if not os.path.exists(p):
            missing.append(capture)
            continue
        img = Image.open(p).convert('RGBA')
        jp = os.path.join(src, capture + '.json')
        rects = json.load(open(jp)) if os.path.exists(jp) else {}
        if fn:
            FUNCS[fn](ImageDraw.Draw(img), rects)
        if img.width > MAX_WIDTH:
            img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)),
                             Image.LANCZOS)
        out_dir = os.path.join(repo, 'docs', 'assignments', lab, 'images')
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, final)
        img.convert('RGB').save(out, optimize=True)
        made.append('%-34s -> %s/%s  %d x %d  %.0f KB' %
                    (capture, lab, final, img.width, img.height,
                     os.path.getsize(out) / 1024))
    print('\n'.join(made))
    if missing:
        print('\nno capture found for: ' + ', '.join(sorted(set(missing))))
    print('\n%d figures written. Now: mkdocs build --strict' % len(made))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    repo_root = sys.argv[2] if len(sys.argv) > 2 else \
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1], repo_root)
