"""Calibrate pure Sparsh/Kelvin-Voigt QA thresholds for LeapXELA collection."""

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import mujoco as mj
import numpy as np

from leapxela.episode import (
    PREGRIP_FRACTION,
    build_model,
    control_targets,
    profile_from_args,
)
from leapxela.flex_force import (
    DEFAULT_FLEX_DAMPING,
    DEFAULT_FLEX_STIFFNESS,
    DEFAULT_FORCE_WINDOW,
    DEFAULT_VELOCITY_SMOOTHING,
)
from leapxela.hand_builder import MODEL_VARIANT, TAXEL_COUNT
from leapxela.paths import data_dir
from leapxela.sensors import (
    MODEL_SCHEMA_VERSION,
    SparshSensorConfig,
    build_sparsh_readers,
    read_sparsh,
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def calibration_args(args: argparse.Namespace) -> SimpleNamespace:
    return SimpleNamespace(
        grip_fraction=args.grip_fraction,
        thumb_grip_fraction=args.thumb_grip_fraction,
        # profile_from_args reads this too; the noise floor should be measured in
        # the same pre-curled pose collection runs start from.
        pregrip_fraction=args.pregrip_fraction,
        thumb_delay=args.thumb_delay,
        pulse_hz=1.0,
        pulse_amplitude=0.15,
        shear_amplitude=0.15,
        squeeze_steps=4,
    )


def collect_noise_floor(args: argparse.Namespace) -> dict:
    model, skins, tips = build_model([], args.palm_pitch, 0.0, 0.0)
    data = mj.MjData(model)
    profile = profile_from_args("hold", calibration_args(args))
    config = SparshSensorConfig(
        args.stiffness,
        args.damping,
        args.window,
        args.use_qvel,
        args.velocity_smoothing,
        0.0,
        0.0,
        0.0,
        None,
        None,
    )
    readers = build_sparsh_readers(model, skins, tips, config)
    timestep = float(model.opt.timestep)
    sample_every = max(1, round(1.0 / (args.sample_hz * timestep)))
    total_steps = int(np.ceil(args.duration / timestep))
    normals = []
    totals = []
    for step in range(total_steps):
        t = (step + 1) * timestep
        data.ctrl[:] = control_targets(model, t, profile)
        mj.mj_step(model, data)
        if step % sample_every != 0:
            continue
        readout = read_sparsh(model, data, readers, 0.0)
        normal = readout.flat[:, 2]
        normals.append(normal.copy())
        totals.append(float(np.sum(normal)))
    normal_array = np.asarray(normals, dtype=np.float64)
    total_array = np.asarray(totals, dtype=np.float64)
    per_taxel_noise = float(np.percentile(np.abs(normal_array), args.percentile))
    total_noise = float(np.percentile(np.abs(total_array), args.percentile))
    return {
        "samples": int(normal_array.shape[0]),
        "taxels": TAXEL_COUNT,
        "per_taxel_abs_percentile_n": per_taxel_noise,
        "total_abs_percentile_n": total_noise,
        "activity_threshold_n": max(args.min_activity_threshold, per_taxel_noise * args.margin),
        "min_peak_normal_n": max(args.min_peak_normal_floor, total_noise * args.margin),
        "min_contact_fraction": args.min_contact_fraction,
        "normal_mean_n": float(np.mean(normal_array)),
        "normal_std_n": float(np.std(normal_array)),
        "total_normal_mean_n": float(np.mean(total_array)),
        "total_normal_std_n": float(np.std(total_array)),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calibrate Sparsh/Kelvin-Voigt thresholds for LeapXELA."
    )
    parser.add_argument("--duration", type=float, default=2.0)
    parser.add_argument("--sample-hz", type=float, default=100.0)
    parser.add_argument("--palm-pitch", type=float, default=0.0)
    parser.add_argument("--grip-fraction", type=float, default=0.55)
    parser.add_argument("--thumb-grip-fraction", type=float, default=0.35)
    parser.add_argument("--pregrip-fraction", type=float, default=PREGRIP_FRACTION)
    parser.add_argument("--thumb-delay", type=float, default=0.5)
    parser.add_argument("--stiffness", type=float, default=DEFAULT_FLEX_STIFFNESS)
    parser.add_argument("--damping", type=float, default=DEFAULT_FLEX_DAMPING)
    parser.add_argument("--window", type=int, default=DEFAULT_FORCE_WINDOW)
    parser.add_argument("--use-qvel", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--velocity-smoothing", type=float, default=DEFAULT_VELOCITY_SMOOTHING,
    )
    parser.add_argument("--percentile", type=float, default=99.5)
    parser.add_argument("--margin", type=float, default=5.0)
    parser.add_argument("--min-activity-threshold", type=float, default=0.005)
    parser.add_argument("--min-peak-normal-floor", type=float, default=0.01)
    parser.add_argument("--min-contact-fraction", type=float, default=0.05)
    parser.add_argument(
        "--output", type=Path,
        default=data_dir() / "leapxela_generated" / "sparsh_sensor_calibration.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "schema_version": MODEL_SCHEMA_VERSION,
        "model_variant": MODEL_VARIANT,
        "mujoco_version": mj.__version__,
        "method": "no-object noise-floor threshold calibration",
        "args": {key: str(value) if isinstance(value, Path) else value
                 for key, value in vars(args).items()},
        "noise_floor": collect_noise_floor(args),
        "stiffness": args.stiffness,
        "damping": args.damping,
        "window": args.window,
        "use_qvel": args.use_qvel,
        "velocity_smoothing": args.velocity_smoothing,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    result["sha256"] = file_sha256(args.output)
    args.output.write_text(json.dumps(result, indent=2))
    print(f"wrote Sparsh sensor calibration: {args.output}")


if __name__ == "__main__":
    main()
