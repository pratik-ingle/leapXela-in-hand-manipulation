#!/usr/bin/env python3

import sys


def main() -> int:
    try:
        import pyrealsense2 as rs
    except Exception as e:
        print(
            "Failed to import pyrealsense2. Install librealsense Python bindings.\n"
            f"Error: {e}",
            file=sys.stderr,
        )
        return 1

    try:
        import cv2
        import numpy as np
    except Exception as e:
        print(f"Failed to import OpenCV/numpy: {e}", file=sys.stderr)
        return 1

    pipeline = rs.pipeline()
    config = rs.config()

    # D435i supports both color + depth. If your camera differs, adjust these.
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    align_to = rs.stream.color
    align = rs.align(align_to)
    colorizer = rs.colorizer()

    try:
        pipeline.start(config)
    except Exception as e:
        print(f"Failed to start RealSense pipeline: {e}", file=sys.stderr)
        return 1

    try:
        while True:
            # The default timeout is 5000ms; on some systems the first frames can
            # take longer right after `pipeline.start()`.
            frames = pipeline.wait_for_frames(20000)
            # frames = align.process(frames)
            print("getting frames")

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                continue

            color = np.asanyarray(color_frame.get_data())
            depth_color = np.asanyarray(colorizer.colorize(depth_frame).get_data())

            stacked = np.hstack((color, depth_color))
            cv2.imshow("RealSense (color | depth)", stacked)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):  # q or ESC
                break
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.stop()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())