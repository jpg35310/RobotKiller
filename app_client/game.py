import sys
import json
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow
# from PyQt5.QtWidgets import Q, QLabel, QGridLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import QSize

import paho.mqtt.client as mqtt

from interfaces.MainAppUi import Ui_MainWindow

#############################################################################################
#                                Initialisation des constantes                              #
#############################################################################################
mqtt_host = 'localhost'
mqtt_port = 1883
mqtt_subscribe = 'robot'

MOVE_FORWARD = ['move_forward', QtCore.Qt.Key_Up]
MOVE_BACKWARD = ['move_back', QtCore.Qt.Key_Down]
MOVE_LEFT = ['move_left', QtCore.Qt.Key_Left]
MOVE_RIGHT = ['move_right', QtCore.Qt.Key_Right]
ARM_UP = ['arm_up', QtCore.Qt.Key_W]
ARM_DOWN = ['arm_down', QtCore.Qt.Key_S]

INIT_ROBOT_STATUS = {
    MOVE_FORWARD[0]: False,
    MOVE_BACKWARD[0]: False,
    MOVE_LEFT[0]: False,
    MOVE_RIGHT[0]: False,
    ARM_UP[0]: False,
    ARM_DOWN[0]: False
}

# sur la base du dico ci-dessus, il faut modifier l'intégralité du code pour 
# fonctionner de la manière suivante :
# INIT_ROBOT_STATUS = {
#     MOVE_FORWARD_LEFT[0]: False,
#     MOVE_BACKWARD_LEFT[0]: False,
#     MOVE_FORWARD_RIGHT[0]: False,
#     MOVE_BACKWARD_RIGHT[0]: False,
#     ARM_UP[0]: False,
#     ARM_DOWN[0]: False,
#     CLAMP_OPEN[0]: False,
#     CLAMP_CLOSE[0]: False,
#     MAX_SPEED[0]: valeur numérique de 1 à 1000
#     MIN_SPEED[0]: valeur numérique de 1 à 1000
#     COLLISION[0]: valeur numérique de 1 à 1000
# }

# De plus le server_robot.py va renvoyer l'information de distance (MESURE) que ce programme
# devra afficher dans l'interface graphique.

# Et pour finir il faudra modifier l'interface graphique
# J'ai rajouté une image qui décrit l'interface

def on_connect(mqttc, userdata, rc, t):
    print('connected...rc=' + str(rc))
    # A mon avis les commandes ci-dessous sont à supprimer
    #  mqttc.publish(topic='device/sensor/temperature',
    #               payload='80', qos=0)


def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))


def on_publish(mqttc, userdata, mid):
    print('message published')
    # mqttc.disconnect()


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class HelloWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.ROBOT_STATUS = self.init_robot_status()

        self.KEYS = {
            MOVE_FORWARD[1]: {
                'function': self.send_to_robot,
                'action': MOVE_FORWARD[0],
                'button_name': 'mvForwardButton',
                'button': None,
                'restrict_with': [MOVE_BACKWARD[0]]
            },
            MOVE_BACKWARD[1]: {
                'function': self.send_to_robot,
                'action': MOVE_BACKWARD[0],
                'button_name': 'mvBackButton',
                'button': None,
                'restrict_with': [MOVE_FORWARD[0]]
            },
            MOVE_LEFT[1]: {
                'function': self.send_to_robot,
                'action': MOVE_LEFT[0],
                'button_name': 'mvLeftButton',
                'button': None,
                'restrict_with': [MOVE_RIGHT[0]]
            },
            MOVE_RIGHT[1]: {
                'function': self.send_to_robot,
                'action': MOVE_RIGHT[0],
                'button_name': 'mvRightButton',
                'button': None,
                'restrict_with': [MOVE_LEFT[0]]
            },
            ARM_UP[1]: {
                'function': self.send_to_robot,
                'action': ARM_UP[0],
                'button_name': 'chFwButton',
                'button': None,
                'restrict_with': [ARM_DOWN[0]]
            },
            ARM_DOWN[1]: {
                'function': self.send_to_robot,
                'action': ARM_DOWN[0],
                'button_name': 'chBackButton',
                'button': None,
                'restrict_with': [ARM_UP[0]]
            },
        }

        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = on_connect
        self.mqttc.on_disconnect = on_disconnect
        self.mqttc.on_publish = on_publish
        self.mqttc.connect(host=mqtt_host, port=mqtt_port)
        self.mqttc.loop_start()

        self.grabKeyboard()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.game_started = False
        self.init_timer()
        self.ui.startGameButton.clicked.connect(self.startTimer)

        self.prepare_navigation_buttons()

        self.show()

    @staticmethod
    def init_robot_status():
        return INIT_ROBOT_STATUS.copy()

    def send_to_robot(self, active, call_action, button=None, restricted_with=[]):

        if len(restricted_with) and any(self.ROBOT_STATUS[a] is True for a in restricted_with) or not self.game_started:
            if button.isChecked():
                button.toggle()
            return

        if button:
            if button.isChecked() is not active:
                button.toggle()

        if not self.ROBOT_STATUS[call_action] == active:
            self.ROBOT_STATUS[call_action] = active
            self.send_robot_status()

    def send_robot_status(self):
        self.mqttc.publish(mqtt_subscribe, json.dumps(self.ROBOT_STATUS), 1)

    def prepare_navigation_buttons(self):
        def btn_click(btn, action):
            action['function'](btn.isChecked(), action['action'], btn, action['restrict_with'])

        # /********** Forward Button ********/
        self.ui.mvForwardButton.setCheckable(True)
        self.ui.mvForwardButton.clicked.connect(lambda: btn_click(self.ui.mvForwardButton, self.KEYS[MOVE_FORWARD[1]]))
        self.KEYS[MOVE_FORWARD[1]]['button'] = self.ui.mvForwardButton

        # /********** Backward Button ********/
        self.ui.mvBackButton.setCheckable(True)
        self.ui.mvBackButton.clicked.connect(lambda: btn_click(self.ui.mvBackButton, self.KEYS[MOVE_BACKWARD[1]]))
        self.KEYS[MOVE_BACKWARD[1]]['button'] = self.ui.mvBackButton

        # /********** Turn Left Button ********/
        self.ui.mvLeftButton.setCheckable(True)
        self.ui.mvLeftButton.clicked.connect(lambda: btn_click(self.ui.mvLeftButton, self.KEYS[MOVE_LEFT[1]]))
        self.KEYS[MOVE_LEFT[1]]['button'] = self.ui.mvLeftButton

        # /********** Turn Right Button ********/
        self.ui.mvRightButton.setCheckable(True)
        self.ui.mvRightButton.clicked.connect(lambda: btn_click(self.ui.mvRightButton, self.KEYS[MOVE_RIGHT[1]]))
        self.KEYS[MOVE_RIGHT[1]]['button'] = self.ui.mvRightButton

        # /********** Lift Arm Up Button ********/
        self.ui.chFwButton.setCheckable(True)
        self.ui.chFwButton.clicked.connect(lambda: btn_click(self.ui.chFwButton, self.KEYS[ARM_UP[1]]))
        self.KEYS[ARM_UP[1]]['button'] = self.ui.chFwButton

        # /********** Lift Arm Down Button ********/
        self.ui.chBackButton.setCheckable(True)
        self.ui.chBackButton.clicked.connect(lambda: btn_click(self.ui.chBackButton, self.KEYS[ARM_DOWN[1]]))
        self.KEYS[ARM_DOWN[1]]['button'] = self.ui.chBackButton

    def init_timer(self):
        self.game_round = 120

        self.game_time = QtCore.QTime(0, 0, 30)
        self.ui.timeLeftLcd.display(self.game_time.toString('mm:ss'))

        self.game_timer = QtCore.QTimer()
        self.game_timer.timeout.connect(self.timerEvent)

    def startTimer(self):
        try:
            self.game_timer.start(1000) # Timer du jeu en ms
            self.game_started = True
        except Exception as e:
            print("Exception:", e)

    def timerEvent(self):
        t = self.game_time.addSecs(-1)
        self.ui.timeLeftLcd.display(t.toString('mm:ss'))
        self.game_time = t
        if not t.minute() and not t.second():
            self.stop_game()

    def stop_game(self):
        self.ROBOT_STATUS = self.init_robot_status()
        self.send_robot_status()
        self.game_started = False
        self.init_timer()

    def enterEvent(self, event):
        print("Enter event")

    def keyPressEvent(self, event):

        # if event.key() == QtCore.Qt.Key_Escape:
        #     self.close()

        if event.key() in self.KEYS and not event.isAutoRepeat():
            key = self.KEYS[event.key()]
            key['function'](True, key['action'], key['button'], key['restrict_with'])

    def keyReleaseEvent(self, event):
        if event.key() in self.KEYS:
            key = self.KEYS[event.key()]
            key['function'](False, key['action'], key['button'])

    def closeEvent(self, event):
        print("Closing App")
        if self.game_started:
            self.stop_game()
        self.mqttc.disconnect()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    sys.exit(app.exec_())
