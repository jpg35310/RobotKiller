# /usr/bin/env python

#from __future__ import absolute_import, division
import time
import os
import sys
import subprocess

import pygame
from pygame.locals import *
from RkClassesHardware import Robotkiller 


########### Prog de test qui ne marche pas.... ####################


# Initiallisation de la librairie PYGAME qui oblige à lancer un affichage
pygame.init() # initialisation de la librairie pour la gestion du graphique
EcranPi = pygame.display.set_mode((640, 480)) # pas le choix, obliger de lancer un affichage 
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

speed_caterpillar = 200
slow_distance = 10

caterpillar_speed = 200
caterpillar_left_go = False
caterpillar_right_go = False
caterpillar_left_way = True
caterpillar_right_way = True
caterpillar_left_stop = True
caterpillar_right_stop = True

#############################################################################################
########################## Les objets du programme ##########################################
#############################################################################################

#############################################################################################
########################## PROGRAMME PRINCIPAL ##############################################
#############################################################################################


robotkiller = Robotkiller()
time.sleep(1)

while prog_main :
    prog_game = True
    count_time = 0
    print("RoboKiller est pret")
    if input_state_bp == False :
        print("Lancement de RoboKiller")
        while prog_game :
            count_time = count_time + 0.02
#            print(count_time)
            if count_time > game_time :
                prog_game = False
#            time.sleep(0.02) # Pour gérer la vitesse de la boucle while      
            pygame.time.delay(30)
#            mesure_distance = robotkiller.eyes.measured(slow_distance)

            caterpillar_left_go = False
            caterpillar_right_go = False
            key=pygame.key.get_pressed()  #checking pressed keys
            if key[pygame.K_LSHIFT]:
                # Chemille gauche - Marche avant
                print("Chemille gauche - Marche avant")
                caterpillar_left_go = True
                caterpillar_left_way = True
                caterpillar_left_stop = False

            if key[pygame.K_LSHIFT] : # Touche enfoncée
                # Chemille gauche - Marche avant
                print("Chemille gauche - Marche avant")
                caterpillar_left_go = True
                caterpillar_left_way = True
                caterpillar_left_stop = False

            if key[pygame.K_LALT]:
                # Chemille gauche - Arret forcé
                print("Chemille gauche - stop")
                caterpillar_left_stop = True

            if key[pygame.K_LCTRL]:
                #Chemille gauche - Marche arrière
                print("Chemille gauche - Marche arrière")
                caterpillar_left_go = True
                caterpillar_left_way = False
                caterpillar_left_stop = False

            if key[pygame.K_RSHIFT]:
                # Chemille droit - Marche avant
                print("Chemille droite - Marche avant")
                caterpillar_right_go = True
                caterpillar_right_way = True
                caterpillar_right_stop = False

            if key[pygame.K_RALT]:
                # Chemille droit - Arret forcé
                print("Chemille droite - Stop")
                caterpillar_right_stop = True

            if key[pygame.K_RCTRL]:
                print("Chemille droite - Marche arrière")
                #Chemille droite - Marche arrière
                caterpillar_right_go = True
                caterpillar_right_way = False
                caterpillar_right_stop = False

            events = pygame.event.get() #  retourne une liste d'events dans une table
            # pygame.event.pump() # Un truc qui sert à rien : permettre à la mémoire tampon d'événements de circuler facilement et d'éviter les mauvais comportements subtils entre différents systèmes
            for event in events : # on dépile la table evenement par évenement  
                if event.type == QUIT:
                    print("Sortie du programme")
                    prog_game = False
                    prog_main = False
                    pygame.quit

            #     elif event.type == KEYDOWN and event.key == K_LSHIFT : # Touche enfoncée
            #         # Chemille gauche - Marche avant
            #         print("Chemille gauche - Marche avant")
            #         caterpillar_left_go = True
            #         caterpillar_left_way = True
            #         caterpillar_left_stop = False

            #     elif event.type == KEYDOWN and event.key == K_LALT:
            #         # Chemille gauche - Arret forcé
            #         print("Chemille gauche - stop")
            #         caterpillar_left_stop = True

            #     elif event.type == KEYDOWN and event.key == K_LCTRL:
            #         #Chemille gauche - Marche arrière
            #         print("Chemille gauche - Marche arrière")
            #         caterpillar_left_go = True
            #         caterpillar_left_way = False
            #         caterpillar_left_stop = False

            #     elif event.type == KEYDOWN and event.key == K_RSHIFT:
            #         # Chemille droit - Marche avant
            #         caterpillar_right_go = True
            #         caterpillar_right_way = True
            #         caterpillar_right_stop = False

            #     elif event.type == KEYDOWN and  event.key == K_RALT:
            #         # Chemille droit - Arret forcé
            #         caterpillar_right_stop = True

            #     elif event.type == KEYDOWN and event.key == K_RCTRL:
            #         #Chemille droite - Marche arrière
            #         caterpillar_right_go = True
            #         caterpillar_right_way = False
            #         caterpillar_right_stop = False

            #     elif event.type == KEYUP and (event.key == K_LSHIFT or event.key == K_LCTRL): # Touche relachée
            #         # Chemille gauche - Marche avant
            #         caterpillar_left_go = False

            #     elif event.type == KEYUP and (event.key == K_RSHIFT or event.key == K_RCTRL):
            #         # Chemille gauche - Marche avant
            #         caterpillar_right_go = False

                # elif event.key == pygame.locals.K_ESCAPE: # sortir du programme
                #     print("Sortie du programme")
                #     prog_game = False
                #     prog_main = False


            robotkiller.left.running(caterpillar_speed,caterpillar_left_go,caterpillar_left_way,caterpillar_left_stop)
            robotkiller.right.running(caterpillar_speed,caterpillar_right_go,caterpillar_right_way,caterpillar_right_stop)
 
# Sortie propre du programme
pygame.quit()
print("Arret system")
#os.system('sudo halt')
