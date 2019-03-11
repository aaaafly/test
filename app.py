
import json

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)


ACCESS_TOKEN = 'dy6ze9aF7gFIwzqoflHoPRV/Z8aO/NpWHswJt8Tzj02dIISCVDRZeAprehpfVzpvMX0grDAgycZBaT3WadkxhQeS3ZpMRTZTTaggufUGa4XWf5xIPWz/dJ9SOKI6R7hAqazmeJDXXJzLTb3LFOpRZwdB04t89/1O/w1cDnyilFU='
SECRET = 'e38e393f3a88e64d2d2c49a556fcac5c'

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
    user_id = event.source.user_id
    print("user_id =", user_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@app.route('/')
def homepage():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run()
