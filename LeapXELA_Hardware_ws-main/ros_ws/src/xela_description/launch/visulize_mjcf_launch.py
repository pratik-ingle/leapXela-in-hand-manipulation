from __future__ import annotations

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "scene_path",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("xela_description"), "mjcf", "scene.xml"]
                ),
                description="MJCF scene XML path override",
            ),
            Node(
                package="xela_description",
                executable="visulize_mjcf",
                name="visulize_mjcf",
                output="screen",
                parameters=[{"scene_path": LaunchConfiguration("scene_path")}],
            ),
        ]
    )

