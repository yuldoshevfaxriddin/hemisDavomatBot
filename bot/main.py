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
    
def getProfilData(base_html):
    soup = bs4.BeautifulSoup(base_html,'lxml')
    header_data = soup.find('header',{'class':'main-header'}).find('nav').find('ul').find_all('li')
    profil_img = soup.find('header',{'class':'main-header'}).find('nav').find('ul').find('img',{'class':'user-image'})['src']
    username = soup.find('header',{'class':'main-header'}).find('nav').find('ul').find('span',{'class':'user-name'}).text
    guruh = soup.find('header',{'class':'main-header'}).find('nav').find('ul').find('span',{'class':'user-role'}).text
    respons = {
        'user_image':profil_img,
        'username': username,
        'guruh':guruh
    }
    return respons


def hemisLoginClient(user_id=None,user_ps=None ):
    if not (user_id is None or user_ps is None):
        session= r.Session()
        headers = {
            'User-Agent':'Chrome/51.0.2704.103 Safari/537.36 (Assalomu aleykum)'
        }
        respons_get = session.get( URL_LOGIN, headers = headers)
        html = respons_get.text
        with open('test.html','w',encoding='utf-8') as f :
            f.write(html)

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
        login_data['cookies'] = respons_post.cookies.get_dict()
        with open('cookies.json','w') as file:
           file.write(json.dumps(respons_post.cookies.get_dict()))

        # return login_data
        return session
    
def checkUserLogin(user_id,user_password,cookies_dict=None):
    # userni tekshiradi, login bo'lgan bo'lsa davomatni uzatadi,bolmasa login qilib davomatni uzatadi
    respons = r.get(URL_DAVOMAT,cookies=cookies_dict)
    # cookies fayl tasdiqlangan bo'lsa
    if len(respons.history)==0:
        print('login bo\'lgan user')
        text = getDavomatList(respons.text)
        profil = getProfilData(respons.text)
        returned_data = {
            'login':'succes',
            'data':text,
            'cookies':cookies_dict,
            'profil-data':profil
        }
        # print(returned_data)
        respons.close()
        return returned_data
    # cookies tasdiqlanmasa
    else:
        print('not login')
        new_client = hemisLoginClient(user_id=user_id,user_ps=user_password)
        returned = new_client.get(URL_DAVOMAT)
        if len(returned.history)>0:
            print('login error')
            returned_data = {
                'login':'login-error',
                'user-id':user_id,
                'password':user_password
            }
            with open('login-errors.txt','a') as f:
                f.write(f'{user_id}  {user_password}\n')
            with open(str(user_id)+'-login-error.html','w',encoding='utf-8') as file:
                file.write(returned.text)
            new_client.close()
            return returned_data
        else :
            text = getDavomatList(returned.text)
            profil = getProfilData(returned.text)
            print('login succes')
            returned_data = {
                'login':'succes',
                'cookies':returned.cookies.get_dict(),
                'profil-data':profil,
                'data':text
            }
            new_client.close()
            return returned_data
        

# user_id_test = '390201100297'
# user_ps_test = '390201100297d'

# user_id_test = '390201100299'
# user_ps_test = 'AB8310385'

# user_id_test = '390201100296'
# user_ps_test = 'AB390201100296'
# user_id_test = '390201100040'
# user_ps_test = 'AB81663288'
        
# user_id_test = '390201100067'
# user_ps_test = 'AB43218765'

# print(checkUserLogin(user_id_test,user_ps_test))

# client = hemisLoginClient(user_id = user_id_test,user_ps = user_ps_test)
# print(client)
# test = {"_frontendasdUser": "d589ssaee348dcb1cbdfaae24486c23040114a27b01dd93da24890ddd609bf34a%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22_frontendUser%22%3Bi%3A1%3Bs%3A46%3A%22%5B%2218%22%2C%22tG3FjTMA1yF6uNcm2Wx7O3KVRIU2ETxP%22%2C3600%5D%22%3B%7D", "frontend": "3rqhdlivbpap99rneh8l27cv13"}

# print(checkUserLogin(user_id_test,user_ps_test))


# t = client.get(URL_DAVOMAT)
# t = r.get(URL_DAVOMAT,cookies=local_cookies)
# print(t)
# davomat = getDavomatList(t.text)
# print(davomat)
# message = ''
# if davomat[0][0]=="Ma'lumotlar mavjud emas":
#     print('Sizda qoldirilgan darslar yo\q !')
#     sendMessageBot('Sizda qoldirilgan darslar yo\'q !')
# else:
#     for i in davomat:
#         message +=  f''' 🆔 {i[0]}
#         🕧 {i[1]}
#         📅 {i[2]}
#         📚 {i[3]}
#         🔖 {i[4]}
#         🤫 {i[5]}
#         ⏲ {i[6]}
#         👨‍🏫 {i[7]}\n '''
#     message +='Qoldirilgan darslar: '+str(len(davomat))
#     sendMessageBot(message)


