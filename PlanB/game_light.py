#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
import os 
import time
import json
import pygame
from pygame.locals import *
from RkClassesHardware_light import Robotkiller

CIEL = 0, 200, 255
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0


def func_aff_move():

    screen__line_forward_left = pygame.draw.rect(screen, WHITE, [300, 20, 100, 50], 5)
    screen_forward_left = pygame.draw.rect(screen, color_screen_forward_left, [300, 20, 100, 50])

    screen_line_backward_left = pygame.draw.rect(screen, WHITE, [300, 80, 100, 50], 5)
    screen_backward_left = pygame.draw.rect(screen, color_screen_backward_left, [300, 80, 100, 50])

    screen_line_forward_right = pygame.draw.rect(screen, WHITE, [500, 20, 100, 50], 5)
    screen_forward_right = pygame.draw.rect(screen, color_screen_forward_right, [500, 20, 100, 50])

    screen_line_backward_right = pygame.draw.rect(screen, WHITE, [500, 80, 100, 50], 5)
    screen_backward_right = pygame.draw.rect(screen, color_screen_backward_right, [500, 80, 100, 50])

    pass 


if __name__ == '__main__':

    color_screen_forward_left = WHITE
    color_screen_backward_left = WHITE
    color_screen_forward_right = WHITE
    color_screen_backward_right = WHITE

    white_color = WHITE

    max_speed = 200
    min_speed = 50
    distance = 10
    move_forward_left = False 
    move_backward_left = False
    move_forward_right = False
    move_backward_right = False
    arm_up = True
    arm_down = False
    clamp_open = True
    clamp_close = False

    game_time = 120         # durée du jeu en seconde

    prog_main = True        # Variable pour la gestion de la boucle principale (PB)
    prog_game = True        # Variable pour la gestion de la boucle principale (jeux)

    robotkiller = Robotkiller()
    
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS']="8,610"
    screen = pygame.display.set_mode((1350, 150))
    pygame.display.set_caption('RobotKiller')
    fond = pygame.image.load("background.jpg").convert()
    screen.blit(fond, (0, 0))
    pygame.display.flip()

    chaine="Mesure Distance"
    font=pygame.font.SysFont("broadway",12,bold=False,italic=False)
    text=font.render(chaine,1,(1,1,1))
    screen.blit(text,(30,30))

    func_aff_move()

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
                robotkiller.pince.arret()
                robotkiller.arm.arret()
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
                move_forward_left = True
                color_screen_forward_left = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 4:
                # Chemille gauche - Marche avant - Rallentir
                move_forward_left = False
                color_screen_forward_left = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 6:
                #Chemille gauche - Marche arrière
                move_backward_left = True
                color_screen_backward_left = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 6:
                # Chemille gauche - Marche arrière - Rallentir
                move_backward_left = False
                color_screen_backward_left = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 5:
                # Chemille droite - Marche avant
                move_forward_right = True
                color_screen_forward_right = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 5:
                # Chemille droite - Marche avant - Rallentir
                move_forward_right = False
                color_screen_forward_right = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 7:
                #Chemille droite - Marche arrière
                move_backward_right = True
                color_screen_backward_right = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 7:
                # Chemille droite - Rallentir
                move_backward_right = False
                color_screen_backward_right = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                #Bras - UP
                arm_up = True
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 2:
                #Bras - Down
                arm_down = True
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 0 :
                #Bras - UP - Stop
                arm_up = False
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 2 :
                #Bras - Down - Stop
                arm_down = False
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
                #Pince - Close
                clamp_close = True
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 3:
                #Pince - Open 
                clamp_open = True
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 1 :
                #Pince - Close
                clamp_close = False
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 3 :
                #Pince - Open 
                clamp_open = False
                change_message = True



#        if change_message == True :
        robotkiller.pince.work(clamp_open, clamp_close)
        robotkiller.arm.work(arm_up,arm_down)
        robotkiller.left.running(max_speed, min_speed, move_forward_left, move_backward_left, False)
        robotkiller.right.running(max_speed, min_speed, move_forward_right, move_backward_right, False)
        # change_message = False

#        distance_to_collision = int(robotkiller.eyes.measured(distance))
        func_aff_move()
        pygame.display.flip() 

    # Sortie propre du programme
    pygame.quit()
    print("Arret system")
