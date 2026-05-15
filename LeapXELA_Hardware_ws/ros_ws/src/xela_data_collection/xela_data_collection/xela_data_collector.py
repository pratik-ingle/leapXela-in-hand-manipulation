#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image

import numpy as np
from pathlib import Path

from leap_hand.srv import LeapState
from sensor_msgs.msg import JointState

from datetime import datetime

class Storage:
    def __init__(self, stream_name: str):
        date = datetime.now().strftime("%Y%m%d")
        time = datetime.now().strftime("%H%M%S")
        self.stream_name = stream_name + "_" + date + "_" + time
        self.current_index = 0
        self._file = None
        self._ensure_open()
    
    def store(self, raw_image: Image, normalized_image: Image, state: JointState):
        self._ensure_open()
        idx = f"{self.current_index:06d}"
        grp = self._root.require_group(idx)

        raw_arr = self._decode_ros_image(raw_image)
        norm_arr = self._decode_ros_image(normalized_image)

        self._write_or_replace_dataset(grp, "raw_image", raw_arr)
        self._write_or_replace_dataset(grp, "normalized_image", norm_arr)

        self._write_image_attrs(grp["raw_image"], raw_image)
        self._write_image_attrs(grp["normalized_image"], normalized_image)

        st = grp.require_group("state")
        self._write_or_replace_dataset(st, "position", np.asarray(state.position, dtype=np.float64))
        self._write_or_replace_dataset(st, "velocity", np.asarray(state.velocity, dtype=np.float64))
        self._write_or_replace_dataset(st, "effort", np.asarray(state.effort, dtype=np.float64))

        name_dt = self._h5py.string_dtype(encoding="utf-8")
        self._write_or_replace_dataset(
            st, "name", np.asarray(state.name, dtype=object).astype(name_dt)
        )

        if state.header is not None:
            st.attrs["stamp_sec"] = int(state.header.stamp.sec)
            st.attrs["stamp_nanosec"] = int(state.header.stamp.nanosec)
            st.attrs["frame_id"] = str(state.header.frame_id)

        grp.attrs["index"] = int(self.current_index)
        self._file.flush()
        self.current_index += 1

    def close(self) -> None:
        if getattr(self, "_file", None) is not None:
            try:
                self._file.flush()
                self._file.close()
            finally:
                self._file = None

    def __del__(self) -> None:  # pragma: no cover
        try:
            self.close()
        except Exception:
            pass

    def _ensure_open(self) -> None:
        if getattr(self, "_file", None) is not None:
            return
        try:
            import h5py  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError(
                "HDF5 support requires 'h5py'. Install it (e.g. apt/pip) and retry."
            ) from e

        self._h5py = h5py
        self._path = Path.cwd() / "data" / f"{self.stream_name}.h5"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._file = self._h5py.File(self._path, "a")
        self._root = self._file.require_group(self.stream_name)

    def _decode_ros_image(self, msg: Image) -> np.ndarray:
        self._ensure_open()
        h, w = int(msg.height), int(msg.width)
        channels = 3

        enc = (msg.encoding or "").upper()
        if "32F" in enc:
            dtype = np.float32
        elif "32S" in enc or "32I" in enc:
            dtype = np.int32
        elif "16U" in enc:
            dtype = np.uint16
        elif "8U" in enc:
            dtype = np.uint8
        else:
            dtype = np.float32

        arr = np.frombuffer(msg.data, dtype=dtype)
        expected = h * w * channels
        if arr.size != expected:
            raise ValueError(
                f"Unexpected image buffer size: got {arr.size}, expected {expected} "
                f"(h={h}, w={w}, channels={channels}, dtype={dtype}, enc={msg.encoding})."
            )
        return arr.reshape((h, w, channels))

    def _write_or_replace_dataset(self, group, name: str, data: np.ndarray) -> None:
        self._ensure_open()
        if name in group:
            del group[name]
        group.create_dataset(
            name, data=data, compression="gzip", compression_opts=4, shuffle=True
        )

    def _write_image_attrs(self, ds, msg: Image) -> None:
        ds.attrs["height"] = int(msg.height)
        ds.attrs["width"] = int(msg.width)
        ds.attrs["encoding"] = str(msg.encoding)
        ds.attrs["is_bigendian"] = int(msg.is_bigendian)
        ds.attrs["step"] = int(msg.step)
        if msg.header is not None:
            ds.attrs["stamp_sec"] = int(msg.header.stamp.sec)
            ds.attrs["stamp_nanosec"] = int(msg.header.stamp.nanosec)
            ds.attrs["frame_id"] = str(msg.header.frame_id)
    


class XelaDataCollector(Node):
    """
    Subscribes to:
      - /leap_image (published by xela_image_publisher)
      - /leap_image_normalized (published by xela_image_publisher)

    If message_filters is available, uses approximate time synchronization and
    calls a single paired callback. Otherwise, falls back to two independent
    subscriptions and logs reception.
    """

    def __init__(self):
        super().__init__("xela_data_collector")


        self.storage = Storage("xela_data")

        self._last_raw: Image | None = None
        self._last_norm: Image | None = None
        self._last_state: JointState | None = None
        # Prefer synchronized callbacks when possible
        try:
            from message_filters import Subscriber, ApproximateTimeSynchronizer

            self._raw_sub = Subscriber(self, Image, "/leap_image")
            self._norm_sub = Subscriber(self, Image, "/leap_image_normalized")
            self._state_sub = Subscriber(self, JointState, "/leap_state")
            # Reasonable defaults for two topics at ~same rate
            self._sync = ApproximateTimeSynchronizer(
                [self._raw_sub, self._norm_sub, self._state_sub],
                queue_size=30,
                slop=0.05,
                allow_headerless=False,
            )
            self._sync.registerCallback(self._on_synced_images)
            self.get_logger().info("Using approximate time sync for image topics.")
        except Exception as e:
            self.get_logger().warn(
                f"message_filters not available (or failed to init): {e}. "
                "Falling back to independent subscriptions."
            )
            self._sub_raw = self.create_subscription(Image, "/leap_image", self._on_raw, 10)
            self._sub_norm = self.create_subscription(
                Image, "/leap_image_normalized", self._on_norm, 10
            )
            self._state_sub = self.create_subscription(JointState, "/leap_state", self._on_state, 10)
    
    
    def _decode_image(self, msg: Image, *, dtype: np.dtype) -> np.ndarray:
        # Publisher uses 3 channels and packs raw bytes.
        h, w = int(msg.height), int(msg.width)
        arr = np.frombuffer(msg.data, dtype=dtype)

        expected = h * w * 3
        if arr.size != expected:
            raise ValueError(
                f"Unexpected image buffer size: got {arr.size}, expected {expected} "
                f"(h={h}, w={w}, channels=3, dtype={dtype})."
            )
        return arr.reshape((h, w, 3))

    def _on_synced_images(self, raw_msg: Image, norm_msg: Image, state_msg: JointState):
        self._last_raw = raw_msg
        self._last_norm = norm_msg
        self._last_state = state_msg
        # Note: xela_image_publisher sets encoding "32FC3" for both topics, but
        # /leap_image is currently filled from an int32 array. We decode raw as int32
        # and normalized as float32 to match the actual byte content.

        self.storage.store(raw_msg, norm_msg, state_msg)
        try:
            raw = self._decode_image(raw_msg, dtype=np.int32)
            norm = self._decode_image(norm_msg, dtype=np.float32)
        except Exception as e:
            self.get_logger().error(f"Failed to decode images: {e}")
            return

        self.get_logger().info(
            f"Synced images: raw[{raw.shape}] norm[{norm.shape}] "
            f"t_raw={raw_msg.header.stamp.sec}.{raw_msg.header.stamp.nanosec:09d} "
            f"t_norm={norm_msg.header.stamp.sec}.{norm_msg.header.stamp.nanosec:09d}"
            f"t_state={state_msg.header.stamp.sec}.{state_msg.header.stamp.nanosec:09d}"
        )

     

    def _on_raw(self, msg: Image):
        self._last_raw = msg
        self.get_logger().debug(
            f"Raw image received: {msg.height}x{msg.width} enc={msg.encoding}"
        )

    def _on_norm(self, msg: Image):
        self._last_norm = msg
        self.get_logger().debug(
            f"Normalized image received: {msg.height}x{msg.width} enc={msg.encoding}"
        )

    def _on_state(self, msg: JointState):
        self._last_state = msg
        self.get_logger().debug(f"Hand state received: {msg.position} {msg.velocity} {msg.effort}")


def main(args=None):
    rclpy.init(args=args)
    node = XelaDataCollector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

