# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'master-thesis-uiuKjprC.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(776, 590)
        MainWindow.setStyleSheet(u"")
        self.actionImages = QAction(MainWindow)
        self.actionImages.setObjectName(u"actionImages")
        self.actionImages.setCheckable(True)
        self.actionImages.setChecked(True)
        self.actionAccess_i_Client = QAction(MainWindow)
        self.actionAccess_i_Client.setObjectName(u"actionAccess_i_Client")
        self.actionAccess_i_Client.setCheckable(True)
        self.actionAccess_i_Client.setChecked(True)
        self.actionGuidewire_Tracking = QAction(MainWindow)
        self.actionGuidewire_Tracking.setObjectName(u"actionGuidewire_Tracking")
        self.actionGuidewire_Tracking.setCheckable(True)
        self.actionGuidewire_Tracking.setChecked(True)
        self.actionOpen_3D_Scan_Suite = QAction(MainWindow)
        self.actionOpen_3D_Scan_Suite.setObjectName(u"actionOpen_3D_Scan_Suite")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.AccessiClient = QFrame(self.centralwidget)
        self.AccessiClient.setObjectName(u"AccessiClient")
        self.AccessiClient.setMinimumSize(QSize(371, 0))
        self.AccessiClient.setFrameShape(QFrame.Box)
        self.AccessiClient.setFrameShadow(QFrame.Sunken)
        self.verticalLayout = QVBoxLayout(self.AccessiClient)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.AccessiClient)
        self.label.setObjectName(u"label")
        self.label.setEnabled(False)

        self.verticalLayout.addWidget(self.label)

        self.Accessi_stuff = QTabWidget(self.AccessiClient)
        self.Accessi_stuff.setObjectName(u"Accessi_stuff")
        self.Accessi_stuff.setEnabled(True)
        self.connect = QWidget()
        self.connect.setObjectName(u"connect")
        self.formLayout_3 = QFormLayout(self.connect)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(-1, 9, -1, -1)
        self.label_2 = QLabel(self.connect)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.field_ip_address = QLineEdit(self.connect)
        self.field_ip_address.setObjectName(u"field_ip_address")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.field_ip_address)

        self.label_3 = QLabel(self.connect)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.field_client_name = QLineEdit(self.connect)
        self.field_client_name.setObjectName(u"field_client_name")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.field_client_name)

        self.label_11 = QLabel(self.connect)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_11)

        self.field_version = QLineEdit(self.connect)
        self.field_version.setObjectName(u"field_version")

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.field_version)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout_3.setItem(3, QFormLayout.LabelRole, self.horizontalSpacer)

        self.button_register = QPushButton(self.connect)
        self.button_register.setObjectName(u"button_register")
        self.button_register.setMinimumSize(QSize(0, 40))
        self.button_register.setAutoDefault(True)

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.button_register)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout_3.setItem(4, QFormLayout.LabelRole, self.horizontalSpacer_2)

        self.status_register = QLabel(self.connect)
        self.status_register.setObjectName(u"status_register")
        self.status_register.setEnabled(True)
        self.status_register.setAlignment(Qt.AlignCenter)
        self.status_register.setWordWrap(True)
        self.status_register.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.status_register)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout_3.setItem(5, QFormLayout.LabelRole, self.horizontalSpacer_3)

        self.button_request_control = QPushButton(self.connect)
        self.button_request_control.setObjectName(u"button_request_control")
        self.button_request_control.setEnabled(False)
        self.button_request_control.setMinimumSize(QSize(0, 40))
        self.button_request_control.setAutoDefault(True)

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.button_request_control)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout_3.setItem(6, QFormLayout.LabelRole, self.horizontalSpacer_4)

        self.status_request_control = QLabel(self.connect)
        self.status_request_control.setObjectName(u"status_request_control")
        self.status_request_control.setEnabled(True)
        self.status_request_control.setAlignment(Qt.AlignCenter)
        self.status_request_control.setWordWrap(True)
        self.status_request_control.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.formLayout_3.setWidget(6, QFormLayout.FieldRole, self.status_request_control)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout_3.setItem(7, QFormLayout.LabelRole, self.horizontalSpacer_6)

        self.button_release_control = QPushButton(self.connect)
        self.button_release_control.setObjectName(u"button_release_control")
        self.button_release_control.setEnabled(False)
        self.button_release_control.setMinimumSize(QSize(0, 40))

        self.formLayout_3.setWidget(7, QFormLayout.FieldRole, self.button_release_control)

        self.status_release_control = QLabel(self.connect)
        self.status_release_control.setObjectName(u"status_release_control")
        self.status_release_control.setEnabled(True)
        self.status_release_control.setAlignment(Qt.AlignCenter)
        self.status_release_control.setWordWrap(True)
        self.status_release_control.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.formLayout_3.setWidget(8, QFormLayout.FieldRole, self.status_release_control)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.formLayout_3.setItem(8, QFormLayout.LabelRole, self.horizontalSpacer_7)

        self.Accessi_stuff.addTab(self.connect, "")
        self.templates = QWidget()
        self.templates.setObjectName(u"templates")
        self.verticalLayout_6 = QVBoxLayout(self.templates)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.button_get_templates = QPushButton(self.templates)
        self.button_get_templates.setObjectName(u"button_get_templates")
        self.button_get_templates.setEnabled(False)

        self.verticalLayout_6.addWidget(self.button_get_templates)

        self.table_templates = QTableWidget(self.templates)
        if (self.table_templates.columnCount() < 3):
            self.table_templates.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_templates.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_templates.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_templates.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_templates.setObjectName(u"table_templates")
        self.table_templates.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_templates.setProperty("showDropIndicator", False)
        self.table_templates.setDragDropOverwriteMode(False)
        self.table_templates.setAlternatingRowColors(True)
        self.table_templates.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_templates.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_6.addWidget(self.table_templates)

        self.button_open_template = QPushButton(self.templates)
        self.button_open_template.setObjectName(u"button_open_template")
        self.button_open_template.setEnabled(False)

        self.verticalLayout_6.addWidget(self.button_open_template)

        self.status_open_template = QLabel(self.templates)
        self.status_open_template.setObjectName(u"status_open_template")
        self.status_open_template.setEnabled(True)
        self.status_open_template.setAlignment(Qt.AlignCenter)
        self.status_open_template.setWordWrap(True)
        self.status_open_template.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_6.addWidget(self.status_open_template)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.button_start_template = QPushButton(self.templates)
        self.button_start_template.setObjectName(u"button_start_template")
        self.button_start_template.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_start_template.sizePolicy().hasHeightForWidth())
        self.button_start_template.setSizePolicy(sizePolicy)
        self.button_start_template.setMinimumSize(QSize(0, 50))
        self.button_start_template.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.button_start_template.setFont(font)
        self.button_start_template.setStyleSheet(u"")
        self.button_start_template.setCheckable(False)

        self.horizontalLayout_2.addWidget(self.button_start_template)

        self.button_stop_template = QPushButton(self.templates)
        self.button_stop_template.setObjectName(u"button_stop_template")
        self.button_stop_template.setEnabled(False)
        sizePolicy.setHeightForWidth(self.button_stop_template.sizePolicy().hasHeightForWidth())
        self.button_stop_template.setSizePolicy(sizePolicy)
        self.button_stop_template.setMinimumSize(QSize(0, 50))
        self.button_stop_template.setBaseSize(QSize(0, 0))
        self.button_stop_template.setFont(font)
        self.button_stop_template.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.button_stop_template)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)

        self.status_start_stop_template = QLabel(self.templates)
        self.status_start_stop_template.setObjectName(u"status_start_stop_template")
        self.status_start_stop_template.setEnabled(True)
        self.status_start_stop_template.setAlignment(Qt.AlignCenter)
        self.status_start_stop_template.setWordWrap(True)
        self.status_start_stop_template.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_6.addWidget(self.status_start_stop_template)

        self.Accessi_stuff.addTab(self.templates, "")
        self.parameters = QWidget()
        self.parameters.setObjectName(u"parameters")
        self.formLayout_2 = QFormLayout(self.parameters)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_4 = QLabel(self.parameters)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setEnabled(False)
        font1 = QFont()
        font1.setBold(True)
        self.label_4.setFont(font1)

        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.label_4)

        self.line = QFrame(self.parameters)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.line)

        self.label_7 = QLabel(self.parameters)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_7)

        self.button_get_parameter = QPushButton(self.parameters)
        self.button_get_parameter.setObjectName(u"button_get_parameter")
        self.button_get_parameter.setEnabled(False)
        self.button_get_parameter.setMinimumSize(QSize(0, 40))

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.button_get_parameter)

        self.status_get_parameter = QLabel(self.parameters)
        self.status_get_parameter.setObjectName(u"status_get_parameter")
        self.status_get_parameter.setEnabled(True)
        self.status_get_parameter.setAlignment(Qt.AlignCenter)
        self.status_get_parameter.setWordWrap(True)
        self.status_get_parameter.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.status_get_parameter)

        self.line_2 = QFrame(self.parameters)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Raised)
        self.line_2.setLineWidth(1)
        self.line_2.setFrameShape(QFrame.HLine)

        self.formLayout_2.setWidget(5, QFormLayout.SpanningRole, self.line_2)

        self.label_5 = QLabel(self.parameters)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setEnabled(False)
        self.label_5.setFont(font1)

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_5)

        self.label_6 = QLabel(self.parameters)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.label_6)

        self.combo_set_parameter_choice = QComboBox(self.parameters)
        self.combo_set_parameter_choice.setObjectName(u"combo_set_parameter_choice")
        self.combo_set_parameter_choice.setEditable(False)
        self.combo_set_parameter_choice.setMaxVisibleItems(25)
        self.combo_set_parameter_choice.setInsertPolicy(QComboBox.InsertAlphabetically)

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.combo_set_parameter_choice)

        self.label_8 = QLabel(self.parameters)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.label_8)

        self.field_parameter_value = QLineEdit(self.parameters)
        self.field_parameter_value.setObjectName(u"field_parameter_value")

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.field_parameter_value)

        self.button_set_parameter = QPushButton(self.parameters)
        self.button_set_parameter.setObjectName(u"button_set_parameter")
        self.button_set_parameter.setEnabled(False)
        self.button_set_parameter.setMinimumSize(QSize(0, 40))
        self.button_set_parameter.setAutoDefault(True)

        self.formLayout_2.setWidget(9, QFormLayout.FieldRole, self.button_set_parameter)

        self.status_set_parameter = QLabel(self.parameters)
        self.status_set_parameter.setObjectName(u"status_set_parameter")
        self.status_set_parameter.setEnabled(True)
        self.status_set_parameter.setAlignment(Qt.AlignCenter)
        self.status_set_parameter.setWordWrap(True)
        self.status_set_parameter.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.formLayout_2.setWidget(10, QFormLayout.FieldRole, self.status_set_parameter)

        self.combo_get_parameter_choice = QComboBox(self.parameters)
        self.combo_get_parameter_choice.setObjectName(u"combo_get_parameter_choice")
        self.combo_get_parameter_choice.setEditable(False)
        self.combo_get_parameter_choice.setMaxVisibleItems(25)
        self.combo_get_parameter_choice.setInsertPolicy(QComboBox.InsertAlphabetically)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.combo_get_parameter_choice)

        self.Accessi_stuff.addTab(self.parameters, "")

        self.verticalLayout.addWidget(self.Accessi_stuff)


        self.gridLayout.addWidget(self.AccessiClient, 0, 4, 1, 1)

        self.SubPrograms = QFrame(self.centralwidget)
        self.SubPrograms.setObjectName(u"SubPrograms")
        self.SubPrograms.setMinimumSize(QSize(376, 0))
        self.SubPrograms.setFrameShape(QFrame.Box)
        self.SubPrograms.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_8 = QVBoxLayout(self.SubPrograms)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_9 = QLabel(self.SubPrograms)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setEnabled(False)

        self.verticalLayout_8.addWidget(self.label_9)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_14 = QLabel(self.SubPrograms)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_6.addWidget(self.label_14)

        self.field_output_directory = QLineEdit(self.SubPrograms)
        self.field_output_directory.setObjectName(u"field_output_directory")

        self.horizontalLayout_6.addWidget(self.field_output_directory)

        self.button_select_output_dir = QPushButton(self.SubPrograms)
        self.button_select_output_dir.setObjectName(u"button_select_output_dir")
        self.button_select_output_dir.setMaximumSize(QSize(20, 16777215))

        self.horizontalLayout_6.addWidget(self.button_select_output_dir)


        self.verticalLayout_9.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_15 = QLabel(self.SubPrograms)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_9.addWidget(self.label_15)

        self.combo_show_output_dimensions = QComboBox(self.SubPrograms)
        self.combo_show_output_dimensions.addItem("")
        self.combo_show_output_dimensions.addItem("")
        self.combo_show_output_dimensions.addItem("")
        self.combo_show_output_dimensions.addItem("")
        self.combo_show_output_dimensions.addItem("")
        self.combo_show_output_dimensions.setObjectName(u"combo_show_output_dimensions")
        self.combo_show_output_dimensions.setEditable(False)

        self.horizontalLayout_9.addWidget(self.combo_show_output_dimensions)


        self.verticalLayout_9.addLayout(self.horizontalLayout_9)

        self.line_5 = QFrame(self.SubPrograms)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.check_websocket_active = QCheckBox(self.SubPrograms)
        self.check_websocket_active.setObjectName(u"check_websocket_active")
        self.check_websocket_active.setEnabled(False)
        self.check_websocket_active.setChecked(True)

        self.horizontalLayout.addWidget(self.check_websocket_active)

        self.check_websocket_output = QCheckBox(self.SubPrograms)
        self.check_websocket_output.setObjectName(u"check_websocket_output")
        self.check_websocket_output.setEnabled(False)

        self.horizontalLayout.addWidget(self.check_websocket_output)


        self.verticalLayout_9.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.check_websocket_save = QCheckBox(self.SubPrograms)
        self.check_websocket_save.setObjectName(u"check_websocket_save")
        self.check_websocket_save.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.check_websocket_save)

        self.status_websocket_image = QLabel(self.SubPrograms)
        self.status_websocket_image.setObjectName(u"status_websocket_image")
        self.status_websocket_image.setWordWrap(True)
        self.status_websocket_image.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.horizontalLayout_4.addWidget(self.status_websocket_image)


        self.verticalLayout_9.addLayout(self.horizontalLayout_4)

        self.line_4 = QFrame(self.SubPrograms)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line_4)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.check_cnn_active = QCheckBox(self.SubPrograms)
        self.check_cnn_active.setObjectName(u"check_cnn_active")
        self.check_cnn_active.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.check_cnn_active)

        self.check_cnn_output = QCheckBox(self.SubPrograms)
        self.check_cnn_output.setObjectName(u"check_cnn_output")
        self.check_cnn_output.setEnabled(False)
        self.check_cnn_output.setChecked(False)

        self.horizontalLayout_8.addWidget(self.check_cnn_output)


        self.verticalLayout_9.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.check_cnn_save = QCheckBox(self.SubPrograms)
        self.check_cnn_save.setObjectName(u"check_cnn_save")
        self.check_cnn_save.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.check_cnn_save)

        self.status_cnn = QLabel(self.SubPrograms)
        self.status_cnn.setObjectName(u"status_cnn")
        self.status_cnn.setWordWrap(True)
        self.status_cnn.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.horizontalLayout_5.addWidget(self.status_cnn)


        self.verticalLayout_9.addLayout(self.horizontalLayout_5)

        self.line_3 = QFrame(self.SubPrograms)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.check_guidewire_tracking_active = QCheckBox(self.SubPrograms)
        self.check_guidewire_tracking_active.setObjectName(u"check_guidewire_tracking_active")
        self.check_guidewire_tracking_active.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.check_guidewire_tracking_active)

        self.check_tracking_output = QCheckBox(self.SubPrograms)
        self.check_tracking_output.setObjectName(u"check_tracking_output")
        self.check_tracking_output.setEnabled(False)
        self.check_tracking_output.setChecked(False)

        self.horizontalLayout_3.addWidget(self.check_tracking_output)


        self.verticalLayout_9.addLayout(self.horizontalLayout_3)

        self.status_guidewire_tracking = QLabel(self.SubPrograms)
        self.status_guidewire_tracking.setObjectName(u"status_guidewire_tracking")
        self.status_guidewire_tracking.setEnabled(True)
        self.status_guidewire_tracking.setWordWrap(True)
        self.status_guidewire_tracking.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_9.addWidget(self.status_guidewire_tracking)

        self.check_tracking_move_slice = QCheckBox(self.SubPrograms)
        self.check_tracking_move_slice.setObjectName(u"check_tracking_move_slice")
        self.check_tracking_move_slice.setEnabled(False)

        self.verticalLayout_9.addWidget(self.check_tracking_move_slice)

        self.status_move_mri_slice = QLabel(self.SubPrograms)
        self.status_move_mri_slice.setObjectName(u"status_move_mri_slice")
        self.status_move_mri_slice.setEnabled(True)
        self.status_move_mri_slice.setWordWrap(True)
        self.status_move_mri_slice.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_9.addWidget(self.status_move_mri_slice)

        self.check_tracking_save = QCheckBox(self.SubPrograms)
        self.check_tracking_save.setObjectName(u"check_tracking_save")
        self.check_tracking_save.setEnabled(False)

        self.verticalLayout_9.addWidget(self.check_tracking_save)

        self.line_6 = QFrame(self.SubPrograms)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.check_collision_detection_active = QCheckBox(self.SubPrograms)
        self.check_collision_detection_active.setObjectName(u"check_collision_detection_active")
        self.check_collision_detection_active.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.check_collision_detection_active)

        self.check_collision_output = QCheckBox(self.SubPrograms)
        self.check_collision_output.setObjectName(u"check_collision_output")
        self.check_collision_output.setEnabled(False)
        self.check_collision_output.setChecked(False)

        self.horizontalLayout_7.addWidget(self.check_collision_output)


        self.verticalLayout_9.addLayout(self.horizontalLayout_7)

        self.status_collision_detection = QLabel(self.SubPrograms)
        self.status_collision_detection.setObjectName(u"status_collision_detection")
        self.status_collision_detection.setEnabled(True)
        self.status_collision_detection.setWordWrap(True)
        self.status_collision_detection.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_9.addWidget(self.status_collision_detection)

        self.check_cathbot_collision_feedback = QCheckBox(self.SubPrograms)
        self.check_cathbot_collision_feedback.setObjectName(u"check_cathbot_collision_feedback")
        self.check_cathbot_collision_feedback.setEnabled(False)

        self.verticalLayout_9.addWidget(self.check_cathbot_collision_feedback)

        self.status_cathbot_feedback = QLabel(self.SubPrograms)
        self.status_cathbot_feedback.setObjectName(u"status_cathbot_feedback")
        self.status_cathbot_feedback.setEnabled(True)
        self.status_cathbot_feedback.setWordWrap(True)
        self.status_cathbot_feedback.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout_9.addWidget(self.status_cathbot_feedback)

        self.check_collision_save = QCheckBox(self.SubPrograms)
        self.check_collision_save.setObjectName(u"check_collision_save")
        self.check_collision_save.setEnabled(False)

        self.verticalLayout_9.addWidget(self.check_collision_save)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_9.addItem(self.horizontalSpacer_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer)


        self.verticalLayout_8.addLayout(self.verticalLayout_9)


        self.gridLayout.addWidget(self.SubPrograms, 0, 5, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 776, 22))
        self.menu3D_Suite = QMenu(self.menubar)
        self.menu3D_Suite.setObjectName(u"menu3D_Suite")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu3D_Suite.menuAction())
        self.menu3D_Suite.addAction(self.actionOpen_3D_Scan_Suite)

        self.retranslateUi(MainWindow)

        self.Accessi_stuff.setCurrentIndex(0)
        self.button_set_parameter.setDefault(True)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionImages.setText(QCoreApplication.translate("MainWindow", u"Images", None))
        self.actionAccess_i_Client.setText(QCoreApplication.translate("MainWindow", u"Access-i Client", None))
        self.actionGuidewire_Tracking.setText(QCoreApplication.translate("MainWindow", u"Guidewire Tracking", None))
        self.actionOpen_3D_Scan_Suite.setText(QCoreApplication.translate("MainWindow", u"Open 3D Scan Suite", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Access-i Client", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"IP Address", None))
        self.field_ip_address.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Client Name", None))
        self.field_client_name.setText(QCoreApplication.translate("MainWindow", u"Martin Reinok Python Client", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.field_version.setText(QCoreApplication.translate("MainWindow", u"v2", None))
        self.button_register.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.status_register.setText("")
        self.button_request_control.setText(QCoreApplication.translate("MainWindow", u"Request Control", None))
        self.status_request_control.setText("")
        self.button_release_control.setText(QCoreApplication.translate("MainWindow", u"Release Control", None))
        self.status_release_control.setText("")
        self.Accessi_stuff.setTabText(self.Accessi_stuff.indexOf(self.connect), QCoreApplication.translate("MainWindow", u"Connect", None))
        self.button_get_templates.setText(QCoreApplication.translate("MainWindow", u"Get Templates", None))
        ___qtablewidgetitem = self.table_templates.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem1 = self.table_templates.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Interactive", None));
        ___qtablewidgetitem2 = self.table_templates.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"ID", None));
        self.button_open_template.setText(QCoreApplication.translate("MainWindow", u"Open Template", None))
        self.status_open_template.setText("")
        self.button_start_template.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.button_stop_template.setText(QCoreApplication.translate("MainWindow", u"Stop/Close Template", None))
        self.status_start_stop_template.setText("")
        self.Accessi_stuff.setTabText(self.Accessi_stuff.indexOf(self.templates), QCoreApplication.translate("MainWindow", u"Templates", None))
#if QT_CONFIG(accessibility)
        self.parameters.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Get Parameter", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Parameter", None))
        self.button_get_parameter.setText(QCoreApplication.translate("MainWindow", u"Get Parameter", None))
        self.status_get_parameter.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Set Parameter", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Parameter", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Value", None))
        self.button_set_parameter.setText(QCoreApplication.translate("MainWindow", u"Set Parameter", None))
        self.status_set_parameter.setText("")
        self.Accessi_stuff.setTabText(self.Accessi_stuff.indexOf(self.parameters), QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Sub Programs", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Output Directory", None))
        self.field_output_directory.setText(QCoreApplication.translate("MainWindow", u"C:/Users/C/Desktop/Master Thesis/LOG_IMAGES", None))
        self.button_select_output_dir.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Show Output Dimensions", None))
        self.combo_show_output_dimensions.setItemText(0, QCoreApplication.translate("MainWindow", u"512x512", None))
        self.combo_show_output_dimensions.setItemText(1, QCoreApplication.translate("MainWindow", u"1024x1024", None))
        self.combo_show_output_dimensions.setItemText(2, QCoreApplication.translate("MainWindow", u"2048x2048", None))
        self.combo_show_output_dimensions.setItemText(3, QCoreApplication.translate("MainWindow", u"128x128", None))
        self.combo_show_output_dimensions.setItemText(4, QCoreApplication.translate("MainWindow", u"256x256", None))

        self.check_websocket_active.setText(QCoreApplication.translate("MainWindow", u"Access-i Websocket", None))
        self.check_websocket_output.setText(QCoreApplication.translate("MainWindow", u"Show Output", None))
        self.check_websocket_save.setText(QCoreApplication.translate("MainWindow", u"Save Websocket Images", None))
        self.status_websocket_image.setText("")
        self.check_cnn_active.setText(QCoreApplication.translate("MainWindow", u"CNN Active", None))
        self.check_cnn_output.setText(QCoreApplication.translate("MainWindow", u"Show Output", None))
        self.check_cnn_save.setText(QCoreApplication.translate("MainWindow", u"Save CNN Images", None))
        self.status_cnn.setText("")
        self.check_guidewire_tracking_active.setText(QCoreApplication.translate("MainWindow", u"Guidewire Tracking", None))
        self.check_tracking_output.setText(QCoreApplication.translate("MainWindow", u"Show Output", None))
        self.status_guidewire_tracking.setText("")
        self.check_tracking_move_slice.setText(QCoreApplication.translate("MainWindow", u"Move MRI Slice", None))
        self.status_move_mri_slice.setText("")
        self.check_tracking_save.setText(QCoreApplication.translate("MainWindow", u"Save Tracking Images", None))
        self.check_collision_detection_active.setText(QCoreApplication.translate("MainWindow", u"Collision Detection", None))
        self.check_collision_output.setText(QCoreApplication.translate("MainWindow", u"Show Output", None))
        self.status_collision_detection.setText("")
        self.check_cathbot_collision_feedback.setText(QCoreApplication.translate("MainWindow", u"CathBot Feedback", None))
        self.status_cathbot_feedback.setText("")
        self.check_collision_save.setText(QCoreApplication.translate("MainWindow", u"Save Collision Detection Images", None))
        self.menu3D_Suite.setTitle(QCoreApplication.translate("MainWindow", u"ScanSuite", None))
    # retranslateUi

