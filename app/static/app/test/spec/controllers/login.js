'use strict';

var rootScope;
beforeEach(module(function ($provide) {
  rootScope = {
    user: {}
  };
  $provide.value('rootScope', rootScope);
}));

describe('Controller: LoginCtrl', function () {

  // load the controller's module
  beforeEach(module('appApp'));

  var LoginCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    LoginCtrl = $controller('LoginCtrl', {
      $scope: scope,
	  $rootScope: $rootScope
      // place here mocked dependencies
    });
  }));

  it('should attach a login object to the scope', function () {
    console.log('scope.login:',scope.login);
	expect(scope.login).toEqual({});
  });
  
  it('should attach a signup object to the scope', function () {
    
	expect(scope.signup).toEqual({});
  });
  
  
  
  
  
});
