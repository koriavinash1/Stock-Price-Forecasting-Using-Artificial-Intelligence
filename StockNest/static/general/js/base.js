/* ROOTSCOPE VARIABLES 
tUrl
openHubCourse
*/

/* GLOBAL VARIABLES/FUNCTIONS
DEBUG
S3_REGION_CODE
STATIC_BUCKET
MAIN_BUCKET
MAIN_COGNITO_POOL
CAPTCHA_PUBLIC_KEY
JW_LIC_KEY
IS_LOGGED
hideSidebar
closeTopNav
topNavSpaceConf
showSidebar
hideTopbar
showTopbar
widthConf
randomString
ehLoad
ehDone
gotoLogin
ehLoadSet
EMOJI_JSON
*/

const NAVBAR_TOGGLE_BREAKPOINT = 800;
var isSidebarPresent = false;
var IS_LOGGED = false;
// const messaging = firebase.messaging();
NProgress.configure({ showSpinner: false });

$(document).ready(function() {
  $('#page-content-wrapper').css("display","block");
});

function topNavSpaceConf(){
  if ($(window).width() > 850){
    $('#topNavSpaceDiv').show();
    $('#topContentSpaceDiv').remove();
  }
  else{
   $('#topNavSpaceDiv').remove();
   $('#topContentSpaceDiv').show();
  }
}

// function hideSidebar(){
//   $('#sidebar-wrapper').hide();
//   $('#sidebarmenu-toggle').hide();
//   $('#page-content-wrapper').css("margin-left","0px");
//   isSidebarPresent = false;
//   widthConf();
// }

// function showSidebar(){
//   isSidebarPresent = true;
//   widthConf();
// }

function hideTopBar(){
  $('#mainTopNavList').hide();
}

function showTopBar(){
  $('#mainTopNavList').show();
}

function widthConf() {
  setTimeout(function(){//solves notification width problem
    var contentWidth = $("#page-content-wrapper").width()+'px';
    $("#eduhubNotification").css("width", contentWidth);
  }, 1000);
  topNavSpaceConf();
  var contentWidth = $("#page-content-wrapper").width()+'px';
  $("#eduhubNotification").css("width", contentWidth);
  var wv = $(window).width();
  if(wv<993){
    $('.show-sm').css("display","block");
    $('.show-lg').css("display","none");
  }
  else{
    $('.show-lg').css("display","block");
    $('.show-sm').css("display","none");      
  }
  if(wv>767 && IS_LOGGED){ 
    $('#notificationBell-lg').show();    
    $('#notificationBell-xs').remove();
  }
  else if(wv< 767 && IS_LOGGED){ 
    $('#notificationBell-xs').show();    
    $('#notificationBell-lg').remove();
  }
  if (!isSidebarPresent){
    contentWidth = $("#page-content-wrapper").width()+'px';
    $("#eduhubNotification").css("width", contentWidth);
    return;
  } 
  if(wv>767){ 
    // $("#sidebar-wrapper").show(); 
    // $('#sidebarmenu-toggle').hide();
    $('#page-content-wrapper').css("margin-left","60px");
  }
  else{ 
  //   $("#sidebar-wrapper").hide();
  //   $("#sidebarmenu-toggle").show();
    $('#page-content-wrapper').css("margin-left","0px");
  }
  contentWidth = $("#page-content-wrapper").width()+'px';
  $("#eduhubNotification").css("width", contentWidth);
};

widthConf();
$(window).resize(function(){
  widthConf();
});

function randomString(length) {
    var tmpLength = 0;
    tmpLength = length;
    if (length == null)tmpLength = 20;
    var str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  ;
    var result = '';
    for (var i = tmpLength; i > 0; --i) result += str[Math.floor(Math.random() * str.length)];
    return result;
}
var angularDependencies = ['yaru22.angular-timeago','ngCookies','ngImgCrop','ngAnimate','ngSanitize','ngRoute','vcRecaptcha','ngResource','ngTouch','ui.bootstrap','angular-intro','ngMessages','chart.js'];
// if(!DEBUG) angularDependencies.push('ngRaven');
var app = angular.module('eduhub',angularDependencies);
//constants
// const BUCKET_URL = "https://s3-"+S3_REGION_CODE+".amazonaws.com/" + MAIN_BUCKET + "/";
// const DEFAULT_AUDIO_THUMBNAIL = BUCKET_URL+ "constants/hub/audiofilethumbnail.png";
// const DEFAULT_NOTRACK_THUMBNAIL = BUCKET_URL + "constants/hub/nopreview.jpeg"
// const STATIC_FILE_ENDPOINT = "https://"+STATIC_BUCKET+".s3-"+S3_REGION_CODE+".amazonaws.com/";
// var sfJson = {};
///// TOP NAV CONSTANTS

const STOCK_PAGE = [['About', '/stocks/aboutmodel', 'About Model Parameters'],
                                          ['Predict', '/stocks/predict', 'Predict future!'], 
                                          ['Compare', '/stocks/compare', 'Compare Companies'],
                                          ['Hypothesis', '/stocks/hypothesis', 'Mathematical Hypothesis'],
                                          ['News', '/stocks/news', 'Market Sentiments']];

const REALESTATE_PAGE = [['About', '/realestate/aboutmodel', 'About Model Parameters'],
                                          ['Predict', '/realestate/predict', 'Predict future!'], 
                                          ['Compare', '/realestate/compare', 'Compare Companies'],
                                          ['Hypothesis', '/realestate/hypothesis', 'Mathematical Hypothesis'],
                                          ['News', '/realestate/news', 'Market Sentiments']];

const GOLD_PAGE = [['About', '/gold/aboutmodel', 'About Model Parameters'],
                                          ['Predict', '/gold/predict', 'Predict future!'], 
                                          ['Compare', '/gold/compare', 'Compare Companies'],
                                          ['Hypothesis', '/gold/hypothesis', 'Mathematical Hypothesis'],
                                          ['News', '/gold/news', 'Market Sentiments']];

const BANKING_PAGE = [[['About', '/banking/aboutmodel', 'About Model Parameters'],
                                          ['Predict', '/banking/predict', 'Predict future!'], 
                                          ['Compare', '/banking/compare', 'Compare Companies'],
                                          ['Hypothesis', '/banking/hypothesis', 'Mathematical Hypothesis'],
                                          ['News', '/banking/news', 'Market Sentiments']];
/////


function downloadURL(url,filename) {
  var a = document.createElement("a");
  document.body.appendChild(a);
  a.style = "display: none";
  a.href = url;
  //a.target = "_self";
  a.download = filename;
  a.click();
};

/*---------------------------------------------------------*/
app.controller('notificationController', ['$scope','$window',function($scope,$window){
  var opendd;
  $scope.awaitingNotifications = null;
  init();

  messaging.onMessage(function(payload) {
    $scope.$apply(function(){
      $scope.allNotifications.push(payload);
      $scope.awaitingNotifications++;
      updateLocalStorage();
    });
  });
 
  function init(){
    $scope.allNotifications = JSON.parse(localStorage.getItem('allNotifications'));
    $scope.awaitingNotifications = JSON.parse(localStorage.getItem('awaitingNotifications'));
    if($scope.allNotifications == null) $scope.allNotifications = [];
    if($scope.awaitingNotifications == null) $scope.awaitingNotifications = 0;
  }
    
  $scope.showNotifications = function($event){
    var targetdd = angular.element($event.target).closest('.dropdown-container').find('.dropdown-menu');
    opendd = targetdd;
    if(targetdd.hasClass('fadeInDown')) hidedd(targetdd);
    else{
      targetdd.css('display', 'block').removeClass('fadeOutUp').addClass('fadeInDown')
        .on('animationend webkitAnimationEnd oanimationend MSAnimationEnd', function(){
          angular.element(this).show();
        });
      targetdd.find('.dropdown-body')[0].scrollTop = 0;
    }
    $scope.awaitingNotifications = 0;
    updateLocalStorage();
  };

  function updateLocalStorage(){
    localStorage.setItem('allNotifications', JSON.stringify($scope.allNotifications));
    localStorage.setItem('awaitingNotifications', JSON.stringify($scope.awaitingNotifications)); 
  }
  
  $scope.clearAll = function(){
    $scope.allNotifications = [];
    $scope.awaitingNotifications = 0
    $scope.showBadge = false;
    updateLocalStorage();    
  }

  $scope.openNotification = function(idx){
    var nObj = $scope.allNotifications[idx];
    $scope.allNotifications.splice(idx,1);
    updateLocalStorage();
    $window.location.href = nObj.notification.click_action;
  };

  //Hide dropdown function
  var hidedd = function(targetdd){
    targetdd.removeClass('fadeInDown').addClass('fadeOutUp')
    .on('animationend webkitAnimationEnd oanimationend MSAnimationEnd', function(){
        angular.element(this).hide();
      });
    opendd = null;
  }

  window.onclick = function(event){
    var clickedElement = angular.element(event.target);
    var clickedDdTrigger = clickedElement.closest('.dd-trigger').length;
    var clickedDdContainer = clickedElement.closest('.dropdown-menu').length;
    if(opendd != null && clickedDdTrigger == 0 && clickedDdContainer == 0){
      hidedd(opendd);
    }
  }

}]);
/*-----------------------------------------------------------------------*/

app.factory('httpRequestInterceptor', ['$cookies','$injector','$q','$interval','$location',function ($cookies,$injector,$q,$interval,$location) {
  var nrefresh = 0;
  function timeRefresh(){
    var auth = $cookies.get("wauth");
    $.post("/api/v1/login/refreshauth/",
      {
        wauth: auth,
        force:true
      },
      function(data,status){
        if(data) if(data.wauth) $cookies.put("wauth",data.wauth);
    });  
  }
  $interval(timeRefresh,18000000);
  function retryHttpRequest(config, deferred){
    nrefresh += 1;
    function successCallback(response){
      nrefresh = 0;
      deferred.resolve(response);
    }
    function errorCallback(response){
      if (nrefresh > 10) {
        //timeout enough requests;
        $location.path('/login');
        deferred.reject(response);
      }
      else {
        retryHttpRequest(config,deferred);
      }
      
    }
    var $http = $injector.get('$http');
    $http(config).then(successCallback, errorCallback);
  }
  return {
    request: function (config) {
      if (config.load) ehLoad();
      var urlString = config.url ;
      //ignore if some other resource
      if (urlString.indexOf('http://') === 0 || urlString.indexOf('https://') === 0) return config;
      var auth = $cookies.get("wauth");
      if (auth) config.headers['Authorization'] = 'keyw='+auth;
      return config;  
    },
    response: function(response) {
      // do something on success
      if (response.config.load) ehDone();
      return response;
    },
    responseError: function(rejection) {
      // do something on error
      if (rejection.config.load) ehDone();//if the refresh code is executed then a new request with same config will be made
      if (rejection.status == 412){
        var deferred = $q.defer();
        var auth = $cookies.get("wauth");
        $.post("/api/v1/login/refreshauth/",
          {
            wauth: auth,
            force:false
          },
          function(data,status){
              if(data) if(data.wauth){
                $cookies.put("wauth",data.wauth);
                retryHttpRequest(rejection.config,deferred);
              }
        });  
        return deferred.promise;  
      }
      if (rejection.status == 401 && errorString(rejection) == "Token not found"){
        //if preconditon resolving lead to 401, redie
        $cookies.remove('wauth');
        $cookies.remove('udata');
        $location.search({});//no search params, code too complex cant keep track of page which made req
        $location.path('/login');
      }
      return $q.reject(rejection);
      }
  };
}]);

app.filter('trunc', function() {
  return function(str,len) {
    var final = null;
    if(str == null) return;
    if (str.length > len ){
      final = str.substring(0,len)+ "...";
      return final;
    }
    return str;
  };
});

function tUrl(path){//global function for template url
    return '/static/' + path;
}

app.service('navUpdateService',function(){
  var topNavObj = null;
  var sideNavObj = null;
  return {
    setTopNav: function(obj){ topNavObj = obj},
    // setSideNav: function(obj){ sideNavObj = obj},
    getTopNav: function(obj){ return topNavObj},
    // /getSideNav: function(obj){ return sideNavObj},
    highlightIndex: function(array,index){
      var arr = angular.copy(array);
      for (i = 0; i < arr.length; i++){
        if (i == index) arr[i].push(1);
        else arr[i].push(0);
      }
      return arr;
    },
    addOffset: function(array,offset){
      var arr = angular.copy(array);
      for (i=0 ; i< arr.length; i++) arr[i][1] += (offset + "/"); //1 index is the url element
      return arr;
    }
  }
});

app.controller('topNavController', ['$scope','navUpdateService','$location','$cookies','ehGlobals','$sce',function($scope,navUpdateService,$location,$cookies,ehGlobals,$sce){
  $scope.topNavList = null;
  var codingWindowSet = false;

  $scope.$watch(function(){return ehGlobals.loggedUser;},function(val){
    $scope.loggedUser = val;
  },true);

  $scope.$watch(function(){return navUpdateService.getTopNav();},function(topNavObj){
    if (topNavObj == null){
      hideTopBar();
    }
    else if (topNavObj.key == "SCHOOL_ADMIN"){
      var index =  topNavObj.index;
      $scope.topNavList = navUpdateService.highlightIndex(TN_SCHOOL_ADMIN,index);
      showTopBar();
    }
    else if (topNavObj.key == "NORMAL"){
      var index =  topNavObj.index;
      $scope.topNavList = navUpdateService.highlightIndex(TN_NORMAL,index);
      showTopBar();
    }
  },true);

  $scope.gotoMyHub = function(){
    $(".navbar-collapse").collapse('hide');
    $location.path('/hub/myhub/');
  }
  $scope.gotoSettings = function(){
    $(".navbar-collapse").collapse('hide');
    $location.path('/settings/basic/');
  }
  $scope.topBarClicked = function(val){
    $(".navbar-collapse").collapse('hide');
    $location.search({});
    $location.path(val);
  }
  
  $scope.logOutUser = function(){
    $(".navbar-collapse").collapse('hide');
    for (key in localStorage){
      if(key.indexOf("intro") == -1) localStorage.removeItem(key);
      //remove everything except for intro
    }
    $cookies.remove('wauth');
    $cookies.remove('udata');
    ehGlobals.set('loggedUser',null);
    deleteFIRToken();
    $location.path('/login');
  }
  function deleteFIRToken(){
    messaging.getToken()
    .then(function(currentToken){
      messaging.deleteToken(currentToken)
      .then(function() {
        })
        .catch(function(err) {
        });
        // [END delete_token]
      })
      .catch(function(err) {
    });
  }
}])

// app.controller('sideNavController', ['$scope','navUpdateService','ehGlobals','$sce','$timeout','ehIntroService', function($scope,navUpdateService,ehGlobals,$sce,$timeout,ehIntroService){
//   $scope.sideNavList = null;
//   $scope.introPresent = false;

//   $scope.$watch(function(){return ehGlobals.sidenavSpaceHtml;},function(val){
//     $scope.sidenavSpaceHtml = $sce.trustAsHtml(val);
//   },true);

//   $scope.$watch(function(){return ehIntroService.getPage();},function(val){
//     if(val) $scope.introPresent = true;
//     else $scope.introPresent = false;
//   })

//   $scope.$watch(function(){return navUpdateService.getSideNav();},function(sideNavObj){
//     if (sideNavObj == null){
//       hideSidebar();
//     }
//     else{
//       showSidebar();
//       if (sideNavObj.key == "SCHOOL_HOME"){
//         var index =  sideNavObj.index;
//         $scope.sideNavList = navUpdateService.highlightIndex(SN_SCHOOL_HOME,index);
//       }
//       else if (sideNavObj.key == "HUB"){
//         var index =  sideNavObj.index;
//         $scope.sideNavList = navUpdateService.highlightIndex(SN_HUB,index);
//       }
//       else if (sideNavObj.key == "MYHUB"){
//         var index =  sideNavObj.index;
//         var uid = ehGlobals.loggedUser.id;//will exist because its in myhub(satisfies routecheck)
//         var ls = navUpdateService.highlightIndex(SN_MYHUB,index);
//         ls[0][1] += uid+"/";
//         $scope.sideNavList = ls;
//       }
//       else if (sideNavObj.key == "SETTINGS"){
//         var index =  sideNavObj.index;
//         $scope.sideNavList = navUpdateService.highlightIndex(SN_SETTINGS,index);
//       }
//       else if (sideNavObj.key == "COURSE"){
//         var index =  sideNavObj.index;
//         if(sideNavObj.course_id){
//           $scope.sideNavList = navUpdateService.addOffset(navUpdateService.highlightIndex(SN_COURSE,index),sideNavObj.course_id);
//         }
//         else $scope.sideNavList = navUpdateService.highlightIndex(SN_COURSE,index);
//       }
//       updateIntroOptions();
//     }
//   },true);

//   function updateIntroOptions(){
//     var steps = [];
//     var sn = $scope.sideNavList;
//     if (sn == null) return;
//     for(i=0;i<sn.length; i++){
//       var snElem = sn[i];
//       var elemIdStr = "#sideNavElem"+i;
//       steps.push({element:elemIdStr,position:"right",intro:snElem[2]});
//     }
//     ehIntroService.addSteps(steps,1);//1 for sidebarSteps
//   }

//   $scope.helpPressed = function(){
//     ehIntroService.start(1);
//   }

// }])

app.config(['$httpProvider','$interpolateProvider','$sceDelegateProvider','$cookiesProvider','$routeProvider','$locationProvider','vcRecaptchaServiceProvider','$resourceProvider',function ($httpProvider,$interpolateProvider,$sceDelegateProvider,$cookiesProvider,$routeProvider,$locationProvider,vcRecaptchaServiceProvider,$resourceProvider){
  vcRecaptchaServiceProvider.setSiteKey(CAPTCHA_PUBLIC_KEY);
  // jwplayer.key= JW_LIC_KEY;
  $cookiesProvider.defaults.path = '/'; //not affecting the default object, had to manually set object
  $httpProvider.defaults.useXDomain = true;
  delete $httpProvider.defaults.headers.common['X-Requested-With'];
  $httpProvider.interceptors.push('httpRequestInterceptor');
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
  // const s3staticResourceUrl = STATIC_FILE_ENDPOINT + "**";
  // $sceDelegateProvider.resourceUrlWhitelist([
  //   'self',
  //   s3staticResourceUrl
  // ]); 

  $resourceProvider.defaults.actions = {
    create: {method: 'PUT'},
    get:    {method: 'GET'},
    getAll: {method: 'GET', isArray:true},
    update: {method: 'PATCH'},
    delete: {method: 'DELETE'}
  };
  $resourceProvider.defaults.stripTrailingSlashes = false;
  //routes: params used templateUrl,topnav,sidenav,login
  //login type: user (has to be logged in),type:school (has to be school user)

  var isLogged = ['ehGlobals','$location','$q','$timeout',function(ehGlobals,$location,$q,$timeout){
    var deferred = $q.defer();
    $timeout(function(){
      if (ehGlobals.loggedUser){
        deferred.resolve();
        return;
      }
      deferred.reject();
      var redirect = $location.url();
      $location.path('/login').search("redirect_url",redirect);
    });
    return deferred.promise;
  }];

  var isSchoolUser = ['ehGlobals','$location','$q','$timeout',function(ehGlobals,$location,$q,$timeout){
    var deferred = $q.defer();
    $timeout(function(){
      if (ehGlobals.loggedUser){
        if ([0,1,2].indexOf(ehGlobals.loggedUser.userType) == -1){
          deferred.reject();
          $location.path('/school/required/');
          return;
        }
        else{
          deferred.resolve();
          return;
        }
      }
      else{
        deferred.reject();
        var redirect = $location.url();
        $location.path('/login').search("redirect_url",redirect);
      }
    });
    return deferred.promise;
  }];

  var isSchoolAdmin = ['ehGlobals','$location','$q','$timeout',function(ehGlobals,$location,$q,$timeout){
    var deferred = $q.defer();
    $timeout(function(){
      if (ehGlobals.loggedUser){
        if (ehGlobals.loggedUser.userType == 2){
          deferred.resolve();
          return;
        }
        else{
          deferred.reject();
          $location.path('/school/admin/required/');
          return;
        }  
      }
      deferred.reject();
      var redirect = $location.url();
      $location.path('/login').search("redirect_url",redirect);
    });
    return deferred.promise;
  }];

  var homeResolver = ['ehGlobals','$location','$q','$timeout',function(ehGlobals,$location,$q,$timeout){
    var deferred = $q.defer();
    $location.search({});
    $timeout(function(){
      deferred.reject();//since nothing at /
      if (ehGlobals.loggedUser){
        if ([0,1,2].indexOf(ehGlobals.loggedUser.userType) != -1){
          $location.path('/school/home/');
        }
        else{
          $location.path('/hub/streams/');
        }
      }
      else{
        $location.path('/hub/streams/');
      }
    });
    return deferred.promise;
  }];
  
  $routeProvider
  .when("/login", {
    templateUrl: tUrl('login/templates/login.html'),
    topnav:null,
    sidenav:null
  })
  $routeProvider
  .when("/signup/", {
    templateUrl: tUrl('login/templates/signup.html'),
    topnav:null,
    sidenav:null
  })
  $routeProvider
  .when("/signup/:mode*\/", {
    templateUrl: tUrl('login/templates/signup.html'),
    topnav:null,
    sidenav:null
  })
  .when("/forgot/", {
    templateUrl: tUrl('login/templates/forgot.html'),
    topnav:null,
    sidenav:null
  })
  .when("/emailconfirm/", {
    templateUrl: tUrl('login/templates/emailconfirm.html'),
    topnav:null,
    sidenav:null
  })
  .when("/password/reset/", {
    templateUrl: tUrl('login/templates/resetpassword.html'),
    topnav:null,
    sidenav:null
  })
  .when("/docs/privacy/", {
    templateUrl: tUrl('general/templates/privacypolicy.html'),
    topnav:null,
    sidenav:null
  })
  .when("/demo/", {
    templateUrl: tUrl('school/templates/demo.html'),
    topnav:{key:"NORMAL",index:1},
    sidenav:null
  })

  //// HUB PAGES  ////
  $routeProvider
  .when("/", {
    resolve:{
      routeCheck: homeResolver
    }
  })
  $routeProvider
  .when("/hub/", {
    redirectTo: "/hub/streams/"
  })
  $routeProvider
  .when("/settings/basic/", {
    templateUrl : tUrl("general/templates/settingsbasic.html"),
    topnav: {key:"NORMAL",index:-1},
    sidenav: {key:"SETTINGS",index:0},
    resolve:{
      routeCheck:isLogged
    }
  })
  $routeProvider
  .when("/settings/security/", {
    templateUrl : tUrl("general/templates/settingssecurity.html"),
    topnav: {key:"NORMAL",index:-1},
    sidenav: {key:"SETTINGS",index:1},
    resolve:{
      routeCheck:isLogged
    }
  })
  $routeProvider
  .when("/settings/notification/", {
    template : "<hr class='marg0'><div style='margin:10px 10px;' class='alert alert-info'>Coming soon</div>",
    topnav: {key:"NORMAL",index:-1},
    sidenav: {key:"SETTINGS",index:2},
    resolve:{
      routeCheck:isLogged
    }
  })
  $routeProvider
  .when("/hub/streams/", {
    templateUrl : tUrl("hub/templates/streamhome.html"),
    topnav: {key:"NORMAL",index:0,space:"HUB_SEARCH"},
    sidenav: {key:"HUB",index:0}
  })
  .when("/hub/tracks/", {
    templateUrl : tUrl("hub/templates/trackhome.html"),
    topnav: {key:"NORMAL",index:0,space:"HUB_SEARCH"},
    sidenav: {key:"HUB",index:1},
  })
  .when("/hub/courses/", {
    templateUrl : tUrl("hub/templates/coursehome.html"),
    topnav: {key:"NORMAL",index:0,space:"HUB_SEARCH"},
    sidenav: {key:"HUB",index:2}
  })
  .when("/hub/stream/:stream_id/", {
    templateUrl : tUrl("hub/templates/playstream.html"),
    topnav: {key:"NORMAL",index:0,space:"HUB_SEARCH"},
    sidenav: {key:"HUB",index:0},
  })
  .when("/hub/track/:track_id/", {
    templateUrl : tUrl("hub/templates/playtrack.html"),
    topnav: {key:"NORMAL",index:0,space:"HUB_SEARCH"},
    sidenav: {key:"HUB",index:1},
  })
  .when("/hub/playlist/:playlist_id/", {
    templateUrl : tUrl("hub/templates/playlist.html"),
    topnav: {key:"NORMAL",index:0},
    sidenav: {key:"HUB",index:-1},
  })
  .when("/hub/search/", {
    templateUrl : tUrl("hub/templates/hubsearch.html"),
    topnav: {key:"NORMAL",index:0,space:"HUB_SEARCH"},
    sidenav: {key:"HUB",index:-1},
    reloadOnSearch:false
  })
  .when("/hub/myhub/", {
    templateUrl : tUrl("hub/templates/myhub.html"),
    topnav: {key:"NORMAL",index:0},
    sidenav: {key:"MYHUB",index:1},
    resolve:{
      routeCheck: isLogged
    }
  })
  .when("/hub/settings/", {
    template : "<hr class='marg0'><div style='margin:10px 10px;' class='alert alert-info'>Coming soon</div>",
    topnav: {key:"NORMAL",index:0},
    sidenav: {key:"MYHUB",index:2},
    resolve:{
      routeCheck: isLogged
    }
  })
  .when("/hub/user/:user_id/", {
    templateUrl : tUrl("hub/templates/user.html"),
    topnav: {key:"NORMAL",index:0},
    sidenav: {key:"MYHUB",index:0},
  })
  .when("/hub/user/", {
    templateUrl : tUrl("hub/templates/user.html"),
    topnav: {key:"NORMAL",index:0},
    sidenav: {key:"MYHUB",index:0},
  })
  .when("/hub/upload/", {
    templateUrl : tUrl("hub/templates/editUploadStream.html"),
    topnav: {key:"NORMAL",index:0},
    sidenav: null,
    resolve:{
      routeCheck:isLogged
    }
  })
  .when("/hub/edit/stream/:stream_id/", {
    templateUrl : tUrl("hub/templates/editUploadStream.html"),
    topnav: {key:"NORMAL",index:0},
    sidenav: null,
    resolve:{
      routeCheck:isLogged
    }
  })
  .when("/hub/edit/track/:track_id/", {
    templateUrl : tUrl("hub/templates/createEditTrack.html"),
    topnav: {key:"NORMAL",index:0},
    sidenav: null,
    resolve:{
      routeCheck:isLogged
    }
  })
  .when("/hub/create/track/", {
    templateUrl : tUrl("hub/templates/createEditTrack.html"),
    topnav: {key:"NORMAL",index:0},
    sidenav: null,
    resolve:{
      routeCheck:isLogged
    }
  })

  //////////
  .when("/school/required/", {
    templateUrl : tUrl("school/templates/schoolAccountRequired.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: null,
  })
  $routeProvider
  .when("/school/admin/required/", {
    templateUrl: tUrl('school/templates/reqadmin.html'),
    topnav:{key:"NORMAL",index:-1},
    sidenav:null
  })
  /////// SCHOOL ADMIN PAGES /////

  $routeProvider
  .when("/school/admin/home/", {
    templateUrl : tUrl("school/templates/admin/adminCollege.html"),
    topnav: {key:"SCHOOL_ADMIN",index:0},
    sidenav: null,
    resolve:{
      routeCheck:isSchoolAdmin
    }
  })
  .when("/school/admin/departments/", {
    templateUrl : tUrl("school/templates/admin/adminDepartments.html"),
    topnav: {key:"SCHOOL_ADMIN",index:1},
    sidenav: null,
    resolve:{
      routeCheck:isSchoolAdmin
    }
  })
  .when("/school/admin/faculty/", {
    templateUrl : tUrl("school/templates/admin/adminFaculty.html"),
    topnav: {key:"SCHOOL_ADMIN",index:2},
    sidenav: null,
    resolve:{
      routeCheck:isSchoolAdmin
    }
  })
  .when("/school/admin/courses/", {
    templateUrl : tUrl("school/templates/admin/adminCourses.html"),
    topnav: {key:"SCHOOL_ADMIN",index:3},
    sidenav: null,
    resolve:{
      routeCheck:isSchoolAdmin
    }
  })
  .when("/school/admin/students/", {
    templateUrl : tUrl("school/templates/admin/adminStudents.html"),
    topnav: {key:"SCHOOL_ADMIN",index:4},
    sidenav: null,
    resolve:{
      routeCheck:isSchoolAdmin
    }
  })
  .when("/school/admin/timetable/", {
    templateUrl : tUrl("school/templates/admin/adminTimetable.html"),
    topnav: {key:"SCHOOL_ADMIN",index:5},
    sidenav: null,
    resolve:{
      routeCheck:isSchoolAdmin
    }
  })
  .when("/school/admin/grades/", {
    templateUrl : tUrl("school/templates/admin/adminGrades.html"),
    topnav: {key:"SCHOOL_ADMIN",index:6},
    sidenav: null,
    resolve:{
      routeCheck:isSchoolAdmin
    }
  })
  ////

  /// SCHOOL PAGES ////
  $routeProvider
  .when("/school/", {
    redirectTo: '/school/home/'
  })
  $routeProvider
  .when("/school/home/", {
    templateUrl : tUrl("school/templates/schoolHome.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"SCHOOL_HOME",index:0},
    resolve:{
      routeCheck: isSchoolUser
    }
  })
  .when("/school/mycourses/", {
    templateUrl : tUrl("school/templates/myCourses.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"SCHOOL_HOME",index:1},
    resolve:{
      routeCheck: isSchoolUser
    }
  })
  .when("/school/allcourses/", {
    templateUrl : tUrl("school/templates/allCourses.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"SCHOOL_HOME",index:1},
    resolve:{
      routeCheck: isSchoolUser
    }
  })
  .when("/school/chats/", {
    templateUrl : tUrl("school/templates/chats.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"SCHOOL_HOME",index:2},
    resolve:{
      routeCheck: isSchoolUser
    }
  })
  .when("/school/events/", {
    templateUrl : tUrl("school/templates/events.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"SCHOOL_HOME",index:3},
    resolve:{
      routeCheck: isSchoolUser
    }
  })
  .when("/school/stories/", {
    templateUrl : tUrl("school/templates/stories.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"SCHOOL_HOME",index:4},
    resolve:{
      routeCheck: isSchoolUser
    }
  })
  .when("/school/events/create/", {
    templateUrl : tUrl("school/templates/createEditEvent.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: null,
    resolve:{
      routeCheck: isSchoolUser
    }
  })
  .when("/school/events/edit/:event_id/", {
    templateUrl : tUrl("school/templates/createEditEvent.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: null,
    resolve:{
      routeCheck: isSchoolUser
    }
  })

  //// SCHOOL COURSE PAGES ///

  .when("/school/course/:course_id/", {//course landing page
    templateUrl : tUrl("school/templates/courseLandingPage.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"SCHOOL_HOME",index:1},
    resolve: {
      routeCheck: isSchoolUser
    }
  })

  .when("/school/course/content/:course_id/", {
    templateUrl : tUrl("school/templates/courseContent.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"COURSE",index:0},
    resolve:{
      check: isSchoolUser
    }
  })
  .when("/school/course/grades/:course_id/", {
    templateUrl : tUrl("school/templates/courseGrades.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"COURSE",index:1},
    resolve:{
      check: isSchoolUser
    }
  })
  .when("/school/course/info/:course_id/", {
    templateUrl : tUrl("school/templates/courseInfo.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"COURSE",index:2},
    resolve:{
      check: isSchoolUser
    }
  })
  .when("/school/course/settings/:course_id/", {
    templateUrl : tUrl("school/templates/courseSettings.html"),
    topnav: {key:"NORMAL",index:1},
    sidenav: {key:"COURSE",index:3},
    resolve:{
      check: isSchoolUser
    }
  })

  /////

  //////
  $routeProvider.otherwise({
    templateUrl: tUrl('general/templates/404.html'),
    topnav: null,
    sidenav:null
  })

  $locationProvider.html5Mode(true);
}]);

app.run(['$http','$cookies','$rootScope','navUpdateService','ehGlobals','s3service','ehIntroService','$location',function($http,$cookies,$rootScope,navUpdateService,ehGlobals,s3service,ehIntroService,$location){
  //add user object to rootscope
  ehGlobals.set('sidenavSpaceHtml',"");
  ehGlobals.set("loggedUser",$cookies.getObject("udata"));

  $rootScope.tUrl = function(path){
    return tUrl(path);
  }

  $rootScope.openHubCourse=function(c){
    $http.get('/api/v1/hub/viewsupdate/?type=c&id='+c.id,{load:true}).then(function successCallback(response) {
      viewtoken = response.data.token;
    }, function errorCallback(response){}).finally(function(){
      $http.post('/api/v1/hub/viewsupdate/',{type:"c",id:c.id,token:viewtoken}).then(function successCallback(response) {
      }, function errorCallback(response){}).finally(function(){
        window.location.href = c.url;
      });
    });
  }

  $rootScope.gotoLogin = function(){
    var redirect = $location.url();
    $location.path('/login').search("redirect_url",redirect); 
  }

  $rootScope.openSchoolCourse=function(c){
    $http.get('/api/v1/school/course/?type=checkReg&id='+c.id).then(function successCallback(response){
      if(response.data.isRegistered){
        $location.path('/school/course/content/'+c.id+"/");
      }
      else{
        $location.path('/school/course/'+c.id+"/");
      }
    },function errorCallback(response){
      notificationSetup.show(errorString(response),5,'d');
    })
  }
  
  $rootScope.$on('$routeChangeStart', function (event, next, prev) {
    $('#page-content-wrapper').show();
    $('#eduhubNotification').hide();
    ehGlobals.set('sidenavSpaceHtml',"");
    $('#mainErrDiv').hide();
    s3service.resetCredentials();
    ehIntroService.reset();
  });

  $rootScope.$on('$routeChangeSuccess', function (event, next, prev) {
    NProgress.done();
    if(next){
      var route = next.$$route;
      var params = next.params;
      if (route){
        navUpdateService.setTopNav(route.topnav);
        navUpdateService.setSideNav(route.sidenav);
        //check for course urls

        if (route.sidenav){
          var s = route.sidenav;
          showSidebar();
          if(s.key == "COURSE"){
            s.course_id = params.course_id;
            navUpdateService.setSideNav(s);
          }
        }

        //configure top nav space div
        if (route.topnav){
          var spaceMode = route.topnav.space;
          if (spaceMode == "HUB_SEARCH"){
            $rootScope.topNavSpaceUrl = tUrl('hub/templates/searchbarTemplate.html');
            $rootScope.topContentSpaceUrl = tUrl('hub/templates/searchbarTemplate.html');
          }
          else{
            $rootScope.topNavSpaceUrl = '';
            $rootScope.topContentSpaceUrl = '';
          }
        }
        else{
          $rootScope.topNavSpaceUrl = '';
          $rootScope.topContentSpaceUrl = '';
        }
      }
      else{//404
        navUpdateService.setTopNav({key:"NORMAL",index:-1});
        navUpdateService.setSideNav(null);
      }
    }
  });

  $rootScope.$on('$routeChangeError',function(event,next,prev){
    //all resolve rejects come here
  })

  //for jquery file upload
  $.ajaxSetup({
    beforeSend: function (xhr)
    {
      var auth = $cookies.get("wauth");
      var authHeader = 'keyw='+auth ;
      if (auth) xhr.setRequestHeader("Authorization",authHeader);  
    }
  });
}]);

app.service('loginPopUpSetup',function(){
  return {
    show: function(msg){
      var text = msg;
      if (msg == null)text = "You need to log in to perform this action";
      $('#loginpopuptext').html(msg);
      $('#loginPopUp').modal("show");
    }
  }
});

app.filter('trunc', function() {
  return function(str,len) {
    var final = null;
    if(str == null) return;
    if (str.length > len ){
      final = str.substring(0,len)+ "...";
      return final;
    }
    return str;
  };
});

var prevSecs = 0;
var prevDuration = 0;
app.service('notificationSetup',function(){
  var html = null, duration = null, type = null;
  return {
    show: function(html, duration, type){//type = S uccess, I nfo, W arning, D anger
      var cl = null,cla=null;
      $('#notificationIcon').removeClass("fa-exclamation-triangle fa-check-circle-o fa-info-circle fa-exclamation");
      if (type == 's'){
        cl = "#82e0aa";
        cla = "fa-check-circle-o";
      }
      else if (type == 'i'){
        cl = "#a3e4d7";
        cla = "fa-info-circle";
      }
      else if (type == 'w'){
        cl = "#f7dc6f";
        cla = "fa-exclamation-triangle";
      }
      else if (type == 'd'){
        cl = "#FF9494";
        cla = "fa-exclamation";
      }
      else return;
      $('#notificationIcon').addClass(cla);
      var secs = Math.floor(new Date().getTime() / 1000);
      if(secs - prevSecs < prevDuration)//still showing alert
      {
        $('#notificationBody').html(html);
        $('#eduhubNotification').css("background-color", cl);
        return; 
      }
      $('#notificationBody').html(html);
      $('#eduhubNotification').css("background-color", cl);
      $('#eduhubNotification').fadeIn(500);
      $('#eduhubNotification').delay(duration*1000).fadeOut(500);
      prevSecs = Math.floor(new Date().getTime() / 1000);
      prevDuration = duration;   
    }, 
    getType : function(){
      return type;
    }
  }
});

app.directive('onButtonClick',['$location',function ( $location ) {
  return function ( scope, element, attrs ) {
    var path;
    
    attrs.$observe( 'onButtonClick', function (val) {
      path = val;
    });
    
    element.bind( 'click', function () {
      scope.$apply( function () {
        $location.search({});
        $location.path(path);
      });
    });
  };
}]);

function errorString(response){
  var str = "An error occurred";
  if (response.status == -1) return "Could not connect to server. Please check your internet connection.";
  try{
    var readable = response.data.error.readable;
    if (readable){
     str = readable;
     return str;
    }
  }
  catch(e){
  }
  return str;
}

function errHandler(response) {
  var code = response.status;
  if (code == 404){
    $('#mainErrDiv').html("Oops! Page not found.");
    $('#mainErrDiv').show();
    $('#page-content-wrapper').hide();
    hideSidebar();
  }
  else if(code == 406){
    $('#mainErrDiv').html("Oops! Something went wrong.");
    $('#mainErrDiv').show();
    $('#page-content-wrapper').hide();
    hideSidebar();
  }
  else if (code == 401){
    $('#mainErrDiv').html("Unauthorized! You are not authorized to view to this page.");
    $('#mainErrDiv').show();
    $('#page-content-wrapper').hide();
    hideSidebar();
  }
  else if (code == 403){
    $('#mainErrDiv').html("Forbidden! You are not authorized to view to this page.");
    $('#mainErrDiv').show();
    $('#page-content-wrapper').hide();
    hideSidebar();
  }
  else if (code == -1){
    $('#mainErrDiv').html("Server not reachable! Please check your internet connection.");
    $('#mainErrDiv').show();
    $('#page-content-wrapper').hide();
    hideSidebar();
  }
}

function urlify(text) {
  var urlRegex = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
  return text.replace(urlRegex, function(url) {
      return '<a href="' + url + '">' + url + '</a>';
  })
}
var loadCount = 0;
var minLoadAnimate = 50;//makes sure that the timeout is called after this many ms, this interval is sufficient for next request to be made, which is only triggered when the first one gets completed
function ehLoad(){
  if (loadCount == 0) NProgress.start();
  loadCount += 1;
};

function ehDone(){
  loadCount -= 1;
  if (loadCount == 0) setTimeout(ehLoadTimeout, minLoadAnimate);
}

function ehLoadSet(val){//progress in %
  if (val != 100) NProgress.set(val/100);
  else NProgress.done();
}

function ehLoadTimeout(){
  if (loadCount == 0) NProgress.done();
}
//bootstrap dropdowns won't dismiss on click
$(document).on('click', '.eh-dropdown.dropdown-menu', function (e) {
  e.stopPropagation();
});
///


///////// DIRECTIVES /////////

//// GENERAL ////

app.directive('ehfile', function() {
  return {
    restrict: 'E',
    template: '<input type="file" />',
    replace: true,
    require: 'ngModel',
    link: function(scope, element, attr, ctrl) {
      var listener = function() {
        scope.$apply(function() {
          attr.multiple ? ctrl.$setViewValue(element[0].files) : ctrl.$setViewValue(element[0].files[0]);
        });
      }
      element.bind('change', listener);
    }
  }
});

app.factory('ehGlobals', [function(){
  var data = {
    loggedUser: null,
    isStudent:false,
    isFaculty:false,
    isSchoolAdmin:false,
    isSchoolUser:false,
    sidenavSpaceHtml:'',
    topNavSpaceUrl:''
  };
  data.set = function(key,val){
    this[key] = val;
    if(key == 'loggedUser'){
      if(val){
        IS_LOGGED = true;
        requestPermission();
        var newconf = {is:false,if:false,isa:false,isu:false};
        switch(val.userType){
          case 0:
            newconf.isu = true
            newconf.is = true
            break;
          case 1:
            newconf.isu = true
            newconf.if = true
            break;
          case 2:
            newconf.isu = true
            newconf.isa = true
            break;
          default:
            break;
        }
        this.isStudent = newconf.is;
        this.isFaculty = newconf.if;
        this.isSchoolAdmin = newconf.isa;
        this.isSchoolUser = newconf.isu;
      }
      else{
        this.isStudent = false;
        this.isFaculty = false;
        this.isSchoolAdmin = false;
        this.isSchoolUser = false;
        IS_LOGGED = false;
        $('#notificationBell-lg').hide();
        $('#notificationBell-xs').hide();
      }
    }
  }
  data.get = function(key){
    return this.key
  }
  return data;
}])

app.directive('ehUserBlock', [function(){
  return {
    controller:'userInfoController',
    scope: {
      user:"<"
    },
    restrict: 'E',
    templateUrl: tUrl('general/templates/userInfoTemplate.html'),
  };
}]);

app.directive('ehDiscussionBlock', [function(){
  return {
    controller:'discussionController',
    scope: {
      setup:"<"
    },
    restrict: 'E',
    templateUrl: tUrl('chats/templates/discussionTemplate.html'),
  };
}]);

app.directive('ehChatBlock', [function(){
  return {
    controller:'chatController',
    scope: {
      id:"<"
    },
    restrict: 'E',
    templateUrl: tUrl('chats/templates/chatTemplate.html')
  };
}]);

app.directive('ehNoteBlock', [function(){
  return {
    controller:'privateNoteController',
    scope: {
      forObj:"<",
      itemId:"<"
    },
    restrict: 'E',
    templateUrl: tUrl('admin/templates/privateNoteViewer.html')
  };
}]);

app.directive('ehFileViewer', ['jwPlayerService',function(jwPlayerService){
  function link($scope, element, attrs){
    const imgExtensions = ['png','jpeg','jpg'];
    const mediaExtensions = ['mp3','mp4','mov','avi','flv','wmv'];
    var wasMedia = false;
    $scope.$watch('url', function(val) {
      resetView();
      if(val){
        viewFile(val);
      }
    });
    function viewFile(url){
      if(!url){
        resetView();
        return;
      }
      var ext = url.split(".").pop();
      if (!ext){
        resetView();
        return;
      }

      ext = ext.toLowerCase();
      if (ext.indexOf('?') != -1){//remove get params
        ext = ext.substring(0,ext.indexOf('?'));
      }
      if (imgExtensions.indexOf(ext) != -1){
        var height = null;
        if(window.innerHeight>700) height = window.innerHeight-300;
        else height = window.innerHeight-200;
        var htmlStr = "<img width='100%' height='"+height+"' src='"+url+ "' />";
        element.html(htmlStr);
        return;
      }
      else if (mediaExtensions.indexOf(ext) != -1){
        //use jwplayer service
        wasMedia = true;
        const newId = randomString(10);
        var htmlStr = "<div id='"+newId+"'></div>";
        element.html(htmlStr);
        jwPlayerService.setup(newId,[{title:"",sources:[{file:url}]}]);
      }
      else{
        gdocsViewer(url);
      }
      
    }

    function gdocsViewer(url){
      var htmlStr = '';
      var iframeId = randomString(10);
      var height = null;
      ehLoad();
      if(window.innerHeight>700) height = window.innerHeight-300;
      else height = window.innerHeight-200;
      htmlStr = "<iframe width='100%' id='"+iframeId+"' style='background-color:#f2f2f2;' frameborder='0' height='"+height+"' ></iframe>";
      element.html(htmlStr);
      $('#'+iframeId).load(function(){
        ehDone();
      })
      const gdocsString = 'https://docs.google.com/viewer?embedded=true&url=';
      var finalUrl = gdocsString + encodeURIComponent(url);
      $('#'+iframeId).attr('src',finalUrl);
    }

    function pdfViewer(url){
      var canvasId = randomString(10);
      var prevBtnId = randomString(10);
      var nextBtnId = randomString(10);
      var pageNumId = randomString(10);
      var pageCountId = randomString(10);
      element.html("<div><button id='"+prevBtnId+"'>Previous</button><button id='"+nextBtnId+"'>Next</button>&nbsp; &nbsp;<span>Page: <span id='"+pageNumId+"'></span> / <span id='"+pageCountId+"'></span></span></div><canvas id='"+canvasId+"'></canvas>");
      var pdfDoc = null,
          pageNum = 1,
          pageRendering = false,
          pageNumPending = null,
          scale = 1,
          canvas = document.getElementById(canvasId),
          ctx = canvas.getContext('2d');

      /**
       * Get page info from document, resize canvas accordingly, and render page.
       * @param num Page number.
       */
      function renderPage(num) {
        pageRendering = true;
        // Using promise to fetch the page
        pdfDoc.getPage(num).then(function(page) {
          var viewport = page.getViewport(scale);
          canvas.height = viewport.height;
          canvas.width = viewport.width;
          // Render PDF page into canvas context
          var renderContext = {
            canvasContext: ctx,
            viewport: viewport
          };
          var renderTask = page.render(renderContext);

          // Wait for rendering to finish
          renderTask.promise.then(function() {
            pageRendering = false;
            if (pageNumPending !== null) {
              // New page rendering is pending
              renderPage(pageNumPending);
              pageNumPending = null;
            }
          });
        });

        // Update page counters
        document.getElementById(pageNumId).textContent = pageNum;
      }

      /**
       * If another page rendering in progress, waits until the rendering is
       * finised. Otherwise, executes rendering immediately.
       */
      function queueRenderPage(num) {
        if (pageRendering) {
          pageNumPending = num;
        } else {
          renderPage(num);
        }
      }

      /**
       * Displays previous page.
       */
      function onPrevPage() {
        if (pageNum <= 1) {
          return;
        }
        pageNum--;
        queueRenderPage(pageNum);
      }

      document.getElementById(prevBtnId).addEventListener('click', onPrevPage);

      /**
       * Displays next page.
       */
      function onNextPage() {
        if (pageNum >= pdfDoc.numPages) {
          return;
        }
        pageNum++;
        queueRenderPage(pageNum);
      }
      document.getElementById(nextBtnId).addEventListener('click', onNextPage);

      /**
       * Asynchronously downloads PDF.
       */
      PDFJS.getDocument(url).then(function(pdfDoc_) {
        pdfDoc = pdfDoc_;
        document.getElementById(pageCountId).textContent = pdfDoc.numPages;

        // Initial/first page rendering
        renderPage(pageNum);
      });
    }

    function resetView(){
      if (wasMedia) jwplayer().remove();
      element.html('');
      wasMedia = false;
    }

  }
  return {
    link: link,
    scope:{
      url: "<"
    },
    restrict:'E'
  };
}]);

angular.module('eduhub').factory('focus', ['$timeout','$window',function($timeout, $window) {
  return function(id) {
    // timeout makes sure that it is invoked after any other event has been triggered.
    // e.g. click events that need to run before the focus or
    // inputs elements that are in a disabled state but are enabled when those events
    // are triggered.
    $timeout(function() {
      var element = $window.document.getElementById(id);
      if(element)
        element.focus();
    }); 
  };
}]);

function sendTokenToServer(token){
  if (isTokenSentToServer()) return; //already sent
  /*
  $http.post("/api/v1/admin/user/",{type:"firebase",firTokenW:token}).then(function successCallback(response){
    setTokenSentToServer(true);
  },function errorCallback(response){
  })
  */
  if (!IS_LOGGED) return;
  $.ajax({
    type: "POST",
    url: "/api/v1/admin/user/",
    data: {type:"firebase",firTokenW:token},
    success: function(data){setTokenSentToServer(true);},
    dataType: "json"
  });
}

function setTokenSentToServer(sent) {
  if (sent) {
    window.localStorage.setItem('sentToServer', 1);
  } else {
    window.localStorage.setItem('sentToServer', 0);
  }
}

function isTokenSentToServer() {
  if (window.localStorage.getItem('sentToServer') == 1) {
        return true;
  }
  return false;
}

function requestPermission(){
  messaging.requestPermission()
  .then(function() {
   messaging.getToken()
    .then(function(currentToken) {
      if (currentToken) {
        sendTokenToServer(currentToken);
        //updateUIForPushEnabled(currentToken);
      } else {
        // Show permission request.
        console.log('No Instance ID token available. Request permission to generate one.');
        // Show permission UI.
        //updateUIForPushPermissionRequired();
        setTokenSentToServer(false);
      }
    })
    .catch(function(err) {
      console.log('An error occurred while retrieving token. ', err);
      //showToken('Error retrieving Instance ID token. ', err);
      setTokenSentToServer(false);
    });
  })
  .catch(function(err) {
    console.log('Unable to get permission to notify.', err);
  });
}

function registerServiceWorker(){
  if ('serviceWorker' in navigator){
    var sw_url = '/static/eduhub-sw.js';
    if (DEBUG) sw_url = '/static/eduhubdebug-sw.js';
    navigator.serviceWorker.register(sw_url, {scope: '/static/'})
    .then(function(reg) {
      messaging.useServiceWorker(reg);
      requestPermission();
      messaging.onTokenRefresh(function() {
        messaging.getToken()
        .then(function(refreshedToken){
          // Indicate that the new Instance ID token has not yet been sent to the
          // app server.
          setTokenSentToServer(false);
          // Send Instance ID token to app server.
          sendTokenToServer(refreshedToken);
          // ...
        })
        .catch(function(err) {
          console.log('Unable to retrieve refreshed token ', err);
          showToken('Unable to retrieve refreshed token ', err);
        });
      });
    }).catch(function(error) {
      // registration failed
      console.log('Registration failed with ' + error);
    });
  }
}

registerServiceWorker();

////// http resources

app.factory('schoolCourseResource', ['$resource', function($resource){
  return $resource('/api/v1/school/course/',{id:'@id'},{
    'getInfo':{method:'get',params:{type:'info'}},
    'getContent':{method:'get',params:{type:'content'}},
    'myCourses':{method:'get',params:{type:'m'}},
    'allCourses':{method:'get',params:{type:'a'}}
  });
}])

app.factory('privateNoteResource', ['$resource', function($resource){
  return $resource('/api/v1/admin/note/:noteId/',{},{
    'get':{url:'api/v1/admin/note/:forObj/:itemId/',method:'get',params:{forObj:'@forObj',itemId:'@itemId'}},
    'edit':{method:'patch',params:{noteId:'@noteId'}},
    'delete':{method:'delete',params:{noteId:'@noteId'}},
    'create':{method:'put'}
  });
}])

//////

////emoji load
/*
var EMOJI_JSON = {};
$.ajax({
  dataType: "json",
  url: tUrl('general/emoji.json'),
  success: function(json){
    EMOJI_JSON = json;
  }
})
app.controller('emojiController', ['$scope', function($scope){
  $scope.emojis = EMOJI_JSON;
}])
*/