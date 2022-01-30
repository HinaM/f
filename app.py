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

line_bot_api = LineBotApi('1LfsGLYz1CNlGNlcfDLpluE7FGt4w9W+87FcwVRHeVylKDaCNmLz7DZry85W2jzZXzXpjrt861qc5gGlQzwjK8v0tEUbOTa3If+nN8/y9Z7AY33vsLS7FZQGB1wrLTagLuOqnpQrCJAjm/ZPEh4CQQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3992488dc7b5b2fbded071e2646d8756')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
   
