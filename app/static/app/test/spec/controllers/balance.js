'use strict';

describe('Controller: BalanceCtrl', function () {

  // load the controller's module
  beforeEach(module('appApp'));

  var BalanceCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    BalanceCtrl = $controller('BalanceCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(BalanceCtrl.awesomeThings.length).toBe(3);
  });
});
