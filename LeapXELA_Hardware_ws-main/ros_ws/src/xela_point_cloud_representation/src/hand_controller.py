#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

import os

from ament_index_python.packages import get_package_share_directory

import mujoco as mj
from mujoco import mjtObj

from sensor_msgs.msg import JointState

from PyQt5 import QtCore, QtWidgets

class HandController(Node):
    def __init__(self) -> None:
        super().__init__("hand_controller")
        ################## MujoCo model loading ##########################
        xela_description_share = get_package_share_directory("xela_description")
        self._model_path = os.path.join(xela_description_share, "mjcf", "scene.xml")
        # MuJoCo's Python API loads MJCF via from_xml_path (not from_file).
        self._model = mj.MjModel.from_xml_path(self._model_path)
        self.joint_limits = self.get_joint_limits()
        self.get_logger().info(f"Joint limits: {self.joint_limits}")
        ################### ROS publisher ####################
        self._joint_pub = self.create_publisher(JointState, "xela_joint_publisher", 10)
        self._joint_names = list(self.joint_limits.keys())
        # Current (pending) slider values live here (can change without publishing).
        self._joint_positions = {name: 0.0 for name in self._joint_names}
        # Latched values that are continuously published after pressing Publish.
        self._latched_joint_positions = {name: 0.0 for name in self._joint_names}
        self._publishing_enabled = False
        for name, (lo, hi) in self.joint_limits.items():
            if lo <= 0.0 <= hi:
                self._joint_positions[name] = 0.0
            else:
                self._joint_positions[name] = 0.5 * (lo + hi)
        self._latched_joint_positions.update(self._joint_positions)

        # Continuous publisher (only active when enabled via the UI button).
        self._publish_timer = self.create_timer(0.05, self._publish_if_enabled)

        ################### UI ####################
        self._qt_app = None
        self._window = None
        self._spin_timer = None
        self._sliders = {}
        self._value_labels = {}
    


    def get_joint_limits(self) -> dict:
        joint_limits = {}
        # MuJoCo Python bindings differ slightly by version (njnt vs njoint).
        njnt = getattr(self._model, "njnt", None)
        if njnt is None:
            njnt = getattr(self._model, "njoint", None)
        if njnt is None and hasattr(self._model, "joint"):
            njnt = len(self._model.joint)
        if njnt is None:
            raise AttributeError("Could not determine number of joints from MuJoCo model.")

        for i in range(int(njnt)):
            joint_name = mj.mj_id2name(self._model, mjtObj.mjOBJ_JOINT, i) or str(i)
            joint_limits[joint_name] = (
                float(self._model.jnt_range[i, 0]),
                float(self._model.jnt_range[i, 1]),
            )
        return joint_limits

    def publish_joint_state(self, positions: dict | None = None) -> None:
        if positions is None:
            positions = self._joint_positions
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(self._joint_names)
        msg.position = [float(positions[n]) for n in self._joint_names]
        self._joint_pub.publish(msg)

    def _publish_if_enabled(self) -> None:
        if self._publishing_enabled:
            self.publish_joint_state(self._latched_joint_positions)

    def latch_and_start_publishing(self) -> None:
        self._latched_joint_positions.update(self._joint_positions)
        self._publishing_enabled = True
        self.publish_joint_state(self._latched_joint_positions)

    @staticmethod
    def _slider_to_value(slider_int: int, lo: float, hi: float, steps: int) -> float:
        if steps <= 0:
            return float(lo)
        t = float(slider_int) / float(steps)
        return float(lo + t * (hi - lo))

    @staticmethod
    def _value_to_slider(value: float, lo: float, hi: float, steps: int) -> int:
        if hi == lo or steps <= 0:
            return 0
        t = (float(value) - float(lo)) / (float(hi) - float(lo))
        if t < 0.0:
            t = 0.0
        if t > 1.0:
            t = 1.0
        return int(round(t * steps))

    def start_ui(self) -> int:
        self._qt_app = QtWidgets.QApplication([])

        self._window = QtWidgets.QWidget()
        self._window.setWindowTitle("XELA Joint Publisher")
        root = QtWidgets.QVBoxLayout(self._window)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        root.addWidget(scroll)

        inner = QtWidgets.QWidget()
        form = QtWidgets.QFormLayout(inner)
        form.setLabelAlignment(QtCore.Qt.AlignLeft)
        scroll.setWidget(inner)

        steps = 1000
        for joint_name in self._joint_names:
            lo, hi = self.joint_limits[joint_name]

            row = QtWidgets.QWidget()
            row_layout = QtWidgets.QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)

            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(steps)
            slider.setSingleStep(1)
            slider.setPageStep(10)
            slider.setTracking(True)
            slider.setValue(self._value_to_slider(self._joint_positions[joint_name], lo, hi, steps))

            value_label = QtWidgets.QLabel()
            value_label.setMinimumWidth(220)

            def on_change(v: int, jn=joint_name, jlo=lo, jhi=hi) -> None:
                val = self._slider_to_value(v, jlo, jhi, steps)
                self._joint_positions[jn] = val
                self._value_labels[jn].setText(f"{val:.4f}  [{jlo:.4f}, {jhi:.4f}]")
                # Intentionally do not publish here; publishing is latched by the button.

            slider.valueChanged.connect(on_change)

            self._sliders[joint_name] = slider
            self._value_labels[joint_name] = value_label
            value_label.setText(
                f"{self._joint_positions[joint_name]:.4f}  [{lo:.4f}, {hi:.4f}]"
            )

            row_layout.addWidget(slider, 1)
            row_layout.addWidget(value_label, 0)

            form.addRow(joint_name, row)

        btn_row = QtWidgets.QWidget()
        btn_layout = QtWidgets.QHBoxLayout(btn_row)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        publish_btn = QtWidgets.QPushButton("Publish (latch & stream)")
        publish_btn.clicked.connect(self.latch_and_start_publishing)
        btn_layout.addStretch(1)
        btn_layout.addWidget(publish_btn, 0)
        root.addWidget(btn_row)

        self._spin_timer = QtCore.QTimer()
        self._spin_timer.setInterval(10)
        self._spin_timer.timeout.connect(lambda: rclpy.spin_once(self, timeout_sec=0.0))
        self._spin_timer.start()

        self._window.resize(900, 600)
        self._window.show()

        # Do not start streaming until the user presses Publish.
        return int(self._qt_app.exec_())

def main(args=None) -> None:
    rclpy.init(args=args)
    node = HandController()
    try:
        exit_code = node.start_ui()
    except KeyboardInterrupt:
        exit_code = 0
    finally:
        node.destroy_node()
        rclpy.shutdown()
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
