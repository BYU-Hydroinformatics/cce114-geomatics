# Week 9 — Metadata

**Due this week (Saturday, 11:59 pm unless noted):**

- [Quiz 7: Metadata](../assignments/deliverables.md#reading-quizzes)
- [Lab 8: Metadata](../assignments/lab-08/README.md)

## Tuesday — Metadata, Part 1

*Day 16 · Concepts lecture (Dr. Ames)*

### Topics

- What metadata is and why it matters
- Metadata standards and styles
- Reading metadata to judge whether data is fit for use

### Slides

- [Spatial Metadata](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-16/metadata.html)

### Materials

- [A brief metadata melodrama](http://t.ly/rPYx)

### In-class activity

What I learned about metadata: write down a couple of things you learned today. Record your completion on Learning Suite.

<!-- tuesday-notes -->
*In the [Spatial Metadata](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-16/metadata.html) deck, "A brief metadata melodrama." The script is below; the original is "Metadata Football Data.docx" in the Lectures/Archived folder.*

**Setup.** Nine volunteers, each handed one role card printed from the script. Props are optional; a cape for Data helps.

**Cast.** Data; the villains Unreliability and Irrelevance; the six heroes What, Where, When, Why, How, Who.

**Run.** Read in order. Data reads the opening line, the villains attack, the heroes arrive one at a time, and Data closes. Eight minutes including applause.

**Script.**

**Data:** Hello, my name is Data. I am not a robot on Star Trek. I am an important bit of spatial information about the world. I can be very useful for solving engineering and science problems. Oh no! Who is that? I hope it isn't my old nemesis, Unreliability!

**Unreliability:** It is I! (evil laugh) Unreliability! And I am here to destroy your value, Data! Since you have no metadata, I am going to make you worthless and meaningless to future users. Sure, maybe that one person who created you will still love you and care about you, but no one else! Because they have no clue what you are, they will dare not use you for anything! (another evil laugh)

**Data:** Woe is me! Will no one come to my rescue?

**What:** Have no fear, Data! I am here to save you! I am the metadata element of "What"! I will describe what you are. I'll be like a citation or bibliography for you! No one will ever have to wonder what you are again!

**Where:** Have no fear, Data! I am here to save you too! I am the metadata element of "Where"! I will tell the world what part of the world you represent! I will give them your latitude (pause for cheer from the audience), your longitude (pause for cheer). I will give them (wait for it) your projection information!

**When:** Have no fear, Data! I am here to save you too! I am the metadata element of "When"! I will tell the world when you were created! I will tell the world what date or time you represent! No one will ever again falsely accuse you of being older or younger than you are! No early retirement center for you, Data! I love you, Data! (gets down on one knee) When, Data? When will you love me back?

**Data:** I feel so happy now to be protected by What, Where, and When! Yay! But wait, who is that coming to attack now? Oh dear, could it be? No! (scream) It's Irrelevance!

**Irrelevance:** Ha ha ha ha (evil screeching laugh). It's too late for you, Data! I am Irrelevance! Some people call me "So what!" I am here to destroy you once and for all! You are nothing to me! There is no reason for your existence! I will make sure the world knows you have no purpose! We don't even know how you were created or by whom! For all you know... (Darth Vader voice) I AM YOUR FATHER!

**Why:** Have no fear, Data! I am here to save you! I am the metadata element of "Why"! I will tell the world why you were created! Your life will now have real meaning! If the world knows why you were created then they can better use you for your intended purpose! No longer will people be trying to misuse you for weird and inappropriate purposes! I am awesome! (small dance) (beats chest) (chanting: Why! Why! Why! Why!)

**How:** Have no fear, Data! I am here to save you! I am the metadata element of "How"! I will tell the world how you were created! Were you collected by GPS? Satellite? A guy with a yardstick? You will never have to wonder again! I am all-knowledgeable. (shouting) I will tell you how!

**Who:** Have no fear, Data! I am here to save you! I am the metadata element of "Who"! I will tell the world who created you! No longer will you wonder who brought you into being! The world will know! The world must know! I am about to tell you right now! The words are about to come out of my mouth! Here it comes! I am about to say it! Your... creator... was...

**Data:** Well, that was strange, but I feel so much safer and happier now! I have meaning! I have purpose! I... AM... DATA! (shouting)

*Same deck, "In-class activity: What I learned about metadata."*

Five minutes after the melodrama. Students write down a couple of things they learned, one of which they will actually check the next time they download data, and enter them on *In Class Activity: What I learned about metadata*. Collect two or three answers out loud.

## Thursday — Writing and Evaluating Metadata

*Day 17 · Demo and hands-on (Dr. Halgren)*

<!-- thursday-notes -->
**Feeds** [Lab 8](../assignments/lab-08/README.md).

### At a glance

| | |
| --- | --- |
| **Goal** | Students write metadata for a layer in QGIS, save it with the data, and evaluate a published dataset against the six questions (what, who, where, when, why, how). |
| **Why this week** | Tuesday was the what and why of metadata, with the melodrama. Today students produce it rather than read it. Lab 8 asks for metadata on Utah County layers and a wetland dataset, and Quiz 7 sends them to gis.utah.gov and data.gov. |
| **Students bring** | Laptop with QGIS 3.44. Any layer they already have (the Week 2 Utah County boundary is ideal). |
| **Graded item** | *In Class Activity: AGRC Metadata* (5 points). Each student fills one row of the **AGRC Metadata** tab in the class Google Sheet for a dataset they evaluated. |
| **Feeds** | Lab 8: Metadata. Due Saturday. Quiz 7 closes Saturday; Quiz 8 opens today. |

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
