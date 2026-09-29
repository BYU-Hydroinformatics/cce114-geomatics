# Day 8 deck figure: the Layer menu with Create Layer open, captured by QGIS 3.44 rendering its
# own QMenu widgets. Runs INSIDE QGIS at launch:
#
#   MENU_OUT=<out dir> /Applications/QGIS.app/Contents/MacOS/QGIS --nologo --code \
#     tools/qgis_day08_create_layer_menu_shot.py
#
# On macOS the menubar is native, but the Layer menu and its Create Layer submenu still exist as
# QMenu objects. QWidget.grab() paints them through Qt's own style at the screen's device pixel
# ratio (2x on Retina) without showing them, so no screen-recording permission is needed.
# Writes layer-menu.png, create-layer-menu.png and a JSON of item rectangles for compositing.
#
# Then composite the deck figure with the system Python (needs Pillow; QGIS's bundle may not):
#
#   python3 tools/qgis_day08_create_layer_menu_shot.py --compose <out dir> \
#     slides/day-08/images/vec-create-layer-menu.png
#
# The Layer menu is cropped at the separator below Paste Style and faded out, the Create
# Layer submenu sits beside it on the Create Layer row as Qt places it, and a red box marks
# New GeoPackage Layer. Box and placement come from the JSON, not from pixel guesses.
import os
import sys
import json
import time
import traceback


def compose(src, dst):
    from PIL import Image, ImageDraw, ImageFilter
    info = json.load(open(os.path.join(src, 'menu-rects.json')))
    k = info['dpr']
    lay = Image.open(os.path.join(src, 'layer-menu.png')).convert('RGBA')
    sub = Image.open(os.path.join(src, 'create-layer-menu.png')).convert('RGBA')
    rows = info['layer']['rows']
    create_row = next(r for r in rows if r['text'] == 'Create Layer')
    paste = next(r for r in rows if r['text'] == 'Paste Style')
    cut = int((paste['rect'][1] + paste['rect'][3]) * k) + 4
    lay = lay.crop((0, 0, lay.width, cut))
    fade = 48
    alpha = lay.getchannel('A')
    px = alpha.load()
    for y in range(cut - fade, cut):
        f = (cut - y) / fade
        for x in range(lay.width):
            px[x, y] = int(px[x, y] * f)
    lay.putalpha(alpha)

    m = 16                       # margin for shadow and box
    sx = lay.width - int(4 * k)  # submenu overlaps its parent a few points, as Qt draws it
    sy = int(create_row['rect'][1] * k)
    W = sx + sub.width + m * 2
    H = max(lay.height, sy + sub.height) + m * 2
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([m + 4, m + 5, m + lay.width + 4, m + lay.height - fade], fill=(0, 0, 0, 70))
    sd.rectangle([m + sx + 4, m + sy + 5, m + sx + sub.width + 4, m + sy + sub.height + 5],
                 fill=(0, 0, 0, 70))
    img = shadow.filter(ImageFilter.GaussianBlur(7))
    img.alpha_composite(lay, (m, m))
    img.alpha_composite(sub, (m + sx, m + sy))

    g = next(r for r in info['create']['rows'] if r['text'].startswith('New GeoPackage Layer'))
    x, y, w, h = [int(v * k) for v in g['rect']]
    d = ImageDraw.Draw(img)
    d.rectangle([m + sx + x - 4, m + sy + y - 4, m + sx + x + w + 4, m + sy + y + h + 4],
                outline=(216, 27, 27, 255), width=6)
    img.save(dst, optimize=True)
    print(dst, img.size)


if len(sys.argv) > 1 and sys.argv[1] == '--compose':
    compose(sys.argv[2], sys.argv[3])
    raise SystemExit

from qgis.PyQt.QtCore import QTimer
from qgis.PyQt.QtWidgets import QApplication, QMenu
from qgis.core import QgsProject
from qgis.utils import iface

OUT = os.environ['MENU_OUT']
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, 'menu-shot.log')
KEEP = []


def log(*a):
    with open(LOG, 'a') as f:
        f.write(' '.join(str(x) for x in a) + '\n')


def settle(seconds):
    end = time.time() + seconds
    while time.time() < end:
        QApplication.processEvents()
        time.sleep(0.05)


def clean(t):
    return t.replace('&', '')


def find_menu(parent, text):
    for a in parent.actions():
        if clean(a.text()) == text and a.menu() is not None:
            return a, a.menu()
    raise RuntimeError('no menu %r' % text)


def dump(menu, name):
    menu.ensurePolished()
    menu.adjustSize()
    rows = []
    for a in menu.actions():
        r = menu.actionGeometry(a)
        rows.append({'text': clean(a.text()), 'sep': a.isSeparator(), 'visible': a.isVisible(),
                     'enabled': a.isEnabled(), 'shortcut': a.shortcut().toString(),
                     'rect': [r.x(), r.y(), r.width(), r.height()]})
    return {'name': name, 'size': [menu.width(), menu.height()], 'rows': rows}


def main():
    settle(4)
    mb = iface.mainWindow().menuBar()
    _, layer = find_menu(mb, 'Layer')
    create_act, create = find_menu(layer, 'Create Layer')
    KEEP.extend([layer, create])
    gpkg = [a for a in create.actions() if clean(a.text()).startswith('New GeoPackage Layer')][0]
    info = {'dpr': QApplication.primaryScreen().devicePixelRatio()}
    info['layer'] = dump(layer, 'layer')
    info['create'] = dump(create, 'create')
    layer.setActiveAction(create_act)
    create.setActiveAction(gpkg)
    settle(0.5)
    pl = layer.grab()
    pc = create.grab()
    log('layer grab', pl.width(), pl.height(), pl.devicePixelRatio())
    log('create grab', pc.width(), pc.height(), pc.devicePixelRatio())
    pl.save(os.path.join(OUT, 'layer-menu.png'))
    pc.save(os.path.join(OUT, 'create-layer-menu.png'))
    with open(os.path.join(OUT, 'menu-rects.json'), 'w') as f:
        json.dump(info, f, indent=1)


try:
    main()
except Exception:
    log('EXCEPTION\n' + traceback.format_exc())
log('done')
QgsProject.instance().setDirty(False)
os._exit(0)
