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
mqtt_host = '192.168.0.43'
mqtt_port = 1883
mqtt_subscribe = 'robot'

MOVE_FORWARD_LEFT = ['move_forward_left', QtCore.Qt.Key_Shift]
MOVE_BACKWARD_LEFT = ['move_backward_left', QtCore.Qt.Key_Control]
MOVE_FORWARD_RIGHT = ['move_forward_right', QtCore.Qt.Key_Shift]
MOVE_BACKWARD_RIGHT = ['move_backward_right', QtCore.Qt.Key_Control]
ARM_UP = ['arm_up', QtCore.Qt.Key_Up]
ARM_DOWN = ['arm_up', QtCore.Qt.Key_Down]
CLAMP_OPEN = ['clamp_open', QtCore.Qt.Key_Left]
CLAMP_CLOSE = ['clamp_close', QtCore.Qt.Key_Right]

INIT_ROBOT_STATUS = {
    MOVE_FORWARD_LEFT[0]: False,
    MOVE_BACKWARD_LEFT[0]: False,
    MOVE_FORWARD_RIGHT[0]: False,
    MOVE_BACKWARD_RIGHT[0]: False,
    ARM_UP[0]: False,
    ARM_DOWN[0]: False,
    CLAMP_OPEN[0]: False,
    CLAMP_CLOSE[0]: False,
    'min_speed': 50,
    'max_speed': 100,
    'distance': 10,
    'working': False
}

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
            MOVE_FORWARD_LEFT[1]: {
                'function': self.send_to_robot,
                'action': MOVE_FORWARD_LEFT[0],
                'button_name': '﻿chLeftFwButton',
                'button': None,
                'restrict_with': [ARM_UP[0], ARM_DOWN[0]]
            },
            MOVE_BACKWARD_LEFT[1]: {
                'function': self.send_to_robot,
                'action': MOVE_BACKWARD_LEFT[0],
                'button_name': '﻿chLeftBackButton',
                'button': None,
                'restrict_with': [ARM_UP[0], ARM_DOWN[0]]
            },
            MOVE_FORWARD_RIGHT[1]: {
                'function': self.send_to_robot,
                'action': MOVE_FORWARD_RIGHT[0],
                'button_name': '﻿chRightFwButton',
                'button': None,
                'restrict_with': [ARM_UP[0], ARM_DOWN[0]]
            },
            MOVE_BACKWARD_RIGHT[1]: {
                'function': self.send_to_robot,
                'action': MOVE_BACKWARD_RIGHT[0],
                'button_name': '﻿chRightBackButton',
                'button': None,
                'restrict_with': [ARM_UP[0], ARM_DOWN[0]]
            },
            ARM_UP[1]: {
                'function': self.send_to_robot,
                'action': ARM_UP[0],
                'button_name': '﻿armUpButton',
                'button': None,
                'restrict_with': []
            },
            ARM_DOWN[1]: {
                'function': self.send_to_robot,
                'action': ARM_DOWN[0],
                'button_name': '﻿armDownButton',
                'button': None,
                'restrict_with': []
            },
            CLAMP_OPEN[1]: {
                'function': self.send_to_robot,
                'action': CLAMP_OPEN[0],
                'button_name': '﻿clampOpenButton',
                'button': None,
                'restrict_with': []
            },
            CLAMP_CLOSE[1]: {
                'function': self.send_to_robot,
                'action': CLAMP_CLOSE[0],
                'button_name': '﻿clampCloseButton',
                'button': None,
                'restrict_with': []
            },
        }

        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = on_connect
        self.mqttc.on_disconnect = on_disconnect
        self.mqttc.on_publish = on_publish
        self.mqttc.on_message = self.on_message
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

    def on_message(self, mqttc, userdata, msg):
        message = json.loads(msg.payload)
        if 'collision' in message:
            self.update_distance_lcd(message['collision'])

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

        # /********** LEFT Forward Button ********/
        self.ui.chLeftFwButton.setCheckable(True)
        self.ui.chLeftFwButton.clicked.connect(lambda: btn_click(self.ui.chLeftFwButton, self.KEYS[MOVE_FORWARD_LEFT[1]]))
        self.KEYS[MOVE_FORWARD_LEFT[1]]['button'] = self.ui.chLeftFwButton

        # /********** RIGHT Forward Button ********/
        self.ui.chRightFwButton.setCheckable(True)
        self.ui.chRightFwButton.clicked.connect(
            lambda: btn_click(self.ui.chRightFwButton, self.KEYS[MOVE_FORWARD_RIGHT[1]]))
        self.KEYS[MOVE_FORWARD_RIGHT[1]]['button'] = self.ui.chRightFwButton

        # /********** LEFT Backward Button ********/
        self.ui.chLeftBackButton.setCheckable(True)
        self.ui.chLeftBackButton.clicked.connect(lambda: btn_click(self.ui.chLeftBackButton, self.KEYS[MOVE_BACKWARD_LEFT[1]]))
        self.KEYS[MOVE_BACKWARD_LEFT[1]]['button'] = self.ui.chLeftBackButton

        # /********** RIGHT Backward Button ********/
        self.ui.chRightBackButton.setCheckable(True)
        self.ui.chRightBackButton.clicked.connect(lambda: btn_click(self.ui.chRightBackButton, self.KEYS[MOVE_BACKWARD_RIGHT[1]]))
        self.KEYS[MOVE_BACKWARD_RIGHT[1]]['button'] = self.ui.chRightBackButton

        # /********** Lift Arm Up Button ********/
        self.ui.armUpButton.setCheckable(True)
        self.ui.armUpButton.clicked.connect(lambda: btn_click(self.ui.armUpButton, self.KEYS[ARM_UP[1]]))
        self.KEYS[ARM_UP[1]]['button'] = self.ui.armUpButton

        # /********** Lift Arm Down Button ********/
        self.ui.armDownButton.setCheckable(True)
        self.ui.armDownButton.clicked.connect(lambda: btn_click(self.ui.armDownButton, self.KEYS[ARM_DOWN[1]]))
        self.KEYS[ARM_DOWN[1]]['button'] = self.ui.armDownButton

        # /********** CLAMP Open Button ********/
        self.ui.clampOpenButton.setCheckable(True)
        self.ui.clampOpenButton.clicked.connect(lambda: btn_click(self.ui.clampOpenButton, self.KEYS[CLAMP_OPEN[1]]))
        self.KEYS[CLAMP_OPEN[1]]['button'] = self.ui.clampOpenButton

        # /********** CLAMP Open Button ********/
        self.ui.clampCloseButton.setCheckable(True)
        self.ui.clampCloseButton.clicked.connect(lambda: btn_click(self.ui.clampCloseButton, self.KEYS[CLAMP_CLOSE[1]]))
        self.KEYS[CLAMP_CLOSE[1]]['button'] = self.ui.clampCloseButton

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
            self.ROBOT_STATUS['working'] = self.game_started
        except Exception as e:
            print("Exception:", e)

    def timerEvent(self):
        t = self.game_time.addSecs(-1)
        self.ui.timeLeftLcd.display(t.toString('mm:ss'))
        self.game_time = t
        if not t.minute() and not t.second():
            self.stop_game()

    def update_distance_lcd(self, distance):
        self.ui.distanceLcd.display('{0}'.format(distance))

    def stop_game(self):
        self.ROBOT_STATUS = self.init_robot_status()
        self.ROBOT_STATUS['working'] = True
        self.send_robot_status()
        self.ROBOT_STATUS['working'] = False
        self.send_robot_status()
        self.game_started = False
        self.init_timer()

    def enterEvent(self, event):
        print("Enter event")

    def keyPressEvent(self, event):
        print('Key', event.text(), 'Code', event.key())
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
    mainWin.show()
    sys.exit(app.exec_())
