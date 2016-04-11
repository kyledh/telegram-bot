## About
Telegram Bot
## Install
```
$ pip install pyTelegramBotAPI
$ pip install flask
$ git clone https://github.com/kyledh/telegram-bot.git
```
## Setting
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
You must configure HTTPS certificate
```
server
    {
        listen 443 ssl;
        server_name <ip/host where the bot is running>;

        ... HTTPS certificate ...

        location / {
                proxy_pass http://localhost:8443;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_redirect off;
        }
    }
```
## Help
```
/qducc  QDUCC user info
/love  ❤
/ip  Inquiry IP address
eg: /ip 8.8.8.8
/qr Links to QR code
eg: /qr g.cn
/cat Cat pictures
/tts Text to Speech
/test  Test
/help  Help
```
## TODO
- whois
- pic
- disqus