
from tick_app.models import (AggregateCodes, Company, DataType, ReportedIncome, YearLimit, CFlow,
                             Income, BSheet, Profile, KeyMetrics, FinGrowth, Institutional,
                             KeyExecutives, IncomeGrowth, BSheetGrowth, CFlowGrowth, Ratios, RatiosTTM, EV, KeyMetricsTTM, MutualFund, Peers,
                             Price, Dividend, AnalysisTools, ReportedBSheet, ReportedCFlow, Rates, RevenueLocation, Ranges, RevenueSector)

from rest_framework import serializers
from django.http import JsonResponse
from .companyDetails import getCompanyProfile, getCompanyKeyExecutives, getCompanyInsiderTrading
model_dict = {
    'institutional-holder': Institutional,
    'mutual-fund-holder': MutualFund,
    'stock_peers': Peers,
    'profile': Profile,
    'key-executives': KeyExecutives,
}


def profile_func(f_company, f_table):
    return_list = []
    columns = []

    model_select = model_dict[f_table]

    _symbol = Company.objects.filter(company_name=f_company)
    symbol_ = _symbol[0].symbol

    print("symbol", symbol_)
    fields_list = [f.name for f in model_select._meta.get_fields()]
    print(fields_list)

    if f_table == 'profile':

        data_ = model_select.objects.filter(symbol=symbol_)[0]

        for field in fields_list:
            if 'id' in field:
                pass
            else:
                return_list.append(
                    {'field': field, 'value': getattr(data_, field)})

    else:
        data_ = model_select.objects.filter(symbol=symbol_)
        for data in data_:
            datalist = []
            for field in fields_list:
                if 'id' not in field.lower():
                    datalist.append(getattr(data, field))
            return_list.append(datalist)
        columns = [x for x in fields_list if 'id' not in x]

    return (return_list, columns)


class profile_func2(serializers.Serializer):
    company = serializers.CharField(write_only=True)
    exchange = serializers.CharField(write_only=True)
    resp_data = serializers.ReadOnlyField()
    def validate(self, data):
        # return_list = []
        # t_table = data.get('table', None)
        t_company = data.get('company', None)
        t_exchange = data.get('exchange', None)
        # model_select = model_dict[t_table]
        _symbol = Company.objects.filter(company_name=t_company, exchange=t_exchange)
        symbol_ = _symbol[0].symbol
        profile = getCompanyProfile(symbol_)
        keyExecutives = getCompanyKeyExecutives(symbol_)
        insiderTrading = getCompanyInsiderTrading(symbol_)
#         insiderTrading.append({
#   "symbol" : "AAPL",
#   "filingDate" : "2022-11-23 18:30:27",
#   "transactionDate" : "2022-11-22",
#   "reportingCik" : "0001631982",
#   "transactionType" : "S-Sale",
#   "securitiesOwned" : 31505.0,
#   "companyCik" : "0000320193",
#   "reportingName" : "KONDO CHRIS",
#   "typeOfOwner" : "officer: Principal Accounting Officer",
#   "acquistionOrDisposition" : "D",
#   "formType" : "4",
#   "securitiesTransacted" : 20200.0,
#   "price" : 148.72,
#   "securityName" : "Common Stock",
#   "link" : "https://www.sec.gov/Archives/edgar/data/0000320193/000032019322000113/0000320193-22-000113-index.htm"
# })
        tradingData = []
        for record in insiderTrading:
            record['value'] = record['securitiesTransacted'] * record['price']
            tradingData.append(record)
        # fields_list = [f.name for f in model_select._meta.get_fields()]

        # if t_table == 'profile':
        #     data_ = model_select.objects.filter(symbol=symbol_)[0]
        #     for field in fields_list:
        #         if 'id' in field:
        #             pass
        #         else:
        #             return_list.append(
        #                 {'field': field, 'value': getattr(data_, field)})
        # else:
        #     return_list = model_select.objects.filter(symbol=symbol_).values()
        response = {"resp_data": {"profile": profile, "keyExecutives": keyExecutives, "insiderTrading": tradingData}}
        print("ProfileResponse", response)
        return response
