
from tick_app.models import (AggregateCodes, Company,DataType, ReportedIncome,YearLimit,CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend,AnalysisTools,ReportedBSheet,ReportedCFlow,Rates,RevenueLocation,Ranges,RevenueSector,Pnl,FinBsheet,FinCflow,MetricsList)
import requests
import json
from datetime import date
from tickers.settings import GetSecretProperties

model_dict={

'Income':Income,
'balanceSheet':BSheet,
'cashFlows':CFlow,
'financial-growth':FinGrowth,
'Income_Growth':IncomeGrowth,
'balanceSheet_Growth':BSheetGrowth,
'cashFlow_Growth':CFlowGrowth,
'revenue_sector':RevenueSector,
'revenue_location':RevenueLocation,
'reported_income':ReportedIncome,
'reported_bsheet':ReportedBSheet,
'reported_cflow':ReportedCFlow,
"pnl":Pnl,
}

incomeFieldList = ['date', 'revenue', 'costOfRevenue', 'grossProfit', 'grossProfitRatio', 'researchAndDevelopmentExpenses', 'generalAndAdministrativeExpenses', 'sellingAndMarketingExpenses', 'otherExpenses', 'operatingExpenses', 'costAndExpenses', 'interestExpense', 'depreciationAndAmortization', 'ebitda', 'ebitdaratio', 'operatingIncome', 'operatingIncomeRatio', 'totalOtherIncomeExpensesNet', 'incomeBeforeTax', 'incomeBeforeTaxRatio', 'incomeTaxExpense', 'netIncome', 'netIncomeRatio', 'eps', 'epsdiluted', 'weightedAverageShsOut', 'weightedAverageShsOutDil']
balanceSheetFieldList = ['date', 'cashAndCashEquivalents', 'shortTermInvestments', 'cashAndShortTermInvestments', 'netReceivables', 'inventory', 'otherCurrentAssets', 'totalCurrentAssets', 'propertyPlantEquipmentNet', 'goodwill', 'intangibleAssets', 'goodwillAndIntangibleAssets', 'longTermInvestments', 'taxAssets', 'otherNonCurrentAssets', 'totalNonCurrentAssets', 'otherAssets', 'totalAssets', 'accountPayables', 'shortTermDebt', 'taxPayables', 'deferredRevenue', 'otherCurrentLiabilities', 'totalCurrentLiabilities', 'longTermDebt', 'deferredRevenueNonCurrent', 'deferredTaxLiabilitiesNonCurrent', 'otherNonCurrentLiabilities', 'totalNonCurrentLiabilities', 'otherLiabilities', 'totalLiabilities', 'commonStock', 'retainedEarnings', 'accumulatedOtherComprehensiveIncomeLoss', 'netDebt', 'othertotalStockholdersEquity', 'totalDebt', 'totalInvestments', 'totalLiabilitiesAndStockholdersEquity', 'totalStockholdersEquity']
cashFlowFieldList = ['date', 'netIncome', 'inventory', 'accountsPayables', 'accountsReceivables', 'acquisitionsNet', 'capitalExpenditure', 'cashAtBeginningOfPeriod', 'cashAtEndOfPeriod', 'changeInWorkingCapital', 'commonStockIssued', 'commonStockRepurchased', 'debtRepayment', 'deferredIncomeTax', 'depreciationAndAmortization', 'dividendsPaid', 'effectOfForexChangesOnCash', 'freeCashFlow', 'investmentsInPropertyPlantAndEquipment', 'netCashProvidedByOperatingActivities', 'netCashUsedForInvestingActivites', 'netCashUsedProvidedByFinancingActivities', 'netChangeInCash', 'operatingCashFlow', 'otherFinancingActivites', 'otherInvestingActivites', 'otherNonCashItems', 'otherWorkingCapital', 'purchasesOfInvestments', 'salesMaturitiesOfInvestments', 'stockBasedCompensation']
bSheetGrowthFieldList = ['date', 'growthCashAndCashEquivalents', 'growthShortTermInvestments', 'growthCashAndShortTermInvestments', 'growthNetReceivables', 'growthInventory', 'growthOtherCurrentAssets', 'growthTotalCurrentAssets', 'growthPropertyPlantEquipmentNet', 'growthGoodwill', 'growthIntangibleAssets', 'growthGoodwillAndIntangibleAssets', 'growthLongTermInvestments', 'growthTaxAssets', 'growthOtherNonCurrentAssets', 'growthTotalNonCurrentAssets', 'growthOtherAssets', 'growthTotalAssets', 'growthAccountPayables', 'growthShortTermDebt', 'growthTaxPayables', 'growthDeferredRevenue', 'growthOtherCurrentLiabilities', 'growthTotalCurrentLiabilities', 'growthLongTermDebt', 'growthDeferredRevenueNonCurrent', 'growthDeferrredTaxLiabilitiesNonCurrent', 'growthOtherNonCurrentLiabilities', 'growthTotalNonCurrentLiabilities', 'growthOtherLiabilities', 'growthTotalLiabilities', 'growthCommonStock', 'growthRetainedEarnings', 'growthAccumulatedOtherComprehensiveIncomeLoss', 'growthOthertotalStockholdersEquity', 'growthTotalStockholdersEquity', 'growthTotalLiabilitiesAndStockholdersEquity', 'growthTotalInvestments', 'growthTotalDebt', 'growthNetDebt']
cFlowGrowthFieldList = ['date', 'growthNetIncome', 'growthDepreciationAndAmortization', 'growthDeferredIncomeTax', 'growthStockBasedCompensation', 'growthChangeInWorkingCapital', 'growthAccountsReceivables', 'growthInventory', 'growthAccountsPayables', 'growthOtherWorkingCapital', 'growthOtherNonCashItems', 'growthNetCashProvidedByOperatingActivites', 'growthInvestmentsInPropertyPlantAndEquipment', 'growthAcquisitionsNet', 'growthPurchasesOfInvestments', 'growthSalesMaturitiesOfInvestments', 'growthOtherInvestingActivites', 'growthNetCashUsedForInvestingActivites', 'growthDebtRepayment', 'growthCommonStockIssued', 'growthCommonStockRepurchased', 'growthDividendsPaid', 'growthOtherFinancingActivites', 'growthNetCashUsedProvidedByFinancingActivities', 'growthEffectOfForexChangesOnCash', 'growthNetChangeInCash', 'growthCashAtEndOfPeriod', 'growthCashAtBeginningOfPeriod', 'growthOperatingCashFlow', 'growthCapitalExpenditure', 'growthFreeCashFlow']
incomeGrowthFieldList = ['date', 'growthRevenue', 'growthCostOfRevenue', 'growthGrossProfit', 'growthGrossProfitRatio', 'growthResearchAndDevelopmentExpenses', 'growthGeneralAndAdministrativeExpenses', 'growthSellingAndMarketingExpenses', 'growthOtherExpenses', 'growthOperatingExpenses', 'growthCostAndExpenses', 'growthInterestExpense', 'growthDepreciationAndAmortization', 'growthEBITDA', 'growthEBITDARatio', 'growthOperatingIncome', 'growthOperatingIncomeRatio', 'growthTotalOtherIncomeExpensesNet', 'growthIncomeBeforeTax', 'growthIncomeBeforeTaxRatio', 'growthIncomeTaxExpense', 'growthNetIncome', 'growthNetIncomeRatio', 'growthEPS', 'growthEPSDiluted', 'growthWeightedAverageShsOut', 'growthWeightedAverageShsOutDil']

def fin_func(f_company,f_table,f_from,f_to):
    return_list=[]
    model_select=model_dict[f_table]
    
    _symbol=Company.objects.filter(company_name=f_company)
    symbol_=_symbol[0].symbol
    date_range=list(range(int(f_from),int(f_to)+1))
    date_range=[str(x) for x in date_range]
    print("symbol",symbol_, date_range)

    try:
        try:
            data_=model_select.objects.filter(symbol=symbol_).order_by('year')
        except:
            data_=model_select.objects.filter(symbol=symbol_).order_by('date')
    except:
        try:
            data_=model_select.objects.filter(company_name=f_company).order_by('year')
        except:
            data_=model_select.objects.filter(company_name=f_company).order_by('date')


    

   
    fields_list=[f.name for f in model_select._meta.get_fields()]
    
    try:    
        filter_data=[x for x in data_ if x.year.split('-')[0] in date_range ]
        dates_available=([x.year.split('-')[0] for x in data_])
    except:
        filter_data=[x for x in data_ if x.date.split('-')[0] in date_range ]
        dates_available=([x.date.split('-')[0] for x in data_])   

    for field_ in fields_list:
        if 'date' in field_ or 'year' in field_ or 'id'==field_ or 'symbol' in field_ or 'company' in field_:
            pass
        else:
            data_l=[]
            dict_={'field':field_}
            try:
                metric_obj=AnalysisTools.objects.filter(metrics=field_)[0]
                unit1=getattr(metric_obj,'unit1')
                unit2=getattr(metric_obj,'unit2')
                for i in date_range:
                
                    if str(i) in dates_available:
                        try:
                            x=[x for x in filter_data if x.year.split('-')[0] == i][0]
                        except:
                            x=[x for x in filter_data if x.date.split('-')[0] == i][0]
                        #dict_[i]=
                        if 'millions' in unit1:
                            
                            try:
                                data_l.append(str(round(getattr(x,field_)/1000000,2)))   #+'M')
                            except:
                                data_l.append(getattr(x,field_))
                        elif 'decimals' in unit2:
                            
                            try:
                                data_l.append(str(round(getattr(x,field_)/1000000,2)))
                            except:
                                data_l.append(getattr(x,field_))

                    else:
                                        
                        #dict_[i]= 'NA'
                        data_l.append('NA')
            except:
                for i in date_range:
                    if str(i) in dates_available:
                        try:
                            x=[x for x in filter_data if x.year.split('-')[0] == i][0]
                        except:
                            x=[x for x in filter_data if x.date.split('-')[0] == i][0]
                        data_l.append(getattr(x,field_))
                    else:
                        data_l.append("NA")



        #    dict_['data_l']=[x.replace('M','') for x in data_l]
            dict_['data_l']=data_l
            
            return_list.append(dict_)
        

    
    return (return_list, date_range)

def fin_func_latest(f_company,f_table, display, period, quarter,f_from,f_to, exchange):
    print("FUN FUNC LATEST")
    return_list=[]
    _symbol=Company.objects.filter(company_name=f_company, exchange=exchange)
    symbol_=_symbol[0].symbol
    currentYear = date.today().year
    date_range=list(range(int(f_from),int(f_to)+1))
    date_range=[str(x) for x in date_range]
    fields_list = []
    IS_DA_FINANCIALS_FROM_DB = False
    if IS_DA_FINANCIALS_FROM_DB:
        if (display == "Growth"):
            f_table = f_table + "_" + "Growth"
        model_select=model_dict[f_table]
        fields_list = [f.name for f in model_select._meta.get_fields()]
        orderBy = "date"
        if 'year' in fields_list:
            orderBy = "year"
            data_ = model_select.objects.filter(symbol=symbol_, year__gte=str(f_from), year__lte=str(f_to)).order_by(orderBy)
        else:
            data_ = model_select.objects.filter(symbol=symbol_, date__gte=str(f_from)+"-01-01", date__lte=str(f_to)+"-12-31" ).order_by(orderBy)
        return ParseDataFromDBResponse(fields_list, data_, display, period, date_range)
    else:
        print("##### EXECUTIN API CASE ########")
        url = "https://financialmodelingprep.com/api"
        limit = ""
        queryString = ""
        if period == "Quarter":
            maxYear = (currentYear + 2)-int(f_from)
            limit = str((maxYear * 4))
            queryString = "?period=quarter&limit=" + limit + "&"
        else:
            limit = str(((currentYear+1)-int(f_from)))
            queryString = "?limit=" + limit + "&"
        if f_table == "Income" and display=="Growth":
            fields_list = incomeGrowthFieldList
            url = url + "/v3/income-statement-growth/" + symbol_ + queryString
        elif f_table == "BalanceSheet" and display=="Growth":
            fields_list = bSheetGrowthFieldList
            url = url + "/v3/balance-sheet-statement-growth/" + symbol_ + queryString
        elif f_table == "CashFlows" and display=="Growth":
            fields_list = cFlowGrowthFieldList
            url = url + "/v3/cash-flow-statement-growth/" + symbol_ + queryString
        elif f_table == "Income":
            fields_list = incomeFieldList
            url = url + "/v3/income-statement/" + symbol_ + queryString
        elif f_table == "BalanceSheet":
            fields_list = balanceSheetFieldList
            url = url + "/v3/balance-sheet-statement/" + symbol_ + queryString
        elif f_table == "CashFlows":
            fields_list = cashFlowFieldList
            url = url + "/v3/cash-flow-statement/" + symbol_ + queryString
        data_ = ExecuteAPI(url, date_range)
        print('printing data financials.py 179')
        print('-------here-----------')
        print(data_)
        print('------end-------')
        return ParseDataFromAPIResponse(fields_list, data_, display, period, date_range, quarter)

def ExecuteAPI(url, dateRange):
    SECRETS = {}
    response = []
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
        p_api = SECRETS['FINANCIALPREP_API_KEY']
        url = url + "apikey=" + p_api
        apiResponse = requests.get(f"{url}")
        data = json.loads(apiResponse.content)
        year = ""
        for obj in data:
            year = str(obj['date']).split("-")[0]
            if (year in dateRange):
                response.append(obj)
                year=""
    except Exception as e:
        print(e)
    return response

def ParseDataFromAPIResponse(fields_list, data_, display, period, dateRange, quarter):
    print("#### PARSING API RESPONSE ############")
    responseFileds = []
    response = []
    print('---------------On the TOP------------')
    print(fields_list)
    print(data_)
    print(display)
    print(period)
    print(dateRange)
    print(quarter)

    print('---------------On the TOP------------')
    for field_ in fields_list:
        if 'date' == field_ or 'year' == field_ or 'id'== field_ or 'symbol' == field_ or 'company' == field_ or 'period' == field_ or field_.lower().endswith("ratio"):
            pass
        else:
            dict_={'field':field_}
            try:
                dict_['metric']=field_
                metric_obj=AnalysisTools.objects.filter(metrics=field_)[0]
                metrics=MetricsList.objects.filter( metric=field_).values("metric", "unit","measure","category","description","function","interpretation","limitation","good_range","bad_range")
                print('---------------printing metrics 226--------------')
                print(metrics)
                dict_['details']=metrics
                print('---------------printing metrics 226--------------')

                print('financials.py 216')
                print('--------------')
                print(field_)
                print('--------------')
                unit1=getattr(metric_obj,'unit1')
                unit2=getattr(metric_obj,'unit2')
               
                for x in data_:
                    filter = ""
                    if period == "Quarter":
                        if x['period'] in quarter:
                            filter = str(x['year']) + "_" + x['period'] if 'year' in fields_list else str(x['date']).split("-")[0] + "_" + x['period']
                            responseFileds.append(filter)
                    else:
                        filter = str(x['year']) if 'year' in fields_list else str(x['date']).split("-")[0]
                        responseFileds.append(filter)
                    if display == "Growth":
                        try:
                            dict_[filter] = str(round(x[field_]*100, 2)) + "%" if (x[field_] != None) else str(0) + "%"
                        except:
                            dict_[filter] = str(x[field_]*100) + "%" if (x[field_] != None) else str(0) + "%"
                    else:
                        if 'million' in unit1:
                            try:
                                dict_[filter] = f'{(str(round(x[field_])/1000000, 2)):,}' if (x[field_] != None) else 0
                            except:
                                dict_[filter] = f'{(x[field_]):,}' if (x[field_] != None) else 0
                        elif 'decimal' in unit2:
                            try:
                                dict_[filter] = f'{(str(round(x[field_], 2))):,}' if (x[field_] != None) else 0.00
                            except:
                                dict_[filter] = f'{(x[field_]):,}' if (x[field_] != None) else 0.00
                        elif 'percent' in unit1 or 'percent' in unit2:
                            try:
                                dict_[filter] = str(round(x[field_]*100, 2)) + "%" if (x[field_] != None) else str(0) + "%"
                            except:
                                dict_[filter] = str(x[field_]*100)  + "%" if (x[field_] != None) else str(0) + "%"
                        else:
                            dict_[filter] = f'{(x[field_]):,}' if (x[field_] != None) else 0
            except Exception as e:
                print(e)
                for x in data_:
                    filter = str(x['year']) if 'year' in fields_list else str(x['date']).split("-")[0]
                    dict_[filter] = f'{(x[field_]):,}' if (x[field_] != None) else 0
            response.append(dict_)
    return(response, dateRange, sorted(set(responseFileds)))

def ParseDataFromDBResponse(fields_list, data_,display , period, dateRange):
    responseFileds = []
    response = []
    for field_ in fields_list:
        if 'date' == field_ or 'year' == field_ or 'id'== field_ or 'symbol' == field_ or 'company' == field_:
            pass
        else:
            dict_={'field':field_}
            try:
                dict_['metric']=field_
                metric_obj=AnalysisTools.objects.filter(metrics=field_)[0]
                unit1=getattr(metric_obj,'unit1')
                unit2=getattr(metric_obj,'unit2')
                for x in data_:
                    filter = ""
                    if period == "Quarter":
                        filter = str(getattr(x, 'year')) + "_" + getattr(x, 'period') if 'year' in fields_list else str(getattr(x, 'date')).split("-")[0] + "_" + getattr(x, 'period')
                    else:
                        filter = str(getattr(x, 'year')) if 'year' in fields_list else str(getattr(x, 'date')).split("-")[0]
                    responseFileds.append(filter)
                    if display == "Growth":
                        try:
                            dict_[filter] = str(round(x[field_]*100, 2)) if (x[field_] != None) else str(0) + "%"
                        except:
                            dict_[filter] = str(x[field_]*100) + "%" if (x[field_] != None) else str(0) + "%"
                    else:
                        if 'million' in unit1:
                            try:
                                dict_[filter] = f'{(str(round(getattr(x, field_))/1000000, 2)):,}'
                            except:
                                dict_[filter] = f'{(getattr(x, field_)):,}'
                        elif 'decimal' in unit2:
                            try:
                                dict_[filter] = f'{(str(round(getattr(x, field_), 2))):,}'
                            except:
                                dict_[filter] = f'{(getattr(x, field_)):,}'
                        elif 'percent' in unit1 or 'percent' in unit2:
                            try:
                                dict_[filter] = str(round(x[field_]*100, 2)) if (x[field_] != None) else str(0) + "%"
                            except:
                                dict_[filter] = str(x[field_]*100) + "%" if (x[field_] != None) else str(0) + "%"
                        else:
                            dict_[filter] = f'{(getattr(x, field_)):,}'
            except:
                for x in data_:
                    filter = str(getattr(x, 'year')) if 'year' in fields_list else str(getattr(x, 'date')).split("-")[0]
                    dict_[filter] = f'{(getattr(x, field_)):,}'
            response.append(dict_)
    return(response, dateRange, sorted(set(responseFileds)))
