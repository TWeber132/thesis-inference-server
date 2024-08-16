import hydra
import numpy as np

from inference_server_client import InferenceServerClient


@hydra.main(version_base=None, config_path="./configs", config_name="language_1_view")
def main(cfg):
    """If load_dataset_language dependency can be met

    # test_dataset = load_dataset_language(
    #     cfg.dataset.n_perspectives, cfg.dataset.path + '/test')

    # i = 0
    # text_query = test_dataset.datasets['language'].read_sample(i)
    # gt_pose = test_dataset.datasets['grasp_pose'].read_sample(i)['grasp_pose']

    # colors = []
    # extrinsics = []
    # intrinsics = []
    # for idx in range(3):
    #     color = test_dataset.datasets['color'].read_sample_at_idx(
    #         i, idx)[..., :3]
    #     camera_config = test_dataset.datasets['camera_config'].read_sample_at_idx(
    #         i, idx)
    #     extrinsic = camera_config['pose'].astype(dtype=np.float32)
    #     intrinsic = camera_config['intrinsics'].astype(dtype=np.float32)
    #     colors.append(color)
    #     extrinsics.append(extrinsic)
    #     intrinsics.append(intrinsic)

        Otherwise some random data"""
    text_query = "Grasp something, anything really"
    gt_pose = np.ones((4, 4), dtype=np.float32)
    colors = [np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)]*3
    extrinsic = np.array([[1., 0., 0., 0.],
                          [0., 1., 0., 0.],
                          [0., 0., 1., 0.],
                          [0., 0., 0., 1.]], dtype=np.float32)
    extrinsics = [extrinsic]*3
    intrinsic = np.array(
        (450., 0, 320., 0, 450., 240., 0, 0, 1), dtype=np.float32)
    intrinsics = [intrinsic]*3

    inference_server_client = InferenceServerClient(
        url="http://172.20.1.3:31708")
    optimized_pose = inference_server_client.optimize_pose(camera_color_imgs=colors,
                                                           camera_pose_htms=extrinsics,
                                                           camera_instrinsics=intrinsics,
                                                           optimization_config=cfg.optimization_config,
                                                           text_query=text_query)
    op_xyz = optimized_pose[:3, 3]
    gt_xyz = gt_pose[:3, 3]
    xyz_off = gt_xyz - op_xyz
    print(f'Result: \n {optimized_pose}')
    print(f"Expected: \n {gt_pose}")
    print("Off by: ", xyz_off)


if __name__ == "__main__":
    main()
