"""Convert a CCE 114 lab Google Doc to Markdown + images for the GitHub repo.
Usage: doc2md.py <docId> <outdir>   -> <outdir>/README.md + <outdir>/images/*"""
import sys, os, re, io, base64, urllib.request
sys.path.insert(0, os.path.expanduser("~/Code/claude-skills/skills/cce114-assignments/lib"))
import cce_docs as c
from googleapiclient.http import MediaIoBaseDownload

doc_id, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir + "/images", exist_ok=True)

# 1. Markdown export (text + inline images as base64 reference defs)
req = c.DRIVE.files().export_media(fileId=doc_id, mimeType="text/markdown")
buf = io.BytesIO(); dl = MediaIoBaseDownload(buf, req)
done = False
while not done: _, done = dl.next_chunk()
md = buf.getvalue().decode("utf-8")

# 2. Decode inline-image reference definitions -> files
def_pat = re.compile(r'\[(image\d+)\]:\s*<data:image/(\w+);base64,([A-Za-z0-9+/=\s]+?)>\s*$', re.M)
saved = {}
for m in def_pat.finditer(md):
    name, ext, b64 = m.group(1), m.group(2), m.group(3)
    ext = {"jpeg": "jpg"}.get(ext, ext)
    fn = f"images/{name}.{ext}"
    with open(os.path.join(outdir, fn), "wb") as f:
        f.write(base64.b64decode(re.sub(r"\s", "", b64)))
    saved[name] = fn
md = def_pat.sub("", md)
for name, fn in saved.items():
    md = re.sub(r'!\[[^\]]*\]\[' + name + r'\]', f'![{name}]({fn})', md)
print(f"inline images decoded: {len(saved)}")

# 3. Positioned (anchored) images: fetch via Docs API, insert at anchor paragraphs
d = c._get(doc_id)
pos = d.get("positionedObjects", {})
anchors = []  # (startIndex, objId, paragraph text)
def walk(content):
    for el in content:
        if "paragraph" in el:
            p = el["paragraph"]
            ids = p.get("positionedObjectIds", [])
            if ids:
                text = "".join(r.get("textRun", {}).get("content", "") for r in p.get("elements", []))
                for oid in ids: anchors.append((el["startIndex"], oid, text))
        elif "table" in el:
            for row in el["table"].get("tableRows", []):
                for cell in row.get("tableCells", []): walk(cell.get("content", []))
walk(d["body"]["content"])
anchors.sort()

c._CREDS.refresh(__import__("google.auth.transport.requests", fromlist=["Request"]).Request()) if not c._CREDS.valid else None
tok = c._CREDS.token
lines = md.split("\n")
for n, (_si, oid, ptext) in enumerate(anchors, 1):
    props = pos[oid]["positionedObjectProperties"]["embeddedObject"]
    uri = props.get("imageProperties", {}).get("contentUri")
    fn = f"images/anchored{n}.png"
    if uri:
        r = urllib.request.Request(uri, headers={"Authorization": f"Bearer {tok}"})
        data = urllib.request.urlopen(r, timeout=120).read()
        with open(os.path.join(outdir, fn), "wb") as f: f.write(data)
        kind = "image"
    else:
        kind = "DRAWING (placeholder ref; crop from PDF)"
    # find the anchor paragraph's line in the md (escape-insensitive) and insert after
    probe = re.sub(r"\s+", " ", ptext).strip()[:32]
    idx = None
    if probe:
        for i, ln in enumerate(lines):
            if probe and probe in re.sub(r"\s+", " ", ln.replace("\\", "")):
                idx = i; break
    if idx is None:
        lines.append(""); lines.append(f"![anchored{n}]({fn})")
        print(f"  anchored{n}: {kind} anchor NOT FOUND ('{probe}'), APPENDED at end")
    else:
        lines[idx + 1:idx + 1] = ["", f"![anchored{n}]({fn})"]
        print(f"  anchored{n}: {kind} inserted after line {idx} ('{probe[:30]}')")
md = "\n".join(lines)

# 4. Tidy: drop empty heading lines, collapse >2 blank lines
md = re.sub(r'^#{1,6}\s*\**\s*$', '', md, flags=re.M)
md = re.sub(r'\n{3,}', '\n\n', md)
open(os.path.join(outdir, "README.md"), "w").write(md.strip() + "\n")
print(f"wrote {outdir}/README.md ({len(md)//1024} KB), images: {len(os.listdir(outdir + '/images'))}")
