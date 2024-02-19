import requests as r
import json
import queue
import threading

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
}

url  = 'http://httpbin.org/ip'
url_ip_info = 'http://ipinfo.io/json'
url_test = 'http://student.ubtuit.uz'
amusoft = 'http://amusoft.uz/'
s = r.Session()

with open("proxy.txt","r") as file:
    proxy_list = json.loads(file.read())
# print(len(proxy_list['proxies']))


with open("proxy_2.txt","r") as file:
    proxy_2 = file.read().split('\n')
print(len(proxy_2))

temp = ['194.182.178.90', '162.223.94.164', '159.203.61.169', '207.2.120.15', '198.176.56.39', '202.5.16.44', '198.176.56.41', '198.176.56.42', '207.2.120.16', '89.145.162.81', '103.127.1.130', '198.176.56.43', '142.171.194.101', '162.223.91.11', '167.71.5.83', '114.156.77.107', '128.199.202.122', '159.65.77.168', '202.131.65.110', '190.103.177.131', '133.18.234.13', '103.135.103.1', '52.76.70.173']

heards = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'
}
q = queue.Queue()
# for i in proxy_2:
for i in temp:
    q.put(i)


count = 0
succes_list = []

def check_proxy():
    global q
    global count
    global succes_list
    org_url = url_test
    while not q.empty():
        ip = q.get()
        try:
            proxy = {
                'http':f"http://{ip}",
                'https':f"https://{ip}"
            }        
            respons = s.get(org_url,proxies=proxy,timeout=10)
            # r_ip = json.loads(respons.text)['ip']
            # # r_ip = json.loads(respons.tex)['origin']
            print(f'{count} succes {ip}')
            with open(f'proxy/{ip}.html','w',encoding='utf-8') as file:
                file.write(respons.text)
            succes_list.append(ip)
            # print(respons.text)
        except Exception as ex:
            print(f'{count} fail {ip}')
            print(ex)
            # break
        finally:
            count += 1
    print('ip ',succes_list)


# for _ in range(10):
threading.Thread(target=check_proxy).start()


# count = 0
# #for i in range(10):
# # for i in proxy_list['proxies']:
# for i in range(len(proxy_2)):
#     #ip = proxy_list['proxies'][i]['proxy']
#     # ip = i['proxy']
#     ip = proxy_2[count]

#     # proxy = {
#     #         'http':f"http://{ip}",
#     #         'https':f"https://{ip}"
#     #     }
#     # respons = s.get(url_ip_info,proxies=proxy,timeout=5)
#     # print(f'{count} succes {ip}',json.loads(respons.text)['ip'])
#     try:
        
#         proxy = {
#             'http':f"http://{ip}",
#             'https':f"https://{ip}"
#         }        
#         respons = s.get(url_ip_info,proxies=proxy,timeout=5)
#         print(f'{count} succes {ip}',json.loads(respons.text)['ip'])
#         with open('proxy-succes.txt','a') as file:
#             file.write(json.loads(respons.text)['ip']+'\n')
#     except:
#         print(f'{count} fail {ip}')
#     count += 1
#     #print(proxy_list['proxies'][i]['proxy'])
# #print(s.get(url, headers=headers,proxies=proxy).text)


