"""YAML configuration for dataset collection.

`collect_flex_dataset` takes 54 arguments, so reproducing a dataset means
reproducing a 54-flag command line. A config file records the whole run in one
place; the CLI still wins where both set a value, so a single config can be
reused while sweeping one knob.

The section for each argument is derived from its name prefix rather than a
hand-written table, so a newly added flag lands in the right place on its own and
the schema cannot drift from the parser.

    collection:            # what to sweep and how much of it
      shapes: [box, disk, T]
      counts: [1, 2, 3]
      scale: 0.4
    grasp:                 # how the hand closes
      pattern: squeeze
    placement:             # where objects start
      mode: per-pad
    sparsh:                # Kelvin-Voigt sensor parameters
      stiffness: 100.0
    render:                # video and heatmap output
      video_samples: 1
    calibration:           # the object-size search, when scale is 0
      trials: 3
"""

import argparse
from pathlib import Path
from typing import Any

import yaml

from leapxela.episode import PLACEABLE_SHAPES

# Ordered: the first matching prefix wins, so put the more specific rules first.
# Verified to partition every collector argument with no leftovers or collisions.
SECTION_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("sparsh", ("sparsh_",)),
    ("calibration", ("calib_",)),
    ("render", ("cloud_", "arrow_", "heatmap_", "force_scale", "video_", "orbit_")),
    ("grasp", ("grip_", "thumb_", "pregrip_", "pulse_", "shear_", "squeeze_", "grasp_")),
    # zone_weights/min_pad_coverage are placement knobs without the prefix: the
    # flags read better short, and naming them here beats renaming the flags.
    ("placement", ("placement_", "settle_", "palm_", "object_adhesion",
                   "zone_weights", "min_pad_coverage")),
)
# Everything a rule does not claim.
DEFAULT_SECTION = "collection"
SECTIONS = (DEFAULT_SECTION,) + tuple(name for name, _ in SECTION_RULES)

# Where a section's own name is redundant inside it, the prefix is dropped:
# `sparsh_stiffness` reads as `sparsh.stiffness`, not `sparsh.sparsh_stiffness`.
# Sections absent here keep the full argument name.
SECTION_STRIP = {
    "sparsh": "sparsh_",
    "calibration": "calib_",
    "placement": "placement_",
    "grasp": "grasp_",
}


def split_dest(dest: str) -> tuple[str, str]:
    """Argument name -> (section, key in that section)."""
    for name, prefixes in SECTION_RULES:
        if dest.startswith(prefixes):
            strip = SECTION_STRIP.get(name)
            if strip and dest.startswith(strip):
                return name, dest[len(strip):]
            return name, dest
    return DEFAULT_SECTION, dest


# `--config` names the file being read, so it is not itself settable from inside
# one; allowing it would invite a config that silently points at another.
NOT_CONFIGURABLE = frozenset({argparse.SUPPRESS, "help", "config"})


def parser_actions(parser: argparse.ArgumentParser) -> dict:
    """Argument name -> its argparse action, for type and choices checking."""
    return {
        action.dest: action
        for action in parser._actions
        if action.dest not in NOT_CONFIGURABLE
    }


def dest_by_key(parser: argparse.ArgumentParser) -> dict[tuple[str, str], str]:
    """(section, key) -> argument name, built by inverting `split_dest`.

    Derived from the parser rather than by re-adding the stripped prefix: only
    some of a section's arguments carry it. `grasp.pattern` is `grasp_pattern`,
    but `grasp.grip_fraction` is plain `grip_fraction`, and there is no way to
    tell which from the key alone.
    """
    mapping: dict[tuple[str, str], str] = {}
    for dest in parser_actions(parser):
        pair = split_dest(dest)
        if pair in mapping:
            raise ValueError(
                f"section rules are ambiguous: {dest} and {mapping[pair]} "
                f"both map to {pair}"
            )
        mapping[pair] = dest
    return mapping


def config_schema(parser: argparse.ArgumentParser) -> dict[str, list[str]]:
    """Valid keys per section, for building configs and for error messages."""
    schema: dict[str, list[str]] = {name: [] for name in SECTIONS}
    for section, key in dest_by_key(parser):
        schema[section].append(key)
    return {name: sorted(keys) for name, keys in schema.items() if keys}


# `scale` is the one argument whose config form is richer than its CLI form: a
# number, the string "max", or a per-shape mapping. Forcing the parser's float
# type on it would reject the last two.
POLYMORPHIC = frozenset({"scale"})
MAX_SCALE = "max"


def _check_scale(value, shapes):
    """Validate the polymorphic `scale`, naming the accepted forms on failure."""
    if isinstance(value, str):
        if value == MAX_SCALE:
            return value
        # A quoted number is still a number: `scale: "0.4"` is valid YAML and
        # must not be mistaken for an unknown sentinel.
        try:
            return float(value)
        except ValueError:
            raise ValueError(
                f"scale: {value!r} is not understood; use a number, "
                f"'{MAX_SCALE}', or a mapping of shape to number"
            )
    if isinstance(value, dict):
        out = {}
        for shape, size in value.items():
            if shape not in shapes:
                raise ValueError(
                    f"scale: '{shape}' is not a placeable shape; expected one of "
                    f"{sorted(shapes)}"
                )
            try:
                out[shape] = float(size)
            except (TypeError, ValueError):
                raise ValueError(f"scale.{shape}: {size!r} is not a number")
        return out
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(
            f"scale: {value!r} is not understood; use a number, "
            f"'{MAX_SCALE}', or a mapping of shape to number"
        )


def _coerce(action, value, dest: str):
    """Apply the argument's own type and choices.

    argparse validates neither for values injected through `set_defaults`, so a
    config could otherwise smuggle in a string where a float is expected, or a
    `sensor_mode` that no code path handles.
    """
    # A list-valued argument written as a scalar must become a one-item list.
    # `pattern: squeeze` otherwise arrives as a string and gets *indexed* like a
    # sequence downstream, quietly selecting the grasp pattern 's'.
    wants_list = action.nargs in ("+", "*") or isinstance(action.nargs, int)
    if wants_list and value is not None and not isinstance(value, list):
        value = [value]

    if action.type is not None and value is not None:
        try:
            if isinstance(value, list):
                value = [action.type(item) for item in value]
            elif not isinstance(value, bool):
                value = action.type(value)
        except (TypeError, ValueError) as error:
            raise ValueError(f"{dest}: cannot read {value!r} as {action.type.__name__}: {error}")
    if action.choices is not None:
        candidates = value if isinstance(value, list) else [value]
        for item in candidates:
            if item not in action.choices:
                raise ValueError(
                    f"{dest}: {item!r} is not one of {list(action.choices)}"
                )
    return value


def _resolve_paths(action, value, base: Path):
    """Make relative paths relative to the config file, not the working directory.

    A shipped config names `data/...`; without this it would resolve differently
    depending on where the collector happened to be launched from.
    """
    if action.type is not Path or value is None:
        return value
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def load_config(path: Path | str, parser: argparse.ArgumentParser) -> dict[str, Any]:
    """Read a config into `{argument_name: value}` ready for `set_defaults`.

    Unknown sections and unknown keys raise rather than being ignored. Silently
    skipping them means a typo such as `shape:` for `shapes:` quietly collects
    the default shape set instead of the one that was asked for.
    """
    config_path = Path(path)
    if not config_path.is_file():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with config_path.open(encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError(f"Config root must be a mapping: {config_path}")

    actions = parser_actions(parser)
    schema = config_schema(parser)
    lookup = dest_by_key(parser)
    base = config_path.resolve().parent
    flat: dict[str, Any] = {}

    for section, entries in raw.items():
        if section not in schema:
            raise ValueError(
                f"{config_path}: unknown section '{section}'; "
                f"expected one of {sorted(schema)}"
            )
        if entries is None:
            continue
        if not isinstance(entries, dict):
            raise ValueError(f"{config_path}: section '{section}' must be a mapping")
        for key, value in entries.items():
            dest = lookup.get((section, key))
            if dest is None:
                raise ValueError(
                    f"{config_path}: unknown key '{section}.{key}'; "
                    f"'{section}' accepts {schema[section]}"
                )
            action = actions[dest]
            if dest in POLYMORPHIC:
                flat[dest] = _check_scale(value, set(PLACEABLE_SHAPES))
                continue
            flat[dest] = _resolve_paths(action, _coerce(action, value, dest), base)
    return flat


def dump_schema(parser: argparse.ArgumentParser) -> str:
    """A commented skeleton config listing every argument and its default."""
    lines = ["# Every collector argument, with its default. Delete what you do not need."]
    actions = parser_actions(parser)
    lookup = dest_by_key(parser)
    for section, keys in config_schema(parser).items():
        lines.append(f"{section}:")
        for key in keys:
            action = actions[lookup[(section, key)]]
            default = action.default
            if isinstance(default, Path):
                default = str(default)
            # Help strings wrap across source lines; a raw newline here would
            # end the YAML comment and leave the rest as broken syntax.
            note = " ".join((action.help or "").split())
            lines.append(f"  {key}: {default!r}" + (f"   # {note}" if note else ""))
    return "\n".join(lines) + "\n"
