# Week 9 Hands-On — Writing and Evaluating Metadata

**Hands-On Practice**{ .badge .badge-handson } · *Day 17 · Thursday of [Week 9 — Metadata](../weeks/week-09.md)*

### Topics

- Creating and editing metadata in QGIS
- Finding and evaluating datasets on gis.utah.gov and data.gov

<!-- runsheet -->
**Feeds** [Lab 8](../assignments/lab-08/README.md).

### At a glance

| | |
| --- | --- |
| **Goal** | Students write metadata for a layer in QGIS, save it with the data, and evaluate a published dataset against the six questions (what, who, where, when, why, how). |
| **Why this week** | Tuesday was the what and why of metadata, with the melodrama. Today students produce it rather than read it. Lab 8 asks for metadata on Utah County layers and a wetland dataset, and Quiz 7 sends them to gis.utah.gov and data.gov. |
| **Students bring** | Laptop with QGIS 3.44. Any layer they already have (the Week 2 Utah County boundary is ideal). |
| **Graded item** | *In Class Activity: AGRC Metadata* (5 points). Each student fills one row of the **AGRC Metadata** tab in the class Google Sheet for a dataset they evaluated. |
| **Feeds** | Lab 8: Metadata. Due Saturday. Quiz 7 closes Saturday; Quiz 8 opens today. |

### Practice run before class

> [!TIP]
> Twenty minutes, mostly filling in a dialog. The value is knowing where each of the eight
> metadata pages lives before you are standing at the projector.

**What you need.** QGIS 3.44 LTR, the county boundary from [UtahCountyData.zip](https://github.com/BYU-Hydroinformatics/cce114-geomatics/releases/download/course-data-2026/UtahCountyData.zip), a UGRC
product page open at [gis.utah.gov/products/sgid](https://gis.utah.gov/products/sgid/), and one
thin [data.gov](https://www.data.gov) dataset page for contrast. Find that thin one in advance;
hunting for a bad example live wastes five minutes.

**Do this, in order.**

1. On the UGRC page, locate the six answers out loud: what the data is, who stewards it, where it
   sits (usually NAD83 UTM 12N), when it was last updated, why it exists, and how it was made.
   Then find the license.
2. In QGIS, right-click the layer > **Properties > Metadata** and walk all eight pages in order:
   **Identification**, **Categories**, **Keywords**, **Access**, **Extent**, **Contacts**,
   **History**, **Validation**.
3. Write a real two-sentence abstract, pick an ISO category, add three keywords, set the license,
   click **Set from layer** for the extent, add yourself as `pointOfContact`, and write three
   history lines.
4. Open the **Validation** page and watch the remaining gaps disappear as you fill them.
5. **Metadata > Save metadata to file** to write a `.qmd` next to the layer, and find it in the
   Browser panel. For a GeoPackage layer use **Save to database** instead, then copy the
   GeoPackage to a new folder, open it in a fresh project, and confirm the metadata came along.
6. Open **Layer Properties > Information** and see your abstract and contacts rendered there.
7. Now try answering the same six questions from the thin data.gov page. Two or three will be
   impossible, which is the point of the exercise.

**You are ready when** you can reach any of the eight pages without hunting, and you have a `.qmd`
on disk you can open in a text editor to show it is only XML.

**The one that bites.** Editing metadata and clicking OK saves nothing durable. Without **Save
metadata to file** or **Save to database**, it lives only in the project file.

### Before class

- [ ] The class Google Sheet open at the **AGRC Metadata** tab. Its columns are: Name, Name of the Dataset, Link to download, What does the data represent, Who created it and who maintains it, Spatial Reference, Why (purpose), How was it created, When created or updated, Where, Key attributes. Clear old rows.
- [ ] A UGRC product page open, for example the Utah County Boundaries or Roads page on [gis.utah.gov/products/sgid](https://gis.utah.gov/products/sgid/), and one [data.gov](https://www.data.gov) dataset page with thin metadata for contrast.
- [ ] QGIS open with the county boundary loaded.
- [ ] Learning Suite open to the *AGRC Metadata* activity.

### Plan (50 minutes)

| Time | Segment |
| --- | --- |
| 0:00 | Mini-devotional |
| 0:03 | Read metadata on a UGRC product page: find the six answers |
| 0:09 | QGIS Layer Properties > Metadata: fill the Identification, Categories, Keywords, Access, Extent, Contacts, and History pages |
| 0:19 | Save it: to a `.qmd` sidecar and into the GeoPackage; show it travel with the data |
| 0:24 | A dataset with bad metadata: what you cannot tell, and what could go wrong |
| 0:29 | Students: evaluate one dataset, fill a row in the sheet |
| 0:43 | Lab 8 pointer; Quiz 7 and Quiz 8 reminders |

### Walkthrough

#### 1. Reading metadata that exists

On the UGRC product page, find and read aloud: the description (what), the steward and contact (who), the coordinate system, usually NAD83 UTM 12N (where), the update date and cadence (when), the purpose statement (why), and the source and method, such as compiled from county recorders or digitized from imagery (how). Then the license. Say: if any of these is missing you are guessing, and Tuesday's melodrama was about what happens when you guess.

#### 2. Writing it in QGIS

Right-click the layer > **Properties > Metadata**. Walk the left-hand pages:

1. **Identification**: Identifier (a stable name), Title, Type `dataset`, Language, Abstract. Write a real abstract in two sentences: what the features are and what they are for.
2. **Categories**: pick an ISO category (Boundaries, Transportation, Inland Waters).
3. **Keywords**: a vocabulary of `GCMD` or just `Free` and three terms.
4. **Access**: Fees `none`, License `CC BY 4.0` or the UGRC license, a Rights line naming the source.
5. **Extent**: **Set from layer** for the spatial extent and CRS; add a temporal extent if the data has a date.
6. **Contacts**: name, organization, email, role `pointOfContact`.
7. **History**: one line per processing step: `Downloaded from UGRC SGID 2026-10-29`, `Reprojected to EPSG:26912`, `Clipped to Utah County`.
8. **Validation** page: click it; it lists what is still empty.

#### 3. Save it so it survives

- **Metadata > Save metadata to file** writes a `.qmd` next to the layer. Show it in the Browser panel.
- For a GeoPackage layer, **Save to database** stores it inside the file. Copy the GeoPackage to a new folder, add it to a new project, and open Properties > Metadata: it is still there. Metadata that lives in a Word file on someone's laptop is not metadata.
- The **Layer > Layer Properties > Information** page now displays the abstract and contacts. That page is what a colleague sees first.

#### 4. Bad metadata, on purpose

Open the thin data.gov dataset. Ask the room to answer the six questions from the page alone. Usually two or three are impossible. Ask what they would have to assume to use it in a design, and what happens when the assumption is wrong. This is the Quiz 7 Part 2 exercise in miniature.

### Student activity

Each student picks one dataset from gis.utah.gov or data.gov (not one already taken by the person next to them), reads its metadata, and fills one row in the **AGRC Metadata** tab of the class sheet: name, dataset, link, and the six answers plus spatial reference and key attributes. Where the metadata does not say, they write "not stated." Then they mark **In Class Activity: AGRC Metadata** complete on Learning Suite with the dataset name. Full credit for a complete row.

### Lab 8 pointer

Lab 8 Part 1 is today's QGIS metadata on the Utah County boundary and roads layers; Part 2 evaluates the Lehi wetland shapefile, whose metadata is deliberately incomplete. Everything they need is in the Metadata dialog they just used.

### Common snags

- **The Metadata page is empty after reopening.** They edited and clicked OK but never saved to file or database; layer metadata in the project only lives in the project file.
- **Set from layer does nothing for extent.** The layer has no CRS assigned. Fix Source > Assigned CRS first.
- **Validation still complains.** It requires Identifier, Title, Type, Language, Abstract, a Contact, and a License. Fill those seven.
- **The class sheet row overwrites someone else's.** Have students add rows at the bottom and put their name first.
- **`.qmd` is not recognized on the lab machines.** It is just XML; open it in Notepad to show it.

#### Links

- [gis.utah.gov/data](https://gis.utah.gov/data/) and [data.gov](https://www.data.gov)
