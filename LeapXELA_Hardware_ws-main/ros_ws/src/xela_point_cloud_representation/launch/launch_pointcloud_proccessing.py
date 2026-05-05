from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    robot_description_path = LaunchConfiguration("robot_description_path")
    node_name = LaunchConfiguration("node_name")
    log_level = LaunchConfiguration("log_level")
    default_robot_description_path = PathJoinSubstitution(
        [FindPackageShare("xela_description"), "mjcf", "scene_touch_point_cloud.xml"]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "robot_description_path",
                default_value=default_robot_description_path,
                description=(
                    "Path to the MuJoCo XML (MJCF) used by the pointcloud processing node."
                ),
            ),
            DeclareLaunchArgument(
                "node_name",
                default_value="process_hand_sensors_into_pointcloud",
                description="ROS node name.",
            ),
            DeclareLaunchArgument(
                "log_level",
                default_value="info",
                description="ROS logging level for the pointcloud processing node (debug, info, warn, error, fatal).",
            ),
            Node(
                package="xela_point_cloud_representation",
                executable="process_hand_sensors_into_pointcloud",
                name=node_name,
                output="screen",
                arguments=["--ros-args", "--log-level", log_level],
                parameters=[
                    {"robot_description_path": robot_description_path},
                ],
            ),
        ]
    )
