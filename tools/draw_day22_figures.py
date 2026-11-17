"""Draw the Day 22 figures for attribute tables in overlays and for the layer workflow.

Two jobs, both original drawings (no textbook art):

* The small maps on the "two layers, two attribute tables" slides. Their geometry and piece order
  come from tools/day22-attribute-demo.json, which tools/qgis_day22_attribute_demo.py writes by
  running the real QGIS 3.44 Intersection and Union on two invented layers. Piece numbers on the
  maps match the row order of the tables on the slides.
* The generic geoprocessing workflow (layers as rectangles, operations as ovals) that replaces the
  diagram from Bolstad's GIS Fundamentals. Operation 2 takes two inputs on purpose, and the layers
  between operations are labeled intermediate layers.
* The Intersection dialog capture, cropped and boxed in red.

    python3 -m venv /tmp/gpvenv && /tmp/gpvenv/bin/pip install shapely matplotlib numpy pillow
    /tmp/gpvenv/bin/python tools/draw_day22_figures.py [dialog.png dialog.json]
"""

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch
from shapely import wkt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from draw_geoprocessing_figures import (D22, INK, L1_EDGE, L1_FILL, L2_EDGE, L2_FILL, NAVY,  # noqa: E402
                                        OUT_EDGE, OUT_FILL, PASTELS, draw, frame)

HERE = Path(__file__).resolve().parent
DEMO = json.loads((HERE / "day22-attribute-demo.json").read_text())
BOUNDS = (-0.15, -0.3, 4.15, 3.75)
RED = "#c8102e"


def save(fig, name):
    fig.savefig(D22 / name, dpi=200, facecolor="white", metadata={"Software": None})
    plt.close(fig)
    print("wrote", D22 / name)


def small_map():
    fig = plt.figure(figsize=(3.2, 2.7))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    return fig, ax


def label(ax, geom, text, color=NAVY, size=12):
    p = geom.representative_point()
    ax.text(p.x, p.y, text, ha="center", va="center", fontsize=size, fontweight="bold", color=color, zorder=5)


def badge(ax, geom, n):
    p = geom.representative_point()
    ax.text(p.x, p.y, str(n), ha="center", va="center", fontsize=12, fontweight="bold", color=NAVY, zorder=6,
            bbox=dict(boxstyle="circle,pad=0.25", fc="white", ec=NAVY, lw=1.4))


def fig_inputs(which):
    fig, ax = small_map()
    data = DEMO[which]
    for r in data["rows"]:
        g = wkt.loads(r["wkt"])
        if which == "counties":
            draw(ax, g, L1_FILL, L1_EDGE, lw=1.6)
            c = g.centroid
            ax.text(c.x, c.y + 0.75, r["attrs"][1].replace(" ", "\n"), ha="center", va="center",
                    fontsize=12, fontweight="bold", color=L1_EDGE)
        else:
            draw(ax, g, L2_FILL, L2_EDGE, lw=1.6)
            label(ax, g, r["attrs"][1].replace(" ", "\n"), color=L2_EDGE)
    frame(ax, None, BOUNDS)
    return fig


def fig_output(which):
    fig, ax = small_map()
    for r in DEMO["counties"]["rows"]:
        draw(ax, wkt.loads(r["wkt"]), "none", "#cccccc", lw=0.8, ls="--", z=0)
    for r in DEMO["catchments"]["rows"]:
        draw(ax, wkt.loads(r["wkt"]), "none", "#cccccc", lw=0.8, ls="--", z=0)
    for i, r in enumerate(DEMO[which]["rows"]):
        g = wkt.loads(r["wkt"])
        fill = OUT_FILL if which == "intersection" else PASTELS[i % len(PASTELS)]
        draw(ax, g, fill, OUT_EDGE, lw=1.4, z=2)
        badge(ax, g, i + 1)
    frame(ax, None, BOUNDS)
    return fig


# ---------------------------------------------------------------- layer workflow

def layer_box(fig, cx, cy, text, kind, w=0.135, h=0.2):
    styles = {
        "input": (L1_FILL, L1_EDGE, "-"),
        "intermediate": ("#f4f4f4", "#8a8a8a", "--"),
        "output": (OUT_FILL, OUT_EDGE, "-"),
    }
    fc, ec, ls = styles[kind]
    fig.patches.append(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, transform=fig.transFigure,
                                      boxstyle="round,pad=0.004,rounding_size=0.012",
                                      fc=fc, ec=ec, lw=2.2, ls=ls, zorder=2))
    fig.text(cx, cy, text, ha="center", va="center", fontsize=15, fontweight="bold", color=INK, zorder=3,
             linespacing=1.25)
    return (cx, cy, w, h)


def op_oval(fig, cx, cy, text, w=0.165, h=0.25):
    fig.patches.append(Ellipse((cx, cy), w, h, transform=fig.transFigure, fc=NAVY, ec=NAVY, zorder=2))
    fig.text(cx, cy, text, ha="center", va="center", fontsize=14, fontweight="bold", color="white",
             zorder=3, linespacing=1.25)
    return (cx, cy, w, h)


def link(fig, a, b):
    fig.patches.append(FancyArrowPatch(a, b, transform=fig.transFigure, arrowstyle="-|>",
                                       mutation_scale=22, lw=2.4, color="#5b6f8a", zorder=1,
                                       shrinkA=0, shrinkB=0))


def fig_layer_workflow():
    fig = plt.figure(figsize=(16, 6.2))
    top, bot = 0.66, 0.27
    in1 = layer_box(fig, 0.08, top, "Input\nlayer", "input")
    op1 = op_oval(fig, 0.255, top, "1st spatial\noperation")
    im1 = layer_box(fig, 0.43, top, "Intermediate\nlayer 1", "intermediate")
    in2 = layer_box(fig, 0.43, bot, "Second\ninput layer", "input")
    op2 = op_oval(fig, 0.605, (top + bot) / 2, "2nd spatial\noperation")
    im2 = layer_box(fig, 0.78, (top + bot) / 2, "Intermediate\nlayer 2", "intermediate")
    op3 = op_oval(fig, 0.78, 0.13, "3rd spatial\noperation", w=0.15, h=0.2)
    out = layer_box(fig, 0.93, 0.13, "Final\noutput", "output", w=0.12, h=0.2)

    def right(o): return (o[0] + o[2] / 2, o[1])
    def left(o): return (o[0] - o[2] / 2, o[1])

    link(fig, right(in1), left(op1))
    link(fig, right(op1), left(im1))
    link(fig, right(im1), (op2[0] - 0.06, op2[1] + 0.08))
    link(fig, right(in2), (op2[0] - 0.06, op2[1] - 0.08))
    link(fig, right(op2), left(im2))
    link(fig, (im2[0], im2[1] - im2[3] / 2), (op3[0], op3[1] + op3[3] / 2))
    link(fig, right(op3), left(out))

    # input counts, so "one input" vs "two inputs" is explicit
    fig.text(op1[0], op1[1] + 0.165, "one input", ha="center", fontsize=13, style="italic", color="#5b6f8a")
    fig.text(op2[0], op2[1] + 0.165, "two inputs", ha="center", fontsize=13, style="italic", color="#5b6f8a")

    # bracket over both intermediate layers
    y = 0.93
    x0, x1 = im1[0] - im1[2] / 2, im2[0] + im2[2] / 2
    fig.add_artist(plt.Line2D([x0, x0, x1, x1], [y - 0.03, y, y, y - 0.03], transform=fig.transFigure,
                              color="#8a8a8a", lw=1.8))
    fig.text((x0 + x1) / 2, y + 0.035, "intermediate layers: made along the way, kept so you can retrace your steps",
             ha="center", va="center", fontsize=14, color="#555555", fontweight="bold")
    return fig


# ---------------------------------------------------------------- dialog annotation

def annotate_dialog(png, rects_json):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(png).convert("RGB")
    r = json.loads(Path(rects_json).read_text())
    a, b = r["INPUT_FIELDS"], r["OVERLAY_FIELDS"]
    pad = 10
    box = (min(a[0], b[0]) - pad, a[1] - pad, max(a[0] + a[2], b[0] + b[2]) + pad, b[1] + b[3] + pad)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=18, outline=RED, width=7)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 40, index=0)
    except OSError:
        font = ImageFont.load_default()
    d.text((box[0] + 330, box[3] + 14), "Leave both empty = keep every field from both layers",
           fill=RED, font=font)
    im = im.crop((20, 30, im.width - 20, 1000))
    out = D22 / "ws-intersection-dialog-qgis.png"
    im.save(out, optimize=True)
    print("wrote", out, im.size)


if __name__ == "__main__":
    save(fig_inputs("counties"), "ws-attr-counties.png")
    save(fig_inputs("catchments"), "ws-attr-catchments.png")
    save(fig_output("intersection"), "ws-attr-intersection.png")
    save(fig_output("union"), "ws-attr-union.png")
    save(fig_layer_workflow(), "ws-workflow-layers.png")
    if len(sys.argv) == 3:
        annotate_dialog(sys.argv[1], sys.argv[2])
