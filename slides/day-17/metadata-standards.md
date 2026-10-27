---
marp: true
theme: cce114
paginate: true
footer: "CCE 114 · Day 17 — Metadata Standards"
---

<!-- _class: lead -->
<!-- _paginate: skip -->

![bg right:45% w:95%](images/md-thursday-qgis.jpg)

# Metadata Standards and Fitness for Use

CCE 114 Geomatics
Dr. Dan Ames and Dr. James Halgren

<!-- Thursday lead-in, Week 9. About fifteen minutes of slides, then the hands-on session in QGIS (the Week 9 hands-on guide). Tuesday covered what metadata is, why it matters, and the six questions; today covers the standards those questions are written in, where the record sits in a download, and how to read one to decide whether the data are fit for your use. The last slide is the QGIS Metadata dialog, which is where the hands-on picks up. -->

---

# Today's Goals

![bg right:32% w:80%](images/md-label-record.jpg)

By the end of class you should be able to:

- Name the main metadata **standards**: FGDC CSDGM and ISO 19115
- Find where metadata **lives** in a download: `.xml`, `.qmd`, GeoPackage, `.prj`
- Read a metadata record and judge whether the data are **fit for your use**
- **Write** metadata for a layer in QGIS and save it so it travels with the data

<!-- Recap Tuesday in one breath: a label is a metadata record, and every record answers what, where, when, why, how, and who. Today is the formal version of that label, then you write one yourself. -->

---

<!-- _class: lead -->

# Metadata standards and styles

---

# Why standardize metadata at all?

<div class="columns" style="align-items:start;">
<div>

- If everyone invents their own fields, nothing is **searchable**
- A standard fixes the **field names**, so software can index them
- It fixes the **expected content**, so a "date" is a date
- It makes records **portable** between agencies and software

</div>
<div>

![w:340 center](images/md-card-catalog.jpg)

- A **standard** says what has to be there
- A **style** or **profile** says how one organization fills it in
- Same idea as a survey report template: fixed headings, local content

</div>
</div>

<!-- The library-catalog analogy works well: a card catalog is only useful because every card has the same fields in the same places. A metadata standard is a card catalog for data. -->

---

# FGDC CSDGM: the U.S. federal standard

![bg right:36% w:94%](images/md-fgdc-federal.jpg)

- **Content Standard for Digital Geospatial Metadata**, from the Federal Geographic Data Committee
- Executive Order 12906 (1994) told federal agencies to document geospatial data this way as part of the National Spatial Data Infrastructure
- Current version is FGDC-STD-001-1998
- Usually travels as a sidecar **`.xml`** file next to the shapefile
- Still everywhere: most Utah and federal downloads you open this semester are FGDC

<!-- This is the standard the students will actually meet in Lab 8: the Utah County Boundaries download ships an FGDC XML file alongside the shapefile. Since 2010 the FGDC has endorsed the ISO standards and encouraged agencies to migrate, but the installed base of FGDC records is enormous, so you still have to be able to read one. -->

---

# The seven sections of an FGDC record

<div class="columns" style="align-items:start;">
<div>

1. **Identification** — title, abstract, purpose, keywords, bounding coordinates
2. **Data Quality** — accuracy, completeness, **lineage**
3. **Spatial Data Organization** — points, vectors, or raster cells
4. **Spatial Reference** — projection, datum, units

</div>
<div>

![w:340 center](images/md-seven-sections.jpg)

5. **Entity and Attribute** — what each column and code means
6. **Distribution** — where to get it, format, constraints
7. **Metadata Reference** — who wrote *the metadata*, and when

</div>
</div>

<!-- Section 5 is the one nobody fills in and everybody needs. Section 7 matters more than it looks: a 1998 metadata record attached to a 2024 dataset is a warning sign. -->

---

# What an FGDC record looks like inside

![bg right:30% w:94%](images/md-xml-inside.jpg)

```xml
<metadata>
  <idinfo>
    <citation><citeinfo>
      <origin>Utah Geospatial Resource Center</origin>
      <pubdate>20240115</pubdate>
      <title>Utah County Boundaries</title>
    </citeinfo></citation>
    <descript><abstract>...</abstract><purpose>...</purpose></descript>
    <spdom><bounding><westbc>...</westbc><eastbc>...</eastbc></bounding></spdom>
  </idinfo>
  <metainfo><metd>20240115</metd></metainfo>
</metadata>
```

<!-- Generic skeleton, not a real record: the point is the shape, not the values. Tell students the search terms from Lab 8: Ctrl+F for "metd" to find the metadata date, and "bounding" to find the extent. XML is verbose but it is plain text, so you can always read it in a browser or a text editor. -->

---

# ISO 19115: the international standard

![bg right:32% w:94%](images/md-iso-global.jpg)

- **ISO 19115, *Geographic information — Metadata***, is the international equivalent
- Richer and more structured than FGDC, but organized the same way: identification, quality, spatial representation, reference system, distribution
- Used across Europe, Australia, Canada, and increasingly by U.S. federal agencies
- **QGIS layer metadata follows the ISO 19115 model**, which is why the panel you will use in a few minutes has fields like *Identification, Extent, Access, Fields, History*

<!-- Current revision is ISO 19115-1; the XML encodings are ISO 19139 and ISO 19115-3 (mention in passing, not on the slide). The practical takeaway for this class: FGDC and ISO ask the same six questions with different tag names. If you can read one you can read the other. QGIS chose ISO, which is one reason FGDC .xml files do not import cleanly into QGIS. -->

---

# Other styles you will meet

<div class="columns" style="align-items:start;">
<div>

- **Dublin Core** — 15 general-purpose elements (title, creator, date, rights…). Not spatial, but it underlies a lot of catalogs
- **DCAT / Project Open Data** — the schema behind [data.gov](https://www.data.gov)

</div>
<div>

![w:340 center](images/md-other-styles.jpg)

- **STAC** — SpatioTemporal Asset Catalog, used for satellite and drone imagery collections
- **Esri metadata styles** — ArcGIS can write FGDC, ISO, or its own style; the same record, different export

</div>
</div>

<!-- Do not memorize this list. Recognize the names so that when a download says "ISO 19139 metadata" or "STAC catalog" you know it is the same six questions in a different wrapper. -->

---

# Where does the metadata actually live?

<div class="columns" style="align-items:start;">
<div>

- **Shapefile** — sidecar `.xml` beside the `.shp`, plus the `.prj` that holds the coordinate system
- **GeoPackage** — stored *inside* the `.gpkg` file
- **QGIS layer** — a `.qmd` sidecar file, or inside the project file

</div>
<div>

![w:250 center](images/md-where-it-lives.jpg)

- **Web service** — returned in the service's `GetCapabilities` or item page
- **Data portal** — on the download page itself
- If you unzip a download and never open anything but the `.shp`, you threw the metadata away

</div>
</div>

<!-- Practical and worth emphasizing: the metadata is usually already in the folder they downloaded. Lab 8 has them open the XML in a browser. Also flag the format mismatch: an FGDC .xml from Utah's portal does not import automatically into QGIS the way it does into ArcGIS Pro, which is why Lab 8 has them create metadata by hand. -->

---

<!-- _class: lead -->

# Reading metadata: is this data fit for use?

---

# A fitness-for-use checklist

<div class="columns" style="align-items:start;">
<div>

1. **Scale / resolution** — what is the smallest thing this can represent?
2. **Date** — when collected, when updated?
3. **CRS and units** — projection, datum, feet or meters?
4. **Completeness** — is anything missing or unmapped?

</div>
<div>

![w:340 center](images/md-fitness-checklist.jpg)

5. **Accuracy and lineage** — how was it made, and from what?
6. **Attributes** — is every column defined?
7. **Constraints** — license, restrictions, required credit
8. **Contact** — who answers questions?

</div>
</div>

<!-- Tell them to run this list on the datasets in Lab 8 and again on every dataset in the site-selection project later in the semester. Anything you cannot answer from the metadata is a risk you are carrying into your design. -->

---

<!-- _class: quiz -->

# Which dataset would you use?

![bg right:40% w:94%](images/md-two-datasets.jpg)

You are laying out a new road west of Lehi and you need building footprints.

<div class="columns" style="align-items:start;">
<div>

**Dataset A**
Collected 2013, 1:24,000, no lineage given, no contact

</div>
<div>

**Dataset B**
Collected 2024, from 6-inch imagery, lineage documented, county GIS contact listed

</div>
</div>

<ol type="A">
<li>A</li><li>B</li><li>Either</li><li>Neither, until you check something else</li>
</ol>

<!-- Hypothetical example. B is the obvious answer, but push on D: you still do not know either dataset's coordinate system or use constraints from what is printed here, and a 2024 footprint layer digitized for planning purposes is still not a survey. The habit to build is "what did the metadata not tell me?" -->

---

# Worked example: Utah County Boundaries

<div class="columns" style="align-items:start;">
<div>

- Download the shapefile from the Utah portal
- Unzip it and open the `.xml` in a browser: it is plain text
- Search for **`UGRC`** to find *who*
- Search for **`metd`** to find *when* — the metadata date, written `YYYYMMDD`

</div>
<div>

![w:340 center](images/md-utah-county.jpg)

- Search for **`bounding`** to find *where*
- Read the abstract and keywords for *what*
- Read the purpose for *why*
- The coordinate system is **not** in the XML — it is in the `.prj` file in the same folder

</div>
</div>

<!-- This is Part 1 of Lab 8, so treat it as a preview and let them follow along if they have laptops open. The .prj point catches almost everyone: the CRS lives in a separate file from the rest of the metadata. -->

---

# Where to find data *with* metadata

<div class="columns" style="align-items:start;">
<div>

**[gis.utah.gov/data](https://gis.utah.gov/data/)**

- Utah Geospatial Resource Center (UGRC, formerly AGRC)
- The state's official clearinghouse for spatial data, and one of the oldest in the country
- Nearly everything ships with a metadata record

</div>
<div>

![w:340 center](images/md-data-portals.jpg)

**[data.gov](https://www.data.gov)**

- The U.S. federal open-data catalog
- Hundreds of thousands of datasets, wildly varying metadata quality
- Great practice at deciding what you cannot trust

</div>
</div>

<!-- Quiz 7 Part 2 sends students to both of these. Do not browse them live here: the hands-on session opens a UGRC product page and a thin data.gov page right after the slides, so finish the deck and switch to the browser. -->

---

# Metadata in QGIS: Layer Properties > Metadata

![h:490 center](images/md-qgis-metadata-panel.png)

<!-- QGIS 3.44 Layer Properties, Metadata page, for the UGRC Utah County Boundaries layer with the identification fields filled in. Right-click a layer, Properties, Metadata, and you get the ISO-style tabs: identification, categories, keywords, access, extent, contact, links, history, validation. This is the hand-off slide: leave it up, switch to QGIS, and start the hands-on walkthrough from this dialog. -->

---

<!-- _class: activity -->

# Final Thoughts

<div class="columns" style="grid-template-columns: 1.7fr 1fr; font-size: 0.74em;">
<div>

**Quiz: Fit for Your Use?** Eight questions on your phone: the **standards** and where the record **lives**, then reading a record and **deciding**. **Scan the code**, or open the link under it.

- Not graded, and every answer explains itself
- Good practice for Quiz 7 and Lab 8

**Before next class**

- **Quiz 7: Metadata** and **[Lab 8: Metadata](https://byu-hydroinformatics.github.io/cce114-geomatics/assignments/lab-08/)** are due **Saturday, 11:59 pm**
- **Quiz 8: Geoprocessing** opens today on Learning Suite and is due **Saturday of next week**
- Reading for next week: *GIS Fundamentals*, Chapter 9 (Basic Spatial Analysis)
- Record today's activity on Learning Suite
- Questions? Office hours: [calendly.com/dan-ames/office-hours](https://calendly.com/dan-ames/office-hours)

</div>
<div>

![w:300 center](images/md-quiz-fitness-qr.png)

<span style="font-size: 0.45em; color: #4a5568;">byu-hydroinformatics.github.io/cce114-geomatics/quizzes/fitness/</span>

</div>
</div>

<!-- Show this at the end of the hands-on session, not after the slides. Lab 8 Part 1 is the metadata they just wrote in QGIS, so it should go quickly. -->

<!-- Split notes (2026-10-26): this deck is the second half of the original Day 16 "Spatial Metadata" deck, moved to Thursday because Tuesday ran long. The break is the "Metadata standards and styles" divider. The QGIS Metadata dialog slide moved from the middle of the standards section to the end so the deck hands off into QGIS. Due dates checked against Learning Suite 2026-10-26. -->
