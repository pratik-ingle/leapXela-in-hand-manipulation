from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    # Prefixed args avoid collisions with the included launches' `node_name`.
    hand_controller_node_name = LaunchConfiguration("hand_controller_node_name")
    perline_noise_publisher_node_name = LaunchConfiguration(
        "perline_noise_publisher_node_name"
    )
    pointcloud_processing_node_name = LaunchConfiguration(
        "pointcloud_processing_node_name"
    )
    pointcloud_processing_log_level = LaunchConfiguration(
        "pointcloud_processing_log_level"
    )

    sensor_joints_path = LaunchConfiguration("sensor_joints_path")
    robot_description_path = LaunchConfiguration("robot_description_path")

    xela_pcr_launch_dir = PathJoinSubstitution(
        [FindPackageShare("xela_point_cloud_representation"), "launch"]
    )

    default_sensor_joints_path = PathJoinSubstitution(
        [FindPackageShare("xela_description"), "mjcf", "sensor_joints.json"]
    )
    default_robot_description_path = PathJoinSubstitution(
        [FindPackageShare("xela_description"), "mjcf", "scene_touch_point_cloud.xml"]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "hand_controller_node_name",
                default_value="hand_controller",
                description="Node name for the hand controller.",
            ),
            DeclareLaunchArgument(
                "perline_noise_publisher_node_name",
                default_value="sensor_value_publisher_fake",
                description="Node name for the per-line noise publisher (fake sensor publisher).",
            ),
            DeclareLaunchArgument(
                "sensor_joints_path",
                default_value=default_sensor_joints_path,
                description="Path to `sensor_joints.json` (installed in xela_description).",
            ),
            DeclareLaunchArgument(
                "robot_description_path",
                default_value=default_robot_description_path,
                description="Path to the MuJoCo XML (MJCF) used by the pointcloud processing node.",
            ),
            DeclareLaunchArgument(
                "pointcloud_processing_node_name",
                default_value="process_hand_sensors_into_pointcloud",
                description="Node name for the pointcloud processing node.",
            ),
            DeclareLaunchArgument(
                "pointcloud_processing_log_level",
                default_value="info",
                description="Log level for the pointcloud processing node (debug, info, warn, error, fatal).",
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([xela_pcr_launch_dir, "launch_hand_controller.py"])
                ),
                launch_arguments={
                    "node_name": hand_controller_node_name,
                }.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [xela_pcr_launch_dir, "launch_perline_noise_publisher.py"]
                    )
                ),
                launch_arguments={
                    "node_name": perline_noise_publisher_node_name,
                    "sensor_joints_path": sensor_joints_path,
                }.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [xela_pcr_launch_dir, "launch_pointcloud_proccessing.py"]
                    )
                ),
                launch_arguments={
                    "node_name": pointcloud_processing_node_name,
                    "robot_description_path": robot_description_path,
                    "log_level": pointcloud_processing_log_level,
                }.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution(
                        [xela_pcr_launch_dir, "launch_hand_touch_point_cloud.py"]
                    )
                ),
            ),
        ]
    )
