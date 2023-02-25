
from tick_app.models import (AggregateCodes, Company,DataType, ReportedIncome,YearLimit,CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend,AnalysisTools,ReportedBSheet,ReportedCFlow,Rates,RevenueLocation,Ranges,RevenueSector)

model_dict={


'reported_income':ReportedIncome,
'reported_bsheet':ReportedBSheet,
'reported_cflow':ReportedCFlow

}

def reportedfin_func(f_company,f_table,f_year):
    return_list=[]

 

    model_select=model_dict[f_table]
           
    fields_list=[f.name for f in model_select._meta.get_fields()]
  

    data_=model_select.objects.filter(company_name=f_company)
    for data in data_:
        datalist=[]
        if f_year in str(data.year):
            for field in fields_list:
                if field.lower()!='id' and field.lower()!='year':
                    datalist.append(getattr(data,field))
            return_list.append(datalist)
    
    columns=[x for x in fields_list if str(x)!='id']
    columns=[x for x in columns if str(x.lower())!='year']
    
    columns=[f_year if 'value2' in str(x) else x for x in columns  ]
    columns=[int(f_year)-1 if 'value1' in str(x) else x for x in columns  ]

    return (return_list,columns)


def reportedfin_func_latest(f_company,f_table,f_year):
    return_list=[]
    model_select=model_dict[f_table]      
    fields_list=[f.name for f in model_select._meta.get_fields()]
    data_=model_select.objects.filter(company_name=f_company)
    for data in data_:
        datalist={}
        if f_year in str(data.year):
            for field in fields_list:
                if field.lower()!='id' and field.lower()!='year':
                    datalist[field] = getattr(data,field)
            return_list.append(datalist)
    columns=[{"label":x, "id": x} for x in fields_list if str(x)!='id' and str(x.lower())!='year']
    # columns=[x for x in columns if str(x.lower())!='year']
    columns=[{"label": f_year, "id": "value2"} if 'value2' in str(x) else x for x in columns  ]
    columns=[{"label":str(int(f_year)-1), "id": "value1"} if 'value1' in str(x) else x for x in columns]
    return (return_list,columns)


