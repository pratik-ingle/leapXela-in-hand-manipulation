from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import gradio as gr
import numpy as np

import rclpy
from rclpy.node import Node


def _default_data_dir() -> Path:
    """
    Prefer the workspace's `ros_ws/data/` folder (common in this repo), but fall back to `cwd/data/`.
    """
    here = Path(__file__).resolve()
    # .../ros_ws/src/xela_data_collection/xela_data_collection/xela_dataset_visulizer.py
    # parents[0]=file, [1]=xela_data_collection (python pkg), [2]=xela_data_collection (ros pkg),
    # [3]=src, [4]=ros_ws
    try:
        ros_ws = here.parents[4]
        candidate = ros_ws / "data"
        if candidate.exists():
            return candidate
    except Exception:
        pass
    return Path.cwd() / "data"


def _resolve_in_data_dir(p: str | Path, data_dir: Path) -> Path:
    """
    Resolve a user-provided path or filename into an actual file path.

    - If `p` is an existing path (absolute or relative), use it.
    - If `p` looks like a bare filename (no path separators), look for it under `data_dir`.
    - Otherwise, return it as-is (caller will surface file-not-found).
    """
    raw = Path(p) if isinstance(p, Path) else Path(str(p).strip())
    if str(raw).strip() == "":
        return raw

    if raw.exists():
        return raw.resolve()

    # If user typed just "something.h5", treat it as a file inside the data dir.
    if raw.parent == Path(".") and ("/" not in str(p)) and ("\\" not in str(p)):
        candidate = (data_dir / raw.name)
        if candidate.exists():
            return candidate.resolve()
        # even if it doesn't exist, keep the candidate so the error message is helpful
        return candidate

    return raw


def _list_data_files(data_dir: Path) -> List[Path]:
    if not data_dir.exists():
        return []
    files = [p for p in data_dir.iterdir() if p.is_file()]
    # Prefer HDF5-ish extensions first, then everything else.
    def key(p: Path) -> Tuple[int, str]:
        ext = p.suffix.lower()
        prio = 0 if ext in {".h5", ".hdf5"} else 1
        return (prio, p.name.lower())

    return sorted(files, key=key)


def _load_sample(
    h5_path: Path, stream: str, index: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, List[List[Any]], Dict[str, Any]]:
    try:
        import h5py  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "This visualizer requires 'h5py'. Install it (e.g. `pip install h5py`)."
        ) from e

    with h5py.File(h5_path, "r") as f:
        if stream not in f:
            streams = list(f.keys())
            if not streams:
                raise RuntimeError(f"No top-level groups found in {h5_path}.")
            stream = streams[0]

        g = f[stream]
        idxs = sorted([k for k in g.keys() if str(k).isdigit()], key=lambda s: int(s))
        if not idxs:
            raise RuntimeError(f"No digit-named samples found in {h5_path} under stream '{stream}'.")

        i = int(index)
        if i < 0:
            i = 0
        if i >= len(idxs):
            i = len(idxs) - 1
        idx_key = idxs[i]

        grp = g[idx_key]

        norm = np.asarray(grp["normalized_image"])

        st = grp["state"]
        names = [n.decode("utf-8") if isinstance(n, (bytes, bytearray)) else str(n) for n in st["name"][()]]
        pos = np.asarray(st["position"][()], dtype=np.float64).tolist()
        vel = np.asarray(st["velocity"][()], dtype=np.float64).tolist()
        eff = np.asarray(st["effort"][()], dtype=np.float64).tolist()

        rows: List[List[Any]] = []
        for i, name in enumerate(names):
            rows.append(
                [
                    name,
                    pos[i] if i < len(pos) else None,
                    vel[i] if i < len(vel) else None,
                    eff[i] if i < len(eff) else None,
                ]
            )

        meta: Dict[str, Any] = {
            "stream": stream,
            "index": int(index),
            "index_key": idx_key,
            "normalized_image_attrs": {
                k: _jsonable(grp["normalized_image"].attrs.get(k)) for k in grp["normalized_image"].attrs.keys()
            },
            "state_attrs": {k: _jsonable(st.attrs.get(k)) for k in st.attrs.keys()},
        }

    norm_u8 = _to_uint8_image(norm)
    ch0 = _upscale_for_display(_channel_to_rgb(norm_u8, 0), target_height=420)
    ch1 = _upscale_for_display(_channel_to_rgb(norm_u8, 1), target_height=420)
    ch2 = _upscale_for_display(_channel_to_rgb(norm_u8, 2), target_height=420)
    return ch0, ch1, ch2, rows, meta


def _jsonable(v: Any) -> Any:
    if isinstance(v, (np.generic,)):
        return v.item()
    if isinstance(v, (bytes, bytearray)):
        try:
            return v.decode("utf-8")
        except Exception:
            return repr(v)
    return v


def _to_uint8_image(arr: np.ndarray) -> np.ndarray:
    a = np.asarray(arr)
    if a.ndim == 2:
        a = a[:, :, None]
    if a.shape[-1] == 1:
        a = np.repeat(a, 3, axis=-1)
    if a.dtype == np.uint8:
        return a

    a = a.astype(np.float32, copy=False)
    if not np.isfinite(a).any():
        return np.zeros_like(a, dtype=np.uint8)

    lo = float(np.nanmin(a))
    hi = float(np.nanmax(a))
    if hi <= lo:
        return np.zeros(a.shape, dtype=np.uint8)

    a = (a - lo) / (hi - lo)
    a = np.clip(a, 0.0, 1.0)
    return (a * 255.0).round().astype(np.uint8)


def _upscale_for_display(img: np.ndarray, target_height: int = 420, max_scale: int = 50) -> np.ndarray:
    """
    The XELA images are tiny (e.g. 26x31). Gradio displays at native resolution,
    so we upscale with nearest-neighbor to make them visually inspectable.
    """
    a = np.asarray(img)
    if a.ndim != 3:
        return a
    h = int(a.shape[0])
    if h <= 0:
        return a
    scale = int(np.ceil(float(target_height) / float(h)))
    scale = max(1, min(scale, int(max_scale)))
    if scale == 1:
        return a
    a = np.repeat(a, scale, axis=0)
    a = np.repeat(a, scale, axis=1)
    return a


def _channel_to_rgb(norm_u8_rgb: np.ndarray, channel: int) -> np.ndarray:
    a = np.asarray(norm_u8_rgb)
    if a.ndim != 3 or a.shape[-1] < 3:
        raise ValueError(f"Expected HxWx3 image, got shape={a.shape}.")
    c = int(channel)
    c = 0 if c < 0 else (2 if c > 2 else c)
    g = a[:, :, c]
    return np.stack([g, g, g], axis=-1)


def _get_stream_and_count(h5_path: Path) -> Tuple[str, int]:
    try:
        import h5py  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "This visualizer requires 'h5py'. Install it (e.g. `pip install h5py`)."
        ) from e

    with h5py.File(h5_path, "r") as f:
        streams = list(f.keys())
        if not streams:
            raise RuntimeError(f"No top-level groups found in {h5_path}.")
        stream = streams[0]
        g = f[stream]
        idxs = sorted([k for k in g.keys() if str(k).isdigit()], key=lambda s: int(s))
        return stream, len(idxs)


def visulize_dataset() -> None:
    data_dir = _default_data_dir()
    data_files = _list_data_files(data_dir)

    # Back-compat default: prefer xela_data.h5 if present, otherwise first file in data/.
    default_h5 = data_dir / "xela_data.h5"
    if not default_h5.exists() and data_files:
        default_h5 = data_files[0]

    stream, n = _get_stream_and_count(default_h5)
    if n <= 0:
        raise RuntimeError(f"No samples found in {default_h5} under stream '{stream}'.")

    with gr.Blocks(title="XELA dataset visualizer") as demo:
        gr.Markdown("## XELA dataset visualizer")

        with gr.Row():
            dataset_file_in = gr.Dropdown(
                label=f"Dataset file (from {data_dir})",
                choices=[p.name for p in data_files] if data_files else [],
                value=default_h5.name if default_h5.parent == data_dir else (data_files[0].name if data_files else None),
                interactive=True,
                allow_custom_value=True,
            )
            h5_path_in = gr.Textbox(
                label="HDF5 path",
                value=str(default_h5),
                interactive=True,
            )
            stream_in = gr.Textbox(
                label="Stream (top-level group)",
                value=stream,
                interactive=True,
            )

        idx = gr.Slider(
            label="current_index",
            minimum=0,
            maximum=max(0, n - 1),
            value=0,
            step=1,
        )

        with gr.Row(equal_height=True):
            ch0_out = gr.Image(label="normalized_image x", type="numpy", height=420)
            ch1_out = gr.Image(label="normalized_image y", type="numpy", height=420)
            ch2_out = gr.Image(label="normalized_image z", type="numpy", height=420)

        state_out = gr.Dataframe(
            label="state",
            value=[["", None, None, None]],
            headers=["name", "position", "velocity", "effort"],
            datatype=["str", "number", "number", "number"],
            interactive=False,
            wrap=True,
        )
        meta_out = gr.JSON(label="metadata")

        def update(dataset_file: str, h5_path: str, stream_name: str, index: int):
            p = _resolve_in_data_dir(dataset_file if str(dataset_file).strip() else h5_path, data_dir)
            ch0, ch1, ch2, rows, meta = _load_sample(p, stream_name, int(index))
            return ch0, ch1, ch2, rows, meta

        idx.change(
            update,
            inputs=[dataset_file_in, h5_path_in, stream_in, idx],
            outputs=[ch0_out, ch1_out, ch2_out, state_out, meta_out],
        )

        def refresh(dataset_file: str, h5_path: str, stream_name: str):
            p = _resolve_in_data_dir(dataset_file if str(dataset_file).strip() else h5_path, data_dir)
            # if stream_name invalid, fall back to first group
            try:
                import h5py  # type: ignore
            except Exception as e:
                raise RuntimeError(
                    "This visualizer requires 'h5py'. Install it (e.g. `pip install h5py`)."
                ) from e
            with h5py.File(p, "r") as f:
                if stream_name not in f:
                    streams = list(f.keys())
                    if not streams:
                        raise RuntimeError(f"No top-level groups found in {p}.")
                    stream_name = streams[0]
                g = f[stream_name]
                idxs = sorted([k for k in g.keys() if str(k).isdigit()])
                n_local = len(idxs)
            if n_local <= 0:
                raise RuntimeError(f"No samples found in {p} under stream '{stream_name}'.")
            # update slider range and also load index 0
            ch0, ch1, ch2, rows, meta = _load_sample(p, stream_name, 0)
            return (
                str(p),
                stream_name,
                gr.Slider(minimum=0, maximum=max(0, n_local - 1), value=0, step=1, label="current_index"),
                ch0,
                ch1,
                ch2,
                rows,
                meta,
            )

        refresh_btn = gr.Button("Reload file / refresh index range")
        refresh_btn.click(
            refresh,
            inputs=[dataset_file_in, h5_path_in, stream_in],
            outputs=[h5_path_in, stream_in, idx, ch0_out, ch1_out, ch2_out, state_out, meta_out],
        )

        def set_path_from_dropdown(dataset_file: str) -> str:
            # Allow either a filename in data_dir or a full/relative path the user pasted.
            p = _resolve_in_data_dir(dataset_file, data_dir)
            return str(p)

        dataset_file_in.change(set_path_from_dropdown, inputs=[dataset_file_in], outputs=[h5_path_in])

    # Bind to all interfaces so it's reachable from other machines on the LAN.
    server_port = 7860
    server_name = "0.0.0.0"
    rclpy.logging.get_logger("xela_dataset_visulizer").info(
        f"Gradio hosted at:  {server_name}:{server_port})"
    )
    demo.launch(server_name=server_name, server_port=server_port)



class XelaDatasetVisulizer(Node):
    def __init__(self,func):
        super().__init__("xela_dataset_visulizer")
        
        self.func = func
        # Gradio blocks; run it immediately when node is constructed.
        self.func()
        

def main():
    rclpy.init()
    node = None
    try:
        # This starts the Gradio UI (blocks until it stops).
        node = XelaDatasetVisulizer(visulize_dataset)
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()

    
if __name__ == "__main__":
    main()

