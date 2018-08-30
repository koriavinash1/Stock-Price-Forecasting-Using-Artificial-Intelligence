from django.conf.urls import url
from django.contrib import admin
from stock_backend.apis import updateDatabaseHistory, updateDatabaseCurrent, \
                                 updateModelPredictions, trainModel, updateNews, updateTweets,\
                                 actualVspred, predict, compare, getCompanyList
from stock_backend.views import stocksPage, stocksAdminPage
from banking.views import aboutModelBanking, predictBanking, compareBanking, \
                                    hypothesisBanking, newsBanking
from realestate.views import aboutModelRealestate, predictRealestate, compareRealestate, \
                                    hypothesisRealestate, newsRealestate, realestatePage
from login.views import indexPage, loginPage
from gold_prediction.apis import updateGoldDB, trainGoldModel
from gold_prediction.views import goldPage
from banking.apis import updateBankDB
from realestate.apis import  trainRealestateModel, updateRealestateDB
from login.apis import predictPath, getDetails


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', indexPage),
    url(r'^stocks/', stocksPage),
    url(r'^gold/', goldPage),
    url(r'^realestate/', realestatePage),
    url(r'^stocksadmin/', stocksAdminPage),
    url(r'^login/', loginPage),
]

urlpatterns +=[
    url(r'^api/v1/index/pathpredict/$', predictPath),
    url(r'^api/v1/index/details/$', getDetails),
]

urlpatterns +=[
    url(r'^api/v1/stocks/updatedb/$', updateDatabaseHistory),
    url(r'^api/v1/stocks/updatemodel/$', updateModelPredictions),
    url(r'^api/v1/stocks/trainmodel/$', trainModel),
    url(r'^api/v1/stocks/updatenews/$', updateNews),
    url(r'^api/v1/stocks/updatetweets/$', updateTweets),
    url(r'^api/v1/stocks/actualvspred/$', actualVspred),
    url(r'^api/v1/stocks/predict/$', predict),
    url(r'^api/v1/stocks/compare/$', compare),
    url(r'^api/v1/stocks/getCompanyList/$', getCompanyList),
]

urlpatterns+=[
    url(r'^api/v1/gold/updatedb/$',updateGoldDB),
    # url(r'^api/v1/gold/updatedb/$',updateGoldModel),
    url(r'^api/v1/gold/trainmodel/$', trainGoldModel),
    # url(r'^api/v1/gold/updatedb/$', updateGoldTweets),
    # url(r'^api/v1/gold/updatedb/$', updateGoldNews),
    # url(r'^api/v1/gold/updatedb/$', Goldactualvspred),
    # url(r'^api/v1/gold/updatedb/$', predict),
]

urlpatterns+=[
    url(r'^api/v1/bank/updatedb/$', updateBankDB),
]

urlpatterns +=[
    url(r'^api/v1/realestate/train/$', trainRealestateModel),
    url(r'^api/v1/realestate/updateDB/$', updateRealestateDB)
]