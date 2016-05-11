'use strict';

/**
 * @ngdoc service
 * @name appApp.appService
 * @description
 * # appService
 * Service in the appApp.
 */
angular.module('appApp')
  .service('appService', function ($http) {
    // AngularJS will instantiate a singleton by calling "new" on this function
		var serviceBase = 'http://10.0.0.20:8080/api/';

        
        
        this.get = function (q,object) {
            return $http.get(serviceBase + q, object).then(function (results) {
                return results.data;
            });
        };
        this.post = function (q, object) {
            return $http.post(serviceBase + q, object).then(function (results) {
                return results.data;
            });
        };
        this.put = function (q, object) {
            return $http.put(serviceBase + q, object).then(function (results) {
                return results.data;
            });
        };
        this.delete = function (q) {
            return $http.delete(serviceBase + q).then(function (results) {
                return results.data;
            });
        };

       
	
	
  });
