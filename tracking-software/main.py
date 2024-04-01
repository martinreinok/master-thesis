import sys; sys.path.append("./modules")
from typing import Literal
from threading import Thread
from main_ui import Ui_MainWindow
import modules.accessi_local as Access
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from modules.AccessiWebsocket import AccessiWebsocket
from modules.CNNModel import CNNModel
from modules.GuidewireTracking import GuidewireTracking
from modules.VideoViewer import VideoViewer
from modules.AccessiClient import AccessiClient
from scan_suite import ScanSuiteWindow as ScanSuite

"""
Live Server info:
(optional) route add 192.168.182.0 mask 255.255.255.0 192.168.182.1 if 47 -p
Access-i IP: 10.89.184.9
Version: v1

Access-i simulator info:
Access-i IP: 127.0.0.1
Version: v2

Client IP: 192.168.182.20
Subnet: 255.255.255.0
Gateway: 192.168.182.1
DNS1: 192.168.182.1
"""

DEVICE: Literal["cuda", "cpu"] = "cuda"
IP_ADDRESS_DEFAULT = "127.0.0.1"
VERSION_DEFAULT = "v2"
CLIENT_NAME_DEFAULT = "Martin Reinok Python Client"
OUTPUT_DIRECTORY_DEFAULT = "C:/Users/O/Desktop/Master Thesis/LOG_IMAGES/06.03.2024"
CNN_MODEL_DEFAULT = "MODEL_512_V3"


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scan_suite = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.table_templates.setColumnCount(3)
        self.output_path = None

        """
        Defaults
        """
        self.ui.field_ip_address.setText(IP_ADDRESS_DEFAULT)
        self.ui.field_version.setText(VERSION_DEFAULT)
        self.ui.field_client_name.setText(CLIENT_NAME_DEFAULT)
        self.ui.field_output_directory.setText(OUTPUT_DIRECTORY_DEFAULT)

        """
        Threads
        """
        self.websocket_thread = None
        self.tracking_thread = None
        self.cnn_thread = None

        """
        Modules
        """
        self.access_client: AccessiClient = AccessiClient(self.ui)
        self.accessi_websocket: AccessiWebsocket = AccessiWebsocket(access_instance=self.access_client.Access,
                                                                    window=self)
        self.cnn: CNNModel = CNNModel(window=self, subscribe_port=None, cnn_model=CNN_MODEL_DEFAULT)
        self.tracking: GuidewireTracking = GuidewireTracking(window=self, subscribe_port=None)
        self.accessi_websocket.status_websocket_signal.connect(self.update_websocket_status)

        """
        Buttons
        """
        self.ui.button_register.clicked.connect(self.access_client.register)
        self.ui.button_request_control.clicked.connect(self.access_client.request_control)
        self.ui.button_release_control.clicked.connect(self.access_client.release_control)
        self.ui.button_get_templates.clicked.connect(self.access_client.get_templates)
        self.ui.button_open_template.clicked.connect(self.access_client.open_template)
        self.ui.button_start_template.clicked.connect(self.access_client.start_template)
        self.ui.button_stop_template.clicked.connect(self.access_client.stop_template)
        self.ui.button_get_parameter.clicked.connect(self.access_client.get_parameter)
        self.ui.button_set_parameter.clicked.connect(self.access_client.set_parameter)
        self.ui.button_select_output_dir.clicked.connect(self.select_output_directory)
        self.ui.field_parameter_value.returnPressed.connect(self.access_client.set_parameter)
        self.ui.actionOpen_3D_Scan_Suite.triggered.connect(self.open_scan_suite)

        """
        Checkboxes
        """
        self.ui.check_websocket_active.stateChanged.connect(self.set_websocket_active)
        self.ui.check_cnn_active.stateChanged.connect(self.set_cnn_active)
        self.ui.check_websocket_output.stateChanged.connect(self.show_websocket_output)
        self.ui.check_cnn_output.stateChanged.connect(self.show_cnn_output)
        self.ui.check_tracking_output.stateChanged.connect(self.show_tracking_output)
        self.ui.check_guidewire_tracking_active.stateChanged.connect(self.set_tracking_active)
        self.ui.check_tracking_move_slice.stateChanged.connect(self.set_tracking_move_slice)

        """
        Combo
        """
        for method in [method for method in dir(Access.ParameterStandard) if
                       callable(getattr(Access.ParameterStandard, method)) and method.startswith("get_")]:
            self.ui.combo_get_parameter_choice.addItem(method)

        for method in [method for method in dir(Access.ParameterStandard) if
                       callable(getattr(Access.ParameterStandard, method)) and method.startswith("set_")]:
            self.ui.combo_set_parameter_choice.addItem(method)

    def set_websocket_active(self):
        if self.ui.check_websocket_active.isChecked():
            if self.websocket_thread is None:
                self.websocket_thread = Thread(target=self.accessi_websocket.run_websocket_thread, daemon=True)
                self.websocket_thread.start()
            for checkbox in [self.ui.check_websocket_output, self.ui.check_websocket_save, self.ui.check_cnn_active]:
                checkbox.setEnabled(True)
                checkbox.stateChanged.emit(checkbox.isChecked())
            self.ui.check_websocket_active.setEnabled(False)
        else:
            self.websocket_thread = None

    def set_cnn_active(self):
        if self.ui.check_cnn_active.isChecked():
            self.cnn = CNNModel(window=self, subscribe_port=self.accessi_websocket.PUBLISH_PORT)
            self.cnn.status_cnn_signal.connect(self.update_cnn_status)
            self.cnn_thread = Thread(target=self.cnn.start, daemon=True, args=[DEVICE])
            self.cnn_thread.start()
            # Checkboxes are toggled in the thread due to long imports.
        else:
            self.cnn_thread = None

    def set_tracking_active(self):
        if self.ui.check_guidewire_tracking_active.isChecked():
            self.tracking = GuidewireTracking(window=self, subscribe_port=self.cnn.PUBLISH_PORT)
            self.tracking.status_guidewire_tracking_signal.connect(self.update_guidewire_tracking_status)
            self.tracking.status_move_slice_signal.connect(self.update_move_mri_slice_status)
            self.tracking_thread = Thread(target=self.tracking.start, daemon=True)
            self.tracking_thread.start()
            for checkbox in [self.ui.check_tracking_output]:
                checkbox.setEnabled(True)
                checkbox.stateChanged.emit(checkbox.isChecked())
        else:
            self.tracking_thread = None

    def open_scan_suite(self):
        self.scan_suite = ScanSuite(accessi_ip_address=self.ui.field_ip_address.text(),
                                    accessi_version=self.ui.field_version.text(),
                                    SUBSCRIBE_PORT=self.tracking.RAW_COORDINATE_PUBLISH_PORT)

    def show_websocket_output(self):
        if self.ui.check_websocket_output.isChecked():
            viewer = VideoViewer(window=self, zmq_port=self.accessi_websocket.PUBLISH_PORT, window_name="MRI Image",
                                 checkbox=self.ui.check_websocket_output, websocket_dataformat=True,
                                 save_images_button=self.ui.check_websocket_save, save_images_folder="Websocket")
            Thread(target=viewer.start, daemon=True).start()

    def show_cnn_output(self):
        if self.ui.check_cnn_output.isChecked():
            viewer = VideoViewer(window=self, zmq_port=self.cnn.PUBLISH_PORT, window_name="CNN Prediction",
                                 checkbox=self.ui.check_cnn_output,
                                 save_images_button=self.ui.check_cnn_save, save_images_folder="CNN")
            Thread(target=viewer.start, daemon=True).start()

    def show_tracking_output(self):
        if self.ui.check_tracking_output.isChecked():
            viewer = VideoViewer(window=self, zmq_port=self.tracking.PUBLISH_PORT, window_name="Guidewire Tracking",
                                 checkbox=self.ui.check_tracking_output,
                                 save_images_button=self.ui.check_tracking_save, save_images_folder="Tracking")
            Thread(target=viewer.start, daemon=True).start()

    def set_tracking_move_slice(self):
        self.tracking.move_slice = self.ui.check_tracking_move_slice.isChecked()

    def update_guidewire_tracking_status(self, status):
        self.ui.status_guidewire_tracking.setText(status)

    def update_websocket_status(self, status):
        self.ui.status_websocket_image.setText(status)

    def update_cnn_status(self, status):
        self.ui.status_cnn.setText(status)

    def update_move_mri_slice_status(self, status):
        self.ui.status_move_mri_slice.setText(status)

    def closeEvent(self, event):
        try:
            if self.access_client.registered:
                self.access_client.stop_template()
                self.access_client.release_control()
                self.access_client.Access.Authorization.deregister()
        except:
            pass
        if self.scan_suite is not None:
            self.scan_suite.close()
        QMainWindow.closeEvent(self, event)

    def select_output_directory(self):
        directory = select_directory()
        self.ui.field_output_directory.setText(directory)


def select_directory():
    file_dialog = QFileDialog()
    directory_path = file_dialog.getExistingDirectory(None, "Select Directory", "")
    return directory_path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
