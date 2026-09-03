# Web Mapping with AI Experience

**Practice Your Skills · 15 points · due Wednesday of Week 14 at 11:59 pm on Learning Suite**

Learn how to build a website with a map on it, with an AI assistant helping from the first line.
This is the one assignment in the course designed around AI: use it as fully and creatively as you
like, and tell us what you did. Kicked off in class on Thursday of Week 11 (Harrison Stewart
presents and grades it); see the [Week 11 hands-on page](../hands-on/week-11.md).

## What you turn in

A single PDF on Learning Suite containing:

1. **The public URL** of your web page.
2. **A screenshot** of the page with the map showing your data.
3. **A short AI note** (150 to 300 words): which tools you used, the two or three prompts that
   mattered most, one thing the AI got wrong and how you found and fixed it, and what you checked
   yourself.

The page itself must stay online through the last day of finals.

## What the page must do

| Requirement | Detail |
| --- | --- |
| Interactive map | Pan and zoom in the browser. Leaflet, MapLibre GL, or OpenLayers are all fine; Google Maps and ArcGIS JS are fine too if you can use them free. |
| Basemap | Any tile basemap: OpenStreetMap, a Carto style, satellite. |
| Your own layer | At least one layer **you exported from QGIS** as GeoJSON, drawn on the map. Something from a lab, the final project, or the Belonging Map all count. |
| Popups | Clicking a feature shows at least two of its attributes. |
| Title and credits | A title, your name, and one line naming the data source. |
| Public | Hosted where anyone can open the URL without logging in. |

That is the whole bar. Anything beyond it (a legend, a layer switcher, a second layer, styling by
attribute, a chart, a search box) is welcome and makes a better portfolio piece, but it is not
graded.

## How to do it

### 1. Get a layer out of QGIS

Right-click a layer > **Export > Save Features As...**. Format **GeoJSON**, CRS **EPSG:4326
(WGS 84)**. Web maps expect longitude and latitude in degrees; a GeoJSON in UTM will draw in the
ocean off Africa. Keep the file under a few megabytes: simplify or filter first if it is a
statewide layer (**Vector > Geometry Tools > Simplify**, or a Query Builder filter).

### 2. Ask the AI for the page

Any assistant works: Claude, ChatGPT, Gemini, Copilot. A prompt that produces a working page
first try:

> Write a single self-contained `index.html` that uses Leaflet from a CDN. Show an OpenStreetMap
> basemap centered on Provo, Utah at zoom 12. Load a file called `data.geojson` from the same
> folder with `fetch`, add it to the map, style the features in blue, and open a popup on click
> that lists the feature's properties. Add a title bar with the text "My Map" and a footer with
> "Data: UGRC SGID".

Save the reply as `index.html` next to `data.geojson`. Then iterate: paste any error from the
browser console back to the assistant, ask for a legend, ask it to color by an attribute.

### 3. Test it locally

Browsers block a page opened from disk from loading a local file with `fetch`. Run a one-line
server in the folder and open the address it prints:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` in a browser. Press F12 to see the console if the map is blank.

### 4. Publish it

The easiest free host is **GitHub Pages**:

1. Create a free account at [github.com](https://github.com) if you do not have one, and a new
   public repository (any name, for example `cce114-webmap`).
2. Upload `index.html` and `data.geojson` (the **Add file > Upload files** button works; no git
   needed).
3. **Settings > Pages**, Source: **Deploy from a branch**, Branch: `main`, folder `/ (root)`,
   Save. After a minute the page is at `https://<your-username>.github.io/<repository>/`.

Netlify Drop, Cloudflare Pages, or a BYU-hosted page are equally acceptable. What matters is a
URL that works in a private browser window.

## Grading (15 points)

| Points | For |
| --- | --- |
| 6 | The page loads at the URL, the map pans and zooms, and your GeoJSON layer draws in the right place |
| 3 | Popups show attributes; title and credits present |
| 4 | The AI note: specific prompts, an error you caught, what you verified yourself |
| 2 | Screenshot and URL in the PDF as asked |

A page that does not load at grading time scores at most 6 total, so test the URL in a private
window before you submit.

## Help

- Harrison's office hours (see Learning Suite for times) and the lab hour after class in Weeks 12
  and 13.
- The [AI Use Policy](../policies/ai-policy.md): this assignment is explicitly AI-assisted, and
  disclosure is the deliverable, not a confession.
