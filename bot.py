#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import personal  # This is my personal file
from utils import *
import telebot
import logging
import json


CONFIG = json.load(open('config.json'))

BOT_NAME = CONFIG['bot_name']

WEBHOOK_URL_BASE = "https://%s" % (CONFIG["webhook_host"])
WEBHOOK_URL_PATH = "/%s/" % (CONFIG["api_token"])

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(CONFIG["api_token"])

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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                 ("你好! 我是"+BOT_NAME+"\n"
                  "/help 获取指令详情\n(๑•̀ㅂ•́)ﻭ✧"))


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, (
"""
/qducc  QDUCC user info
/love  ❤
/ip  Inquiry IP address
eg: /ip 8.8.8.8
/qr  Links to QR code
eg: /qr g.cn
/cat  Cat pictures
/tts  Text to Speech
/test  Test
/help  Help
"""))


@bot.message_handler(commands=['love'])
def send_pastdays(message):
    love = personal.love()
    PASTDAYS = love.pastdays()
    bot.send_message(message.chat.id,
                 ("❤️❤️❤️已经在一起"+PASTDAYS+"天"))


@bot.message_handler(commands=['cat'])
def send_pic(message):
    url = 'http://thecatapi.com/api/images/get?format=src&type=jpg'
    file = download(url)
    bot.send_photo(message.chat.id, file) 


@bot.message_handler(commands=['qr'])
def qr(message):
    text = message.text.split(' ')[1]
    url = 'https://api.qrserver.com/v1/create-qr-code/?size=500x500&data=' + text
    file = download(url, type='qr')
    bot.send_photo(message.chat.id, file)


@bot.message_handler(commands=['whois'])
def send_whois(message):
    pass


@bot.message_handler(commands=['ip'])
def send_ip_address(message):
    ip = message.text.split(' ')[1].encode('utf-8')
    ret_dict = ip_address(ip)
    bot.send_message(message.chat.id,
                 ("IP: "+ip+"\n"
                   +ret_dict['address']+"\n"
                   +ret_dict['geoip']))


@bot.message_handler(commands=['qducc'])
def send_qducc(message):
    qducc = personal.qducc()
    ret_dict = qducc.qducc_user_info()
    bot.send_message(message.chat.id,
                 ("注册用户数: "+ret_dict['user_count']+"\n"
                    +"激活用户数: "+ret_dict['user_activate_count']+"\n"
                    +"今日活跃用户数: "+ret_dict['user_request_count']+"\n"))


@bot.message_handler(commands=['tts'])
def tts(message):
    text = message.text.split(' ')[1]
    url = 'http://tts.baidu.com/text2audio'
    params = {'lan': 'zh','ie': 'UTF-8','text': text,}
    file = download(url,params=params)
    bot.send_voice(message.chat.id,file)


@bot.message_handler(commands=['test'])
def send_test(message):
    bot.send_message(message.chat.id,
                 ('❤️'))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, message.text)


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app.run(host=CONFIG["webhook_listen"],
        port=CONFIG["webhook_port"],
        debug=True)
