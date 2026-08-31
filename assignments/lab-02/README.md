# Lab 2: Map Symbology and Layouts

**Civil and Construction Engineering 114 — Geomatics**

Winter 2026 · Dr. Dan Ames

Brigham Young University   
Lab assignment developed by Nathan Godfrey and Dr. Ames

![World map with QGIS and BYU logos](images/title-hero.png)

## **Background**

Your GIS skills will allow you to assist in a wide variety of work, not just engineering. GIS is used in various fields, including banking, public health, and national defense. It helps produce the food you eat (irrigation, pest control, weather forecasting, soil/crop analysis, shipping routes), takes you to school (Google/Apple Maps, traffic control, snowplows), and powers your life (electricity, internet, cell coverage). GIS organizes the world around you, and the more creatively you can use it, the more opportunities you’ll find in any field. 

The situation in this problem statement doesn’t reflect a full-time job, but is a genuine application of GIS in the film industry. As you complete this lab, consider where else your GIS skills could be applied.  
Utah has a serious film resume, by the way. Kanab, down in the state's red rock country, hosted so many Westerns (more than 100 productions have been shot in Kane County since Tom Mix's Deadwood Coach in 1924\) that director William Wellman nicknamed it "Little Hollywood" while filming Buffalo Bill there in the 1940s. Today's location scouts still do their first pass the way you're about to: with satellite imagery and GIS layers, long before anyone drives out for a look. Source: https://www.visitutah.com/places-to-go/cities-and-towns/kanab/little-hollywood-museum

In this lab, you’ll repeat the previous skills of finding, downloading, and adding data to QGIS. Then, you will customize the symbology (how the data is displayed on the map). Many datasets include more than just a **point**, **line**, or **polygon**. They’ll also include names, reference codes, dates, and other data, which we can use symbology to visualize. Last, you’ll create a map layout, essentially a polished arrangement of your map and various cartographic elements on a page. 

## **Problem Statement**

You, a GIS pro, have been approached by a film production company to help scout locations for an upcoming movie. Although they haven't provided any plot-specific details, they have asked for assistance in identifying locations that meet the following criteria:

1. A location within the city limits of a small town (let’s say a population significantly less than anything in the Provo/Orem/Springville area). The smaller the better.  
2. There must be an airport within the city/town limits  
3. There must be a major highway/freeway that runs through the town

Given these requirements, you think the project might be an action film. It could also be a documentary on transportation engineering in small towns… Huh. Regardless, you need to create a map according to their specifications.

## **Learning Objectives**

* Repeat skills from the previous lab  
* Learn how to differentiate between and use point, line, and polygon vector data  
* Learn how to customize symbology in QGIS  
* Learn how to use symbology to represent data attributes  
* Learn how to create and use labels for your data in QGIS  
* Learn how to produce a professional map layout

## **Software and Data**

* For this lab, we will use the GIS software application QGIS. This is a free and open-source GIS package that runs on Windows, Mac, and Linux operating systems. The software is pre-installed on the computers in the Clyde Building 234 computer lab. You can also download it and install it on your own computer from this website: [https://www.qgis.org/](https://www.qgis.org/). We will be using the latest *Long Term Version* in this course.   
* There are no custom data downloads for this lab. Follow the instructions to download data from the State of Utah GIS website: [https://gis.utah.gov/products/sgid/](https://gis.utah.gov/products/sgid/)  
* Google imagery will also be used as a base layer. 

## **Instructions**

### **Data and Map Setup**

1. Open a new project  
2. Add a satellite image base layer using either the Data Source Manager or the QuickMapServices plugin as described in the previous lab.  
3. Look at the bottom right of your QGIS window for a wireframe globe next to 4 letters followed by a number. This shows the current **coordinate reference system** (a topic we’ll discuss further at another time). Click on that.

4. In the “Project CRS” window that pops up, type “26912” into the Filter. Select the “NAD83 / UTM zone 12N” projection and click OK. Press OK on any other windows that pop up to choose default datum transformation options.

5. **SAVE** your project  
6. Use the UGRC website from last time to find the data you need for this lab. The Utah GIS website is here: [https://gis.utah.gov/products/sgid/categories/](https://gis.utah.gov/products/sgid/categories/)   
   1. Download the “Utah Roads” data in the Transportation category, and “Utah Municipal Boundaries” data in the Boundaries category.  
   2. **WARNING**: The Utah Roads dataset is very large (as you might imagine), so it will likely take a LONG time to download over a slow dorm connection. If it doesn’t download completely, try doing it on a fast WIFI on campus.   
   3. **NOTE:** If the shapefiles for these datasets won’t download (i.e., the Utah server sometimes fails), you can also choose the GeoPackage download, which can be loaded into QGIS without needing to be unzipped. **It’s just another file format for the same data\!**   
7. Use this link to download the point data for Utah Airports ([https://gis-support-utah-em.hub.arcgis.com/datasets/utah::utah-airport-locations/about](https://gis-support-utah-em.hub.arcgis.com/datasets/utah::utah-airport-locations/about))   
8. Download and unzip the file for each, then drag and drop the folder for each onto your map.  
   1. **NOTE:** If you downloaded GeoPackage files, then you can literally just drag and drop the file into your map, or you can use the “Add Data” button to browse to the file and double-click it to open it. GeoPackage files don’t need to be unzipped.  
9. You should see 4 layers in the Layers Panel now. Three vector datasets (point, polyline, polygon) and your raster (image) basemap.

NOTE: Your exact layer names will depend on the download format. You might see names like Utah\_Municipal\_Boundaries, Municipalities, Utah\_Roads, or AirportLocations. The steps below refer to the municipal boundaries, roads, and airports layers; use whatever spelling shows up in your Layers Panel.  
![image1](images/image1.png)

### **Point Symbology**

10. Double-click on “airport\_locations” in the Layers Panel, and find the “Symbology” tab on the left side of the window that opens.  
11. You’ll see options to change the marker, adjust its color, and more. We want more options. Click on “Simple Marker” in the box at the top. This will bring up different options.

12. Click the green \+ next to “Simple Marker” to add another layer to this symbol.  
13. Change the “Symbol layer type” to SVG Marker, and choose an SVG image at the bottom of the window.

14. Adjust the colors, sizes, and other elements of both marker layers until you achieve a symbol you like. Click OK.  
15. **SAVE** your project

### **Polyline Symbology**

16. Double-click on “roads” in the Layers Panel, and again find the “Symbology” tab on the left side of the window that opens.  
17. For our roads, we need to distinguish highways/freeways from the rest. One way to do this is by using categorized symbology. At the very top, change the dropdown from “Single Symbol” to “Categorized.”  
18. Change the “Value” dropdown to “CARTOCODE” ([UGRC](https://docs.google.com/spreadsheets/d/1jQ_JuRIEtzxj60F0FAGmdu5JrFpfYBbSt3YzzCjxpfI/edit?gid=1856320934#gid=1856320934) link)  
19. Click “Classify” at the bottom of the window. You should now see numbers 1-18 in different colors, though maybe not in numeric order (the codes are stored as text, so the list may run 1, 10, 11 … 18, 2, 3 …). Uncheck the checkboxes next to 6-18, wherever they appear in the list, and click OK. The numbered roads 1-5 represent interstates and major highways and should now be the only road lines visible on the map.  
20. Reopen the symbology for the roads layer, and set all roads with codes (values) 1-5 to the same color (any color easily visible on this map). You can change the color, line width, and other settings by double-clicking on the short sample line next to the associated number.  
21. While we’re here, double-click in the “Legend” column to edit what the map legend will display later. Replace the numbers 1-5 with “Highway”. Press OK to close the window.

22. **SAVE** your project\!

### **Polygon Symbology**

23. Next, we want to organize the symbology of city boundaries so it's easy to compare them and determine how their populations compare to those of other cities. **Graduated symbology** is a straightforward way to achieve this. Double click on the “municipal\_boundaries” layer and, in the symbology tab, change “Single Symbol” to “Graduated” in the dropdown at the top.  
24. Change “Value” to “POPLASTESTIMATE” so that QGIS organizes the cities by the latest population estimate. (If you downloaded shapefiles, this field shows up as “POPLASTEST” — shapefile field names are capped at 10 characters, a limit inherited from a 1980s database format.)  
25. Click “Classify.” You should now see ranges of numbers split into different colors.  
26. Set the “Classes” variable to 5\. You can play with this to see how it adds more or fewer color divisions to your range, but set it to 5 when you’re ready to move on.  
27. Choose a different color ramp (by clicking the dropdown arrow next to “Color ramp”) and invert it if you’d like. In this example, the cities with lower populations will be greener since that’s what the client is looking for.

28. Let’s make these polygons transparent so that we can still see the terrain below. Click “Layer Rendering” at the bottom of the window, then set the opacity slider to 40-50%. Press OK.  
29. Your map should look something like this:

![image2](images/image2.png)

### **Labels**

30. If you know your Utah geography really well, this result might be fine. However, it would be best to add labels for each city. Double-click on the “municipal\_boundaries” layer again, and this time find the “Labels” tab on the left.  
31. Change “No Labels” to “Single Labels” and make sure “Value” is set to the field with the city names (NAME)

32. Find “Buffer” in the left column and click on it. Check the box “Draw text buffer.”  
33. Experiment with the options for Text, Buffer, Background, and Shadow if desired. After clicking Apply or OK, you should see labels for each polygon on the map.

![image3](images/image3.png)

34. **SAVE** your project  
35. Identify a location that meets the criteria outlined in the problem statement. **Look for a city polygon of one of the two lower population categories (one of the greens, in this example) that contains both a highway and an airport.** Keep your map view zoomed in on this location, even though the examples from now on will show a different view (sorry, no free answers\!). If you have trouble with this step or need clarification, ask a classmate, a TA, or Dr. Ames for help.

### **Layouts and Cartographic Elements**

##### New Layout

36. Navigate to *Project\>\>New Print Layout…* and a new window will open for you to design a Layout (basically a print-view)  
37. Go back up to the top of your screen and navigate to *View\>\>Show Grid*. Ensure *that "Show Grid"* and *"Snap to Grid"* are checked. This will make your life much easier.

##### Adding a Map

38. Click the “Add New Map” button, ![image4](images/image4.png) then draw a box where your map will be located.  
39. Use the ![image5](images/image5.png) “Move item content” tool to zoom and pan around on this new layout map. Have this layout display the city/town you found that meets the film company’s criteria.

##### Neatline

40. Use ![image6](images/image6.png) “Add Shape” to create a rectangle around the entire page that will act as your neatline.

![Layout window with neatline rectangle and Items panel](images/anchored1.png)

##### Legend

41. Now use the ![image7](images/image7.png) “Add Legend” button and draw a box for the legend. You’ll notice that it doesn’t follow the boundaries you drew. We’ll have to edit its content to fit our layout.  
42. Go to the “Item Properties” tab in the bottom right panel. Uncheck “Auto update” under “Legend Items” so that we can freely edit the contents.  
43. Select your basemap (e.g., “Google Satellite”) from this list, then click the red minus “-” button to **remove** it from the legend. Do the same for each layer that isn’t included in this layout.  
44. Double-click on any legend item in the panel to change the text. Do this to change confusing file/layer names to something that helps the viewer understand your layout.  
45. Add a legend background if needed by scrolling down in the “Item Properties” and expanding the “Background” section. Choose a color that makes each legend item clearly visible.

![Editing legend items in Item Properties](images/anchored2.png)

##### North Arrow and Scale Bar

46. Use ![image8](images/image8.png)and ![image9](images/image9.png) to add a north arrow and a scale bar to your layout.  
47. For the north arrow, use the “Item Properties” panel to select an **arrow**, and scroll down in the same panel to “SVG Parameters” to change the colors.  
48. For the scale bar, use the “Style” and other options to change its look. Use the “Units” and “Segments” sections to change the bar units and length to be useful.

##### Title and Citation

49. Use ![image10](images/image10.png) “Add Label” to add a title to your layout. Draw the rectangle, then use the “Item Properties” panel on the right side to edit the text.  
50. Adjust the text size and alignment under “Appearance” in the same panel to fit your layout.

![Adding and editing a title label in the layout](images/anchored3.png)

51. Use “Add Label” again. This time, we’ll use it to add the necessary citations to the layout.  
52. In one text box/label, write your name, date, and lab number  
53. In the same text box or a new one, add the following data citations and projection information (adjust these for each lab):  
    1. “Basemap: Google Satellite”  
    2. “Data: UGRC”  
    3. “Projection: EPSG:26912”

##### Export Layout

54. **SAVE** your project  
55. For this class, you’ll want to export your layouts as a PDF. With the layout open, in the top menu, navigate to *Layout\>\>Export as PDF…*  
56. Give your layout a name and leave all of the export options at their defaults.  
57. Save it anywhere, but keep track of where you saved it in case Learning Suite loses your submission or something else happens. Your final PDF should resemble this (with your own name, information, and map view). Your map will feature your own styling, colors, icons, and more. Just ensure they meet the project's goals. In other words, you’re not recreating this map exactly; make your own map that meets the project goals. 

![image11](images/image11.png) 

### **Important Points**

- For optimal readability, it is generally best not to overlap items on the map. The north arrow and scale bar are the exceptions. To improve their readability, you may add backgrounds or font buffers to them and position them over the map in less important positions.  
- To edit a cartographic element after it has been placed, select it and use the “Item Properties'' tab. You can change almost anything about each map element.  
- “Lab 2” is not a suitable title for a map layout. Pick something that describes the content, such as “Filming Site Selection” or “Fault Lines Near BYU Campus.”  
- Legends should show all the layers used on the map, regardless of whether they are labeled. This is referred to as an “exhaustive legend.” As you’ve seen, editing the legend is doable. Also, the labels in a legend should be descriptive and professional; capitalize layer names, be descriptive, and avoid underscores or unprofessional symbols.  
- Often, satellite imagery is the standard basemap of choice. Depending on the purpose, different basemaps may be acceptable if they enhance the visual presentation and clarity of a map or if the lab specifies a basemap to use.  
- If necessary, you can also use blank space on a layout to accommodate additional maps, images, and text. Some maps need more explanation than a simple legend, though it is best to keep your maps simple so that they can be better understood.  
- **You may design your map in any way you wish, provided it contains the proper data sets, is professionally presented, and incorporates the necessary cartographic elements.**

## **Deliverables**

Submit a PDF file that contains:

1. Your name, date, class section, and lab assignment number  
2. Your map layout  
3. The name of your chosen city location  
4. The grading rubric, filled in with your self-evaluation

## **Grading Rubric**

The following rubric will be used to evaluate your lab assignment. Use this as a guide to ensure that you include all the required elements for this lab. Shown under “Score” is the maximum possible points you can receive for each item. 

In some cases, points are awarded on a "yes or no" basis, giving full points if something is present and none if it is not. In other cases, points are awarded on a scale, depending on how well you complete the task. Please keep this in mind. For example, if there is a written answer required, grading will be based on a scale of points, depending on the quality and completeness of your written answer.

Copy the rubric and paste it into your lab report. Fill in your self-evaluation of the rubric, showing how many points you feel you have earned for each item. 

| Requirement | Score |
| ----- | ----- |
| Create and include the required map layout: Google Satellite basemap layer is visible *(2 pts)* Proper custom symbology for each of the 3 data layers *(10 pts)* Roads layer only shows highways (cartocodes 1-5) *(2 pts)* Municipal boundaries layer is transparent *(2 pts)* Municipal boundaries are clearly labeled with city names *(2 pts)* Chosen location meets film company’s criteria *(4 pts)* Zoomed to an appropriate level that clearly shows which city/town you’ve chosen *(2 pts)* Includes all required cartographic elements: *(6 pts total)* Neatline *(1 pt)* Legend *(1 pt)* North Arrow *(1 pt)* Scale Bar *(1 pt)* Title *(1 pt)* Citations and name/date/lab \# *(1 pt)* | /30 |
| **Total** | **/30** |

## **Using AI on This Lab**

AI tools like ChatGPT and Gemini can be genuinely useful here, if you use them to learn rather than to skip the learning. Good uses: asking what a "cartocode" or graduated symbology actually is, decoding a cryptic QGIS error message, asking why your labels or legend aren't showing what you expect, or quizzing yourself on the difference between point, line, and polygon data before the exam. What's not okay: having AI pick your city for you, write your self-evaluation, or generate a map or screenshot you pass off as your own work. The whole point of this lab is that YOU can drive the symbology and layout tools — a skill you only get by clicking through them yourself. If you do use AI along the way, say so in your submission, and make sure you can explain and defend every part of your map as your own understanding.

* OK: "Explain what a graduated color ramp does in QGIS" or "What does this error mean: ..."  
* OK: "Quiz me on map layout elements and what each one is for"  
* Not OK: "Which Utah town has an airport and a highway and a small population?" — that's the deliverable, and finding it yourself is the fun part.

