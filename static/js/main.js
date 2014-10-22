'use strict';
/*globals requirejs */

requirejs.config({
    baseUrl: 'static/',
    paths: {
        'jquery': 'js/jquery-1.11.0',
        'underscore': 'js/underscore',
        'backbone': 'js/backbone'
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
        }
    }
});

// Start loading the main app file. Put all of
// your application logic in there.
requirejs(['js/app/main']);