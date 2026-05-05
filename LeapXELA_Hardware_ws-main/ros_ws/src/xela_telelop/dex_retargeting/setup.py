import os

from setuptools import find_packages, setup

package_name = 'dex_retargeting'
_setup_dir = os.path.dirname(os.path.abspath(__file__))


def _walk_data_files(source_relative: str, share_subdir: str):
    """Map files under source_relative (from setup.py) into share/<pkg>/<share_subdir>/."""
    pairs = []
    base = os.path.join(_setup_dir, source_relative)
    if not os.path.isdir(base):
        return pairs
    for dirpath, _, filenames in os.walk(base):
        rel = os.path.relpath(dirpath, base)
        if rel in (os.curdir, '.'):
            dest_dir = os.path.join('share', package_name, share_subdir)
        else:
            dest_dir = os.path.join('share', package_name, share_subdir, rel)
        files = [
            os.path.relpath(os.path.join(dirpath, fn), _setup_dir)
            for fn in filenames
        ]
        if files:
            pairs.append((dest_dir, files))
    return pairs


_data_files = [
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (
        os.path.join('share', package_name, 'launch'),
        [os.path.join('launch', 'hand_pose_teleop.launch.py')],
    ),
]
_data_files += _walk_data_files(os.path.join('dex_retargeting', 'configs'), 'configs')
_data_files += _walk_data_files('assets', 'assets')

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=_data_files,
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='mohammad200h@hotmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'hand_pose_publisher = dex_retargeting.hand_pose_publisher:main',
            'hand_viewer = dex_retargeting.hand_viewer:main',
            'leap_realsense = dex_retargeting.leap_realsense:main',
            'leap_xela_realsense = dex_retargeting.leap_xela_realsense:main',
        ],
    },
)
