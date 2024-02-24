from random import random

import cv2
import sys
import zmq
import json
import math
import base64
import pickle
import asyncio
import numpy as np
import trackpy as tp
from typing import Literal
from threading import Thread
from datetime import datetime
from QtUI import Ui_MainWindow
import accessi_local as Access
from types import SimpleNamespace
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from PySide6.QtCore import Signal, QObject

DEVICE: Literal["cuda", "cpu"] = "cuda"


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.table_templates.setColumnCount(3)
        self.output_path = None

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
        self.accessi_websocket: AccessiWebsocket = AccessiWebsocket()
        self.cnn: CNNModel = CNNModel(None)
        self.tracking: GuidewireTracking = GuidewireTracking(None)
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

        """
        Checkboxes
        """
        self.ui.check_websocket_active.stateChanged.connect(self.set_websocket_active)
        self.ui.check_websocket_save.stateChanged.connect(self.set_save_websocket_output)
        self.ui.check_cnn_save.stateChanged.connect(self.set_save_cnn_output)
        self.ui.check_tracking_save.stateChanged.connect(self.set_save_tracking_output)
        self.ui.check_collision_save.stateChanged.connect(self.set_save_collision_output)
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
            self.cnn = CNNModel(self.accessi_websocket.PUBLISH_PORT)
            self.cnn.status_cnn_signal.connect(self.update_cnn_status)
            self.cnn_thread = Thread(target=self.cnn.start, daemon=True)
            self.cnn_thread.start()
            # Checkboxes are toggled in the thread due to long imports.
        else:
            self.cnn_thread = None

    def set_tracking_active(self):
        if self.ui.check_guidewire_tracking_active.isChecked():
            self.tracking = GuidewireTracking(self.cnn.PUBLISH_PORT)
            self.tracking.status_guidewire_tracking_signal.connect(self.update_guidewire_tracking_status)
            self.tracking.status_move_slice_signal.connect(self.update_move_mri_slice_status)
            self.tracking_thread = Thread(target=self.tracking.start, daemon=True)
            self.tracking_thread.start()
            for checkbox in [self.ui.check_tracking_output]:
                checkbox.setEnabled(True)
                checkbox.stateChanged.emit(checkbox.isChecked())
        else:
            self.tracking_thread = None

    def show_websocket_output(self):
        if self.ui.check_websocket_output.isChecked():
            viewer = VideoViewer(zmq_port=self.accessi_websocket.PUBLISH_PORT, window_name="MRI Image",
                                 checkbox=self.ui.check_websocket_output, websocket_dataformat=True)
            Thread(target=viewer.start, daemon=True).start()

    def show_cnn_output(self):
        if self.ui.check_cnn_output.isChecked():
            viewer = VideoViewer(zmq_port=self.cnn.PUBLISH_PORT, window_name="CNN Prediction",
                                 checkbox=self.ui.check_cnn_output)
            Thread(target=viewer.start, daemon=True).start()

    def show_tracking_output(self):
        if self.ui.check_tracking_output.isChecked():
            viewer = VideoViewer(zmq_port=self.tracking.PUBLISH_PORT, window_name="Guidewire Tracking",
                                 checkbox=self.ui.check_tracking_output)
            Thread(target=viewer.start, daemon=True).start()

    def set_save_websocket_output(self):
        if self.ui.check_websocket_save.isChecked():
            pass

    def set_save_cnn_output(self):
        state = self.ui.check_cnn_save.isChecked()

    def set_save_tracking_output(self):
        state = self.ui.check_tracking_save.isChecked()

    def set_save_collision_output(self):
        state = self.ui.check_collision_save.isChecked()

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
        QMainWindow.closeEvent(self, event)

    def select_output_directory(self):
        directory = select_directory()
        self.ui.field_output_directory.setText(directory)


class AccessiClient:

    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.Access = Access
        self.template_id = None
        self.registered = False

    def register(self):
        ip_address = self.ui.field_ip_address.text()
        client_name = self.ui.field_client_name.text()
        version = self.ui.field_version.text()
        if all(field is not None for field in [ip_address, client_name, version]):
            self.Access.config.ip_address = self.ui.field_ip_address.text()
            self.Access.config.version = version
            self.Access.config.timeout = 8
            try:
                reg = self.Access.Authorization.register(name="UTwente", start_date="20231102", warn_date="20251002",
                                                         expire_date="20251102", system_id="152379",
                                                         hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D",
                                                         informal_name=client_name)
            except Exception as error:
                self.ui.status_register.setStyleSheet("color: red")
                self.ui.status_register.setText(str(error))
                return
            if reg.result.success:
                self.ui.status_register.setStyleSheet("color: green")
                self.ui.status_register.setText(f"{reg.result.success}, privilege: {reg.privilegeLevel}")
                self.ui.button_request_control.setEnabled(True)
                self.ui.button_get_templates.setEnabled(True)
                self.ui.button_get_parameter.setEnabled(True)
                self.ui.button_set_parameter.setEnabled(True)
                self.ui.check_websocket_active.setEnabled(True)
                self.ui.check_websocket_active.stateChanged.emit(self.ui.check_websocket_active.isChecked())
                self.registered = True
            else:
                self.ui.status_register.setStyleSheet("color: red")
                self.ui.status_register.setText(f"{reg.result.success}, reason: {reg.result.reason}")

    def request_control(self):
        status = self.Access.HostControl.get_state()
        if status.result.success and status.value.canRequestControl:
            control = self.Access.HostControl.request_host_control()
            if control.result.success:
                self.ui.status_request_control.setStyleSheet("color: green")
                self.ui.status_request_control.setText(f"{control.result.success}")
                self.ui.button_release_control.setEnabled(True)
            else:
                self.ui.status_request_control.setStyleSheet("color: red")
                self.ui.status_request_control.setText(f"{control.reason}")
        else:
            self.ui.status_request_control.setStyleSheet("color: red")
            self.ui.status_request_control.setText(f"{status.value.cannotRequestControlReason}")
        self.Access.HostControl.request_host_control()

    def release_control(self):
        status = self.Access.HostControl.get_state()
        if status.result.success and status.value.canReleaseControl:
            control = self.Access.HostControl.release_host_control()
            if control.result.success:
                self.ui.status_release_control.setStyleSheet("color: green")
                self.ui.status_release_control.setText(f"{control.result.success}")
            else:
                self.ui.status_release_control.setStyleSheet("color: red")
                self.ui.status_release_control.setText(f"{control.reason}")

    def get_templates(self):
        templates = self.Access.TemplateExecution.get_templates()
        if templates.result.success:
            for row, template in enumerate(templates.value):
                if row >= self.ui.table_templates.rowCount():
                    self.ui.table_templates.insertRow(row)
                self.ui.table_templates.setItem(row, 0, QTableWidgetItem(template.label))
                self.ui.table_templates.setItem(row, 1, QTableWidgetItem(str(template.isInteractive)))
                self.ui.table_templates.setItem(row, 2, QTableWidgetItem(template.id))
        self.ui.button_open_template.setEnabled(True)

    def open_template(self):
        template = self.ui.table_templates.selectedItems()
        if template:
            self.template_id = template[2].text()
            open_template = self.Access.TemplateModification.open(self.template_id)
            if open_template.result.success:
                self.ui.status_open_template.setStyleSheet("color: green")
                self.ui.status_open_template.setText(f"{open_template.result.success}: {template[0].text()}")
                self.ui.button_start_template.setEnabled(True)
                self.ui.button_stop_template.setEnabled(True)
            else:
                self.ui.status_open_template.setStyleSheet("color: red")
                self.ui.status_open_template.setText(f"{open_template.result.reason}")

    def start_template(self):
        if self.template_id:
            try:
                start = self.Access.TemplateExecution.start(self.template_id)
                if start.result.success:
                    self.ui.status_start_stop_template.setStyleSheet("color: green")
                    self.ui.status_start_stop_template.setText(f"Start: {start.result.success}")
                else:
                    self.ui.status_start_stop_template.setStyleSheet("color: red")
                    self.ui.status_start_stop_template.setText(f"Start: {start.result.reason}")
            except Exception as err:
                self.ui.status_start_stop_template.setStyleSheet("color: red")
                self.ui.status_start_stop_template.setText(f"Error: {err}")

    def stop_template(self):
        stop = self.Access.TemplateExecution.stop()
        if self.Access.TemplateExecution.get_state().value.canStop:
            if stop.result.success:
                self.ui.status_start_stop_template.setStyleSheet("color: green")
                self.ui.status_start_stop_template.setText(f"Stop: {stop.result.success}")
            else:
                self.ui.status_start_stop_template.setStyleSheet("color: red")
                self.ui.status_start_stop_template.setText(f"Stop: {stop.result.reason}")
        self.Access.TemplateModification.close()

    def get_parameter(self):
        parameter = self.ui.combo_get_parameter_choice.currentText()
        try:
            answer = getattr(self.Access.ParameterStandard, parameter)()
            self.Access.ParameterStandard.get_slice_position_dcs()
            if answer.result.success:
                del answer.result
                value = ""
                for attr_name, attr_value in answer.__dict__.items():
                    value += f"{attr_name}: {getattr(answer, attr_name)}\n"
                self.ui.status_get_parameter.setText(f"{value}")
            else:
                self.ui.status_get_parameter.setText(f"{answer.result.reason}")
        except Exception as err:
            self.ui.status_get_parameter.setText(f"Error: {err}")

    def set_parameter(self):
        parameter = self.ui.combo_set_parameter_choice.currentText()
        try:
            val = [float(num.strip()) for num in self.ui.field_parameter_value.text().split(",")]
            if len(val) >= 9:
                val_tuples = [(val[i], val[i + 1], val[i + 2]) for i in range(0, 9, 3)]
                answer = getattr(self.Access.ParameterStandard, parameter)(*val_tuples)
            else:
                answer = getattr(self.Access.ParameterStandard, parameter)(*val)
            if answer.result.success:
                self.ui.status_set_parameter.setText(f"valueSet: {answer.valueSet}")
            else:
                self.ui.status_set_parameter.setText(f"{answer.result.reason}")
        except Exception as err:
            self.ui.status_set_parameter.setText(f"Error: {err}")


class AccessiWebsocket(QObject):
    status_websocket_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.PUBLISH_PORT = None

    async def get_websocket_data(self, connected_event: asyncio.Event):
        async with await Access.connect_websocket() as websocket:
            connected_event.set()
            context = zmq.Context()
            publisher_socket = context.socket(zmq.PUB)
            self.PUBLISH_PORT = publisher_socket.bind_to_random_port("tcp://127.0.0.1")
            while True:
                try:
                    message = await websocket.recv()
                    decoded_message = json.dumps(Access.handle_websocket_message(message)).encode()
                    publisher_socket.send(decoded_message)
                    _, metadata = convert_websocket_data_to_image(decoded_message)
                    self.status_websocket_signal.emit(f"Latency: {calculate_latency(metadata)}s")
                except Exception as err:
                    if "received 1000 (OK); then sent 1000 (OK)" not in str(err):
                        print(f"Websocket error: {err}")

    async def main(self):
        try:
            # Run websocket
            websocket_connected_event = asyncio.Event()
            asyncio.create_task(self.get_websocket_data(connected_event=websocket_connected_event))
            await websocket_connected_event.wait()
            image_service = Access.Image.connect_to_default_web_socket()
            print(f"Access-i ImageServiceConnection: {image_service}")
            Access.Image.set_image_format("raw16bit")
            while window.ui.check_websocket_active.isChecked():
                await asyncio.sleep(0.05)
        except Exception as error:
            print("An error occurred:", error)

    def run_websocket_thread(self):
        try:
            asyncio.run(self.main())
        except Exception as error:
            print(error)


class VideoViewer:
    def __init__(self, zmq_port, window_name, checkbox, websocket_dataformat=False):
        self.zmq_port = zmq_port
        self.window_name = window_name
        self.checkbox = checkbox
        self.websocket = websocket_dataformat

    def start(self):
        if self.zmq_port is None:
            print("Output not available yet.")
            self.checkbox.setChecked(False)
            return
        context = zmq.Context()
        subscriber_socket = context.socket(zmq.SUB)
        subscriber_socket.connect("tcp://127.0.0.1:" + str(self.zmq_port))
        subscriber_socket.subscribe("")
        subscriber_socket.RCVTIMEO = 200

        while self.checkbox.isChecked():
            try:
                data = subscriber_socket.recv()
                if self.websocket:
                    image, _ = convert_websocket_data_to_image(data)
                    if image is None:
                        cv2.waitKey(1)
                        continue
                else:
                    imagedata: ImageData = pickle.loads(data)
                    image = imagedata.image
                selected_resolution_text = window.ui.combo_show_output_dimensions.currentText()
                width, height = map(int, selected_resolution_text.split('x'))
                resized_image = cv2.resize(image, (width, height))
                cv2.imshow(self.window_name, resized_image)
                cv2.waitKey(1)
            except zmq.error.Again:
                cv2.waitKey(1)
                continue
            except Exception as e:
                cv2.waitKey(1)
                print(f"Error: {e}")
                break
        else:
            try:
                cv2.destroyWindow(self.window_name)
            except:
                pass


class ImageData:
    def __init__(self, image_data=None, metadata=None):
        self.image = image_data
        self.metadata = metadata


class CNNModel(QObject):
    status_cnn_signal = Signal(str)

    def __init__(self, subscribe_port):
        super().__init__()
        self.PUBLISH_PORT = None
        self.SUBSCRIBE_PORT = subscribe_port
        self.path_to_model_directory = "MODEL_512"
        self.checkpoint_name = "checkpoint_final.pth"
        self.folds = (4,)
        self.model = None

    def prepare_cnn(self, torch, nnUNetPredictor, path_to_model_directory, checkpoint_name, folds):
        """
        Returns the model which is prepared to predict.
        """
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        predictor = nnUNetPredictor(tile_step_size=1, use_gaussian=True, use_mirroring=True,
                                    perform_everything_on_gpu=True, device=torch.device(DEVICE, 0),
                                    verbose=False, verbose_preprocessing=False, allow_tqdm=False)
        predictor.initialize_from_trained_model_folder(path_to_model_directory, checkpoint_name=checkpoint_name,
                                                       use_folds=folds)
        return predictor

    def predict(self, image_data):
        try:
            image = cv2.resize(image_data, (350, 350)).astype(np.float32) / 255.0
            cnn_input = image.reshape(1, 1, image.shape[0], image.shape[1])
            props = {'spacing': (999, 1, 1)}
            return self.model.predict_single_npy_array(cnn_input, props, None, None, False)[0]

        except Exception as error:
            print(f"Error occurred in prediction: {error}")
        return None

    def start(self):
        # imports are here because they take a long time. They are in a separate thread.
        import torch
        from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
        context = zmq.Context()
        subscriber_socket = context.socket(zmq.SUB)
        subscriber_socket.setsockopt(zmq.CONFLATE, 1)
        subscriber_socket.connect("tcp://127.0.0.1:" + str(self.SUBSCRIBE_PORT))
        subscriber_socket.subscribe("")
        publisher_socket = context.socket(zmq.PUB)
        self.PUBLISH_PORT = publisher_socket.bind_to_random_port("tcp://127.0.0.1")
        self.model = self.prepare_cnn(torch=torch, nnUNetPredictor=nnUNetPredictor,
                                      path_to_model_directory=self.path_to_model_directory, folds=self.folds,
                                      checkpoint_name=self.checkpoint_name)
        for checkbox in [window.ui.check_cnn_output, window.ui.check_cnn_save,
                         window.ui.check_guidewire_tracking_active,
                         window.ui.check_tracking_move_slice, window.ui.check_collision_detection_active,
                         window.ui.check_cathbot_collision_feedback, window.ui.check_collision_save,
                         window.ui.check_tracking_save]:
            checkbox.setEnabled(True)
            checkbox.stateChanged.emit(checkbox.isChecked())
        while window.ui.check_cnn_active.isChecked():
            data = subscriber_socket.recv()
            image, metadata = convert_websocket_data_to_image(data)
            if image is None:
                continue
            output_image = self.predict(image)
            if output_image is not None:
                output_image = (output_image * 255).astype(np.uint8)
                output = ImageData(image_data=output_image, metadata=metadata)
                publisher_socket.send(pickle.dumps(output))
                self.status_cnn_signal.emit(f"Latency: {calculate_latency(metadata)}s")


class ArtifactTracker:
    """
    Did not manage to get any existing trackers to work, so why not just reinvent the wheel...
    """

    def __init__(self, initial_coordinate, artifact_id, max_range=30):
        self.max_range = max_range
        self.coordinates = initial_coordinate
        self.trajectory = [initial_coordinate]
        self.movement_vector = [0, 0]
        self.id = artifact_id
        self.color = (random() * 255, random() * 255, random() * 255)
        self.track_lost = 0

    def update(self, new_coordinates):
        """
        Find the closest coordinate within max_range
        """
        closest_coordinate = None
        min_distance = float('inf')
        for coord in new_coordinates:
            dist = self.distance(coord)
            if dist < min_distance and dist <= self.max_range:
                closest_coordinate = coord
                min_distance = dist
        if closest_coordinate is not None:
            self.track_lost = 0
            previous_coordinates = self.coordinates
            self.coordinates = closest_coordinate
            self.trajectory.append(closest_coordinate)
            self.movement_vector = self.calculate_movement_vector(previous_coordinates)
        else:
            self.track_lost += 1

    def calculate_movement_vector(self, previous_coordinates):
        """
        Calculate the movement vector from previous coordinates to new coordinates and normalize it.
        """
        return np.array(self.coordinates) - np.array(previous_coordinates)

    def distance(self, coordinate):
        """
        Calculate the Euclidean distance between two coordinates.
        """
        return math.sqrt((coordinate[0] - self.coordinates[0]) ** 2 + (coordinate[1] - self.coordinates[1]) ** 2)


class GuidewireTracking(QObject):
    status_guidewire_tracking_signal = Signal(str)
    status_move_slice_signal = Signal(str)

    def __init__(self, subscribe_port):
        super().__init__()
        self.PUBLISH_PORT = None
        self.SUBSCRIBE_PORT = subscribe_port
        self.move_slice = False
        self.MRI: Access.ParameterStandard = Access.ParameterStandard()
        self.voxel_size = None
        self.subscriber_socket = None
        self.publisher_socket = None
        self.previous_positions = None

    @staticmethod
    def find_artifact_centroids(image, gaussian_kernel: int = 9):
        """
        Applies gaussian blur and thresholding to separate artifacts from noise.
        The center of gravity of each remaining blob is returned.
        """
        blurred = cv2.GaussianBlur(image, (gaussian_kernel, gaussian_kernel), 0)
        _, threshold = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        threshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2RGB)
        centroids = []
        if len(contours) > 0:
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    centroids.append((cX, cY))
                    cv2.circle(threshold, (cX, cY), 3, (0, 255, 0), -1)
        return centroids, threshold

    def convert_px_to_mm(self, px, metadata):
        if self.voxel_size is None:
            self.voxel_size = metadata.value.image.dimensions.voxelSize.column
        return self.voxel_size * px

    def start(self, movement_threshold_mm=2):
        context = zmq.Context()
        self.subscriber_socket = context.socket(zmq.SUB)
        self.subscriber_socket.setsockopt(zmq.CONFLATE, 1)
        self.subscriber_socket.connect("tcp://127.0.0.1:" + str(self.SUBSCRIBE_PORT))
        self.subscriber_socket.subscribe("")
        self.publisher_socket = context.socket(zmq.PUB)
        self.PUBLISH_PORT = self.publisher_socket.bind_to_random_port("tcp://127.0.0.1")
        tracker_id = 0
        trackers = []
        while window.ui.check_guidewire_tracking_active.isChecked():
            data = self.subscriber_socket.recv()
            prediction: ImageData = pickle.loads(data)
            if prediction.image is None:
                continue
            centroids, threshold = self.find_artifact_centroids(prediction.image)
            for tracker in trackers:
                tracker.update(centroids)
                if tracker.coordinates in centroids:
                    centroids.remove(tracker.coordinates)
                # Erase tracker if it has lost marker for more than 5 frames
                trackers = [tracker for tracker in trackers if tracker.track_lost <= 5]
            if len(centroids) > 0:
                for centroid in centroids:
                    trackers.append(ArtifactTracker(centroid, tracker_id))
                    tracker_id += 1
            average_movement = []
            for tracker in trackers:
                for coordinate in tracker.trajectory:
                    cv2.circle(threshold, coordinate, 2, color=tracker.color, thickness=-1)
                average_movement.append(tracker.movement_vector)
            if average_movement:
                average_movement = np.mean(average_movement, axis=0)
                self.status_guidewire_tracking_signal.emit(
                    f"({len(trackers)}) Move: {average_movement[0]} | {average_movement[1]}")
            else:
                self.status_guidewire_tracking_signal.emit("No guidewire detected.")

            output = ImageData(image_data=threshold, metadata=prediction.metadata)
            self.publisher_socket.send(pickle.dumps(output))

    def move_slice_to_target(self, forward_z, side_to_side_x):
        current_location = self.MRI.get_slice_position_dcs().value
        target_location = [current_location.x + forward_z,
                           current_location.y + side_to_side_x,
                           current_location.z]
        answer = self.MRI.set_slice_position_dcs(x=target_location[0], y=target_location[1],
                                                 z=target_location[2])
        self.status_move_slice_signal.emit(f"Move({forward_z},{side_to_side_x}): {answer.result.success}, "
                                           f"{answer.result.reason}, valueSet: {answer.valueSet}")
        """
        Wait for changes to take effect
        """
        allowed_difference = 3
        while True:
            data = self.subscriber_socket.recv()
            prediction: ImageData = pickle.loads(data)
            new_location = prediction.metadata.value.image.coordinates.mrSliceDcs.position
            diff_x = abs(new_location.x - target_location[0]) < allowed_difference
            diff_y = abs(new_location.y - target_location[1]) < allowed_difference
            diff_z = abs(new_location.z - target_location[2]) < allowed_difference
            if all([diff_x, diff_y, diff_z]):
                self.previous_positions = None
                break


class CollisionDetection:
    pass


def json_to_object(json_string):
    return json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))


def select_directory():
    file_dialog = QFileDialog()
    directory_path = file_dialog.getExistingDirectory(None, "Select Directory", "")
    return directory_path


def convert_websocket_data_to_image(websocket_data):
    image_data = json.loads(websocket_data.decode('utf-8'), object_hook=lambda d: SimpleNamespace(**d))
    image = None
    metadata = None
    if "imageStream" in image_data:
        metadata = image_data[2]
        image = image_data[2].value.image.data
        image = np.frombuffer(base64.b64decode(image), dtype=np.uint16)
        image = np.reshape(image, (image_data[2].value.image.dimensions.columns,
                                   image_data[2].value.image.dimensions.rows))
        image = (image / image.max() * 255).astype(np.uint8)
    return image, metadata


def calculate_latency(metadata):
    """

    :param metadata: the 'image[2]' list from websocket imageStream.
    :return: latency compared to datetime.now() in seconds
    """
    image_timestamp = datetime.strptime(metadata.value.image.acquisition.time, '%H%M%S.%f')
    return (datetime.strptime(datetime.now().strftime('%H%M%S.%f'), '%H%M%S.%f') - image_timestamp).total_seconds()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
