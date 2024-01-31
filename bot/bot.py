


TOKEN = "5695969116:AAHVXa83GZ_T9ebUXgH3Uy7vXkIe1jmfxu0"


import telebot
from telebot import types
    
bot = telebot.TeleBot(TOKEN)
    
@bot.message_handler(commands=['start'])
def start(message:types.Message):

    tg_user_id = message.from_user.id 
    sql_query = f''
    tg_user_first_name = message.from_user.first_name
    tg_user_last_name = message.from_user.first_name
    tg_user_username = message.from_user.username

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Bottom 1")
    item2 = types.KeyboardButton("Bottom 2")
    markup.add(item1, item2)
    
    bot.send_message(message.chat.id, "Select option:", reply_markup=markup)
    
    #Bottom 1
@bot.message_handler(func=lambda message: message.text == "Bottom 1")
def button1(message):
    button_foo = types.InlineKeyboardButton('Foo', callback_data='foo')
    button_bar = types.InlineKeyboardButton('Bar', callback_data='bar')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_foo)
    keyboard.add(button_bar)
    bot.send_message(message.chat.id, "U select bottom 1",reply_markup=keyboard)
    
    #Bottom 2
@bot.message_handler(func=lambda message: message.text == "Bottom 2")
def button2(message):
    bot.send_message(message.chat.id, "U select bottom 2")
    

@bot.callback_query_handler(func=lambda message: True)
def test(message):
    print(message.from_user)
    bot.send_message(1742197944,message)

    #Start bot
if __name__ == '__main__':
    bot.polling(none_stop=True)