from paho.mqtt import publish






def publish_message_on():
    msgs = [{'topic': "cmnd/sonoff/power", 'payload': "on"}]

    publish.multiple(msgs, hostname='m12.cloudmqtt.com', port=10820, keepalive=60, auth={'username':"mlawbgod", 'password':"xaGpbI5L7gQX"})

def publish_message_off():
    msgs = [{'topic': "cmnd/sonoff/power", 'payload': "off"}]

    publish.multiple(msgs, hostname='m12.cloudmqtt.com', port=10820, keepalive=60, auth={'username': "mlawbgod", 'password': "xaGpbI5L7gQX"})


