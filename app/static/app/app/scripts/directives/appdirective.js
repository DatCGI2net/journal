'use strict';

/**
 * @ngdoc directive
 * @name appApp.directive:appDirective
 * @description
 * # appDirective
 */
angular.module('appApp')
  .directive('appDirective', function () {
    return {
      template: '<div></div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the appDirective directive');
      }
    };
  });
