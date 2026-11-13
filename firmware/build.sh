#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Build the worxpad ZMK firmware in the digest-pinned zmk-build-arm image and write firmware/dist/worxpad.uf2.
#
#   bash firmware/build.sh            (or: make firmware)
#
# Steps:
#   1. Tag the image from its digest in tools/images.lock (pull by digest only if it is not present).
#   2. West workspace in firmware/.build/ws. `west update` runs only when firmware/zmk/config/west.yml changed
#      since the last fetch; it is the only step with network (about 3 GB on the first run).
#   3. `west build` with --network none, the studio-rpc-usb-uart snippet and CONFIG_ZMK_STUDIO=y. The log is
#      firmware/.build/worxpad.log; the memory summary is printed at the end.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
TAG="zmkfirmware/zmk-build-arm:stable"
DIGEST="$(awk -v tag="$TAG" '$1 == tag { print $2 }' "$REPO/tools/images.lock")"
[[ -n "$DIGEST" ]] || { echo "$TAG is not in tools/images.lock" >&2; exit 1; }

WS_REL="firmware/.build/ws"
WS="$REPO/$WS_REL"
BUILD_REL="firmware/.build/worxpad"
LOG="$REPO/firmware/.build/worxpad.log"
MANIFEST="$REPO/firmware/zmk/config/west.yml"
FETCHED="$WS/.west/west.yml.fetched"

if ! docker image inspect "$DIGEST" >/dev/null 2>&1; then
    docker pull --quiet "$DIGEST"
fi
docker tag "$DIGEST" "$TAG"

mkdir -p "$WS/config" "$REPO/firmware/.build/ccache" "$REPO/firmware/dist"

# run_in_image <network> <command>: the repository at /w, working directory the west workspace.
run_in_image() {
    local network="$1" command="$2"
    docker run --rm --network "$network" -u "$(id -u):$(id -g)" -e HOME=/tmp \
        -e CCACHE_DIR=/w/firmware/.build/ccache \
        -v "$REPO":/w -w "/w/$WS_REL" "$TAG" bash -c "$command"
}

if ! cmp -s "$MANIFEST" "$FETCHED"; then
    cp "$MANIFEST" "$WS/config/west.yml"
    run_in_image bridge "set -e; [ -d .west ] || west init -l config; \
        west update --fetch-opt=--filter=tree:0"
    cp "$MANIFEST" "$FETCHED"
fi

echo "building worxpad//zmk; log in ${LOG#"$REPO"/}"
if ! run_in_image none "west zephyr-export >/dev/null && west build -p -s zmk/app -d /w/$BUILD_REL \
        -b worxpad//zmk -S studio-rpc-usb-uart -- -DZMK_EXTRA_MODULES=/w -DCONFIG_ZMK_STUDIO=y" \
        >"$LOG" 2>&1; then
    tail -n 60 "$LOG" >&2
    echo "firmware build failed; full log in ${LOG#"$REPO"/}" >&2
    exit 1
fi

# The Adafruit nRF52 bootloader takes only UF2 family 0xADA52840 with the application at 0x26000.
python3 - "$REPO/$BUILD_REL/zephyr/zmk.uf2" <<'PY'
import struct, sys
data = open(sys.argv[1], "rb").read()
_, _, flags, address, _, _, _, family = struct.unpack("<8I", data[:32])
if not flags & 0x2000 or family != 0xADA52840 or address != 0x26000:
    sys.exit(f"UF2 family {family:#x} at {address:#x}: not 0xada52840 at 0x26000")
PY
# Options the worxpad code relies on. src/display_power.c needs ZMK's blank-on-idle to stop the LVGL tick.
for option in CONFIG_WORXPAD_STATUS_SCREEN=y CONFIG_WORXPAD_DISPLAY_POWER=y CONFIG_ZMK_DISPLAY_BLANK_ON_IDLE=y; do
    if ! grep -qx "$option" "$REPO/$BUILD_REL/zephyr/.config"; then
        echo "$option is not in the build configuration" >&2
        exit 1
    fi
done
cp "$REPO/$BUILD_REL/zephyr/zmk.uf2" "$REPO/firmware/dist/worxpad.uf2"
grep -E '^\s+(FLASH|RAM):' "$LOG"
echo "wrote firmware/dist/worxpad.uf2"
