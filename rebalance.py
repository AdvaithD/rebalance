import requests
import pandas as pd
import numpy as np

COUNT = 20

ticker_url = "https://api.coinmarketcap.com/v2/ticker/"
ticker_params = {"limit": COUNT, "structure": "array"}

ticker_response = requests.get(ticker_url, ticker_params).json()
tickers = ticker_response["data"]

def extract_caps(coin):
    return {
        "symbol": coin['symbol'],
        "market_cap": coin['quotes']['USD']['market_cap']
    }

market_caps = list(map(extract_caps, tickers))

fund = pd.DataFrame(market_caps, columns=["symbol", "market_cap"])

fund['market_cap'] = fund['market_cap'] / fund['market_cap'].sum()
fund['allocation'] = fund['market_cap']

for i in fund.index:
    overflow = fund.loc[i, 'allocation'] - 0.1

    if(overflow > 0):
        fund.loc[i, 'allocation'] = 0.1
        rest = fund.loc[i + 1:, "market_cap"]
        nested_alloc = rest / rest.sum()
        fund.loc[i + 1:, "allocation"] += overflow * nested_alloc

fund['allocation'] = round(fund['allocation'] * 100, 2)

############################## HISTORICAL MARKET CAPS ##########################

table = pd.read_csv("crypto-markets.csv")
table = table[["symbol", "market", "date"]]
