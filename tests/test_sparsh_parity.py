"""Parity between leapxela's sparsh sensor and the sparsh-skin-sim original.

leapxela's sparsh sensor is a port of ``sparsh-skin-sim/util/flex_util.py`` and
``util/fk_taxel_util.py``.  These tests drive both libraries over the same model
and the same inputs, so any difference is a port defect rather than a difference
in simulation setup.

The two packages normally live in separate conda envs; ``sparsh_compare/`` holds
scripts that run each side in its own env and diff the traces.  Here everything
runs in one interpreter, which is what makes it cheap enough to keep in CI.
"""

import numpy as np
import pytest

from leapxela import flex_force as lx_flex
from leapxela.fk_taxel import (
    HAND_SS_URDF,
    TAXEL_MAP_JSON,
    build_taxel_ids_in_fk_order,
    compute_fk_taxels,
)

# Force, displacement and velocity come out bitwise identical; only the contact
# label splat picks up float reordering, and that stays near machine epsilon.
FORCE_ATOL = 1e-12
# The FK layer runs in torch float32, and the two envs ship different torch
# versions, so differences land at float32 epsilon (~1.2e-7).
FK_ATOL = 1e-5

GAINS = {
    "stiffness": 100.0,
    "damping": 0.05,
    "window": 5,
    "use_qvel": True,
    "velocity_smoothing": 0.3,
}


def _control_ramp(model, steps, grip_fraction=0.6):
    low = model.actuator_ctrlrange[:, 0].copy()
    high = model.actuator_ctrlrange[:, 1].copy()
    target = low + grip_fraction * (high - low)
    ramp = np.linspace(0.0, 1.0, steps, dtype=np.float64)[:, None]
    return low[None, :] + ramp * (target - low)[None, :]


def _free_body_geom_names(model):
    import mujoco as mj

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


def test_flex_topology_matches_upstream(sparsh_scene_model, sparsh_flex_util, leapxela_hand):
    """Both models must expose the same flexes with the same vertex counts.

    Everything downstream assumes it, and a mismatch here would silently
    invalidate every other parity claim.
    """
    model_lx = leapxela_hand[0]
    upstream = sorted(sparsh_flex_util.list_flex_names(sparsh_scene_model))
    ported = sorted(lx_flex.list_flex_names(model_lx))
    assert ported == upstream

    for name in upstream:
        lx_vertices = lx_flex.flex_vertex_body_ids(model_lx, name).shape
        ss_vertices = sparsh_flex_util.flex_vertex_body_ids(sparsh_scene_model, name).shape
        assert lx_vertices == ss_vertices, name


def test_estimator_trajectories_match_on_upstream_scene(
    sparsh_scene_model, sparsh_flex_util
):
    """Run both estimators over the same scene and the same control ramp."""
    import mujoco as mj

    model = sparsh_scene_model
    flex_names = sorted(lx_flex.list_flex_names(model))
    geom_names = _free_body_geom_names(model)
    ctrl = _control_ramp(model, 60)

    data_lx = mj.MjData(model)
    data_ss = mj.MjData(model)
    est_lx = {
        name: lx_flex.FlexForceEstimator(
            model, name, GAINS["stiffness"], GAINS["damping"],
            GAINS["window"], GAINS["use_qvel"], GAINS["velocity_smoothing"],
        )
        for name in flex_names
    }
    est_ss = {
        name: sparsh_flex_util.FlexForceEstimator(model, name, **GAINS)
        for name in flex_names
    }

    saw_contact = False
    for step in range(ctrl.shape[0]):
        data_lx.ctrl[:] = ctrl[step]
        data_ss.ctrl[:] = ctrl[step]
        mj.mj_step(model, data_lx)
        mj.mj_step(model, data_ss)
        for name in flex_names:
            frame = est_lx[name].update(model, data_lx)
            force, displacement, velocity = est_ss[name].update(model, data_ss)
            np.testing.assert_allclose(frame.force, force, atol=FORCE_ATOL, rtol=0)
            np.testing.assert_allclose(
                frame.displacement, displacement, atol=FORCE_ATOL, rtol=0
            )
            np.testing.assert_allclose(frame.velocity, velocity, atol=FORCE_ATOL, rtol=0)

            label_lx, count_lx = lx_flex.flex_vertex_contact_forces(
                model, data_lx, name, geom_names
            )
            label_ss, count_ss = sparsh_flex_util.flex_vertex_contact_forces(
                model, data_ss, name, geom_names
            )
            assert count_lx == count_ss
            np.testing.assert_allclose(label_lx, label_ss, atol=FORCE_ATOL, rtol=0)
            saw_contact = saw_contact or count_lx > 0

    assert saw_contact, "no contact occurred; the parity check would be vacuous"


def test_upstream_reads_leapxela_generated_model(leapxela_hand, sparsh_flex_util):
    """The upstream core must work unchanged on leapxela's generated model."""
    import mujoco as mj

    model, _skins, _tips = leapxela_hand
    flex_names = sorted(lx_flex.list_flex_names(model))
    ctrl = _control_ramp(model, 40)

    data = mj.MjData(model)
    est_lx = {
        name: lx_flex.FlexForceEstimator(
            model, name, GAINS["stiffness"], GAINS["damping"],
            GAINS["window"], GAINS["use_qvel"], GAINS["velocity_smoothing"],
        )
        for name in flex_names
    }
    est_ss = {
        name: sparsh_flex_util.FlexForceEstimator(model, name, **GAINS)
        for name in flex_names
    }

    for step in range(ctrl.shape[0]):
        data.ctrl[:] = ctrl[step]
        mj.mj_step(model, data)
        for name in flex_names:
            frame = est_lx[name].update(model, data)
            force, _u, _v = est_ss[name].update(model, data)
            np.testing.assert_allclose(frame.force, force, atol=FORCE_ATOL, rtol=0)


def test_default_damping_override_matches_upstream(sparsh_scene_model, sparsh_flex_util):
    """Both silently swap B for the model's dof_damping at the exact default."""
    name = "flex_uspa46_1"
    ported = lx_flex.FlexForceEstimator(sparsh_scene_model, name, 100.0, 0.05, 5, True, 0.3)
    upstream = sparsh_flex_util.FlexForceEstimator(sparsh_scene_model, name, damping=0.05)
    assert ported.damping == upstream.damping

    # A non-default value must survive untouched on both sides.
    ported_fixed = lx_flex.FlexForceEstimator(sparsh_scene_model, name, 100.0, 0.2, 5, True, 0.3)
    upstream_fixed = sparsh_flex_util.FlexForceEstimator(
        sparsh_scene_model, name, damping=0.2
    )
    assert ported_fixed.damping == upstream_fixed.damping == 0.2


def test_fk_assets_are_byte_identical(sparsh_fk_util):
    """The ported FK layer must read the same URDF and taxel map as upstream."""
    import hashlib

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    assert digest(HAND_SS_URDF) == digest(sparsh_fk_util._DEFAULT_URDF_PATH)
    assert digest(TAXEL_MAP_JSON) == digest(sparsh_fk_util._DEFAULT_TAXEL_MAP_PATH)


def test_fk_order_permutation_matches_upstream(sparsh_fk_util):
    ported = build_taxel_ids_in_fk_order(TAXEL_MAP_JSON)
    upstream = sparsh_fk_util.build_taxel_ids_in_fk_order(
        sparsh_fk_util._DEFAULT_TAXEL_MAP_PATH
    )
    np.testing.assert_array_equal(ported, upstream)
    np.testing.assert_array_equal(np.sort(ported), np.arange(368))


@pytest.mark.parametrize("pose_index", range(4))
def test_fk_taxel_frames_match_upstream(sparsh_fk_util, pose_index):
    rng = np.random.default_rng(pose_index)
    angles = rng.uniform(-0.5, 1.5, size=16).astype(np.float32)
    forces = rng.normal(scale=0.2, size=(368, 3))

    ported = compute_fk_taxels(angles, forces, HAND_SS_URDF, TAXEL_MAP_JSON, 0.02, 0.015, True)
    upstream = sparsh_fk_util.compute_fk_taxels(
        angles,
        forces,
        urdf_path=sparsh_fk_util._DEFAULT_URDF_PATH,
        deform_scale=0.02,
        max_disp=0.015,
        mujoco_world=True,
    )

    for field in (
        "positions",
        "rotations",
        "forces_local",
        "forces_world",
        "positions_deformed",
    ):
        np.testing.assert_allclose(
            np.asarray(getattr(ported, field), dtype=np.float64),
            np.asarray(getattr(upstream, field), dtype=np.float64),
            atol=FK_ATOL,
            rtol=0,
            err_msg=f"{field} diverged at pose {pose_index}",
        )


def test_episode_feeds_fk_the_same_force_frame_as_upstream(
    leapxela_hand_with_object, sparsh_flex_util, sparsh_fk_util
):
    """The FK layer must be driven in vertex-body axes, as sparsh-skin-sim drives it.

    `sensors.read_sparsh().flat` flips the normal so it reads compression-positive
    alongside the contact sensor. Feeding *that* to compute_fk_taxels -- which the
    episode used to do -- inverted forces_local/forces_world and pushed
    positions_deformed the wrong way relative to upstream. `flat_body` is the
    channel the FK is fed instead.
    """
    import mujoco as mj

    from leapxela.sensors import (
        SparshSensorConfig,
        build_sparsh_readers,
        read_sparsh,
    )

    model, skins, tips, _geom_names = leapxela_hand_with_object
    config = SparshSensorConfig(
        GAINS["stiffness"], GAINS["damping"], GAINS["window"],
        GAINS["use_qvel"], GAINS["velocity_smoothing"], 0.0, 0.0, 0.0, None, None,
    )
    readers = build_sparsh_readers(model, skins, tips, config)
    flex_names = sorted(lx_flex.list_flex_names(model))
    upstream_estimators = {
        name: sparsh_flex_util.FlexForceEstimator(model, name, **GAINS)
        for name in flex_names
    }

    data = mj.MjData(model)
    for _ in range(260):
        mj.mj_step(model, data)
        readout = read_sparsh(model, data, readers, 0.0)
        upstream_forces = {
            name: estimator.update(model, data)[0]
            for name, estimator in upstream_estimators.items()
        }

    upstream_packed = sparsh_fk_util.flex_forces_to_taxel_forces(model, upstream_forces)
    assert np.abs(upstream_packed).max() > 0.0, "no signal; the check would be vacuous"

    # The channel fed to FK matches upstream exactly...
    np.testing.assert_allclose(readout.flat_body, upstream_packed, atol=1e-12, rtol=0)
    # ...and the sensor channel is the same reading with the normal flipped.
    np.testing.assert_allclose(readout.flat[:, :2], upstream_packed[:, :2], atol=1e-12, rtol=0)
    np.testing.assert_allclose(readout.flat[:, 2], -upstream_packed[:, 2], atol=1e-12, rtol=0)
    assert not np.allclose(readout.flat, readout.flat_body), (
        "normal channel is not actually loaded, so this test proves nothing"
    )
