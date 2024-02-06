"""
https://github.com/MIC-DKFZ/nnUNet/blob/master/nnunetv2/inference/examples.py
"""
# %matplotlib inline
from skimage import measure
import torch
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
import cv2
import numpy as np
from scipy.interpolate import splprep, splev
import siemens_access_library as access_library
import asyncio
import threading
import json
from types import SimpleNamespace
from io import BytesIO
import base64


class CNNModel:
    def __init__(self, path_to_model_directory="MODEL", checkpoint_name="checkpoint_final.pth", folds=(4,)):
        self.model = self.prepare_cnn(path_to_model_directory, checkpoint_name, folds)

    def prepare_cnn(self, path_to_model_directory="MODEL", checkpoint_name="checkpoint_final.pth", folds=(4,)):
        """
        :param path_to_model_directory: must have dataset.json & folder containing the fold e.g. fold_4/checkpoint_final.pth
        :param checkpoint_name: e.g. checkpoint_final.pth
        :param folds: tuple of folds e.g. (4,)
        :return:
        The model which is prepared to predict
        """
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        predictor = nnUNetPredictor(
            tile_step_size=1,
            use_gaussian=True,
            use_mirroring=True,
            perform_everything_on_gpu=True,
            device=torch.device('cpu', 0),
            verbose=False,
            verbose_preprocessing=False,
            allow_tqdm=False
        )
        predictor.initialize_from_trained_model_folder(path_to_model_directory, checkpoint_name=checkpoint_name,
                                                       use_folds=folds)
        return predictor

    async def image_callback_cnn(self, image_data):
        if "imageStream" in image_data:
            """
            """
            image_data = json.loads(json.dumps(image_data), object_hook=lambda d: SimpleNamespace(**d))
            image_buffer = image_data[2].value.image.data
            decoded_data = base64.b64decode(image_buffer)
            try:
                image_array = np.frombuffer(decoded_data, dtype=np.uint16)
                image_array = np.reshape(image_array, (image_data[2].value.image.dimensions.columns,
                                                       image_data[2].value.image.dimensions.rows))
                # How to do this conversion properly, 16-bit to 8-bit, but the image max usually caps at ~1400
                image = (image_array / image_array.max() * 255).astype(np.uint8)
                image = cv2.resize(image, (512, 512)).astype(np.float32) / 255.0
                cnn_input = image.reshape(1, 1, image.shape[0], image.shape[1])
                props = {'spacing': (999, 1, 1)}
                output = self.model.predict_single_npy_array(cnn_input, props, None, None, True)[0]
                output_display = (output * 255).astype(np.uint8).reshape(512, 512)
                image_display = (image * 255).astype(np.uint8)
                cv2.imshow("Input Image", image_display)
                cv2.imshow("Output Image", output_display)
                print(f"output_mix/max: {output.min()}/{output.max()}, output_display_mix/max: {output_display.min()}/{output_display.max()}")
                cv2.waitKey(1)
            except Exception as error:
                print(f"Error in callback: {error}")


def draw_spline(image_data):
    spline_points = []
    labels = measure.label(image_data > 128)
    properties = measure.regionprops(labels)
    centers = np.array([prop.centroid for prop in properties])
    if len(centers) > 1:
        tck, _ = splprep(centers.T, s=0)
        spline_points = splev(np.linspace(0, 1, 1000), tck)
    return spline_points


def run_websocket_in_thread(session_id, callback_function):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(Access.connect_websocket(session_id, callback_function))


"""
Client IP: 192.168.182.20
Subnet: 255.255.255.0
Gateway: 192.168.182.0
DNS1: 192.168.182.1
"""
Access = access_library.Access("10.89.184.9", ssl_verify=False, version="v1")
Model = CNNModel()

active_check = Access.get_is_active()
if active_check is None:
    raise SystemExit("Server not active")
print(f"Active: {active_check.value}")

version = Access.get_version()
print(f"Version: {version.value}")

register = Access.register(name="UTwente", start_date="20231102", warn_date="20251002",
                           expire_date="20251102", system_id="152379",
                           hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D",
                           informal_name="Martin Reinok Python Client")
print(f"Register: {register.result.success}, Session: {register.sessionId}")

image_format = Access.set_image_format(register.sessionId, "raw16bit")

"""
Initialize websocket loop for image service
"""

thread = threading.Thread(target=run_websocket_in_thread, args=(register.sessionId, Model.image_callback_cnn))
thread.start()
# Connect the image service to existing websocket

image_service = Access.connect_image_service_to_default_web_socket(register.sessionId)
print(f"ImageServiceConnection: {image_service.result.success}")

cv2.destroyAllWindows()