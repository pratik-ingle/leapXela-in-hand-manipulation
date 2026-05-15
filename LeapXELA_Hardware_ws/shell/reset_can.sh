#!/usr/bin/env bash
set -euo pipefail

CAN0=${1:-can0}
CAN1=${2:-can1}
VCAN=${3:-vcan0}

echo "Resetting CAN setup for interfaces: $CAN0, $CAN1, $VCAN"

run() {
  # Run a command but don't fail the whole reset if it errors.
  # Useful for idempotency when interfaces/rules don't exist.
  set +e
  sudo "$@"
  local rc=$?
  set -e
  return $rc
}

echo "Removing CAN gateway rules (flush)."
run cangw -F >/dev/null 2>&1 || true

echo "Bringing down CAN interfaces (if present)."
run ip link set down "$CAN0" >/dev/null 2>&1 || true
run ip link set down "$CAN1" >/dev/null 2>&1 || true
run ip link set down "$VCAN" >/dev/null 2>&1 || true

echo "Deleting vcan interface (if present)."
run ip link del "$VCAN" >/dev/null 2>&1 || true

echo "Detaching slcan (if present)."
if command -v slcand >/dev/null 2>&1; then
  # Try clean detach first.
  run slcand -c -F "$CAN0" >/dev/null 2>&1 || true
  run slcand -c -F "$CAN1" >/dev/null 2>&1 || true
fi

echo "Stopping any remaining slcand processes for $CAN0/$CAN1."
run pkill -f "slcand.*[[:space:]]${CAN0}([[:space:]]|$)" >/dev/null 2>&1 || true
run pkill -f "slcand.*[[:space:]]${CAN1}([[:space:]]|$)" >/dev/null 2>&1 || true

echo "Optionally unloading modules (best-effort)."
run modprobe -r can-gw >/dev/null 2>&1 || true
run modprobe -r vcan >/dev/null 2>&1 || true
run modprobe -r slcan >/dev/null 2>&1 || true

echo "Done."

