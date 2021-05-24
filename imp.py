import telebot
from telebot import types
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

name = ''
surname = ''
age = 0
owm = OWM('9309475ee560b818de0bbdf7ce7a6e1d')
mgr = owm.weather_manager()
UserCh = ''

bot = telebot.TeleBot("1814310452:AAGouE-8B9b4hx3plDNXKlTVUamtfXyBMXI")



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "У бота можно узнать погоду с помощью команды /pogoda")



@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == '/pogoda':
        keyboard = types.InlineKeyboardMarkup()
        key_Mos = types.InlineKeyboardButton(text='Москва', callback_data='Moscow')
        keyboard.add(key_Mos)
        key_Sar = types.InlineKeyboardButton(text='Саратов', callback_data='Saratov')
        keyboard.add(key_Sar)
        key_UserChoise = types.InlineKeyboardButton(text='Выбрать самому', callback_data='UserChoise')
        keyboard.add(key_UserChoise)
        bot.send_message(message.from_user.id, "В каком городе ты хочешь узнать погоду?", reply_markup=keyboard)

    else:
        bot.send_message(message.from_user.id, "У бота можно узнать погоду с помощью команды /pogoda")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "Moscow":
        observation = mgr.weather_at_place('Москва')
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        temp= round(temp)
        answ = 'В Москве сейчас ' + str(temp) + ' градусов по цельсию'
        bot.send_message(call.message.chat.id, answ)
        #bot.send_message(call.message.chat.id, "Приятно познакомиться! Теперь запишу в БД!")
    elif call.data == "Saratov":
        observation = mgr.weather_at_place('Саратов')
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        temp= round(temp)
        answ = 'В Саратове сейчас ' + str(temp) + ' градусов по цельсию'
        bot.send_message(call.message.chat.id, answ)
    elif call.data == "UserChoise":
         bot.send_message(call.message.chat.id, "Ну давай. Только пиши без ошибок")
         bot.register_next_step_handler(call.message, userChoise)


@bot.message_handler(func=lambda m: True)
def userChoise(message):
    try:
        global UserCh
        UserCh = message.text
        observation = mgr.weather_at_place(UserCh)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        temp= round(temp)
        bot.send_message(message.from_user.id, 'В городе ' + UserCh + ' сейчас ' + str(temp) + ' градусов по цельсию');
        bot.send_message(message.from_user.id, '/pogoda');
    except Exception:
        bot.send_message(message.from_user.id, 'Не понял, давай еще раз');
        bot.register_next_step_handler(message, userChoise)

bot.polling()