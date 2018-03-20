// baseApp
var baseApp = angular.module('baseApp', []);

// baseApp Configuration
// 1. check out csrf token from site cookies on the browser (for django POST)
// 2. change binding symbol from {{}} to {! !}
baseApp.config(['$httpProvider', function($httpProvider, $interpolateProvider) {

    // 1. check out csrf token from site cookies on the browser (for django POST)
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

    // 2. change binding symbol from {{}} to {! !}
    $interpolateProvider.startSymbol('{!');
    $interpolateProvider.endSymbol('!}');

}]);




