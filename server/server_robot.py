#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
import time
import json
import paho.mqtt.client as mqtt
from plugins.helpers import print_exception 
from RkClassesHardware import Robotkiller

#############################################################################################
#                                                                                           #
#                                ROBOTKILLER THE ULTIMATE KILLER                            #
#                                                                                           #
#                                 Application serveur coté robot                            #
#                                                                                           #
#############################################################################################
#
#
#############################################################################################
#                                Initialisation des constantes                              #
#############################################################################################
mqtt_host = 'localhost'
mqtt_port = 1883
mqtt_subscribe = 'robot'

#############################################################################################
#                                Initialisation des variables                               #
#############################################################################################
# En majuscule les variables globales
MESSAGE_FROM_MQTT = {
    "move_forward_left": False,
    "move_backward_left": False,
    "move_forward_right": False,
    "move_backward_right": False,
    "arm_up": False,
    "clamp_open": False,
    "clamp_close": False,
    "min_speed": 50,
    "max_speed": 100,
    "working": False
}

MESSAGE_TO_MQTT = "Echec" # A definir pour renvoyer l'info de distance à l'IHM


#############################################################################################
#                                       Class                                               #
#############################################################################################

class Mosquitto(object):
    def __init__(self):
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        self.mqttc.on_message = self.on_message
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_unsubscribe = self.on_unsubscribe
        self.mqttc.connect(host=mqtt_host, port=mqtt_port)
        self.mqttc.subscribe(mqtt_subscribe, 1)

    def on_connect(self, mqttc, userdata, rc, t):
        print('connected...rc=' + str(rc))

    def on_disconnect(self, mqttc, userdata, rc):
        print('disconnected...rc=' + str(rc))

    def on_message(self, mqttc, userdata, msg):
        print('message received...')
        print('topic: ' + msg.topic + ', qos: ' + str(msg.qos) + ', message: ' + str(msg.payload))
        global MESSAGE_FROM_MQTT
#        MESSAGE_FROM_MQTT = json.loads(msg.payload) # Sous windows
        MESSAGE_FROM_MQTT = json.loads(msg.payload.decode('utf-8')) # Sous Raspberry Pi

    def on_subscribe(self, mqttc, userdata, mid, granted_qos):
        print('subscribed (qos=' + str(granted_qos) + ')')

    def on_unsubscribe(self, mqttc, userdata, mid, granted_qos):
        print('unsubscribed (qos=' + str(granted_qos) + ')')

    def start(self):
        self.mqttc.loop_start()

    def stop(self):
        self.mqttc.loop_start()

#############################################################################################
#                                       Main                                                #
#############################################################################################

if __name__ == '__main__':

    prog_game = True
    count_time = 0
    game_time = 60

    robotkiller = Robotkiller()
    mosquitto = Mosquitto()
    mosquitto.start()
 
    print("Lancement boucle robot")
    while prog_game :
        # Pour les tests je garde la temporisation
        # Mais je dois remplacer cela par un arret depuis le bouton poussoir du robot
        # en possition tous les items à Flase 
        # en gros => c'est l'arret d'urgence
   
        count_time = count_time + 0.2
        if count_time > game_time :
            prog_game = False

        measure_distance = 9999999

        time.sleep(0.2) # Pour gérer la vitesse de la boucle while      
#        print("Ca marche bien")

        # print("traitement")
        # print('move_forward_left' + str(MESSAGE_FROM_MQTT.get("move_forward_left")))
        # print('move_forward_left' + str(MESSAGE_FROM_MQTT.get("move_backward_left")))
        # print('move_forward_left' + str(MESSAGE_FROM_MQTT.get("move_forward_right")))
        # print('move_forward_left' + str(MESSAGE_FROM_MQTT.get("move_backward_right")))
        # print('move_forward_left' + str(MESSAGE_FROM_MQTT.get("arm_up")))
        # print('move_forward_left' + str(MESSAGE_FROM_MQTT.get("arm_down")))

        is_playing = MESSAGE_FROM_MQTT.get("working", False)
        max_speed = MESSAGE_FROM_MQTT.get("max_speed", 200)
        min_speed = MESSAGE_FROM_MQTT.get("min_speed", 50)
        distance = MESSAGE_FROM_MQTT.get("distance", 10)

        while (is_playing):
            is_playing = MESSAGE_FROM_MQTT.get("working", False)
            move_forward_left = MESSAGE_FROM_MQTT.get("move_forward_left", False)
            move_backward_left = MESSAGE_FROM_MQTT.get("move_backward_left", False)
            move_forward_right = MESSAGE_FROM_MQTT.get("move_forward_right", False)
            move_backward_right = MESSAGE_FROM_MQTT.get("move_backward_right", False)
            arm_up = MESSAGE_FROM_MQTT.get("arm_up", False)
            arm_down = MESSAGE_FROM_MQTT.get("arm_down", False)

            clamp_open = MESSAGE_FROM_MQTT.get("clamp_open", False)
            clamp_close = MESSAGE_FROM_MQTT.get("clamp_close", False)

    #        robotkiller.pince.work(clamp_open,clamp_close)

            robotkiller.arm.work(arm_up,arm_down)
            robotkiller.left.running(max_speed, min_speed, move_forward_left, move_backward_left, False)
            robotkiller.right.running(max_speed, min_speed, move_forward_right, move_backward_right, False)

            # Et il faut que je fasse la communication vers MQTT avec JSON + dico comme dans game.py
            # Voila
            distance_to_collision = int(robotkiller.eyes.measured(distance))
            if not measure_distance == distance_to_collision:
                measure_distance = distance_to_collision
                mosquitto.mqttc.publish('robot', json.dumps({'collision': measure_distance}))
            # mesure_distance = robotkiller.eyes.measured(slow_distance)



    mosquitto.stop()
    print("C'est fini")
    
