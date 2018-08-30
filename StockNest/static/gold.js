var app = angular.module('techfinGold',[]);

app.config(['$httpProvider','$interpolateProvider', function ($httpProvider,$interpolateProvider){
  $httpProvider.defaults.useXDomain = true;
  delete $httpProvider.defaults.headers.common['X-Requested-With'];
//  $httpProvider.interceptors.push('httpRequestInterceptor');
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
}]);

// var background = ['rgba(255, 99, 132, 0.2)','rgba(54, 162, 235, 0.2)','rgba(255, 206, 86, 0.2)','rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)', 'rgba(255, 200, 200, 0.2)', 'rgba(75, 200, 192, 0.2)','rgba(255, 102, 255,0.2','rgba(255, 170, 64, 0.2'];
//  $(document).ready(function() {
// 	$('#predInfobtn').click();
// 	$('#showPredbtn').click();	 	
// });

function drawGraph(type,id,data,labels,company){
  $("#canvas_"+id.toString()).remove();
  $("#parent_"+id.toString()).append($('<canvas />', {'id':'canvas_'+id.toString()}).height(600).width(1000));
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

function multipleGraph(type,id,data1,data2, labels1, companyname1, companyname2){
  $("#canvas_"+id.toString()).remove();
  $("#parent_"+id.toString()).append($('<canvas />', {'id':'canvas_'+id.toString()}).height(600).width(1000));
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
	$scope.companySelected = "goldPrediction";

	$scope.termType = function(){
		if($scope.termSelect == "short") $scope.displayList = $scope.companyList.slice(10, 15);
		else if($scope.termSelect == "mid") $scope.displayList = $scope.companyList.slice(5, 10);
		else if($scope.termSelect == "long") $scope.displayList = $scope.companyList.slice(0, 5);
		else $scope.displayList = $scope.companyList;
		console.log($scope.termSelect);
		console.log($scope.displayList);
		window.location.replace("#predict")
	};

 $(document).ready(function() {
	$scope.showPred();
	$scope.predictInfo();	 	
});

	$scope.showPred = function(){
		$http.get("/api/v1/stocks/actualvspred/?company=" + $scope.companySelected).then(function successCallback(response){
			var graphData = response.data.graphData;
			$scope.MSE = response.data.mse;
			$scope.MAE = response.data.mae;
			// alerst("company MSE: "+ MSE.toString()+ "\n company MAE: " + MAE.toString()) ;
			// console.log(graphData.expected, graphData.predictions, graphData.labels);
			multipleGraph('lines','goldmodel', graphData.expected, graphData.predictions, graphData.labels, "predictions","actual");

			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};

	$scope.predictInfo = function(){
		$http.get("/api/v1/stocks/predict/?company=" + $scope.companySelected).then(function successCallback(response){
			var predictions = response.data.predictions;
			drawGraph('lines','goldprediction', predictions.price, predictions.label, "prediction");

			}, function errorCallback(response){
		alert("Some Problem...."); 
		});
	};
});