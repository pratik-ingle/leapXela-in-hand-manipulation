#!/usr/bin/env python3

import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
from threading import RLock

from leap_hand_utils.dynamixel_client import DynamixelClient
import leap_hand_utils.leap_hand_utils as lhu
from leap_hand.srv import LeapPosition, LeapVelocity, LeapEffort, LeapState
from base import LeapXelaBase


class LeapXELANode(Node):
    def __init__(self):
        super().__init__('leaphand_node')

        # Guards all reads/writes to the hand hardware so they never overlap.
        self._hw_mutex = RLock()

        # Creates services that can give information about the hand out
        self.create_service(LeapPosition, 'leap_position', self.pos_srv)
        self.create_service(LeapVelocity, 'leap_velocity', self.vel_srv)
        self.create_service(LeapEffort, 'leap_effort', self.eff_srv)
        self.create_service(LeapState, 'leap_state', self.state_srv)

        self._leapXela = LeapXelaBase()
        self.create_subscription(JointState, 'cmd_xela', self._receive_pose, 10)

        self.pub = self.create_publisher(JointState, 'leap_state', 10)
        self.timer = self.create_timer(0.1, self.publish_state)

    def publish_state(self):
        with self._hw_mutex:
            pos, vel, cur = self._leapXela.dxl_client.read_pos_vel_cur()
            msg = JointState()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'joint8', 
                        'joint9', 'joint10', 'joint11', 'joint12', 'joint13', 'joint14', 'joint15', 'joint16']
            msg.position = pos.tolist()
            msg.velocity = vel.tolist()
            msg.effort = cur.tolist()
            self.pub.publish(msg)

    # Receive LEAP pose and directly control the robot
    def _receive_pose(self, msg):
        pose = msg.position
        self.curr_pos = np.array(pose)
        
        with self._hw_mutex:
            self._leapXela.set_joints_degrees(self.curr_pos)

    # Service that reads and returns the pos of the robot in regular LEAP Embodiment scaling.
    def pos_srv(self, request, response):
        with self._hw_mutex:
            response.position = self._leapXela.dxl_client.read_pos().tolist()
        return response

    # Service that reads and returns the vel of the robot in LEAP Embodiment
    def vel_srv(self, request, response):
        with self._hw_mutex:
            response.velocity = self._leapXela.dxl_client.read_vel().tolist()
        return response

    # Service that reads and returns the effort/current of the robot in LEAP Embodiment
    def eff_srv(self, request, response):
        with self._hw_mutex:
            response.effort = self._leapXela.dxl_client.read_cur().tolist()
        return response

    def state_srv(self, request, response):
        with self._hw_mutex:
            pos, vel, cur = self._leapXela.dxl_client.read_pos_vel_cur()

        response.position = pos.tolist()
        response.velocity = vel.tolist()
        response.effort = cur.tolist()
        return response


    def safe_disconnect(self):
        self._leapXela.safe_disconnect()

    def destroy_node(self):
        self.safe_disconnect()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    leaphand_node = LeapXELANode()
    try:
        rclpy.spin(leaphand_node)
    finally:
        leaphand_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
