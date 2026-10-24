"""Summarise sensor traces by physical behaviour rather than per-step values.

``compare_traces.py`` answers "are these two runs numerically identical?".  That
question only makes sense when the model and the timestep match.  When they
differ -- leapxela runs dt=0.002/implicitfast, sparsh-skin-sim runs
dt=0.010/Euler -- step-aligned diffing is meaningless, so compare what the sensor
actually reports instead: how hard it was pressed, where, and for how long.

Pass several traces to get a side-by-side table.
"""

import argparse
import json
from pathlib import Path

import numpy as np


INTEGRATOR_NAMES = {0: "euler", 1: "rk4", 2: "implicit", 3: "implicitfast"}


def load_trace(path: Path) -> tuple[dict, dict]:
    with np.load(path, allow_pickle=False) as handle:
        arrays = {key: handle[key] for key in handle.files}
    meta = json.loads(str(arrays.pop("metadata_json")))
    return arrays, meta


def summarize(arrays: dict, meta: dict, activity_threshold: float) -> dict:
    flex_names = meta["flex_names"]
    forces = {name: arrays[f"force/{name}"] for name in flex_names}
    contacts = {name: arrays[f"contact_force/{name}"] for name in flex_names}

    # Per-vertex force magnitude over the whole run, across all patches.
    peak_taxel = 0.0
    peak_total = 0.0
    peak_normal = 0.0
    active_taxels = 0
    peak_patch = ""
    for name, trace in forces.items():
        magnitude = np.linalg.norm(trace, axis=-1)
        patch_peak = float(magnitude.max())
        if patch_peak > peak_taxel:
            peak_taxel = patch_peak
            peak_patch = name
        peak_total = max(peak_total, float(magnitude.sum(axis=-1).max()))
        # Compression-positive normal, matching the sensors.py convention.
        peak_normal = max(peak_normal, float((-trace[..., 2]).max()))
        active_taxels = max(
            active_taxels, int(((-trace[..., 2]) > activity_threshold).sum(axis=-1).max())
        )

    contact_peak = max(
        float(np.linalg.norm(trace, axis=-1).max()) for trace in contacts.values()
    )
    contact_counts = np.stack(
        [arrays[f"contact_count/{name}"] for name in flex_names]
    ).sum(axis=0)
    contacting = np.flatnonzero(contact_counts > 0)
    time = arrays["time"]
    first_contact = float(time[contacting[0]]) if contacting.size else float("nan")

    return {
        "impl": meta["impl"],
        "dt": meta["timestep"],
        "integrator": INTEGRATOR_NAMES.get(meta["integrator"], str(meta["integrator"])),
        "steps": meta["steps"],
        "duration": meta.get("duration", float(time[-1])),
        "peak_taxel_n": peak_taxel,
        "peak_patch": peak_patch,
        "peak_total_n": peak_total,
        "peak_normal_n": peak_normal,
        "active_taxels": active_taxels,
        "contact_peak_n": contact_peak,
        "peak_ncon": int(arrays["ncon"].max()),
        "first_contact_s": first_contact,
    }


def print_table(rows: list[tuple[str, dict]]) -> None:
    print("=" * 100)
    print("BEHAVIOURAL SUMMARY")
    print("=" * 100)
    header = (
        f"{'trace':<22}{'impl':<10}{'dt':>7}{'integrator':>14}{'dur(s)':>8}"
        f"{'peak_taxel':>12}{'peak_norm':>11}{'active':>8}{'contact':>10}"
    )
    print(header)
    print("-" * 100)
    for label, summary in rows:
        print(
            f"{label:<22}{summary['impl']:<10}{summary['dt']:>7g}"
            f"{summary['integrator']:>14}{summary['duration']:>8.3f}"
            f"{summary['peak_taxel_n']:>12.4f}{summary['peak_normal_n']:>11.4f}"
            f"{summary['active_taxels']:>8d}{summary['contact_peak_n']:>10.4f}"
        )
    print("-" * 100)
    print("peak_taxel / peak_norm / contact in newtons; active = taxels over threshold")
    print()
    for label, summary in rows:
        print(
            f"  {label:<22} peak patch={summary['peak_patch']:<22} "
            f"peak ncon={summary['peak_ncon']:<5d} first contact={summary['first_contact_s']:.4f}s"
        )


def relative_table(rows: list[tuple[str, dict]], baseline: str) -> None:
    lookup = dict(rows)
    if baseline not in lookup:
        return
    base = lookup[baseline]
    print()
    print(f"RELATIVE TO '{baseline}' (ratio; 1.000 = identical behaviour)")
    print("-" * 100)
    print(f"{'trace':<22}{'peak_taxel':>12}{'peak_norm':>12}{'contact':>12}{'active':>12}")
    print("-" * 100)
    for label, summary in rows:
        def ratio(key: str) -> float:
            denominator = base[key]
            return summary[key] / denominator if denominator else float("nan")

        print(
            f"{label:<22}{ratio('peak_taxel_n'):>12.3f}{ratio('peak_normal_n'):>12.3f}"
            f"{ratio('contact_peak_n'):>12.3f}{ratio('active_taxels'):>12.3f}"
        )
    print("-" * 100)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "traces",
        nargs="+",
        help="Paths, optionally as label=path",
    )
    parser.add_argument("--activity-threshold", type=float, default=0.005)
    parser.add_argument("--baseline", default=None, help="Label to take ratios against")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = []
    for item in args.traces:
        label, _, raw = item.partition("=")
        if not raw:
            raw, label = label, Path(label).stem
        arrays, meta = load_trace(Path(raw))
        rows.append((label, summarize(arrays, meta, args.activity_threshold)))
    print_table(rows)
    if args.baseline:
        relative_table(rows, args.baseline)


if __name__ == "__main__":
    main()
