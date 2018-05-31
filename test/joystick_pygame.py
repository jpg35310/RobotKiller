# /usr/bin/env python
from __future__ import absolute_import, division
import time
import os
import sys
import subprocess

import pygame
from pygame.locals import *
from RkClassesHardware import Robotkiller 

# Initiallisation de la librairie PYGAME qui oblige à lancer un affichage
pygame.init() # initialisation de la librairie pour la gestion du graphique
screen = pygame.display.set_mode((640, 480)) # pas le choix, obliger de lancer un affichage 
pygame.display.set_caption('RobotKiller')
# pygame.key.set_repeat(60, 60) # premet de renvoyer l'info KEYDOWN / KEYUP
# pygame.key.set_repeat(400, 30)

#############################################################################################
########################## Initialisation des variables######################################
#############################################################################################
game_time = 120         # durée du jeu en seconde

prog_main = True        # Variable pour la gestion de la boucle principale (PB)
prog_game = True        # Variable pour la gestion de la boucle principale (jeux)

input_state_bp = False

#speed_caterpillar = 200
slow_distance = 10

caterpillar_speed = 200
caterpillar_left_go = False
caterpillar_right_go = False
caterpillar_left_way = True
caterpillar_right_way = True
caterpillar_left_stop = True
caterpillar_right_stop = True

arm_move_up = False
arm_move_down = False

pince_open = False
pince_close = False

#############################################################################################
########################## Les objets du programme ##########################################
#############################################################################################

#############################################################################################
########################## PROGRAMME PRINCIPAL ##############################################
#############################################################################################


robotkiller = Robotkiller()
time.sleep(1)

pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# Get count of joysticks
joystick_count = pygame.joystick.get_count()
#print("Number of joysticks: {}".format(joystick_count) )

for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

#     print("Joystick {}".format(i) )

#     # Get the name from the OS for the controller/joystick
#     name = joystick.get_name()
#     print("Joystick name: {}".format(name) )

#     axes = joystick.get_numaxes()
#     print("Number of axes: {}".format(axes) )

#     for i in range( axes ):
#         axis = joystick.get_axis( i )
#         print("Axis {} value: {:>6.3f}".format(i, axis) )

#     buttons = joystick.get_numbuttons()
#     print("Number of buttons: {}".format(buttons) )

#     for i in range( buttons ):
#         button = joystick.get_button( i )
#         print("Button {:>2} value: {}".format(i,button) )



while prog_main :
    prog_game = True
    count_time = 0
    print("RoboKiller est pret")
    if input_state_bp == False :
        print("Lancement de RoboKiller")
        while prog_game :
            count_time = count_time + 0.03
#            print(count_time)
            if count_time > game_time :
                prog_game = False
#            time.sleep(0.02) # Pour gérer la vitesse de la boucle while      
            pygame.time.delay(30)
            mesure_distance = robotkiller.eyes.measured(slow_distance)
            print(mesure_distance)
            events = pygame.event.get() #  retourne une liste d'events dans une table
            # pygame.event.pump() # Un truc qui sert à rien : permettre à la mémoire tampon d'événements de circuler facilement et d'éviter les mauvais comportements subtils entre différents systèmes
            for event in events : # on dépile la table evenement par évenement  
                if event.type == QUIT :
                    print("Sortie du programme")
                    prog_game = False
                    prog_main = False
                    pygame.quit

                # if event.type == pygame.JOYBUTTONDOWN:
                #     print("Joystick button pressed.")
                #     print(event.button)
                # if event.type == pygame.JOYBUTTONUP:
                #     print("Joystick button released.")
                #     print(event.button)

                if event.type == pygame.JOYBUTTONDOWN and event.button == 4:
                    # Chemille gauche - Marche avant
                    caterpillar_left_go = True
                    caterpillar_left_way = True
                    caterpillar_left_stop = False

                if event.type == pygame.JOYBUTTONDOWN and event.button == 6:
                    #Chemille gauche - Marche arrière
                    caterpillar_left_go = True
                    caterpillar_left_way = False
                    caterpillar_left_stop = False

                if event.type == pygame.JOYBUTTONUP and (event.button == 6 or event.button == 4):
                    # Chemille gauche - Rallentir
                    caterpillar_left_go = False

                if event.type == pygame.JOYBUTTONDOWN and event.button == 5:
                    # Chemille droite - Marche avant
                    print("Chemille droite - Marche avant")
                    caterpillar_right_go = True
                    caterpillar_right_way = True
                    caterpillar_right_stop = False

                if event.type == pygame.JOYBUTTONDOWN and event.button == 7:
                    #Chemille droite - Marche arrière
                    caterpillar_right_go = True
                    caterpillar_right_way = False
                    caterpillar_right_stop = False

                if event.type == pygame.JOYBUTTONUP and (event.button == 5 or event.button == 7):
                    # Chemille droite - Rallentir
                    caterpillar_right_go = False

                # Gestion du bras
                if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                    #Bras - UP
                    arm_move_up = True

                if event.type == pygame.JOYBUTTONDOWN and event.button == 2:
                    #Bras - Down
                    arm_move_down = True

                if event.type == pygame.JOYBUTTONUP and event.button == 0 :
                    #Bras - UP - Stop
                    arm_move_up = False

                if event.type == pygame.JOYBUTTONUP and event.button == 2 :
                    #Bras - Down - Stop
                    arm_move_down = False

                # Gestion de la pince
                if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
                    #Pince - Close
                    pince_close = True

                if event.type == pygame.JOYBUTTONDOWN and event.button == 3:
                    #Pince - Open 
                    pince_open = True

                if event.type == pygame.JOYBUTTONUP and event.button == 1 :
                    #Pince - Close
                    pince_close = False

                if event.type == pygame.JOYBUTTONUP and event.button == 3 :
                    #Pince - Open 
                    pince_open = False

            robotkiller.pince.work(pince_open,pince_close)
            robotkiller.arm.work(arm_move_up,arm_move_down)
            robotkiller.left.running(caterpillar_speed,caterpillar_left_go,caterpillar_left_way,caterpillar_left_stop)
            robotkiller.right.running(caterpillar_speed,caterpillar_right_go,caterpillar_right_way,caterpillar_right_stop)

 
# Sortie propre du programme
pygame.quit()
print("Arret system")
#os.system('sudo halt')
