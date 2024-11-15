import os
import sys
from curl_cffi import requests

GM_COOKIE = os.environ.get("GM_COOKIE","")
COOKIE_ENV = GM_COOKIE

body = """
    {}
"""

response = requests.post(
    url="https://gmgard.com/api/PunchIn/Do",
    impersonate="chrome120",
    headers={
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
        "Priority":"u=0"
    },
    cookies=COOKIE_ENV,
    data=body
    
)

print(response.text)
