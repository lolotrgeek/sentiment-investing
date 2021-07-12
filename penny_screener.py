# original script credit goes to https://www.reddit.com/r/algotrading/comments/n7xa2e/screener_for_finding_penny_stocks_about_to_blow/?utm_source=share&utm_medium=ios_app&utm_name=iossmf
# modified with asyncio for much faster results (~30 seconds OLD vs ~3 seconds NEW)

'''
INSTRUCTIONS

> pip install sentiment-investor, aiohttp
sign up for an api key at https://sentimentinvestor.com/
enter your token and key before running the script
'''

import re
import requests
import json
import asyncio
import selectors
import aiohttp
from sentipy.sentipy import Sentipy

token = "EnvxpnjQb1N1epsUBvep"
key = "539369186852268"
sentipy = Sentipy(token=token, key=key)

metric = "RHI"
limit = 96 # can be up to 96
sorted_data = sentipy.sort(metric, limit)
trending_stocks = sorted_data.sort

urls = []
results = []

for stock in trending_stocks:
	if stock.SGP > 1.05:
		urls.append(f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{stock.ticker}?modules=defaultKeyStatistics')

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Windows Fix - https://stackoverflow.com/a/66772242

async def get(url):
	try:
		async with aiohttp.ClientSession() as session:
			async with session.get(url=url) as response:
				response = await response.read()
				response = json.loads(response)
				stock_cap = int(response['quoteSummary']['result'][0]['defaultKeyStatistics']['enterpriseValue']['raw'])
				if 1000000000 > stock_cap > 1:
					ticker = re.split('https://query2.finance.yahoo.com/v10/finance/quoteSummary/| ?modules=defaultKeyStatistics', url)[1][:-1]
					results.append(ticker)
	except:
		pass

async def main(urls):
	await asyncio.gather(*[get(url) for url in urls])


if __name__ == '__main__':
	asyncio.run(main(urls))
	print(results)