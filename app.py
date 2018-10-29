from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('dy6ze9aF7gFIwzqoflHoPRV/Z8aO/NpWHswJt8Tzj02dIISCVDRZeAprehpfVzpvMX0grDAgycZBaT3WadkxhQeS3ZpMRTZTTaggufUGa4XWf5xIPWz/dJ9SOKI6R7hAqazmeJDXXJzLTb3LFOpRZwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e38e393f3a88e64d2d2c49a556fcac5c')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    app.run()
