var margin = 40, 
    width = 1200,
	height = 800;


function nullFreeData(data, categoryToGroup) {
	var cleanData = [];
	var dataRecord;

	for (var i in data) {
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

   	var scaler = 0.5;
	var lWidth = width * scaler,
		lHeight = height * scaler;

	var categories = ["Sex", "Class", "Embarked", "Age_Group"];

	/* Function to Draw Bar Chart */
	function draw_bar_chart(categoryToGroup="Sex") {
		// Remove nulls from categories
		data = nullFreeData(data, categoryToGroup);


		var svgSingleVarCategory = dimple.newSvg("#chartContainer", lWidth + margin, lHeight + margin);
	    var singleVarGroupByChart = new dimple.chart(svgSingleVarCategory, data);
	    var x = singleVarGroupByChart.addCategoryAxis("x", [categoryToGroup]);
	    var y = singleVarGroupByChart.addMeasureAxis("y","PassengerID");

	    singleVarGroupByChart.setBounds(margin*1.5, margin*1.2, lWidth - margin*2, lHeight - margin*1.2);

	    /* Axis titles */
	    x.title = categoryToGroup;
	    var seriesOrderRule = getSeriesOrderRule(categoryToGroup);
	    x.addOrderRule(seriesOrderRule);
	    x.ticks = seriesOrderRule.length-1;

	    y.title = "Number of Passengers";
	    y.ticks = 5;

	    var chartSeries = singleVarGroupByChart.addSeries(null, dimple.plot.bar);
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

	    // Customize ToolTip
		chartSeries.getTooltipText = function (e) {
			return [
		    	categoryToGroup + ": " + e.x,
		    	"Count: " + e.y,
		    	"Percent: " + (e.y * 100 / data.length).toFixed(2) + " %"
		    ];
		};

	    singleVarGroupByChart.draw();
	};
    
    /* Function to Update the Bar chart according to Category */
    function update(categoryToGroup) {
    	// Remove the previous SVG
    	d3.select("svg").remove();

    	// Append new SVG grouped by the selected category
    	draw_bar_chart(categoryToGroup);

    };


    var categoryIndex = 0;
    var categoryInterval = setInterval(function() { 
              update(categories[categoryIndex]);

              categoryIndex++;

              if (categoryIndex >= categories.length) {
                clearInterval(categoryInterval);
				
                // Add Category buttons
                var buttons = d3.select('div #intro')
                          .append('div')
                          .attr('id', 'buttonSet')
                          .attr('class', 'btn-group')
                          .selectAll('button')
                          .data(categories)
                          .enter()
                          .append('button')
                          .attr("value", function(d) { return d; })
                          .text(function(d) { return d; });

                // Add button On-Click event handler
                buttons.on("click", function(d) {

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
                  	update(d);
                }); 
              }
          }, 1000);


    draw_bar_chart();

}





