"""Objects must land with most of their footprint over the palm sensor pads.

The palm is three separated 36.2 x 21.7 mm islands. The legacy spawn point is the
midpoint of pads 1 and 2, which is bare palm between them: a single object landed
there covered ~0.3 of its footprint with taxels and by three objects the worst was
often 0.0. Per-pad placement draws a zone -- pads 1 and 2 count as one, seam
included -- and keeps a candidate only if enough of its footprint measures onto a
pad.

Two ways of measuring coverage appear below, deliberately. The tests on the
requirement itself sample the object's volume with an independent sampler and
score the SETTLED result, which is what the size caps are calibrated against.
The zone tests call the placer's own `pad_coverage` at spawn, which is the thing
the placer can actually be held to; settling is physics and moves objects.
"""

import mujoco as mj
import numpy as np
import pytest
from matplotlib.path import Path as MplPath
from scipy.spatial import ConvexHull

from leapxela.episode import (
    MIN_PAD_COVERAGE,
    OBJECT_SHAPES,
    OBJECT_SIZES,
    PALM_FLEX_NAMES,
    PLACEABLE_SHAPES,
    RETIRED_SHAPES,
    ROLLING_SHAPES,
    SETTLE_DURATION,
    SHAPE_MAX_SCALE,
    TETROMINO_BLOCK_HALF,
    TETROMINO_BLOCKS,
    ZONE_WEIGHTS,
    ObjectSpec,
    _flex_vertices,
    apply_pregrip,
    build_model,
    check_placement_feasible,
    control_targets,
    flat_orientation,
    footprint_points,
    footprint_rectangles,
    is_tetromino,
    max_scale_for,
    object_body_name,
    object_geom_names,
    object_mass,
    pad_coverage,
    pad_regions,
    place_objects,
    place_objects_per_pad,
    profile_from_args,
    shape_index,
    tetromino_block_offsets,
)

SAMPLES = 600


class _Profile:
    grip_fraction = 0.55
    thumb_grip_fraction = 0.35
    pregrip_fraction = 0.40
    thumb_delay = 0.5
    pulse_hz = 1.0
    pulse_amplitude = 0.15
    shear_amplitude = 0.15
    squeeze_steps = 4


def _pad_paths(model, data):
    paths = []
    for name in PALM_FLEX_NAMES:
        v = _flex_vertices(model, data, name)[:, :2]
        paths.append(MplPath(v[ConvexHull(v).vertices]))
    return paths


def _sample_volume(shape, scale, rng):
    """Uniform points inside the object, in its body frame."""
    if is_tetromino(shape):
        half = TETROMINO_BLOCK_HALF * scale
        offsets = tetromino_block_offsets(shape, scale)
        pick = rng.integers(0, TETROMINO_BLOCKS, SAMPLES)
        return offsets[pick] + rng.uniform(-half, half, size=(SAMPLES, 3))
    size = np.asarray(OBJECT_SIZES[shape], dtype=np.float64) * scale
    if shape == "box":
        return rng.uniform(-size[:3], size[:3], size=(SAMPLES, 3))
    theta = rng.uniform(0, 2 * np.pi, SAMPLES)
    radius = size[0] * np.sqrt(rng.uniform(0, 1, SAMPLES))
    return np.column_stack([
        radius * np.cos(theta), radius * np.sin(theta),
        rng.uniform(-size[1], size[1], SAMPLES),
    ])


def _place_and_settle(shape, scale, count, seed, mode="per-pad"):
    specs = [ObjectSpec(shape, scale, object_mass(scale, 0.0))] * count
    model, _skins, _tips = build_model(specs, 0.0, 0.0, 0.010)
    data = mj.MjData(model)
    apply_pregrip(model, data, _Profile.pregrip_fraction)
    rng = np.random.default_rng(seed)
    if mode == "per-pad":
        place_objects_per_pad(model, data, specs, rng)
    else:
        place_objects(model, data, specs, 0.012, 0.008, True, rng)
    profile = profile_from_args("hold", _Profile)
    for _ in range(int(SETTLE_DURATION / model.opt.timestep)):
        data.ctrl[:] = control_targets(model, 0.0, profile)
        mj.mj_step(model, data)
    return model, data, specs


def _coverage(model, data, specs, seed):
    paths = _pad_paths(model, data)
    rng = np.random.default_rng(seed + 7717)
    out = []
    for index, spec in enumerate(specs):
        body = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(index))
        pts = _sample_volume(spec.shape, spec.scale, rng)
        pts = pts @ data.xmat[body].reshape(3, 3).T + data.xpos[body]
        inside = np.zeros(len(pts), dtype=bool)
        for path in paths:
            inside |= path.contains_points(pts[:, :2])
        out.append(float(inside.mean()))
    return out


# --------------------------------------------------------------------------
# the requirement itself
# --------------------------------------------------------------------------
def _spawn_height_spread_mm(model, data, specs):
    zs = [
        data.xpos[mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(i))][2]
        for i in range(len(specs))
    ]
    return (max(zs) - min(zs)) * 1000.0


@pytest.mark.parametrize("shape", PLACEABLE_SHAPES)
@pytest.mark.parametrize("count", [1, 2, 3])
def test_every_object_sits_majority_on_a_pad(shape, count):
    """At its capped size, every object keeps >50% of its volume over taxels.

    Covers every placeable shape, not the five it used to. That gap is how the
    long tetrominoes kept a cap of 1.00 at one object: nothing ever checked
    them, and an I at 1.00 is about 48 mm long against a 36.2 mm pad.
    """
    scale = max_scale_for(shape, count)
    for seed in range(3):
        model, data, specs = _place_and_settle(shape, scale, count, seed)
        covers = _coverage(model, data, specs, seed)
        assert min(covers) > 0.5, (
            f"{shape} x{count} at scale {scale} seed {seed}: "
            f"coverage {[round(c, 3) for c in covers]}"
        )


@pytest.mark.parametrize("shape", ["box", "disk", "cylinder"])
@pytest.mark.parametrize("count", [2, 3])
def test_capped_sizes_are_placed_side_by_side_not_stacked(shape, count):
    """A stacked object projects onto the pad while touching nothing.

    Coverage cannot see it -- the upper object still scores full marks -- but
    objects_sensed falls short of the count. The caps exist to keep every object
    on the palm, so this checks the spawn heights agree.
    """
    scale = max_scale_for(shape, count)
    for seed in range(3):
        model, data, specs = _place_and_settle(shape, scale, count, seed)
        spread = _spawn_height_spread_mm(model, data, specs)
        assert spread < 15.0, (
            f"{shape} x{count} at its cap {scale} stacked: spawn heights span "
            f"{spread:.1f} mm"
        )


def test_per_pad_beats_legacy_on_the_hardest_case():
    """Three objects is where legacy placement collapses; this pins the gain."""
    shape, count = "box", 3
    scale = max_scale_for(shape, count)
    per_pad, legacy = [], []
    for seed in range(3):
        model, data, specs = _place_and_settle(shape, scale, count, seed)
        per_pad.extend(_coverage(model, data, specs, seed))
        model, data, specs = _place_and_settle(shape, scale, count, seed, "legacy")
        legacy.extend(_coverage(model, data, specs, seed))
    assert min(per_pad) > 0.5
    assert np.mean(per_pad) > np.mean(legacy) + 0.2


# --------------------------------------------------------------------------
# flat, and only spun about the pad normal
# --------------------------------------------------------------------------
@pytest.mark.parametrize("shape", PLACEABLE_SHAPES)
def test_objects_are_placed_flat(shape):
    """Tumbling stood boxes on edge and dropped cylinders across the pad seam.

    Flat means the object's own 'up' after orientation is world +z (or -z: a box
    resting on the opposite face is equally flat).
    """
    scale = min(0.4, max_scale_for(shape, 1) or 0.4)
    model, data, _specs = _place_and_settle(shape, scale, 1, 0)
    body = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(0))
    rotation = data.xmat[body].reshape(3, 3)
    # After settling, some axis of the body must still be near world up.
    alignment = np.abs(rotation[2, :]).max()
    assert alignment > np.cos(np.deg2rad(25.0)), (
        f"{shape} is not resting flat: best axis alignment {alignment:.3f}"
    )


def test_flat_orientation_is_yaw_only():
    """The generator itself must only spin about +z, before any settling."""
    for shape in PLACEABLE_SHAPES:
        for yaw in (0.0, 1.0, 2.5, 5.0):
            quat = flat_orientation(shape, yaw)
            rot = np.zeros(9)
            mj.mju_quat2Mat(rot, quat)
            rot = rot.reshape(3, 3)
            assert np.abs(rot[2, :]).max() > 0.999, (
                f"{shape} at yaw {yaw} is not flat: {rot[2, :]}"
            )


# --------------------------------------------------------------------------
# zone weighting
# --------------------------------------------------------------------------
# Placement used to draw a PAD and jitter the object inside it, which made every
# count-3 episode come out as exactly one object per pad: the jitter bound left
# an object at cap size a millimetre of play, and the bounding-sphere overlap
# test demanded 30 mm of clearance for a 17.6 mm box, so two objects could never
# share a pad. The tests below are the ones that fail on that design.
def _placed(shape, scale, count, seeds, **kwargs):
    """Per-seed, per-object pad coverage: (seeds, count, 3)."""
    specs = [ObjectSpec(shape, scale, object_mass(scale, 0.0))] * count
    model, _skins, _tips = build_model(specs, 0.0, 0.0, 0.010)
    data = mj.MjData(model)
    apply_pregrip(model, data, _Profile.pregrip_fraction)
    regions = pad_regions(model, data)

    out = []
    for seed in range(seeds):
        place_objects_per_pad(
            model, data, specs, np.random.default_rng(seed), **kwargs
        )
        episode = []
        for index, item in enumerate(specs):
            body = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(index))
            geom_ids = [
                mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
                for name in object_geom_names(index, item.shape)
            ]
            cloud = footprint_points(
                model, geom_ids, data.xmat[body].reshape(3, 3)
            ) + data.xpos[body][:2]
            episode.append(pad_coverage(cloud, regions))
        out.append(episode)
    return np.array(out)


def _shared_fraction(covers):
    """Episodes where two objects claim the same pad."""
    return np.mean([len(set(row.tolist())) < len(row) for row in covers.argmax(axis=2)])


def test_objects_share_a_pad_below_the_cap_and_need_one_each_at_it():
    """Sharing is a function of size, and the cap is the size where it stops.

    This is the behaviour the screenshot was missing, and it comes back as soon
    as objects are small enough to fit two to a pad -- the old code could not
    share at ANY collectable size, because bounding-sphere separation demanded
    30 mm of clearance for a 17.6 mm box.

    Both ends are pinned deliberately. `scale: max` sizes objects so that three
    of them fill the pads, which leaves no room to share; the variety this test
    is about needs a size below the cap. README records the trade-off.
    """
    cap = max_scale_for("T", 3)
    roomy = _shared_fraction(_placed("T", round(cap * 0.5, 2), 3, 60))
    at_cap = _shared_fraction(_placed("T", cap, 3, 60))
    assert roomy > 0.20, f"only {roomy:.0%} of episodes shared a pad at half cap"
    assert at_cap < roomy, (
        f"sharing did not fall with size: {roomy:.0%} at half cap, {at_cap:.0%} at cap"
    )


def test_an_object_can_bridge_the_seam_between_pads_one_and_two():
    """An object wide enough to span the 11.6 mm seam sometimes does.

    Impossible under pad-confined jitter at any size, because the object centre
    could never leave a pad. It needs width: to keep half its footprint on taxel
    while centred over the seam an object must be at least twice the seam wide,
    about 23 mm, so this is the one behaviour that wants a LARGE object and shows
    up at the cap rather than below it.
    """
    covers = _placed("T", max_scale_for("T", 3), 3, 80)
    on_both = (covers[:, :, 0] > 0.05) & (covers[:, :, 1] > 0.05)
    assert on_both.any(axis=1).mean() > 0.02, (
        f"only {on_both.any(axis=1).mean():.0%} of episodes bridged the seam"
    )


def test_pad_three_is_often_left_empty():
    """The point of weighting the fingerward strip: whole episodes skip pad 3.

    Sized below the cap for the same reason as the sharing test: three
    cap-sized objects need all three pads, so none can be spared.
    """
    covers = _placed("T", round(max_scale_for("T", 3) * 0.5, 2), 3, 60)
    empty = covers[:, :, 2].max(axis=1) < 0.05
    assert empty.mean() > 0.05, f"pad 3 was used in every episode but {empty.sum()}"
    assert empty.mean() < 0.95, "pad 3 is never used at all"


def test_zone_share_tracks_the_weights():
    """A single object lands in the fingerward strip about ZONE_WEIGHTS[0] of the time."""
    covers = _placed("disk", 0.5, 1, 60)[:, 0, :]
    fingerward = (covers[:, 0] + covers[:, 1]) > covers[:, 2]
    np.testing.assert_allclose(
        [fingerward.mean(), 1.0 - fingerward.mean()], ZONE_WEIGHTS, atol=0.15
    )


def test_zone_weights_are_honoured():
    """Driving the weights to one zone must actually confine placement to it."""
    wrist_only = _placed("disk", 0.5, 1, 20, zone_weights=(0.0, 1.0))[:, 0, :]
    assert (wrist_only[:, 2] > 0.5).all(), "objects landed off the wrist pad"

    fingerward_only = _placed("disk", 0.5, 1, 20, zone_weights=(1.0, 0.0))[:, 0, :]
    assert (fingerward_only[:, 2] < 0.05).all(), "objects landed on the wrist pad"


@pytest.mark.parametrize("weights", [(0.4, 0.4, 0.2), (-1.0, 1.0), (0.0, 0.0)])
def test_bad_zone_weights_are_refused(weights):
    """Three weights is the old per-pad shape and would silently mis-normalise."""
    specs = [ObjectSpec("box", 0.4, object_mass(0.4, 0.0))]
    model, _skins, _tips = build_model(specs, 0.0, 0.0, 0.010)
    data = mj.MjData(model)
    apply_pregrip(model, data, _Profile.pregrip_fraction)
    with pytest.raises(ValueError, match="zone_weights"):
        place_objects_per_pad(
            model, data, specs, np.random.default_rng(0), zone_weights=weights
        )


@pytest.mark.parametrize("shape", ["box", "disk", "cylinder", "T", "O"])
@pytest.mark.parametrize("count", [1, 2, 3])
def test_placed_objects_meet_the_coverage_floor(shape, count):
    """The standing requirement, now asserted against the placer's own measure.

    `test_every_object_sits_majority_on_a_pad` checks the same thing after
    settling with an independent volume sampler; this checks it at spawn, which
    is where the placer can actually be held to it.
    """
    covers = _placed(shape, max_scale_for(shape, count), count, 20)
    worst = covers.sum(axis=2).min()
    assert worst >= MIN_PAD_COVERAGE - 1e-9, (
        f"{shape} x{count} at its cap covered only {worst:.2f} of a footprint"
    )


@pytest.mark.parametrize("shape", ["box", "disk", "T"])
def test_objects_do_not_spawn_inside_one_another(shape):
    """The guarantee the bounding-sphere test used to provide, kept by footprints."""
    count = 3
    scale = max_scale_for(shape, count)
    specs = [ObjectSpec(shape, scale, object_mass(scale, 0.0))] * count
    model, _skins, _tips = build_model(specs, 0.0, 0.0, 0.010)
    data = mj.MjData(model)
    apply_pregrip(model, data, _Profile.pregrip_fraction)
    object_geoms = {
        mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
        for index, item in enumerate(specs)
        for name in object_geom_names(index, item.shape)
    }
    for seed in range(20):
        place_objects_per_pad(model, data, specs, np.random.default_rng(seed))
        for index in range(data.ncon):
            contact = data.contact[index]
            both = contact.geom1 in object_geoms and contact.geom2 in object_geoms
            assert not (both and contact.dist < -1e-6), (
                f"{shape} seed {seed}: objects overlap by "
                f"{-contact.dist * 1000:.2f} mm at spawn"
            )


def test_rolling_shapes_stay_confined_to_one_pad():
    """The cylinder is exempt from free placement because it rolls.

    Free placement regressed it: coverage says how much of a footprint is on
    taxel, not how near an edge it sits, so a cylinder accepted at 95% coverage
    beside the seam rolls into it. Measured across coverage floors up to 0.95 it
    settled at 0.00-0.17, so no threshold fixes it -- it has to be held near a
    pad centre, as it was before.
    """
    assert "cylinder" in ROLLING_SHAPES
    covers = _placed("cylinder", max_scale_for("cylinder", 1), 1, 30)[:, 0, :]
    # Confined means the footprint touches ONE pad. It does not mean the pad
    # holds all of it: the cylinder is 36 mm long against a 21.7 mm pad width,
    # so a crosswise one overhangs however well it is centred.
    touched = (covers > 0.01).sum(axis=1)
    assert (touched == 1).all(), (
        f"a cylinder reached more than one pad: pads touched {sorted(set(touched))}"
    )
    # The fingerward bias still applies, split across the two pads it covers.
    assert (covers[:, :2].sum(axis=1) > covers[:, 2]).mean() > 0.5


def test_free_shapes_are_not_confined_to_one_pad():
    """The counterpart: a non-rolling shape does leave the single-pad regime."""
    covers = _placed("disk", 0.5, 3, 40)
    assert (covers.max(axis=2) < 0.95).any(), (
        "every disk sat wholly within one pad -- free placement is not in effect"
    )


# --------------------------------------------------------------------------
# footprint geometry
# --------------------------------------------------------------------------
def test_footprint_points_follow_the_tetromino_outline_not_its_box():
    """A T covers four of the six cells of its bounding box, and no more.

    The overlap test is only as tight as this: if the footprint fell back to a
    bounding box, two tetrominoes could not nest and sharing would regress.
    """
    scale = 0.4
    specs = [ObjectSpec("T", scale, object_mass(scale, 0.0))]
    model, _skins, _tips = build_model(specs, 0.0, 0.0, 0.010)
    geom_ids = [
        mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
        for name in object_geom_names(0, "T")
    ]
    cloud = footprint_points(model, geom_ids, np.eye(3))

    # A T fills 4 of the 6 cells of its 3x2 bounding box. Asked cell by cell --
    # is any sampled point near this cell's centre? -- rather than by binning the
    # cloud, because lattice points land exactly on cell boundaries.
    cell = 2.0 * TETROMINO_BLOCK_HALF * scale
    low, high = cloud.min(axis=0), cloud.max(axis=0)
    span = (high - low) / cell
    assert np.allclose(np.round(span), [3, 2]), f"T box is not 3x2 cells: {span}"

    covered = 0
    for column in range(3):
        for row in range(2):
            centre = low + cell * np.array([column + 0.5, row + 0.5])
            covered += np.min(np.linalg.norm(cloud - centre, axis=1)) < cell / 4.0
    assert covered == 4, (
        f"T footprint covers {covered} of 6 cells, expected 4 -- the outline was "
        "lost and the bounding box used instead"
    )


def test_footprint_rectangles_need_a_flat_object():
    """A tumbled object has no well-defined footprint rectangle; say so loudly."""
    specs = [ObjectSpec("box", 0.4, object_mass(0.4, 0.0))]
    model, _skins, _tips = build_model(specs, 0.0, 0.0, 0.010)
    geom_ids = [mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, object_geom_names(0, "box")[0])]
    tilted = np.zeros(9)
    mj.mju_quat2Mat(tilted, flat_orientation("box", 0.0))
    tilted = tilted.reshape(3, 3)
    footprint_rectangles(model, geom_ids, tilted)      # flat: fine

    corner = np.zeros(4)
    mj.mju_axisAngle2Quat(corner, np.array([1.0, 1.0, 0.0]) / np.sqrt(2), 0.9)
    rotation = np.zeros(9)
    mj.mju_quat2Mat(rotation, corner)
    with pytest.raises(ValueError, match="flat object"):
        footprint_rectangles(model, geom_ids, rotation.reshape(3, 3))


# --------------------------------------------------------------------------
# size caps and the retired sphere
# --------------------------------------------------------------------------
def test_over_cap_combination_is_refused_with_the_ceiling_named():
    cap = max_scale_for("box", 3)
    with pytest.raises(ValueError, match=f"ceiling for x3 is scale {cap:g}"):
        check_placement_feasible("box", 1.0, 3)
    # The same size is fine with fewer objects -- the cap tightens with count.
    roomier = max_scale_for("box", 1)
    assert roomier > cap
    check_placement_feasible("box", roomier, 1)
    with pytest.raises(ValueError):
        check_placement_feasible("box", roomier, 3)
    for count in (1, 2, 3):
        check_placement_feasible("box", max_scale_for("box", count), count)


def test_sphere_is_retired_but_keeps_its_label_slot():
    """Removing it outright would relabel every dataset already collected."""
    assert "sphere" in RETIRED_SHAPES
    assert "sphere" not in PLACEABLE_SHAPES
    assert shape_index("sphere") == 2
    assert shape_index("box") == 0 and shape_index("cylinder") == 1
    with pytest.raises(ValueError, match="retired"):
        check_placement_feasible("sphere", 0.5, 1)


def test_disk_is_appended_so_existing_indices_are_untouched():
    assert shape_index("disk") == len(OBJECT_SHAPES) - 1
    assert [shape_index(s) for s in ("I", "J", "L", "O", "S", "T", "Z")] == list(range(3, 10))


def test_caps_tighten_with_object_count():
    """Pad 3 is 33.1 mm from pad 1, so bigger objects stop fitting all three."""
    for shape, per_count in SHAPE_MAX_SCALE.items():
        assert shape in PLACEABLE_SHAPES
        caps = [per_count[n] for n in sorted(per_count)]
        assert caps == sorted(caps, reverse=True), f"{shape}: {per_count}"
    # Every placeable shape is capped now that tetrominoes are measured.
    assert set(SHAPE_MAX_SCALE) == set(PLACEABLE_SHAPES)
    # An unknown shape is unconstrained rather than crashing.
    assert max_scale_for("nonesuch", 3) is None
