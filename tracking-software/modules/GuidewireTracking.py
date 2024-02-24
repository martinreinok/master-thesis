"""

"""

import cv2
import zmq
import pickle
import numpy as np
import accessi_local as Access
from PySide6.QtCore import Signal, QObject
from ImageData import ImageData
from ArtifactTracker import ArtifactTracker


class GuidewireTracking(QObject):
    status_guidewire_tracking_signal = Signal(str)
    status_move_slice_signal = Signal(str)

    def __init__(self, window, subscribe_port):
        super().__init__()
        self.PUBLISH_PORT = None
        self.SUBSCRIBE_PORT = subscribe_port
        self.move_slice = False
        self.MRI: Access.ParameterStandard = Access.ParameterStandard()
        self.voxel_size = None
        self.subscriber_socket = None
        self.publisher_socket = None
        self.previous_positions = None
        self.window = window

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
        while self.window.ui.check_guidewire_tracking_active.isChecked():
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
                unique_coordinates = set(tracker.trajectory)
                for coordinate in unique_coordinates:
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