from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "xacro_path",
                default_value="xela_models/urdf/aftf.xacro",
                description="Absolute path, or 'pkg/path', or path relative to xela_models share.",
            ),
            DeclareLaunchArgument(
                "taxels",
                default_value="false",
                description="If true, pass taxel:=1 into the xacro so taxel links are included.",
            ),
            DeclareLaunchArgument("gui", default_value="true"),
            DeclareLaunchArgument("fixed_base", default_value="true"),
            DeclareLaunchArgument("use_realtime", default_value="false"),
            DeclareLaunchArgument("frame_length", default_value="0.04"),
            DeclareLaunchArgument("line_width", default_value="2.0"),
            DeclareLaunchArgument("update_hz", default_value="30.0"),
            Node(
                package="xela_pybullet_viewer",
                executable="pybullet_xacro_viewer",
                name="pybullet_xacro_viewer",
                output="screen",
                parameters=[
                    {
                        "xacro_path": LaunchConfiguration("xacro_path"),
                        "taxels": LaunchConfiguration("taxels"),
                        "gui": LaunchConfiguration("gui"),
                        "fixed_base": LaunchConfiguration("fixed_base"),
                        "use_realtime": LaunchConfiguration("use_realtime"),
                        "frame_length": LaunchConfiguration("frame_length"),
                        "line_width": LaunchConfiguration("line_width"),
                        "update_hz": LaunchConfiguration("update_hz"),
                    }
                ],
            ),
        ]
    )

