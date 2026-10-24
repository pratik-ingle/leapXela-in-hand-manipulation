"""Sparsh-compatible FK packing for LeapXELA taxel features."""

from dataclasses import dataclass
from pathlib import Path

import einops
import numpy as np
import pytorch_kinematics as pk
import torch

from leapxela.paths import HAND_WORKSPACE, MJCF_DIR
from leapxela.taxel_layout import DATA_COLLECTION_RELDIR


N_TAXELS = 368
HAND_SS_URDF = MJCF_DIR / "hand_ss.urdf"
TAXEL_MAP_JSON = HAND_WORKSPACE / DATA_COLLECTION_RELDIR / "leap_sensor_taxel_map.json"

XELA_FLATTEN_ORDER = {
    "3aftc_palm_link": 30,
    "link_15_4x4_palm_link": 16,
    "link_14_4x4_palm_link": 16,
    "0aftc_palm_link": 30,
    "link_2_4x4_palm_link": 16,
    "link_1A_4x4_palm_link": 16,
    "1B_4x4_palm_link": 16,
    "1aftc_palm_link": 30,
    "link_6_4x4_palm_link": 16,
    "link_5A_4x4_palm_link": 16,
    "5B_4x4_palm_link": 16,
    "2aftc_palm_link": 30,
    "link_10_4x4_palm_link": 16,
    "link_9A_4x4_palm_link": 16,
    "9B_4x4_palm_link": 16,
    "ahr_palm_2_4x6_palm_link": 24,
    "ahr_palm_1_4x6_palm_link": 24,
    "ahr_palm_3_4x6_palm_link": 24,
}

_PATCH_TO_TAXEL_MAP = {
    "3aftc_palm_link": ("TH", "tip", True, False),
    "link_15_4x4_palm_link": ("TH", "second", False, False),
    "link_14_4x4_palm_link": ("TH", "third", False, False),
    "0aftc_palm_link": ("IF", "tip", True, False),
    "link_2_4x4_palm_link": ("IF", "second", False, False),
    "link_1A_4x4_palm_link": ("IF", "third", False, False),
    "1B_4x4_palm_link": ("IF", "fourth", False, False),
    "1aftc_palm_link": ("MF", "tip", True, False),
    "link_6_4x4_palm_link": ("MF", "second", False, False),
    "link_5A_4x4_palm_link": ("MF", "third", False, False),
    "5B_4x4_palm_link": ("MF", "fourth", False, False),
    "2aftc_palm_link": ("RF", "tip", True, False),
    "link_10_4x4_palm_link": ("RF", "second", False, False),
    "link_9A_4x4_palm_link": ("RF", "third", False, False),
    "9B_4x4_palm_link": ("RF", "fourth", False, False),
    "ahr_palm_2_4x6_palm_link": ("Palm", "up_right", False, True),
    "ahr_palm_1_4x6_palm_link": ("Palm", "up_left", False, True),
    "ahr_palm_3_4x6_palm_link": ("Palm", "down_left", False, True),
}

FK_FLIP_IN_PLANE_LINKS = frozenset({"ahr_palm_2_4x6_palm_link"})
FK_FLIP_Y_LINKS = frozenset(name for name in XELA_FLATTEN_ORDER if "4x4" in name)
LEAP_JOINT_ORDER = [
    "if_mcp", "if_rot", "if_pip", "if_dip",
    "mf_mcp", "mf_rot", "mf_pip", "mf_dip",
    "rf_mcp", "rf_rot", "rf_pip", "rf_dip",
    "th_cmc", "th_axl", "th_mcp", "th_ipl",
]

_MUJOCO_PALM_R = np.array(
    [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, -1.0, 0.0]],
    dtype=np.float64,
)
_MUJOCO_PALM_T = np.array([0.0, 0.0, 0.1], dtype=np.float64)
_KINEMATIC_CHAIN = None
_CACHED_URDF_PATH: Path | None = None
_TAXEL_IDS_IN_FK_ORDER: np.ndarray | None = None


@dataclass(frozen=True)
class FkTaxelResult:
    positions: np.ndarray
    rotations: np.ndarray
    forces_local: np.ndarray | None
    forces_world: np.ndarray | None
    positions_deformed: np.ndarray | None


def _load_json(path: Path) -> dict:
    import json

    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def get_sensor_grid(patch_name: str) -> tuple[np.ndarray, np.ndarray, float]:
    if "aftc" in patch_name:
        h, w = 0.031, 0.039
        h_res, w_res = 6, 6
        x = np.linspace(0.5 - h_res / 2, h_res / 2 + 0.5, h_res, endpoint=False) * h / h_res
        y = np.linspace(0.5, w_res + 0.5, w_res, endpoint=False) * w / w_res
        xx_, yy_ = np.meshgrid(x, y)
        xx = np.concatenate([xx_[:4, :].flatten(), xx_[-2, 1:-1], xx_[-1, 2:-2]], axis=0)
        yy = np.concatenate([yy_[:4, :].flatten(), yy_[-2, 1:-1], yy_[-1, 2:-2]], axis=0)
        return xx, yy, 0.029
    if "4x4" in patch_name:
        h, w = 0.026, 0.024
        h_res, w_res = 4, 4
        x = np.linspace(0.5, h_res + 0.5, h_res, endpoint=False) * h / h_res
        y = np.linspace(0.5, w_res + 0.5, w_res, endpoint=False) * w / w_res
        xx, yy = np.meshgrid(x, y)
        return xx, yy, 0.0044
    if "4x6" in patch_name:
        x = 0.00435 + np.arange(6) * 0.00725
        y = 0.00425 + np.arange(4) * 0.00717
        xx, yy = np.meshgrid(x, y)
        return xx, yy, 0.0
    raise ValueError(f"Unknown patch name: {patch_name}")


def _tip_ids_in_fk_grid_order(ids: list[int]) -> list[int]:
    grid = np.full((6, 6), -1, dtype=np.int32)
    grid[0, 2:6] = ids[0:4]
    grid[1, 1:6] = ids[4:9]
    grid[2, 0:6] = ids[9:15]
    grid[3, 0:6] = ids[15:21]
    grid[4, 1:6] = ids[21:26]
    grid[5, 2:6] = ids[26:30]
    out = np.full((6, 6), -1, dtype=np.int32)
    for row in range(6):
        for column in range(6):
            out[row, column] = grid[5 - column, 5 - row]
    return out[:4, :].reshape(-1).tolist() + out[4, 1:5].tolist() + out[5, 2:4].tolist()


def _palm_ids_in_fk_grid_order(ids: list[int], patch: str) -> list[int]:
    hw = np.asarray(ids, dtype=np.int32).reshape(6, 4)
    if patch == "up_right":
        return hw.T.reshape(-1).tolist()
    return np.flipud(np.rot90(hw, -1)).reshape(-1).tolist()


def _flatten_patch_taxel_ids(
    map_dict: dict, finger: str, patch: str, is_tip: bool, is_palm: bool
) -> list[int]:
    patch_dict = map_dict["Palm"][patch] if is_palm else map_dict[finger][patch]
    row_keys = sorted(patch_dict.keys(), key=lambda key: int(key))
    ids: list[int] = []
    for key in row_keys:
        ids.extend(int(value) for value in patch_dict[key])
    if is_tip:
        return _tip_ids_in_fk_grid_order(ids)
    if is_palm:
        return _palm_ids_in_fk_grid_order(ids, patch)
    return ids


def build_taxel_ids_in_fk_order(map_path: Path) -> np.ndarray:
    map_dict = _load_json(map_path)
    taxel_ids: list[int] = []
    for link_name, count in XELA_FLATTEN_ORDER.items():
        finger, patch, is_tip, is_palm = _PATCH_TO_TAXEL_MAP[link_name]
        ids = _flatten_patch_taxel_ids(map_dict, finger, patch, is_tip, is_palm)
        if len(ids) != count:
            raise ValueError(f"{link_name}: expected {count} ids, got {len(ids)}")
        taxel_ids.extend(ids)
    out = np.asarray(taxel_ids, dtype=np.int32)
    if out.shape[0] != N_TAXELS:
        raise ValueError(f"Expected {N_TAXELS} taxel ids, got {out.shape[0]}")
    if not np.array_equal(np.sort(out), np.arange(N_TAXELS)):
        raise ValueError("FK taxel ids do not cover 0..367 exactly once")
    return out


def taxel_ids_in_fk_order(map_path: Path) -> np.ndarray:
    global _TAXEL_IDS_IN_FK_ORDER
    if _TAXEL_IDS_IN_FK_ORDER is None:
        _TAXEL_IDS_IN_FK_ORDER = build_taxel_ids_in_fk_order(map_path)
    return _TAXEL_IDS_IN_FK_ORDER


def fk_order_to_taxel_id(map_path: Path) -> np.ndarray:
    return taxel_ids_in_fk_order(map_path).copy()


def forces_by_taxel_id_to_fk_order(forces_by_id: np.ndarray, map_path: Path) -> np.ndarray:
    forces_by_id = np.asarray(forces_by_id, dtype=np.float64)
    if forces_by_id.shape != (N_TAXELS, 3):
        raise ValueError(f"Expected ({N_TAXELS}, 3), got {forces_by_id.shape}")
    return forces_by_id[taxel_ids_in_fk_order(map_path)]


def _get_kinematic_chain(urdf_path: Path):
    global _KINEMATIC_CHAIN, _CACHED_URDF_PATH
    resolved = Path(urdf_path).resolve()
    if _KINEMATIC_CHAIN is None or _CACHED_URDF_PATH != resolved:
        _KINEMATIC_CHAIN = pk.build_chain_from_urdf(resolved.read_text().lstrip())
        _CACHED_URDF_PATH = resolved
    return _KINEMATIC_CHAIN


def urdf_base_to_mujoco_world(
    positions: np.ndarray, rotations: np.ndarray | None
) -> np.ndarray | tuple[np.ndarray, np.ndarray]:
    positions = np.asarray(positions, dtype=np.float64)
    squeeze = positions.ndim == 2
    if squeeze:
        positions = positions[None, ...]
    pos_w = np.einsum("ij,tsj->tsi", _MUJOCO_PALM_R, positions) + _MUJOCO_PALM_T
    if rotations is None:
        return pos_w[0] if squeeze else pos_w
    rotations = np.asarray(rotations, dtype=np.float64)
    if rotations.ndim == 3:
        rotations = rotations[None, ...]
    rot_w = np.einsum("ij,tsjk->tsik", _MUJOCO_PALM_R, rotations)
    if squeeze:
        return pos_w[0], rot_w[0]
    return pos_w, rot_w


def get_fk_taxel_frames(
    joint_angles: np.ndarray, urdf_path: Path, mujoco_world: bool
) -> tuple[np.ndarray, np.ndarray]:
    joint_angles = np.asarray(joint_angles, dtype=np.float32)
    if joint_angles.ndim == 1:
        joint_angles = joint_angles[None, :]
    if joint_angles.ndim != 2 or joint_angles.shape[-1] != 16:
        raise ValueError(f"Expected joint_angles (T,16) or (16,), got {joint_angles.shape}")
    chain = _get_kinematic_chain(urdf_path)
    joint_tensor = torch.tensor(joint_angles).float()
    joint_dict = {name: joint_tensor[:, index] for index, name in enumerate(LEAP_JOINT_ORDER)}
    joint_poses = chain.forward_kinematics(joint_dict)
    positions, rotations = [], []
    for link_name, count in XELA_FLATTEN_ORDER.items():
        joint_pose = joint_poses[link_name].get_matrix().numpy()
        xx, yy, d = get_sensor_grid(link_name)
        if link_name in FK_FLIP_IN_PLANE_LINKS:
            xx = xx.max() + xx.min() - xx
            yy = yy.max() + yy.min() - yy
        elif link_name in FK_FLIP_Y_LINKS:
            yy = yy.max() + yy.min() - yy
        sensor_local = np.stack([xx.flatten(), yy.flatten()], axis=-1)
        sensor_local = np.concatenate(
            [sensor_local, np.zeros_like(sensor_local)], axis=-1
        )
        sensor_local[..., -2] = d
        sensor_local[..., -1] = 1
        t = joint_pose.shape[0]
        pose_rep = einops.repeat(joint_pose, "t i j -> t s i j", s=count)
        pose_flat = einops.rearrange(pose_rep, "t s i j -> (t s) i j")
        local_flat = einops.repeat(sensor_local, "s c -> (t s) c", t=t)
        world_h = np.einsum("m i j, m j -> m i", pose_flat, local_flat)
        pose_flat[..., :, 3] = world_h
        pose_ts = einops.rearrange(pose_flat, "(t s) i j -> t s i j", s=count)
        positions.append(pose_ts[..., :3, 3])
        rotations.append(pose_ts[..., :3, :3])
    pos = np.concatenate(positions, axis=1)
    rot = np.concatenate(rotations, axis=1)
    if mujoco_world:
        pos, rot = urdf_base_to_mujoco_world(pos, rot)
    return pos, rot


def deform_taxel_positions(
    positions: np.ndarray,
    rotations: np.ndarray,
    forces_local: np.ndarray,
    deform_scale: float,
    max_disp: float,
) -> np.ndarray:
    squeeze = positions.ndim == 2
    if squeeze:
        positions = positions[None, ...]
        rotations = rotations[None, ...]
        forces_local = forces_local[None, ...]
    world_disp = np.einsum("tsij,tsj->tsi", rotations, forces_local) * deform_scale
    norms = np.linalg.norm(world_disp, axis=-1, keepdims=True)
    world_disp = np.where(
        norms > max_disp,
        world_disp * (max_disp / (norms + 1.0e-12)),
        world_disp,
    )
    deformed = positions + world_disp
    return deformed[0] if squeeze else deformed


def compute_fk_taxels(
    joint_angles: np.ndarray,
    forces_by_taxel_id: np.ndarray | None,
    urdf_path: Path,
    map_path: Path,
    deform_scale: float,
    max_disp: float,
    mujoco_world: bool,
) -> FkTaxelResult:
    joint_angles = np.asarray(joint_angles, dtype=np.float32)
    single = joint_angles.ndim == 1
    if single:
        joint_angles = joint_angles[None, :]
    positions, rotations = get_fk_taxel_frames(joint_angles, urdf_path, mujoco_world)
    pos = positions[0]
    rot = rotations[0]
    forces_local = None
    forces_world = None
    positions_deformed = None
    if forces_by_taxel_id is not None:
        forces_by_taxel_id = np.asarray(forces_by_taxel_id, dtype=np.float64)
        if forces_by_taxel_id.ndim == 2:
            forces_by_taxel_id = forces_by_taxel_id[None, ...]
        forces_fk = np.stack(
            [forces_by_taxel_id_to_fk_order(frame, map_path) for frame in forces_by_taxel_id],
            axis=0,
        )
        forces_local = forces_fk[0]
        forces_world = np.einsum("nij,nj->ni", rot, forces_local)
        positions_deformed = deform_taxel_positions(
            pos, rot, forces_local, deform_scale, max_disp
        )
    return FkTaxelResult(pos, rot, forces_local, forces_world, positions_deformed)
