import numpy as np


def normalize(image):
    return (image - np.min(image)) / (np.max(image) - np.min(image))
