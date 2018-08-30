var app = angular.module('techfin',[]);

app.config(['$httpProvider','$interpolateProvider', function ($httpProvider,$interpolateProvider){
  $httpProvider.defaults.useXDomain = true;
  delete $httpProvider.defaults.headers.common['X-Requested-With'];
//  $httpProvider.interceptors.push('httpRequestInterceptor');
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
}]);

app.controller('home', function($scope, $http){
	$scope.InvestmentPeriod = 50;
	$scope.InvestmentRisk = 50;
	$scope.pathTable = false;
	$scope.showList = false;
	$scope.type = 'b';
	$scope.tableList = []
	$scope.estimatePath = function(){
		$scope.showList = false;
		// console.log($scope.InvestmentPeriod);console.log($scope.InvestmentRisk);console.log($scope.Investmentamt);
		$http.post('/api/v1/index/pathpredict/', {'amt': $scope.Investmentamt, 'period': $scope.InvestmentPeriod, 'risk': $scope.InvestmentRisk}).then(function successCallback(response){
			console.log(response.data.percentagedistri);
			$scope.sbanks = response.data.banks;
			$scope.complist = response.data.stockcompanies.slice(1, response.data.stockcompanies.length -1);
			$scope.pptyList = response.data.propertyList;
			$scope.percentage = response.data.percentagedistri;
			console.log($scope.percentage);
			$scope.pathTable = true;
			}, function errorCallback(response){
				alert("Something went wrong..")
		});
	};
	
	$scope.riskProfile = function(){
		$scope.InvestmentRisk = 0;
		if($scope.riskq1 ==null ||$scope.riskq4 ==null||$scope.riskq3 ==null||$scope.riskq2 ==null){
			alert("answer to all questions"); return;
		}
		// console.log($scope.riskq1 +$scope.riskq2+$scope.riskq3+$scope.riskq4);
		$scope.InvestmentRisk = (parseInt($scope.riskq1) + parseInt($scope.riskq2)+parseInt($scope.riskq3)+parseInt($scope.riskq4))/4;
		console.log($scope.InvestmentRisk);
		$('#riskprofile').modal("hide");
	};
	
	$scope.timeProfile = function(){
		$scope.InvestmentTime = 0;
		if($scope.timeq1 ==null ||$scope.timeq3 ==null||$scope.timeq2 ==null){
			alert("answer to all questions"); return;
		}
		// console.log($scope.riskq1 +$scope.riskq2+$scope.riskq3+$scope.riskq4);
		$scope.InvestmentTime=(parseInt($scope.timeq1)+parseInt($scope.timeq2)+parseInt($scope.timeq3))/3;
		console.log($scope.InvestmentTime);
		$('#timeprofile').modal("hide");
	};

	$scope.getList = function(val){
		console.log(val);
		if(val == "b"){ $scope.tableList = $scope.sbanks;$scope.type = 'b';}
		else if(val == "s"){ $scope.tableList = $scope.complist; $scope.type = 's';}
		else if(val == "p"){$scope.tableList = $scope.pptyList; $scope.type = 'p';}
		console.log($scope.tableList);
		$scope.showList = true;
	};

	$scope.getDetails = function(val, type){
		console.log(val, type);
		$http.get('/api/v1/index/details/?name='+val+'&type='+type).then(function successCallback(response){
			$scope.details = response.data;
			if(type == 'p'){
				 $('details').html("<div id='map'></div>");
				 console.log($scope.details);
				 initMap($scope.details.LatLng);
			}
			}, function errorCallback(response){
			alert("Something went wrong..")
		});
		
	};

	function initMap(LatLng) {
		var myLatLng = LatLng;

		var map = new google.maps.Map(document.getElementById('map'), {
		  zoom: 4,
		  center: myLatLng
		});

		var marker = new google.maps.Marker({
		  position: myLatLng,
		  map: map,
		  title: 'Hello World!'
		});
	}

	$scope.stocks = function(){window.location.replace("/stocks");};
	$scope.banking = function(){window.location.replace("/banking");};
	$scope.gold = function(){window.location.replace("/gold");};
	$scope.realestate = function(){window.location.replace("/realestate");}; 	
});