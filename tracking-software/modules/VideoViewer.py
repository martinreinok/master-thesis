"""

"""
import os
import cv2
import zmq
import pickle
from datetime import datetime
from ImageData import ImageData
from shared_methods import convert_websocket_data_to_image


class VideoViewer:
    def __init__(self, window, zmq_port, window_name, checkbox, websocket_dataformat=False, save_images_button=None,
                 save_images_folder=None):
        self.zmq_port = zmq_port
        self.window_name = window_name
        self.checkbox = checkbox
        self.websocket = websocket_dataformat
        self.save_images_button = save_images_button
        self.save_images_folder = save_images_folder
        self.window = window

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
                    image, metadata = convert_websocket_data_to_image(data)
                    if image is None:
                        cv2.waitKey(1)
                        continue
                else:
                    imagedata: ImageData = pickle.loads(data)
                    image = imagedata.image
                    metadata = imagedata.metadata
                selected_resolution_text = self.window.ui.combo_show_output_dimensions.currentText()
                width, height = map(int, selected_resolution_text.split('x'))
                resized_image = cv2.resize(image, (width, height))
                cv2.imshow(self.window_name, resized_image)
                cv2.waitKey(1)
                if self.save_images_button.isChecked():
                    save_folder = os.path.join(self.window.ui.field_output_directory.text(), self.save_images_folder)
                    os.makedirs(save_folder, exist_ok=True)
                    timestamp = datetime.strptime(metadata.value.image.acquisition.time, '%H%M%S.%f')
                    filename = f"{timestamp.strftime('%H%M%S.%f')[:-3]}.jpg"
                    cv2.imwrite(os.path.join(save_folder, filename), resized_image)
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
