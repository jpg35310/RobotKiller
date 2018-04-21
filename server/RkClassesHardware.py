#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from helpers import print_exception # là, il y a un truc qui merde / a voir plus tard / déplacer dans racine
import RPi.GPIO as GPIO    # GPIO et PWM soft - utilisé uniquement avec Caterpillar         
from RPIO import PWM       # GPIO et PWM via DMA - utilisé uniquement avec ServoMotor
import time
#
#############################################################################################
#                                                                                           #
#                                ROBOTKILLER THE ULTIMATE KILLER                            #
#                                                                                           #
#                        Class des servos moteurs et des drivers des moteurs                #
#                                                                                           #
#############################################################################################
#
#############################################################################################
#                                Initialisation des variables                               #
#############################################################################################
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
#
# En majuscule les variables globales
a_pwm = 32                      # Chenille - Commande PWM moteur A -        BCM: 12 / pin: 32
b_pwm = 33                      # Chenille - Commande PWM moteur B -        BCM: 13 / pin: 33
a_dir = 12                      # Chenille - Sens de rotation du moteur A - BCM: 18 / pin: 12
b_dir = 13                      # Chenille - Sens de rotation du moteur B - BCM: 27 / pin: 13
MAX_SPEED = 100                 # max speed est la valeur maxi de cycle du PWM supporté par le hardware
COLLISION_SPEED = 20            # min speed est la valeur maxi de cycle en cas de risque de collision

pin_trigger1 = 11               # Capteur de distance ultrason - trigger 
pin_echo1 = 7                   # Capteur de distance ultrason - echo
COLLISION = False               # Risque de collision qui doit obliger le rebot à passer en vitesse réduite 
temperature = 26                # Température ambiante en °C  
speedSound =33100 + (0.6*temperature)   # calcul de la vitesse du son en cm/s

ledavg = 35                     # LED - LED Avant Gauche (Verte) -          BCM: xx / pin: 35
ledavd = 36                     # LED - LED Avant Droite (Verte) -          BCM: xx / pin: 36
ledarg = 37                     # LED - LED Arrière Gauche (Rouge) -        BCM: xx / pin: 37
ledard = 38                     # LED - LED Arrière Droite (Rouge) -        BCM: xx / pin: 38

pin_pince = 25                  # Bras - pince -                            BCM: 25 / pin: 22
pin_bras1 = 24                  # Bras - bras principale -                  BCM: 24 / pin: 18
pin_bras2 = 23                  # Bras - bras de la pince -                 BCM: 23 / pin: 16
pin_bp = 40                     # BP - Bouton poussoir de lancement -       BCM: XX / pin: 40

pince_servo_cal_m = (2300-600)/180  # valeur M propre à chaque servo
pince_servo_cal_x1 = 600            # valeur x1 propre à chaque servo
pince_angle_min = 20                # Pince ouverte
pince_angle = 20                    # Position au démarrage
pince_angle_max = 100               # Pince fermé
pince_angle_inc = 2

bras1_servo_cal_m = (2250-750)/140  # valeur M propre à chaque servo
bras1_servo_cal_x1 = 750            # valeur x1 propre à chaque servo
bras1_angle_min = 15                # min:10° = bras relevé au max
bras1_angle = 50                    # Position au démarrage
bras1_angle_max = 110               # max: 125° = bras au sol
bras1_angle_inc = 1

bras2_servo_cal_m = (2250-750)/140  # valeur M propre à chaque servo
bras2_servo_cal_x1 = 750            # valeur x1 propre à chaque servo
bras2_angle_min = 20                # min:x° = 
bras2_angle = 70                    # Position au démarrage
bras2_angle_max = 91                # max: x° =
bras2_angle_inc = 1 

io_initialized = False          # Variable pour intialiser qu'une seule fois les GPIO


#############################################################################################
#                     L'objet principale qui doit être appelé  de l'extérieur               #
#                                                                                           #
#   Fonctionnement:                                                                         #
#   from RkClassesHardware import robotkiller                                               #
#   robotkiller = Robotkiller()                                                             #
#                                                                                           #
#   L'ensemble des appels suivant doivent être dans une boucle                              #
#   avec un temps de cycle de 20 à 100ms / test réalisé à 30ms                              #
#                                                                                           #
#   Fonctionnement des chenilles:                                                           #
#   robotkiller.right.running(max_speed,acceleration,forward,stopping)                      #
#   robotkiller.left.running(max_speed,acceleration,forward,stopping)                       #
#       max_speed = vitesse maxi du jeu de 0=arret à 100=maxi / test réalisé à 80 et 100    # 
#       acceleration = True => touche clavier enfoncé et le moteur accélé jusqu'a max_speed # 
#       acceleration = False => touche clavier relaché et le moteur ralenti puis s'arrête   # 
#       forward = True on avance / Flase on recule                                          #
#       stopping =  Flase = ok / True = Arrêt brusque                                       #
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
        io_init()
        self.left = Caterpillar(a_pwm, a_dir, ledavg, ledarg)
        self.right = Caterpillar(b_pwm, b_dir, ledavd, ledard)
        self.pince = ServoMotor(pin_pince,pince_servo_cal_m,pince_servo_cal_x1,pince_angle_inc,pince_angle_min,pince_angle_max,pince_angle)
        self.arm = Arm()
        self.eyes = Distance(pin_echo1, pin_trigger1)

    # def __del__(self):
    #     GPIO.cleanup()
    #     PWM.cleanup()

    def runnings(self,left_max_speed,left_acceleration,left_forward,left_stopping,right_max_speed,right_acceleration,right_forward,right_stopping):
        self.left.running(left_max_speed,left_acceleration,left_forward,left_stopping)
        self.right.running(right_max_speed,right_acceleration,right_forward,right_stopping)

    def measures(self,slow_distance,mesure_distance):
        self.eyes.measured(slow_distance)

    def works(self,pince_open,pince_close,arm_up,arm_down):
        self.pince.work(pince_open,pince_close)
        self.arm.work(arm_up,arm_down)


#############################################################################################
#                       Fonction initialisation des GPIO pour RPi.GPIO                      #
#############################################################################################

def io_init():                                                  # Initiallisation nécessaire pour RPi.GPIO
    global io_initialized                                       # Définition d'une variable globale
    if io_initialized:                                          # Si déja initialisé on sort sans rien faire
        return
    #GPIO.setmode(GPIO.BCM)                                     # mode de numérotation des pins
    GPIO.setmode(GPIO.BOARD)                                    # mode de numérotation de la carte
    GPIO.setwarnings(False)                                     # Suppression des warnings
    GPIO.setup(a_pwm, GPIO.OUT)                                 # Caterpillar moteur A - PWM 
    GPIO.setup(b_pwm, GPIO.OUT)                                 # Caterpillar moteur B - PWM 
    GPIO.setup(a_dir, GPIO.OUT)                                 # Caterpillar moteur A - DIR 
    GPIO.setup(b_dir, GPIO.OUT)                                 # Caterpillar moteur B - DIR 
    GPIO.setup(ledavg, GPIO.OUT, initial = GPIO.LOW)            # LED avant gauche
    GPIO.setup(ledavd, GPIO.OUT, initial = GPIO.LOW)            # LED avant droite
    GPIO.setup(ledarg, GPIO.OUT, initial = GPIO.LOW)            # LED arrière gauche
    GPIO.setup(ledard, GPIO.OUT, initial = GPIO.LOW)            # LED arrière gauche
    GPIO.setup(pin_bp, GPIO.IN, pull_up_down = GPIO.PUD_UP)     # Bouton pousoir
    GPIO.setup(pin_trigger1,GPIO.OUT)                           # Capteur ulrasonic - Trigger
    GPIO.setup(pin_echo1,GPIO.IN)                               # Capteur ulrasonic - Echo
    io_initialized = True


#############################################################################################
#                                  Class privées                                            #
#############################################################################################

class Caterpillar(object):
    def __init__(self, pwm_pin, dir_pin, leda_pin, ledr_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin
        self.leda_pin = leda_pin
        self.ledr_pin = ledr_pin
        self.last_direction = True              # Dernier sens de rotation du moteur / False = Arrière / True = Avancer
        self.acceleration_inc = 1               # Incrément de l'accélération (par défaut 3)
        self.speed = 0                          # vitesse courante de la chenille
        self.motor = GPIO.PWM(pwm_pin, 2500)    # Définition de la fréquence en ms 
        self.motor.start(0)                     # Démarrage du moteur à l'arret

 
    def running(self,max_speed,acceleration,forward,stopping):
        # Arret d'urgence
        if (stopping == True) or ((acceleration == True) and (forward != self.last_direction)) : 
            self.speed = 0
            GPIO.output(self.leda_pin,GPIO.LOW)
            GPIO.output(self.ledr_pin,GPIO.LOW)

        # Marche avant
        elif (forward == True) :
            GPIO.output(self.leda_pin,GPIO.HIGH)
            GPIO.output(self.ledr_pin,GPIO.LOW)
            GPIO.output(self.dir_pin,GPIO.LOW)

        # Marche arrière
        elif (forward == False) :
            GPIO.output(self.leda_pin,GPIO.LOW)
            GPIO.output(self.ledr_pin,GPIO.HIGH)
            GPIO.output(self.dir_pin,GPIO.HIGH)


        # Acceleration et sécurité      
        if (COLLISION == True) and (acceleration == True) :
            if self.speed < COLLISION_SPEED :                
                self.speed = self.speed + self.acceleration_inc
            if self.speed > COLLISION_SPEED :                
                self.speed = self.speed - self.acceleration_inc

        elif (acceleration == True) and  (stopping == False):  
            self.speed = self.speed + self.acceleration_inc
            if self.speed > max_speed :                      #Vitesse maxi du jeu
                self.speed = max_speed
            elif self.speed > MAX_SPEED :                    #Vitesse maxi supporté par le hardware
                self.speed = MAX_SPEED

        # Ralentir et s'arrêter      
        else :
            self.speed = self.speed - self.acceleration_inc
            if self.speed < 0 :                             #Si on est arrêté, on y reste et pas valeur négative
                self.speed = 0
 
        
        self.motor.ChangeDutyCycle(self.speed)              # Envois de la nouvelle vitesse au moteur
#        print("Speed Cycle: {0:5.1f}".format(self.speed))
        self.last_direction = forward                       # Mémorisation du sens de rotation


class Distance(object):
    def __init__(self, pin_echo, pin_trigger):
        self.echo_pin = pin_echo
        self.trigger_pin = pin_trigger
        self.mesure_distance = 0
        GPIO.output(self.trigger_pin, False)                # On passe le trigger à Low
        time.sleep(0.5)                                     # On attend que le module à ultrason s'inititalise la première fois (sinon ca bug)

    def measured(self,slow_distance):
        # Mesure de la distance
        GPIO.output(self.trigger_pin, True)                 # Envoyer une impulsion de 10us pour déclencher la mesure (Front haut)
        time.sleep(0.00001)                                 # on attend 10us
        GPIO.output(self.trigger_pin, False)                # Envoyer une impulsion de 10us pour déclencher la mesure  (Front bas)
        start = time.time()
        while GPIO.input(self.echo_pin)==0:
          start = time.time()
        while GPIO.input(self.echo_pin)==1:
          stop = time.time()
        elapsed = stop-start                                # Calcule de la durée de l'impulsion
        distance = elapsed * speedSound                     # La distance parcourue pendant ce temps = le temps X la vitesse du son (cm/s)
        self.mesure_distance = distance / 2                 # C'était la distance aller et retour donc on divise la valeur par 2
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
        self.servo = PWM.Servo()            # utilisation de la librairie RPIO qui gère les DMA
        self.servo.__init__(0, 20000, 10)   # Initiallisation de la librairie sur DMA: 0 / f=50Hz / impultion mini: 10µs 
        self.servo.set_servo(self.servo_pin, round(((self.servo_cal_m*self.angle_move)+self.servo_cal_x1)/10,0)*10)


    def __del__(self):
        self.angle_move = self.angle_init
        self.servo.set_servo(self.servo_pin, round(((self.servo_cal_m*self.angle_move)+self.servo_cal_x1)/10,0)*10)
        time.sleep(0.1)                     # pour que le servo ait le temps de revenir un possition de départ

    def work(self,way_left,way_right):
        if (way_left == True) and (way_right == False):
            self.angle_move = self.angle_move - self.angle_inc
            if self.angle_move < self.angle_min :
                self.angle_move = self.angle_min    

        elif (way_left == False) and (way_right == True):  
            self.angle_move = self.angle_move + self.angle_inc
            if self.angle_move > self.angle_max :
                self.angle_move = self.angle_max 

        print("Angle_inc: {0:5.1f}".format(self.angle_inc))
        print("Angle_min: {0:5.1f}".format(self.angle_min))
        print("Angle_max: {0:5.1f}".format(self.angle_max))
        print("Angle_move: {0:5.1f}".format(self.angle_move))
        self.servo.set_servo(self.servo_pin, round(((self.servo_cal_m*self.angle_move)+self.servo_cal_x1)/10,0)*10)


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

