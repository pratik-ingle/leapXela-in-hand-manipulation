# mjpython sim/static_retarget_test.py
import os
import time
import numpy as np
import mujoco as mj
import mujoco.viewer
from dex_retargeting.retargeting_config import RetargetingConfig
from dex_retargeting.constants import (
    get_default_config_path, RobotName, RetargetingType, HandType,
)

SCENE    = "/Users/pratik/Documents/PhD/Research_stay/leapXela/LeapXELA_Hardware_ws-main/mujoco_c_example/mjcf/scene.xml"
URDF_DIR = "/Users/pratik/Documents/PhD/Research_stay/leapXela/sim/dex-urdf/robots/hands"

# --- 1. Build retargeter ---
RetargetingConfig.set_default_urdf_dir(URDF_DIR)
cfg_path = get_default_config_path(RobotName.leap, RetargetingType.vector, HandType.right)
retargeter = RetargetingConfig.load_from_file(
    str(cfg_path),
    override={"low_pass_alpha": -1},  # disable filtering for this static inversion test
).build()
print("retargeter joints:", retargeter.joint_names)

# --- 2. Build MuJoCo model ---
model = mj.MjModel.from_xml_path(SCENE)
data  = mj.MjData(model)

# --- 3. Map retargeter joint name -> MuJoCo actuator id.
#     Fill this in *after* running inspect_leapjoint_name.py.
#     LEAP's URDF typically names joints "0".."15"; we map those to LeapXela's *_act names.
JOINT_TO_ACT = {
    "1":  "if_mcp_act",
    "0":  "if_rot_act",
    "2":  "if_pip_act",
    "3":  "if_dip_act",
    "5":  "mf_mcp_act",
    "4":  "mf_rot_act",
    "6":  "mf_pip_act",
    "7":  "mf_dip_act",
    "9":  "rf_mcp_act",
    "8":  "rf_rot_act",
    "10":  "rf_pip_act",
    "11":  "rf_dip_act",
    "12":  "th_cmc_act",
    "13":  "th_axl_act",
    "14":  "th_mcp_act",
    "15":  "th_ipl_act",
}

joint_to_actuator = []
for jn in retargeter.joint_names:
    act_name = JOINT_TO_ACT.get(jn)
    aid = mj.mj_name2id(model, mj.mjtObj.mjOBJ_ACTUATOR, act_name) if act_name else -1
    joint_to_actuator.append(aid if aid >= 0 else None)
    print(f"{jn:>20s} -> {act_name}  (actuator id {aid})")

# --- 4. Two static poses ---
# ---- Build canonical 4-vec targets from the LEAP URDF itself ----
robot = retargeter.optimizer.robot
scale = retargeter.optimizer.scaling     # 1.6 from YAML

# 1) Robot at full extension: all joints = 0
def L(name):
    return robot.get_link_pose(robot.get_link_index(name))[:3, 3]

origin_link_names = retargeter.optimizer.origin_link_names
task_link_names = retargeter.optimizer.task_link_names

def target_from_qpos(qpos):
    robot.compute_forward_kinematics(qpos.astype(np.float32))
    origin_pos = np.stack([L(name) for name in origin_link_names])
    task_pos = np.stack([L(name) for name in task_link_names])
    return ((task_pos - origin_pos) / scale).astype(np.float32)

qpos_open_robot = np.zeros(robot.dof, dtype=np.float32)
open_target = target_from_qpos(qpos_open_robot)

# 2) Curled target: midpoint of the robot joint limits.
limits = robot.joint_limits               # (dof, 2) Pinocchio order
qpos_curl = limits.mean(axis=1).astype(np.float32)   # midpoint = visibly curled
fist_target = target_from_qpos(qpos_curl)

print("open_target (4,3):\n", np.round(open_target, 3))
print("fist_target (4,3):\n", np.round(fist_target, 3))

def stable_retarget(target_vec, initial_qpos, n=20):
    # This static test uses targets generated from known robot qpos. Warm-start
    # from that same qpos so the optimizer returns the intended inverse solution.
    retargeter.set_qpos(initial_qpos.astype(np.float32))
    for _ in range(n):
        q = retargeter.retarget(target_vec)
    return q

qpos_open = stable_retarget(open_target, qpos_open_robot)
retargeter.reset()
qpos_fist = stable_retarget(fist_target, qpos_curl)
retargeter.reset()
print("open qpos:", np.round(qpos_open, 2))
print("fist qpos:", np.round(qpos_fist, 2))

# --- 5. Apply to MuJoCo and toggle every 2 s ---
def apply(qpos):
    for aid, q in zip(joint_to_actuator, qpos):
        if aid is not None:
            data.ctrl[aid] = float(q)

with mujoco.viewer.launch_passive(model=model, data=data,
                                  show_left_ui=False, show_right_ui=True) as viewer:
    mj.mjv_defaultFreeCamera(model, viewer.cam)
    apply(qpos_open)
    showing = "OPEN"
    last = time.time()
    while viewer.is_running():
        t = time.time()
        if t - last > 2.0:
            showing = "FIST" if showing == "OPEN" else "OPEN"
            apply(qpos_fist if showing == "FIST" else qpos_open)
            last = t
            print(f"-> {showing}")
        mj.mj_step(model, data)
        viewer.sync()
        dt_left = model.opt.timestep - (time.time() - t)
        if dt_left > 0:
            time.sleep(dt_left)