"""Draw the GIS file-format tile sheet used by the Day 2 deck.

Run from the repository root:  python3 tools/make_file_format_tiles.py
Writes slides/day-02/images/dm-file-format-icons.jpg. Drawn rather than AI-generated so
every extension label is exact.
"""
from PIL import Image, ImageDraw, ImageFont
import math

S=2  # supersample
W,H=1800,1350
img=Image.new("RGBA",(W*S,H*S),(255,255,255,0))
d=ImageDraw.Draw(img)
fb=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf",64*S)
fs=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf",40*S)

# (label, band color, sublabel, glyph)
tiles=[
 (".shp","#1f6f3f","Shapefile","poly"),
 (".gpkg","#2c5aa0","GeoPackage","layers"),
 (".geojson","#c8791d","GeoJSON","json"),
 (".kml","#7a3e9d","KML","pin"),
 (".tif","#b5342b","GeoTIFF","grid"),
 (".csv","#5c6670","CSV / XY","table"),
 (".dbf","#1f6f3f","Attributes","table"),
 (".prj","#1f6f3f","Coord. system","globe"),
 (".gdb","#2c5aa0","Geodatabase","layers"),
]

cols=3; tw,th=430,390; gx=(W-cols*tw)//(cols+1); gy=(H-3*th)//4
def tile(x,y,label,color,sub,glyph):
    x*=S;y*=S;w=tw*S;h=th*S;fold=70*S
    # shadow
    d.rounded_rectangle([x+10*S,y+12*S,x+w+10*S,y+h+12*S],radius=18*S,fill=(0,0,0,40))
    # page
    d.polygon([(x,y),(x+w-fold,y),(x+w,y+fold),(x+w,y+h),(x,y+h)],fill="#f7f7f5",outline="#bfc3c8",width=3*S)
    d.polygon([(x+w-fold,y),(x+w-fold,y+fold),(x+w,y+fold)],fill="#dcdfe3",outline="#bfc3c8",width=3*S)
    # band
    d.rectangle([x-8*S,y+40*S,x+w-fold-10*S,y+40*S+96*S],fill=color)
    d.text((x+22*S,y+48*S),label,font=fb,fill="white")
    # glyph area
    cx,cy=x+w//2,y+235*S
    ink=color
    if glyph=="poly":
        pts=[(cx-75*S,cy-35*S),(cx-25*S,cy-60*S),(cx+60*S,cy-42*S),(cx+75*S,cy+15*S),(cx+8*S,cy+50*S),(cx-65*S,cy+25*S)]
        d.polygon(pts,fill="#cfe6d6",outline=ink,width=5*S)
        for p in pts: d.ellipse([p[0]-8*S,p[1]-8*S,p[0]+8*S,p[1]+8*S],fill=ink)
    elif glyph=="layers":
        for i,col in enumerate(["#9db8e0","#7e9fd1","#5c85c2"]):
            o=(2-i)*24*S
            d.polygon([(cx,cy-32*S+o),(cx+90*S,cy+o),(cx,cy+32*S+o),(cx-90*S,cy+o)],fill=col,outline=ink,width=4*S)
    elif glyph=="json":
        f=ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf",27*S)
        for i,t in enumerate(['{ "type": "Point",','  "coordinates":','  [-111.65, 40.25] }']):
            d.text((cx-150*S,cy-55*S+i*36*S),t,font=f,fill=ink)
    elif glyph=="pin":
        d.ellipse([cx-50*S,cy-80*S,cx+50*S,cy+20*S],fill="#d9c4e6",outline=ink,width=5*S)
        d.polygon([(cx-38*S,cy),(cx+38*S,cy),(cx,cy+65*S)],fill="#d9c4e6",outline=ink,width=5*S)
        d.polygon([(cx-38*S,cy),(cx+38*S,cy),(cx,cy+65*S)],fill="#d9c4e6")
        d.ellipse([cx-18*S,cy-48*S,cx+18*S,cy-12*S],fill="white",outline=ink,width=4*S)
    elif glyph=="grid":
        n=6;c=26*S;ox=cx-n*c//2;oy=cy-n*c//2
        for i in range(n):
            for j in range(n):
                v=int(120+100*math.sin(i*0.9)*math.cos(j*0.7))
                d.rectangle([ox+j*c,oy+i*c,ox+(j+1)*c,oy+(i+1)*c],fill=(v,v//2+40,40),outline="white",width=2*S)
    elif glyph=="table":
        ox=cx-105*S;oy=cy-65*S;cw=70*S;rh=28*S
        d.rectangle([ox,oy,ox+3*cw,oy+rh],fill=ink)
        for r in range(1,5):
            d.rectangle([ox,oy+r*rh,ox+3*cw,oy+(r+1)*rh],fill="white" if r%2 else "#eef0f2",outline="#9aa0a6",width=2*S)
        for cc in range(1,3):
            d.line([(ox+cc*cw,oy),(ox+cc*cw,oy+5*rh)],fill="#9aa0a6",width=2*S)
        d.rectangle([ox,oy,ox+3*cw,oy+5*rh],outline=ink,width=3*S)
    elif glyph=="globe":
        r=65*S
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill="#d7e6dc",outline=ink,width=5*S)
        d.ellipse([cx-r//2,cy-r,cx+r//2,cy+r],outline=ink,width=3*S)
        d.line([(cx-r,cy),(cx+r,cy)],fill=ink,width=3*S)
        d.line([(cx-r*0.87,cy-r//2),(cx+r*0.87,cy-r//2)],fill=ink,width=3*S)
        d.line([(cx-r*0.87,cy+r//2),(cx+r*0.87,cy+r//2)],fill=ink,width=3*S)
        d.line([(cx,cy-r),(cx,cy+r)],fill=ink,width=3*S)
    # sublabel
    bb=d.textbbox((0,0),sub,font=fs)
    d.text((x+(w-(bb[2]-bb[0]))//2,y+h-55*S),sub,font=fs,fill="#3a3f47")

for i,(l,c,s,g) in enumerate(tiles):
    r,cc=divmod(i,cols)
    tile(gx+cc*(tw+gx),gy+r*(th+gy),l,c,s,g)

img=img.resize((W,H),Image.LANCZOS)
bg=Image.new("RGB",img.size,"white"); bg.paste(img,mask=img.split()[3])
bg.save("slides/day-02/images/dm-file-format-icons.jpg",quality=88)
print("ok")
