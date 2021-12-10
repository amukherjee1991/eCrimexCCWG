#==============================================================================
#!/usr/bin/env python2
#author          :Arghya Mukherjee, Utulsa, APWG
#date            :20110930
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
import re



#eCrimex API
eCrimex_Api=""
# eCrimex_api_url="http://api.ecrimex.net/groups/bc0e1b369b881717a42fb79ce086f9e88213845a"
# eCrimex_api_url="http://api.sandbox.ecrimex.net/groups/dcc920f93ebdccd939030a755febcd57db629dd9"
eCrimex_api_url="https://api.ecx2.ecrimex.net/crypto/entry"
headers = {
    'Authorization': eCrimex_Api,
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "fbc8a920-71c2-81e6-221a-c76e4bde0fa5"
    }

all_address=[]

def fix_date(astring):
	size_date=len(line[2])
	date=line[2]
	date=date[:size_date - 6]
	date= datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
	epoch = datetime.datetime.utcfromtimestamp(0)
	new_date=(date - epoch).total_seconds()
	return int(new_date)

email=""


def find_ltc(regex_string,message):
	
	ltc_match=re.findall(ltc,line[1],re.MULTILINE)
	
	# fix_date(line[2])

	if len(ltc_match)>0:

		
		# bitcoin["address"]=match

		# print match
		for m in ltc_match:
			bitcoin={}
			bitcoin["crimeCategory"]=""
			bitcoin["submitter"]="APWG"
			bitcoin["procedure"]="automated"
			bitcoin["email"]="upload@apwg.org"
			bitcoin["source"]="CDA"
			bitcoin["address"]=m
			bitcoin["timestamp"]=fix_date(line[2])
			bitcoin["currency"]="LTC"
			# print bitcoin
			all_address.append(bitcoin)

def find_btc(regex_string,message):
	btc_match=re.findall(btc,line[1],re.MULTILINE)
	# bitcoin={}
	# bitcoin["submitter"]="APWG"
	# bitcoin["procedure"]="automated"
	# bitcoin["email"]="upload@apwg.org"
	# bitcoin["source"]="CDA"
	if len(btc_match)>0:
		
		# bitcoin["address"]=match

		# print match
		for m in btc_match:
			bitcoin={}
			bitcoin["crimeCategory"]=""
			bitcoin["submitter"]="APWG"
			bitcoin["procedure"]="automated"
			bitcoin["email"]=email
			bitcoin["source"]="CDA"
			bitcoin["timestamp"]=fix_date(line[2])
			bitcoin["currency"]="BTC"
			bitcoin["address"]=m
			# print bitcoin
			all_address.append(bitcoin)

def find_eth(regex_string,message):
	eth_match=re.findall(eth,line[1],re.MULTILINE)
	# 
	if len(eth_match)>0:
		
		for m in eth_match:
			bitcoin={}
			bitcoin["crimeCategory"]=""
			bitcoin["submitter"]="APWG"
			bitcoin["procedure"]="automated"
			bitcoin["email"]=email
			bitcoin["source"]="CDA"
			bitcoin["timestamp"]=fix_date(line[2])
			bitcoin["currency"]="ETH"
			bitcoin["address"]=m
			# print bitcoin
			all_address.append(bitcoin)

def find_xrp(regex_string,message):
	xrp_match=re.findall(xrp,line[1],re.MULTILINE)
	
	if len(xrp_match)>0:
		
		for m in xrp_match:
			bitcoin={}
			bitcoin["crimeCategory"]=""
			bitcoin["submitter"]="APWG"
			bitcoin["procedure"]="automated"
			bitcoin["email"]=email
			bitcoin["source"]="CDA"
			bitcoin["timestamp"]=fix_date(line[2])
			bitcoin["currency"]="XRP"
			bitcoin["address"]=m
			# print bitcoin,message
			all_address.append(bitcoin)


def find_dash(regex_string,message):
	dash_match=re.findall(dash,line[1],re.MULTILINE)
	
	if len(dash_match)>0:
		
		for m in dash_match:
			bitcoin={}
			bitcoin["crimeCategory"]=""
			bitcoin["submitter"]="APWG"
			bitcoin["procedure"]="automated"
			bitcoin["email"]=email
			bitcoin["source"]="CDA"
			bitcoin["timestamp"]=fix_date(line[2])
			bitcoin["currency"]="DASH"
			bitcoin["address"]=m
		# print bitcoin
			all_address.append(bitcoin)

def find_monero(regex_string,message):
	monero_match=re.findall(xmr,line[1],re.MULTILINE)
	
	if len(monero_match)>0:
		
		for m in monero_match:
			bitcoin={}
			bitcoin["crimeCategory"]=""
			bitcoin["submitter"]="APWG"
			bitcoin["procedure"]="automated"
			bitcoin["email"]="null"
			bitcoin["source"]="CDA"
			bitcoin["timestamp"]=fix_date(line[2])
			bitcoin["currency"]="XMR"
			bitcoin["address"]=m
		# print bitcoin
			all_address.append(bitcoin)

def find_doge(regex_string,message):
	doge_match=re.findall(doge,line[1],re.MULTILINE)
	
	if len(doge_match)>0:
		
		for m in doge_match:
			bitcoin={}
			bitcoin["crimeCategory"]="null"
			bitcoin["submitter"]="APWG"
			bitcoin["procedure"]="automated"
			bitcoin["email"]=email
			bitcoin["source"]="CDA"
			bitcoin["timestamp"]=fix_date(line[2])
			bitcoin["currency"]="DOGE"
			bitcoin["address"]=m
		# print bitcoin
			all_address.append(bitcoin)

def find_neo(regex_string,message):
	neo_match=re.findall(neo,line[1],re.MULTILINE)
	
	if len(neo_match)>0:
		
		for m in neo_match:
			bitcoin={}
			bitcoin["crimeCategory"]="null"
			bitcoin["submitter"]="APWG"
			bitcoin["procedure"]="automated"
			bitcoin["email"]=email
			bitcoin["source"]="CDA"
			bitcoin["timestamp"]=fix_date(line[2])
			bitcoin["currency"]="NEO"
			bitcoin["address"]=m
		# print bitcoin
			all_address.append(bitcoin)


#initialised at 0
with open('max_yesterday.csv','r') as csvfile:
	#skip header line
	next(csvfile)
	csv_reader=csv.reader(csvfile)
	for r in csv_reader:
		# print r
		last_row_id=int(r[0])

# read the scraped telegram channel file
with open('cda_scraped.csv','r') as csvfile:
	#skip header line
	next(csvfile)
	csv_reader=csv.reader(csvfile)

	#look for the regular expressions (manually verified)
	for line in csv_reader:
		btc='^[13][a-km-zA-HJ-NP-Z0-9]{26,33}'
		bch="[q|p][a-z0-9]{41}"
		eth="^0x[a-fA-F0-9]{40}"
		ltc="^[LM][a-km-zA-HJ-NP-Z1-9]{26,33}"
		dash="X[1-9A-HJ-NP-Za-km-z]{33}"
		xrp="^r[0-9a-zA-Z]{24,34}"
		xmr="[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}"
		neo="^A[0-9a-zA-Z]{33}"
		doge="^D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}"
		# M8P4sZxQHKmpr69XmJVBAaxB3Aswb
		
		if int(line[0])>last_row_id:

			stringmatch=["intercept","extortion","sextortion","ransomware","generator","blocklist","blacklist","hack","malicious","launder","additional XRP accounts","spam","is moving","stolen","breach","phish","scam"]
			# if "blocklist" in line[1] or "blacklist" in line[1] or "hack" in line[1] or "malicious" in line[1] or "launder" in line[1] or "phish" in line[1] or "scam" in line[1]:
			# if any(stringmatch) in line[1]:
			if any(ext in str(line[1]) for ext in stringmatch):


				find_btc(btc,line[1])
				find_eth(eth,line[1])
				find_ltc(ltc,line[1])
				find_xrp(xrp,line[1])
				find_dash(dash,line[1])
				find_monero(xmr,line[1])
				find_doge(doge,line[1])
				find_neo(neo,line[1])

#write updated row id from telegram
header=['value']
with open("max_yesterday.csv","wb") as csvfile_out:
	writer = csv.writer(csvfile_out)
	writer.writerow(header)
	writer.writerow([line[0]])



def func_post(alist):

	error_list_index=[]
	for i,pl in enumerate(all_address):
		pl=str(pl).replace("'", '\"')
		print pl,i
		
		try:

			response = requests.request("POST", eCrimex_api_url, data=str(pl), headers=headers)
			time.sleep(1)

			print response.status_code
			print response.text
		except:
			error_list_index.append([int(i)])
# all_address=all_address[:5]
func_post(all_address)



def print_addresses(alist):
	for i,add in enumerate(all_address):
		print i,add


print_addresses(all_address)

print len(all_address)





		


