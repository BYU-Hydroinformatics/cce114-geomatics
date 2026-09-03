# Week 4 Thursday: GPS Field Collection and Importing the Class Data

**Day 7 · Thursday · Field collection, then live demo in QGIS (Dr. Halgren)** · feeds [Lab 3](../assignments/lab-03/README.md)

## At a glance

| | |
| --- | --- |
| **Goal** | Students collect real positions with their phones, then watch those positions land on a map in QGIS in the right place, in metres, with the scatter between students visible as error. |
| **Why this week** | Tuesday Dr. Ames covered how GPS works, trilaterated Prague on paper, and found Air Force One. Today is the other half: what a phone position is once you have it. Lab 3 repeats this workflow with seven campus sites and a group average. |
| **Students bring** | A phone with a GPS app that shows full-precision latitude and longitude (not Google or Apple Maps; see below). Laptop with QGIS 3.44. |
| **Graded item** | *In Class Activity: GPS Class Activity* (5 points). Students enter three positions in the class sheet and record the three site names on Learning Suite. |
| **Feeds** | Lab 3: GPS Data Collection and Importing Into QGIS. Due Saturday. |

## Before class

- [ ] The class Google Sheet open on the projector at the **GPS activity** tab (linked from the Week 4 entries on Learning Suite). The header row is `Your Name, Location Name, Latitude (Decimal Degrees), Longitude (Decimal Degrees), ...` with three example rows. Clear last semester's student rows if any remain.
- [ ] The campus site list from Lab 3 Part 1 printed or on a slide (Joseph statue in the JSB grove, Tree of Life, Testing Center lobby, Maeser statue, Tau Beta Pi statue by the Clyde, the bridge to the LSB, the ESC pendulum, the library entrance windows, the JFSB fountain, the bike rack between the Talmage and JFSB, the Brigham Young statue south of the ASB, the TNRB 4th-floor bust, the MOA entrance, the Victory Bell, Cosmo in the Bookstore).
- [ ] A TA stays in the room to watch belongings while students are out.
- [ ] Free GPS apps to suggest: **GPS Status** or **GPS Test** (Android), **GPS Coordinates** or the built-in **Compass** app (iPhone; it shows degrees, minutes, seconds, so they need to convert or use another app). Any app that shows five or more decimal places of a degree is fine.
- [ ] QGIS open with the Google satellite XYZ basemap and the project CRS set to **EPSG:26912**, so the import lands in metres immediately.
- [ ] The [tagis.dep.wv.gov/convert](https://tagis.dep.wv.gov/convert/) converter open in a tab for the cross-check.

## Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | Instructions: groups of two or three, three sites each from the list, full precision, enter rows in the sheet before coming back |
| 0:06 | Students out of the building collecting (20 minutes; set a timer and a hard return time) |
| 0:26 | Download the sheet as CSV; import into QGIS as a delimited text layer |
| 0:33 | Reproject to UTM, add easting and northing fields, cross-check one point in the converter |
| 0:40 | Measure the scatter: two students at the same site, distance between their points |
| 0:46 | Record completion on Learning Suite; Lab 3 pointer |

## Walkthrough

### 1. Instructions before they leave (3 minutes)

Say these five things and put them on the screen:

1. Groups of two or three. Each person records their own reading at each site, even standing together. That difference is the point.
2. Pick **three sites** from the list. Stand exactly at the spot described.
3. Record **every digit** your phone shows. `40.2466` is not good enough; `40.246604` is.
4. Latitude is the first number, about 40.25 here; longitude is about **negative** 111.65. West longitudes are negative in decimal degrees.
5. Type your rows into the **GPS activity** tab (name, site name, latitude, longitude) before you come back in. Be back by the time on the screen.

### 2. From the sheet to QGIS (7 minutes)

1. In Google Sheets, **File > Download > Comma Separated Values (.csv)** for the GPS activity tab. Save it as `class_gps.csv`.
2. If the sheet has stray rows (blank names, the example rows, a `N`/`W` suffix on numbers), fix them in the CSV now, out loud. Real field data is messy; this is normal.
3. In QGIS: **Layer > Add Layer > Add Delimited Text Layer...** File name = the CSV. File format: CSV. Under **Geometry Definition** choose **Point coordinates**, X field = the longitude column, Y field = the latitude column, Geometry CRS = **EPSG:4326 (WGS 84)**. Click **Add**.
4. The points appear on campus. If one is in the ocean or Asia, a sign is wrong or latitude and longitude are swapped. Find whose it is and fix the row; that is the lesson.

### 3. Metres, not degrees (7 minutes)

1. Point at the bottom-right CRS badge: the project is **EPSG:26912, NAD83 / UTM zone 12N**. The layer is stored in degrees but drawn in metres; QGIS reprojects on the fly.
2. Make it permanent: right-click the layer > **Export > Save Features As...** Format GeoPackage, file `class_gps.gpkg`, CRS **EPSG:26912**. Add the saved file to the map.
3. On the new layer, open the **Field Calculator**: new field `easting`, decimal, expression `$x`; then `northing` with `$y`. Sanity check: eastings near 444,000 to 445,000 and northings near 4,455,000 to 4,456,000.
4. Paste one student's latitude and longitude into the converter with output set to **UTM NAD83 Zone 12N**. It should match the field calculator to within a metre. Two tools, one answer.

### 4. Seeing the error (6 minutes)

1. Pick a site that several students visited. Zoom in until their points separate.
2. **Measure Line** tool (the ruler): click from one student's point to another's. Ten metres apart at the same statue is typical for a phone. Ask why: buildings, sky view, whether the phone had settled.
3. Optional if time: **Vector > Geometry Tools > Mean Coordinate(s)** grouped by the site-name field. That group average is what Lab 3 asks them to compute by hand.

## Student activity

Students must have entered three rows in the GPS activity sheet during the field time. On Learning Suite, they open **In Class Activity: GPS Class Activity**, mark it complete, and type the names of the three sites they entered. Full credit for three rows in the sheet and the names recorded.

## Lab 3 pointer

Lab 3 Part 1 is the same collection at seven sites in groups, with a group average and a conversion to UTM in the converter. Part 2 is today's import, plus creating a polygon of the campus and computing its area. Students who kept today's CSV and GeoPackage have Part 2 half done.

## Common snags

- **All the points are stacked in one place or in the Gulf of Guinea.** Latitude and longitude are swapped, or the longitude lost its minus sign. Check the X and Y field choices in the import dialog.
- **A point is 100 km off.** Someone typed `40.2466 N` with a letter, so the field imported as text. Strip the letters in the CSV and re-add.
- **"Layer has no CRS" or points do not draw in metres.** The Geometry CRS in the import dialog was left blank. It must be EPSG:4326 because that is what phones report.
- **`$x` returns degrees.** They ran the field calculator on the original CSV layer, not the reprojected GeoPackage. `$x` is in the layer's own CRS.
- **Phones report only four decimals.** The app is rounding. Switch to one of the apps listed above.

## Links

- [Day 7 lecture page](../lectures/day-07.md)
- [Lab 3: GPS Data Collection and Importing Into QGIS](../assignments/lab-03/README.md)
- Tuesday's decks: [GPS, Part 1](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-06/gps-part-1.html) and [GPS, Part 2](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-07/gps-part-2.html)
