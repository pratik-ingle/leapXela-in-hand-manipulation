#!/usr/bin/env python3

import json
import time

import rclpy
from rclpy.node import Node
from perlin_noise import PerlinNoise
import numpy as np
from ament_index_python.packages import get_package_share_directory

from xela_point_cloud_representation.msg import Sensor, Texel, HandSensors

def generate_perlin_noise(dim=(4, 6), seed=None):
    """
    Generate a 2D Perlin noise field with shape (height, width).

    The `perlin_noise` library expects coordinates (float or iterable of floats),
    so we sample a regular grid in [0, 1]x[0, 1].
    """
    height, width = dim
    if seed is None:
        seed = int(time.time_ns() % (2**32))
    noise = PerlinNoise(octaves=6, seed=seed)
    field = np.zeros((height, width), dtype=float)
    for y in range(height):
        for x in range(width):
            # Sample at cell centers to avoid "special" grid-aligned coordinates
            # that can collapse to exactly 0.0 for some octave/seed combinations.
            field[y, x] = noise([(x + 0.5) / width, (y + 0.5) / height])
    return field


def generate_sensor_msg_for_uspa46(sensor_joints, sensor_name):
    sensor_msg = Sensor()
    sensor_msg.name = sensor_name
    sensor_locations = sensor_joints[sensor_name]
    noise = generate_perlin_noise(dim=(4,6))*-1
    for y in range(4):
        for x in range(6):
            texel = Texel()
            texel.loc = str(x)+"_"+str(y)
            texel.x = 0.0
            texel.y = 0.0
            texel.z = float(noise[y, x])
            texel.joint_x = sensor_locations[str(x)+"_"+str(y)]["x"]
            texel.joint_y = sensor_locations[str(x)+"_"+str(y)]["y"]
            texel.joint_z = sensor_locations[str(x)+"_"+str(y)]["z"]
            sensor_msg.texels.append(texel)
    return sensor_msg

def generate_sensor_msg_for_uspa44(sensor_joints, sensor_name):
    sensor_msg = Sensor()
    sensor_msg.name = sensor_name
    sensor_locations = sensor_joints[sensor_name]
    noise = generate_perlin_noise(dim=(4,4))
    # rclpy.logging.get_logger("sensor_value_publisher_fake").info(f"noise: {noise}")
    for y in range(4):
        for x in range(4):
            texel = Texel()
            texel.loc = str(x)+"_"+str(y)
            texel.x = 0.0
            texel.y = 0.0
            texel.z = float(noise[y, x])
            # rclpy.logging.get_logger("sensor_value_publisher_fake").info(f"texel.z: {texel.z}")
            texel.joint_x = sensor_locations[str(x)+"_"+str(y)]["x"]
            texel.joint_y = sensor_locations[str(x)+"_"+str(y)]["y"]
            texel.joint_z = sensor_locations[str(x)+"_"+str(y)]["z"]
            sensor_msg.texels.append(texel)
    return sensor_msg

def generate_sensor_msg_for_fingertip_30(sensor_joints, sensor_name):
    sensor_msg = Sensor()
    sensor_msg.name = sensor_name
    sensor_locations = sensor_joints[sensor_name]
    noise = generate_perlin_noise(dim=(3,10))
    noise = noise.flatten()
    for idx in range(0,30):
        texel = Texel()
        texel.loc = str(idx+1)
        texel.x = 0.0
        texel.y = 0.0
        texel.z = float(noise[idx])
        texel.joint_x = sensor_locations[str(idx+1)]["x"]
        texel.joint_y = sensor_locations[str(idx+1)]["y"]
        texel.joint_z = sensor_locations[str(idx+1)]["z"]
        sensor_msg.texels.append(texel)
    return sensor_msg

class SensorValuePublisherFake(Node):
    def __init__(self) -> None:
        super().__init__("sensor_value_publisher_fake")
        self.declare_parameter("sensor_joints_path", "")
        self.sensor_joints = self.load_sensor_joints()

        self.publisher_ = self.create_publisher(HandSensors, "fake_sensor_values", 10)

        self.timer = self.create_timer(1.0, self.publish_sensor_values)

    def load_sensor_joints(self):
        sensor_joints_path = self.get_parameter("sensor_joints_path").get_parameter_value().string_value
        if not sensor_joints_path:
            sensor_joints_path = (
                get_package_share_directory("xela_description")
                + "/mjcf/sensor_joints.json"
            )

        with open(sensor_joints_path, "r") as f:
            return json.load(f)

    def publish_sensor_values(self):
        # sensor_msg = generate_sensor_msg_for_uspa44(self.sensor_joints, "if_bs_uspa44")
        hand_sensors_msg = HandSensors()
        hand_sensors_msg.if_bs_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "if_bs_uspa44")
        hand_sensors_msg.mf_bs_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "mf_bs_uspa44")
        hand_sensors_msg.rf_bs_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "rf_bs_uspa44")
        hand_sensors_msg.if_md_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "if_md_uspa44")
        hand_sensors_msg.mf_md_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "mf_md_uspa44")
        hand_sensors_msg.rf_md_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "rf_md_uspa44")
        hand_sensors_msg.if_px_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "if_px_uspa44")
        hand_sensors_msg.mf_px_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "mf_px_uspa44")
        hand_sensors_msg.rf_px_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "rf_px_uspa44")
        hand_sensors_msg.th_px_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "th_px_uspa44")
        hand_sensors_msg.th_ds_uspa44 = generate_sensor_msg_for_uspa44(self.sensor_joints, "th_ds_uspa44")
        hand_sensors_msg.uspa46_1 = generate_sensor_msg_for_uspa46(self.sensor_joints, "uspa46_1")
        hand_sensors_msg.uspa46_2 = generate_sensor_msg_for_uspa46(self.sensor_joints, "uspa46_2")
        hand_sensors_msg.uspa46_3 = generate_sensor_msg_for_uspa46(self.sensor_joints, "uspa46_3")
        hand_sensors_msg.if_ds = generate_sensor_msg_for_fingertip_30(self.sensor_joints, "if_ds")
        hand_sensors_msg.mf_ds = generate_sensor_msg_for_fingertip_30(self.sensor_joints, "mf_ds")
        hand_sensors_msg.rf_ds = generate_sensor_msg_for_fingertip_30(self.sensor_joints, "rf_ds")
        hand_sensors_msg.th_ds = generate_sensor_msg_for_fingertip_30(self.sensor_joints, "th_ds")
        self.publisher_.publish(hand_sensors_msg)
    
def main(args=None) -> None:
    rclpy.init(args=args)
    node = SensorValuePublisherFake()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
