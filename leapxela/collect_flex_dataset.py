"""Dataset generator for the LeapXELA flex taxel hand.

For each object shape, sweeps the object count 1..5 at a *fixed* size and
collects N accepted samples per (shape, count) for the shape- and
quantity-inference models.

Acceptance is strict: a sample counts only if every spawned object was still in
the hand at the end, so the count label is never ambiguous. Episodes that lose
an object are retried (up to --max-attempts) rather than kept with a corrected
label. Buckets that cannot reach N are reported, not silently shortened.

Object size is calibrated first unless --scale is given: strict retention is the
binding constraint, and the size that survives count 5 is not obvious a priori.

    conda run --no-capture-output -n leapxela python \
        collect_leapxela_flex_dataset.py --samples 1
"""

import argparse
import csv
import json
import shutil
import subprocess
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import mujoco
import numpy as np
from tqdm import tqdm

from leapxela.paths import data_dir, repo_root
from leapxela.episode import (
    ABORT_CHECK_TIME,
    CLOUD_SOURCES,
    GRASP_PATTERNS,
    MIN_PAD_COVERAGE,
    OBJECT_ADHESION_GAP,
    PALM_PITCH_DEG,
    PLACEABLE_SHAPES,
    PLACEMENT_MODES,
    PLACEMENT_HEIGHT,
    PLACEMENT_JITTER,
    PREGRIP_FRACTION,
    SETTLE_DURATION,
    THUMB_DELAY,
    THUMB_GRIP_FRACTION,
    ZONE_WEIGHTS,
    ObjectSpec,
    check_placement_feasible,
    max_scale_for,
    object_mass,
    run_episode,
)
from leapxela.flex_force import (
    DEFAULT_FLEX_DAMPING,
    DEFAULT_FLEX_STIFFNESS,
    DEFAULT_FORCE_WINDOW,
    DEFAULT_VELOCITY_SMOOTHING,
)
from leapxela.collect_config import load_config
from leapxela.sensors import MODEL_SCHEMA_VERSION, SENSOR_MODES

CALIB_SCALES = (0.3, 0.45, 0.6, 0.75, 0.9, 1.0)
CALIB_COUNTS = (1, 3, 5)
CALIB_TRIALS = 3
# Retention is decided by the close and the first squeeze cycles, so calibration
# does not need the full episode length.
CALIB_DURATION = 6.0
STAGING_NAME = "_attempt"


def episode_args(args: argparse.Namespace, duration: float, video: bool):
    """The Namespace `run_episode` expects, with dataset-level knobs applied."""
    return argparse.Namespace(
        duration=duration,
        # Never abort a video run: those re-simulate an episode that was already
        # accepted, and an abort would leave the sample folder without its npz.
        abort_check_time=0.0 if video else args.abort_check_time,
        sample_hz=args.sample_hz,
        grip_fraction=args.grip_fraction,
        thumb_grip_fraction=args.thumb_grip_fraction,
        thumb_delay=args.thumb_delay,
        pregrip_fraction=args.pregrip_fraction,
        palm_pitch=args.palm_pitch,
        object_adhesion=args.object_adhesion,
        object_adhesion_gap=args.object_adhesion_gap,
        placement_jitter=args.placement_jitter,
        placement_height=args.placement_height,
        settle_duration=args.settle_duration,
        placement_mode=args.placement_mode,
        zone_weights=args.zone_weights,
        min_pad_coverage=args.min_pad_coverage,
        orientation_random=True,
        object_mass=0.0,
        seed=args.seed,
        pulse_hz=args.pulse_hz,
        pulse_amplitude=args.pulse_amplitude,
        shear_amplitude=args.shear_amplitude,
        squeeze_steps=args.squeeze_steps,
        orbit_revolutions=args.orbit_revolutions,
        heatmap_channel=args.heatmap_channel,
        sensor_mode=args.sensor_mode,
        heatmap_source=args.heatmap_source,
        sparsh_stiffness=args.sparsh_stiffness,
        sparsh_damping=args.sparsh_damping,
        sparsh_window=args.sparsh_window,
        sparsh_use_qvel=args.sparsh_use_qvel,
        sparsh_velocity_smoothing=args.sparsh_velocity_smoothing,
        sparsh_activity_threshold=args.sparsh_activity_threshold,
        sparsh_min_peak_normal=args.sparsh_min_peak_normal,
        sparsh_min_contact_fraction=args.sparsh_min_contact_fraction,
        sparsh_deform_scale=args.sparsh_deform_scale,
        sparsh_max_displacement=args.sparsh_max_displacement,
        sparsh_calibration=args.sparsh_calibration,
        force_scale=args.force_scale,
        cloud_view=args.cloud_view,
        cloud_grid=args.cloud_grid,
        cloud_source=args.cloud_source,
        cloud_deform=args.cloud_deform,
        arrow_scale=args.arrow_scale,
        video=video,
    )


def uniform_specs(shape: str, scale: float, count: int) -> list:
    """`count` identical objects.

    Built directly rather than through `sample_specs`, whose multi-object path
    deliberately randomises shape and size from the --multi-* pools; this
    dataset fixes both so only the count varies.
    """
    return [ObjectSpec(shape, scale, object_mass(scale, 0.0))] * count


def episode_rng(
    seed: int, shape: str, count: int, sample: int, attempt: int, pattern: str,
):
    """Deterministic stream per attempt.

    zlib.crc32 rather than hash(): Python salts string hashes per process, so
    hash() would make --seed non-reproducible across runs and across workers.
    Pattern is in the key so two patterns at the same sample index do not share
    object poses.
    """
    return np.random.default_rng(
        [seed, zlib.crc32(shape.encode()), zlib.crc32(pattern.encode()),
         count, sample, attempt]
    )


def bucket_dir(run_dir: Path, shape: str, count: int, pattern: str) -> Path:
    """`run/shape/count_N/pattern/` — one folder per grasp pattern."""
    return run_dir / shape / f"count_{count}" / pattern


def is_accepted(results: dict, criterion: str) -> bool:
    """Strict: every spawned object accounted for, and no divergence.

    `held` is the original criterion and is purely kinematic -- an object lying
    in the unsensed pocket between the palm pads and the finger bases satisfies
    it while contributing nothing to the tactile signal, so the episode keeps a
    count label the taxels cannot support. `sensed` requires each object to
    actually be touching a membrane, which is the guarantee the quantity task
    needs. Default stays `held` so existing yields do not shift silently.
    """
    if criterion == "sensed" and results.get("sensor_mode") == "sparsh":
        raise ValueError("--acceptance sensed is contact-derived and invalid in sparsh mode")
    counted = results["objects_held"] if criterion == "held" else results["objects_sensed"]
    return (
        results["divergences"] == 0
        and counted == results["object_count"]
        and results["passed"]
    )


MAX_SCALE = "max"


def scale_argument(text: str):
    """`--scale` accepts a number or the sentinel.

    A plain `type=float` cannot express the sentinel, and argparse type-converts
    *string* defaults too -- so injecting `scale: max` from a config through
    `set_defaults` would hit `float('max')` without this.
    """
    if text == MAX_SCALE:
        return MAX_SCALE
    return float(text)


def max_scale_across(shape: str, counts) -> float | None:
    """Largest size that fits this shape at EVERY count in the run.

    The cap tightens with count, so a run sweeping 1-3 is bound by the count-3
    entry; sweeping 1-2 can go larger. Returns None for shapes with no cap.
    """
    caps = [max_scale_for(shape, count) for count in counts]
    known = [cap for cap in caps if cap is not None]
    return min(known) if known else None


def resolve_scales(
    args: argparse.Namespace, calibrated: float | None = None
) -> dict[str, float]:
    """One object size per shape.

    Per shape rather than per count on purpose: the collector fixes size so that
    count is the only thing varying across a bucket (see `uniform_specs`). Sizing
    each count separately would let a quantity model read the count off the
    object size instead of the tactile signal.

    `args.scale` accepts a number (that size for every shape), 0 (calibrate, then
    clamp per shape), the string "max", or a {shape: number} mapping with "max"
    filling in the shapes it omits.
    """
    requested = args.scale
    if calibrated is not None:
        requested = calibrated

    def fallback(shape: str) -> float:
        cap = max_scale_across(shape, args.counts)
        if cap is None:
            raise ValueError(
                f"'{shape}' has no measured size cap, so 'max' cannot resolve it; "
                f"give it an explicit scale"
            )
        return cap

    scales: dict[str, float] = {}
    for shape in args.shapes:
        if isinstance(requested, dict):
            value = requested.get(shape)
            chosen = fallback(shape) if value is None else float(value)
        elif isinstance(requested, str):
            chosen = fallback(shape)
        else:
            chosen = float(requested)
            # A calibrated size is a retention estimate, not a pad-fit one, so it
            # can land above what a shape can physically hold. Clamp rather than
            # refuse: the sweep already spent its episodes.
            cap = max_scale_across(shape, args.counts)
            if calibrated is not None and cap is not None:
                chosen = min(chosen, cap)
        scales[shape] = chosen
    return scales


def validate_args(args: argparse.Namespace) -> None:
    if args.sensor_mode == "sparsh" and args.acceptance == "sensed":
        raise ValueError("--acceptance sensed is invalid with --sensor-mode sparsh")
    if args.heatmap_source == "both" and args.sensor_mode != "both":
        raise ValueError("--heatmap-source both requires --sensor-mode both")
    # Only an explicitly requested size is checked. Calibration candidates are
    # sizes to TRY -- CALIB_SCALES reaches 1.0, well past most caps, and
    # validating them here refused even `leapxela-collect` with no arguments.
    # The sweep skips over-cap cells instead, and its winner is clamped per shape
    # by resolve_scales, so the calibrated path cannot produce a refused size.
    pending_calibration = not isinstance(args.scale, (dict, str)) and args.scale <= 0.0
    if args.placement_mode == "per-pad" and not pending_calibration:
        for shape, scale in resolve_scales(args).items():
            for count in args.counts:
                check_placement_feasible(shape, scale, count)


def run_attempt(
    shape: str, scale: float, count: int, pattern: str, output_dir: Path,
    args: argparse.Namespace, duration: float, video: bool,
    sample: int, attempt: int,
) -> dict:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    return run_episode(
        uniform_specs(shape, scale, count),
        pattern,
        episode_args(args, duration, video),
        output_dir,
        episode_rng(args.seed, shape, count, sample, attempt, pattern),
    )


def calib_trial(job: dict) -> dict:
    """One calibration episode, in its own staging dir so workers cannot collide."""
    args = job["args"]
    results = run_attempt(
        job["shape"], job["scale"], job["count"], args.grasp_pattern[0],
        job["staging"], args, args.calib_duration, False, 0, job["trial"],
    )
    if job["staging"].exists():
        shutil.rmtree(job["staging"])
    return {
        "key": (job["scale"], job["shape"], job["count"]),
        "accepted": int(is_accepted(results, args.acceptance)),
        "peak": results["peak_total_normal_n"],
        "aborted": results["aborted"],
    }


def calibrate(args: argparse.Namespace, staging_root: Path, pool) -> dict:
    """Strict-retention rate per (scale, shape, count), and the scale to use.

    Sweeps every shape the dataset will contain, not a single representative
    one: shapes differ enormously here -- measured at scale 0.3, box holds 5
    objects on the first attempt every time while spheres roll out of the hand,
    so calibrating on box alone picks a size that cannot fill the sphere
    buckets.

    Picks the scale with the best *worst-case* rate over every (shape, count)
    cell, since the hardest cell is what decides whether generation terminates.
    Falls back to the mean rate over cells when the worst-case ties, then to
    peak force, preferring the size that reads more strongly.

    Mean rate is not a nicety: a cell can be infeasible at *every* size (five
    spheres never stay in the hand), which pins worst_rate to 0 for the whole
    sweep. Ranking straight to peak force there picks the largest scale -- the
    one that grips hardest on the cells it can still hold -- which is the worst
    available answer. Mean rate keeps the ranking on retention until retention
    genuinely cannot separate two scales.

    Trials are independent episodes, so they run on the same pool as collection.
    `episode_rng` keys off (shape, count, trial) alone, so the table -- and the
    scale it chooses -- does not depend on the order they complete in.
    """
    episodes = (len(args.calib_scales) * len(args.shapes)
                * len(args.calib_counts) * args.calib_trials)
    print(f"calibrating object size over scales {list(args.calib_scales)} "
          f"x shapes {list(args.shapes)} x counts {list(args.calib_counts)} "
          f"x {args.calib_trials} trials ({args.calib_duration:g} s, no video)")
    print(f"  {episodes} episodes, none of them saved: this phase only measures "
          "retention to choose the object size. Dataset collection starts after "
          "it.")
    # Cells above a shape's cap are skipped, not run: the objects could not be
    # placed at that size, so the trial would measure nothing and the episodes
    # would be wasted. Skipping also keeps the sweep from refusing outright.
    def placeable(shape: str, scale: float, count: int) -> bool:
        if args.placement_mode != "per-pad":
            return True
        cap = max_scale_for(shape, count)
        return cap is None or scale <= cap + 1e-9

    planned = [
        (s, sh, c, t)
        for s in args.calib_scales
        for sh in args.shapes
        for c in args.calib_counts
        for t in range(args.calib_trials)
        if placeable(sh, s, c)
    ]
    skipped = (
        len(args.calib_scales) * len(args.shapes) * len(args.calib_counts)
        * args.calib_trials - len(planned)
    )
    if skipped:
        print(f"  skipping {skipped} calibration episodes whose size cannot be "
              f"placed at that count")
    jobs = [
        {"args": args, "scale": scale, "shape": shape, "count": count,
         "trial": trial,
         "staging": staging_root / f"{STAGING_NAME}_calib_{index:04d}"}
        for index, (scale, shape, count, trial) in enumerate(planned)
    ]
    outcomes = {}
    for outcome in pool(calib_trial, jobs):
        outcomes.setdefault(outcome["key"], []).append(outcome)

    table = []
    for scale in args.calib_scales:
        cells = {}
        peaks = []
        for shape in args.shapes:
            for count in args.calib_counts:
                # Missing means the cell was skipped as unplaceable at this size.
                # It is left out of the row rather than scored as a failure: the
                # size was never tried, so it says nothing about retention.
                trials = outcomes.get((scale, shape, count))
                if not trials:
                    continue
                cells[f"{shape}_{count}"] = (
                    sum(o["accepted"] for o in trials) / args.calib_trials
                )
                # Aborted trials only saw the first ~2 s, so their peak is not
                # comparable to a full episode's -- averaging them in drags the
                # tie-break down in proportion to how often a scale drops an
                # object. This is therefore the mean peak over trials that ran
                # to completion, which the retention rates above already select
                # for. With --abort-check-time 0 nothing aborts and it is the
                # same mean as before the abort path existed; with abort on it
                # is a conditional mean and will read higher. Only ever used to
                # break a tie between scales with equal worst-case retention.
                peaks.extend(o["peak"] for o in trials if not o["aborted"])
        if not cells:
            # Every cell at this size was unplaceable, so it cannot be ranked.
            continue
        worst = min(cells.values())
        worst_cell = min(cells, key=cells.get)
        row = {
            "scale": scale,
            "rate_by_shape_count": cells,
            "worst_rate": worst,
            "worst_cell": worst_cell,
            "mean_rate": float(np.mean(list(cells.values()))),
            # Conditional mean over the trials that ran to completion, so it is
            # biased *upward* by exactly the scales that drop objects most: at a
            # size where only the count-1 cells survive, those cells alone set
            # it, and they read the highest forces in the sweep. That is why it
            # ranks last, behind both retention terms.
            "mean_peak_normal_n": float(np.mean(peaks)) if peaks else 0.0,
        }
        table.append(row)
        print(f"  scale {scale:4.2f} | worst {worst * 100:3.0f}% "
              f"at {worst_cell:<14} | mean {row['mean_rate'] * 100:3.0f}% "
              f"| mean peak {row['mean_peak_normal_n']:5.2f} N")
    if not table:
        raise ValueError(
            "no calibration size could be placed for any requested shape and "
            f"count. Lower --calib-scales (currently {list(args.calib_scales)}) "
            "or drop the highest counts; the per-shape caps are in README.md."
        )
    best = max(
        table,
        key=lambda r: (r["worst_rate"], r["mean_rate"],
                       r["mean_peak_normal_n"]),
    )
    dead = [cell for cell, rate in best["rate_by_shape_count"].items()
            if rate == 0.0]
    if dead:
        print(f"  WARNING: at the chosen scale {best['scale']:g}, no trial "
              f"retained every object in: {', '.join(dead)}. Those buckets will "
              "exhaust --max-attempts and come up short. Drop the count or "
              "shape from the run if you do not want to pay for the attempts "
              "-- do NOT raise --pregrip-fraction to compensate: measured, 0.50 "
              "and above makes the fingers diverge (NaN QACC at t~0.03) rather "
              "than gripping harder.")
    print(f"  chosen scale {best['scale']:g} (worst-case strict retention "
          f"{best['worst_rate'] * 100:.0f}% at {best['worst_cell']}, mean "
          f"{best['mean_rate'] * 100:.0f}%)")
    return {"table": table, "chosen_scale": best["scale"]}


def collect_sample(job: dict) -> dict:
    """Collect one accepted sample, retrying until --max-attempts.

    One sample -- not one bucket -- is the unit of work, because bucket costs
    differ by ~30x (box count 1 accepts first try; sphere count 5 exhausts 30
    attempts), and a pool given whole buckets is decided by its slowest one.
    Samples are independent: `episode_rng` keys off (shape, count, pattern,
    sample, attempt) and each writes `count_N/<pattern>/sample_NNN`.
    """
    args = job["args"]
    shape, count, scale, sample, pattern = (
        job["shape"], job["count"], job["scale"], job["sample"], job["pattern"]
    )
    bucket = bucket_dir(job["run_dir"], shape, count, pattern)
    bucket.mkdir(parents=True, exist_ok=True)
    staging = bucket / f"{STAGING_NAME}_{sample:03d}"
    accepted = None
    attempts_used = 0
    for attempt in range(args.max_attempts):
        attempts_used += 1
        results = run_attempt(
            shape, scale, count, pattern, staging, args, args.duration,
            False, sample, attempt,
        )
        if is_accepted(results, args.acceptance):
            accepted = (attempt, results)
            break
    if accepted is None:
        if staging.exists():
            shutil.rmtree(staging)
        return {"shape": shape, "count": count, "pattern": pattern,
                "sample": sample, "attempts_used": attempts_used, "record": None}
    attempt, results = accepted
    sample_dir = bucket / f"sample_{sample:03d}"
    if sample_dir.exists():
        shutil.rmtree(sample_dir)
    staging.rename(sample_dir)
    # Video is re-run rather than rendered up front: rejected attempts far
    # outnumber accepted ones under strict acceptance, and the episode is
    # deterministic in its seed, so this reproduces the kept episode exactly
    # while paying render cost only for samples that survive.
    wants_video = args.video_samples < 0 or sample < args.video_samples
    if wants_video:
        run_attempt(
            shape, scale, count, pattern, sample_dir, args, args.duration,
            True, sample, attempt,
        )
    record = {
        "path": str(sample_dir.relative_to(job["run_dir"])),
        "shape": shape,
        "count": count,
        "scale": scale,
        "pattern": pattern,
        "sensor_mode": results["sensor_mode"],
        "primary_sensor": results["primary_sensor"],
        "objects_held": results["objects_held"],
        "peak_total_normal_n": results["peak_total_normal_n"],
        "contact_peak_total_normal_n": results["contact_peak_total_normal_n"],
        "sparsh_peak_total_normal_n": results["sparsh_peak_total_normal_n"],
        "contact_fraction": results["contact_fraction"],
        "sparsh_contact_fraction": results["sparsh_contact_fraction"],
        "attempts": attempt + 1,
        "video": wants_video,
    }
    metadata_path = sample_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text())
    metadata["dataset"] = record
    metadata_path.write_text(json.dumps(metadata, indent=2))
    return {"shape": shape, "count": count, "pattern": pattern,
            "sample": sample, "attempts_used": attempts_used, "record": record}


def group_buckets(outcomes: list, shapes: list, counts: list, patterns: list,
                  requested: int) -> list:
    """Per-(shape, count, pattern) summaries, in the order of the args.

    Rebuilt from sample outcomes so `dataset.json` and `index.csv` keep the
    layout they had when a bucket was the unit of work, whatever order the pool
    finished in.
    """
    buckets = []
    for shape in shapes:
        for count in counts:
            for pattern in patterns:
                mine = sorted(
                    (o for o in outcomes
                     if o["shape"] == shape and o["count"] == count
                     and o["pattern"] == pattern),
                    key=lambda o: o["sample"],
                )
                samples = [o["record"] for o in mine if o["record"] is not None]
                buckets.append({
                    "shape": shape,
                    "count": count,
                    "pattern": pattern,
                    "requested": requested,
                    "accepted": len(samples),
                    "attempts_used": sum(o["attempts_used"] for o in mine),
                    "samples": samples,
                })
    return buckets


def git_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=repo_root(),
        capture_output=True, text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def build_parser() -> argparse.ArgumentParser:
    """The full argument surface, separate from parsing.

    Split out so the YAML loader can read each argument's type and choices
    straight off the parser instead of maintaining a second copy of the schema.
    """
    parser = argparse.ArgumentParser(
        description="Collect a LeapXELA shape x count tactile dataset.",
    )
    parser.add_argument(
        "--config", type=Path, default=None,
        help="YAML config supplying defaults for any argument below; flags given "
             "on the command line still win. See leapxela/configs/ for examples",
    )
    parser.add_argument(
        "--shapes", nargs="+", choices=list(PLACEABLE_SHAPES),
        default=["box", "cylinder", "disk"],
        help="primitives (box/cylinder/disk) and tetrominoes (I/O/T/L/J/S/Z). "
             "Size is capped per shape and count -- see the table in README.md",
    )
    parser.add_argument(
        "--counts", nargs="+", type=int, default=[1, 2, 3, 4, 5],
        help="object counts to collect; one folder per count",
    )
    parser.add_argument(
        "--samples", type=int, default=1,
        help="accepted samples per (shape, count)",
    )
    parser.add_argument(
        "--scale", type=scale_argument, default=0.0,
        help=f"object size multiplier: a number, 0 to calibrate one, or "
             f"'{MAX_SCALE}' to give each shape the largest size that fits it at "
             f"every requested count. A config may also map shape to number",
    )
    parser.add_argument("--duration", type=float, default=10.0)
    parser.add_argument(
        "--max-attempts", type=int, default=30,
        help="episodes tried per sample before giving up on it",
    )
    parser.add_argument(
        "--video-samples", type=int, default=1,
        help="accepted samples per bucket that also get grasp.mp4 "
             "(-1 renders every sample, 0 renders none)",
    )
    parser.add_argument(
        # Measured on a 10-core M-series: aggregate stepping throughput is 2.90x
        # at 3 workers, 7.29x at 8, and regresses to 7.00x at 10. Episodes are
        # single-threaded, so 8 is the knee -- lower it on a machine in use.
        "--workers", type=int, default=8,
        help="parallel worker processes; samples are independent",
    )
    parser.add_argument(
        "--abort-check-time", type=float, default=ABORT_CHECK_TIME,
        help="seconds after which an attempt that has already lost an object "
             "is abandoned rather than simulated to the end; 0 disables",
    )
    parser.add_argument(
        "--grasp-pattern", nargs="+", choices=GRASP_PATTERNS, default=["pulse"],
        help="pattern(s) collected; each is a folder under count_N/ and gets "
             "--samples of its own",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--calib-scales", nargs="+", type=float, default=list(CALIB_SCALES),
    )
    parser.add_argument(
        "--calib-counts", nargs="+", type=int, default=list(CALIB_COUNTS),
    )
    parser.add_argument("--calib-trials", type=int, default=CALIB_TRIALS)
    parser.add_argument("--calib-duration", type=float, default=CALIB_DURATION)
    parser.add_argument("--sample-hz", type=float, default=100.0)
    parser.add_argument("--grip-fraction", type=float, default=0.55)
    parser.add_argument(
        "--thumb-grip-fraction", type=float, default=THUMB_GRIP_FRACTION,
    )
    parser.add_argument("--thumb-delay", type=float, default=THUMB_DELAY)
    parser.add_argument(
        "--pregrip-fraction", type=float, default=PREGRIP_FRACTION,
    )
    parser.add_argument(
        "--acceptance", choices=("held", "sensed"), default="held",
        help="what every spawned object must satisfy. 'held' is kinematic and "
             "counts objects lying in the unsensed pocket; 'sensed' requires "
             "each to actually touch a taxel membrane",
    )
    parser.add_argument("--palm-pitch", type=float, default=PALM_PITCH_DEG)
    parser.add_argument(
        "--object-adhesion", type=float, default=0.0,
        help="adhesive force in N between OBJECTS ONLY, holding a multi-object "
             "cluster together (0 = off). Never applied to object-hand or "
             "object-skin contacts, so the taxel signal is not biased. "
             "Needs MuJoCo >= 3.11",
    )
    parser.add_argument(
        "--object-adhesion-gap", type=float, default=OBJECT_ADHESION_GAP,
        help="distance in metres over which object adhesion keeps acting; "
             "must be > 0 or adhesion has no effect at any strength",
    )
    parser.add_argument(
        "--placement-jitter", type=float, default=PLACEMENT_JITTER,
    )
    parser.add_argument(
        "--placement-height", type=float, default=PLACEMENT_HEIGHT,
    )
    parser.add_argument(
        "--settle-duration", type=float, default=SETTLE_DURATION,
    )
    parser.add_argument("--pulse-hz", type=float, default=1.0)
    parser.add_argument("--pulse-amplitude", type=float, default=0.15)
    parser.add_argument("--shear-amplitude", type=float, default=0.15)
    parser.add_argument("--squeeze-steps", type=int, default=4)
    parser.add_argument("--orbit-revolutions", type=float, default=1.0)
    parser.add_argument("--heatmap-channel", default="normal")
    parser.add_argument("--sensor-mode", choices=SENSOR_MODES, default="contact")
    parser.add_argument(
        "--heatmap-source", choices=("primary", "contact", "sparsh", "both"),
        default="primary",
    )
    parser.add_argument("--sparsh-stiffness", type=float, default=DEFAULT_FLEX_STIFFNESS)
    parser.add_argument("--sparsh-damping", type=float, default=DEFAULT_FLEX_DAMPING)
    parser.add_argument("--sparsh-window", type=int, default=DEFAULT_FORCE_WINDOW)
    parser.add_argument(
        "--sparsh-use-qvel", action=argparse.BooleanOptionalAction, default=True,
    )
    parser.add_argument(
        "--sparsh-velocity-smoothing", type=float,
        default=DEFAULT_VELOCITY_SMOOTHING,
    )
    parser.add_argument("--sparsh-activity-threshold", type=float, default=0.005)
    parser.add_argument("--sparsh-min-peak-normal", type=float, default=0.01)
    parser.add_argument("--sparsh-min-contact-fraction", type=float, default=0.05)
    parser.add_argument("--sparsh-deform-scale", type=float, default=0.02)
    parser.add_argument("--sparsh-max-displacement", type=float, default=0.015)
    parser.add_argument("--sparsh-calibration", type=Path, default=None)
    parser.add_argument("--force-scale", type=float, default=0.5)
    parser.add_argument("--cloud-view", action=argparse.BooleanOptionalAction,
                        default=True)
    parser.add_argument(
        "--placement-mode", choices=PLACEMENT_MODES, default="per-pad",
        help="per-pad lays each object flat on a palm pad so most of its\n"
             "footprint is over taxels; legacy reproduces the old spawn",
    )
    parser.add_argument(
        "--zone-weights", type=float, nargs=2, default=list(ZONE_WEIGHTS),
        metavar=("FINGERWARD", "WRIST"),
        help="how often each placement zone is drawn: the fingerward strip\n"
             "(pads 1 and 2 plus the seam between them) against the wrist\n"
             "pad. Raising the first leaves pad 3 empty in more episodes",
    )
    parser.add_argument(
        "--min-pad-coverage", type=float, default=MIN_PAD_COVERAGE,
        help="least fraction of an object's footprint that must sit over\n"
             "taxels. Lowering it allows more off-centre placements, at the\n"
             "cost of weaker readings",
    )
    parser.add_argument("--cloud-grid", default="surface")
    parser.add_argument(
        "--cloud-source", choices=(*CLOUD_SOURCES, "both"), default="leapxela",
        help="point-cloud geometry in the video: leapxela MuJoCo taxel sites, "
             "sparsh URDF FK as sparsh-skin-sim draws it, or both",
    )
    parser.add_argument(
        "--cloud-deform", action=argparse.BooleanOptionalAction, default=True,
        help="sparsh cloud only: draw force-deformed taxel positions",
    )
    parser.add_argument("--arrow-scale", type=float, default=1.0)
    parser.add_argument(
        "--output-root", type=Path,
        default=data_dir() / "leapxela_data",
        help="a timestamped run folder is created inside this root",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse the command line, with a --config file supplying the defaults.

    Precedence is CLI > config > argparse default, which falls out of injecting
    the config through `set_defaults` before the real parse.
    """
    parser = build_parser()
    pre = argparse.ArgumentParser(add_help=False)
    pre.add_argument("--config", type=Path, default=None)
    known, _rest = pre.parse_known_args(argv)
    if known.config is not None:
        parser.set_defaults(**load_config(known.config, parser))
    args = parser.parse_args(argv)
    args.config = known.config
    return args


def main() -> None:
    args = parse_args()
    validate_args(args)
    started = time.time()
    run_dir = args.output_root / datetime.now().strftime("run_%Y%m%d_%H%M%S")
    run_dir.mkdir(parents=True)
    print(f"run folder: {run_dir}")

    # One pool for both phases. chunksize=1 because episode costs are wildly
    # uneven -- batching hands a worker several hard jobs while others idle.
    executor = (
        ProcessPoolExecutor(max_workers=args.workers) if args.workers > 1
        else None
    )

    def pool(fn, jobs, description, unit):
        """Run jobs and display completion, throughput, and acceptance status."""
        if executor is not None:
            futures = [executor.submit(fn, job) for job in jobs]
            stream = (future.result() for future in as_completed(futures))
        else:
            stream = (fn(job) for job in jobs)

        outcomes = []
        kept = failed = attempts = 0
        with tqdm(
            stream,
            total=len(jobs),
            desc=description,
            unit=unit,
            dynamic_ncols=True,
            smoothing=0.1,
        ) as progress:
            for outcome in progress:
                outcomes.append(outcome)
                if "record" in outcome:
                    attempts += outcome["attempts_used"]
                    kept += outcome["record"] is not None
                    failed += outcome["record"] is None
                    progress.set_postfix(
                        kept=kept, failed=failed, attempts=attempts,
                        refresh=False,
                    )
                elif "accepted" in outcome:
                    kept += outcome["accepted"]
                    failed += not outcome["accepted"]
                    progress.set_postfix(
                        retained=kept, dropped=failed, refresh=False,
                    )
        return outcomes

    try:
        calibration = None
        calibrated = None
        if not isinstance(args.scale, (dict, str)) and args.scale <= 0.0:
            calibration = calibrate(
                args, run_dir,
                lambda fn, jobs: pool(fn, jobs, "Calibrating", "trial"),
            )
            calibrated = calibration["chosen_scale"]
            (run_dir / "calibration.json").write_text(
                json.dumps(calibration, indent=2)
            )
        # One size per shape: each takes the largest that fits it at every count
        # in this run, so a shape is never held back by a harder one.
        scales = resolve_scales(args, calibrated)
        if calibration is None:
            print("using fixed object scale (calibration skipped)")

        # Hardest first: high counts need the most attempts, so starting them
        # early keeps them off the tail where they would decide the wall clock.
        jobs = sorted(
            [
                {"args": args, "shape": shape, "count": count,
                 "pattern": pattern, "scale": scales[shape],
                 "sample": sample, "run_dir": run_dir}
                for shape in args.shapes
                for count in args.counts
                for pattern in args.grasp_pattern
                for sample in range(args.samples)
            ],
            key=lambda job: -job["count"],
        )
        n_buckets = (
            len(args.shapes) * len(args.counts) * len(args.grasp_pattern)
        )
        sizes = ", ".join(f"{shape} {value:g}" for shape, value in scales.items())
        print(f"collecting {n_buckets} buckets x {args.samples} samples "
              f"({len(jobs)} episodes to fill) at scale {sizes}, "
              f"{args.duration:g} s each, {args.workers} workers")
        outcomes = pool(collect_sample, jobs, "Collecting", "sample")
    finally:
        if executor is not None:
            executor.shutdown()

    buckets = group_buckets(
        outcomes, args.shapes, args.counts, args.grasp_pattern, args.samples,
    )
    rows = [s for bucket in buckets for s in bucket["samples"]]
    with (run_dir / "index.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "shape", "count", "scale", "pattern",
                        "sensor_mode", "primary_sensor", "objects_held",
                        "peak_total_normal_n", "contact_peak_total_normal_n",
                        "sparsh_peak_total_normal_n", "contact_fraction",
                        "sparsh_contact_fraction", "attempts", "video"],
        )
        writer.writeheader()
        writer.writerows(rows)

    elapsed = time.time() - started
    (run_dir / "dataset.json").write_text(json.dumps({
        "created": datetime.now().isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        # Flex forces are not comparable across MuJoCo versions (3.11 moved flex
        # elasticity into the CG solver), so the version is part of a dataset's
        # identity, not incidental environment detail.
        "mujoco_version": mujoco.__version__,
        "schema_version": MODEL_SCHEMA_VERSION,
        "elapsed_seconds": round(elapsed, 1),
        # One size per shape: each takes the largest that fits it at every count
        # in this run, so a shape is not held back by a harder one. index.csv
        # carries the same value per sample.
        "object_scales": scales,
        # Surfaced beside the scales rather than left in `args` alone: together
        # they decide where on the palm the signal lands.
        "placement": {
            "mode": args.placement_mode,
            "zone_weights": list(args.zone_weights),
            "min_pad_coverage": args.min_pad_coverage,
        },
        "acceptance": f"strict: objects_{args.acceptance} == object_count",
        # The config names where the run came from; `args` is the resolved result
        # after CLI overrides, which is what actually produced this dataset.
        "config_path": str(args.config) if args.config else None,
        "args": {k: (str(v) if isinstance(v, Path) else v)
                 for k, v in vars(args).items()},
        "calibration": calibration,
        "buckets": buckets,
        "total_samples": len(rows),
    }, indent=2))

    short = [b for b in buckets if b["accepted"] < b["requested"]]
    print(f"\n{len(rows)} samples in {elapsed / 60:.1f} min -> {run_dir}")
    print(" shape      count  pattern    accepted  attempts  accept rate")
    for bucket in buckets:
        rate = bucket["accepted"] / max(bucket["attempts_used"], 1)
        print(f"  {bucket['shape']:<9} {bucket['count']:>4}  "
              f"{bucket['pattern']:<9} "
              f"{bucket['accepted']:>7}/{bucket['requested']:<3} "
              f"{bucket['attempts_used']:>7}  {rate * 100:>7.0f}%")
    if short:
        print("\nbuckets that did not reach the requested sample count:")
        for bucket in short:
            print(f"  {bucket['shape']} count={bucket['count']} "
                  f"{bucket['pattern']}: "
                  f"{bucket['accepted']}/{bucket['requested']} "
                  f"(hit --max-attempts {args.max_attempts})")


if __name__ == "__main__":
    main()
