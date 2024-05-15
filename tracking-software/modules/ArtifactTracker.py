"""

"""
import math
import numpy as np
from random import random


class ArtifactTracker:
    """
    Did not manage to get any existing trackers to work, so why not just reinvent the wheel...
    """

    def __init__(self, initial_coordinate, artifact_id, max_range=15):
        self.max_range = max_range
        self.initial_coordinate = initial_coordinate
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
            self.coordinates = closest_coordinate
            self.trajectory.append(closest_coordinate)
            self.movement_vector = self.calculate_movement_vector(self.initial_coordinate)
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
