from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription([
        Node(
            package='xela_point_cloud_representation',
            executable='hand_touch_point_cloud.py',
            name='hand_touch_point_cloud',
            output='screen',
        ),
    ])
