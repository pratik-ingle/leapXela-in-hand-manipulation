"""Grasp test for the flex taxel sensors.

Places an object on the palm-up hand, closes the fingers, then pulse-squeezes
while recording all 368 taxels in hardware taxel-ID order. Saves an npz sensor
log, 3-channel hand-heatmap snapshots, and an orbiting MP4 render with the live
heatmap drawn on the hand and as a palm-view panel.
"""

import argparse
import hashlib
import itertools
import zlib
import json
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import mediapy
import mujoco as mj
import numpy as np

from leapxela.hand_builder import (
    FINGERTIP_POSE_JSON,
    GEOM_TO_PATCH,
    HAND_WORKSPACE,
    MODEL_VARIANT,
    REST_SETTLE_DURATION,
    SENSOR_DEFINITIONS,
    SOLVER_ITERATIONS,
    SOLVER_TOLERANCE,
    TIMESTEP,
    TAXEL_COUNT,
    TIP_FINGERS,
    TIP_GRID_ROWCOL,
    add_flex_sensor,
    add_tip_flex,
    build_hand_layout,
    load_base_model,
    save_hand_heatmap,
    tip_canvas,
    tip_surface_offsets,
    trim_pad_boxes,
    _flex_vertices,
    _vertex_displacements
)
from leapxela.fk_taxel import (
    HAND_SS_URDF,
    TAXEL_MAP_JSON,
    compute_fk_taxels,
    fk_order_to_taxel_id,
)
from leapxela.flex_force import (
    DEFAULT_FLEX_DAMPING,
    DEFAULT_FLEX_STIFFNESS,
    DEFAULT_FORCE_WINDOW,
    DEFAULT_VELOCITY_SMOOTHING,
)
from leapxela.paths import data_dir
from leapxela.sensors import (
    MODEL_SCHEMA_VERSION,
    SENSOR_MODES,
    build_contact_readers,
    build_sparsh_readers,
    contact_enabled,
    make_sparsh_config,
    primary_source,
    read_contact_data,
    read_sparsh,
    to_body_frame,
    resolve_heatmap_sources,
    sparsh_enabled,
)
from leapxela.taxel_layout import build_layout
from leapxela.visualizer import (
    CHANNELS,
    CLOUD_MARKER_RADIUS,
    MARKER_RADIUS,
    SPARSH_MARKER_RADIUS,
    TaxelPanel,
    bare_scene_option,
    channel_values,
    dim_flex_skins,
    draw_sparsh_arrows,
    draw_taxel_arrows,
    draw_taxel_markers,
    marker_colours,
    panel_taxel_ids,
    paste_panel,
    sparsh_force_colours,
)


OBJECT_BODY_NAME = "grasp_object"
OBJECT_GEOM_NAME = "grasp_object_geom"
# Multi-object placement. Objects must start low: a 30 mm per-object stagger
# dropped N=5 from ~120 mm and lost half of them.
PLACEMENT_JITTER = 0.012
PLACEMENT_HEIGHT = 0.008
SETTLE_DURATION = 0.5
PLACEMENT_ATTEMPTS = 40
MULTI_SHAPES = ("box", "cylinder", "disk")
MULTI_SCALE_RANGE = (0.45, 0.80)
# Distinct colours so objects can be told apart in the video.
OBJECT_COLOURS = (
    [0.15, 0.35, 0.90, 1.0], [0.90, 0.45, 0.10, 1.0],
    [0.20, 0.75, 0.35, 1.0], [0.80, 0.20, 0.60, 1.0],
    [0.95, 0.85, 0.20, 1.0],
)
OBJECT_MASS = 0.8
# (slide, spin, roll) on the object geoms. Shared with the object-object contact
# pairs below: a <pair> ignores the geoms' friction and falls back to its own
# default of slide 1.0, so writing it in one place is what keeps adhesion the
# only thing those pairs change.
OBJECT_FRICTION = (0.8, 0.005, 0.0001)
# Default reach of object-object adhesion. This has to span the gap objects are
# PLACED at, not just the contact tolerance: at 2 mm the objects never touch each
# other and adhesion does literally nothing (3 spheres measured identical to
# adhesion off, 1/3 held and 0/3 sensed). At 10 mm the same case goes to 3/3 held
# and 3/3 sensed. 25 mm over-clumps -- 5 boxes drop from 4/5 sensed to 3/5 -- so
# the useful range is bounded on both sides.
OBJECT_ADHESION_GAP = 0.010
# pair/adhesion landed in MuJoCo 3.11.0 (2026-07-27). 3.10 silently lacks the
# attribute -- spec.add_pair() has no `adhesion` field at all -- so without this
# check the flag would appear to work and do nothing.
ADHESION_MIN_MUJOCO = (3, 11)
# Share of post-close frames an object must be touching a membrane to count
# toward objects_sensed.
SENSED_FRACTION = 0.5
OBJECT_SIZES = {
    "sphere": [0.028, 0.0, 0.0],
    "box": [0.022, 0.022, 0.022],
    "cylinder": [0.02, 0.045, 0.0],
    # A flat cylinder resting on its circular face. Measured the most
    # pad-friendly primitive: at r=22 mm it still keeps every one of three
    # objects majority-on-pad, where the sphere fails outright.
    "disk": [0.022, 0.005, 0.0],
}
OBJECT_GEOM_TYPES = {
    "sphere": mj.mjtGeom.mjGEOM_SPHERE,
    "box": mj.mjtGeom.mjGEOM_BOX,
    "cylinder": mj.mjtGeom.mjGEOM_CYLINDER,
    "disk": mj.mjtGeom.mjGEOM_CYLINDER,
}
# The sphere is retired: on a palm of three separated pads it sits in unstable
# equilibrium and rolls into the unsensed gap. Measured over a short grasp, every
# sphere configuration reported held>0 but objects_sensed=0 -- held, never felt.
# It stays in the registry so `shape_index` 2 keeps its meaning in datasets
# already collected; it is simply not offered by default and is rejected by
# per-pad placement.
RETIRED_SHAPES = ("sphere",)
# Tetrominoes, ported from sparsh-skin-sim's util/objects_util.py. Unlike the
# primitives above these are non-convex, so a grasp lands on several disjoint
# taxel patches instead of one contiguous patch -- which is the point of
# collecting them against a dense (sparsh) readout.
#
# Each entry is the piece's four unit cells on a square lattice; the geometry is
# built from them in tetromino_block_offsets().
TETROMINO_CELLS = {
    "I": ((0, 0), (1, 0), (2, 0), (3, 0)),
    "O": ((0, 0), (1, 0), (0, 1), (1, 1)),
    "T": ((0, 0), (1, 0), (2, 0), (1, 1)),
    "L": ((0, 0), (0, 1), (0, 2), (1, 2)),
    "J": ((1, 0), (1, 1), (1, 2), (0, 2)),
    "S": ((1, 0), (2, 0), (0, 1), (1, 1)),
    "Z": ((0, 0), (1, 0), (1, 1), (2, 1)),
}
TETROMINO_BLOCKS = 4
# Half-edge of one block at scale 1. Upstream uses 0.012, which makes a scale-1
# T piece 72x48 mm against the 44 mm box here -- too big for this palm before
# calibration has a chance to shrink it. At 0.008 an I piece spans 64 mm, in the
# same range as the primitives, and --scale still tunes it from there.
TETROMINO_BLOCK_HALF = 0.008
# shape_index is written into every npz as a training label, so this order is
# APPEND-ONLY and spelled out rather than derived. Deriving it from
# sorted(OBJECT_SIZES) broke the moment `disk` was added -- it sorts between
# cylinder and sphere and would have shifted sphere from 2 to 3, silently
# relabelling every dataset already collected. New shapes go on the end.
OBJECT_SHAPES = (
    "box",        # 0
    "cylinder",   # 1
    "sphere",     # 2  retired, slot kept so old labels stay valid
    "I",          # 3
    "J",          # 4
    "L",          # 5
    "O",          # 6
    "S",          # 7
    "T",          # 8
    "Z",          # 9
    "disk",       # 10
)
# Offered by default and accepted by per-pad placement.
PLACEABLE_SHAPES = tuple(s for s in OBJECT_SHAPES if s not in RETIRED_SHAPES)

# Largest scale at which `count` objects of this shape all fit side by side on
# the pads with the majority of each footprint over taxels. Above it the
# combination is refused rather than burning collection attempts on a size that
# cannot satisfy the label.
#
# Measured by running the placement below and scoring the settled result, not by
# fitting footprints on paper. Three things only measurement catches:
#
#   * A fit search free to pick the best offset put the cylinder at 0.62. The
#     real placement jitters, and the cylinder fails from 0.40.
#   * Coverage alone is not enough. Oversized objects used to be STACKED, and a
#     stacked object still projects onto the pad while touching nothing -- full
#     coverage, but objects_sensed short of the count. A size passes here only
#     if every object is placed side by side.
#   * Spawn-time coverage is not enough either. The cylinder rolls, so a size
#     that starts fine can settle at 0.04; scoring happens after the settle.
#
# Re-measured for zone placement. The earlier table was built when each object
# was confined to its own pad and objects were separated by bounding spheres, so
# at three objects nothing with a bounding radius over ~16.5 mm could occupy both
# pad 1 and pad 3. Neither constraint holds now -- objects share the fingerward
# strip and are separated by their footprints -- so the caps at two and three
# objects are markedly looser.
#
# They are TIGHTER at one object for the long tetrominoes, which used to sit at
# 1.00. That was never measured: the coverage test only covered box, disk,
# cylinder, T and O, so I/J/L/S/Z inherited a cap that does not hold. An I at
# 1.00 is roughly 48 mm long against a 36.2 mm pad.
SHAPE_MAX_SCALE = {
    #            n=1   n=2   n=3
    "box":      {1: 0.75, 2: 0.70, 3: 0.50},
    "disk":     {1: 0.95, 2: 0.65, 3: 0.50},
    # r 20 x L 90 mm base: long and thin is the worst fit for a 36 x 22 mm pad,
    # and it is the one shape held to a single pad (see ROLLING_SHAPES).
    "cylinder": {1: 0.40, 2: 0.40, 3: 0.30},
    # Measured per piece rather than shared. They do not in fact agree: the I is
    # a 4x1 bar and caps far below the rest, while the compact 2x2 O caps highest.
    "I": {1: 0.60, 2: 0.60, 3: 0.60},
    "J": {1: 0.95, 2: 0.85, 3: 0.55},
    "L": {1: 0.90, 2: 0.75, 3: 0.55},
    "O": {1: 1.00, 2: 1.00, 3: 0.75},
    "S": {1: 1.00, 2: 0.90, 3: 0.65},
    "T": {1: 0.95, 2: 0.85, 3: 0.70},
    "Z": {1: 0.85, 2: 0.85, 3: 0.65},
}


def max_scale_for(shape: str, count: int) -> float | None:
    """Cap for this shape at this object count, or None if unconstrained."""
    per_count = SHAPE_MAX_SCALE.get(shape)
    if per_count is None:
        return None
    # Counts past the table are at least as tight as its last entry.
    return per_count.get(count, min(per_count.values()))


def check_placement_feasible(shape: str, scale: float, count: int) -> None:
    """Refuse shape/scale combinations that cannot sit majority-on-pad."""
    if shape in RETIRED_SHAPES:
        raise ValueError(
            f"'{shape}' is retired: on this palm it rolls into the gap between "
            f"pads and reads zero on the taxels. Use one of {PLACEABLE_SHAPES}."
        )
    cap = max_scale_for(shape, count)
    if cap is not None and scale > cap + 1e-9:
        raise ValueError(
            f"{shape} x{count} at scale {scale:g} does not fit the palm pads: "
            f"{count} of them cannot sit side by side on "
            f"{PAD_EXTENT_MM[0]:.0f}x{PAD_EXTENT_MM[1]:.0f} mm pads with half "
            f"their footprint over taxels. Measured ceiling for x{count} is "
            f"scale {cap:g}."
        )


# Palm pad footprint, for error messages. Measured from the generated hand.
PAD_EXTENT_MM = (36.2, 21.7)

# How an object is oriented to lie flat before the random yaw is applied.
# Anything not listed rests flat already at identity (box, disk, tetrominoes).
FLAT_BASE_EULER = {
    # The cylinder's axis is local z and it is long, so it lies on its side.
    "cylinder": (np.pi / 2, 0.0, 0.0),
}


def is_tetromino(shape: str) -> bool:
    return shape in TETROMINO_CELLS


def shape_index(shape: str) -> int:
    """Class label for `shape`, stable across additions to the registry."""
    return OBJECT_SHAPES.index(shape)


def tetromino_block_offsets(shape: str, scale: float) -> np.ndarray:
    """Body-local block centres, (4, 3), with the piece centred on its own COM.

    Centring matters because the free joint acts at the body origin: an
    off-centre piece would spin up as soon as it is dropped.
    """
    half = TETROMINO_BLOCK_HALF * float(scale)
    cells = np.asarray(TETROMINO_CELLS[shape], dtype=np.float64) * (2.0 * half)
    cells -= cells.mean(axis=0)
    return np.column_stack([cells[:, 0], cells[:, 1], np.zeros(len(cells))])


def tetromino_half_extent(shape: str, scale: float) -> np.ndarray:
    """Axis-aligned half-extent of the whole piece in body-local axes, (3,).

    Keeps the npz `object_sizes` field meaningful and (N, 3)-shaped for pieces
    that have no single geom size.
    """
    half = TETROMINO_BLOCK_HALF * float(scale)
    offsets = tetromino_block_offsets(shape, scale)
    return np.abs(offsets).max(axis=0) + half


def object_size_vector(shape: str, scale: float) -> np.ndarray:
    """The (3,) size recorded for an object, whatever its shape family."""
    if is_tetromino(shape):
        return tetromino_half_extent(shape, scale)
    return np.asarray(OBJECT_SIZES[shape], dtype=np.float64) * float(scale)
# The sensor pads are separated islands on an open palm, so a free-standing
# object (especially the sphere) is in unstable equilibrium and rolls off
# within ~0.9 s. The object is therefore placed at its resting height and the
# fingers start cradling it immediately, which is also how you would load a
# real hand.
CLOSE_START = 0.0
CLOSE_END = 1.5
SPAWN_GAP = 0.001
PALM_GEOM_NAMES = ("uspa46_1", "uspa46_2", "uspa46_3")
# A ball on the flat, level palm sits in unstable equilibrium between the
# separated pads and escapes before the fingers close. Three measures keep it
# in: spawn over the fingerward pads, pitch the palm so any roll runs into the
# fingers, and start with the fingers already slightly curled.
SPAWN_PAD_NAMES = ("uspa46_1", "uspa46_2")
PALM_FLEX_NAMES = ("flex_uspa46_1", "flex_uspa46_2", "flex_uspa46_3")
PLACEMENT_MODES = ("per-pad", "legacy")
# Placement draws a ZONE, not a pad. Pads 1 and 2 sit side by side at the same y
# with only an 11.6 mm bare seam between them, so their joint bounding box --
# 84.1 x 21.8 mm, 86% of it taxel -- behaves as one region: an object anywhere in
# it, seam included, still lands mostly on sensor. Treating them as one zone is
# what lets two objects share a pad and lets a single object bridge the seam.
# Pad 3 is its own zone: 33 mm back toward the wrist, hardest to cradle, drawn
# least often.
ZONE_NAMES = ("fingerward", "wrist")
ZONE_WEIGHTS = (0.8, 0.2)
# The standing requirement is that the majority of every object sits over the
# taxel pads. Free sampling can put a candidate partly on bare palm, so it is
# enforced by measuring the footprint rather than by confining the jitter.
MIN_PAD_COVERAGE = 0.5
# Shapes that roll, which free placement cannot serve. Coverage measures how much
# of a footprint is on taxel, not how close it sits to an edge -- and a cylinder
# started 95% on a pad but alongside the seam rolls straight into it. Measured:
# at every coverage floor up to 0.95 the cylinder settles at 0.00-0.17 coverage,
# so no threshold rescues it. These shapes keep the old behaviour, confined to
# one pad with the jitter bounded by that pad's own extent, which is the only
# thing that holds them. Everything else is placed freely across a zone.
ROLLING_SHAPES = ("cylinder",)
# Fraction of the leftover pad a rolling shape may be jittered by.
ROLLING_JITTER = 0.5
# Objects are separated by their footprints, not their bounding spheres, so they
# spawn close enough to share a pad. This margin keeps them from spawning in
# contact, which would load the sensor before the fingers move.
PLACEMENT_CLEARANCE = 0.002
# Pitching the palm fingers-down (as the old in-hand scene builder did) retains the
# object but rolls it past the pads into the unsensed pocket between the palm
# and the finger bases: measured, even -2 deg drops the 0.5x sphere from 24
# sensed contacts to 0. The fingerward spawn and pre-curl below achieve the
# retention on their own, so the default is level; --palm-pitch still tilts.
PALM_PITCH_DEG = 0.0
# Measured: at 0.15 the palm is too flat to hold a cluster (1-2 of 3 objects
# retained); the deeper cup formed at 0.40 retains 3 of 3. Tightening the
# cluster instead made retention worse, so the bowl depth is the mechanism.
PREGRIP_FRACTION = 0.40
# At a common grip fraction the commanded pose is self-colliding: the thumb is
# driven into the index and stalls ~57 deg short of its target even with no
# object present. Giving the thumb a smaller closure target removes the
# collision entirely; delaying its ramp additionally frees the index.
THUMB_GRIP_FRACTION = 0.35
THUMB_DELAY = 0.5
GRASP_PATTERNS = ("hold", "pulse", "squeeze", "regrasp", "tap", "shear")
# regrasp and tap deliberately break contact, so they cannot be held to the
# same contact-fraction floor as the patterns that stay closed.
PATTERN_MIN_CONTACT = {
    "hold": 0.5, "pulse": 0.5, "squeeze": 0.5, "shear": 0.5,
    "regrasp": 0.3, "tap": 0.2,
}
SQUEEZE_STEP_SECONDS = 0.9
REGRASP_HZ = 0.35
TAP_HZ = 1.5
TAP_DEPTH = 0.5
SHEAR_HZ = 0.7
VIDEO_FPS_TARGET = 30.0
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
# The camera circles the hand so no contact stays hidden behind the fingers
# for the whole clip. Start on the familiar side view used elsewhere.
ORBIT_DISTANCE = 0.30
ORBIT_ELEVATION = -25.0
ORBIT_START_AZIMUTH = 120.0
ORBIT_LOOKAT_LIFT = 0.02
PANEL_SIZE = 320
PANEL_MARGIN_PX = 16
# Bare taxel cloud rendered beside the hand, same viewpoint, nothing occluding.
# The camera is framed on the cloud itself: the thumb sits far lateral of the
# fingers, so the cloud spans ~235 mm and needs its own distance, not the hand's.
CLOUD_WIDTH = 640
# The cloud shrinks a lot as the hand closes (181 mm radius at pre-grip vs
# 78 mm once gripping), so the camera tracks the live centroid and extent
# instead of being framed once on the rest pose.
CLOUD_TRACK_ALPHA = 0.1
CLOUD_MARGIN = 1.12
CLOUD_GRIDS = ("surface", "magnet")
# Which geometry the point-cloud panel draws.
#   leapxela - MuJoCo taxel sites on the simulated hand, in scene coordinates
#   sparsh   - URDF forward kinematics, the same view sparsh-skin-sim's
#              demos/demo_fk.py shows in Open3D, in its own nominal world frame
CLOUD_SOURCES = ("leapxela", "sparsh")


def resolve_cloud_sources(cloud_source: str) -> list[str]:
    if cloud_source == "both":
        return list(CLOUD_SOURCES)
    if cloud_source not in CLOUD_SOURCES:
        raise ValueError(f"Unknown cloud source '{cloud_source}'")
    return [cloud_source]


def hand_joint_qpos(model: mj.MjModel, data: mj.MjData) -> np.ndarray:
    """The 16 actuated joint angles, in the order the FK layer expects."""
    return data.qpos[
        np.array([int(model.jnt_qposadr[j]) for j in model.actuator_trnid[:, 0]])
    ]


def fk_cloud_positions(
    joint_angles: np.ndarray,
    forces_body: np.ndarray | None,
    args: argparse.Namespace,
    deform: bool,
) -> np.ndarray:
    """Taxel positions as sparsh-skin-sim's FK visualiser draws them, in FK order.

    `forces_body` is in flex vertex-body axes, matching what the FK layer is fed
    everywhere else. Upstream's viewer shows the deformed positions by default,
    so `deform` follows that.
    """
    return fk_cloud_frame(joint_angles, forces_body, args, deform)[0]


def track_cloud_camera(
    model: mj.MjModel, state: dict, positions: np.ndarray, azimuth: float
) -> mj.MjvCamera:
    """Keep a cloud filling its panel as the hand closes. Mutates `state`.

    Each cloud source carries its own state because the two live in different
    frames -- the leapxela cloud in scene coordinates, the sparsh one in the
    FK's nominal world about 0.16 m away.
    """
    centre = positions.mean(axis=0)
    radius = float(np.max(np.linalg.norm(positions - centre, axis=1)))
    state["lookat"] += CLOUD_TRACK_ALPHA * (centre - state["lookat"])
    state["distance"] += CLOUD_TRACK_ALPHA * (
        cloud_camera_distance(model, radius) - state["distance"]
    )
    camera = orbit_camera(state["lookat"], azimuth)
    camera.distance = state["distance"]
    return camera


def fk_cloud_frame(
    joint_angles: np.ndarray,
    forces_body: np.ndarray | None,
    args: argparse.Namespace,
    deform: bool,
) -> tuple[np.ndarray, np.ndarray | None]:
    """(positions, world forces) for the sparsh cloud; forces are None without input."""
    fk = compute_fk_taxels(
        joint_angles,
        forces_body,
        HAND_SS_URDF,
        TAXEL_MAP_JSON,
        args.sparsh_deform_scale,
        args.sparsh_max_displacement,
        True,
    )
    positions = (
        fk.positions_deformed
        if deform and fk.positions_deformed is not None
        else fk.positions
    )
    return np.asarray(positions, dtype=np.float64), fk.forces_world


def cloud_camera_distance(model: mj.MjModel, radius: float) -> float:
    """Distance at which a bounding sphere of `radius` fills the cloud panel.

    Derived from the camera's field of view rather than a tuned constant: the
    panel is narrower than it is tall, so the horizontal fov is the limiting
    one.
    """
    fovy = np.radians(float(model.vis.global_.fovy))
    aspect = CLOUD_WIDTH / VIDEO_HEIGHT
    fovx = 2.0 * np.arctan(np.tan(0.5 * fovy) * aspect)
    return CLOUD_MARGIN * radius / np.sin(0.5 * min(fovy, fovx))


# Acceptance needs every spawned object, so an episode that has already lost one
# can never be kept. Measured over 10 s episodes, the held count reaches its
# final value by t~0.5-1.0 s and never recovers, so simulating the remaining 9 s
# only delays a rejection that is already decided. Checked after CLOSE_END so the
# grip has fully closed. Rejected samples are discarded either way -- nothing
# that reaches the dataset changes, only the time spent not reaching it.
ABORT_CHECK_TIME = 2.0


MIN_PEAK_TOTAL_NORMAL = 0.1
# Multi-object floor: only rejects episodes with no sensed contact at all, well
# below the 0.04 N faint grasps that are deliberately kept.
MULTI_MIN_PEAK_NORMAL = 0.01
MAX_FINAL_DISTANCE = 0.15


def layout_entries_by_patch() -> dict:
    entries_by_patch = {}
    for entry in build_layout(HAND_WORKSPACE).entries:
        entries_by_patch.setdefault(entry.patch, []).append(entry)
    return entries_by_patch


@dataclass(frozen=True)
class ObjectSpec:
    shape: str
    scale: float
    mass: float


def object_body_name(index: int) -> str:
    return OBJECT_BODY_NAME if index == 0 else f"{OBJECT_BODY_NAME}_{index}"


def object_geom_name(index: int) -> str:
    return OBJECT_GEOM_NAME if index == 0 else f"{OBJECT_GEOM_NAME}_{index}"


def object_geom_names(index: int, shape: str) -> list[str]:
    """Every collision geom belonging to object `index`.

    Primitives are one body / one geom; a tetromino is one body carrying four
    box geoms. Everything that used to name a single geom -- contact filtering,
    sensed-object attribution, adhesion pairs, placement extents -- goes through
    this so neither family is a special case at the call site.
    """
    base = object_geom_name(index)
    if not is_tetromino(shape):
        return [base]
    return [f"{base}_block{block}" for block in range(TETROMINO_BLOCKS)]


def object_geom_groups(specs: list) -> list[list[str]]:
    return [object_geom_names(index, item.shape) for index, item in enumerate(specs)]


def resolve_object_geoms(
    model: mj.MjModel, groups: list[list[str]]
) -> tuple[np.ndarray, np.ndarray]:
    """Flat geom ids across all objects, plus the object each one belongs to."""
    ids, owners = [], []
    for index, names in enumerate(groups):
        for name in names:
            geom_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
            if geom_id < 0:
                raise ValueError(f"Object geom '{name}' not found")
            ids.append(geom_id)
            owners.append(index)
    return (
        np.asarray(ids, dtype=np.int64),
        np.asarray(owners, dtype=np.int64),
    )


def episode_label(specs: list, output_dir: Path) -> str:
    """Identify an episode on stdout.

    The staging directory name alone is opaque (`_attempt_calib_0091`), is
    reused verbatim by every retry of a sample, and the dataset collector runs
    several workers whose lines interleave -- so a bare name cannot be traced
    back to what was being grasped. `--multi-shapes` episodes mix shapes and
    sizes, hence the "mixed" collapse.
    """
    shapes = {spec.shape for spec in specs}
    scales = {spec.scale for spec in specs}
    shape = specs[0].shape if len(shapes) == 1 else "mixed"
    scale = f"s{specs[0].scale:.2f}" if len(scales) == 1 else "s=mixed"
    return f"{shape} x{len(specs)} {scale} [{output_dir.name}]"


def add_object_adhesion(spec: mj.MjSpec, specs: list, adhesion: float, gap: float) -> int:
    """Stick the objects to each other -- and to nothing else. Returns pair count.

    Scoped through explicit <pair> elements rather than geom/adhesion because a
    contact takes the SUM of its two geoms' adhesion: a value on the object
    geoms would leak into every object-hand contact as `a + 0`, and those are
    exactly the contacts the taxels read. A pair overrides that sum for the
    named pair alone, so flex-vs-object contacts stay at adhesion 0 and the
    recorded signal is untouched.

    `gap` is not optional. Adhesion only acts while a contact exists, and with
    gap=0 a contact exists only while the geoms interpenetrate -- so the moment
    objects begin to separate the contact disappears and takes the pull with it.
    Measured on two spheres: at gap=0 even 0.5 N (2.4x the object's weight) only
    slowed the fall, while 1 mm of gap held it.
    """
    if adhesion <= 0.0:
        return 0
    version = tuple(int(part) for part in mj.__version__.split(".")[:2])
    if version < ADHESION_MIN_MUJOCO:
        raise RuntimeError(
            f"--object-adhesion needs MuJoCo >= "
            f"{'.'.join(str(v) for v in ADHESION_MIN_MUJOCO)}, found {mj.__version__}. "
            "pair/adhesion does not exist in this build and would be silently ignored."
        )
    if gap <= 0.0:
        raise ValueError(
            f"object adhesion {adhesion} N needs a non-zero gap to do anything; "
            "with gap=0 the contact vanishes as soon as the objects separate"
        )
    slide, spin, roll = OBJECT_FRICTION
    groups = object_geom_groups(specs)
    pairs = 0
    for first, second in itertools.combinations(range(len(specs)), 2):
        # A tetromino carries four geoms, so sticking two of them together means
        # every cross pair. Pairs within one object are never emitted -- a piece
        # does not adhere to itself, and MuJoCo would reject the self-pair.
        for left, right in itertools.product(groups[first], groups[second]):
            pair = spec.add_pair()
            pair.geomname1 = left
            pair.geomname2 = right
            pair.condim = 3
            pair.friction = [slide, slide, spin, roll, roll]
            pair.adhesion = adhesion
            pair.gap = gap
            pairs += 1
    return pairs


def sensed_objects(
    data: mj.MjData, object_geom_ids: np.ndarray, geom_owners: np.ndarray
) -> np.ndarray:
    """Boolean per object: is it touching a taxel-bearing membrane right now?

    `count_held` is kinematic -- distance from the palm and height -- so an
    object resting in the unsensed pocket between the palm pads and the finger
    bases counts as held while contributing nothing to the tactile signal. This
    is the count the taxels actually support, and the two differ exactly in the
    case this adhesion work exists to fix.

    `geom_owners` maps each entry of `object_geom_ids` to its object, so a
    tetromino touching a pad with any of its four blocks counts once, not four
    times.
    """
    object_count = int(geom_owners.max()) + 1 if len(geom_owners) else 0
    sensed = np.zeros(object_count, dtype=bool)
    count = data.ncon
    if count == 0:
        return sensed
    flex = np.asarray(data.contact.flex)[:count]
    geom = np.asarray(data.contact.geom)[:count]
    for side in (0, 1):
        touching = geom[(flex[:, side] >= 0), 1 - side]
        hit = np.isin(object_geom_ids, touching)
        if hit.any():
            sensed[geom_owners[hit]] = True
    return sensed


def assert_adhesion_scoped(data: mj.MjData, object_geom_ids: np.ndarray) -> None:
    """Every adhesive contact must be object-object, and never touch a flex.

    The entire case for object-only adhesion is that the contacts the taxels
    read are left alone, so it is checked rather than trusted: a stray geom-level
    adhesion, or a MuJoCo change to how pair adhesion is resolved, would
    otherwise quietly bias every force in the dataset.
    """
    count = data.ncon
    if count == 0:
        return
    adhesive = np.asarray(data.contact.adhesion)[:count] != 0.0
    if not adhesive.any():
        return
    flex = np.asarray(data.contact.flex)[:count][adhesive]
    geoms = np.asarray(data.contact.geom)[:count][adhesive]
    if (flex >= 0).any():
        raise AssertionError(
            "adhesion reached a flex contact: the taxel readings are being "
            f"biased (flex ids {np.unique(flex[flex >= 0]).tolist()})"
        )
    if not np.isin(geoms, object_geom_ids).all():
        stray = np.unique(geoms[~np.isin(geoms, object_geom_ids)]).tolist()
        raise AssertionError(
            f"adhesion reached non-object geoms {stray}; it must apply between "
            "objects only"
        )


# A compiled hand is ~49 MB, so this cache has to stay small: a default run
# touches 54 distinct models during calibration (6 scales x 3 shapes x 3 counts)
# and 15 during collection, which unbounded across 8 workers would reach ~21 GB.
# Two entries already capture the win that matters -- one pool job is one sample,
# and run_sample loops up to --max-attempts (30) attempts plus the video re-run
# against identical specs, so a single entry serves the whole retry loop.
MODEL_CACHE_SIZE = 2


@lru_cache(maxsize=MODEL_CACHE_SIZE)
def _build_model_cached(
    specs: tuple, palm_pitch_deg: float, object_adhesion: float, object_adhesion_gap: float
):
    """Compile the hand, memoised on everything that shapes it.

    Callers must treat the returned model, skins and tips as READ-ONLY: they are
    shared by every episode that follows in this process, so a stray write would
    corrupt them silently and only under parallelism. `run_episode` holds to that
    -- it mutates only its own `MjData` -- and `tests/test_model_cache.py` pins
    the behaviour.
    """
    return _build_model_uncached(
        list(specs), palm_pitch_deg, object_adhesion, object_adhesion_gap
    )


def build_model(
    specs: list, palm_pitch_deg: float, object_adhesion: float, object_adhesion_gap: float
):
    """Public entry point; `specs` is a list, so it is keyed as a tuple.

    ObjectSpec is a frozen dataclass, which makes the whole argument list
    hashable and the model a pure function of it.
    """
    return _build_model_cached(
        tuple(specs), palm_pitch_deg, object_adhesion, object_adhesion_gap
    )


@lru_cache(maxsize=MODEL_CACHE_SIZE)
def _hand_layout_cached(
    specs: tuple, palm_pitch_deg: float, object_adhesion: float, object_adhesion_gap: float
):
    model, skins, tips = _build_model_cached(
        specs, palm_pitch_deg, object_adhesion, object_adhesion_gap
    )
    # A fresh MjData, i.e. the hand at qpos0 rather than the pre-curled pose,
    # which is what makes this a pure function of the model.
    return build_hand_layout(model, mj.MjData(model), skins, tips)


def hand_layout(
    specs: list, palm_pitch_deg: float, object_adhesion: float, object_adhesion_gap: float
):
    """Reference taxel layout for the hand these specs build. Read-only, shared."""
    return _hand_layout_cached(
        tuple(specs), palm_pitch_deg, object_adhesion, object_adhesion_gap
    )


def clear_model_cache() -> None:
    """Drop the cached hands. For tests and for callers that need the memory back."""
    _build_model_cached.cache_clear()
    _hand_layout_cached.cache_clear()


def _build_model_uncached(
    specs: list, palm_pitch_deg: float, object_adhesion: float, object_adhesion_gap: float
):
    entries_by_patch = layout_entries_by_patch()
    spec = load_base_model("Box")
    spec.option.iterations = SOLVER_ITERATIONS
    spec.option.tolerance = SOLVER_TOLERANCE
    spec.option.timestep = TIMESTEP
    trim_pad_boxes(spec)
    tilt_palm(spec, palm_pitch_deg)
    skins = [
        add_flex_sensor(
            spec, definition, entries_by_patch[GEOM_TO_PATCH[definition.geom_name]]
        )
        for definition in SENSOR_DEFINITIONS
    ]
    magnet_pose = json.loads(FINGERTIP_POSE_JSON.read_text())
    surface_offsets = tip_surface_offsets(magnet_pose)
    tips = [
        add_tip_flex(
            spec, finger, entries_by_patch[f"tip_{finger}"], surface_offsets[finger]
        )
        for finger in TIP_FINGERS
    ]
    camera_x = np.array([-0.783, -0.622, 0.0])
    camera_y = np.array([0.332, -0.419, 0.845])
    camera_x /= np.linalg.norm(camera_x)
    camera_y /= np.linalg.norm(camera_y)
    camera_z = np.cross(camera_x, camera_y)
    camera_quat = np.zeros(4)
    mj.mju_mat2Quat(
        camera_quat, np.column_stack((camera_x, camera_y, camera_z)).ravel()
    )
    spec.worldbody.add_camera(
        name="side", pos=[-0.183, 0.396, 0.296], quat=camera_quat.tolist()
    )
    spec.worldbody.add_light(
        name="top", pos=[0.0, 0.3, 1.0], dir=[0.0, -0.2, -1.0], type=mj.mjtLightType.mjLIGHT_DIRECTIONAL
    )
    for index, item in enumerate(specs):
        # Parked apart until the episode places them; the real pose is written
        # into qpos after the hand has been pre-curled.
        body = spec.worldbody.add_body(
            name=object_body_name(index), pos=[0.0, 0.0, 0.5 + 0.1 * index]
        )
        body.add_freejoint()
        # Colour by object index rather than by shape: in a multi-object episode
        # the video has to distinguish the objects, not their kinds.
        colour = OBJECT_COLOURS[index % len(OBJECT_COLOURS)]
        names = object_geom_names(index, item.shape)
        if is_tetromino(item.shape):
            half = TETROMINO_BLOCK_HALF * item.scale
            # item.mass is the mass of the whole piece, so split it over the
            # blocks -- MuJoCo's geom `mass` is per geom.
            block_mass = item.mass / TETROMINO_BLOCKS
            for name, offset in zip(
                names, tetromino_block_offsets(item.shape, item.scale)
            ):
                body.add_geom(
                    name=name,
                    type=mj.mjtGeom.mjGEOM_BOX,
                    pos=offset.tolist(),
                    size=[half, half, half],
                    mass=block_mass,
                    rgba=colour,
                    contype=3,
                    conaffinity=3,
                    condim=3,
                    friction=list(OBJECT_FRICTION),
                )
            continue
        body.add_geom(
            name=names[0],
            type=OBJECT_GEOM_TYPES[item.shape],
            size=(
                np.asarray(OBJECT_SIZES[item.shape], dtype=np.float64)
                * item.scale
            ).tolist(),
            mass=item.mass,
            rgba=colour,
            contype=3,
            conaffinity=3,
            condim=3,
            friction=list(OBJECT_FRICTION),
        )
    add_object_adhesion(spec, specs, object_adhesion, object_adhesion_gap)
    model = spec.compile()
    model.vis.global_.offwidth = max(VIDEO_WIDTH, CLOUD_WIDTH)
    model.vis.global_.offheight = VIDEO_HEIGHT
    model.vis.headlight.ambient = [0.3, 0.3, 0.3]
    model.vis.headlight.diffuse = [0.7, 0.7, 0.7]
    model.vis.headlight.specular = [0.8, 0.8, 0.8]
    return model, skins, tips


def tilt_palm(spec: mj.MjSpec, pitch_deg: float) -> None:
    """Pitch the welded palm fingers-down about the world x axis."""
    if pitch_deg == 0.0:
        return
    palm = spec.body("palm")
    rotation = np.zeros(4)
    mj.mju_axisAngle2Quat(
        rotation, np.array([1.0, 0.0, 0.0]), np.deg2rad(pitch_deg)
    )
    tilted = np.zeros(4)
    mj.mju_mulQuat(tilted, rotation, np.asarray(palm.quat, dtype=np.float64))
    palm.quat = tilted.tolist()


def pregrip_targets(model: mj.MjModel, pregrip_fraction: float) -> np.ndarray:
    low = model.actuator_ctrlrange[:, 0]
    high = model.actuator_ctrlrange[:, 1]
    return low + pregrip_fraction * (high - low)


def apply_pregrip(
    model: mj.MjModel, data: mj.MjData, pregrip_fraction: float
) -> None:
    """Start the hand already curled, so it cannot flick the object at t=0."""
    targets = pregrip_targets(model, pregrip_fraction)
    for actuator_id in range(model.nu):
        joint_id = int(model.actuator_trnid[actuator_id, 0])
        data.qpos[int(model.jnt_qposadr[joint_id])] = targets[actuator_id]
    data.ctrl[:] = targets
    mj.mj_forward(model, data)


def orbit_camera(lookat: np.ndarray, azimuth: float) -> mj.MjvCamera:
    camera = mj.MjvCamera()
    camera.lookat[:] = lookat
    camera.azimuth = azimuth
    camera.elevation = ORBIT_ELEVATION
    camera.distance = ORBIT_DISTANCE
    return camera



def palm_pad_centre(model: mj.MjModel, data: mj.MjData) -> np.ndarray:
    pad_ids = [
        mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
        for name in PALM_GEOM_NAMES
    ]
    return np.mean([data.geom_xpos[g] for g in pad_ids], axis=0)


def count_held(
    model: mj.MjModel, data: mj.MjData, body_ids: list, palm_center: np.ndarray
) -> int:
    """Objects still in the hand -- the count the tactile signal reflects."""
    return sum(
        1 for body_id in body_ids
        if np.linalg.norm(data.xpos[body_id] - palm_center) <= MAX_FINAL_DISTANCE
        and data.xpos[body_id][2] >= palm_center[2] - 0.05
    )


def support_extent(
    model: mj.MjModel, geom_id: int, rotation: np.ndarray
) -> float:
    """Half-extent of a rotated geom along world up.

    Needed so a randomly oriented object rests on the palm instead of
    interpenetrating it: a tumbled box reaches further down than its half-size.
    """
    size = np.asarray(model.geom_size[geom_id], dtype=np.float64)
    up = rotation[2, :]
    kind = int(model.geom_type[geom_id])
    if kind == mj.mjtGeom.mjGEOM_SPHERE:
        return float(size[0])
    if kind == mj.mjtGeom.mjGEOM_BOX:
        return float(np.abs(up) @ size[:3])
    # Cylinder: radius sweeps the axes perpendicular to its own, half-length
    # projects along it.
    radial = float(size[0] * np.sqrt(max(0.0, 1.0 - up[2] ** 2)))
    return float(abs(size[1] * up[2]) + radial)


def body_support_extent(
    model: mj.MjModel, geom_ids: list[int], rotation: np.ndarray
) -> float:
    """How far a multi-geom object reaches BELOW its body origin, along world up.

    `place_objects` lifts the body origin by this much so the lowest point of the
    object clears the palm. Each geom contributes its own half-extent minus how
    far its centre sits above the origin -- `rotation[2, :]` is already the row
    that projects a body-local vector onto world up, so the offset is dotted
    with it directly rather than rotated first. For a single-geom object centred
    on its body this reduces to `support_extent`.
    """
    up = rotation[2, :]
    return max(
        support_extent(model, geom_id, rotation)
        - float(up @ np.asarray(model.geom_pos[geom_id], dtype=np.float64))
        for geom_id in geom_ids
    )


def body_bounding_radius(model: mj.MjModel, geom_ids: list[int]) -> float:
    """Radius of a sphere at the body origin enclosing every geom, any orientation.

    Conservative by construction -- each geom contributes its own centre offset
    plus its own bounding radius. `place_objects` treats a clear bounding sphere
    as proof a slot is free, so under-estimating here is what spawns objects
    inside one another.
    """
    return max(
        float(np.linalg.norm(model.geom_pos[geom_id]))
        + bounding_radius(model, geom_id)
        for geom_id in geom_ids
    )


def pad_regions(model: mj.MjModel, data: mj.MjData) -> list[tuple]:
    """Per-pad (centre_xy, half_extent_xy, top_z) for the three palm pads.

    Read from the flex vertices rather than the pad geoms: the membrane is what
    an object actually rests on, and its extent is what "on the pad" means.
    """
    regions = []
    for name in PALM_FLEX_NAMES:
        vertices = _flex_vertices(model, data, name)
        low = vertices[:, :2].min(axis=0)
        high = vertices[:, :2].max(axis=0)
        regions.append((
            0.5 * (low + high),
            0.5 * (high - low),
            float(vertices[:, 2].max()),
        ))
    return regions


def flat_orientation(shape: str, yaw: float) -> np.ndarray:
    """Quaternion laying `shape` on its stable face, then spun by `yaw` about +z.

    Tumbling an object with a uniform random quaternion -- what legacy placement
    does -- stands boxes on edge and drops cylinders across the pad seam. Every
    shape here has one flat rest pose; only the spin about the pad normal varies.
    """
    quat = np.zeros(4)
    euler = FLAT_BASE_EULER.get(shape)
    if euler is None:
        base = np.array([1.0, 0.0, 0.0, 0.0])
    else:
        base = np.zeros(4)
        mj.mju_euler2Quat(base, np.asarray(euler, dtype=np.float64), "xyz")
    spin = np.zeros(4)
    mj.mju_axisAngle2Quat(spin, np.array([0.0, 0.0, 1.0]), yaw)
    mj.mju_mulQuat(quat, spin, base)
    return quat


def footprint_half_extent(
    model: mj.MjModel, geom_ids: list[int], rotation: np.ndarray
) -> np.ndarray:
    """Half-extent of the object's xy footprint once rotated, for jitter bounds."""
    extent = np.zeros(2)
    for geom_id in geom_ids:
        size = np.asarray(model.geom_size[geom_id], dtype=np.float64)
        kind = int(model.geom_type[geom_id])
        if kind == int(mj.mjtGeom.mjGEOM_SPHERE):
            local = np.repeat(size[0], 3)
        elif kind == int(mj.mjtGeom.mjGEOM_BOX):
            local = size[:3]
        else:
            local = np.array([size[0], size[0], size[1]])
        # Support function of a box under rotation, which bounds every primitive
        # here without needing a per-shape projection.
        reach = np.abs(rotation[:2, :]) @ local
        centre = np.abs(rotation[:2, :] @ np.asarray(model.geom_pos[geom_id]))
        extent = np.maximum(extent, centre + reach)
    return extent


def placement_zones(model: mj.MjModel, data: mj.MjData) -> list[tuple]:
    """Regions an object centre may be drawn from: (centre_xy, half_xy, top_z).

    Pads 1 and 2 are merged into one zone spanning the seam between them, so the
    sampler can put two objects on one pad or one object across both. Pad 3 is
    its own zone. `pad_regions` stays the primitive underneath: coverage is still
    measured against the three pads individually, and only the *draw* is by zone.
    """
    regions = pad_regions(model, data)
    zones = []
    for group in ((0, 1), (2,)):
        low = np.min([regions[i][0] - regions[i][1] for i in group], axis=0)
        high = np.max([regions[i][0] + regions[i][1] for i in group], axis=0)
        top = max(regions[i][2] for i in group)
        zones.append((0.5 * (low + high), 0.5 * (high - low), top))
    return zones


def footprint_points(
    model: mj.MjModel, geom_ids: list[int], rotation: np.ndarray, per_axis: int = 9
) -> np.ndarray:
    """Body-frame xy samples of the object's true footprint, one cloud per object.

    A tetromino's footprint is the union of its four cells, which its bounding
    box overstates by a third or more -- and that overstatement is exactly the
    room two objects need to nest. Sampling the geoms themselves keeps the L, T,
    S and Z outlines honest, and masking cylinders to their ellipse keeps a disk
    from claiming its bounding square's corners.

    The cloud is computed once per object because yaw is drawn before the attempt
    loop; each candidate position then only translates it.
    """
    axis = np.linspace(-1.0, 1.0, per_axis)
    lattice = np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1)
    lattice = lattice.reshape(-1, 3)

    clouds = []
    for geom_id in geom_ids:
        size = np.asarray(model.geom_size[geom_id], dtype=np.float64)
        kind = int(model.geom_type[geom_id])
        if kind == int(mj.mjtGeom.mjGEOM_SPHERE):
            local, radial = np.repeat(size[0], 3), (0, 1, 2)
        elif kind == int(mj.mjtGeom.mjGEOM_BOX):
            local, radial = size[:3], ()
        else:
            # Cylinder and capsule: radius on x/y, half-length on z.
            local, radial = np.array([size[0], size[0], size[1]]), (0, 1)
        points = lattice * local
        if radial:
            keep = np.linalg.norm(lattice[:, radial], axis=1) <= 1.0
            points = points[keep]
        points = points + np.asarray(model.geom_pos[geom_id], dtype=np.float64)
        clouds.append(points @ rotation[:2, :].T)
    return np.concatenate(clouds)


def pad_coverage(points_xy: np.ndarray, regions: list[tuple]) -> np.ndarray:
    """Per-pad fraction of a footprint cloud lying over each pad.

    Returned per pad rather than summed so callers can ask "is this object on
    both pads 1 and 2?" as well as "is it majority-on-pad?". The pads do not
    overlap, so the total is the sum.
    """
    shares = []
    for centre, half, _top in regions:
        inside = np.all(np.abs(points_xy - centre) <= half, axis=1)
        shares.append(float(np.count_nonzero(inside)) / len(points_xy))
    return np.asarray(shares)


def footprint_rectangles(
    model: mj.MjModel, geom_ids: list[int], rotation: np.ndarray
) -> list[tuple]:
    """Per-geom (centre_xy, axes, half) oriented rectangles bounding the footprint.

    The overlap test works on these rather than on one bounding sphere per body.
    A sphere around a 17.6 mm box demands 30.5 mm of clearance because it swallows
    the object's height and diagonal, which is what used to make two objects
    unable to share a 36.2 mm pad even though their footprints fit side by side.

    Every placeable shape is laid flat by `flat_orientation`, so exactly one body
    axis points along world up and the other two span the footprint. Which one is
    vertical varies -- the cylinder lies on its side, so its own axis is in the
    plane -- so it is read off the rotation rather than assumed. A world-aligned
    box would be a cheaper bound but grows by sqrt(2) at 45 degrees of yaw, giving
    back much of the room this is meant to recover.
    """
    up = np.abs(rotation[2, :])
    vertical = int(np.argmax(up))
    if up[vertical] < 0.99:
        raise ValueError(
            "footprint_rectangles needs a flat object: no body axis lies along "
            f"world up (|rotation[2]| = {np.round(up, 3).tolist()})"
        )
    plane = [index for index in range(3) if index != vertical]
    # Columns, not rows: rotation[:, i] is body axis i expressed in world.
    axes = np.stack([rotation[:2, index] for index in plane])

    rectangles = []
    for geom_id in geom_ids:
        size = np.asarray(model.geom_size[geom_id], dtype=np.float64)
        kind = int(model.geom_type[geom_id])
        if kind == int(mj.mjtGeom.mjGEOM_SPHERE):
            local = np.repeat(size[0], 3)
        elif kind == int(mj.mjtGeom.mjGEOM_BOX):
            local = size[:3]
        else:
            local = np.array([size[0], size[0], size[1]])
        centre = rotation[:2, :] @ np.asarray(model.geom_pos[geom_id])
        rectangles.append((centre, axes, local[plane]))
    return rectangles


def rectangles_overlap(left: tuple, right: tuple, clearance: float) -> bool:
    """Separating-axis test between two footprint rectangles, inflated by clearance."""
    left_centre, left_axes, left_half = left
    right_centre, right_axes, right_half = right
    delta = right_centre - left_centre
    for axes, half, other_axes, other_half in (
        (left_axes, left_half, right_axes, right_half),
        (right_axes, right_half, left_axes, left_half),
    ):
        for index in range(2):
            axis = axes[index]
            reach = half[index] + float(np.abs(other_axes @ axis) @ other_half)
            if abs(float(delta @ axis)) > reach + clearance:
                return False
    return True


def place_objects_per_pad(
    model: mj.MjModel, data: mj.MjData, specs: list, rng: np.random.Generator,
    zone_weights: tuple = ZONE_WEIGHTS,
    min_pad_coverage: float = MIN_PAD_COVERAGE,
) -> None:
    """Place each object flat over the palm pads, favouring the fingerward pair.

    The legacy region is centred between pads 1 and 2, which is bare palm -- a
    single object landed there covers ~0.3 of its footprint with taxels, and by
    three objects the worst is often 0.0. So placement is confined to the pads,
    but by *measuring* how much of each footprint lands on taxels rather than by
    pinning each object inside one pad.

    That distinction is the whole point. Bounding the jitter by a single pad's
    extent left an object at cap size barely a millimetre of play, and separating
    objects by their bounding spheres demanded 30 mm of clearance for a 17.6 mm
    box, so two objects could never share a pad and every count-3 episode came
    out as one object per pad. Here the centre is drawn freely inside a zone --
    pads 1 and 2 are one zone spanning the seam between them -- and a candidate
    is kept if it clears the objects already down and still has
    `min_pad_coverage` of its footprint over taxels. Sharing a pad, clustering,
    and bridging the seam all follow from that one draw.

    Pads 1 and 2 are drawn more often than pad 3: they sit 44 mm from the
    fingertips against pad 3's 77 mm, so they are the ones the fingers actually
    close onto, and many episodes should use only that pair.
    """
    regions = pad_regions(model, data)
    zones = placement_zones(model, data)
    weights = np.asarray(zone_weights, dtype=np.float64)
    if weights.shape != (len(zones),) or weights.min() < 0.0 or weights.sum() <= 0.0:
        raise ValueError(
            f"zone_weights must be {len(zones)} non-negative numbers that sum "
            f"above zero, one per zone {ZONE_NAMES}; got {zone_weights}"
        )
    weights = weights / weights.sum()

    placed = []
    for index, item in enumerate(specs):
        geom_ids = [
            mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
            for name in object_geom_names(index, item.shape)
        ]
        quat = flat_orientation(item.shape, rng.uniform(0.0, 2.0 * np.pi))
        rotation = np.zeros(9)
        mj.mju_quat2Mat(rotation, quat)
        rotation = rotation.reshape(3, 3)
        lift = body_support_extent(model, geom_ids, rotation)
        radius = body_bounding_radius(model, geom_ids)
        # Yaw is fixed for this object, so its footprint is shaped once here and
        # every candidate below only translates it.
        cloud = footprint_points(model, geom_ids, rotation)
        rectangles = footprint_rectangles(model, geom_ids, rotation)
        half = footprint_half_extent(model, geom_ids, rotation)

        # A rolling shape is drawn per pad and held near that pad's centre; every
        # other shape is drawn per zone and placed freely within it. The pad
        # weights are the zone weights with the fingerward share split across the
        # two pads it covers, so the fingerward bias survives either way.
        if item.shape in ROLLING_SHAPES:
            draw_regions = regions
            draw_weights = np.array(
                [weights[0] / 2.0, weights[0] / 2.0, weights[1]]
            )
        else:
            draw_regions, draw_weights = zones, weights
        confined = item.shape in ROLLING_SHAPES

        # cloud/rectangles/lift/half change every iteration, so they are bound as
        # defaults rather than captured: a closure over them would silently use
        # the last object's geometry if these were called after the loop moved on.
        def candidate_in(where, half=half, lift=lift, confined=confined,
                         draw_regions=draw_regions):
            centre, region_half, top = draw_regions[where]
            if confined:
                # Bounded by what is left of the pad once the footprint is
                # accounted for, so a rolling object never starts near an edge.
                slack = np.maximum(region_half - half, 0.0) * ROLLING_JITTER
            else:
                # The centre may sit anywhere the object still overlaps the zone
                # -- the coverage test, not this bound, decides whether that is
                # enough taxel. Clamping at zero keeps an object wider than its
                # zone centred rather than flipping the interval inside out.
                slack = np.maximum(region_half - 0.5 * half, 0.0)
            return np.array([
                centre[0] + rng.uniform(-slack[0], slack[0]),
                centre[1] + rng.uniform(-slack[1], slack[1]),
                top + lift + SPAWN_GAP,
            ])

        def clears(candidate, rectangles=rectangles):
            offset = candidate[:2]
            return not any(
                rectangles_overlap(
                    (mine[0] + offset, mine[1], mine[2]),
                    (theirs[0] + other[:2], theirs[1], theirs[2]),
                    PLACEMENT_CLEARANCE,
                )
                for other, other_rectangles, _ in placed
                for mine in rectangles
                for theirs in other_rectangles
            )

        def coverage_of(candidate, cloud=cloud):
            return float(pad_coverage(cloud + candidate[:2], regions).sum())

        # The best candidate that fits beside the objects already down is kept as
        # the loop runs. An object too large to reach min_pad_coverage anywhere --
        # a disk wider than the pad is tall, say -- then lands on its best spot
        # rather than being stacked, because stacking is the worse failure: it is
        # invisible to a coverage check, since the upper object still projects
        # onto the pad while touching nothing, and shows up only as
        # objects_sensed falling short of the count.
        position, best_coverage = None, -1.0
        def consider(candidate):
            nonlocal position, best_coverage
            if not clears(candidate):
                return False
            coverage = coverage_of(candidate)
            if coverage > best_coverage:
                position, best_coverage = candidate, coverage
            return coverage >= min_pad_coverage

        for _ in range(PLACEMENT_ATTEMPTS):
            if consider(candidate_in(
                int(rng.choice(len(draw_regions), p=draw_weights))
            )):
                break
        else:
            # The strip is full: sweep the regions in weight order so a third
            # oversized object reaches pad 3, then the pad centres, which are the
            # highest-coverage spots on the palm.
            for where in np.argsort(-draw_weights):
                if consider(candidate_in(int(where))):
                    break
            else:
                for centre, _pad_half, top in regions:
                    spot = np.array([centre[0], centre[1], top + lift + SPAWN_GAP])
                    if consider(spot):
                        break

        if position is None:
            # Genuinely no room beside the others: stack, as legacy does.
            top_of_stack = max(
                other[2] + other_radius for other, _rectangles, other_radius in placed
            )
            centre, _region_half, _top = draw_regions[int(np.argmax(draw_weights))]
            position = np.array([
                centre[0], centre[1], top_of_stack + lift + SPAWN_GAP
            ])
        placed.append((position, rectangles, radius))
        address = int(model.jnt_qposadr[int(model.body_jntadr[
            mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(index))
        ])])
        data.qpos[address : address + 7] = np.concatenate([position, quat])
    mj.mj_forward(model, data)


def placement_region(model: mj.MjModel, data: mj.MjData) -> tuple:
    """Palm-frame region objects may be placed in: (origin, across, fingerward,
    support height). Derived from the palm pads, not hard-coded."""
    palm_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, "palm")
    rotation = data.xmat[palm_id].reshape(3, 3)
    spawn_ids = [
        mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
        for name in SPAWN_PAD_NAMES
    ]
    centre = np.mean([data.geom_xpos[g] for g in spawn_ids], axis=0)
    support = max(
        float(np.max(_flex_vertices(model, data, f"flex_uspa46_{index}")[:, 2]))
        for index in (1, 2, 3)
    )
    return centre, rotation[:, 0], rotation[:, 2], support


def bounding_radius(model: mj.MjModel, geom_id: int) -> float:
    """Radius of the smallest sphere enclosing the geom, for any orientation.

    `max(geom_size)` is not it: a box's half-edge is sqrt(3) smaller than its
    corner distance, so using it lets two boxes spawn inside one another.
    """
    size = model.geom_size[geom_id]
    kind = int(model.geom_type[geom_id])
    if kind == int(mj.mjtGeom.mjGEOM_SPHERE):
        return float(size[0])
    if kind == int(mj.mjtGeom.mjGEOM_BOX):
        return float(np.linalg.norm(size[:3]))
    if kind in (int(mj.mjtGeom.mjGEOM_CYLINDER),
                int(mj.mjtGeom.mjGEOM_CAPSULE)):
        return float(np.hypot(size[0], size[1]))
    return float(np.linalg.norm(size[:3]))


def place_objects(
    model: mj.MjModel, data: mj.MjData, specs: list, jitter: float,
    height_step: float, randomize_orientation: bool, rng: np.random.Generator,
) -> None:
    """Scatter the objects over the palm region without overlapping them."""
    centre, across, fingerward, support = placement_region(model, data)
    placed = []
    for index, item in enumerate(specs):
        geom_ids = [
            mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
            for name in object_geom_names(index, item.shape)
        ]
        radius = body_bounding_radius(model, geom_ids)
        if randomize_orientation:
            quat = rng.normal(size=4)
            quat /= np.linalg.norm(quat)
        else:
            quat = np.array([1.0, 0.0, 0.0, 0.0])
        rotation = np.zeros(9)
        mj.mju_quat2Mat(rotation, quat)
        lift = body_support_extent(model, geom_ids, rotation.reshape(3, 3))
        # Rejection-sample a slot on the palm that clears everything already
        # placed. Bounding spheres are conservative, so a "clear" slot really
        # is free.
        position = None
        for _ in range(PLACEMENT_ATTEMPTS):
            candidate = (
                centre
                + rng.uniform(-jitter, jitter) * across
                + rng.uniform(-jitter, jitter) * fingerward
            )
            candidate[2] = support + lift + SPAWN_GAP + index * height_step
            if all(
                np.linalg.norm(candidate - other) > radius + other_radius
                for other, other_radius in placed
            ):
                position = candidate
                break
        if position is None:
            # The palm cannot fit another object side by side, so stack this
            # one directly on top of the cluster. Guarantees no overlap (the
            # old code fell through and spawned objects 30 mm inside each
            # other, which launched them at ~1 m/s) and is how a real handful
            # of objects piles up anyway.
            top = max(
                other[2] + other_radius for other, other_radius in placed
            )
            position = centre.copy()
            position[2] = top + lift + SPAWN_GAP
        placed.append((position, radius))
        address = int(model.jnt_qposadr[int(model.body_jntadr[
            mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(index))
        ])])
        data.qpos[address : address + 7] = np.concatenate([position, quat])
    mj.mj_forward(model, data)



@dataclass(frozen=True)
class GraspProfile:
    pattern: str
    grip_fraction: float
    thumb_grip_fraction: float
    pregrip_fraction: float
    thumb_delay: float
    pulse_hz: float
    pulse_amplitude: float
    shear_amplitude: float
    squeeze_steps: int


def profile_from_args(pattern: str, args: argparse.Namespace) -> GraspProfile:
    return GraspProfile(
        pattern=pattern,
        grip_fraction=args.grip_fraction,
        thumb_grip_fraction=args.thumb_grip_fraction,
        pregrip_fraction=args.pregrip_fraction,
        thumb_delay=args.thumb_delay,
        pulse_hz=args.pulse_hz,
        pulse_amplitude=args.pulse_amplitude,
        shear_amplitude=args.shear_amplitude,
        squeeze_steps=args.squeeze_steps,
    )


def thumb_mask(model: mj.MjModel) -> np.ndarray:
    return np.array([
        mj.mj_id2name(model, mj.mjtObj.mjOBJ_ACTUATOR, i).startswith("th_")
        for i in range(model.nu)
    ])


def lateral_mask(model: mj.MjModel) -> np.ndarray:
    """Abduction / axial-roll actuators, which slide the object sideways."""
    names = [
        mj.mj_id2name(model, mj.mjtObj.mjOBJ_ACTUATOR, i)
        for i in range(model.nu)
    ]
    return np.array(["_rot_" in name or "_axl_" in name for name in names])


def control_targets(
    model: mj.MjModel, t: float, profile: GraspProfile
) -> np.ndarray:
    low = model.actuator_ctrlrange[:, 0]
    high = model.actuator_ctrlrange[:, 1]
    span = high - low
    is_thumb = thumb_mask(model)
    # The thumb closes less far than the fingers, otherwise the commanded pose
    # drives it into the index and both stall.
    grip = low + np.where(
        is_thumb, profile.thumb_grip_fraction, profile.grip_fraction
    ) * span
    pregrip = pregrip_targets(model, profile.pregrip_fraction)

    close_span = CLOSE_END - CLOSE_START
    finger_phase = np.clip((t - CLOSE_START) / close_span, 0.0, 1.0)
    thumb_phase = np.clip(
        (t - CLOSE_START - profile.thumb_delay) / close_span, 0.0, 1.0
    )
    phase = np.where(is_thumb, thumb_phase, finger_phase)
    smooth = phase * phase * (3.0 - 2.0 * phase)
    targets = pregrip + smooth * (grip - pregrip)
    if t < CLOSE_END + profile.thumb_delay:
        return np.clip(targets, low, high)

    elapsed = t - CLOSE_END - profile.thumb_delay
    if profile.pattern == "hold":
        modulation = 0.0
    elif profile.pattern == "pulse":
        modulation = 0.5 * profile.pulse_amplitude * (
            1.0 - np.cos(2.0 * np.pi * profile.pulse_hz * elapsed)
        )
    elif profile.pattern == "squeeze":
        # Staircase to progressively firmer grips, then back to the start.
        cycle = profile.squeeze_steps * 2
        index = int(elapsed / SQUEEZE_STEP_SECONDS) % cycle
        level = index if index < profile.squeeze_steps else cycle - index - 1
        modulation = profile.pulse_amplitude * level / max(
            profile.squeeze_steps - 1, 1
        )
    elif profile.pattern == "regrasp":
        # Release most of the way back to the pre-grip pose, then re-close.
        release = 0.5 * (1.0 - np.cos(2.0 * np.pi * REGRASP_HZ * elapsed))
        return np.clip(
            targets + release * (pregrip - targets), low, high
        )
    elif profile.pattern == "tap":
        release = 0.5 * (1.0 - np.cos(2.0 * np.pi * TAP_HZ * elapsed))
        return np.clip(
            targets + TAP_DEPTH * release * (pregrip - targets), low, high
        )
    elif profile.pattern == "shear":
        lateral = profile.shear_amplitude * np.sin(
            2.0 * np.pi * SHEAR_HZ * elapsed
        )
        return np.clip(
            targets + np.where(lateral_mask(model), lateral * span, 0.0),
            low, high,
        )
    else:
        raise ValueError(f"Unknown grasp pattern '{profile.pattern}'")
    # Squeeze with the fingers only. Modulating the thumb too would push it
    # past the closure ceiling that keeps it clear of the index, undoing the
    # anti-jam fix exactly when the grip is firmest.
    return np.clip(
        targets + np.where(is_thumb, 0.0, modulation * span), low, high
    )


class TaxelFrames:
    """Fixed local grid of all 368 taxels, plus rigid-body FK onto it.

    Mirrors the sparsh convention (`tactile_ssl/data/xela_tactile.py`):
    positions are forward kinematics of the parent link composed with a grid
    that is constant in that link's frame. Two grids are carried:
    `local_surface` is where contact happens (the membrane rest vertices) and
    is the primary one; `local_magnet` is the raw calibrated magnet centres,
    which sit ~8-10 mm inside the surface but match the real hand's layout.
    """

    def __init__(
        self,
        model: mj.MjModel,
        data: mj.MjData,
        skins: list,
        tips: list,
        entries_by_patch: dict,
    ):
        self.body_ids = np.zeros(TAXEL_COUNT, dtype=np.int64)
        self.body_names = np.empty(TAXEL_COUNT, dtype=object)
        self.local_surface = np.zeros((TAXEL_COUNT, 3))
        self.local_magnet = np.zeros((TAXEL_COUNT, 3))
        self.local_normal = np.zeros((TAXEL_COUNT, 3))
        # Per-taxel frame in its link: columns are the shear-x, shear-y and
        # outward-normal axes the readings are expressed in.
        self.local_rotation = np.zeros((TAXEL_COUNT, 3, 3))
        self.palm_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, "palm")

        patches = [
            (skin.parent_body_name, skin.flex_name, skin.taxel_ids,
             GEOM_TO_PATCH[skin.definition.geom_name],
             np.tile(
                 np.column_stack(
                     (skin.tangent_u, skin.tangent_v, skin.normal)
                 ),
                 (len(skin.taxel_ids), 1, 1),
             ))
            for skin in skins
        ] + [
            (tip.parent_body_name, tip.flex_name, tip.taxel_ids,
             f"tip_{tip.finger}", tip.vertex_rotations)
            for tip in tips
        ]
        for body_name, flex_name, taxel_ids, patch, rotations in patches:
            body_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, body_name)
            rotation = data.xmat[body_id].reshape(3, 3)
            origin = data.xpos[body_id]
            # Membrane rest vertices pulled back into the link frame: the
            # anchors hold every vertex here, so this is a fixed local grid.
            vertices = _flex_vertices(model, data, flex_name)
            self.local_surface[taxel_ids] = (vertices - origin) @ rotation
            self.local_rotation[taxel_ids] = rotations
            self.local_normal[taxel_ids] = rotations[:, :, 2]
            self.body_ids[taxel_ids] = body_id
            self.body_names[taxel_ids] = body_name
            for entry in entries_by_patch[patch]:
                self.local_magnet[entry.taxel_id] = entry.pos

    def world(self, data: mj.MjData, local: np.ndarray) -> np.ndarray:
        rotations = data.xmat[self.body_ids].reshape(-1, 3, 3)
        return data.xpos[self.body_ids] + np.einsum(
            "nij,nj->ni", rotations, local
        )

    def palm(self, data: mj.MjData, local: np.ndarray) -> np.ndarray:
        palm_rotation = data.xmat[self.palm_id].reshape(3, 3)
        return (self.world(data, local) - data.xpos[self.palm_id]) @ palm_rotation

    def world_vectors(self, data: mj.MjData, readings: np.ndarray) -> np.ndarray:
        """Per-taxel (shear_x, shear_y, normal_z) rotated into world.

        The normal channel is compression-positive, so it maps onto the
        outward normal: a pressed taxel yields an arrow standing off the
        surface, tilted by the shear.
        """
        rotations = data.xmat[self.body_ids].reshape(-1, 3, 3)
        axes = np.einsum("nij,njk->nik", rotations, self.local_rotation)
        return np.einsum("nik,nk->ni", axes, readings)

    def palm_directions(self, data: mj.MjData, local: np.ndarray) -> np.ndarray:
        palm_rotation = data.xmat[self.palm_id].reshape(3, 3)
        rotations = data.xmat[self.body_ids].reshape(-1, 3, 3)
        return np.einsum("nij,nj->ni", rotations, local) @ palm_rotation


def sample_specs(
    shape: str, scale: float, count: int, args: argparse.Namespace,
    rng: np.random.Generator,
) -> list:
    """Object specs for one episode.

    A single object honours the --objects/--object-scale sweep exactly.
    Multi-object episodes draw from the independent --multi-shapes and
    --multi-scale-range pools, so shape and size can each be fixed (one shape /
    equal range bounds) or varied without touching the other.
    """
    per_pad = getattr(args, "placement_mode", "per-pad") == "per-pad"

    def fit(item_shape: str, item_scale: float) -> float:
        """Clamp to what actually fits on a pad at this count.

        The --multi-scale-range pool spans 0.45-0.80 and most shapes cap below
        that at three objects, so sampling freely would hand run_episode specs it
        is bound to refuse. Clamping keeps the sweep usable instead of turning
        every multi-object episode into an error.
        """
        cap = max_scale_for(item_shape, count) if per_pad else None
        return item_scale if cap is None else min(item_scale, cap)

    if count == 1:
        scale = fit(shape, scale)
        return [ObjectSpec(shape, scale, object_mass(scale, args.object_mass))]
    low, high = args.multi_scale_range
    specs = []
    for _ in range(count):
        item_shape = str(rng.choice(args.multi_shapes))
        item_scale = fit(item_shape, float(rng.uniform(low, high)))
        specs.append(ObjectSpec(
            item_shape, item_scale, object_mass(item_scale, args.object_mass)
        ))
    return specs


def object_mass(scale: float, override: float) -> float:
    """Density-preserving mass unless an absolute mass is pinned."""
    if override > 0.0:
        return override
    return OBJECT_MASS * scale ** 3


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def apply_sparsh_calibration(args: argparse.Namespace) -> None:
    path = getattr(args, "sparsh_calibration", None)
    if path is None:
        return
    payload = json.loads(Path(path).read_text())
    noise_floor = payload["noise_floor"]
    args.sparsh_stiffness = payload["stiffness"]
    args.sparsh_damping = payload["damping"]
    args.sparsh_window = payload["window"]
    args.sparsh_use_qvel = payload["use_qvel"]
    args.sparsh_velocity_smoothing = payload["velocity_smoothing"]
    args.sparsh_activity_threshold = noise_floor["activity_threshold_n"]
    args.sparsh_min_peak_normal = noise_floor["min_peak_normal_n"]
    args.sparsh_min_contact_fraction = noise_floor["min_contact_fraction"]


def run_episode(
    specs: list, pattern: str, args: argparse.Namespace, output_dir: Path,
    rng: np.random.Generator,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    profile = profile_from_args(pattern, args)
    object_count = len(specs)
    placement_mode = getattr(args, "placement_mode", "per-pad")
    if placement_mode not in PLACEMENT_MODES:
        raise ValueError(f"Unknown placement mode '{placement_mode}'")
    if placement_mode == "per-pad":
        # Refused here rather than after a wasted episode: an over-cap object
        # provably cannot sit majority-on-pad, so retrying it never helps.
        for item in specs:
            check_placement_feasible(item.shape, item.scale, object_count)
    # One entry per object, each holding that object's geoms: a tetromino has
    # four, every primitive has one.
    geom_groups = object_geom_groups(specs)
    geom_names = [name for group in geom_groups for name in group]
    sensor_mode = getattr(args, "sensor_mode", "contact")
    if sensor_mode not in SENSOR_MODES:
        raise ValueError(f"Unknown sensor mode '{sensor_mode}'")
    main_source = primary_source(sensor_mode)
    heatmap_sources = resolve_heatmap_sources(
        sensor_mode, getattr(args, "heatmap_source", "primary")
    )
    if sparsh_enabled(sensor_mode) and getattr(args, "sparsh_calibration", None) is not None:
        apply_sparsh_calibration(args)
        args.sparsh_calibration_hash = file_sha256(args.sparsh_calibration)
    sparsh_config = make_sparsh_config(args)
    model, skins, tips = build_model(
        specs, args.palm_pitch, args.object_adhesion, args.object_adhesion_gap
    )
    object_geom_ids, object_geom_owners = resolve_object_geoms(model, geom_groups)
    timestep = model.opt.timestep
    contact_readers = (
        build_contact_readers(model, skins, tips, geom_names)
        if contact_enabled(sensor_mode)
        else []
    )
    sparsh_readers = (
        build_sparsh_readers(model, skins, tips, sparsh_config)
        if sparsh_enabled(sensor_mode)
        else []
    )
    layout = hand_layout(
        specs, args.palm_pitch, args.object_adhesion, args.object_adhesion_gap
    )

    data = mj.MjData(model)
    # Curl first, then place: the pads move as the fingers curl, and a hand that
    # snapped into the pre-grip after placement would flick the object away.
    apply_pregrip(model, data, args.pregrip_fraction)
    # Capture the fixed local grid while the hand is at rest and untouched.
    frames_ref = TaxelFrames(
        model, data, skins, tips, layout_entries_by_patch()
    )
    palm_center = palm_pad_centre(model, data)
    if placement_mode == "per-pad":
        place_objects_per_pad(
            model, data, specs, rng,
            tuple(getattr(args, "zone_weights", ZONE_WEIGHTS)),
            float(getattr(args, "min_pad_coverage", MIN_PAD_COVERAGE)),
        )
    else:
        place_objects(
            model, data, specs, args.placement_jitter, args.placement_height,
            args.orientation_random, rng,
        )

    for _ in range(int(np.ceil(args.settle_duration / timestep))):
        data.ctrl[:] = control_targets(model, 0.0, profile)
        mj.mj_step(model, data)

 
    object_addresses = [
        int(model.jnt_qposadr[int(model.body_jntadr[
            mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(i))
        ])]) for i in range(object_count)
    ]
    object_body_ids = [
        mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, object_body_name(i))
        for i in range(object_count)
    ]
    settled_held = count_held(model, data, object_body_ids, palm_center)

    hand_joint_ids = model.actuator_trnid[:, 0]
    hand_qpos_index = np.array(
        [int(model.jnt_qposadr[j]) for j in hand_joint_ids]
    )
    taxel_counts = [len(skin.taxel_ids) for skin in skins] + [
        len(tip.taxel_ids) for tip in tips
    ]
    total_taxels = TAXEL_COUNT

    def display_grids(flats: dict) -> dict:
        grids = {}
        for skin in skins:
            count_u, count_v = skin.definition.count[:2]
            grids[skin.definition.geom_name] = flats[
                skin.definition.geom_name
            ].reshape(count_u, count_v, 3)
        for tip in tips:
            grids[f"{tip.finger}_tip"] = tip_canvas(
                tip, flats[f"{tip.finger}_tip"]
            )
        return grids
    sample_count = int(args.duration * args.sample_hz)
    sample_every = max(1, round(1.0 / (args.sample_hz * timestep)))
    frame_every = max(1, round(1.0 / (VIDEO_FPS_TARGET * timestep)))

    tactile = np.zeros((sample_count, total_taxels, 3))
    tactile_contact = (
        np.zeros((sample_count, total_taxels, 3)) if contact_enabled(sensor_mode)
        else None
    )
    tactile_sparsh = (
        np.zeros((sample_count, total_taxels, 3)) if sparsh_enabled(sensor_mode)
        else None
    )
    # The same readings in flex vertex-body axes, i.e. without the
    # compression-positive normal flip. Not written to the npz -- it exists so the
    # FK layer is driven in the frame sparsh-skin-sim drives it in, and it is
    # recoverable from tactile_sparsh by negating the normal channel.
    tactile_sparsh_body = (
        np.zeros((sample_count, total_taxels, 3)) if sparsh_enabled(sensor_mode)
        else None
    )
    sparsh_flex_force = {
        item.name: np.zeros((sample_count, len(item.taxel_ids), 3))
        for item in sparsh_readers
    }
    sparsh_flex_force_sensor = {
        item.name: np.zeros((sample_count, len(item.taxel_ids), 3))
        for item in sparsh_readers
    }
    sparsh_flex_displacement = {
        item.name: np.zeros((sample_count, len(item.taxel_ids), 3))
        for item in sparsh_readers
    }
    sparsh_flex_velocity = {
        item.name: np.zeros((sample_count, len(item.taxel_ids), 3))
        for item in sparsh_readers
    }
    taxel_positions_log = np.zeros((sample_count, total_taxels, 3), np.float32)
    taxel_magnet_log = np.zeros((sample_count, total_taxels, 3), np.float32)
    taxel_normal_log = np.zeros((sample_count, total_taxels, 3), np.float32)
    tactile_times = np.zeros(sample_count)
    hand_qpos = np.zeros((sample_count, model.nu))
    ctrl_log = np.zeros((sample_count, model.nu))
    object_poses = np.zeros((sample_count, object_count, 7))
    object_vels = np.zeros((sample_count, object_count, 6))
    contact_counts = np.zeros(sample_count, dtype=np.int64)
    sparsh_active_counts = np.zeros(sample_count, dtype=np.int64)
    total_normal = np.zeros(sample_count)
    contact_total_normal = np.zeros(sample_count)
    sparsh_total_normal = np.zeros(sample_count)

    settled_index = max(0, int(CLOSE_START * args.sample_hz) - 1)
    closed_index = int(CLOSE_END * args.sample_hz) - 1
    snapshot_grids_by_source = {
        source: {"settled": None, "closed": None, "peak": None}
        for source in (("contact", "sparsh") if sensor_mode == "both" else (main_source,))
    }
    peak_normal = -1.0
    contact_peak_normal = -1.0
    sparsh_peak_normal = -1.0
    latest_by_source = {
        source: np.zeros((TAXEL_COUNT, 3))
        for source in (("contact", "sparsh") if sensor_mode == "both" else (main_source,))
    }

    # Rendering dominates episode cost (~24 s for a 5 s episode). Dataset
    # collection retries rejected episodes, so it runs with --no-video and pays
    # the render cost only for the samples it keeps.
    renderer = (
        mj.Renderer(model, height=VIDEO_HEIGHT, width=VIDEO_WIDTH)
        if args.video else None
    )
    scene_option = mj.MjvOption()
    scene_option.geomgroup[:] = 1
    cloud_renderer = (
        mj.Renderer(model, height=VIDEO_HEIGHT, width=CLOUD_WIDTH)
        if args.video and args.cloud_view else None
    )
    cloud_option = bare_scene_option()
    # One grid drives the framing, the spheres and the arrows, so they cannot
    # disagree. Both grids are logged to the npz regardless of this choice.
    cloud_local = (
        frames_ref.local_surface if args.cloud_grid == "surface"
        else frames_ref.local_magnet
    )
    cloud_sources = resolve_cloud_sources(getattr(args, "cloud_source", "leapxela"))
    # FK slot -> taxel id, for permuting taxel-id-ordered readings onto the FK cloud.
    fk_order = fk_order_to_taxel_id(TAXEL_MAP_JSON)
    # Each cloud lives in its own frame -- the leapxela one is MuJoCo taxel sites
    # in scene coordinates, the sparsh one is URDF FK in its own nominal world,
    # ~0.16 m away -- so the tracking camera needs separate state per source.
    cloud_cameras = {}
    for source in cloud_sources:
        rest = (
            frames_ref.world(data, cloud_local) if source == "leapxela"
            else fk_cloud_positions(
                hand_joint_qpos(model, data), None, args, args.cloud_deform
            )
        )
        centre = rest.mean(axis=0)
        cloud_cameras[source] = {
            "lookat": centre,
            "distance": cloud_camera_distance(
                model, float(np.max(np.linalg.norm(rest - centre, axis=1)))
            ),
        }
    orbit_lookat = palm_center + np.array([0.0, 0.0, ORBIT_LOOKAT_LIFT])
    panel = TaxelPanel(
        layout, panel_taxel_ids(skins, tips), PANEL_SIZE, PANEL_SIZE,
        TAXEL_COUNT,
    )
    marker_sensors = (
        [(skin.flex_name, skin.taxel_ids) for skin in skins]
        + [(tip.flex_name, tip.taxel_ids) for tip in tips]
    )
    dim_flex_skins(model)
    force_scale = args.force_scale
    frames = []

    total_steps = int(np.ceil(args.duration / timestep))
    sample_index = 0
    sensed_log = np.zeros((sample_count, object_count), dtype=bool)
    abort_reason = None
    t = 0.0
    for step in range(total_steps):
        t = (step + 1) * timestep
        data.ctrl[:] = control_targets(model, t, profile)
        mj.mj_step(model, data)
        # Bail out of an episode that can no longer be accepted (see
        # ABORT_CHECK_TIME). Both tests are necessary conditions for acceptance:
        # a divergence fails outright, and an object outside the hand can be
        # neither held nor sensed.
        if args.abort_check_time > 0.0 and step % sample_every == 0:
            if data.warning[mj.mjtWarning.mjWARN_BADQACC].number > 0:
                abort_reason = "divergence"
            elif t >= args.abort_check_time and count_held(
                model, data, object_body_ids, palm_center
            ) < object_count:
                abort_reason = "object_lost"
            if abort_reason is not None:
                break
        if step % sample_every == 0 and sample_index < sample_count:
            if args.object_adhesion > 0.0:
                assert_adhesion_scoped(data, object_geom_ids)
            sensed_log[sample_index] = sensed_objects(
                data, object_geom_ids, object_geom_owners
            )
            source_flats = {}
            source_grids = {}
            if contact_enabled(sensor_mode):
                contact_frame = read_contact_data(contact_readers, data)
                assert tactile_contact is not None
                tactile_contact[sample_index] = contact_frame.flat
                source_flats["contact"] = contact_frame.flat
                source_grids["contact"] = contact_frame.grids
                contact_counts[sample_index] = contact_frame.contact_count
                contact_total_normal[sample_index] = float(np.sum(contact_frame.flat[:, 2]))
            if sparsh_enabled(sensor_mode):
                sparsh_frame = read_sparsh(
                    model,
                    data,
                    sparsh_readers,
                    sparsh_config.activity_threshold,
                )
                assert tactile_sparsh is not None
                assert tactile_sparsh_body is not None
                tactile_sparsh[sample_index] = sparsh_frame.flat
                tactile_sparsh_body[sample_index] = sparsh_frame.flat_body
                source_flats["sparsh"] = sparsh_frame.flat
                source_grids["sparsh"] = sparsh_frame.grids
                sparsh_active_counts[sample_index] = sparsh_frame.active_taxels
                sparsh_total_normal[sample_index] = float(np.sum(sparsh_frame.flat[:, 2]))
                for name, values in sparsh_frame.flex_force.items():
                    sparsh_flex_force[name][sample_index] = values
                for name, values in sparsh_frame.flex_force_sensor.items():
                    sparsh_flex_force_sensor[name][sample_index] = values
                for name, values in sparsh_frame.flex_displacement.items():
                    sparsh_flex_displacement[name][sample_index] = values
                for name, values in sparsh_frame.flex_velocity.items():
                    sparsh_flex_velocity[name][sample_index] = values
            flat = source_flats[main_source]
            tactile[sample_index] = flat
            taxel_positions_log[sample_index] = frames_ref.palm(
                data, frames_ref.local_surface
            )
            taxel_magnet_log[sample_index] = frames_ref.palm(
                data, frames_ref.local_magnet
            )
            taxel_normal_log[sample_index] = frames_ref.palm_directions(
                data, frames_ref.local_normal
            )
            tactile_times[sample_index] = t
            hand_qpos[sample_index] = data.qpos[hand_qpos_index]
            ctrl_log[sample_index] = data.ctrl
            for oi, addr in enumerate(object_addresses):
                object_poses[sample_index, oi] = data.qpos[addr : addr + 7]
                dof = int(model.jnt_dofadr[int(model.body_jntadr[
                    object_body_ids[oi]
                ])])
                object_vels[sample_index, oi] = data.qvel[dof : dof + 6]
            total_normal[sample_index] = float(np.sum(flat[:, 2]))
            for source, source_flat in source_flats.items():
                latest_by_source[source] = source_flat
                if sample_index == settled_index and source in snapshot_grids_by_source:
                    snapshot_grids_by_source[source]["settled"] = display_grids(
                        source_grids[source]
                    )
                if sample_index == closed_index and source in snapshot_grids_by_source:
                    snapshot_grids_by_source[source]["closed"] = display_grids(
                        source_grids[source]
                    )
            if contact_enabled(sensor_mode) and t >= CLOSE_END:
                if contact_total_normal[sample_index] > contact_peak_normal:
                    contact_peak_normal = contact_total_normal[sample_index]
                    if "contact" in snapshot_grids_by_source:
                        snapshot_grids_by_source["contact"]["peak"] = display_grids(
                            source_grids["contact"]
                        )
            if sparsh_enabled(sensor_mode) and t >= CLOSE_END:
                if sparsh_total_normal[sample_index] > sparsh_peak_normal:
                    sparsh_peak_normal = sparsh_total_normal[sample_index]
                    if "sparsh" in snapshot_grids_by_source:
                        snapshot_grids_by_source["sparsh"]["peak"] = display_grids(
                            source_grids["sparsh"]
                        )
            if total_normal[sample_index] > peak_normal:
                peak_normal = total_normal[sample_index]
            sample_index += 1
        if renderer is not None and step % frame_every == 0:
            azimuth = ORBIT_START_AZIMUTH + 360.0 * args.orbit_revolutions * (
                t / args.duration
            )
            render_source = heatmap_sources[0]
            render_flat = latest_by_source[render_source]
            render_values = channel_values(render_flat, args.heatmap_channel)
            for source in heatmap_sources:
                source_values = channel_values(
                    latest_by_source[source], args.heatmap_channel
                )
                force_scale = max(force_scale, float(np.max(np.abs(source_values))))
            renderer.update_scene(
                data,
                camera=orbit_camera(orbit_lookat, azimuth),
                scene_option=scene_option,
            )
            # The rendered cloud is exactly the one logged to the dataset: FK
            # of the fixed local grid, in world coordinates for the renderer.
            draw_taxel_markers(
                renderer.scene,
                frames_ref.world(data, frames_ref.local_surface),
                marker_colours(render_values, args.heatmap_channel, force_scale),
                MARKER_RADIUS,
            )
            panels = [
                panel.render_labeled(
                    channel_values(latest_by_source[source], args.heatmap_channel),
                    args.heatmap_channel,
                    force_scale,
                    source,
                )
                for source in heatmap_sources
            ]
            panel_image = np.concatenate(panels, axis=1) if len(panels) > 1 else panels[0]
            frame = paste_panel(
                renderer.render(),
                panel_image,
                PANEL_MARGIN_PX,
            )
            if cloud_renderer is not None:
                cloud_frames = []
                for cloud_source in cloud_sources:
                    camera_state = cloud_cameras[cloud_source]
                    if cloud_source == "sparsh":
                        # Reproduces sparsh-skin-sim's demos/demo_fk.py view: the
                        # FK cloud coloured by force magnitude on its own per-frame
                        # scale, 1 mm dots, arrows only where the skin is loaded.
                        # It always shows the sparsh reading -- that is what the
                        # upstream viewer is -- falling back to the primary source
                        # when sparsh is not enabled.
                        driving = "sparsh" if "sparsh" in latest_by_source else main_source
                        cloud_positions, fk_world_forces = fk_cloud_frame(
                            hand_joint_qpos(model, data),
                            to_body_frame(latest_by_source[driving]),
                            args,
                            args.cloud_deform,
                        )
                        cloud_colours, _vmax = sparsh_force_colours(fk_world_forces)
                        cloud_renderer.update_scene(
                            data,
                            camera=track_cloud_camera(
                                model, camera_state, cloud_positions, azimuth
                            ),
                            scene_option=cloud_option,
                        )
                        draw_taxel_markers(
                            cloud_renderer.scene, cloud_positions, cloud_colours,
                            SPARSH_MARKER_RADIUS,
                        )
                        draw_sparsh_arrows(
                            cloud_renderer.scene, cloud_positions, fk_world_forces,
                            cloud_colours,
                        )
                        cloud_frames.append(cloud_renderer.render())
                        continue

                    cloud_positions = frames_ref.world(data, cloud_local)
                    cloud_camera = track_cloud_camera(
                        model, camera_state, cloud_positions, azimuth
                    )
                    for source in heatmap_sources:
                        source_flat = latest_by_source[source]
                        source_values = channel_values(source_flat, args.heatmap_channel)
                        cloud_renderer.update_scene(
                            data, camera=cloud_camera, scene_option=cloud_option
                        )
                        cloud_colours = marker_colours(
                            source_values, args.heatmap_channel, force_scale
                        )
                        draw_taxel_markers(
                            cloud_renderer.scene, cloud_positions, cloud_colours,
                            CLOUD_MARKER_RADIUS,
                        )
                        draw_taxel_arrows(
                            cloud_renderer.scene,
                            cloud_positions,
                            frames_ref.world_vectors(data, source_flat),
                            cloud_colours,
                            args.arrow_scale * force_scale,
                        )
                        cloud_frames.append(cloud_renderer.render())
                frame = np.concatenate([frame] + cloud_frames, axis=1)
            frames.append(frame)
    if renderer is not None:
        renderer.close()
    if cloud_renderer is not None:
        cloud_renderer.close()

    if abort_reason is not None:
        # No npz, metadata or heatmaps: the episode is rejected, and writing
        # them would only cost I/O for something the caller throws away.
        objects_held = count_held(model, data, object_body_ids, palm_center)
        print(
            f"ABORT {episode_label(specs, output_dir)}: {abort_reason} at "
            f"t={t:.2f}s of {args.duration:g}s, "
            f"held={objects_held}/{object_count}"
        )
        return {
            "passed": False,
            "aborted": True,
            "abort_reason": abort_reason,
            "abort_time_s": float(t),
            "divergences": int(
                data.warning[mj.mjtWarning.mjWARN_BADQACC].number
            ),
            "object_held": bool(objects_held > 0),
            "object_count": object_count,
            "objects_held": objects_held,
            "objects_sensed": 0,
            "peak_total_normal_n": float(max(peak_normal, 0.0)),
            "contact_peak_total_normal_n": float(max(contact_peak_normal, 0.0)),
            "sparsh_peak_total_normal_n": float(max(sparsh_peak_normal, 0.0)),
            "contact_fraction": 0.0,
            "sparsh_contact_fraction": 0.0,
            "sensor_mode": sensor_mode,
            "primary_sensor": main_source,
            "mujoco_version": mj.__version__,
        }

    for source, snapshots in snapshot_grids_by_source.items():
        for tag, grids in snapshots.items():
            if grids is None:
                continue
            suffixed = output_dir / f"hand_heatmap_{source}_{tag}.png"
            save_hand_heatmap(layout, grids, suffixed)
            if source == main_source:
                save_hand_heatmap(layout, grids, output_dir / f"hand_heatmap_{tag}.png")
    if renderer is not None:
        mediapy.write_video(
            output_dir / "grasp.mp4", frames, fps=1.0 / (frame_every * timestep)
        )

    pulse_mask = tactile_times >= CLOSE_END
    contact_fraction = (
        float(np.mean(contact_counts[pulse_mask] > 0))
        if contact_enabled(sensor_mode) else 0.0
    )
    sparsh_contact_fraction = (
        float(np.mean(sparsh_active_counts[pulse_mask] > 0))
        if sparsh_enabled(sensor_mode) else 0.0
    )
    final_distance = float(
        np.min(np.linalg.norm(object_poses[-1, :, :3] - palm_center, axis=1))
    )
    divergences = int(data.warning[mj.mjtWarning.mjWARN_BADQACC].number)
    objects_held = count_held(model, data, object_body_ids, palm_center)
    # Scored over the same post-close window as contact_fraction, and by
    # majority rather than "ever": contacts flicker, and an object that brushed
    # a pad early and then fell out is not something the taxels can be asked to
    # count. Measured on the 3-sphere baseline, "ever" gave 2 while only 1
    # object was still in the hand at the end.
    object_sensed_fraction = sensed_log[pulse_mask].mean(axis=0)
    objects_sensed = int(np.sum(object_sensed_fraction >= SENSED_FRACTION))
    held = objects_held > 0
    # Small clusters read weakly on purpose (0.04-0.3 N for 1-5 small objects
    # is expected and accepted), so multi-object episodes are not failed for a
    # faint signal -- dropping them would bias the dataset toward heavy grasps.
    # But an episode with *no* sensed contact is not weak, it is empty: it
    # carries a count label with zero tactile evidence for it, which is
    # actively wrong training data for both the shape and quantity tasks.
    contact_signal_ok = (
        contact_peak_normal >= MIN_PEAK_TOTAL_NORMAL
        and contact_fraction >= PATTERN_MIN_CONTACT[pattern]
    ) if object_count == 1 and contact_enabled(sensor_mode) else (
        contact_peak_normal >= MULTI_MIN_PEAK_NORMAL and contact_fraction > 0.0
        if contact_enabled(sensor_mode) else True
    )
    sparsh_signal_ok = (
        sparsh_peak_normal >= sparsh_config.min_peak_normal
        and sparsh_contact_fraction >= sparsh_config.min_contact_fraction
    ) if sparsh_enabled(sensor_mode) else True
    if sensor_mode == "contact":
        signal_ok = contact_signal_ok
    elif sensor_mode == "sparsh":
        signal_ok = sparsh_signal_ok
    else:
        signal_ok = contact_signal_ok and sparsh_signal_ok
    primary_peak_normal = (
        contact_peak_normal if main_source == "contact" else sparsh_peak_normal
    )
    peak_normal = primary_peak_normal
    passed = divergences == 0 and held and signal_ok

    palm_quat = np.zeros(4)
    mj.mju_mat2Quat(palm_quat, data.xmat[frames_ref.palm_id])
    skin_names = (
        [skin.definition.geom_name for skin in skins]
        + [f"{tip.finger}_tip" for tip in tips]
    )
    skin_taxel_ids = np.concatenate(
        [skin.taxel_ids for skin in skins] + [tip.taxel_ids for tip in tips]
    )
    npz_fields = dict(
        tactile=tactile,
        sensor_mode=np.asarray(sensor_mode),
        primary_sensor=np.asarray(main_source),
        schema_version=np.asarray(MODEL_SCHEMA_VERSION),
        model_variant=np.asarray(MODEL_VARIANT),
        solver_iterations=np.asarray(model.opt.iterations),
        solver_tolerance=np.asarray(model.opt.tolerance),
        # Rigid-body FK of the fixed local grid, palm frame, taxel-id order.
        taxel_positions=taxel_positions_log,
        taxel_positions_magnet=taxel_magnet_log,
        taxel_normals=taxel_normal_log,
        taxel_local_surface=frames_ref.local_surface.astype(np.float32),
        taxel_local_magnet=frames_ref.local_magnet.astype(np.float32),
        taxel_local_normal=frames_ref.local_normal.astype(np.float32),
        taxel_body_names=frames_ref.body_names.astype(str),
        palm_world_pos=data.xpos[frames_ref.palm_id].astype(np.float32),
        palm_world_quat=palm_quat.astype(np.float32),
        feature_layout=np.array(
            "sparsh 6-channel input = concatenate([tactile, taxel_positions], "
            "axis=-1) -> (T, 368, 6) as [shear_x, shear_y, normal_z, x, y, z]"
        ),
        sensor_force_frame=np.array("taxel-local; z is compression-positive"),
        position_frame=np.array("palm"),
        shape_label=np.array(specs[0].shape),
        grasp_pattern=np.array(pattern),
        shape_index=np.array(shape_index(specs[0].shape)),
        # Quantity-task labels, weakest to strongest evidence:
        #   object_count   - spawned; includes objects that fell out entirely
        #   objects_held   - still near the palm, but KINEMATIC only: an object
        #                    lying in the unsensed pocket counts here while
        #                    contributing nothing to the tactile signal
        #   objects_sensed - touched a taxel membrane at some point in the
        #                    episode; the only one the tactile data supports
        # Train quantity on objects_sensed. The others overcount by exactly the
        # objects the taxels never felt.
        object_count=np.array(object_count),
        objects_held=np.array(objects_held),
        objects_sensed=np.array(objects_sensed),
        object_sensed_fraction=object_sensed_fraction.astype(np.float32),
        object_sensed_log=sensed_log,
        mujoco_version=np.asarray(mj.__version__),
        objects_held_after_settle=np.array(settled_held),
        object_shapes=np.array([o.shape for o in specs]),
        object_shape_indices=np.array([shape_index(o.shape) for o in specs]),
        object_scales=np.array([o.scale for o in specs], dtype=np.float32),
        # For a tetromino this is the piece's local axis-aligned half-extent
        # rather than a geom size, so the field keeps its (N, 3) shape and
        # meaning across both object families. metadata.json carries the cells.
        object_sizes=np.array(
            [object_size_vector(o.shape, o.scale) for o in specs],
            dtype=np.float32,
        ),
        object_masses=np.array([o.mass for o in specs], dtype=np.float32),
        object_scale=np.array(specs[0].scale, dtype=np.float32),
        object_size=object_size_vector(specs[0].shape, specs[0].scale).astype(
            np.float32
        ),
        object_mass_kg=np.array(specs[0].mass, dtype=np.float32),
        tactile_times=tactile_times,
        skin_names=np.array(skin_names),
        skin_taxel_ids=skin_taxel_ids,
        skin_taxel_counts=np.array(taxel_counts),
        tip_grid_rowcol=np.array(TIP_GRID_ROWCOL),
        id_grid=build_layout(HAND_WORKSPACE).id_grid,
        hand_qpos=hand_qpos,
        ctrl=ctrl_log,
        object_poses=object_poses,
        object_vels=object_vels,
        object_pose=object_poses[:, 0],
        object_vel=object_vels[:, 0],
        contact_count=contact_counts,
        sparsh_active_count=sparsh_active_counts,
        total_normal=total_normal,
        contact_total_normal=contact_total_normal,
        sparsh_total_normal=sparsh_total_normal,
    )
    if tactile_contact is not None:
        npz_fields["tactile_contact"] = tactile_contact
    if tactile_sparsh is not None:
        npz_fields["tactile_sparsh"] = tactile_sparsh
        npz_fields["sparsh_stiffness"] = np.asarray(sparsh_config.stiffness)
        npz_fields["sparsh_damping"] = np.asarray(sparsh_config.damping)
        npz_fields["sparsh_window"] = np.asarray(sparsh_config.window)
        npz_fields["sparsh_velocity_smoothing"] = np.asarray(
            sparsh_config.velocity_smoothing
        )
        npz_fields["sparsh_activity_threshold"] = np.asarray(
            sparsh_config.activity_threshold
        )
        npz_fields["sparsh_min_peak_normal"] = np.asarray(
            sparsh_config.min_peak_normal
        )
        npz_fields["sparsh_min_contact_fraction"] = np.asarray(
            sparsh_config.min_contact_fraction
        )
        npz_fields["sparsh_fk_order_to_taxel_id"] = fk_order_to_taxel_id(TAXEL_MAP_JSON)
        # Every sparsh_fk/* array is in FK (link-flatten) order, NOT taxel-id
        # order -- index them through sparsh_fk_order_to_taxel_id. The force
        # frame is recorded because it changed: it used to be the flipped
        # sensor frame, and files without this key predate the fix.
        npz_fields["sparsh_fk_order"] = np.asarray("fk_link_flatten")
        npz_fields["sparsh_fk_force_frame"] = np.asarray("flex_vertex_body")
        # float64 to match sparsh-skin-sim's flex_taxel_fk/* exactly. It doubles
        # these arrays on disk -- rotations alone is (T, 368, 3, 3) -- but keeps
        # the two datasets diffable without a dtype cast.
        fk_positions = np.zeros((sample_count, TAXEL_COUNT, 3), dtype=np.float64)
        fk_rotations = np.zeros((sample_count, TAXEL_COUNT, 3, 3), dtype=np.float64)
        fk_forces_local = np.zeros((sample_count, TAXEL_COUNT, 3), dtype=np.float64)
        fk_forces_world = np.zeros((sample_count, TAXEL_COUNT, 3), dtype=np.float64)
        fk_positions_deformed = np.zeros((sample_count, TAXEL_COUNT, 3), dtype=np.float64)
        # Driven with the vertex-body forces, not the compression-positive ones:
        # sparsh-skin-sim feeds compute_fk_taxels its raw estimator output. Feeding
        # the flipped normal here inverted the normal channel of forces_local and
        # forces_world, and since deform_taxel_positions displaces along the whole
        # rotated force vector, it bent positions_deformed away from upstream too.
        for index in range(sample_count):
            fk = compute_fk_taxels(
                hand_qpos[index],
                tactile_sparsh_body[index],
                HAND_SS_URDF,
                TAXEL_MAP_JSON,
                args.sparsh_deform_scale,
                args.sparsh_max_displacement,
                True,
            )
            fk_positions[index] = fk.positions
            fk_rotations[index] = fk.rotations
            assert fk.forces_local is not None
            assert fk.forces_world is not None
            assert fk.positions_deformed is not None
            fk_forces_local[index] = fk.forces_local
            fk_forces_world[index] = fk.forces_world
            fk_positions_deformed[index] = fk.positions_deformed
        npz_fields["sparsh_fk/positions"] = fk_positions
        npz_fields["sparsh_fk/rotations"] = fk_rotations
        npz_fields["sparsh_fk/forces_local"] = fk_forces_local
        npz_fields["sparsh_fk/forces_world"] = fk_forces_world
        npz_fields["sparsh_fk/positions_deformed"] = fk_positions_deformed
        for name, values in sparsh_flex_force.items():
            npz_fields[f"sparsh_flex_force/{name}"] = values
        for name, values in sparsh_flex_force_sensor.items():
            npz_fields[f"sparsh_flex_force_sensor/{name}"] = values
        for name, values in sparsh_flex_displacement.items():
            npz_fields[f"sparsh_flex_displacement/{name}"] = values
        for name, values in sparsh_flex_velocity.items():
            npz_fields[f"sparsh_flex_velocity/{name}"] = values
    np.savez_compressed(output_dir / "sensor_log.npz", **npz_fields)
    results = {
        "passed": bool(passed),
        "aborted": False,
        "divergences": divergences,
        "object_held": bool(held),
        "object_count": object_count,
        "objects_held": objects_held,
        "objects_sensed": objects_sensed,
        "object_sensed_fraction": object_sensed_fraction.round(3).tolist(),
        "objects_held_after_settle": settled_held,
        "object_final_distance_m": final_distance,
        "peak_total_normal_n": float(peak_normal),
        "contact_peak_total_normal_n": float(max(contact_peak_normal, 0.0)),
        "sparsh_peak_total_normal_n": float(max(sparsh_peak_normal, 0.0)),
        "contact_fraction": contact_fraction,
        "sparsh_contact_fraction": sparsh_contact_fraction,
        "contact_signal_ok": bool(contact_signal_ok),
        "sparsh_signal_ok": bool(sparsh_signal_ok),
        "signal_ok": bool(signal_ok),
        "sensor_mode": sensor_mode,
        "primary_sensor": main_source,
        "object_adhesion_n": float(args.object_adhesion),
        "object_adhesion_gap_m": float(args.object_adhesion_gap),
        # MuJoCo 3.11 moved flex elasticity into the CG solver, so tactile
        # forces are not comparable across versions -- measured, the same
        # seeded episode shifts by a few percent. Recorded so a dataset can
        # never be silently mixed across a version boundary.
        "mujoco_version": mj.__version__,
    }
    metadata = {
        "shape": specs[0].shape,
        "object_scale": specs[0].scale,
        "object_count": object_count,
        "objects": [
            {"shape": o.shape, "scale": o.scale, "mass_kg": o.mass,
             "shape_index": shape_index(o.shape),
             "size": object_size_vector(o.shape, o.scale).tolist(),
             # Only tetrominoes carry these; they are what makes the piece
             # geometry recoverable from the metadata alone.
             **({"tetromino_cells": [list(c) for c in TETROMINO_CELLS[o.shape]],
                 "tetromino_block_half": TETROMINO_BLOCK_HALF * o.scale,
                 "tetromino_blocks": TETROMINO_BLOCKS}
                if is_tetromino(o.shape) else {})}
            for o in specs
        ],
        "placement_jitter": args.placement_jitter,
        "placement_height": args.placement_height,
        "settle_duration": args.settle_duration,
        "orientation_random": args.orientation_random,
        "seed": args.seed,
        "object_size": object_size_vector(specs[0].shape, specs[0].scale).tolist(),
        "object_mass_kg": specs[0].mass,
        "phases": {
            "close_start_s": CLOSE_START,
            "close_end_s": CLOSE_END,
            "duration_s": args.duration,
        },
        "grasp_pattern": pattern,
        "grip_fraction": args.grip_fraction,
        "thumb_grip_fraction": args.thumb_grip_fraction,
        "thumb_delay": args.thumb_delay,
        "pregrip_fraction": args.pregrip_fraction,
        "palm_pitch_deg": args.palm_pitch,
        "pulse_hz": args.pulse_hz,
        "pulse_amplitude": args.pulse_amplitude,
        "shear_amplitude": args.shear_amplitude,
        "squeeze_steps": args.squeeze_steps,
        "orbit_revolutions": args.orbit_revolutions,
        "heatmap_channel": args.heatmap_channel,
        "heatmap_source": getattr(args, "heatmap_source", "primary"),
        "heatmap_sources_rendered": heatmap_sources,
        "force_scale_n": force_scale,
        "cloud_view": args.cloud_view,
        "cloud_grid": args.cloud_grid,
        "arrow_scale": args.arrow_scale,
        "sample_hz": args.sample_hz,
        "tactile_shape": list(tactile.shape),
        "sensor_mode": sensor_mode,
        "primary_sensor": main_source,
        "schema_version": MODEL_SCHEMA_VERSION,
        "model_variant": MODEL_VARIANT,
        "solver": {
            "iterations": int(model.opt.iterations),
            "tolerance": float(model.opt.tolerance),
        },
        "sparsh_sensor": {
            "enabled": sparsh_enabled(sensor_mode),
            "stiffness": np.asarray(sparsh_config.stiffness).tolist(),
            "damping": np.asarray(sparsh_config.damping).tolist(),
            "window": sparsh_config.window,
            "use_qvel": sparsh_config.use_qvel,
            "velocity_smoothing": sparsh_config.velocity_smoothing,
            "activity_threshold": sparsh_config.activity_threshold,
            "min_peak_normal": sparsh_config.min_peak_normal,
            "min_contact_fraction": sparsh_config.min_contact_fraction,
            "calibration_path": sparsh_config.calibration_path,
            "calibration_hash": sparsh_config.calibration_hash,
            "urdf": str(HAND_SS_URDF),
            "taxel_order": "hardware-id for tactile arrays; sparsh_fk arrays use fk order",
            # tactile_sparsh keeps the compression-positive flip so it matches
            # tactile_contact; the FK layer is fed the unflipped estimator output
            # so it matches sparsh-skin-sim.
            "tactile_force_frame": "sensor (normal flipped compression-positive)",
            "fk_force_frame": "flex_vertex_body (matches sparsh-skin-sim)",
        },
        "taxel_positions_shape": list(taxel_positions_log.shape),
        "position_frame": "palm",
        "position_convention": (
            "rigid-body FK of a fixed local grid; taxel_positions are the "
            "sensing surface (contact happens here), taxel_positions_magnet "
            "are the calibrated magnet centres ~8-10 mm inside it"
        ),
        "results": results,
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))
    status = "PASS" if passed else "FAIL"
    label = episode_label(specs, output_dir)
    print(
        f"{status} {label}: held={objects_held}/{object_count}, "
        f"sensed={objects_sensed}/{object_count}, "
        f"peak normal={peak_normal:.3f} N, "
        f"contact fraction={contact_fraction:.2f}, "
        f"divergences={divergences}"
    )
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Grasp an object and record the flex taxel sensors."
    )
    parser.add_argument(
        "--objects", nargs="+", choices=list(PLACEABLE_SHAPES),
        default=["box", "cylinder", "disk"],
        help="primitives (box/cylinder/disk) and tetrominoes (I/O/T/L/J/S/Z). "
             "Size is capped per shape and count -- see the table in README.md",
    )
    parser.add_argument(
        "--object-scale", nargs="+", type=float, default=[1.0],
        help="object size multipliers, e.g. 0.5 1.0 1.5 (mass follows scale^3)",
    )
    parser.add_argument(
        "--object-mass", type=float, default=0.0,
        help="pin an absolute object mass in kg (0 = density-preserving)",
    )
    parser.add_argument("--duration", type=float, default=10.0)
    parser.add_argument("--sample-hz", type=float, default=100.0)
    parser.add_argument("--grip-fraction", type=float, default=0.55)
    parser.add_argument(
        "--thumb-grip-fraction", type=float, default=THUMB_GRIP_FRACTION,
        help="thumb closure target; lower than the fingers so the commanded "
             "pose does not drive the thumb into the index",
    )
    parser.add_argument(
        "--thumb-delay", type=float, default=THUMB_DELAY,
        help="seconds the thumb ramp lags the fingers",
    )
    parser.add_argument(
        "--grasp-pattern", nargs="+", choices=GRASP_PATTERNS, default=["pulse"],
        help="motion pattern(s) after closing; runs the cross-product with "
             "--objects and --object-scale",
    )
    parser.add_argument(
        "--multi-count", nargs="+", type=int, default=[1],
        help="number(s) of objects per episode; cross-producted with the "
             "other sweeps. Counts above 1 use the --multi-* pools below",
    )
    parser.add_argument(
        "--multi-shapes", nargs="+", choices=list(PLACEABLE_SHAPES),
        default=list(MULTI_SHAPES),
        help="shape pool for multi-object episodes; pass one to fix the shape",
    )
    parser.add_argument(
        "--multi-scale-range", nargs=2, type=float, default=list(MULTI_SCALE_RANGE),
        metavar=("MIN", "MAX"),
        help="scale range for multi-object episodes; equal values fix the size",
    )
    parser.add_argument(
        "--object-adhesion", type=float, default=0.0,
        help="adhesive force in N between OBJECTS ONLY, to hold a multi-object "
             "cluster together (0 = off). Never applied to object-hand or "
             "object-skin contacts, so the taxel signal is unaffected. "
             "Needs MuJoCo >= 3.11",
    )
    parser.add_argument(
        "--object-adhesion-gap", type=float, default=OBJECT_ADHESION_GAP,
        help="distance in metres over which object adhesion keeps acting. "
             "Must be > 0: at gap=0 the contact dies the instant the objects "
             "separate and adhesion does nothing at any strength",
    )
    parser.add_argument(
        "--placement-jitter", type=float, default=PLACEMENT_JITTER,
        help="half-width of the palm-plane placement region in metres",
    )
    parser.add_argument(
        "--placement-height", type=float, default=PLACEMENT_HEIGHT,
        help="vertical stagger per object; objects settle into a cluster",
    )
    parser.add_argument(
        "--settle-duration", type=float, default=SETTLE_DURATION,
        help="seconds the cluster settles before the grip closes",
    )
    parser.add_argument(
        "--orientation-random", action=argparse.BooleanOptionalAction,
        default=True,
        help="legacy placement only: uniform random orientation. per-pad always "
             "lays objects flat and randomises only the spin about the pad normal",
    )
    parser.add_argument(
        "--placement-mode", choices=PLACEMENT_MODES, default="per-pad",
        help="per-pad centres each object on a palm pad, flat, so the majority "
             "of its footprint is over taxels; legacy is the previous jittered "
             "spawn around the pad-1/pad-2 midpoint, kept for reproducing old runs",
    )
    parser.add_argument(
        "--zone-weights", type=float, nargs=2, default=list(ZONE_WEIGHTS),
        metavar=("FINGERWARD", "WRIST"),
        help="how often each placement zone is drawn: the fingerward strip "
             "(pads 1 and 2 plus the seam between them) against the wrist pad "
             "(pad 3). Raising the first leaves pad 3 empty in more episodes",
    )
    parser.add_argument(
        "--min-pad-coverage", type=float, default=MIN_PAD_COVERAGE,
        help="least fraction of an object's footprint that must sit over taxels. "
             "Lowering it allows more off-centre placements, including objects "
             "bridging the pad-1/pad-2 seam, at the cost of weaker readings",
    )
    parser.add_argument(
        "--abort-check-time", type=float, default=ABORT_CHECK_TIME,
        help="seconds after which an episode that has already lost an object "
             "is abandoned instead of simulated to the end; 0 disables",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--shear-amplitude", type=float, default=0.15)
    parser.add_argument("--squeeze-steps", type=int, default=4)
    parser.add_argument(
        "--pregrip-fraction", type=float, default=PREGRIP_FRACTION,
        help="how far the fingers are curled before the object is placed",
    )
    parser.add_argument(
        "--palm-pitch", type=float, default=PALM_PITCH_DEG,
        help="palm pitch in degrees, negative tips the fingers down",
    )
    parser.add_argument("--pulse-hz", type=float, default=1.0)
    parser.add_argument("--pulse-amplitude", type=float, default=0.15)
    parser.add_argument(
        "--orbit-revolutions", type=float, default=1.0,
        help="camera revolutions around the hand per episode (0 = fixed view)",
    )
    parser.add_argument(
        "--heatmap-channel", choices=CHANNELS, default="normal",
        help="taxel channel shown by the live heatmap in the video",
    )
    parser.add_argument(
        "--sensor-mode", choices=SENSOR_MODES, default="contact",
        help="which tactile readout to save as primary: contact, sparsh, or both",
    )
    parser.add_argument(
        "--heatmap-source", choices=("primary", "contact", "sparsh", "both"),
        default="primary",
        help="sensor source visualized in video/heatmaps; both is valid only "
             "with --sensor-mode both",
    )
    parser.add_argument(
        "--sparsh-stiffness", type=float, default=DEFAULT_FLEX_STIFFNESS,
        help="Kelvin-Voigt stiffness K used by the Sparsh batch sensor",
    )
    parser.add_argument(
        "--sparsh-damping", type=float, default=DEFAULT_FLEX_DAMPING,
        help="Kelvin-Voigt damping B used by the Sparsh batch sensor",
    )
    parser.add_argument(
        "--sparsh-window", type=int, default=DEFAULT_FORCE_WINDOW,
        help="history window for finite-difference velocity when qvel is disabled",
    )
    parser.add_argument(
        "--sparsh-use-qvel", action=argparse.BooleanOptionalAction, default=True,
        help="use MuJoCo qvel for the Sparsh velocity term",
    )
    parser.add_argument(
        "--sparsh-velocity-smoothing", type=float,
        default=DEFAULT_VELOCITY_SMOOTHING,
        help="EMA coefficient applied to the Sparsh velocity term",
    )
    parser.add_argument(
        "--sparsh-activity-threshold", type=float, default=0.005,
        help="compression-positive normal force per taxel that counts as active",
    )
    parser.add_argument(
        "--sparsh-min-peak-normal", type=float, default=0.01,
        help="minimum total normal force for pure Sparsh QA",
    )
    parser.add_argument(
        "--sparsh-min-contact-fraction", type=float, default=0.05,
        help="minimum post-close fraction with any active Sparsh taxel",
    )
    parser.add_argument(
        "--sparsh-deform-scale", type=float, default=0.02,
        help="Sparsh FK visual displacement scale in metres per Newton",
    )
    parser.add_argument(
        "--sparsh-max-displacement", type=float, default=0.015,
        help="cap for Sparsh FK force-deformed taxel positions",
    )
    parser.add_argument(
        "--sparsh-calibration", type=Path, default=None,
        help="optional calibration JSON recorded in metadata",
    )
    parser.add_argument(
        "--force-scale", type=float, default=0.5,
        help="heatmap full-scale force in N (auto-expands if exceeded)",
    )
    parser.add_argument(
        "--video", action=argparse.BooleanOptionalAction, default=True,
        help="render grasp.mp4; --no-video keeps the npz, heatmaps and "
             "metadata but skips rendering, which dominates episode cost",
    )
    parser.add_argument(
        "--cloud-view", action=argparse.BooleanOptionalAction, default=True,
        help="render the bare taxel point cloud beside the hand view",
    )
    parser.add_argument(
        "--cloud-grid", choices=CLOUD_GRIDS, default="surface",
        help="which fixed local grid the point cloud draws: the sensing "
             "surface, or the calibrated magnet centres ~8 mm inside it",
    )
    parser.add_argument(
        "--cloud-source", choices=(*CLOUD_SOURCES, "both"), default="leapxela",
        help="geometry the point cloud draws: 'leapxela' the MuJoCo taxel sites "
             "on the simulated hand, 'sparsh' the URDF forward kinematics as "
             "sparsh-skin-sim's demos/demo_fk.py shows them, 'both' side by side",
    )
    parser.add_argument(
        "--cloud-deform", action=argparse.BooleanOptionalAction, default=True,
        help="sparsh cloud only: draw force-deformed taxel positions, which is "
             "what upstream's viewer shows by default",
    )
    parser.add_argument(
        "--arrow-scale", type=float, default=1.0,
        help="force at which a cloud arrow reaches full length, "
             "as a multiple of the heatmap force scale",
    )
    parser.add_argument(
        "--output-root", type=Path,
        default=data_dir() / "leapxela_flex_grasp_test",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    failures = []
    runs = 0
    for shape in args.objects:
        for scale in args.object_scale:
            for count in args.multi_count:
                for pattern in args.grasp_pattern:
                    # Each episode gets its own stream so a run is reproducible
                    # from --seed regardless of the sweep order.
                    # zlib.crc32, not hash(): Python salts string hashes per
                    # process, so hash() would make --seed non-reproducible.
                    rng = np.random.default_rng(
                        [args.seed, zlib.crc32(shape.encode()),
                         int(scale * 1000), count,
                         GRASP_PATTERNS.index(pattern)]
                    )
                    specs = sample_specs(shape, scale, count, args, rng)
                    # Scale 1, count 1 and the default pattern keep the
                    # original directory name so existing paths stay valid.
                    name = shape if scale == 1.0 else f"{shape}_{scale:g}x"
                    if count != 1:
                        name = f"{name}_x{count}"
                    if pattern != "pulse":
                        name = f"{name}_{pattern}"
                    results = run_episode(
                        specs, pattern, args, args.output_root / name, rng
                    )
                    runs += 1
                    if not results["passed"]:
                        failures.append(name)
                    
    if failures:
        raise SystemExit(f"Grasp test failed for: {', '.join(failures)}")
    print(f"All {runs} grasp runs passed. Logs: {args.output_root}")


if __name__ == "__main__":
    main()
