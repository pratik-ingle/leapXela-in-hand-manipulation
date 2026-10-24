"""Run 2: each package builds its own scene, matched on everything matchable.

Run 1 (``dump_sensor_trace.py`` against a shared ``.mjb``) isolates the sensor
code by making every input bit-identical.  This script answers the other half of
the question -- do the two *shipping pipelines* agree -- by letting each package
construct its own scene the way it normally would, while holding the object,
grasp pattern, timestep, integrator and solver settings equal.

The object pose cannot be made bit-identical across two different scene graphs,
so the output is compared distributionally rather than step-by-step.

Both sides use their own policy: ``episode.control_targets`` and
``motion_util.grasp_target`` were verified to produce bitwise-identical targets
for every pattern, so policy is not a confound here.
"""

import argparse
import json
import platform
import sys
from pathlib import Path
from types import SimpleNamespace

import mujoco as mj
import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPARSH_ROOT = REPO_ROOT / "sparsh-skin-sim"
SPARSH_SCENE_RELPATH = Path("leapXELA_model/scene_mjx_cube_CoACD_mjx_flex_sensor.xml")
TAXEL_COUNT = 368
SOLVER_ITERATIONS = 50
SOLVER_TOLERANCE = 0.0
PALM_FLEX = "flex_uspa46_1"

INTEGRATORS = {
    "euler": mj.mjtIntegrator.mjINT_EULER,
    "rk4": mj.mjtIntegrator.mjINT_RK4,
    "implicit": mj.mjtIntegrator.mjINT_IMPLICIT,
    "implicitfast": mj.mjtIntegrator.mjINT_IMPLICITFAST,
}


def apply_pregrip_generic(model: mj.MjModel, pregrip_fraction: float) -> None:
    """Pre-curl the hand and bake it into qpos0, without importing either package.

    Mirrors episode.apply_pregrip: drive each actuated joint to
    low + fraction * (high - low). Written model-generically so the sparsh scene
    starts from the same pose as the leapxela hand.
    """
    low = model.actuator_ctrlrange[:, 0]
    high = model.actuator_ctrlrange[:, 1]
    targets = low + pregrip_fraction * (high - low)
    data = mj.MjData(model)
    for actuator_id in range(model.nu):
        joint_id = int(model.actuator_trnid[actuator_id, 0])
        data.qpos[int(model.jnt_qposadr[joint_id])] = targets[actuator_id]
    mj.mj_forward(model, data)
    model.qpos0[:] = data.qpos


def palm_centre(model: mj.MjModel) -> np.ndarray:
    data = mj.MjData(model)
    mj.mj_forward(model, data)
    fid = mj.mj_name2id(model, mj.mjtObj.mjOBJ_FLEX, PALM_FLEX)
    adr = int(model.flex_vertadr[fid])
    num = int(model.flex_vertnum[fid])
    return data.flexvert_xpos[adr : adr + num].mean(axis=0)


def place_free_body(model: mj.MjModel, body_name: str, pos: np.ndarray) -> None:
    body_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, body_name)
    qadr = int(model.jnt_qposadr[int(model.body_jntadr[body_id])])
    model.qpos0[qadr : qadr + 7] = [*pos, 1.0, 0.0, 0.0, 0.0]


def build_leapxela(args):
    from leapxela.episode import ObjectSpec, build_model, control_targets, profile_from_args
    from leapxela.sensors import (
        SparshSensorConfig, build_contact_readers, build_sparsh_readers,
        read_contact_data, read_sparsh,
    )

    model, skins, tips = build_model(
        [ObjectSpec("box", 1.0, args.object_mass)], args.palm_pitch, 0.0, 0.0
    )
    model.opt.timestep = args.dt
    model.opt.integrator = INTEGRATORS[args.integrator]
    model.opt.iterations = SOLVER_ITERATIONS
    model.opt.tolerance = SOLVER_TOLERANCE

    apply_pregrip_generic(model, args.pregrip_fraction)
    centre = palm_centre(model)
    place_free_body(model, "grasp_object", centre + [0.0, 0.0, args.clearance])

    profile = profile_from_args(args.pattern, SimpleNamespace(
        grip_fraction=args.grip_fraction, thumb_grip_fraction=args.thumb_grip_fraction,
        pregrip_fraction=args.pregrip_fraction, thumb_delay=args.thumb_delay,
        pulse_hz=1.0, pulse_amplitude=0.15, shear_amplitude=0.15, squeeze_steps=4,
    ))
    config = SparshSensorConfig(
        args.stiffness, args.damping, args.window, True, args.velocity_smoothing,
        0.0, 0.0, 0.0, None, None,
    )
    sparsh_readers = build_sparsh_readers(model, skins, tips, config)
    contact_readers = build_contact_readers(model, skins, tips, ["grasp_object_geom"])

    def policy(t):
        return control_targets(model, t, profile)

    def read(model_, data):
        readout = read_sparsh(model_, data, sparsh_readers, 0.0)
        contact = read_contact_data(contact_readers, data)
        return {
            "sparsh_flat": readout.flat.copy(),
            "contact_flat": contact.flat.copy(),
        }

    return model, policy, read, "leapxela-native", ["grasp_object_geom"]


def build_sparsh(args, sparsh_root: Path):
    sys.path.insert(0, str(sparsh_root))
    from util import flex_util, fk_taxel_util, motion_util, objects_util

    scene = sparsh_root / SPARSH_SCENE_RELPATH
    spec = mj.MjSpec.from_file(scene.as_posix())
    # Spawn through the package's own object helper, matched to leapxela's box.
    objects_util.add_cube(
        spec, name="test_box", half_size=args.object_half_size, mass=args.object_mass,
        above_palm=True, flex_name=PALM_FLEX, clearance=args.clearance,
    )
    model = spec.compile()
    model.opt.timestep = args.dt
    model.opt.integrator = INTEGRATORS[args.integrator]
    model.opt.iterations = SOLVER_ITERATIONS
    model.opt.tolerance = SOLVER_TOLERANCE

    # The stock scene ships a 77mm reorientation cube that also lands on the skin.
    # Leaving it in would mean comparing a one-object grasp against a two-object
    # one, so it is disabled and parked rather than deleted.
    stock = mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, "cube")
    if stock >= 0:
        model.geom_contype[stock] = 0
        model.geom_conaffinity[stock] = 0
        place_free_body(model, "cube", np.array([0.0, 0.0, -5.0]))

    # add_cube defaults to contype=1/conaffinity=2, which collides with the flex
    # skins but not the rigid hand structure; leapxela's objects use 3/3. Left
    # unmatched the upstream hand simply drops the box, and the comparison
    # measures retention rather than sensing. Friction, size, solref and solimp
    # already agree.
    if args.match_contact_bitmask:
        for name in ("test_box", "test_box_geom"):
            gid = mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
            if gid >= 0:
                model.geom_contype[gid] = 3
                model.geom_conaffinity[gid] = 3

    apply_pregrip_generic(model, args.pregrip_fraction)
    centre = palm_centre(model)
    place_free_body(model, "test_box", centre + [0.0, 0.0, args.clearance])

    profile = motion_util.default_grasp_profile(args.pattern)
    profile = type(profile)(
        pattern=args.pattern, grip_fraction=args.grip_fraction,
        thumb_grip_fraction=args.thumb_grip_fraction,
        pregrip_fraction=args.pregrip_fraction, thumb_delay=args.thumb_delay,
        pulse_hz=1.0, pulse_amplitude=0.15, shear_amplitude=0.15, squeeze_steps=4,
    )
    flex_names = sorted(flex_util.list_flex_names(model))
    estimators = {
        name: flex_util.FlexForceEstimator(
            model, name, stiffness=args.stiffness, damping=args.damping,
            window=args.window, use_qvel=True,
            velocity_smoothing=args.velocity_smoothing,
        )
        for name in flex_names
    }

    def policy(t):
        return motion_util.grasp_target(model, t, profile)

    def read(model_, data):
        forces = {n: e.update(model_, data)[0] for n, e in estimators.items()}
        body = fk_taxel_util.flex_forces_to_taxel_forces(model_, forces)
        flipped = body.copy()
        flipped[:, 2] = -flipped[:, 2]
        return {"sparsh_flat": flipped, "sparsh_body": body}

    return model, policy, read, "sparsh-native", ["test_box_geom", "test_box"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--impl", choices=("leapxela", "sparsh"), required=True)
    parser.add_argument("--sparsh-root", type=Path, default=DEFAULT_SPARSH_ROOT)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--pattern", default="squeeze")
    parser.add_argument("--duration", type=float, default=2.5)
    parser.add_argument("--dt", type=float, default=0.001)
    parser.add_argument("--integrator", choices=tuple(INTEGRATORS), default="euler")
    parser.add_argument(
        "--palm-pitch", type=float, default=0.0,
        help="leapxela only: tilt the palm, in degrees. leapxela levels the palm "
        "(0 deg) while the upstream scene mounts the hand at ~17.7 deg, which is "
        "what governs whether the object stays on the pad.",
    )
    parser.add_argument("--object-mass", type=float, default=0.3)
    parser.add_argument("--object-half-size", type=float, default=0.022)
    parser.add_argument("--clearance", type=float, default=0.035)
    parser.add_argument(
        "--match-contact-bitmask", action=argparse.BooleanOptionalAction, default=True,
        help="sparsh only: raise the spawned cube to leapxela's contype/conaffinity 3/3",
    )
    parser.add_argument("--grip-fraction", type=float, default=0.55)
    parser.add_argument("--thumb-grip-fraction", type=float, default=0.35)
    parser.add_argument("--pregrip-fraction", type=float, default=0.40)
    parser.add_argument("--thumb-delay", type=float, default=0.5)
    parser.add_argument("--stiffness", type=float, default=100.0)
    parser.add_argument("--damping", type=float, default=0.05)
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--velocity-smoothing", type=float, default=0.3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.impl == "leapxela":
        model, policy, read, tag, geom_names = build_leapxela(args)
    else:
        model, policy, read, tag, geom_names = build_sparsh(args, args.sparsh_root)

    data = mj.MjData(model)
    steps = max(2, int(round(args.duration / float(model.opt.timestep))))
    series: dict[str, list] = {}
    times, ncon, ctrl_log = [], [], []

    for step in range(steps):
        t = (step + 1) * float(model.opt.timestep)
        target = policy(t)
        data.ctrl[:] = target
        mj.mj_step(model, data)
        times.append(float(data.time))
        ncon.append(int(data.ncon))
        ctrl_log.append(np.asarray(target, dtype=np.float64))
        for key, value in read(model, data).items():
            series.setdefault(key, []).append(np.asarray(value, dtype=np.float64))

    arrays = {key: np.stack(value) for key, value in series.items()}
    arrays["time"] = np.asarray(times)
    arrays["ncon"] = np.asarray(ncon)
    arrays["ctrl"] = np.stack(ctrl_log)

    meta = {
        "impl": "leapxela" if args.impl == "leapxela" else "sparsh",
        "run": tag,
        "sensors": "both" if args.impl == "leapxela" else "sparsh",
        "model_path": tag,
        "pattern": args.pattern,
        "flex_names": sorted(
            mj.mj_id2name(model, mj.mjtObj.mjOBJ_FLEX, i) for i in range(model.nflex)
        ),
        "contact_geom_names": geom_names,
        "object_mass": args.object_mass,
        "object_half_size": args.object_half_size,
        "steps": steps,
        "duration": float(steps * model.opt.timestep),
        "timestep": float(model.opt.timestep),
        "integrator": int(model.opt.integrator),
        "solver_iterations": int(model.opt.iterations),
        "solver_tolerance": float(model.opt.tolerance),
        "nq": int(model.nq), "nv": int(model.nv), "nflex": int(model.nflex),
        "mujoco": mj.__version__, "numpy": np.__version__,
        "python": platform.python_version(),
    }
    arrays["metadata_json"] = json.dumps(meta, indent=2)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.out, **arrays)

    print(f"[{tag}] wrote {args.out}")
    print(f"  dt={model.opt.timestep} integrator={int(model.opt.integrator)} "
          f"iters={model.opt.iterations}")
    print(f"  nq={model.nq} nflex={model.nflex} steps={steps} "
          f"duration={meta['duration']:.3f}s pattern={args.pattern}")
    print(f"  peak ncon={int(arrays['ncon'].max())}")
    for key in ("sparsh_flat", "contact_flat"):
        if key in arrays:
            normal = arrays[key][..., 2]
            print(f"  {key:<12} peak taxel {normal.max():+.5f} N  "
                  f"peak total {normal.sum(axis=-1).max():+.5f} N")


if __name__ == "__main__":
    main()
