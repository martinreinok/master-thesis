# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_uiPOvhtw.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
    QFormLayout, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 550)
        MainWindow.setMinimumSize(QSize(700, 550))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        self.actionOpen_3D_Scan_Suite = QAction(MainWindow)
        self.actionOpen_3D_Scan_Suite.setObjectName(u"actionOpen_3D_Scan_Suite")
        self.actionLight = QAction(MainWindow)
        self.actionLight.setObjectName(u"actionLight")
        self.actionLight.setCheckable(True)
        self.actionDark = QAction(MainWindow)
        self.actionDark.setObjectName(u"actionDark")
        self.actionDark.setCheckable(True)
        self.actionDark.setChecked(True)
        self.actionOpen_CathBot_CAN_Interface = QAction(MainWindow)
        self.actionOpen_CathBot_CAN_Interface.setObjectName(u"actionOpen_CathBot_CAN_Interface")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.AccessiClient = QFrame(self.centralwidget)
        self.AccessiClient.setObjectName(u"AccessiClient")
        self.AccessiClient.setFrameShape(QFrame.Shape.Box)
        self.AccessiClient.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout = QVBoxLayout(self.AccessiClient)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.AccessiClient)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.line = QFrame(self.AccessiClient)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.tabWidget = QTabWidget(self.AccessiClient)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.formLayout = QFormLayout(self.tab)
        self.formLayout.setObjectName(u"formLayout")
        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.field_ip_address = QLineEdit(self.tab)
        self.field_ip_address.setObjectName(u"field_ip_address")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.field_ip_address)

        self.field_client_name = QLineEdit(self.tab)
        self.field_client_name.setObjectName(u"field_client_name")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.field_client_name)

        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.field_version = QLineEdit(self.tab)
        self.field_version.setObjectName(u"field_version")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.field_version)

        self.button_register = QPushButton(self.tab)
        self.button_register.setObjectName(u"button_register")
        self.button_register.setEnabled(True)
        self.button_register.setMinimumSize(QSize(0, 40))

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.button_register)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.formLayout.setItem(3, QFormLayout.LabelRole, self.horizontalSpacer)

        self.status_register = QLabel(self.tab)
        self.status_register.setObjectName(u"status_register")
        self.status_register.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_register.setWordWrap(True)
        self.status_register.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.status_register)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.formLayout.setItem(4, QFormLayout.LabelRole, self.horizontalSpacer_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.formLayout.setItem(8, QFormLayout.LabelRole, self.horizontalSpacer_3)

        self.status_release_control = QLabel(self.tab)
        self.status_release_control.setObjectName(u"status_release_control")
        self.status_release_control.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_release_control.setWordWrap(True)
        self.status_release_control.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.status_release_control)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.formLayout.setItem(6, QFormLayout.LabelRole, self.horizontalSpacer_4)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.formLayout.setItem(5, QFormLayout.LabelRole, self.horizontalSpacer_5)

        self.button_request_control = QPushButton(self.tab)
        self.button_request_control.setObjectName(u"button_request_control")
        self.button_request_control.setEnabled(False)
        self.button_request_control.setMinimumSize(QSize(0, 40))

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.button_request_control)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.formLayout.setItem(7, QFormLayout.LabelRole, self.horizontalSpacer_6)

        self.status_request_control = QLabel(self.tab)
        self.status_request_control.setObjectName(u"status_request_control")
        self.status_request_control.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_request_control.setWordWrap(True)
        self.status_request_control.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.status_request_control)

        self.button_release_control = QPushButton(self.tab)
        self.button_release_control.setObjectName(u"button_release_control")
        self.button_release_control.setEnabled(False)
        self.button_release_control.setMinimumSize(QSize(0, 40))

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.button_release_control)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_3 = QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.button_get_templates = QPushButton(self.tab_2)
        self.button_get_templates.setObjectName(u"button_get_templates")
        self.button_get_templates.setEnabled(False)

        self.verticalLayout_3.addWidget(self.button_get_templates)

        self.table_templates = QTableWidget(self.tab_2)
        if (self.table_templates.columnCount() < 3):
            self.table_templates.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_templates.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_templates.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_templates.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table_templates.setObjectName(u"table_templates")
        self.table_templates.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_templates.setProperty("showDropIndicator", False)
        self.table_templates.setDragDropOverwriteMode(False)
        self.table_templates.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.verticalLayout_3.addWidget(self.table_templates)

        self.button_open_template = QPushButton(self.tab_2)
        self.button_open_template.setObjectName(u"button_open_template")
        self.button_open_template.setEnabled(False)

        self.verticalLayout_3.addWidget(self.button_open_template)

        self.status_open_template = QLabel(self.tab_2)
        self.status_open_template.setObjectName(u"status_open_template")
        self.status_open_template.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_open_template.setWordWrap(True)
        self.status_open_template.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.status_open_template)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.button_start_template = QPushButton(self.tab_2)
        self.button_start_template.setObjectName(u"button_start_template")
        self.button_start_template.setEnabled(False)
        self.button_start_template.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.button_start_template.setFont(font)

        self.horizontalLayout_2.addWidget(self.button_start_template)

        self.button_stop_template = QPushButton(self.tab_2)
        self.button_stop_template.setObjectName(u"button_stop_template")
        self.button_stop_template.setEnabled(False)
        self.button_stop_template.setMinimumSize(QSize(0, 50))
        self.button_stop_template.setFont(font)

        self.horizontalLayout_2.addWidget(self.button_stop_template)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.status_start_stop_template = QLabel(self.tab_2)
        self.status_start_stop_template.setObjectName(u"status_start_stop_template")
        self.status_start_stop_template.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_start_stop_template.setWordWrap(True)
        self.status_start_stop_template.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout_3.addWidget(self.status_start_stop_template)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.formLayout_2 = QFormLayout(self.tab_5)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_6 = QLabel(self.tab_5)
        self.label_6.setObjectName(u"label_6")
        font1 = QFont()
        font1.setBold(True)
        self.label_6.setFont(font1)

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.formLayout_2.setItem(0, QFormLayout.FieldRole, self.horizontalSpacer_7)

        self.label_7 = QLabel(self.tab_5)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.combo_get_parameter_choice = QComboBox(self.tab_5)
        self.combo_get_parameter_choice.setObjectName(u"combo_get_parameter_choice")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.combo_get_parameter_choice)

        self.button_get_parameter = QPushButton(self.tab_5)
        self.button_get_parameter.setObjectName(u"button_get_parameter")
        self.button_get_parameter.setEnabled(False)
        self.button_get_parameter.setMinimumSize(QSize(0, 40))

        self.formLayout_2.setWidget(2, QFormLayout.SpanningRole, self.button_get_parameter)

        self.status_get_parameter = QLabel(self.tab_5)
        self.status_get_parameter.setObjectName(u"status_get_parameter")
        self.status_get_parameter.setWordWrap(True)
        self.status_get_parameter.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout_2.setWidget(3, QFormLayout.SpanningRole, self.status_get_parameter)

        self.line_3 = QFrame(self.tab_5)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMinimumSize(QSize(0, 0))
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(4, QFormLayout.SpanningRole, self.line_3)

        self.label_8 = QLabel(self.tab_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_8)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.formLayout_2.setItem(5, QFormLayout.FieldRole, self.horizontalSpacer_8)

        self.label_9 = QLabel(self.tab_5)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_9)

        self.combo_set_parameter_choice = QComboBox(self.tab_5)
        self.combo_set_parameter_choice.setObjectName(u"combo_set_parameter_choice")

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.combo_set_parameter_choice)

        self.button_set_parameter = QPushButton(self.tab_5)
        self.button_set_parameter.setObjectName(u"button_set_parameter")
        self.button_set_parameter.setEnabled(False)
        self.button_set_parameter.setMinimumSize(QSize(0, 40))

        self.formLayout_2.setWidget(8, QFormLayout.SpanningRole, self.button_set_parameter)

        self.status_set_parameter = QLabel(self.tab_5)
        self.status_set_parameter.setObjectName(u"status_set_parameter")
        self.status_set_parameter.setWordWrap(True)
        self.status_set_parameter.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout_2.setWidget(9, QFormLayout.SpanningRole, self.status_set_parameter)

        self.label_10 = QLabel(self.tab_5)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.label_10)

        self.field_parameter_value = QLineEdit(self.tab_5)
        self.field_parameter_value.setObjectName(u"field_parameter_value")

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.field_parameter_value)

        self.tabWidget.addTab(self.tab_5, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.horizontalLayout.addWidget(self.AccessiClient)

        self.SubPrograms = QFrame(self.centralwidget)
        self.SubPrograms.setObjectName(u"SubPrograms")
        self.SubPrograms.setFrameShape(QFrame.Shape.Box)
        self.SubPrograms.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.SubPrograms)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.SubPrograms)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.line_2 = QFrame(self.SubPrograms)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.tabWidget_2 = QTabWidget(self.SubPrograms)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.formLayout_3 = QFormLayout(self.tab_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.check_websocket_active = QCheckBox(self.tab_3)
        self.check_websocket_active.setObjectName(u"check_websocket_active")
        self.check_websocket_active.setEnabled(False)
        self.check_websocket_active.setChecked(True)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.check_websocket_active)

        self.check_websocket_output = QCheckBox(self.tab_3)
        self.check_websocket_output.setObjectName(u"check_websocket_output")
        self.check_websocket_output.setEnabled(False)
        self.check_websocket_output.setCheckable(True)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.check_websocket_output)

        self.check_websocket_save = QCheckBox(self.tab_3)
        self.check_websocket_save.setObjectName(u"check_websocket_save")
        self.check_websocket_save.setEnabled(False)

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.check_websocket_save)

        self.status_websocket_image = QLabel(self.tab_3)
        self.status_websocket_image.setObjectName(u"status_websocket_image")
        self.status_websocket_image.setWordWrap(True)
        self.status_websocket_image.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.status_websocket_image)

        self.line_5 = QFrame(self.tab_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_3.setWidget(3, QFormLayout.SpanningRole, self.line_5)

        self.check_cnn_active = QCheckBox(self.tab_3)
        self.check_cnn_active.setObjectName(u"check_cnn_active")
        self.check_cnn_active.setEnabled(False)

        self.formLayout_3.setWidget(4, QFormLayout.LabelRole, self.check_cnn_active)

        self.check_cnn_output = QCheckBox(self.tab_3)
        self.check_cnn_output.setObjectName(u"check_cnn_output")
        self.check_cnn_output.setEnabled(False)

        self.formLayout_3.setWidget(4, QFormLayout.FieldRole, self.check_cnn_output)

        self.check_cnn_save = QCheckBox(self.tab_3)
        self.check_cnn_save.setObjectName(u"check_cnn_save")
        self.check_cnn_save.setEnabled(False)

        self.formLayout_3.setWidget(5, QFormLayout.LabelRole, self.check_cnn_save)

        self.status_cnn = QLabel(self.tab_3)
        self.status_cnn.setObjectName(u"status_cnn")
        self.status_cnn.setWordWrap(True)
        self.status_cnn.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout_3.setWidget(5, QFormLayout.FieldRole, self.status_cnn)

        self.line_6 = QFrame(self.tab_3)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_3.setWidget(6, QFormLayout.SpanningRole, self.line_6)

        self.check_guidewire_tracking_active = QCheckBox(self.tab_3)
        self.check_guidewire_tracking_active.setObjectName(u"check_guidewire_tracking_active")
        self.check_guidewire_tracking_active.setEnabled(False)

        self.formLayout_3.setWidget(7, QFormLayout.LabelRole, self.check_guidewire_tracking_active)

        self.check_tracking_output = QCheckBox(self.tab_3)
        self.check_tracking_output.setObjectName(u"check_tracking_output")
        self.check_tracking_output.setEnabled(False)

        self.formLayout_3.setWidget(7, QFormLayout.FieldRole, self.check_tracking_output)

        self.status_guidewire_tracking = QLabel(self.tab_3)
        self.status_guidewire_tracking.setObjectName(u"status_guidewire_tracking")
        self.status_guidewire_tracking.setWordWrap(True)
        self.status_guidewire_tracking.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout_3.setWidget(8, QFormLayout.SpanningRole, self.status_guidewire_tracking)

        self.check_tracking_move_slice = QCheckBox(self.tab_3)
        self.check_tracking_move_slice.setObjectName(u"check_tracking_move_slice")
        self.check_tracking_move_slice.setEnabled(False)

        self.formLayout_3.setWidget(9, QFormLayout.LabelRole, self.check_tracking_move_slice)

        self.status_move_mri_slice = QLabel(self.tab_3)
        self.status_move_mri_slice.setObjectName(u"status_move_mri_slice")
        self.status_move_mri_slice.setWordWrap(True)
        self.status_move_mri_slice.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout_3.setWidget(10, QFormLayout.SpanningRole, self.status_move_mri_slice)

        self.check_tracking_save = QCheckBox(self.tab_3)
        self.check_tracking_save.setObjectName(u"check_tracking_save")
        self.check_tracking_save.setEnabled(False)

        self.formLayout_3.setWidget(11, QFormLayout.LabelRole, self.check_tracking_save)

        self.line_7 = QFrame(self.tab_3)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_3.setWidget(12, QFormLayout.SpanningRole, self.line_7)

        self.check_collision_detection_active = QCheckBox(self.tab_3)
        self.check_collision_detection_active.setObjectName(u"check_collision_detection_active")
        self.check_collision_detection_active.setEnabled(False)

        self.formLayout_3.setWidget(14, QFormLayout.LabelRole, self.check_collision_detection_active)

        self.check_collision_output = QCheckBox(self.tab_3)
        self.check_collision_output.setObjectName(u"check_collision_output")
        self.check_collision_output.setEnabled(False)

        self.formLayout_3.setWidget(14, QFormLayout.FieldRole, self.check_collision_output)

        self.status_collision_detection = QLabel(self.tab_3)
        self.status_collision_detection.setObjectName(u"status_collision_detection")
        self.status_collision_detection.setWordWrap(True)
        self.status_collision_detection.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout_3.setWidget(15, QFormLayout.SpanningRole, self.status_collision_detection)

        self.check_cathbot_collision_feedback = QCheckBox(self.tab_3)
        self.check_cathbot_collision_feedback.setObjectName(u"check_cathbot_collision_feedback")
        self.check_cathbot_collision_feedback.setEnabled(False)

        self.formLayout_3.setWidget(16, QFormLayout.LabelRole, self.check_cathbot_collision_feedback)

        self.status_cathbot_feedback = QLabel(self.tab_3)
        self.status_cathbot_feedback.setObjectName(u"status_cathbot_feedback")
        self.status_cathbot_feedback.setWordWrap(True)
        self.status_cathbot_feedback.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByKeyboard|Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextBrowserInteraction|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.formLayout_3.setWidget(17, QFormLayout.SpanningRole, self.status_cathbot_feedback)

        self.check_collision_save = QCheckBox(self.tab_3)
        self.check_collision_save.setObjectName(u"check_collision_save")
        self.check_collision_save.setEnabled(False)

        self.formLayout_3.setWidget(18, QFormLayout.LabelRole, self.check_collision_save)

        self.line_4 = QFrame(self.tab_3)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_3.setWidget(19, QFormLayout.LabelRole, self.line_4)

        self.label_14 = QLabel(self.tab_3)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setEnabled(False)
        font2 = QFont()
        font2.setPointSize(8)
        font2.setItalic(True)
        self.label_14.setFont(font2)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_14.setWordWrap(True)
        self.label_14.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.formLayout_3.setWidget(13, QFormLayout.SpanningRole, self.label_14)

        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_4 = QVBoxLayout(self.tab_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_11 = QLabel(self.tab_4)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_3.addWidget(self.label_11)

        self.field_output_directory = QLineEdit(self.tab_4)
        self.field_output_directory.setObjectName(u"field_output_directory")

        self.horizontalLayout_3.addWidget(self.field_output_directory)

        self.button_select_output_dir = QPushButton(self.tab_4)
        self.button_select_output_dir.setObjectName(u"button_select_output_dir")
        self.button_select_output_dir.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.button_select_output_dir)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_13 = QLabel(self.tab_4)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_6.addWidget(self.label_13)

        self.combo_show_output_dimensions = QComboBox(self.tab_4)
        self.combo_show_output_dimensions.addItem("")
        self.combo_show_output_dimensions.addItem("")
        self.combo_show_output_dimensions.addItem("")
        self.combo_show_output_dimensions.addItem("")
        self.combo_show_output_dimensions.setObjectName(u"combo_show_output_dimensions")

        self.horizontalLayout_6.addWidget(self.combo_show_output_dimensions)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.line_8 = QFrame(self.tab_4)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_8)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, -1, 10)
        self.label_12 = QLabel(self.tab_4)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_7.addWidget(self.label_12)

        self.combo_accessi_image_format = QComboBox(self.tab_4)
        self.combo_accessi_image_format.addItem("")
        self.combo_accessi_image_format.addItem("")
        self.combo_accessi_image_format.setObjectName(u"combo_accessi_image_format")

        self.horizontalLayout_7.addWidget(self.combo_accessi_image_format)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.check_save_latency_data = QCheckBox(self.tab_4)
        self.check_save_latency_data.setObjectName(u"check_save_latency_data")

        self.verticalLayout_4.addWidget(self.check_save_latency_data)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.tabWidget_2.addTab(self.tab_4, "")

        self.verticalLayout_2.addWidget(self.tabWidget_2)


        self.horizontalLayout.addWidget(self.SubPrograms)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 700, 33))
        self.menuScanSuite = QMenu(self.menubar)
        self.menuScanSuite.setObjectName(u"menuScanSuite")
        self.menuCathBot_Settings = QMenu(self.menubar)
        self.menuCathBot_Settings.setObjectName(u"menuCathBot_Settings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuScanSuite.menuAction())
        self.menubar.addAction(self.menuCathBot_Settings.menuAction())
        self.menuScanSuite.addAction(self.actionOpen_3D_Scan_Suite)
        self.menuCathBot_Settings.addAction(self.actionOpen_CathBot_CAN_Interface)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Hub", None))
        self.actionOpen_3D_Scan_Suite.setText(QCoreApplication.translate("MainWindow", u"Open 3D Suite", None))
        self.actionLight.setText(QCoreApplication.translate("MainWindow", u"Light", None))
        self.actionDark.setText(QCoreApplication.translate("MainWindow", u"Dark", None))
        self.actionOpen_CathBot_CAN_Interface.setText(QCoreApplication.translate("MainWindow", u"Open CathBot CAN Interface", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Access-i Client", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"IP Address", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Client Name", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Version", None))
        self.button_register.setText(QCoreApplication.translate("MainWindow", u"Register", None))
        self.status_register.setText("")
        self.status_release_control.setText("")
        self.button_request_control.setText(QCoreApplication.translate("MainWindow", u"Request Control", None))
        self.status_request_control.setText("")
        self.button_release_control.setText(QCoreApplication.translate("MainWindow", u"Release Control", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Connect", None))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Templates", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Get Parameter", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Parameter", None))
        self.button_get_parameter.setText(QCoreApplication.translate("MainWindow", u"Get Parameter", None))
        self.status_get_parameter.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Set Parameter", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Parameter", None))
        self.button_set_parameter.setText(QCoreApplication.translate("MainWindow", u"Set Parameter", None))
        self.status_set_parameter.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Value", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Parameters", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Sub Programs", None))
        self.check_websocket_active.setText(QCoreApplication.translate("MainWindow", u"Access-i Websocket", None))
        self.check_websocket_output.setText(QCoreApplication.translate("MainWindow", u"Show Output", None))
        self.check_websocket_save.setText(QCoreApplication.translate("MainWindow", u"Save Websocket Images", None))
        self.status_websocket_image.setText("")
        self.check_cnn_active.setText(QCoreApplication.translate("MainWindow", u"CNN Active", None))
        self.check_cnn_output.setText(QCoreApplication.translate("MainWindow", u"Show Output", None))
        self.check_cnn_save.setText(QCoreApplication.translate("MainWindow", u"Save Images", None))
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
#if QT_CONFIG(tooltip)
        self.check_cathbot_collision_feedback.setToolTip(QCoreApplication.translate("MainWindow", u"Requires Ixxat USB-to-CAN to be connected, drivers installed.", None))
#endif // QT_CONFIG(tooltip)
        self.check_cathbot_collision_feedback.setText(QCoreApplication.translate("MainWindow", u"CathBot Haptic Feedback", None))
        self.status_cathbot_feedback.setText("")
        self.check_collision_save.setText(QCoreApplication.translate("MainWindow", u"Save Collision Images", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Must be set before launching 3D Suite to have an effect", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Modules", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Output Directory", None))
        self.button_select_output_dir.setText(QCoreApplication.translate("MainWindow", u"Choose...", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Show Output Dimensions", None))
        self.combo_show_output_dimensions.setItemText(0, QCoreApplication.translate("MainWindow", u"512x512", None))
        self.combo_show_output_dimensions.setItemText(1, QCoreApplication.translate("MainWindow", u"1024x1024", None))
        self.combo_show_output_dimensions.setItemText(2, QCoreApplication.translate("MainWindow", u"256x256", None))
        self.combo_show_output_dimensions.setItemText(3, QCoreApplication.translate("MainWindow", u"128x128", None))

        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Access-i Image Format", None))
        self.combo_accessi_image_format.setItemText(0, QCoreApplication.translate("MainWindow", u"raw16bit", None))
        self.combo_accessi_image_format.setItemText(1, QCoreApplication.translate("MainWindow", u"dicom", None))

        self.check_save_latency_data.setText(QCoreApplication.translate("MainWindow", u"Save Timing Data (Each module separately, sync to NTP!)", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Output Settings", None))
        self.menuScanSuite.setTitle(QCoreApplication.translate("MainWindow", u"3D Suite", None))
        self.menuCathBot_Settings.setTitle(QCoreApplication.translate("MainWindow", u"CathBot Settings", None))
    # retranslateUi

