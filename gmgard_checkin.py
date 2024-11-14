# -- coding: utf-8 --
import os
import sys
from curl_cffi import requests

GM_COOKIE = os.environ.get("GM_COOKIE","")
COOKIE = os.environ.get("COOKIE", "")
COOKIE_ENV = GM_COOKIE or COOKIE

pushplus_token = os.environ.get("PUSHPLUS_TOKEN")
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN","")
chat_id = os.environ.get("CHAT_ID","")
telegram_api_url = os.environ.get("TELEGRAM_API_URL","https://api.telegram.org") # 代理api,可以使用自己的反代
def telegram_Bot(token,chat_id,message):
    url = f'{telegram_api_url}/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': message
    }
    r = requests.post(url, json=data)
    response_data = r.json()
    msg = response_data['ok']
    print(f"telegram推送结果：{msg}\n")
def pushplus_ts(token, rw, msg):
    url = 'https://www.pushplus.plus/send/'
    data = {
        "token": token,
        "title": rw,
        "content": msg
    }
    r = requests.post(url, json=data)
    msg = r.json().get('msg', None)
    print(f'pushplus推送结果：{msg}\n')

def load_send():
    global send
    global hadsend
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
            hadsend=True
        except:
            print("加载notify.py的通知服务失败，请检查~")
            hadsend=False
    else:
        print("加载通知服务失败,缺少notify.py文件")
        hadsend=False
load_send()

if COOKIE_ENV:
    url = f"https://gmgard.com/api/PunchIn/Do"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Accept":"*/*",
        "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding":"gzip, deflate, br, zstd",
        "Content-Type":"application/json",
        "X-Requested-With":"XMLHttpRequest",
        "Origin":"https://gmgard.com",
        "DNT":"1",
        "Sec-GPC":"1",
        "Connection":"keep-alive",
        "Referer":"https://gmgard.com/",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "Priority":"u=0",
        "Cookie": COOKIE_ENV
    }

    try:
        response = requests.post(url, headers=headers,impersonate="chrome110")
        response_data = response.json()
        print(response_data)
        print(COOKIE_ENV)
        message = response_data.get('message')
        success = response_data.get('success')
        send("gmgard签到", message)
        if success == "true":
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
        else:
            print(message)
            if telegram_bot_token and chat_id:
                telegram_Bot(telegram_bot_token, chat_id, message)
            if pushplus_token:
                pushplus_ts(pushplus_token, "gmgard签到", message)
    except Exception as e:
        print("发生异常:", e)
        print("实际响应内容:", response.text)
else:
    print("请先设置Cookie")