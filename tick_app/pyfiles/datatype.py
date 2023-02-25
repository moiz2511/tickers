
import requests
import json, datetime
from django.core import serializers
from tickers.settings import GetSecretProperties
from tick_app.models import (Company, DataType, YearLimit, CFlow,
                             Income, BSheet, Profile, KeyMetrics, FinGrowth, Institutional,
                             KeyExecutives, IncomeGrowth, BSheetGrowth, CFlowGrowth, Ratios, RatiosTTM, EV, KeyMetricsTTM, MutualFund, Peers,
                             Price, Dividend, AnalysisTools, 
                             Dcf, Levereddcf, Riskpremium, Fmpcompanies)

def datatype_fun(companies, p_dtype, p_year):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    print(p_dtype)
    matchedType = False
    p_dtype = str(p_dtype).strip()
    if p_dtype == 'income-statement' or p_dtype.lower() == "all":
        matchedType = True
        print(companies)
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/income-statement/{p_symbol}?limit={p_year}&apikey={p_api}")
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if Income.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        income_entry = Income(
                            symbol=i['symbol'],
                            date=i['date'],
                            revenue=i['revenue'],
                            costOfRevenue=i['costOfRevenue'],
                            grossProfit=i['grossProfit'],
                            grossProfitRatio=i['grossProfitRatio'],
                            researchAndDevelopmentExpenses=i['researchAndDevelopmentExpenses'],
                            generalAndAdministrativeExpenses=i['generalAndAdministrativeExpenses'],
                            sellingAndMarketingExpenses=i['sellingAndMarketingExpenses'],
                            otherExpenses=i['otherExpenses'],
                            operatingExpenses=i['operatingExpenses'],
                            costAndExpenses=i['costAndExpenses'],
                            interestExpense=i['interestExpense'],
                            depreciationAndAmortization=i['depreciationAndAmortization'],
                            ebitda=i['ebitda'],
                            ebitdaratio=i['ebitdaratio'],
                            operatingIncome=i['operatingIncome'],
                            operatingIncomeRatio=i['operatingIncomeRatio'],
                            totalOtherIncomeExpensesNet=i['totalOtherIncomeExpensesNet'],
                            incomeBeforeTax=i['incomeBeforeTax'],
                            incomeBeforeTaxRatio=i['incomeBeforeTaxRatio'],
                            incomeTaxExpense=i['incomeTaxExpense'],
                            netIncome=i['netIncome'],
                            netIncomeRatio=i['netIncomeRatio'],
                            eps=i['eps'],
                            epsdiluted=i['epsdiluted'],
                            weightedAverageShsOut=i['weightedAverageShsOut'],
                            weightedAverageShsOutDil=i['weightedAverageShsOutDil']
                        )
                        income_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = Income.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API INCOME STATEMENT EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'balance-sheet-statement' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{p_symbol}?limit={p_year}&apikey={p_api}")
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api ")
                    return ('api error')
                else:
                    return
            except:
                for i in data:
                    if BSheet.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        balance_entry = BSheet(
                            symbol=i['symbol'],
                            date=i['date'],
                            cashAndCashEquivalents=i['cashAndCashEquivalents'],
                            shortTermInvestments=i['shortTermInvestments'],
                            cashAndShortTermInvestments=i['cashAndShortTermInvestments'],
                            netReceivables=i['netReceivables'],
                            inventory=i['inventory'],
                            otherCurrentAssets=i['otherCurrentAssets'],
                            totalCurrentAssets=i['totalCurrentAssets'],
                            propertyPlantEquipmentNet=i['propertyPlantEquipmentNet'],
                            goodwill=i['goodwill'],
                            intangibleAssets=i['intangibleAssets'],
                            goodwillAndIntangibleAssets=i['goodwillAndIntangibleAssets'],
                            longTermInvestments=i['longTermInvestments'],
                            taxAssets=i['taxAssets'],
                            otherNonCurrentAssets=i['otherNonCurrentAssets'],
                            totalNonCurrentAssets=i['totalNonCurrentAssets'],
                            otherAssets=i['otherAssets'],
                            totalAssets=i['totalAssets'],
                            accountPayables=i['accountPayables'],
                            shortTermDebt=i['shortTermDebt'],
                            taxPayables=i['taxPayables'],
                            deferredRevenue=i['deferredRevenue'],
                            otherCurrentLiabilities=i['otherCurrentLiabilities'],
                            totalCurrentLiabilities=i['totalCurrentLiabilities'],
                            longTermDebt=i['longTermDebt'],
                            deferredRevenueNonCurrent=i['deferredRevenueNonCurrent'],
                            deferredTaxLiabilitiesNonCurrent=i['deferredTaxLiabilitiesNonCurrent'],
                            otherNonCurrentLiabilities=i['otherNonCurrentLiabilities'],
                            totalNonCurrentLiabilities=i['totalNonCurrentLiabilities'],
                            otherLiabilities=i['otherLiabilities'],
                            totalLiabilities=i['totalLiabilities'],
                            commonStock=i['commonStock'],
                            retainedEarnings=i['retainedEarnings'],
                            accumulatedOtherComprehensiveIncomeLoss=i['accumulatedOtherComprehensiveIncomeLoss'],
                            othertotalStockholdersEquity=i["othertotalStockholdersEquity"],
                            totalStockholdersEquity=i["totalStockholdersEquity"],
                            totalLiabilitiesAndStockholdersEquity=i["totalLiabilitiesAndStockholdersEquity"],
                            totalInvestments=i["totalInvestments"],
                            totalDebt=i["totalDebt"],
                            netDebt=i["netDebt"]
                        )
                        balance_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = BSheet.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API BALANCE SHEET STATEMENT EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'cash-flow-statement' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{p_symbol}?limit={p_year}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if CFlow.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        cash_entry = CFlow(
                            symbol=i['symbol'],
                            date=i['date'],
                            netIncome=i['netIncome'],
                            depreciationAndAmortization=i['depreciationAndAmortization'],
                            deferredIncomeTax=i['deferredIncomeTax'],
                            stockBasedCompensation=i['stockBasedCompensation'],
                            changeInWorkingCapital=i['changeInWorkingCapital'],
                            accountsReceivables=i['accountsReceivables'],
                            inventory=i['inventory'],
                            accountsPayables=i['accountsPayables'],
                            otherWorkingCapital=i['otherWorkingCapital'],
                            otherNonCashItems=i['otherNonCashItems'],
                            netCashProvidedByOperatingActivities=i['netCashProvidedByOperatingActivities'],
                            investmentsInPropertyPlantAndEquipment=i['investmentsInPropertyPlantAndEquipment'],
                            acquisitionsNet=i['acquisitionsNet'],
                            purchasesOfInvestments=i['purchasesOfInvestments'],
                            salesMaturitiesOfInvestments=i['salesMaturitiesOfInvestments'],
                            otherInvestingActivites=i['otherInvestingActivites'],
                            netCashUsedForInvestingActivites=i['netCashUsedForInvestingActivites'],
                            debtRepayment=i['debtRepayment'],
                            commonStockIssued=i['commonStockIssued'],
                            commonStockRepurchased=i['commonStockRepurchased'],
                            dividendsPaid=i['dividendsPaid'],
                            otherFinancingActivites=i['otherFinancingActivites'],
                            netCashUsedProvidedByFinancingActivities=i[
                                'netCashUsedProvidedByFinancingActivities'],
                            effectOfForexChangesOnCash=i['effectOfForexChangesOnCash'],
                            netChangeInCash=i['netChangeInCash'],
                            cashAtEndOfPeriod=i['cashAtEndOfPeriod'],
                            cashAtBeginningOfPeriod=i['cashAtBeginningOfPeriod'],
                            operatingCashFlow=i['operatingCashFlow'],
                            capitalExpenditure=i['capitalExpenditure'],
                            freeCashFlow=i['freeCashFlow']
                        )
                        cash_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = CFlow.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API CASH FLOW STATEMENT EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'profile' or p_dtype.lower() == "all":
        print("### Profile Acquisition request received ######")
        matchedType = True
        count = 0
        for p_symbol in companies:
            try:
                response = requests.get(
                    f"https://financialmodelingprep.com/api/v4/company-outlook?symbol={p_symbol}&apikey={p_api}")
                data = json.loads(response.content)
                print(data)
                if 'profile' not in data.keys():
                    print("profile key not in results")
                    continue
                if Profile.objects.filter(symbol=p_symbol).exists():
                    print("Profile Already exists")
                    continue
                else:
                    print("Print profile not exists")
                    i = data['profile']
                    print(i)
                    profile_entry = Profile(
                        symbol=i['symbol'],
                        price=i['price'],
                        beta=i['beta'],
                        volAvg=i['volAvg'],
                        mktCap=i['mktCap'],
                        lastDiv=i['lastDiv'],
                        range=i['range'],
                        changes=i['changes'],
                        companyName=i['companyName'],
                        currency=i['currency'],
                        cik=i['cik'],
                        isin=i['isin'],
                        cusip=i['cusip'],
                        exchange=i['exchange'],
                        exchangeShortName=i['exchangeShortName'],
                        industry=i['industry'],
                        website=i['website'],
                        description=i['description'],
                        ceo=i['ceo'],
                        sector=i['sector'],
                        country=i['country'],
                        fullTimeEmployees=i['fullTimeEmployees'],
                        phone=i['phone'],
                        address=i['address'],
                        city=i['city'],
                        state=i['state'],
                        zip=i['zip'],
                        dcfDiff=i['dcfDiff'],
                        dcf=i['dcf'],
                        image=i['image'],
                        ipoDate=i['ipoDate'],
                        defaultImage=i['defaultImage'],
                        isEtf=i['isEtf'],
                        isActivelyTrading=i['isActivelyTrading'],
                    )
                    profile_entry.save()
                    count = count+1
            except Exception as ex:
                print("Exception Occured", ex)
                continue
                
        # if(count > 0):
        #     data_json = Profile.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API PROFILE EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'key-metrics' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/key-metrics/{p_symbol}?limit={p_year}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if KeyMetrics.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        key_metrics_entry = KeyMetrics(
                            symbol=i['symbol'],
                            date=i['date'],
                            period=i['period'],
                            revenuePerShare=i['revenuePerShare'],
                            netIncomePerShare=i['netIncomePerShare'],
                            operatingCashFlowPerShare=i['operatingCashFlowPerShare'],
                            freeCashFlowPerShare=i['freeCashFlowPerShare'],
                            cashPerShare=i['cashPerShare'],
                            bookValuePerShare=i['bookValuePerShare'],
                            tangibleBookValuePerShare=i['tangibleBookValuePerShare'],
                            shareholdersEquityPerShare=i['shareholdersEquityPerShare'],
                            interestDebtPerShare=i['interestDebtPerShare'],
                            marketCap=i['marketCap'],
                            enterpriseValue=i['enterpriseValue'],
                            peRatio=i['peRatio'],
                            priceToSalesRatio=i['priceToSalesRatio'],
                            pocfratio=i['pocfratio'],
                            pfcfRatio=i['pfcfRatio'],
                            pbRatio=i['pbRatio'],
                            ptbRatio=i['ptbRatio'],
                            evToSales=i['evToSales'],
                            enterpriseValueOverEBITDA=i['enterpriseValueOverEBITDA'],
                            evToOperatingCashFlow=i['evToOperatingCashFlow'],
                            evToFreeCashFlow=i['evToFreeCashFlow'],
                            earningsYield=i['earningsYield'],
                            freeCashFlowYield=i['freeCashFlowYield'],
                            debtToEquity=i['debtToEquity'],
                            debtToAssets=i['debtToAssets'],
                            netDebtToEBITDA=i['netDebtToEBITDA'],
                            currentRatio=i['currentRatio'],
                            interestCoverage=i['interestCoverage'],
                            incomeQuality=i['incomeQuality'],
                            dividendYield=i['dividendYield'],
                            payoutRatio=i['payoutRatio'],
                            salesGeneralAndAdministrativeToRevenue=i['salesGeneralAndAdministrativeToRevenue'],
                            researchAndDdevelopementToRevenue=i['researchAndDdevelopementToRevenue'],
                            intangiblesToTotalAssets=i['intangiblesToTotalAssets'],
                            capexToOperatingCashFlow=i['capexToOperatingCashFlow'],
                            capexToRevenue=i['capexToRevenue'],
                            capexToDepreciation=i['capexToDepreciation'],
                            stockBasedCompensationToRevenue=i['stockBasedCompensationToRevenue'],
                            grahamNumber=i['grahamNumber'],
                            roic=i['roic'],
                            returnOnTangibleAssets=i['returnOnTangibleAssets'],
                            grahamNetNet=i['grahamNetNet'],
                            workingCapital=i['workingCapital'],
                            tangibleAssetValue=i['tangibleAssetValue'],
                            netCurrentAssetValue=i['netCurrentAssetValue'],
                            investedCapital=i['investedCapital'],
                            averageReceivables=i['averageReceivables'],
                            averagePayables=i['averagePayables'],
                            averageInventory=i['averageInventory'],
                            daysSalesOutstanding=i['daysSalesOutstanding'],
                            daysPayablesOutstanding=i['daysPayablesOutstanding'],
                            daysOfInventoryOnHand=i['daysOfInventoryOnHand'],
                            receivablesTurnover=i['receivablesTurnover'],
                            payablesTurnover=i['payablesTurnover'],
                            inventoryTurnover=i['inventoryTurnover'],
                            roe=i['roe'],
                            capexPerShare=i['capexPerShare']
                        )
                        key_metrics_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = KeyMetrics.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API KEY METRICS EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'financial-growth' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:

            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/financial-growth/{p_symbol}?limit={p_year}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if FinGrowth.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        fin_growth_entry = FinGrowth(
                            symbol=i['symbol'],
                            date=i['date'],
                            period=i['period'],
                            revenueGrowth=i['revenueGrowth'],
                            grossProfitGrowth=i['grossProfitGrowth'],
                            ebitgrowth=i['ebitgrowth'],
                            operatingIncomeGrowth=i['operatingIncomeGrowth'],
                            netIncomeGrowth=i['netIncomeGrowth'],
                            epsgrowth=i['epsgrowth'],
                            epsdilutedGrowth=i['epsdilutedGrowth'],
                            weightedAverageSharesGrowth=i['weightedAverageSharesGrowth'],
                            weightedAverageSharesDilutedGrowth=i['weightedAverageSharesDilutedGrowth'],
                            dividendsperShareGrowth=i['dividendsperShareGrowth'],
                            operatingCashFlowGrowth=i['operatingCashFlowGrowth'],
                            freeCashFlowGrowth=i['freeCashFlowGrowth'],
                            tenYRevenueGrowthPerShare=i['tenYRevenueGrowthPerShare'],
                            fiveYRevenueGrowthPerShare=i['fiveYRevenueGrowthPerShare'],
                            threeYRevenueGrowthPerShare=i['threeYRevenueGrowthPerShare'],
                            tenYOperatingCFGrowthPerShare=i['tenYOperatingCFGrowthPerShare'],
                            fiveYOperatingCFGrowthPerShare=i['fiveYOperatingCFGrowthPerShare'],
                            threeYOperatingCFGrowthPerShare=i['threeYOperatingCFGrowthPerShare'],
                            tenYNetIncomeGrowthPerShare=i['tenYNetIncomeGrowthPerShare'],
                            fiveYNetIncomeGrowthPerShare=i['fiveYNetIncomeGrowthPerShare'],
                            threeYNetIncomeGrowthPerShare=i['threeYNetIncomeGrowthPerShare'],
                            tenYShareholdersEquityGrowthPerShare=i['tenYShareholdersEquityGrowthPerShare'],
                            fiveYShareholdersEquityGrowthPerShare=i['fiveYShareholdersEquityGrowthPerShare'],
                            threeYShareholdersEquityGrowthPerShare=i['threeYShareholdersEquityGrowthPerShare'],
                            tenYDividendperShareGrowthPerShare=i['tenYDividendperShareGrowthPerShare'],
                            fiveYDividendperShareGrowthPerShare=i['fiveYDividendperShareGrowthPerShare'],
                            threeYDividendperShareGrowthPerShare=i['threeYDividendperShareGrowthPerShare'],
                            receivablesGrowth=i['receivablesGrowth'],
                            inventoryGrowth=i['inventoryGrowth'],
                            assetGrowth=i['assetGrowth'],
                            bookValueperShareGrowth=i['bookValueperShareGrowth'],
                            debtGrowth=i['debtGrowth'],
                            rdexpenseGrowth=i['rdexpenseGrowth'],
                            sgaexpensesGrowth=i['sgaexpensesGrowth']
                        )
                        fin_growth_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = FinGrowth.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API FINANCIAL GROWTH EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'institutional-holder' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/institutional-holder/{p_symbol}?apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if Institutional.objects.filter(symbol=p_symbol, dateReported=i['dateReported']).exists():
                        pass
                    else:
                        ins_entry = Institutional(
                            symbol=p_symbol,
                            holder=i['holder'],
                            shares=i['shares'],
                            dateReported=i['dateReported'],
                            change=i['change']
                        )
                        ins_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = Institutional.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API INSTITUTIONAL HOLDER EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'key-executives' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/key-executives/{p_symbol}?apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if KeyExecutives.objects.filter(symbol=p_symbol, name=i['name']).exists():
                        pass
                    else:
                        key_entry = KeyExecutives(
                            symbol=p_symbol,
                            title=i['title'],
                            name=i['name'],
                            pay=i['pay'],
                            currencyPay=i['currencyPay'],
                            gender=i['gender'],
                            yearBorn=i['yearBorn'],
                            titleSince=i['titleSince']
                        )
                        key_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = KeyExecutives.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API KEY EXECUTIVES EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'income-statement-growth' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/income-statement-growth/{p_symbol}?limit={p_year}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if IncomeGrowth.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        incomeg_entry = IncomeGrowth(
                            date=i['date'],
                            symbol=i['symbol'],
                            period=i['period'],
                            growthRevenue=i['growthRevenue'],
                            growthCostOfRevenue=i['growthCostOfRevenue'],
                            growthGrossProfit=i['growthGrossProfit'],
                            growthGrossProfitRatio=i['growthGrossProfitRatio'],
                            growthResearchAndDevelopmentExpenses=i['growthResearchAndDevelopmentExpenses'],
                            growthGeneralAndAdministrativeExpenses=i['growthGeneralAndAdministrativeExpenses'],
                            growthSellingAndMarketingExpenses=i['growthSellingAndMarketingExpenses'],
                            growthOtherExpenses=i['growthOtherExpenses'],
                            growthOperatingExpenses=i['growthOperatingExpenses'],
                            growthCostAndExpenses=i['growthCostAndExpenses'],
                            growthInterestExpense=i['growthInterestExpense'],
                            growthDepreciationAndAmortization=i['growthDepreciationAndAmortization'],
                            growthEBITDA=i['growthEBITDA'],
                            growthEBITDARatio=i['growthEBITDARatio'],
                            growthOperatingIncome=i['growthOperatingIncome'],
                            growthOperatingIncomeRatio=i['growthOperatingIncomeRatio'],
                            growthTotalOtherIncomeExpensesNet=i['growthTotalOtherIncomeExpensesNet'],
                            growthIncomeBeforeTax=i['growthIncomeBeforeTax'],
                            growthIncomeBeforeTaxRatio=i['growthIncomeBeforeTaxRatio'],
                            growthIncomeTaxExpense=i['growthIncomeTaxExpense'],
                            growthNetIncome=i['growthNetIncome'],
                            growthNetIncomeRatio=i['growthNetIncomeRatio'],
                            growthEPS=i['growthEPS'],
                            growthEPSDiluted=i['growthEPSDiluted'],
                            growthWeightedAverageShsOut=i['growthWeightedAverageShsOut'],
                            growthWeightedAverageShsOutDil=i['growthWeightedAverageShsOutDil']
                        )
                        incomeg_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = IncomeGrowth.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API INCOME STATEMENT GROWTH EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'balance-sheet-statement-growth' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:

            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/balance-sheet-statement-growth/{p_symbol}?limit={p_year}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if BSheetGrowth.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        bg_entry = BSheetGrowth(
                            date=i['date'],
                            symbol=i['symbol'],
                            period=i['period'],
                            growthCashAndCashEquivalents=i['growthCashAndCashEquivalents'],
                            growthShortTermInvestments=i['growthShortTermInvestments'],
                            growthCashAndShortTermInvestments=i['growthCashAndShortTermInvestments'],
                            growthNetReceivables=i['growthNetReceivables'],
                            growthInventory=i['growthInventory'],
                            growthOtherCurrentAssets=i['growthOtherCurrentAssets'],
                            growthTotalCurrentAssets=i['growthTotalCurrentAssets'],
                            growthPropertyPlantEquipmentNet=i['growthPropertyPlantEquipmentNet'],
                            growthGoodwill=i['growthGoodwill'],
                            growthIntangibleAssets=i['growthIntangibleAssets'],
                            growthGoodwillAndIntangibleAssets=i['growthGoodwillAndIntangibleAssets'],
                            growthLongTermInvestments=i['growthLongTermInvestments'],
                            growthTaxAssets=i['growthTaxAssets'],
                            growthOtherNonCurrentAssets=i['growthOtherNonCurrentAssets'],
                            growthTotalNonCurrentAssets=i['growthTotalNonCurrentAssets'],
                            growthOtherAssets=i['growthOtherAssets'],
                            growthTotalAssets=i['growthTotalAssets'],
                            growthAccountPayables=i['growthAccountPayables'],
                            growthShortTermDebt=i['growthShortTermDebt'],
                            growthTaxPayables=i['growthTaxPayables'],
                            growthDeferredRevenue=i['growthDeferredRevenue'],
                            growthOtherCurrentLiabilities=i['growthOtherCurrentLiabilities'],
                            growthTotalCurrentLiabilities=i['growthTotalCurrentLiabilities'],
                            growthLongTermDebt=i['growthLongTermDebt'],
                            growthDeferredRevenueNonCurrent=i['growthDeferredRevenueNonCurrent'],
                            growthDeferrredTaxLiabilitiesNonCurrent=i['growthDeferrredTaxLiabilitiesNonCurrent'],
                            growthOtherNonCurrentLiabilities=i['growthOtherNonCurrentLiabilities'],
                            growthTotalNonCurrentLiabilities=i['growthTotalNonCurrentLiabilities'],
                            growthOtherLiabilities=i['growthOtherLiabilities'],
                            growthTotalLiabilities=i['growthTotalLiabilities'],
                            growthCommonStock=i['growthCommonStock'],
                            growthRetainedEarnings=i['growthRetainedEarnings'],
                            growthAccumulatedOtherComprehensiveIncomeLoss=i[
                                'growthAccumulatedOtherComprehensiveIncomeLoss'],
                            growthOthertotalStockholdersEquity=i['growthOthertotalStockholdersEquity'],
                            growthTotalStockholdersEquity=i['growthTotalStockholdersEquity'],
                            growthTotalLiabilitiesAndStockholdersEquity=i[
                                'growthTotalLiabilitiesAndStockholdersEquity'],
                            growthTotalInvestments=i['growthTotalInvestments'],
                            growthTotalDebt=i['growthTotalDebt'],
                            growthNetDebt=i['growthNetDebt']
                        )
                        bg_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = BSheetGrowth.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API BALANCE SHEET STATEMENT GROWTH EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'cash-flow-statement-growth' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/cash-flow-statement-growth/{p_symbol}?limit={p_year}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if CFlowGrowth.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        c_entry = CFlowGrowth(
                            date=i['date'],
                            symbol=i['symbol'],
                            period=i['period'],
                            growthNetIncome=i['growthNetIncome'],
                            growthDepreciationAndAmortization=i['growthDepreciationAndAmortization'],
                            growthDeferredIncomeTax=i['growthDeferredIncomeTax'],
                            growthStockBasedCompensation=i['growthStockBasedCompensation'],
                            growthChangeInWorkingCapital=i['growthChangeInWorkingCapital'],
                            growthAccountsReceivables=i['growthAccountsReceivables'],
                            growthInventory=i['growthInventory'],
                            growthAccountsPayables=i['growthAccountsPayables'],
                            growthOtherWorkingCapital=i['growthOtherWorkingCapital'],
                            growthOtherNonCashItems=i['growthOtherNonCashItems'],
                            growthNetCashProvidedByOperatingActivites=i[
                                'growthNetCashProvidedByOperatingActivites'],
                            growthInvestmentsInPropertyPlantAndEquipment=i[
                                'growthInvestmentsInPropertyPlantAndEquipment'],
                            growthAcquisitionsNet=i['growthAcquisitionsNet'],
                            growthPurchasesOfInvestments=i['growthPurchasesOfInvestments'],
                            growthSalesMaturitiesOfInvestments=i['growthSalesMaturitiesOfInvestments'],
                            growthOtherInvestingActivites=i['growthOtherInvestingActivites'],
                            growthNetCashUsedForInvestingActivites=i['growthNetCashUsedForInvestingActivites'],
                            growthDebtRepayment=i['growthDebtRepayment'],
                            growthCommonStockIssued=i['growthCommonStockIssued'],
                            growthCommonStockRepurchased=i['growthCommonStockRepurchased'],
                            growthDividendsPaid=i['growthDividendsPaid'],
                            growthOtherFinancingActivites=i['growthOtherFinancingActivites'],
                            growthNetCashUsedProvidedByFinancingActivities=i[
                                'growthNetCashUsedProvidedByFinancingActivities'],
                            growthEffectOfForexChangesOnCash=i['growthEffectOfForexChangesOnCash'],
                            growthNetChangeInCash=i['growthNetChangeInCash'],
                            growthCashAtEndOfPeriod=i['growthCashAtEndOfPeriod'],
                            growthCashAtBeginningOfPeriod=i['growthCashAtBeginningOfPeriod'],
                            growthOperatingCashFlow=i['growthOperatingCashFlow'],
                            growthCapitalExpenditure=i['growthCapitalExpenditure'],
                            growthFreeCashFlow=i['growthFreeCashFlow']
                        )
                        c_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = CFlowGrowth.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API CASH FLOW STATEMENT GROWTH EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'ratios' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/ratios/{p_symbol}?limit={p_year}&apikey={p_api}")
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if Ratios.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        ratio_entry = Ratios(
                            symbol=i['symbol'],
                            date=i['date'],
                            period=i['period'],
                            currentRatio=i['currentRatio'],
                            quickRatio=i['quickRatio'],
                            cashRatio=i['cashRatio'],
                            daysOfSalesOutstanding=i['daysOfSalesOutstanding'],
                            daysOfInventoryOutstanding=i['daysOfInventoryOutstanding'],
                            operatingCycle=i['operatingCycle'],
                            daysOfPayablesOutstanding=i['daysOfPayablesOutstanding'],
                            cashConversionCycle=i['cashConversionCycle'],
                            grossProfitMargin=i['grossProfitMargin'],
                            operatingProfitMargin=i['operatingProfitMargin'],
                            pretaxProfitMargin=i['pretaxProfitMargin'],
                            netProfitMargin=i['netProfitMargin'],
                            effectiveTaxRate=i['effectiveTaxRate'],
                            returnOnAssets=i['returnOnAssets'],
                            returnOnEquity=i['returnOnEquity'],
                            returnOnCapitalEmployed=i['returnOnCapitalEmployed'],
                            netIncomePerEBT=i['netIncomePerEBT'],
                            ebtPerEbit=i['ebtPerEbit'],
                            ebitPerRevenue=i['ebitPerRevenue'],
                            debtRatio=i['debtRatio'],
                            debtEquityRatio=i['debtEquityRatio'],
                            longTermDebtToCapitalization=i['longTermDebtToCapitalization'],
                            totalDebtToCapitalization=i['totalDebtToCapitalization'],
                            interestCoverage=i['interestCoverage'],
                            cashFlowToDebtRatio=i['cashFlowToDebtRatio'],
                            companyEquityMultiplier=i['companyEquityMultiplier'],
                            receivablesTurnover=i['receivablesTurnover'],
                            payablesTurnover=i['payablesTurnover'],
                            inventoryTurnover=i['inventoryTurnover'],
                            fixedAssetTurnover=i['fixedAssetTurnover'],
                            assetTurnover=i['assetTurnover'],
                            operatingCashFlowPerShare=i['operatingCashFlowPerShare'],
                            freeCashFlowPerShare=i['freeCashFlowPerShare'],
                            cashPerShare=i['cashPerShare'],
                            payoutRatio=i['payoutRatio'],
                            operatingCashFlowSalesRatio=i['operatingCashFlowSalesRatio'],
                            freeCashFlowOperatingCashFlowRatio=i['freeCashFlowOperatingCashFlowRatio'],
                            cashFlowCoverageRatios=i['cashFlowCoverageRatios'],
                            shortTermCoverageRatios=i['shortTermCoverageRatios'],
                            capitalExpenditureCoverageRatio=i['capitalExpenditureCoverageRatio'],
                            dividendPaidAndCapexCoverageRatio=i['dividendPaidAndCapexCoverageRatio'],
                            dividendPayoutRatio=i['dividendPayoutRatio'],
                            priceBookValueRatio=i['priceBookValueRatio'],
                            priceToBookRatio=i['priceToBookRatio'],
                            priceToSalesRatio=i['priceToSalesRatio'],
                            priceEarningsRatio=i['priceEarningsRatio'],
                            priceToFreeCashFlowsRatio=i['priceToFreeCashFlowsRatio'],
                            priceToOperatingCashFlowsRatio=i['priceToOperatingCashFlowsRatio'],
                            priceCashFlowRatio=i['priceCashFlowRatio'],
                            priceEarningsToGrowthRatio=i['priceEarningsToGrowthRatio'],
                            priceSalesRatio=i['priceSalesRatio'],
                            dividendYield=i['dividendYield'],
                            enterpriseValueMultiple=i['enterpriseValueMultiple'],
                            priceFairValue=i['priceFairValue']
                        )
                        ratio_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = Ratios.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API RATIOS EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'ratios-ttm' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/ratios-ttm/{p_symbol}?apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if RatiosTTM.objects.filter(symbol=p_symbol).exists():
                        pass
                    else:
                        ratiottm_entry = RatiosTTM(
                            symbol=p_symbol,
                            dividendYielTTM=i['dividendYielTTM'],
                            dividendYielPercentageTTM=i['dividendYielPercentageTTM'],
                            peRatioTTM=i['peRatioTTM'],
                            pegRatioTTM=i['pegRatioTTM'],
                            payoutRatioTTM=i['payoutRatioTTM'],
                            currentRatioTTM=i['currentRatioTTM'],
                            quickRatioTTM=i['quickRatioTTM'],
                            cashRatioTTM=i['cashRatioTTM'],
                            daysOfSalesOutstandingTTM=i['daysOfSalesOutstandingTTM'],
                            daysOfInventoryOutstandingTTM=i['daysOfInventoryOutstandingTTM'],
                            operatingCycleTTM=i['operatingCycleTTM'],
                            daysOfPayablesOutstandingTTM=i['daysOfPayablesOutstandingTTM'],
                            cashConversionCycleTTM=i['cashConversionCycleTTM'],
                            grossProfitMarginTTM=i['grossProfitMarginTTM'],
                            operatingProfitMarginTTM=i['operatingProfitMarginTTM'],
                            pretaxProfitMarginTTM=i['pretaxProfitMarginTTM'],
                            netProfitMarginTTM=i['netProfitMarginTTM'],
                            effectiveTaxRateTTM=i['effectiveTaxRateTTM'],
                            returnOnAssetsTTM=i['returnOnAssetsTTM'],
                            returnOnEquityTTM=i['returnOnEquityTTM'],
                            returnOnCapitalEmployedTTM=i['returnOnCapitalEmployedTTM'],
                            netIncomePerEBTTTM=i['netIncomePerEBTTTM'],
                            ebtPerEbitTTM=i['ebtPerEbitTTM'],
                            ebitPerRevenueTTM=i['ebitPerRevenueTTM'],
                            debtRatioTTM=i['debtRatioTTM'],
                            debtEquityRatioTTM=i['debtEquityRatioTTM'],
                            longTermDebtToCapitalizationTTM=i['longTermDebtToCapitalizationTTM'],
                            totalDebtToCapitalizationTTM=i['totalDebtToCapitalizationTTM'],
                            interestCoverageTTM=i['interestCoverageTTM'],
                            cashFlowToDebtRatioTTM=i['cashFlowToDebtRatioTTM'],
                            companyEquityMultiplierTTM=i['companyEquityMultiplierTTM'],
                            receivablesTurnoverTTM=i['receivablesTurnoverTTM'],
                            payablesTurnoverTTM=i['payablesTurnoverTTM'],
                            inventoryTurnoverTTM=i['inventoryTurnoverTTM'],
                            fixedAssetTurnoverTTM=i['fixedAssetTurnoverTTM'],
                            assetTurnoverTTM=i['assetTurnoverTTM'],
                            operatingCashFlowPerShareTTM=i['operatingCashFlowPerShareTTM'],
                            freeCashFlowPerShareTTM=i['freeCashFlowPerShareTTM'],
                            cashPerShareTTM=i['cashPerShareTTM'],
                            operatingCashFlowSalesRatioTTM=i['operatingCashFlowSalesRatioTTM'],
                            freeCashFlowOperatingCashFlowRatioTTM=i['freeCashFlowOperatingCashFlowRatioTTM'],
                            cashFlowCoverageRatiosTTM=i['cashFlowCoverageRatiosTTM'],
                            shortTermCoverageRatiosTTM=i['shortTermCoverageRatiosTTM'],
                            capitalExpenditureCoverageRatioTTM=i['capitalExpenditureCoverageRatioTTM'],
                            dividendPaidAndCapexCoverageRatioTTM=i['dividendPaidAndCapexCoverageRatioTTM'],
                            priceBookValueRatioTTM=i['priceBookValueRatioTTM'],
                            priceToBookRatioTTM=i['priceToBookRatioTTM'],
                            priceToSalesRatioTTM=i['priceToSalesRatioTTM'],
                            priceEarningsRatioTTM=i['priceEarningsRatioTTM'],
                            priceToFreeCashFlowsRatioTTM=i['priceToFreeCashFlowsRatioTTM'],
                            priceToOperatingCashFlowsRatioTTM=i['priceToOperatingCashFlowsRatioTTM'],
                            priceCashFlowRatioTTM=i['priceCashFlowRatioTTM'],
                            priceEarningsToGrowthRatioTTM=i['priceEarningsToGrowthRatioTTM'],
                            priceSalesRatioTTM=i['priceSalesRatioTTM'],
                            dividendYieldTTM=i['dividendYieldTTM'],
                            enterpriseValueMultipleTTM=i['enterpriseValueMultipleTTM'],
                            priceFairValueTTM=i['priceFairValueTTM'],
                            dividendPerShareTTM=i['dividendPerShareTTM']
                        )
                        ratiottm_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = RatiosTTM.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API RATIOS-TTM EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'enterprise-values' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/enterprise-values/{p_symbol}?limit={p_year}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if EV.objects.filter(symbol=i['symbol'], date=i['date']).exists():
                        pass
                    else:
                        ev_entry = EV(
                            symbol=i['symbol'],
                            date=i['date'],
                            stockPrice=i['stockPrice'],
                            numberOfShares=i['numberOfShares'],
                            marketCapitalization=i['marketCapitalization'],
                            minusCashAndCashEquivalents=i['minusCashAndCashEquivalents'],
                            addTotalDebt=i['addTotalDebt'],
                            enterpriseValue=i['enterpriseValue']
                        )
                        ev_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = EV.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API ENTERPRICE VALUES EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'key-metrics-ttm' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{p_symbol}?limit={p_year}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if KeyMetricsTTM.objects.filter(symbol=p_symbol).exists():
                        pass
                    else:
                        keyttm_entry = KeyMetricsTTM(
                            symbol=p_symbol,
                            revenuePerShareTTM=i['revenuePerShareTTM'],
                            netIncomePerShareTTM=i['netIncomePerShareTTM'],
                            operatingCashFlowPerShareTTM=i['operatingCashFlowPerShareTTM'],
                            freeCashFlowPerShareTTM=i['freeCashFlowPerShareTTM'],
                            cashPerShareTTM=i['cashPerShareTTM'],
                            bookValuePerShareTTM=i['bookValuePerShareTTM'],
                            tangibleBookValuePerShareTTM=i['tangibleBookValuePerShareTTM'],
                            shareholdersEquityPerShareTTM=i['shareholdersEquityPerShareTTM'],
                            interestDebtPerShareTTM=i['interestDebtPerShareTTM'],
                            marketCapTTM=i['marketCapTTM'],
                            enterpriseValueTTM=i['enterpriseValueTTM'],
                            peRatioTTM=i['peRatioTTM'],
                            priceToSalesRatioTTM=i['priceToSalesRatioTTM'],
                            pocfratioTTM=i['pocfratioTTM'],
                            pfcfRatioTTM=i['pfcfRatioTTM'],
                            pbRatioTTM=i['pbRatioTTM'],
                            ptbRatioTTM=i['ptbRatioTTM'],
                            evToSalesTTM=i['evToSalesTTM'],
                            enterpriseValueOverEBITDATTM=i['enterpriseValueOverEBITDATTM'],
                            evToOperatingCashFlowTTM=i['evToOperatingCashFlowTTM'],
                            evToFreeCashFlowTTM=i['evToFreeCashFlowTTM'],
                            earningsYieldTTM=i['earningsYieldTTM'],
                            freeCashFlowYieldTTM=i['freeCashFlowYieldTTM'],
                            debtToEquityTTM=i['debtToEquityTTM'],
                            debtToAssetsTTM=i['debtToAssetsTTM'],
                            netDebtToEBITDATTM=i['netDebtToEBITDATTM'],
                            currentRatioTTM=i['currentRatioTTM'],
                            interestCoverageTTM=i['interestCoverageTTM'],
                            incomeQualityTTM=i['incomeQualityTTM'],
                            dividendYieldTTM=i['dividendYieldTTM'],
                            dividendYieldPercentageTTM=i['dividendYieldPercentageTTM'],
                            payoutRatioTTM=i['payoutRatioTTM'],
                            salesGeneralAndAdministrativeToRevenueTTM=i[
                                'salesGeneralAndAdministrativeToRevenueTTM'],
                            researchAndDevelopementToRevenueTTM=i['researchAndDevelopementToRevenueTTM'],
                            intangiblesToTotalAssetsTTM=i['intangiblesToTotalAssetsTTM'],
                            capexToOperatingCashFlowTTM=i['capexToOperatingCashFlowTTM'],
                            capexToRevenueTTM=i['capexToRevenueTTM'],
                            capexToDepreciationTTM=i['capexToDepreciationTTM'],
                            stockBasedCompensationToRevenueTTM=i['stockBasedCompensationToRevenueTTM'],
                            grahamNumberTTM=i['grahamNumberTTM'],
                            roicTTM=i['roicTTM'],
                            returnOnTangibleAssetsTTM=i['returnOnTangibleAssetsTTM'],
                            grahamNetNetTTM=i['grahamNetNetTTM'],
                            workingCapitalTTM=i['workingCapitalTTM'],
                            tangibleAssetValueTTM=i['tangibleAssetValueTTM'],
                            netCurrentAssetValueTTM=i['netCurrentAssetValueTTM'],
                            investedCapitalTTM=i['investedCapitalTTM'],
                            averageReceivablesTTM=i['averageReceivablesTTM'],
                            averagePayablesTTM=i['averagePayablesTTM'],
                            averageInventoryTTM=i['averageInventoryTTM'],
                            daysSalesOutstandingTTM=i['daysSalesOutstandingTTM'],
                            daysPayablesOutstandingTTM=i['daysPayablesOutstandingTTM'],
                            daysOfInventoryOnHandTTM=i['daysOfInventoryOnHandTTM'],
                            receivablesTurnoverTTM=i['receivablesTurnoverTTM'],
                            payablesTurnoverTTM=i['payablesTurnoverTTM'],
                            inventoryTurnoverTTM=i['inventoryTurnoverTTM'],
                            roeTTM=i['roeTTM'],
                            capexPerShareTTM=i['capexPerShareTTM'],
                            dividendPerShareTTM=i['dividendPerShareTTM']
                        )
                        keyttm_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = KeyMetricsTTM.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API KEY METRICS-TTM EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'mutual-fund-holder' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/mutual-fund-holder/{p_symbol}?apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if MutualFund.objects.filter(symbol=p_symbol, dateReported=i.get('dateReported')).exists():
                        pass
                    else:
                        mutual_entry = MutualFund(
                            symbol=p_symbol,
                            holder=i['holder'],
                            shares=i['shares'],
                            dateReported=i['dateReported'],
                            change=i['change'],
                            weightPercent=i['weightPercent']

                        )
                        mutual_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = MutualFund.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API MUTUALFUND HOLDER EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'stock_peers' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v4/stock_peers?symbol={p_symbol}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    if Peers.objects.filter(symbol=i['symbol']).exists():
                        pass
                    else:
                        stock_entry = Peers(
                            symbol=i['symbol'],
                            peersList=(',').join(i['peersList'])
                        )
                        stock_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = Peers.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        # data_json = serializers.serialize( "python", Peers.objects.all())
        # return data_json
        print(" DATA ACQ API STOCK PEERS EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'historical-price-full' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        now = datetime.datetime.now()
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/historical-price-full/{p_symbol}?from={str(now.year-int(p_year))}-01-01&to={str(now.year)}-{str(now.month)}-{str(now.day)}&apikey={p_api}")
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data['historical']:
                    if Price.objects.filter(symbol=p_symbol, date=i['date']).exists():
                        pass
                    else:
                        price_entry = Price(
                            symbol=p_symbol,
                            date=i.get('date'),
                            open=i.get('open'),
                            high=i.get('high'),
                            low=i.get('low'),
                            close=i.get('close'),
                            adjClose=i.get('adjClose'),
                            volume=i.get('volume'),
                            unadjustedVolume=i.get('unadjustedVolume'),
                            change=i.get('change'),
                            changePercent=i.get('changePercent'),
                            vwap=i.get('vwap'),
                            label=i.get('label'),
                            changeOverTime=i.get('changeOverTime'),
                        )
                        price_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = Price.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API HISTORICAL PRICE FULL EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'stock_dividend' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        now = datetime.datetime.now()
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{p_symbol}?from={str(now.year-int(p_year))}-01-01&to={str(now.year)}-{str(now.month)}-{str(now.day)}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                if data.get('historical', "") == "":
                    print(" DATA ACQ API STOCKS DIVIDEND EXECUTED")
                    return "success"
                for i in data['historical']:
                    if Dividend.objects.filter(symbol=p_symbol, date=i['date']).exists():
                        pass
                    else:
                        try:
                            dividend_ = i['dividend']
                        except:
                            dividend_ = None
                        d_entry = Dividend(
                            symbol=p_symbol,
                            date=i['date'],
                            label=i['label'],
                            adjDividend=i['adjDividend'],
                            dividend=dividend_,
                            recordDate=i['recordDate'],
                            paymentDate=i['paymentDate'],
                            declarationDate=i['declarationDate']
                        )
                        d_entry.save()
                        count = count+1
        # if(count > 0):
        #     data_json = Dividend.objects.all()
        #     data_json = data_json.order_by("-id").all()
        #     if (p_dtype.lower() == "all"):
        #         resultData = resultData + data_json[:count]
        #     else:
        #         data_json = data_json[:count]
        #         data_json = serializers.serialize("python", data_json)
        #         return data_json
        # else:
        #     return []
        print(" DATA ACQ API STOCKS DIVIDEND EXECUTED")
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'discounted-cash-flow' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        now = datetime.datetime.now()
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v4/advanced_discounted_cash_flow?symbol={p_symbol}&apikey={p_api}")
            print(p_symbol, p_api)
            data = json.loads(response.content)
            print(data)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    print("##### DISCOUNTED CASH FLOW LOOP #########")
                    try:
                        entry = Dcf(
                            symbol=i.get('symbol'),
                            year=i.get('year'),
                            revenue=i.get('revenue'),
                            revenuePercentage=i.get('revenuePercentage'),
                            ebitda=i.get('ebitda'),
                            ebitdaPercentage=i.get('ebitdaPercentage'),
                            ebit=i.get('ebit'),
                            ebitPercentage=i.get('ebitPercentage'),
                            depreciation=i.get('depreciation'),
                            depreciationPercentage=i.get('depreciationPercentage'),
                            totalCash=i.get('totalCash'),
                            totalCashPercentage=i.get('totalCashPercentage'),
                            receivables=i.get('receivables'),
                            receivablesPercentage=i.get('receivablesPercentage'),
                            inventories=i.get('inventories'),
                            inventoriesPercentage=i.get('inventoriesPercentage'),
                            payable=i.get('payable'),
                            payablePercentage=i.get('payablePercentage'),
                            capitalExpenditure=i.get('capitalExpenditure'),
                            capitalExpenditurePercentage=i.get('capitalExpenditurePercentage'),
                            price=i.get('price'),
                            beta=i.get('beta'),
                            dilutedSharesOutstanding=i.get('dilutedSharesOutstanding'),
                            costofDebt=i.get('costofDebt'),
                            taxRate=i.get('taxRate'),
                            afterTaxCostOfDebt=i.get('afterTaxCostOfDebt'),
                            riskFreeRate=i.get('riskFreeRate'),
                            marketRiskPremium=i.get('marketRiskPremium'),
                            costOfEquity=i.get('costOfEquity'),
                            totalDebt=i.get('totalDebt'),
                            totalEquity=i.get('totalEquity'),
                            totalCapital=i.get('totalCapital'),
                            debtWeighting=i.get('debtWeighting'),
                            equityWeighting=i.get('equityWeighting'),
                            wacc=i.get('wacc'),
                            taxRateCash=i.get('taxRateCash'),
                            ebiat=i.get('ebiat'),
                            ufcf=i.get('ufcf'),
                            sumPvUfcf=i.get('sumPvUfcf'),
                            longTermGrowthRate=i.get('longTermGrowthRate'),
                            presentTerminalValue=i.get('presentTerminalValue'),
                            enterpriseValue=i.get('enterpriseValue'),
                            netDebt=i.get('netDebt'),
                            equityValue=i.get('equityValue'),
                            equityValuePerShare=i.get('equityValuePerShare'),
                            freeCashFlowT1=i.get('freeCashFlowT1')
                        )
                        print("######## CHECKING FOR DATA EXISTANCE ########")
                        record = Dcf.objects.filter(symbol=i['symbol'], year=i['year'])
                        print("######## DONE CHECKING FOR DATA EXISTANCE ########")
                        print(record)
                        if record.exists():
                            entry.id = record.id
                        entry.save()
                        count = count+1
                    except Exception as e:
                        print(e)
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'levered-discounted-cash-flow' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        now = datetime.datetime.now()
        for p_symbol in companies:
            response = requests.get(
                f"https://financialmodelingprep.com/api/v4/advanced_levered_discounted_cash_flow?symbol={p_symbol}&apikey={p_api}")
            
            data = json.loads(response.content)
            try:
                if 'Invalid API' in data['Error Message']:
                    print("error api")
                    return ('api error')
                else:
                    return ('other error')
            except:
                for i in data:
                    record = Levereddcf.objects.filter(symbol=p_symbol, year=i['year'])
                    entry = Levereddcf(
                        symbol=p_symbol,
                        year=i.get('year'),
                        revenue=i.get('revenue'),
                        revenuePercentage=i.get('revenuePercentage'),
                        capitalExpenditure = i.get('capitalExpenditure'),
                        capitalExpenditurePercentage = i.get('capitalExpenditurePercentage'),
                        price = i.get('price'),
                        beta = i.get('beta'),
                        dilutedSharesOutstanding = i.get('dilutedSharesOutstanding'),
                        costofDebt = i.get('costofDebt'),
                        taxRate = i.get('taxRate'),
                        afterTaxCostOfDebt = i.get('afterTaxCostOfDebt'),
                        riskFreeRate = i.get('riskFreeRate'),
                        marketRiskPremium = i.get('marketRiskPremium'),
                        costOfEquity = i.get('costOfEquity'),
                        totalDebt = i.get('totalDebt'),
                        totalEquity = i.get('totalEquity'),
                        totalCapital = i.get('totalCapital'),
                        debtWeighting = i.get('debtWeighting'),
                        equityWeighting = i.get('equityWeighting'),
                        wacc = i.get('wacc'),
                        operatingCashFlow = i.get('operatingCashFlow'),
                        pvLfcf = i.get('pvLfcf'),
                        sumPvLfcf = i.get('sumPvLfcf'),
                        longTermGrowthRate = i.get('longTermGrowthRate'),
                        freeCashFlow = i.get('freeCashFlow'),
                        terminalValue = i.get('terminalValue'),
                        presentTerminalValue = i.get('presentTerminalValue'),
                        enterpriseValue = i.get('enterpriseValue'),
                        netDebt = i.get('netDebt'),
                        equityValue = i.get('equityValue'),
                        equityValuePerShare = i.get('equityValuePerShare'),
                        freeCashFlowT1 = i.get('freeCashFlowT1'),
                        operatingCashFlowPercentage = i.get('operatingCashFlowPercentage'),
                    )
                    if record.exists():
                        entry.id = record.id
                    entry.save()
                    count = count+1
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'market-risk-premium' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        now = datetime.datetime.now()
        response = requests.get(
            f"https://financialmodelingprep.com/api/v4/market_risk_premium?apikey={p_api}")
        data = json.loads(response.content)
        try:
            if 'Invalid API' in data['Error Message']:
                print("error api")
                return ('api error')
            else:
                return ('other error')
        except:
            for i in data:
                record = Riskpremium.objects.filter(country=i['country'], continent=i['continent'])
                entry = Riskpremium(
                    country=i.get('country'),
                    continent=i.get('continent'),
                    totalEquityRiskPremium=i.get('totalEquityRiskPremium'),
                    countryRiskPremium=i.get('countryRiskPremium')
                )
                if record.exists():
                    entry.id = record.id
                entry.save()
                count = count+1
        if (p_dtype.lower() != "all"):
            return "success"

    if p_dtype == 'fmp-companies' or p_dtype.lower() == "all":
        matchedType = True
        count = 0
        now = datetime.datetime.now()
        response = requests.get(
            f"https://financialmodelingprep.com/api/v3/stock/list?apikey={p_api}")
        data = json.loads(response.content)
        try:
            if 'Invalid API' in data['Error Message']:
                print("error api")
                return ('api error')
            else:
                return ('other error')
        except:
            for i in data:
                try:
                    record = Fmpcompanies.objects.filter(symbol=i.get('symbol'))
                    entry = Fmpcompanies(
                        symbol=i.get('symbol'),
                        name=i.get('name'),
                        price=i.get('price'),
                        exchange=i.get('exchange'),
                        exchangeShortName=i.get('exchangeShortName'),
                        type=i.get('type')
                    )
                    if record.exists():
                        entry.id = record.id
                    entry.save()
                    count = count+1
                except Exception as e:
                    print(e)
        if (p_dtype.lower() != "all"):
            return "success"

    if(not matchedType):
        return ("not available")
    return "success"
