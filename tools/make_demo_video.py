"""Turn one leapxela episode into the README demo video and GIF preview.

Lays out the episode's grasp.mp4 (hand view + taxel cloud, with the empty band
between them cropped out) above a palm-vs-finger force trace with a moving
cursor, then writes an H.264 MP4 and a GIF.

    MUJOCO_GL=egl leapxela-episode --objects box --multi-count 3 \
        --multi-shapes box --multi-scale-range 0.5 0.5 --grasp-pattern regrasp \
        --sensor-mode sparsh --seed 7 --orbit-revolutions 0 --cloud-source sparsh \
        --force-scale 0.05 --grip-fraction 0.85 --output-root /tmp/demo
    python tools/make_demo_video.py /tmp/demo/box_x3_regrasp docs/media/demo_3cubes_regrasp

Needs ffmpeg with libx264 on PATH (the leapxela conda env ships one).
"""

import argparse
import json
import shutil
import subprocess
from pathlib import Path

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont

# Taxels at or below this read as idle: SPARSH settles at a ~0.005 N offset on
# every taxel, which summed over ~300 finger taxels would swamp the contacts.
ACTIVE_THRESHOLD_N = 0.01

WIDTH = 1600
HEADER_H = 56
VIEW_H = 720
STRIP_H = 230
# Columns kept from the 1920-wide grasp.mp4: the 1280 px hand view minus its
# empty right margin, and the middle of the 640 px cloud panel.
HAND_COLS = (0, 1040)
CLOUD_COLS = (1320, 1880)
BG = (12, 12, 16)
PALM_COLOUR = "#ff9f1c"
FINGER_COLOUR = "#2ec4f0"
TEXT = (236, 238, 242)
TEXT_DIM = (200, 204, 212)

# GIF colours that cover few pixels (hot taxels, plot lines) get dropped by
# median cut and come out brown or green, so they are pinned in the palette.
PINNED_GIF_COLOURS = [
    (255, 0, 0), (230, 40, 20), (255, 120, 0), (255, 200, 0), (200, 230, 40),
    (60, 230, 160), (0, 160, 255), (0, 0, 255), (40, 40, 230),
    (46, 196, 240), (255, 159, 28), (235, 235, 235),
]


def hex_rgb(colour: str) -> tuple:
    return tuple(int(colour[i:i + 2], 16) for i in (1, 3, 5))


def region_forces(log) -> tuple:
    """Summed active-taxel force magnitude on the palm pads and on the fingers."""
    ids, counts, names = log["skin_taxel_ids"], log["skin_taxel_counts"], log["skin_names"]
    offsets = np.concatenate([[0], np.cumsum(counts)])
    palm = np.concatenate([
        ids[offsets[i]:offsets[i + 1]]
        for i, name in enumerate(names) if name.startswith("uspa46")
    ])
    fingers = np.setdiff1d(np.arange(log["tactile"].shape[1]), palm)
    magnitude = np.linalg.norm(log["tactile"], axis=-1)
    magnitude = magnitude * (magnitude > ACTIVE_THRESHOLD_N)
    return magnitude[:, palm].sum(1), magnitude[:, fingers].sum(1)


def force_strip(times, palm, fingers, close_end):
    """Static plot image plus a data -> pixel mapping for the per-frame cursor."""
    dpi = 100
    bg = np.array(BG) / 255
    fig = plt.figure(figsize=(WIDTH / dpi, STRIP_H / dpi), dpi=dpi, facecolor=bg)
    ax = fig.add_axes([0.055, 0.22, 0.925, 0.68], facecolor=bg)
    ax.axvspan(0, close_end, color="white", alpha=0.06, lw=0)
    ax.text(close_end / 2, 0.93, "closing", transform=ax.get_xaxis_transform(),
            ha="center", va="top", color="#9aa0aa", fontsize=10)
    ax.plot(times, palm, color=PALM_COLOUR, lw=2.2, label="palm pads (objects resting)")
    ax.plot(times, fingers, color=FINGER_COLOUR, lw=2.2, label="fingers (grasp contacts)")
    ax.set_xlim(0, times[-1])
    ax.set_ylim(0, max(palm.max(), fingers.max()) * 1.55)
    ax.set_xlabel("time (s)", color="#c8ccd4", fontsize=11)
    ax.set_ylabel("taxel force (N)", color="#c8ccd4", fontsize=11)
    ax.tick_params(colors="#c8ccd4", labelsize=10)
    for spine in ax.spines.values():
        spine.set_color("#3a3f4b")
    ax.grid(color="#2a2e38", lw=0.8)
    legend = ax.legend(loc="upper right", ncol=2, frameon=False, fontsize=11)
    for text in legend.get_texts():
        text.set_color("#e6e8ec")
    fig.canvas.draw()
    image = np.asarray(fig.canvas.buffer_rgba())[..., :3].copy()
    rows = image.shape[0]
    # Agg can round the canvas a pixel short; pad so every frame is the same size.
    image = np.vstack([image, np.full((STRIP_H - rows, WIDTH, 3), BG, np.uint8)])
    transform = ax.transData

    def to_pixel(t, value):
        x, y = transform.transform((t, value))
        return int(round(x)), int(round(rows - y))

    y_limit = ax.get_ylim()[1]
    plt.close(fig)
    return image, to_pixel, y_limit, rows


def header_image(meta: dict) -> np.ndarray:
    count = meta.get("object_count", 1)
    shapes = {obj["shape"] for obj in meta.get("objects", [])} or {meta.get("shape")}
    noun = {"box": "cube"}.get(shapes.pop(), "object") if len(shapes) == 1 else "object"
    title = f"LEAP Hand + XELA skin  ·  {count} {noun}{'s' if count > 1 else ''}  ·  {meta['grasp_pattern']}"
    image = Image.new("RGB", (WIDTH, HEADER_H), BG)
    draw = ImageDraw.Draw(image)
    bold = ImageFont.truetype(font_manager.findfont("DejaVu Sans:bold"), 22)
    regular = ImageFont.truetype(font_manager.findfont("DejaVu Sans"), 18)
    draw.text((24, 15), title, font=bold, fill=TEXT)
    draw.text((HAND_COLS[1] - HAND_COLS[0] + 12, 18), "368 taxels  ·  blue idle → red loaded",
              font=regular, fill=TEXT_DIM)
    return np.asarray(image)


def write_mp4(episode: Path, out: Path, ffmpeg: str) -> None:
    log = np.load(episode / "sensor_log.npz")
    meta = json.loads((episode / "metadata.json").read_text())
    times = log["tactile_times"]
    palm, fingers = region_forces(log)
    strip, to_pixel, y_limit, rows = force_strip(
        times, palm, fingers, meta["phases"]["close_end_s"]
    )
    header = header_image(meta)
    capture = cv2.VideoCapture(str(episode / "grasp.mp4"))
    fps = capture.get(cv2.CAP_PROP_FPS)
    height = HEADER_H + VIEW_H + STRIP_H
    encoder = subprocess.Popen(
        [ffmpeg, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{WIDTH}x{height}", "-r", f"{fps:.6f}", "-i", "-",
         "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", str(out)],
        stdin=subprocess.PIPE,
    )
    frame_index = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        view = np.hstack([frame[:, slice(*HAND_COLS)], frame[:, slice(*CLOUD_COLS)]])
        now = min(frame_index / fps, times[-1])
        sample = min(int(np.searchsorted(times, now)), len(times) - 1)
        panel = strip.copy()
        x, y_top = to_pixel(now, y_limit)
        _, y_bottom = to_pixel(now, 0.0)
        cv2.line(panel, (x, y_top), (x, y_bottom), (235, 235, 235), 1, cv2.LINE_AA)
        for value, colour in ((palm[sample], PALM_COLOUR), (fingers[sample], FINGER_COLOUR)):
            cv2.circle(panel, to_pixel(now, value), 6, hex_rgb(colour), -1, cv2.LINE_AA)
        cv2.putText(panel, f"t = {now:4.1f} s", (WIDTH - 140, rows - 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (230, 230, 230), 1, cv2.LINE_AA)
        encoder.stdin.write(np.ascontiguousarray(np.vstack([header, view, panel])).tobytes())
        frame_index += 1
    encoder.stdin.close()
    if encoder.wait() != 0:
        raise RuntimeError("ffmpeg failed to encode the demo video")


def write_gif(mp4: Path, out: Path, width: int, step: int, colours: int) -> None:
    capture = cv2.VideoCapture(str(mp4))
    fps = capture.get(cv2.CAP_PROP_FPS)
    frames, index = [], 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        if index % step == 0:
            height = round(frame.shape[0] * width / frame.shape[1] / 2) * 2
            frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        index += 1
    # One palette for the whole clip, so a colour means the same force in every frame.
    mosaic = Image.fromarray(np.vstack(frames[:: max(1, len(frames) // 12)]))
    free = colours - len(PINNED_GIF_COLOURS)
    base = mosaic.quantize(colors=free, method=Image.Quantize.MEDIANCUT)
    entries = base.getpalette()[: 3 * free] + [v for c in PINNED_GIF_COLOURS for v in c]
    palette = Image.new("P", (1, 1))
    palette.putpalette(entries + [0] * (768 - len(entries)))
    images = [
        Image.fromarray(f).quantize(palette=palette, dither=Image.Dither.NONE) for f in frames
    ]
    images[0].save(out, save_all=True, append_images=images[1:],
                   duration=round(1000 * step / fps), loop=0, optimize=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("episode_dir", type=Path, help="episode folder holding grasp.mp4 and sensor_log.npz")
    parser.add_argument("out_stem", type=Path, help="output path without extension; writes .mp4 and .gif")
    parser.add_argument("--gif-width", type=int, default=720)
    parser.add_argument("--gif-step", type=int, default=3, help="keep every Nth frame in the GIF")
    parser.add_argument("--gif-colours", type=int, default=128)
    args = parser.parse_args()

    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise SystemExit("ffmpeg not found on PATH")
    args.out_stem.parent.mkdir(parents=True, exist_ok=True)
    mp4 = args.out_stem.with_suffix(".mp4")
    write_mp4(args.episode_dir, mp4, ffmpeg)
    write_gif(mp4, args.out_stem.with_suffix(".gif"), args.gif_width, args.gif_step, args.gif_colours)
    print(f"wrote {mp4} and {args.out_stem.with_suffix('.gif')}")


if __name__ == "__main__":
    main()
