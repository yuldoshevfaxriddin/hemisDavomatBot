import requests as r


headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
}
proxy = {
    'http':'http://51.68.140.136:8080',
    'https':'https://51.68.140.136:8080'
}
url  = 'https://httpbin.org/ip'
url_test = 'https://student.ubtuit.uz'

print(r.get(url).text)
print(r.get(url, headers=headers).text)
print(r.get(url, headers=headers,proxies=proxy).text)
# print(r.get(url, headers=headers,proxies=proxies).text)


# print(r.get(url_test).text)
# print(r.get(url_test, headers=headers).text)
# print(r.get(url_test, headers=headers,proxies=proxies).text)
# print(r.get(url_test, headers=headers,proxies=proxy).text)
