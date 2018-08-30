var app = angular.module('techfinStocksAdmin',[]);

app.config(['$httpProvider','$interpolateProvider', function ($httpProvider,$interpolateProvider){
  $httpProvider.defaults.useXDomain = true;
  delete $httpProvider.defaults.headers.common['X-Requested-With'];
//  $httpProvider.interceptors.push('httpRequestInterceptor');
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
}]);

app.controller('home', function($scope, $http){
	$scope.companyList = $scope.displayList = ['EICHERMOT',  'BOSCHLTD', 'MARUTI', 'ULTRACEMCO', 'HEROMOTOCO',
				 'TATAMOTORS', 'BPCL', 'AXISBANK', 'TATASTEEL', 'ZEEL', 
				 'CIPLA', 'TATAPOWER', 'BANKBARODA', 'NTPC', 'ONGC'];
	$scope.predictionLengths = [1, 2, 5, 10, 30];
	$scope.checkboxList = [false, false, false, false, false, false, false, false, false, false, false, false, false, false, false]; 
	$scope.updateModel = function(){
		if(!confirm("Do you really want to update Model?.....")) return
		$http.put("/api/v1/stocks/updatemodel/",{'update': true, 'seqlength': 30}).then(function successCallback(response){
			alert("models updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};
	$scope.updateNews = function(){
		$http.put("/api/v1/stocks/updatenews/",{'update': true}).then(function successCallback(response){
			alert("models updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});

	};
	$scope.updateTweets = function(){
		$http.put("/api/v1/stocks/updatetweets/",{'update': true}).then(function successCallback(response){
			alert("models updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});

	};
	$scope.updateMS = function(){
		$http.put("/api/v1/stocks/updatems/",{'update': true}).then(function successCallback(response){
			alert("models updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});

	};
	$scope.trainModel = function(){
		$("#trainModal").modal("show");
	};
	$scope.updateDB = function(){
		$("#updatedbModal").modal("show");
	};

	$scope.update = function(companyList, checkboxList){
		var comp = [];
		for(i =0; i < checkboxList.length; i++)  if(checkboxList[i]) 	comp.push(companyList[i]);

		$http.put("/api/v1/stocks/updatedb/",{'update': true, 'companies': comp}).then(function successCallback(response){
			alert("database updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};

	$scope.train = function(companyList, checkboxList){
		var comp = [];
		for(i =0; i < checkboxList.length; i++)  if(checkboxList[i]) 	comp.push(companyList[i]);

		$http.put("/api/v1/stocks/trainmodel/",{'update': true, 'companies': comp, 'plength': $scope.lengthSelected, 'seqlength': $scope.seqlengthSelected}).then(function successCallback(response){
			alert("database updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};


	// For gold prediction.............

	$scope.updateGoldModel = function(){
		if(!confirm("Do you really want to update Model?.....")) return
		$http.put("/api/v1/stocks/updatemodel/",{'update': true, 'seqlength': 30, 'plength': 2, 'gold': true}).then(function successCallback(response){
			alert("models updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};

	$scope.trainGoldModel = function(){
		$http.put("/api/v1/gold/trainmodel/",{'update': true, 'plength': 2, 'seqlength': 30}).then(function successCallback(response){
			alert("database updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};

	$scope.updateGoldDB = function(){
		$http.put("/api/v1/gold/updatedb/",{'update': true}).then(function successCallback(response){
			alert("database updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};
	
	$scope.updateGoldNews = function(){
		$http.put("/api/v1/stocks/updatenews/",{'update': true, 'gold':true}).then(function successCallback(response){
			alert("models updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};

	$scope.updateGoldTweets = function(){
		$http.put("/api/v1/stocks/updatetweets/",{'update': true, "gold":true}).then(function successCallback(response){
			alert("models updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};

	// Banking.......

	$scope.updateBankDB = function(){
		$http.put("/api/v1/bank/updatedb/",{'update': true}).then(function successCallback(response){
			alert("database updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};


	// realestate model...........
	$scope.trainRealEstateModel = function(){
		$http.post("/api/v1/realestate/train/",{'update': true}).then(function successCallback(response){
			alert("Model Trained!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};


	$scope.updateRealEstateDB = function(){
		$http.put("/api/v1/realestate/updateDB/",{'update': true}).then(function successCallback(response){
			alert("database updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};


	$scope.RealEstatePrediction = function(){
		$http.put("/api/v1/realestate/updatePrediction/",{'update': true}).then(function successCallback(response){
			alert("database updated!!!!");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};
});	