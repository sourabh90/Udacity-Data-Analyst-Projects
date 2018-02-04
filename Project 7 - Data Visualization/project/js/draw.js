var margin = 40, 
    width = 1200,
	height = 800;

/* Function used to remove null records from a category of data like Age Group, Embarked etc */
function nullFreeData(data, categoryToGroup) {
	var cleanData = [];
	var dataRecord;

	for (var i=0; i <= data.length-1; i++) {
		dataRecord = data[i];
		if (dataRecord[categoryToGroup] === "") {
			continue;
		}
		cleanData.push(dataRecord);
	}

	return cleanData;
}


/* Function to create the Bar-chart ordering rules depending on the category */
function getSeriesOrderRule(categoryToGroup) {
	var seriesOrderRule = {
		"Sex": ["Male", "Female"],
		"Class": ["First Class", "Second Class", "Third Class"],
		"Embarked": ["Southampton", "Cherbourg", "Queenstown"],
		"Age_Group": ["Child", "Youth", "Adult", "Mid-Age", "Old", "Very Old"]
	};

	return seriesOrderRule[categoryToGroup];
}


/* Main Draw Function -- invoked from index.html */
function draw(data) {
	"use strict";

   	var scaler = 0.6;					// Used to define chart size
	var lWidth = width * scaler,
		lHeight = height * scaler;

	var categories = ["Sex", "Class", "Embarked", "Age_Group"];	

	/* Function to Draw the bar charts 
	 * Category to group used to create the bars in the bar chart,
	 * and category to color is used to split the bars by category  
	 */
	function draw_bar_chart(categoryToGroup="Sex", categoryToColor = "") {

		// Remove nulls from categories
		if(categoryToGroup === "Embarked" || categoryToGroup === "Age_Group") {
			var cleanData = nullFreeData(data, categoryToGroup);
		} else {
			var cleanData = data;
		}

		// Create the SVG Element & Chart
		var svg = dimple.newSvg("#chartContainer", lWidth + margin, lHeight + margin);
	    var chart = new dimple.chart(svg, cleanData);
	    chart.setBounds(margin*1.5, margin*1.2, lWidth - margin*2, lHeight - margin*1.5);

		if(categoryToColor === "") {
			var x = chart.addCategoryAxis("x", [categoryToGroup]);
	    } else {
	    	var x = chart.addCategoryAxis("x", [categoryToGroup, categoryToColor]);
	    }

	    // Count by number of passgers by categories
	    var y = chart.addMeasureAxis("y","PassengerID");

	    /* Axis titles */
	    var seriesOrderRule = getSeriesOrderRule(categoryToGroup);
	    x.addOrderRule(seriesOrderRule);
	    x.ticks = seriesOrderRule.length-1;

	    y.title = "Number of Passengers";
	    y.ticks = 6;

	    if(categoryToColor === "") {
			var chartSeries = chart.addSeries(null, dimple.plot.bar);
	    } else {
	    	var chartSeries = chart.addSeries(categoryToColor, dimple.plot.bar);
	    	chart.addLegend(margin*2, margin, lWidth - margin*2 + 15, 40, "right");
	    }

	    chartSeries.aggregate = dimple.aggregateMethod.count;    
	    chartSeries.barGap = 0.3;

	    // Chart Title
	    var text = svg.append("text")
			.attr("x", chart._xPixels() + chart._widthPixels() / 2)
			.attr("y", chart._yPixels() - 20)
			.style("text-anchor", "middle")
			.style("font-family", "sans-serif")
			.style("font-weight", "bold");

		if (categoryToColor === "") {
			text.text("Passenger counts by " + categoryToGroup);
		} else {
			text.text( categoryToColor + "s by " + categoryToGroup);
		}

	    // Removing X axis tick lines
	    svg.selectAll('.dimple-gridline')
	    	.style("visibility", "hidden");

	    // Choose colors for Survivals
	    if (categoryToColor === "Survival") {
		    chart.defaultColors = [
		    	{fill: "#E93215", stroke: "#CD2207", opacity: 0.6},
		    	{fill: "#5BC684", stroke: "#2AB05D", opacity: 0.6}
		    ];
		}

	    // Customize ToolTip
		chartSeries.getTooltipText = function (e) {
			var toolTipText = [];
			if(categoryToColor === "") {
				toolTipText = [
		    		categoryToGroup + ": " + e.x,
		    		"Count: " + e.y,
		    		"Percent: " + (e.y * 100 / cleanData.length).toFixed(2) + " %"
		    	];
			} else {
				toolTipText = [
					categoryToColor + ": " + e.aggField, 
		    		categoryToGroup + ": " + e.x,
		    		"Count: " + e.y,
		    		"Percent: " + (e.y * 100 / cleanData.length).toFixed(2) + " %"
		    	];
			}

		    return toolTipText;
		};

	    chart.draw(1000);
	};
    
    /* Function to update_chart the Bar chart according to Category */
    function update_chart(categoryToGroup, categoryToColor = "") {
    	// Remove the previous SVG
    	d3.select("svg").remove();

    	// Append new SVG grouped by the selected category
    	draw_bar_chart(categoryToGroup, categoryToColor);
    };

    /* Function to add buttons to categorise and navigate */
    function add_base_buttons(categoryToGroup="Sex", categoryToColor = "") {
    	// Add Category buttons
	    var category_buttons = d3.select('div #chartContainer')
	                          .append('div')
	                          .attr('id', 'buttonSet')
	                          .attr('class', 'btn-group')
	                          .selectAll('button')
	                          .data(categories)
	                          .enter()
	                          .append('button')
	                          .attr("value", function(d) { return d; })
	                          .text(function(d) { return d; });

	    //Add Navigation Buttons
	    if(categoryToColor === "") {
	        var navButtonSetValues = ["Next"];
	    } else {
	        var navButtonSetValues = ["Next >>", "<< Previous"];
	    }
            
	    var navigation_buttons = d3.select('div #chartContainer')
	                          .append('div')
	                          .attr('id', 'navButtonSet')
	                          .attr('class', 'nav-btn-group')
	                          .selectAll('button')
	                          .data(navButtonSetValues)
	                          .enter()
	                          .append('button')
	                          .attr("value", function(d) { return d; })
	                          .text(function(d) { return d; })
	                          .style("float", "right");

	    // Add button On-Click event handlers
	    category_buttons.on("click", function(d) {

			// Keep the button Group same
			d3.select(".btn-group")
				.selectAll("button")
				.transition()
				.duration(500)
				.style("background", "#079DCD")
				.style("color", "white")
				.style("font-weight", "normal")
				.style("font-size", "10");
			                  
			// Mark the selected button differently
			d3.select(this)
			    .transition()
			    .duration(500)
			    .style("background", "#85CFE7")
			    .style("color", "black")
			    .style("font-weight", "bold")
			    .style("font-size", "9");

			// update_chart the SVG Bar Chart
			update_chart(d, categoryToColor);
		}); 

	    navigation_buttons.on("click", function(d, clickIndex) {

	        if (d.substr(0, 4) === "Next") {
			    //Clear the chart container div
			    d3.select('div #chartContainer')
			        .selectAll('div')
			        .remove();

			    // Remove the svg
			    d3.select("svg").remove();
			        
			    if(clickIndex === 0 && d === "Next") { 
			       	draw_bar_chart("Sex", "Survival");
			        //animate_chart("Sex", "Survival");
    				add_base_buttons("Sex", "Survival");

    				// Add Analysis
					d3.select("#footer")
					   	.select("h4")
					    .text("Analysis on Survival"); 

					d3.select("#footer")
					    .selectAll("li")
					    .remove();


					d3.select("#footer").select("ul")
					   	.selectAll("li")
					    .data([
					    		"Huge number of deaths for male passengers. Alomost 52% of entire deaths were of males. Whereas only 9% of entire deaths was for females.",
					    		"Huge number of deaths for third class passengers, almost 41% of entire deaths. Comparatively much lower deaths for first and second classes.",
					    		"The embarkment points does not really help us understanding the survivals.",
					    		"Survivals and deaths are pretty equally distributed across different Age groups."
					    	])
					    .enter()
					    .append("li")
					    .text(function(d) { return d; });
			    }
			    else {
			    	draw_final_chart();
					// Add Analysis
					d3.select("#footer")
					    .select("h4")
					    .text("Conclusion"); 

					d3.select("#footer")
					    .selectAll("li")
					    .remove();


					d3.select("#footer").select("ul")
					    .selectAll("li")
					    .data([
					    		"Females were survived most. Very less females died from first and second classes. Few females died from third class.",
					    		"Males were died mostly from third and second class, but in first class some of males were survived.",
					    		"All children from second class were saved. First class children, youths, and adults got much better survival rates. But all other age groups were died irrespective of class",
					    		"Almost 60% of children were saved. Other age groups have much higher deaths."
					    	])
					    .enter()
					    .append("li")
					    .text(function(d) { return d; });

					d3.select("#footer")
					    .append("p")
					    .attr("class", "text")
					    .text("We can conclude that children and females were tried to be saved during the disaster. First class passengers were also saved. Most of the male passengers died from second and third class across all age groups.")
					    .style("font-weight", "bold")
					    .style("font-size", "14px");
			    }
		    } else {
		        //Clear the chart container div
			    d3.select('div #chartContainer')
			        .selectAll('div')
			        .remove();

			    // Remove the svg
			    d3.select("svg").remove();

			    draw_bar_chart();
			    //animate_chart();
			    add_base_buttons("Sex", "");

			    // Add Analysis
				d3.select("#footer")
					.select("h4")
					.text("Summary of Passengers"); 

				d3.select("#footer")
					.selectAll("li")
					.remove();

				d3.select("#footer").select("ul")
					.selectAll("li")
					.data([
					    	"It can be clearly seen that around 65% Male passengers were onboarded in Titanic.",
					    	"More than 50% passengers belonged to third class.",
					    	"Around 75% passengers were boarded from Southampton.",
					    	"Age distribution was pretty much normal."
					    ])
					.enter()
					.append("li")
					.text(function(d) { return d; });
		    }

	    }); 

	    // Mark Sex Button as Enabled
	    update_chart("Sex", categoryToColor);
	            
	    d3.select(".btn-group")
	        .select("button")
	        .transition()
	        .duration(500)
	        .style("background", "#85CFE7")
	        .style("color", "black")
	        .style("font-weight", "bold")
	        .style("font-size", "9");

    };

    //animate_chart();

    update_chart("Sex", "");
    add_base_buttons("Sex", "");

    /* Function to animate the first 2 bar charts */
    function animate_chart(categoryToGroup="Sex", categoryToColor = "") {
    	var categoryIndex = 0;
    	var categoryInterval = setInterval(function() { 
 
	    	update_chart(categories[categoryIndex], categoryToColor);
			categoryIndex++;
			if (categoryIndex > categories.length) {
				clearInterval(categoryInterval);
				add_base_buttons(categoryToGroup, categoryToColor);
	    	}
    	}, 1000);

	}

	// Final Chart
	function draw_final_chart() {
		// Create drop down groups
		var dropDownDiv = d3.select('div #chartContainer')
							.append('div');

		dropDownDiv.append('h4')
			.text('Select below 2 categories to display the survivals -');

	    dropDownDiv.selectAll('label')
	    	.data(['Horizontal Category', 'Vertical Category'])
	    	.enter()
			.append('label')
			.attr('class', 'custom-label')
			.text(function(d) { return d; })
			.append('select')
			.attr('id', function(d) { return 'dropDownSet' + (d[0] === 'H' ? 0 : 1); } )
			.attr('class', 'custom-dropdown');

		var cat1 = d3.select('div #dropDownSet0');

		cat1.selectAll('option')
			.data(categories)
			.enter()
			.append('option')
			.attr("value", function(d) { return d; })
			.text(function(d) { return d; });

		var cat2 = d3.select('div #dropDownSet1');

		cat2.selectAll('option')
			.data(categories)
			.enter()
			.append('option')
			.attr("value", function(d) { return d; })
			.text(function(d) { return d; });

		cat2.on("change", function(d) {
			var cat1_value = cat1.property('value');
			var cat2_value = cat2.property('value');

			// Remove the SVG
			d3.select("svg").remove();

			draw_multi_category_chart(cat1_value, cat2_value);
		});

		// Draw the Multi category chart by Sex-Sex
		draw_multi_category_chart();

		var navigation_buttons = d3.select('div #chartContainer')
							  .select(".custom-label")
	                          .append('div')
	                          .attr('id', 'navButtonSet')
	                          .attr('class', 'nav-btn-group')
	                          .selectAll('button')
	                          .data(["Previous"])
	                          .enter()
	                          .append('button')
	                          .attr("value", function(d) { return d; })
	                          .text(function(d) { return d; })
	                          .style("float", "right");


	    navigation_buttons.on("click", function() {

			//Clear the chart container div
			d3.select('div #chartContainer')
			   .selectAll('div')
			   .remove();

			// Remove the svg
			d3.select("svg").remove();
			        
			draw_bar_chart("Sex", "Survival");
    		add_base_buttons("Sex", "Survival");

			// Add Analysis
			d3.select("#footer")
				.select("h4")
				.text("Analysis on Survival"); 

			d3.select("#footer")
				.selectAll("li")
				.remove();


			d3.select("#footer").select("ul")
				.selectAll("li")
				.data([
					"Huge number of deaths for male passengers. Alomost 52% of entire deaths were of males. Whereas only 9% of entire deaths was for females.",
					"Huge number of deaths for third class passengers, almost 41% of entire deaths. Comparatively much lower deaths for first and second classes.",
					"The embarkment points does not really help us understanding the survivals.",
					"Survivals and deaths are pretty equally distributed across different Age groups."
				])
				.enter()
				.append("li")
				.text(function(d) { return d; });

	    }); 

	    // Mark Sex Button as Enabled
	    d3.select(".btn-group")
	        .select("button")
	        .transition()
	        .duration(500)
	        .style("background", "#85CFE7")
	        .style("color", "black")
	        .style("font-weight", "bold")
	        .style("font-size", "9");   

	}


	/* Function to draw Bubble ring charts group by categories */
    function draw_multi_category_chart(cat_x="Sex", cat_y="Sex") {
    	scaler = 0.5;
		lWidth = width * scaler;
		lHeight = height * scaler;

    	data = nullFreeData(data, cat_x);
    	data = nullFreeData(data, cat_y);

    	var svg = dimple.newSvg("#chartContainer", lWidth + margin + 300, lHeight + margin + 100);
	    var chart = new dimple.chart(svg, data);

	    if (cat_x === "Age_Group") {
	    	chart.setBounds(margin*2.5, margin*2, lWidth - margin + 300, lHeight - margin);
		} else {
			chart.setBounds(margin*2.5, margin*2, lWidth - margin, lHeight - margin);
		}
	    var x = chart.addCategoryAxis("x", cat_x);
	    var y = chart.addCategoryAxis("y", cat_y);
	    var p = chart.addMeasureAxis("p", "PassengerID");

	    var rings = chart.addSeries("Survival", dimple.plot.pie);

	    if (cat_y === "Age_Group" && cat_x != "Age_Group") {
	    	rings.innerRadius = 10;
	    	rings.outerRadius = 25;
		} else if (cat_y === "Age_Group" && cat_x === "Age_Group") {
	    	rings.innerRadius = 15;
	    	rings.outerRadius = 30;
		} else {
			rings.innerRadius = 30;
			rings.outerRadius = 50;
		}

		if (cat_x === "Age_Group") {
			chart.addLegend(margin*2, margin*1.5, lWidth + 200, lHeight + 15, "right");
		} else {
			chart.addLegend(margin*2, margin*1.5, lWidth + 15, margin * 1.5, "right");
		}

	    /* Axis titles */
	    var seriesOrderRule_x = getSeriesOrderRule(cat_x);
	    x.addOrderRule(seriesOrderRule_x);
	    x.ticks = seriesOrderRule_x.length-1;

	    var seriesOrderRule_y = getSeriesOrderRule(cat_y);
	    y.addOrderRule(seriesOrderRule_y);
	    y.ticks = seriesOrderRule_y.length-1;

	    // Sum of Passengers
	    rings.aggregate = dimple.aggregateMethod.count;  

	    svg.selectAll('.dimple-gridline')
	    	.style("visibility", "true");

	    chart.defaultColors = [
		    {fill: "#E93215", stroke: "#CD2207", opacity: 0.6},
		    {fill: "#5BC684", stroke: "#2AB05D", opacity: 0.6}
		]; 

		// Customize ToolTip
		rings.getTooltipText = function (e) {
			var toolTipText;
			if (cat_x === cat_y) {
				toolTipText = [
					"Survival: " + e.aggField[0],
					cat_x + ": " + e.cx,
					"Passenger Count: " + e.cp,
					"Pie Percentage: " + (e.piePct * 100).toFixed(2) + " %"
				];
			} else {
				toolTipText = [
					"Survival: " + e.aggField[0],
					cat_x + ": " + e.cx,
					cat_y + ": " + e.cy,
					"Passenger Count: " + e.cp,
					"Pie Percentage: " + (e.piePct * 100).toFixed(2) + " %"
				];
			}

			return toolTipText;
		};

		if (cat_x === cat_y) {
		    svg.append("text")
				.attr("x", chart._xPixels() + chart._widthPixels() / 2)
				.attr("y", chart._yPixels() - 20)
				.style("text-anchor", "middle")
				.style("font-family", "sans-serif")
				.style("font-weight", "bold")
				.text("Passenger Survivals by " + cat_x);
		} else {
			svg.append("text")
				.attr("x", chart._xPixels() + chart._widthPixels() / 2)
				.attr("y", chart._yPixels() - 20)
				.style("text-anchor", "middle")
				.style("font-family", "sans-serif")
				.style("font-weight", "bold")
				.text("Passenger Survivals by " + cat_x + "-" + cat_y);
		}

	    chart.draw(1000);
    }
}
