#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
import time
import pigpio
from plugins.helpers import print_exception 

#############################################################################################
#                                                                                           #
#                                ROBOTKILLER THE ULTIMATE KILLER                            #
#                                                                                           #
#                        Class des servos moteurs et des drivers des moteurs                #
#                                                                                           #
#############################################################################################
#
#############################################################################################
#               Explications pour gerer les bras/pince avec une valeur angulaire            #
#############################################################################################
# Micro Servo Tower Pro SG90 (course de -90° à +90° soit 180°)
# Cablage: orange => PWM / Rouge => +5VDC / Marron => GND 
# Fréquence = 50Hz
# Position -90° = impultion de 1ms 
# Position 0° = impultion de 1.5ms 
# Position 90° = impultion de 2.0ms 
# Vitesse: 0.1 s/60 degree: pour calculer le time.sleep(x)  
#
# Micro Servo Tower Pro MG91 (course de 120°)
# Cablage: orange => PWM / Rouge => +5VDC / Marron => GND 
# Fréquence = 50Hz
# Position -60° = impultion de 1ms 
# Position 0° = impultion de 1.5ms 
# Position 60° = impultion de 2.0ms 
# Vitesse: 0.1 s/60 degree: pour calculer le time.sleep(x) 
#
# Pour trouver la bonne formule 
# Exemple:  PULSE = ((2300-600)/180)*ANGLE)+600 
# ou PULSE est la valeur de servo.set_servo(BCM, PULSE)
# donc il faut touver les deux points extreme : ( a taton manuellement)
# (x1: Min en ° / y1: PULSE min) et (x2: Max en ° / y2: PULSE max)
# calculer M = (Y2-Y1)/(x2-x1) en fraction (pas d'arrondi)
# formule PULSE = (M * angle) + y1
#
# Formule pour Micro Servo Tower Pro SG90 (pince)
# 0° = 600 // 180° = 2300
# PULSE = (((2300-600)/180)*ANGLE)+600
#
# Formule pour Micro Servo Tower Pro MG91 (bras N°1 et bras N°2)
# 0° = 700 // 120° = 2290
# PULSE = (((2250-750)/120)*ANGLE)+750
#
#############################################################################################
#                                Initialisation des constantes                              #
#############################################################################################
a_pwm = 12                      # Chenille - Commande PWM moteur A -        BCM: 12 / pin: 32
b_pwm = 13                      # Chenille - Commande PWM moteur B -        BCM: 13 / pin: 33

a_dir = 18                      # Chenille - Sens de rotation du moteur A - BCM: 18 / pin: 12
b_dir = 27                      # Chenille - Sens de rotation du moteur B - BCM: 27 / pin: 13

pin_trigger = 17                # Capteur de distance ultrason - trigger -   BCM:17 /pin: 11 
pin_echo = 4                    # Capteur de distance ultrason - echo -      BCM:04 /pin: 07
COLLISION = False               # Risque de collision qui oblige à passer en vitesse réduite 
temperature = 26                # Température ambiante en °C  
speedSound =33100 + (0.6*temperature)   # calcul de la vitesse du son en cm/s

ledavg = 19                     # LED - LED Avant Gauche (Verte) -          BCM: 19 / pin: 35
ledavd = 16                     # LED - LED Avant Droite (Verte) -          BCM: 16 / pin: 36
ledarg = 26                     # LED - LED Arrière Gauche (Rouge) -        BCM: 26 / pin: 37
ledard = 20                     # LED - LED Arrière Droite (Rouge) -        BCM: 20 / pin: 38

pin_pince = 25                  # Bras - pince -                            BCM: 25 / pin: 22
pin_bras1 = 24                  # Bras - bras principale -                  BCM: 24 / pin: 18
pin_bras2 = 23                  # Bras - bras de la pince -                 BCM: 23 / pin: 16
pin_bp = 21                     # BP - Bouton poussoir de lancement -       BCM: 21 / pin: 40

pince_servo_cal_m = (2300-600)/180  # valeur M propre à chaque servo
pince_servo_cal_x1 = 600            # valeur x1 propre à chaque servo
pince_angle_min = 20                # Pince ouverte
pince_angle_max = 100               # Pince fermé

bras1_servo_cal_m = (2250-750)/140  # valeur M propre à chaque servo
bras1_servo_cal_x1 = 750            # valeur x1 propre à chaque servo
bras1_angle_min = 15                # min:10° = bras relevé au max
bras1_angle_max = 110               # max: 125° = bras au sol

bras2_servo_cal_m = (2250-750)/140  # valeur M propre à chaque servo
bras2_servo_cal_x1 = 750            # valeur x1 propre à chaque servo
bras2_angle_min = 20                # min:x° = 
bras2_angle_max = 91                # max: x° =

#############################################################################################
#                                Initialisation des variables                               #
#############################################################################################
# En majuscule les variables globales
MAX_SPEED = 200                 # max speed est la valeur maxi de cycle du PWM supporté par le hardware
                                # 200 pour les moteurs de base
                                # 125 pour les moteurs de compétition !!!

COLLISION_SPEED = 50            # min speed est la valeur maxi de cycle en cas de risque de collision
max_speed_inc = 5

pince_angle = 20                # Position au démarrage
pince_angle_inc = 1

bras1_angle = 50                # Position au démarrage
bras1_angle_inc = 1

bras2_angle = 70                # Position au démarrage
bras2_angle_inc = 1 

#pigpio_host = "localhost"
pigpio_host = "192.168.0.151"
pigpio_tcp_port =8888

#############################################################################################
#              L'objet principale qui doit être appelé du programme principal               #
#                                                                                           #
#   Fonctionnement:                                                                         #
#   from RkClassesHardware import robotkiller                                               #
#   robotkiller = Robotkiller()                                                             #
#                                                                                           #
#   L'ensemble des appels suivant doivent être dans une boucle                              #
#   avec un temps de cycle de 20 à 100ms / test réalisé à 30ms                              #
#                                                                                           #
#   Fonctionnement des chenilles:                                                           #
#   robotkiller.right.running(max_speed,acceleration,forward,move_stop)                     #
#   robotkiller.left.running(max_speed,acceleration,forward,move_stop)                      #
#       max_speed = vitesse maxi du jeu de 0=arret à 200=maxi / test réalisé à 80 et 100    #
#       min_speed = Vitesse maxi en cas de risque de collision                              # 
#       move_forward: "True" = touche clavier enfoncé, le moteur accélé jusqu'a max_speed   # 
#                     "False" = touche clavier relaché, le moteur ralenti puis s'arrête     #
#       move_backward: idem move forward                                                    # 
#       move_stop: "True" = Arrêt                                                           #
#                                                                                           #
#   Fonctionnement du capteur de distance:                                                  #
#   mesure_distance = robotkiller.eyes.measured(slow_distance)                              #
#       mesure_distance = distance en cm de l'objet en face / il faut l'afficher dans IHM   #
#       slow_distance = valeur en cm qui va réduir la vitesse du robot                      #
#                                                                                           #
#   Fonctionnement de la pince                                                              #
#   robotkiller.pince.work(open,close)                                                      # 
#       open = True la pince se fermer                                                      #                                                                                            #
#       close = True la pince s'ouvre                                                       #
#       open & close = True / il ne se passera rien                                         #
#       open & close = False / la pince ne bouge plus                                       #
#                                                                                           #             
#   Fonctionnement du bras                                                                  #
#   robotkiller.bras.work(up,down)                                                          # 
#       up = True le bras monte                                                             #                                                                                            #
#       down = True le bras descend                                                         #
#       up & down = True / il ne se passera rien                                            #
#       up & down  = False / le bras ne bouge plus                                          #
#                                                                                           #             
#############################################################################################

class Robotkiller(object):

    def __init__(self):
        self.left = Caterpillar(a_pwm, a_dir, ledavg, ledarg)
        self.right = Caterpillar(b_pwm, b_dir, ledavd, ledard)
        self.pince = ServoMotor(pin_pince,pince_servo_cal_m,pince_servo_cal_x1,pince_angle_inc,pince_angle_min,pince_angle_max,pince_angle)
        self.arm = Arm()
        self.eyes = Distance(pin_echo, pin_trigger)
        self.button = PushButton(pin_bp)

    def runnings(self,left_max_speed, left_min_speed, left_move_forward, left_backward, left_move_stop, right_max_speed, right_min_speed, right_move_forward, right_backward, right_move_stop):
        self.left.running(left_max_speed, left_min_speed, left_move_forward, left_backward, left_move_stop)
        self.right.running(right_max_speed, right_min_speed, right_move_forward, right_backward, right_move_stop)

    def measures(self,slow_distance,mesure_distance):
        self.eyes.measured(slow_distance)

    def works(self,pince_open,pince_close,arm_up,arm_down):
        self.pince.work(pince_open,pince_close)
        self.arm.work(arm_up,arm_down)

    def pushs(self,status):
        self.button.push()


#############################################################################################
#                                  Class privées                                            #
#############################################################################################

class Caterpillar(object):
    def __init__(self, pwm_pin, dir_pin, leda_pin, ledr_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.leda_pin = leda_pin
        self.ledr_pin = ledr_pin
        self.last_direction = True                              # Dernier sens de rotation du moteur / False = Arrière / True = Avancer
        self.acceleration_inc = max_speed_inc                   # Incrément de l'accélération (par défaut 3)
        self.speed = 0                                          # vitesse courante de la chenille
        self.motor = pigpio.pi(pigpio_host, pigpio_tcp_port)    # Création d'une instance PIGPIO
        if not self.motor.connected:
            print("Erreur initialisation PiGPIO")
            exit()    
        self.motor.set_mode(self.dir_pin, pigpio.OUTPUT)
        self.motor.set_mode(self.leda_pin, pigpio.OUTPUT)
        self.motor.set_mode(self.ledr_pin, pigpio.OUTPUT)
        self.motor.write(self.dir_pin,0)
        self.motor.write(self.leda_pin,0)
        self.motor.write(self.ledr_pin,0)
#        self.motor.set_PWM_frequency(self.pwm_pin,8000)    # PWM Soft - Définition de la fréquence en ms soit 8KHz=8000 au lieu de 20KHz=20000
        self.motor.hardware_PWM(self.pwm_pin, 4000, 0)      # PWM Hard - Au final 4KHz avec un dutycycle de 0%, donc moteur à l'arret
        self.motor.set_PWM_range(self.pwm_pin, 200)         # donc 50 = 1/4 à 1 pour un cycle, 100=1/2,   150=3/4, 200/on

    def running(self,max_speed,min_speed,move_forward,move_backward,move_stop):

        # Arret d'urgence
        if (move_stop == True) or ((move_forward == True) and (self.last_direction = "backward")) or ((move_backward == True) and (self.last_direction = "forward")) : 
            self.speed = 0
            self.motor.write(self.leda_pin,0)
            self.motor.write(self.ledr_pin,0)

        # Marche avant
        elif (move_forward == True and self.speed > 0) :
            self.motor.write(self.leda_pin,1)
            self.motor.write(self.ledr_pin,0)
            self.motor.write(self.dir_pin,0)

        # Marche arrière
        elif (move_backward == True and self.speed > 0) :
            self.motor.write(self.leda_pin,0)
            self.motor.write(self.ledr_pin,1)
            self.motor.write(self.dir_pin,1)

        # Acceleration et sécurité      
        if (COLLISION == True) and ((move_forward == True) or ((move_backward == True) :
            if self.speed < COLLISION_SPEED :                
                self.speed = self.speed + self.acceleration_inc
            if self.speed > COLLISION_SPEED :                
                self.speed = self.speed - self.acceleration_inc

        elif ((move_forward == True) or ((move_backward == True)) and  (move_stop == False):  
            self.speed = self.speed + self.acceleration_inc
            if self.speed > max_speed :                         #Vitesse maxi du jeu
                self.speed = max_speed
            elif self.speed > MAX_SPEED :                       #Vitesse maxi supporté par le hardware
                self.speed = MAX_SPEED

        # Ralentir et s'arrêter      
        else :
            if self.speed == 0 :
                pass
            else:
                self.speed = self.speed - self.acceleration_inc
            
            if self.speed <= 0 :                                #Si on est arrêté, on y reste et pas valeur négative
                self.speed = 0
                
                self.motor.write(self.leda_pin,0)
                self.motor.write(self.ledr_pin,0)
 
        self.motor.set_PWM_dutycycle(self.pwm_pin, self.speed)  # Envois de la nouvelle vitesse au moteur
#        print("Speed Cycle: {0:5.1f}".format(self.speed))


        # Mémorisation du sens de rotation
        if move_forward = True :
            self.last_direction = "forward"                           
        elif move_backward = True :
            self.last_direction = "backward"                           
        
class Distance(object):
    def __init__(self, pin_echo, pin_trigger):
        self.echo_pin = pin_echo
        self.trigger_pin = pin_trigger
        self.mesure_distance = 0
        self.mesure = pigpio.pi(pigpio_host, pigpio_tcp_port)   # utilisation de la librairie PiGPIO qui gère les DMA
        if not self.mesure.connected:
             print("Erreur initialisation PiGPIO")
             exit()    
        self.mesure.set_mode(self.trigger_pin, pigpio.OUTPUT)
        self.mesure.set_mode(self.echo_pin, pigpio.INPUT)
        self.mesure.write(self.trigger_pin, 0)                  # On passe le trigger à Low
        time.sleep(0.5)                                         # On attend que le module à ultrason s'inititalise la première fois (sinon ca bug)
        self.toolong = 10000                                    # temps maxi de la mesure en ms
        self.high_tick = None                                   # 
        self.echo_time = self.toolong
        self.echo_tick = self.mesure.get_current_tick()         # valeur du temps CPU en µs
        self.cb = self.mesure.callback(self.echo_pin, pigpio.EITHER_EDGE, self._cbf)

    def _cbf(self, gpio, level, tick):
        # Mesure de l'interval de temps (en tick) : echo_time 
        if level == 1:
            self.high_tick = tick
        else:
            if self.high_tick is not None:
                echo_time = tick - self.high_tick
            if echo_time < self.toolong:
               self.echo_time = echo_time
               self.echo_tick = tick
            else:
               self.echo_time = self.toolong
            self.high_tick = None

    def measured(self,slow_distance):
        # Mesure de la distance
        self.mesure.gpio_trigger(self.trigger_pin, 10, 1)       # impulsion de 10us pour déclencher la mesure (Front haut)
        time.sleep(0.00001)
        distance = self.echo_time / 1000000.0 * speedSound      # La distance parcourue pendant ce temps = le temps X la vitesse du son (cm/s)
        self.mesure_distance = distance / 2                     # C'était la distance aller et retour donc on divise la valeur par 2
#        print("Distance Class: {0:5.1f}".format(self.mesure_distance))
#        print("slow_distance Class: {0:5.1f}".format(SLOW_DISTANCE))
        # Calcul du risque de collision nécessitant de passer en vitesse réduite
        global COLLISION
        if self.mesure_distance < slow_distance :
            COLLISION = True
        else :
            COLLISION = False
        # On retourne la mesure de distance au Prog principal pour affichage sur l'IHM        
        return (self.mesure_distance)

class ServoMotor(object):
    def __init__(self, servo_pin, servo_cal_m, servo_cal_x1, inc_angle, min_angle, max_angle, angle):
        self.servo_pin = servo_pin          # Pin GPIO du servo
        self.servo_cal_m = servo_cal_m      # valeur M propre à chaque servo
        self.servo_cal_x1 = servo_cal_x1    # valeur x1 propre à chaque servo
        self.angle_inc = inc_angle
        self.angle_min = min_angle
        self.angle_max = max_angle
        self.angle_move = angle
        self.angle_init = angle
        self.servo = pigpio.pi(pigpio_host, pigpio_tcp_port)    # utilisation de la librairie PiGPIO qui gère les DMA
        if not self.servo.connected:
            print("Erreur initialisation PiGPIO")
            exit()    
        self.servo.set_servo_pulsewidth(self.servo_pin, round(((self.servo_cal_m*self.angle_move)+self.servo_cal_x1)/10,0)*10)

    def __del__(self):
        self.angle_move = self.angle_init
#        self.servo.set_servo_pulsewidth(self.servo_pin, round(((self.servo_cal_m*self.angle_move)+self.servo_cal_x1)/10,0)*10)
# Là j'ai un problème de compréhension du foncitonnement de la destruction des objets
        time.sleep(0.5)                     # pour que le servo ait le temps de revenir en possition de départ

    def work(self,way_left,way_right):
        if (way_left == True) and (way_right == False):
            self.angle_move = self.angle_move - self.angle_inc
            if self.angle_move < self.angle_min :
                self.angle_move = self.angle_min    

        elif (way_left == False) and (way_right == True):  
            self.angle_move = self.angle_move + self.angle_inc
            if self.angle_move > self.angle_max :
                self.angle_move = self.angle_max 

        # print("Angle_inc: {0:5.1f}".format(self.angle_inc))
        # print("Angle_min: {0:5.1f}".format(self.angle_min))
        # print("Angle_max: {0:5.1f}".format(self.angle_max))
        # print("Angle_move: {0:5.1f}".format(self.angle_move))
        self.servo.set_servo_pulsewidth(self.servo_pin, round(((self.servo_cal_m*self.angle_move)+self.servo_cal_x1)/10,0)*10)

class Arm(object):
    def __init__(self):
        self.arm_up = False
        self.arm_down = False
        self.bras1 = ServoMotor(pin_bras1,bras1_servo_cal_m,bras1_servo_cal_x1,bras1_angle_inc,bras1_angle_min,bras1_angle_max,bras1_angle)
        self.bras2 = ServoMotor(pin_bras2,bras2_servo_cal_m,bras2_servo_cal_x1,bras2_angle_inc,bras2_angle_min,bras2_angle_max,bras2_angle)

    def work(self,arm_up,arm_down):

        if (arm_up == True) and (arm_down == False):
            self.bras1.work(True,False)
            self.bras2.work(False,True)

        elif (arm_up == False) and (arm_down == True):  
            self.bras1.work(False,True)
            self.bras2.work(True,False)

class PushButton(object):
    def __init__(self, bp_pin):
        self.bp_pin = bp_pin
        self.status = 0
        self.bp = pigpio.pi(pigpio_host, pigpio_tcp_port)    # Création d'une instance PIGPIO
        if not self.bp.connected:
            print("Erreur initialisation PiGPIO")
            exit()    
        self.bp.set_mode(self.bp_pin, pigpio.INPUT)
        self.high_tick = None                                 # 
        self.bp_time = 0
        self.bp_tick = self.bp.get_current_tick()         # valeur du temps CPU en µs
        self.cb = self.bp.callback(self.bp_pin, pigpio.EITHER_EDGE, self._cbf)

    def _cbf(self, gpio, level, tick):
        # Mesure de l'interval de temps (en tick) : bp_time 
        if level == 1:
            self.high_tick = tick
            print("entrée dans level 1)")
        else:
            if self.high_tick is not None:
                bp_time = tick - self.high_tick
                self.bp_time = bp_time / 1000000000.0           # Durée du maintien du bp en millisecondes
                print("bp_time: {0:5.1f}".format(self.bp_time))
                self.bp_tick = tick
            self.high_tick = None

    def push(self):
        # Arret d'urgence
        print("bp_time: {0:5.1f}".format(self.bp_time))
        if (self.bp_time > 1) and (self.bp_time < 3000) :       # lors d'un appuie bref sur le bp < à 3 secondes
            self.status = 1                                       # Pour arrêt des chenilles en cas de problème
        elif self.bp_time > 3000  :                             # lors d'un appuie long sur le bp > à 3 secondes
            self.status = 2                                       # Arrêt de l'OS
        else :
            self.status = 0                                       # si pas d'appuie renvoit de 0
        return (self.status)                                      # on renvoit la valeur du BP



