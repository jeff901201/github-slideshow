# app.py輸入：
# ======載入LineBot所需要的套件======
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


# ======這裡是呼叫的py功能======
import os
import datetime
import time
import re

# ======這裡是呼叫的檔案內容=====
# from Message_Food import *
# from Message_Photo import *
# from Message_History import *


# ========ChatBot開始==========

app = Flask(__name__)

# Channel Access Token(TOKEN)
line_bot_api = LineBotApi(
    'AGhhX07Z2jbJtJRMnlOWVeZM33x7V7OLfgiLdQhfKsD4LvSY6gS9j6cFbXFNRhJrGdg5ck/R/9a/i8auqkPsKK6R+D+yEfBJ6/tYXB2KwvG7Igz3yaMR1HdN8ftk1lrniFYiZRik1MmuZeiVdIo9ewdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('bdf756c2189c2d8d9605630c1b521d66')
# Your user ID
line_bot_api.push_message(
    'U0ce0ad2e18e22d8294456f03a27454e5', TextSendMessage(text='恭喜成功第一步！'))

# ========監聽所有來自 /callback 的 Post Request==========


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# ========訊息傳遞區塊==========
##### 基本上程式編輯都在這個function #####


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    if re.match('啟動', message):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('啟動'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
# 使用re.match做文字比對比較不會有資安疑慮
# reply無法回覆多條訊息，只能回覆一條訊息且無法主動回覆
# "TextSendMessage"line所規定的格式
# 訊息傳遞有兩種1.reply 2.psuh


# ========主程式==========
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  # "0,0,0,0"代表全世界的ip都可以向機器人連線
