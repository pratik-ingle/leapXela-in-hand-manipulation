"""Three-way similarity report over (T, 368, 3) taxel traces.

``compare_traces.py`` answers "are these two runs identical?", which is the right
question only when model, timestep and inputs all match.  This tool answers
"are these two readouts *similar*?", which is what is needed when comparing:

* leapxela's sparsh sensor vs the sparsh-skin-sim original (same quantity, should match)
* either sparsh sensor vs leapxela's contact sensor (different physical quantity --
  MuJoCo contact wrenches vs ``K*u + B*v`` -- so the useful output is the fitted
  scale factor and the spatial agreement, not an equality check)

Sources are given as ``label=path.npz:array_key`` so one trace file can supply
more than one readout (leapxela records sparsh and contact in the same pass).

Usage::

    python compare_taxels.py \\
        lx-sparsh=r1/lx.npz:sparsh_flat \\
        ss-sparsh=r1/ss.npz:sparsh_flat \\
        lx-contact=r1/lx.npz:contact_flat
"""

import argparse
import itertools
import json
from pathlib import Path

import numpy as np


INTEGRATOR_NAMES = {0: "euler", 1: "rk4", 2: "implicit", 3: "implicitfast"}
LOADED_EPS = 1e-6


def load_source(item: str, from_time: float, to_time: float) -> tuple[str, np.ndarray, dict]:
    label, _, rest = item.partition("=")
    if not rest:
        raise SystemExit(f"expected label=path.npz:array_key, got '{item}'")
    path_part, _, key = rest.partition(":")
    key = key or "sparsh_flat"
    with np.load(Path(path_part), allow_pickle=False) as handle:
        if key not in handle.files:
            raise SystemExit(f"{path_part} has no array '{key}'; has {sorted(handle.files)[:12]}")
        array = np.asarray(handle[key], dtype=np.float64)
        meta = json.loads(str(handle["metadata_json"]))
        time = handle["time"] if "time" in handle.files else None
        ncon = handle["ncon"] if "ncon" in handle.files else None

    # Restricting the window matters: the global peak lands during the object's
    # initial impact, a transient that says little about the held grasp. Passing
    # --from-time past the close compares the regime collection actually samples.
    if time is not None and (from_time > 0.0 or to_time < np.inf):
        mask = (time >= from_time) & (time <= to_time)
        if not mask.any():
            raise SystemExit(f"{path_part}: no samples in [{from_time}, {to_time}]")
        array = array[mask]
        ncon = ncon[mask] if ncon is not None else None
        time = time[mask]

    meta = {**meta, "array_key": key, "_time": time, "_ncon": ncon}
    return label, array, meta


def peak_frame(normal: np.ndarray) -> int:
    """Index of the frame carrying the most total compression."""
    return int(np.argmax(normal.sum(axis=-1)))


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    def rank(x):
        order = np.argsort(x, kind="stable")
        ranks = np.empty_like(order, dtype=np.float64)
        ranks[order] = np.arange(len(x), dtype=np.float64)
        return ranks

    return pearson(rank(a), rank(b))


def pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = a - a.mean()
    b = b - b.mean()
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(a @ b / denom) if denom > 0 else float("nan")


def scale_fit(a: np.ndarray, b: np.ndarray) -> tuple[float, float]:
    """Least-squares b ~= alpha * a through the origin, with R^2."""
    denom = float(a @ a)
    if denom <= 0:
        return float("nan"), float("nan")
    alpha = float(a @ b) / denom
    residual = b - alpha * a
    total = float(((b - b.mean()) ** 2).sum())
    r2 = 1.0 - float((residual**2).sum()) / total if total > 0 else float("nan")
    return alpha, r2


def summarize(label: str, array: np.ndarray, meta: dict, threshold: float) -> dict:
    normal = array[..., 2]
    magnitude = np.linalg.norm(array, axis=-1)
    total = normal.sum(axis=-1)
    frame = peak_frame(normal)
    active = normal[frame] > threshold
    ncon = meta.get("_ncon")
    return {
        "mean_total_normal": float(total.mean()),
        "mean_ncon": float(np.mean(ncon)) if ncon is not None else float("nan"),
        "label": label,
        "key": meta["array_key"],
        "impl": meta["impl"],
        "dt": meta["timestep"],
        "integrator": INTEGRATOR_NAMES.get(meta["integrator"], meta["integrator"]),
        "steps": array.shape[0],
        "peak_taxel_normal": float(normal.max()),
        "peak_taxel_magnitude": float(magnitude.max()),
        "peak_total_normal": float(total.max()),
        "peak_frame": frame,
        "argmax_taxel": int(np.argmax(normal[frame])),
        "active_taxels": int(active.sum()),
        "ever_active": int((normal > threshold).any(axis=0).sum()),
    }


def compare_pair(a: np.ndarray, b: np.ndarray, threshold: float) -> dict:
    """a is the reference; alpha answers 'b is alpha times a'."""
    aligned = a.shape == b.shape
    result = {"aligned": aligned}

    na, nb = a[..., 2], b[..., 2]
    fa = peak_frame(na)
    # When step counts differ (native scenes) each side uses its own peak frame.
    fb = fa if aligned else peak_frame(nb)

    va, vb = na[fa], nb[fb]
    loaded = (np.abs(va) > LOADED_EPS) | (np.abs(vb) > LOADED_EPS)
    result["loaded_taxels"] = int(loaded.sum())

    if loaded.any():
        result["pearson_peak"] = pearson(va[loaded], vb[loaded])
        result["spearman_peak"] = spearman(va[loaded], vb[loaded])
        alpha, r2 = scale_fit(va[loaded], vb[loaded])
        result["alpha_peak"] = alpha
        result["r2_peak"] = r2
    else:
        result.update(pearson_peak=float("nan"), spearman_peak=float("nan"),
                      alpha_peak=float("nan"), r2_peak=float("nan"))

    set_a = set(np.flatnonzero(na[fa] > threshold))
    set_b = set(np.flatnonzero(nb[fb] > threshold))
    union = set_a | set_b
    result["jaccard"] = len(set_a & set_b) / len(union) if union else float("nan")
    result["argmax_match"] = int(np.argmax(na[fa])) == int(np.argmax(nb[fb]))

    if aligned:
        diff = np.abs(a - b)
        result["max_abs"] = float(diff.max())
        result["mean_abs"] = float(diff.mean())
        mask = (np.abs(a) > LOADED_EPS) | (np.abs(b) > LOADED_EPS)
        result["rmse_loaded"] = (
            float(np.sqrt(((a[mask] - b[mask]) ** 2).mean())) if mask.any() else 0.0
        )
        ta, tb = na.sum(axis=-1), nb.sum(axis=-1)
        result["total_series_pearson"] = pearson(ta, tb)
        alpha_all, r2_all = scale_fit(ta, tb)
        result["alpha_series"] = alpha_all
        result["r2_series"] = r2_all
    return result


def fmt(value, spec=".4f"):
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float) and not np.isfinite(value):
        return "n/a"
    return format(value, spec) if isinstance(value, float) else str(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", help="label=path.npz:array_key")
    parser.add_argument("--threshold", type=float, default=0.005,
                        help="Active-taxel threshold on the normal channel, newtons")
    parser.add_argument("--from-time", type=float, default=0.0,
                        help="Ignore samples before this time; use it to skip the "
                             "landing transient and compare the held grasp")
    parser.add_argument("--to-time", type=float, default=float("inf"))
    parser.add_argument("--title", default="TAXEL COMPARISON")
    args = parser.parse_args()

    loaded = [load_source(item, args.from_time, args.to_time) for item in args.sources]
    if args.from_time > 0.0 or np.isfinite(args.to_time):
        print(f"window: t in [{args.from_time:g}, {args.to_time:g}] s")

    print("=" * 104)
    print(args.title)
    print("=" * 104)

    print(f"\n{'source':<14}{'impl':<10}{'array':<14}{'steps':>7}{'peak taxel':>12}"
          f"{'peak total':>12}{'mean total':>12}{'mean ncon':>11}{'active':>8}")
    print("-" * 104)
    summaries = {}
    for label, array, meta in loaded:
        s = summarize(label, array, meta, args.threshold)
        summaries[label] = s
        print(f"{label:<14}{s['impl']:<10}{s['key']:<14}{s['steps']:>7d}"
              f"{s['peak_taxel_normal']:>12.5f}{s['peak_total_normal']:>12.5f}"
              f"{s['mean_total_normal']:>12.5f}{s['mean_ncon']:>11.1f}"
              f"{s['active_taxels']:>8d}")
    print("-" * 104)
    print("newtons on the compression-positive normal channel; "
          f"active = taxels over {args.threshold} N at the peak frame")

    print(f"\n{'pair':<28}{'alpha':>10}{'R2':>8}{'pearson':>10}{'spearman':>10}"
          f"{'jaccard':>9}{'argmax':>8}{'max_abs':>12}{'rmse':>11}")
    print("-" * 104)
    for (la, aa, _ma), (lb, ab, _mb) in itertools.combinations(loaded, 2):
        r = compare_pair(aa, ab, args.threshold)
        print(f"{la + ' -> ' + lb:<28}"
              f"{fmt(r['alpha_peak'], '.4f'):>10}{fmt(r['r2_peak'], '.4f'):>8}"
              f"{fmt(r['pearson_peak'], '.4f'):>10}{fmt(r['spearman_peak'], '.4f'):>10}"
              f"{fmt(r['jaccard'], '.3f'):>9}{fmt(r['argmax_match']):>8}"
              f"{fmt(r.get('max_abs'), '.3e'):>12}{fmt(r.get('rmse_loaded'), '.3e'):>11}")
    print("-" * 104)
    print("alpha: least-squares 'second ~= alpha x first' over loaded taxels at the peak frame")
    print("max_abs / rmse only defined when both traces have the same step count")

    for (la, aa, _ma), (lb, ab, _mb) in itertools.combinations(loaded, 2):
        r = compare_pair(aa, ab, args.threshold)
        if not r["aligned"]:
            continue
        print(f"\n  {la} -> {lb}: total-normal series pearson "
              f"{fmt(r['total_series_pearson'], '.5f')}, "
              f"alpha {fmt(r['alpha_series'], '.4f')} (R2 {fmt(r['r2_series'], '.4f')}), "
              f"loaded taxels {r['loaded_taxels']}")


if __name__ == "__main__":
    main()
