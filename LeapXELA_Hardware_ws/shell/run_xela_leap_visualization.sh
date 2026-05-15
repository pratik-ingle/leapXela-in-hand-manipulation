#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

./run_xela_server_leap.sh &
SERVER_PID=$!

cleanup() {
  echo "Stopping XELA server..."
  kill "$SERVER_PID" 2>/dev/null || true
  wait "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "Waiting for XELA server to start..."
sleep 3

./visulize_xela_leap.sh
