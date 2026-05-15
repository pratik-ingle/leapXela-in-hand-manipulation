
import numpy as np
from leap_hand_utils.dynamixel_client import *
import leap_hand_utils.leap_hand_utils as lhu
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
import json

def load_pose(pose_name):
    pose_path = Path(get_package_share_directory('leap_hand')) / 'config' / 'pose.json'
    with pose_path.open('r', encoding='utf-8') as f:
        pose = json.load(f)

    return pose[pose_name]

class LeapXelaBase:
    def __init__(self):
        self.kP = 600
        self.kI = 0
        self.kD = 200
        self.curr_lim = 550
        self.prev_pos = self.pos = self.curr_pos = lhu.allegro_to_LEAPhand(np.zeros(16))
        self.motors = motors = [i for i in range(16)]
        try:
            self.dxl_client = DynamixelClient(motors, '/dev/serial/by-id/usb-FTDI_USB__-__Serial_Converter_FTA2U1HJ-if00-port0', 4000000)
            self.dxl_client.connect()
            print("Connected via /dev/serial/by-id (ttyUSB4)")
        except Exception as e:
            try:
                # self.dxl_client = DynamixelClient(motors, '/dev/ttyUSB0', 57600)
                self.dxl_client = DynamixelClient(motors, '/dev/ttyUSB0', 4000000)

                self.dxl_client.connect()
                print("Connected via /dev/ttyUSB0")
            except Exception as e2:
                try:
                    self.dxl_client = DynamixelClient(motors, '/dev/ttyUSB1', 4000000)
                    self.dxl_client.connect()
                    print("Connected via /dev/ttyUSB1")
                except Exception as e3:
                    self.dxl_client = DynamixelClient(motors, 'COM13', 4000000)
                    self.dxl_client.connect()
                    print("Connected via COM13")
        self.dxl_client.sync_write(motors, np.ones(len(motors))*5, 11, 1)
        self.dxl_client.set_torque_enabled(motors, True)
        self.dxl_client.sync_write(motors, np.ones(len(motors)) * self.kP, 84, 2)
        self.dxl_client.sync_write([0,4,8], np.ones(3) * (self.kP * 0.75), 84, 2)
        self.dxl_client.sync_write(motors, np.ones(len(motors)) * self.kI, 82, 2)
        self.dxl_client.sync_write(motors, np.ones(len(motors)) * self.kD, 80, 2)
        self.dxl_client.sync_write([0,4,8], np.ones(3) * (self.kD * 0.75), 80, 2)
        self.dxl_client.sync_write(motors, np.ones(len(motors)) * self.curr_lim, 102, 2)
 
    def set_joints_degrees(self, degrees_array):
        """Set all 16 joints using degree values (list or np.array of length 16)."""
        if len(degrees_array) != 16:
            print("Error: Please provide exactly 16 values (one per joint).")
            return
        try:
            radians_array = np.radians(degrees_array)
            self.dxl_client.write_desired_pos(self.motors, radians_array)
        except Exception as e:
            print(f"Warning: Failed to write joint positions: {e}")
    
    def safe_disconnect(self):
        """Safely disconnect from Dynamixel motors, handling I/O errors gracefully."""
        if hasattr(self, 'dxl_client') and self.dxl_client:
            try:
                # Try to disable torque first
                if self.dxl_client.is_connected:
                    self.dxl_client.port_handler.is_using = False
                    try:
                        self.dxl_client.set_torque_enabled(self.motors, False, retries=0)
                    except:
                        pass  # Ignore errors during torque disable
            except:
                pass  # Ignore errors during cleanup
            finally:
                try:
                    if self.dxl_client.is_connected:
                        self.dxl_client.port_handler.closePort()
                except:
                    pass  # Ignore I/O errors during port close
 
    def read_pos_degrees(self):
        """Read current joint positions and return in degrees."""
        pos_rad = self.dxl_client.read_pos()
        return np.degrees(pos_rad)
 