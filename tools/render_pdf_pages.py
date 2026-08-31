"""Render a lab Google Doc's PDF export to per-page PNGs (150 dpi).
Usage: render_pdf_pages.py <docId> <outdir>"""
import sys, os, io
sys.path.insert(0, os.path.expanduser("~/Code/claude-skills/skills/cce114-assignments/lib"))
import cce_docs as c
from googleapiclient.http import MediaIoBaseDownload
import pymupdf

doc_id, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
try:
    req = c.DRIVE.files().export_media(fileId=doc_id, mimeType="application/pdf")
    buf = io.BytesIO(); dl = MediaIoBaseDownload(buf, req)
    done = False
    while not done: _, done = dl.next_chunk()
    data = buf.getvalue()
except Exception:
    # Drive API caps exports at 10 MB; the web export endpoint has no such cap.
    import urllib.request
    from google.auth.transport.requests import Request
    if not c._CREDS.valid: c._CREDS.refresh(Request())
    r = urllib.request.Request(
        f"https://docs.google.com/document/d/{doc_id}/export?format=pdf",
        headers={"Authorization": f"Bearer {c._CREDS.token}"})
    data = urllib.request.urlopen(r, timeout=300).read()
pdf = pymupdf.open(stream=data, filetype="pdf")
for i, page in enumerate(pdf, 1):
    page.get_pixmap(dpi=150).save(f"{outdir}/p{i:02d}.png")
print(f"{len(pdf)} pages -> {outdir} (each 1275x1650 px at 150 dpi)")
