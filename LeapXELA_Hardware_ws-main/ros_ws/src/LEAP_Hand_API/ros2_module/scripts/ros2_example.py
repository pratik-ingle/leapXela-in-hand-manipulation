#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from leap_hand.srv import LeapPosition
import time
import numpy as np
import leap_hand_utils.leap_hand_utils as lhu

from base import load_pose
class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(LeapPosition, '/leap_position')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = LeapPosition.Request()
        self.pub_hand = self.create_publisher(JointState, '/cmd_xela', 10) 


        self.subscription = self.create_subscription(
            JointState,
            '/leap_state',
            self.listener_callback,
            10)

        initial_joint_degrees = load_pose('closed')
        self._cmd_msg = JointState()
        # JointState fields require a Python sequence of Python floats (numpy scalars fail ROS type checks).
        self._cmd_msg.position = [float(x) for x in initial_joint_degrees]
        self._cmd_timer = self.create_timer(0.1, self._publish_cmd)
        
    def listener_callback(self, msg):
        self.get_logger().info('Received leap state: %s' % msg)

    def _publish_cmd(self):
        self.pub_hand.publish(self._cmd_msg)

    def send_request(self):
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()



def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClientAsync()
    try:
        rclpy.spin(minimal_client)
    finally:
        minimal_client.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()