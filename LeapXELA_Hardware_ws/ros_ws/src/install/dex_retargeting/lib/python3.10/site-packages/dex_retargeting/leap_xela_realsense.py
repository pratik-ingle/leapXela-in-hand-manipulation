import multiprocessing
import time
from queue import Empty
from typing import Optional
import pyrealsense2 as rs

import cv2
import numpy as np
import tyro
from loguru import logger
from dex_retargeting.resource_paths import get_robot_hand_urdf_dir
from dex_retargeting.sapien_robot_setup import create_viewer_with_robot

from dex_retargeting.constants import (
    RobotName,
    RetargetingType,
    HandType,
    get_default_config_path,
)
from dex_retargeting.retargeting_config import RetargetingConfig
from dex_retargeting.single_hand_detector import SingleHandDetector


def start_retargeting(queue: multiprocessing.Queue, robot_dir: str, config_path: str):
    RetargetingConfig.set_default_urdf_dir(str(robot_dir))
    logger.info(f"Start retargeting with config {config_path}")
    retargeting = RetargetingConfig.load_from_file(config_path).build()

    hand_type = "Right" if "right" in config_path.lower() else "Left"
    detector = SingleHandDetector(hand_type=hand_type, selfie=False)

    _scene, viewer, robot, sapien_joint_names = create_viewer_with_robot(
        config_path, str(robot_dir)
    )

    retargeting_joint_names = retargeting.joint_names
    retargeting_to_sapien = np.array(
        [retargeting_joint_names.index(name) for name in sapien_joint_names]
    ).astype(int)

    while True:
        try:
            bgr = queue.get(timeout=5)
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        except Empty:
            logger.error(
                "Fail to fetch image from camera in 5 secs. Please check your web camera device."
            )
            return

        _, joint_pos, keypoint_2d, wrist_rot = detector.detect(rgb)
        bgr = detector.draw_skeleton_on_image(bgr, keypoint_2d, style="default")
        cv2.imshow("realtime_retargeting_demo", bgr)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if joint_pos is None:
            logger.warning(f"{hand_type} hand is not detected.")
        else:
            retargeting_type = retargeting.optimizer.retargeting_type
            indices = retargeting.optimizer.target_link_human_indices
            if retargeting_type == "POSITION":
                indices = indices
                ref_value = joint_pos[indices, :]
            else:
                origin_indices = indices[0, :]
                task_indices = indices[1, :]
                ref_value = joint_pos[task_indices, :] - joint_pos[origin_indices, :]
            qpos = retargeting.retarget(ref_value)
            robot.set_qpos(qpos[retargeting_to_sapien])

        for _ in range(2):
            viewer.render()


def produce_frame(queue: multiprocessing.Queue, camera_path: Optional[str] = None):
    """
    Captures color frames from a RealSense camera and puts them into a multiprocessing queue.

    Parameters:
        queue (multiprocessing.Queue): Queue to put frames into.
        camera_path (Optional[str]): Not used with RealSense. Reserved for interface consistency.
    """
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)

    time.sleep(2)

    try:
        while True:
            frames = pipeline.wait_for_frames(15000)
            color_frame = frames.get_color_frame()

            if not color_frame:
                continue

            color_image = np.asanyarray(color_frame.get_data())
            queue.put(color_image)
            time.sleep(1 / 30.0)

    except Exception as e:
        print(f"Error in RealSense stream: {e}")

    finally:
        pipeline.stop()


def main(
    robot_name: RobotName = RobotName.leap_xela,
    retargeting_type: RetargetingType = RetargetingType.dexpilot,
    hand_type: HandType = HandType.right,
    camera_path: Optional[str] = None,
):
    """
    RealSense hand retargeting demo for the Leap XELA right-hand URDF
    (`assets/robots/hands/leap_xela/leap_xela_right.urdf`).

    Only right-hand configs are provided for leap_xela in this package.
    """
    config_path = get_default_config_path(robot_name, retargeting_type, hand_type)
    robot_dir = get_robot_hand_urdf_dir()

    queue = multiprocessing.Queue(maxsize=1000)
    producer_process = multiprocessing.Process(
        target=produce_frame, args=(queue, camera_path)
    )
    consumer_process = multiprocessing.Process(
        target=start_retargeting, args=(queue, str(robot_dir), str(config_path))
    )

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()
    time.sleep(5)

    print("done")


if __name__ == "__main__":
    tyro.cli(main)
