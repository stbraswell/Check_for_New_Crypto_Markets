import json
import requests
import datetime
import csv
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

#####TODO:
# Add new markets to a list
# Generate html for email
# Hook up email func
# Load APScheduler
# For new markets, create email with graph of movement (send daily for 2? weeks)

### API docs
# api docs: https://bittrex.com/home/api
# https://github.com/thebotguys/golang-bittrex-api/wiki/Bittrex-API-Reference-(Unofficial)

dir = os.path.dirname(__file__)
mrkt_file = os.path.join(dir,'Market_list.csv')
get_markets = 'https://bittrex.com/api/v1.1/public/getmarkets'
get_market_summaries = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
get_market_summaries_indiv = 'https://bittrex.com/api/v1.1/public/getmarketsummary?market=eth-xrp'
now = datetime.datetime.now()
aDayAgo = now - datetime.timedelta(days=1)
aDayAgo_str = str(aDayAgo)[:16]
aDayAgo_str = datetime.datetime.strptime(aDayAgo_str, '%Y-%m-%d %H:%M')
marketList = []


def emailit(body):
	fromaddr = "me@email.com"
	toaddr = ["me@email.com"]
	pfile= '/path/to/file'
	msg = MIMEMultipart('alternative')
	subject= 'New Markets' 
	msg['From'] = fromaddr
	msg['To'] = ", ".join(toaddr) #toaddr
	msg['Subject'] = subject
	file = open(pfile, 'rb') 
	pword= file.read() 
	text = "You found Waldo!  Great Job! -Me"
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(body, 'html')
	msg.attach(part1)
	msg.attach(part2)
	
	#Send it
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, pword)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


# Ping API for market summaries
r=requests.get(get_market_summaries, timeout=5)
var= r.json() 

#  Loop over markets and print Name if it was added within the last day
for mrkt in var['result']:
	# grab 'Created' and convert to datetime
	ts_str =  mrkt['Created'][:16]
	ts = datetime.datetime.strptime(ts_str, '%Y-%m-%dT%H:%M') #"2017-06-06T01:22:35.727"
	marketList.append(mrkt['MarketName'])
	if ts > aDayAgo_str:
		print mrkt['MarketName']

# Write list of all markets to file
#if os.path.isfile(snRetest_counter):		
with open(mrkt_file,'wb') as f:
	clusterwriter = csv.writer(f)
	for item in marketList:
		clusterwriter.writerow([item])

# store all markets in csv
# read csv into list
# when checking for new markets, if its not in list send email
# this way the script can run every hour