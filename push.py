import schedule
import time
import random

from linebot import LineBotApi
from linebot.models import *
from imgurpython import ImgurClient

import requests
import json
import re
from bs4 import BeautifulSoup as bs


import os

secrets = 'e38e393f3a88e64d2d2c49a556fcac5c'
channel_access_token = 'dy6ze9aF7gFIwzqoflHoPRV/Z8aO/NpWHswJt8Tzj02dIISCVDRZeAprehpfVzpvMX0grDAgycZBaT3WadkxhQeS3ZpMRTZTTaggufUGa4XWf5xIPWz/dJ9SOKI6R7hAqazmeJDXXJzLTb3LFOpRZwdB04t89/1O/w1cDnyilFU='
your_id='Uf5cf17f090a2dca6b8631ee06816306a'

line_bot_api = LineBotApi(channel_access_token)

def push():
    print("working at")
    print(time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()))

    msg1 = TextSendMessage("%Y-%m-%d %H:%M:%S\n", time.localtime())
    line_bot_api.push_message(your_id,messages=msg1)
    msg2 = ImageSendMessage(original_content_url=https://www.instagram.com/p/BtvENlGHLnN/media/?size=l,preview_image_url=https://www.instagram.com/p/BtvENlGHLnN/media/?size=l)
    line_bot_api.push_message(your_id,messages=msg2)
    
  
schedule.every().hour.do(push)

while True:
    schedule.run_pending()
    time.sleep(1)