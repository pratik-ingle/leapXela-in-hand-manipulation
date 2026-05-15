#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2

import threading
import time
from typing import Optional

import numpy as np
import open3d as o3d


class HandTouchPointCloud(Node):
    def __init__(self) -> None:
        super().__init__('hand_touch_point_cloud')
        self.subscription = self.create_subscription(
            PointCloud2,
            'hand_touch_point_cloud',
            self._on_point_cloud,
            10,
        )

        self._lock = threading.Lock()
        self._latest_xyz: Optional[np.ndarray] = None
        self._latest_stamp_ns: Optional[int] = None
        self._last_log_time_ns = 0
        self._stop_event = threading.Event()

        self._viewer_thread = threading.Thread(target=self._viewer_loop, daemon=True)
        self._viewer_thread.start()

    def _on_point_cloud(self, msg: PointCloud2) -> None:
        pts = point_cloud2.read_points(msg, field_names=('x', 'y', 'z'), skip_nans=True)
        xyz = np.fromiter((c for p in pts for c in p), dtype=np.float32).reshape(-1, 3)
        with self._lock:
            self._latest_xyz = xyz
            self._latest_stamp_ns = self.get_clock().now().nanoseconds

        # Throttled log: confirm we are actually receiving points.
        now_ns = self.get_clock().now().nanoseconds
        if now_ns - self._last_log_time_ns > int(1.0e9):
            self._last_log_time_ns = now_ns
            if xyz.size == 0:
                self.get_logger().warn('Received PointCloud2 but 0 points after filtering NaNs.')
            else:
                mn = xyz.min(axis=0)
                mx = xyz.max(axis=0)
                self.get_logger().info(
                    f'Received {xyz.shape[0]} points. Bounds min={mn.tolist()} max={mx.tolist()}'
                )

    def destroy_node(self) -> bool:
        self._stop_event.set()
        return super().destroy_node()

    def _viewer_loop(self) -> None:
        vis = o3d.visualization.Visualizer()
        vis.create_window(window_name='hand_touch_point_cloud', width=960, height=720)

        pcd = o3d.geometry.PointCloud()
        vis.add_geometry(pcd)
        vis.add_geometry(o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.05))

        render_opt = vis.get_render_option()
        if render_opt is not None:
            render_opt.background_color = np.asarray([0.0, 0.0, 0.0])
            render_opt.point_size = 5.0

        view_ctl = vis.get_view_control()
        last_stamp_ns: Optional[int] = None
        ever_reset = False

        while not self._stop_event.is_set():
            xyz: Optional[np.ndarray] = None
            stamp_ns: Optional[int] = None
            with self._lock:
                if self._latest_xyz is not None:
                    xyz = self._latest_xyz
                    self._latest_xyz = None
                    stamp_ns = self._latest_stamp_ns
                    self._latest_stamp_ns = None

            if xyz is not None:
                pcd.points = o3d.utility.Vector3dVector(xyz.astype(np.float64, copy=False))
                pcd.paint_uniform_color([0.1, 0.8, 0.1])
                vis.update_geometry(pcd)

                # If the first cloud arrives (or a newer cloud comes in), reset camera once so
                # we actually see the points even if the default view is "looking away".
                if stamp_ns is not None and stamp_ns != last_stamp_ns:
                    last_stamp_ns = stamp_ns
                    if view_ctl is not None and not ever_reset:
                        view_ctl.set_zoom(0.8)
                        vis.reset_view_point(True)
                        ever_reset = True

            vis.poll_events()
            vis.update_renderer()
            time.sleep(0.01)

        vis.destroy_window()


def main(args=None) -> None:
    rclpy.init(args=args)
    node = HandTouchPointCloud()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
