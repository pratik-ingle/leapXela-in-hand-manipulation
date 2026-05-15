#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
IN_XACRO="${SCRIPT_DIR}/aftc.xacro"
ROS_WS_DIR="$(cd -- "${SCRIPT_DIR}/../../../.." && pwd)"
MESH_DIR="${ROS_WS_DIR}/src/xela_models/xela_models/mesh"
OUT_URDF="${MESH_DIR}/aftc_taxel1_mujoco.urdf"

usage() {
  cat <<'EOF'
Usage:
  ./generate_aftc_for_mujoco.sh [-o OUTPUT.urdf]

Generates a URDF from aftc.xacro with taxels enabled (taxel:=1),
and rewrites URIs:
  package://xela_models/... -> ../...

Options:
  -o  Output URDF path (default: <ros_ws>/src/xela_models/xela_models/mesh/aftc_taxel1_mujoco.urdf)
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

mkdir -p "$(dirname -- "${OUT_URDF}")"
tmp_out="$(mktemp)"
trap 'rm -f "${tmp_out}"' EXIT

xacro --inorder "${IN_XACRO}" taxel:=1 > "${tmp_out}"

export TMP_OUT="${tmp_out}"
export OUT_URDF
python3 - <<'PY'
import os
import xml.etree.ElementTree as ET

tmp_out = os.environ["TMP_OUT"]
out_urdf = os.environ["OUT_URDF"]

with open(tmp_out, "r", encoding="utf-8") as f:
    s = f.read()

s = s.replace("package://xela_models/", "../")
s = s.replace("package://xela_models", "..")

root = ET.fromstring(s)

# Ensure every link has an inertial tag with mass 5g (0.005kg).
for link in root.findall("link"):
    inertial = link.find("inertial")
    if inertial is None:
        inertial = ET.Element("inertial")
        # URDF convention: inertial is typically first under <link>.
        link.insert(0, inertial)

    origin = inertial.find("origin")
    if origin is None:
        origin = ET.SubElement(inertial, "origin", {"xyz": "0 0 0", "rpy": "0 0 0"})

    mass = inertial.find("mass")
    if mass is None:
        mass = ET.SubElement(inertial, "mass", {"value": "0.005"})
    else:
        mass.set("value", "0.005")

    inertia = inertial.find("inertia")
    if inertia is None:
        inertia = ET.SubElement(inertial, "inertia")
    inertia.attrib.update(
        {
            "ixx": "1e-6",
            "ixy": "0",
            "ixz": "0",
            "iyy": "1e-6",
            "iyz": "0",
            "izz": "1e-6",
        }
    )

ET.ElementTree(root).write(out_urdf, encoding="utf-8", xml_declaration=True)
PY

echo "Wrote: ${OUT_URDF}"
