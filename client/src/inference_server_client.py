import numpy as np
import numpy.typing as npt
from typing import List, Dict

import time
from omegaconf import OmegaConf, DictConfig

from http_client import HttpClient


class InferenceServerClient:
    def __init__(self, url: str = "http://172.20.1.3:31708") -> None:
        self.http_client = HttpClient(url)
        response_content = self.http_client.health_check()
        if response_content == None:
            raise RuntimeError("Inference server health check failed")

    def optimize_pose(self,
                      camera_color_imgs: List[npt.NDArray[np.uint8]],
                      camera_pose_htms: List[npt.NDArray[np.float32]],
                      camera_instrinsics: List[npt.NDArray[np.float32]],
                      optimization_config: DictConfig,
                      text_query: str = "Pick up something please") -> npt.NDArray[np.float32]:

        observations = self._construct_observation_dict(
            camera_color_imgs, camera_pose_htms, camera_instrinsics)

        payload = {
            'observations': observations,
            'optimization_config': OmegaConf.to_container(optimization_config),
            'text': text_query,
            'optimizer_name': "language_1_view",
            'return_trajectory': True,
            'reset_optimizer': True
        }
        request_id = self.http_client.submit_task('/optimize_poses', payload)
        optimized_pose = None
        while optimized_pose is None:
            time.sleep(0.2)
            optimized_pose = self.http_client.get_result(request_id)
        return optimized_pose

    def _construct_observation_dict(self, camera_color_imgs, camera_pose_htms, camera_instrinsics) -> List[Dict]:
        assert all(len(lst) == len(camera_color_imgs)
                   for lst in [camera_pose_htms, camera_instrinsics])

        observations = []
        for ccimg, cphtm, cintr in zip(camera_color_imgs, camera_pose_htms, camera_instrinsics):
            assert ccimg.dtype == np.uint8, "Camera color image has wrong data type, deserialization on the server would crash as a result."
            assert cphtm.shape == (
                4, 4), "Expected a homogeneous transformation matrix"
            assert cphtm.dtype == np.float32, "Camera extrinsic has wrong data type, deserialization on the server would crash as a result."
            cintr = np.reshape(cintr, (3, 3))
            assert cintr.dtype == np.float32, "Camera intrinsic has wrong data type, deserialization on the server would crash as a result."

            observations.append({'color': ccimg.tobytes(),
                                 'color_shape': ccimg.shape,
                                 'extrinsics': cphtm.tobytes(),
                                 'intrinsics': cintr.tobytes()})

        return observations
