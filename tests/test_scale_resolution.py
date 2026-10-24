"""Object size is resolved per shape, not per bucket.

The size cap tightens with object count, so a run sweeping counts 1-3 used to be
stuck at the tightest cap across every shape it collected -- `disk` sat at 0.40
because `box` was in the same run. `scale: max` gives each shape the largest size
that fits it at every requested count instead.

Per shape rather than per count on purpose: within a shape the size is constant,
so the count label cannot be read off the object size.
"""

from pathlib import Path

import pytest
import yaml

from leapxela.collect_flex_dataset import (
    MAX_SCALE,
    max_scale_across,
    parse_args,
    resolve_scales,
    scale_argument,
    validate_args,
)
from leapxela.episode import PLACEABLE_SHAPES, check_placement_feasible, max_scale_for


def _config(tmp_path, collection, name="run.yaml"):
    path = tmp_path / name
    path.write_text(yaml.safe_dump({"collection": collection}))
    return path


def _args(tmp_path, collection, extra=()):
    return parse_args(["--config", str(_config(tmp_path, collection)), *extra])


# --------------------------------------------------------------------------
# what `max` resolves to
# --------------------------------------------------------------------------
@pytest.mark.parametrize("counts", [(1,), (1, 2), (1, 2, 3), (3,)])
@pytest.mark.parametrize("shape", ["box", "disk", "cylinder", "O", "T"])
def test_max_is_the_tightest_cap_across_requested_counts(tmp_path, shape, counts):
    """Derived from SHAPE_MAX_SCALE rather than restated, so the two cannot drift."""
    args = _args(tmp_path, {"shapes": [shape], "counts": list(counts), "scale": MAX_SCALE})
    expected = min(max_scale_for(shape, count) for count in counts)
    assert resolve_scales(args) == {shape: expected}
    assert max_scale_across(shape, counts) == expected


def test_max_lifts_a_shape_that_a_harder_one_would_hold_back(tmp_path):
    """The whole point: a roomy shape is no longer pinned to a tight one's cap.

    Checked on `O`, the most pad-friendly piece, against `box`. It used to be
    `disk` against `box`, but the re-measured caps put those two level at counts
    1-3 (both 0.50), which would make this pass for the wrong reason.
    """
    shapes = ["box", "O", "T"]
    args = _args(tmp_path, {"shapes": shapes, "counts": [1, 2, 3],
                            "scale": MAX_SCALE})
    scales = resolve_scales(args)
    assert scales["O"] > scales["box"], scales
    assert scales == {
        shape: min(max_scale_for(shape, count) for count in (1, 2, 3))
        for shape in shapes
    }


def test_caps_loosen_when_fewer_counts_are_collected(tmp_path):
    """Sweeping 1-2 does not need to fit three objects on three pads."""
    two = resolve_scales(_args(tmp_path, {"shapes": ["box"], "counts": [1, 2],
                                          "scale": MAX_SCALE}))
    three = resolve_scales(_args(tmp_path, {"shapes": ["box"], "counts": [1, 2, 3],
                                            "scale": MAX_SCALE}))
    assert two["box"] > three["box"]


@pytest.mark.parametrize("shape", PLACEABLE_SHAPES)
def test_every_resolved_size_is_actually_placeable(tmp_path, shape):
    """`max` must never resolve to something the placement then refuses."""
    counts = [1, 2, 3]
    args = _args(tmp_path, {"shapes": [shape], "counts": counts, "scale": MAX_SCALE})
    scale = resolve_scales(args)[shape]
    for count in counts:
        check_placement_feasible(shape, scale, count)
    validate_args(args)


# --------------------------------------------------------------------------
# the other forms
# --------------------------------------------------------------------------
def test_a_number_applies_to_every_shape(tmp_path):
    args = _args(tmp_path, {"shapes": ["box", "disk"], "counts": [1, 2, 3], "scale": 0.35})
    assert resolve_scales(args) == {"box": 0.35, "disk": 0.35}


def test_mapping_sets_named_shapes_and_max_fills_the_rest(tmp_path):
    args = _args(tmp_path, {"shapes": ["box", "disk", "T"], "counts": [1, 2, 3],
                            "scale": {"disk": 0.5}})
    scales = resolve_scales(args)
    assert scales["disk"] == 0.5, "an explicit entry must win"
    assert scales["box"] == max_scale_across("box", [1, 2, 3]), "omitted shapes fall back"
    assert scales["T"] == max_scale_across("T", [1, 2, 3])


def test_cli_scale_overrides_a_config_mapping(tmp_path):
    args = _args(tmp_path, {"shapes": ["box", "disk"], "counts": [1, 2, 3],
                            "scale": {"disk": 0.5}}, extra=["--scale", "0.3"])
    assert resolve_scales(args) == {"box": 0.3, "disk": 0.3}


def test_max_works_from_the_command_line_too(tmp_path):
    """argparse type-converts string defaults, so `max` needs its own type."""
    assert scale_argument(MAX_SCALE) == MAX_SCALE
    assert scale_argument("0.4") == 0.4
    args = parse_args(["--shapes", "disk", "--counts", "1", "2", "3", "--scale", MAX_SCALE])
    assert resolve_scales(args) == {
        "disk": min(max_scale_for("disk", count) for count in (1, 2, 3))
    }


def test_unknown_shape_or_word_is_refused(tmp_path):
    with pytest.raises(ValueError, match="not a placeable shape"):
        parse_args(["--config", str(_config(tmp_path, {"scale": {"banana": 0.5}}))])
    with pytest.raises(ValueError, match="not understood"):
        parse_args(["--config", str(_config(tmp_path, {"scale": "biggest"}, "b.yaml"))])


# --------------------------------------------------------------------------
# calibration: candidates are sizes to try, not requests
# --------------------------------------------------------------------------
def test_bare_defaults_are_accepted():
    """`leapxela-collect` with no arguments was refused outright.

    validate_args checked every calibration candidate against the caps, and
    CALIB_SCALES reaches 1.0 -- well past most of them.
    """
    validate_args(parse_args([]))


@pytest.mark.parametrize("argv", [
    ["--shapes", "disk", "--counts", "1"],
    ["--shapes", "box", "--counts", "1", "2", "3"],
    ["--shapes", "cylinder", "--counts", "3"],
])
def test_calibration_runs_are_not_refused_for_candidate_sizes(argv):
    validate_args(parse_args(argv))


def test_an_explicit_over_cap_size_is_still_refused():
    """Loosening calibration must not loosen actual requests."""
    with pytest.raises(ValueError, match="does not fit the palm pads"):
        validate_args(parse_args(["--shapes", "box", "--counts", "3", "--scale", "0.9"]))


def test_a_calibrated_size_is_clamped_per_shape(tmp_path):
    """The sweep ranks by retention, which can land above what a shape can hold."""
    args = _args(tmp_path, {"shapes": ["box", "disk"], "counts": [1, 2, 3], "scale": 0})
    scales = resolve_scales(args, calibrated=1.0)
    assert scales["box"] == max_scale_across("box", [1, 2, 3])
    assert scales["disk"] == max_scale_across("disk", [1, 2, 3])
    # A calibrated value below every cap survives untouched.
    assert resolve_scales(args, calibrated=0.2) == {"box": 0.2, "disk": 0.2}


# --------------------------------------------------------------------------
# the shipped presets
# --------------------------------------------------------------------------
CONFIG_DIR = Path(__file__).resolve().parents[1] / "leapxela" / "configs"


@pytest.mark.parametrize("name", sorted(p.name for p in CONFIG_DIR.glob("*.yaml")))
def test_preset_resolves_to_placeable_sizes(name):
    args = parse_args(["--config", str(CONFIG_DIR / name)])
    validate_args(args)
    pending = not isinstance(args.scale, (dict, str)) and args.scale <= 0.0
    if pending:
        return
    for shape, scale in resolve_scales(args).items():
        for count in args.counts:
            check_placement_feasible(shape, scale, count)
