"""Build the animated "One state, two UTM zones" map for the Day 14 projections deck.

Draws Idaho and its neighbors in NAD83 / Idaho Transverse Mercator (EPSG:8826), with the UTM
zone boundaries at 120, 114 and 108 degrees west. When the slide opens, the IDTM zone grows
outward from its central meridian (114 W, the same line UTM splits the state on) and the
Tater Mercator badge pops in alongside it. The animation only runs under Marp's bespoke
`.bespoke-marp-active` class, so static exports show the finished state.

State outlines come from the Natural Earth layer that ships with QGIS, so nothing is
downloaded. Needs pyproj, pyogrio and shapely (a scratch venv is fine):

    python tools/make_idaho_utm_svg.py > /tmp/idaho.svg

then paste the output between the `idaho-utm:begin` and `idaho-utm:end` markers in
slides/day-14/coordinate-systems-and-projections.md.
"""

import numpy as np
import shapely
from pyogrio.raw import read
from pyproj import Transformer

GPKG = "/Applications/QGIS.app/Contents/Resources/qgis/resources/data/world_map.gpkg"
W, H = 620, 560                    # SVG size in px
LON0, LON1, LAT0, LAT1 = -121.5, -105.5, 40.3, 49.8
TO_IDTM = Transformer.from_crs(4326, 8826, always_xy=True)

_, _, wkb, fields = read(GPKG, layer="states_provinces", where="adm0_a3='USA'", columns=["name"])
names = list(fields[0])
geoms = shapely.from_wkb(wkb)
box = shapely.box(LON0, LAT0, LON1, LAT1)


def project(g):
    return shapely.transform(g, lambda xy: np.column_stack(TO_IDTM.transform(xy[:, 0], xy[:, 1])))


# Fit the projected view box to the SVG.
frame = project(shapely.segmentize(box, 0.1))
fx0, fy0, fx1, fy1 = frame.bounds
scale = min(W / (fx1 - fx0), H / (fy1 - fy0))
ox = (W - (fx1 - fx0) * scale) / 2
oy = (H - (fy1 - fy0) * scale) / 2


def px(x, y):
    return ox + (x - fx0) * scale, oy + (fy1 - y) * scale


def path(g):
    out = []
    polys = g.geoms if hasattr(g, "geoms") else [g]
    for p in polys:
        if p.is_empty or p.geom_type != "Polygon":
            continue
        for ring in [p.exterior, *p.interiors]:
            pts = [px(x, y) for x, y in ring.coords]
            out.append("M" + "L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + "Z")
    return "".join(out)


def meridian(lon):
    lats = np.linspace(LAT0, LAT1, 40)
    xs, ys = TO_IDTM.transform(np.full_like(lats, lon), lats)
    return "M" + "L".join(f"{a:.1f},{b:.1f}" for a, b in (px(x, y) for x, y in zip(xs, ys)))


states, idaho = [], None
for name, g in zip(names, geoms):
    clipped = shapely.intersection(g, box)
    if clipped.is_empty:
        continue
    d = path(project(shapely.simplify(clipped, 0.01)))
    if name == "Idaho":
        idaho = project(clipped)
        idaho_d = d
    else:
        states.append(d)

# IDTM zone: a band symmetric about 114 W that covers the whole state.
cm_x, _ = TO_IDTM.transform(-114, 45)
ix0, iy0, ix1, iy1 = idaho.bounds
half = max(cm_x - ix0, ix1 - cm_x) * 1.04
bx0, by1 = px(cm_x - half, iy1)
bx1, by0 = px(cm_x + half, iy0)
by1 -= 10
by0 += 10
cmx_px, _ = px(cm_x, 0)


def label_at(lon, lat):
    return px(*TO_IDTM.transform(lon, lat))


z11 = label_at(-117, 40.75)
z12 = label_at(-111, 40.75)
z13 = label_at(-107, 40.75)

badge_w = 150
badge_h = badge_w * 477 / 520
badge_x, badge_y = W - badge_w - 14, 14

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="inherit"><style>
.id-band,.id-badge,.id-tag{{transform-box:fill-box;transform-origin:center}}
.bespoke-marp-active .id-band{{animation:id-grow 1.4s cubic-bezier(.2,.8,.2,1) .8s both}}
.bespoke-marp-active .id-cm{{animation:id-draw 1.4s ease-out .8s both}}
.bespoke-marp-active .id-tag{{animation:id-fade .6s ease-out 2s both}}
.bespoke-marp-active .id-badge{{animation:id-pop 1.1s cubic-bezier(.3,1.6,.5,1) .8s both}}
@keyframes id-grow{{from{{transform:scaleX(0);opacity:0}}to{{transform:scaleX(1);opacity:1}}}}
@keyframes id-draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@keyframes id-fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes id-pop{{0%{{transform:scale(0) rotate(-30deg);opacity:0}}100%{{transform:scale(1) rotate(-5deg);opacity:1}}}}
@media (prefers-reduced-motion:reduce){{.bespoke-marp-active .id-band,.bespoke-marp-active .id-cm,.bespoke-marp-active .id-tag,.bespoke-marp-active .id-badge{{animation:none}}}}
</style>
<defs><clipPath id="id-badge-clip"><rect x="{badge_x:.0f}" y="{badge_y:.0f}" width="{badge_w}" height="{badge_h:.0f}" rx="14"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="14" fill="#f4f7fa"/>
<path d="{"".join(states)}" fill="#e3e8ee" stroke="#ffffff" stroke-width="1.5"/>
<path d="{idaho_d}" fill="#c9dcef" stroke="#002e5d" stroke-width="2.5" stroke-linejoin="round"/>
<g fill="none" stroke="#5a6b7d" stroke-width="2" stroke-dasharray="7 6">
<path d="{meridian(-120)}"/><path d="{meridian(-114)}"/><path d="{meridian(-108)}"/>
</g>
<g font-size="17" font-weight="700" fill="#5a6b7d" text-anchor="middle">
<text x="{z11[0]:.0f}" y="{z11[1]:.0f}">UTM 11</text>
<text x="{z12[0]:.0f}" y="{z12[1]:.0f}">UTM 12</text><text x="{z13[0]:.0f}" y="{z13[1]:.0f}">UTM 13</text>
</g>
<rect class="id-band" x="{bx0:.1f}" y="{by1:.1f}" width="{bx1 - bx0:.1f}" height="{by0 - by1:.1f}" rx="6" fill="#e8590c" fill-opacity="0.16" stroke="#e8590c" stroke-width="3" stroke-dasharray="10 6"/>
<path class="id-cm" d="{meridian(-114)}" pathLength="1" stroke-dasharray="1" fill="none" stroke="#c92a2a" stroke-width="4"/>
<g class="id-tag" font-weight="700" text-anchor="middle">
<text x="{cmx_px:.0f}" y="{by1 - 10:.0f}" font-size="19" fill="#c92a2a">IDTM, centered on 114° W</text>
</g>
<g class="id-badge"><image href="images/crs-tater-mercator-badge.jpg" x="{badge_x:.0f}" y="{badge_y:.0f}" width="{badge_w}" height="{badge_h:.0f}" clip-path="url(#id-badge-clip)" preserveAspectRatio="xMidYMid slice"/>
<rect x="{badge_x:.0f}" y="{badge_y:.0f}" width="{badge_w}" height="{badge_h:.0f}" rx="14" fill="none" stroke="#ffffff" stroke-width="5"/></g>
</svg>'''

print(svg.replace("\n", ""))  # one line, so Markdown keeps it a single HTML block
