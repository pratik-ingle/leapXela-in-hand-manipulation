"""Filesystem anchors for the leapxela package.

Deliberately duplicates repo_root()/data_dir() from mantaray/paths.py rather
than sharing them: leapxela runs in a different conda env with an incompatible
MuJoCo pin and must not import mantaray. A fourth package for 25 lines would
cost more than the duplication.
"""

import os
from pathlib import Path

MJCF_DIR = Path(__file__).resolve().parent / "mjcf"

# Vendored calibration inputs for taxel_layout.build_layout(). Holds only the
# three files build_layout actually reads (it ET-parses robot.xml and execs
# leapXelaMap.py; it never compiles the model), so the 13 MB upstream mesh tree
# is not needed and the pipeline runs from a fresh clone.
HAND_WORKSPACE = Path(__file__).resolve().parent / "hardware"


def repo_root() -> Path:
    """Repo root, so run outputs land in the tracked ./data tree.

    Walks up for a directory holding both pyproject.toml and .git, so a vendored
    copy inside another repo cannot false-positive. Override with
    JEPA_TACTILE_ROOT.
    """
    override = os.environ.get("JEPA_TACTILE_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").exists() and (parent / ".git").exists():
            return parent
    return Path.cwd()


def data_dir() -> Path:
    return repo_root() / "data"
