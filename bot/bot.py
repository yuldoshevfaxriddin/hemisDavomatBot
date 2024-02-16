
import telebot
from telebot import types
import json
import requests 

import dataBaseTest 
import main

#TOKEN = ''
TOKEN = '6931900857:AAHLe1o1sXFo3S0jryo1gs_Us9b4FI7mTDY'

bot = telebot.TeleBot(TOKEN)

HELP_MESSAGE = """ 
/start - Botni ishga tushirish
/davomat - Davomatni olish
/profil - Profil ma'lumotlarini ko'rish
/delete - Profil ma'lumotlarini botdan o'chirib tashlash
/help - Botdan foydalanish haqida qo'llanma
Xato, kamchiliklar, takliflar bo'yicha quyidagi accauntga murojat qilishingiz mumkin! @Faxriddin_yuldoshev 
"""

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
        "User-Agent": "Telegram Bot Yuldoshev Faxriddin (https://github.com/yuldoshevfaxriddin/)",
        "content-type": "application/json"
    }
    try:
        response = requests.post(URL_SEND_MESSAGE, json=payload, headers=headers)

        print(response.text)
    except:
        print("Internetga ulanmagan o'xshidi ov ...")


def davomatGenerate(davomat_lst):
    message = ''
    for i in davomat_lst:
        message +=  f''' 🆔 {i[0]}
        🕧 {i[1]}
        📅 {i[2]}
        📚 {i[3]}
        🔖 {i[4]}
        🤫 (Sabablimi ?) {i[5]} 
        ⏲ {i[6]} soat
        👨‍🏫 {i[7]}\n '''
    message +='Qoldirilgan darslar : '+str(len(davomat_lst))+' ta nb'
    return message

@bot.message_handler(commands=['start'])
def start(message:types.Message):

    tg_user_id = message.from_user.id 
    # print(tg_user_id)
    check_user = dataBaseTest.selectUserId(tg_user_id)
    # print(check_user)

    if len(check_user) == 0:
        with open('tg-user-id.txt','a') as users:
            users.write(f'{tg_user_id} {message.from_user.first_name} {message.from_user.username}\n')
        print('start command register')
        message_info = '''Tizimdan foydalanish uchun hemis login parolingizni kiriting ! Masalan: \n<b>login 390201100000 AB1234567 </b>'''
        bot.send_message(tg_user_id,message_info,parse_mode='html')
        
    else:
        print('start command login')
        # print(check_user)
        hemis_username = ''
        for i in check_user:
            hemis_username += (i[3] +'\n')
        hemis_login = check_user[0][1]
        hemis_password = check_user[0][2]
        send_data = hemis_login+'-'+hemis_password#+'-'+message.message_id
        keyboard = types.InlineKeyboardMarkup()
        davomat = types.InlineKeyboardButton('Davomatni olish',callback_data='getDavomat-'+send_data)
        keyboard.add(davomat)
        bot.send_message(tg_user_id,'Tizimdan ro\'yhatdan o\'tgansiz ! Profilingiz :\n<b>'+hemis_username+'</b>',parse_mode='html',reply_markup=keyboard)

@bot.message_handler(commands=['davomat'])
def get_davomat(message:types.Message):
    print('get davomat')

    get_data = dataBaseTest.selectUserId(message.from_user.id)
    if len(get_data) != 0 :
        bot.send_message(message.from_user.id,'Davomat yuklanmoqda')
        get_hemis_login = get_data[0][1]
        get_hemis_password = get_data[0][2]
        get_hemis_cookies = json.loads(get_data[0][5])

        davomat = main.checkUserLogin(get_hemis_login,get_hemis_password,get_hemis_cookies)
        if davomat['login']=='succes':
            # print(davomat)
            dataBaseTest.updateCookies(message.from_user.id,json.dumps(davomat['cookies']))
            # davomatni uzatish
            bot.send_message(message.from_user.id,davomatGenerate(davomat['data']))
        else:
            bot.send_message(message.from_user.id,'Login parol xato !')
    else:
        bot.send_message(message.from_user.id,'Botdan ro\'yxatdan o\'tmagansiz !')
    # edit_text = 'malom '
    # bot.edit_message_text(chat_id=message.from_user.id,message_id=message.id,text=edit_text)

@bot.message_handler(commands=['profil'])
def send_hemis_profil(message:types.Message):
    user_info = dataBaseTest.selectUserId(message.from_user.id)
    if len(user_info) == 0:
        bot.send_message(message.from_user.id,'Botdan ro\'yxatdan o\'tmagansiz !')
    else:
        bot.send_message(message.from_user.id,'Profilingiz : '+user_info[0][3])

@bot.message_handler(func=lambda message: message.text.startswith('/edit'))
def edit_hemis_profil(message:types.Message):
    user_info = dataBaseTest.selectUserId(message.from_user.id)
    if len(user_info) == 0:
        bot.send_message(message.from_user.id,'Botdan ro\'yxatdan o\'tmagansiz !')
    else:
        user_data = message.text.split()
        print(user_data)
        if len(user_data)>2:
            login = user_data[1]
            password = user_data[2]
            # print(data)
            if not login.startswith('390'):
                bot.send_message(message.chat.id, f"<b>login : {login}\nparol : {password} </b>\nmenimcha noto\'g\'ri ma\'lumot kiritdingiz, qayta kiriting !",parse_mode='html')
                return
            
            bot.delete_message(chat_id=message.from_user.id, message_id=message.id)
            send_data = login+'-'+password
            keyboard = types.InlineKeyboardMarkup()
            yes = types.InlineKeyboardButton('Ha',callback_data='update-'+send_data)
            no = types.InlineKeyboardButton('Yo\'q',callback_data='no-1')
            keyboard.add(yes,no)
            bot.send_message(message.chat.id, f"<b>login : {login}\nparol : {password} </b>\nqabul qilinsinmi ?",reply_markup=keyboard,parse_mode='html')
        else :
            bot.send_message(message.chat.id,"Hemis login parolingizni o'zgartirish uchun quyidagi tartibda jo'nating.\n<b>/edit yangi_login yangi_parol</b>\nMasalan :\n<b>/edit 390201100000 AB1234567 </b>",parse_mode='html')

@bot.message_handler(commands=['get-all-data'])
def send_all_data_statistik(message:types.Message):
    # print('send data',message.text)
    print('get-data')
    if 'login' in message.text:
        with open('users.txt','w') as users_txt:
            users_txt.write(str(dataBaseTest.selectAllData()))
        bot.send_document(chat_id=message.from_user.id, document=open('login-errors.txt','r'))
        bot.send_document(chat_id=message.from_user.id, document=open('tg-user-id.txt','r'))
        bot.send_document(chat_id=message.from_user.id, document=open('users.txt','r'))
        bot.send_document(chat_id=message.from_user.id, document=open('delete-users.txt','r'))
        bot.send_message('1742197944', message.from_user)

@bot.message_handler(commands=['delete'])
def delete_user(message:types.Message):

    user_info = dataBaseTest.selectUserId(message.from_user.id)
    if len(user_info) == 0:
        bot.send_message(message.from_user.id,'Botdan ro\'yxatdan o\'tmagansiz !')
    else:
        keyboard = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton('Ha',callback_data='deleteYes')
        no = types.InlineKeyboardButton('Yo\'q',callback_data='no-2')
        keyboard.add(yes,no)
        bot.send_message(message.from_user.id,'Profilingiz : <b>'+user_info[0][3]+'</b>\nProfilingizni o\'chirasizmi ?',reply_markup=keyboard,parse_mode='html')


@bot.message_handler(commands=['help'])
def help_comman(message:types.Message):
    print('help')
   
    bot.send_message(message.from_user.id,HELP_MESSAGE)


@bot.message_handler(commands=['send-message'])
def bot_send_messages(message:types.Message):
    print('send message')    
    message_text = message.text[14:]
    with open('tg-user-id.txt','r') as file:
        all_info = file.read()
        info = all_info.split('\n')

    users_list = []
    users_db = dataBaseTest.selectAllData()
    for i in info:
        if len(i) != 0:
            users_list.append(i.split()[0])
    for i in users_db:
        users_list.append(i[6])
    new_users_list = set(users_list)
    # barcha foydalanuvchilarga habar yuborish

    for user_id in new_users_list:
        # print(type(i),i)
        sendMessageBot(message_text,user_id)
    print(len(info)-1,' ta habar jo\'natildi')
    # print(new_users_list)
    # print(new_users_list[1])
    # print(type(new_users_list[1]))
    # bot.send_message('1742197944', str(message.from_user.id) + message_text)
    # bot.send_message(new_users_list[1],message_text)

@bot.message_handler(func=lambda message: True )
def login_message(message:types.Message):    
    data = message.text.split() 
    # bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    # print('delete true')

    # print(data)
    if len(data) > 2:
        login = data[1]
        password = data[2]
        # print(data)
        if not login.startswith('390'):
            bot.send_message(message.chat.id, f"<b>login : {login}\nparol : {password} </b>\nmenimcha noto\'g\'ri ma\'lumot kiritdingiz, qayta kiriting !",parse_mode='html')
            return 
        send_data = login+'-'+password
        keyboard = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton('Ha',callback_data='yes-'+send_data)
        no = types.InlineKeyboardButton('Yo\'q',callback_data='no-0')
        keyboard.add(yes,no)
        bot.send_message(message.chat.id, f"<b>login : {login}\nparol : {password} </b>\nqabul qilinsinmi ?",reply_markup=keyboard,parse_mode='html')
    else :
        message_info = '''Tizimdan foydalanish uchun hemis login parolingizni kiriting ! Masalan: \n<b>login 390201100 AB1234567 </b>'''
        bot.send_message(message.chat.id,message_info,parse_mode='html')

@bot.callback_query_handler(func=lambda message: message.data.startswith('update'))
def callback_data_update(message:types.CallbackQuery):

    bot.delete_message(chat_id=message.from_user.id, message_id=message.message.id)
    print('update yes')
    data = message.data.split('-')
    hemis_login = data[1]
    hemis_password = data[2]
    check = dataBaseTest.updateUserData(tg_user_id=message.from_user.id,hemis_user_id=hemis_login,hemis_user_password=hemis_password)
    bot.send_message(message.from_user.id,'Ma\'lumotlaringiz yangilandi !')

@bot.callback_query_handler(func=lambda message: message.data.startswith('yes'))
def callback_data_yes(message:types.CallbackQuery):

    bot.delete_message(chat_id=message.from_user.id, message_id=message.message.id)
    print('delete yes')
    bot.send_message(message.from_user.id, 'Davomat yuklanmoqda')
    # davomatni uzat
    data = message.data.split('-')

    hemis_login = data[1]
    hemis_password = data[2]
    check = dataBaseTest.selectUserId(tg_user_id=message.from_user.id)
    if len(check)==0:
        hemis_data = main.checkUserLogin(user_id=hemis_login,user_password=hemis_password)
        if hemis_data['login'] == 'succes':
            tg_user_id  = message.from_user.id
            tg_user_first_name = message.from_user.first_name
            tg_user_last_name = message.from_user.first_name
            tg_user_username = message.from_user.username
            # print(hemis_data)
            hemis_profil = hemis_data['profil-data']['username'] #+'  '+hemis_data['profil-data']['guruh']
            hemis_img = hemis_data['profil-data']['user_image']
            hemis_cookies = json.dumps(hemis_data['cookies'])
            # print(hemis_cookies)

            dataBaseTest.insertData(hemis_user_id=hemis_login,hemis_user_password=hemis_password,hemis_profil=hemis_profil,
                                    hemis_img=hemis_img,tg_user_id=tg_user_id,tg_username=tg_user_username,tg_first_name=tg_user_first_name,
                                    tg_last_name=tg_user_last_name,hemis_cookies_dict=hemis_cookies)
            print('data insertion succes')
            # davomatni uzatish
            # print(hemis_data['data'])
            bot.send_message(tg_user_id, davomatGenerate(hemis_data['data']))

        else :
            #login qilishda xatolik
            print('Registration login error')
            bot.send_message(message.from_user.id,"Login tasdiqlanmadi !\nLogin parolingizni tekshirib ko\'ring")
    else:
        get_hemis_login = check[0][1]
        get_hemis_password = check[0][2]
        get_hemis_cookies = json.loads(check[0][5])
        davomat = main.checkUserLogin(get_hemis_login,get_hemis_password,get_hemis_cookies)
        if davomat['login']=='succes':
            print('cache login succes')
            dict_string = json.dumps(davomat['cookies'])
            # print(type(dict_string),dict_string)
            dataBaseTest.updateCookies(message.from_user.id,dict_string)
            # print(davomat)
            # davomatni uzatish
            bot.send_message(message.from_user.id,davomatGenerate(davomat['data']))
        else:
            bot.send_message(message.from_user.id,'Hemis tizimiga kirishda xatolik !\nLogin parolingizni tekshirib ko\'ring')
    
@bot.callback_query_handler(func=lambda message: message.data.startswith('deleteYes'))
def delete_user(message:types.Message):
    print('Delete user')
    user_info = dataBaseTest.selectUserId(message.from_user.id)
    with open('delete-users.txt','a') as file:
        file.write(str(user_info)+'\n')
    dataBaseTest.deleteUser(message.from_user.id)
    bot.send_message(message.from_user.id,user_info[0][3]+' ma\'lumotlari o\'chirildi.')

@bot.callback_query_handler(func=lambda message: message.data.startswith('no'))
def callback_data_no(message:types.CallbackQuery):
    data = message.data.split('-')
    print(data)
    # qaytadan kiritishni sora
    bot.delete_message(chat_id=message.from_user.id, message_id=message.message.id)
    print('delete no')
    if data[1]=='0':
        bot.send_message(message.from_user.id,'Qaytadan kiriting')

@bot.callback_query_handler(func=lambda message: message.data.startswith('getDavomat'))
def callback_data_getDavomat(message:types.CallbackQuery):
    # davomatni uzat
    bot.delete_message(chat_id=message.from_user.id, message_id=message.message.id)
    # print('delete davomat')

    print('davomat')
    get_data = dataBaseTest.selectUserId(message.from_user.id)
    # print(get_data)
    if len(get_data) == 0:
        bot.send_message(message.from_user.id,'Botdan ro\'yxatdan o\'tmagansiz !')
        return 
    bot.send_message(message.from_user.id, 'Davomat yuklanmoqda')
    get_hemis_login = get_data[0][1]
    get_hemis_password = get_data[0][2]
    get_hemis_cookies = json.loads(get_data[0][5])

    davomat = main.checkUserLogin(get_hemis_login,get_hemis_password,get_hemis_cookies)
    if davomat['login']=='succes':
        # print(davomat)
        dataBaseTest.updateCookies(message.from_user.id,json.dumps(davomat['cookies']))
        # davomatni uzatish
        bot.send_message(message.from_user.id,davomatGenerate(davomat['data']))
    else:
        bot.send_message(message.from_user.id,'Qaytadan kiriting, Login bilan muammo !')

    #Start bot

if __name__ == '__main__':
    bot.polling(none_stop=True)
    # while True:
    #     try:
    #         print('bot ishga tushdi')
    #         bot.polling(none_stop=True)
    #     except :
    #         print('tugadi xatolik aniqlandi')
    #         sendMessageBot('@hemis_davomat_bot Botda exseption paydo bo\'ldi. Bot o\'chdi.')
    #     finally:
    #         print('tugadi xatolik')


