# Week 7 Thursday: Web Services in QGIS

**Day 13 · Thursday · Live demo and hands-on in QGIS (Dr. Halgren)** · feeds [Lab 6](../assignments/lab-06/README.md) · includes the Community and Professional Map Experience pitch

## At a glance

| | |
| --- | --- |
| **Goal** | Students connect QGIS to the Utah ArcGIS REST services, add three or more live layers without downloading anything, and export a layout. |
| **Why this week** | Tuesday covered where spatial data comes from and the alphabet of web services (WMS, WMTS, WFS, ArcGIS REST, XYZ). Lab 6 is a mini project built entirely from web services, so today is a running start on it. |
| **Students bring** | Laptop with QGIS 3.44 and a working network connection. |
| **Graded item** | *In Class Activity: Getting Data through Web Mapping Services* (5 points). Upload a layout image built from three or more service layers. |
| **Feeds** | Lab 6: Spatial Data Web Services. Due Saturday. Concepts Exam 1 closed Wednesday. |

## Before class

- [ ] The UGRC endpoint open in a browser tab: `https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/` (the plain directory listing; scroll it once so you know what is there).
- [ ] The **ArcGIS REST Server** connection already created in QGIS (steps below) so the demo starts at the browse step.
- [ ] Isabel (who grades the Community and Professional Map Experience) ready for a ten-minute pitch, or you give it.
- [ ] Learning Suite open to the *Getting Data through Web Mapping Services* activity.

## Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | The endpoint in a browser: what a REST directory is; a layer's JSON page |
| 0:08 | QGIS: new ArcGIS REST connection, browse, add three layers |
| 0:16 | Style, filter with a query, note the projection each service arrives in |
| 0:22 | One WMS and one XYZ for contrast; Data Source Manager's left column |
| 0:27 | Students: three-plus layers, layout, upload |
| 0:40 | Community and Professional Map Experience pitch |

## Walkthrough

### 1. Look at the service before touching QGIS

1. Open the endpoint URL. It is a folder listing of feature services: boundaries, transportation, water, cadastre, and so on. Click one (for example a roads service), then a layer inside it. The page shows the fields, the geometry type, the spatial reference (WKID), and the record count.
2. Scroll to the bottom and click **Query**; set `Where` to `1=1`, `Out fields` to `*`, `Format` to JSON, and run it. That JSON is what QGIS receives. Nobody is emailing a shapefile.

### 2. Connect QGIS

1. **Layer > Data Source Manager > ArcGIS REST Server**. Click **New**, Name `UGRC`, URL the endpoint above. OK, then **Connect**.
2. The tree lists every service. Expand one, tick a layer, and **Add**. Do this for a polygon (counties or municipalities), a line (roads or streams), and a point layer (schools, hospitals, or cell sites). Close the dialog.
3. Right-click a layer > **Properties > Source**. The provider is `arcgisfeatureserver` and the URL is the layer's REST page. Point out the CRS: UGRC serves most layers in EPSG:26912 already.
4. **Properties > Source > Query Builder**: `"COUNTY" = 'UTAH'` (use the real field name) to fetch only part of a statewide layer. The filter runs on the server.

### 3. The other kinds, briefly

- **WMS/WMTS**: Data Source Manager > WMS/WMTS > New. Any public WMS works; the USGS National Map services are a reliable example. Add a layer; it is an image, not features, so Identify returns nothing useful and there is no attribute table. That is the WMS trade: fast, pretty, not analyzable.
- **XYZ**: already used in Week 2. Tiles, images, no attributes.
- Say the rule of thumb from Lab 6: WMS is a picture, WFS and ArcGIS REST feature services are ingredients.

### 4. Layout

Same as Week 3: **Project > New Print Layout**, map, legend, scale bar, north arrow, title, and a data-source label that names the services. Export as PNG.

## Student activity

Students connect to the UGRC endpoint, pick three or more layers that interest them, style them so they are distinguishable, add the required map elements in a layout, and export an image. Upload it to **In Class Activity: Getting Data through Web Mapping Services**. Full credit for three service layers and a layout; a screenshot of the canvas earns partial credit.

## Community and Professional Map Experience pitch (10 minutes)

Due Wednesday of Week 10. The assignment: attend a real construction or engineering event or presentation, take a picture there, build a QGIS map of where it was held plus anything relevant, and write what maps were shown and what they learned about map-based communication, answering three questions (what data, what analysis, what decision). Cover:

1. **What counts.** A city council or planning commission meeting (Provo and Orem post agendas online; most have a public-works or land-use item every week), a UDOT open house, an ASCE or AGC student chapter meeting with an industry speaker, a BYU engineering seminar with a practitioner. The easy option is a city council meeting.
2. **What to capture.** A photo at the event, a photo of any map shown, and notes on the three questions while it is fresh.
3. **The map.** The same venue-point-plus-basemap layout from the Week 3 Belonging Map demo, now with something from today's session: the parcel, the road, or the district the agenda item was about, pulled from the UGRC services.
4. **When.** Meetings are usually Tuesday evenings; there are three weeks left. Pick one tonight.

## Common snags

- **"Failed to connect" to the REST server.** The URL has a trailing space or is missing `/rest/services`. Copy it from this page.
- **Layers add but draw nothing.** The layer is huge and QGIS is still fetching; wait, or set a Query Builder filter first. Statewide parcels will not load in class.
- **Layers do not overlap.** One arrived in EPSG:4326 and the project is 3857 or 26912. On-the-fly reprojection handles it, but check the layer CRS in Source if something is far away.
- **WMS shows nothing at this zoom.** Many WMS layers have scale limits; zoom out.
- **No internet.** There is no offline fallback for this session. The Clyde building lab machines are wired; move there.

## Links

- [Day 13 lecture page](../lectures/day-13.md)
- [Lab 6: Spatial Data Web Services](../assignments/lab-06/README.md)
- [Community and Professional Map Experience](../assignments/deliverables.md#community-and-professional-map-experience-week-10)
- Tuesday's deck: [Finding Spatial Data and Web Services](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-12/finding-spatial-data-and-web-services.html)
