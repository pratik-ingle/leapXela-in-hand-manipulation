#!/usr/bin/env bash
set -euo pipefail

cd /tmp

if [[ -d mujoco/.git ]]; then
  cd mujoco
  git fetch --all --tags
else
  git clone https://github.com/google-deepmind/mujoco.git
  cd mujoco
fi

git checkout main

cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=/usr/local

cmake --build build -j"$(nproc)"
cmake --install build

