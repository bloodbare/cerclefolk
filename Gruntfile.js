module.exports = function (grunt) {
    'use strict';
    grunt.initConfig({
        'pkg': 'cerclefolk.theme',
        'less': {
            'dist': {
                'options': {
                    'paths': [],
                    'strictMath': false,
                    'sourceMap': true,
                    'outputSourceFiles': true,
                    'sourceMapURL': '++theme++cerclefolk/less/cerclefolk-compiled.css.map',
                    'sourceMapFilename': 'src/cerclefolk.theme/cerclefolk/theme/diazo_cercle/less/cerclefolk-compiled.css.map',
                    'modifyVars': {
                        "isPlone": "false"
                    }
                },
                'files': {
                    'src/cerclefolk.theme/cerclefolk/theme/diazo_cercle/less/cerclefolk-compiled.css': 'src/cerclefolk.theme/cerclefolk/theme/diazo_cercle/less/barceloneta.plone.local.less',
                }
            }
        },

        'watch': {
            'scripts': {
                'files': ['src/cerclefolk.theme/cerclefolk/theme/diazo_cercle/less/*.less'],
                'tasks': ['less']
            }
        }
    });

    // grunt.loadTasks('tasks');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.registerTask('default', ['watch']);
    grunt.registerTask('compile', ['less']);
};
