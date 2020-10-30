#==============================================================================
#!/usr/bin/env python2
#author          :Arghya Mukherjee, Utulsa, APWG
#date            :20110905
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
import dateutil
import time
import json

from os import path
#Bitcoin_abuse_api_key
api_token="IlgGuZgN7QliY52WGD1PXMM16AsDTd2vEjjCnxwgfM2fSiPxYegC1wgeIEPW"
#Download file from bitcoinabuse every day
today=datetime.datetime.now().strftime("%Y-%m-%d")
url_bitcoinabuse="https://www.bitcoinabuse.com/api/download/1d?api_token="+api_token
out_file = 'data'+"_"+today+"_1d"+".csv"
os.system("wget -O {0} {1}".format(out_file, url_bitcoinabuse))
#Abuse Types
url_bitcoinabuse_type="https://www.bitcoinabuse.com/api/abuse-types?api_token="+api_token
bitcoinabuse_types=requests.get("https://www.bitcoinabuse.com/api/abuse-types?api_token=IlgGuZgN7QliY52WGD1PXMM16AsDTd2vEjjCnxwgfM2fSiPxYegC1wgeIEPW")
alist=bitcoinabuse_types.json()


ids=[]
labels=[]
for rows in alist:
    for k,v in rows.items():
        if k=="id":
            ids.append(v)
        else:
            labels.append(v.encode("utf-8"))
mydict=dict(zip(ids,labels))
print mydict
print "#############################################"

def dict_finder(dict, value):
    for k, v in dict.iteritems():
        if k == value:
            return v

#eCrimex API
eCrimex_Api="" #<- my api goes here
eCrimex_api_url="http://api.ecrimex.net/groups/bc0e1b369b881717a42fb79ce086f9e88213845a"
# eCrimex_api_url="http://api.sandbox.ecrimex.net/groups/dcc920f93ebdccd939030a755febcd57db629dd9"
headers = {
    'Authorization': eCrimex_Api,
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "fbc8a920-71c2-81e6-221a-c76e4bde0fa5"
    }


#function to fix date format
def time_convert(d):

	new_date=dateutil.parser.parse(d).strftime('%s')
	return new_date


btc=[]
alist=[]
parser_list=[]

with open(out_file,'r') as csvfile:
	csv_reader=csv.reader(csvfile)
	for line in csv_reader:
		# line[5]=line[5].decode("utf-8")
		# alist=[]
		
		try:

			if line[0].isdigit()==True:
				payload ={}
				alist.append([line[0],line[1],time_convert(line[8]),"bitcoinabuse.com"])
				btc.append(line[1])

				payload["address"]=line[1]
				payload["timestamp"]=int(time_convert(line[8]))
				payload["source"]="bitcoinabuse.com"
				payload["email"]="upload@apwg.org"
				payload["submitter"]="APWG"
				payload["procedure"]="automated"
				payload["currency"]="BTC"
				x=dict_finder(mydict,line[2])
				payload["crimeCategory"]=dict_finder(mydict,int(line[2]))
				# print payload
			parser_list.append(payload)
			
		except:
		
			continue


error_list_index=[]
for i,pl in enumerate(parser_list):

	pl=str(pl).replace("'", '\"')
	print pl,i
	# print pl
	try:

		response = requests.request("POST", eCrimex_api_url, data=str(pl), headers=headers)
		time.sleep(.5)

		print response.status_code
	except:
		error_list_index.append([int(i)])

print error_list_index



