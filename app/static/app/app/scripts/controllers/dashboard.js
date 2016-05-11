'use strict';

/**
 * @ngdoc function
 * @name appApp.controller:DashboardCtrl
 * @description
 * # DashboardCtrl
 * Controller of the appApp
 */
angular.module('appApp')
  .controller('DashboardCtrl', function ($rootScope,$scope, $cookies, $location, appService) {
    
	$scope.balance={};
	
	$scope.logout = function () {
		console.log('logout');
		appService.delete('user/logout').then(function (results) {
			
			$rootScope.user = {};
			$cookies.remove('username');
			$cookies.remove('userid');
			$cookies.remove('loggedin');
			$location.path('login');
		});
	};
	
	// check balance
	appService.get('balance/check/').then(function(res){
		
		console.log('balance:',res)
	});
	
	
	
  });
