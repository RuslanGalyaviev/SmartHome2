import configparser
from mqtt import *
import time
import json

def termostat():
    publish_message_status()
    time.sleep(1)
    last_line = json.load(open("dump.json"))
    last_line = last_line["StatusSNS"]["DS18B20"]["Temperature"]
    print("Прошло 60 сек")
    conf = configparser.RawConfigParser()
    conf.read("termostat.conf")
    conf.set("termostat", "tempinroom", last_line)
    with open("termostat.conf", "w") as config:
        conf.write(config)
    if conf.get('termostat', 'status') == 'on':
        if conf.getfloat('termostat', 'tempinroom') <= conf.getfloat('termostat', 'on'):
            publish_message_on()
            print('Включено')
        if conf.getfloat('termostat', 'tempinroom') >= conf.getfloat('termostat', 'off'):
            publish_message_off()
            print('Выключено')

while True:
    termostat()
    time.sleep(60)