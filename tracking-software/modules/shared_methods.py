"""

"""

import json
import base64
import numpy as np
from datetime import datetime
from types import SimpleNamespace


def json_to_object(json_string):
    return json.loads(json_string, object_hook=lambda d: SimpleNamespace(**d))


def convert_websocket_data_to_image(websocket_data):
    image_data = json.loads(websocket_data.decode('utf-8'), object_hook=lambda d: SimpleNamespace(**d))
    image = None
    metadata = None
    if "imageStream" in image_data:
        image, metadata = convert_metadata_to_image(image_data[2])
    return image, metadata


def convert_metadata_to_image(metadata):
    image = metadata.value.image.data
    image = np.frombuffer(base64.b64decode(image), dtype=np.uint16)
    image = np.reshape(image, (metadata.value.image.dimensions.columns, metadata.value.image.dimensions.rows))
    image = (image / image.max() * 255).astype(np.uint8)
    return image, metadata


def calculate_latency(metadata):
    """

    :param metadata: the 'image[2]' list from websocket imageStream.
    :return: latency compared to datetime.now() in seconds
    """
    image_timestamp = datetime.strptime(metadata.value.image.acquisition.time, '%H%M%S.%f')
    return (datetime.strptime(datetime.now().strftime('%H%M%S.%f'), '%H%M%S.%f') - image_timestamp).total_seconds()
