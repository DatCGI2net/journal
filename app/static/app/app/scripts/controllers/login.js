'use strict';

/**
 * @ngdoc function
 * @name appApp.controller:LoginCtrl
 * @description
 * # LoginCtrl
 * Controller of the appApp
 */
angular.module('appApp')
  .controller('LoginCtrl', function ($rootScope, $scope, $cookies, $location, appService) {
    
	$scope.login = {};
	$scope.signup = {};
	
	$rootScope.user = {};
	
	
	$scope.doLogin = function(login){
		console.log('login:',login);
		
		appService.post('user/login', {
                    user: login
                }).then(function (results) {
                    //Data.toast(results);
                    if (results.username == login.email) {
						$rootScope.user=results;
						
						
                        $rootScope.authenticated = true;
						
                        $rootScope.user.id = results.id;
                        $rootScope.user.name = results.username;
                        $rootScope.user.email = results.email;
						$cookies.put('loggedin',1);
						$cookies.put('userid', $rootScope.user.id);
						$cookies.put('username', $rootScope.user.name);
						
                        $location.path('/');
                    }
                });
	};
   	
	
	
  });
