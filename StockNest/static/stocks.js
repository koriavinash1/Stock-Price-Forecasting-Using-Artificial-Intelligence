var app = angular.module('techfinStocks',[]);

app.config(['$httpProvider','$interpolateProvider', function ($httpProvider,$interpolateProvider){
  $httpProvider.defaults.useXDomain = true;
  delete $httpProvider.defaults.headers.common['X-Requested-With'];
//  $httpProvider.interceptors.push('httpRequestInterceptor');
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
}]);

// var background = ['rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)','rgba(255, 206, 86, 0.2)','rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)', 'rgba(255, 200, 200, 0.2)', 'rgba(75, 200, 192, 0.2)','rgba(255, 102, 255,0.2','rgba(255, 170, 64, 0.2'];

function drawGraph(type,id,data,labels,company){
  $("#canvas_"+id.toString()).remove();
  $("#parent_"+id.toString()).append($('<canvas />', {'id':'canvas_'+id.toString()}).height(550).width(950));
  var qid = document.getElementById("canvas_"+id.toString());
  var myChart = new Chart(qid, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: company,
        data: data,
        backgroundColor:'rgba(255, 99, 132, 0.2)',
        borderWidth: 2,
      }]
    },
    options: {
        responsive: false,
    }
  });
}

function multipleGraph(type,id,data1,data2, labels1, companyname2, companyname1){
  $("#canvas_"+id.toString()).remove();
  $("#parent_"+id.toString()).append($('<canvas />', {'id':'canvas_'+id.toString()}).height(550).width(950));
  var qid = document.getElementById("canvas_"+id.toString());
  var myChart = new Chart(qid, {
    type: 'line',
    data: {
      labels: labels1,
      datasets: [{
        label: companyname1,
        data: data2,
        backgroundColor:'rgba(0,0,255, 0.2)',
        borderWidth: 2,
      },
      {
        label: companyname2,
        data: data1,
        backgroundColor:'rgba(255, 0, 0, 0.2)',
        borderWidth: 2,
      }]
    },
    options: {
        responsive: false,
    }
  });
}

app.controller('home', function($scope, $http){
	// First row: TOP trading, Second row: Moderate Trading, Third row: Lowest Trading
	// $scope.companyList = ['EICHERMOT',  'BOSCHLTD', 'MARUTI', 'ULTRACEMCO', 'HEROMOTOCO', 'BAJAJ-AUTO', 'DRREDDY', 'TCS', 'ACC', 'HDFCBANK', 
	// 	'TATAMOTORS', 'BPCL', 'AXISBANK', 'TATASTEEL', 'ZEEL', 'CIPLA', 'SUNPHARMA', 'AUROPHARMA', 'HCLTECH', 'INFY', 'TATAMOTORS',
	// 	'TATAPOWER', 'BANKBARODA', 'NTPC', 'ONGC', 'POWERGRID', 'HINDALCO', 'COALINDIA', 'AMBUJACEM', 'VEDL', 'TATAMTRDVR'];

	$scope.companyList = $scope.displayList = ['EICHERMOT',  'BOSCHLTD', 'MARUTI', 'ULTRACEMCO', 'HEROMOTOCO',
				 'TATAMOTORS', 'BPCL', 'AXISBANK', 'TATASTEEL', 'ZEEL', 
				 'CIPLA', 'TATAPOWER', 'BANKBARODA', 'NTPC', 'ONGC'];

	$scope.termSelect = "";
	$scope.predictionLengths = [1, 2, 5, 10, 30];
	$scope.companySelected = null;

	$scope.ourSuggestion = "";
	$scope.errorInfo = "";
	$scope.suggestion = false;

	$scope.termType = function(){
		if($scope.termSelect == "short") $scope.displayList = $scope.companyList.slice(10, 15);
		else if($scope.termSelect == "mid") $scope.displayList = $scope.companyList.slice(5, 10);
		else if($scope.termSelect == "long") $scope.displayList = $scope.companyList.slice(0, 5);
		else $scope.displayList = $scope.companyList;
		console.log($scope.termSelect);
		console.log($scope.displayList);
		window.location.replace("#predict")
	};

	$scope.companyChanged = function(){
		console.log($scope.companySelected);
		if($scope.companySelected != null) $('#predBtn').show();
	};

	$scope.showPred = function(comp){
		$http.get("/api/v1/stocks/actualvspred/?company=" + comp).then(function successCallback(response){
			var graphData = response.data.graphData;
			var MSE = response.data.mse;
			var MAE = response.data.mae*100;
			$scope.errorInfo = "The deviation of Predicted price from the actual stock price is:  " + MAE.toString().slice(0,5)+"%" ;
			// console.log(graphData.expected, graphData.predictions, graphData.labels);
			multipleGraph('lines','stockprediction', graphData.expected, graphData.predictions, graphData.labels, "actual", "predictions");

			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};

	$scope.predictInfo = function(){
		$http.get("/api/v1/stocks/predict/?company=" + $scope.companySelected).then(function successCallback(response){
			var predictions = response.data.predictions;
			console.log(predictions);
			drawGraph('lines','stockprediction', predictions.stocks, predictions.label, "prediction");
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};

	$scope.compare = function(){
		if($scope.companySelected1 == $scope.companySelected2) {alert("Both companies can't be same...");return;};
		$http.get("/api/v1/stocks/compare/?company1=" + $scope.companySelected1 + "&company2="+$scope.companySelected2).then(function successCallback(response){
			var predictions = response.data.predictions;
			$scope.compTableInfo = response.data.tableInfo;
			$scope.suggestion = true;
			console.log($scope.compTableInfo);
			// multipleGraph('lines','stockcompare', predictions.company1, predictions.company2, predictions.labels, $scope.companySelected1.name.toString(), $scope.companySelected2.name.toString());
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};

	$scope.lengthChanged = function(){
		console.log($scope.lengthSelected);
	};

	$scope.groupStatusChanged = function(){
		$scope.displayList1 = []
		$http.get("/api/v1/stocks/getCompanyList/").then(function successCallback(response){
			$scope.compInfo = response.data.company_data;
			// console.log($scope.compInfo);
			for(i=0; i<$scope.compInfo.length; i++) 
				if($scope.groupingStatus == "low"){
					// console.log($scope.groupingStatus);
					if($scope.compInfo[i].turnoverbyvolume < 1000) $scope.displayList1.push($scope.compInfo[i]);
				}
				else if ($scope.groupingStatus == "mid"){
					// console.log($scope.groupingStatus);
					if($scope.compInfo[i].turnoverbyvolume < 10000 && $scope.compInfo[i].turnoverbyvolume > 1000) {
						$scope.displayList1.push($scope.compInfo[i]);
					}
				}
				else if ($scope.groupingStatus == "high"){ 
					// console.log($scope.groupingStatus);
					if( $scope.compInfo[i].turnoverbyvolume > 10000) {
						$scope.displayList1.push($scope.compInfo[i]);
					}
				}
			// console.log($scope.displayList);
		
			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};
});