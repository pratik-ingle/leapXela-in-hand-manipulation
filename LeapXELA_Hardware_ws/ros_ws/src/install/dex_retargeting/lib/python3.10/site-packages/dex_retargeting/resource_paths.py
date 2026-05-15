"""Resolve configs and robot assets for both install/share and source trees."""
from pathlib import Path
from typing import Optional


def _package_share_dir() -> Optional[Path]:
    try:
        from ament_index_python.packages import get_package_share_directory

        return Path(get_package_share_directory("dex_retargeting"))
    except Exception:
        return None


def _source_package_root() -> Path:
    """Parent of the inner `dex_retargeting` Python package (ROS package root)."""
    return Path(__file__).resolve().parent.parent


def get_robot_hand_urdf_dir() -> Path:
    """Directory passed to RetargetingConfig.set_default_urdf_dir (hand URDFs)."""
    share = _package_share_dir()
    if share is not None:
        p = share / "assets" / "robots" / "hands"
        if p.is_dir():
            return p
    p2 = _source_package_root() / "assets" / "robots" / "hands"
    if p2.is_dir():
        return p2
    raise FileNotFoundError(
        "dex_retargeting hand URDF assets not found. "
        "Rebuild the package so `assets` is installed under share/dex_retargeting."
    )


def get_configs_dir() -> Path:
    """Base `configs` directory (contains `teleop` and `offline`)."""
    share = _package_share_dir()
    if share is not None:
        p = share / "configs"
        if p.is_dir():
            return p
    p2 = _source_package_root() / "dex_retargeting" / "configs"
    if p2.is_dir():
        return p2
    raise FileNotFoundError(
        "dex_retargeting configs not found. "
        "Rebuild the package so `configs` is installed under share/dex_retargeting."
    )
