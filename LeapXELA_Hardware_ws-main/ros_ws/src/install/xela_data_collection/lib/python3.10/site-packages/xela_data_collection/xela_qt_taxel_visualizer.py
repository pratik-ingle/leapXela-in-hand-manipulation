#!/usr/bin/env python3

import threading
from dataclasses import dataclass

import rclpy
from rclpy.node import Node

from xela_server_ros2.msg import SensStream


@dataclass
class VizState:
    sensor_index: int = 0
    texel_num: int = 0
    latest_xyz: tuple[float, float, float] = (0.0, 0.0, 0.0)


class XelaQtSubscriber(Node):
    def __init__(self, state: VizState, state_lock: threading.Lock) -> None:
        super().__init__("xela_qt_visualizer")
        self._state = state
        self._lock = state_lock

        self.declare_parameter("sensor_index", int(self._state.sensor_index))
        self.declare_parameter("texel_num", int(self._state.texel_num))

        self.add_on_set_parameters_callback(self._on_set_params)

        self._sub = self.create_subscription(SensStream, "/xServTopic", self._on_stream, 10)

        # Apply initial params (in case launch/CLI set them).
        self._apply_params()

    def _apply_params(self) -> None:
        try:
            si = int(self.get_parameter("sensor_index").value)
            tn = int(self.get_parameter("texel_num").value)
        except Exception:
            return
        with self._lock:
            self._state.sensor_index = max(0, si)
            self._state.texel_num = max(0, tn)

    def _on_set_params(self, params):
        from rcl_interfaces.msg import SetParametersResult

        with self._lock:
            for p in params:
                if p.name == "sensor_index":
                    try:
                        v = int(p.value)
                    except Exception:
                        return SetParametersResult(successful=False, reason="sensor_index must be an int")
                    if v < 0:
                        return SetParametersResult(successful=False, reason="sensor_index must be >= 0")
                    self._state.sensor_index = v
                elif p.name == "texel_num":
                    try:
                        v = int(p.value)
                    except Exception:
                        return SetParametersResult(successful=False, reason="texel_num must be an int")
                    if v < 0:
                        return SetParametersResult(successful=False, reason="texel_num must be >= 0")
                    self._state.texel_num = v

        return SetParametersResult(successful=True)

    def _on_stream(self, msg: SensStream) -> None:
        with self._lock:
            si = int(self._state.sensor_index)
            tn = int(self._state.texel_num)

        try:
            taxel = msg.sensors[si].taxels[tn]
        except Exception as e:
            self.get_logger().warn(f"Could not read sensors[{si}].taxels[{tn}]: {e}")
            return

        with self._lock:
            self._state.latest_xyz = (float(taxel.x), float(taxel.y), float(taxel.z))


def main(args=None) -> None:
    try:
        import pyqtgraph as pg
        from PySide6 import QtCore, QtWidgets
    except Exception as e:
        raise SystemExit(
            "Missing Qt deps for xela_qt_visualizer.\n"
            "Install: pip install pyqtgraph PySide6\n"
            f"Import error: {e}"
        )

    rclpy.init(args=args)

    state = VizState(sensor_index=0, texel_num=0)
    state_lock = threading.Lock()
    node = XelaQtSubscriber(state, state_lock)

    # ROS spinning in a background thread so Qt owns the main thread.
    stop_event = threading.Event()

    def spin() -> None:
        executor = rclpy.executors.SingleThreadedExecutor()
        executor.add_node(node)
        while rclpy.ok() and not stop_event.is_set():
            executor.spin_once(timeout_sec=0.05)
        try:
            executor.remove_node(node)
        except Exception:
            pass

    spin_thread = threading.Thread(target=spin, daemon=True)
    spin_thread.start()

    app = QtWidgets.QApplication([])
    win = QtWidgets.QWidget()
    win.setWindowTitle("XELA PyQtGraph live texel values (x/y/z)")

    layout = QtWidgets.QVBoxLayout(win)

    controls = QtWidgets.QHBoxLayout()
    layout.addLayout(controls)

    sensor_spin = QtWidgets.QSpinBox()
    sensor_spin.setRange(0, 1024)
    sensor_spin.setPrefix("sensor_index=")
    texel_spin = QtWidgets.QSpinBox()
    texel_spin.setRange(0, 100000)
    texel_spin.setPrefix("texel_num=")

    apply_btn = QtWidgets.QPushButton("Apply")

    controls.addWidget(sensor_spin)
    controls.addWidget(texel_spin)
    controls.addWidget(apply_btn)
    controls.addStretch(1)

    plot = pg.PlotWidget()
    plot.setBackground("w")
    plot.showGrid(x=True, y=True, alpha=0.25)
    plot.setTitle("Current x/y/z values")
    plot.setLabel("left", "value")
    plot.setLabel("bottom", "axis")
    plot.getPlotItem().getAxis("bottom").setTicks([[(0, "X"), (1, "Y"), (2, "Z")]])
    layout.addWidget(plot)

    bars = pg.BarGraphItem(x=[0, 1, 2], height=[0, 0, 0], width=0.6, brushes=["#1f77b4", "#ff7f0e", "#2ca02c"])
    plot.addItem(bars)
    label = pg.TextItem("", anchor=(0, 0))
    plot.addItem(label)
    label.setPos(0, 0)

    def sync_spins_from_state() -> None:
        with state_lock:
            si = int(state.sensor_index)
            tn = int(state.texel_num)
        sensor_spin.blockSignals(True)
        texel_spin.blockSignals(True)
        sensor_spin.setValue(si)
        texel_spin.setValue(tn)
        sensor_spin.blockSignals(False)
        texel_spin.blockSignals(False)

    def apply_from_ui() -> None:
        si = int(sensor_spin.value())
        tn = int(texel_spin.value())
        node.set_parameters(
            [
                rclpy.parameter.Parameter("sensor_index", rclpy.Parameter.Type.INTEGER, si),
                rclpy.parameter.Parameter("texel_num", rclpy.Parameter.Type.INTEGER, tn),
            ]
        )

    apply_btn.clicked.connect(apply_from_ui)
    sensor_spin.editingFinished.connect(apply_from_ui)
    texel_spin.editingFinished.connect(apply_from_ui)

    sync_spins_from_state()

    timer = QtCore.QTimer()
    timer.setInterval(50)  # ~20 Hz UI refresh

    def on_tick() -> None:
        with state_lock:
            si = int(state.sensor_index)
            tn = int(state.texel_num)
            x, y, z = state.latest_xyz

        # Keep spins in sync in case params were set from CLI.
        # Never overwrite user input while the widget is being edited/focused.
        if not sensor_spin.hasFocus() and not texel_spin.hasFocus():
            if sensor_spin.value() != si or texel_spin.value() != tn:
                sync_spins_from_state()

        bars.setOpts(height=[x, y, z])
        y_min = min(0.0, float(x), float(y), float(z))
        y_max = max(1.0, float(x), float(y), float(z))
        plot.setYRange(y_min * 1.15, y_max * 1.15, padding=0)
        label.setText(f"sensor={si}  texel={tn}    x={x:.3f}  y={y:.3f}  z={z:.3f}")
        label.setPos(0, y_max * 1.05)

    timer.timeout.connect(on_tick)
    timer.start()

    win.resize(900, 550)
    win.show()
    try:
        app.exec()
    finally:
        stop_event.set()
        node.destroy_node()
        rclpy.shutdown()

