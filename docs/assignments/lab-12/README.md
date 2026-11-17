# Lab 12: Choose Your Own Adventure

**Lab**{ .badge .badge-lab } · Due Saturday of Week 14, 11:59 pm · Introduced on Tuesday of [Week 13](../../weeks/week-13.md)

**Civil and Construction Engineering 114 — Geomatics**

Brigham Young University

*Your problem, your county, the Lab 11 workflow.*

![Five site-selection choices laid out side by side](images/fp-choose-problem.jpg)

## **What This Lab Is**

Lab 12 is the final project for CCE 114. It is a lab like the eleven before it, only you choose the
problem. In [Lab 11](../lab-11/README.md) you were handed the criteria, the data and the steps for
siting a Walmart in Utah County. In Lab 12 you pick what to site and where, write the criteria
yourself, find the data, and run the analysis in QGIS from start to finish.

You do Lab 12 **individually**. Everyone picks their own problem and county, does their own
analysis, and submits their own report. You are welcome to talk ideas over with classmates, but the
QGIS work, the maps and the writing must be yours.

## **The Rules**

* Choose **one** of the five problems below.
* Choose **one Utah county**, any county except Utah County (Lab 11 already worked there; the point
  is to carry the method somewhere new).
* **Sign up** in class on Tuesday of Week 13 with your name, problem and county. Only one or two
  students per county, first come, first served.
* Use at least **four** appropriate datasets.
* **Write the steps down first:** your criteria, the data that answers each one, the tool that
  does each step, and the order. Then run them.

## **Choose Your Problem**

Find a suitable location in your county for:

1. A **solar panel farm**
2. A **landfill**
3. An **airport**
4. An **LDS temple**
5. An **irrigation reservoir**

For whichever you pick, answer the same four questions you answered for Lab 11:

* **What are the criteria?** Write each one as something a computer can check: a number and a
  unit, such as "within 2 miles of a highway," not "close to roads."
* **What data are required?** Name the layer that answers each criterion and where it comes from.
* **What tools and analyses are needed?** Name the QGIS tool for each step.
* **In what order?** Draw the workflow diagram: layers as rectangles, tools as ovals.

## **Data**

The [UGRC SGID](https://gis.utah.gov/) is the place to start for Utah layers, through a download or
the web service connection from [Lab 6](../lab-06/README.md). If a layer you need does not exist,
digitizing your own is a legitimate data source, as long as your report says so. Every layer in your
report needs its source named.

Check the coordinate system of every layer before you run a distance tool, and reproject first if
it is in Web Mercator or latitude and longitude. This is the step that went wrong most often in Lab 11.

## **What to Include in Your Report**

The report is a brief technical document, not an essay: **4 to 5 pages**, mostly graphics with some
discussion. It must include at least:

* A **cover page**.
* A **problem statement:** what you are siting, where, and why.
* A **description of all the data** you used: every layer, where it came from, and its projection.
* A **workflow diagram** (layers as rectangles, tools as ovals), or at least a bullet list of your
  analysis steps in order. The diagram is worth the most points of any single item.
* **Two maps** with all the required elements, described below.
* A **discussion of your results**, ending with your **recommendation**: the site you would choose
  and why it won.

## **What to Include in Your Maps**

* One or more maps or screenshots of your **input data, intermediate data and processing steps**,
  showing the "in-between" layers you made on the way to the final map. These are where most of
  the grade separation happens: a single beautiful final map with no evidence of the processing is
  not a complete submission. Screenshots of the QGIS map canvas are fine for these, and be liberal:
  more screenshots of your work are better than fewer.
* A **final results map** made in Print Layout, with all the required cartographic elements: title,
  legend, scale bar, north arrow, neatline, data sources and projection.
* At least one **inset map** zoomed to your selected sites.
* A **point marker** on each selected site.

## **What to Hand In**

* **One PDF report**, submitted on Learning Suite, holding the write-up, the intermediate maps and
  data that show your processing steps, and the final results map. Not a folder of images and not a
  QGIS project file.
* Due the **Saturday of Week 14** at 11:59 pm.
* There is no presentation: the report is the deliverable.

## **Grading Rubric (60 points)**

| Item | Points |
| --- | --- |
| Problem statement | 5 |
| Data description | 5 |
| Workflow diagram | 15 |
| Maps | 15 |
| Appropriate, working analysis | 10 |
| Write-up | 10 |
| **Total** | **60** |

## **Getting Help**

The rest of class on Tuesday of Week 13, Thursday of Week 13 in a Winter semester (it is
Thanksgiving in Fall), the second half of Tuesday of Week 14, and Thursday of Week 14 are work
sessions. Bring your data and a specific
question: a tool that will not run, a projection mismatch, a layer you cannot find. Use the work
sessions for the hard parts and do the writing and map layout on your own time.

AI can help you plan a workflow and polish your writing; the QGIS work and the results must be your
own. See the [AI Use Policy](../../policies/ai-policy.md).

Slides from the kickoff: [Lab 12: Choose Your Own Adventure](https://byu-hydroinformatics.github.io/cce114-geomatics/slides/day-24/lab-12-choose-your-own-adventure.html).
