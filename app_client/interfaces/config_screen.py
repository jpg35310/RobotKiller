from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QWidget, QLCDNumber


class ConfigurationPanel(QWidget):

    def __init__(self):
        super(ConfigurationPanel, self).__init__()
        self.timer = None

        self.init_layout()

    def init_layout(self):
        self.timer = QLCDNumber()
        self.timer.display(200)

        layout = QHBoxLayout(self)
        layout.addWidget(self.timer)

        self.setLayout(layout)
