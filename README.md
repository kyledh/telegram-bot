## 关于

Telegram Bot

## 安装

```
$ pip install pyTelegramBotAPI
$ pip install flask
$ git clone https://github.com/kyledh/telegram-bot.git
```

## 设置

```
$ cd telegram-bot
$ cp config.json.sample config.json
```

### config.json

```
{
    "api_token": "53a1sc531zx53c1z83c43a84sd5s",
    "bot_name": "@nxxx_bot",
    "webhook_host": "a.com",
    "webhook_port": 8443,
    "webhook_listen": "0.0.0.0"
}
```

### nginx.conf

必须配置 HTTPS 证书
```
server
    {
        listen 443 ssl;
        server_name <ip/host where the bot is running>;

        ... HTTPS 证书 ...

        location / {
                proxy_pass http://localhost:8443;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_redirect off;
        }
    }
```

## 帮助

- /ip  查新 IP 地址
- /cat  猫
- /webshot  网页截图
eg: /ip 8.8.8.8
- /qr 链接转二维码
eg: /qr g.cn.
- /tts 文字转语音
eg: /tts 你好
eg: /tts en-How are you
- /help  查看指令

## TODO

- whois
- pic
- disqus
- 小黄鸡

## 感谢

[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

[python-telegram-bot](https://github.com/pAyDaAr/python-telegram-bot)
