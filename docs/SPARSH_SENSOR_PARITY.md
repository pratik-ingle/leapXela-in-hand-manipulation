# Sparsh sensor: leapxela vs sparsh-skin-sim

Validation of the sparsh (Kelvin–Voigt) tactile sensor that was ported into
`leapxela` alongside the existing contact sensor, against the original in
`sparsh-skin-sim`.

Each package ran in its own conda env — `leapxela` (py3.12, numpy 1.26.4) and
`sparsh-skin` (py3.11, numpy 2.4.6) — both on mujoco 3.11.0.

> **Round 2 (after the `dt` change) is in
> [Matched-timestep three-way comparison](#matched-timestep-three-way-comparison) at the
> bottom.** With `dt=0.001` and the integrator matched, the two sparsh sensors are
> **bitwise identical** on a shared model. Everything between here and there is the
> original round, which diagnosed why they differed before.

## Verdict (round 1, dt mismatched)

**The port is numerically exact. The sensor is not calibrated for the environment
it was ported into.**

The code is a faithful copy: given the same model and the same inputs, the two
implementations produce bitwise-identical forces. But `leapxela` runs a 5× smaller
timestep and a different integrator, and the Kelvin–Voigt gain `K = 100 N/m` was
tuned for the upstream setup. In leapxela's setup the same physical grasp reads
**≈4.7× lower** relative to ground-truth contact force, and a least-squares refit
asks for **K ≈ 753 N/m**, not 100.

| | leapxela | sparsh-skin-sim |
|---|---|---|
| timestep | `0.002` | `0.010` |
| integrator | `implicitfast` | `Euler` |
| fitted `K` (scalar, vs contact ground truth) | **752.9 N/m** | **76.2 N/m** |
| shipped `DEFAULT_FLEX_STIFFNESS` | 100.0 | 100.0 |

---

## What is provably identical

The sensor substrate matches exactly, which is what makes a numeric comparison
meaningful rather than merely indicative:

- Same 18 flexes, same names, same per-flex vertex counts (24 palm / 16 phalange / 30 tip)
- Same vertex-body quaternions, same flex joint damping (0.05), same zero joint stiffness
- `hand_ss.urdf` and `leap_sensor_taxel_map.json` byte-identical across the repos
  (sha256 `4506ade6…`, `b10d7966…`)
- leapxela packs all 368 hardware taxel ids exactly once

### Force core — bitwise identical

Both libraries driven over the same model with the same deterministic control ramp,
each in its own conda env, traces diffed offline.

| scenario | model | force | displacement | velocity | contact label |
|---|---|---|---|---|---|
| A — upstream scene | sparsh scene XML | `0.0` | `0.0` | `0.0` | `4.4e-16` |
| B — leapxela hand | leapxela `.mjb`, no object | `0.0` | `0.0` | `0.0` | `0.0` |
| B2 — leapxela hand + box | leapxela `.mjb`, box on palm | `0.0` | `0.0` | `0.0` | `2.2e-16` |

Max absolute difference, 300 steps × 18 flexes. `0.0` means bitwise identical across
two Python versions and two numpy major versions. The `~1e-16` on contact labels is
float reordering inside the barycentric splat.

Scenario A reached 0.65 N peak estimated force and 1.40 N peak ground-truth contact,
so this is a loaded comparison, not a comparison of zeros.

Scenario B also confirms the **upstream core reads leapxela's generated model
unchanged** — the port did not fork the model format.

### FK layer — float32 epsilon

| field | max abs diff |
|---|---|
| `fk_order` (368-permutation) | `0.0` |
| `forces_local` | `0.0` |
| `positions` | `3.0e-08` |
| `positions_deformed` | `3.0e-08` |
| `forces_world` | `7.0e-08` |
| `rotations` | `1.2e-07` |

`1.19e-07` is exactly float32 machine epsilon (2⁻²³); the two envs ship torch 2.3.0
and 2.13.0. Nothing here is a code difference.

---

## Where behaviour diverges, and why

Same model, same library, varying **only** `dt` and integrator — this isolates the
simulation setup from the code. 2.0 s of simulated time in every row.

| setting | peak taxel | peak normal | ground-truth contact | vs upstream |
|---|---|---|---|---|
| `dt=0.010` Euler *(sparsh native)* | 0.9116 N | 0.2000 N | 1.3928 N | 1.000 |
| `dt=0.010` implicitfast | 0.2103 N | 0.2058 N | 1.5494 N | 0.231 |
| `dt=0.002` Euler | 0.1263 N | 0.1244 N | 2.6291 N | 0.139 |
| `dt=0.002` implicitfast *(leapxela native)* | 0.1264 N | 0.1245 N | 2.6292 N | 0.139 |

**The timestep dominates; the integrator is secondary.** Changing `dt` alone
reproduces leapxela's behaviour almost exactly (0.139 vs 0.139); changing the
integrator alone only gets to 0.231.

Note the two columns move in *opposite* directions: the estimated force falls 7×
while the true contact force nearly doubles. Per-flex, the estimate/ground-truth
ratio has a median of **0.4545 at dt=0.010** and **0.0959 at dt=0.002** — the
leapxela sensor under-reads by **4.7×**.

### leapxela's simulation is the more physical of the two

The upstream setting produces membrane displacements up to **9.0 mm** on
`flex_uspa46_2`, a palm pad whose taxel pitch is 7.25 mm — the skin is passing
through itself. At `dt=0.002` the same patch peaks at **0.50 mm**. The upstream
per-flex ratios also scatter wildly (0.15 → 4.86, with palm pads *over*-reading by
2.3–4.9×), while leapxela's are consistent (0.048 → 0.18).

So the divergence is not leapxela regressing. It is leapxela running a better-resolved
contact simulation while still using a gain fitted to an under-resolved one.

### Refitting the gain

Using the library's own `fit_kelvin_voigt` against MuJoCo contact wrenches:

| | `K` scalar | `K` per-axis (x, y, z) | `B` scalar |
|---|---|---|---|
| `dt=0.010` Euler | 76.2 N/m | 3.3, 43.4, 290.2 | −0.591 |
| `dt=0.002` implicitfast | 752.9 N/m | 473.9, 371.4, 947.7 | 1.886 |

The shipped default of 100 N/m is a good fit for upstream (76.2) and roughly **10×
too low** for leapxela. `FlexForceEstimator.calibrate` already exists to install a
fitted gain — `calibrate_sparsh_sensor.py` just never calls it, fitting only
noise-floor thresholds.

---

## Defects found

### 1. `calibrate_sparsh_sensor` crashed on every invocation — **fixed**

`calibration_args` built a `SimpleNamespace` without `pregrip_fraction`, which
`episode.profile_from_args` reads, so the CLI died with `AttributeError` before doing
any work. Added the field plus a `--pregrip-fraction` flag defaulting to the shared
`PREGRIP_FRACTION = 0.40`, matching `episode` and `collect_flex_dataset`.

### 2. Calibration thresholds reject every episode — **reported, not fixed**

With the generated calibration applied, all three grasps fail QA despite being
physically grasped (`held=1/1, sensed=1/1`, `contact fraction=0.00`). Without it, all
three pass.

| gate | calibrated value | actual signal | verdict |
|---|---|---|---|
| `activity_threshold_n` | 0.6393 N | 0.1193 N peak per-taxel | 5.4× too high |
| `min_peak_normal_n` | 65.08 N | 1.96 N peak total | 33× too high |

Root cause is a **startup transient**: peak |taxel normal| during the "no-object"
run is 0.447 N at **t = 0.012 s**, when the membranes settle and the hand snaps into
pre-grip. The p99.5 statistic absorbs it, then `--margin 5.0` multiplies it.

| sampling window | → `activity_threshold` | → `min_peak_normal` |
|---|---|---|
| all 0.00–2.00 s *(current)* | 0.639 N | 65.08 N |
| skip first 0.25 s | 0.068 N | 4.33 N |
| last 1.00 s | 0.027 N | 1.83 N |

Discarding a warm-up window fixes `activity_threshold`. It does **not** fix
`min_peak_normal`, which stays above the real 1.96 N signal until the very last
window — because that gate multiplies a 368-taxel *sum* of noise by 5, while a real
grasp concentrates its signal on a few taxels. Both need a decision about calibration
policy, so they are left alone.

### 3. Recorded `sha256` can never validate the file — **reported, not fixed**

`calibrate_sparsh_sensor.py` digests the JSON *before* inserting the `sha256` key,
then rewrites the file. Measured on a real run: recorded `828e4907…`, actual
`b0e79cf2…`. `episode.apply_sparsh_calibration` consumes this payload.

### 4. API divergence: `flex_vertex_contact_forces` lost its `None` sentinel

Upstream accepts `contact_geom_names=None` to mean "count every contact". The port
requires an explicit list, and passing `[]` silently returns all zeros instead of
everything. Covered by a regression test so the asymmetry is at least documented.

---

## Test suite

29 tests, all passing (`conda run -n leapxela python -m pytest tests/`), ~15 s.

- `tests/test_sparsh_parity.py` (10) — topology, estimator trajectories, upstream
  reading leapxela's model, the shared `damping == 0.05` override, FK asset hashes,
  FK permutation, FK frames over 4 poses. Runs both libraries in one interpreter.
- `tests/test_sparsh_sensor.py` (15) — leapxela-only wrapper behaviour: 368-taxel
  coverage, contact/sparsh sharing a taxel assignment, the z-flip sign convention
  checked against MuJoCo contact wrenches, active-taxel counting, both-source
  agreement, mode switches, `resolve_heatmap_sources` error branches.
- `tests/test_leapxela_dual_sensors.py` (4) — pre-existing; these were dying at
  collection before the env fix.

**The z-flip in `sensors.py:62` is correct.** It is the port's one deliberate
divergence from upstream, and it agrees with ground-truth contact sign under load.

### Cross-env harness

`tests/sparsh_compare/` holds the two-env drivers used for the tables above. The
pytest modules run both libraries in one interpreter for speed; these scripts run each
package in its own env, which is the configuration that actually ships.

```bash
# force core, each side in its own env
conda run -n sparsh-skin python tests/sparsh_compare/dump_sensor_trace.py \
    --impl sparsh   --model sparsh-xml --out ss.npz
conda run -n leapxela    python tests/sparsh_compare/dump_sensor_trace.py \
    --impl leapxela --model sparsh-xml --out lx.npz
python tests/sparsh_compare/compare_traces.py ss.npz lx.npz

# leapxela's model into the sparsh env, via a compiled .mjb
conda run -n leapxela python tests/sparsh_compare/export_leapxela_mjb.py \
    --object box --out hand.mjb

# behavioural table (matched simulated time, not step count)
conda run -n leapxela python tests/sparsh_compare/dump_sensor_trace.py \
    --impl leapxela --model sparsh-xml --duration 2.0 --dt 0.01 --integrator euler --out a.npz
python tests/sparsh_compare/summarize_traces.py a=a.npz b=b.npz --baseline a
```

`.mjb` is how a leapxela-built model crosses into the sparsh env: both run mujoco
3.11.0, so a binary model round-trips exactly with assets baked in, and the sparsh env
never needs the leapxela package.

`sparsh-skin-sim` is a separate untracked checkout and was **not modified**.

---

## Environment

`pytorch_kinematics` was missing from the `leapxela` env, so `leapxela.episode`,
`leapxela.fk_taxel` and `leapxela.calibrate_sparsh_sensor` all failed at import —
nothing sparsh-related ran there at all.

`pip install -e ".[leapxela]" && pip install -e ".[dev]"` resolved cleanly:
**numpy stayed at 1.26.4**, mujoco 3.11.0 and torch 2.3.0 untouched. Added
pytorch-kinematics 0.10.0, arm_pytorch_utilities, pytorch_seed, lxml, pytest 9.1.1,
ruff. The stale `entry_points.txt` refreshed, so `leapxela-calibrate-sparsh` is now on
PATH.

## Recommended next steps

1. **Refit `K` for leapxela's timestep.** Have `calibrate_sparsh_sensor` call
   `FlexForceEstimator.calibrate` / `fit_kelvin_voigt` against contact ground truth
   and write the fitted gains, rather than shipping the upstream 100 N/m. Expect
   ~750 N/m scalar, or per-axis with the normal channel near 950 N/m.
2. **Discard a warm-up window** before computing the noise floor — the first 0.25 s
   is settling, not noise.
3. **Reconsider `min_peak_normal`** — scaling a 368-taxel noise sum by `--margin 5.0`
   produces a gate above any real grasp.
4. **Fix the `sha256` ordering** so the digest validates the file it is stored in.

---
---

# Matched-timestep three-way comparison

Round 2, after `leapxela` moved to `dt=0.001`. Three readouts compared on a matched
test setup: **leapxela sparsh**, **sparsh-skin-sim sparsh**, and **leapxela contact**.

## Verdict

**With the timestep and integrator matched, the two sparsh sensors are bitwise
identical.** The round-1 gap was entirely simulation setup, not code.

**The contact sensor reports nearly the same total force but distributes it very
differently** — same total to within 5%, spread over 7× more taxels.

## Setup

`dt = 0.001`, `integrator = Euler`, `iterations = 50`, `tolerance = 0.0`,
`squeeze` pattern, 22 mm box at 0.3 kg, 2.5 s, `K = 100 N/m`. Every trace logs these
and they are asserted, not eyeballed.

Three things were verified equal before any sensor number was trusted:

- **Taxel indexing**: leapxela's `skin.taxel_ids` and upstream's
  `fk_taxel_util.build_flex_taxel_mapper` agree on **368/368** taxel ids →
  `(flex, vertex)`. Each side packs with its own function, so this is tested, not assumed.
- **Grasp policy**: `episode.control_targets` and `motion_util.grasp_target` produce
  **bitwise-identical** targets for all six patterns (`hold`, `pulse`, `squeeze`,
  `regrasp`, `tap`, `shear`); actuator order and `ctrlrange` also match. The policy is
  as exact a port as the sensor.
- **Object contact parameters**: friction `(0.8, 0.005, 0.0001)`, size, `solref` and
  `solimp` already match; only `contype`/`conaffinity` differed (3/3 vs 1/2), and
  matching them changed nothing measurable.

### One correction to note

`sparsh-skin-sim` is **still running at `dt=0.01`** on disk. The edit to
`leapXELA_model/simplify_model_for_mjx_flex.py` was never regenerated into
`leapXela_generated_mjx_flex_sensorCoACD.xml`, which still declares
`timestep="0.01" integrator="Euler"`. The harness overrides `dt` at runtime, so these
results are correct — but a plain `demos/` or `data_collection` run still uses 0.01.

## Run 1 — shared model, held-grasp window (t ≥ 1.5 s)

One `.mjb` carried across both envs, same replayed control trajectory
(sha `5f3f3c5a…`), so every input is bit-identical.

| source | peak taxel | peak total | mean total | mean ncon | active taxels |
|---|---|---|---|---|---|
| leapxela sparsh | 0.06993 N | 2.39161 N | 2.38565 N | 73.0 | 168 |
| sparsh-skin-sim sparsh | 0.06993 N | 2.39161 N | 2.38565 N | 73.0 | 168 |
| leapxela contact | 0.19379 N | 2.29072 N | 2.28070 N | 73.0 | **24** |

| pair | α | R² | Pearson | Spearman | Jaccard | max abs | RMSE |
|---|---|---|---|---|---|---|---|
| lx-sparsh → ss-sparsh | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.000** | **0.0** | **0.0** |
| lx-sparsh → lx-contact | 1.7267 | 0.8633 | 0.9539 | 0.4998 | 0.143 | 1.24e-01 | 9.02e-03 |

The two sparsh readouts match to `max_abs = 0.000e+00` across the full
`(2500, 368, 3)` trace, in two Python versions and two numpy major versions.

## What the contact sensor tells you that sparsh does not

Both sensors are on the same hand, same step, same contact:

- **Total force agrees to ~5%** — 2.29 N contact vs 2.39 N sparsh.
- **Spatial distribution does not.** Contact concentrates on **24** taxels peaking at
  0.194 N; sparsh spreads the same load over **168** taxels peaking at 0.070 N.
- Pearson 0.954 with Spearman 0.500: where both see load they agree on magnitude, but
  they rank the many small readings differently. Jaccard 0.143 — they mostly disagree
  about which taxels count as "active".

This is physically expected rather than a defect: contact wrenches are localized to
actual contact points, while `K·u + B·v` reads membrane displacement, which propagates
to neighbouring vertices. **It does mean an activity threshold tuned on one sensor will
not transfer to the other.**

## Run 2 — native scenes

Each package built its own scene with a matched box and matched grasp. This run does
**not** isolate the sensor, and the reason is the finding.

| source | peak taxel | mean total | mean ncon | active |
|---|---|---|---|---|
| leapxela, level palm | 0.06993 N | 2.38565 N | 73.0 | 168 |
| leapxela, palm tilted 17.72° | 0.06391 N | 2.24248 N | 67.0 | 116 |
| sparsh-skin-sim native | 0.00505 N | 0.76873 N | **4.0** | 120 |

**The upstream scene does not retain the object.** Held contacts collapse from 73 to
4 after the close, so its taxel values reflect a dropped box, not a weaker sensor.

The two hands are mounted differently in world space:

| | palm normal | tilt from +z | palm centre |
|---|---|---|---|
| leapxela | `[0, 0, 1]` | **0.00°** | `[-0.005, 0.096, 0.132]` |
| sparsh-skin-sim | `[0.304, -0.001, 0.953]` | **17.72°** | `[0.102, 0.016, -0.009]` |

leapxela levels the palm through `tilt_palm`; the upstream scene keeps the hand's
natural URDF pose, and the pad axes are additionally yawed ~90°.

Tilt alone does **not** explain the loss: leapxela at the same 17.72° still holds 67
contacts. So retention comes from the rest of leapxela's scene setup — object placed
at resting height, pre-curl applied before placement, and the trimmed pad boxes.
Sensitivity of the sensor itself to that tilt is small and well behaved:
level → tilted gives α 0.919, Pearson 0.992, Spearman 0.943.

## How to reproduce

```bash
# Run 1 — shared model
conda run -n leapxela python tests/sparsh_compare/export_leapxela_mjb.py \
    --object box --pattern squeeze --duration 2.5 --dt 0.001 --integrator euler \
    --out $S/shared_hand.mjb
conda run -n leapxela    python tests/sparsh_compare/dump_sensor_trace.py \
    --impl leapxela --sensors both --model $S/shared_hand.mjb \
    --ctrl $S/shared_hand.ctrl.npy --out $S/lx.npz
conda run -n sparsh-skin python tests/sparsh_compare/dump_sensor_trace.py \
    --impl sparsh --model $S/shared_hand.mjb \
    --ctrl $S/shared_hand.ctrl.npy --out $S/ss.npz

conda run -n leapxela python tests/sparsh_compare/compare_taxels.py \
    lx-sparsh=$S/lx.npz:sparsh_flat ss-sparsh=$S/ss.npz:sparsh_flat \
    lx-contact=$S/lx.npz:contact_flat --from-time 1.5

# Run 2 — native scenes
conda run -n leapxela    python tests/sparsh_compare/dump_native_trace.py --impl leapxela ...
conda run -n sparsh-skin python tests/sparsh_compare/dump_native_trace.py --impl sparsh ...
```

`--from-time 1.5` is important: the global peak lands during the object's initial
impact, a transient that says little about the held grasp.

## What this changes

1. **The port is settled.** No further sparsh-vs-sparsh validation is needed; the
   pytest suite (29 tests) covers it as a regression.
2. **`K = 100 N/m` is still the round-1 problem.** dt=0.001 makes the two sensors
   agree with *each other*, but both still under-read against contact ground truth.
   Refitting the gain remains the open item.
3. **Don't compare leapxela and sparsh-skin-sim through their native scenes** — the
   hand mounting and object retention differ enough to swamp any sensor signal. Use
   the shared-`.mjb` path.
4. **Regenerate the upstream scene** if you want `demos/` and `data_collection` to run
   at 0.001; the script edit alone does not affect them.
