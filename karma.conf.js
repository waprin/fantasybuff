// Karma configuration
// Generated on Wed Oct 22 2014 16:49:37 GMT-0400 (EDT)

module.exports = function (config) {
    'use strict';
    config.set({

        // base path that will be used to resolve all patterns (eg. files, exclude)
        basePath: 'static/',


        // frameworks to use
        // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
        frameworks: ['jasmine', 'requirejs'],


        // list of files to exclude
        exclude: [
            'js/app/main.js'
        ],

        coffeePreprocessor: {
            // options passed to the coffee compiler
            options: {
                bare: true,
                sourceMap: true,
                // transforming the filenames
                transformPath: function (path) {
                    return path.replace(/\.coffee$/, '_bare.js');
                }
            }
        },

        // preprocess matching files before serving them to the browser
        // available preprocessors: https://npmjs.org/browse/keyword/karma-preprocessor
        preprocessors: {
            '**/*.coffee': ['coffee']
        },

        // list of files / patterns to load in the browser
        files: [
            {pattern: 'text.js', included: false},
            {pattern: 'js/jquery-1.11.0.js', included: false},
            {pattern: 'js/underscore.js', included: false},
            {pattern: 'js/backbone.js', included: false},
            {pattern: 'js/app/templates/*.html', included: false},
            {pattern: 'js/app/*.coffee', included: false},
            {pattern: 'js/app/*.js', included: false},
            {pattern: 'test/**/*.coffee', included: false},
            {pattern: 'test/**/*Spec.js', included: false},
            {pattern: 'test/**/*Spec.js', included: false},
            {pattern: '**/*.ejs', included: false},
            'test/main-test.js'
        ],

        // test results reporter to use
        // possible values: 'dots', 'progress'
        // available reporters: https://npmjs.org/browse/keyword/karma-reporter
        reporters: ['dots'],


        // web server port
        port: 9876,


        // enable / disable colors in the output (reporters and logs)
        colors: true,


        // level of logging
        // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,


        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: true,


        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        browsers: ['Chrome'],


        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        singleRun: false
    });
};
