"""leapxela-side behaviour of the sparsh sensor that has no upstream counterpart.

``sensors.py`` wraps the ported Kelvin-Voigt core so it can stand in for, or run
alongside, the original contact sensor.  That wrapper adds things sparsh-skin-sim
never had -- a 368-taxel flat packing, a sign flip on the normal channel, and the
contact/sparsh/both mode switch -- so it needs its own tests.
"""

import mujoco as mj
import numpy as np
import pytest

from leapxela.flex_force import flex_vertex_contact_forces
from leapxela.hand_builder import TAXEL_COUNT
from leapxela.sensors import (
    SENSOR_MODES,
    SparshSensorConfig,
    build_contact_readers,
    build_sparsh_readers,
    contact_enabled,
    default_sparsh_config,
    make_sparsh_config,
    primary_source,
    read_contact_data,
    read_sparsh,
    resolve_heatmap_sources,
    sparsh_enabled,
)


ACTIVITY_THRESHOLD = 0.005


def _config(**overrides) -> SparshSensorConfig:
    base = dict(
        stiffness=100.0,
        damping=0.05,
        window=5,
        use_qvel=True,
        velocity_smoothing=0.3,
        activity_threshold=ACTIVITY_THRESHOLD,
        min_peak_normal=0.01,
        min_contact_fraction=0.05,
        calibration_path=None,
        calibration_hash=None,
    )
    base.update(overrides)
    return SparshSensorConfig(**base)


@pytest.fixture(scope="module")
def loaded_readout(leapxela_hand_with_object):
    """Step until the box has settled on the palm, then read both sensors."""
    model, skins, tips, geom_names = leapxela_hand_with_object
    config = _config()
    sparsh_readers = build_sparsh_readers(model, skins, tips, config)
    contact_readers = build_contact_readers(model, skins, tips, geom_names)

    data = mj.MjData(model)
    best = None
    for _ in range(400):
        mj.mj_step(model, data)
        sparsh = read_sparsh(model, data, sparsh_readers, ACTIVITY_THRESHOLD)
        contact = read_contact_data(contact_readers, data)
        if best is None or contact.contact_count > best[0].contact_count:
            best = (contact, sparsh)
    assert best is not None
    contact, sparsh = best
    assert contact.contact_count > 0, "object never touched the skin"
    return model, skins, tips, geom_names, contact, sparsh, sparsh_readers


def test_sparsh_readers_cover_every_taxel_exactly_once(leapxela_hand):
    model, skins, tips = leapxela_hand
    readers = build_sparsh_readers(model, skins, tips, _config())

    ids = np.concatenate([reader.taxel_ids.ravel() for reader in readers])
    assert ids.size == TAXEL_COUNT
    np.testing.assert_array_equal(np.sort(ids), np.arange(TAXEL_COUNT))


def test_sparsh_and_contact_readers_share_taxel_assignment(leapxela_hand):
    """Both sources must write the same taxel id to the same patch.

    They are meant to be interchangeable views of one sensor, so a mismatched
    packing would make `--sensor-mode both` compare unrelated taxels.
    """
    model, skins, tips = leapxela_hand
    sparsh = build_sparsh_readers(model, skins, tips, _config())
    contact = build_contact_readers(model, skins, tips, [])

    assert [r.name for r in sparsh] == [r.name for r in contact]
    for left, right in zip(sparsh, contact):
        np.testing.assert_array_equal(left.taxel_ids, right.taxel_ids)


def test_normal_channel_is_flipped_against_body_frame(loaded_readout):
    """`sensors.py` negates z so the normal reads compression-positive."""
    *_, sparsh, _readers = loaded_readout
    assert sparsh.flex_force  # patches present
    for name, body in sparsh.flex_force.items():
        sensor = sparsh.flex_force_sensor[name]
        np.testing.assert_allclose(sensor[:, 2], -body[:, 2], rtol=0, atol=0)
        # The tangential channels must pass through untouched.
        np.testing.assert_allclose(sensor[:, :2], body[:, :2], rtol=0, atol=0)


def test_compression_reads_positive_on_the_normal_channel(loaded_readout):
    """The flipped sign must agree with MuJoCo's own contact wrenches.

    This is the one place the port deliberately diverges from upstream, so it is
    checked against ground truth rather than against sparsh-skin-sim.
    """
    model, skins, tips, geom_names, _contact, sparsh, readers = loaded_readout

    # Re-run to a loaded state and compare signs on the patch under the object.
    data = mj.MjData(model)
    for reader in readers:
        reader.estimator.reset()

    best_patch, best_normal, best_label = None, 0.0, None
    for _ in range(400):
        mj.mj_step(model, data)
        readout = read_sparsh(model, data, readers, ACTIVITY_THRESHOLD)
        for reader in readers:
            label, count = flex_vertex_contact_forces(
                model, data, reader.estimator.flex_name, geom_names
            )
            if count == 0:
                continue
            normal = float(readout.flex_force_sensor[reader.name][:, 2].max())
            if normal > best_normal:
                best_patch, best_normal, best_label = reader.name, normal, label

    assert best_patch is not None, "no patch registered a contact"
    assert best_normal > ACTIVITY_THRESHOLD, (
        f"loaded patch {best_patch} reported normal {best_normal:.5f} N, "
        "which is at or below the noise floor -- the sign flip may be inverted"
    )
    # Ground-truth normal on the same patch, in the same flipped convention.
    assert float((-best_label[:, 2]).max()) > 0.0


def test_active_taxels_counted_on_the_flipped_channel(loaded_readout):
    *_, sparsh, _readers = loaded_readout
    expected = sum(
        int(np.count_nonzero(grid[:, 2] > ACTIVITY_THRESHOLD))
        for grid in sparsh.flex_force_sensor.values()
    )
    assert sparsh.active_taxels == expected
    assert sparsh.active_taxels > 0


def test_both_sources_agree_on_which_taxels_are_loaded(loaded_readout):
    """contact and sparsh should light up overlapping taxels on the same press."""
    *_, contact, sparsh, _readers = loaded_readout

    contact_active = set(np.flatnonzero(np.abs(contact.flat[:, 2]) > 1e-6))
    sparsh_active = set(np.flatnonzero(sparsh.flat[:, 2] > ACTIVITY_THRESHOLD))
    assert contact_active, "contact sensor reported nothing"
    assert sparsh_active, "sparsh sensor reported nothing"

    overlap = contact_active & sparsh_active
    assert overlap, (
        f"contact lit {sorted(contact_active)[:8]}... and sparsh lit "
        f"{sorted(sparsh_active)[:8]}... with no taxel in common"
    )


def test_readouts_are_flat_368_by_3(loaded_readout):
    *_, contact, sparsh, _readers = loaded_readout
    assert contact.flat.shape == (TAXEL_COUNT, 3)
    assert sparsh.flat.shape == (TAXEL_COUNT, 3)


@pytest.mark.parametrize(
    "mode,expected_contact,expected_sparsh",
    [("contact", True, False), ("sparsh", False, True), ("both", True, True)],
)
def test_mode_switches(mode, expected_contact, expected_sparsh):
    assert mode in SENSOR_MODES
    assert contact_enabled(mode) is expected_contact
    assert sparsh_enabled(mode) is expected_sparsh


def test_heatmap_source_resolution_and_errors():
    assert resolve_heatmap_sources("both", "both") == ["contact", "sparsh"]
    assert resolve_heatmap_sources("both", "primary") == ["contact"]
    assert resolve_heatmap_sources("sparsh", "primary") == ["sparsh"]
    assert resolve_heatmap_sources("contact", "contact") == ["contact"]

    with pytest.raises(ValueError, match="Unknown heatmap source"):
        resolve_heatmap_sources("both", "nonsense")
    with pytest.raises(ValueError, match="requires contact or both"):
        resolve_heatmap_sources("sparsh", "contact")
    with pytest.raises(ValueError, match="requires sparsh or both"):
        resolve_heatmap_sources("contact", "sparsh")


def test_primary_source_prefers_contact_in_both_mode():
    assert primary_source("both") == "contact"


def test_make_sparsh_config_falls_back_to_defaults():
    """An argparse Namespace missing every sparsh flag must still build."""
    from argparse import Namespace

    config = make_sparsh_config(Namespace())
    reference = default_sparsh_config(0.005, 0.01, 0.05, None, None)
    assert config == reference


def test_make_sparsh_config_stringifies_calibration_path(tmp_path):
    from argparse import Namespace

    path = tmp_path / "calibration.json"
    config = make_sparsh_config(Namespace(sparsh_calibration=path))
    assert config.calibration_path == str(path)


def test_contact_reader_requires_named_geoms(leapxela_hand_with_object):
    """An empty geom list filters every contact out -- there is no 'all' sentinel.

    Upstream accepts contact_geom_names=None to mean "any contact"; the port
    dropped that, so passing [] silently yields zeros rather than everything.
    """
    model, skins, tips, geom_names = leapxela_hand_with_object
    data = mj.MjData(model)
    for _ in range(260):
        mj.mj_step(model, data)

    named, count_named = flex_vertex_contact_forces(
        model, data, "flex_uspa46_1", geom_names
    )
    empty, count_empty = flex_vertex_contact_forces(model, data, "flex_uspa46_1", [])
    assert count_empty == 0
    np.testing.assert_array_equal(empty, np.zeros_like(empty))
    assert count_named >= count_empty
