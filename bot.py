#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import personal# This is my personal file
from utils import *
import telebot
import logging
import json


CONFIG = json.load(open('config.json'))

API_TOKEN = CONFIG['api_token']
BOT_NAME = CONFIG['@bot_name']

WEBHOOK_HOST = CONFIG['webhook_host']
WEBHOOK_PORT = CONFIG['webhook_port']
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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                 ("你好! 我是"+BOT_NAME+"\n"
                  "/help 获取指令详情\n(๑•̀ㅂ•́)ﻭ✧"))


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, (
"""
/qducc  青大CC信息
/love  在一起
/ip  IP 归属地
eg: /ip @8.8.8.8
/test  测试指令
/help  获取指令详情
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


@bot.message_handler(commands=['test'])
def send_test(message):
    bot.send_message(message.chat.id,
                 ('❤️'))


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, message.text)


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        debug=True)
