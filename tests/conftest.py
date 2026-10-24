"""Shared fixtures for the leapxela sensor tests.

The sparsh parity tests compare leapxela's ported sensor against the original in
``sparsh-skin-sim``.  That repo is a separate, untracked checkout, so every
fixture that reaches into it skips cleanly when it is absent.

Both libraries import in one interpreter (the sparsh force core needs only
mujoco + numpy, and the leapxela env now carries torch/pytorch_kinematics), so
parity runs in-process here.  The cross-env scripts under ``sparsh_compare/``
cover the same ground with each package in its own conda env.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import mujoco as mj
import numpy as np
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPARSH_ROOT = REPO_ROOT / "sparsh-skin-sim"
SPARSH_SCENE_RELPATH = Path("leapXELA_model/scene_mjx_cube_CoACD_mjx_flex_sensor.xml")

SOLVER_ITERATIONS = 50
SOLVER_TOLERANCE = 0.0


def pytest_addoption(parser):
    parser.addoption(
        "--sparsh-sim-root",
        action="store",
        default=str(DEFAULT_SPARSH_ROOT),
        help="Path to the sparsh-skin-sim checkout used for parity tests",
    )


@pytest.fixture(scope="session")
def sparsh_root(request) -> Path:
    root = Path(request.config.getoption("--sparsh-sim-root"))
    if not root.exists():
        pytest.skip(f"sparsh-skin-sim not found at {root}")
    return root


@pytest.fixture(scope="session")
def sparsh_flex_util(sparsh_root):
    """The upstream Kelvin-Voigt core (mujoco + numpy only)."""
    if str(sparsh_root) not in sys.path:
        sys.path.insert(0, str(sparsh_root))
    return pytest.importorskip("util.flex_util")


@pytest.fixture(scope="session")
def sparsh_fk_util(sparsh_root):
    """The upstream FK taxel layer (needs torch + pytorch_kinematics)."""
    if str(sparsh_root) not in sys.path:
        sys.path.insert(0, str(sparsh_root))
    return pytest.importorskip("util.fk_taxel_util")


@pytest.fixture(scope="session")
def sparsh_scene_model(sparsh_root) -> mj.MjModel:
    """The upstream scene, with the solver overrides every sparsh entry point applies."""
    path = sparsh_root / SPARSH_SCENE_RELPATH
    if not path.exists():
        pytest.skip(f"Upstream scene not found: {path}")
    model = mj.MjModel.from_xml_path(path.as_posix())
    model.opt.iterations = SOLVER_ITERATIONS
    model.opt.tolerance = SOLVER_TOLERANCE
    return model


def _build_leapxela_model(object_specs):
    from leapxela.episode import build_model

    return build_model(object_specs, 0.0, 0.0, 0.0)


@pytest.fixture(scope="session")
def leapxela_hand():
    """The generated leapxela hand with no objects: (model, skins, tips)."""
    return _build_leapxela_model([])


@pytest.fixture(scope="session")
def leapxela_hand_with_object():
    """Hand plus one box parked just above a palm pad, so contact starts quickly.

    Returns (model, skins, tips, geom_names). The object rest pose is written into
    qpos0 so every MjData starts loaded the same way.
    """
    from leapxela.episode import ObjectSpec, object_body_name, object_geom_name
    from leapxela.flex_force import flex_id

    model, skins, tips = _build_leapxela_model([ObjectSpec("box", 1.0, 0.3)])

    data = mj.MjData(model)
    mj.mj_forward(model, data)
    fid = flex_id(model, "flex_uspa46_1")
    vert_adr = int(model.flex_vertadr[fid])
    vert_num = int(model.flex_vertnum[fid])
    centre = data.flexvert_xpos[vert_adr : vert_adr + vert_num].mean(axis=0)

    body_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(0))
    qpos_adr = int(model.jnt_qposadr[int(model.body_jntadr[body_id])])
    model.qpos0[qpos_adr : qpos_adr + 7] = [
        centre[0], centre[1], centre[2] + 0.035, 1.0, 0.0, 0.0, 0.0
    ]
    return model, skins, tips, [object_geom_name(0)]


def settle_with_contact(model, readers_step, steps=220):
    """Step until the object has landed, calling readers_step(data) each step.

    Returns the MjData so callers can read the loaded state.
    """
    data = mj.MjData(model)
    for _ in range(steps):
        mj.mj_step(model, data)
        readers_step(data)
    return data
