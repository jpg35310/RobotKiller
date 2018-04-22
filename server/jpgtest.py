#!/usr/bin/python
# -*- coding: utf-8 -*-
#
from helpers import print_exception # là, il y a un truc qui merde / a voir plus tard / déplacer dans racine
import os                # Fonction du système d'exploitation
import time              # bibliothèque pour gestion du temps
from RkClassesHardware import Robotkiller


speed_game = 0.03   # soit 30ms ce qui est le temps de la boucle des commandes vers le robot
game_time = 5		# temps de jeu en secondes
prog_main = True


slow_distance = 15	# Si obstacle à moins de 15cm, les moteurs passent en vitesse réduite 
mesure_distance = slow_distance

os.system("clear") 

# Initialisation des class
robotkiller = Robotkiller()


# Le programme principal
while prog_main :
	print("\n+---------------/ RobotKiller /---------------+")
	print("|                                               |")
	print("| Maquette d'essai pour test des commandes      |")
	print("|                                               |")
	print("+-----------------------------------------------+\n")
	print("Choix du programme de test ?")
	choix = input("0. Chenille avance\n1. Chenille recule\n2. Chenille ralentir en avancant\n\
3. Chenille ralentir en reculant\n4. Chenille stop\n\
5. Bras monté\n6. Bras descendre\n\
7. Ouvrir pince\n8. Fermer pince\n\
9. Test de la mort qui tue !\n\
10. Sortie programme\nChoix: ")

	if choix == 0 :
		print("Chenille avance")
		print("tempo 5 secondes ")
		prog_game = True
		count_time = 0
		while prog_game :
			count_time = count_time + speed_game
			if count_time > game_time :
				prog_game = False
			time.sleep(speed_game) # Pour gérer la vitesse de la boucle while      
			#robotkiller.right.running(max_speed,acceleration,forward,stopping)
			robotkiller.right.running(100,True,True,False)
			robotkiller.left.running(100,True,True,False)
			mesure_distance = robotkiller.eyes.measured(slow_distance)
			print("Distance Prog: {0:5.1f}".format(mesure_distance))

			
	if choix == 1 :
		print("Chenille recule")
		print("tempo 5 secondes ")
		prog_game = True
		count_time = 0
		while prog_game :
			count_time = count_time + speed_game
			if count_time > game_time :
				prog_game = False
			time.sleep(speed_game) # Pour gérer la vitesse de la boucle while      
			#robotkiller.right.running(max_speed,acceleration,forward,stopping)
			robotkiller.right.running(100,True,False,False)
			robotkiller.left.running(100,True,False,False)

	if choix == 2 :
		print("Chenille ralentir en avancant")
		print("tempo 5 secondes ")
		prog_game = True
		count_time = 0
		while prog_game :
			count_time = count_time + speed_game
			if count_time > game_time :
				prog_game = False
			time.sleep(speed_game) # Pour gérer la vitesse de la boucle while      
			#robotkiller.right.running(max_speed,acceleration,forward,stopping)
			robotkiller.right.running(100,False,True,False)
			robotkiller.left.running(100,False,True,False)

	if choix == 3 :
		print("Chenille ralentir en reculant")
		print("tempo 5 secondes ")
		prog_game = True
		count_time = 0
		while prog_game :
			count_time = count_time + speed_game
			if count_time > game_time :
				prog_game = False
			time.sleep(speed_game) # Pour gérer la vitesse de la boucle while      
			#robotkiller.right.running(max_speed,acceleration,forward,stopping)
			robotkiller.right.running(100,False,False,False)
			robotkiller.left.running(100,False,False,False)

	if choix == 4 :
		print("Chenille stop")
		#robotkiller.right.running(max_speed,acceleration,forward,stopping)
		robotkiller.right.running(100,True,True,True)
		robotkiller.left.running(100,False,False,True)

	if choix == 5 :
		print("Bras monté")
		#robotkiller.arm.work(up,down)
		robotkiller.arm.work(True,False)

	if choix == 6 :
		print("Bras descendre")
		#robotkiller.arm.work(up,down)
		robotkiller.arm.work(False,True)

	if choix == 7 :
		print("Ouvrir pince")
		#robotkiller.pince.work(open,close)
		robotkiller.pince.work(True,False)

	if choix == 8 :
		print("Fermer pince")
		#robotkiller.pince.work(open,close)
		robotkiller.pince.work(False,True)

	if choix == 9 :
		print("Test de la mort qui tue !")


	# Sortie propre du programme
	if choix == 10 :
		print("Fin du programme")
		prog_main = False


