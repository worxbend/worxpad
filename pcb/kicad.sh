#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Runs a command inside the pinned KiCad 10.0.7 container (digest in tools/images.lock), network off,
# repository mounted at /w. tools/kicad_env.sh seeds the library tables first.
#   pcb/kicad.sh python3 pcb/gen/build.py schematic
set -eu
repo_root=$(cd "$(dirname "$0")/.." && pwd)
image=$(awk '$1 == "kicad/kicad:10.0.7" { print $2 }' "$repo_root/tools/images.lock")
[ -n "$image" ] || { echo "kicad/kicad:10.0.7 is not in tools/images.lock" >&2; exit 1; }
exec docker run --rm --network none --user "$(id -u):$(id -g)" -e HOME=/tmp -e PYTHONHASHSEED=0 \
    -v "$repo_root:/w" -w /w "$image" bash -c 'bash tools/kicad_env.sh && "$@"' kicad.sh "$@"
