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
MESSAGE_FROM_MQTT = {}
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
        MESSAGE_FROM_MQTT = json.loads(msg.payload)

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

        time.sleep(0.2) # Pour gérer la vitesse de la boucle while      
#        print("Ca marche bien")
        
        move_forward_left=MESSAGE_FROM_MQTT.get("move_forward_left")
        move_backward_left=MESSAGE_FROM_MQTT.get("move_backward_left")
        move_forward_right=MESSAGE_FROM_MQTT.get("move_forward_right")
        move_backward_right=MESSAGE_FROM_MQTT.get("move_backward_right")
        arm_up=MESSAGE_FROM_MQTT.get("arm_up")
        arm_down=MESSAGE_FROM_MQTT.get("arm_down")
        clamp_open=MESSAGE_FROM_MQTT.get("clamp_open")
        clamp_close=MESSAGE_FROM_MQTT.get("clamp_close")
              
        robotkiller.pince.work(CLAMP_OPEN,CLAMP_CLOSE) 
        robotkiller.arm.work(ARM_UP,ARM_DOWN)
        robotkiller.left.running(MAX_SPEED, MIN_SPEED, MOVE_FORWARD_LEFT,MOVE_BACKWARD_LEFT)
        robotkiller.right.running(MAX_SPEED, MIN_SPEED, MOVE_FORWARD_RIGHT,MOVE_BACKWARD_RIGHT)

        # Et il faut que je fasse la communication vers MQTT avec JSON + dico comme dans game.py
        mesure_distance = robotkiller.eyes.measured(slow_distance)


    mosquitto.stop()
    print("C'est fini")
    
