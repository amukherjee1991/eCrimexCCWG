#==============================================================================
#!/usr/bin/env python3
#author          :Arghya Mukherjee, Utulsa, APWG
#date            :20110930
#usage           :python pyscript.py
#notes           :keep the APWG[2].csv in the same folder as of the script or change path while reading the csv
#python_version  :3
#==============================================================================

from telethon import TelegramClient, sync
from telethon import utils
from telethon.tl.functions.messages import GetMessagesViewsRequest
from telethon.tl.functions.messages import ReadHistoryRequest
import csv
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import (
PeerChannel
)

from telethon.tl.functions.messages import (GetHistoryRequest)


api_id =  #add api_id
api_hash = '' # add api_hash
phone = ' ' #add phone number

client = TelegramClient('session_name', api_id, api_hash).start()

me = client.get_me()

user_input_channel='' # add telegram channel number

if user_input_channel.isdigit():
    entity = PeerChannel(int(user_input_channel))
else:
    entity = user_input_channel

my_channel = client.get_entity(entity)

offset_id = 0
limit = 100
all_messages = []
total_messages = 0
total_count_limit = 0
all_id=[]
all_date=[]

# all_messages=[]
while True:
    # print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
    history = client(GetHistoryRequest(
        peer=my_channel,
        offset_id=offset_id,
        offset_date=None,
        add_offset=0,
        limit=limit,
        max_id=0,
        min_id=0,
        hash=0
    ))
    if not history.messages:
        break
    messages = history.messages
    for message in messages:
        all_messages.append(message.message)
        all_id.append(message.id)
        all_date.append(message.date)
    offset_id = messages[len(messages) - 1].id
    total_messages = len(all_messages)
    if total_count_limit != 0 and total_messages >= total_count_limit:
        break

id_message=zip(all_id[::-1],all_messages[::-1],all_date[::-1])

with open('cda_scraped.csv', 'w') as file:
	writer = csv.writer(file)
# #         writer.writerow([time, views, id, channel_username, text])
	for im in id_message:
		# print (im[0],",",im[1])
		try:

			message=im[1].decode()
			writer.writerow([im[0],message,im[2]])
		except:
			writer.writerow([im[0],im[1],im[2]])
		# try:

		# 	writer.writerow([im[0],im[1]])
		# except:
		# 	writer.writerow([im[0],im[1].encode('utf-8')])