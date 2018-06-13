#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
import os 
import time
from datetime import timedelta, datetime, date, time
import json
import pygame
from pygame.locals import *
from RkClassesHardware_light import Robotkiller, Caterpillar

CIEL = 0, 200, 255
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0

 
class Chrono:
    def __init__(self, position, font, color=(255, 255, 255)):
        self.chrono = datetime.combine(date.today(), time(0, 0))
        self.font = font
        self.color = color
        self.label = self._make_chrono_label()
        self.rect = self.label.get_rect(topleft=position)
 
    def _make_chrono_label(self):
        "Crée une Surface représentant le temps du chrono"
        return font.render(self.chrono.strftime("%M : %S"),
                           True, self.color)
 
    def update(self, dt):
        """Mise à jour du temps écoulé.
 
        dt est le nombre de millisecondes
        """
        old_chrono = self.chrono
        self.chrono += timedelta(milliseconds=dt)
        # Comme le chrono n'indique pas les fractions de secondes,
        # on ne met à jour le label que si quelque chose de visible a changé
        if old_chrono.second != self.chrono.second:
            self.label = self._make_chrono_label()
 
    def draw(self, surface):
        surface.blit(self.label, self.rect)
       
         


def func_aff_move():

    screen__line_forward_left = pygame.draw.rect(screen, WHITE, [300, 20, 100, 50], 5)
    screen_forward_left = pygame.draw.rect(screen, color_screen_forward_left, [300, 20, 100, 50])

    screen_line_backward_left = pygame.draw.rect(screen, WHITE, [300, 80, 100, 50], 5)
    screen_backward_left = pygame.draw.rect(screen, color_screen_backward_left, [300, 80, 100, 50])

    screen_line_forward_right = pygame.draw.rect(screen, WHITE, [500, 20, 100, 50], 5)
    screen_forward_right = pygame.draw.rect(screen, color_screen_forward_right, [500, 20, 100, 50])

    screen_line_backward_right = pygame.draw.rect(screen, WHITE, [500, 80, 100, 50], 5)
    screen_backward_right = pygame.draw.rect(screen, color_screen_backward_right, [500, 80, 100, 50])

    screen_line_arm_up = pygame.draw.rect(screen, WHITE, [700, 20, 100, 50], 5)
    screen_arm_up = pygame.draw.rect(screen, color_screen_arm_up, [700, 20, 100, 50])

    screen_line_arm_down = pygame.draw.rect(screen, WHITE, [700, 80, 100, 50], 5)
    screen_arm_down = pygame.draw.rect(screen, color_screen_arm_down, [700, 80, 100, 50])

    screen_line_clamp_open = pygame.draw.rect(screen, WHITE, [900, 20, 100, 50], 5)
    screen_clamp_open = pygame.draw.rect(screen, color_screen_clamp_open, [900, 20, 100, 50])

    screen_line_clamp_close = pygame.draw.rect(screen, WHITE, [900, 80, 100, 50], 5)
    screen_clamp_close = pygame.draw.rect(screen, color_screen_clamp_close, [900, 80, 100, 50])

    pass 


if __name__ == '__main__':

    color_screen_forward_left = WHITE
    color_screen_backward_left = WHITE
    color_screen_forward_right = WHITE
    color_screen_backward_right = WHITE
    color_screen_arm_up = WHITE
    color_screen_arm_down = WHITE
    color_screen_clamp_open = WHITE
    color_screen_clamp_close = WHITE

    white_color = WHITE

    distance = 10
    move_right = 0
    move_left = 0

    arm_up = True
    arm_down = False
    clamp_open = True
    clamp_close = False

    prog_main = True        # Variable pour la gestion de la boucle principale (PB)
 
    robotkiller = Robotkiller()
    
    pygame.init()
    os.environ['SDL_VIDEO_WINDOW_POS']="8,610"
    screen = pygame.display.set_mode((1350, 150))
    pygame.display.set_caption('RobotKiller')
    fond = pygame.image.load("background.jpg").convert()
    screen.blit(fond, (0, 0))
    func_aff_move()

    # gestion du temps
    font = pygame.font.Font(None, 64)
    fps_clock = pygame.time.Clock()
    chrono = Chrono(position=(40, 50), font=font)

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
    
        #Limitation de vitesse de la boucle
        #25 frames par secondes suffisent
        pygame.time.Clock().tick(25)

        dt = fps_clock.tick(60)
        chrono.update(dt)      
 
#        screen.fill(0)
        screen.blit(fond, (0, 0))
        chrono.draw(screen)
        pygame.display.update()

        # screen_time=str(cout_time)
        # font=pygame.font.SysFont("broadway",14,bold=True,italic=False)
        # text=font.render(screen_time,1,(1,1,1))
        # screen.blit(text,(30,30))


        events = pygame.event.get() #  retourne une liste d'events dans une table
        # pygame.event.pump() # Un truc qui sert à rien : permettre à la mémoire tampon d'événements de circuler facilement et d'éviter les mauvais comportements subtils entre différents systèmes
        for event in events : # on dépile la table evenement par évenement

#            time.sleep(0.01)
  
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
                move_left = Caterpillar.MOTOR_FORWARD
                color_screen_forward_left = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 4:
                # Chemille gauche - Marche avant - Rallentir
                move_left = Caterpillar.MOTOR_STOP
                color_screen_forward_left = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 6:
                #Chemille gauche - Marche arrière
                move_left = Caterpillar.MOTOR_BACKWARD
                color_screen_backward_left = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 6:
                # Chemille gauche - Marche arrière - Rallentir
                move_left = Caterpillar.MOTOR_STOP
                color_screen_backward_left = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 5:
                # Chemille droite - Marche avant
                move_right = Caterpillar.MOTOR_FORWARD
                color_screen_forward_right = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 5:
                # Chemille droite - Marche avant - Rallentir
                move_right = Caterpillar.MOTOR_STOP
                color_screen_forward_right = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 7:
                #Chemille droite - Marche arrière
                move_right = Caterpillar.MOTOR_BACKWARD
                color_screen_backward_right = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 7:
                # Chemille droite - Rallentir
                move_right = Caterpillar.MOTOR_STOP
                color_screen_backward_right = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                #Bras - UP
                arm_up = True
                color_screen_arm_up = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 2:
                #Bras - Down
                arm_down = True
                color_screen_arm_down = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 0 :
                #Bras - UP - Stop
                arm_up = False
                color_screen_arm_up = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 2 :
                #Bras - Down - Stop
                arm_down = False
                color_screen_arm_down = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
                #Pince - Close
                clamp_close = True
                color_screen_clamp_close = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONDOWN and event.button == 3:
                #Pince - Open 
                clamp_open = True
                color_screen_clamp_open = GREEN
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 1 :
                #Pince - Close
                clamp_close = False
                color_screen_clamp_close = WHITE
                change_message = True

            if event.type == pygame.JOYBUTTONUP and event.button == 3 :
                #Pince - Open 
                clamp_open = False
                color_screen_clamp_open = WHITE
                change_message = True

#        if change_message == True :
        robotkiller.pince.work(clamp_open, clamp_close)
        robotkiller.arm.work(arm_up,arm_down)
        robotkiller.left.running(move_left)
        robotkiller.right.running(move_right)
        # change_message = False

#        distance_to_collision = int(robotkiller.eyes.measured(distance))
        func_aff_move()
        pygame.display.flip() 

    # Sortie propre du programme
    pygame.quit()
    print("Arret system")
