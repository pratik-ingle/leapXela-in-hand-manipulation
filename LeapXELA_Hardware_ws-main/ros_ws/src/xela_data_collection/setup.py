import os

from setuptools import setup

package_name = "xela_data_collection"

setup(
    name=package_name,
    version="0.0.1",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            [
                "launch/xela_server_and_client.launch.py",
                "launch/xela_dataset_visulizer.launch.py",
            ],
        ),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Your Name",
    maintainer_email="you@example.com",
    description="Client node that calls the XelaSensorStream service.",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "xela_image_publisher = xela_data_collection.xela_image_publisher:main",
            "xela_taxel_visulizer = xela_data_collection.xela_taxel_visulizer:main",
            "xela_qt_taxel_visualizer = xela_data_collection.xela_qt_taxel_visualizer:main",
            "xela_data_collector = xela_data_collection.xela_data_collector:main",
            "xela_dataset_visulizer = xela_data_collection.xela_dataset_visulizer:main",
        ],
    },
)

