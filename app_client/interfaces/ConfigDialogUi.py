# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configuration.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Configuration(object):
    def setupUi(self, Configuration):
        Configuration.setObjectName("Configuration")
        Configuration.setWindowModality(QtCore.Qt.WindowModal)
        Configuration.resize(518, 347)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        Configuration.setFont(font)
        Configuration.setLocale(QtCore.QLocale(QtCore.QLocale.French, QtCore.QLocale.France))
        Configuration.setSizeGripEnabled(False)
        Configuration.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(Configuration)
        self.buttonBox.setGeometry(QtCore.QRect(10, 310, 501, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Configuration)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 501, 281))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 7)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.robotIp = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.robotIp.setFont(font)
        self.robotIp.setObjectName("robotIp")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.robotIp)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.playTime = QtWidgets.QSpinBox(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.playTime.setFont(font)
        self.playTime.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.playTime.setMinimum(1)
        self.playTime.setMaximum(9999)
        self.playTime.setSingleStep(5)
        self.playTime.setObjectName("playTime")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.playTime)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.chSpeed = QtWidgets.QSlider(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chSpeed.sizePolicy().hasHeightForWidth())
        self.chSpeed.setSizePolicy(sizePolicy)
        self.chSpeed.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.chSpeed.setMouseTracking(True)
        self.chSpeed.setMaximum(100)
        self.chSpeed.setProperty("value", 7)
        self.chSpeed.setOrientation(QtCore.Qt.Horizontal)
        self.chSpeed.setInvertedAppearance(False)
        self.chSpeed.setInvertedControls(False)
        self.chSpeed.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.chSpeed.setTickInterval(10)
        self.chSpeed.setObjectName("chSpeed")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.chSpeed)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.chSpeedCollision = QtWidgets.QSlider(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chSpeedCollision.sizePolicy().hasHeightForWidth())
        self.chSpeedCollision.setSizePolicy(sizePolicy)
        self.chSpeedCollision.setAcceptDrops(True)
        self.chSpeedCollision.setStatusTip("")
        self.chSpeedCollision.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly|QtCore.Qt.ImhLowercaseOnly|QtCore.Qt.ImhSensitiveData)
        self.chSpeedCollision.setMaximum(100)
        self.chSpeedCollision.setOrientation(QtCore.Qt.Horizontal)
        self.chSpeedCollision.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.chSpeedCollision.setTickInterval(10)
        self.chSpeedCollision.setObjectName("chSpeedCollision")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.chSpeedCollision)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.collisionDistance = QtWidgets.QSpinBox(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.collisionDistance.setFont(font)
        self.collisionDistance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.collisionDistance.setSuffix("")
        self.collisionDistance.setMinimum(1)
        self.collisionDistance.setMaximum(9999)
        self.collisionDistance.setSingleStep(5)
        self.collisionDistance.setObjectName("collisionDistance")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.collisionDistance)
        self.chSpeedCollisionValue = QtWidgets.QSpinBox(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chSpeedCollisionValue.sizePolicy().hasHeightForWidth())
        self.chSpeedCollisionValue.setSizePolicy(sizePolicy)
        self.chSpeedCollisionValue.setWrapping(True)
        self.chSpeedCollisionValue.setFrame(True)
        self.chSpeedCollisionValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.chSpeedCollisionValue.setReadOnly(False)
        self.chSpeedCollisionValue.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.chSpeedCollisionValue.setMaximum(100)
        self.chSpeedCollisionValue.setObjectName("chSpeedCollisionValue")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.chSpeedCollisionValue)
        self.chSpeedValue = QtWidgets.QSpinBox(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chSpeedValue.sizePolicy().hasHeightForWidth())
        self.chSpeedValue.setSizePolicy(sizePolicy)
        self.chSpeedValue.setWrapping(True)
        self.chSpeedValue.setFrame(True)
        self.chSpeedValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.chSpeedValue.setReadOnly(False)
        self.chSpeedValue.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.chSpeedValue.setMaximum(100)
        self.chSpeedValue.setObjectName("chSpeedValue")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.chSpeedValue)

        self.retranslateUi(Configuration)
        self.buttonBox.accepted.connect(Configuration.accept)
        self.buttonBox.rejected.connect(Configuration.reject)
        self.buttonBox.rejected.connect(Configuration.close)
        self.chSpeedCollision.valueChanged['int'].connect(self.chSpeedCollisionValue.setValue)
        self.chSpeed.valueChanged['int'].connect(self.chSpeedValue.setValue)
        self.chSpeedValue.valueChanged['int'].connect(self.chSpeed.setValue)
        self.chSpeedCollisionValue.valueChanged['int'].connect(self.chSpeedCollision.setValue)
        QtCore.QMetaObject.connectSlotsByName(Configuration)

    def retranslateUi(self, Configuration):
        _translate = QtCore.QCoreApplication.translate
        Configuration.setWindowTitle(_translate("Configuration", "Configuration"))
        self.label.setText(_translate("Configuration", "IP Address of Robot"))
        self.robotIp.setInputMask(_translate("Configuration", "000.000.000.000"))
        self.robotIp.setPlaceholderText(_translate("Configuration", "192.169.0.1"))
        self.label_2.setText(_translate("Configuration", "Play time in seconds"))
        self.playTime.setSuffix(_translate("Configuration", " seconds"))
        self.label_3.setText(_translate("Configuration", "Vitesse maxi des chenilles en %"))
        self.label_4.setText(_translate("Configuration", "Vitesse chenilles en % si collision"))
        self.label_5.setText(_translate("Configuration", "Distance mini collision"))
        self.chSpeedCollisionValue.setSuffix(_translate("Configuration", " %"))
        self.chSpeedValue.setSuffix(_translate("Configuration", " %"))

