import requests as r
import bs4
import json

URL_HOME = "https://student.ubtuit.uz" #  home page 
URL_TABLE = "https://student.ubtuit.uz/education/exam-table" #  dars jadvali
URL_LOGIN = "https://student.ubtuit.uz/dashboard/login" # login page
URL_DAVOMAT = 'https://student.ubtuit.uz/education/attendance' # davomat

TOKEN = "5976427002:AAE5Yiuvv1Ws6Ca-oklP68t3Fa9SzlFftGM"
URL_SEND_MESSAGE = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def sendMessageBot(text,user = '1742197944'):
    payload = {
        "text": text,
        "chat_id":user,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
        "disable_notification": False,
        "reply_to_message_id": None
    }
    headers = {
        "accept": "application/json",
        "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
        "content-type": "application/json"
    }

    response = r.post(URL_SEND_MESSAGE, json=payload, headers=headers)

    print(response.text)

def getSemestrsList(base_html):
    soup = bs4.BeautifulSoup(base_html,'lxml')
    data = soup.find('div',{'id':'attendance-grid'})
    semestrs_list = data.find('div',{'class':'info-box box-mini'}).find('ul',{'class':'pagination'}).findAll('li')
    semestrs = []
    #URL_DAVOMAT = 'https://student.ubtuit.uz/education/attendance' # davomat
    for i in semestrs_list:
        semestrs.append({'text':i.find('a').text,
                         'link':URL_DAVOMAT + i.find('a')['href']})
    return semestrs
    

def getDavomatList(base_html):
    soup = bs4.BeautifulSoup(base_html,'lxml')
    try:
        data = soup.find('div',{'id':'attendance-grid'})
        davomat_list = data.find('div',{'class':'box box-default'}).find('div',{'id':'data-grid'}).find('table').find('tbody').findAll('tr')
        respons_list = []
        for i in davomat_list:
            t = []
            for a in i.findAll('td'):
                t.append(a.text)
            respons_list.append(t)
        return respons_list
    
    except :
        return 'error'
    

def hemisLoginClient(user_id=None,user_ps=None ):
    if not (user_id is None or user_ps is None):
        session= r.Session()
        headers = {
            'User-Agent':'Chrome/51.0.2704.103 Safari/537.36'
        }
        respons_get = session.get( URL_LOGIN, headers = headers)
        html = respons_get.text
        soup = bs4.BeautifulSoup(html,'lxml')
        csrf_frontend = soup.find("input")['value']
        login_data = {
            '_csrf-frontend':csrf_frontend,
            'FormStudentLogin[login]':user_id,
            'FormStudentLogin[password]':user_ps
            }
        respons_post = session.post(URL_LOGIN, data=login_data, cookies = respons_get.cookies.get_dict())
        if respons_get.status_code != 200:
            print(f'Error {respons_get.url} status code not 200')
            return
        '''
        print(respons_get)
        print(respons_get.cookies.get_dict())
        print(respons_get.text)
        print(respons_post)
        print(respons_post.cookies.get_dict())
        print(respons_post.text)
        '''
        login_data['cookies'] = respons_post.cookies.get_dict()
        with open('cookies.json','w') as file:
           file.write(json.dumps(respons_post.cookies.get_dict()))

        # return login_data
        return session

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br', 
    'Accept-Language': 'en-US,en;q=0.5', 
    'Connection': 'keep-alive', 
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 
    'Cookie': 'frontend=sovof9tl1bb5v9leagkhq7sh9v; _csrf-frontend=fb1319230a0efba0a4e239d780d418262087be233118c41abada040f7318743ca%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22IQ0H4FjPm1f0JT90C1s5l-ROmIt_3Vth%22%3B%7D; _frontendUser=e65d589ae348dcb1cbdfaae24486c23040114a27b01dd93da24890ddd609bf34a%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22_frontendUser%22%3Bi%3A1%3Bs%3A46%3A%22%5B%2218%22%2C%22tG3FjTMA1yF6uNcm2Wx7O3KVRIU2ETxP%22%2C3600%5D%22%3B%7D', 
    'DNT': '1', 'Host': 'student.ubtuit.uz', 
    'Referer': 'https://student.ubtuit.uz/education/attendance', 
    'Sec-Fetch-Dest': 'empty', 
    'Sec-Fetch-Mode': 'cors', 
    'Sec-Fetch-Site': 'same-origin', 
    'Sec-GPC': '1', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0', 
    'X-CSRF-Token': 'vOT1umyOs_jlvZLQsx8KXMve5_w_4dN4KDQwKovRp8b1tcXyWMjZqIiM9OD5SzNsiO-UyVPMgTdFfUR1uIfTrg==', 
    'X-PJAX': 'true', 
    'X-PJAX-Container': '#attendance-grid', 
    'X-Requested-With': 'XMLHttpRequest'
    }

user_id = ''
user_ps = ''

client = hemisLoginClient(user_id = user_id,user_ps = user_ps)
#print(client)

t = client.get(URL_DAVOMAT)
# t = r.get(URL_DAVOMAT,cookies=local_cookies)
print(t)
davomat = getDavomatList(t.text)
message = ''
if davomat[0][0]=="Ma'lumotlar mavjud emas":
    print('Sizda qoldirilgan darslar yo\q !')
    sendMessageBot('Sizda qoldirilgan darslar yo\'q !')
else:
    for i in davomat:
        message +=  f''' 🆔 {i[0]}
        🕧 {i[1]}
        📅 {i[2]}
        📚 {i[3]}
        🔖 {i[4]}
        🤫 {i[5]}
        ⏲ {i[6]}
        👨‍🏫 {i[7]}\n '''
    message +='Qoldirilgan darslar: '+str(len(davomat))
    sendMessageBot(message)


