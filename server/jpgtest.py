#!/usr/bin/python
# -*- coding: utf-8 -*-
#
import os                # Fonction du système d'exploitation
import time              # bibliothèque pour gestion du temps
from RkClassesHardware import io_init
from RkClassesHardware import Caterpillars
from RkClassesHardware import acceleration
from RkClassesHardware import ServoMotors
from RkClassesHardware import chg_angle


game_time = 10	# temps de jeu en secondes
prog_main = True

pince_angle = 90
bras1_angle = 50
bras2_angle = 70

os.system("clear") 

# Initialisation des class

io_init()
caterpillar = Caterpillars()
servomotor = ServoMotors()

# Un petit mouvement du bras pour monter qu'il est en vie !!!
servomotor.bras1.angle(bras1_angle)
servomotor.bras2.angle(bras2_angle)
servomotor.pince.angle(pince_angle)
time.sleep(2)


# Le programme principal
while prog_main :
	print("\n+---------------/ RobotKiller /---------------+")
	print("|                                               |")
	print("| Maquette d'essai pour test des commandes      |")
	print("|                                               |")
	print("+-----------------------------------------------+\n")
	print("Choix du programme de test ?")
	choix = input("1. Test Chenille\n2. Test bras\n3. none\n4. none\n5. Sortie programme\nChoix: ")

	if choix == 1 :
		print("Test Chenille ")
		prog_game = True
		count_time = 0

		speed_caterpillar_right = 1			# Vitesse de la chenille de -MAXSPEED à 0 à +MAXSPEED / faut mettre 1 ou -1 pour demarrer
		auto_caterpillar_right = 1			#  1 = Accélération jusqu'a MAXSPEED / 0 = Relentissement jusqu'a 0 

		speed_caterpillar_left = 1
		auto_caterpillar_left = 1

		while prog_game :
			count_time = count_time + 0.02
			if count_time > game_time :
				prog_game = False
			time.sleep(0.02) # Pour gérer la vitesse de la boucle while      
			print(speed_caterpillar_right)
			print(speed_caterpillar_left)
			speed_caterpillar_right=acceleration(speed_caterpillar_right, auto_caterpillar_right)
			caterpillar.right.setspeed(speed_caterpillar_right)
			speed_caterpillar_left=acceleration(speed_caterpillar_left, auto_caterpillar_left)
			caterpillar.left.setspeed(speed_caterpillar_left)
		# Arret des chenilles
		caterpillar.right.setspeed(0)
		caterpillar.left.setspeed(0)	

	if choix == 2 :
		print("Test du bras")
	# 	pince_angle = 1 
	# #	bras1_angle = 10 
	# #	bras2_angle = 90
	# 	servomotor.bras1.angle(bras1_angle)
	# 	servomotor.bras2.angle(bras2_angle)
	# 	servomotor.pince.angle(pince_angle)
	# 	while var < 15: # Repeter 10 fois
	# 		auto_bras1 = True
	# 		bras1_way = True
	# 		auto_bras2 = True
	# 		bras2_way = False
	# 		bras1_angle = chg_angle(bras1_angle, 1, bras1_angle_min, bras1_angle_max, auto_bras1, bras1_way)
	# 		bras2_angle = chg_angle(bras2_angle, 1, bras2_angle_min, bras2_angle_max, auto_bras2, bras2_way)
	# 		servomotor.bras1.angle(bras1_angle)
	# 		servomotor.bras2.angle(bras2_angle)
	# 		time.sleep(0.25)
	# 		var = var + 1
	# 		print(var)
	# 	auto_bras1 = False
	# 	auto_bras2 = False
	# 	time.sleep(2)

	if choix == 3 :
		print("Test N°3 ")

	if choix == 4 :
		print("Test du moteur PWM ")

	# Sortie propre du programme
	if choix == 5 :
		print("Fin du programme")
		prog_main = False

pince_angle = 1 
bras1_angle = 15 # à 10 ca force et l'intensité augmente à 500 mA au lieu de 200mA 
bras2_angle = 90
speed_caterpillar_left = 0
speed_caterpillar_right = 0      
caterpillar.left.setspeed(speed_caterpillar_left)
caterpillar.right.setspeed(speed_caterpillar_right)
servomotor.bras1.angle(bras1_angle)
servomotor.bras2.angle(bras2_angle)
servomotor.pince.angle(pince_angle)
time.sleep(1)
servomotor.bras1.stop()
servomotor.bras2.stop()
servomotor.pince.stop()
GPIO.cleanup()
PWM.cleanup()
