import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize

import paho.mqtt.client as mqtt


def on_connect(mqttc, userdata, rc, t):
    print('connected...rc=' + str(rc))
    mqttc.publish(topic='device/sensor/temperature',
                  payload='80', qos=0)


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
    KEYS = {
        QtCore.Qt.Key_Up: ["UP Key", 0, (1, 1)],
        QtCore.Qt.Key_Down: ["Down Key", 0, (2, 1)],
        QtCore.Qt.Key_Left: ["Left Key", 0, (3, 1)],
        QtCore.Qt.Key_Right: ["Right Key", 0, (4, 1)],
        QtCore.Qt.Key_D: ["D Key", 0, (5, 1)],
        QtCore.Qt.Key_A: ["A Key", 0, (6, 1)],
    }

    def __init__(self):
        QMainWindow.__init__(self)

        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = on_connect
        self.mqttc.on_disconnect = on_disconnect
        self.mqttc.on_publish = on_publish
        self.mqttc.connect(host='localhost', port=1883)
        self.mqttc.loop_start()

        self.setMinimumSize(QSize(640, 640))
        self.setWindowTitle("Hello world")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setSpacing(1)
        centralWidget.setLayout(self.gridLayout)

        for key in self.KEYS:
            title = QLabel("{} is {}".format(self.KEYS[key][0], "active" if self.KEYS[key][1] else "disabled"), self)
            title.setAlignment(QtCore.Qt.AlignCenter)
            title.setContentsMargins(0, 0, 0, 0)
            title.setStyleSheet('QLabel {background-color: white; color: red; font-size: 24px; font-weight: bold}')
            posA, posB = self.KEYS[key][2]
            self.gridLayout.addWidget(title, posA, posB)

    def enterEvent(self, event):
        print("Enter event")

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

        if event.key() in self.KEYS:
            self.KEYS[event.key()][1] = 1
            self._update_widgetText(event.key())

    def keyReleaseEvent(self, event):
        if event.key() in self.KEYS:
            self.KEYS[event.key()][1] = 0
            self._update_widgetText(event.key())

    def _update_widgetText(self, keyEvent):
        posA, posB = self.KEYS[keyEvent][2]
        title = "{} is {}".format(self.KEYS[keyEvent][0], "active" if self.KEYS[keyEvent][1] else "disabled")
        item = self.gridLayout.itemAtPosition(posA, posB)
        w = item.widget()
        w.setText(title)
        self.mqttc.publish('robot', title, 1)

    def closeEvent(self, event):
        print("Closing App")
        self.mqttc.disconnect()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit(app.exec_())
