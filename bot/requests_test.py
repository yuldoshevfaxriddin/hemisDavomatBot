import requests as r
http_proxy  = "http://185.203.238.204:8080"
# https_proxy = "https://10.10.1.11:1080"
# ftp_proxy   = "ftp://10.10.1.10:3128"

proxy = {
    'http':'195.158.16.9:3128',
    # 'https':'46.47.197.210:31228'
    }

proxies = { 
              "http"  : http_proxy, 
            #   "https" : https_proxy, 
            #   "ftp"   : ftp_proxy
            }

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
}

url  = 'https://httpbin.org/ip'
url_test = 'https://student.ubtuit.uz'

print(r.get(url).text)
print(r.get(url, headers=headers).text)
print(r.get(url, headers=headers,proxies=proxies).text)
print(r.get(url, headers=headers,proxies=proxy).text)

