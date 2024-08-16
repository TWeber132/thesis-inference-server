import numpy as np
import time
import hydra
from omegaconf import OmegaConf


from client import HttpClient
from clip_nerf.src.lib.dataset.utils import load_dataset_language


@hydra.main(version_base=None, config_path="../configs", config_name="language_1_view")
def main(cfg):
    inference_server_url = "http://172.20.1.3:31708"
    http_client = HttpClient(inference_server_url)
    health_check = http_client.health_check()
    print(f'http server health check: {health_check}')
    i = 1
    test_dataset = load_dataset_language(
        cfg.dataset.n_perspectives, cfg.dataset.path + '/test')
    text = test_dataset.datasets['language'].read_sample(i)
    gt_pose = test_dataset.datasets['grasp_pose'].read_sample(i)['grasp_pose']
    color = test_dataset.datasets['color'].read_sample_at_idx(
        i, 0)[..., :3]
    camera_config = test_dataset.datasets['camera_config'].read_sample_at_idx(
        i, 0)
    extrinsic = camera_config['pose']
    intrinsic = np.reshape(camera_config['intrinsics'], (3, 3))
    extrinsic = extrinsic.astype(np.float32)
    intrinsic = intrinsic.astype(np.float32)
    color_shape = color.shape
    observations = [{'color': color.tobytes(),
                     'color_shape': color_shape,
                     'intrinsics': intrinsic.tobytes(),
                     'extrinsics': extrinsic.tobytes()}]
    opt_conf = OmegaConf.to_container(
        cfg.validation.grasp_opt_config['optimization_config'])
    payload = {
        'observations': observations,
        'optimization_config': opt_conf,
        'texts': text,
        'optimizer_name': "language_1_view",
        'return_trajectory': True,
        'reset_optimizer': False
    }
    # request_id = http_client.submit_task('process_np_array', payload)
    request_id = http_client.submit_task('/optimize_poses', payload)
    optimized_pose = None
    while optimized_pose is None:
        time.sleep(0.2)
        optimized_pose = http_client.get_result(request_id)
    op_xyz = optimized_pose[:3, 3]
    gt_xyz = gt_pose[:3, 3]
    xyz_off = gt_xyz - op_xyz
    print(f'Result: \n {optimized_pose}')
    print(f"Expected: \n {gt_pose}")
    print("Off by: ", xyz_off)


if __name__ == "__main__":
    main()
