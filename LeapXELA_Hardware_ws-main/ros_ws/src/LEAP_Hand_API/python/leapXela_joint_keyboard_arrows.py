import os
import sys
import time
import threading
import termios

import numpy as np
from pynput import keyboard

# Ensure we can import the sibling script when run directly.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from leapXela_keyboard import LeapNode  # Reuse the same Dynamixel/hand setup


JOINT_LABELS = [
    "Index MCP Side",
    "Index MCP Forward",
    "Index PIP",
    "Index DIP",
    "Middle MCP Side",
    "Middle MCP Forward",
    "Middle PIP",
    "Middle DIP",
    "Ring MCP Side",
    "Ring MCP Forward",
    "Ring PIP",
    "Ring DIP",
    "Thumb MCP Side",
    "Thumb Rotation",
    "Thumb MCP Forward",
    "Thumb Phalange",
]


def clamp(x, lo, hi):
    low = min(lo, hi)
    high = max(lo, hi)
    return max(low, min(high, x))


FORBIDDEN_JOINT_INDICES = [] #[4, 5, 6, 7]


def sync_forbidden_joints_to_current(leap_hand, desired_joint_degrees):
    """
    Prevent actively commanding joints we want to leave alone.

    We still call `set_joints_degrees()` which writes all 16 motors, so we
    overwrite the forbidden indices with the motors' current measured angles
    right before each write.
    """
    if not FORBIDDEN_JOINT_INDICES:
        return

    current_degrees = leap_hand.read_pos_degrees()
    for idx in FORBIDDEN_JOINT_INDICES:
        desired_joint_degrees[idx] = current_degrees[idx]

def get_current_joint_degree_for_active_joint(leap_hand, active_joint):
    current_degrees = leap_hand.read_pos_degrees()
    return current_degrees[active_joint]

def run_pynput(leap_hand, desired_joint_degrees, min_angle, max_angle, step_degrees):
    # Active joint index in range [0..15].
    # Left/Right changes this index; Up/Down changes only this joint's degree value.
    state = {
        "active_joint": 4,  # Match the original thumb-phalanx index used in leapXela_keyboard.py
        "last_msg": "Use arrows to control joints, 'q' to quit.",
        "running": True,
    }
    lock = threading.Lock()

    def on_press(key):
        with lock:
            did_change = False
            is_adjustment = False

            if key == keyboard.Key.left:
                state["active_joint"] = (state["active_joint"] - 1) % 16
                did_change = True
                state["last_msg"] = (
                    f"Selected joint {state['active_joint']}: {JOINT_LABELS[state['active_joint']]}"
                )
            elif key == keyboard.Key.right:
                state["active_joint"] = (state["active_joint"] + 1) % 16
                did_change = True
                state["last_msg"] = (
                    f"Selected joint {state['active_joint']}: {JOINT_LABELS[state['active_joint']]}"
                )
            elif key == keyboard.Key.up:
                joint = state["active_joint"]
                new_val = desired_joint_degrees[joint] + step_degrees
                # desired_joint_degrees[joint] = clamp(new_val, min_angle, max_angle)
                desired_joint_degrees[joint] = new_val

                did_change = True
                is_adjustment = True
                state["last_msg"] = (
                    f"Increased joint {joint} -> {desired_joint_degrees[joint]:.1f} deg"
                )
            elif key == keyboard.Key.down:
                joint = state["active_joint"]
                new_val = desired_joint_degrees[joint] - step_degrees
                # desired_joint_degrees[joint] = clamp(new_val, min_angle, max_angle)
                desired_joint_degrees[joint] = new_val
                did_change = True
                is_adjustment = True
                state["last_msg"] = (
                    f"Decreased joint {joint} -> {desired_joint_degrees[joint]:.1f} deg"
                )
            else:
                try:
                    if key.char and key.char.lower() == "q":
                        state["running"] = False
                        return False
                except AttributeError:
                    pass

            # Only write to motors on value changes (Up/Down).
            if did_change and is_adjustment:
                sync_forbidden_joints_to_current(leap_hand, desired_joint_degrees)
                leap_hand.set_joints_degrees(desired_joint_degrees)

    print("LEAP Hand Joint Control (pynput)")
    print("Controls: Left/Right select joint, Up/Down adjust value, q to quit")

    stdin_fd = sys.stdin.fileno()
    old_attrs = None
    if sys.stdin.isatty():
        old_attrs = termios.tcgetattr(stdin_fd)
        new_attrs = termios.tcgetattr(stdin_fd)
        new_attrs[3] = new_attrs[3] & ~termios.ECHO  # lflags: disable local echo
        termios.tcsetattr(stdin_fd, termios.TCSADRAIN, new_attrs)

    try:
        with keyboard.Listener(on_press=on_press) as listener:
            current_degree = get_current_joint_degree_for_active_joint(leap_hand, state["active_joint"])
            print(f"Current degree: {current_degree}")
            while state["running"]:
                with lock:
                    joint = state["active_joint"]
                    status = (
                        f"Selected joint: {joint}/15 | "
                        f"Label: {JOINT_LABELS[joint]} | "
                        f"Desired: {desired_joint_degrees[joint]:.1f} deg | "
                        f"Step: +/- {step_degrees:.1f} deg | "
                        f"Clamp: {min_angle:.1f}..{max_angle:.1f} deg"
                    )
                    msg = state["last_msg"]
                print(f"\r{status} | {msg}    ", end="", flush=True)
                time.sleep(0.05)

            listener.join()
    finally:
        if old_attrs is not None:
            termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_attrs)
    print()


def main():
    # Same style of constraints as the original sinusoidal script.
    min_angle = 120.0
    max_angle = 40.0
    step_degrees = 5.0
    print("Hello")

    leap_hand = LeapNode()


    figers = {
        "joints_name":["mcp","rot","pip","dip"],
        "ll":[270,185,195,180],
        "ul":[150,90,165,85]
    }
    thumb = {
        "joints_name":["cmc","axl","mcp","ipl"],
        "ll":[105,110,215,155],
        "ul":[15,5,35,295]
    }

    limits = {
        "if":{
            "id":[4,5,6,7],
            "ll":figers["ll"],
            "ul":figers["ul"],
        },
        "mf":{
            "id":[8,9,10,11],
            "ll":figers["ll"],
            "ul":figers["ul"],
        },
        "rf":{
            "id":[12,13,14,15],
            "ll":figers["ll"],
            "ul":figers["ul"],
        },
        "th":{
            "id":[0,1,2,3],
            "ll":thumb["ll"],
            "ul":thumb["ul"],
        },
    }

    # Base joint configuration (16 joints total), matching leapXela_keyboard.py.
    desired_joint_degrees = [
        180,  # : 
        180,  
        180,  # Thumb: th_mcp_active
        90,  # Thumb: th_ipl_act
        265,
        180,
        180,
        180,  # Middle finger
        265,
        180,
        180,
        180,  # Ring finger
        265,
        180,
        180,
        180,  # Thumb (indices 12..15)
    ]

    print("Initializing motors to base configuration...")
    sync_forbidden_joints_to_current(leap_hand, desired_joint_degrees)
    leap_hand.set_joints_degrees(desired_joint_degrees)
    time.sleep(0.5)

    try:
        run_pynput(leap_hand, desired_joint_degrees, min_angle, max_angle, step_degrees)
    except KeyboardInterrupt:
        pass
    finally:
        print("\nDisconnecting...")
        try:
            leap_hand.safe_disconnect()
        except Exception:
            pass


if __name__ == "__main__":
    main()

