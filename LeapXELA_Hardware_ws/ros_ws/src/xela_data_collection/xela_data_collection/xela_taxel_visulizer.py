#!/usr/bin/env python3

import threading
from typing import Optional

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class XelaTaxelVisualizer(Node):
    def __init__(self) -> None:
        super().__init__("xela_taxel_visualizer")

        self._lock = threading.Lock()
        self._latest: Optional[np.ndarray] = None
        self._dirty = False

        self._sub = self.create_subscription(Image, "/leap_image_normalized", self._on_image, 10)

    def _on_image(self, msg: Image) -> None:
        if msg.encoding != "32FC3":
            self.get_logger().warning(
                f"Unsupported encoding: {msg.encoding} (expected 32FC3)"
            )
            return

        expected_step = msg.width * 3 * 4  # 3 channels * float32 bytes
        if msg.step != expected_step:
            self.get_logger().warning(
                f"Unexpected step: {msg.step} (expected {expected_step})"
            )

        img = np.frombuffer(msg.data, dtype=np.float32)
        expected_size = int(msg.height * msg.width * 3)
        if img.size != expected_size:
            self.get_logger().warning(
                f"Unexpected data size: {img.size} (expected {expected_size})"
            )
            return

        img = img.reshape((int(msg.height), int(msg.width), 3))
        with self._lock:
            self._latest = img
            self._dirty = True

    def pop_latest(self) -> Optional[np.ndarray]:
        with self._lock:
            if not self._dirty:
                return None
            self._dirty = False
            return None if self._latest is None else self._latest.copy()


def main(args=None) -> None:
    # Matplotlib should run in the main thread on many platforms.
    import matplotlib.pyplot as plt

    rclpy.init(args=args)
    node = XelaTaxelVisualizer()

    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()

    plt.ion()
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    fig.canvas.manager.set_window_title("Leap XELA /leap_image channels")

    ims = []
    channel_labels = ["X", "Y", "Z"]
    for i, ax in enumerate(axes):
        ax.set_title(channel_labels[i])
        ax.set_xticks([])
        ax.set_yticks([])
        im = ax.imshow(np.zeros((26, 31), dtype=np.float32), cmap="viridis")
        ims.append(im)

    plt.tight_layout()

    try:
        while rclpy.ok() and plt.fignum_exists(fig.number):
            img = node.pop_latest()
            if img is not None:
                for c in range(3):
                    channel = img[:, :, c]
                    ims[c].set_data(channel)
                    # Keep autoscaling responsive to incoming data
                    ims[c].set_clim(float(np.nanmin(channel)), float(np.nanmax(channel)))
                fig.canvas.draw_idle()

            plt.pause(0.03)  # ~33 FPS UI update loop
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        try:
            plt.close(fig)
        except Exception:
            pass

