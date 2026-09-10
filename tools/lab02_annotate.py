"""Draw Lab 2's red boxes and callouts onto the raw QGIS captures.

The capture scripts (tools/qgis_lab02_dialog_shots.py and tools/qgis_lab02_window_shots.py) save
a <shot>.json next to each <shot>.png giving the pixel rectangle of every widget worth pointing
at, so the annotations follow the widgets rather than hand-measured coordinates. Re-capture a
shot at a different size and re-run this; the boxes still land in the right place.

    python3 tools/lab02_annotate.py <shots dir> <output dir>

Everything is drawn at the capture's native 2x, then the finished images are written out. The
callout wording is carried over from the original Lab 2 figures where those had one.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

RED = (216, 27, 27, 255)
PINK_BG = (250, 226, 228, 255)
PINK_EDGE = (150, 24, 30, 255)
PAD = 10
LINE = 6

FONT_CANDIDATES = [
    '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
    '/System/Library/Fonts/Helvetica.ttc',
    '/Library/Fonts/Arial Bold.ttf',
]


def font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def box(draw, rect, pad=PAD, width=LINE, color=RED):
    x, y, w, h = rect
    draw.rectangle([x - pad, y - pad, x + w + pad, y + h + pad], outline=color, width=width)


def text_size(draw, s, f):
    l, t, r, b = draw.textbbox((0, 0), s, font=f)
    return r - l, b - t


def note(draw, xy, lines, f, anchor='lt', color=RED, bg=None, edge=None):
    """Draw a short red note, optionally on a filled callout panel."""
    widths, heights = [], []
    for line in lines:
        w, h = text_size(draw, line, f)
        widths.append(w)
        heights.append(h)
    tw = max(widths)
    lh = int(max(heights) * 1.45)
    th = lh * len(lines)
    x, y = xy
    if anchor[0] == 'r':
        x -= tw
    if anchor[0] == 'c':
        x -= tw // 2
    if anchor[1] == 'b':
        y -= th
    if bg is not None:
        m = 22
        draw.rectangle([x - m, y - m, x + tw + m, y + th + m], fill=bg,
                       outline=edge or bg, width=LINE)
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=f, fill=color)
    return x, y, tw, th


def arrow(draw, start, end, color=RED, width=LINE):
    """A straight arrow from start to end with a solid triangular head."""
    import math
    draw.line([start, end], fill=color, width=width)
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 34
    for spread in (2.6, -2.6):
        draw.line([end, (end[0] + size * math.cos(ang + spread),
                         end[1] + size * math.sin(ang + spread))], fill=color, width=width)
    draw.polygon([end,
                  (end[0] + size * math.cos(ang + 2.6), end[1] + size * math.sin(ang + 2.6)),
                  (end[0] + size * math.cos(ang - 2.6), end[1] + size * math.sin(ang - 2.6))],
                 fill=color)


def load(src, name):
    img = Image.open(os.path.join(src, name + '.png')).convert('RGBA')
    path = os.path.join(src, name + '.json')
    rects = json.load(open(path)) if os.path.exists(path) else {}
    return img, ImageDraw.Draw(img), rects


MAX_WIDTH = 2000

# Figures that are mostly satellite imagery. As PNG these run 1.3 to 3 MB each and dominate the
# lab folder; at JPEG quality 90 with no chroma subsampling they are a third of the size and the
# panel text and red annotations are indistinguishable at full magnification. Every other figure
# is flat UI and stays PNG.
PHOTOGRAPHIC = {
    'map-after-symbology', 'map-with-labels', 'finished-layout',
    'layout-neatline', 'layout-legend-properties', 'layout-north-arrow-scalebar',
    'layout-title-label',
}


def save(img, dst, name):
    """Write the finished figure, capped at the repository's 2000 px width limit."""
    if img.width > MAX_WIDTH:
        img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)),
                         Image.LANCZOS)
    ext = '.jpg' if name in PHOTOGRAPHIC else '.png'
    path = os.path.join(dst, name + ext)
    if ext == '.jpg':
        img.convert('RGB').save(path, quality=90, optimize=True, subsampling=0)
    else:
        img.convert('RGB').save(path, optimize=True)
    print('%-32s %5d x %-5d %6.0f KB  %s' % (name, img.width, img.height,
                                             os.path.getsize(path) / 1024, ext))


def main(src, dst):
    os.makedirs(dst, exist_ok=True)
    f28, f34, f40 = font(28), font(34), font(40)

    # ---- steps 3-4: the Project CRS dialog, box on the Filter field
    img, d, r = load(src, 'crs-dialog')
    if 'filter' in r:
        box(d, r['filter'])
        note(d, (r['filter'][0], r['filter'][1] + r['filter'][3] + 34),
             ['Type the EPSG code here'], f28)
    save(img, dst, 'crs-dialog')

    # ---- steps 11-12: the symbol layer stack and the green + that adds to it
    img, d, r = load(src, 'point-symbology')
    if 'add-layer' in r:
        box(d, r['add-layer'])
        note(d, (r['add-layer'][0] - 30, r['add-layer'][1] + r['add-layer'][3] + 34),
             ['Adds another', 'symbol layer'], f28, anchor='rt')
    if 'symbol-tree' in r:
        box(d, r['symbol-tree'])
    save(img, dst, 'point-symbology')

    # ---- step 13: the SVG Marker layer selected, SVG browser on screen
    img, d, r = load(src, 'point-svg-marker')
    if 'symbol-tree' in r:
        box(d, r['symbol-tree'])
    save(img, dst, 'point-svg-marker')

    # ---- steps 18-19: what Classify actually produces
    img, d, r = load(src, 'roads-categorized')
    for k in ('value', 'classify'):
        if k in r:
            box(d, r[k])
    if 'categories' in r:
        # The Legend column leaves a wide empty strip inside the list; put the notes there so
        # they cannot run off the right edge of the capture.
        x, y, w, h = r['categories']
        nx = x + 900
        note(d, (nx, y + 60), ['CARTOCODE is a text field, so the', 
                               'list runs 1, 10, 11 ... 18, 2, 3 ...'], f28)
        arrow(d, (nx - 40, y + 90), (x + 420, y + 60))
        note(d, (nx, y + h - 190), ['Classify leaves this "all other values"',
                                    'row behind, and it starts out checked'], f28)
        arrow(d, (nx - 40, y + h - 130), (x + 620, y + h - 34))
    save(img, dst, 'roads-categorized')

    # ---- steps 20-21: one merged Highway category
    img, d, r = load(src, 'roads-merged-highway')
    if 'categories' in r:
        x, y, w, h = r['categories']
        box(d, r['categories'])
        note(d, (x + 40, y + h + 60),
             ['One row for all five highway codes, and', '"all other values" unchecked'], f28)
    save(img, dst, 'roads-merged-highway')

    # ---- steps 24-27: graduated classes, and the precision that cleans up the labels
    img, d, r = load(src, 'municipalities-graduated')
    for k in ('value', 'mode', 'classes', 'precision'):
        if k in r:
            box(d, r[k])
    if 'precision' in r and 'classes' in r:
        px, py, pw, ph = r['precision']
        cx, cy, cw, ch = r['classes']
        nx, ny = cx - 1500, cy - 460
        note(d, (nx, ny), ['Set Precision to 0 so the class labels read',
                           '892 - 3229 rather than 892.0000 - 3229.0000'], f28)
        arrow(d, (nx + 900, ny - 30), (px + pw // 2, py + ph + 30))
    save(img, dst, 'municipalities-graduated')

    # ---- step 28: opacity
    img, d, r = load(src, 'layer-rendering-opacity')
    if 'opacity' in r:
        box(d, r['opacity'])
        note(d, (r['opacity'][0], r['opacity'][1] - 60),
             ['Expand Layer Rendering to reach the opacity slider'], f28, anchor='lb')
    save(img, dst, 'layer-rendering-opacity')

    # ---- steps 31-32: labels and the text buffer
    img, d, r = load(src, 'labels-tab')
    for k in ('mode', 'sections'):
        if k in r:
            box(d, r[k])
    save(img, dst, 'labels-tab')

    # ---- step 40: the neatline, and the note about layout item order
    img, d, r = load(src, 'layout-neatline')
    for k in ('items-panel', 'shape-tool'):
        if k in r:
            box(d, r[k])
    note(d, (1180, 1500),
         ['Just like your map views, Layouts have layers.',
          'If your neatline is on top of your map it will',
          'cover it up. Use the panel labeled "Items" on',
          'the right side of the Layout window to drag',
          'items above/below each other.'],
         f40, color=(20, 20, 20, 255), bg=PINK_BG, edge=PINK_EDGE)
    save(img, dst, 'layout-neatline')

    # ---- steps 42-45: the legend's Item Properties
    img, d, r = load(src, 'layout-legend-properties')
    for k in ('auto-update', 'item-tree', 'remove'):
        if k in r:
            box(d, r[k], pad=8)
    if 'auto-update' in r:
        x, y, w, h = r['auto-update']
        note(d, (x - 60, y), ['Uncheck this first', 'so the list can be edited'], f28,
             anchor='rt')
        arrow(d, (x - 70, y + 20), (x - 20, y + 16))
    # Notes go in the empty layout canvas to the left of the panel: anchored to the right of
    # these widgets they run off the edge of the capture.
    if 'remove' in r:
        x, y, w, h = r['remove']
        note(d, (x - 300, y + 120), ['Select a legend entry above,', 'then this red minus removes it'],
             f28, anchor='rt')
        arrow(d, (x - 280, y + 130), (x + w // 2 - 6, y + h + 24))
    if 'item-tree' in r:
        x, y, w, h = r['item-tree']
        note(d, (x - 300, y + h - 160), ['Double click an entry', 'to rename it'], f28,
             anchor='rt')
        arrow(d, (x - 280, y + h - 130), (x + 60, y + h - 90))
    save(img, dst, 'layout-legend-properties')

    # ---- steps 49-50: the title label
    img, d, r = load(src, 'layout-title-label')
    for k in ('text', 'font'):
        if k in r:
            box(d, r[k], pad=8)
    if 'text' in r:
        x, y, w, h = r['text']
        note(d, (x - 60, y + 40), ['Edit text here'], f34, anchor='rt')
        arrow(d, (x - 70, y + 60), (x - 18, y + 60))
    if 'font' in r:
        x, y, w, h = r['font']
        note(d, (x - 60, y - 10), ['Edit font attributes here'], f34, anchor='rt')
        arrow(d, (x - 70, y + 14), (x - 18, y + 20))
    save(img, dst, 'layout-title-label')

    # ---- the Layers panel grab includes a tall empty tail below the last layer
    lp = os.path.join(src, 'layers-panel.png')
    if os.path.exists(lp):
        img = Image.open(lp).convert('RGBA')
        img = img.crop((0, 0, img.width, min(img.height, 1500)))
        # Sample inside the panel's own border, or the border itself counts as content.
        inset = 12
        bg = img.getpixel((img.width - 40, img.height - 40))
        bottom = img.height
        for y in range(img.height - inset, 0, -1):
            row = [img.getpixel((x, y)) for x in range(inset, img.width - inset, 20)]
            if any(abs(px[0] - bg[0]) + abs(px[1] - bg[1]) + abs(px[2] - bg[2]) > 24
                   for px in row):
                bottom = min(img.height, y + 70)
                break
        save(img.crop((0, 0, img.width, bottom)), dst, 'layers-panel')

    # ---- shots that need no annotation, copied through
    for name in ('layout-north-arrow-scalebar', 'map-after-symbology', 'map-with-labels',
                 'finished-layout',
                 'icon-add-map', 'icon-move-item-content', 'icon-add-shape', 'icon-add-legend',
                 'icon-add-north-arrow', 'icon-add-scalebar', 'icon-add-label'):
        p = os.path.join(src, name + '.png')
        if os.path.exists(p):
            img = Image.open(p).convert('RGBA')
            save(img, dst, name)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
