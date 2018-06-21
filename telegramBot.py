import telebot
import json
from mqtt import *
import time
from temp import *
import config
import configparser

bot = telebot.TeleBot(config.tokken)

conf = configparser.RawConfigParser()
conf.read("termostat.conf")




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
        conf.set("termostat", "status", "on")
        conf.write(open("termostat.conf", "w"))
        bot.send_message(message.chat.id, "Термостат включен: включение при " + conf.get('termostat','on') + "°C выключение при " + conf.get('termostat', 'off') + "°C")

    if 'off' in message.text:
        bot.send_message(message.chat.id, "Термостат выключен")
        conf.set("termostat", "status", "off")
        conf.write(open("termostat.conf", "w"))
    if 'Настроить' in message.text:
        msg = bot.send_message(message.chat.id, 'Введите температру включения:')
        bot.register_next_step_handler(msg, onTemp)

def onTemp(message):
    while True:
        if not message.text.isdigit():
            msg = bot.send_message(message.chat.id, "Введите число")
            bot.register_next_step_handler(msg, onTemp)

        else:
            conf.set("termostat", "on", message.text)
            with open("termostat.conf", "w") as config:
                conf.write(config)
            print(message.text)
            msg = bot.send_message(message.chat.id, "Введите температуру выключения")
            bot.register_next_step_handler(msg, offTemp)
        break

def offTemp(message):
    while True:
        if not message.text.isdigit():
            msg = bot.send_message(message.chat.id, "Введите число")
            bot.register_next_step_handler(msg, offTemp)
        else:
            conf.set("termostat", "off", message.text)
            with open("termostat.conf", "w") as config:
                conf.write(config)
            print(message.text)
            bot.send_message(message.chat.id, "Термостат включен: включение при " + conf.get('termostat',
                                                                                             'on') + "°C выключение при " + conf.get(
                'termostat', 'off') + "°C")
        break


def read_log_senMessage(message):
    publish_message_status()
    time.sleep(1)
    last_line = json.load(open("dump.json"))
    last_line = last_line["StatusSNS"]["DS18B20"]["Temperature"]
    bot.send_message(message.chat.id,
                     "Сейчас температура в помещение: " + str(last_line) + "°C, " + "В Казани сейчас: " + temp())
    print(temp())





def get_updates():
    url = 'https://api.telegram.org/bot' + config.tokken + '/GetUpdates'
    r = requests.get(url)
    write_json(r.json())
    result = r.json()

    print(result)


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)



bot.polling(none_stop=True, interval=0)






























