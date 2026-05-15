#!/usr/bin/env python3

import json
import time
from pathlib import Path

import rclpy
from rclpy.node import Node
from perlin_noise import PerlinNoise
import numpy as np
from ament_index_python.packages import get_package_share_directory

from xela_point_cloud_representation.msg import  Texel, HandSensors


from leap_taxel_map import (
    get_flatten_hand,
    get_sorted_1D_hand_taxels_map,
    LEAP_XELA_ID,
    sorted_1D_hand_taxel_name,
    taxel_location_map_for_image_representation,
)





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

def generate_perlin_noise_for_leap():
    #shape (26, 31)
    noise = generate_perlin_noise(dim=(26, 31))
    return noise

def perlin_noise_to_1D_texels_array(noise):
    texels_array = []
    texel_loc_map = taxel_location_map_for_image_representation(LEAP_XELA_ID)
    for taxel_id, loc in texel_loc_map.items():
        texel = noise[loc[0], loc[1]]
        texels_array.append(texel)
    return texels_array

def taxel_1d_sensor_names():
    map_path = Path(__file__).resolve().parent / "leap_sensor_taxel_map.json"
    with open(map_path, "r") as f:
        map_dict = json.load(f)

    hand_hw_flat, hand_sim_flat = get_flatten_hand(map_dict)
    map_ = get_sorted_1D_hand_taxels_map(hand_hw_flat, hand_sim_flat)
    sorted_sim = sorted_1D_hand_taxel_name(map_, hand_hw_flat)
    
    return sorted_sim


def generate_sensor_msg_for_leap():
    noise = generate_perlin_noise_for_leap()
    texels_array_1d = perlin_noise_to_1D_texels_array(noise)
    sensor_names_1d = taxel_1d_sensor_names()

    sensor_msg = HandSensors()
    idx = 0
    for sensor_name, texel_z in zip(sensor_names_1d, texels_array_1d):
        texel = Texel()
        texel.sensor_name = sensor_name
        print(f"Sensor name: {sensor_name}", "texel_z: ", texel_z)
        texel.z = texel_z
        texel.taxel_id = idx
        texel.joint_x = sensor_name+"_slide_x"
        texel.joint_y = sensor_name+"_slide_y"
        texel.joint_z = sensor_name+"_slide_z"
        sensor_msg.texels.append(texel)
        idx += 1
    
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
        hand_sensors_msg = generate_sensor_msg_for_leap()

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
