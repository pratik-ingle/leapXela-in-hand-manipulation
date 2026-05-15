from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Gradio binds to 127.0.0.1:7860 by default. You can override these via
    # GRADIO_SERVER_NAME / GRADIO_SERVER_PORT environment variables if needed.
    #
    # This launch file simply starts the visualizer executable; the UI itself
    # lets you choose the HDF5 path and stream.
    name_arg = DeclareLaunchArgument(
        "node_name",
        default_value="xela_dataset_visulizer",
        description="ROS node name for the dataset visualizer process",
    )

    vis = Node(
        package="xela_data_collection",
        executable="xela_dataset_visulizer",
        name=LaunchConfiguration("node_name"),
        output="screen",
    )

    return LaunchDescription([name_arg, vis])

