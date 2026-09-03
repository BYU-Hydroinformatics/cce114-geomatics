# Week 2 Thursday: First Map in QGIS

**Day 3 · Thursday · Live demo and hands-on in QGIS (Dr. Halgren)** · feeds [Lab 1](../assignments/lab-01/README.md)

## At a glance

| | |
| --- | --- |
| **Goal** | Every student leaves with a QGIS project that has a basemap, the four Utah County layers, and a point layer they created and edited themselves. |
| **Why this week** | Tuesday named the data models (vector point, line, polygon; raster). Today students see each one as a real layer, and they learn the two moves Lab 1 depends on: adding a web basemap and adding downloaded data. |
| **Students bring** | Laptop with QGIS 3.44 LTR. [UtahCountyData.zip](https://byu-hydroinformatics.github.io/cce114-geomatics/lectures/data/UtahCountyData.zip) downloaded and unzipped (38 MB; have them start the download while the devotional happens). |
| **Graded item** | *In Class Activity: First Map: Utah County* (5 points). Upload a screenshot. |
| **Feeds** | Lab 1: Getting Started with GIS (download from UGRC, XYZ basemap, simple symbology). Due Saturday. |

## Before class

- [ ] QGIS 3.44 open on the projector machine, a new empty project, and the zip already unzipped to a folder with a short path (for example `C:\GIS\UtahCounty` or `~/GIS/UtahCounty`).
- [ ] The Google satellite XYZ connection already added under **XYZ Tiles** in the Browser panel (steps below), so the demo does not stall on typing a URL.
- [ ] Learning Suite open to the *First Map: Utah County* activity so you can show where the screenshot goes.
- [ ] The [Lab 1 page](../assignments/lab-01/README.md) open in a tab.

## Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | Today's goal; students unzip the data |
| 0:06 | Demo 1: a web basemap two ways (OpenStreetMap, then a Google satellite XYZ connection) |
| 0:14 | Demo 2: add the four Utah County layers and read each one's data model in Layer Properties |
| 0:24 | Demo 3: create a GeoPackage point layer, digitize three "new towers," move a vertex on a road |
| 0:34 | Students build the same map and add their own points |
| 0:45 | Screenshot and upload; show where Lab 1 lives and the UGRC download page it starts from |

## Walkthrough

### 1. A basemap two ways

1. In the **Browser** panel, expand **XYZ Tiles** and double-click **OpenStreetMap**. It ships with QGIS; nothing to configure.
2. Right-click **XYZ Tiles > New Connection...** Name it `Google Satellite` and paste the URL: `https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}`. Click OK, then double-click the new entry.
3. Point out the coordinates in the status bar as you move the mouse, and the **EPSG:3857** badge at bottom right: web basemaps set the project to Web Mercator. That is fine for today.

Say out loud: a basemap is a picture of the world served in tiles. You cannot click on a road in it and ask its name. That is the difference between a raster picture and vector data, which is the next step.

### 2. Four layers, four data models

1. **Layer > Add Layer > Add Vector Layer...** (or drag from the Browser panel). Add the county boundary, the major roads, and the cellular towers from the unzipped folder. Choose the `.shp` file for each.
2. **Layer > Add Layer > Add Raster Layer...** and add the DEM.
3. Drag layers so the order is towers, roads, boundary, DEM, basemap. Layers draw bottom to top.
4. For each layer, right-click **Properties > Information** and read the line that names the data model: *Geometry: Point*, *Line*, *Polygon*, or for the DEM the *Dimensions* and *Pixel size* lines. Ask the class which model each is before you reveal it.
5. Use the **Identify Features** tool (the blue "i") on a tower and on a road. Vector features carry attributes; the DEM returns a single number, the elevation of that cell.
6. Open the towers **Attribute Table** (F6). One row per feature is the whole idea of a vector layer.

### 3. Create and edit a layer

1. **Layer > Create Layer > New GeoPackage Layer...** Database: browse to the data folder and name it `week02.gpkg`. Table name `new_towers`, geometry type **Point**, CRS **EPSG:26912 (NAD83 / UTM zone 12N)** so coordinates are in meters. Add a text field `name` and an integer field `height_m`. OK.
2. Select the new layer, click **Toggle Editing** (the pencil), then **Add Point Feature**. Click three spots on the map; fill in the attribute form each time.
3. **Save Layer Edits**, then toggle editing off. Show that the points survive a project save and reopen; the shapefile towers and your GeoPackage towers are the same kind of thing.
4. Select the roads layer, toggle editing, choose the **Vertex Tool**, and drag one vertex of a road a little. Then **discard** the change (toggle editing off and choose Discard) so the class sees that edits are not real until saved.

### 4. Where Lab 1 starts

Open [gis.utah.gov/products/sgid](https://gis.utah.gov/products/sgid/) and show **Browse our data > Geoscience > Utah Quaternary Faults > Download > Shapefile**. Lab 1 is exactly the sequence they just did: download, unzip, add vector layer, add basemap, symbolize.

## Student activity

Students reproduce the map with their own three points, arrange layers so the towers sit on top of the satellite basemap, and take a screenshot showing the map canvas and the Layers panel. Upload it to **In Class Activity: First Map: Utah County** on Learning Suite before leaving. Full credit for a screenshot with the four layers plus their own point layer visible.

## Common snags

- **"Invalid data source" when adding a shapefile.** They picked one of the sidecar files (`.dbf`, `.shx`). Choose the `.shp`.
- **Layers do not line up, or the basemap is blank.** The DEM or a shapefile is missing its `.prj`. Right-click the layer > **Set CRS** to EPSG:26912. The basemap needs internet; the Clyde building Wi-Fi occasionally drops.
- **Nothing happens when they click to add a point.** Editing is not toggled on, or the wrong layer is selected in the Layers panel. Both show the same symptom.
- **Google tiles refuse to load.** Fall back to OpenStreetMap; the exercise does not depend on imagery.
- **macOS says the zip "can't be opened."** Move it out of Downloads first; QGIS on macOS cannot read from Desktop, Documents, or Downloads without permission.

## Links

- [Day 3 lecture page](../lectures/day-03.md)
- [Lab 1: Getting Started with GIS](../assignments/lab-01/README.md)
- Tuesday's deck: [GIS Data Models & File Formats](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-02/gis-data-models.html)
