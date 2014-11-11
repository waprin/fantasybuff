'use strict';
/*globals requirejs */

requirejs.config({
    baseUrl: '/static/js/',
    paths: {
        'jquery': 'lib/jquery-1.11.0',
        'underscore': 'lib/underscore',
        'backbone': 'lib/backbone',
        'd3': 'lib/d3',
        'd3.bullet': 'lib/d3.bullets',
        'bootstrap': 'lib/bootstrap'
    },
    shim: {
        'underscore': {
            exports: '_'
        },
        'd3': {
            exports: 'd3'
        },
        'd3.bullet': ['d3'],
        'backbone': {
            //These script dependencies should be loaded before loading
            //backbone.js
            deps: ['underscore', 'jquery'],
            //Once loaded, use the global 'Backbone' as the
            //module value.
            exports: 'Backbone'
        },
        "bootstrap": {
            deps: ["jquery"],
            exports: "$.fn.popover"
        }
    }
});

// Start loading the main app file. Put all of
// your application logic in there.
requirejs(['app/league_view']);