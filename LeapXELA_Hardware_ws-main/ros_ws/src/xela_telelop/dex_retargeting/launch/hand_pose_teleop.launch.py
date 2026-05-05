from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    robot_name = LaunchConfiguration("robot_name")
    retargeting_type = LaunchConfiguration("retargeting_type")
    hand_type = LaunchConfiguration("hand_type")
    topic = LaunchConfiguration("topic")

    common_params = [
        {"robot_name": robot_name},
        {"retargeting_type": retargeting_type},
        {"hand_type": hand_type},
        {"topic": topic},
    ]

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "robot_name",
                default_value="leap_xela",
                description=(
                    "RobotName enum key, e.g. leap, leap_xela, allegro, shadow. "
                    "Note: leap_xela configs in this package are right-hand only."
                ),
            ),
            DeclareLaunchArgument(
                "retargeting_type",
                default_value="dexpilot",
                description="RetargetingType enum key: dexpilot, vector, position",
            ),
            DeclareLaunchArgument(
                "hand_type",
                default_value="right",
                description="HandType enum key: right or left (leap_xela supports right only in this package)",
            ),
            DeclareLaunchArgument(
                "topic",
                default_value="hand_pose",
                description="sensor_msgs/JointState topic for both nodes",
            ),
            Node(
                package="dex_retargeting",
                executable="hand_pose_publisher",
                name="hand_pose_publisher",
                parameters=common_params,
                output="screen",
            ),
            Node(
                package="dex_retargeting",
                executable="hand_viewer",
                name="hand_viewer",
                parameters=common_params,
                output="screen",
            ),
        ]
    )
