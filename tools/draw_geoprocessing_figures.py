"""Draw the geoprocessing concept figures for the Day 18 and Day 22 decks.

These replace figures that came from Bolstad's *GIS Fundamentals* and the Esri tool help, so the
decks no longer reproduce copyrighted art. Every shape and raster here is synthetic: random but
seeded, so a rerun gives identical images. Nothing is real data, and the figures say so by not
naming any real place.

Needs shapely 2, matplotlib and numpy (not in the QGIS bundle; use a venv):

    python3 -m venv /tmp/gpvenv && /tmp/gpvenv/bin/pip install shapely matplotlib numpy
    /tmp/gpvenv/bin/python tools/draw_geoprocessing_figures.py

Writes PNGs into slides/day-18/images/ and slides/day-22/images/ (each deck keeps its own copy,
because nothing references an image outside its own folder).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import FancyArrowPatch, Patch
from shapely import contains_xy
from shapely.affinity import scale, translate
from shapely.geometry import LineString, MultiPoint, Point, Polygon, box
from shapely.ops import split, unary_union, voronoi_diagram

ROOT = Path(__file__).resolve().parent.parent
D18 = ROOT / "slides/day-18/images"
D22 = ROOT / "slides/day-22/images"

NAVY = "#002e5d"
INK = "#333333"
L1_FILL, L1_EDGE = "#cfdcec", "#5b6f8a"     # first input layer: counties, rectangle
L2_FILL, L2_EDGE = "#f6c48b", "#c06a15"     # second input layer: catchment, circle
OUT_FILL, OUT_EDGE = "#9fd08f", "#3f7a3a"   # output
PASTELS = ["#f7c6c7", "#c6dbef", "#d9f0d3", "#fde0a8", "#e3d0f0", "#c7eae5",
           "#fbd5e8", "#e6e6b8", "#d0e1f9", "#f9d9c3", "#d5f5e3", "#ead1dc"]

plt.rcParams.update({
    "font.family": ["Avenir Next", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 13,
    "text.color": INK,
})


# ---------------------------------------------------------------- geometry helpers

def draw(ax, geom, fc, ec, lw=1.0, alpha=1.0, ls="-", z=1):
    if geom.is_empty:
        return
    if geom.geom_type in ("Polygon", "MultiPolygon", "GeometryCollection"):
        parts = getattr(geom, "geoms", [geom])
        for g in parts:
            if g.geom_type == "Polygon":
                x, y = g.exterior.xy
                ax.fill(x, y, fc=fc, ec="none", alpha=alpha, zorder=z)
                for hole in g.interiors:
                    hx, hy = hole.xy
                    ax.fill(hx, hy, fc="white", ec="none", zorder=z)
                ax.plot(x, y, color=ec, lw=lw, ls=ls, zorder=z + 0.1)
                for hole in g.interiors:
                    hx, hy = hole.xy
                    ax.plot(hx, hy, color=ec, lw=lw, ls=ls, zorder=z + 0.1)
            elif g.geom_type == "MultiPolygon":
                draw(ax, g, fc, ec, lw, alpha, ls, z)
    elif geom.geom_type in ("LineString", "MultiLineString"):
        for g in getattr(geom, "geoms", [geom]):
            x, y = g.xy
            ax.plot(x, y, color=ec, lw=lw, ls=ls, zorder=z)
    elif geom.geom_type in ("Point", "MultiPoint"):
        for g in getattr(geom, "geoms", [geom]):
            ax.plot(g.x, g.y, "o", color=ec, ms=5, zorder=z)


def frame(ax, title, bounds):
    ax.set_aspect("equal")
    ax.axis("off")
    minx, miny, maxx, maxy = bounds
    pad = 0.04 * max(maxx - minx, maxy - miny)
    ax.set_xlim(minx - pad, maxx + pad)
    ax.set_ylim(miny - pad, maxy + pad)
    if title:
        ax.set_title(title, color=NAVY, fontsize=16, fontweight="bold", pad=8)


def smooth_blob(cx, cy, r, wobble, n, seed):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 2 * np.pi, 200, endpoint=False)
    rr = np.full_like(t, r)
    for k in range(2, 2 + n):
        rr += wobble * r * rng.uniform(-1, 1) / k * np.cos(k * t + rng.uniform(0, 2 * np.pi))
    return Polygon(np.c_[cx + rr * np.cos(t), cy + rr * np.sin(t)])


def region():
    """A state-shaped study area: a box with one ragged coast."""
    rng = np.random.default_rng(7)
    xs = np.linspace(0, 10, 40)
    bottom = 0.35 * np.sin(xs * 1.3) + rng.normal(0, 0.08, xs.size)
    pts = [(0, 7), (10, 7)] + list(zip(xs[::-1], bottom[::-1]))
    return Polygon(pts).buffer(0)


def counties(reg, n=22, seed=3):
    rng = np.random.default_rng(seed)
    minx, miny, maxx, maxy = reg.bounds
    pts = MultiPoint(np.c_[rng.uniform(minx, maxx, n), rng.uniform(miny, maxy, n)])
    cells = voronoi_diagram(pts, envelope=box(-5, -5, 15, 12))
    return [c.intersection(reg) for c in cells.geoms if not c.intersection(reg).is_empty]


def catchment():
    river = LineString([(1.2, 6.4), (2.6, 5.2), (3.8, 4.6), (5.0, 3.4), (6.4, 2.6), (8.2, 1.0)])
    shape = river.buffer(1.05, quad_segs=16)
    return unary_union([shape, smooth_blob(2.0, 5.6, 1.1, 0.25, 4, 11)]).simplify(0.02)


def subcatchments(c):
    cuts = [LineString([(2.0, 3.0), (5.2, 6.5)]), LineString([(4.6, 0.8), (7.6, 4.2)])]
    parts = [c]
    for cut in cuts:
        nxt = []
        for p in parts:
            nxt.extend(split(p, cut).geoms)
        parts = nxt
    return sorted(parts, key=lambda p: -p.centroid.y)


def arrow(fig, x0, x1, y, label=None):
    fig.patches.append(FancyArrowPatch((x0, y), (x1, y), transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=28, lw=2.5, color=NAVY))
    if label:
        fig.text((x0 + x1) / 2, y + 0.05, label, ha="center", va="bottom",
                 fontsize=13, color=NAVY, fontweight="bold")


def save(fig, name, folders):
    for folder in folders:
        fig.savefig(folder / name, dpi=200, facecolor="white")
    plt.close(fig)
    print("wrote", name, "->", ", ".join(f.parent.name for f in folders))


def three_panel(figsize=(10, 3.9)):
    fig = plt.figure(figsize=figsize)
    axes = [fig.add_axes([0.02, 0.06, 0.27, 0.8]),
            fig.add_axes([0.37, 0.06, 0.27, 0.8]),
            fig.add_axes([0.72, 0.06, 0.27, 0.8])]
    return fig, axes


# ---------------------------------------------------------------- figures

def fig_reclassify(kind):
    reg = region()
    ny, nx = 70, 100
    xs, ys = np.meshgrid(np.linspace(0, 10, nx), np.linspace(0, 7, ny))
    rng = np.random.default_rng(21 if kind == "wind" else 33)
    field = np.zeros_like(xs)
    if kind == "wind":
        # windy along the coast and on two ridges
        field += 4.5 * np.exp(-((ys - 0.6) ** 2) / 1.2)
        for _ in range(2):
            cx, cy = rng.uniform(2, 8), rng.uniform(3.5, 6)
            field += 3.5 * np.exp(-((xs - cx) ** 2 / 2.5 + (ys - cy) ** 2 / 0.3))
        field = np.clip(np.round(1 + field + rng.normal(0, 0.18, field.shape)), 1, 7)
        bounds = np.arange(0.5, 8.5, 1)
        cin = ListedColormap(plt.cm.Blues(np.linspace(0.12, 0.95, 7)))
        in_title, in_legend = "Wind speed", [str(i) for i in range(1, 8)]
        thresh, lo, hi = 4, "low", "high"
        rule = "< 4  →  low\n≥ 4  →  high"
        out_title = "Wind class"
    else:
        # a few towns and one city; people per unit area
        for _ in range(7):
            cx, cy = rng.uniform(1, 9), rng.uniform(0.8, 6.2)
            field += rng.uniform(15, 120) * np.exp(-((xs - cx) ** 2 + (ys - cy) ** 2) / rng.uniform(0.15, 0.6))
        field += 260 * np.exp(-((xs - 6.8) ** 2 + (ys - 1.6) ** 2) / 0.9)
        field += rng.gamma(1.5, 1.2, field.shape)
        bounds = np.array([0, 2, 5, 10, 25, 50, 250, 1000])
        cin = ListedColormap(plt.cm.Greys(np.linspace(0.08, 0.95, 7)))
        in_title = "Population density"
        in_legend = ["0–2", "2–5", "5–10", "10–25", "25–50", "50–250", "250+"]
        thresh, lo, hi = 10, "sparse", "dense"
        rule = "< 10  →  sparse\n≥ 10  →  dense"
        out_title = "Population class"

    inside = contains_xy(reg, xs, ys)
    data = np.where(inside, field, np.nan)
    out = np.where(inside, (field >= thresh).astype(float), np.nan)

    fig = plt.figure(figsize=(10, 3.4))
    a1 = fig.add_axes([0.0, 0.04, 0.31, 0.8])
    a2 = fig.add_axes([0.57, 0.04, 0.31, 0.8])
    ext = (0, 10, 0, 7)
    a1.imshow(data, origin="lower", extent=ext, cmap=cin, norm=BoundaryNorm(bounds, cin.N),
              interpolation="nearest")
    cout = ListedColormap(["#e9eef5", "#1f4e85"] if kind == "wind" else ["#eeeeee", "#444444"])
    a2.imshow(out, origin="lower", extent=ext, cmap=cout, vmin=0, vmax=1, interpolation="nearest")
    for a, t in ((a1, in_title), (a2, out_title)):
        draw(a, reg.boundary, "none", "#555555", lw=1)
        frame(a, t, reg.bounds)
    a1.legend(handles=[Patch(fc=cin(i), ec="#777777", label=l) for i, l in enumerate(in_legend)],
              loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=9, frameon=False,
              handlelength=1.2, borderaxespad=0.2)
    a2.legend(handles=[Patch(fc=cout(0), ec="#777777", label=lo), Patch(fc=cout(1), ec="#777777", label=hi)],
              loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=10, frameon=False,
              handlelength=1.2, borderaxespad=0.2)
    arrow(fig, 0.41, 0.55, 0.46)
    fig.text(0.48, 0.60, "Reclassify", ha="center", fontsize=14, fontweight="bold", color=NAVY)
    fig.text(0.48, 0.34, rule, ha="center", va="top", fontsize=10, family="monospace",
             bbox=dict(boxstyle="round,pad=0.5", fc="#fff8ee", ec=L2_EDGE))
    return fig


def fig_buffer():
    rng = np.random.default_rng(5)
    pts = [Point(p) for p in [(0.6, 3.2), (1.6, 3.9), (1.2, 1.4), (2.9, 2.6), (3.3, 0.7), (2.1, 2.3)]]
    lines = [LineString([(0.3, 3.9), (1.4, 2.8), (2.0, 1.5), (3.6, 0.5)]),
             LineString([(1.4, 2.8), (2.7, 3.7), (3.6, 3.9)]),
             LineString([(2.0, 1.5), (3.1, 2.1)]),
             LineString([(0.4, 1.0), (1.0, 1.6), (2.0, 1.5)])]
    polys = [smooth_blob(1.2, 3.0, 0.75, 0.3, 4, 1), smooth_blob(2.8, 1.2, 0.55, 0.3, 4, 2),
             smooth_blob(0.8, 0.9, 0.35, 0.3, 4, 3)]
    d = 0.35
    fig = plt.figure(figsize=(10, 5.6))
    cols = [("Points", pts), ("Lines", lines), ("Polygons", polys)]
    for i, (name, geoms) in enumerate(cols):
        top = fig.add_axes([0.13 + i * 0.29, 0.52, 0.26, 0.38])
        bot = fig.add_axes([0.13 + i * 0.29, 0.04, 0.26, 0.38])
        for g in geoms:
            if name == "Polygons":
                draw(top, g, L1_FILL, L1_EDGE, lw=1.2)
            else:
                draw(top, g, "none", L1_EDGE, lw=2)
        for g in geoms:
            draw(bot, g.buffer(d, quad_segs=24), L2_FILL, L2_EDGE, lw=1.2, alpha=0.7, z=1)
        for g in geoms:
            if name == "Polygons":
                draw(bot, g, L1_FILL, L1_EDGE, lw=1.2, z=3)
            else:
                draw(bot, g, "none", L1_EDGE, lw=2, z=3)
        b = (-0.1, 0.1, 4.0, 4.3)
        frame(top, name, b)
        frame(bot, None, b)
    fig.text(0.07, 0.71, "Input", ha="center", va="center", fontsize=15, fontweight="bold", color=NAVY)
    fig.text(0.07, 0.23, "Buffer\noutput", ha="center", va="center", fontsize=15, fontweight="bold", color=NAVY)
    return fig


def fig_difference():
    reg = region()
    cs = counties(reg)
    c = catchment().intersection(reg)
    fig, (a1, a2, a3) = three_panel(figsize=(10, 3.6))
    for g in cs:
        draw(a1, g, L1_FILL, L1_EDGE, lw=0.8)
    draw(a2, reg, "#f4f4f4", "#bbbbbb", lw=0.8, ls="--")
    draw(a2, c, L2_FILL, L2_EDGE, lw=1.2, z=2)
    for g in cs:
        draw(a3, g.difference(c), OUT_FILL, OUT_EDGE, lw=0.8)
    draw(a3, c.boundary, "none", L2_EDGE, lw=1.2, ls="--", z=3)
    for a, t in ((a1, "Counties"), (a2, "Catchment"), (a3, "Counties minus catchment")):
        frame(a, t, reg.bounds)
    fig.text(0.33, 0.46, "–", ha="center", va="center", fontsize=34, color=NAVY, fontweight="bold")
    arrow(fig, 0.655, 0.71, 0.46)
    return fig


def fig_intersection():
    reg = region()
    cs = counties(reg)
    subs = subcatchments(catchment().intersection(reg))
    names = ["A", "B", "C"]
    fig = plt.figure(figsize=(10, 4.4))
    a1 = fig.add_axes([0.02, 0.36, 0.27, 0.56])
    a2 = fig.add_axes([0.37, 0.36, 0.27, 0.56])
    a3 = fig.add_axes([0.72, 0.36, 0.27, 0.56])
    for i, g in enumerate(cs):
        draw(a1, g, L1_FILL, L1_EDGE, lw=0.8)
    draw(a2, reg, "#f4f4f4", "#bbbbbb", lw=0.8, ls="--")
    tones = ["#f8d3a6", "#f2a65a", "#d9822b"]
    for g, n, t in zip(subs, names, tones):
        draw(a2, g, t, L2_EDGE, lw=1.2, z=2)
        p = g.representative_point()
        a2.text(p.x, p.y, n, ha="center", va="center", fontsize=13, fontweight="bold", color="white", zorder=5)
    draw(a3, reg, "none", "#cccccc", lw=0.8, ls="--")
    pieces = []
    for ci, cg in enumerate(cs):
        for si, sg in enumerate(subs):
            x = cg.intersection(sg)
            if x.area > 0.02:
                pieces.append((ci + 1, names[si], x))
    for k, (_, _, x) in enumerate(pieces):
        draw(a3, x, PASTELS[k % len(PASTELS)], "#555555", lw=0.8)
    for a, t in ((a1, "Counties"), (a2, "Catchments"), (a3, "Intersection")):
        frame(a, t, reg.bounds)
    fig.text(0.33, 0.64, "+", ha="center", va="center", fontsize=30, color=NAVY, fontweight="bold")
    arrow(fig, 0.655, 0.71, 0.64)

    # a few rows of the output attribute table, keyed to numbered pieces
    show = sorted(pieces, key=lambda p: -p[2].area)[:4]
    for n, (cid, sname, x) in enumerate(show, 1):
        p = x.representative_point()
        a3.text(p.x, p.y, str(n), ha="center", va="center", fontsize=10, fontweight="bold",
                color=NAVY, zorder=6, bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec=NAVY, lw=0.8))
    tab = fig.add_axes([0.58, 0.01, 0.41, 0.30])
    tab.axis("off")
    rows = [[str(n), f"County {cid}", f"Catchment {s}"] for n, (cid, s, _) in enumerate(show, 1)]
    t = tab.table(cellText=rows, colLabels=["piece", "county", "catchment"], loc="center",
                  cellLoc="center", colColours=["#e8eef6"] * 3)
    t.auto_set_font_size(False)
    t.set_fontsize(13)
    t.scale(1, 1.5)
    fig.text(0.555, 0.17, "Output table:\nattributes of both", ha="right", va="center", fontsize=13, color=INK)
    return fig


def fig_union():
    reg = region()
    cs = counties(reg)
    circle = Point(8.6, 4.2).buffer(2.1, quad_segs=32)
    fig = plt.figure(figsize=(10, 4.0))
    a1 = fig.add_axes([0.02, 0.12, 0.27, 0.74])
    a2 = fig.add_axes([0.37, 0.12, 0.27, 0.74])
    a3 = fig.add_axes([0.72, 0.12, 0.27, 0.74])
    for g in cs:
        draw(a1, g, L1_FILL, L1_EDGE, lw=0.8)
    draw(a2, reg, "#f4f4f4", "#bbbbbb", lw=0.8, ls="--")
    draw(a2, circle, L2_FILL, L2_EDGE, lw=1.2, z=2)
    for g in cs:
        draw(a3, g.difference(circle), L1_FILL, OUT_EDGE, lw=0.8)
        draw(a3, g.intersection(circle), OUT_FILL, OUT_EDGE, lw=0.8)
    draw(a3, circle.difference(reg), L2_FILL, OUT_EDGE, lw=0.8)
    b = reg.union(circle).bounds
    for a, t in ((a1, "Counties"), (a2, "Circle"), (a3, "Union")):
        frame(a, t, b)
    fig.legend(handles=[Patch(fc=OUT_FILL, ec=OUT_EDGE, label="in both"),
                        Patch(fc=L1_FILL, ec=OUT_EDGE, label="county only"),
                        Patch(fc=L2_FILL, ec=OUT_EDGE, label="circle only")],
               loc="lower right", bbox_to_anchor=(0.99, 0.0), ncol=3, fontsize=10, frameon=False,
               handlelength=1.2, columnspacing=0.8)
    fig.text(0.33, 0.48, "+", ha="center", va="center", fontsize=30, color=NAVY, fontweight="bold")
    arrow(fig, 0.655, 0.71, 0.48)
    return fig


def simple_inputs():
    rect = box(0, 1, 4, 3.6)
    left, right = box(0, 1, 2, 3.6), box(2, 1, 4, 3.6)
    circle = Point(2.0, 1.1).buffer(1.25, quad_segs=48)
    return rect, left, right, circle


def fig_simple(kind):
    _, left, right, circle = simple_inputs()
    fig = plt.figure(figsize=(9, 3.6))
    a1 = fig.add_axes([0.03, 0.05, 0.38, 0.8])
    a2 = fig.add_axes([0.59, 0.05, 0.38, 0.8])
    for g in (left, right):
        draw(a1, g, L1_FILL, L1_EDGE, lw=1.5)
    draw(a1, circle, L2_FILL, L2_EDGE, lw=1.5, alpha=0.75, z=2)
    a1.text(1.0, 3.2, "input", ha="center", fontsize=11, color=L1_EDGE)
    a1.text(2.0, -0.4, "overlay", ha="center", fontsize=11, color=L2_EDGE)
    if kind == "intersection":
        for g in (left, right):
            draw(a2, g.intersection(circle), OUT_FILL, OUT_EDGE, lw=1.5)
        for g in (left, right):
            draw(a2, g, "none", "#cccccc", lw=0.8, ls="--", z=0)
        draw(a2, circle, "none", "#cccccc", lw=0.8, ls="--", z=0)
        title = "Intersection: in both"
    else:
        for g in (left, right):
            draw(a2, g.difference(circle), OUT_FILL, OUT_EDGE, lw=1.5)
            draw(a2, g.intersection(circle), OUT_FILL, OUT_EDGE, lw=1.5)
        draw(a2, circle.difference(box(0, 1, 4, 3.6)), OUT_FILL, OUT_EDGE, lw=1.5)
        title = "Union: in either"
    b = (-0.2, -0.5, 4.2, 3.7)
    frame(a1, "Inputs", b)
    frame(a2, title, b)
    arrow(fig, 0.44, 0.56, 0.45)
    return fig


def fig_summary():
    _, _, _, circle = simple_inputs()
    rect = box(0, 1, 4, 3.6)
    fig = plt.figure(figsize=(10, 3.4))
    specs = [("In both?", "Intersection", rect.intersection(circle)),
             ("In either?", "Union", rect.union(circle)),
             ("In this but not that?", "Difference", rect.difference(circle))]
    for i, (q, tool, res) in enumerate(specs):
        a = fig.add_axes([0.02 + i * 0.335, 0.2, 0.3, 0.62])
        draw(a, rect, "none", L1_EDGE, lw=1, ls="--", z=0)
        draw(a, circle, "none", L2_EDGE, lw=1, ls="--", z=0)
        draw(a, res, OUT_FILL, OUT_EDGE, lw=1.6, z=2)
        frame(a, q, (-0.2, -0.3, 4.2, 3.7))
        fig.text(0.02 + i * 0.335 + 0.15, 0.08, tool, ha="center", fontsize=15, fontweight="bold", color=NAVY)
    return fig


def fig_units():
    """The same 10 typed into Buffer, for a layer in degrees and for one in meters."""
    reg = scale(region(), 0.6, 0.6, origin=(0, 0))         # about 6 x 4 degrees, roughly a state
    town = Point(2.6, 2.1)
    fig = plt.figure(figsize=(10, 3.9))
    a1 = fig.add_axes([0.03, 0.04, 0.42, 0.8])
    a2 = fig.add_axes([0.55, 0.04, 0.42, 0.8])
    for a in (a1, a2):
        draw(a, reg, L1_FILL, L1_EDGE, lw=1.2)
    draw(a1, town.buffer(10, quad_segs=64), L2_FILL, L2_EDGE, lw=1.5, alpha=0.55, z=2)
    # 10 km at roughly 111 km per degree
    draw(a2, town.buffer(10 / 111, quad_segs=64).buffer(0.0), L2_FILL, L2_EDGE, lw=1.5, z=2)
    for a in (a1, a2):
        draw(a, town, "none", NAVY, z=4)
    a2.annotate("10 km", (town.x + 0.05, town.y + 0.05), (town.x + 0.9, town.y + 0.9), fontsize=13,
                color=L2_EDGE, fontweight="bold", arrowprops=dict(arrowstyle="-", color=L2_EDGE))
    a1.text(2.6, -5.5, "the whole state, and far beyond", ha="center", fontsize=12, color=L2_EDGE,
            fontweight="bold", zorder=5)
    a1.text(3.0, 3.1, "state", ha="center", va="center", fontsize=11, color=L1_EDGE, zorder=5)
    frame(a1, "Layer in degrees: 10 means 10°", (-7.6, -8.0, 12.8, 12.2))
    frame(a2, "Reprojected to meters: 10 km", (-0.2, -0.3, 6.2, 4.5))
    return fig


def fig_title():
    """The intersection output on its own, square, for the title slide."""
    reg = region()
    cs = counties(reg)
    subs = subcatchments(catchment().intersection(reg))
    fig = plt.figure(figsize=(6, 6))
    a = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    for g in cs:
        draw(a, g, "#eef2f7", "#9aa9bd", lw=0.8)
    k = 0
    for cg in cs:
        for sg in subs:
            x = cg.intersection(sg)
            if x.area > 0.02:
                draw(a, x, PASTELS[k % len(PASTELS)], "#555555", lw=1.0, z=2)
                k += 1
    frame(a, None, (1.0, 0.6, 9.0, 7.0))
    return fig


if __name__ == "__main__":
    both = [D18, D22]
    save(fig_reclassify("wind"), "gp-reclassify-wind.png", [D18])
    save(fig_reclassify("pop"), "gp-reclassify-pop.png", [D18])
    save(fig_reclassify("wind"), "ws-reclassify-wind.png", [D22])
    save(fig_reclassify("pop"), "ws-reclassify-population.png", [D22])
    save(fig_buffer(), "gp-buffer-vector.png", [D18])
    save(fig_buffer(), "ws-buffer-types.png", [D22])
    save(fig_difference(), "gp-difference-counties.png", [D18])
    save(fig_difference(), "ws-erase-catchment.png", [D22])
    save(fig_intersection(), "gp-intersection-counties.png", [D18])
    save(fig_intersection(), "ws-intersect-catchments.png", [D22])
    save(fig_union(), "gp-union-counties.png", [D18])
    save(fig_simple("intersection"), "ws-intersect-simple.png", [D22])
    save(fig_summary(), "gp-overlay-summary.png", [D18])
    save(fig_title(), "gp-title-overlay.png", [D18])
    save(fig_units(), "gp-reproject-units.png", [D18])
