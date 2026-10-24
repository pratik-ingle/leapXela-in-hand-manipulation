"""Diff two sensor traces produced by ``dump_sensor_trace.py``.

Prints a per-field max/mean absolute difference table and exits non-zero when
anything exceeds the tolerance.  Also importable, so the pytest parity module
can reuse the same comparison logic.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np


FIELDS = ("force", "displacement", "velocity", "contact_force")


def load_trace(path: Path) -> tuple[dict, dict]:
    with np.load(path, allow_pickle=False) as handle:
        arrays = {key: handle[key] for key in handle.files}
    meta = json.loads(str(arrays.pop("metadata_json")))
    return arrays, meta


def compare(
    left: dict, right: dict, atol: float, rtol: float
) -> tuple[list[dict], list[str]]:
    """Return (per-field rows, structural problems)."""
    rows = []
    problems = []

    shared_keys = set(left) & set(right)
    for key in sorted(set(left) ^ set(right)):
        problems.append(f"key present in only one trace: {key}")

    for key in sorted(shared_keys):
        a = np.asarray(left[key], dtype=np.float64)
        b = np.asarray(right[key], dtype=np.float64)
        if a.shape != b.shape:
            problems.append(f"{key}: shape {a.shape} vs {b.shape}")
            continue
        if a.size == 0:
            continue
        diff = np.abs(a - b)
        scale = np.maximum(np.abs(a), np.abs(b))
        # Same tolerance rule numpy.allclose uses, reported rather than asserted.
        tolerance = atol + rtol * np.abs(b)
        rows.append(
            {
                "key": key,
                "shape": a.shape,
                "max_abs": float(diff.max()),
                "mean_abs": float(diff.mean()),
                "max_rel": float((diff / np.where(scale > 0, scale, 1.0)).max()),
                "peak_magnitude": float(scale.max()),
                "n_exceed": int((diff > tolerance).sum()),
            }
        )
    return rows, problems


def group_by_field(rows: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        field = row["key"].split("/")[0]
        grouped.setdefault(field, []).append(row)
    return grouped


def print_report(rows, problems, meta_a, meta_b, atol, rtol) -> None:
    print("=" * 78)
    print("SENSOR TRACE COMPARISON")
    print("=" * 78)
    for label, meta in (("A", meta_a), ("B", meta_b)):
        print(
            f"  {label}: impl={meta['impl']:9s} dt={meta['timestep']:<7g} "
            f"integrator={meta['integrator']} mujoco={meta['mujoco']} "
            f"numpy={meta['numpy']} py={meta['python']}"
        )
        print(f"     model {meta['model_path']}")
    print(f"  tolerance: atol={atol:g} rtol={rtol:g}")
    print()

    if problems:
        print("STRUCTURAL PROBLEMS")
        for problem in problems:
            print(f"  ! {problem}")
        print()

    grouped = group_by_field(rows)
    print(f"{'field':<16}{'entries':>8}{'max_abs':>14}{'mean_abs':>14}"
          f"{'peak_mag':>13}{'exceed':>9}")
    print("-" * 78)
    for field in sorted(grouped):
        field_rows = grouped[field]
        max_abs = max(r["max_abs"] for r in field_rows)
        mean_abs = float(np.mean([r["mean_abs"] for r in field_rows]))
        peak = max(r["peak_magnitude"] for r in field_rows)
        exceed = sum(r["n_exceed"] for r in field_rows)
        flag = "  <-- FAIL" if exceed else ""
        print(f"{field:<16}{len(field_rows):>8}{max_abs:>14.3e}{mean_abs:>14.3e}"
              f"{peak:>13.3e}{exceed:>9d}{flag}")
    print("-" * 78)

    worst = [r for r in rows if r["n_exceed"]]
    if worst:
        worst.sort(key=lambda r: r["max_abs"], reverse=True)
        print("\nWORST DIVERGING ENTRIES")
        for row in worst[:15]:
            print(f"  {row['key']:<40} max_abs={row['max_abs']:.6e} "
                  f"max_rel={row['max_rel']:.3e} n={row['n_exceed']}")

    total_exceed = sum(r["n_exceed"] for r in rows)
    print()
    if problems or total_exceed:
        print(f"RESULT: DIVERGENT ({total_exceed} element(s) beyond tolerance, "
              f"{len(problems)} structural problem(s))")
    else:
        print(f"RESULT: IDENTICAL within atol={atol:g} across {len(rows)} arrays")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--atol", type=float, default=1e-12)
    parser.add_argument("--rtol", type=float, default=0.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    left, meta_a = load_trace(args.left)
    right, meta_b = load_trace(args.right)
    rows, problems = compare(left, right, args.atol, args.rtol)
    print_report(rows, problems, meta_a, meta_b, args.atol, args.rtol)
    return 1 if problems or sum(r["n_exceed"] for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
