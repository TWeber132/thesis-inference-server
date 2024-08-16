import numpy as np
import requests
import msgpack


class HttpClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def submit_task(self, task_name, payload):
        headers = {'Content-Type': 'application/octet-stream'}
        data = msgpack.packb(payload)
        response = requests.post(
            f'{self.base_url}/{task_name}', headers=headers, data=data)
        if response.status_code == 200:
            data = msgpack.unpackb(response.content, raw=False)
            return data['task_id']
        else:
            return None

    def health_check(self):
        response = requests.get(f'{self.base_url}/health')
        if response.status_code == 200:
            return response.content
        else:
            return None

    def get_result(self, task_id):
        response = requests.get(f'{self.base_url}/result/{task_id}')
        if response.status_code == 200:
            response_data = msgpack.unpackb(response.content, raw=False)
            if response_data['status'] == 'completed':
                optimized_pose = response_data['optimized_pose']
                optimized_loss = response_data['optimized_loss']
                trajectory = response_data['trajectory']
                duration = response_data['duration']
                print(f"Completed task {task_id} after {duration} seconds")
                print(f"Optimized_loss: {optimized_loss}")
                optimized_pose = np.frombuffer(
                    optimized_pose, dtype=np.float32).reshape(4, 4)
                return optimized_pose
            elif response_data['status'] in ['not found', 'failed']:
                raise Exception(
                    f'Failed to get result: {response_data["status"]}')
            else:
                return None
        else:
            raise Exception(
                f'Failed to get result: status code {response.status_code}')
