"""Tetromino objects: non-convex grasp targets for the dense sparsh readout.

Ported from sparsh-skin-sim's `TETRIS_SHAPES`. Unlike every other leapxela
object, a tetromino is one body carrying four box geoms, so the tests here
concentrate on the places that used to assume one geom per object: mass
splitting, placement extents, contact attribution, and adhesion pairing.
"""

import itertools

import mujoco as mj
import numpy as np
import pytest

from leapxela.episode import (
    OBJECT_MASS,
    OBJECT_SHAPES,
    TETROMINO_BLOCK_HALF,
    TETROMINO_BLOCKS,
    TETROMINO_CELLS,
    ObjectSpec,
    body_bounding_radius,
    body_support_extent,
    build_model,
    is_tetromino,
    object_geom_groups,
    object_geom_names,
    object_mass,
    object_size_vector,
    resolve_object_geoms,
    sensed_objects,
    shape_index,
    support_extent,
    tetromino_block_offsets,
    tetromino_half_extent,
)

ALL_TETROMINOES = sorted(TETROMINO_CELLS)


def _geom_ids(model, groups, index):
    return [
        mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name) for name in groups[index]
    ]


def test_shape_index_keeps_primitive_labels_stable():
    """shape_index is a training label written into every npz.

    Re-sorting the registry when tetrominoes were added would have silently
    relabelled every dataset already collected, so this pins the old three.
    """
    assert shape_index("box") == 0
    assert shape_index("cylinder") == 1
    assert shape_index("sphere") == 2
    assert [shape_index(name) for name in ALL_TETROMINOES] == list(range(3, 10))
    # Unique, and never re-ordered: new shapes append, so these indices hold
    # however many shapes get added later.
    assert len(OBJECT_SHAPES) == len(set(OBJECT_SHAPES))
    assert OBJECT_SHAPES[:3] == ("box", "cylinder", "sphere")


@pytest.mark.parametrize("shape", ALL_TETROMINOES)
def test_blocks_are_centred_on_the_piece_com(shape):
    """The free joint acts at the body origin; an off-centre piece would spin up."""
    offsets = tetromino_block_offsets(shape, 1.0)
    assert offsets.shape == (TETROMINO_BLOCKS, 3)
    np.testing.assert_allclose(offsets.mean(axis=0), np.zeros(3), atol=1e-12)
    np.testing.assert_allclose(offsets[:, 2], np.zeros(TETROMINO_BLOCKS))


@pytest.mark.parametrize("shape", ALL_TETROMINOES)
def test_blocks_tile_without_overlap_or_gaps(shape):
    """Adjacent cells must touch exactly, so the piece is one solid body."""
    offsets = tetromino_block_offsets(shape, 1.0)
    pitch = 2.0 * TETROMINO_BLOCK_HALF
    for left, right in itertools.combinations(offsets, 2):
        separation = np.abs(left - right)[:2]
        # Distinct cells on a lattice: at least one axis a whole pitch apart,
        # and never a fractional offset that would interpenetrate.
        assert separation.max() >= pitch - 1e-12
        for axis in separation:
            assert abs(axis / pitch - round(axis / pitch)) < 1e-9


@pytest.mark.parametrize("shape", ALL_TETROMINOES)
@pytest.mark.parametrize("scale", [0.5, 1.0])
def test_block_masses_sum_to_the_piece_mass(shape, scale):
    """MuJoCo's geom mass is per geom, so the piece mass has to be split."""
    expected = object_mass(scale, 0.0)
    model, _skins, _tips = build_model(
        [ObjectSpec(shape, scale, expected)], 0.0, 0.0, 0.0
    )
    body_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, "grasp_object")
    assert float(model.body_mass[body_id]) == pytest.approx(expected, rel=1e-9)
    assert expected == pytest.approx(OBJECT_MASS * scale**3, rel=1e-9)


@pytest.mark.parametrize("shape", ALL_TETROMINOES)
def test_geom_group_is_four_named_blocks(shape):
    names = object_geom_names(0, shape)
    assert len(names) == TETROMINO_BLOCKS
    assert len(set(names)) == TETROMINO_BLOCKS
    assert is_tetromino(shape)
    # Primitives stay single-geom and keep their historic name.
    assert object_geom_names(0, "box") == ["grasp_object_geom"]


def test_bounding_radius_encloses_every_block():
    """place_objects treats a clear bounding sphere as proof a slot is free.

    Under-estimating here is what spawns objects inside one another, so the
    body radius must dominate every block's own reach from the body origin.
    """
    specs = [ObjectSpec("I", 1.0, object_mass(1.0, 0.0))]
    model, _skins, _tips = build_model(specs, 0.0, 0.0, 0.0)
    groups = object_geom_groups(specs)
    ids = _geom_ids(model, groups, 0)

    radius = body_bounding_radius(model, ids)
    for geom_id in ids:
        corner = float(np.linalg.norm(model.geom_size[geom_id][:3]))
        reach = float(np.linalg.norm(model.geom_pos[geom_id])) + corner
        assert radius >= reach - 1e-12

    # An I piece is 4 blocks long: its radius must exceed a single block's.
    assert radius > np.linalg.norm(model.geom_size[ids[0]][:3])


def test_support_extent_tracks_orientation():
    """A piece stood on end reaches further below its origin than one laid flat.

    This is the number place_objects lifts the body by, so getting it wrong
    either buries the object in the palm or drops it from a height.
    """
    specs = [ObjectSpec("I", 1.0, object_mass(1.0, 0.0))]
    model, _skins, _tips = build_model(specs, 0.0, 0.0, 0.0)
    ids = _geom_ids(model, object_geom_groups(specs), 0)

    # Laid flat the piece is one block thick, so it reaches exactly one half down.
    flat = body_support_extent(model, ids, np.eye(3))
    assert flat == pytest.approx(TETROMINO_BLOCK_HALF, rel=1e-9)

    # Stood on end: the long (local x) axis maps onto world up, so the lowest
    # block's centre offset adds to the reach.
    on_end_rotation = np.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0]])
    on_end = body_support_extent(model, ids, on_end_rotation)
    offsets = tetromino_block_offsets("I", 1.0)
    furthest = float(np.abs(offsets[:, 0]).max())
    assert on_end == pytest.approx(TETROMINO_BLOCK_HALF + furthest, rel=1e-9)
    assert on_end > flat

    # A single-geom object sits on its own body origin, so the body-level
    # reduction must agree exactly with the per-geom function.
    box_specs = [ObjectSpec("box", 1.0, object_mass(1.0, 0.0))]
    box_model, _s, _t = build_model(box_specs, 0.0, 0.0, 0.0)
    box_ids = _geom_ids(box_model, object_geom_groups(box_specs), 0)
    assert body_support_extent(box_model, box_ids, np.eye(3)) == pytest.approx(
        support_extent(box_model, box_ids[0], np.eye(3)), rel=1e-12
    )


@pytest.mark.parametrize("shape", ALL_TETROMINOES)
def test_object_size_vector_is_the_piece_half_extent(shape):
    """npz `object_sizes` stays (N, 3) and meaningful for pieces with no geom size."""
    size = object_size_vector(shape, 1.0)
    assert size.shape == (3,)
    np.testing.assert_allclose(size, tetromino_half_extent(shape, 1.0))
    assert size[2] == pytest.approx(TETROMINO_BLOCK_HALF)
    # Every block centre lies inside the reported extent.
    offsets = tetromino_block_offsets(shape, 1.0)
    assert np.all(np.abs(offsets) <= size + 1e-12)
    # Primitives are unaffected.
    np.testing.assert_allclose(object_size_vector("box", 1.0), [0.022, 0.022, 0.022])


def test_scale_multiplies_the_whole_piece():
    half_scale = object_size_vector("T", 0.5)
    full_scale = object_size_vector("T", 1.0)
    np.testing.assert_allclose(half_scale * 2.0, full_scale, rtol=1e-12)


def test_adhesion_pairs_the_cross_product_and_never_self_pairs():
    """Two tetrominoes stick together through all 16 block combinations."""
    both = [ObjectSpec("T", 1.0, 0.8), ObjectSpec("L", 1.0, 0.8)]
    model, _skins, _tips = build_model(both, 0.0, 0.5, 0.010)
    assert model.npair == TETROMINO_BLOCKS * TETROMINO_BLOCKS

    mixed = [ObjectSpec("T", 1.0, 0.8), ObjectSpec("box", 1.0, 0.8),
             ObjectSpec("sphere", 1.0, 0.8)]
    model_mixed, _s, _t = build_model(mixed, 0.0, 0.5, 0.010)
    # T-box 4, T-sphere 4, box-sphere 1.
    assert model_mixed.npair == 9

    # No pair may join a body to itself.
    groups = object_geom_groups(both)
    ids, owners = resolve_object_geoms(model, groups)
    owner_of = dict(zip(ids.tolist(), owners.tolist()))
    for pair in range(model.npair):
        left = int(model.pair_geom1[pair])
        right = int(model.pair_geom2[pair])
        assert owner_of[left] != owner_of[right]


def test_sensed_objects_counts_a_multi_geom_object_once():
    """Any one of a tetromino's four blocks touching a pad marks the piece sensed.

    The pre-tetromino code index-aligned geoms to objects, which would have made
    a four-geom object read as four objects.
    """
    specs = [ObjectSpec("T", 1.0, 0.8), ObjectSpec("box", 1.0, 0.8)]
    model, _skins, _tips = build_model(specs, 0.0, 0.0, 0.0)
    groups = object_geom_groups(specs)
    ids, owners = resolve_object_geoms(model, groups)

    assert ids.shape == (TETROMINO_BLOCKS + 1,)
    np.testing.assert_array_equal(owners, [0, 0, 0, 0, 1])

    # No contacts at all -> nothing sensed, and the result is per object.
    data = mj.MjData(model)
    mj.mj_forward(model, data)
    sensed = sensed_objects(data, ids, owners)
    assert sensed.shape == (len(specs),)
    assert not sensed.any()
