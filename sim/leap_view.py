import time
import mujoco as mj
import mujoco.viewer

scene = "/Users/pratik/Documents/PhD/Research_stay/leapXela/LeapXELA_Hardware_ws-main/mujoco_c_example/mjcf/scene.xml"

# spec = mj.MjSpec.from_file(scene)
# model = spec.compile()
model = mj.MjModel.from_xml_path(scene)
data = mj.MjData(model)

with mujoco.viewer.launch_passive(
    model=model, data=data, show_left_ui=True, show_right_ui=True
) as viewer:
    mj.mjv_defaultFreeCamera(model, viewer.cam)
    mj.mj_forward(model, data)
    while viewer.is_running():
        step_start = time.time()
        
        mj.mj_step(model, data)
        viewer.sync()
        
        # real-time pacing 
        dt_left = model.opt.timestep - (time.time() - step_start)
        if dt_left > 0:
            time.sleep(dt_left)