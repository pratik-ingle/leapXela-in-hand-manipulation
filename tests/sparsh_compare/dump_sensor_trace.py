"""Dump taxel traces for cross-implementation comparison.

The leapxela sparsh sensor was ported from sparsh-skin-sim, and the two packages
live in different conda envs (``leapxela`` and ``sparsh-skin``).  This script runs
in either one: ``--impl`` selects which library to import, and the import is lazy
so neither env ever needs the other's dependencies.

Give both runs the same ``.mjb`` and the same ``--ctrl`` trajectory and every input
is bit-identical, so any difference in the output is the sensor code.  Outputs are
packed to ``(T, 368, 3)`` by hardware taxel id using each side's *own* packing --
leapxela via ``sensors.read_sparsh``, upstream via
``fk_taxel_util.flex_forces_to_taxel_forces`` -- which also tests that the two
packings agree rather than assuming it.

``--sensors both`` additionally reads leapxela's original contact sensor in the
same pass, so the two readouts are exactly time-aligned.

Usage::

    python dump_sensor_trace.py --impl leapxela --sensors both \\
        --model hand.mjb --ctrl hand.ctrl.npy --out lx.npz
    python dump_sensor_trace.py --impl sparsh \\
        --model hand.mjb --ctrl hand.ctrl.npy --out ss.npz
"""

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import mujoco as mj
import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SPARSH_ROOT = REPO_ROOT / "sparsh-skin-sim"
SPARSH_SCENE_RELPATH = Path("leapXELA_model/scene_mjx_cube_CoACD_mjx_flex_sensor.xml")
TAXEL_COUNT = 368

# Every sparsh-skin-sim entry point overrides these two before stepping; the
# shipped XML has iterations=5, which leaves the skins under-converged.
SOLVER_ITERATIONS = 50
SOLVER_TOLERANCE = 0.0

INTEGRATORS = {
    "euler": mj.mjtIntegrator.mjINT_EULER,
    "rk4": mj.mjtIntegrator.mjINT_RK4,
    "implicit": mj.mjtIntegrator.mjINT_IMPLICIT,
    "implicitfast": mj.mjtIntegrator.mjINT_IMPLICITFAST,
}


# --------------------------------------------------------------------------
# Implementation adapters
#
# The two libraries expose the same algorithm behind different signatures:
# sparsh-skin-sim uses keyword-only gains and returns a plain tuple, leapxela
# uses positional gains and returns a FlexForceFrame. leapxela also owns the
# contact sensor and the calibrated taxel layout, which upstream has no
# equivalent for. These adapters hide all of that so the trace loop is one loop.
# --------------------------------------------------------------------------
class _LeapxelaImpl:
    """Reads through leapxela's own sensors.py facade, not the raw core.

    That is deliberate: the facade is what collection actually uses, so it is
    what should be compared -- including its taxel packing and its normal-channel
    sign flip.
    """

    name = "leapxela"
    provides_contact = True

    def __init__(self, sensors_mode: str):
        from leapxela import flex_force, sensors

        self._flex = flex_force
        self._sensors = sensors
        self._mode = sensors_mode
        self._model = None
        self._skins = None
        self._tips = None
        self._sparsh_readers = None
        self._contact_readers = None

    def build_model(self, spec: str, sparsh_root: Path):
        """leapxela rebuilds its hand in-process so skins/tips are available.

        A bare .mjb cannot supply the FlexSkin/TipSkin objects the contact sensor
        and the calibrated taxel ids come from, so when a .mjb is given we load it
        for physics and rebuild the layout metadata alongside it.
        """
        from leapxela.episode import build_model as lx_build

        if spec == "sparsh-xml":
            path = sparsh_root / SPARSH_SCENE_RELPATH
            model = mj.MjModel.from_xml_path(path.as_posix())
            self._skins, self._tips = None, None
            return model, path.as_posix()

        path = Path(spec)
        model = (
            mj.MjModel.from_binary_path(path.as_posix())
            if path.suffix == ".mjb"
            else mj.MjModel.from_xml_path(path.as_posix())
        )
        # Rebuild the layout to recover skins/tips. Object specs do not affect
        # skin/tip taxel ids, so an empty build is enough for the metadata.
        _m, skins, tips = lx_build([], 0.0, 0.0, 0.0)
        self._skins, self._tips = skins, tips
        return model, path.as_posix()

    def setup(self, model, gains, geom_names):
        self._model = model
        if self._skins is None:
            raise RuntimeError(
                "leapxela readers need the generated hand layout; "
                "pass a leapxela .mjb rather than --model sparsh-xml"
            )
        config = self._sensors.SparshSensorConfig(
            gains["stiffness"], gains["damping"], gains["window"],
            gains["use_qvel"], gains["velocity_smoothing"],
            0.0, 0.0, 0.0, None, None,
        )
        self._sparsh_readers = self._sensors.build_sparsh_readers(
            model, self._skins, self._tips, config
        )
        if self._mode in ("contact", "both"):
            self._contact_readers = self._sensors.build_contact_readers(
                model, self._skins, self._tips, geom_names
            )

    def read(self, model, data) -> dict:
        out = {}
        readout = self._sensors.read_sparsh(model, data, self._sparsh_readers, 0.0)
        out["sparsh_flat"] = readout.flat.copy()
        # Body-frame copy: sensors.py flips z, upstream does not, so the
        # like-for-like comparison needs the unflipped channel too.
        body = np.zeros((TAXEL_COUNT, 3), dtype=np.float64)
        for reader in self._sparsh_readers:
            body[reader.taxel_ids] = readout.flex_force[reader.name]
        out["sparsh_body"] = body
        if self._contact_readers is not None:
            contact = self._sensors.read_contact_data(self._contact_readers, data)
            out["contact_flat"] = contact.flat.copy()
            out["contact_count"] = contact.contact_count
        return out

    def taxel_ids(self) -> dict:
        ids = {}
        for skin in self._skins:
            ids[skin.flex_name] = np.asarray(skin.taxel_ids).ravel()
        for tip in self._tips:
            ids[tip.flex_name] = np.asarray(tip.taxel_ids).ravel()
        return ids


class _SparshImpl:
    name = "sparsh"
    provides_contact = False

    def __init__(self, sparsh_root: Path, sensors_mode: str):
        sys.path.insert(0, str(sparsh_root))
        from util import flex_util, fk_taxel_util

        self._flex = flex_util
        self._fk = fk_taxel_util
        self._estimators = None
        self._flex_names = None

    def build_model(self, spec: str, sparsh_root: Path):
        if spec == "sparsh-xml":
            path = sparsh_root / SPARSH_SCENE_RELPATH
            return mj.MjModel.from_xml_path(path.as_posix()), path.as_posix()
        path = Path(spec)
        model = (
            mj.MjModel.from_binary_path(path.as_posix())
            if path.suffix == ".mjb"
            else mj.MjModel.from_xml_path(path.as_posix())
        )
        return model, path.as_posix()

    def setup(self, model, gains, geom_names):
        self._flex_names = sorted(self._flex.list_flex_names(model))
        self._estimators = {
            name: self._flex.FlexForceEstimator(
                model, name,
                stiffness=gains["stiffness"], damping=gains["damping"],
                window=gains["window"], use_qvel=gains["use_qvel"],
                velocity_smoothing=gains["velocity_smoothing"],
            )
            for name in self._flex_names
        }

    def read(self, model, data) -> dict:
        forces = {}
        for name, estimator in self._estimators.items():
            force, _u, _v = estimator.update(model, data)
            forces[name] = force
        body = self._fk.flex_forces_to_taxel_forces(model, forces)
        flipped = body.copy()
        flipped[:, 2] = -flipped[:, 2]
        return {"sparsh_body": body, "sparsh_flat": flipped}

    def taxel_ids(self) -> dict:
        mapper = self._fk.build_flex_taxel_mapper(self._model_ref)
        ids = {}
        for taxel_id, (flex_name, vertex) in mapper.items():
            ids.setdefault(flex_name, {})[vertex] = taxel_id
        return {
            name: np.array([v for _k, v in sorted(entry.items())], dtype=np.int64)
            for name, entry in ids.items()
        }


def load_impl(impl: str, sparsh_root: Path, sensors_mode: str):
    if impl == "leapxela":
        return _LeapxelaImpl(sensors_mode)
    if impl == "sparsh":
        return _SparshImpl(sparsh_root, sensors_mode)
    raise ValueError(f"Unknown impl '{impl}'")


def free_body_geom_names(model: mj.MjModel) -> list[str]:
    """Names of geoms on free-floating bodies, i.e. the objects that press the skin."""
    names = []
    for geom_id in range(model.ngeom):
        body_id = int(model.geom_bodyid[geom_id])
        adr = int(model.body_jntadr[body_id])
        count = int(model.body_jntnum[body_id])
        if not any(
            int(model.jnt_type[adr + offset]) == int(mj.mjtJoint.mjJNT_FREE)
            for offset in range(count)
        ):
            continue
        name = mj.mj_id2name(model, mj.mjtObj.mjOBJ_GEOM, geom_id)
        if name:
            names.append(name)
    return names


def control_ramp(model: mj.MjModel, steps: int, grip_fraction: float) -> np.ndarray:
    """Fallback trajectory when no --ctrl file is supplied: a plain linear ramp."""
    low = model.actuator_ctrlrange[:, 0].copy()
    high = model.actuator_ctrlrange[:, 1].copy()
    target = low + grip_fraction * (high - low)
    ramp = np.linspace(0.0, 1.0, steps, dtype=np.float64)[:, None]
    return low[None, :] + ramp * (target - low)[None, :]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--impl", choices=("leapxela", "sparsh"), required=True)
    parser.add_argument(
        "--sensors", choices=("sparsh", "contact", "both"), default="sparsh",
        help="'contact'/'both' are leapxela-only; upstream has no contact sensor",
    )
    parser.add_argument("--model", default="sparsh-xml")
    parser.add_argument("--ctrl", type=Path, default=None,
                        help="Replay a saved (T,16) trajectory; the shared-input path")
    parser.add_argument("--sparsh-root", type=Path, default=DEFAULT_SPARSH_ROOT)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--duration", type=float, default=None)
    parser.add_argument("--grip-fraction", type=float, default=0.6)
    parser.add_argument("--stiffness", type=float, default=100.0)
    parser.add_argument("--damping", type=float, default=0.05)
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--no-use-qvel", dest="use_qvel", action="store_false")
    parser.add_argument("--velocity-smoothing", type=float, default=0.3)
    parser.add_argument("--dt", type=float, default=None)
    parser.add_argument("--integrator", choices=tuple(INTEGRATORS), default=None)
    parser.add_argument("--contact-labels", action=argparse.BooleanOptionalAction, default=True,
                        help="Also record MuJoCo contact-wrench ground truth per flex")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.sensors != "sparsh" and args.impl != "leapxela":
        raise SystemExit("--sensors contact/both requires --impl leapxela")

    impl = load_impl(args.impl, args.sparsh_root, args.sensors)
    model, model_path = impl.build_model(args.model, args.sparsh_root)
    impl._model_ref = model

    model.opt.iterations = SOLVER_ITERATIONS
    model.opt.tolerance = SOLVER_TOLERANCE
    if args.dt is not None:
        model.opt.timestep = args.dt
    if args.integrator is not None:
        model.opt.integrator = INTEGRATORS[args.integrator]

    geom_names = free_body_geom_names(model)

    if args.ctrl is not None:
        ctrl = np.load(args.ctrl)
        ctrl_hash = hashlib.sha256(Path(args.ctrl).read_bytes()).hexdigest()
        if ctrl.shape[1] != model.nu:
            raise SystemExit(f"ctrl has {ctrl.shape[1]} columns, model has {model.nu} actuators")
    else:
        steps = (
            args.steps if args.duration is None
            else max(2, int(round(args.duration / float(model.opt.timestep))))
        )
        ctrl = control_ramp(model, steps, args.grip_fraction)
        ctrl_hash = None

    gains = {
        "stiffness": args.stiffness,
        "damping": args.damping,
        "window": args.window,
        "use_qvel": args.use_qvel,
        "velocity_smoothing": args.velocity_smoothing,
    }
    impl.setup(model, gains, geom_names)

    flex_names = sorted(impl._flex.list_flex_names(model))
    data = mj.MjData(model)

    series: dict[str, list] = {}
    times, ncon, contact_counts = [], [], []
    labels = {name: [] for name in flex_names} if args.contact_labels else {}

    for step in range(ctrl.shape[0]):
        data.ctrl[:] = ctrl[step]
        mj.mj_step(model, data)
        times.append(float(data.time))
        ncon.append(int(data.ncon))
        frame = impl.read(model, data)
        for key, value in frame.items():
            if key == "contact_count":
                contact_counts.append(int(value))
                continue
            series.setdefault(key, []).append(np.asarray(value, dtype=np.float64))
        if args.contact_labels:
            for name in flex_names:
                label, _count = impl._flex.flex_vertex_contact_forces(
                    model, data, name, geom_names
                )
                labels[name].append(np.asarray(label, dtype=np.float64))

    arrays = {key: np.stack(value) for key, value in series.items()}
    arrays["time"] = np.asarray(times)
    arrays["ncon"] = np.asarray(ncon)
    arrays["ctrl"] = ctrl
    if contact_counts:
        arrays["contact_count"] = np.asarray(contact_counts)
    for name, stack in labels.items():
        arrays[f"contact_label/{name}"] = np.stack(stack)
    for name, ids in impl.taxel_ids().items():
        arrays[f"taxel_ids/{name}"] = np.asarray(ids, dtype=np.int64)

    meta = {
        "impl": impl.name,
        "sensors": args.sensors,
        "model_path": model_path,
        "ctrl_path": str(args.ctrl) if args.ctrl else None,
        "ctrl_sha256": ctrl_hash,
        "flex_names": flex_names,
        "contact_geom_names": geom_names,
        "gains": gains,
        "steps": int(ctrl.shape[0]),
        "duration": float(ctrl.shape[0] * model.opt.timestep),
        "timestep": float(model.opt.timestep),
        "integrator": int(model.opt.integrator),
        "solver_iterations": int(model.opt.iterations),
        "solver_tolerance": float(model.opt.tolerance),
        "nq": int(model.nq),
        "nv": int(model.nv),
        "nflex": int(model.nflex),
        "mujoco": mj.__version__,
        "numpy": np.__version__,
        "python": platform.python_version(),
    }
    arrays["metadata_json"] = json.dumps(meta, indent=2)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.out, **arrays)

    print(f"[{impl.name}/{args.sensors}] wrote {args.out}")
    print(f"  model      {model_path}")
    print(f"  dt         {model.opt.timestep}  integrator {int(model.opt.integrator)}"
          f"  iters {model.opt.iterations}")
    print(f"  steps      {ctrl.shape[0]}  duration {meta['duration']:.3f}s"
          f"  ctrl_sha {(ctrl_hash or 'n/a')[:16]}")
    print(f"  contact    geoms={geom_names} peak ncon={int(arrays['ncon'].max())}")
    for key in ("sparsh_flat", "contact_flat"):
        if key in arrays:
            normal = arrays[key][..., 2]
            print(f"  {key:<12} peak taxel normal {normal.max():+.5f} N   "
                  f"peak total {normal.sum(axis=-1).max():+.5f} N")
    print(f"  mujoco     {mj.__version__}  numpy {np.__version__}  py {platform.python_version()}")


if __name__ == "__main__":
    main()
