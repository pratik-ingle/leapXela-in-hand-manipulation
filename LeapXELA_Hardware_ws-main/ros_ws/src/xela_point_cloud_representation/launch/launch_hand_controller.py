from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description() -> LaunchDescription:
    node_name = LaunchConfiguration("node_name")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "node_name",
                default_value="hand_controller",
                description="ROS node name.",
            ),
            Node(
                package="xela_point_cloud_representation",
                executable="hand_controller.py",
                name=node_name,
                output="screen",
            ),
        ]
    )

