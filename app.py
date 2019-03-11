

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

app = Flask(__name__)

#----------------ACCESS_TOKEN----------------#

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
SECRET = os.environ.get('SECRET')

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # get user id when reply
    user_id = (str)event.source.user_id
    group_id = (str)event.source.group_id
    
    
    msg = "user_id =" + user_id + "\ngroup_id = " + group_id

    line_bot_api.reply_message(event.reply_token,msg)
    
if __name__ == "__main__":
    app.run()
