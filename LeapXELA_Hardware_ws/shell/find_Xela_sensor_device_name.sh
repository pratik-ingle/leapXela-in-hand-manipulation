#!/usr/bin/env bash
set -euo pipefail

TARGET_VENDOR_ID="0403"
TARGET_MODEL_ID="6015"
EXPECTED_COUNT="${EXPECTED_COUNT:-2}"

# Use udev's by-id links to map USB devices to ttyUSB*
if [ ! -d /dev/serial/by-id ]; then
  echo "/dev/serial/by-id does not exist. Are the usbserial/ftdi_sio modules loaded?"
  exit 1
fi

echo "Looking for FTDI Bridge(I2C/SPI/UART/FIFO) devices (${TARGET_VENDOR_ID}:${TARGET_MODEL_ID})..."

matches=()
match_details=()

# Loop over by-id entries and verify vendor/model via udev properties
while IFS= read -r -d '' link; do
  dev_node="$(readlink -f "$link" || true)"
  case "$dev_node" in
    /dev/ttyUSB*) ;;
    *) continue ;;
  esac

  props="$(udevadm info -q property -n "$dev_node" 2>/dev/null || true)"
  vendor_id="$(printf '%s\n' "$props" | awk -F= '$1=="ID_VENDOR_ID"{print $2; exit}')"
  model_id="$(printf '%s\n' "$props" | awk -F= '$1=="ID_MODEL_ID"{print $2; exit}')"
  if [ "$vendor_id" = "$TARGET_VENDOR_ID" ] && [ "$model_id" = "$TARGET_MODEL_ID" ]; then
    serial_short="$(printf '%s\n' "$props" | awk -F= '$1=="ID_SERIAL_SHORT"{print $2; exit}')"
    model="$(printf '%s\n' "$props" | awk -F= '$1=="ID_MODEL"{print $2; exit}')"
    matches+=("$dev_node")
    match_details+=("by-id=$(basename "$link") serial=${serial_short:-?} model=${model:-?}")
  fi
done < <(find /dev/serial/by-id -maxdepth 1 -type l -print0 2>/dev/null)

# De-dup (multiple by-id names can point to the same ttyUSB)
unique_matches=()
unique_details=()
for i in "${!matches[@]}"; do
  seen=false
  for u in "${unique_matches[@]:-}"; do
    if [ "$u" = "${matches[$i]}" ]; then
      seen=true
      break
    fi
  done
  if [ "$seen" = false ]; then
    unique_matches+=("${matches[$i]}")
    unique_details+=("${match_details[$i]}")
  fi
done

count="${#unique_matches[@]}"
if [ "$count" -ne "$EXPECTED_COUNT" ]; then
  echo "Expected $EXPECTED_COUNT matching devices (${TARGET_VENDOR_ID}:${TARGET_MODEL_ID}) but found $count."
  echo "Matches found:"
  if [ "$count" -eq 0 ]; then
    echo "  (none)"
  else
    for i in "${!unique_matches[@]}"; do
      echo "  - ${unique_matches[$i]} (${unique_details[$i]})"
    done
  fi
  echo
  echo "Tip: run 'lsusb | grep ${TARGET_VENDOR_ID}:${TARGET_MODEL_ID}' and 'dmesg | grep ttyUSB' to confirm the kernel created ttyUSB nodes."
  exit 2
fi

for i in "${!unique_matches[@]}"; do
  echo "${unique_matches[$i]}  (${unique_details[$i]})"
done