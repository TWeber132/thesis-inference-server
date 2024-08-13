import numpy as np
import time
import hydra
from omegaconf import OmegaConf


from client import HttpClient


@hydra.main(version_base=None, config_path="../configs", config_name="language_1_view")
def main(cfg):
    detection_url = "http://localhost:8076"
    http_client = HttpClient(detection_url)
    health_check = http_client.health_check()
    print(f'http server health check: {health_check}')

    opt_conf = OmegaConf.to_container(
        cfg.validation.grasp_opt_config['optimization_config'])
    payload = {
        'observations': np.random.rand(3, 224, 224, 3).tobytes(),
        'optimization_config': opt_conf,
        'texts': ["blue", "black", "yellow"],
        'optimizer_name': "language_1_view",
        'return_trajectory': True,
        'reset_optimizer': False
    }
    # request_id = http_client.submit_task('process_np_array', payload)
    request_id = http_client.submit_task('/optimize_poses', payload)
    batch_result = None
    while batch_result is None:
        time.sleep(0.2)
        batch_result = http_client.get_result(request_id)
    print(f'batch result: {batch_result}')


if __name__ == "__main__":
    main()
