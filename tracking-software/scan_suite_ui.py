# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'master-thesis-ui-scan-3d-suiteiluNri.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDockWidget, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_ScanSuite(object):
    def setupUi(self, ScanSuite):
        if not ScanSuite.objectName():
            ScanSuite.setObjectName(u"ScanSuite")
        ScanSuite.resize(751, 545)
        self.actionIP_Address = QAction(ScanSuite)
        self.actionIP_Address.setObjectName(u"actionIP_Address")
        self.centralwidget = QWidget(ScanSuite)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        ScanSuite.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ScanSuite)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 751, 22))
        ScanSuite.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ScanSuite)
        self.statusbar.setObjectName(u"statusbar")
        ScanSuite.setStatusBar(self.statusbar)
        self.dock_settings = QDockWidget(ScanSuite)
        self.dock_settings.setObjectName(u"dock_settings")
        self.dock_settings.setMinimumSize(QSize(308, 502))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_scanner = QFrame(self.dockWidgetContents)
        self.frame_scanner.setObjectName(u"frame_scanner")
        self.frame_scanner.setMinimumSize(QSize(0, 0))
        self.frame_scanner.setFrameShape(QFrame.Box)
        self.frame_scanner.setFrameShadow(QFrame.Sunken)
        self.formLayout_4 = QFormLayout(self.frame_scanner)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_4 = QLabel(self.frame_scanner)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        self.label_4.setFont(font)

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.label_8 = QLabel(self.frame_scanner)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setEnabled(False)
        self.label_8.setFont(font)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.label_8)

        self.label = QLabel(self.frame_scanner)
        self.label.setObjectName(u"label")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label)

        self.field_scan_start_coordinates = QLineEdit(self.frame_scanner)
        self.field_scan_start_coordinates.setObjectName(u"field_scan_start_coordinates")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.field_scan_start_coordinates)

        self.label_2 = QLabel(self.frame_scanner)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.field_scan_end_coordinates = QLineEdit(self.frame_scanner)
        self.field_scan_end_coordinates.setObjectName(u"field_scan_end_coordinates")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.field_scan_end_coordinates)

        self.label_3 = QLabel(self.frame_scanner)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.field_image_amount = QSpinBox(self.frame_scanner)
        self.field_image_amount.setObjectName(u"field_image_amount")
        self.field_image_amount.setValue(10)

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.field_image_amount)

        self.label_12 = QLabel(self.frame_scanner)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.label_12)

        self.combo_select_template = QComboBox(self.frame_scanner)
        self.combo_select_template.setObjectName(u"combo_select_template")

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.combo_select_template)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout_4.setItem(5, QFormLayout.LabelRole, self.horizontalSpacer)

        self.button_load_model = QPushButton(self.frame_scanner)
        self.button_load_model.setObjectName(u"button_load_model")
        self.button_load_model.setEnabled(True)
        self.button_load_model.setMinimumSize(QSize(0, 40))

        self.formLayout_4.setWidget(5, QFormLayout.FieldRole, self.button_load_model)

        self.status_load_model = QLabel(self.frame_scanner)
        self.status_load_model.setObjectName(u"status_load_model")
        self.status_load_model.setWordWrap(True)
        self.status_load_model.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.formLayout_4.setWidget(6, QFormLayout.FieldRole, self.status_load_model)


        self.verticalLayout.addWidget(self.frame_scanner)

        self.frame_register = QFrame(self.dockWidgetContents)
        self.frame_register.setObjectName(u"frame_register")
        self.frame_register.setMinimumSize(QSize(0, 0))
        self.frame_register.setFrameShape(QFrame.Box)
        self.frame_register.setFrameShadow(QFrame.Sunken)
        self.formLayout_3 = QFormLayout(self.frame_register)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_10 = QLabel(self.frame_register)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_10)

        self.field_ip_address = QLineEdit(self.frame_register)
        self.field_ip_address.setObjectName(u"field_ip_address")
        self.field_ip_address.setEnabled(False)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.field_ip_address)

        self.label_9 = QLabel(self.frame_register)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.field_client_name = QLineEdit(self.frame_register)
        self.field_client_name.setObjectName(u"field_client_name")
        self.field_client_name.setEnabled(False)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.field_client_name)

        self.label_11 = QLabel(self.frame_register)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_11)

        self.field_version = QLineEdit(self.frame_register)
        self.field_version.setObjectName(u"field_version")
        self.field_version.setEnabled(False)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.field_version)


        self.verticalLayout.addWidget(self.frame_register)

        self.frame_tcp = QFrame(self.dockWidgetContents)
        self.frame_tcp.setObjectName(u"frame_tcp")
        self.frame_tcp.setMinimumSize(QSize(0, 0))
        self.frame_tcp.setMaximumSize(QSize(16777215, 16777215))
        self.frame_tcp.setFrameShape(QFrame.Box)
        self.frame_tcp.setFrameShadow(QFrame.Sunken)
        self.formLayout_2 = QFormLayout(self.frame_tcp)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_7 = QLabel(self.frame_tcp)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.label_5 = QLabel(self.frame_tcp)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.label_6 = QLabel(self.frame_tcp)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setEnabled(False)
        self.label_6.setFont(font)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.label_6)

        self.field_tcp_port = QLineEdit(self.frame_tcp)
        self.field_tcp_port.setObjectName(u"field_tcp_port")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.field_tcp_port)


        self.verticalLayout.addWidget(self.frame_tcp)

        self.dock_settings.setWidget(self.dockWidgetContents)
        ScanSuite.addDockWidget(Qt.LeftDockWidgetArea, self.dock_settings)

        self.retranslateUi(ScanSuite)

        QMetaObject.connectSlotsByName(ScanSuite)
    # setupUi

    def retranslateUi(self, ScanSuite):
        ScanSuite.setWindowTitle(QCoreApplication.translate("ScanSuite", u"3D Suite", None))
        self.actionIP_Address.setText(QCoreApplication.translate("ScanSuite", u"IP Address", None))
        self.label_4.setText(QCoreApplication.translate("ScanSuite", u"Scan Settings", None))
        self.label_8.setText(QCoreApplication.translate("ScanSuite", u"Scanning is not implemented.\nOnly 3D models can be loaded.", None))
        self.label.setText(QCoreApplication.translate("ScanSuite", u"Scan Start", None))
        self.field_scan_start_coordinates.setPlaceholderText(QCoreApplication.translate("ScanSuite", u"0,0,0 (x, y, z)", None))
        self.label_2.setText(QCoreApplication.translate("ScanSuite", u"Scan End", None))
        self.field_scan_end_coordinates.setPlaceholderText(QCoreApplication.translate("ScanSuite", u"0,0,0 (x, y, z)", None))
        self.label_3.setText(QCoreApplication.translate("ScanSuite", u"Images Amount", None))
        self.label_12.setText(QCoreApplication.translate("ScanSuite", u"Select Template", None))
        self.button_load_model.setText(QCoreApplication.translate("ScanSuite", u"Load 3D Scan", None))
        self.status_load_model.setText("")
        self.label_10.setText(QCoreApplication.translate("ScanSuite", u"IP Address", None))
        self.field_ip_address.setText(QCoreApplication.translate("ScanSuite", u"127.0.0.1", None))
        self.label_9.setText(QCoreApplication.translate("ScanSuite", u"Client Name", None))
        self.field_client_name.setText(QCoreApplication.translate("ScanSuite", u"ScanSuite", None))
        self.label_11.setText(QCoreApplication.translate("ScanSuite", u"Version", None))
        self.field_version.setText(QCoreApplication.translate("ScanSuite", u"v2", None))
        self.label_7.setText(QCoreApplication.translate("ScanSuite", u"Port", None))
        self.label_5.setText(QCoreApplication.translate("ScanSuite", u"TCP Settings", None))
        self.label_6.setText(QCoreApplication.translate("ScanSuite", u"For receiving artifact position data", None))
    # retranslateUi

