"""Kelvin-Voigt force estimates for LeapXELA flex taxels.

This is the Sparsh batch sensor core adapted to the packaged LeapXELA model:
per-vertex slide displacement and velocity are converted to force with
``f = K u + B v``.  Outputs are in each vertex body's local axes; the generated
hand now aligns those bodies to the taxel frames.
"""

from collections import deque
from dataclasses import dataclass

import mujoco as mj
import numpy as np


DEFAULT_FLEX_STIFFNESS = 100.0
DEFAULT_FLEX_DAMPING = 0.05
DEFAULT_FORCE_WINDOW = 5
DEFAULT_VELOCITY_SMOOTHING = 0.3


def flex_id(model: mj.MjModel, flex_name: str) -> int:
    found = mj.mj_name2id(model, mj.mjtObj.mjOBJ_FLEX, flex_name)
    if found < 0:
        raise ValueError(f"Flex '{flex_name}' not found")
    return int(found)


def list_flex_names(model: mj.MjModel) -> list[str]:
    names = []
    for index in range(model.nflex):
        name = mj.mj_id2name(model, mj.mjtObj.mjOBJ_FLEX, index)
        if name is not None:
            names.append(name)
    return names


def flex_vertex_body_ids(model: mj.MjModel, flex_name: str) -> np.ndarray:
    fid = flex_id(model, flex_name)
    address = int(model.flex_vertadr[fid])
    count = int(model.flex_vertnum[fid])
    return np.asarray(model.flex_vertbodyid[address : address + count], dtype=np.int32)


def flex_joint_ids(model: mj.MjModel, flex_name: str) -> np.ndarray:
    body_ids = flex_vertex_body_ids(model, flex_name)
    joint_ids = []
    for body_id in body_ids:
        start = int(model.body_jntadr[int(body_id)])
        count = int(model.body_jntnum[int(body_id)])
        if count != 3:
            raise ValueError(
                f"Flex '{flex_name}' vertex body {int(body_id)} has {count} joints"
            )
        joint_ids.append(np.arange(start, start + count, dtype=np.int32))
    return np.stack(joint_ids, axis=0)


def _joint_qpos_width(joint_type: int) -> int:
    if joint_type == int(mj.mjtJoint.mjJNT_FREE):
        return 7
    if joint_type == int(mj.mjtJoint.mjJNT_BALL):
        return 4
    return 1


def flex_joint_qpos_dof_addresses(
    model: mj.MjModel, flex_name: str
) -> tuple[np.ndarray, np.ndarray, tuple[int, int]]:
    joint_ids = flex_joint_ids(model, flex_name)
    flat = joint_ids.reshape(-1)
    for joint_id in flat:
        if _joint_qpos_width(int(model.jnt_type[int(joint_id)])) != 1:
            raise ValueError(
                f"Flex '{flex_name}' joint {int(joint_id)} is not a scalar slide joint"
            )
    qpos_address = np.asarray(model.jnt_qposadr[flat], dtype=np.int32)
    dof_address = np.asarray(model.jnt_dofadr[flat], dtype=np.int32)
    return qpos_address, dof_address, joint_ids.shape


def flex_joint_displacements(model: mj.MjModel, data: mj.MjData, flex_name: str) -> np.ndarray:
    qpos_address, _, shape = flex_joint_qpos_dof_addresses(model, flex_name)
    return (
        np.asarray(data.qpos[qpos_address] - model.qpos0[qpos_address], dtype=np.float64)
        .reshape(shape)
    )


def flex_joint_velocities(model: mj.MjModel, data: mj.MjData, flex_name: str) -> np.ndarray:
    _, dof_address, shape = flex_joint_qpos_dof_addresses(model, flex_name)
    return np.asarray(data.qvel[dof_address], dtype=np.float64).reshape(shape)


def _as_coeff(coeff: float | np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    array = np.asarray(coeff, dtype=np.float64)
    if array.ndim == 0:
        return np.full(shape, float(array), dtype=np.float64)
    if array.shape == shape:
        return array
    if array.shape == (shape[-1],):
        return np.broadcast_to(array, shape).copy()
    if array.shape == (shape[0], 1) or array.shape == (shape[0],):
        return np.broadcast_to(array.reshape(shape[0], 1), shape).copy()
    raise ValueError(f"Coefficient shape {array.shape} cannot broadcast to {shape}")


def kelvin_voigt_force(
    displacement: np.ndarray,
    velocity: np.ndarray,
    stiffness: float | np.ndarray,
    damping: float | np.ndarray,
) -> np.ndarray:
    displacement = np.asarray(displacement, dtype=np.float64)
    velocity = np.asarray(velocity, dtype=np.float64)
    if displacement.shape != velocity.shape:
        raise ValueError(
            f"displacement shape {displacement.shape} != velocity shape {velocity.shape}"
        )
    stiffness_array = _as_coeff(stiffness, displacement.shape)
    damping_array = _as_coeff(damping, displacement.shape)
    return stiffness_array * displacement + damping_array * velocity


def fit_kelvin_voigt(
    displacements: np.ndarray,
    velocities: np.ndarray,
    forces: np.ndarray,
    per_axis: bool,
) -> tuple[np.ndarray, np.ndarray]:
    u = np.asarray(displacements, dtype=np.float64)
    v = np.asarray(velocities, dtype=np.float64)
    f = np.asarray(forces, dtype=np.float64)
    if u.shape != v.shape or u.shape != f.shape:
        raise ValueError("displacements, velocities and forces must share a shape")
    if u.ndim == 2:
        u, v, f = u[None], v[None], f[None]
    if u.ndim != 3 or u.shape[-1] != 3:
        raise ValueError(f"Expected (T, n_vert, 3), got {u.shape}")
    if per_axis:
        stiffness = np.empty(3, dtype=np.float64)
        damping = np.empty(3, dtype=np.float64)
        for axis in range(3):
            design = np.column_stack((u[..., axis].ravel(), v[..., axis].ravel()))
            coeff, *_ = np.linalg.lstsq(design, f[..., axis].ravel(), rcond=None)
            stiffness[axis], damping[axis] = coeff
        return stiffness, damping
    design = np.column_stack((u.ravel(), v.ravel()))
    coeff, *_ = np.linalg.lstsq(design, f.ravel(), rcond=None)
    return np.asarray(coeff[0]), np.asarray(coeff[1])


def flex_vertex_contact_forces(
    model: mj.MjModel,
    data: mj.MjData,
    flex_name: str,
    contact_geom_names: list[str],
) -> tuple[np.ndarray, int]:
    """Ground-truth contact-force labels in vertex-body axes."""
    fid = flex_id(model, flex_name)
    vert_adr = int(model.flex_vertadr[fid])
    vert_num = int(model.flex_vertnum[fid])
    body_ids = flex_vertex_body_ids(model, flex_name)
    contact_geom_ids = set()
    for name in contact_geom_names:
        geom_id = mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, name)
        if geom_id < 0:
            raise ValueError(f"Contact geom '{name}' not found")
        contact_geom_ids.add(int(geom_id))

    element_count = int(model.flex_elemnum[fid])
    data_address = int(model.flex_elemdataadr[fid])
    elements = model.flex_elem[
        data_address : data_address + 3 * element_count
    ].reshape(element_count, 3)

    forces_world = np.zeros((vert_num, 3), dtype=np.float64)
    wrench = np.zeros(6, dtype=np.float64)
    contact_count = 0
    for contact_id in range(data.ncon):
        contact = data.contact[contact_id]
        flex_sides = (int(contact.flex[0]), int(contact.flex[1]))
        if fid not in flex_sides:
            continue
        side = flex_sides.index(fid)
        other_geom = int(contact.geom[1 - side])
        if other_geom not in contact_geom_ids:
            continue
        mj.mj_contactForce(model, data, contact_id, wrench)
        force_world = contact.frame.reshape(3, 3).T @ wrench[:3]
        if side == 0:
            force_world = -force_world
        for vertex_id, weight in _flex_contact_vertex_weights(
            model, data, contact, side, vert_adr, vert_num, elements
        ):
            forces_world[vertex_id] += weight * force_world
        contact_count += 1

    forces_local = np.zeros_like(forces_world)
    for index, body_id in enumerate(body_ids):
        rotation = data.xmat[int(body_id)].reshape(3, 3)
        forces_local[index] = rotation.T @ forces_world[index]
    return forces_local, contact_count


def _flex_contact_vertex_weights(
    model: mj.MjModel,
    data: mj.MjData,
    contact: mj.MjContact,
    side: int,
    vert_adr: int,
    vert_num: int,
    elements: np.ndarray,
) -> list[tuple[int, float]]:
    vertex = int(contact.vert[side])
    if 0 <= vertex < vert_num:
        return [(vertex, 1.0)]
    element = int(contact.elem[side])
    if element < 0 or element >= len(elements):
        vertices = data.flexvert_xpos[vert_adr : vert_adr + vert_num]
        distances = np.linalg.norm(vertices - contact.pos[None, :], axis=1)
        return [(int(np.argmin(distances)), 1.0)]
    triangle = elements[element]
    points = data.flexvert_xpos[vert_adr + triangle]
    basis = np.column_stack((points[1] - points[0], points[2] - points[0]))
    offsets, *_ = np.linalg.lstsq(basis, contact.pos - points[0], rcond=None)
    weights = np.array(
        [1.0 - offsets[0] - offsets[1], offsets[0], offsets[1]], dtype=np.float64
    )
    weights = np.clip(weights, 0.0, None)
    total = float(weights.sum())
    if total <= 0.0:
        weights[:] = 1.0 / 3.0
    else:
        weights /= total
    return [(int(triangle[index]), float(weights[index])) for index in range(3)]


@dataclass(frozen=True)
class FlexForceFrame:
    force: np.ndarray
    displacement: np.ndarray
    velocity: np.ndarray


class FlexForceEstimator:
    """Online Kelvin-Voigt estimator for one flex."""

    def __init__(
        self,
        model: mj.MjModel,
        flex_name: str,
        stiffness: float | np.ndarray,
        damping: float | np.ndarray,
        window: int,
        use_qvel: bool,
        velocity_smoothing: float,
    ) -> None:
        if window < 2:
            raise ValueError("window must be >= 2")
        self.flex_name = flex_name
        self.stiffness = stiffness
        self.damping = damping
        self.window = int(window)
        self.use_qvel = bool(use_qvel)
        self.velocity_smoothing = float(np.clip(velocity_smoothing, 0.0, 1.0))
        self._qadr, self._dadr, self._shape = flex_joint_qpos_dof_addresses(
            model, flex_name
        )
        self._u_hist: deque[np.ndarray] = deque(maxlen=self.window)
        self._t_hist: deque[float] = deque(maxlen=self.window)
        self._v_smooth: np.ndarray | None = None
        if isinstance(damping, (float, int)) and float(damping) == DEFAULT_FLEX_DAMPING:
            joint_ids = flex_joint_ids(model, flex_name)
            dof = model.jnt_dofadr[joint_ids.reshape(-1)]
            self.damping = float(np.mean(model.dof_damping[dof]))

    def reset(self) -> None:
        self._u_hist.clear()
        self._t_hist.clear()
        self._v_smooth = None

    def set_gains(self, stiffness: float | np.ndarray, damping: float | np.ndarray) -> None:
        self.stiffness = stiffness
        self.damping = damping

    def calibrate(
        self,
        displacements: np.ndarray,
        velocities: np.ndarray,
        forces: np.ndarray,
        per_axis: bool,
    ) -> tuple[np.ndarray, np.ndarray]:
        stiffness, damping = fit_kelvin_voigt(
            displacements, velocities, forces, per_axis
        )
        self.set_gains(stiffness, damping)
        return stiffness, damping

    def update(self, model: mj.MjModel, data: mj.MjData) -> FlexForceFrame:
        displacement = np.asarray(
            data.qpos[self._qadr] - model.qpos0[self._qadr], dtype=np.float64
        ).reshape(self._shape)
        self._u_hist.append(displacement.copy())
        self._t_hist.append(float(data.time))
        if self.use_qvel:
            velocity = np.asarray(data.qvel[self._dadr], dtype=np.float64).reshape(
                self._shape
            )
        else:
            velocity = self._velocity_from_history()
        if self._v_smooth is None or self.velocity_smoothing <= 0.0:
            self._v_smooth = velocity.copy()
        else:
            alpha = self.velocity_smoothing
            self._v_smooth = (1.0 - alpha) * self._v_smooth + alpha * velocity
        force = kelvin_voigt_force(
            displacement, self._v_smooth, self.stiffness, self.damping
        )
        return FlexForceFrame(force, displacement, self._v_smooth.copy())

    def _velocity_from_history(self) -> np.ndarray:
        if len(self._u_hist) < 2:
            return np.zeros(self._shape, dtype=np.float64)
        dt = self._t_hist[-1] - self._t_hist[-2]
        if dt <= 0.0:
            return np.zeros(self._shape, dtype=np.float64)
        return (self._u_hist[-1] - self._u_hist[-2]) / dt


class AllFlexForceEstimator:
    """Kelvin-Voigt estimators for a known list of flexes."""

    def __init__(
        self,
        model: mj.MjModel,
        flex_names: list[str],
        stiffness: float | np.ndarray,
        damping: float | np.ndarray,
        window: int,
        use_qvel: bool,
        velocity_smoothing: float,
    ) -> None:
        self.estimators = {
            name: FlexForceEstimator(
                model, name, stiffness, damping, window, use_qvel, velocity_smoothing
            )
            for name in flex_names
        }

    def reset(self) -> None:
        for estimator in self.estimators.values():
            estimator.reset()

    def update(self, model: mj.MjModel, data: mj.MjData) -> dict[str, FlexForceFrame]:
        return {
            name: estimator.update(model, data)
            for name, estimator in self.estimators.items()
        }
