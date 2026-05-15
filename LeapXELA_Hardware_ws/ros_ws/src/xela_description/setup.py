from __future__ import annotations

import os
from pathlib import Path

from setuptools import find_packages, setup

package_name = 'xela_description'

here = Path(__file__).resolve().parent


def _data_files_under(rel_dir: str, install_subdir: str):
    """
    Collect all files under `rel_dir` into `share/<pkg>/<install_subdir>/...`.
    """
    src_root = here / rel_dir
    out = []
    if not src_root.exists():
        return out
    for root, _, files in os.walk(src_root):
        if not files:
            continue
        root_path = Path(root)
        rel = root_path.relative_to(src_root)
        install_dir = str(Path("share") / package_name / install_subdir / rel)
        # ament_python requires sources in data_files to be relative paths
        rel_sources = [str((root_path / f).relative_to(here)) for f in files]
        out.append((install_dir, rel_sources))
    return out


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['urdf/robot.urdf']),
        ('share/' + package_name, ['urdf/finger.urdf']),
        ('share/' + package_name, ['urdf/thumb.urdf']),
        ('share/' + package_name, ['urdf/palm.urdf']),
        ('share/' + package_name, ['urdf/hand.urdf']),
    ]
    + _data_files_under("launch", "launch")
    + _data_files_under("mjcf", "mjcf")
    + _data_files_under("urdf/assets", "assets"),
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
            'visulize = urdf.visulize_node:main',
            'visulize_finger = urdf.visulize_finger_node:main',
            'visulize_thumb = urdf.visulize_thumb_node:main',
            'visulize_palm = urdf.visulize_palm_node:main',
            'visulize_hand = urdf.visulize_hand_node:main',
            'visulize_mjcf = mjcf.visulize_mjcf:main',
        ],
    },
)

