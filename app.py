
import random
import datetime

#--------------google sheet api--------------#

import requests
import json
import re
from bs4 import BeautifulSoup as bs

#----------------line bot api----------------#

from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import tempfile,os
from config import client_id, client_secret, album_id

app = Flask(__name__)

#----------------ACCESS_TOKEN----------------#

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
SECRET = os.environ.get('SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

#----------------my_function----------------#
#柚子積分
def ma_score():
	apikey='AIzaSyAzpWOZ2DM5t84gHbBdUttvKNuuhflOJ6E'
    	getvalueurl='https://sheets.googleapis.com/v4/spreadsheets/1_J3nBaOmvBx9agkXByT-2sMv_vHkR74OHcArc6mluQw/values/A2:B?key=%s' % (apikey)
	res = requests.get(getvalueurl)
    	data = res.content
	
	jsondata = json.loads(data)
	values = jsondata['values']
	
	out="《柚子麻將10月積分》\n"
	i=1

	if not values:
		out="not found"
	else:
        	for row in values:
			out+=('%2d |%3s |%5s\n' % (i,row[0], row[1]))
            		i+=1
    	return out

#妮封面

client = ImgurClient(client_id, client_secret)
images = client.get_album_images('37qwmzq')
Ni_ask_URL = images[0].link
Ni_URL_1 = images[1].link
Ni_URL_2 = images[2].link
Ni_URL_3 = images[3].link

#--------------my_function--------------#

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
	#get取的訊息
	get = event.message.text

#功能
#------------------------------------------------------------------------------------------------------#
	if(get == '帕妮妮?'):
		msg = TextSendMessage('大家好我說帕妮妮一號！' )
        	#回復訊息msg
        	line_bot_api.reply_message(event.reply_token,msg)        
#------------------------------------------------------------------------------------------------------#
    	elif(get == '抽飯飯'):
        	eat = choosewhattoeat()
        
        	msg = TextSendMessage(eat)
        
        	#回復訊息msg
        	line_bot_api.reply_message(event.reply_token,msg)
#------------------------------------------------------------------------------------------------------#
    	elif(get == '柚子積分'):
        	score = ma_score()
        
        	msg = TextSendMessage(score)
        
        	#回復訊息msg
        	line_bot_api.reply_message(event.reply_token,msg)

if __name__ == "__main__":
    app.run()
