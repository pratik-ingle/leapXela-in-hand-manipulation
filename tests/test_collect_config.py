"""YAML configuration for dataset collection.

The collector takes 54 arguments, so a run is only reproducible if it can be
written down. The config supplies defaults and the CLI still wins, which is the
property most of these tests pin.

The section for each argument is derived from its name prefix rather than a
hand-written mapping, so the round-trip tests here are what stop the schema
drifting from the parser as arguments are added.
"""

from pathlib import Path

import pytest
import yaml

from leapxela.collect_config import (
    DEFAULT_SECTION,
    NOT_CONFIGURABLE,
    SECTIONS,
    config_schema,
    dest_by_key,
    dump_schema,
    load_config,
    parser_actions,
    split_dest,
)
from leapxela.collect_flex_dataset import build_parser, parse_args, validate_args

CONFIG_DIR = Path(__file__).resolve().parents[1] / "leapxela" / "configs"


@pytest.fixture(scope="module")
def parser():
    return build_parser()


def _write(tmp_path, payload, name="run.yaml"):
    path = tmp_path / name
    path.write_text(yaml.safe_dump(payload))
    return path


# --------------------------------------------------------------------------
# schema: sections are derived, so they must stay a clean partition
# --------------------------------------------------------------------------
def test_sections_partition_every_argument(parser):
    """No argument may be dropped or land in two sections."""
    dests = set(parser_actions(parser))
    mapping = dest_by_key(parser)
    assert set(mapping.values()) == dests
    assert len(mapping) == len(dests), "two arguments collapsed onto one key"
    for (section, _key), dest in mapping.items():
        assert section in SECTIONS
        assert split_dest(dest)[0] == section


def test_key_round_trips_back_to_its_argument(parser):
    mapping = dest_by_key(parser)
    for (section, key), dest in mapping.items():
        assert split_dest(dest) == (section, key)


def test_section_prefix_is_stripped_only_where_it_is_real(parser):
    """`grasp.pattern` is grasp_pattern, but `grasp.grip_fraction` is grip_fraction.

    Re-adding the prefix by rule produced `grasp_grip_fraction`, which is not an
    argument -- hence deriving the reverse map from the parser instead.
    """
    mapping = dest_by_key(parser)
    assert mapping[("grasp", "pattern")] == "grasp_pattern"
    assert mapping[("grasp", "grip_fraction")] == "grip_fraction"
    assert mapping[("sparsh", "stiffness")] == "sparsh_stiffness"
    assert mapping[("calibration", "scales")] == "calib_scales"
    assert mapping[("placement", "mode")] == "placement_mode"
    assert mapping[("placement", "palm_pitch")] == "palm_pitch"
    assert mapping[("collection", "shapes")] == "shapes"


def test_config_itself_is_not_configurable(parser):
    """A config naming another config would be a confusing indirection."""
    assert "config" in NOT_CONFIGURABLE
    assert "config" not in parser_actions(parser)
    assert "config" not in config_schema(parser)[DEFAULT_SECTION]


def test_dump_schema_is_loadable_yaml(parser):
    """The generated skeleton must itself be a valid config."""
    text = dump_schema(parser)
    parsed = yaml.safe_load(text)
    assert set(parsed) <= set(SECTIONS)
    for section, keys in config_schema(parser).items():
        assert set(parsed[section]) == set(keys)


# --------------------------------------------------------------------------
# precedence: CLI > config > argparse default
# --------------------------------------------------------------------------
def test_config_supplies_defaults(tmp_path):
    path = _write(tmp_path, {"collection": {"samples": 5, "workers": 3}})
    args = parse_args(["--config", str(path)])
    assert args.samples == 5
    assert args.workers == 3


def test_cli_beats_config(tmp_path):
    path = _write(tmp_path, {"collection": {"samples": 5, "workers": 3}})
    args = parse_args(["--config", str(path), "--samples", "20"])
    assert args.samples == 20, "an explicit flag must win over the config"
    assert args.workers == 3, "untouched config values must survive"


def test_arguments_in_neither_keep_their_default(tmp_path):
    path = _write(tmp_path, {"collection": {"samples": 5}})
    default = parse_args([]).max_attempts
    assert parse_args(["--config", str(path)]).max_attempts == default


def test_config_path_is_recorded_on_args(tmp_path):
    path = _write(tmp_path, {"collection": {"samples": 2}})
    assert parse_args(["--config", str(path)]).config == path
    assert parse_args([]).config is None


# --------------------------------------------------------------------------
# strictness: a typo must fail loudly, not silently collect the wrong thing
# --------------------------------------------------------------------------
def test_unknown_section_is_refused(tmp_path, parser):
    path = _write(tmp_path, {"collektion": {"samples": 2}})
    with pytest.raises(ValueError, match="unknown section 'collektion'"):
        load_config(path, parser)


def test_unknown_key_is_refused_and_lists_the_valid_ones(tmp_path, parser):
    """`shape:` for `shapes:` would otherwise collect the default shape set."""
    path = _write(tmp_path, {"collection": {"shape": ["box"]}})
    with pytest.raises(ValueError, match="unknown key 'collection.shape'"):
        load_config(path, parser)


def test_key_in_the_wrong_section_is_refused(tmp_path, parser):
    path = _write(tmp_path, {"grasp": {"samples": 2}})
    with pytest.raises(ValueError, match="unknown key 'grasp.samples'"):
        load_config(path, parser)


def test_non_mapping_root_and_section_are_refused(tmp_path, parser):
    flat = tmp_path / "flat.yaml"
    flat.write_text("- just\n- a list\n")
    with pytest.raises(ValueError, match="root must be a mapping"):
        load_config(flat, parser)

    bad = _write(tmp_path, {"collection": 5}, "bad.yaml")
    with pytest.raises(ValueError, match="must be a mapping"):
        load_config(bad, parser)


def test_missing_config_file_is_refused(tmp_path, parser):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nope.yaml", parser)


def test_empty_config_is_accepted(tmp_path, parser):
    path = tmp_path / "empty.yaml"
    path.write_text("")
    assert load_config(path, parser) == {}


# --------------------------------------------------------------------------
# types and choices, which argparse does not apply to injected defaults
# --------------------------------------------------------------------------
def test_types_are_applied(tmp_path, parser):
    path = _write(tmp_path, {
        "collection": {"counts": [1, 2], "scale": "0.4", "output_root": "/tmp/x"},
    })
    flat = load_config(path, parser)
    assert flat["counts"] == [1, 2]
    assert isinstance(flat["scale"], float) and flat["scale"] == 0.4
    assert isinstance(flat["output_root"], Path)


def test_choices_are_validated(tmp_path, parser):
    path = _write(tmp_path, {"collection": {"sensor_mode": "bogus"}})
    with pytest.raises(ValueError, match="not one of"):
        load_config(path, parser)


def test_choices_are_validated_per_item_for_lists(tmp_path, parser):
    path = _write(tmp_path, {"collection": {"shapes": ["box", "banana"]}})
    with pytest.raises(ValueError, match="banana"):
        load_config(path, parser)


def test_unreadable_value_names_the_argument(tmp_path, parser):
    path = _write(tmp_path, {"collection": {"workers": "many"}})
    with pytest.raises(ValueError, match="workers"):
        load_config(path, parser)


# --------------------------------------------------------------------------
# paths resolve against the config, so a shipped config is relocatable
# --------------------------------------------------------------------------
def test_relative_paths_resolve_against_the_config_not_the_cwd(tmp_path, parser):
    nested = tmp_path / "cfg"
    nested.mkdir()
    path = _write(nested, {"collection": {"output_root": "out/here"}})
    flat = load_config(path, parser)
    assert flat["output_root"] == (nested / "out" / "here").resolve()


def test_absolute_paths_are_left_alone(tmp_path, parser):
    path = _write(tmp_path, {"collection": {"output_root": "/var/data/run"}})
    assert load_config(path, parser)["output_root"] == Path("/var/data/run")


# --------------------------------------------------------------------------
# the shipped presets must actually work
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "name", sorted(p.name for p in CONFIG_DIR.glob("*.yaml"))
)
def test_shipped_preset_loads_and_validates(name):
    """Including validate_args, so a preset can never ship an over-cap size."""
    args = parse_args(["--config", str(CONFIG_DIR / name)])
    validate_args(args)
    assert args.shapes and args.counts
    assert args.output_root.is_absolute()


def test_presets_exist():
    assert sorted(p.name for p in CONFIG_DIR.glob("*.yaml")), "no presets shipped"


def test_scalar_is_wrapped_for_list_valued_arguments(tmp_path, parser):
    """`pattern: squeeze` must not arrive as a bare string.

    grasp_pattern is nargs="+", and the collector indexes it per sample. A plain
    string is indexable, so it silently selected the grasp pattern 's' instead of
    failing.
    """
    path = _write(tmp_path, {
        "grasp": {"pattern": "squeeze"},
        "collection": {"shapes": "box", "counts": 2},
    })
    flat = load_config(path, parser)
    assert flat["grasp_pattern"] == ["squeeze"]
    assert flat["shapes"] == ["box"]
    assert flat["counts"] == [2]


def test_a_list_stays_a_list(tmp_path, parser):
    path = _write(tmp_path, {"grasp": {"pattern": ["squeeze", "pulse"]}})
    assert load_config(path, parser)["grasp_pattern"] == ["squeeze", "pulse"]


# --------------------------------------------------------------------------
# on-disk layout: one folder per grasp pattern under count_N/
# --------------------------------------------------------------------------
def test_bucket_dir_nests_pattern_under_count(tmp_path):
    from leapxela.collect_flex_dataset import bucket_dir, group_buckets

    path = bucket_dir(tmp_path, "box", 3, "squeeze")
    assert path == tmp_path / "box" / "count_3" / "squeeze"


def test_group_buckets_splits_by_pattern():
    from leapxela.collect_flex_dataset import group_buckets

    outcomes = [
        {"shape": "box", "count": 3, "pattern": "hold", "sample": 0,
         "attempts_used": 1, "record": {"path": "box/count_3/hold/sample_000"}},
        {"shape": "box", "count": 3, "pattern": "squeeze", "sample": 0,
         "attempts_used": 2, "record": {"path": "box/count_3/squeeze/sample_000"}},
    ]
    buckets = group_buckets(outcomes, ["box"], [3], ["squeeze", "hold"], 1)
    assert [b["pattern"] for b in buckets] == ["squeeze", "hold"]
    assert buckets[0]["accepted"] == 1
    assert buckets[1]["samples"][0]["path"].endswith("hold/sample_000")

