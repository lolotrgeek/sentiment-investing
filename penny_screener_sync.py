import requests
import sentipy
from sentipy.sentipy import Sentipy

token = "<your api token>"
key = "<your api key>"
sentipy = Sentipy(token=token, key=key)

metric = "RHI"
limit = 96  # can be up to 96
sortData = sentipy.sort(metric, limit)
trendingTickers = sortData.sort

stock_list = []

for stock in trendingTickers:

    yf_json = requests.get(
        "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}?modules=summaryDetail%2CdefaultKeyStatistics%2Cprice".format(stock.ticker)).json()

    stock_cap = 0

    try:
        volume = yf_json["quoteSummary"]["result"][0]["summaryDetail"]["volume"]["raw"]
        stock_cap = int(yf_json["quoteSummary"]["result"][0]["defaultKeyStatistics"]["enterpriseValue"]["raw"])
        exchange = yf_json["quoteSummary"]["result"][0]["price"]["exchangeName"]

        if stock.SGP > 1.3 and stock_cap > 200000000 and volume > 500000 and exchange == "NasdaqGS" or exchange == "NYSE":
            stock_list.append(stock.ticker)

    except:
        pass

print(stock_list)
