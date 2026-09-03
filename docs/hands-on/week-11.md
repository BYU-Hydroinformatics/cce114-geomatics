# Week 11 Thursday: Georeferencing in QGIS, and the Web Mapping with AI Kickoff

**Day 21 · Thursday · Live demo and hands-on in QGIS (Dr. Halgren), then the Web Mapping with AI kickoff (Harrison)** · feeds [Lab 10](../assignments/lab-10/README.md) and the [Web Mapping with AI Experience](../assignments/web-mapping-with-ai.md)

## At a glance

| | |
| --- | --- |
| **Goal** | Students georeference an image that has no coordinates of its own, understand ground control points, transformation types, and residuals, and see what a good registration looks like. Then they get the Web Mapping with AI assignment launched with a live example. |
| **Why this week** | Tuesday Dr. Ames presented georeferencing and students georeferenced their own pencil sketch of their neighborhood. Today upgrades that to a real plan sheet or historic map with quality control, which is what a site plan for Lab 10's Domes for Mozambique project needs. The Web Mapping experience is due Wednesday of Week 14, so three weeks of lead time start now. |
| **Students bring** | Laptop with QGIS 3.44. Their georeferenced sketch from Tuesday, if they finished it. |
| **Graded item** | None on Thursday. Tuesday's *Georeference Your Neighborhood Sketch* (5 points) is Dr. Ames's item; students who did not finish can upload it after today's session. |
| **Feeds** | Lab 10: Geoplanning, Domes for Mozambique. Due Saturday. Web Mapping with AI Experience, due Wednesday of Week 14. |

## Before class

- [ ] An image to georeference, saved locally: a scanned historic USGS quad of Provo from [USGS topoView](https://ngmdb.usgs.gov/topoview/) (download the JPEG, not the GeoTIFF, so it truly has no coordinates), or a campus plan sheet PDF exported to PNG. Test it once.
- [ ] QGIS open with the Google satellite XYZ basemap and the project CRS at **EPSG:26912**. The Georeferencer is under **Layer > Georeferencer...** in 3.44 (Raster > Georeferencer in older versions).
- [ ] Harrison ready with a finished example web map open in a browser and the [assignment page](../assignments/web-mapping-with-ai.md) in a tab.
- [ ] A GeoJSON export of any layer ready (steps below) for the kickoff demo.

## Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | Why georeference: plan sheets, old maps, drone photos, your sketch |
| 0:06 | Georeferencer: open image, place four GCPs from the map canvas |
| 0:14 | Transformation settings: linear, Helmert, polynomial, thin plate spline; residuals and RMS |
| 0:20 | Run, overlay with transparency, judge it; add two more GCPs and rerun |
| 0:26 | What Lab 10's site plan needs from this |
| 0:30 | Web Mapping with AI kickoff: the deliverable, a finished example, QGIS to GeoJSON to a web page in ten minutes |
| 0:46 | Questions; where to get help |

## Walkthrough

### 1. Why

A drawing, a scan, a photo: pixels with no idea where they are. Georeferencing attaches real-world coordinates to pixel positions so the image can sit under vector data. Every renovation project starts with an old plan sheet; every site visit produces a sketch. Tuesday's sketch was the gentle version; today's image is the working version.

### 2. Ground control points

1. **Layer > Georeferencer...** In the Georeferencer window, **Open Raster** and choose the image. It appears in its own canvas with pixel coordinates.
2. **Add Point** tool. Click a feature you can also find on the basemap: a road intersection, a building corner, a bridge end. In the dialog, click **From Map Canvas**, then click the same feature on the QGIS map. The GCP appears in the table with source pixels and destination coordinates.
3. Repeat for four points, spread to the corners of the image. Say the rule: spread wide, avoid a line, use hard corners not soft edges.

### 3. Transformation settings and residuals

1. **Settings > Transformation Settings**. Walk the list: **Linear** (shift and scale only, needs 2 GCPs), **Helmert** (adds rotation, 2 GCPs), **Polynomial 1** (affine, 3 GCPs, the default for a flat scan), **Polynomial 2** (6 GCPs, corrects gentle warps), **Thin Plate Spline** (bends locally to fit every point exactly, which hides bad points). Resampling **Cubic** for imagery, **Nearest neighbor** for a categorical scan. Target CRS EPSG:26912. Output file next to the image. Tick **Load in project when done**.
2. Look at the GCP table: the **dX, dY** and **residual** columns appear once there are enough points for the chosen transformation. The **Mean error (RMS)** is at the bottom. A residual of 30 m on a 1:24,000 scan is a misplaced click; 3 m is fine.
3. Turn off one point (untick it) and watch the RMS change. That is quality control, and it is why TPS with four points is meaningless: it forces zero residual everywhere.

### 4. Run and judge

1. **Start Georeferencing**. The output loads over the basemap. Set its opacity to 50 percent and toggle it. Do the roads line up across the whole image or only near the GCPs?
2. Add two more GCPs in the worst area, switch to Polynomial 2, rerun. Better in the middle, and the corners? Discuss what more points buy and when they stop helping.
3. Optional: **Vector** digitize a building footprint from the georeferenced 1950s map and compare to today's imagery. That is a change-detection analysis in two minutes.

### 5. Lab 10 connection

Domes for Mozambique places a site inside a project boundary and plans around it. If the site drawing comes as an image, this is how it becomes a layer. Also point out that Lab 10 starts by **choosing a CRS for Mozambique** (UTM 36S or 37S), the Week 8 lesson applied somewhere new.

## Web Mapping with AI kickoff (16 minutes, Harrison)

The assignment is on the site: [Web Mapping with AI Experience](../assignments/web-mapping-with-ai.md). Cover:

1. **The deliverable in one sentence.** A public web page with an interactive map showing at least one layer you made in QGIS, built with an AI assistant, plus a short note on how you used the AI and what you checked.
2. **A finished example.** Open one: pan, zoom, click a feature, see a popup. This is the bar; it is not high.
3. **Live, in ten minutes.** Right-click any layer in QGIS > **Export > Save Features As...**, format **GeoJSON**, CRS **EPSG:4326** (web maps expect degrees). Open an AI assistant and paste a prompt like: *Write a single HTML file that uses Leaflet from a CDN, shows an OpenStreetMap basemap centered on Provo, Utah, loads `data.geojson` from the same folder, styles it, and shows each feature's attributes in a popup.* Save the reply as `index.html` next to the GeoJSON. Open it in a browser (a local server may be needed for `fetch`; the assignment page has the one-line command). It works, or the AI fixes what it got wrong when you paste the error back.
4. **Publish.** Create a GitHub repository, upload the two files, enable **Pages** in Settings. The page URL is the submission. The assignment page walks this with screenshots.
5. **Where to get help.** Harrison's office hours and the Week 12 lab hour. Start this week; the last week of the semester is the final project.

## Common snags

- **Georeferencer menu is missing.** It is a core plugin; **Plugins > Manage and Install > Installed > Georeferencer GDAL** must be ticked.
- **Output loads far from the basemap.** The target CRS did not match the map canvas CRS at the time the GCPs were captured. Redo with both at 26912.
- **RMS column is blank.** Not enough points for the transformation; Polynomial 2 needs six.
- **The image is upside down or mirrored.** A scan from a PDF sometimes carries a rotation flag. Rotate it in an image editor first, or just place the GCPs and let Helmert handle rotation.
- **`fetch` of the GeoJSON fails in the browser.** Opening `index.html` from disk blocks local file loads. Run `python3 -m http.server` in the folder and open `http://localhost:8000`, or publish to Pages and test there.

## Links

- [Day 21 lecture page](../lectures/day-21.md)
- [Lab 10: Domes for Mozambique](../assignments/lab-10/README.md)
- [Web Mapping with AI Experience](../assignments/web-mapping-with-ai.md)
- [Tuesday activities: Georeference Your Neighborhood Sketch](tuesday-activities.md#week-11-georeference-your-neighborhood-sketch)
- [USGS topoView](https://ngmdb.usgs.gov/topoview/) for historic quads
