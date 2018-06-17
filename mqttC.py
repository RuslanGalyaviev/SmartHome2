import paho.mqtt.client as mqtt
import json
from collections import namedtuple


def on_connect(client, userdata, flags, rc):
    print('Статус кода :'+str(rc))
    # client.subscribe('stat/sonoff/RESULT/#')
    client.subscribe('stat/sonoff/STATUS10/#')

def on_message(cliend, userdata, msg):
    print(msg.payload)
    x = json.loads(msg.payload)
    # print(type(x))
    # print(x['Time'])
    write_log(x)
    # x = json.loads(msg.payload, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    # temp = x.Time
    # write_log(temp)

def write_log(data):
    log = data
    with open("dump.json", "w") as f:
        # print(log, file=f)
        json.dump(log, f, indent=2, ensure_ascii=False)




def conect_broker():
  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message

  client.connect('m12.cloudmqtt.com', 10820, 60)
  client.username_pw_set('mlawbgod', 'xaGpbI5L7gQX')
  client.loop_forever()



if __name__ == '__main__':
    conect_broker()


