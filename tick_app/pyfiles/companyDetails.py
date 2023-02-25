import requests
import json
from tickers.settings import GetSecretProperties

def getCompanyMarketCap(symbol):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/market-capitalization/{symbol}?apikey={p_api}")
    data = json.loads(response.content)
    return data

def getCompanyStockPrice(symbol):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey={p_api}")
    data = json.loads(response.content)
    return data

def getCompaniesQuote(symbols):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/quote/{symbols}?apikey={p_api}")
    data = json.loads(response.content)
    return data

def getScreenerCompaniesData(symbols, period):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/quote/{symbols}?apikey={p_api}")
    data = json.loads(response.content)
    stockPriceChange = getCompanyStockPriceChange(symbols)
    output = []
    for company in data:
        for stockPrice in stockPriceChange:
            if stockPrice['symbol'] == company['symbol']:
                company['yearChange'] = stockPrice[str(period)+'Y']
                company['1D'] = stockPrice['1D']
                company['5D'] = stockPrice['5D']
                company['1M'] = stockPrice['1M']
                company['3M'] = stockPrice['3M']
                company['6M'] = stockPrice['6M']
                company['ytd'] = stockPrice['ytd']
                company['1Y'] = stockPrice['1Y']
                company['3Y'] = stockPrice['3Y']
                company['5Y'] = stockPrice['5Y']
                company['10Y'] = stockPrice['10Y']
                company['max'] = stockPrice['max']
        output.append(company)
    return output

def getCompanyProfile(symbol):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={p_api}")
    data = json.loads(response.content)
    return data

def getCompanyKeyExecutives(symbol):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/key-executives/{symbol}?apikey={p_api}")
    data = json.loads(response.content)
    return data

def getCompanyInsiderTrading(symbol):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    response = requests.get(
        f"https://financialmodelingprep.com/api/v4/insider-trading?symbol={symbol}&page=0&apikey={p_api}")
    data = json.loads(response.content)
    return data

def getCompanyStockPriceChange(symbols):
    SECRETS = {}
    try:
        SECRETS = GetSecretProperties.getSecretsObj()
    except Exception as e:
        print(e)
    p_api = SECRETS['FINANCIALPREP_API_KEY']
    response = requests.get(
        f"https://financialmodelingprep.com/api/v3/stock-price-change/{symbols}?apikey={p_api}")
    data = json.loads(response.content)
    return data