import paho.mqtt.client as mqtt


def on_connect(mqttc, userdata, rc, t):
    print('connected...rc=' + str(rc))


def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))


def on_message(mqttc, userdata, msg):
    print('message received...')
    print('topic: ' + msg.topic + ', qos: ' +
          str(msg.qos) + ', message: ' + str(msg.payload))


def on_subscribe(mqttc, userdata, mid, granted_qos):
    print('subscribed (qos=' + str(granted_qos) + ')')


def on_unsubscribe(mqttc, userdata, mid, granted_qos):
    print('unsubscribed (qos=' + str(granted_qos) + ')')


mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
mqttc.connect(host='localhost', port=1883)
mqttc.subscribe('robot', 1)
mqttc.loop_forever()
