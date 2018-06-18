import telebot
import requests
import json
from mqtt import *
import time
from temp import *
tokken = "586569609:AAGkb_-IPu3qy9kZX9En2hJGHp-TUaCqqsI"

bot = telebot.TeleBot(tokken)



@bot.message_handler(commands=['/start'])
def handle_start(messasge):
    mark_up = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark_up.row('Вкл','Выкл' ,'Темп')
    bot.send_message(messasge.chat.id, "Привет", reply_markup=mark_up)


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
    publish_message_status()
    time.sleep(1)
    last_line = json.load(open("dump.json"))
    last_line = last_line["StatusSNS"]["DS18B20"]["Temperature"]
    bot.send_message(message.chat.id, "Сейчас температура в помещение: " + str(last_line) + "°C, " + "В Казани сейчас: " + temp())
    print(temp())




bot.polling(none_stop = True, interval =0)








def get_updates():
    url ='https://api.telegram.org/bot' + tokken + '/GetUpdates'
    r = requests.get(url)
    write_json(r.json())
    # result = r.json()['result'][-1]['message']['from']['username']
    result = r.json()

    print(result)

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)