## About
Telegram Bot
## Install
```
$ pip install pyTelegramBotAPI
$ pip install flask
$ git clone https://github.com/kyledh/telegram-bot.git
```
## Setting
### bot.py
```
API_TOKEN = '<api_token>'
BOT_NAME = "@<bot username>"
WEBHOOK_HOST = '<ip/host where the bot is running>'
WEBHOOK_PORT = 8443  # port need to be 'open'
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
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