require(['app/views/tab_view', 'app/d3/linechart', 'jquery', 'backbone', 'underscore', 'd3', 'd3.bullet', 'bootstrap'], function (tab_view, line_chart, $, Backbone, _, d3) {
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


    function BulletChart(element_selector, data) {
        console.log('creating bullet chart', data);
        console.log(data);
        var margin = MARGINS;
        margin.left = margin.left + 20;
        var width = WIDTH - margin.left - margin.right,
            height = HEIGHT - margin.top - margin.bottom,

            chart = d3.bullet()
                .width(width)
                .height(height),


            svg = d3.select(element_selector).selectAll("svg")
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
                    if (fieldName === 'lineup_scores') {
                        return [this.get('lineup_min'), this.get('lineup_max')];
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
                    if (name === 'lineup') {
/*                        console.log("cleaning up lineups");*/
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
                el: $("#dashboard-reportcard-tab"),

                initialize: function () {
                    this.listenTo(this.model, "change:average_waiver_score", this.render);
                },

                render: function () {
/*                    console.log("rendering report card");*/
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
                        this.bulletChart = new BulletChart("#dashboard-reportcard-tab", data);
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
                },

                updateLineChart: function () {
                    var scores = this.model.getWeeklyScores(this.fieldName),
                        ranges = this.model.getRanges(this.fieldName);
                    line_chart.buildLineCharts(this.el, scores.length, ranges, LINE_HEIGHT, LINE_WIDTH, LINE_MARGINS);
                    line_chart.updateLineCharts(this.el, scores, ranges, LINE_HEIGHT, LINE_WIDTH, LINE_MARGINS);
                },

                render: function () {
                    this.$el.append(new LineupTableView({model: this.model, fieldName: this.fieldName}).render().el);
                    return this;
                }
            }),
            lineupView = new LineChartView({
                model: roguesReportCard,
                el: $('#dashboard-lineup-tab'),
                fieldName: 'lineup_scores',
                updateEvent: "change:lineup_scores",
                range: [0, 50]
            }),
            draftView = new LineChartView({
                model: roguesReportCard,
                el: $('#dashboard-draft-tab'),
                fieldName: 'draft_scores',
                updateEvent: "change:draft_scores",
                range: [100, 300]
            }),
            waiverView = new LineChartView({
                model: roguesReportCard,
                el: $('#dashboard-waiver-tab'),
                fieldName: 'waiver_scores',
                updateEvent: "change:waiver_scores",
                range: [-50, 50]
            }),
            tradeView = new LineChartView({
                model: roguesReportCard,
                el: $('#dashboard-trade-tab'),
                fieldName: 'trade_scores',
                updateEvent: "change:trade_scores",
                range: [-50, 50]
            }),

            reportCardView = new ReportCardView({model: roguesReportCard}),
            AppRouter = Backbone.Router.extend({
                routes: {
                    "team/:id": "getTeam",
                    "lineup/:id": "lineup",
                    "lineup": "lineup",
                    "reportcard/:id": "reportcard",
                    "reportcard": "reportcard",
                    "draft/:id": "draft",
                    "draft": "draft",
                    "waiver/:id": "waiver",
                    "waiver": "waiver",
                    "trade/:id": "trade",
                    "trade": "trade",
                    "*actions": "default" // Backbone will try match the route above first
                }
            }),
            app_router = new AppRouter();

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

        window.mode = "reportcard";
        var activeMatch = function (child, name, id) {
            "use strict";
            var child_id = child.attr("id");
            console.log("ok child is is " + child_id + " id is " + name + " : " + (child_id === name));
            return child_id === name;
        };

        var tabView = new tab_view.TabView({"activeMatch": activeMatch, "prefix": "dashboard"});

        $("#league_navigation").append(tabView.render([
            {id: 'reportcard', name: "Report Card", href: "#reportcard"},
            {id: 'lineup', name: "Lineups", href: "#lineup"},
            {id: 'draft', name : 'Draft', href: "#draft"},
            {id: 'waiver', name: 'Waiver', href: "#waiver"},
            {id: 'trade', name: 'Trade', href: "#trade"}
        ]).el);


        app_router.on('route', function (name, id) {
            "use strict";
            id = id[0];
            if (name === 'getTeam') {
                name = window.mode;
            } else {
                console.log("chaning window mode to " + name);
                window.mode = name;
            }
            if (id) {
                roguesReportCard.set('team_id', id);
                roguesReportCard.fetch().done(function () {
                    $(".team-link-header").html("Team: " + $("#team-link-" + id).html());
                });
            }

        });

        // Instantiate the router
        app_router.on('route:getTeam', function (id) {
            app_router.navigate(window.mode + '/' + id, {replace: true});
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