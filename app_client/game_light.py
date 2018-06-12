#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
import os 
import time
import json
import paho.mqtt.client as mqtt
import pygame
from pygame.locals import *


#############################################################################################
#                                Initialisation des constantes                              #
#############################################################################################
mqtt_host = '192.168.0.151'
mqtt_port = 1883
mqtt_subscribe = 'robot'

INIT_ROBOT_STATUS = {
    "move_forward_left": False,
    "move_backward_left": False,
    "move_forward_right": False,
    "move_backward_right": False,
    "arm_up": True,
    "arm_down": False,
    "clamp_open": True,
    "clamp_close": False,
    "min_speed": 50,
    "max_speed": 200,
    "working": False
}

MESSAGE_TO_MQTT = INIT_ROBOT_STATUS.copy()

MESSAGE_FROM_MQTT = {}



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
#        message = json.loads(msg.payload) # Sous windows
        message = json.loads(msg.payload.decode('utf-8')) # Sous Raspberry Pi
        MESSAGE_FROM_MQTT.update(message)

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

    game_time = 120         # durée du jeu en seconde

    prog_main = True        # Variable pour la gestion de la boucle principale (PB)
    prog_game = True        # Variable pour la gestion de la boucle principale (jeux)


    mosquitto = Mosquitto()
    mosquitto.start()

    
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS']="0,568"  
    screen = pygame.display.set_mode((1366, 200))  
    pygame.display.set_caption('RobotKiller')
    fond = pygame.image.load("background.jpg").convert()
    screen.blit(fond, (0,0))
    pygame.display.flip()

    chaine="ma chaine sur une seule ligne"
    font=pygame.font.SysFont("broadway",24,bold=False,italic=False)
    text=font.render(chaine,1,(1,1,1))
    screen.blit(text,(30,30))
    pygame.display.flip() 


    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    #print("Number of joysticks: {}".format(joystick_count) )
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    # is_playing = MESSAGE_FROM_MQTT.get("working", False)
    # max_speed = MESSAGE_FROM_MQTT.get("max_speed", 200)
    # min_speed = MESSAGE_FROM_MQTT.get("min_speed", 50)
    # distance = MESSAGE_FROM_MQTT.get("distance", 10)

    change_message = False

    while prog_main:
 #       continuer = int(input())
        events = pygame.event.get() #  retourne une liste d'events dans une table
        # pygame.event.pump() # Un truc qui sert à rien : permettre à la mémoire tampon d'événements de circuler facilement et d'éviter les mauvais comportements subtils entre différents systèmes
        for event in events : # on dépile la table evenement par évenement

            time.sleep(0.05)
  
            if event.type == QUIT :
                print("Sortie du programme")
                prog_game = False
                prog_main = False
 
            # if event.type == pygame.JOYBUTTONDOWN:
            #     print("Joystick button pressed.")
            #     print(event.button)
            # if event.type == pygame.JOYBUTTONUP:
            #     print("Joystick button released.")
            #     print(event.button)

            if event.type == pygame.JOYBUTTONDOWN and event.button == 4:
                # Chemille gauche - Marche avant
                MESSAGE_TO_MQTT["move_forward_left"] = True
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 4:
                # Chemille gauche - Marche avant - Rallentir
                MESSAGE_TO_MQTT["move_forward_left"] = False
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 6:
                #Chemille gauche - Marche arrière
                MESSAGE_TO_MQTT["move_backward_left"] = True
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 6:
                # Chemille gauche - Marche arrière - Rallentir
                MESSAGE_TO_MQTT["move_backward_left"] = False
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 5:
                # Chemille droite - Marche avant
                MESSAGE_TO_MQTT["move_forward_right"] = True
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 5:
                # Chemille droite - Marche avant - Rallentir
                MESSAGE_TO_MQTT["move_forward_right"] = False
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 7:
                #Chemille droite - Marche arrière
                MESSAGE_TO_MQTT["move_backward_right"] = True
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 7:
                # Chemille droite - Rallentir
                MESSAGE_TO_MQTT["move_backward_right"] = False
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                #Bras - UP
                MESSAGE_TO_MQTT["arm_up"] = True
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 2:
                #Bras - Down
                MESSAGE_TO_MQTT["arm_down"] = True
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 0 :
                #Bras - UP - Stop
                MESSAGE_TO_MQTT["arm_up"] = False
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 2 :
                #Bras - Down - Stop
                MESSAGE_TO_MQTT["arm_down"] = False
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
                #Pince - Close
                MESSAGE_TO_MQTT["clamp_close"] = True 
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 3:
                #Pince - Open 
                MESSAGE_TO_MQTT["clamp_open"] = True
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 1 :
                #Pince - Close
                MESSAGE_TO_MQTT["clamp_close"] = False
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 3 :
                #Pince - Open 
                MESSAGE_TO_MQTT["clamp_open"] = False
                change_message = True

        if change_message == True :
            mosquitto.mqttc.publish(mqtt_subscribe, json.dumps(MESSAGE_TO_MQTT), 1)
            change_message = False

#        mosquitto.mqttc.publish(mqtt_subscribe, json.dumps(INIT_ROBOT_STATUS), 1)


    # Sortie propre du programme
    pygame.quit
    pygame.quit()
    print("Arret system")
