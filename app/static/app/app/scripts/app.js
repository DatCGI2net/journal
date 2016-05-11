'use strict';

/**
 * @ngdoc overview
 * @name appApp
 * @description
 * # appApp
 *
 * Main module of the application.
 */
angular
  .module('appApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
	'toaster'
  ])
  .factory("EntryUtil", ['toasterConfig',
    function (toasterConfig) { // This service connects to our REST API

        

	var obj = {};
	obj.changeUSTCode = function(ustcode){
			//console.log('changeUST:'+ustcode);
			var steuersatzObj=[];
			if (ustcode== "1" || ustcode== "2" || ustcode== "9" || ustcode== "12"){
				steuersatzObj =toasterConfig.steuersatz;
				return steuersatzObj;
			}
			steuersatzObj = [toasterConfig.steuersatz[0]];//toasterConfig.steuersatz;
			if (ustcode== "5" || ustcode== "6" || ustcode== "7" || ustcode== "27"|| ustcode== "77")
				return steuersatzObj;
			//steuersatzObj = [];
			for( v in toasterConfig.steuersatz){
				
				var item =toasterConfig.steuersatz[v];
				if(item.key!=="13%")
					steuersatzObj.push(item);
			};
			
			return steuersatzObj;
		};
		
		obj.getUSTCode=function(ustcode){
			var it={};
			for( v in toasterConfig.ustCodes){
				
				var item =toasterConfig.ustCodes[v];
				//console.log('compare:',item.key,ustcode);
				if(item.key === (ustcode + "")){
					it =item;
					break;
				}
				
			};
			return it;
		}
		
		obj.getsteuersatz=function(steuersatz){
			var it={};
			for( v in toasterConfig.steuersatz){
				
				var item =toasterConfig.steuersatz[v];
				if(item.key=== (""+steuersatz)){
					it =item;
					break;
				}
				
			};
			return it;
		};
		
		obj.scrubentry = function(entry){
			var newEntry=angular.copy(entry);
			delete newEntry['ustCodes'];
			delete newEntry['steuersatzObj'];
			newEntry.ust_code=parseInt(newEntry.ust_code.key);
			newEntry.steuersatz=parseInt(newEntry.steuersatz.key);
			if(newEntry.eingang==='')
				newEntry.eingang=0
			if(newEntry.ausgang==='')
				newEntry.ausgang=0
			if(newEntry.skonto==='')
				newEntry.skonto=0
			
			if( newEntry.tag instanceof Date)
				newEntry.tag=newEntry.tag.getFullYear()+'-'+(newEntry.tag.getMonth()+1)+'-'+newEntry.tag.getDate() ;
			else{
				
				var tds = newEntry.tag.split('.');
		
				newEntry.tag=tds[2]+'-'+tds[1]+'-'+tds[0] ;
			}
			/*
			var ks = Object.keys(entry);
			for( k in ks){
				if(k !=='ustCodes' || k !== 'steuersatzObj')
				newEntry[k]=entr[k];
			}
			*/
			
			return newEntry;
		};

	return obj;
}])
  .config(function($interpolateProvider){
		$interpolateProvider.startSymbol('{$');
		$interpolateProvider.endSymbol('$}');
	})
	.config(function($httpProvider){
		$httpProvider.defaults.headers.post['Content-Type'] = 'application/json; charset=utf-8';
		$httpProvider.defaults.headers.common['X-Requested-With']='XMLHttpRequest';
		$httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
		
		//Enable cross domain calls
		$httpProvider.defaults.useXDomain = true;
	 
		//Remove the header containing XMLHttpRequest used to identify ajax call 
		//that would prevent CORS from working
		//delete $httpProvider.defaults.headers.common['X-Requested-With'];
	})
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/dashboard.html',
        controller: 'DashboardCtrl',
        controllerAs: 'dashboard'
      })
      .when('/balance', {
        templateUrl: 'views/balance.html',
        controller: 'BalanceCtrl',
        controllerAs: 'balance'
      })
	  .when('/entry', {
        templateUrl: 'views/entry.html',
        controller: 'EntryCtrl',
        controllerAs: 'entry'
      })
	  .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
	  .when('/user/login', {
        templateUrl: 'views/login.html',
        controller: 'LoginCtrl',
        controllerAs: 'login'
      })
	  
	  .when('/user/signup', {
        templateUrl: 'views/signup.html',
        controller: 'UserCtrl',
        controllerAs: 'user'
      })
	  .when('/user/profile', {
        templateUrl: 'views/profile.html',
        controller: 'UserCtrl',
        controllerAs: 'user'
      })
      .otherwise({
        redirectTo: '/'
      });
  })
  .run(function ($rootScope, $location, appService,$cookies) {
        $rootScope.$on("$routeChangeStart", function (event, next, current) {
			//
			var sessionid=$cookies.get('loggedin');
			if(sessionid !== undefined && sessionid.length > 0){
				$rootScope.authenticated = true;
				$rootScope.user ={};
				
				$rootScope.user.id = $cookies.get('userid');
				$rootScope.user.name = $cookies.get('username');
				console.log('$rootScope.user:',$rootScope.user);
				return;
			}
			console.log('loggedin:'+sessionid);
			//console.log('path:'+$location.path());
            if($rootScope.user === undefined || typeof $rootScope.authenticated == 'undefined' || $rootScope.authenticated===false) {
				var nextUrl = next.$$route.originalPath;
				//console.log('nextUrl:'+nextUrl);
				var path =$location.path();
				if (nextUrl == '/user/login' || path == '/user/signup' || path == '/user/verify' || path == '/user/agreement') {
					

				} else {
					
				
					appService.get('user/session').then(function (results) {
						if (results.id && results.id !== '') {

							$rootScope.authenticated = true;
							$rootScope.user.id = results.id;
							$rootScope.user.name = results.name;
							$rootScope.user.email = results.email;
							$location.path("/");
						} else {
							var nextUrl = next.$$route.originalPath;
							if (nextUrl == '/user/login') {

							} else {
								$location.path("/user/login");
							}
						}
					});
				}
            }
        });
    })
  ;
