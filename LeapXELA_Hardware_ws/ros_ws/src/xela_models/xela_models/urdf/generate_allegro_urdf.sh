#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IN_XACRO="${SCRIPT_DIR}/allegro_hand_right.xacro"
OUT_URDF="${PWD}/allegro_hand_right_taxel1.urdf"
ROS_WS_DIR="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"

usage() {
  cat <<'EOF'
Usage:
  ./generate_allegro_urdf.sh [-o OUTPUT.urdf]

Generates a URDF from allegro_hand_right.xacro with taxel enabled (taxel:=1).

Options:
  -o  Output URDF path (default: $PWD/allegro_hand_right_taxel1.urdf)
  -h  Show this help
EOF
}

while getopts ":o:h" opt; do
  case "${opt}" in
    o) OUT_URDF="${OPTARG}" ;;
    h) usage; exit 0 ;;
    \?) echo "Unknown option: -${OPTARG}" >&2; usage; exit 2 ;;
    :) echo "Missing argument for -${OPTARG}" >&2; usage; exit 2 ;;
  esac
done

# Best-effort environment setup so $(find xela_models) works.
set +u
if [[ -n "${ROS_DISTRO:-}" && -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]]; then
  # shellcheck disable=SC1090
  source "/opt/ros/${ROS_DISTRO}/setup.bash"
elif [[ -f "/opt/ros/humble/setup.bash" ]]; then
  # shellcheck disable=SC1091
  source "/opt/ros/humble/setup.bash"
fi

if [[ -f "${ROS_WS_DIR}/install/setup.bash" ]]; then
  # shellcheck disable=SC1090
  source "${ROS_WS_DIR}/install/setup.bash"
elif [[ -f "${ROS_WS_DIR}/install/local_setup.bash" ]]; then
  # shellcheck disable=SC1090
  source "${ROS_WS_DIR}/install/local_setup.bash"
fi
set -u

if ! command -v xacro >/dev/null 2>&1; then
  echo "ERROR: 'xacro' not found in PATH. Source your ROS environment first." >&2
  exit 127
fi

if [[ ! -f "${IN_XACRO}" ]]; then
  echo "ERROR: Input xacro not found: ${IN_XACRO}" >&2
  exit 1
fi

mkdir -p "$(dirname -- "${OUT_URDF}")"

tmp_out="$(mktemp)"
trap 'rm -f "${tmp_out}"' EXIT

# taxel:=1 enables taxel geometry in xela.xacro sensor macros.
xacro --inorder "${IN_XACRO}" taxel:=1 > "${tmp_out}"
mv -f "${tmp_out}" "${OUT_URDF}"

echo "Wrote: ${OUT_URDF}"
