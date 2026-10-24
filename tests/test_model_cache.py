"""The hand model is compiled once per distinct configuration, not per rollout.

Collection used to rebuild the whole hand for every attempt -- ~177 rebuilds in a
default run, all but a handful identical. The model is a pure function of
(specs, palm pitch, adhesion, gap), so it is memoised.

The cache is only sound while every consumer treats the model, skins, tips and
layout as read-only, because they are now shared by every subsequent episode in
the process. `test_cached_model_does_not_leak_between_episodes` is the test that
would actually catch a violation; the rest guard the mechanics.
"""

import mujoco as mj
import numpy as np
import pytest

from leapxela.episode import (
    MODEL_CACHE_SIZE,
    ObjectSpec,
    _build_model_cached,
    _hand_layout_cached,
    build_model,
    clear_model_cache,
    hand_layout,
    object_mass,
)

# Within the per-pad size cap for a single object, so run_episode accepts it.
BOX = [ObjectSpec("box", 0.7, object_mass(0.7, 0.0))]


@pytest.fixture(autouse=True)
def _isolate_cache():
    """Every test starts and ends with an empty cache."""
    clear_model_cache()
    yield
    clear_model_cache()


def test_identical_specs_reuse_one_compiled_model():
    first = build_model(BOX, 0.0, 0.0, 0.010)
    second = build_model(BOX, 0.0, 0.0, 0.010)
    # Same objects, not merely equal: this is what makes the rebuild disappear.
    assert first[0] is second[0]
    assert first[1] is second[1]
    assert first[2] is second[2]
    assert _build_model_cached.cache_info().hits >= 1


def test_a_list_and_its_tuple_hit_the_same_entry():
    """build_model takes a list; the key is the tuple of it."""
    spec = BOX[0]
    from_list = build_model(list(BOX), 0.0, 0.0, 0.010)
    # An equal-but-distinct spec must hit the same entry: ObjectSpec is frozen,
    # so the key is by value, not identity.
    from_copy = build_model(
        [ObjectSpec(spec.shape, spec.scale, spec.mass)], 0.0, 0.0, 0.010
    )
    assert from_list[0] is from_copy[0]


@pytest.mark.parametrize(
    "specs,pitch,adhesion,gap",
    [
        ([ObjectSpec("box", 1.0, 0.8)], 0.0, 0.0, 0.010),
        ([ObjectSpec("sphere", 1.0, 0.8)], 0.0, 0.0, 0.010),   # shape
        ([ObjectSpec("box", 0.5, 0.8)], 0.0, 0.0, 0.010),      # scale
        ([ObjectSpec("box", 1.0, 0.4)], 0.0, 0.0, 0.010),      # mass
        ([ObjectSpec("box", 1.0, 0.8)] * 2, 0.0, 0.0, 0.010),  # count
        ([ObjectSpec("box", 1.0, 0.8)], 5.0, 0.0, 0.010),      # palm pitch
        ([ObjectSpec("box", 1.0, 0.8)], 0.0, 0.5, 0.010),      # adhesion
        ([ObjectSpec("box", 1.0, 0.8)], 0.0, 0.5, 0.020),      # gap
    ],
)
def test_every_key_field_produces_a_distinct_model(specs, pitch, adhesion, gap):
    """Anything that changes the compiled hand must miss the cache."""
    reference = build_model([ObjectSpec("box", 1.0, 0.8)], 0.0, 0.0, 0.010)
    candidate = build_model(specs, pitch, adhesion, gap)
    is_reference_config = (
        [(o.shape, o.scale, o.mass) for o in specs] == [("box", 1.0, 0.8)]
        and (pitch, adhesion, gap) == (0.0, 0.0, 0.010)
    )
    assert (candidate[0] is reference[0]) == is_reference_config


def test_cache_stays_bounded():
    """A compiled hand is ~49 MB, so an unbounded cache would exhaust memory."""
    for scale in (0.4, 0.5, 0.6, 0.7, 0.8):
        build_model([ObjectSpec("box", scale, 0.8)], 0.0, 0.0, 0.010)
        assert _build_model_cached.cache_info().currsize <= MODEL_CACHE_SIZE
    assert _build_model_cached.cache_info().currsize == MODEL_CACHE_SIZE


def test_layout_is_cached_on_the_same_key():
    first = hand_layout(BOX, 0.0, 0.0, 0.010)
    second = hand_layout(BOX, 0.0, 0.0, 0.010)
    assert first is second
    assert _hand_layout_cached.cache_info().currsize <= MODEL_CACHE_SIZE
    # Different hand -> different layout.
    other = hand_layout([ObjectSpec("sphere", 1.0, 0.8)], 0.0, 0.0, 0.010)
    assert other is not first


def test_stepping_does_not_mutate_the_shared_model():
    """A cached model is reused by later episodes, so stepping must not touch it.

    qpos0 is the one most likely to drift: place_objects writes the object pose,
    and if it ever wrote to the model instead of the data the next episode would
    silently start from a different pose.
    """
    model, _skins, _tips = build_model(BOX, 0.0, 0.0, 0.010)
    qpos0 = model.qpos0.copy()
    timestep = float(model.opt.timestep)
    iterations = int(model.opt.iterations)

    data = mj.MjData(model)
    for _ in range(200):
        mj.mj_step(model, data)

    np.testing.assert_array_equal(model.qpos0, qpos0)
    assert float(model.opt.timestep) == timestep
    assert int(model.opt.iterations) == iterations


def test_cached_model_does_not_leak_between_episodes(tmp_path):
    """Two episodes from one cached model must match two from fresh models.

    This is the guarantee the cache rests on: if any consumer mutated the shared
    model, skins or tips, the second episode would diverge from the first.
    """
    from types import SimpleNamespace

    from leapxela.episode import (
        PALM_PITCH_DEG,
        PLACEMENT_HEIGHT,
        PLACEMENT_JITTER,
        PREGRIP_FRACTION,
        THUMB_DELAY,
        run_episode,
    )

    def args():
        return SimpleNamespace(
            duration=0.4, sample_hz=100.0, grip_fraction=0.55,
            thumb_grip_fraction=0.35, pregrip_fraction=PREGRIP_FRACTION,
            thumb_delay=THUMB_DELAY, pulse_hz=1.0, pulse_amplitude=0.15,
            shear_amplitude=0.15, squeeze_steps=4, palm_pitch=PALM_PITCH_DEG,
            object_adhesion=0.0, object_adhesion_gap=0.010,
            placement_jitter=PLACEMENT_JITTER, placement_height=PLACEMENT_HEIGHT,
            settle_duration=0.1, orientation_random=True, abort_check_time=0.0,
            seed=0, video=False, orbit_revolutions=1.0, heatmap_channel="normal",
            force_scale=0.5, cloud_view=False, cloud_grid="surface",
            arrow_scale=1.0, sensor_mode="contact", heatmap_source="primary",
            sparsh_stiffness=100.0, sparsh_damping=0.05, sparsh_window=5,
            sparsh_use_qvel=True, sparsh_velocity_smoothing=0.3,
            sparsh_activity_threshold=0.005, sparsh_min_peak_normal=0.01,
            sparsh_min_contact_fraction=0.05, sparsh_deform_scale=0.02,
            sparsh_max_displacement=0.015, sparsh_calibration=None,
        )

    def tactile(out_dir):
        with np.load(out_dir / "sensor_log.npz", allow_pickle=False) as handle:
            return handle["tactile"].copy()

    # Two runs sharing one cached model.
    first_dir, second_dir = tmp_path / "cached_a", tmp_path / "cached_b"
    run_episode(BOX, "pulse", args(), first_dir, np.random.default_rng(0))
    run_episode(BOX, "pulse", args(), second_dir, np.random.default_rng(0))
    assert _build_model_cached.cache_info().hits >= 1

    # One run against a model compiled fresh for the purpose.
    clear_model_cache()
    fresh_dir = tmp_path / "fresh"
    run_episode(BOX, "pulse", args(), fresh_dir, np.random.default_rng(0))

    cached_first, cached_second = tactile(first_dir), tactile(second_dir)
    np.testing.assert_array_equal(cached_first, cached_second)
    np.testing.assert_array_equal(cached_first, tactile(fresh_dir))
