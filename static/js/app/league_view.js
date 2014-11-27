require(['jquery', 'backbone', 'underscore', 'd3', 'd3.bullet', 'bootstrap'], function ($, Backbone, _, d3) {
    /*'use strict';*/
    /*jslint todo: true*/
    /*jslint nomen: true*/
    /*globals d3,console*/

    var viewportWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0),
        w;
    if (viewportWidth > 700) {
        w = viewportWidth * 0.7;
    } else {
        w = viewportWidth * 0.9;
    }


    var WIDTH =  w,
        HEIGHT = 50,
        MARGINS = {
            top: 20,
            right: 20,
            bottom: 20,
            left: 70
        };


    function BulletChart(data) {
        console.log('creating bullet chart', data);
        console.log(data);
        var margin = MARGINS;
        margin.left = margin.left + 20;
        var width = WIDTH - margin.left - margin.right,
            height = HEIGHT - margin.top - margin.bottom,

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
                /*.style("text-anchor", "begin")*/
                .attr("transform", "translate(-87," + height / 2 + ")");

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

    var LINE_WIDTH = w,
        LINE_HEIGHT = 200,
        LINE_MARGINS = {
            top: 20,
            right: 20,
            bottom: 20,
            left: 50
        };

    function buildLineCharts(element, numWeeks, range) {
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

        console.log('ticklist', tickList);
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

    function updateLineCharts(element, lineData, range) {
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


    $(document).ready(function () {
        var data = [
                {"title": "Lineup", "subtitle": "Points Missed", "ranges": [0, 100], "measures": [90], "markers": [0]},
                {"title": "Waiver", "subtitle": "Value Gained", "ranges": [0, 100], "measures": [35], "markers": [0]},
                {"title": "Draft", "subtitle": "Value Gained", "ranges": [0, 100], "measures": [25], "markers": [0]},
                {"title": "Trades", "subtitle": "Value Gained", "ranges": [0, 100], "measures": [50], "markers": [0]}
            ],

            ReportCardModel = Backbone.Model.extend({
                url: function () {
                    return this.get("team_id") + '/';
                },

                getRanges: function (fieldName) {
                    if (fieldName === 'draft_scores') {
                        return [this.get('draft_min'), this.get('draft_max')];
                    }
                    if (fieldName === 'waiver_scores') {
                        return [this.get('waiver_min'), this.get('waiver_max')];
                    }
                    if (fieldName === 'trade_scores') {
                        return [this.get('trade_min'), this.get('trade_max')];
                    }
                    if (fieldName === 'lineups') {
                        return [0, 50];
                    }
                    throw "Can't find fieldName " + fieldName;
                },

                getWeeklyScores: function (name) {
                    var scorecards = this.get(name);
                    if (!scorecards) {
                        return null;
                    }
                    scorecards.sort(function (a, b) {
                        return a.week - b.week;
                    });
                    if (name === 'lineups') {
                        console.log("cleaning up lineups");
                        _.each(scorecards, function (scorecard) {
                            scorecard.value = scorecard.delta;
                        });
                    }
                    return scorecards;
                }
            }),

            roguesReportCard = new ReportCardModel({
                team_id: '6'
            }),

            ReportCardView = Backbone.View.extend({
                el: $("#reportcard_vis_container"),

                initialize: function () {
                    this.listenTo(this.model, "change:average_waiver_score", this.render);
                },

                render: function () {
                    console.log("rendering report card");
                    if (this.model.get('average_waiver_score') !== undefined) {
                        console.log("rendering lineup score", this.model.get('average_lineup_score'));
                        data[0].ranges[0] = this.model.get('min_average_lineup');
                        data[0].ranges[1] = this.model.get('max_average_lineup');
                        data[0].measures[0] = this.model.get('average_lineup_score');
                        data[0].markers[0] = this.model.get('average_lineup_score');

                        data[1].ranges[0] = this.model.get('min_average_waiver');
                        data[1].ranges[1] = this.model.get('max_average_waiver');
                        data[1].measures[0] = this.model.get('average_waiver_score');
                        data[1].markers[0] = this.model.get('average_waiver_score');

                        data[2].ranges[0] = this.model.get('min_average_draft');
                        data[2].ranges[1] = this.model.get('max_average_draft');
                        data[2].measures[0] = this.model.get('average_draft_score');
                        data[2].markers[0] = this.model.get('average_draft_score');

                        data[3].ranges[0] = this.model.get('min_average_trade');
                        data[3].ranges[1] = this.model.get('max_average_trade');
                        data[3].measures[0] = this.model.get('average_trade_score');
                        data[3].markers[0] = this.model.get('average_trade_score');
                        console.log("done hacking data", data);
                    } else {
                        return this;
                    }
                    if (!this.bulletChart) {
                        this.bulletChart = new BulletChart(data);
                    } else {
                        this.bulletChart.updateBullets(data);
                    }
                    return this;
                }
            }),
            LineupTableView = Backbone.View.extend({
                'template': _.template($("#lineup-table-template").html()),

                'className': 'lineup-table',

                initialize: function (options) {
                    this.listenTo(this.model, "change", this.render);
                    this.fieldName = options.fieldName;
                },

                render: function () {
                    var field = this.fieldName;
                    field = field.split('_')[0];
                    this.$el.html(this.template({ 'team_id': this.model.get('team_id'),
                            'scorecards': this.model.getWeeklyScores(this.fieldName),
                        'field': field
                        }));
                    return this;
                }
            }),

            LineChartView = Backbone.View.extend({
                initialize: function (options) {
                    //this.listenTo(this.model, "change:scorecards", this.updateLineChart);
                    this.listenTo(this.model, options.updateEvent, this.updateLineChart);
                    this.fieldName = options.fieldName;
                    this.range = options.range;
                    this.built = false;
                },

                updateLineChart: function () {
                    var scores = this.model.getWeeklyScores(this.fieldName),
                        ranges = this.model.getRanges(this.fieldName);
                    buildLineCharts(this.el, scores.length, ranges);
                    updateLineCharts(this.el, scores, ranges);
                },

                render: function () {
                    this.$el.append(new LineupTableView({model: this.model, fieldName: this.fieldName}).render().el);
                    return this;
                }
            }),
            TabView = Backbone.View.extend({
                el: $("#league_navigation"),

                initialize: function () {
                    var _that = this;
                    /*jslint unparam:true*/
                    Backbone.history.on('route', function (router, name) {
                        if (name.substring(0, 4) !== 'load') {
                            return;
                        }
                        name = name.substring(5);
                        _.each(_that.$el.children(), function (child) {
                            child = $(child);
                            if (child.attr('class') === 'dropdown') {
                                return;
                            }
                            if (child.attr('id').split('-')[0] === name) {
                                child.addClass('active');
                            } else {
                                child.removeClass('active');
                            }
                        });
                    });
                    /*jslint unparam:false*/
                },

                render: function (tabs) {
                    var dropdown = this.$('.dropdown'),
                        first = true,
                        first_item,
                        _that = this;
                    this.$el.empty();
                    this.$el.append(dropdown);

                    _.each(tabs, function (tab) {
                        var elm = _that.$el.append('<li id="' + tab.id + '-tab"><a href="#' + tab.id + '" >' + tab.name + '</a></li>');
                        if (first) {
                            first_item = elm;
                            first = false;
                        }
                    });
                    first_item.addClass('active');
                    return this;
                }
            }),
            lineupView = new LineChartView({
                model: roguesReportCard,
                el: $('#lineup_vis_container'),
                fieldName: 'lineups',
                updateEvent: "change:lineups",
                range: [0, 50]
            }),
            draftView = new LineChartView({
                model: roguesReportCard,
                el: $('#draft_vis_container'),
                fieldName: 'draft_scores',
                updateEvent: "change:draft_scores",
                range: [100, 300]
            }),
            waiverView = new LineChartView({
                model: roguesReportCard,
                el: $('#waiver_vis_container'),
                fieldName: 'waiver_scores',
                updateEvent: "change:waiver_scores",
                range: [-50, 50]
            }),
            tradeView = new LineChartView({
                model: roguesReportCard,
                el: $('#trade_vis_container'),
                fieldName: 'trade_scores',
                updateEvent: "change:trade_scores",
                range: [-50, 50]
            }),

            reportCardView = new ReportCardView({model: roguesReportCard}),
            REPORT_CARD = 1,
            LINEUPS = 2,
            DRAFT = 3,
            WAIVER = 4,
            TRADE = 5,
            AppRouter = Backbone.Router.extend({
                routes: {
                    "team/:id": "getTeam",
                    "lineups/:id": "load_lineups",
                    "lineups": "load_lineups",
                    "reportcard/:id": "load_reportcard",
                    "reportcard": "load_reportcard",
                    "draft/:id": "load_draft",
                    "draft": "load_draft",
                    "waiver/:id": "load_waiver",
                    "waiver": "load_waiver",
                    "trade/:id": "load_trade",
                    "trade": "load_trade",
                    "*actions": "default" // Backbone will try match the route above first
                }
            }),
            app_router = new AppRouter(),
            tabView = new TabView();

        tabView.render([
            {id: 'reportcard', name: "Report Card"},
            {id: 'lineups', name: "Lineups"},
            {id: 'draft', name : 'Draft'},
            {id: 'waiver', name: 'Waiver'},
            {id: 'trade', name: 'Trade'}
        ]);
        lineupView.render();
        draftView.render();
        reportCardView.render();
        waiverView.render();
        tradeView.render();

        $(lineupView.el).hide();
        $(reportCardView.el).hide();
        $(draftView.el).hide();
        $(waiverView.el).hide();
        $(tradeView.el).hide();

        window.mode = REPORT_CARD;

        // Instantiate the router
        app_router.on('route:getTeam', function (id) {
            console.log("got team " , id)
            roguesReportCard.set('team_id', id);
            roguesReportCard.fetch();
            $(".team-link-header").html("Team: " + $("#team-link-" + id).html());
            if (window.mode === LINEUPS) {
                app_router.navigate('lineups/' + id, {replace: true});
            } else if (window.mode === REPORT_CARD) {
                app_router.navigate('reportcard/' + id, {replace: true});
            } else if (window.mode === DRAFT) {
                app_router.navigate('draft/' + id, {replace: true});
            } else if (window.mode === WAIVER) {
                app_router.navigate('waiver/' + id, {replace: true});
            } else if (window.mode === TRADE) {
                app_router.navigate('trade/' + id, {replace: true});
            }
        });

        app_router.on('route:load_lineups', function (id) {
            console.log('in load lineups');
            window.mode = LINEUPS;

            $(reportCardView.el).hide();
            $(lineupView.el).show();
            $(draftView.el).hide();
            $(waiverView.el).hide();
            $(tradeView.el).hide();

            if (id) {
                roguesReportCard.set('team_id', id);
                roguesReportCard.fetch();
                $(".team-link-header").html("Team: " + $("#team-link-" + id).html());
            } else {
                id = roguesReportCard.get('team_id', id);
            }
            app_router.navigate('lineups/' + id, {replace: true});

        });

        app_router.on('route:load_reportcard', function (id) {
            $(lineupView.el).hide();
            $(reportCardView.el).show();
            $(draftView.el).hide();
            $(waiverView.el).hide();
            $(tradeView.el).hide();

            if (id) {
                roguesReportCard.set('team_id', id);
                roguesReportCard.fetch();
                $(".team-link-header").html("Team: " + $("#team-link-" + id).html());
            } else {
                id = roguesReportCard.get('team_id', id);
            }
            app_router.navigate('reportcard/' + id, {replace: true});
        });
        app_router.on('route:load_draft', function (id) {
            $(lineupView.el).hide();
            $(reportCardView.el).hide();
            $(draftView.el).show();
            $(waiverView.el).hide();
            $(tradeView.el).hide();

            if (id) {
                roguesReportCard.set('team_id', id);
                roguesReportCard.fetch();
                $(".team-link-header").html("Team: " + $("#team-link-" + id).html());
            } else {
                id = roguesReportCard.get('team_id', id);
            }
            app_router.navigate('draft/' + id, {replace: true});
        });
        app_router.on('route:load_waiver', function (id) {
            console.log('in load waiver');
            $(lineupView.el).hide();
            $(reportCardView.el).hide();
            $(draftView.el).hide();
            $(waiverView.el).show();
            $(tradeView.el).hide();

            if (id) {
                roguesReportCard.set('team_id', id);
                roguesReportCard.fetch();
                $(".team-link-header").html("Team: " + $("#team-link-" + id).html());
            } else {
                id = roguesReportCard.get('team_id', id);
            }
            app_router.navigate('waiver/' + id, {replace: true});
        });
        app_router.on('route:load_trade', function (id) {
            $(lineupView.el).hide();
            $(reportCardView.el).hide();
            $(draftView.el).hide();
            $(waiverView.el).hide();
            $(tradeView.el).show();

            if (id) {
                roguesReportCard.set('team_id', id);
                roguesReportCard.fetch();
                $(".team-link-header").html("Team: " + $("#team-link-" + id).html());
            } else {
                id = roguesReportCard.get('team_id', id);
            }
            app_router.navigate('trade/' + id, {replace: true});
        });

        app_router.on('route:default', function () {
            console.log("default route!");
            roguesReportCard.set('team_id', 6);
            var initialLoad = roguesReportCard.fetch();
            initialLoad.done(function () {
                app_router.navigate('reportcard/6', {replace: true, trigger: true});
            });
        });

        // Start Backbone history a necessary step for bookmarkable URL's
        Backbone.history.start();
    });


});