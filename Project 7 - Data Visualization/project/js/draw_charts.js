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



function drawBasicSummaryChart(data, categoryToGroup) {
	var scaler = 0.5;
	var lWidth = width * scaler,
		lHeight = height * scaler;

	var data = nullFreeData(data, categoryToGroup);

    /* Group by Gender */
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

    /*singleVarGroupByChart.defaultColors = [
	    new dimple.color("#197DA5") 
	];*/

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
    // debugger;
	chartSeries.getTooltipText = function (e) {
		return [
	    	categoryToGroup + ": " + e.x,
	    	"Count: " + e.y,
	    	"Percent: " + (e.y * 100 / data.length).toFixed(2) + " %"
	    ];
	};

    singleVarGroupByChart.draw();

    // Removing Null Values
    chartSeries.shapes.style("opacity", function (e) {
    	//debugger;
	    return (e.x === 0 || e.x === "" ? 0 : 0.8);
	});

};

