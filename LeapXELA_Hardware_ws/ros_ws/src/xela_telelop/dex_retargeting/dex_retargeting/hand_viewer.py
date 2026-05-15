"""ROS 2 node: Sapien viewer that applies JointState from hand_pose_publisher."""
from pathlib import Path
from typing import Optional

import numpy as np
import rclpy
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
from dex_retargeting.sapien_robot_setup import create_viewer_with_robot


def _enum_from_str(enum_cls, value: str):
    try:
        return enum_cls[value]
    except KeyError as e:
        valid = ", ".join(m.name for m in enum_cls)
        raise ValueError(f"Invalid {enum_cls.__name__} {value!r}. Expected one of: {valid}") from e


class HandViewer(Node):
    def __init__(self):
        super().__init__("hand_viewer")

        self.declare_parameter("robot_name", "leap")
        self.declare_parameter("retargeting_type", "dexpilot")
        self.declare_parameter("hand_type", "right")
        self.declare_parameter("topic", "hand_pose")
        self.declare_parameter("render_hz", 60.0)

        robot_name = _enum_from_str(RobotName, self.get_parameter("robot_name").value)
        retargeting_type = _enum_from_str(
            RetargetingType, self.get_parameter("retargeting_type").value
        )
        hand_type = _enum_from_str(HandType, self.get_parameter("hand_type").value)
        topic = self.get_parameter("topic").value
        render_hz = float(self.get_parameter("render_hz").value)

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
        retargeting = RetargetingConfig.load_from_file(str(config_path)).build()
        self._pin_joint_names = list(retargeting.joint_names)

        self._scene, self._viewer, self._robot, sapien_joint_names = (
            create_viewer_with_robot(str(config_path), str(robot_dir))
        )

        pin_indices = [
            self._pin_joint_names.index(name) for name in sapien_joint_names
        ]
        self._retargeting_to_sapien = np.array(pin_indices, dtype=int)

        self._latest_qpos: Optional[np.ndarray] = None
        self.create_subscription(JointState, topic, self._on_joint, 10)
        period = 1.0 / max(render_hz, 1.0)
        self.create_timer(period, self._render_tick)

        self.get_logger().info(f"Subscribing to JointState on '{topic}'.")

    def _on_joint(self, msg: JointState):
        if not msg.name or not msg.position:
            return
        if list(msg.name) != self._pin_joint_names:
            name_to_i = {n: i for i, n in enumerate(msg.name)}
            try:
                qpos = np.array(
                    [float(msg.position[name_to_i[n]]) for n in self._pin_joint_names],
                    dtype=np.float64,
                )
            except KeyError:
                self.get_logger().warn(
                    "JointState names do not match expected pin joint names; skipping."
                )
                return
        else:
            qpos = np.array(msg.position, dtype=np.float64)
        if qpos.shape[0] != len(self._pin_joint_names):
            self.get_logger().warn("JointState length mismatch; skipping.")
            return
        self._latest_qpos = qpos

    def _render_tick(self):
        if self._latest_qpos is not None:
            sapien_q = self._latest_qpos[self._retargeting_to_sapien]
            self._robot.set_qpos(sapien_q)
        for _ in range(2):
            self._viewer.render()


def main(args=None):
    rclpy.init(args=args)
    node = HandViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
