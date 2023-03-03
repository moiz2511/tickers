from django.urls import path

from . import views
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# urlpatterns = [
#     path("", views.index, name="index"),
#     path("following/<int:profile_id>", views.following, name="following"),
#     path("login", views.login_view, name="login"),
#     path("login", views.login_view, name="login"),
#     path("logout", views.logout_view, name="logout"),
#     path("register", views.register, name="register"),
#     path('open_tweet/<int:tweet_id>',views.open_tweet,name="open_tweet"),
#     path('profile/<int:user_id>',views.profile,name="profile"),

#     path('deletetweet/<int:tweet_id>',views.deletetweet,name="deletetweet"),
#     #API Routes
#     path("tweets",views.compose,name="compose"),
#     path("feed/<int:profile_id>",views.feed,name="feed"),
#     path("like/<int:tweet_id>",views.like,name="like"),
#     path("follow/<int:user_id>",views.follow,name="follow"),
#     path("tweetdetails/<int:tweet_id>",views.tweetdetails,name="tweetdetails"),
#     path("editsave/<int:tweet_id>",views.editsave,name="editsave"),


#     path("post/<int:tweet_id>",views.comment_post,name="comment_post"),

#     path("deletecomment/<int:comment_id>",views.deletecomment,name="deletecomment"),
#     path("comments/<int:tweet_id>",views.comments,name="comments")

# ]

urlpatterns = [

    path('token', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register', views.registerUser, name='register'),
    path('user/profile', views.getUserProfile, name="users-profile"),
    path('user/profile/update', views.updateUserProfile, name="user-profile-update"),
    path('user/password/update', ChangePasswordView.as_view(), name="update-user-password"),
    path('users', views.getUsers, name="users"),
    path('users/<str:pk>/get', views.getUserById, name='user'),
#     path('users/<str:pk>/delete', views.deleteUser, name='user-delete'),
    path('users/<str:pk>/update', views.updateUser, name='user-admin-update'),
    path('forgotpassword/link', views.forgotPassword, name="forgot-password-link"),
    path('resetpassword', views.forgotPasswordValidateAndReset, name='reset-password'),
    
    path('contactpage', views.contactMailInfo, name='contactpage-create'),
    path('contactpage/get', views.getContactMailInfo, name='contactpage-get'),
    path('contactpage/update', views.updateContactMailInfo, name='contactpage-update'),


#     path("", views.index, name="index"),
#     path("context/investing_styles",
#          views.investingStyle, name="investing_styles"),
#     path("context/analysis_model", views.analysisModel, name="analysis_model"),
#     path("context/screen_model", views.screenModel, name="screen_model"),
#     path("data-analysis", views.data_analysis, name="data_analysis"),
#     path("data-processing", views.data_processing, name="data_processing"),
#     path("dp_investing_styles",
#          views.dpInvestingStyle, name="dp_investing_styles"),
#     path("strategies/", views.strategies, name="strategies"),
    path("suggest/<str:keyword>", views.suggest, name="suggest"),
    path("suggest_super/<str:keyword>",
         views.suggest_super, name="suggest_super"),
    path(
        "suggest_category/<str:keyword>",
        views.suggest_category,
        name="suggest_category",
    ),
    path(
        "asuggest_metrics/<str:keyword>", views.suggest_metrics, name="suggest_metrics"
    ),
    path("suggest_ranges/<str:keyword>",
         views.suggest_ranges, name="suggest_ranges"),
#     path("results", views.results, name="results"),
#     path("upload_results", views.upload_results, name="upload_results"),
#     path("lregression", views.lregression, name="lregression"),
#     path("create-metrics/", views.create_metrics, name="create_metrics"),
#     path("financials", views.financials, name="financials"),
#     path("reported-financials", views.reported_financials,
#          name="reported_financials"),
#     path("profile-group", views.profile_group, name="profile_group"),
#     path("keymetrics-group", views.keymetrics_group, name="keymetrics_group"),
#     path("rate-group", views.rate_group, name="rate_group"),
#     path("financial-notes", views.financial_notes, name="financial_notes"),
#     path("ranges", views.ranges, name="ranges"),
#     path("ranges_dp/", views.ranges_dp, name="ranges_dp"),
#     path("model_dp/", views.model_dp, name="model_dp"),
#     path("aggragate_fiancials/", views.aggragate_fiancials,
#          name="aggragate_fiancials"),
#     path("advancedRatios/", views.advancedRatios, name="advancedRatios"),
#     path("market-data", views.market_data, name="market_data"),
    # screen 3
    path("strategy", StrategyView.as_view()),
    path("deletestrategy", DeleteStrategyView.as_view()),
    path("editstrategy", EditStrategyView.as_view()),
    path("getstrategy", GetStrategyView.as_view()),
    path("getScreenModels", GetStrategyView.as_view()),
    path("context/getScreenModels", GetScreenModelView.as_view()),
    # screen 4
    path("metric", MetricView.as_view()),
    path("deletemetric", DeleteMetricView.as_view()),
    path("editmetric", EditMetricView.as_view()),
    path("getmetric", GetMetricView.as_view()),
    # screen 5
    path("model", ModelView.as_view()),
    path("deletemodel", DeleteModelView.as_view()),
    path("editmodel", EditModelView.as_view()),
    path("getmodel", GetModelView.as_view()),
    # screen 8
    path("getdrop", GetDropView.as_view()),
    path("advanceratio", AdvanceratioView.as_view()),
    path("editadvanceratio", EditAdvanceratioView.as_view()),
    path("deleteadvanceratio", DeleteAdvanceratioView.as_view()),
    path("getadvanceratio", GetadvanceratiodataView.as_view()),
    # screen 6
    path("aggregateview", AggregateView.as_view()),
    path("aggregatedrop", AggregateDropView.as_view()),
    path("deleteaggregateview", DeleteAggregateView.as_view()),
    path("EditAggregateview", EditAggregateView.as_view()),
    path("getaggregatedview", GetAggregatedView.as_view()),

    # metric List Apis
    path("getAllTools", GetAllToolsView.as_view()),
    path("getAllMetrics", GetAllMetricsView.as_view()),
    path("getAllMeasures", GetAllMeasuresView.as_view()),
    path("getAllCategories", GetAllCategoriesView.as_view()),
    path("getMeasuresByTool", GetMeasuresByToolView.as_view()),
    path("getCategoryByMeasure", GetCategoryByMeasureView.as_view()),
    path("getMetricByCategory", GetMetricByCategoryView.as_view()),
    path("getMetricsByTool", GetMetricsByToolView.as_view()),
    path("getAllMetricsByCategory", GetMetricsByOnlyCategoryView.as_view()),
    # context investing styles screen
    path("context/investingStyle", InvestingStylesView.as_view()),
    path("context/getAllStyles", GetAllStylesView.as_view()),
    path("context/investingStyle/edit", EditInvestingStylesView.as_view()),
    path("context/investingStyle/get", GetInvestingStylesView.as_view()),
    path("context/investingStyle/delete", DeleteInvestingStyleView.as_view()),
    path("context/companies/filter", GetCompaniesByMetricsFilterView.as_view()),
    path("context/analysisModel/get", GetContextAnalysisModelsView.as_view()),
    path("context/mentorsByStyle", GetMentorsListByStyleView.as_view()),
    path("context/analysisModelsByMentor", GetAnalysisModelsListByMentorView.as_view()),
    path("context/categoryByAnalysisModel", GetCategoryListByAnalysisModelView.as_view()),
    path("context/getMetrics", GetMetricsListView.as_view()),
    path("context/getMeasuresByAnalysisModel", GetMeasureListByAnalysisModelView.as_view()),
    path("getMarketCap/company/<symbol>", GetCompanyMarketCap.as_view()),
    path("getStockPrice/company/<symbol>", GetCompanyStockPrice.as_view()),
    path("company/quote/<symbols>", GetCompaniesQuote.as_view()),

    path("getExchangeValues", GetExchangesValuesView.as_view()),
    path("getSectorByExchange", GetSectorByExchangeView.as_view()),
    path("getIndustryByExchangeSector", GetIndustryByExchangeSectorView.as_view()),
    path("getCompaniesByExchangeSectorIndustry", GetCompanyByExchangeSectorIndustryView.as_view()),
    path("getAllCompanies", GetAllDistinctCompaniesView.as_view()),
    path("getExchangesByCompanyName", GetExchangesByCompanyNameView.as_view()),

    path("companies/profile", GetCompanyProfileBasedOnTable.as_view()),

    path("dataAcquisition/Api", DataAcquisitionAPIView.as_view()),
    path("dataAcquisition/fileUpload", DataAcquisitionFileUploadView.as_view()),
    path("dataAcquisitionApiTypes", DataAcquisitionAPITypesView.as_view()),
    path("dataAcquisitionYearLimits", DataAcquisitionAPIYearLimitsView.as_view()),

    path("rates/countries", GetAvailableCountriesForRatesView.as_view()),
    path("rates/rateTypes", GetRateTypesByCountryView.as_view()),

    path("dataanalysis/fundamentalchart", data_analysis_process.as_view()),
    path("dataAnalysis/financials", DataAnalysisFinancialsView.as_view()),
    path("dataAnalysis/marketData", DataAnalysisMarketDataView.as_view()),
    path("dataAnalysis/keymetrics", DataAnalysisKeyMetricsView.as_view()),
    path("dataAnalysis/ranges", DataAnalysisRangesView.as_view()),
    path("dataAnalysis/lregression", DataAnalysisLinerRegressionView.as_view()),
    path("dataAnalysis/reportedFinancials", DataAnalysisReportedFinancialsView.as_view()),
    path("dataAnalysis/financialNotes", DataAnalysisFinancialNotesView.as_view()),
    path("dataAnalysis/rates", DataAnalysisRatesView.as_view()),
    path("ranges/metricsList", RangesMetricsListView.as_view()),

    path("dataProcessing/advancedRatios", DPGetAdvancedRatiosView.as_view()),
    path("dataProcessing/fundamentalchart", DPGetFundamentalChartDataView.as_view()),
    path("dataProcessing/fundamentalchart/create", DPCreateFundamentalChartDataView.as_view()),
    path("dataProcessing/fundamentalchart/update", DPUpdateFundamentalChartDataView.as_view()),
    path("dataProcessing/fundamentalchart/delete", DPDeleteFundamentalChartDataView.as_view()),
    path("getRatiosNamesByMetric", GetRangesNamesByMetricView.as_view()),

    path("screener/company/countries", GetCompaniesCountries.as_view()),
    path("screener/company/exchanges", GetCompaniesExchanges.as_view()),

    path("screener/countries/exchange", GetExchangesByCountry.as_view()),
    # path("screener/state", GetStateByCountryAndExchange.as_view()),
    path("screener/city", GetCityByCountryAndExchange.as_view()),
    path("screener/sector", GetScreenerSectorByExchangeView.as_view()),
    path("screener/industry", GetScreenerIndustryByExchangeSectorView.as_view()),
    path("screener/getCategories", GetScreenerCategories.as_view()),
    path("screener/getMetrics", GetScreenerMetricsByCategory.as_view()),
    path("screener/getCompanies/filers", GetCompaniesByFilters.as_view()),
    path("screener/company/data", GetScreenerCompaniesData.as_view()),
    path("screener/filter/companies", GetScreenerCompaniesByMetricsFilterView.as_view()),
    # path("screener/comapanies/performance", GetScreenerCompaniesPerformance.asview()),
]
