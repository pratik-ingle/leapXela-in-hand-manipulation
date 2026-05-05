#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

import mujoco as mj
import mujoco.viewer


class VisulizeMjcfNode(Node):
    def __init__(self) -> None:
        super().__init__("visulize_mjcf")

        self.declare_parameter("scene_path", "scene.xml")
        self._scene_path: str = self.get_parameter("scene_path").value

        self.get_logger().info(f"Scene path: {self._scene_path}")

        spec = mj.MjSpec.from_file(self._scene_path)

        self._model = spec.compile()
        self._data = mj.MjData(self._model)

        self.render()


    def render(self):
        with mujoco.viewer.launch_passive(
            model=self._model, data=self._data, show_left_ui=False, show_right_ui=False
        ) as viewer:
            mj.mjv_defaultFreeCamera(self._model, viewer.cam)
            mj.mj_forward(self._model, self._data)

            while viewer.is_running():
                mj.mj_step(self._model, self._data)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = VisulizeMjcfNode()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
