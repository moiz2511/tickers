

from pandas.core.indexing import convert_from_missing_indexer_tuple
import requests
import json
from django.core import serializers
import pandas as pd

from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import statistics
import plotly.express as px
from sklearn.linear_model import LinearRegression





from tick_app.models import (Company,DataType,YearLimit,CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend,AnalysisTools, CustomMetrics, CustomRatios, Ranges)

store_tables = [CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend]

def custom_function(d_metrics,scat,cat,tool,d_companies,date_range,d_ranges):
    return_list=[]
    length_metric=len(d_metrics)
    n_years=len(date_range)
    for metric in d_metrics:

        object=(CustomRatios.objects.filter(measure=scat).filter(category=cat)
                .filter(metrics=metric))
        print("object.....................",object[0])
        numerator_=(object[0].numerator)
        denominator_=(object[0].denominator)
        numerator_source=CustomMetrics.objects.filter(metrics=numerator_)[0].source
        print("object.....................",numerator_source)
        try:
            denominator_source=CustomMetrics.objects.filter(metrics=denominator_)[0].source
        except:
            denominator_source=CustomMetrics.objects.filter(metrics=numerator_)[0].source

        print(numerator_source, denominator_source)
        global store_tables
        print(numerator_source.replace("tick_app_",'').replace("_",''))
        print([str(x).split("<class")[1].replace("tick_app.models.","").replace(">",'').replace(" ",'').lower() for x in store_tables])
        numerator_metric=[x for x in store_tables if str(x).split("<class")[1].replace("'",'').replace("tick_app.models.","").replace(">",'').replace(' ','').lower()==numerator_source.replace("tick_app_",'').replace("_",'')]
        numerator_metric=numerator_metric[0]
        print(numerator_metric)
        denominator_metric=[x for x in store_tables if str(x).split("<class")[1].replace("'",'').replace("tick_app.models.","").replace(">",'').replace(' ','').lower()==denominator_source.replace("tick_app_",'').replace("_",'')]
        denominator_metric=denominator_metric[0]
        print(denominator_)
        print('company',d_companies)
        for company in d_companies:
            print("CMpNY :", company)
            _symbol=Company.objects.filter(company_name=company)
            symbol_=_symbol[0].symbol
            print(symbol_)


            numerator_data=numerator_metric.objects.filter(symbol=symbol_).order_by('date')
            denominator_data=denominator_metric.objects.filter(symbol=symbol_).order_by('date')


            numerator_data=[x for x in numerator_data if x.date.split('-')[0] in date_range ]
            denominator_data=[x for x in denominator_data if x.date.split('-')[0] in date_range ]

            data_=[]
            for i in numerator_data:
                for j in denominator_data:
                    if i.date==j.date and i.symbol == j.symbol:
                       
                        if float(getattr(j,denominator_)) == 0:
                            print(float(getattr(j,denominator_)))
                            data_.append({'date':i.date, 'value':0})
                        else:

                    
                            data_.append({'date':i.date, 'value':round(float(getattr(i,numerator_))/float(getattr(j,denominator_)),2)})

            print(data_)
            filter_data=[x for x in data_ if x['date'].split('-')[0] in date_range ]
            dates_available=([x['date'].split('-')[0] for x in data_]) 
            data_l=[]
            dict_={'company_name':company,'symbol':symbol_,'metric':metric}
            print(filter_data)
            
            for i in date_range:
                print(i,dates_available)
                if str(i) in dates_available:

                    x=[x for x in filter_data if x['date'].split('-')[0] == i][0]

                    print("x.................",x)
            
                    dict_[i]=x['value']
                    data_l.append(x['value'])
            
                else:
                    dict_[i]= 0
                    data_l.append((0))

            print("data_l.................",data_l)
            mean_=round(sum([float(x) for x in data_l])/len(data_l),2)
            print("mean..................",mean_)
            sd=round(statistics.stdev([float(x) for x in data_l]),2)
            try:
                rsd=str(round((sd/mean_)*100,2))+'%'
            except:
                rsd="undefined"
            data_l.append(mean_)
            data_l.append(sd)
            data_l.append(rsd)
            dict_['data_l']=data_l
                
            return_list.append(dict_)

#for average industry data
    
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
            
                data_l=[]

                object=(CustomRatios.objects.filter(measure=scat).filter(category=cat)
                        .filter(metrics=metric))
                print(object)
                numerator_=(object[0].numerator)
                denominator_=(object[0].denominator)
                numerator_source=CustomMetrics.objects.filter(metrics=numerator_)[0].source
                try:
                    denominator_source=CustomMetrics.objects.filter(metrics=denominator_)[0].source
                except:
                    denominator_source=CustomMetrics.objects.filter(metrics=numerator_)[0].source

                print(numerator_source, denominator_source)

                if 'nan' not in industry_.lower() and len(industry_)>1: 
            
                    exchange_=_symbol[0].exchange
                    dict_={'company_name':f'{industry_} Average','symbol':'','metric':metric}
                    
                    companies_i=Company.objects.filter(industry=industry_).filter(exchange=exchange_)
                    print('companies..',companies_i)
                    companies_i=[x.symbol for x in companies_i]
                    list_data=[]
                    company_data=[]

                    for c in companies_i:
                        data_list=[]


                        print("companies are_",c)
                        try:
                            numerator_data=numerator_metric.objects.filter(symbol=c).order_by('date')
                            denominator_data=denominator_metric.objects.filter(symbol=c).order_by('date')
                        except:
                            numerator_data=numerator_metric.objects.filter(symbol=c).order_by('year')
                            denominator_data=denominator_metric.objects.filter(symbol=c).order_by('year')

                        try:

                            numerator_data=[x for x in numerator_data if x.date.split('-')[0] in date_range ]
                            denominator_data=[x for x in denominator_data if x.date.split('-')[0] in date_range ]
                        except:
                            numerator_data=[x for x in numerator_data if x.year.split('-')[0] in date_range ]
                            denominator_data=[x for x in denominator_data if x.year.split('-')[0] in date_range ]
                        data_=[]
                        for i in numerator_data:
                            for j in denominator_data:
                                if i.date==j.date and i.symbol == j.symbol:
                                
                                    if float(getattr(j,denominator_)) == 0:
                                        print(float(getattr(j,denominator_)))
                                        data_.append({'date':i.date, 'value':0})
                                    else:

                                
                                        data_.append({'date':i.date, 'value':round(float(getattr(i,numerator_))/float(getattr(j,denominator_)),2)})

                        print(data_)
                        filter_data=[x for x in data_ if x['date'].split('-')[0] in date_range ]
                        dates_available=([x['date'].split('-')[0] for x in data_]) 
                        data_c=[]
                        print(filter_data)
                        
                        for i in date_range:
                            print(i,dates_available)
                            if str(i) in dates_available:

                                x=[x for x in filter_data if x['date'].split('-')[0] == i][0]

                                print(x)
                        
                                dict_[i]=x['value']
                                data_list.append(x['value'])
                        
                            else:
                                dict_[i]= 0
                                data_list.append((0))
                        company_data.append(data_list)

                try:
                        
                    data_avg=[]
                    for i in range(len(company_data[0])):
                        sum_=0
                        for k in company_data:
                            print(f'values are for year {i} is {k[i]} ')
                            if k[i] is None:
                                sum_=sum_+0
                            else:
                            
                                sum_=sum_+k[i]


                        avg_=sum_/len(companies_i)
                        data_avg.append(round(avg_,2))
                    data_l=data_avg
                    print("data_l.............",data_l)
                    print("avg............",avg_)
                    for j,i in enumerate(date_range):
                        print(i,dates_available)

                
                        dict_[i]=data_l[j]
                
                    
                    

                    
                    mean_=round(sum([float(x) for x in data_l])/len(data_l),2)
                    print('mean________________',mean_)

                    sd=round(statistics.stdev([float(x) for x in data_l]),2)

                
                    try:
                        rsd= str(round((sd/mean_)*100,2))+'%'
                    except:
                        rsd="undefined"


                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['data_l']=data_l
                    print("correct data",data_l)
                    
                    
                        
                    return_list.append(dict_)

    #median for industry
                    dict_={'company_name':f'{industry_} Median','symbol':'','metric':metric}
                    
                    data_med=[]
                    for i in range(len(company_data[0])):
                        med_=[]
                        for k in company_data:
                            print(f'values are for year {i} is {k[i]} ')
                            if k[i] is None:
                                med_.append(0)
                            else:
                                med_.append(k[i])
                        median_=statistics.median(med_)
                        data_med.append(round(median_,2))
                            
                                


    
                    data_l=data_med
                    for j,i in enumerate(date_range):
                        print(i,dates_available)

                
                        dict_[i]=data_l[j]
                        
                
                    
                    

                    
                    mean_=round(sum([float(x) for x in data_l])/len(data_l),2)

                    sd=round(statistics.stdev([float(x) for x in data_l]),2)

                
                    try:
                        rsd=str(round((sd/mean_)*100,2))+'%'
                    except:
                        rsd="undefined"


                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['data_l']=data_l
                    print("correct data",data_l)
                    
                    
                        
                    return_list.append(dict_)
                except:
                    pass



#for average sector data
    
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
            
                data_l=[]

                object=(CustomRatios.objects.filter(measure=scat).filter(category=cat)
                        .filter(metrics=metric))
                print(object)
                numerator_=(object[0].numerator)
                denominator_=(object[0].denominator)
                numerator_source=CustomMetrics.objects.filter(metrics=numerator_)[0].source
                try:
                    denominator_source=CustomMetrics.objects.filter(metrics=denominator_)[0].source
                except:
                    denominator_source=CustomMetrics.objects.filter(metrics=numerator_)[0].source

                print(numerator_source, denominator_source)

                if 'nan' not in sector_.lower() and len(sector_)>1: 
            
                    exchange_=_symbol[0].exchange
                    dict_={'company_name':f'{sector_} Average','symbol':'','metric':metric}
                    
                    companies_i=Company.objects.filter(sector=sector_).filter(exchange=exchange_)
                    print('companies..',companies_i)
                    companies_i=[x.symbol for x in companies_i]
                    list_data=[]
                    company_data=[]

                    for c in companies_i:
                        data_list=[]


                        print("companies are__",c)
                        try:
                            numerator_data=numerator_metric.objects.filter(symbol=c).order_by('date')
                            denominator_data=denominator_metric.objects.filter(symbol=c).order_by('date')
                        except:
                            numerator_data=numerator_metric.objects.filter(symbol=c).order_by('year')
                            denominator_data=denominator_metric.objects.filter(symbol=c).order_by('year')

                        try:

                            numerator_data=[x for x in numerator_data if x.date.split('-')[0] in date_range ]
                            denominator_data=[x for x in denominator_data if x.date.split('-')[0] in date_range ]
                        except:
                            numerator_data=[x for x in numerator_data if x.year.split('-')[0] in date_range ]
                            denominator_data=[x for x in denominator_data if x.year.split('-')[0] in date_range ]
                        data_=[]
                        for i in numerator_data:
                            for j in denominator_data:
                                if i.date==j.date and i.symbol == j.symbol:
                                
                                    if float(getattr(j,denominator_)) == 0:
                                        print(float(getattr(j,denominator_)))
                                        data_.append({'date':i.date, 'value':0})
                                    else:

                                
                                        data_.append({'date':i.date, 'value':round(float(getattr(i,numerator_))/float(getattr(j,denominator_)),2)})

                        print(data_)
                        filter_data=[x for x in data_ if x['date'].split('-')[0] in date_range ]
                        dates_available=([x['date'].split('-')[0] for x in data_]) 
                        data_c=[]
                        print(filter_data)
                        
                        for i in date_range:
                            print(i,dates_available)
                            if str(i) in dates_available:

                                x=[x for x in filter_data if x['date'].split('-')[0] == i][0]

                                print(x)
                        
                                dict_[i]=x['value']
                                data_list.append(x['value'])
                        
                            else:
                                dict_[i]= 0
                                data_list.append((0))
                        company_data.append(data_list)


                data_avg=[]
                try:
                        
                    for i in range(len(company_data[0])):
                        sum_=0
                        for k in company_data:
                            print(f'values are for year {i} is {k[i]} ')
                            if k[i] is None:
                                sum_=sum_+0
                            else:
                            
                                sum_=sum_+k[i]


                        avg_=sum_/len(companies_i)
                        data_avg.append(round(avg_,2))
                    data_l=data_avg
                    for j,i in enumerate(date_range):
                        print(i,dates_available)

                
                        dict_[i]=data_l[j]
                
                    
                    

                    
                    mean_=round(sum([float(x) for x in data_l])/len(data_l),2)

                    sd=round(statistics.stdev([float(x) for x in data_l]),2)

                
                    try:
                        rsd=str(round((sd/mean_)*100,2))+'%'
                    except:
                        rsd="undefined"


                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['data_l']=data_l
                    print("correct data",data_l)
                    
                    
                        
                    return_list.append(dict_)


    #median for sector
                    dict_={'company_name':f'{sector_} Median','symbol':'','metric':metric}
                    
                    data_med=[]
                    for i in range(len(company_data[0])):
                        med_=[]
                        for k in company_data:
                            print(f'values are for year {i} is {k[i]} ')
                            if k[i] is None:
                                med_.append(0)
                            else:
                                med_.append(k[i])
                        median_=statistics.median(med_)
                        data_med.append(round(median_,2))
                            
                                


    
                    data_l=data_med
                    for j,i in enumerate(date_range):
                        print(i,dates_available)

                
                        dict_[i]=data_l[j]
                        
                
                    
                    

                    
                    mean_=round(sum([float(x) for x in data_l])/len(data_l),2)

                    sd=round(statistics.stdev([float(x) for x in data_l]),2)

                
                    try:
                        rsd=str(round((sd/mean_)*100,2))+'%'
                    except:
                        rsd="undefined"


                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['data_l']=data_l
                    print("correct data",data_l)
                    
                    
                        
                    return_list.append(dict_)
                except:
                    pass













    company_l=[]
    symbol_l=[]
    year_l=[]
    metrics_l=[]
    value_l=[]
    colors_l=[]
    print('datagot',return_list)
    for i in return_list:
        for j in date_range:
            company_l.append(i['company_name'])
            symbol_l.append(i['symbol'])
            year_l.append(j)
            value_l.append(i[j])
            colors_l.append(f"{i['company_name']} {i['metric']}")
    
            metrics_l.append(i['metric'])

    df = pd.DataFrame({
        "Company": company_l,
        "Year":year_l,
        "Value": value_l,
        "Legend": colors_l,
        "Metrics": metrics_l
    })
    fig_bar = px.bar(df, x="Year", y="Value", color="Legend",hover_name="Company", barmode='group')

    _graphs=[]
    _graphs.append(df)
    for metric in d_metrics:
        for range_ in d_ranges:
            range_obj=Ranges.objects.filter(metrics=metric).filter(name=range_)
            if len(range_obj)>0:
                try:    
                    range_obj=range_obj[0]
                    max_value=range_obj.max
                    min_value=range_obj.min
                    if float(max_value) == float(min_value):

                        df_range = pd.DataFrame({
                                
                                "Year":date_range,
                                "Company": '',
                                "Value": max_value,
                                "Legend": f'{range_} {metric}',
                                "Metrics": metric
                            })
                        _graphs.append(df_range)
                    else:
                        df_range = pd.DataFrame({
                                
                                "Year":date_range,
                                "Company": '',
                                "Value": max_value,
                                "Legend": f'{range_} {metric} Max',
                                "Metrics": metric
                            })
                        _graphs.append(df_range)

                        df_range = pd.DataFrame({
                                
                                "Year":date_range,
                                "Company": '',
                                "Value": min_value,
                                "Legend": f'{range_} {metric} Min',
                                "Metrics": metric
                            })
                        _graphs.append(df_range)
                except:
                    pass                        

                        

        
        df=pd.concat(_graphs)




    fig_line = px.line(df, x="Year", y="Value", color="Legend",hover_name="Company")
    


    fig_line.update_layout(plot_bgcolor='rgb(255,255,255)')
    fig_line.update_xaxes(showline=True, linecolor='grey')
    fig_line.update_yaxes(showline=True, linecolor='grey')
    fig_line.update_xaxes(gridwidth=0.0001, gridcolor='#F1F1F1')
    fig_line.update_yaxes(gridwidth=0.01, gridcolor='#F1F1F1')
    
    fig_line.update_layout(legend=dict(
        orientation="v",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))
    fig_line.update_layout(legend_title_text='')




    fig_bar.update_layout(plot_bgcolor='rgb(255,255,255)')
    fig_bar.update_xaxes(showline=True, linecolor='grey')
    fig_bar.update_yaxes(showline=True, linecolor='grey')
    fig_bar.update_xaxes(gridwidth=0.0001, gridcolor='#F1F1F1')
    fig_bar.update_yaxes(gridwidth=0.01, gridcolor='#F1F1F1')
    
    fig_bar.update_layout(legend=dict(
        orientation="v",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))
    fig_bar.update_layout(legend_title_text='')

    


    

    plt_line = plot(fig_line, output_type='div',show_link=False,include_plotlyjs=False)
    plt_bar = plot(fig_bar, output_type='div',show_link=False,include_plotlyjs=False)




    return(return_list,plt_bar,plt_line)







def analysis_function(d_metrics,scat,cat,tool,d_companies,date_range,d_ranges):


    print("ranges inside function",d_ranges)
    return_list=[]
    print("metrics are", d_metrics)
    length_metric=len(d_metrics)

    if len(d_metrics)<1:
        d_metrics=AnalysisTools.objects.filter(tools=tool).filter(super_category=scat).filter(category=cat).order_by('id')
        d_metrics=list(([x.metrics for x in d_metrics]))
 


    
    for metric in d_metrics:
        industry_list=[]
        sector_list=[]


        
        object=(AnalysisTools.objects.filter(tools=tool)
                .filter(super_category=scat).filter(category=cat)
                .filter(metrics=metric))
        print(tool,scat,cat,metric,object)
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
              
                    metric_obj=AnalysisTools.objects.filter(metrics=metric)[0]
                    print(getattr(metric_obj,'metrics'), getattr(metric_obj,'unit1'))
                    unit1=getattr(metric_obj,'unit1')
                    unit2=getattr(metric_obj,'unit2')
               
                    if 'millions' in unit1:
                    
                        try:
                            print("value obtained is",getattr(x,metric))
                            dict_[i]=str(round(getattr(x,metric)/1000000,2))+'M'
                            data_l.append(str(round(getattr(x,metric)/1000000,2))+'M')
                        except:
                            print("0 is appending M")
                            dict_[i]=str(0)+'M'
                            data_l.append(str(0)+'M')
                    elif 'decimals' in unit2:
                        try:
                            print("value is",getattr(x,metric))
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

            data_l.append(mean_)
            data_l.append(sd)
            data_l.append(rsd)
            dict_['data_l']=data_l
            print("values appended",data_l)
                
            return_list.append(dict_)




#for average industry data



            
            industry_=_symbol[0].industry
            if industry_ in industry_list:
                pass
            else:
                industry_list.append(industry_)
                data_l=[]
                metric_obj=AnalysisTools.objects.filter(metrics=metric)[0]
                print(getattr(metric_obj,'metrics'), getattr(metric_obj,'unit1'))
                unit1=getattr(metric_obj,'unit1')
                unit2=getattr(metric_obj,'unit2')

                if 'nan' not in industry_.lower() and len(industry_)>1: 
            
                    exchange_=_symbol[0].exchange
                    dict_={'company_name':f'{industry_} Average','symbol':'','metric':metric}
                    
                    companies_i=Company.objects.filter(industry=industry_).filter(exchange=exchange_)
                    print('companies..',companies_i)
                    companies_i=[x.symbol for x in companies_i]
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
                            print(f'values are for year {i} is {k[i]} ')
                            if k[i] is None:
                                sum_=sum_+0
                            else:
                            
                                sum_=sum_+k[i]


                        avg_=sum_/len(companies_i)
                        data_avg.append(avg_)

                    for j,i in enumerate(date_range):
                            if 'millions' in unit1:
                            
                                dict_[i]=str(round(data_avg[j]/1000000,2))+'M'
                                data_l.append(str(round(data_avg[j]/1000000,2))+'M')
                            elif 'decimals' in unit2:
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

                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['data_l']=data_l
                    
                    
                        
                    return_list.append(dict_)

    #median of industry


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
                            print(f'values are for year {i} is {k[i]} ')
                            if k[i] is None:
                                median_list.append(0)
                            else:
                            
                                median_list.append(k[i])



                        median_=statistics.median(median_list)
                        data_median.append(median_)

                    for j,i in enumerate(date_range):
                            if 'millions' in unit1:
                                print("i")
                                dict_[i]=str(round(data_median[j]/1000000,2))+'M'
                                data_l.append(str(round(data_median[j]/1000000,2))+'M')
                            elif 'decimals' in unit2:
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

                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['data_l']=data_l
                        
                    return_list.append(dict_)


            








            #for average and median sector

            sector_=_symbol[0].sector
            if sector_ in sector_list:
                pass
            else:
                sector_list.append(sector_)
                print('sector is ',sector_)
                data_l=[]
                metric_obj=AnalysisTools.objects.filter(metrics=metric)[0]
                print(getattr(metric_obj,'metrics'), getattr(metric_obj,'unit1'))
                unit1=getattr(metric_obj,'unit1')
                unit2=getattr(metric_obj,'unit2')

                if 'nan' not in sector_.lower() and len(sector_)>1: 
            
                    exchange_=_symbol[0].exchange
                    dict_={'company_name':f'{sector_} Average','symbol':'','metric':metric}
                    
                    companies_i=Company.objects.filter(sector=sector_).filter(exchange=exchange_)
                    print('companies..',companies_i)
                    companies_i=[x.symbol for x in companies_i]
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
                    data_avg=[]
                    for i in range(len(list_data[0])):
                        sum_=0
                        for k in list_data:
                            print(f'values are for year {i} is {k[i]} ')
                            if k[i] is None:
                                sum_=sum_+0
                            else:
                            
                                sum_=sum_+k[i]

                        print('sum is ',sum_, len(companies_i))
                        print("companies are ",len(companies_i))
                        avg_=sum_/len(companies_i)
                        data_avg.append(avg_)

                    for j,i in enumerate(date_range):
                            if 'millions' in unit1:
                                print("i")
                                dict_[i]=str(round(data_avg[j]/1000000,2))+'M'
                                data_l.append(str(round(data_avg[j]/1000000,2))+'M')
                            elif 'decimals' in unit2:
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

                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['data_l']=data_l
                        
                    return_list.append(dict_)

    #median of sector


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
                            print(f'values are for year {i} is {k[i]} ')
                            if k[i] is None:
                                median_list.append(0)
                            else:
                            
                                median_list.append(k[i])



                        median_=statistics.median(median_list)
                        data_median.append(median_)

                    for j,i in enumerate(date_range):
                            if 'millions' in unit1:
                                print("i")
                                dict_[i]=str(round(data_median[j]/1000000,2))+'M'
                                data_l.append(str(round(data_median[j]/1000000,2))+'M')
                            elif 'decimals' in unit2:
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

                    data_l.append(mean_)
                    data_l.append(sd)
                    data_l.append(rsd)
                    dict_['data_l']=data_l
                        
                    return_list.append(dict_)


                






            

            


                    






            
    
    company_l=[]
    symbol_l=[]
    year_l=[]
    metrics_l=[]
    value_l=[]
    colors_l=[]
    _graphs=[]
    print('datagot',return_list)
    for i in return_list:
        for j in date_range:
            company_l.append(i['company_name'])
            symbol_l.append(i['symbol'])
            year_l.append(j)
            value_l.append(i[j])
            colors_l.append(f"{i['company_name']} {i['metric']}")
    
            metrics_l.append(i['metric'])

    df = pd.DataFrame({
        "Company": company_l,
        "Year":year_l,
        "Value": value_l,
        "Legend": colors_l,
        "Metrics": metrics_l
    })
    fig_bar = px.bar(df, x="Year", y="Value", color="Legend",hover_name="Company", barmode='group')

    if len(df[df['Metrics']=='stockPrice'])>1:
        price_df=df[df['Metrics']=='stockPrice']
        regressor = LinearRegression()
        x=price_df['Year'].values.reshape(-1,1)
        y=price_df['Value'].values.reshape(-1,1)
        
        regressor.fit(x,y)
        
        price_df['Value']=regressor.predict(x).reshape(1,-1)[0]
        price_df['Legend']=price_df['Company'].apply(lambda x:f"{x} Regression")

        eplison_list=[x-2 for x in list(price_df['Value'])]
        eplison=sum(eplison_list)/len(eplison_list)
        print('eplison',eplison)
        standard_deviation_minus_2=[x-(2*eplison) for x in list(price_df['Value'])]
        standard_deviation_minus=[x-(1*eplison) for x in list(price_df['Value'])]
        standard_deviation_plus_2=[x+(2*eplison) for x in list(price_df['Value'])]
        standard_deviation_plus=[x+(1*eplison) for x in list(price_df['Value'])]

        
        print(standard_deviation_minus_2)
        ecart_df_minus_2=price_df. copy()
        ecart_df_minus_2['Value']=standard_deviation_minus_2
        ecart_df_minus_2['Legend']=ecart_df_minus_2['Company'].apply(lambda x:f"{x} 2 Standard Deviation -")

        print("edf",ecart_df_minus_2)

        ecart_df_minus=price_df. copy()
        ecart_df_minus['Value']=standard_deviation_minus
        ecart_df_minus['Legend']=ecart_df_minus['Company'].apply(lambda x:f"{x} Standard Deviation -")

        ecart_df_plus_2=price_df. copy()
        ecart_df_plus_2['Value']=standard_deviation_plus_2
        ecart_df_plus_2['Legend']=ecart_df_plus_2['Company'].apply(lambda x:f"{x} 2 Standard Deviation +")

        ecart_df_plus=price_df. copy()
        ecart_df_plus['Value']=standard_deviation_plus
        ecart_df_plus['Legend']=ecart_df_plus['Company'].apply(lambda x:f"{x} Standard Deviation +")

        #graph for mean of sector
        _graphs=[price_df,ecart_df_minus, ecart_df_plus_2, ecart_df_plus, ecart_df_minus_2]



        

    _graphs.append(df)
    for metric in d_metrics:
        for range_ in d_ranges:
            range_obj=Ranges.objects.filter(metrics=metric).filter(name=range_)
            if len(range_obj)>0:
                try:    
                    range_obj=range_obj[0]
                    max_value=range_obj.max
                    min_value=range_obj.min
                    if float(max_value) == float(min_value):

                        df_range = pd.DataFrame({
                                
                                "Year":date_range,
                                "Company": '',
                                "Value": max_value,
                                "Legend": f'{range_} {metric}',
                                "Metrics": metric
                            })
                        _graphs.append(df_range)
                    else:
                        df_range = pd.DataFrame({
                                
                                "Year":date_range,
                                "Company": '',
                                "Value": max_value,
                                "Legend": f'{range_} {metric} Max',
                                "Metrics": metric
                            })
                        _graphs.append(df_range)

                        df_range = pd.DataFrame({
                                
                                "Year":date_range,
                                "Company": '',
                                "Value": min_value,
                                "Legend": f'{range_} {metric} Min',
                                "Metrics": metric
                            })
                        _graphs.append(df_range)
                except:
                    pass                        

                        

        
        df=pd.concat(_graphs)
        print("df------------",df)
        print('type............................',type(df['Value']))
        pd.set_option('display.max_rows', None)
        df['Value'] = df['Value'].apply(lambda x:str(x).replace("M",'')).astype(float)


            #graph for mean of industry

    fig_line = px.line(df, x="Year", y="Value", color="Legend",hover_name="Company")
    


    fig_line.update_layout(plot_bgcolor='rgb(255,255,255)')
    fig_line.update_xaxes(showline=True, linecolor='grey')
    fig_line.update_yaxes(showline=True, linecolor='grey')
    fig_line.update_xaxes(gridwidth=0.0001, gridcolor='#F1F1F1')
    fig_line.update_yaxes(gridwidth=0.01, gridcolor='#F1F1F1')
    
    fig_line.update_layout(legend=dict(
        orientation="v",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))
    fig_line.update_layout(legend_title_text='')




    fig_bar.update_layout(plot_bgcolor='rgb(255,255,255)')
    fig_bar.update_xaxes(showline=True, linecolor='grey')
    fig_bar.update_yaxes(showline=True, linecolor='grey')
    fig_bar.update_xaxes(gridwidth=0.0001, gridcolor='#F1F1F1')
    fig_bar.update_yaxes(gridwidth=0.01, gridcolor='#F1F1F1')
    
    fig_bar.update_layout(legend=dict(
        orientation="v",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))
    fig_bar.update_layout(legend_title_text='')

    


    

    plt_line = plot(fig_line, output_type='div',show_link=False,include_plotlyjs=False)
    plt_bar = plot(fig_bar, output_type='div',show_link=False,include_plotlyjs=False)

    if length_metric<1:
        d_metrics=['All Metrics']


    return(return_list,plt_bar,plt_line)



def quote(p_symbol,p_company,p_api,from_,to_):


    response=requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{p_symbol}?serietype=line&apikey={p_api}")
    data=json.loads(response.content)
    

    try:
        if 'Invalid API' in data['Error Message']:
            print("error api")
            return ('api error')
        else:
            return ('other error')
    except:
        print(data)
        data=data['historical']
        data=data[::-1]
        df=pd.DataFrame(data)
        df['Company']=p_company
        df['Symbol']=p_symbol
        date_range=list(range(int(from_),int(to_)+1))
        date_range=[str(x) for x in date_range]
        n_years=len(date_range)

        df['Filter']=df['date'].apply(lambda x:'yes' if str(x).split('-')[0] in date_range else 'no')
    
        
        print("df got", df.head())
        print(len(df))
        
        df=df[df['Filter']=='yes']
        df.drop('Filter', axis=1, inplace=True)
        df['Legend']=df['Company'].apply(lambda x:f"{x} Close price")
        reg_df=df.copy()



        regressor = LinearRegression()
        x=np.array(pd.to_datetime(reg_df['date']).values.reshape(-1,1), dtype='float')
        y=reg_df['close'].values.reshape(-1,1)
        
        regressor.fit(x,y)
        
        reg_df['close']=regressor.predict(x).reshape(1,-1)[0]
        reg_df['Legend']=reg_df['Company'].apply(lambda x:f"{x} Regression")

        eplison_list=[x-2 for x in list(reg_df['close'])]
        eplison=sum(eplison_list)/len(eplison_list)
      
        standard_deviation_minus_2=[x-(2*eplison) for x in list(reg_df['close'])]
        standard_deviation_minus=[x-(1*eplison) for x in list(reg_df['close'])]
        standard_deviation_plus_2=[x+(2*eplison) for x in list(reg_df['close'])]
        standard_deviation_plus=[x+(1*eplison) for x in list(reg_df['close'])]

        
      
        ecart_df_minus_2=reg_df. copy()
        ecart_df_minus_2['close']=standard_deviation_minus_2
        ecart_df_minus_2['Legend']=ecart_df_minus_2['Company'].apply(lambda x:f"{x} 2 Standard Deviation -")


        ecart_df_minus=reg_df. copy()
        ecart_df_minus['close']=standard_deviation_minus
        ecart_df_minus['Legend']=ecart_df_minus['Company'].apply(lambda x:f"{x} Standard Deviation -")

        ecart_df_plus_2=reg_df. copy()
        ecart_df_plus_2['close']=standard_deviation_plus_2
        ecart_df_plus_2['Legend']=ecart_df_plus_2['Company'].apply(lambda x:f"{x} 2 Standard Deviation +")

        ecart_df_plus=reg_df. copy()
        ecart_df_plus['close']=standard_deviation_plus
        ecart_df_plus['Legend']=ecart_df_plus['Company'].apply(lambda x:f"{x} Standard Deviation +")

        
        

        final_df=pd.concat([df,reg_df,ecart_df_minus, ecart_df_plus_2, ecart_df_plus, ecart_df_minus_2])

 




    fig_line = px.line(final_df, x="date", y="close", color="Legend",hover_name="Company")

    fig_line.update_layout(plot_bgcolor='rgb(255,255,255)')
    fig_line.update_xaxes(showline=True, linecolor='grey')
    fig_line.update_yaxes(showline=True, linecolor='grey')
    fig_line.update_xaxes(gridwidth=0.0001, gridcolor='#F1F1F1')
    fig_line.update_yaxes(gridwidth=0.01, gridcolor='#F1F1F1')
    
    fig_line.update_layout(legend=dict(
        orientation="v",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))
    fig_line.update_layout(legend_title_text='')
    plt_line = plot(fig_line, output_type='div',show_link=False,include_plotlyjs=False)

    return (plt_line,df)
          
