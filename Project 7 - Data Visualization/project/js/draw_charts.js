var margin = 40, 
    width = 1200,
	height = 800;


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



function getSeriesOrderRule(categoryToGroup) {
	var seriesOrderRule = {
		"Sex": ["Male", "Female"],
		"Class": ["First Class", "Second Class", "Third Class"],
		"Embarked": ["Southampton", "Cherbourg", "Queenstown"],
		"Age_Group": ["Child", "Youth", "Adult", "Mid-Age", "Old", "Very Old"]
	};

	return seriesOrderRule[categoryToGroup];
}



function draw(data) {
	"use strict";

   	var scaler = 0.6;
	var lWidth = width * scaler,
		lHeight = height * scaler;

	var categories = ["Sex", "Class", "Embarked", "Age_Group"];

	/* Function to Draw Bar Chart */
	function draw_bar_chart(categoryToGroup="Sex", categoryToColor = "") {

		// Remove nulls from categories
		if(categoryToGroup === "Embarked" || categoryToGroup === "Age_Group") {
			var cleanData = nullFreeData(data, categoryToGroup);
		} else {
			var cleanData = data;
		}

		var svgSingleVarCategory = dimple.newSvg("#chartContainer", lWidth + margin, lHeight + margin);
	    var singleVarGroupByChart = new dimple.chart(svgSingleVarCategory, cleanData);

		if(categoryToColor === "") {
			var x = singleVarGroupByChart.addCategoryAxis("x", [categoryToGroup]);
	    } else {
	    	var x = singleVarGroupByChart.addCategoryAxis("x", [categoryToGroup, categoryToColor]);
	    }

	    var y = singleVarGroupByChart.addMeasureAxis("y","PassengerID");

	    singleVarGroupByChart.setBounds(margin*1.5, margin*1.2, lWidth - margin*2, lHeight - margin*1.2);

	    /* Axis titles */
	    //debugger;
	    x.title = categoryToGroup;
	    var seriesOrderRule = getSeriesOrderRule(categoryToGroup);
	    x.addOrderRule(seriesOrderRule);
	    x.ticks = seriesOrderRule.length-1;

	    y.title = "Number of Passengers";
	    y.ticks = 6;

	    if(categoryToColor === "") {
			var chartSeries = singleVarGroupByChart.addSeries(null, dimple.plot.bar);
	    } else {
	    	var chartSeries = singleVarGroupByChart.addSeries(categoryToColor, dimple.plot.bar);
	    	singleVarGroupByChart.addLegend(margin*2, margin, lWidth - margin*2 + 15, 40, "right");
	    }

	    chartSeries.aggregate = dimple.aggregateMethod.count;    
	    chartSeries.barGap = 0.2;

	    svgSingleVarCategory.append("text")
				    		.attr("x", singleVarGroupByChart._xPixels() + singleVarGroupByChart._widthPixels() / 2)
				    		.attr("y", singleVarGroupByChart._yPixels() - 20)
				    		.style("text-anchor", "middle")
				    		.style("font-family", "sans-serif")
				    		.style("font-weight", "bold")
				    		.text("Passenger counts by " + categoryToGroup);


	    // Removing X axis tick lines
	    svgSingleVarCategory.selectAll('.dimple-gridline')
	    		  			.style("visibility", "hidden");

	    if (categoryToColor === "Survival") {
		    singleVarGroupByChart.defaultColors = [
		    	{fill: "#FB8072", stroke: "rgb(210, 107, 95)", opacity: 0.8},
		    	{fill: "#80B1D3", stroke: "rgb(107, 148, 177)", opacity: 0.8}
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

	    singleVarGroupByChart.draw();
	};
    
    /* Function to Update the Bar chart according to Category */
    function update(categoryToGroup, categoryToColor = "") {
    	// Remove the previous SVG
    	d3.select("svg").remove();
    	//d3.select("#navButtonSet").remove();

    	// Append new SVG grouped by the selected category
    	draw_bar_chart(categoryToGroup, categoryToColor);

    };

    function add_category_nav_buttons(categoryToGroup="Sex", categoryToColor = "") {
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
	            var navButtonSetValues = ["Previous", "Next"];
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
			            .style("background", "#4CAF50")
			            .style("color", "white")
			            .style("font-weight", "normal")
			            .style("font-size", "10");
		                  
		        // Mark the selected button differently
		        d3.select(this)
		              .transition()
		              .duration(500)
		              .style("background", "#3e8e41")
		              .style("color", "black")
		              .style("font-weight", "bold")
		              .style("font-size", "9");

		        // Update the SVG Bar Chart
		        update(d, categoryToColor);
	       	}); 

	        navigation_buttons.on("click", function(d, clickCount) {

	           	if (d === "Next") {
			        //Clear the chart container div
			        d3.select('div #chartContainer')
			          .selectAll('div')
			          .remove();

			        // Remove the svg
			        d3.select("svg").remove();
			        
			        if(clickCount === 0) { 
			        	draw_bar_chart("Sex", "Survival");
			        	animate_svg("Sex", "Survival");
			    	}
			    	else {
			    		// TODO:: Make the final chart
			    		draw_final_chart();
			    	}
		        } else {
		        	//Clear the chart container div
			        d3.select('div #chartContainer')
			          .selectAll('div')
			          .remove();

			        // Remove the svg
			        d3.select("svg").remove();

			        draw_bar_chart();
			        animate_svg();
		        }

	        }); 

	        // Mark Sex Button as Enabled
	        update("Sex", categoryToColor);
	            
	        d3.select(".btn-group")
	                  .select("button")
	                  .transition()
	                  .duration(500)
	                  .style("background", "#3e8e41")
	                  .style("color", "black")
	                  .style("font-weight", "bold")
	                  .style("font-size", "9");

    };

    animate_svg();

    function animate_svg(categoryToGroup="Sex", categoryToColor = "") {
    	var categoryIndex = 0;
    	var categoryInterval = setInterval(function() { 
 
	    	update(categories[categoryIndex], categoryToColor);
			categoryIndex++;
			if (categoryIndex > categories.length) {
				clearInterval(categoryInterval);
				add_category_nav_buttons(categoryToGroup, categoryToColor);
	    	}
    	}, 1000);

	}

	// Final Chart
	function draw_final_chart() {
		// Create drop down groups
		var dropDownDiv = d3.select('div #chartContainer')
							.append('div');

		dropDownDiv.append('h4')
			.text('Select any 2 categories to display the survivals')
			.append('br');

	    dropDownDiv.selectAll('label')
	    	.data(['Horizontal Category', 'Vertical Category'])
	    	.enter()
			.append('label')
			.attr('class', 'custom-label')
			.text(function(d) { return d; })
			.append('select')
			.attr('id', function(d) { return 'dropDownSet' + (d === 'Horizontal Category' ? 0 : 1); } )
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

		draw_multi_category_chart();
	}

    function draw_multi_category_chart(cat_x="Sex", cat_y="Sex") {
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
	    	rings.innerRadius = 15;
	    	rings.outerRadius = 30;
		} else if (cat_y === "Age_Group" && cat_x === "Age_Group") {
	    	rings.innerRadius = 20;
	    	rings.outerRadius = 35;
		} else {
			rings.innerRadius = 40;
			rings.outerRadius = 60;
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

	    chart.defaultColors = [
		   	{fill: "#FB8072", stroke: "rgb(210, 107, 95)", opacity: 0.8},
		    {fill: "#80B1D3", stroke: "rgb(107, 148, 177)", opacity: 0.8}
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

	    chart.draw();

    }

}





