SUMMARY
======================
The sinking of the RMS Titanic is one of the most infamous shipwrecks in history.  On April 15, 1912, during her maiden voyage, the Titanic sank after colliding with an iceberg, killing 1502 out of 2224 passengers and crew. This sensational tragedy shocked the international community and led to better safety regulations for ships.

The dataset is publicly available at https://www.kaggle.com/ and contains a sample of 891 passengers out of 2224. This project tries to anylyze and visualize the data itself, and what factors helped one group of passengers to survive.

From the Visualizations  I find the below factors were key to survival.

	- Females survivals rates are much more higher than that of males. Gender played a vital role during the disaster.
	- Class played a much vital role during the disaster. Third class is where most of the passengers perished.
	- Children were saved slightly higher than rest of the Age Groups. In fact it's the age group where more were saved than died. 


DESIGN
======================
Data Conversion
---------------
The input data was in a raw format, and formatted the data accoringly so that it will be easier to plot and analyse. Reformatted column Survivals as "Died/Survived" instead of 0/1, Class as "First/Second/Third" instead of 1/2/3 etc. Added a new field named Age Group according to the Age. Age 0 - 15 is represented as Child, 15 - 25 as Youth, 25 - 40 as Adult etc. 
A separate python module was written for this that converted the input data accordingly before being used by D3.


The story is designed in 3 charts(Dimple), and the webpage is divided into 3 sections. The sectons are below.

	- Header section, does not change with charts
	- Chart section, displays the chart and changes per user action
	- Summary section, displays the summary of analysis and changes with chart category

The below 3 categories of chart are displayed.

	- Summary: Summarizes input passenger data, example - count of passengers by Sex, Class, Embarkment, Age Group. Bar chart is used.
	- Survivals: Summarizes survivals by categories like Sex, Class, Embarkment, and Age Group. Vertical Grouped Bar chart is used. RED color was used for Deaths, and GREEN was used to mark survivals.
	- Survivals by multiple category: User can select 2 category from <Sex, Class, Embarkment, Age Group>. Based on the user selected inputs, the chart is refreshed. Ring Matrix is used.

Dimple.js was used for creating the chart. D3.js was used to maintaining the chart and navigating between charts.


FEEDBACK
======================
1. From "Nok Lam Chan"
Comment: Hi, it looks good. In the last chart. I found that if I change horizontal axis, the graph won't refresh. It only refreshes when I also change vertical axis. You may want to check on that.

Action: Changed the design as Nok suggested. Now selecting any category refreshes the last chart.

2. From "Santhosh Naganathan"
Comment: Hi Sourabh,
Very interesting & well done. Have performed the same using Bokeh couple of months ago with a group of college kids :). 

3. From "Sanmoy Das"
Comment: Hi, it looks very good. I would tell you to do some cosmetic change in the charts. Remove the grid lines from the first 2 charts, and add gridlines to the last chart to add a tabular feel.

Action: Changed the chart as suggested, and modified the gridlines.


RESOURCES
======================
https://www.kaggle.com/c/titanic

http://dimplejs.org/examples_viewer.html?id=bars_vertical_grouped

http://dimplejs.org/examples_viewer.html?id=ring_matrix

https://github.com/PMSI-AlignAlytics/dimple/wiki

https://github.com/d3/d3/wiki/Tutorials

https://www.w3schools.com
