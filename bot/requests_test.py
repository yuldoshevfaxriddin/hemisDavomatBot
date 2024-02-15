import requests as r

proxy = {
    'http':'46.47.197.210:31228',
    'https':'46.47.197.210:31228'
    }

url  = 'https://httpbin.org/ip'
url_test = 'https://student.ubtuit.uz'

res = r.get(url,proxies=proxy)
print(res)
print(res.text)
