from tick_app.models import (AggregateCodes, Company,DataType, ReportedIncome,YearLimit,CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend,AnalysisTools,ReportedBSheet,ReportedCFlow,Rates,RevenueLocation,Ranges,RevenueSector)
import pandas
from datetime import date, timedelta, datetime
import requests
import json
from tickers.settings import GetSecretProperties
model_dict={

'historical-price-full':Price,
'stock-dividend':Dividend,

}

def market_data_func(f_company,f_table,f_from,f_to):
    return_list=[]
    startdate=''.join(f_from.split('-')[::-1])
    startdate=datetime.strptime(startdate, "%d%m%Y").date()
    enddate=''.join(f_to.split('-')[::-1])
    enddate=datetime.strptime(enddate, "%d%m%Y").date()
    date_range=list(pandas.date_range(startdate,enddate-timedelta(days=1),freq='d'))
    date_range=[str(x.strftime("%Y-%m-%d")) for x in date_range]

    model_select=model_dict[f_table]

    fields_list=[f.name for f in model_select._meta.get_fields()]
    columns=[str(x) for x in fields_list]
    print(columns)
    _symbol=Company.objects.filter(company_name=f_company)
    symbol_=_symbol[0].symbol

    columns=[x for x in columns if x.lower()!='id' ]
    data_got=model_select.objects.filter(symbol=symbol_)
    date_range=[str(x) for x in date_range]
    data_got=[x for x in data_got if str(x.date) in date_range ]

    for data in data_got:
        data_append= []
        for field in fields_list:
            if field.lower()!='id':
                data_append.append(getattr(data,field))
        return_list.append(data_append)
    print(columns)
    return(return_list, columns)


def market_data_func_latest(f_company, f_exchange,f_table,f_from,f_to):
    _symbol=Company.objects.filter(company_name=f_company, exchange=f_exchange)
    symbol_=_symbol[0].symbol
    IS_DA_HISTORICAL_DATA_FROM_DB = False
    if IS_DA_HISTORICAL_DATA_FROM_DB:
        model_select=model_dict[f_table]

        fields_list=[f.name for f in model_select._meta.get_fields()]
        columns=[str(x) for x in fields_list]
        columns=[x for x in columns if x.lower()!='id' ]
        data_got=model_select.objects.filter(symbol=symbol_, date__gte=f_from, date__lte=f_to)

        object_list = []
        for data in data_got:
            object_data = {}
            for field in fields_list:
                if field.lower()!='id':
                    object_data[field] = getattr(data,field)
            object_list.append(object_data)
        return(object_list, columns)
    else:
        columns = []
        url = "https://financialmodelingprep.com/api"
        if f_table == "historical-price-full":
            columns = ["date", "open", "high", "low", "close", "adjClose", "volume", "unadjustedVolume", "change", "changePercent", "vwap", "label", "changeOverTime"]
            url = url + "/v3/historical-price-full/"+symbol_+"?from=" + f_from +"&to=" + f_to
        else:
            columns = "date", "label", "adjDividend", "dividend", "recordDate", "paymentDate", "declarationDate"
            url = url + "/v3/historical-price-full/stock_dividend/"+ symbol_ +"?from=" + f_from +"&to=" + f_to
        return (ExecuteAPI(url), columns)

def ExecuteAPI(url):
    SECRETS = {}
    response = []
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
        p_api = SECRETS['FINANCIALPREP_API_KEY']
        url = url + "&apikey=" + p_api
        print(url)
        apiResponse = requests.get(f"{url}")
        data = json.loads(apiResponse.content)
        response = data['historical']
    except Exception as e:
        print(e)
    return response