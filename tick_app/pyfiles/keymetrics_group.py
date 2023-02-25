import requests
import json
from datetime import date
from tick_app.models import (Company, RatiosTTM, KeyMetricsTTM, MetricsList)
from tickers.settings import GetSecretProperties
from .companyDetails import getCompanyProfile
model_dict={
'ratios-ttm':RatiosTTM,
'keymetrics-ttm':KeyMetricsTTM
}

unitSymbolDict = {
    "million": "M",
    "decimal": "",
    "days": "days",
    "x time": "x",
    "percent": "%",
    "monetary": "ccy"
}

def keymetrics_func(f_company, f_exchange, f_table, category, frequency, quarter, fromYear, toYear):
    # SECRETS = {}
    # try:
    #     SECRETS = GetSecretProperties.getSecretsObj()
    # except Exception as e:
    #     print(e)
    return_list=[]
    date_range=list(range(int(fromYear),int(toYear)+1))
    date_range=[str(x) for x in date_range]
    # model_select=model_dict[f_table]
    _symbol=Company.objects.filter(company_name=f_company, exchange=f_exchange)
    symbol_=_symbol[0].symbol
    print("symbol",symbol_)
    # fields_list=[f.name for f in model_select._meta.get_fields()]
    # print(fields_list)
    # data_ = model_select.objects.filter(symbol=symbol_)[0]
    # data_ = callFinPrepApi(symbol_, SECRETS['FINANCIALPREP_API_KEY'], f_table)[0]
    metrics = []
    if f_table == "Ratios":
        metrics=MetricsList.objects.filter(source="tick_app_ratios", category=category).values("metric", "unit","measure","category","description")
    else:
        metrics=MetricsList.objects.filter(source="tick_app_keymetrics", category=category).values("metric", "unit","measure","category","description")
    metricsList = [metric['metric'] for metric in metrics]
    metricsUnit = {}
    for metric in metrics:
        metricDetail={'unit':metric['unit'],'measure':metric['measure'],'category':metric['category'],'description':metric['description']}
        metricsUnit[metric['metric']]=metricDetail

    currentYear = date.today().year
    url = "https://financialmodelingprep.com/api"
    ttmURL = url
    limit = ""
    queryString = ""
    try:
        if frequency == "Quarter":
            maxYear = (currentYear + 2)-int(fromYear)
            limit = str((maxYear * 4))
            queryString = "?period=quarter&limit=" + limit + "&"
        else:
            limit = str(((currentYear+1)-int(fromYear)))
            queryString = "?limit=" + limit + "&"
    except Exception as e:
        print(e)
    if f_table == "Ratios":
        url = url + "/v3/ratios/"+symbol_ + queryString
        ttmURL = ttmURL + "/v3/ratios-ttm/"+symbol_+"?"
        ratiosTTMRespose = ExecuteAPI(ttmURL, date_range, False)
        # ratiosTTMResp, ratiosTTMRespFields = ParseDataFromAPIResponse(metricsTTM, ratiosTTMRespose, frequency, date_range, True, quarter)
        ratiosRespose = ExecuteAPI(url, date_range, True)
        ratiosResp, ratiosRespFields = ParseDataFromAPIResponse(metricsList, ratiosRespose, frequency, date_range, False, quarter, metricsUnit, symbol_)
        finalRatiosResp = []
        for ratioData in ratiosResp:
            try:
                unit = metricsUnit[ratioData['metric']]
                ratioData["ttm"] = getValueParsedByUnit(ratiosTTMRespose[0][ratioData['metric']+"TTM"], unit)
            except Exception as e:
                print(e)
                ratioData["ttm"] = getValueParsedByUnit(0, unit)
            ratioData["unit"] = unit
            # if unit is not None and unit != "":
            #     if unitSymbolDict[unit] is not None and unitSymbolDict[unit] != "":
            #         unitSymbol = unitSymbolDict[unit]
            #         if unitSymbol == "ccy":
            #             data = getCompanyProfile(symbol_)
            #             unitSymbol = data[0]['currency']
            #         ratioData['field'] = ratioData['metric'] + " ("+unitSymbol+")"
            finalRatiosResp.append(ratioData)
        objectResponse = {}
        objectResponse['ratiosResp'] = finalRatiosResp
        # objectResponse['ratiosTTMResp'] = ratiosTTMResp
        objectResponse['ratiosRespFields'] = ratiosRespFields
        objectResponse['metricsUnit'] = metricsUnit
        # objectResponse['ratiosTTMRespFields'] = ratiosTTMRespFields
        return_list.append(objectResponse)
    else:
        url = url + "/v3/key-metrics/"+symbol_ + queryString
        ttmURL = ttmURL + "/v3/key-metrics-ttm/"+symbol_+"?"
        keyMetrics = ExecuteAPI(url, date_range, True)
        keyMetricsResp, keyMetricsRespFields = ParseDataFromAPIResponse(metricsList, keyMetrics, frequency, date_range, False, quarter, metricsUnit, symbol_)
        keyTTMMetrics = ExecuteAPI(ttmURL, date_range, False)
        # keyTTMMetricsResp, keyTTMMetricsRespFields = ParseDataFromAPIResponse(metricsTTM, keyTTMMetrics, frequency, date_range, True, quarter)
        finalKeyMetricsResp = []
        for keyMetric in keyMetricsResp:
            try:
                unit = metricsUnit[keyMetric['metric']]
                keyMetric["ttm"] = getValueParsedByUnit(keyTTMMetrics[0][keyMetric['metric']+"TTM"], metricsUnit[keyMetric['metric']])
            except Exception as e:
                print(e)
                keyMetric["ttm"] = getValueParsedByUnit(0, metricsUnit[keyMetric['metric']])
            keyMetric["unit"] = metricsUnit[keyMetric['metric']]
            # if unit is not None and unit != "":
            #     if unitSymbolDict[unit] is not None and unitSymbolDict[unit] != "":
            #         unitSymbol = unitSymbolDict[unit]
            #         if unitSymbol == "ccy":
            #             data = getCompanyProfile(symbol_)
            #             unitSymbol = data['currency']
            #         keyMetric['field'] = keyMetric['metric'] + " ("+unitSymbol+")"
            finalKeyMetricsResp.append(keyMetric)
        objectResponse = {}
        objectResponse['keyMetricsResp'] = finalKeyMetricsResp
        # objectResponse['keyTTMMetricsResp'] = keyTTMMetricsResp
        objectResponse['keyMetricsRespFields'] = keyMetricsRespFields
        objectResponse['metricsUnit'] = metricsUnit
        # objectResponse['keyTTMMetricsRespFields'] = keyTTMMetricsRespFields
        return_list.append(objectResponse)
    # for field in data_.keys():
    #     if 'id' in field:
    #         pass
    #     else:
    #         # value = round(float(getattr(data_, field)), 2) if type(getattr(data_, field))==float else getattr(data_, field)
    #         value = round(float(data_[field]), 2) if type(data_[field])==float else data_[field]
    #         return_list.append({'field': field,'value': value})
    return (return_list)

def ExecuteAPI(url, dateRange, filterReponse):
    SECRETS = {}
    response = []
    SECRETS = GetSecretProperties.getSecretsObj()
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    url = url + "apikey=" + p_api
    apiResponse = requests.get(f"{url}")
    data = json.loads(apiResponse.content)
    year = ""
    if filterReponse:
        for obj in data:
            year = str(obj['date']).split("-")[0]
            if (year in dateRange):
                response.append(obj)
                year=""
    else:
        response = data
    return response

def callFinPrepApi(companySymbol, apiKey, tableName):
    url = "https://financialmodelingprep.com/api/v3/"+ tableName + "/" + companySymbol + "?apikey=" + apiKey
    response = requests.get(url)
    return response.json()


def ParseDataFromAPIResponse(fields_list, data_, period, dateRange, isTTM, quarter, metricsUnit, symbol_):
    print("#### PARSING API RESPONSE ############")
    responseFileds = []
    response = []
    for field_ in fields_list:
        if 'date' == field_ or 'year' == field_ or 'id'== field_ or 'symbol' == field_ or 'company' == field_ or 'period' == field_:
            pass
        else:
            dict_={'field':field_}
            try:
                dict_['metric']=field_
                if not isTTM:
                    for x in data_:
                        filter = ""
                        if period == "Quarter":
                            if x['period'] in quarter:
                                filter = str(x['year']) + "_" + x['period'] if 'year' in fields_list else str(x['date']).split("-")[0] + "_" + x['period']
                                responseFileds.append(filter)
                        else:
                            filter = str(x['year']) if 'year' in fields_list else str(x['date']).split("-")[0]
                            responseFileds.append(filter)
                        unit = metricsUnit[field_]
                        dict_[filter] = getValueParsedByUnit(x[field_], unit)
                        dict_["unit"] = unit
                        if unit is not None and unit != "":
                            if unitSymbolDict[unit] is not None and unitSymbolDict[unit] != "":
                                unitSymbol = unitSymbolDict[unit]
                                if unitSymbol == "ccy":
                                    data = getCompanyProfile(symbol_)
                                    unitSymbol = data[0]['currency']
                                dict_['field'] = field_ + " ("+unitSymbol+")"
                        # if 'million' in unit:
                        #     try:
                        #         dict_[filter] = f'{(str(round(x[field_])/1000000, 2)):,}' if (x[field_] != None) else 0
                        #     except:
                        #         dict_[filter] = f'{(x[field_]):,}' if (x[field_] != None) else 0
                        # elif 'decimal' in unit:
                        #     try:
                        #         dict_[filter] = (str(round(x[field_], 2))) if (x[field_] != None) else 0.00
                        #     except:
                        #         dict_[filter] = (x[field_]) if (x[field_] != None) else 0.00
                        # elif 'percent' in unit:
                        #     try:
                        #         dict_[filter] = f'{(str(round(x[field_]*100, 2))+ "%")}' if (x[field_] != None) else str(0) + "%"
                        #     except:
                        #         dict_[filter] = f'{str(x[field_]*100)+ "%"}' if (x[field_] != None) else str(0) + "%"
                        # else:
                        #     dict_[filter] = (x[field_]) if (x[field_] != None) else 0
                else:
                    for obj in data_:
                        try:
                            dict_[field_] = obj[field_]
                            unit = metricsUnit[field_.replace("TTM")]
                            print(field_, unit)
                            # if 'million' in unit:
                            #     try:
                            #         dict_[field_] = f'{(str(round(obj[field_])/1000000, 2)):,}' if (obj[field_] != None) else 0
                            #     except:
                            #         dict_[field_] = f'{(obj[field_]):,}' if (obj[field_] != None) else 0
                            # elif 'decimal' in unit:
                            #     try:
                            #         dict_[field_] = (str(round(obj[field_], 2))) if (obj[field_] != None) else 0.00
                            #     except:
                            #         dict_[field_] = (obj[field_]) if (obj[field_] != None) else 0.00
                            # elif 'percent' in unit:
                            #     try:
                            #         dict_[field_] = f'{(str(round(obj[field_]*100, 2))+ "%")}' if (obj[field_] != None) else str(0) + "%"
                            #     except:
                            #         dict_[field_] = f'{str(obj[field_]*100)+ "%"}' if (obj[field_] != None) else str(0) + "%"
                            # else:
                            #     dict_[field_] = (obj[field_]) if (obj[field_] != None) else 0
                            dict_[field_] = getValueParsedByUnit(obj[field_], unit)
                            dict_["unit"] = unit
                            if unit is not None and unit != "":
                                if unitSymbolDict[unit] is not None and unitSymbolDict[unit] != "":
                                    dict_['field'] = field_ + " ("+unitSymbolDict[unit]+")"
                        except Exception:
                            pass
                    responseFileds = dateRange
            except Exception as e:
                print(e)
            response.append(dict_)
    return(response, sorted(set(responseFileds)))

def getValueParsedByUnit(value, unit):
    respValue = value
    isFloatValue = isinstance(value, float)
    if 'million' in unit and not isFloatValue:
        try:
            respValue = f'{(str(round(value)/1000000, 2)):,}' if (value != None) else 0
        except:
            respValue = f'{(value):,}' if (value != None) else 0
    elif 'percent' in unit:
        try:
            respValue = f'{(str(round(value*100, 2))+ "%")}' if (value != None) else str(0) + "%"
        except:
            respValue = f'{str(value*100)+ "%"}' if (value != None) else str(0) + "%"
    # elif 'decimal' in unit or 'monetary' in unit:
    else:
        try:
            respValue = (str(round(value, 2))) if (value != None) else 0.00
        except:
            respValue = (value) if (value != None) else 0.00
    return respValue