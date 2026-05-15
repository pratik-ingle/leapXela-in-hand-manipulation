import numpy as np
from leap_hand_utils.dynamixel_client import *
import leap_hand_utils.leap_hand_utils as lhu
import time
import sys
 
class LeapNode:
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
        # self.dxl_client.write_desired_pos(self.motors, self.curr_pos)
 
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
 
def main():
    # Parameters
    frequency = 100.0  # Hz - update rate
    num_cycles = 10   # Number of complete cycles to perform
    min_angle = 90.0  # Minimum angle (degrees)
    max_angle = 180.0 # Maximum angle (degrees)
    
    leap_hand = LeapNode()
    
    # Initialize thumb values
    thumb_phalange = max_angle  # Start at 180
    thumb_rot = 180.0  # Keep rotation fixed
    
    # Define the base joint configuration
    desired_joint_degrees = [
        180, 180, 180, 180,   # Index finger (MCP Side, MCP Forward, PIP, DIP)
        180, 180, 180, 180,   # Middle finger
        180, 180, 180, 180,   # Ring finger
        180, thumb_rot, 180, thumb_phalange    # Thumb
    ]
    
    print("=== LEAP Hand Sinusoidal Thumb Control ===")
    print(f"Frequency: {frequency} Hz")
    print(f"Number of cycles: {num_cycles}")
    print(f"Angle range: {min_angle}° to {max_angle}°")
    print(f"Starting position: {thumb_phalange}°")
    print("==========================================")
    
    # Set initial position
    leap_hand.set_joints_degrees(desired_joint_degrees)
    time.sleep(0.5)  # Give time to reach initial position
    
    # Calculate timing
    period = 1.0 / frequency  # Time for one update
    total_steps_per_cycle = int(max_angle - min_angle) * 2  # 180 steps down + 180 steps up = 360 steps
    step_size = 1.0  # 1 degree per step
    
    # Initialize cycle tracking
    current_angle = max_angle
    direction = -1  # -1 for going down, +1 for going up
    cycle_count = 0
    step_count = 0
    has_reached_min = False  # Track if we've reached min at least once
    
    print(f"\nStarting sinusoidal motion...")
    print(f"Each cycle: 180° -> 90° -> 180° ({total_steps_per_cycle} steps total)")
    print(f"Update period: {period:.3f} seconds\n")
    
    try:
        start_time = time.time()
        
        while cycle_count < num_cycles:
            # Update thumb phalange angle
            current_angle += direction * step_size
            
            # Check if we've reached the limits
            if current_angle <= min_angle:
                current_angle = min_angle
                direction = 1  # Start going up
                has_reached_min = True  # Mark that we've been to the minimum
            elif current_angle >= max_angle:
                current_angle = max_angle
                direction = -1  # Start going down
                # A complete cycle is: max -> min -> max
                # Only count cycle if we've reached min at least once
                if has_reached_min:
                    cycle_count += 1
                    if cycle_count <= num_cycles:
                        print(f"Cycle {cycle_count}/{num_cycles} completed. Angle: {current_angle:.1f}°")
                    has_reached_min = False  # Reset for next cycle
            
            # Update the joint configuration
            desired_joint_degrees[3] = current_angle
            thumb_phalange = current_angle
            
            # Move hand to new position
            leap_hand.set_joints_degrees(desired_joint_degrees)
            
            # Print progress (less frequently to avoid spam)
            step_count += 1
            if step_count % 10 == 0:
                print(f"\rStep: {step_count}, Angle: {current_angle:.1f}°, Cycle: {cycle_count}/{num_cycles}", end='', flush=True)
            
            # Wait for next update based on frequency
            time.sleep(period)
        
        elapsed_time = time.time() - start_time
        print(f"\n\nCompleted {num_cycles} cycles in {elapsed_time:.2f} seconds")
        print(f"Average cycle time: {elapsed_time/num_cycles:.2f} seconds")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\nDisconnecting...")
        try:
            leap_hand.safe_disconnect()
        except:
            pass  # Ignore any errors during disconnect
        print("Sinusoidal control ended")
 
if __name__ == "__main__":
    main()
