'use strict';

/**
 * @ngdoc filter
 * @name appApp.filter:appFilter
 * @function
 * @description
 * # appFilter
 * Filter in the appApp.
 */
angular.module('appApp')
  .filter('appFilter', function () {
    return function (input) {
      return 'appFilter filter: ' + input;
    };
  });
