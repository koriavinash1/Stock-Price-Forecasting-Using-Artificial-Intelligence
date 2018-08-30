var app = angular.module('techfinlogin',[]);

app.config(['$httpProvider','$interpolateProvider', function ($httpProvider,$interpolateProvider){
  $httpProvider.defaults.useXDomain = true;
  delete $httpProvider.defaults.headers.common['X-Requested-With'];
//  $httpProvider.interceptors.push('httpRequestInterceptor');
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
}]);

app.controller('login', function($scope, $http){
	$scope.username = $scope.password = null
	$scope.loginview = true;
	$scope.signupview = false;
	$scope.login = function(){
		if( $scope.username == null || $scope.password == null){alert("Enter proper user details.."); return;}
		// if($scope.username == "test" && $scope.password == "test"){window.location.replace("/index");}
		// else{alert("user not found")}
		$http.post("api/v1/login",{'username': $scope.username, 'password': $scope.password}).then(function successCallback(response){
			window.location.replace("/index");
			}, function errorCallback(response){
			alert("something went wrong..")
		});
	};
	$scope.signupviewfunc = function(){
		$scope.signupview = true;
		$scope.loginview = false;
	}

	$scope.signup = function(){

	};
});