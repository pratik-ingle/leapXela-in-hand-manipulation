import multiprocessing
import queue
import signal
import threading
import time
from pathlib import Path

import cv2
import mediapipe as mp
import mujoco as mj
import mujoco.viewer
import numpy as np
from dex_retargeting.constants import (
    HandType,
    RetargetingType,
    RobotName,
    get_default_config_path,
)
from dex_retargeting.retargeting_config import RetargetingConfig
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


SIM_DIR = Path(__file__).resolve().parent
REPO_ROOT = SIM_DIR.parent

SCENE = REPO_ROOT / "LeapXELA_Hardware_ws-main" / "mujoco_c_example" / "mjcf" / "scene.xml"
URDF_DIR = (
    REPO_ROOT
    / "LeapXELA_Hardware_ws-main"
    / "ros_ws"
    / "src"
    / "xela_telelop"
    / "dex_retargeting"
    / "assets"
    / "robots"
    / "hands"
)
MODEL_PATH = SIM_DIR / "assets" / "hand_landmarker.task"

# MediaPipe landmarks used by the LEAP vector-retargeting config:
# [thumb_tip, index_tip, middle_tip, ring_tip]
TIP_IDS = [4, 8, 12, 16]
WRIST_ID = 0
PALM_SCALE_ID = 9

HAND_CONNECTIONS = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (0, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (0, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (0, 17),
    (17, 18),
    (18, 19),
    (19, 20),
    (5, 9),
    (9, 13),
    (13, 17),
]


JOINT_TO_ACT = {
    "1": "if_mcp_act",
    "0": "if_rot_act",
    "2": "if_pip_act",
    "3": "if_dip_act",
    "5": "mf_mcp_act",
    "4": "mf_rot_act",
    "6": "mf_pip_act",
    "7": "mf_dip_act",
    "9": "rf_mcp_act",
    "8": "rf_rot_act",
    "10": "rf_pip_act",
    "11": "rf_dip_act",
    "12": "th_cmc_act",
    "13": "th_axl_act",
    "14": "th_mcp_act",
    "15": "th_ipl_act",
}


def draw_landmarks(frame, landmarks):
    h, w = frame.shape[:2]
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], (0, 200, 0), 2)
    for pt in pts:
        cv2.circle(frame, pt, 4, (0, 0, 255), -1)


def camera_preview_worker(frame_queue, stop_event):
    """Show camera frames in a separate process to avoid macOS GUI conflicts."""
    # Let the parent process handle Ctrl-C and perform cleanup.
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    window_name = "LeapXela webcam control"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    try:
        while not stop_event.is_set():
            try:
                frame = frame_queue.get(timeout=0.1)
            except queue.Empty:
                key = cv2.waitKey(1) & 0xFF
                if key in (27, ord("q")):
                    stop_event.set()
                    break
                continue

            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1) & 0xFF

            try:
                window_open = cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 1
            except cv2.error:
                window_open = False

            if key in (27, ord("q")) or not window_open:
                stop_event.set()
                break
    finally:
        cv2.destroyAllWindows()


def enqueue_latest(frame_queue, frame):
    """Keep only the newest preview frame so rendering cannot block control."""
    if frame_queue.full():
        try:
            frame_queue.get_nowait()
        except queue.Empty:
            pass
    try:
        frame_queue.put_nowait(frame.copy())
    except queue.Full:
        pass


def finger_lengths(kp):
    """Return thumb/index/middle/ring openness proxies, normalized by palm size."""
    palm = np.linalg.norm(kp[PALM_SCALE_ID] - kp[WRIST_ID]) + 1e-6
    return np.array(
        [np.linalg.norm(kp[tip_id] - kp[WRIST_ID]) for tip_id in TIP_IDS],
        dtype=np.float32,
    ) / palm


def start_command_reader():
    """Read line-based commands from the terminal without blocking simulation."""
    command_queue = queue.Queue()

    def worker():
        while True:
            try:
                command = input().strip().lower()
            except EOFError:
                command = "q"
            command_queue.put(command)
            if command in {"q", "quit", "exit"}:
                break

    threading.Thread(target=worker, daemon=True).start()
    return command_queue


def main():
    RetargetingConfig.set_default_urdf_dir(str(URDF_DIR))
    cfg_path = get_default_config_path(
        RobotName.leap, RetargetingType.vector, HandType.right
    )
    retargeter = RetargetingConfig.load_from_file(str(cfg_path)).build()
    print("retargeter joints:", retargeter.joint_names)

    model = mj.MjModel.from_xml_path(str(SCENE))
    data = mj.MjData(model)

    joint_to_actuator = []
    for joint_name in retargeter.joint_names:
        act_name = JOINT_TO_ACT.get(joint_name)
        actuator_id = (
            mj.mj_name2id(model, mj.mjtObj.mjOBJ_ACTUATOR, act_name)
            if act_name
            else -1
        )
        joint_to_actuator.append(actuator_id if actuator_id >= 0 else None)
        print(f"{joint_name:>20s} -> {act_name}  (actuator id {actuator_id})")

    def apply(qpos):
        for actuator_id, q in zip(joint_to_actuator, qpos):
            if actuator_id is not None:
                data.ctrl[actuator_id] = float(q)

    robot = retargeter.optimizer.robot
    scale = retargeter.optimizer.scaling
    origin_link_names = retargeter.optimizer.origin_link_names
    task_link_names = retargeter.optimizer.task_link_names

    def link_pos(name):
        return robot.get_link_pose(robot.get_link_index(name))[:3, 3]

    def target_from_qpos(qpos):
        robot.compute_forward_kinematics(qpos.astype(np.float32))
        origin_pos = np.stack([link_pos(name) for name in origin_link_names])
        task_pos = np.stack([link_pos(name) for name in task_link_names])
        return ((task_pos - origin_pos) / scale).astype(np.float32)

    qpos_open_robot = np.zeros(robot.dof, dtype=np.float32)
    limits = robot.joint_limits
    # qpos_curl = limits.mean(axis=1).astype(np.float32)
    # qpos_curl = limits[:, 1].astype(np.float32)
    # qpos_curl[[0, 4, 8]] = 0.0
    qpos_curl = np.array([
    1.35,  # joint 1  -> if_mcp_act
    0.00,  # joint 0  -> if_rot_act
    1.08,  # joint 2  -> if_pip_act
    1.86,  # joint 3  -> if_dip_act

    1.48,  # joint 12 -> th_cmc_act
    1.37,  # joint 13 -> th_axl_act
    1.04,  # joint 14 -> th_mcp_act
    1.36,  # joint 15 -> th_ipl_act

    1.35,  # joint 5  -> mf_mcp_act
    0.00,  # joint 4  -> mf_rot_act
    1.08,  # joint 6  -> mf_pip_act
    1.86,  # joint 7  -> mf_dip_act

    1.35,  # joint 9  -> rf_mcp_act
    0.00,  # joint 8  -> rf_rot_act
    1.08,  # joint 10 -> rf_pip_act
    1.86,  # joint 11 -> rf_dip_act
    ], dtype=np.float32)

    open_target = target_from_qpos(qpos_open_robot)
    fist_target = target_from_qpos(qpos_curl)

    open_len = None
    fist_len = None
    alpha_smooth = np.ones(4, dtype=np.float32)
    latest_alpha = None

    base_options = python.BaseOptions(model_asset_path=str(MODEL_PATH))
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.6,
    )

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam 0")

    retargeter.set_qpos(qpos_open_robot)
    apply(qpos_open_robot)
    commands = start_command_reader()
    frame_queue = multiprocessing.Queue(maxsize=1)
    preview_stop = multiprocessing.Event()
    preview_process = multiprocessing.Process(
        target=camera_preview_worker,
        args=(frame_queue, preview_stop),
        daemon=True,
    )
    preview_process.start()

    latest_lengths = None
    should_quit = False

    print("\nTerminal commands:")
    print("  o + Enter: calibrate current hand as open")
    print("  c + Enter: calibrate current hand as fist")
    print("  q + Enter: quit")
    print("Camera preview: press q or Esc in the preview window to close it and quit")
    print("Keep your hand visible to the webcam while calibrating.\n")

    try:
        with vision.HandLandmarker.create_from_options(options) as landmarker:
            with mujoco.viewer.launch_passive(
                model=model,
                data=data,
                show_left_ui=False,
                show_right_ui=True,
            ) as viewer:
                mj.mjv_defaultFreeCamera(model, viewer.cam)

                while viewer.is_running() and not should_quit and not preview_stop.is_set():
                    step_start = time.time()
                    ok, frame = cap.read()

                    if ok:
                        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                        result = landmarker.detect(mp_image)

                        if result.hand_landmarks:
                            landmarks = result.hand_landmarks[0]
                            draw_landmarks(frame, landmarks)
                            kp = np.array(
                                [[lm.x, lm.y, lm.z] for lm in landmarks],
                                dtype=np.float32,
                            )
                            latest_lengths = finger_lengths(kp)

                            if open_len is not None and fist_len is not None:
                                alpha = (latest_lengths - fist_len) / (
                                    open_len - fist_len + 1e-6
                                )
                                alpha = np.clip(alpha, 0.0, 1.0)

                                # Mild smoothing on top of dex-retargeting's internal LPF.
                                alpha_smooth = 0.7 * alpha_smooth + 0.3 * alpha

                                target_vec = (
                                    alpha_smooth[:, None] * open_target
                                    + (1.0 - alpha_smooth[:, None]) * fist_target
                                )
                                qpos = retargeter.retarget(target_vec)
                                apply(qpos)
                                latest_alpha = alpha_smooth.copy()

                        cv2.putText(
                            frame,
                            "terminal: o=open, c=fist, q=quit | preview: q/esc=quit",
                            (20, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2,
                        )
                        if latest_alpha is not None:
                            cv2.putText(
                                frame,
                                "alpha " + " ".join(f"{a:.2f}" for a in latest_alpha),
                                (20, 60),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                (255, 255, 0),
                                2,
                            )
                        enqueue_latest(frame_queue, frame)

                    while not commands.empty():
                        command = commands.get()
                        if command in {"q", "quit", "exit"}:
                            should_quit = True
                            break
                        if latest_lengths is None:
                            print("No hand detected yet; keep your hand visible and try again.")
                            continue
                        if command == "o":
                            open_len = latest_lengths.copy()
                            alpha_smooth[:] = 1.0
                            retargeter.set_qpos(qpos_open_robot)
                            print("calibrated open:", np.round(open_len, 3))
                        elif command == "c":
                            fist_len = latest_lengths.copy()
                            print("calibrated fist:", np.round(fist_len, 3))
                        elif command:
                            print(f"Unknown command {command!r}; use o, c, or q.")

                    mj.mj_step(model, data)
                    viewer.sync()

                    dt_left = model.opt.timestep - (time.time() - step_start)
                    if dt_left > 0:
                        time.sleep(dt_left)
    except KeyboardInterrupt:
        print("\nInterrupted; shutting down.")
    finally:
        preview_stop.set()
        cap.release()
        preview_process.join(timeout=1.0)
        if preview_process.is_alive():
            preview_process.terminate()
            preview_process.join(timeout=1.0)


if __name__ == "__main__":
    main()
