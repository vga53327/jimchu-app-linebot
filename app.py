from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

from linebot.models import (
    MessageEvent, JoinEvent, LeaveEvent, MemberJoinedEvent, MemberLeftEvent, FollowEvent, UnfollowEvent, PostbackEvent,
    TextMessage, ImageMessage,
    TextSendMessage, ImageSendMessage, TemplateSendMessage,
    MessageAction, DatetimePickerAction, PostbackAction, URIAction, CameraAction, CameraRollAction, LocationAction,
    QuickReply, QuickReplyButton,
    ButtonsTemplate,
)

import configparser

import urllib
import random

import requests
from pyquery import PyQuery as pq

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

# 接收 LINE 的資訊

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # print(body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#找圖

@handler.add(MessageEvent, message=TextMessage)
def pixabay_isch(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        try:
            q_string = {'tbm': 'isch', 'q': event.message.text}

            if event.message.text == "user_id":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=str(event))
                )

            url = f"https://www.google.com/search?{urllib.parse.urlencode(q_string)}/"

            res = requests.get(url)
            doc = pq(res.text)

            print('fetch conn finish')

            img_list = []

            for i in doc('img').items():
                img_list.append(i.attr('src'))

            random_img_url = img_list[random.randint(0, len(img_list)+1)]
            print('fetch img url finish')
            print(random_img_url)

            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=random_img_url,
                    preview_image_url=random_img_url
                )
            )
        except:
            pretty_note = '♫♪♬'
            pretty_text = ''
            for i in event.message.text:
                pretty_text += i
                pretty_text += random.choice(pretty_note)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="找不到圖片:" + pretty_text)
            )
            pass



if __name__ == "__main__":
    app.run()
