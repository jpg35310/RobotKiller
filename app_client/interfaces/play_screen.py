import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication)


class PlayScreen(QWidget):

    def __init__(self):
        super(PlayScreen, self).__init__()
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.setWindowTitle('Robot Killer App')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlayScreen()
    sys.exit(app.exec_())