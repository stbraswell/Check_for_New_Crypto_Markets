import json
import requests
import datetime
import csv

# api docs: https://bittrex.com/home/api
# https://github.com/thebotguys/golang-bittrex-api/wiki/Bittrex-API-Reference-(Unofficial)
get_markets = 'https://bittrex.com/api/v1.1/public/getmarkets'
get_market_summaries = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
get_market_summaries_indiv = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market=eth-xrp'
now = datetime.datetime.now()
aDayAgo = now - datetime.timedelta(days=1)
aDayAgo_str = str(aDayAgo)[:16]
aDayAgo_str = datetime.datetime.strptime(aDayAgo_str, '%Y-%m-%d %H:%M')
r=requests.get(get_market_summaries, timeout=5)
var= r.json() 
marketList = []


for mrkt in var['result']:
	# grab 'Created' and convert to datetime
	ts_str =  mrkt['Created'][:16]
	ts = datetime.datetime.strptime(ts_str, '%Y-%m-%dT%H:%M') #"2017-06-06T01:22:35.727"
	marketList.append(mrkt['MarketName'])
	if ts > aDayAgo_str:
		print mrkt['MarketName']

		
		
with open('Market_list.csv','wb') as f:
	clusterwriter = csv.writer(f)
	for item in marketList:
		clusterwriter.writerow([item])

# store all markets in csv
# read csv into list
# when checking for new markets, if its not in list send email
# this way the script can run every hour