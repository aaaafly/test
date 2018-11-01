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

    ma_out="《柚子麻將10月積分》"
    i=1

    if not values:
         ma_out="not found"
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            ma_out += ('\n%2d |%3s |%5s' % (i,row[0], row[1]))
            i+=1
    return ma_out

#抽飯飯
def choosewhattoeat():
    time = ((datetime.datetime.now().hour)+8)%24

    if(time >=10 and time <= 14):
        
        num = random.randint(1,10)           
    
        if(num==1): 
            out='瓦城玩躲貓貓'
        elif(num==2):
            out='麥當當找兔子'
        elif(num==3):
            out='大告'
        elif(num==4):
            out='大J'
        elif(num==5):
            out='告野烤人肉飯'
        elif(num==6):
            out='紅辣椒省起來'
        elif(num==7):
            out='八方'
        elif(num==8):
            out='拉亞'
        elif(num==9):
            out='宏爺'
        elif(num==10):
            out='黑店嘿嘿嘿'
            
    elif(time >14 and time <= 23):

        num = random.randint(1,8)

        if(num==1): 
            out='瓦城玩躲貓貓'
        elif(num==2):
            out='麥當當找兔子'
        elif(num==3):
            out='大告'
        elif(num==4):
            out='大J'
        elif(num==5):
            out='告野烤人肉飯'
        elif(num==6):
            out='紅辣椒省起來'
        elif(num==7):
            out='八方'
        elif(num==8):
            out='黑店嘿嘿嘿'
    else:

        out = "甲賽"

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
    elif(get == '柚子抽'):
        score = "測試"
        
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
    elif(get == '妮問我答-簡單'):
        msg = TemplateSendMessage(
        alt_text='快去打開手機，玩妮問我答囉!',
        template=ButtonsTemplate(
            title='妮問我答-簡單',
            text='請問下列關於兔子的敘述，何者正確?',
            thumbnail_image_url=Ni_ask_URL,
            actions=[
                MessageTemplateAction(
                    label='不會流汗',
                    text='正確答案!!兔子沒有汗腺，不會流汗。\n ◎你獲得新指令-熠楷抽'
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
    elif(get == '妮問我答-困難'):
        msg = TemplateSendMessage(
        alt_text='快去打開手機，玩妮問我答囉!',
        template=ButtonsTemplate(
            title='妮問我答-困難',
            text='二進制數值1001.01等於下列何者十進制數值?',
            thumbnail_image_url=Ni_ask_URL,
            actions=[
                MessageTemplateAction(
                    label='9.25',
                    text='正確解答 \n ◎你獲得新指令-阿樂抽'
                ),
                MessageTemplateAction(
                    label='9.75',
                    text='這是1001.11'
                ),
                MessageTemplateAction(
                    label='13.25',
                    text='這是1101.01'
                ),
                MessageTemplateAction(
                    label='13.75',
                    text='這是1101.11'
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
                        thumbnail_image_url=Ni_URL_1,
                        title='抽兩個噁男',
                        text='這邊有兩個噁男，小心使用',
                        actions=[
                            MessageTemplateAction(
                                label='計概三',
                                text='熠楷抽'
                            ),
                            MessageTemplateAction(
                                label=' ',
                                text=' '
                            ),
                            MessageTemplateAction(
                                label='計概四',
                                text='詠甯抽'
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
                    ),
                    CarouselColumn(
                        thumbnail_image_url=Ni_URL_3,
                        title='我要答題喔喔喔喔喔',
                        text='題目沒更新',
                        actions=[
                            MessageTemplateAction(
                                label='兔題',
                                text='妮問我答-簡單'
                            ),
                            MessageTemplateAction(
                                label=' ',
                                text=' '
                            ),
                            MessageTemplateAction(
                                label='計概一',
                                text='妮問我答-困難'
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
