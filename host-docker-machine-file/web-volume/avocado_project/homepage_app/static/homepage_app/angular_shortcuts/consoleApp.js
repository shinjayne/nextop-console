// consoleApp
var consoleApp = angular.module('consoleApp', []);

// baseApp Configuration
// 1. check out csrf token from site cookies on the browser (for django POST)
// 2. change binding symbol from  to {! !}
consoleApp.config(function($interpolateProvider, $httpProvider) {
        // 1. check out csrf token from site cookies on the browser (for django POST)
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    // 2. change binding symbol from  to {! !}
    $interpolateProvider.startSymbol('{!');
    $interpolateProvider.endSymbol('!}');

});


