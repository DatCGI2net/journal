'use strict';

describe('Directive: appDirective', function () {

  // load the directive's module
  beforeEach(module('appApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<app-directive></app-directive>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the appDirective directive');
  }));
});
