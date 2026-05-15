from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    model = LaunchConfiguration("model")
    gui = LaunchConfiguration("gui")
    rvizconfig = LaunchConfiguration("rvizconfig")

    urdf_file = PathJoinSubstitution(
        [FindPackageShare("xela_models"), "urdf", [model, ".urdf"]]
    )

    robot_description = ParameterValue(
        Command([FindExecutable(name="xacro"), " ", urdf_file]),
        value_type=str,
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument("model", default_value="4x4"),
            DeclareLaunchArgument("gui", default_value="true"),
            DeclareLaunchArgument(
                "rvizconfig",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("xela_models"), "rviz", "urdf.rviz"]
                ),
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                parameters=[{"robot_description": robot_description}],
                output="screen",
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher",
                condition=IfCondition(gui),
                output="screen",
            ),
            Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="joint_state_publisher",
                condition=UnlessCondition(gui),
                output="screen",
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                arguments=["-d", rvizconfig],
                output="screen",
            ),
        ]
    )

