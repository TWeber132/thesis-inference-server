# processes/process.py
import msgpack
import numpy as np

from shared_resources import set_result

from loguru import logger


def process_np_array(byte_data, task_id):
    # Unpack the data
    unpacked_payload = msgpack.unpackb(byte_data, raw=False)
    # Reconstruct the numpy array
    data = unpacked_payload["data"]
    shape = unpacked_payload["shape"]
    dtype = unpacked_payload["dtype"]
    np_array = np.frombuffer(data, dtype=dtype).reshape(shape)

    # Display the numpy array: [batch, ...]
    # for each input in the batch, we emulate the process of the inference server
    # in case of images, we would return pixel coordinates of the detected object
    # now we will return a set of random coordinates
    random_coordinates = []
    for i in range(np_array.shape[0]):
        # get image shape
        data_shape = np_array[i].shape
        # random coordinates
        x = np.random.randint(0, data_shape[1])
        y = np.random.randint(0, data_shape[0])
        # return the coordinates
        random_coordinates.append([x, y])
    random_coordinates = np.array(random_coordinates)

    # Set the result
    results = {
        "status": "completed",
        "data": random_coordinates.tobytes(),
        "shape": random_coordinates.shape,
        "dtype": random_coordinates.dtype.name
    }
    set_result(task_id, results)
    logger.debug(f"Task {task_id} completed")
