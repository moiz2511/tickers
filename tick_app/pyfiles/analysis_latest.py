from ast import operator
from pandas.core.indexing import convert_from_missing_indexer_tuple
import requests
import json
from django.core import serializers
import pandas as pd

from tickers.settings import GetSecretProperties
from plotly.offline import plot
from django.db import connection
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import statistics
import plotly.express as px
from sklearn.linear_model import LinearRegression
from tick_app.models import (Company,DataType,YearLimit,CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend, CustomMetrics, CustomRatios, Ranges, MetricsList, Advancedratio) 
# AnalysisTools - MetricList Table, CustomRatios - Advancedratio

store_tables = [CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend]

def getOperatorSymbol(operatorName):
    operatorName = operatorName.lower()
    if(operatorName == "plus"):
        return "+"
    elif(operatorName == "minus"):
        return "-"
    elif(operatorName == "dividedby"):
        return "/"
    elif(operatorName == "multipliedby"):
        return "*"
    return ""


def custom_function_latest(d_metrics,tool,d_companies,date_range,d_ranges, filters, yUnit):
    print("############ CUSTOM RATIOS FUNCTION TRIGGERED ###############")
    return_list=[]
    n_years=len(date_range)
    for metric in d_metrics:
        for company in d_companies:
            print("CMpNY :", company)
            _symbol=Company.objects.filter(company_name=company)
            symbol_=_symbol[0].symbol
            structuredData = customRatiosBuildQuery(company, metric, date_range, 1)
            data_l=[]
            dict_={'company_name':company,'symbol':symbol_,'metric':metric}
            print(date_range)
            for i in date_range:
                try:
                    if (yUnit == "percent"):
                        dict_[str(i)]=structuredData[str(i)][0]*100
                    else:
                        dict_[str(i)]=structuredData[str(i)][0]
                    data_l.append(structuredData[str(i)][0])
                except:
                    dict_[str(i)]= 0
                    data_l.append((0))

            print("data_l.................",data_l)
            mean_=round(sum([float(x) for x in data_l])/len(data_l),2)
            print("mean..................",mean_)
            sd=round(statistics.stdev([float(x) for x in data_l]),2)
            try:
                rsd=str(round((sd/mean_)*100,2))+'%'
            except:
                rsd="undefined"
            for metricVal in d_metrics:
                for range_ in d_ranges:
                    range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                    max_value = 0.0
                    min_value = 0.0
                    operator = "greaterthan"
                    if len(range_obj)>0:
                        try:
                            range_obj=range_obj[0]
                            max_value=range_obj.max
                            min_value=range_obj.min
                            temp_op = range_obj.operator
                            if (temp_op != None and temp_op != ""):
                                operator = temp_op.lower()
                        except:
                            pass
                    if yUnit == 'percent':
                        dict_['range']=(round((float(max_value)+float(min_value))/2, 2) * 100)
                    else:
                        dict_['range']=round((float(max_value)+float(min_value))/2, 2)
                    res_comment, res_condition  = commentHelperFunction(float(mean_), float(max_value)+float(min_value)/2, operator)
                    dict_['comment'] = res_comment
                    dict_['condition'] = res_condition
            data_l.append(mean_)
            data_l.append(sd)
            data_l.append(rsd)
            dict_['n_years']=n_years
            dict_['mean'] = mean_
            dict_['sd'] = sd
            dict_['rsd'] = rsd
            dict_['data_l']=data_l  
            return_list.append(dict_)
            print("########### FINAL RESULT OF CONDITION 1 :", return_list)

#for average industry data
    if "industryAvg" in filters or "industryMedian" in filters:
        for metric in d_metrics:
            industry_metric=[]
            for company in d_companies:
                _symbol=Company.objects.filter(company_name=company)
                symbol_=_symbol[0].symbol
                industry_=_symbol[0].industry
                if industry_ in industry_metric:
                    pass
                else:
                    industry_metric.append(industry_)
                    if "industryAvg" in filters:
                        data_l=[]
                        print("##### INDUSTRY COUNTER : "+ str(len(industry_)))
                        if 'nan' not in industry_.lower() and len(industry_)>1:
                            dict_={'company_name':f'{industry_} Average','symbol':'','metric':metric}
                            # company_data=[]
                            data_list = []
                            structuredData = customRatiosBuildQuery(company, metric, date_range, 2)
                            for i in date_range:
                                try:
                                    value = round(statistics.mean(structuredData[str(i)]), 2)
                                    dict_[str(i)]= value
                                    data_list.append(value)
                                except:
                                    dict_[str(i)]= 0
                                    data_list.append((0))
                            data_l = data_l + data_list
                            print("##### avarage industry data data_l.............",data_l)
                            mean_=round(sum([float(x) for x in data_l])/len(data_l),2)
                            print('##### avarage industry data mean________________',mean_)
                            sd=round(statistics.stdev([float(x) for x in data_l]),2)
                            try:
                                rsd= str(round((sd/mean_)*100,2))+'%'
                            except:
                                rsd="undefined"
                            for metricVal in d_metrics:
                                for range_ in d_ranges:
                                    range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                                    max_value = 0.0
                                    min_value = 0.0
                                    operator = "greaterthan"
                                    if len(range_obj)>0:
                                        try:    
                                            range_obj=range_obj[0]
                                            max_value=range_obj.max
                                            min_value=range_obj.min
                                            temp_op = range_obj.operator
                                            if (temp_op != None and temp_op != ""):
                                                operator = temp_op.lower()
                                        except:
                                            pass
                                    if yUnit == 'percent':
                                        dict_['range']=(round((float(max_value)+float(min_value))/2, 2) * 100)
                                    else:
                                        dict_['range']=round((float(max_value)+float(min_value))/2, 2)
                                    res_comment, res_condition  = commentHelperFunction(float(mean_), (float(max_value)+float(min_value))/2, operator)
                                    dict_['comment'] = res_comment
                                    dict_['condition'] = res_condition
                            data_l.append(mean_)
                            data_l.append(sd)
                            data_l.append(rsd)
                            dict_['n_years']=n_years
                            dict_['mean'] = mean_
                            dict_['sd'] = sd
                            dict_['rsd'] = rsd
                            dict_['data_l']=data_l
                            return_list.append(dict_)
                        print("######### DONE WITH INDUSTRY AVERAGE ####################")
                    #median for industry
                    if "industryMedian" in filters:
                        dict_={'company_name':f'{industry_} Median','symbol':'','metric':metric}
                        ind_median_data_l = []
                        for i in date_range:
                            try:
                                value = round(statistics.median(structuredData[str(i)]), 2)
                                dict_[str(i)]= value
                                ind_median_data_l.append(value)
                            except:
                                dict_[i]= 0
                                ind_median_data_l.append((0))
                        print("########## DATAL FOR MEDIAN OF INDUSTRY: ", ind_median_data_l)
                        mean_=round(sum([float(x) for x in ind_median_data_l])/len(ind_median_data_l),2)
                        sd=round(statistics.stdev([float(x) for x in ind_median_data_l]),2)
                        try:
                            rsd=str(round((sd/mean_)*100,2))+'%'
                        except:
                            rsd="undefined"
                        for metricVal in d_metrics:
                            for range_ in d_ranges:
                                range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                                max_value = 0.0
                                min_value = 0.0
                                operator = "greaterthan"
                                if len(range_obj)>0:
                                    try:    
                                        range_obj=range_obj[0]
                                        max_value=range_obj.max
                                        min_value=range_obj.min
                                        temp_op = range_obj.operator
                                        if (temp_op != None and temp_op != ""):
                                            operator = temp_op.lower()
                                    except:
                                        pass
                                if yUnit == 'percent':
                                    dict_['range']= (round((float(max_value)+float(min_value))/2, 2) * 100)
                                else:
                                    dict_['range']= round((float(max_value)+float(min_value))/2, 2)
                                res_comment, res_condition  = commentHelperFunction(float(mean_), (float(max_value)+float(min_value))/2, operator)
                                dict_['comment'] = res_comment
                                dict_['condition'] = res_condition
                        ind_median_data_l.append(mean_)
                        ind_median_data_l.append(sd)
                        ind_median_data_l.append(rsd)
                        dict_['n_years']=n_years
                        dict_['mean'] = mean_
                        dict_['sd'] = sd
                        dict_['rsd'] = rsd
                        dict_['data_l']=ind_median_data_l
                        return_list.append(dict_)

#for average sector data
    elif "sectorAvg" in filters or "sectorMedian" in filters:
        for metric in d_metrics:
            sector_metric=[]
            for company in d_companies:
                _symbol=Company.objects.filter(company_name=company)
                symbol_=_symbol[0].symbol
                sector_=_symbol[0].sector
                print("sector is ",sector_)
                if sector_ in sector_metric:
                    pass
                else:
                    sector_metric.append(sector_)
                    if "sectorAvg" in filters:
                        data_l=[]
                        print("LEngth Of Sector is: ", str(len(sector_)))
                        if 'nan' not in sector_.lower() and len(sector_)>1:
                            dict_={'company_name':f'{sector_} Average','symbol':'','metric':metric}
                            data_list=[]
                            structuredData = customRatiosBuildQuery(company, metric, date_range, 3)
                            print("Structure Data is: ", structuredData)
                            for i in date_range:
                                try:
                                    value = round(statistics.mean(structuredData[str(i)]), 2)
                                    dict_[str(i)]=value
                                    data_list.append(value)
                                except:
                                    dict_[i]= 0
                                    data_list.append((0))
                            data_l= data_l + data_list
                            mean_=round(sum([float(x) for x in data_l])/len(data_l),2)
                            sd=round(statistics.stdev([float(x) for x in data_l]),2)
                            try:
                                rsd=str(round((sd/mean_)*100,2))+'%'
                            except:
                                rsd="undefined"
                            for metricVal in d_metrics:
                                for range_ in d_ranges:
                                    range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                                    max_value = 0.0
                                    min_value = 0.0
                                    operator = "greaterthan"
                                    if len(range_obj)>0:
                                        try:    
                                            range_obj=range_obj[0]
                                            max_value=range_obj.max
                                            min_value=range_obj.min
                                            temp_op = range_obj.operator
                                            if (temp_op != None and temp_op != ""):
                                                operator = temp_op.lower()
                                        except:
                                            pass
                                    if yUnit == 'percent':
                                        dict_['range']=(round((float(max_value)+float(min_value))/2, 2) * 100)
                                    else:
                                        dict_['range']=round((float(max_value)+float(min_value))/2, 2)
                                    res_comment, res_condition  = commentHelperFunction(float(mean_), (float(max_value)+float(min_value))/2, operator)
                                    dict_['comment'] = res_comment
                                    dict_['condition'] = res_condition
                            data_l.append(mean_)
                            data_l.append(sd)
                            data_l.append(rsd)
                            dict_['n_years']=n_years
                            dict_['mean'] = mean_
                            dict_['sd'] = sd
                            dict_['rsd'] = rsd
                            dict_['data_l']=data_l
                            print("correct data AVERAGE SECTOR DATA: ",data_l)
                            return_list.append(dict_)
                    #median for sector
                    if "sectorMedian" in filters:
                        dict_={'company_name':f'{sector_} Median','symbol':'','metric':metric}
                        sector_median_data_l = []
                        for i in date_range:
                            try:
                                value = round(statistics.median(structuredData[str(i)]), 2)
                                dict_[str(i)]=value
                                sector_median_data_l.append(value)
                            except:
                                dict_[i]= 0
                                sector_median_data_l.append((0))
                        mean_=round(sum([float(x) for x in sector_median_data_l])/len(sector_median_data_l),2)
                        sd=round(statistics.stdev([float(x) for x in sector_median_data_l]),2)
                        try:
                            rsd=str(round((sd/mean_)*100,2))+'%'
                        except:
                            rsd="undefined"
                        for metricVal in d_metrics:
                            for range_ in d_ranges:
                                range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                                max_value = 0.0
                                min_value = 0.0
                                operator = "greaterthan"
                                if len(range_obj)>0:
                                    try:    
                                        range_obj=range_obj[0]
                                        max_value=range_obj.max
                                        min_value=range_obj.min
                                        temp_op = range_obj.operator
                                        if (temp_op != None and temp_op != ""):
                                            operator = temp_op.lower()
                                    except:
                                        pass
                                if yUnit == 'percent':
                                    dict_['range']=(round((float(max_value)+float(min_value))/2, 2) * 100)
                                else:
                                    dict_['range']=round((float(max_value)+float(min_value))/2, 2)
                                res_comment, res_condition  = commentHelperFunction(float(mean_), (float(max_value)+float(min_value))/2, operator)
                                dict_['comment'] = res_comment
                                dict_['condition'] = res_condition
                        sector_median_data_l.append(mean_)
                        sector_median_data_l.append(sd)
                        sector_median_data_l.append(rsd)
                        dict_['n_years']=n_years
                        dict_['mean'] = mean_
                        dict_['sd'] = sd
                        dict_['rsd'] = rsd
                        dict_['data_l']=sector_median_data_l
                        print("correct data MEDIAN OF SECTOR: ",sector_median_data_l)
                        return_list.append(dict_)

    print('datagot',return_list)
    return(return_list)

def analysis_function_latest(d_metrics,scat,cat,tool,d_companies,date_range,d_ranges, filters, yUnit):
    print("ranges inside function",d_ranges)
    return_list=[]
    print("metrics are", d_metrics)
    length_metric=len(d_metrics)
    n_years = len(date_range)
    # if len(d_metrics)<1:
    #     d_metrics=MetricsList.objects.filter(tool=tool).filter(measure=scat).filter(category=cat).order_by('id')
    #     d_metrics=list(([x.metrics for x in d_metrics]))
    for metric in d_metrics:
        print("### Line 619 Metric is", metric)
        industry_list=[]
        sector_list=[]
        if ((scat != None and scat != "") and (cat != None and cat != "")):
            object=(MetricsList.objects.filter(tool=tool)
                    .filter(measure=scat).filter(category=cat)
                    .filter(metric=metric))
        else:
            object=(MetricsList.objects.filter(tool=tool)
                    .filter(metric=metric))
        metric_=(object[0].source)
        print(metric_)
        global store_tables

        print(metric_.replace("tick_app_",'').replace("_",''))
        print([str(x).split("<class")[1].replace("tick_app.models.","").replace(">",'').replace(" ",'').lower() for x in store_tables])

        metric_=[x for x in store_tables if str(x).split("<class")[1].replace("'",'').replace("tick_app.models.","").replace(">",'').replace(' ','').lower()==metric_.replace("tick_app_",'').replace("_",'').lower()]
        print(metric_)
        metric_=metric_[0]
        print(metric_)
        print('company',d_companies)
        for company in d_companies:
            _symbol=Company.objects.filter(company_name=company)
            symbol_=_symbol[0].symbol
            print("symbol",symbol_)
            try:
                try:
                    data_=metric_.objects.filter(symbol=symbol_).order_by('year')
                except:
                    data_=metric_.objects.filter(symbol=symbol_).order_by('date')
            except:
                try:
                    data_=metric_.objects.filter(symbol=symbol_).order_by('year')
                except:
                    data_=metric_.objects.filter(symbol=symbol_).order_by('date')
            try:    
                filter_data=[x for x in data_ if x.year.split('-')[0] in date_range ]
                dates_available=([x.year.split('-')[0] for x in data_])
            except:
                filter_data=[x for x in data_ if x.date.split('-')[0] in date_range ]
                dates_available=([x.date.split('-')[0] for x in data_])  
            data_l=[]
            dict_={'company_name':company,'symbol':symbol_,'metric':metric}
            for i in date_range:
                if str(i) in dates_available:
                    try:
                        x=[x for x in filter_data if x.year.split('-')[0] == i][0]
                    except:
                        x=[x for x in filter_data if x.date.split('-')[0] == i][0]
                    #dict_[i]=getattr(x,metric)
                    metric_obj=MetricsList.objects.filter(metric=metric)[0]
                    unit=getattr(metric_obj,'tool').lower()
                    if 'financials' in unit:
                        try:
                            print("value obtained is",getattr(x,metric))
                            dict_[i]=str(round(getattr(x,metric)/1000000,2))+'M'
                            data_l.append(str(round(getattr(x,metric)/1000000,2))+'M')
                        except:
                            print("0 is appending M")
                            dict_[i]=str(0)+'M'
                            data_l.append(str(0)+'M')
                    else:
                        try:
                            print("value is",getattr(x,metric))
                            if yUnit == "percent":
                                dict_[i] = str(round(getattr(x,metric) * 100,2))
                            else:
                                dict_[i]=str(round(getattr(x,metric),2))
                            data_l.append(str(round(getattr(x,metric),2)))
                            print("updated data_l", data_l)
                        except:
                            print("0 is appending ")
                            dict_[i]=str(0)
                            data_l.append(str(0))
                else:
                    dict_[i]= 0
                    data_l.append(str(0))
            print("data_l..................",data_l)
            yes='no'
            for x in data_l:
                if 'M' in x:
                    yes='yes'

            mean_=round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2)
            sd=round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2)
            try:
                rsd=str(round((sd/mean_)*100,2))+'%'
            except:
                rsd="undefined"
            if yes=='yes':
                mean_= str(round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2))+'M'
                sd=str(round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2))+'M'
            print("####### IN LINE 718 ######## ")
            for metricVal in d_metrics:
                for range_ in d_ranges:
                    range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                    max_value = 0.0
                    min_value = 0.0
                    operator = "greaterthan"
                    if len(range_obj)>0:
                        try:    
                            range_obj=range_obj[0]
                            max_value=range_obj.max
                            min_value=range_obj.min
                            temp_op = range_obj.operator
                            if (temp_op != None and temp_op != ""):
                                operator = temp_op.lower()
                        except:
                            pass
                    if yUnit == 'percent':
                        dict_['range']= (round((float(max_value)+float(min_value))/2, 2) * 100)
                    else:
                        dict_['range']= round((float(max_value)+float(min_value))/2, 2)
                    leftVal = float(mean_.replace('M', '') if type(mean_) == str else mean_)
                    res_comment, res_condition  = commentHelperFunction(leftVal, (float(max_value)+float(min_value))/2, operator)
                    dict_['comment'] = res_comment
                    dict_['condition'] = res_condition
            data_l.append(mean_)
            data_l.append(sd)
            data_l.append(rsd)
            dict_['n_years']=n_years
            dict_['mean'] = mean_
            dict_['sd'] = sd
            dict_['rsd'] = rsd
            dict_['data_l']=data_l
            print("values appended",data_l)
            return_list.append(dict_)
            print("##### HERE IN LINE 750 #########")
#for average industry data
            industry_=_symbol[0].industry
            if industry_ in industry_list:
                pass
            elif "industryAvg" in filters or "industryMedian" in filters:
                print("### IN LINE 472 "+str(filters))
                industry_list.append(industry_)
                unit1=getattr(metric_obj,'tool').lower()
                if 'nan' not in industry_.lower() and len(industry_)>1: 
                    exchange_=_symbol[0].exchange
                    dict_={'company_name':f'{industry_} Average','symbol':'','metric':metric}
                    companies_i=Company.objects.filter(industry=industry_).filter(exchange=exchange_)
                    print('companies..',companies_i)
                    companies_i=[x.symbol for x in companies_i]
                if "industryAvg" in filters:
                    data_l=[]
                    metric_obj=MetricsList.objects.filter(metric=metric)[0]
                    if 'nan' not in industry_.lower() and len(industry_)>1:
                        list_data=[]
                        for c in companies_i:
                            data_list=[]
                            print("companies are_",c)
                            try:
                                dates_i=metric_.objects.filter(symbol=c).order_by('year')
                                dates_available=([x.year.split('-')[0] for x in dates_i])   
                            except:
                                dates_i=metric_.objects.filter(symbol=c).order_by('date')
                                dates_available=([x.date.split('-')[0] for x in dates_i])   
                            print("cfilter",c, dates_i)
                            for i in date_range:
                                print("#### IN LINE 772 ########")
                                if str(i) in dates_available:
                                    try:
                                        print("####### IN LINE 775 #########")
                                        x=[x for x in dates_i if x.year.split('-')[0] == i][0]
                                    except:
                                        print("####### IN LINE 778 #########")
                                        x=[x for x in dates_i if x.date.split('-')[0] == i][0]
                                    print(metric)
                                    print(x)
                                    data_list.append(getattr(x,metric))
                                else:
                                    data_list.append(0)
                            list_data.append(data_list)
                        data_avg=[]
                        print("###### IN LINE 782 ##########")
                        for i in range(len(list_data[0])):
                            sum_=0
                            for k in list_data:
                                if k[i] is None:
                                    sum_=sum_+0
                                else:
                                    sum_=sum_+k[i]
                            avg_=sum_/len(companies_i)
                            data_avg.append(avg_)

                        for j,i in enumerate(date_range):
                                if 'financials' in unit1:
                                    dict_[i]=str(round(data_avg[j]/1000000,2))+'M'
                                    data_l.append(str(round(data_avg[j]/1000000,2))+'M')
                                else:
                                    dict_[i]=str(round(data_avg[j],2))
                                    data_l.append(str(round(data_avg[j],2)))
                                    yes='no'
                        for x in data_l:
                            if 'M' in x:
                                yes='yes' 
                        mean_=round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2)
                        sd=round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2)
                        try:
                            rsd=str(round((sd/mean_)*100,2))+'%'
                        except:
                            rsd="undefined"
                        if yes=='yes':
                            mean_= str(round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2))+'M'
                            sd=str(round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2))+'M'
                        print("####### IN Line 813 #########")
                        for metricVal in d_metrics:
                            for range_ in d_ranges:
                                range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                                max_value = 0.0
                                min_value = 0.0
                                operator = "greaterthan"
                                if len(range_obj)>0:
                                    try:    
                                        range_obj=range_obj[0]
                                        max_value=range_obj.max
                                        min_value=range_obj.min
                                        temp_op = range_obj.operator
                                        if (temp_op != None and temp_op != ""):
                                            operator = temp_op.lower()
                                    except:
                                        pass
                                if yUnit == 'percent':
                                    dict_['range']= (round((float(max_value)+float(min_value))/2, 2) * 100)
                                else:
                                    dict_['range']= round((float(max_value)+float(min_value))/2, 2)
                                leftVal = float(mean_.replace('M', '') if type(mean_) == str else mean_)
                                res_comment, res_condition  = commentHelperFunction(leftVal, (float(max_value)+float(min_value))/2, operator)
                                dict_['comment'] = res_comment
                                dict_['condition'] = res_condition
                        data_l.append(mean_)
                        data_l.append(sd)
                        data_l.append(rsd)
                        dict_['n_years']=n_years
                        dict_['mean'] = mean_
                        dict_['sd'] = sd
                        dict_['rsd'] = rsd
                        dict_['data_l']=data_l
                        return_list.append(dict_)
                #median of industry
                if "industryMedian" in filters:
                    print(" ######## IN LINE 575 INDUSTRY MEDIAN ############")
                    dict_={'company_name':f'{industry_} Median','symbol':'','metric':metric}
                    list_data=[]
                    data_l=[]
                    for c in companies_i:
                        data_list=[]
                        try:
                            dates_i=metric_.objects.filter(symbol=c).order_by('year')
                            dates_available=([x.year.split('-')[0] for x in dates_i])   
                        except:
                            dates_i=metric_.objects.filter(symbol=c).order_by('date')
                            dates_available=([x.date.split('-')[0] for x in dates_i])   
                        for i in date_range:
                            if str(i) in dates_available:
                                try:
                                    x=[x for x in dates_i if x.year.split('-')[0] == i][0]
                                except:
                                    x=[x for x in dates_i if x.date.split('-')[0] == i][0]
                                data_list.append(getattr(x,metric))
                            else:
                                data_list.append(0)
                        list_data.append(data_list)
                    data_median=[]
                    for i in range(len(list_data[0])):
                        median_list=[]
                        for k in list_data:
                            if k[i] is None:
                                median_list.append(0)
                            else:
                                median_list.append(k[i])
                        median_=statistics.median(median_list)
                        data_median.append(median_)
                    for j,i in enumerate(date_range):
                        if 'financials' in unit1:
                            print("i")
                            dict_[i]=str(round(data_median[j]/1000000,2))+'M'
                            data_l.append(str(round(data_median[j]/1000000,2))+'M')
                        else:
                            dict_[i]=str(round(data_median[j],2))
                            data_l.append(str(round(data_median[j],2)))
                            yes='no'
                    print(data_l)
                    for x in data_l:
                        if 'M' in str(x):
                            yes='yes'
                    mean_=round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2)
                    sd=round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2)
                    try:
                        rsd=str(round((sd/mean_)*100,2))+'%'
                    except:
                        rsd="undefined"
                    if yes=='yes':
                        mean_= str(round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2))+'M'
                        sd=str(round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2))+'M'
                    for metricVal in d_metrics:
                        for range_ in d_ranges:
                            range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                            max_value = 0.0
                            min_value = 0.0
                            operator = "greaterthan"
                            if len(range_obj)>0:
                                try:    
                                    range_obj=range_obj[0]
                                    max_value=range_obj.max
                                    min_value=range_obj.min
                                    temp_op = range_obj.operator
                                    if (temp_op != None and temp_op != ""):
                                        operator = temp_op.lower()
                                except:
                                    pass
                            if yUnit == 'percent':
                                dict_['range']= (round((float(max_value)+float(min_value))/2, 2) * 100)
                            else:
                                dict_['range']= round((float(max_value)+float(min_value))/2, 2)
                            leftVal = float(mean_.replace('M', '') if type(mean_) == str else mean_)
                            res_comment, res_condition  = commentHelperFunction(leftVal, (float(max_value)+float(min_value))/2, operator)
                            dict_['comment'] = res_comment
                            dict_['condition'] = res_condition
                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['n_years']=n_years
                    dict_['mean'] = mean_
                    dict_['sd'] = sd
                    dict_['rsd'] = rsd
                    dict_['data_l']=data_l
                    return_list.append(dict_)
            #for average and median sector
            sector_=_symbol[0].sector
            if sector_ in sector_list:
                pass
            elif "sectorAvg" in filters or "sectorMedian" in filters:
                unit1=getattr(metric_obj,'tool').lower()
                if 'nan' not in sector_.lower() and len(sector_)>1:
                    exchange_=_symbol[0].exchange
                    dict_={'company_name':f'{sector_} Average','symbol':'','metric':metric}
                    companies_i=Company.objects.filter(sector=sector_).filter(exchange=exchange_)
                    print('companies..',companies_i)
                    companies_i=[x.symbol for x in companies_i]
                if "sectorAvg" in filters:
                    sector_list.append(sector_)
                    print('sector is ',sector_)
                    data_l=[]
                    metric_obj=MetricsList.objects.filter(metric=metric)[0]
                    if 'nan' not in sector_.lower() and len(sector_)>1:
                        list_data=[]
                        for c in companies_i:
                            data_list=[]
                            print(symbol_)
                            try:
                                dates_i=metric_.objects.filter(symbol=c).order_by('year')
                                dates_available=([x.year.split('-')[0] for x in dates_i])   
                            except:
                                dates_i=metric_.objects.filter(symbol=c).order_by('date')
                                dates_available=([x.date.split('-')[0] for x in dates_i])   
                            print("sector median cfilter",c, dates_i)
                            for i in date_range:
                                if str(i) in dates_available:
                                    try:
                                        x=[x for x in dates_i if x.year.split('-')[0] == i][0]
                                    except:
                                        x=[x for x in dates_i if x.date.split('-')[0] == i][0]
                                    data_list.append(getattr(x,metric))
                                else:
                                    data_list.append(0)
                            list_data.append(data_list)
                        data_avg=[]
                        for i in range(len(list_data[0])):
                            sum_=0
                            for k in list_data:
                                if k[i] is None:
                                    sum_=sum_+0
                                else:
                                    sum_=sum_+k[i]
                            print('sum is ',sum_, len(companies_i))
                            print("companies are ",len(companies_i))
                            avg_=sum_/len(companies_i)
                            data_avg.append(avg_)
                        for j,i in enumerate(date_range):
                                if 'financials' in unit1:
                                    dict_[i]=str(round(data_avg[j]/1000000,2))+'M'
                                    data_l.append(str(round(data_avg[j]/1000000,2))+'M')
                                else:
                                    dict_[i]=str(round(data_avg[j],2))
                                    data_l.append(str(round(data_avg[j],2)))
                                    yes='no'
                        for x in data_l:
                            if 'M' in x:
                                yes='yes' 
                        mean_=round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2)
                        sd=round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2)
                        try:
                            rsd=str(round((sd/mean_)*100,2))+'%'
                        except:
                            rsd="undefined"
                        if yes=='yes':
                            mean_= str(round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2))+'M'
                            sd=str(round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2))+'M'
                    
                        for metricVal in d_metrics:
                            for range_ in d_ranges:
                                range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                                max_value = 0.0
                                min_value = 0.0
                                operator = "greaterthan"
                                if len(range_obj)>0:
                                    try:    
                                        range_obj=range_obj[0]
                                        max_value=range_obj.max
                                        min_value=range_obj.min
                                        temp_op = range_obj.operator
                                        if (temp_op != None and temp_op != ""):
                                            operator = temp_op.lower()
                                    except:
                                        pass
                                if yUnit == 'percent':
                                    dict_['range']= (round((float(max_value)+float(min_value))/2, 2) * 100)
                                else:
                                    dict_['range']= round((float(max_value)+float(min_value))/2, 2)
                                leftVal = float(mean_.replace('M', '') if type(mean_) == str else mean_)
                                res_comment, res_condition  = commentHelperFunction(leftVal, (float(max_value)+float(min_value))/2, operator)
                                dict_['comment'] = res_comment
                                dict_['condition'] = res_condition
                        data_l.append(mean_)
                        data_l.append(sd)
                        data_l.append(rsd)
                        dict_['n_years']=n_years
                        dict_['mean'] = mean_
                        dict_['sd'] = sd
                        dict_['rsd'] = rsd
                        dict_['data_l']=data_l 
                        return_list.append(dict_)
                #median of sector
                if "sectorMedian" in filters:
                    dict_={'company_name':f'{sector_} Median','symbol':'','metric':metric}
                    list_data=[]
                    data_l=[]
                    for c in companies_i:
                        data_list=[]
                        print(symbol_)
                        try:
                            dates_i=metric_.objects.filter(symbol=c).order_by('year')
                            dates_available=([x.year.split('-')[0] for x in dates_i])   
                        except:
                            dates_i=metric_.objects.filter(symbol=c).order_by('date')
                            dates_available=([x.date.split('-')[0] for x in dates_i])   
                        print("cfilter",c, dates_i)
                        for i in date_range:
                            if str(i) in dates_available:
                                try:
                                    x=[x for x in dates_i if x.year.split('-')[0] == i][0]
                                except:
                                    x=[x for x in dates_i if x.date.split('-')[0] == i][0]
                                data_list.append(getattr(x,metric))
                            else:
                                data_list.append(0)
                        list_data.append(data_list)
                    data_median=[]
                    for i in range(len(list_data[0])):
                        median_list=[]
                        for k in list_data:
                            if k[i] is None:
                                median_list.append(0)
                            else:
                                median_list.append(k[i])
                        print(median_list)
                        median_=statistics.median(median_list)
                        data_median.append(median_)
                    for j,i in enumerate(date_range):
                            if 'financials' in unit1:
                                dict_[i]=str(round(data_median[j]/1000000,2))+'M'
                                data_l.append(str(round(data_median[j]/1000000,2))+'M')
                            else:
                                dict_[i]=str(round(data_median[j],2))
                                data_l.append(str(round(data_median[j],2)))
                                yes='no'
                    print(data_l)
                    for x in data_l:
                        if 'M' in str(x):
                            yes='yes' 
                    mean_=round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2)
                    sd=round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2)
                    try:
                        rsd=str(round((sd/mean_)*100,2))+'%'
                    except:
                        rsd="undefined"
                    if yes=='yes':
                        mean_= str(round(sum([(float(x.replace("M",''))) for x in data_l])/len(data_l),2))+'M'
                        sd=str(round(statistics.stdev([(float(x.replace("M",''))) for x in data_l]),2))+'M'
                    for metricVal in d_metrics:
                        for range_ in d_ranges:
                            range_obj=Ranges.objects.filter(metrics=metricVal).filter(name=range_)
                            max_value = 0.0
                            min_value = 0.0
                            operator = "greaterthan"
                            if len(range_obj)>0:
                                try:    
                                    range_obj=range_obj[0]
                                    max_value=range_obj.max
                                    min_value=range_obj.min
                                    temp_op = range_obj.operator
                                    if (temp_op != None and temp_op != ""):
                                        operator = temp_op.lower()
                                except:
                                    pass
                            if yUnit == 'percent':
                                dict_['range']= (round((float(max_value)+float(min_value))/2, 2) * 100)
                            else:
                                dict_['range']= round((float(max_value)+float(min_value))/2, 2)
                            leftVal = float(mean_.replace('M', '') if type(mean_) == str else mean_)
                            res_comment, res_condition  = commentHelperFunction(leftVal, (float(max_value)+float(min_value))/2, operator)
                            dict_['comment'] = res_comment
                            dict_['condition'] = res_condition
                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['n_years']=n_years
                    dict_['mean'] = mean_
                    dict_['sd'] = sd
                    dict_['rsd'] = rsd
                    dict_['data_l']=data_l   
                    return_list.append(dict_)
    print('datagot',return_list)
    return(return_list)

def quote_latest(p_symbol, p_company, from_, to_):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    response=requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{p_symbol}?serietype=line&apikey={p_api}&from="+str(from_)+"-01-01&to="+str(to_)+"-12-31")
    data=json.loads(response.content)
    try:
        if 'Invalid API' in data['Error Message']:
            print("error api")
            return ('api error')
        else:
            return ('other error')
    except:
        # print(data)
        data=data['historical']
        data=data[::-1]
        df=pd.DataFrame(data)
        df['Company']=p_company
        df['Symbol']=p_symbol
        date_range=list(range(int(from_),int(to_)+1))
        date_range=[str(x) for x in date_range]

        # df['Filter']=df['date'].apply(lambda x:'yes' if str(x).split('-')[0] in date_range else 'no')

        # print("df got", df.head())
        # print(len(df))

        # df=df[df['Filter']=='yes']
        # df.drop('Filter', axis=1, inplace=True)
        # df['Legend']=df['Company'].apply(lambda x:f"{x} Close price")
        reg_df=df.copy()

        regressor = LinearRegression()
        x=np.array(pd.to_datetime(reg_df['date']).values.reshape(-1,1), dtype='float')
        y=reg_df['close'].values.reshape(-1,1)

        regressor.fit(x,y)

        reg_df['close']=regressor.predict(x).reshape(1,-1)[0]
        # reg_df['Legend']=reg_df['Company'].apply(lambda x:f"{x} Regression")
        eplison_list=[x-2 for x in list(reg_df['close'])]
        eplison=sum(eplison_list)/len(eplison_list)

        standard_deviation_minus_2=[x-(2*eplison) for x in list(reg_df['close'])]
        standard_deviation_minus=[x-(1*eplison) for x in list(reg_df['close'])]
        standard_deviation_plus_2=[x+(2*eplison) for x in list(reg_df['close'])]
        standard_deviation_plus=[x+(1*eplison) for x in list(reg_df['close'])]

        ecart_df_minus_2=reg_df. copy()
        ecart_df_minus_2['close']=standard_deviation_minus_2
        # ecart_df_minus_2['Legend']=ecart_df_minus_2['Company'].apply(lambda x:f"{x} 2 Standard Deviation -")

        ecart_df_minus=reg_df. copy()
        ecart_df_minus['close']=standard_deviation_minus
        # ecart_df_minus['Legend']=ecart_df_minus['Company'].apply(lambda x:f"{x} Standard Deviation -")

        ecart_df_plus_2=reg_df. copy()
        ecart_df_plus_2['close']=standard_deviation_plus_2
        # ecart_df_plus_2['Legend']=ecart_df_plus_2['Company'].apply(lambda x:f"{x} 2 Standard Deviation +")

        ecart_df_plus=reg_df. copy()
        ecart_df_plus['close']=standard_deviation_plus
        # ecart_df_plus['Legend']=ecart_df_plus['Company'].apply(lambda x:f"{x} Standard Deviation +")
        final_df=[{"resp_dates": df['date'],"close_price": df['close'],"regression_values": reg_df['close'], "standardDevMinus": ecart_df_minus['close'], "standardDevPlusTwo": ecart_df_plus_2['close'], "standardDevPlus": ecart_df_plus['close'], "standardDevMinusTwo": ecart_df_minus_2['close']}]

    return (df, final_df)

def customRatiosBuildQuery(company, metric, date_range, customType):
    _symbol=Company.objects.filter(company_name=company)
    symbol_=_symbol[0].symbol
    c_industry=_symbol[0].industry
    c_exchange=_symbol[0].exchange
    c_sector=_symbol[0].sector
    print(symbol_)
    advMetricDataResp = Advancedratio.objects.filter(metric=metric)
    advMetricData = advMetricDataResp[0]
    print("#### ADVANCED RATIO METRIC INFO #####")
    print(advMetricData)
    advCondition = ""
    advMetricTable = {}
    nonEmptyItems = tuple()
    counter = 3
    newQuery = """SELECT A.symbol, A.company_name, A.exchange, A.sector, A.industry, A.country,
        avgMetricFilters FROM tick_app_company as A """
    if (advMetricData.item1 is not None and advMetricData.item1 != "") and (advMetricData.operator1 is not None and advMetricData.operator1 != "") and (advMetricData.item2 is not None and advMetricData.item2 != ""):
        advCondition += "round(((((item1Table." + advMetricData.item1 + getOperatorSymbol(advMetricData.operator1) + "item2Table." + advMetricData.item2 + ")"
        nonEmptyItems += (advMetricData.item1, advMetricData.item2,)
        advMetricTable['item1Table'] = advMetricData.item1
        advMetricTable['item2Table'] = advMetricData.item2
    if (advMetricData.item3 is not None and advMetricData.item3 != "") and (advMetricData.operator2 is not None and advMetricData.operator2 != ""):
        advCondition += getOperatorSymbol(advMetricData.operator2) + "item3Table." + advMetricData.item3 + ")"
        nonEmptyItems += (advMetricData.item3,)
        advMetricTable['item3Table'] = advMetricData.item3
        counter -= 1
    if (advMetricData.item4 is not None and advMetricData.item4 != "") and (advMetricData.operator3 is not None and advMetricData.operator3 != ""):
        advCondition += getOperatorSymbol(advMetricData.operator3) + "item4Table." + advMetricData.item4 + ")"
        nonEmptyItems += (advMetricData.item4,)
        advMetricTable['item4Table'] = advMetricData.item4
        counter -= 1
    if (advMetricData.item5 is not None and advMetricData.item5 != "") and (advMetricData.operator4 is not None and advMetricData.operator4 != ""):
        advCondition += getOperatorSymbol(advMetricData.operator4) + "item5Table." + advMetricData.item5 + ")"
        nonEmptyItems += (advMetricData.item5,)
        advMetricTable['item5Table'] = advMetricData.item5
        counter -= 1
    if(advCondition.strip() != ""):
        while counter > 0:
            advCondition +=")"
            counter -= 1
        advCondition += ", 2) as " + metric
    print(advCondition)
    query = "SELECT * FROM tick_app_metricslist WHERE metric in " + str(nonEmptyItems)
    cursor = connection.cursor()
    cursor.execute(query)
    fields = [field_md[0] for field_md in cursor.description]
    AdvMetricResult = [dict(zip(fields, row)) for row in cursor.fetchall()]
    resultDict = {}
    metricTableDict = {}
    for advMetric in AdvMetricResult:
        advDataSource =  advMetric['source']
        if advDataSource in resultDict.keys():
            resultDict[advDataSource] = resultDict[advDataSource] + ""
            metricTableDict[advMetric['metric']] = advDataSource
        else:
            metricTableDict[advMetric['metric']] = advDataSource
            resultDict[advDataSource] = " inner join " + advDataSource + " as " + advDataSource + " on A.symbol=" + advDataSource + ".symbol "
    advMetricsList = list(advMetricTable.values())
    print(advMetricsList)
    # if(customType == 4):
    #     advCondition = advCondition.replace("IsCalcMetricAvg", "avg")
    #     advWhereCondition = " where A.industry = '" + c_industry + "' and A.sector = '" + c_sector + "' and A.exchange = " + c_exchange + "' and "
    if(customType == 3):
        # advCondition = advCondition.replace("IsCalcMetricAvg", "avg")
        advWhereCondition = " where A.sector = '" + c_sector + "' and A.exchange = '" + c_exchange + "' and "
    elif(customType == 2):
        # advCondition = advCondition.replace("IsCalcMetricAvg", "avg")
        advWhereCondition = " where A.industry = '" + c_industry + "' and A.exchange = '" + c_exchange + "' and "
    else:
        # advCondition = advCondition.replace("IsCalcMetricAvg", "")
        advWhereCondition = " where A.symbol ='" + symbol_ + "' and "
    if(len(advMetricsList) > 1):
        yearMetricTableList = []
        previousMetricCond = ""
        count = 1
        for advMetric in advMetricsList:
            if advMetric not in yearMetricTableList:
                if count < 3:
                    advWhereCondition += "year(" + metricTableDict[advMetric] + ".date) = "
                else:
                    advWhereCondition = advWhereCondition.rstrip().rstrip("=")
                    advWhereCondition += previousMetricCond + "year(" + metricTableDict[advMetric] + ".date)"
                if count == 1:
                    previousMetricCond = " and year(" + metricTableDict[advMetric] + ".date) = "
                yearMetricTableList.append(advMetric)
                count += 1
        advWhereCondition = advWhereCondition.rstrip().rstrip("=")
    advCondition += ", year(" + metricTableDict[advMetricsList[0]] + ".date) as year"
    newQuery = newQuery.replace("avgMetricFilters", advCondition)
    advWhereCondition +=  " and year(" + metricTableDict[advMetricsList[0]] + ".date) in " + str(tuple(date_range)) + " group by symbol, year;"
    print("#### QUERY AFTER AVGMetricFilters ", newQuery)
    for metricTab in resultDict.values():
        newQuery += metricTab
    newQuery += advWhereCondition    
    if('item1Table.' in newQuery):
        newQuery = newQuery.replace("item1Table.", metricTableDict[advMetricTable['item1Table']] + ".")
    if('item2Table.' in newQuery):
        newQuery = newQuery.replace("item2Table.", metricTableDict[advMetricTable['item2Table']] + ".")
    if('item3Table.' in newQuery):
        newQuery = newQuery.replace("item3Table.", metricTableDict[advMetricTable['item3Table']] + ".")
    if('item4Table.' in newQuery):
        newQuery = newQuery.replace("item4Table.", metricTableDict[advMetricTable['item4Table']] + ".")
    if('item5Table.' in newQuery):
        newQuery = newQuery.replace("item5Table.", metricTableDict[advMetricTable['item5Table']] + ".")
    print("####### NEW QUERY CONSTRUCTED FOR CUSTOM RATIOS CONDITION1 ", newQuery)
    cursor = connection.cursor()
    cursor.execute(newQuery)
    fields = [field_md[0] for field_md in cursor.description]
    advQueryResult = [dict(zip(fields, row)) for row in cursor.fetchall()]
    # print(advQueryResult)
    structuredData = {}
    for res in advQueryResult:
        if str(res['year']) in structuredData.keys():
            structuredData[str(res['year'])].append(res[metric])
        else:
            structuredData[str(res['year'])] = []
            structuredData[str(res['year'])].append(res[metric])
    print("########### restructured data: ", structuredData)
    return structuredData

def commentHelperFunction(value, range, operator):
    finalRes = "Equal"
    condition = True
    if(operator == "greaterthanorequal"):
        if(value >= range):
            finalRes = "Above"
            condition = True
        else:
            finalRes = "Below"
            condition = False
    elif(operator == "lessthan"):
        if(value < range):
            finalRes = "Below"
            condition = True
        else:
            finalRes = "Above"
            condition = False
    elif(operator == "lessthanorequal"):
        if(value <= range):
            finalRes = "Below"
            condition = True
        else:
            finalRes = "Above"
            condition = False
    else:
        if(value > range):
            finalRes = "Above"
            condition = True
        else:
            finalRes = "Below"
            condition = False
    if(value == range):
        finalRes = "Equal"
    return finalRes, condition
