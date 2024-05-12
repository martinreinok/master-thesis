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
from shared_methods import calculate_latency


class GuidewireTracking(QObject):
    status_guidewire_tracking_signal = Signal(str)
    status_move_slice_signal = Signal(str)

    def __init__(self, window, subscribe_port):
        super().__init__()
        self.PUBLISH_PORT = None
        self.RAW_COORDINATE_PUBLISH_PORT = None
        self.SUBSCRIBE_PORT = subscribe_port
        self.move_slice = False
        self.MRI: Access.ParameterStandard = Access.ParameterStandard()
        self.voxel_size = None
        self.subscriber_socket = None
        self.publisher_socket = None
        self.raw_coordinate_publisher_socket = None
        self.previous_positions = None
        self.window = window
        self.trackers = []

    @staticmethod
    def find_artifact_centroids(image, kernel: int = 7):
        """
        Applies gaussian blur and thresholding to separate artifacts from noise.
        The center of gravity of each remaining blob is returned.
        """
        blurred = cv2.medianBlur(image, kernel)
        # blurred = cv2.GaussianBlur(image, (gaussian_kernel, kernel), 0)
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
                    # cv2.circle(threshold, (cX, cY), 3, (0, 255, 0), -1)
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
        self.raw_coordinate_publisher_socket = context.socket(zmq.PUB)
        self.PUBLISH_PORT = self.publisher_socket.bind_to_random_port("tcp://127.0.0.1")
        self.RAW_COORDINATE_PUBLISH_PORT = self.raw_coordinate_publisher_socket.bind_to_random_port("tcp://127.0.0.1")
        tracker_id = 0
        self.trackers = []
        while self.window.ui.check_guidewire_tracking_active.isChecked():
            data = self.subscriber_socket.recv()
            prediction: ImageData = pickle.loads(data)
            if prediction.image is None:
                continue
            centroids, threshold = self.find_artifact_centroids(prediction.image)

            # Send Centroids Data to socket.
            centroids_mm = [[element * prediction.metadata.value.image.dimensions.voxelSize.column for element in sublist] for sublist in centroids]
            output_3d_suite = ImageData(metadata=prediction.metadata, artifact_coordinates=centroids_mm)
            self.raw_coordinate_publisher_socket.send(pickle.dumps(output_3d_suite))

            if self.window.ui.check_save_latency_data.isChecked():
                latency = calculate_latency(prediction.metadata, write_to_file=True, filename="Tracking_Latency")
            else:
                latency = calculate_latency(prediction.metadata)

            for tracker in self.trackers:
                tracker.update(centroids)
                if tracker.coordinates in centroids:
                    centroids.remove(tracker.coordinates)
                # Erase tracker if it has lost marker for more than 5 frames
                self.trackers = [tracker for tracker in self.trackers if tracker.track_lost <= 5]
            if len(centroids) > 0:
                for centroid in centroids:
                    self.trackers.append(ArtifactTracker(centroid, tracker_id))
                    tracker_id += 1

            average_movement = []
            largest_movement = None
            for tracker in self.trackers:
                if len(tracker.trajectory) >= 2:
                    initial_coordinate, current_coordinate = tracker.trajectory[0], tracker.trajectory[-1]
                    cv2.circle(threshold, initial_coordinate, 4, color=tracker.color, thickness=-1)
                    cv2.circle(threshold, current_coordinate, 4, color=tracker.color, thickness=-1)
                for coordinate in set(tracker.trajectory):
                    cv2.circle(threshold, coordinate, 2, color=tracker.color, thickness=-1)
                # Insignificant movements e.g. standing still are not considered.
                if np.linalg.norm(np.array(tracker.movement_vector)) > movement_threshold_mm:
                    average_movement.append(tracker.movement_vector)
                    if largest_movement is None:
                        largest_movement = tracker
                        continue
                    if np.linalg.norm(np.array(largest_movement.movement_vector)) < np.linalg.norm(np.array(tracker.movement_vector)):
                        largest_movement = tracker

            if largest_movement is not None and len(largest_movement.movement_vector) > 1:
                # average_movement = np.mean(average_movement, axis=0)
                self.status_guidewire_tracking_signal.emit(f"({len(self.trackers)}) Move: {largest_movement.movement_vector[0]} | {largest_movement.movement_vector[1]} (px)")
            elif not largest_movement and len(self.trackers) > 0:
                self.status_guidewire_tracking_signal.emit(f"({len(self.trackers)}) No movement detected")
            else:
                self.status_guidewire_tracking_signal.emit("No guidewire detected.")

            output = ImageData(image_data=threshold, metadata=prediction.metadata)
            self.publisher_socket.send(pickle.dumps(output))

            if self.move_slice and largest_movement is not None and len(largest_movement.movement_vector) > 1:
                self.move_slice_to_target(side_to_side_x=int(self.convert_px_to_mm(largest_movement.movement_vector[0], prediction.metadata)),
                                          forward_z=int(self.convert_px_to_mm(largest_movement.movement_vector[1], prediction.metadata)),
                                          largest_movement_tracker=largest_movement)

    def move_slice_to_target(self, side_to_side_x, forward_z, largest_movement_tracker):
        current_location = self.MRI.get_slice_position_dcs().value
        target_location = [current_location.x + side_to_side_x,
                           current_location.y,
                           current_location.z + forward_z]
        answer = self.MRI.set_slice_position_dcs(x=target_location[0], y=target_location[1],
                                                 z=target_location[2])
        self.status_move_slice_signal.emit(f"Move({forward_z},{side_to_side_x}): {answer.result.success}, "
                                           f"{answer.result.reason}, valueSet: {answer.valueSet}")
        """
        Wait for changes to take effect (this is not good)
        """
        allowed_difference = 2
        while True:
            data = self.subscriber_socket.recv()
            prediction: ImageData = pickle.loads(data)
            new_location = prediction.metadata.value.image.coordinates.mrSliceDcs.position
            diff_x = abs(new_location.x - target_location[0]) < allowed_difference
            diff_y = abs(new_location.y - target_location[1]) < allowed_difference
            diff_z = abs(new_location.z - target_location[2]) < allowed_difference
            if all([diff_x, diff_y, diff_z]):
                # Retain the tracker that was used to move
                self.trackers = [ArtifactTracker(largest_movement_tracker.initial_coordinate, largest_movement_tracker.id)]
                break
