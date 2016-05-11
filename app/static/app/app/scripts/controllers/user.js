'use strict';

/**
 * @ngdoc function
 * @name appApp.controller:UserCtrl
 * @description
 * # UserCtrl
 * Controller of the appApp
 */
angular.module('appApp')
  .controller('UserCtrl', function ($scope, appService, $cookies) {
     
		$scope.user={};
        
		appService.get('user/profile/').then(function(res){
			$scope.user=res;
		});
		
       
		$scope.saveprofile=function (user) {
			
			appService.put("user/profile/" , user).then(function (results) {
					toaster.pop(results);
					
				});
			

		};
            
        
        
        $scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };
	
  });
