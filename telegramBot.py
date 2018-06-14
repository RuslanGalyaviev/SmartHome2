import telebot
import requests
import json
from mqtt import *

tokken = "586569609:AAGkb_-IPu3qy9kZX9En2hJGHp-TUaCqqsI"

bot = telebot.TeleBot(tokken)


@bot.message_handler(commands=['start'])
def handle_start(messasge):
    mark_up = telebot.types.ReplyKeyboardMarkup()
    mark_up.row('Вкл','Выкл' ,'Темп')
    bot.send_message(messasge.from_user.id, "Привет", reply_markup=mark_up)

@bot.message_handler(content_types=['text'])
def send_message(message):
    if 'Вкл' in message.text:
        bot.send_message(message.chat.id, "Включено")
        publish_message_on()
    if 'Выкл' in message.text:
        bot.send_message(message.chat.id, "Выключено")
        publish_message_off()
    if 'Темп' in message.text:
        read_log_senMessage(message)




def read_log_senMessage(message):
    with open('dump.log', 'r') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        bot.send_message(message.chat.id, last_line)





bot.polling(none_stop = True, interval =0)






