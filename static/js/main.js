'use strict';
/*globals requirejs */

requirejs.config({
    baseUrl: '/static/js',
    paths: {
        'jquery': 'lib/jquery-1.11.0',
        'underscore': 'lib/underscore',
        'backbone': 'lib/backbone',
        'bootstrap': 'lib/bootstrap'
    },
    shim: {
        'underscore': {
            exports: '_'
        },
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
    },
    enforceDefine: true
});

// Start loading the main app file. Put all of
// your application logic in there.
requirejs(['app/main']);