(function () {
    'use strict';
    /*jslint todo: true*/
    /*jslint nomen: true*/
    /*globals d3,console,Backbone,$,_*/


    function BulletChart(data) {
        console.log('creating bullet chart', data);
        console.log(data);
        var margin = {top: 15, right: 40, bottom: 20, left: 120},
            width = 960 - margin.left - margin.right,
            height = 50 - margin.top - margin.bottom,

            chart = d3.bullet()
                .width(width)
                .height(height),


            svg = d3.select("#reportcard_vis_container").selectAll("svg")
                .data(data)
                .enter().append("svg")
                .attr("class", "bullet")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                .call(chart),

            title = svg.append("g")
                .style("text-anchor", "end")
                .attr("transform", "translate(-6," + height / 2 + ")");

        title.append("text")
            .attr("class", "title")
            .text(function (d) {
                return d.title;
            });

        title.append("text")
            .attr("class", "subtitle")
            .attr("dy", "1em")
            .text(function (d) {
                return d.subtitle;
            });

        this.updateBullets = function (data) {
            svg.data(data).call(chart); // TODO automatic transition
        };
    }

    var WIDTH = 900,
        HEIGHT = 200,
        MARGINS = {
            top: 20,
            right: 20,
            bottom: 20,
            left: 50
        },
        xRange = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([1, 5]),
        yRange = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0, 50]);


    function buildLineCharts() {
        console.log("load build line charts");
        var vis = d3.select("#lineup_vis_container").select('svg'),
            formatxAxis = d3.format('.0f'),
            xAxis = d3.svg.axis()
                .scale(xRange)
                .tickValues([1, 2, 3, 4, 5])
                .tickSize(6)
                .tickFormat(formatxAxis)
                .tickSubdivide(true),
            yAxis = d3.svg.axis()
                .scale(yRange)
                .ticks(4)
                .tickSize(6)
                .orient('left')
                .tickSubdivide(false);

        vis.append('svg:g')
            .attr('class', 'x axis')
            .attr('transform', 'translate(0,' + (HEIGHT - MARGINS.bottom) + ')')
            .call(xAxis);

        vis.append('svg:g')
            .attr('class', 'y axis')
            .attr('transform', 'translate(' + (MARGINS.left) + ',0)')
            .call(yAxis);
    }

    function updateLineCharts(lineData) {
        console.log('updating line data', lineData);
        var lineFunc = d3.svg.line()
                .x(function (d) {
                    return xRange(d.week);
                })
                .y(function (d) {
                    return yRange(d.delta);
                })
                .interpolate('linear');

        d3.select("#lineup_vis_container")
                .select('svg')
                .select('path.teamline')
                .transition()
                .duration(2000)
                .attr('d', lineFunc(lineData));

        d3.select("#lineup_vis_container")
            .select('svg')
            .selectAll('circle.plotpoints')
            .data(lineData)
            .enter()
            .append('svg:circle')
            .attr('cx', function (d) {
                return xRange(d.week);
            })
            .attr('cy', function (d) {
                return yRange(d.delta);
            })
            .attr('fill', 'red')
            .attr('stroke', 'blue')
            .attr('r', '8')
            .attr('class', 'plotpoints');

        d3.select("#lineup_vis_container")
            .select('svg')
            .selectAll('circle.plotpoints')
            .transition()
            .duration(2000)
            .attr('cy', function (d) {
                return yRange(d.delta);
            });
    }


    $(document).ready(function () {
        var data = [
                {"title": "Lineup", "subtitle": "Points Missed", "ranges": [25, 75, 100], "measures": [90], "markers": [64]},
                {"title": "Waiver", "subtitle": "Value Gained", "ranges": [25, 75, 100], "measures": [35], "markers": [25]},
                {"title": "Draft", "subtitle": "Value Gained", "ranges": [25, 75, 100], "measures": [25], "markers": [25]},
                {"title": "Trades", "subtitle": "Value Gained", "ranges": [25, 75, 100], "measures": [50], "markers": [74]}
            ],

            ReportCardModel = Backbone.Model.extend({
                url: function () {
                    return this.get("team_id") + '/';
                },

                getScorecards: function () {
                    var scorecards = this.get('scorecards');
                    if (!scorecards) {
                        return null;
                    }
                    scorecards.sort(function (a, b) {
                        return a.week - b.week;
                    });
                    return scorecards;
                }
            }),

            roguesReportCard = new ReportCardModel({
                team_id: '6'
            }),

            ReportCardView = Backbone.View.extend({
                el: $("#reportcard_vis_container"),

                initialize: function () {
                    this.listenTo(this.model, "change:lineup_score", this.render);
                },

                render: function () {
                    console.log("rendering report card");
                    if (this.model.get('lineup_score') !== undefined) {
                        console.log("rendering lineup score", this.model.get('lineup_score'));
                        data[0].measures[0] = this.model.get('lineup_score');
                        if (!this.bulletChart) {
                            this.bulletChart = new BulletChart(data);
                        } else {
                            this.bulletChart.updateBullets(data);
                        }
                    }
                    return this;
                }
            }),
            LineupTableView = Backbone.View.extend({
                'template': _.template($("#lineup-table-template").html()),

                initialize: function () {
                    this.listenTo(this.model, "change:scorecards", this.render);
                },

                render: function () {
                    this.$el.html(this.template({'team_id': this.model.get('team_id'), 'scorecards': this.model.get('scorecards')}));
                    return this;
                }
            }),

            LineupView = Backbone.View.extend({
                el: $('#lineup_vis_container'),

                initialize: function () {
                    this.listenTo(this.model, "change:scorecards", this.updateLineChart);

                },

                updateLineChart: function () {
                    updateLineCharts(this.model.getScorecards());
                },

                render: function () {
                    this.$el.append(new LineupTableView({model: this.model}).render().el);
                    buildLineCharts();
                    if (this.model.getScorecards() !== null) {
                        this.updateLineChart();
                    }
                    return this;
                }
            }),
            lineupView = new LineupView({model: roguesReportCard}),
            reportCardView = new ReportCardView({model: roguesReportCard}),
            REPORT_CARD = 1,
            LINEUPS = 2,
            AppRouter = Backbone.Router.extend({
                routes: {
                    "team/:id": "getTeam",
                    "lineups": "loadLineups",
                    "lineups/:id": "loadLineups",
                    "reportcard/:id": "loadReportCard",
                    "*actions": "default" // Backbone will try match the route above first
                }
            }),
            app_router = new AppRouter();

        lineupView.render();
        reportCardView.render();

        $(lineupView.el).hide();
        $(reportCardView.el).hide();

        window.mode = REPORT_CARD;

        // Instantiate the router
        app_router.on('route:getTeam', function (id) {
            roguesReportCard.set('team_id', id);
            roguesReportCard.fetch();
            if (window.mode === LINEUPS) {
                app_router.navigate('lineups/' + id, {replace: true});
            } else if (window.mode === REPORT_CARD) {
                app_router.navigate('reportcard/' + id, {replace: true});
            }
        });

        app_router.on('route:loadLineups', function (id) {
            console.log("load lineups");
            window.mode = LINEUPS;
            $('#lineup-tab').addClass('active');
            $('#report-card-tab').removeClass('active');

            $(reportCardView.el).hide();
            $(lineupView.el).show();

            if (id) {
                roguesReportCard.set('team_id', id);
                roguesReportCard.fetch();
            } else {
                id = roguesReportCard.get('team_id', id);
            }
            app_router.navigate('lineups/' + id, {replace: true});

        });

        app_router.on('route:loadReportCard', function (id) {
            console.log("load report card");
            $('#lineup-tab').removeClass('active');
            $('#report-card-tab').addClass('active');

            $(lineupView.el).hide();
            $(reportCardView.el).show();

            if (id) {
                roguesReportCard.set('team_id', id);
                roguesReportCard.fetch();
            } else {
                id = roguesReportCard.get('team_id', id);
            }
            app_router.navigate('reportcard/' + id, {replace: true});
        });

        app_router.on('route:default', function () {
            roguesReportCard.set('team_id', 6);
            roguesReportCard.fetch();
            app_router.trigger('route:loadReportCard');
        });

        // Start Backbone history a necessary step for bookmarkable URL's
        Backbone.history.start();
    });


}());