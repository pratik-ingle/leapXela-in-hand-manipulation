"""Dump FK taxel frames for cross-implementation comparison.

Same two-env pattern as ``dump_sensor_trace.py``: ``--impl`` picks the library,
imports are lazy.  Each side is given *its own* default URDF and taxel-map paths,
which is how callers actually use it; the two asset files are separately asserted
byte-identical, so any difference here is code, not data.

Joint angles are fixed and seeded, never random at call time, so both envs drive
the identical poses.
"""

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPARSH_ROOT = REPO_ROOT / "sparsh-skin-sim"
N_TAXELS = 368


def joint_angle_set(seed: int, n_random: int) -> np.ndarray:
    """Zeros, a mid-flex pose, then seeded-random poses."""
    rng = np.random.default_rng(seed)
    poses = [
        np.zeros(16, dtype=np.float32),
        np.full(16, 0.4, dtype=np.float32),
        np.linspace(-0.3, 1.2, 16, dtype=np.float32),
    ]
    poses.extend(
        rng.uniform(-0.5, 1.5, size=16).astype(np.float32) for _ in range(n_random)
    )
    return np.stack(poses)


def taxel_forces(seed: int, count: int) -> np.ndarray:
    """Deterministic per-taxel force field, one per pose."""
    rng = np.random.default_rng(seed + 977)
    return rng.normal(scale=0.2, size=(count, N_TAXELS, 3)).astype(np.float64)


class _LeapxelaImpl:
    name = "leapxela"

    def __init__(self):
        from leapxela import fk_taxel

        self._mod = fk_taxel
        self.urdf_path = fk_taxel.HAND_SS_URDF
        self.map_path = fk_taxel.TAXEL_MAP_JSON

    def fk_order(self):
        return self._mod.build_taxel_ids_in_fk_order(self.map_path)

    def compute(self, angles, forces, deform_scale, max_disp, mujoco_world):
        return self._mod.compute_fk_taxels(
            angles,
            forces,
            self.urdf_path,
            self.map_path,
            deform_scale,
            max_disp,
            mujoco_world,
        )


class _SparshImpl:
    name = "sparsh"

    def __init__(self, sparsh_root: Path):
        sys.path.insert(0, str(sparsh_root))
        from util import fk_taxel_util

        self._mod = fk_taxel_util
        self.urdf_path = fk_taxel_util._DEFAULT_URDF_PATH
        self.map_path = fk_taxel_util._DEFAULT_TAXEL_MAP_PATH

    def fk_order(self):
        return self._mod.build_taxel_ids_in_fk_order(self.map_path)

    def compute(self, angles, forces, deform_scale, max_disp, mujoco_world):
        return self._mod.compute_fk_taxels(
            angles,
            forces,
            urdf_path=self.urdf_path,
            deform_scale=deform_scale,
            max_disp=max_disp,
            mujoco_world=mujoco_world,
        )


def load_impl(impl: str, sparsh_root: Path):
    if impl == "leapxela":
        return _LeapxelaImpl()
    if impl == "sparsh":
        return _SparshImpl(sparsh_root)
    raise ValueError(f"Unknown impl '{impl}'")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--impl", choices=("leapxela", "sparsh"), required=True)
    parser.add_argument("--sparsh-root", type=Path, default=DEFAULT_SPARSH_ROOT)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--n-random", type=int, default=5)
    parser.add_argument("--deform-scale", type=float, default=0.02)
    parser.add_argument("--max-disp", type=float, default=0.015)
    parser.add_argument("--no-mujoco-world", dest="mujoco_world", action="store_false")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    impl = load_impl(args.impl, args.sparsh_root)

    poses = joint_angle_set(args.seed, args.n_random)
    forces = taxel_forces(args.seed, len(poses))

    arrays = {
        "joint_angles": poses,
        "forces_by_taxel_id": forces,
        "fk_order": np.asarray(impl.fk_order(), dtype=np.int64),
    }

    # Batched (T,16) input raises NotImplementedError upstream, so drive
    # single-frame on both sides.
    fields = ("positions", "rotations", "forces_local", "forces_world", "positions_deformed")
    collected = {field: [] for field in fields}
    for index in range(len(poses)):
        result = impl.compute(
            poses[index],
            forces[index],
            args.deform_scale,
            args.max_disp,
            args.mujoco_world,
        )
        for field in fields:
            collected[field].append(np.asarray(getattr(result, field), dtype=np.float64))
    for field in fields:
        arrays[field] = np.stack(collected[field])

    meta = {
        "impl": impl.name,
        "urdf_path": str(impl.urdf_path),
        "urdf_sha256": hashlib.sha256(Path(impl.urdf_path).read_bytes()).hexdigest(),
        "map_path": str(impl.map_path),
        "map_sha256": hashlib.sha256(Path(impl.map_path).read_bytes()).hexdigest(),
        "n_poses": int(len(poses)),
        "deform_scale": args.deform_scale,
        "max_disp": args.max_disp,
        "mujoco_world": args.mujoco_world,
        "timestep": 0.0,
        "integrator": -1,
        "numpy": np.__version__,
        "python": platform.python_version(),
    }
    try:
        import torch

        meta["torch"] = torch.__version__
    except ImportError:
        meta["torch"] = "n/a"
    try:
        import mujoco as mj

        meta["mujoco"] = mj.__version__
    except ImportError:
        meta["mujoco"] = "n/a"
    meta["model_path"] = str(impl.urdf_path)
    arrays["metadata_json"] = json.dumps(meta, indent=2)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.out, **arrays)
    print(f"[{impl.name}] wrote {args.out}")
    print(f"  urdf  {impl.urdf_path}")
    print(f"        sha256 {meta['urdf_sha256'][:16]}")
    print(f"  map   {impl.map_path}")
    print(f"        sha256 {meta['map_sha256'][:16]}")
    print(f"  poses {len(poses)}  positions {arrays['positions'].shape}")
    print(f"  torch {meta['torch']}  numpy {np.__version__}  py {platform.python_version()}")


if __name__ == "__main__":
    main()
