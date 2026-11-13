#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Run first in every KiCad container: seed the stock library tables in $HOME (empty, HOME=/tmp) and add
# the project's `worxpad` libraries, resolved relative to each project directory.
# Adapted from worxboard/tools/kicad_env.sh.
set -euo pipefail

KICAD_VER="${KICAD_VER:-10.0}"
TEMPLATES=/usr/share/kicad/template
CFG="$HOME/.config/kicad/$KICAD_VER"
LIB='${KIPRJMOD}/../lib'

mkdir -p "$CFG"
cp "$TEMPLATES"/*-lib-table "$CFG"/

add_lib() {  # add_lib <table> <entry>
    local table="$CFG/$1" entry="$2"
    grep -q '(name "worxpad")' "$table" && return 0
    sed -i '$ d' "$table"                      # drop the closing paren
    printf '  %s\n)\n' "$entry" >> "$table"
}
add_lib fp-lib-table  "(lib (name \"worxpad\")(type \"KiCad\")(uri \"$LIB/worxpad.pretty\")(options \"\")(descr \"worxpad\"))"
add_lib sym-lib-table "(lib (name \"worxpad\")(type \"KiCad\")(uri \"$LIB/worxpad.kicad_sym\")(options \"\")(descr \"worxpad\"))"
