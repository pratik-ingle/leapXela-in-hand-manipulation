from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    node_name = LaunchConfiguration("node_name")
    sensor_joints_path = LaunchConfiguration("sensor_joints_path")

    default_sensor_joints_path = PathJoinSubstitution(
        [FindPackageShare("xela_description"), "mjcf", "sensor_joints.json"]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "node_name",
                default_value="sensor_value_publisher_fake",
                description="ROS node name.",
            ),
            DeclareLaunchArgument(
                "sensor_joints_path",
                default_value=default_sensor_joints_path,
                description="Path to `sensor_joints.json` (installed in xela_description).",
            ),
            Node(
                package="xela_point_cloud_representation",
                executable="sensor_value_publisher_fake.py",
                name=node_name,
                output="screen",
                parameters=[
                    {"sensor_joints_path": sensor_joints_path},
                ],
            ),
        ]
    )
