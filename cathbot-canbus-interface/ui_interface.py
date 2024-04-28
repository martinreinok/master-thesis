# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaceQtBAzV.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(334, 316)
        MainWindow.setMinimumSize(QSize(334, 316))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.slider_default_resistance = QSlider(self.centralwidget)
        self.slider_default_resistance.setObjectName(u"slider_default_resistance")
        self.slider_default_resistance.setMaximum(200)
        self.slider_default_resistance.setValue(10)
        self.slider_default_resistance.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.slider_default_resistance)

        self.field_default_resistance = QLineEdit(self.centralwidget)
        self.field_default_resistance.setObjectName(u"field_default_resistance")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.field_default_resistance.sizePolicy().hasHeightForWidth())
        self.field_default_resistance.setSizePolicy(sizePolicy)
        self.field_default_resistance.setMaximumSize(QSize(60, 16777215))
        self.field_default_resistance.setReadOnly(True)

        self.horizontalLayout.addWidget(self.field_default_resistance)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.check_simulate_collision = QCheckBox(self.centralwidget)
        self.check_simulate_collision.setObjectName(u"check_simulate_collision")

        self.horizontalLayout_5.addWidget(self.check_simulate_collision)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.slider_collision_resistance = QSlider(self.centralwidget)
        self.slider_collision_resistance.setObjectName(u"slider_collision_resistance")
        self.slider_collision_resistance.setMaximum(300)
        self.slider_collision_resistance.setValue(30)
        self.slider_collision_resistance.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider_collision_resistance)

        self.field_collision_resistance = QLineEdit(self.centralwidget)
        self.field_collision_resistance.setObjectName(u"field_collision_resistance")
        sizePolicy.setHeightForWidth(self.field_collision_resistance.sizePolicy().hasHeightForWidth())
        self.field_collision_resistance.setSizePolicy(sizePolicy)
        self.field_collision_resistance.setMaximumSize(QSize(60, 16777215))
        self.field_collision_resistance.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.field_collision_resistance)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.slider_linear_translation = QSlider(self.centralwidget)
        self.slider_linear_translation.setObjectName(u"slider_linear_translation")
        self.slider_linear_translation.setMaximum(20)
        self.slider_linear_translation.setValue(8)
        self.slider_linear_translation.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.slider_linear_translation)

        self.field_linear_translation = QLineEdit(self.centralwidget)
        self.field_linear_translation.setObjectName(u"field_linear_translation")
        sizePolicy.setHeightForWidth(self.field_linear_translation.sizePolicy().hasHeightForWidth())
        self.field_linear_translation.setSizePolicy(sizePolicy)
        self.field_linear_translation.setMaximumSize(QSize(60, 16777215))
        self.field_linear_translation.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.field_linear_translation)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.slider_rotary_translation = QSlider(self.centralwidget)
        self.slider_rotary_translation.setObjectName(u"slider_rotary_translation")
        self.slider_rotary_translation.setMaximum(20)
        self.slider_rotary_translation.setValue(8)
        self.slider_rotary_translation.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_4.addWidget(self.slider_rotary_translation)

        self.field_rotary_translation = QLineEdit(self.centralwidget)
        self.field_rotary_translation.setObjectName(u"field_rotary_translation")
        sizePolicy.setHeightForWidth(self.field_rotary_translation.sizePolicy().hasHeightForWidth())
        self.field_rotary_translation.setSizePolicy(sizePolicy)
        self.field_rotary_translation.setMaximumSize(QSize(60, 16777215))
        self.field_rotary_translation.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.field_rotary_translation)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 40))

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 334, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CathBot CAN bus Interface", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"CathBot Default Resistance", None))
        self.field_default_resistance.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"CathBot Collision Resistance", None))
        self.check_simulate_collision.setText(QCoreApplication.translate("MainWindow", u"Simulate Collision", None))
        self.field_collision_resistance.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"CathBot Linear Motor Translation Factor", None))
        self.field_linear_translation.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"CathBot Rotary Motor Translation Factor", None))
        self.field_rotary_translation.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
    # retranslateUi

