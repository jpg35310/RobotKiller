#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division
import time
import pigpio

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
speedSound = 33100 + (0.6*temperature)   # calcul de la vitesse du son en cm/s

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
bras1_angle_max = 105               # max: 125° = bras au sol 110
# A modifier pour chaque Robot
# RBK01 =>  min = 15 / max =105
# RBK02 =>  min = XX / max =1XX

bras2_servo_cal_m = (2250-750)/140  # valeur M propre à chaque servo
bras2_servo_cal_x1 = 750            # valeur x1 propre à chaque servo
bras2_angle_min = 25                # min:x° = 30
bras2_angle_max = 90                # max: x° = 91 / 90
# A modifier pour chaque Robot
# RBK01 =>  min = 25 / max =90
# RBK02 =>  min = XX / max =XX

#############################################################################################
#                                Initialisation des variables                               #
#############################################################################################
# En majuscule les variables globales
MAX_SPEED = 200                 # max speed est la valeur maxi de cycle du PWM supporté par le hardware

COLLISION_SPEED = 50            # min speed est la valeur maxi de cycle en cas de risque de collision
max_speed_inc = 5
max_speed_dec = 20

pince_angle = 20                # Position au démarrage
pince_angle_inc = 2

bras1_angle = 50                # Position au démarrage
bras1_angle_inc = 2

bras2_angle = 70                # Position au démarrage
bras2_angle_inc = 2

#pigpio_host = "localhost"
pigpio_host = "192.168.0.152"
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


class Controller(object):
    POS_LEFT = 'left'
    POS_RIGHT = 'right'

    MOTOR_FORWARD = 0
    MOTOR_BACKWARD = 1

    SERVO_ARM_1 = 'pin_arm_1'
    SERVO_ARM_2 = 'pin_arm_2'
    SERVO_CLAMP = 'pin_clamp'

    def __init__(self, *args, **kwargs):
        self.pin_motor_left = kwargs.get('pin_motor_left', a_pwm)
        self.pin_dir_left = kwargs.get('pin_dir_left', a_dir)
        self.pin_led_front_left = kwargs.get('pin_led_front_left', ledavg)
        self.pin_led_back_left = kwargs.get('pin_led_back_left', ledarg)

        self.pin_motor_right = kwargs.get('pin_motor_right', b_pwm)
        self.pin_dir_right = kwargs.get('pin_dir_right', b_dir)
        self.pin_led_front_right = kwargs.get('pin_led_front_right', ledavd)
        self.pin_led_back_right = kwargs.get('pin_led_back_right', ledard)

        self.pin_arm_1 = kwargs.get('pin_arm_1', pin_bras1)
        self.pin_arm_2 = kwargs.get('pin_arm_2', pin_bras2)
        self.pin_clamp = kwargs.get('pin_clamp', pin_pince)
        self.pin_bp = kwargs.get('pin_bp', pin_bp)

        self.pin_trigger = kwargs.get('pin_trigger', pin_trigger)
        self.pin_echo = kwargs.get('pin_echo', pin_echo)

        self.pgpio_host = kwargs.get('pgpio_host', pigpio_host)
        self.pgpio_port = kwargs.get('pgpio_port', pigpio_tcp_port)

        self.motor = Controller.init_pgpio(self.pgpio_host, self.pgpio_port)
        self.max_motor_cycle_range = kwargs.get('max_motor_cycle_range', 200)
        self.max_motor_frequency = kwargs.get('max_motor_frequency', 4000)

        self.init_gpio()

    @staticmethod
    def init_pgpio(host, port):
        pi = pigpio.pi(host, port)  # Création d'une instance PIGPIO
        if not pi.connected:
            print("Erreur initialisation PiGPIO")
            raise Exception("Erreur initialisation PiGPIO")

        return pi

    def init_gpio(self):
        self.motor.set_mode(self.pin_dir_left, pigpio.OUTPUT)
        self.motor.set_mode(self.pin_dir_right, pigpio.OUTPUT)
        self.motor.set_mode(self.pin_led_back_left, pigpio.OUTPUT)
        self.motor.set_mode(self.pin_led_back_right, pigpio.OUTPUT)
        self.motor.set_mode(self.pin_led_front_left, pigpio.OUTPUT)
        self.motor.set_mode(self.pin_led_front_right, pigpio.OUTPUT)

        self.motor.hardware_PWM(self.pin_motor_left, self.max_motor_frequency, 0)
        self.motor.hardware_PWM(self.pin_motor_right, self.max_motor_frequency, 0)

        # 50 = 1/4  du cycle, 100=1/2,   150=3/4, 200/on plein puissance
        self.motor.set_PWM_range(self.pin_motor_left, self.max_motor_cycle_range)
        self.motor.set_PWM_range(self.pin_motor_right, self.max_motor_cycle_range)

        self.switch_motor_direction(Controller.POS_LEFT, Controller.MOTOR_FORWARD)
        self.switch_motor_direction(Controller.POS_RIGHT, Controller.MOTOR_FORWARD)

        self.switch_led_back(Controller.POS_LEFT, 0)
        self.switch_led_back(Controller.POS_RIGHT, 0)
        self.switch_led_front(Controller.POS_LEFT, 0)
        self.switch_led_front(Controller.POS_RIGHT, 0)

        self.use_servo(Controller.SERVO_ARM_1, bras1_angle)
        self.use_servo(Controller.SERVO_ARM_2, bras2_angle)
        self.use_servo(Controller.SERVO_CLAMP, pince_angle)

        self.motor.set_mode(self.pin_trigger, pigpio.OUTPUT)
        self.motor.set_mode(self.pin_echo, pigpio.INPUT)

    def switch_led_front(self, side, mode=0):
        value = int(bool(mode))
        if side is Controller.POS_LEFT:
            self.motor.write(self.pin_led_front_left, value)
        if side is Controller.POS_RIGHT:
            self.motor.write(self.pin_led_front_right, value)

    def switch_led_back(self, side, mode=0):
        value = int(bool(mode))
        if side is Controller.POS_LEFT:
            self.motor.write(self.pin_led_back_left, value)
        if side is Controller.POS_RIGHT:
            self.motor.write(self.pin_led_back_right, value)

    def switch_motor_direction(self, side, direction):
        value = int(bool(direction))
        if side is Controller.POS_LEFT:
            self.motor.write(self.pin_dir_left, value)
        if side is Controller.POS_RIGHT:
            self.motor.write(self.pin_dir_right, value)

    def use_motor(self, side, speed=0):
        if side is Controller.POS_LEFT:
            self.motor.set_PWM_dutycycle(self.pin_motor_left, speed)  # Envois de la nouvelle vitesse au moteur
        if side is Controller.POS_RIGHT:
            self.motor.set_PWM_dutycycle(self.pin_motor_right, speed)  # Envois de la nouvelle vitesse au moteur

    def use_servo(self, servo, value, stop=False):
        if stop:
            value = 0

        if servo is Controller.SERVO_ARM_1:
            value = (int(((bras1_servo_cal_m * value) + bras1_servo_cal_x1) / 10) * 10) if value else 0
            self.motor.set_servo_pulsewidth(self.pin_arm_1, value)

        if servo is Controller.SERVO_ARM_2:
            value = (int(((bras2_servo_cal_m * value) + bras2_servo_cal_x1) / 10) * 10) if value else 0
            self.motor.set_servo_pulsewidth(self.pin_arm_2, value)

        if servo is Controller.SERVO_CLAMP:
            value = (int(((pince_servo_cal_m * value) + pince_servo_cal_x1) / 10) * 10) if value else 0
            self.motor.set_servo_pulsewidth(self.pin_clamp, value)

    def echo_callback(self, cb):
        return self.motor.callback(self.pin_echo, pigpio.EITHER_EDGE, cb)

    def activate_trigger(self, duration=10):
        self.motor.gpio_trigger(self.pin_trigger, duration, 1)  # impulsion de 10us pour déclencher la mesure (Front haut)

    def switch_trigger(self, mode):
        value = int(bool(mode))
        self.motor.write(self.pin_trigger, value)

    def get_current_tick(self):
        return self.motor.get_current_tick()


class Robotkiller(object):

    def __init__(self):
        self.controller = Controller()
        self.left = Caterpillar(self.controller, Controller.POS_LEFT)
        self.right = Caterpillar(self.controller, Controller.POS_RIGHT)
        self.pince = ServoMotor(self.controller, Controller.SERVO_CLAMP, pince_angle_inc, pince_angle_min, pince_angle_max, pince_angle)
        self.arm = Arm(self.controller)
        self.eyes = Distance(self.controller)
        # self.button = PushButton(pin_bp)


#############################################################################################
#                                  Class privées                                            #
#############################################################################################

class Caterpillar(object):
    MOTOR_STOP = 0
    MOTOR_FORWARD = 1
    MOTOR_BACKWARD = -1

    def __init__(self, controller, side):
        self.controller = controller
        self.side = side
        self.last_direction = 0                              # Dernier sens de rotation du moteur / False = Arrière / True = Avancer
        self.last_speed = 0
        self.acceleration_inc = max_speed_inc                   # Incrément de l'accélération (par défaut 3)
        self.acceleration_dec = max_speed_dec                   # Incrément de l'accélération (par défaut 3)
        self.speed = 0                                          # vitesse courante de la chenille
        self.max_speed = 200
        self.min_speed = 50

    def running(self, move_direction, *args, **kwargs):
        min_speed = kwargs.get('min_speed', self.min_speed)
        max_speed = kwargs.get('max_speed', self.max_speed)

        # Arret d'urgence
        if (move_direction == Caterpillar.MOTOR_STOP) or (not move_direction == self.last_direction):
            self.speed = 0
            self.controller.switch_led_front(self.side, 0)
            self.controller.switch_led_back(self.side, 0)

        # Marche avant
        if move_direction == Caterpillar.MOTOR_FORWARD and self.speed > 0:
            self.controller.switch_led_front(self.side, 1)
            self.controller.switch_motor_direction(self.side, Controller.MOTOR_FORWARD)

        # Marche arrière
        if move_direction == Caterpillar.MOTOR_BACKWARD and self.speed > 0:
            self.controller.switch_led_back(self.side, 1)
            self.controller.switch_motor_direction(self.side, Controller.MOTOR_BACKWARD)

        if move_direction == Caterpillar.MOTOR_FORWARD or move_direction == Caterpillar.MOTOR_BACKWARD:
            self.speed = min_speed if COLLISION else max_speed
        elif move_direction == Caterpillar.MOTOR_STOP and self.speed > 0:
            self.speed = max(self.speed - self.acceleration_dec, 0)

        if not self.last_speed == self.speed or not self.last_direction == move_direction:
            self.controller.use_motor(self.side, self.speed)  # Envois de la nouvelle vitesse au moteur

        self.last_direction = move_direction
        self.last_speed = self.speed

        
class Distance(object):
    def __init__(self, controller):
        self.measure_distance = 0

        self.controller = controller

        self.controller.switch_trigger(0)  # On passe le trigger à Low
        time.sleep(0.5)  # On attend que le module à ultrason s'inititalise la première fois (sinon ca bug)
        self.toolong = 10000  # temps maxi de la mesure en ms
        self.high_tick = None
        self.echo_time = self.toolong
        self.echo_tick = self.controller.get_current_tick()  # valeur du temps CPU en µs
        self.cb = self.controller.echo_callback(self._cbf)

    def _cbf(self, gpio, level, tick):
        # Measure de l'interval de temps (en tick) : echo_time
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
        global COLLISION
        # Measure de la distance
        self.controller.activate_trigger(10)  # impulsion de 10us pour déclencher la mesure (Front haut)
        time.sleep(0.00001)
        # La distance parcourue pendant ce temps = le temps X la vitesse du son (cm/s)
        distance = self.echo_time / 1000000.0 * speedSound
        # C'était la distance aller et retour donc on divise la valeur par 2
        self.measure_distance = distance / 2

        # Calcul du risque de collision nécessitant de passer en vitesse réduite
        COLLISION = bool(self.measure_distance < slow_distance)
        # On retourne la mesure de distance au Prog principal pour affichage sur l'IHM        
        return self.measure_distance


class ServoMotor(object):
    def __init__(self, controller, servo_id, angle_inc, angle_min, angle_max, angle):
        self.angle_inc = angle_inc
        self.angle_min = angle_min
        self.angle_max = angle_max
        self.angle_move = angle
        self.angle_init = angle

        self.servo_id = servo_id

        self.controller = controller

    def arret(self):
        self.controller.use_servo(self.servo_id, 0, True)
        time.sleep(0.5)                     # pour que le servo ait le temps de revenir en possition de départ

    def work(self, way_left, way_right):
        if (way_left is True) and (way_right is False):
            self.angle_move = self.angle_move - self.angle_inc
            if self.angle_move < self.angle_min:
                self.angle_move = self.angle_min    

        elif (way_left is False) and (way_right is True):
            self.angle_move = self.angle_move + self.angle_inc
            if self.angle_move > self.angle_max:
                self.angle_move = self.angle_max 

        self.controller.use_servo(self.servo_id, self.angle_move)


class Arm(object):
    def __init__(self, controller):
        self.arm_up = False
        self.arm_down = False
        self.controller = controller
        self.bras1 = ServoMotor(controller, Controller.SERVO_ARM_1, bras1_angle_inc, bras1_angle_min, bras1_angle_max, bras1_angle)
        self.bras2 = ServoMotor(controller, Controller.SERVO_ARM_2, bras2_angle_inc, bras2_angle_min, bras2_angle_max, bras2_angle)

    def work(self, arm_up, arm_down):

        if (arm_up is True) and (arm_down is False):
            self.bras1.work(True, False)
            self.bras2.work(False, True)

        elif (arm_up is False) and (arm_down is True):
            self.bras1.work(False, True)
            self.bras2.work(True, False)

    def arret(self):
        self.bras1.arret()
        self.bras2.arret()
