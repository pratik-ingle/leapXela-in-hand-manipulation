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
                "urdf_path",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("xela_description"), "palm.urdf"]
                ),
                description="URDF path override (set to empty to use packaged palm.urdf)",
            ),
            DeclareLaunchArgument(
                "use_gui",
                default_value="true",
                description="Use PyBullet GUI",
            ),
            Node(
                package="xela_description",
                executable="visulize_palm",
                name="visulize_palm_pybullet",
                output="screen",
                parameters=[
                    {
                        "urdf_path": LaunchConfiguration("urdf_path"),
                        "use_gui": LaunchConfiguration("use_gui"),
                    }
                ],
            ),
        ]
    )

