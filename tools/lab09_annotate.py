"""Draw Lab 9's Select by Attribute callout, with the buffer distance the lab actually uses.

The figure this replaces said "We need a 10km buffer" twice, while Lab 9 step 41 buffers Fish
Creek Road by 5 kilometers. The wrong number was baked into the drawing, so the only fix was to
re-shoot the dialog and redraw the note.

    python3 tools/lab09_annotate.py <shots dir> [repo root]

Boxes are placed as fractions of the capture rather than from recorded widget rectangles, because
the processing AlgorithmDialog builds its parameter widgets dynamically and they carry no stable
objectName. Re-check them by eye if the dialog is ever re-captured at a different size.
"""
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lab02_annotate import RED, PINK_BG, PINK_EDGE, font, box, note, MAX_WIDTH  # noqa: E402

# fractions of the capture: (x, y, width, height)
INPUT_ROW = (0.028, 0.122, 0.672, 0.030)
ATTRIBUTE_ROW = (0.028, 0.213, 0.672, 0.030)

CALLOUT = ['The road data that we downloaded was created in geographic',
           'coordinates (EPSG:4269), which are measured in degrees. We need',
           'a 5 km buffer, but QGIS will not process degree coordinates in terms',
           'of linear distance (like kilometers), nor linear distances in terms of',
           'degrees. We must reproject the data into a CRS with projected',
           'coordinates in order to create our 5 km buffer.']


def main(src, repo):
    p = os.path.join(src, 'lab09-select-by-attribute.png')
    img = Image.open(p).convert('RGBA')
    d = ImageDraw.Draw(img)
    W, H = img.size
    for fx, fy, fw, fh in (INPUT_ROW, ATTRIBUTE_ROW):
        box(d, (round(fx * W), round(fy * H), round(fw * W), round(fh * H)), pad=8)
    note(d, (round(0.055 * W), round(0.56 * H)), CALLOUT, font(30),
         color=(20, 20, 20, 255), bg=PINK_BG, edge=PINK_EDGE)
    if img.width > MAX_WIDTH:
        img = img.resize((MAX_WIDTH, round(img.height * MAX_WIDTH / img.width)), Image.LANCZOS)
    out = os.path.join(repo, 'docs', 'assignments', 'lab-09', 'images', 'anchored9.png')
    img.convert('RGB').save(out, optimize=True)
    print('anchored9.png  %d x %d  %.0f KB' % (img.width, img.height,
                                               os.path.getsize(out) / 1024))


if __name__ == '__main__':
    root = sys.argv[2] if len(sys.argv) > 2 else \
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1], root)
