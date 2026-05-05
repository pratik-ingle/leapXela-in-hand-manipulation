from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource, PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Mirror the args from xela_server_ros2/launch/service.launch
    file_arg = DeclareLaunchArgument(
        "file",
        default_value="/etc/xela/xServ.ini",
        description="Path to xServ.ini for XELA server",
    )
    port_arg = DeclareLaunchArgument(
        "port",
        default_value="5000",
        description="TCP port for XELA server/service",
    )
    ip_arg = DeclareLaunchArgument(
        "ip",
        default_value="127.0.0.1",
        description="IP address for XELA server/service",
    )
    d_arg = DeclareLaunchArgument(
        "d",
        default_value="0",
        description="Debug flag for xela_service",
    )

    included_server = IncludeLaunchDescription(
        AnyLaunchDescriptionSource(
            PathJoinSubstitution(
                # xela_server_ros2 installs launch/ contents directly into share/xela_server_ros2/
                [FindPackageShare("xela_server_ros2"), "service.launch"]
            )
        ),
        launch_arguments={
            "file": LaunchConfiguration("file"),
            "port": LaunchConfiguration("port"),
            "ip": LaunchConfiguration("ip"),
            "d": LaunchConfiguration("d"),
        }.items(),
    )

    included_leap = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("leap_hand"), "launch", "launch_leap.py"]
            )
        )
    )

    client_node = Node(
        package="xela_data_collection",
        executable="xela_image_publisher",
        name="xela_simple_client",
        output="screen",
    )

    collector_node = Node(
        package="xela_data_collection",
        executable="xela_data_collector",
        name="xela_data_collector",
        output="screen",
    )

    return LaunchDescription(
        [
            file_arg,
            port_arg,
            ip_arg,
            d_arg,
            included_leap,
            included_server,
            client_node,
            collector_node,
        ]
    )

