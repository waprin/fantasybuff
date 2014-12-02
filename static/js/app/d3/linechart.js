define(['d3'], function (d3) {


    function buildLineCharts(element, numWeeks, range, LINE_HEIGHT, LINE_WIDTH, LINE_MARGINS) {
        var xRange = d3.scale.linear().range([LINE_MARGINS.left, LINE_WIDTH - LINE_MARGINS.right]).domain([1, numWeeks]),
            yRange = d3.scale.linear().range([LINE_HEIGHT - LINE_MARGINS.top, LINE_MARGINS.bottom]).domain([range[0], range[1]]),
            vis = d3.select(element).select('svg'),
            formatxAxis = d3.format('.0f'),
            xAxis,
            yAxis,
            tickList = [],
            i;

        for (i = 1; i <= numWeeks; i = i + 1) {
            tickList.push(i);
        }

        xAxis = d3.svg.axis()
            .scale(xRange)
            .tickValues(tickList)
            .tickFormat(formatxAxis)
            .tickSubdivide(true);
        yAxis = d3.svg.axis()
            .orient('left')
            .scale(yRange)
            .ticks(4)
            .tickSize(6)
            .tickSubdivide(false);

        vis.append('svg:g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0,' + (LINE_HEIGHT - LINE_MARGINS.bottom) + ')')
            .call(xAxis);

        vis.append('svg:g')
            .attr('class', 'y axis')
            .attr('transform', 'translate(' + (LINE_MARGINS.left) + ',0)')
            .call(yAxis);
    }

    function updateLineCharts(element, lineData, range, LINE_HEIGHT, LINE_WIDTH, LINE_MARGINS) {
        console.log('updating line data', lineData);
        console.log(lineData.size);
        var xRange = d3.scale.linear().range([LINE_MARGINS.left, LINE_WIDTH - LINE_MARGINS.right]).domain([1, lineData.length]),
            yRange = d3.scale.linear().range([LINE_HEIGHT - LINE_MARGINS.top, LINE_MARGINS.bottom]).domain([range[0], range[1]]),
            lineFunc = d3.svg.line()
                .x(function (d) {
                    return xRange(d.week);
                })
                .y(function (d) {
                    return yRange(d.value);
                })
                .interpolate('linear');

        d3.select(element)
            .select('svg')
            .select('path.teamline')
            .transition()
            .duration(2000)
            .attr('d', lineFunc(lineData));

        d3.select(element)
            .select('svg')
            .selectAll('circle.plotpoints')
            .data(lineData)
            .enter()
            .append('svg:circle')
            .attr('cx', function (d) {
                return xRange(d.week);
            })
            .attr('cy', function (d) {
                return yRange(d.value);
            })
            .attr('class', 'plotpoints');

        d3.select(element)
            .select('svg')
            .selectAll('circle.plotpoints')
            .transition()
            .duration(2000)
            .attr('cy', function (d) {
                return yRange(d.value);
            });
    }


    return {
        buildLineCharts: buildLineCharts,
        updateLineCharts: updateLineCharts
    };
});
