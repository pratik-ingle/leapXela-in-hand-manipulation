#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from base import load_pose
import threading
import sys
import termios
import time
from pynput import keyboard
min_angle = 120.0
max_angle = 40.0
step_degrees = 5.0

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
class KeyboardNode(Node):

    def __init__(self):
        super().__init__('keyboard_node')
   
        self.pub_hand = self.create_publisher(JointState, '/cmd_xela', 10) 

    def run_pynput(self, desired_joint_degrees, min_angle=min_angle, max_angle=max_angle, step_degrees=step_degrees):
        # Active joint index in range [0..15].
        # Left/Right changes this index; Up/Down changes only this joint's degree value.
        state = {
            "active_joint": 4,  # Match the original thumb-phalanx index used in leapXela_keyboard.py
            "last_msg": "Use arrows to control joints, 'q' to quit.",
            "running": True,
        }
        lock = threading.Lock()

        def publish_desired():
            msg = JointState()
            msg.header.stamp = self.get_clock().now().to_msg()
            # JointState fields require a Python sequence of Python floats.
            msg.position = [float(x) for x in desired_joint_degrees]
            self.pub_hand.publish(msg)

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
                    desired_joint_degrees[joint] = desired_joint_degrees[joint] + step_degrees
                    did_change = True
                    is_adjustment = True
                    state["last_msg"] = f"Increased joint {joint} -> {desired_joint_degrees[joint]:.1f} deg"
                elif key == keyboard.Key.down:
                    joint = state["active_joint"]
                    desired_joint_degrees[joint] = desired_joint_degrees[joint] - step_degrees
                    did_change = True
                    is_adjustment = True
                    state["last_msg"] = f"Decreased joint {joint} -> {desired_joint_degrees[joint]:.1f} deg"
                else:
                    try:
                        if key.char and key.char.lower() == "q":
                            state["running"] = False
                            return False
                    except AttributeError:
                        pass

                # Only publish on value changes (Up/Down).
                if did_change and is_adjustment:
                    publish_desired()

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
                active = state["active_joint"]
                print(f"Current (desired) degree: {desired_joint_degrees[active]}")
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



def main(args=None):
    rclpy.init(args=args)
    keyboard_node = KeyboardNode()
    initial_joint_degrees = load_pose('open')
    try:
        keyboard_node.run_pynput(
            initial_joint_degrees,
            min_angle=min_angle,
            max_angle=max_angle,
            step_degrees=step_degrees,
        )
    finally:
        keyboard_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()