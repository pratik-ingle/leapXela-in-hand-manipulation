"""ROS 2 node: RealSense + hand detection + retargeting; publishes robot joint state."""
from pathlib import Path
import threading
import time
from queue import Empty, Queue
import cv2
import numpy as np
import pyrealsense2 as rs
import rclpy
from loguru import logger
from rclpy.node import Node
from sensor_msgs.msg import JointState

from dex_retargeting.constants import (
    HandType,
    RetargetingType,
    RobotName,
    get_default_config_path,
)
from dex_retargeting.resource_paths import get_robot_hand_urdf_dir
from dex_retargeting.retargeting_config import RetargetingConfig
from dex_retargeting.single_hand_detector import SingleHandDetector


def _enum_from_str(enum_cls, value: str):
    try:
        return enum_cls[value]
    except KeyError as e:
        valid = ", ".join(m.name for m in enum_cls)
        raise ValueError(f"Invalid {enum_cls.__name__} {value!r}. Expected one of: {valid}") from e


def produce_frame_rs(frame_queue: Queue, stop_event: threading.Event):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)
    time.sleep(2)
    try:
        while not stop_event.is_set():
            frames = pipeline.wait_for_frames(15000)
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            color_image = np.asanyarray(color_frame.get_data())
            try:
                frame_queue.put_nowait(color_image)
            except Exception:
                pass
            time.sleep(1 / 30.0)
    except Exception as e:
        logger.error(f"RealSense stream error: {e}")
    finally:
        pipeline.stop()


class HandPosePublisher(Node):
    def __init__(self):
        super().__init__("hand_pose_publisher")

        self.declare_parameter("robot_name", "leap")
        self.declare_parameter("retargeting_type", "dexpilot")
        self.declare_parameter("hand_type", "right")
        self.declare_parameter("topic", "hand_pose")
        self.declare_parameter("show_camera", True)

        robot_name = _enum_from_str(RobotName, self.get_parameter("robot_name").value)
        retargeting_type = _enum_from_str(
            RetargetingType, self.get_parameter("retargeting_type").value
        )
        hand_type = _enum_from_str(HandType, self.get_parameter("hand_type").value)
        topic = self.get_parameter("topic").value
        self._show_camera = self.get_parameter("show_camera").value

        # leap_xela assets/configs in this repo are right-hand only.
        if robot_name is RobotName.leap_xela and hand_type is HandType.left:
            self.get_logger().warn(
                "robot_name=leap_xela only provides right-hand configs; falling back to hand_type=right."
            )
            hand_type = HandType.right

        config_path = get_default_config_path(robot_name, retargeting_type, hand_type)
        if config_path is None:
            raise RuntimeError("Could not resolve retargeting config path.")
        if not Path(config_path).exists():
            raise RuntimeError(
                f"Retargeting config does not exist: {str(config_path)} "
                f"(robot_name={robot_name.name}, retargeting_type={retargeting_type.name}, hand_type={hand_type.name})"
            )

        robot_dir = get_robot_hand_urdf_dir()
        RetargetingConfig.set_default_urdf_dir(str(robot_dir))
        self._retargeting = RetargetingConfig.load_from_file(str(config_path)).build()

        hand_label = "Right" if hand_type == HandType.right else "Left"
        self._detector = SingleHandDetector(hand_type=hand_label, selfie=False)

        joint_names = list(self._retargeting.joint_names)
        self._pub = self.create_publisher(JointState, topic, 10)
        self._msg = JointState()
        self._msg.name = joint_names

        self._frame_queue: Queue = Queue(maxsize=2)
        self._stop = threading.Event()
        self._cam_thread = threading.Thread(
            target=produce_frame_rs, args=(self._frame_queue, self._stop), daemon=True
        )
        self._cam_thread.start()

        self._timer = self.create_timer(1.0 / 30.0, self._on_timer)

        self.get_logger().info(
            f"Publishing JointState on '{topic}' ({len(joint_names)} joints)."
        )

    def _on_timer(self):
        try:
            bgr = self._frame_queue.get(timeout=0.01)
        except Empty:
            return

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        _, joint_pos, keypoint_2d, _wrist_rot = self._detector.detect(rgb)
        if self._show_camera:
            bgr = self._detector.draw_skeleton_on_image(bgr, keypoint_2d, style="default")
            cv2.imshow("hand_pose_publisher", bgr)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                self.get_logger().info("Quit requested from camera window.")
                rclpy.shutdown()

        if joint_pos is None:
            return

        retargeting = self._retargeting
        retargeting_type = retargeting.optimizer.retargeting_type
        indices = retargeting.optimizer.target_link_human_indices
        if retargeting_type == "POSITION":
            ref_value = joint_pos[indices, :]
        else:
            origin_indices = indices[0, :]
            task_indices = indices[1, :]
            ref_value = joint_pos[task_indices, :] - joint_pos[origin_indices, :]

        qpos = retargeting.retarget(ref_value)
        self._msg.header.stamp = self.get_clock().now().to_msg()
        self._msg.position = [float(x) for x in qpos.tolist()]
        self._pub.publish(self._msg)

    def destroy_node(self):
        self._stop.set()
        cv2.destroyAllWindows()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = HandPosePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
