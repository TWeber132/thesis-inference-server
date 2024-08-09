import numpy as np
import time
from http_client.client import HttpClient

detection_url = "http://localhost:8076"
http_client = HttpClient(detection_url)
health_check = http_client.health_check()
print(f'http server health check: {health_check}')

# Batch of images
batch_data = np.random.rand(3, 224, 224, 3)
# Prepare data for the inference server
byte_data = batch_data.tobytes()
data_shape = batch_data.shape
data_type = batch_data.dtype.name
payload = {
    'data': byte_data,
    'shape': data_shape,
    'dtype': data_type
}
request_id = http_client.submit_task('process_np_array', payload)
batch_result = None
while batch_result is None:
    time.sleep(0.2)
    batch_result = http_client.get_result(request_id)
print(f'batch result: {batch_result}')