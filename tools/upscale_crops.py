"""Re-crop drawing-recovered lab images from 300-dpi PDF renders (2x resolution).

The lab conversion recovered Google Drawings by cropping 150-dpi PDF page renders.
This tool finds each such image's exact source region (pixel-exact match against a
fresh 150-dpi render) and replaces the file with the same crop at 300 dpi. Images
that don't match exactly (edited crops, inline-export images) are left untouched.

Usage: upscale_crops.py <docId> <lab_dir>
"""
import sys, os, io, glob
sys.path.insert(0, os.path.expanduser("~/Code/claude-skills/skills/cce114-assignments/lib"))
import cce_docs as c
from googleapiclient.http import MediaIoBaseDownload
import pymupdf, numpy as np
from PIL import Image
import urllib.request

doc_id, lab_dir = sys.argv[1], sys.argv[2]

def export_pdf(doc_id):
    try:
        req = c.DRIVE.files().export_media(fileId=doc_id, mimeType="application/pdf")
        buf = io.BytesIO(); dl = MediaIoBaseDownload(buf, req)
        done = False
        while not done: _, done = dl.next_chunk()
        return buf.getvalue()
    except Exception:
        from google.auth.transport.requests import Request
        if not c._CREDS.valid: c._CREDS.refresh(Request())
        r = urllib.request.Request(
            f"https://docs.google.com/document/d/{doc_id}/export?format=pdf",
            headers={"Authorization": f"Bearer {c._CREDS.token}"})
        return urllib.request.urlopen(r, timeout=300).read()

pdf = pymupdf.open(stream=export_pdf(doc_id), filetype="pdf")
pages150, pages300 = [], []
for page in pdf:
    for dpi, out in ((150, pages150), (300, pages300)):
        pm = page.get_pixmap(dpi=dpi)
        out.append(np.array(Image.open(io.BytesIO(pm.tobytes("png"))).convert("RGB")))

def locate(P, C):
    """Find C's position in P via FFT cross-correlation (jitter-proof: Google's
    PDF export re-rasterizes differently every time), then verify the region is
    the same content — never an edited crop."""
    h, w = C.shape[:2]; H, W = P.shape[:2]
    if h > H or w > W: return None
    Pg = P.astype(np.float32).mean(-1)[::4, ::4]
    Cg = C.astype(np.float32).mean(-1)[::4, ::4]
    k = Cg - Cg.mean()
    S = (Pg.shape[0] + k.shape[0], Pg.shape[1] + k.shape[1])
    corr = np.fft.irfft2(np.fft.rfft2(Pg, S) * np.fft.rfft2(k[::-1, ::-1], S), S)
    py, px = np.unravel_index(np.argmax(corr), corr.shape)
    y0, x0 = (py - k.shape[0] + 1) * 4, (px - k.shape[1] + 1) * 4
    Pi = P.astype(np.int16); Ci = C.astype(np.int16)
    best = None
    for dy in range(-6, 7):
        for dx in range(-6, 7):
            y, x = y0 + dy, x0 + dx
            if y < 0 or x < 0 or y + h > H or x + w > W: continue
            mean = float(np.abs(Pi[y:y + h, x:x + w] - Ci).mean())
            if best is None or mean < best[0]:
                best = (mean, y, x)
    if best is None: return None
    mean, y, x = best
    if mean >= 3.0: return None
    d = np.abs(Pi[y:y + h, x:x + w] - Ci)
    bad = d.max(-1) > 40
    if bad.mean() >= 0.08: return None
    bh, bw = max(h // 16, 1), max(w // 16, 1)
    for by in range(0, h - bh + 1, bh):
        for bx in range(0, w - bw + 1, bw):
            if bad[by:by + bh, bx:bx + bw].mean() > 0.6:
                return None  # dense diff block = a real edit; leave the file alone
    return (y, x, mean)

matched = skipped = 0
for f in sorted(glob.glob(os.path.join(lab_dir, "images", "*.png"))):
    C = np.array(Image.open(f).convert("RGB"))
    hit = None
    for pi, P in enumerate(pages150):
        pos = locate(P, C)
        if pos and (hit is None or pos[2] < hit[1][2]):
            hit = (pi, pos)
    if not hit:
        skipped += 1
        continue
    pi, (y, x, _mean) = hit
    h, w = C.shape[:2]
    big = pages300[pi][y * 2:(y + h) * 2, x * 2:(x + w) * 2]
    Image.fromarray(big).save(f)
    matched += 1
    print(f"  2x: {os.path.basename(f)}  (page {pi + 1})")
print(f"{os.path.basename(lab_dir)}: upscaled {matched}, untouched {skipped}")
