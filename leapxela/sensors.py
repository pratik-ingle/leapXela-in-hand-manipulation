"""Selectable LeapXELA taxel readouts for collection and visualization."""

from dataclasses import dataclass

import mujoco as mj
import numpy as np

from leapxela.flex_force import (
    DEFAULT_FLEX_DAMPING,
    DEFAULT_FLEX_STIFFNESS,
    DEFAULT_FORCE_WINDOW,
    DEFAULT_VELOCITY_SMOOTHING,
    FlexForceEstimator,
)
from leapxela.hand_builder import FlexTaxelSensor, TAXEL_COUNT, pad_vertex_rotations


SENSOR_MODES = ("contact", "sparsh", "both")
SENSOR_SOURCES = ("contact", "sparsh")
PRIMARY_SOURCE = {"contact": "contact", "sparsh": "sparsh", "both": "contact"}
MODEL_SCHEMA_VERSION = "leapxela-dual-sensor-v1"


@dataclass(frozen=True)
class SparshSensorConfig:
    stiffness: float
    damping: float
    window: int
    use_qvel: bool
    velocity_smoothing: float
    activity_threshold: float
    min_peak_normal: float
    min_contact_fraction: float
    calibration_path: str | None
    calibration_hash: str | None


@dataclass(frozen=True)
class ContactPatchReader:
    name: str
    taxel_ids: np.ndarray
    reader: FlexTaxelSensor


@dataclass(frozen=True)
class SparshPatchFrame:
    force_sensor: np.ndarray
    force_body: np.ndarray
    displacement: np.ndarray
    velocity: np.ndarray


@dataclass(frozen=True)
class SparshPatchReader:
    name: str
    taxel_ids: np.ndarray
    estimator: FlexForceEstimator

    def read(self, model: mj.MjModel, data: mj.MjData) -> SparshPatchFrame:
        frame = self.estimator.update(model, data)
        force_sensor = np.asarray(frame.force, dtype=np.float64).copy()
        force_sensor[:, 2] = -force_sensor[:, 2]
        return SparshPatchFrame(
            force_sensor,
            frame.force.copy(),
            frame.displacement.copy(),
            frame.velocity.copy(),
        )


@dataclass(frozen=True)
class ContactReadout:
    flat: np.ndarray
    grids: dict
    contact_count: int


@dataclass(frozen=True)
class SparshReadout:
    # `flat` is the sensor convention: normal flipped so compression reads
    # positive, matching the contact sensor. `flat_body` is the same reading in
    # the flex vertex-body axes the estimator produces, which is what
    # sparsh-skin-sim works in and what the FK layer expects.
    flat: np.ndarray
    flat_body: np.ndarray
    grids: dict
    flex_force: dict[str, np.ndarray]
    flex_force_sensor: dict[str, np.ndarray]
    flex_displacement: dict[str, np.ndarray]
    flex_velocity: dict[str, np.ndarray]
    active_taxels: int


def default_sparsh_config(
    activity_threshold: float,
    min_peak_normal: float,
    min_contact_fraction: float,
    calibration_path: str | None,
    calibration_hash: str | None,
) -> SparshSensorConfig:
    return SparshSensorConfig(
        DEFAULT_FLEX_STIFFNESS,
        DEFAULT_FLEX_DAMPING,
        DEFAULT_FORCE_WINDOW,
        True,
        DEFAULT_VELOCITY_SMOOTHING,
        activity_threshold,
        min_peak_normal,
        min_contact_fraction,
        calibration_path,
        calibration_hash,
    )


def make_sparsh_config(args) -> SparshSensorConfig:
    return SparshSensorConfig(
        getattr(args, "sparsh_stiffness", DEFAULT_FLEX_STIFFNESS),
        getattr(args, "sparsh_damping", DEFAULT_FLEX_DAMPING),
        getattr(args, "sparsh_window", DEFAULT_FORCE_WINDOW),
        getattr(args, "sparsh_use_qvel", True),
        getattr(args, "sparsh_velocity_smoothing", DEFAULT_VELOCITY_SMOOTHING),
        getattr(args, "sparsh_activity_threshold", 0.005),
        getattr(args, "sparsh_min_peak_normal", 0.01),
        getattr(args, "sparsh_min_contact_fraction", 0.05),
        str(args.sparsh_calibration)
        if getattr(args, "sparsh_calibration", None) is not None else None,
        getattr(args, "sparsh_calibration_hash", None),
    )


def to_body_frame(flat: np.ndarray) -> np.ndarray:
    """Undo the compression-positive normal flip, giving flex vertex-body axes.

    Both readouts are packed compression-positive so they can be compared and
    thresholded alike, but the FK layer -- and sparsh-skin-sim throughout -- works
    in the estimator's own body axes. Anything crossing that boundary goes
    through here rather than negating z inline.
    """
    body = np.asarray(flat, dtype=np.float64).copy()
    body[:, 2] = -body[:, 2]
    return body


def contact_enabled(sensor_mode: str) -> bool:
    return sensor_mode in ("contact", "both")


def sparsh_enabled(sensor_mode: str) -> bool:
    return sensor_mode in ("sparsh", "both")


def primary_source(sensor_mode: str) -> str:
    return PRIMARY_SOURCE[sensor_mode]


def resolve_heatmap_sources(sensor_mode: str, heatmap_source: str) -> list[str]:
    if sensor_mode == "both" and heatmap_source == "both":
        return ["contact", "sparsh"]
    if heatmap_source == "primary":
        return [primary_source(sensor_mode)]
    if heatmap_source not in SENSOR_SOURCES:
        raise ValueError(f"Unknown heatmap source '{heatmap_source}'")
    if heatmap_source == "contact" and not contact_enabled(sensor_mode):
        raise ValueError("--heatmap-source contact requires contact or both mode")
    if heatmap_source == "sparsh" and not sparsh_enabled(sensor_mode):
        raise ValueError("--heatmap-source sparsh requires sparsh or both mode")
    return [heatmap_source]


def _skin_tip_items(skins: list, tips: list) -> list[tuple[str, str, str, np.ndarray, np.ndarray]]:
    items = []
    for skin in skins:
        items.append(
            (
                skin.definition.geom_name,
                skin.flex_name,
                skin.parent_body_name,
                skin.taxel_ids,
                pad_vertex_rotations(skin),
            )
        )
    for tip in tips:
        items.append(
            (
                f"{tip.finger}_tip",
                tip.flex_name,
                tip.parent_body_name,
                tip.taxel_ids,
                tip.vertex_rotations,
            )
        )
    return items


def build_contact_readers(
    model: mj.MjModel, skins: list, tips: list, contact_geom_names: list[str]
) -> list[ContactPatchReader]:
    return [
        ContactPatchReader(
            name,
            np.asarray(taxel_ids, dtype=np.int64),
            FlexTaxelSensor(model, flex_name, parent_body, rotations, contact_geom_names),
        )
        for name, flex_name, parent_body, taxel_ids, rotations in _skin_tip_items(skins, tips)
    ]


def build_sparsh_readers(
    model: mj.MjModel, skins: list, tips: list, config: SparshSensorConfig
) -> list[SparshPatchReader]:
    return [
        SparshPatchReader(
            name,
            np.asarray(taxel_ids, dtype=np.int64),
            FlexForceEstimator(
                model,
                flex_name,
                config.stiffness,
                config.damping,
                config.window,
                config.use_qvel,
                config.velocity_smoothing,
            ),
        )
        for name, flex_name, _parent_body, taxel_ids, _rotations in _skin_tip_items(skins, tips)
    ]


def read_contact_data(
    readers: list[ContactPatchReader], data: mj.MjData
) -> ContactReadout:
    flat = np.zeros((TAXEL_COUNT, 3), dtype=np.float64)
    grids = {}
    contact_count = 0
    for item in readers:
        patch_readings, contacts = item.reader.read(data)
        grids[item.name] = patch_readings
        flat[item.taxel_ids] = patch_readings
        contact_count += contacts
    return ContactReadout(flat, grids, contact_count)


def read_sparsh(
    model: mj.MjModel,
    data: mj.MjData,
    readers: list[SparshPatchReader],
    activity_threshold: float,
) -> SparshReadout:
    flat = np.zeros((TAXEL_COUNT, 3), dtype=np.float64)
    flat_body = np.zeros((TAXEL_COUNT, 3), dtype=np.float64)
    grids = {}
    flex_force = {}
    flex_force_sensor = {}
    flex_displacement = {}
    flex_velocity = {}
    active_taxels = 0
    for item in readers:
        frame = item.read(model, data)
        flat[item.taxel_ids] = frame.force_sensor
        # Packed from the estimator output rather than by un-flipping `flat`, so
        # the two stay correct independently of the sign convention above.
        flat_body[item.taxel_ids] = frame.force_body
        grids[item.name] = frame.force_sensor
        flex_force[item.name] = frame.force_body
        flex_force_sensor[item.name] = frame.force_sensor
        flex_displacement[item.name] = frame.displacement
        flex_velocity[item.name] = frame.velocity
        active_taxels += int(np.count_nonzero(frame.force_sensor[:, 2] > activity_threshold))
    return SparshReadout(
        flat,
        flat_body,
        grids,
        flex_force,
        flex_force_sensor,
        flex_displacement,
        flex_velocity,
        active_taxels,
    )
