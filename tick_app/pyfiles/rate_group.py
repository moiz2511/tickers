from datetime import date
from tick_app.models import (AggregateCodes, Company,DataType, ReportedIncome,YearLimit,CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend,AnalysisTools,ReportedBSheet,ReportedCFlow,Rates,RevenueLocation,Ranges,RevenueSector)

def rate_func(r_country,r_rate_type,r_from,r_to):
    date_range=list(range(int(r_from),int(r_to)+1))
    date_range=[str(x) for x in date_range]
    data=Rates.objects.all()

    #data=[x for x in data if str(x.year.split('/')[-1].split(' ')[0]) in date_range ]
    data=[x for x in data if str(x.year).split('/')[-1].split(' ')[0].split('-')[0] in date_range]
    #data=[x for x in data if str(x.country).lstrip() in r_country]

    return data

def rate_func_latest(r_country,r_rate_type,r_from,r_to):
    print(r_country,r_rate_type,r_from,r_to)
    date_range=list(range(int(r_from),int(r_to)+1))
    date_range=[str(x) for x in date_range]
    print("Executing Query")
    data=Rates.objects.filter(country=r_country, rate_type=r_rate_type, year__gte=str(r_from)+"-01-01", year__lte=str(r_to)+"-12-31")
    print("Query Executed")
    #data=[x for x in data if str(x.year.split('/')[-1].split(' ')[0]) in date_range ]
    # data=[x for x in data if str(x.year).split('/')[-1].split(' ')[0].split('-')[0] in date_range]
    #data=[x for x in data if str(x.country).lstrip() in r_country]

    return data


