# mjpython sim/tools/inspect_leapjoint_name.py
import os
import mujoco as mj
from dex_retargeting.retargeting_config import RetargetingConfig
from dex_retargeting.constants import (
    get_default_config_path, RobotName, RetargetingType, HandType,
)

SCENE = "/Users/pratik/Documents/PhD/Research_stay/leapXela/LeapXELA_Hardware_ws-main/mujoco_c_example/mjcf/scene.xml"
URDF_DIR = "/Users/pratik/Documents/PhD/Research_stay/leapXela/sim/dex-urdf/robots/hands"

# --- MuJoCo actuators ---
model = mj.MjModel.from_xml_path(SCENE)
print("=== MuJoCo actuators ===")
for i in range(model.nu):
    print(f"{i:2d}  {mj.mj_id2name(model, mj.mjtObj.mjOBJ_ACTUATOR, i)}")

# --- Retargeter joints ---
RetargetingConfig.set_default_urdf_dir(URDF_DIR)
cfg_path = get_default_config_path(
    RobotName.leap, RetargetingType.vector, HandType.right
)
print(f"\n=== Retargeter config ===\n{cfg_path}")
retargeter = RetargetingConfig.load_from_file(str(cfg_path)).build()
print("\n=== Retargeter joint names (in robot_qpos output order) ===")
for i, n in enumerate(retargeter.joint_names):
    print(f"{i:2d}  {n}")
print(f"\nrobot.dof = {retargeter.optimizer.robot.dof}")