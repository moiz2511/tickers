
import requests
import json
import pandas as pd
from django.core import serializers
import numpy as np


from tick_app.models import (AggregateCodes, Company,DataType, ReportedIncome,YearLimit,CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend,AnalysisTools,ReportedBSheet,ReportedCFlow,Rates,RevenueLocation,Ranges,RevenueSector)

def file_upload(t_table,file):
    
    count=0
    print(t_table)
    dataf=pd.read_excel(file, engine="openpyxl")
    dataf = dataf.replace({np.nan: None})
    print(dataf)
    if "Reported income statement" in t_table:
        
        for j,i in enumerate(dataf['year']):
            print(dataf['post_id'][j])
            r_income_entry=ReportedIncome(
                company_name=dataf['comp_name'][j],
                year=dataf['year'][j],
                post_id=dataf['post_id'][j],
                aggregate_code=dataf['aggregate_code'][j],
                notes=dataf['notes'][j],
                value1=dataf['value1'][j],
                value2=dataf['value2'][j]
            )

            r_income_entry.save()
            count=count+1
        message=f"{file} is uploaded in Reported income statement."
        upload_data=ReportedIncome.objects.order_by('-id')[:count][::-1]
        columns=['company_name','year','post_id','aggregate_code','notes','value1','value2']
    

        pass
    elif "Reported balance sheet" in t_table:
        for j,i in enumerate(dataf['year']):
            print(dataf['post_id'][j])
            r_bsheet_entry=ReportedBSheet(
                company_name=dataf['comp_name'][j],
                year=dataf['year'][j],
                post_id=dataf['post_id'][j],
                aggregate_code=dataf['aggregate_code'][j],
                notes=dataf['notes'][j],
                value1=dataf['value1'][j],
                value2=dataf['value2'][j]
            )

            r_bsheet_entry.save()
            count=count+1 
        message=f"{file} is uploaded in Reported balance sheet."  
        upload_data=ReportedBSheet.objects.order_by('-id')[:10][::-1]
        columns=['company_name','year','post_id','aggregate_code','notes','value1','value2']
        
        
    elif "Reported cash flow sheet" in t_table:  
        for j,i in enumerate(dataf['year']):
            print(dataf['post_id'][j])
            r_cflow_entry=ReportedCFlow(
                company_name=dataf['comp_name'][j],
                year=dataf['year'][j],
                post_id=dataf['post_id'][j],
                aggregate_code=dataf['aggregate_code'][j],
                notes=dataf['notes'][j],
                value1=dataf['value1'][j],
                value2=dataf['value2'][j]
            )

            r_cflow_entry.save() 
            count=count+1
        message=f"{file} is uploaded in Reported cash flow sheet." 
        upload_data=ReportedCFlow.objects.order_by('-id')[:count][::-1] 
        columns=['company_name','year','post_id','aggregate_code','notes','value1','value2']
   
        
    elif "Rates" in t_table:
        for j,i in enumerate(dataf['year']):
            rate_entry=Rates(
                country=dataf['country'][j],
                year=dataf['year'][j],
                rate=dataf['rate'][j],
                rate_type=dataf['rate_type'][j]
            )
            rate_entry.save()
            count=count+1
        message=f"{file} is uploaded in Rates."
        upload_data=Rates.objects.order_by('-id')[:count][::-1]
        columns=['country','year','rate','rate_type']
  



    elif "Aggregate Codes" in t_table:
        for j,i in enumerate(dataf['aggregate_code']):
            ag_code_entry=AggregateCodes(
            aggregate_code=dataf['aggregate_code'][j],
            item=dataf['item'][j],
            source=dataf['source'][j]
            )
            ag_code_entry.save()
            count=count+1
        message=f"{file} is uploaded in Aggregate codes."
        print(message)
        upload_data=AggregateCodes.objects.order_by('-id')[:count][::-1]

        columns=['aggregate_code','item','source']

    
    elif "Ranges" in t_table:
        print("Ranges here", dataf)
        for j,i in enumerate(dataf['metrics']):
            range_entry=Ranges(
             metrics=dataf['metrics'][j],
             name=dataf['name'][j],
             source=dataf['source'][j],
             min=dataf['min'][j],
             max=dataf['max'][j]
        )
            range_entry.save()
            count=count+1

        message=f"{file} is uploaded in Ranges."
        upload_data=Ranges.objects.order_by('-id')[:count][::-1]
        columns=['metrics','name','source','min','max']
  

    elif "Revenue Sector" in t_table:
        for j,i in enumerate(dataf['year']):
            sector_entry=RevenueSector(

                company_name=dataf['comp_name'][j],
                year=dataf['year'][j],
                sector=dataf['sector'][j],
                revenuepersector=dataf['revenuepersector'][j]
            )
            sector_entry.save()
            count=count+1
        message=f"{file} is uploaded in Revenue sector."
        upload_data=RevenueSector.objects.order_by('-id')[:count][::-1]
        columns=['company_name','year','sector','revenuepersector']
  
        
    elif "Revenue Location" in t_table:
        for j,i in enumerate(dataf['year']):
            location_entry=RevenueLocation(

                company_name=dataf['comp_name'][j],
                year=dataf['year'][j],
                location=dataf['location'][j],
                revenueperlocation=dataf['revenueperlocation'][j]
            )
            location_entry.save()
            count=count+1
        message=f"{file} is uploaded in Revenue location." 
        upload_data=RevenueLocation.objects.order_by('-id')[:count][::-1]  
        columns=['company_name','year','location','revenueperlocation']
    return(message, upload_data,columns)