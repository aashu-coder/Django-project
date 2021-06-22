import requests
import random

url = "https://www.fast2sms.com/dev/bulk"

x=str(random.randrange(100,999))

querystring = {"authorization":"QKCX8k1MzLjm7yd5oAelYi9JbfcpTPWG6rgN4DB2HFxOt0wnvIJXqwZ4PIAdy02TBLRuQDpasemVKz5l","sender_id":"FSTSMS","language":"english","route":"qt","numbers":"9424995834","message":"8748","variables":"{#BB#}","variables_values":"1234567890"}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)