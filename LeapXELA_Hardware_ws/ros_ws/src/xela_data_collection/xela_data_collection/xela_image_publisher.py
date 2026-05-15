#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from xela_server_ros2.srv import XelaSensorStream
from xela_server_ros2.msg import SensStream
from .leapXelaMap import LEAP_XELA_ID


import numpy as np

class LeapImage():
    def __init__(self):
        #channels x,y,z
        # Use float32 so we can publish as "32FC3"
        self.image = np.zeros((26, 31, 3), dtype=np.int32)
        self.image_normalized = np.zeros((26, 31, 3), dtype=np.float32)
        self.ids = LEAP_XELA_ID

    def fill_image(self, msg: SensStream):
        for idx, taxel in enumerate(msg.sensors[0].taxels):
            
            rows, cols = np.where(self.ids == idx)
            row,col = rows[0], cols[0]
            self.image[row,col,:] = [taxel.x, taxel.y, taxel.z]
    
    def get_image(self):
        return self.image
    
    def get_normalized_image(self):
        return self.image_normalized

    def normalize_image(self, eps=1e-12):
        img = self.image.astype(np.float32)
        mn, mx = np.min(img), np.max(img)
        n =(img - mn) / (mx - mn + eps)   # -> [0, 1]
        self.image_normalized = n
 

class XelaSimpleClient(Node):
    def __init__(self):
        super().__init__("LeapXelaImagePublisher")

        #State 
        self.leap_image = LeapImage()
        #ROS
        self.cli = self.create_client(XelaSensorStream, "xServStream")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("service xServStream not available, waiting...")

        # Sub
        self.sub = self.create_subscription(SensStream, "/xServTopic", self.on_xela_sensor_stream, 10)
        # Pub
        self.pub = self.create_publisher(Image, "/leap_image", 10)
        self.pub_normalized = self.create_publisher(Image, "/leap_image_normalized", 10)


    def make_request(self, sensor_id: int = 0):
        req = XelaSensorStream.Request()
        # sensor == 0 means "all sensors" per server implementation
        req.sensor = sensor_id

        future = self.cli.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            return future.result()
        else:
            raise RuntimeError(f"Service call failed: {future.exception()}")
    
    def on_xela_sensor_stream(self, msg: SensStream):
        self.leap_image.fill_image(msg)
        self.leap_image.normalize_image()


        timestamp = self.get_clock().now().to_msg()
        # Pumblish Image
        out = Image()
        out.header.stamp = timestamp
        out.header.frame_id = "leap_image"

        img = self.leap_image.get_image()  # (26, 31, 3) int32
        out.height = int(img.shape[0])
        out.width = int(img.shape[1])
        out.encoding = "32FC3"
        out.is_bigendian = False
        out.step = int(out.width * 3 * 4)  # 3 channels * 4 bytes/float32
        out.data = img.tobytes()
        self.pub.publish(out)

        # Publish Normalized Image
        out = Image()
        out.header.stamp = timestamp
        out.header.frame_id = "leap_image"

        img = self.leap_image.get_normalized_image()  # (26, 31, 3) float32
        out.height = int(img.shape[0])
        out.width = int(img.shape[1])
        out.encoding = "32FC3"
        out.is_bigendian = False
        out.step = int(out.width * 3 * 4)  # 3 channels * 4 bytes/float32
        out.data = img.tobytes()
        self.pub_normalized.publish(out)
  
def main(args=None):
    rclpy.init(args=args)

    node = XelaSimpleClient()
    try:
        # Simple example: request all sensors (sensor=0) and print the result
        response = node.make_request(sensor_id=1)
        node.get_logger().info(f"Got {len(response.data)} sensor readings from xServStream")
        print(response)
        # Keep the node alive to receive subscription callbacks until Ctrl+C
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()


