import telebot
import requests
import json
from mqtt import *
import time
from temp import *

tokken = "586569609:AAGkb_-IPu3qy9kZX9En2hJGHp-TUaCqqsI"

bot = telebot.TeleBot(tokken)


@bot.message_handler(commands=['start'])
def handle_start(message):
    mark_up = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark_up.row('Вкл', 'Выкл', 'Темп')
    mark_up.row('Термостат on', 'Термостат off')
    mark_up.row('Настроить термостат')
    bot.send_message(message.chat.id, "Привет", reply_markup=mark_up)


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
    if 'on' in message.text:
        bot.send_message(message.chat.id, "Термостат включен")
    if 'off' in message.text:
        bot.send_message(message.chat.id, "Термостат выключен")
    if 'Настроить' in message.text:
        setting_termostat(message)


def read_log_senMessage(message):
    publish_message_status()
    time.sleep(1)
    last_line = json.load(open("dump.json"))
    last_line = last_line["StatusSNS"]["DS18B20"]["Temperature"]
    bot.send_message(message.chat.id,
                     "Сейчас температура в помещение: " + str(last_line) + "°C, " + "В Казани сейчас: " + temp())
    print(temp())


def setting_termostat(message):
    bot.send_message(message.chat.id, "Введите температуру включения: ")
    get_updates()




def get_updates():
    url = 'https://api.telegram.org/bot' + tokken + '/GetUpdates'
    r = requests.get(url)
    write_json(r.json())
    result = r.json()

    print(result)


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



bot.polling(none_stop=True, interval=0)






























