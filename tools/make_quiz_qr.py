#!/usr/bin/env python3
"""Generate the QR code PNG for a self-check quiz page, for use on a slide.

The quizzes live at docs/quizzes/<slug>/index.html and publish to
<SITE>/quizzes/<slug>/. This writes a plain black-on-white code that a phone can
read off a projector from the back of the room:

    python3 tools/make_quiz_qr.py map-elements slides/day-04/images/mc-quiz-map-elements-qr.png

Keep the slug short. QR density, not the image, is what decides whether the code
scans from the back row, so a directory with an index.html beats a long .html
filename. No third-party QR service: the code is generated here so it cannot
break or start redirecting.
"""
import sys
from pathlib import Path

import qrcode

SITE = "https://byu-hydroinformatics.github.io/cce114-geomatics"


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(f"usage: {Path(sys.argv[0]).name} <quiz-slug> <output.png>")
    slug, out = sys.argv[1], Path(sys.argv[2])
    url = f"{SITE}/quizzes/{slug}/"

    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=12, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"{out}  {img.size[0]}x{img.size[1]}px  {qr.modules_count} modules  ->  {url}")


if __name__ == "__main__":
    main()
