"""Compile the leapxela hand and save it, plus a shared control trajectory, for cross-env runs.

Runs in the ``leapxela`` env only.  The ``.mjb`` is how the leapxela-generated model
reaches the ``sparsh-skin`` env: both envs run mujoco 3.11.0, so a binary model
round-trips exactly with assets baked in, and the sparsh env never needs the
leapxela package installed.

Everything that would otherwise differ between the two envs is baked in here:

* the pre-grip pose is applied and written into ``qpos0``, so both envs start from
  the identical pre-curled hand (this is what ``episode`` does: curl first, then place)
* the object rest pose is written into ``qpos0`` just above a palm pad
* the control trajectory is precomputed from ``episode.control_targets`` and saved
  as ``(T, 16)``, so the sparsh env replays identical actuation without importing
  leapxela or reimplementing the grasp policy
* per-patch taxel ids are emitted so the two packings can be cross-checked
  rather than assumed
"""

import argparse
import hashlib
import json
from pathlib import Path

import mujoco as mj
import numpy as np

from leapxela.episode import (
    GRASP_PATTERNS,
    PREGRIP_FRACTION,
    ObjectSpec,
    apply_pregrip,
    build_model,
    control_targets,
    object_body_name,
    object_geom_name,
    profile_from_args,
)
from leapxela.flex_force import flex_id


PALM_FLEX = "flex_uspa46_1"

INTEGRATORS = {
    "euler": mj.mjtIntegrator.mjINT_EULER,
    "rk4": mj.mjtIntegrator.mjINT_RK4,
    "implicit": mj.mjtIntegrator.mjINT_IMPLICIT,
    "implicitfast": mj.mjtIntegrator.mjINT_IMPLICITFAST,
}


def profile_for(pattern: str, args: argparse.Namespace):
    from types import SimpleNamespace

    return profile_from_args(
        pattern,
        SimpleNamespace(
            grip_fraction=args.grip_fraction,
            thumb_grip_fraction=args.thumb_grip_fraction,
            pregrip_fraction=args.pregrip_fraction,
            thumb_delay=args.thumb_delay,
            pulse_hz=1.0,
            pulse_amplitude=0.15,
            shear_amplitude=0.15,
            squeeze_steps=4,
        ),
    )


def bake_initial_state(model: mj.MjModel, pregrip_fraction: float, has_object: bool,
                       clearance: float) -> dict:
    """Write the pre-curled hand and the object rest pose into qpos0.

    Baking into qpos0 rather than into an MjData is what makes the state travel
    with the .mjb: every MjData built from this model, in either env, starts here.
    """
    data = mj.MjData(model)
    apply_pregrip(model, data, pregrip_fraction)
    model.qpos0[:] = data.qpos

    info = {"pregrip_fraction": pregrip_fraction}
    if not has_object:
        return info

    mj.mj_forward(model, data)
    fid = flex_id(model, PALM_FLEX)
    vert_adr = int(model.flex_vertadr[fid])
    vert_num = int(model.flex_vertnum[fid])
    centre = data.flexvert_xpos[vert_adr : vert_adr + vert_num].mean(axis=0)

    body_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(0))
    qpos_adr = int(model.jnt_qposadr[int(model.body_jntadr[body_id])])
    pose = np.array(
        [centre[0], centre[1], centre[2] + clearance, 1.0, 0.0, 0.0, 0.0],
        dtype=np.float64,
    )
    model.qpos0[qpos_adr : qpos_adr + 7] = pose
    info["object_pose"] = pose.tolist()
    info["object_qpos_adr"] = qpos_adr
    return info


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--object", choices=("none", "box", "sphere", "cylinder"), default="box")
    parser.add_argument("--object-scale", type=float, default=1.0)
    parser.add_argument("--object-mass", type=float, default=0.3)
    parser.add_argument("--clearance", type=float, default=0.035)
    parser.add_argument("--pattern", choices=GRASP_PATTERNS, default="squeeze")
    parser.add_argument("--duration", type=float, default=2.5)
    parser.add_argument("--dt", type=float, default=0.001)
    parser.add_argument("--integrator", choices=tuple(INTEGRATORS), default="euler")
    parser.add_argument("--grip-fraction", type=float, default=0.55)
    parser.add_argument("--thumb-grip-fraction", type=float, default=0.35)
    parser.add_argument("--pregrip-fraction", type=float, default=PREGRIP_FRACTION)
    parser.add_argument("--thumb-delay", type=float, default=0.5)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    specs = (
        []
        if args.object == "none"
        else [ObjectSpec(args.object, args.object_scale, args.object_mass)]
    )
    model, skins, tips = build_model(specs, 0.0, 0.0, 0.0)

    model.opt.timestep = args.dt
    model.opt.integrator = INTEGRATORS[args.integrator]
    state = bake_initial_state(model, args.pregrip_fraction, bool(specs), args.clearance)

    profile = profile_for(args.pattern, args)
    steps = max(2, int(round(args.duration / args.dt)))
    ctrl = np.stack(
        [control_targets(model, (step + 1) * args.dt, profile) for step in range(steps)]
    ).astype(np.float64)

    taxel_ids = {}
    for skin in skins:
        taxel_ids[skin.flex_name] = np.asarray(skin.taxel_ids).ravel().tolist()
    for tip in tips:
        taxel_ids[tip.flex_name] = np.asarray(tip.taxel_ids).ravel().tolist()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    mj.mj_saveModel(model, args.out.as_posix(), None)

    ctrl_path = args.out.with_suffix(".ctrl.npy")
    np.save(ctrl_path, ctrl)
    ctrl_hash = hashlib.sha256(ctrl_path.read_bytes()).hexdigest()

    sidecar = {
        "model": args.out.name,
        "ctrl": ctrl_path.name,
        "ctrl_sha256": ctrl_hash,
        "pattern": args.pattern,
        "duration": float(steps * args.dt),
        "steps": steps,
        "timestep": float(model.opt.timestep),
        "integrator": int(model.opt.integrator),
        "solver_iterations": int(model.opt.iterations),
        "solver_tolerance": float(model.opt.tolerance),
        "object": args.object,
        "object_mass": args.object_mass,
        "object_geom": object_geom_name(0) if specs else None,
        "contact_geom_names": [object_geom_name(0)] if specs else [],
        "taxel_ids": taxel_ids,
        "nq": int(model.nq),
        "nv": int(model.nv),
        "nflex": int(model.nflex),
        "mujoco": mj.__version__,
        **state,
    }
    sidecar_path = args.out.with_suffix(".json")
    sidecar_path.write_text(json.dumps(sidecar, indent=2))

    print(f"wrote {args.out}")
    print(f"      {ctrl_path.name}  {ctrl.shape}  sha256 {ctrl_hash[:16]}")
    print(f"      {sidecar_path.name}")
    print(f"  nq={model.nq} nv={model.nv} nflex={model.nflex}")
    print(f"  dt={model.opt.timestep} integrator={int(model.opt.integrator)} "
          f"iters={model.opt.iterations} tol={model.opt.tolerance}")
    print(f"  pattern={args.pattern} steps={steps} duration={steps * args.dt:.3f}s")
    if specs:
        print(f"  object={args.object} mass={args.object_mass} "
              f"pos={np.round(state['object_pose'][:3], 4).tolist()}")


if __name__ == "__main__":
    main()
