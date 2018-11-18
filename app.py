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
def ma_score(month):
    apikey='AIzaSyAzpWOZ2DM5t84gHbBdUttvKNuuhflOJ6E'
    getvalueurl='https://sheets.googleapis.com/v4/spreadsheets/1_J3nBaOmvBx9agkXByT-2sMv_vHkR74OHcArc6mluQw/values/%s!A2:B?key=%s' % (month,apikey)
    res = requests.get(getvalueurl)
    data = res.content
	
    jsondata = json.loads(data)
    values = jsondata['values']

    ma_out="《柚子麻將%s月積分》" % (month)
    i=1

    if not values:
         ma_out="not found"
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            ma_out+=('\n %2s |%3s |%5s' % (i,row[0], row[1]))
            i+=1
    return ma_out

#抽飯飯
def choosewhattoeat():
    
    time = ((datetime.datetime.now().hour)+8)%24
    
    apikey='AIzaSyAzpWOZ2DM5t84gHbBdUttvKNuuhflOJ6E'
    getvalueurl='https://sheets.googleapis.com/v4/spreadsheets/1QHptsX3e1chR917a_5s23upr28M3EUfe6x3fAY5BLDQ/values/A:C?key=%s' % (apikey)
    res = requests.get(getvalueurl)
    data = res.content
	
    jsondata = json.loads(data)
    values = jsondata['values']

    alltime_max  =int(values[0][2])
    onlynoon_max =int(values[1][2])

    if not values:
        
        out="not found"
    else:
        
        #AM 10:00 ~ PM 03:00
        if(time > 9 and time <= 14):
        
            num = random.randint(1,alltime_max)
            out = values[num][0]

        #PM 03:00 ~ AM 00:00    
        elif(time > 14 and time <= 23):

            num = random.randint(1,onlynoon_max)
            out = values[num][0]

        #AM 00:00 ~ AM 10:00
        else:

            out = "甲賽"

    return (out)

#妮封面

client = ImgurClient(client_id, client_secret)
images = client.get_album_images('37qwmzq')
Ni_ask_URL = images[0].link
Ni_URL_1 = images[0].link
Ni_URL_2 = images[1].link
Ni_URL_3 = images[2].link
Ni_URL_4 = images[3].link


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
    elif(get == '柚子抽'):
        score = ma_score(datetime.datetime.now().month)
        
        msg = TextSendMessage(score)
        
        #回復訊息msg
        line_bot_api.reply_message(event.reply_token,msg)
#------------------------------------------------------------------------------------------------------#        
    elif(get.find('柚子抽') >= 0):
        score = ma_score(get[3:5])
        
        msg = TextSendMessage(score)
        
        #回復訊息msg
        line_bot_api.reply_message(event.reply_token,msg)
#------------------------------------------------------------------------------------------------------#
    elif(get == '妮妮抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images('nnfQKcW')
            
        index = random.randint(0, len(images) - 1)
        photo_URL = images[index].link
        
        msg = ImageSendMessage(original_content_url=photo_URL,preview_image_url=photo_URL)
        
        #回復訊息msg
        line_bot_api.reply_message(event.reply_token,msg)
#------------------------------------------------------------------------------------------------------#        
    elif(get == '溫妮抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images('pFLy2WH')
            
        index = random.randint(0, len(images) - 1)
        photo_URL = images[index].link
        
        msg = ImageSendMessage(original_content_url=photo_URL,preview_image_url=photo_URL)
        #回復訊息msg
        line_bot_api.reply_message(event.reply_token,msg)        
#------------------------------------------------------------------------------------------------------#
    elif (get == '阿樂抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images('FGxNdmr')

        index = random.randint(0, len(images) - 1)
        photo_URL = images[index].link

        msg = ImageSendMessage(original_content_url=photo_URL, preview_image_url=photo_URL)
        # 回復訊息msg
        line_bot_api.reply_message(event.reply_token, msg)
# ------------------------------------------------------------------------------------------------------#
    elif (get == '熠楷抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_image('KtKrxU2')

        photo_URL = images.link

        msg = ImageSendMessage(original_content_url=photo_URL, preview_image_url=photo_URL)
        # 回復訊息msg
        line_bot_api.reply_message(event.reply_token, msg)
 # ------------------------------------------------------------------------------------------------------#
    elif (get == '詠甯抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_image('UPBza8O')

        photo_URL = images.link

        msg = ImageSendMessage(original_content_url=photo_URL, preview_image_url=photo_URL)
        # 回復訊息msg
        line_bot_api.reply_message(event.reply_token, msg)
# ------------------------------------------------------------------------------------------------------#
    elif (get == '淳中抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_image('NbJ2VYV')

        photo_URL = images.link

        msg = ImageSendMessage(original_content_url=photo_URL, preview_image_url=photo_URL)
        # 回復訊息msg
        line_bot_api.reply_message(event.reply_token, msg)
 # ------------------------------------------------------------------------------------------------------#
    elif (get == '怎麼辦辦抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_image('QeiS74H')

        photo_URL = images.link

        msg = ImageSendMessage(original_content_url=photo_URL, preview_image_url=photo_URL)
        # 回復訊息msg
        line_bot_api.reply_message(event.reply_token, msg)
 # ------------------------------------------------------------------------------------------------------#
    elif(get == '兔題抽'):
        msg = TemplateSendMessage(
        alt_text='快去打開手機，玩妮問我答囉!',
        template=ButtonsTemplate(
            title='妮問我答-簡單',
            text='請問下列關於兔子的敘述，何者正確?',
            thumbnail_image_url=Ni_ask_URL,
            actions=[
                MessageTemplateAction(
                    label='不會流汗',
                    text='正確答案!!兔子沒有汗腺，不會流汗。'
                ),
                MessageTemplateAction(
                    label='對水分的需求比其他動物來的多',
                    text='錯!!對水分的需求比其他動物來的少喔'
                ),
                MessageTemplateAction(
                    label='只喜歡吃胡蘿蔔、高麗菜',
                    text='錯!!甚至會吃麥當勞'
                ),
                MessageTemplateAction(
                    label='捕捉時，抓取耳部，較容易捕捉。',
                    text='請不要虐待兔子，應該要以手持腹部或臀部為主要施力點。'
                )
            ]
        )
        )
        #回復訊息msg
        line_bot_api.reply_message(event.reply_token,msg)
#------------------------------------------------------------------------------------------------------#
    elif(get == '妮妮會什麼?'):
        msg = TemplateSendMessage(
            alt_text='這裡看不到，顆顆',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=Ni_URL_0,
                        title='柚子積分',
                        text='11月積分更新中!!',
                        actions=[
                            MessageTemplateAction(
                                label='11月',
                                text='柚子抽11'
                            ),
                            MessageTemplateAction(
                                label='10月',
                                text='柚子抽10'
                            ),
                            MessageTemplateAction(
                                label=' ',
                                text=' '
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=Ni_URL_1,
                        title='抽一些可怕的東西',
                        text='這邊可怕的東西，大家小心使用。',
                        actions=[
                            MessageTemplateAction(
                                label='計概三',
                                text='熠楷抽'
                            ),
                            MessageTemplateAction(
                                label='計概四',
                                text='詠甯抽'
                            ),
                            MessageTemplateAction(
                                label='離散數學',
                                text='怎麼辦辦抽'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=Ni_URL_2,
                        title='抽我老婆',
                        text='這邊有三個我老婆，大家可以多按按',
                        actions=[
                            MessageTemplateAction(
                                label='妮妮',
                                text='妮妮抽'
                            ),
                            MessageTemplateAction(
                                label='溫妮',
                                text='溫妮抽'
                            ),
                            MessageTemplateAction(
                                label='阿樂',
                                text='阿樂抽'
                            )
                        ]
                    )
                ]
            )
        )

        #回復訊息msg
        line_bot_api.reply_message(event.reply_token,msg)
# ------------------------------------------------------------------------------------------------------#

    #測試指令
    elif (get == '#妮妮抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images('nnfQKcW')

        photo_URL = images[len(images) - 1].link

        msg = ImageSendMessage(original_content_url=photo_URL, preview_image_url=photo_URL)
        # 回復訊息msg
        line_bot_api.reply_message(event.reply_token, msg)
# ------------------------------------------------------------------------------------------------------#
    elif (get == '#阿樂抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images('FGxNdmr')

        photo_URL = images[len(images) - 1].link

        msg = ImageSendMessage(original_content_url=photo_URL, preview_image_url=photo_URL)
        # 回復訊息msg
        line_bot_api.reply_message(event.reply_token, msg)
# ------------------------------------------------------------------------------------------------------#
    elif (get == '#溫妮抽'):
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images('pFLy2WH')

        photo_URL = images[len(images) - 1].link

        msg = ImageSendMessage(original_content_url=photo_URL, preview_image_url=photo_URL)
        # 回復訊息msg
        line_bot_api.reply_message(event.reply_token, msg)
# ------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    app.run()
