"""Draw the two Day 6 decimal-place figures as SVG.

  gps-quiz-two-pins.svg      two phones showing Pin A and Pin B, for the quiz slide
  gps-digit-ladder.svg       the same two latitudes digit by digit, with what one step in each
                             digit is worth, and the first digit that differs highlighted

Distances are for latitude: 1 degree is about 111 km, and each decimal place divides by 10.
Usage: python3 tools/make_decimal_place_svgs.py slides/day-06/images
"""
import sys, pathlib

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "slides/day-06/images")
NAVY, BLUE, INK, GRAY, LINE, PALE, ORANGE, ORANGE_PALE = (
    "#002e5d", "#0062b8", "#22262e", "#8a94a3", "#c9d8ea", "#eef3f9", "#e07b39", "#fbe7d9")
SANS = "Avenir Next, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "Menlo, Consolas, DejaVu Sans Mono, monospace"

PIN_A = "40.25132"
PIN_B = "40.26132"
LON = "111.64930"


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>\n{body}</svg>\n')


def pin(x, y, s, color):
    """A map pin whose point sits at (x, y)."""
    return (f'<path d="M{x},{y} C{x - 0.55*s},{y - 0.9*s} {x - s},{y - 1.25*s} {x - s},{y - 1.75*s} '
            f'A{s},{s} 0 1 1 {x + s},{y - 1.75*s} C{x + s},{y - 1.25*s} {x + 0.55*s},{y - 0.9*s} {x},{y} Z" '
            f'fill="{color}"/>\n<circle cx="{x}" cy="{y - 1.75*s}" r="{0.42*s}" fill="#ffffff"/>\n')


def phone(x0, label, lat, color):
    w, h, r = 250, 470, 34
    b = [f'<rect x="{x0}" y="25" width="{w}" height="{h}" rx="{r}" fill="{NAVY}"/>',
         f'<rect x="{x0 + 12}" y="37" width="{w - 24}" height="{h - 24}" rx="{r - 10}" fill="#ffffff"/>',
         f'<rect x="{x0 + w/2 - 34}" y="45" width="68" height="14" rx="7" fill="{NAVY}"/>']
    # an abstract street grid, not a real place
    gx, gy, gw, gh = x0 + 12, 70, w - 24, 230
    b.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="{PALE}"/>')
    for k in range(1, 5):
        b.append(f'<line x1="{gx}" y1="{gy + k*gh/5}" x2="{gx + gw}" y2="{gy + k*gh/5}" stroke="#ffffff" stroke-width="7"/>')
    for k in range(1, 4):
        b.append(f'<line x1="{gx + k*gw/4}" y1="{gy}" x2="{gx + k*gw/4}" y2="{gy + gh}" stroke="#ffffff" stroke-width="7"/>')
    b.append(f'<line x1="{gx}" y1="{gy + gh - 20}" x2="{gx + gw}" y2="{gy + 40}" stroke="{LINE}" stroke-width="10"/>')
    b.append(pin(x0 + w/2, gy + gh/2 + 40, 26, color))
    cx = x0 + w/2
    b.append(f'<text x="{cx}" y="340" text-anchor="middle" font-family="{SANS}" font-size="30" '
             f'font-weight="700" fill="{color}">{label}</text>')
    b.append(f'<text x="{cx}" y="386" text-anchor="middle" font-family="{MONO}" font-size="27" '
             f'fill="{INK}">{lat}° N</text>')
    b.append(f'<text x="{cx}" y="424" text-anchor="middle" font-family="{MONO}" font-size="27" '
             f'fill="{INK}">{LON}° W</text>')
    b.append(f'<rect x="{x0 + w/2 - 50}" y="{25 + h - 26}" width="100" height="6" rx="3" fill="{LINE}"/>')
    return "\n".join(b) + "\n"


def quiz_figure():
    return svg(600, 520, phone(30, "Pin A", PIN_A, BLUE) + phone(320, "Pin B", PIN_B, ORANGE))


def ladder_figure():
    W, H = 1200, 470
    step = 92                      # one character column, wide enough for "1.1 km"
    x_first = 330                  # center of the first character of the number
    rows = [("Pin A", PIN_A, BLUE, 95), ("Pin B", PIN_B, ORANGE, 185)]
    worth = {3: "11 km", 4: "1.1 km", 5: "111 m", 6: "11 m", 7: "1.1 m"}   # index in the string
    differ = next(i for i, (a, b) in enumerate(zip(PIN_A, PIN_B)) if a != b)
    b = []
    cx = lambda i: x_first + i * step
    # highlight the first column that differs
    b.append(f'<rect x="{cx(differ) - step/2 + 3}" y="35" width="{step - 6}" height="265" rx="12" '
             f'fill="{ORANGE_PALE}" stroke="{ORANGE}" stroke-width="3"/>')
    for label, num, color, y in rows:
        b.append(f'<text x="{x_first - 60}" y="{y}" text-anchor="end" font-family="{SANS}" font-size="34" '
                 f'font-weight="700" fill="{color}">{label}</text>')
        for i, ch in enumerate(num + "°"):
            weight = "700" if i == differ else "400"
            fill = ORANGE if (i == differ and color == ORANGE) else INK
            b.append(f'<text x="{cx(i)}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="64" '
                     f'font-weight="{weight}" fill="{fill}">{ch}</text>')
    # the rule line
    b.append(f'<line x1="{cx(0) - step/2}" y1="225" x2="{cx(len(PIN_A))}" y2="225" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<text x="{x_first - 60}" y="282" text-anchor="end" font-family="{SANS}" font-size="24" '
             f'fill="{GRAY}">one step is worth</text>')
    b.append(f'<text x="{(cx(0) + cx(1))/2}" y="282" text-anchor="middle" font-family="{SANS}" font-size="24" '
             f'fill="{GRAY}">1° ≈ 111 km</text>')
    for i, txt in worth.items():
        hot = i == differ
        b.append(f'<text x="{cx(i)}" y="282" text-anchor="middle" font-family="{SANS}" font-size="23" '
                 f'font-weight="{"700" if hot else "400"}" fill="{ORANGE if hot else NAVY}">{txt}</text>')
    # the answer under the highlighted column
    b.append(f'<path d="M{cx(differ)},306 L{cx(differ)},336" stroke="{ORANGE}" stroke-width="4"/>')
    b.append(f'<path d="M{cx(differ) - 10},326 L{cx(differ)},340 L{cx(differ) + 10},326" fill="none" '
             f'stroke="{ORANGE}" stroke-width="4"/>')
    b.append(f'<text x="{cx(differ)}" y="384" text-anchor="middle" font-family="{SANS}" font-size="30" '
             f'font-weight="700" fill="{ORANGE}">0.01° apart ≈ 1.1 km</text>')
    b.append(f'<text x="{W/2}" y="445" text-anchor="middle" font-family="{SANS}" font-size="24" '
             f'fill="{GRAY}">Every digit to the right of it is the same, so it adds nothing</text>')
    return svg(W, H, "\n".join(b) + "\n")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "gps-quiz-two-pins.svg").write_text(quiz_figure())
    (OUT / "gps-digit-ladder.svg").write_text(ladder_figure())
    print("wrote", OUT / "gps-quiz-two-pins.svg", OUT / "gps-digit-ladder.svg")
