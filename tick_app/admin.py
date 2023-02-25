from django.contrib import admin

from .models import *

Company,DataType,YearLimit,CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend,AnalysisTools, RevenueLocation, ReportedIncome,AggregateCodes,Exchanges, ReportedBSheet, AggregatedView

# Register your models here.
@admin.register (Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display=['id','symbol','company_name','isin','currency','exchange']
    

@admin.register (CustomRatios)
class CustomRatiosAdmin(admin.ModelAdmin):
    list_display=['id','measure','category','metrics','code','numerator','denominator']


@admin.register (RevenueLocation)
class RevenueLocationAdmin(admin.ModelAdmin):
    list_display=['id','company_name','year','location','revenueperlocation']


@admin.register (Exchanges)
class Exchanges(admin.ModelAdmin):
    list_display=['id','company_name','symbol','isin','sector','industry','exchange','exchange_short_name','country','currency','marketcap']




@admin.register (CustomMetrics)
class CustomMetricsAdmin(admin.ModelAdmin):
    list_display=['id','tools','measure','category','metrics','source']

@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    list_display=['type','category','target_table']

@admin.register(YearLimit)
class YearLimit(admin.ModelAdmin):
    list_display=['limit']

@admin.register(AnalysisTools)
class AnalysisTools(admin.ModelAdmin):
    list_display=['tools','super_category','category','subcategory','metrics','source','unit1','unit2']

@admin.register(ReportedIncome)
class AnalysisTools(admin.ModelAdmin):
    list_display=['company_name','year','post_id','aggregate_code','notes','value1', 'value2']

@admin.register(ReportedBSheet)
class AnalysisTools(admin.ModelAdmin):
    list_display=['company_name','year','post_id','aggregate_code','notes','value1', 'value2']

@admin.register(RevenueSector)
class AnalysisTools(admin.ModelAdmin):
    list_display=['company_name','year','sector', 'revenuepersector']

@admin.register(AggregateCodes)
class AnalysisTools(admin.ModelAdmin):
    list_display=['aggregate_code','item', 'source']


@admin.register(Ranges)
class AnalysisTools(admin.ModelAdmin):
    list_display=['metrics','name', 'source','max','min']

@admin.register(Rates)
class Rates(admin.ModelAdmin):
    list_display=['country','year','rate','rate_type']


class AggretedViewAdmin(admin.ModelAdmin):
    list_display=['view','name','item1','operator1','item2','operator2','item3','operator3','item4','operator4','item5']



admin.site.register(Income)

admin.site.register(BSheet)



admin.site.register(CFlow)

admin.site.register(Profile)
admin.site.register(KeyMetrics)
admin.site.register(FinGrowth)
admin.site.register(Institutional)
admin.site.register(KeyExecutives)
admin.site.register(IncomeGrowth)
admin.site.register(BSheetGrowth)
admin.site.register(CFlowGrowth)
admin.site.register(Ratios)
admin.site.register(RatiosTTM)
admin.site.register(EV)
admin.site.register(KeyMetricsTTM)
admin.site.register(MutualFund)
admin.site.register(Peers)
admin.site.register(Price)
admin.site.register(Dividend)
admin.site.register(AggregatedView, AggretedViewAdmin)



#admin.site.register(AnalysisTools)

