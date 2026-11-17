"""Generate the cookie-cutter site-selection photo series with real Lab 11 geography.

Each step is an image *edit*, not a fresh generation: the previous step's photo goes in as the
first image (so the counter, light, dough and hands carry over), and a flat shape guide drawn from
the real Lab 11 geometry goes in as the second (so the cutter is actually Utah County, the band is
actually the 2-mile buffer around I-15 inside the county, and the round holes sit where the
existing stores are). The guides are drawn by the `guides` step from GeoJSON exported out of the
Lab 11 GeoPackage (tools/lab11_run_analysis.py writes it):

    ogr2ogr -f GeoJSON -t_srs EPSG:26912 county.geojson UtahCounty.gpkg UtahCounty
    ogr2ogr -f GeoJSON -t_srs EPSG:26912 MajorRoads_UTM.geojson UtahCounty.gpkg MajorRoads_UTM
    ogr2ogr -f GeoJSON -t_srs EPSG:26912 WalmartBuffer_utm.geojson UtahCounty.gpkg WalmartBuffer_utm

Only I-15 is buffered for the band (Lab 11 also buffers the highways, which makes a branching
network no cookie cutter can be). Needs shapely, matplotlib, pillow and openai in a venv:

    python tools/generate_cookie_series.py guides <geojson dir> <work dir>
    python tools/generate_cookie_series.py photos <work dir> <step-1 photo> [first step]

The API key comes from OPENAI_API_KEY or ~/.config/openai/api_key and is never printed.
"""

import base64
import json
import os
import sys
from pathlib import Path

MODEL = os.environ.get("COOKIE_MODEL", "gpt-image-2.5-sunburst")
TWO_MILES = 3218.69

STYLE = ("Keep the same photograph: the same light marble countertop dusted with flour, the same pale "
         "sugar cookie dough, the same warm soft window light from the left, the same three-quarter "
         "overhead camera angle and the same white stainless steel cutters. Photorealistic. Hands only, "
         "no faces. No text, labels, maps, lines or drawings anywhere in the photo: the second image is "
         "only a shape reference and must not appear in the result.")

STEPS = [
    ("ws-cookie-2-county-cutter", "guide_county.png",
     "Edit the first photo. Two hands press a large stainless steel cookie cutter down into the rolled-out "
     "dough. The cutter's outline is exactly the dark silhouette in the second image, with the same "
     "proportions and the same orientation (top of the silhouette toward the back of the counter): a "
     "jagged, irregular west and north edge, a narrow tip at the south-west corner, and a long straight "
     "rectangular arm along the south-east. The cutter fits inside the dough with dough showing outside "
     "it on every side."),
    ("ws-cookie-3-county-dough", "guide_county.png",
     "Edit the first photo. The cutter has been lifted off. What remains on the counter is a piece of dough "
     "cut cleanly to exactly the silhouette shape in the second image, same proportions and orientation. "
     "All the dough that was outside the cutter has been gathered into a rough pile of scraps at the edge "
     "of the frame. The same stainless steel cutter, in the same shape, lies on the counter beside the "
     "dough piece. No hands."),
    ("ws-cookie-4-band-cutter", "guide_band.png",
     "Edit the first photo. Put the large cutter away and remove it from the counter; keep the county-shaped "
     "dough piece exactly where and how it is. Two hands press a long, narrow stainless steel cookie cutter "
     "into that dough. The narrow cutter is exactly the dark band in the second image, placed on the dough "
     "exactly where the dark band sits inside the light gray county shape. It does NOT follow the outer "
     "edge of the dough: it cuts through the interior. It starts at the top edge of the dough a little "
     "right of center, runs down and to the right through the middle of the dough, then bends and runs "
     "down and to the left, ending at the bottom edge left of center, with dough on both sides of it the "
     "whole way. Gentle curves and rounded ends, about one eighth as wide as the dough. Only the dough "
     "inside this narrow band will be kept."),
    ("ws-cookie-5-round-cutters", "guide_final.png",
     "Edit the first photo. The county-shaped dough has been trimmed: only the long, narrow, diagonal strip "
     "of dough that was inside the band cutter remains, exactly the shape of the band (the gray and dark "
     "areas together) in the second image; the rest of the dough has been cleared away. Several small round "
     "stainless steel cookie cutters, all the same size, are being pressed into the strip at the places "
     "marked by the red circles in the second image: a cluster of overlapping circles near the top, and "
     "more spread down the strip. One hand presses a round cutter in; the others sit in the dough."),
    ("ws-cookie-6-result", "guide_final.png",
     "Edit the first photo. All the round cutters have been lifted out and set in a small group beside the "
     "strip, with the little round discs of dough they punched out in a pile next to them. The strip now "
     "has round holes and round bites cut out of it exactly where the red circles are in the second image, "
     "so what remains matches the dark shape in the second image. No hands. Seen slightly from above, like "
     "the final shot of a recipe."),
]


def guides(geo_dir, work):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from shapely.geometry import shape
    from shapely.ops import unary_union

    geo, work = Path(geo_dir), Path(work)
    work.mkdir(parents=True, exist_ok=True)

    def load(name, keep=lambda f: True):
        feats = json.loads((geo / name).read_text())["features"]
        return unary_union([shape(f["geometry"]).buffer(0) for f in feats if keep(f)])

    county = load("county.geojson")
    i15 = load("MajorRoads_UTM.geojson", lambda f: (f["properties"].get("DOT_HWYNAM") or "").strip() == "I-15")
    stores = load("WalmartBuffer_utm.geojson")
    band = i15.buffer(TWO_MILES).intersection(county)
    final = band.difference(stores)

    minx, miny, maxx, maxy = county.bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    h = (maxy - miny) / 0.82
    w = h * 1.5

    def fill(ax, g, fc, ec="none", lw=0, z=1):
        for p in getattr(g, "geoms", [g]):
            x, y = p.exterior.xy
            ax.fill(x, y, fc=fc, ec=ec, lw=lw, zorder=z)
            for hole in p.interiors:
                ax.fill(*hole.xy, fc="white", ec=ec, lw=lw, zorder=z)

    def canvas():
        f = plt.figure(figsize=(15.36, 10.24), dpi=100)
        ax = f.add_axes([0, 0, 1, 1])
        ax.set_xlim(cx - w / 2, cx + w / 2)
        ax.set_ylim(cy - h / 2, cy + h / 2)
        ax.set_aspect("equal")
        ax.axis("off")
        return f, ax

    f, ax = canvas(); fill(ax, county, "#333333"); f.savefig(work / "guide_county.png"); plt.close(f)
    f, ax = canvas(); fill(ax, county, "#dddddd", "#999999", 1.5); fill(ax, band, "#333333", z=2)
    f.savefig(work / "guide_band.png"); plt.close(f)
    f, ax = canvas(); fill(ax, county, "#f2f2f2", "#cccccc", 1); fill(ax, band, "#bbbbbb", z=2); fill(ax, final, "#333333", z=3)
    for p in getattr(stores, "geoms", [stores]):
        x, y = p.exterior.xy
        ax.plot(x, y, color="#c8102e", lw=2, zorder=4)
    f.savefig(work / "guide_final.png"); plt.close(f)
    print("guides written to", work)


def api_key():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        p = Path.home() / ".config/openai/api_key"
        key = p.read_text().strip() if p.exists() else None
    if not key:
        sys.exit("No OpenAI key: set OPENAI_API_KEY or write ~/.config/openai/api_key")
    return key


def photos(work, first_photo, start=None):
    from openai import OpenAI
    client = OpenAI(api_key=api_key())
    work = Path(work)
    prev = Path(first_photo)
    log = []
    begin = False if start else True
    for name, guide, prompt in STEPS:
        out = work / f"{name}.png"
        if not begin:
            if name == start:
                begin = True
            else:
                prev = out
                continue
        full = prompt + " " + STYLE
        with open(prev, "rb") as a, open(work / guide, "rb") as b:
            r = client.images.edit(model=MODEL, image=[a, b], prompt=full, size="1536x1024", quality="high")
        out.write_bytes(base64.b64decode(r.data[0].b64_json))
        log.append({"id": name, "model": MODEL, "input": prev.name, "guide": guide, "prompt": full})
        print("wrote", out, flush=True)
        prev = out
    (work / "series-manifest.json").write_text(json.dumps(log, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "guides":
        guides(sys.argv[2], sys.argv[3])
    else:
        photos(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
