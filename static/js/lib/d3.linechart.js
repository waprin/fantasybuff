(function () {
    /*"use strict";*/
    d3.linechart = function () {
        var ranges = linechartRanges,
            width = 380,
            height = 400,
            range=[0, 100]
            weekRange=[0, 12];

        function linechart(g) {
            g.each(function (d, i) {

            });
        };

        linechart.width = function (x) {
            if (!arguments.length) return width;
            width = x;
            return linechart;
        };

        linechart.height = function (x) {
            if (!arguments.length) return height;
            height = x;
            return linechart;
        };

        linechart.range = function(x) {
            "use strict";
            if (!arguments.length) return range;
            range = x;
            return linechart;
        };

        linechart.weekRange = function(x) {
            "use strict";
            if (!arguments.length) return weekRange;
            weekRange = x;
            return linechart;
        };



        return linechart;
    };

    function linechartRanges(d) {
        return d.ranges;
    }

}());