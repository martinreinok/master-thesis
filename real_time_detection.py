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
import time
import base64


class CNNModel:
    def __init__(self, accessi_instance: access_library.Access, path_to_model_directory="MODEL", checkpoint_name="checkpoint_final.pth", folds=(4,)):
        self.model = self.prepare_cnn(path_to_model_directory, checkpoint_name, folds)
        self.access_i = accessi_instance

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
            device=torch.device('cuda', 0),
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
            TODO: Ignore queue, take most up to date image.
            TODO: Images can be stored but only latest should be processed.
            TODO: Search "calibration" function
            TODO: 256x256(px) images
            """
            start_time = time.time()
            image_data = json.loads(json.dumps(image_data), object_hook=lambda d: SimpleNamespace(**d))
            image_buffer = image_data[2].value.image.data
            decoded_data = base64.b64decode(image_buffer)
            configured_parameters = self.access_i.get_configured_parameters()
            print(f"Configured Parameters: {configured_parameters}")
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
                # print(f"Slice Thickness: {self.access_i.get_slice_thickness().value}, "
                #       f"{self.access_i.get_slice_thickness().result}")
                # print(f"Slice Position: {self.access_i.get_slice_position_dcs().value}")
                # print(f"Slice Orientation Normal: {self.access_i.get_slice_orientation_dcs().normal}")
                # print(f"Slice Orientation Read: {self.access_i.get_slice_orientation_dcs().read}")
                cv2.imshow("Input Image", image_display)
                cv2.imshow("Output Image", output_display)
                cv2.waitKey(1)
            except Exception as error:
                print(f"Error in callback: {error}")
            print("Image processing: %s seconds" % (time.time() - start_time))


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
Model = CNNModel(accessi_instance=Access)

active_check = Access.get_is_active()
if active_check is None:
    raise SystemExit("Server not active")
print(f"Access-i Active: {active_check.value}")

version = Access.get_version()
print(f"Access-i Version: {version.value}")

register = Access.register(name="UTwente", start_date="20231102", warn_date="20251002",
                           expire_date="20251102", system_id="152379",
                           hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D",
                           informal_name="Martin Reinok Python Client")
print(f"Access-i Register: {register.result.success}, Session: {register.sessionId}")
if not register.result.success:
    raise SystemExit("Access-i Registering failed")

image_format = Access.set_image_format("raw16bit")

"""
Initialize websocket loop for image service
"""

thread = threading.Thread(target=run_websocket_in_thread, args=(register.sessionId, Model.image_callback_cnn))
thread.start()
# Connect the image service to existing websocket

image_service = Access.connect_image_service_to_default_web_socket()
print(f"Access-i ImageServiceConnection: {image_service.result.success}")

cv2.destroyAllWindows()
