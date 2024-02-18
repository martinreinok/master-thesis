"""
https://github.com/MIC-DKFZ/nnUNet/blob/master/nnunetv2/inference/examples.py
- Calibration phase
- Tracking phase
"""
import threading

# %matplotlib inline
from skimage import measure
import torch
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
import cv2
import numpy as np
from scipy.interpolate import splprep, splev
import asyncio
from datetime import datetime
import json
from types import SimpleNamespace
import time
import base64
import accessi_local as Access
import queue as ThreadsafeQueue

threadsafe_queue = ThreadsafeQueue.LifoQueue()
opencv_input_image_queue = ThreadsafeQueue.LifoQueue()
opencv_output_image_queue = ThreadsafeQueue.LifoQueue()
slice_movement_requests = ThreadsafeQueue.LifoQueue()


class CNNModel:
    def __init__(self, path_to_model_directory="MODEL", checkpoint_name="checkpoint_final.pth", folds=(4,)):
        self.model = self.prepare_cnn(path_to_model_directory, checkpoint_name, folds)

    def prepare_cnn(self, path_to_model_directory, checkpoint_name, folds):
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
            use_gaussian=False,
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

    def predict(self, image_data):
        try:
            image = cv2.resize(image_data, (512, 512)).astype(np.float32) / 255.0
            cnn_input = image.reshape(1, 1, image.shape[0], image.shape[1])
            props = {'spacing': (999, 1, 1)}
            return image, self.model.predict_single_npy_array(cnn_input, props, None, None, True)[0]
        except Exception as error:
            print(f"Error occurred in prediction: {error}")
        return None

    def callback_thread(self):
        while True:
            # create a copy from the queue
            while threadsafe_queue.empty():
                time.sleep(0.1)
            else:
                image_data = threadsafe_queue.queue[-1]
                if "imageStream" in image_data:
                    start_time = time.time()
                    image_data = json.loads(json.dumps(image_data), object_hook=lambda d: SimpleNamespace(**d))
                    image_buffer = image_data[2].value.image.data
                    image_timestamp = datetime.strptime(image_data[2].value.image.acquisition.time, '%H%M%S.%f')
                    decoded_data = base64.b64decode(image_buffer)
                    image_array = np.frombuffer(decoded_data, dtype=np.uint16)
                    image_array = np.reshape(image_array, (
                        image_data[2].value.image.dimensions.columns,
                        image_data[2].value.image.dimensions.rows))
                    image = (image_array / image_array.max() * 255).astype(np.uint8)
                    input_image, output_image = self.predict(image)
                    opencv_input_image_queue.put(input_image)
                    opencv_output_image_queue.put(output_image)
                    print("Image processing: %s seconds" % (time.time() - start_time))
                    latency = (datetime.strptime(datetime.now().strftime('%H%M%S.%f'),
                                                 '%H%M%S.%f') - image_timestamp).total_seconds()
                    print(f"Image timestamp: {image_timestamp.time()} | Latency: {latency} seconds")


def draw_spline(image_data):
    spline_points = []
    labels = measure.label(image_data > 128)
    properties = measure.regionprops(labels)
    centers = np.array([prop.centroid for prop in properties])
    if len(centers) > 1:
        tck, _ = splprep(centers.T, s=0)
        spline_points = splev(np.linspace(0, 1, 1000), tck)
    return spline_points


def opencv_display_thread(updates_in_second=20):
    last_image = None
    last_output = None
    while True:
        if not opencv_input_image_queue.empty() and not opencv_output_image_queue.empty():
            try:
                input_image = opencv_input_image_queue.get()
                output_image = opencv_output_image_queue.queue[-1]
                output_display = (output_image * 255).astype(np.uint8).reshape(512, 512)
                image_display = (input_image * 255).astype(np.uint8)
                cv2.imshow("Input Image", image_display)
                cv2.imshow("Output Image", output_display)
                last_image = image_display
                last_output = output_display
                cv2.waitKey(1)
            except:
                if last_image is not None and last_output is not None:
                    cv2.imshow("Input Image", last_image)
                    cv2.imshow("Output Image", last_output)
                    cv2.waitKey(1)
                pass
        time.sleep(1 / updates_in_second)


def check_collision(model_geometry_data, prediction_image):
    pass


def follow_guidewire(model_geometry_data, prediction_image):
    pass


async def get_websocket_data(connected_event: asyncio.Event, queue: ThreadsafeQueue):
    async with await Access.connect_websocket() as websocket:
        connected_event.set()
        while True:
            message = await websocket.recv()
            decoded_message = Access.handle_websocket_message(message)
            queue.put(decoded_message)


async def main():
    # Run websocket
    websocket_connected_event = asyncio.Event()
    asyncio.create_task(get_websocket_data(connected_event=websocket_connected_event, queue=threadsafe_queue))
    await websocket_connected_event.wait()

    # Connect the image service to websocket
    image_service = Access.Image.connect_to_default_web_socket()
    print(f"Access-i ImageServiceConnection: {image_service}")

    while True:
        await asyncio.sleep(1)


# Run the asyncio event loop
if __name__ == "__main__":
    """
    Client IP: 192.168.182.20
    Subnet: 255.255.255.0
    Gateway: 192.168.182.0
    DNS1: 192.168.182.1
    """
    Access.config.ip_address = "127.0.0.1"  # "10.89.184.9"
    Access.config.version = "v2"
    Model = CNNModel(path_to_model_directory="MODEL_350")
    register = Access.Authorization.register(name="UTwente", start_date="20231102", warn_date="20251002",
                                             expire_date="20251102", system_id="152379",
                                             hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D",
                                             informal_name="Martin Reinok Python Client")
    print(f"Access-i Register: {register.result.success}, Session: {register.sessionId}")
    if not register.result.success:
        raise SystemExit("Access-i Registering failed")
    image_format = Access.Image.set_image_format("raw16bit")
    output_display_thread = threading.Thread(target=opencv_display_thread, daemon=True)
    cnn_prediction_thread = threading.Thread(target=Model.callback_thread, daemon=True)
    output_display_thread.start()
    cnn_prediction_thread.start()
    asyncio.run(main())
