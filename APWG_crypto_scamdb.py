#==============================================================================
#!/usr/bin/env python2
#author          :Arghya Mukherjee, Utulsa, APWG
#date            :2020-11-10
#usage           :python pyscript.py
#notes           :keep the APWG[2].csv in the same folder as of the script or change path while reading the csv
#python_version  :2.7 
#==============================================================================

import csv
import pandas as pd
import itertools
import io
import wget
import datetime
import requests
import os
from os import path
import dateutil
import time
import json
import re

#eCrimex API
eCrimex_Api="165c79a6a354f443edfd5119a7ae3eea637f756b"
eCrimex_api_url="http://api.ecrimex.net/groups/bc0e1b369b881717a42fb79ce086f9e88213845a"
# eCrimex_api_url="http://api.sandbox.ecrimex.net/groups/dcc920f93ebdccd939030a755febcd57db629dd9"
headers = {
    'Authorization': eCrimex_Api,
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "fbc8a920-71c2-81e6-221a-c76e4bde0fa5"
    }

cryptoscam_url_add="https://api.cryptoscamdb.org/v1/addresses"
cryptoscam_url_verified="https://api.cryptoscamdb.org/v1/verified"

address_req=requests.get(cryptoscam_url_add)
address_json=address_req.json()

verified_good=requests.get(cryptoscam_url_verified)
verified_good_json=verified_good.json()

#function to create payload
def create_row(k,curr,cat,time):
	d={}
	d['address']=k
	d['currency']=curr
	d['crimeCategory']=cat
	d["submitter"]="APWG"
	d["procedure"]="automated"
	d["email"]="upload@apwg.org"
	d["source"]='cryptoscamdb'
	d['timestamp']=time
	# print d
	# d=str(d).replace("'", '\"')
	return d

def timestamps(t):
	ts=[]
	ts.append(t)


id_list=[]
for k,v in verified_good_json.items():
	if k=='result':
		for items in v:
			for key,value in items.items():
				if items['id'] not in id_list:
					id_list.append(str(items['id']))

print id_list
#adddress of id
error=[]
ts=[]
d={}

#Check if file exists 

if path.exists("cryptoscamdb_wallets.csv"):
	with open("cryptoscamdb_wallets.csv",'r') as csvfile:
		next(csvfile)
		csv_reader=csv.reader(csvfile)
		for line in csv_reader:
			if line[0] not in d:

				d[line[0]]=line[1]
else:
	with open("cryptoscamdb_wallets.csv",'w') as file:
		writer = csv.writer(file)
		writer.writerow(["address","coin","category","timestamps"])
	


with open("cryptoscamdb_wallets.csv",'a') as file:
	writer = csv.writer(file)

	for k,v in address_json.items():
		if k=="result":
			for key,value in v.items():
				if value[0]['id'] not in id_list:
					# print key,value
					btc='^[13][a-km-zA-HJ-NP-Z0-9]{26,33}'
					bch="[q|p][a-z0-9]{41}"
					eth="^0x[a-fA-F0-9]{40}"
					ltc="^[LM][a-km-zA-HJ-NP-Z1-9]{26,33}"
					dash="X[1-9A-HJ-NP-Za-km-z]{33}"
					xrp="^r[0-9a-zA-Z]{24,34}"
					# match=re.findall(eth,key,re.MULTILINE)
					match_eth=re.findall(eth,key,re.MULTILINE)
					match_btc=re.findall(btc,key,re.MULTILINE)
					match_ltc=re.findall(ltc,key,re.MULTILINE)
					if match_btc and key.split(" ")[0] not in d:
						writer.writerow([key.split(" ")[0],"BTC",value[0]['category'],int(str(value[0]['updated'])[:10])])
						pl=create_row(key.split(" ")[0],"BTC",value[0]['category'],int(str(value[0]['updated'])[:10]))
						pl=str(pl).replace("'", '\"')
						pl=pl.replace('u"','"')
						print pl

						ts.append(value[0]['updated'])
						try:

							response = requests.request("POST", eCrimex_api_url, data=pl, headers=headers)
							# time.sleep(.5)
							print response.status_code
							print response.content
						except:
							error.append([key.split(" ")[0],"BTC",value[0]['category'],int(str(value[0]['updated'])[:10]),e])
						

					elif match_eth and key.split(" ")[0] not in d:
						writer.writerow([key.split(" ")[0],"ETH",value[0]['category'],int(str(value[0]['updated'])[:10])])
						pl=create_row(key.split(" ")[0],"ETH",value[0]['category'],int(str(value[0]['updated'])[:10]))
						pl=str(pl).replace("'", '\"')
						pl=pl.replace('u"','"')
						print pl
						try:

							response = requests.request("POST", eCrimex_api_url, data=pl, headers=headers)
							# time.sleep(.5)
							print response.status_code
							print response.content
						except:
							error.append([key.split(" ")[0],"ETH",value[0]['category'],int(str(value[0]['updated'])[:10]),e])

					elif match_ltc and key.split(" ")[0] not in d:
						writer.writerow([key.split(" ")[0],"LTC",value[0]['category'],int(str(value[0]['updated'])[:10])])
						pl=create_row(key.split(" ")[0],"LTC",value[0]['category'],int(str(value[0]['updated'])[:10]))
						pl=str(pl).replace("'", '\"')
						pl=pl.replace('u"','"')
						print pl

						try:

							response = requests.request("POST", eCrimex_api_url, data=pl, headers=headers)
							# time.sleep(.5)
							print response.status_code
							print response.content
						except Exception as e:
							error.append([key.split(" ")[0],"LTC",value[0]['category'],int(str(value[0]['updated'])[:10]),e])
						


print error
print "New: ",set(ts),len(set(ts))
