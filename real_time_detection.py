"""
https://github.com/MIC-DKFZ/nnUNet/blob/master/nnunetv2/inference/examples.py
- Calibration phase
- Tracking phase
"""
import os
import threading
import torch
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
import cv2
import numpy as np
import asyncio
from datetime import datetime
import json
from types import SimpleNamespace
import time
import base64
import accessi_local as Access
import queue as ThreadsafeQueue
import tkinter as tk

threadsafe_queue = ThreadsafeQueue.LifoQueue()
opencv_input_image_queue = ThreadsafeQueue.LifoQueue()
opencv_output_image_queue = ThreadsafeQueue.LifoQueue()
opencv_slice_movement_queue = ThreadsafeQueue.LifoQueue()

FOLLOW_GUIDEWIRE = False
FOLLOW_GUIDEWIRE_MRI_REQUEST = False
STOP_ALL_THREADS = False
MRI_IMAGE_SIZE_PX = None
MRI_IMAGE_SIZE_MM = None


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

    def predict(self, image_data):
        try:
            image = cv2.resize(image_data, (350, 350)).astype(np.float32) / 255.0
            cnn_input = image.reshape(1, 1, image.shape[0], image.shape[1])
            props = {'spacing': (999, 1, 1)}
            return image, self.model.predict_single_npy_array(cnn_input, props, None, None, False)[0]

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
                # Clear the queue, should not be done if all images should be saved
                with threadsafe_queue.mutex:
                    threadsafe_queue.queue.clear()
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
                    global MRI_IMAGE_SIZE_PX, MRI_IMAGE_SIZE_MM
                    if MRI_IMAGE_SIZE_PX is None:
                        MRI_IMAGE_SIZE_PX = int(image_data[2].value.image.dimensions.columns)
                    if MRI_IMAGE_SIZE_MM is None:
                        MRI_IMAGE_SIZE_MM = int(image_data[2].value.image.dimensions.voxelSize.column *
                                                image_data[2].value.image.dimensions.columns)
                    image = (image_array / image_array.max() * 255).astype(np.uint8)
                    input_image, output_image = self.predict(image)
                    opencv_input_image_queue.put((input_image * 255).astype(np.uint8))
                    opencv_output_image_queue.put((output_image * 255).astype(np.uint8))
                    print("Image processing: %s seconds" % (time.time() - start_time))
                    latency = (datetime.strptime(datetime.now().strftime('%H%M%S.%f'),
                                                 '%H%M%S.%f') - image_timestamp).total_seconds()
                    print(f"Image timestamp: {image_timestamp.time()} | Latency: {latency} seconds")
                    print(f"Local PC time: {datetime.now().strftime('%H%M%S.%f')}")


def opencv_display_thread(updates_in_second=20):
    last_image = None
    last_output = None
    while True:
        if not opencv_input_image_queue.empty() and not opencv_output_image_queue.empty():
            try:
                input_image = opencv_input_image_queue.get()
                output_image = opencv_output_image_queue.queue[-1]
                input_image = cv2.resize(input_image, (512, 512))
                output_image = cv2.resize(output_image, (512, 512))
                cv2.imshow("Input Image", input_image)
                cv2.imshow("Output Image", output_image)
                last_image = input_image
                last_output = output_image
                cv2.waitKey(1)
            except Exception as error:
                print(error)
                if last_image is not None and last_output is not None:
                    cv2.imshow("Input Image", last_image)
                    cv2.imshow("Output Image", last_output)
                cv2.waitKey(1)
        time.sleep(1 / updates_in_second)
    cv2.destroyAllWindows()


def check_collision(model_geometry_data, prediction_image):
    pass


def find_artifact_centroids(image, gaussian_kernel: int = 5, opencv_show_images=False):
    blurred = cv2.GaussianBlur(image, (gaussian_kernel, gaussian_kernel), 0)
    _, threshold = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    threshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2RGB)
    centroids = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            centroids.append((cX, cY))
            cv2.circle(threshold, (cX, cY), 3, (0, 255, 0), -1)
    if opencv_show_images:
        cv2.imshow("threshold", threshold)
        cv2.imshow("blurred", blurred)
        cv2.waitKey(1)
    return centroids


def get_guidewire_movement_vector(prediction_image, previous_centroids=None):
    """
    Returns moment vectors or None, calculated centroids.
    """
    current_centroids = find_artifact_centroids(prediction_image, opencv_show_images=True)
    if previous_centroids is not None:
        movement_vectors = []
        for current_centroid in current_centroids:
            min_dist = float('inf')
            closest_prev_centroid = None
            for prev_centroid in previous_centroids:
                dist = np.linalg.norm(np.array(current_centroid) - np.array(prev_centroid))
                if dist < min_dist:
                    min_dist = dist
                    closest_prev_centroid = prev_centroid
            if closest_prev_centroid:
                movement_vectors.append(((closest_prev_centroid[0], closest_prev_centroid[1]), current_centroid))
        return movement_vectors, current_centroids
    return [], current_centroids


def toggle_follow_guidewire():
    global FOLLOW_GUIDEWIRE
    FOLLOW_GUIDEWIRE = not FOLLOW_GUIDEWIRE


def toggle_stop_threads():
    global STOP_ALL_THREADS
    STOP_ALL_THREADS = True


def toggle_send_guidewire_tracking_request():
    global FOLLOW_GUIDEWIRE_MRI_REQUEST
    FOLLOW_GUIDEWIRE_MRI_REQUEST = not FOLLOW_GUIDEWIRE_MRI_REQUEST


def create_guidewire_follow_ui():
    root = tk.Tk()
    root.title("Controls")
    toggle_guidewire = tk.Checkbutton(root, text="Follow Guidewire", command=toggle_follow_guidewire)
    toggle_guidewire.pack()
    toggle_mri_follow_guidewire = tk.Checkbutton(root, text="MRI Send Guidewire Request",
                                                 command=toggle_send_guidewire_tracking_request)
    toggle_mri_follow_guidewire.pack()
    quit_button = tk.Button(root, text="Exit Program", command=toggle_stop_threads, width=20, height=5)
    quit_button.pack()
    root.geometry('200x100')
    root.mainloop()


class MRI:
    def __init__(self, access_instance: Access):
        self.access = access_instance

    def get_control(self):
        """
        :return: bool if we have control or not.
        """
        control_state = self.access.HostControl.get_state().value
        if not control_state.hasControl:
            if control_state.canRequestControl:
                self.access.HostControl.request_host_control()
            else:
                print(f"Unable to request control: {control_state.cannotRequestControlReason}")
        return self.access.HostControl.get_state().value.hasControl


def follow_guidewire_thread(movement_threshold_mm=1):
    previous_centroids = None
    global MRI_IMAGE_SIZE_PX, MRI_IMAGE_SIZE_MM, FOLLOW_GUIDEWIRE_MRI_REQUEST
    while True:
        movement_vector_mm = [0, 0]
        if FOLLOW_GUIDEWIRE and not opencv_output_image_queue.empty():
            image = opencv_output_image_queue.queue[-1]
            movement_vectors, current_centroids = get_guidewire_movement_vector(image, previous_centroids)
            previous_centroids = current_centroids
            if movement_vectors:
                vectors_array = np.array(movement_vectors)
                mean_vector = np.mean(np.diff(vectors_array, axis=1), axis=0)
                mean_vector_mm = mean_vector * MRI_IMAGE_SIZE_MM / MRI_IMAGE_SIZE_PX
                movement_vector_mm[0] = mean_vector_mm[0][0]
                movement_vector_mm[1] = mean_vector_mm[0][1]
                print(f"MRI PLANE MOVEMENT SUGGESTION X:{mean_vector_mm[0][0]}, Y:{mean_vector_mm[0][1]}")
                time.sleep(0.2)
            else:
                print("No movement vectors detected.")
                time.sleep(0.2)
        if abs(sum(movement_vector_mm)) > movement_threshold_mm and FOLLOW_GUIDEWIRE_MRI_REQUEST:
            if MRI.get_control():
                current_location = Access.ParameterStandard.get_slice_position_dcs().value
                result = Access.ParameterStandard.set_slice_position_dcs(index=0,
                                                                         x=current_location.x + movement_vector_mm[0],
                                                                         y=current_location.y,
                                                                         z=current_location.z + movement_vector_mm[1])
                print(f"MRI PLANE MOVE: {result}")
        else:
            time.sleep(0.2)


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
    while True:
        await asyncio.sleep(0.1)


def run_websocket_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())


# Run the asyncio event loop
if __name__ == "__main__":
    """
    route add 10.89.184.0 mask 255.255.255.0 192.168.182.1 -p
    """
    """
    Client IP: 192.168.182.20
    Subnet: 255.255.255.0
    Gateway: 192.168.182.0
    DNS1: 192.168.182.1
    """
    Access.config.ip_address = "127.0.0.1"
    Access.config.version = "v2"
    # Access.config.ip_address = "10.89.184.9"
    # Access.config.version = "v1"
    Access.config.timeout = 5  # Template might take time to start up.
    Model = CNNModel(path_to_model_directory="MODEL_350")
    register = Access.Authorization.register(name="UTwente", start_date="20231102", warn_date="20251002",
                                             expire_date="20251102", system_id="152379",
                                             hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D",
                                             informal_name="Martin Reinok Python Client")
    print(f"Access-i Register: {register.result.success}, Session: {register.sessionId}")
    if not register.result.success:
        raise SystemExit("Access-i Registering failed")
    MRI = MRI(Access)
    image_format = Access.Image.set_image_format("raw16bit")
    """
    START SEQUENCE
    """
    if not Access.HostControl.request_host_control().result.success:
        raise Exception(f"{Access.HostControl.request_host_control().result.reason}")
    template_name = "trufi_interactive_rt 1.5"
    templates = Access.TemplateExecution.get_templates()
    print(templates)
    template_id = next((template.id for template in templates.value if template.label == template_name), None)
    Access.TemplateModification.open(template_id)
    Access.TemplateExecution.start(template_id)
    """
    
    """
    output_display_thread = threading.Thread(target=opencv_display_thread, daemon=True)
    cnn_prediction_thread = threading.Thread(target=Model.callback_thread, daemon=True)
    follow_guidewire_thread = threading.Thread(target=follow_guidewire_thread, daemon=True)
    guidewire_ui_thread = threading.Thread(target=create_guidewire_follow_ui, daemon=True)
    websocket_thread = threading.Thread(target=run_websocket_thread, daemon=True)
    websocket_thread.start()
    follow_guidewire_thread.start()
    guidewire_ui_thread.start()
    output_display_thread.start()
    cnn_prediction_thread.start()

    image_service = Access.Image.connect_to_default_web_socket()
    print(f"Access-i ImageServiceConnection: {image_service}")

    while True:
        time.sleep(1)
        if STOP_ALL_THREADS:
            """CLEANUP"""
            Access.TemplateExecution.stop()
            Access.TemplateModification.close(template_id)
            Access.HostControl.release_host_control()
            raise SystemExit
        # print(Access.ParameterStandard.set_slice_position_dcs(index=0, x=4, y=-80, z=-4))
        # print(Access.ParameterStandard.get_slice_position_dcs())
        # print(Access.ParameterStandard.set_slice_position_dcs(index=0, x=0, y=0, z=-4))
