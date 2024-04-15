"""

"""

import cv2
import zmq
import pickle
import numpy as np
from PySide6.QtCore import Signal, QObject
from ImageData import ImageData
from shared_methods import convert_websocket_data_to_image, calculate_latency


class CNNModel(QObject):
    status_cnn_signal = Signal(str)

    def __init__(self, window, subscribe_port, cnn_model):
        super().__init__()
        self.PUBLISH_PORT = None
        self.SUBSCRIBE_PORT = subscribe_port
        self.path_to_model_directory = f"../MODELS/{cnn_model}"
        self.checkpoint_name = "checkpoint_final.pth"
        self.folds = (4,)
        self.model = None
        self.window = window
        self.input_image_dimensions = None

    def prepare_cnn(self, torch, nnUNetPredictor, path_to_model_directory, checkpoint_name, folds, DEVICE):
        """
        Returns the model which is prepared to predict.
        """
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        predictor = nnUNetPredictor(tile_step_size=1, use_gaussian=True, use_mirroring=True,
                                    perform_everything_on_device=True, device=torch.device(DEVICE, 0),
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

    def start(self, DEVICE):
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
                                      checkpoint_name=self.checkpoint_name, DEVICE=DEVICE)
        for checkbox in [self.window.ui.check_cnn_output, self.window.ui.check_cnn_save,
                         self.window.ui.check_guidewire_tracking_active,
                         self.window.ui.check_tracking_move_slice, self.window.ui.check_collision_detection_active,
                         self.window.ui.check_cathbot_collision_feedback, self.window.ui.check_collision_save,
                         self.window.ui.check_tracking_save]:
            checkbox.setEnabled(True)
            checkbox.stateChanged.emit(checkbox.isChecked())
        while self.window.ui.check_cnn_active.isChecked():
            data = subscriber_socket.recv()
            image, metadata = convert_websocket_data_to_image(data)
            if image is None:
                continue
            self.input_image_dimensions = (metadata.value.image.dimensions.columns, metadata.value.image.dimensions.rows)
            output_image = self.predict(image)
            if output_image is not None:
                output_image = (output_image * 255).astype(np.uint8)
                output_image = cv2.resize(output_image, self.input_image_dimensions)
                output = ImageData(image_data=output_image, metadata=metadata)
                publisher_socket.send(pickle.dumps(output))

                if self.window.ui.check_save_latency_data.isChecked():
                    latency = calculate_latency(metadata, write_to_file=True, filename="CNN_Latency")
                else:
                    latency = calculate_latency(metadata)
                self.status_cnn_signal.emit(f"Latency: {latency}s")
