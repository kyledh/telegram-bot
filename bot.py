#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import telebot
import logging


API_TOKEN = '<api_token>'

WEBHOOK_HOST = '<ip/host where the bot is running>'
WEBHOOK_PORT = 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_URL_BASE = "https://%s" % (WEBHOOK_HOST)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data()
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_messages([update.message])
        return ''
    else:
        flask.abort(403)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 ("Hi! (๑•̀ㅂ•́)و✧ 我是 Kyle's Bot.\n"
                  "我一直在这里等着你哦."))


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        debug=True)