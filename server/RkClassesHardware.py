#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#############################################################################################
#                                                                                           #
#                                ROBOTKILLER THE ULTIMATE KILLER                            #
#                                                                                           #
#                        Classes des servos moteurs et des drivers des moteurs              #
#                                                                                           #
#############################################################################################
#
# Explications pour gerer les bras/pince avec une valeur angulaire
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
############################### INITIALISATION ##############################################
#############################################################################################
import RPi.GPIO as GPIO    # GPIO et PWM soft - utilisé uniquement avec Caterpillar         
from RPIO import PWM       # GPIO et PWM via DMA - utilisé uniquement avec ServoMotor

#############################################################################################
########################## Initialisation des variables######################################
#############################################################################################
a_pwm = 32              # Chenille - Commande PWM moteur A -        BCM: 12 / pin: 32
b_pwm = 33              # Chenille - Commande PWM moteur B -        BCM: 13 / pin: 33
a_dir = 12              # Chenille - Sens de rotation du moteur A - BCM: 18 / pin: 12
b_dir = 13              # Chenille - Sens de rotation du moteur B - BCM: 27 / pin: 13
_max_speed = 100        # max speed est la valeur de cycle du PWM
MAX_SPEED = _max_speed  # Vitesse max
acc_def = 2             # Incrément de l'accélération (par défaut 3)

ledavg = 35             # LED - LED Avant Gauche (Verte) -          BCM: xx / pin: 35
ledavd = 36             # LED - LED Avant Droite (Verte) -          BCM: xx / pin: 36
ledarg = 37             # LED - LED Arrière Gauche (Rouge) -        BCM: xx / pin: 37
ledard = 38             # LED - LED Arrière Droite (Rouge) -        BCM: xx / pin: 38

pin_pince = 25          # Bras - pince -                            BCM: 25 / pin: 22
pin_bras1 = 24          # Bras - bras principale -                  BCM: 24 / pin: 18
pin_bras2 = 23          # Bras - bras de la pince -                 BCM: 23 / pin: 16
pin_bp = 40             # BP - Bouton poussoir de lancement -       BCM: XX / pin: 40

auto_caterpillar_left = False
auto_caterpillar_right = False
auto_pince = False
auto_bras1 = False
auto_bras2 = False

speed_caterpillar_left = 0
speed_caterpillar_right = 0

pince_angle_min = 0             # Pince ouverte
pince_angle = 90                 # Position au démarrage
pince_angle_max = 100           # Pince fermé
pince_way = False

bras1_angle_min = 10            # min:10° = bras relevé au max
bras1_angle = 50                # Position au démarrage
bras1_angle_max = 110           # max: 125° = bras au sol
bras1_way = False				#  UP: True ou DOWN: False

bras2_angle_min = 20            # min:x° = 
bras2_angle = 70                # Position au démarrage
bras2_angle_max = 91            # max: x° =
bras2_way = False               # UP: True ou DOWN: False 

io_initialized = False  # Variable pour intialiser qu'une seule fois les servosmoteurs

#############################################################################################
########################## Les objets du programme ##########################################
#############################################################################################
class Caterpillar(object):
    MAX_SPEED = _max_speed

    def __init__(self, pwm_pin, dir_pin, leda_pin, ledr_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.leda_pin = leda_pin
        self.ledr_pin = ledr_pin
#        self.motor = PWM.Servo()            # utilisation de la librairie RPIO qui gère les DMA
#        self.motor.__init__(1, 3000, 10)   # Initiallisation de la librairie sur DMA: 1 / f=20KHz / impultion mini: 1µs 
        self.motor = GPIO.PWM(pwm_pin, 2500)     # Définition de la fréquence en ms 
        self.motor.start(0)                      # Démarrage du moteur à l'arret
    def setspeed(self, speed):
        if speed < 0 :
            speed = -speed
            dir_value = 1
            GPIO.output(self.leda_pin,GPIO.LOW)
            GPIO.output(self.ledr_pin,GPIO.HIGH)
            GPIO.output(self.dir_pin,GPIO.HIGH)
        elif speed > 0 :
            dir_value = 0
            GPIO.output(self.leda_pin,GPIO.HIGH)
            GPIO.output(self.ledr_pin,GPIO.LOW)
            GPIO.output(self.dir_pin,GPIO.LOW)
        elif speed == 0 :
            GPIO.output(self.leda_pin,GPIO.LOW)
            GPIO.output(self.ledr_pin,GPIO.LOW)
        if speed > MAX_SPEED:
            speed = MAX_SPEED
#        self.motor.set_servo(self.pwm_pin, speed)
        self.motor.ChangeDutyCycle(speed)

class Caterpillars(object):
    MAX_SPEED = _max_speed

    def __init__(self):
        self.left = Caterpillar(a_pwm, a_dir, ledavg, ledarg)
        self.right = Caterpillar(b_pwm, b_dir, ledavd, ledard)

    def setspeeds(self, m1_speed, m2_speed):
        self.left.setspeed(m1_speed)
        self.right.setspeed(m2_speed)

#############################################################################################

class ServoMotor(object):

    def __init__(self, servo_pin, servo_cal_m, servo_cal_x1):
        self.servo_pin = servo_pin          # Pin GPIO du servo
        self.servo_cal_m = servo_cal_m      # valeur M propre à chaque servo
        self.servo_cal_x1 = servo_cal_x1    # valeur x1 propre à chaque servo
        self.servo = PWM.Servo()            # utilisation de la librairie RPIO qui gère les DMA
        self.servo.__init__(0, 20000, 10)   # Initiallisation de la librairie sur DMA: 0 / f=50Hz / impultion mini: 10µs 

    def angle(self, angle):
        self.servo.set_servo(self.servo_pin, round(((self.servo_cal_m*angle)+self.servo_cal_x1)/10,0)*10)

    def stop(self):
        self.servo.stop_servo(self.servo_pin)
    
class ServoMotors(object):

    def __init__(self):
        self.pince = ServoMotor(pin_pince, (2300-600)/180, 600)
        self.bras1 = ServoMotor(pin_bras1, (2250-750)/140, 750)
        self.bras2 = ServoMotor(pin_bras2, (2250-750)/140, 750)

    def angles(self, p_angle, b1_angle, b2_angle):
        self.pince.angle(p_angle)
        self.bras1.angle(b1_angle)
        self.bras2.angle(b2_angle)

#############################################################################################
########################## Fonctions du programme  ##########################################
#############################################################################################
def io_init():
    global io_initialized      # Définition d'une variable globale
    if io_initialized:         # Si déja initialisé on sort sans rien faire
        return
    # Initiallisation de la librairie RPi.GPIO as GPIO
    #GPIO.setmode(GPIO.BCM)         # mode de numérotation des pins
    GPIO.setmode(GPIO.BOARD)        # mode de numérotation de la carte
    GPIO.setwarnings(False)         # Suppression des warnings
    GPIO.setup(a_pwm, GPIO.OUT)     # Caterpillar moteur A - PWM 
    GPIO.setup(b_pwm, GPIO.OUT)     # Caterpillar moteur B - PWM 
    GPIO.setup(a_dir, GPIO.OUT)     # Caterpillar moteur A - DIR 
    GPIO.setup(b_dir, GPIO.OUT)     # Caterpillar moteur B - DIR 
    GPIO.setup(ledavg, GPIO.OUT, initial = GPIO.LOW)  # LED avant gauche
    GPIO.setup(ledavd, GPIO.OUT, initial = GPIO.LOW)  # LED avant droite
    GPIO.setup(ledarg, GPIO.OUT, initial = GPIO.LOW)  # LED arrière gauche
    GPIO.setup(ledard, GPIO.OUT, initial = GPIO.LOW)  # LED arrière gauche
    GPIO.setup(pin_bp, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    io_initialized = True
   

#############################################################################################

def acceleration(speed, auto):
    if speed != 0 and speed > 0 and speed < MAX_SPEED and auto == True :
        speed = speed + acc_def
    elif speed != 0 and speed > 0 and auto == False :
        speed = speed - acc_def
    elif speed != 0 and speed < 0 and abs(speed) < MAX_SPEED and auto == True :
        speed = speed - acc_def
    elif speed < 0 and auto == False :
        speed = speed + acc_def
    return speed


#############################################################################################

def chg_angle(angle, inc, angle_min, angle_max, auto, way):
    angle_ok = angle
    if angle > angle_min and angle < angle_max and auto == True and way == True :
        angle = angle + inc
        if angle > angle_min and angle < angle_max :
            angle_ok = angle
    elif angle > angle_min and angle < angle_max and auto == True and way == False :
        angle = angle - inc
        if angle > angle_min and angle < angle_max :
            angle_ok = angle
#    print (angle)
    return angle_ok
