import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='leap_hand',
            executable='keyboard_node.py',
            name='keyboard_node',
            emulate_tty=True,
            output='screen'
        )
    ])
