import sys;

from PySide6.QtCore import QTimer

sys.path.append("./modules")
import time
from threading import Thread
import numpy as np
import vtk
from scan_suite_ui import Ui_ScanSuite
import modules.accessi_local as Access
from PySide6.QtWidgets import QApplication, QMainWindow
from modules.shared_methods import json_to_object, convert_websocket_data_to_image
import zmq
import pickle
from modules.ImageData import ImageData
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class ScanSuiteWindow(QMainWindow):
    def __init__(self, SUBSCRIBE_PORT=None, accessi_ip_address=None, accessi_version=None):
        super().__init__()
        self.ui = Ui_ScanSuite()
        self.ui.setupUi(self)
        self.SUBSCRIBE_PORT = SUBSCRIBE_PORT
        self.Access = Access
        self.registered = False
        self.Access.config.ip_address = accessi_ip_address
        self.Access.config.version = accessi_version
        self.ui.field_ip_address.setText(accessi_ip_address)
        self.ui.field_version.setText(accessi_version)
        self.ui.field_client_name.setText("ScanSuite")
        register = None
        try:
            register = self.Access.Authorization.register(name="UTwente", start_date="20231102", warn_date="20251002",
                                                          expire_date="20251102", system_id="152379",
                                                          hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D",
                                                          informal_name="ScanSuite")
        except:
            pass
        if register is None:
            print(f"ScanSuite Registering failed {register}")
        else:
            print(f"ScanSuite Register: {register}")
            self.registered = register.result.success
        self.vtk_widget = QVTKRenderWindowInteractor(self.ui.centralwidget)
        self.ui.centralwidget.layout().addWidget(self.vtk_widget)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.cube = self.create_cube()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(self.cube.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Create the MRI slice cube
        self.mri_slice = self.create_cube()
        self.mapper_mri_slice = vtk.vtkPolyDataMapper()
        self.mapper_mri_slice.SetInputConnection(self.mri_slice.GetOutputPort())
        self.actor_mri_slice = vtk.vtkActor()
        self.actor_mri_slice.SetMapper(self.mapper_mri_slice)
        self.renderer.AddActor(self.actor_mri_slice)

        axes = vtk.vtkAxesActor()
        axes.SetTotalLength(400, 400, 400)
        widget = vtk.vtkOrientationMarkerWidget()
        widget.SetOrientationMarker(axes)
        widget.SetViewport(0.0, 0.0, 0.4, 0.4)
        rgba = [0] * 4
        vtk.vtkNamedColors().GetColor('Carrot', rgba)
        widget.SetOutlineColor(rgba[0], rgba[1], rgba[2])

        self.renderer.AddActor(axes)
        self.renderer.SetBackground(0.1, 0.2, 0.4)
        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()
        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.interactor.Initialize()

        """
        Buttons
        """
        self.ui.button_scan.clicked.connect(self.scan)

        """
        Threads
        """
        self.slice_transform_thread_active = True
        self.slice_transform_thread = Thread(target=self.get_slice_transform_thread, daemon=True)
        self.slice_transform_thread.start()
        self.timer = QTimer()
        self.timer.timeout.connect(self.interactor.ReInitialize)
        self.timer.start(1000)

    def closeEvent(self, event):
        try:
            if self.registered:
                self.Access.TemplateExecution.stop()
                self.Access.HostControl.release_host_control()
                self.Access.Authorization.deregister()
        except:
            pass
        self.slice_transform_thread_active = False
        self.slice_transform_thread.join()
        self.renderer.RemoveAllViewProps()
        self.vtk_widget.GetRenderWindow().Finalize()
        del self.interactor
        self.vtk_widget.Finalize()
        QMainWindow.closeEvent(self, event)

    # def register(self):
    #     register = self.access_client.register(set_status_labels=False)
    #     if register is not None:
    #         if register.result.success:
    #             self.ui.button_scan.setEnabled(True)
    #             templates = self.access_client.Access.TemplateExecution.get_templates()
    #             if templates.result.success:
    #                 for template in templates.value:
    #                     self.ui.combo_select_template.addItem(template.label)
    #         else:
    #             self.ui.button_scan.setEnabled(False)

    def create_cube(self):
        # Create a cube
        cube = vtk.vtkCubeSource()
        cube.SetCenter(0, 0, 0)
        cube.SetXLength(200)
        cube.SetYLength(200)
        cube.SetZLength(200)
        return cube

    def scan(self):
        pass
        # control = self.access_client.Access.HostControl.request_host_control()
        # if control.result.success:
        #     self.ui.status_scan.setText(f"Request Control: {control.result.success}")
        # else:
        #     self.ui.status_scan.setText(f"Request Control Failed: {control.result.reason}")
        # templates = self.access_client.Access.TemplateExecution.get_templates().value
        # template_label = self.ui.combo_select_template.currentText()
        # template = next((item for item in templates if item.label == template_label), None)
        # if template.isInteractive:
        #     open_template = self.access_client.Access.TemplateModification.open(template.id)
        #     if open_template.result.success:
        #         self.ui.status_scan.setText(f"Template Open: {open_template.result.success}")
        #     else:
        #         self.ui.status_scan.setText(f"Template Open Failed: {open_template.result.reason}")
        # self.ui.status_scan.setText(f"Starting Scan")
        # self.access_client.Access.Image.set_image_format("dicom")
        # self.access_client.Access.TemplateExecution.start(template.id)
        # context = zmq.Context()
        # subscriber_socket = context.socket(zmq.SUB)
        # subscriber_socket.connect("tcp://127.0.0.1:" + str(self.SUBSCRIBE_PORT))
        # subscriber_socket.subscribe("")
        # # Sequence which is not interactive, cane be started x amount of times while changing plane in between.
        # while True:
        #     data = subscriber_socket.recv()
        #     image, metadata = convert_websocket_data_to_image(data)
        #     if "imageStream" in data.decode():
        #         break
        # self.access_client.Access.TemplateExecution.stop()
        # self.ui.status_scan.setText(f"Done, starting processing...")
        # self.access_client.Access.Image.set_image_format("raw16bit")
        # self.access_client.Access.TemplateExecution.stop()
        # self.access_client.Access.HostControl.release_host_control()
        # self.access_client.Access.Authorization.deregister()

    def convert_orientation_for_vtk(self, normal, phase, read):
        """
        Convert MRI slice orientation data to VTK rotation angles.
        """
        x_deg = np.degrees(np.arctan2(read.z, read.x))  # Rotation around x-axis
        y_deg = np.degrees(
            np.arctan2(-phase.y, np.sqrt(phase.x ** 2 + phase.z ** 2)))  # Rotation around y-axis
        z_deg = np.degrees(np.arctan2(normal.y, normal.x))  # Rotation around z-axis
        x_deg %= 360
        y_deg %= 360
        z_deg %= 360

        return x_deg, y_deg, z_deg

    def get_slice_transform_thread(self, update_frequency=1):
        """
        update_frequency: x times a second, time.sleep(1/update_frequency)
        Continuously acquires slice position and orientation data, and updates the 3D model.
        :return:
        """
        while self.slice_transform_thread_active:
            try:
                time.sleep(1 / update_frequency)
                active_status = self.Access.Remote.get_is_active()
                if active_status is not None and active_status.result.success:
                    position = self.Access.ParameterStandard.get_slice_position_dcs().value
                    orientation = self.Access.ParameterStandard.get_slice_orientation_dcs()
                    thickness = self.Access.ParameterStandard.get_slice_thickness().value
                    field_of_view = self.Access.ParameterStandard.get_field_of_view_read().value
                    orientation_vtk = self.convert_orientation_for_vtk(orientation.normal,
                                                                       orientation.phase,
                                                                       orientation.read)
                    self.set_mri_slice_transform(position=(position.x, position.y, position.z),
                                                 rotation=orientation_vtk,
                                                 length=(field_of_view, field_of_view, int(thickness)),
                                                 color=(1, 0, 0))
            except Exception as error:
                print(f"Error in slice transform thread: {error}")

    def set_mri_slice_transform(self, position: tuple = (0, 0, 0), rotation: tuple = (0, 0, 0),
                                length: tuple = (1, 1, 1),
                                color: tuple = (1, 1, 1), opacity: float = 0.5):

        self.actor_mri_slice.SetPosition(position[0], position[1], position[2])
        self.actor_mri_slice.SetOrientation(rotation[0], rotation[1], rotation[2])
        self.mri_slice.SetXLength(length[0])
        self.mri_slice.SetYLength(length[1])
        self.mri_slice.SetZLength(length[2])
        self.actor_mri_slice.GetProperty().SetColor(color)
        self.actor_mri_slice.GetProperty().SetOpacity(opacity)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScanSuiteWindow()
    window.show()
    sys.exit(app.exec())
