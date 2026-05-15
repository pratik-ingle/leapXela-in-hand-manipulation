import re
import tempfile
from pathlib import Path
from typing import Dict, Tuple

import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node


def _expand_package_uris(urdf_xml: str) -> str:
    """
    Replace `package://<pkg>/...` URIs with absolute paths to that package share dir.
    This is necessary for PyBullet to find meshes/materials referenced by the URDF.
    """

    pkgs = set(re.findall(r"package://([^/]+)/", urdf_xml))
    replacements: Dict[str, str] = {}
    for pkg in pkgs:
        try:
            replacements[f"package://{pkg}/"] = str(Path(get_package_share_directory(pkg)).as_posix()) + "/"
        except Exception:
            pass

    for k, v in replacements.items():
        urdf_xml = urdf_xml.replace(k, v)
    return urdf_xml


class PyBulletXacroViewer(Node):
    def __init__(self) -> None:
        super().__init__("pybullet_xacro_viewer")

        self.declare_parameter("xacro_path", "xela_models/urdf/aftf.xacro")
        self.declare_parameter("taxels", False)
        self.declare_parameter("gui", True)
        self.declare_parameter("fixed_base", True)
        self.declare_parameter("use_realtime", False)
        self.declare_parameter("frame_length", 0.04)
        self.declare_parameter("line_width", 2.0)
        self.declare_parameter("update_hz", 30.0)

        xacro_path_param = self.get_parameter("xacro_path").get_parameter_value().string_value
        self._taxels = self.get_parameter("taxels").get_parameter_value().bool_value
        self._gui = self.get_parameter("gui").get_parameter_value().bool_value
        self._fixed_base = self.get_parameter("fixed_base").get_parameter_value().bool_value
        self._use_realtime = self.get_parameter("use_realtime").get_parameter_value().bool_value
        self._frame_len = float(self.get_parameter("frame_length").value)
        self._line_width = float(self.get_parameter("line_width").value)
        update_hz = float(self.get_parameter("update_hz").value)
        self._dt = 1.0 / max(1e-6, update_hz)

        self._pb = None
        self._robot_id = None
        self._debug_ids: Dict[Tuple[int, str], int] = {}

        self._start_pybullet()
        self._robot_id = self._load_xacro_into_pybullet(xacro_path_param)

        if self._use_realtime:
            self._pb.setRealTimeSimulation(1)
        else:
            self._pb.setRealTimeSimulation(0)

        self._timer = self.create_timer(self._dt, self._tick)
        self.get_logger().info("PyBullet viewer running.")

    def _start_pybullet(self) -> None:
        import pybullet as p
        import pybullet_data

        self._pb = p
        cid = p.connect(p.GUI if self._gui else p.DIRECT)
        if cid < 0:
            raise RuntimeError("Failed to connect to PyBullet.")

        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0.0, 0.0, -9.81)

        if self._gui:
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)

        p.loadURDF("plane.urdf")

    def _resolve_xacro_path(self, xacro_path_param: str) -> Path:
        p = Path(xacro_path_param)
        if p.is_file():
            return p

        parts = xacro_path_param.split("/", 1)
        if len(parts) == 2 and parts[0] and parts[1]:
            maybe_pkg = parts[0]
            try:
                share = Path(get_package_share_directory(maybe_pkg))
                cand = share / parts[1]
                if cand.is_file():
                    return cand
            except Exception:
                pass

        share = Path(get_package_share_directory("xela_models"))
        cand = share / xacro_path_param
        if cand.is_file():
            return cand

        raise FileNotFoundError(f"Could not resolve xacro_path: {xacro_path_param}")

    def _load_xacro_into_pybullet(self, xacro_path_param: str) -> int:
        import xacro

        xacro_path = self._resolve_xacro_path(xacro_path_param)
        self.get_logger().info(f"Loading xacro: {xacro_path}")

        mappings = {"taxel": "1" if self._taxels else "0"}
        doc = xacro.process_file(str(xacro_path), mappings=mappings)
        urdf_xml = doc.toxml()
        urdf_xml = _expand_package_uris(urdf_xml)
        # PyBullet's URDF loader can be sensitive to very long single-line XML.
        # Splitting tags across lines keeps the XML equivalent but more parse-friendly.
        urdf_xml = urdf_xml.replace("><", ">\n<")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".urdf", delete=False) as f:
            f.write(urdf_xml)
            urdf_path = f.name

        self.get_logger().info(f"Expanded URDF written to: {urdf_path}")

        flags = 0
        try:
            flags |= self._pb.URDF_USE_INERTIA_FROM_FILE
        except Exception:
            pass

        robot_id = self._pb.loadURDF(
            urdf_path,
            basePosition=[0.0, 0.0, 0.0],
            baseOrientation=[0.0, 0.0, 0.0, 1.0],
            useFixedBase=self._fixed_base,
            flags=flags,
        )
        if robot_id < 0:
            raise RuntimeError("PyBullet failed to load the URDF.")

        return robot_id

    def _draw_frame(self, link_index: int, pos, orn) -> None:
        p = self._pb
        frame_len = self._frame_len

        R = p.getMatrixFromQuaternion(orn)
        x_axis = (R[0], R[3], R[6])
        y_axis = (R[1], R[4], R[7])
        z_axis = (R[2], R[5], R[8])

        def add_or_replace(axis_name: str, end, color):
            key = (link_index, axis_name)
            replace_id = self._debug_ids.get(key, -1)
            uid = p.addUserDebugLine(
                pos,
                end,
                lineColorRGB=color,
                lineWidth=self._line_width,
                lifeTime=0.0,
                replaceItemUniqueId=replace_id,
            )
            self._debug_ids[key] = uid

        end_x = [pos[0] + frame_len * x_axis[0], pos[1] + frame_len * x_axis[1], pos[2] + frame_len * x_axis[2]]
        end_y = [pos[0] + frame_len * y_axis[0], pos[1] + frame_len * y_axis[1], pos[2] + frame_len * y_axis[2]]
        end_z = [pos[0] + frame_len * z_axis[0], pos[1] + frame_len * z_axis[1], pos[2] + frame_len * z_axis[2]]

        add_or_replace("x", end_x, [1, 0, 0])
        add_or_replace("y", end_y, [0, 1, 0])
        add_or_replace("z", end_z, [0, 0, 1])

    def _tick(self) -> None:
        p = self._pb
        rid = self._robot_id
        if rid is None:
            return

        if not self._use_realtime:
            p.stepSimulation()

        base_pos, base_orn = p.getBasePositionAndOrientation(rid)
        self._draw_frame(-1, base_pos, base_orn)

        n = p.getNumJoints(rid)
        for j in range(n):
            st = p.getLinkState(rid, j, computeForwardKinematics=True)
            pos = st[4]
            orn = st[5]
            self._draw_frame(j, pos, orn)

    def destroy_node(self):
        try:
            if self._pb is not None:
                self._pb.disconnect()
        finally:
            return super().destroy_node()


def main() -> None:
    rclpy.init()
    node = PyBulletXacroViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

