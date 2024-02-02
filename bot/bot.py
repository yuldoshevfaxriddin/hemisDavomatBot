
import telebot
from telebot import types
import json

import dataBaseTest 
import main

TOKEN = "6931900857:AAHLe1o1sXFo3S0jryo1gs_Us9b4FI7mTDY"
bot = telebot.TeleBot(TOKEN)

def davomatGenerate(davomat_lst):
    message = ''
    for i in davomat_lst:
        message +=  f''' 🆔 {i[0]}
        🕧 {i[1]}
        📅 {i[2]}
        📚 {i[3]}
        🔖 {i[4]}
        🤫 {i[5]} (Sababli)
        ⏲ {i[6]}
        👨‍🏫 {i[7]}\n '''
    message +='Qoldirilgan darslar: '+str(len(davomat_lst))
    return message


@bot.message_handler(commands=['start'])
def start(message:types.Message):

    tg_user_id = message.from_user.id 
    # print(tg_user_id)
    check_user = dataBaseTest.selectUserId(tg_user_id)
    # print(check_user)

    if len(check_user) == 0:
        print('register')
        message_info = '''Tizimdan foydalanish uchun hemis login parolingizni kiriting ! Masalan: \n<b>login 390201100000 AB1234567 </b>'''
        bot.send_message(tg_user_id,message_info,parse_mode='html')
        
    else:
        print('login')
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
    bot.send_message(message.from_user.id,'Davomat yuklanmoqda')

    get_data = dataBaseTest.selectUserId(message.from_user.id)
    if len(get_data) != 0 :
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

@bot.message_handler(commands=['get-all-data'])
def send_all_data_statistik(message:types.Message):
    print('send data',message.text)
    if 'login' in message.text:
        bot.send_document(chat_id=message.from_user.id, document=open('login-errors.txt','r'))


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
        no = types.InlineKeyboardButton('Yo\'q',callback_data='no')
        keyboard.add(yes,no)
        bot.send_message(message.chat.id, f"<b>login : {login}\nparol : {password} </b>\nqabul qilinsinmi ?",reply_markup=keyboard,parse_mode='html')
    else :
        message_info = '''Tizimdan foydalanish uchun hemis login parolingizni kiriting ! Masalan: \n<b>login 390201100 AB1234567 </b>'''
        bot.send_message(message.chat.id,message_info,parse_mode='html')
    
  
@bot.callback_query_handler(func=lambda message: message.data.startswith('yes'))
def callback_data_yes(message:types.CallbackQuery):

    # bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    # print('delete yes')

    # davomatni uzat
    print('yes')
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
            
            # davomatni uzatish
            # print(hemis_data['data'])
            bot.send_message(tg_user_id, davomatGenerate(hemis_data['data']))

        else :
            #login qilishda xatolik
            bot.send_message(message.from_user.id,"Login tasdiqlanmadi !\nLogin parolingizni tekshirish ko\'ring")
    else:
        get_hemis_login = check[0][1]
        get_hemis_password = check[0][2]
        get_hemis_cookies = json.loads(check[0][5])
        davomat = main.checkUserLogin(get_hemis_login,get_hemis_password,get_hemis_cookies)
        if davomat['login']=='succes':
            dict_string = json.dumps(davomat['cookies'])
            # print(type(dict_string),dict_string)
            dataBaseTest.updateCookies(message.from_user.id,dict_string)
            # print(davomat)
            # davomatni uzatish
            bot.send_message(message.from_user.id,davomatGenerate(davomat['data']))
        else:
            bot.send_message(message.from_user.id,'Hemis tizimiga kirishda xatolik !\nLogin parolingizni tekshirib ko\'ring')
    

@bot.callback_query_handler(func=lambda message: message.data=='no')
def callback_data_no(message:types.CallbackQuery):
    # qaytadan kiritishni sora
    # bot.delete_message(chat_id=message.from_user.id, message_id=int(message.message.message.message_id))
    # print('delete no')

    print('no')
    bot.send_message(message.from_user.id,'Qaytadan kiriting')

@bot.callback_query_handler(func=lambda message: message.data.startswith('getDavomat'))
def callback_data_getDavomat(message:types.CallbackQuery):
    # davomatni uzat
    # bot.delete_message(chat_id=message.from_user.id, message_id=message.message)
    # print('delete davomat')

    print('davomat')
    get_data = dataBaseTest.selectUserId(message.from_user.id)
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


