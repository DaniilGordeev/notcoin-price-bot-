import telebot
from telebot import types
from config import token, admin
import function as f
import time
import schedule
import threading

bot = telebot.TeleBot(token)

@bot.message_handler(regexp='start')
def start(message):
    user_id = message.from_user.id 
    text= f'Привет\n'\
            f"🟡Notcoin = {f.get_price()}"
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    bot.send_message(user_id, text, reply_markup=markup.add(types.KeyboardButton('Установить лимит')))

@bot.message_handler(regexp='Установить лимит')
def set_regular(message):
    f.price_limit.clear()
    user_id = message.from_user.id
    text = f'⬆️Введите верхний предел'
    msg = bot.send_message(user_id, text)
    bot.register_next_step_handler(msg, enter_top_limit)

def enter_top_limit(message):
    user_id = message.from_user.id
    f.price_limit.append(float(message.text))
    text = '⬇️Введите нижний лимит'
    msg = bot.send_message(user_id, text)
    bot.register_next_step_handler(msg, enter_bottom_limit)

def enter_bottom_limit(message):
    user_id = message.from_user.id
    f.price_limit.append(float(message.text))
    text = f'Ваш лимит: \n'\
            f'⬆️Верхний: {f.price_limit[0]}\n'\
            f'⬇️Нижний: {f.price_limit[1]}'
    bot.send_message(user_id, text)
    


def send_notification():
    if f.notification_price(f.price_limit[0], f.price_limit[1]) == 'top_limit':
        text = '⬆️ Был привышен поставленный верхний лимит'
        bot.send_message(admin[0], text)
    if f.notification_price(f.price_limit[0], f.price_limit[1]) == 'bottom_limit':
        text = '⬇️Был привышен поставленный нижний лимит'
        bot.send_message(admin[0], text)

schedule.every().hour.at(':30').do(send_notification)
schedule.every().hour.at(':00').do(send_notification)

def send_price():
    f.price.append(float(f.get_price()))
    del f.price[0]
    text = f"🟡Notcoin = {f.get_price()}\n"\
            f'Цена изменилась на {f.compute_change_price(f.price[0], f.price[1])}'
    bot.send_message(admin[0], text)

schedule.every().hour.at(':00').do(send_price)

def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
    
scheduler_thread = threading.Thread(target=scheduler).start()

bot.polling(non_stop=True, interval=0)