'use strict';

describe('Filter: appFilter', function () {

  // load the filter's module
  beforeEach(module('appApp'));

  // initialize a new instance of the filter before each test
  var appFilter;
  beforeEach(inject(function ($filter) {
    appFilter = $filter('appFilter');
  }));

  it('should return the input prefixed with "appFilter filter:"', function () {
    var text = 'angularjs';
    expect(appFilter(text)).toBe('appFilter filter: ' + text);
  });

});
