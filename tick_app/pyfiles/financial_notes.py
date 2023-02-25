from tick_app.models import (AggregateCodes, Company,DataType, ReportedIncome,YearLimit,CFlow,
Income,BSheet,Profile,KeyMetrics, FinGrowth, Institutional,
KeyExecutives,IncomeGrowth,BSheetGrowth,CFlowGrowth,Ratios,RatiosTTM,EV,KeyMetricsTTM,MutualFund,Peers,
Price,Dividend,AnalysisTools,ReportedBSheet,ReportedCFlow,Rates,RevenueLocation,Ranges,RevenueSector)

model_dict={

'revenue_location':RevenueLocation,
'revenue_sector':RevenueSector,

}

def financial_notes_func(f_company,f_table,f_from,f_to):
    return_list=[]
    
    date_range=list(range(int(f_from),int(f_to)+1))
    model_select=model_dict[f_table]

    fields_list=[f.name for f in model_select._meta.get_fields()]
    columns=[str(x) for x in fields_list]
    print(columns)

    columns=[x for x in columns if 'id' not in x and 'company' not in x]
    data_got=model_select.objects.filter(company_name=f_company)
    date_range=[str(x) for x in date_range]
    data_got=[x for x in data_got if str(x.year) in date_range ]
   
    for data in data_got:
        data_append=[]
        for field in fields_list:
            if 'id'  not in field and 'company' not in field:
                data_append.append(getattr(data,field))
        return_list.append(data_append)

    print(columns)

    return(return_list,columns)

def financial_notes_func_latest(f_company,f_table,f_from,f_to):
    return_list=[]
    date_range=list(range(int(f_from),int(f_to)+1))
    model_select=model_dict[f_table]
    fields_list=[f.name for f in model_select._meta.get_fields()]
    columns=[str(x) for x in fields_list]
    columns=[{"label": x, "id": x} for x in columns if 'id' not in x and 'company' not in x]
    data_got=model_select.objects.filter(company_name=f_company)
    date_range=[str(x) for x in date_range]
    data_got=[x for x in data_got if str(x.year) in date_range ]

    for data in data_got:
        data_append={}
        for field in fields_list:
            if 'id' not in field and 'company' not in field:
                data_append[field] = getattr(data,field)
        return_list.append(data_append)

    return(return_list,columns)
