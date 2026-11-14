# CLAUDE.md

Guidance for Claude Code in this repository.

## Git commits and pull requests

Do not add Claude or AI attribution to commits or PRs. No `Co-Authored-By` trailer, no "Generated with" line.

## What this is

worxpad: an open-hardware wireless macropad with the function set of the Prota Designs GLYF. 16 Choc V2 keys
(4 x 4), two rotary encoders with push, two round buttons, a 1.3 inch 240 x 240 colour display, USB-C,
Bluetooth to several hosts (nRF52840 in a u-blox BMD-340 module), a 1,200 mAh LiPo, and a two-shell CNC
aluminium case. Targets: PCBA at JLCPCB (PCBWay fallback), case at JLCCNC (PCBWay fallback), FDM PETG prototype
on a Bambu A1 mini. First batch: 5 units.

The GLYF is a reference only. Never copy its name, logo, artwork, firmware, software or files. Facts and
measurements live in `research/` and `docs/reference-device.md`.

Nothing has been fabricated, printed or run on hardware. Every document must say so where it matters.

- `board.toml` is the single source of truth for positions, the stack-up, the pin map and the matrix.
  PCB, case and firmware read it; `tools/check_spec.py` checks its arithmetic.
- `docs/decisions.md` records every design decision (D1 to D40) with context, options, reason and owner.
- `research/` is the finished research: decision records per subsystem in `research/components/`, the
  summary in `research/COMPONENTS.md`, the GLYF dossier in `research/DOSSIER.md`. Read it; do not edit it.
- Builders: the PCB generator in `pcb/gen/` (entry point `pcb/gen/build.py`, run in KiCad through
  `pcb/kicad.sh`), the build123d case in `cad/` (`cad/build.py`), the ZMK firmware (`firmware/build.sh`),
  the renders (`tools/render_all.sh`) and the order index (`tools/order_package.py`).
- State on 2026-11-14: the PCB is routed (0 unrouted pads, DRC 0 violations, 0 unconnected, 0 parity) and
  pcb/fab and pcb/production are written; `tools/order_package.py` exits 0. The case checks pass, G1 and G2
  only with a bottoming tap D6 does not yet record. The firmware builds. The renders predate routing. The status
  table in `README.md` holds the numbers.

## Commands

```bash
make help        # list every target
make test        # spec-check, docs-check, pin-check; everything checkable without Docker or hardware
make spec-check  # tools/check_spec.py on board.toml
make docs-check  # every file, picture and anchor named in a Markdown file exists
make pin-check   # tools/check_pins.py: pin map against circuit.py and the firmware
make pcb-test    # circuit self-check and generator unit tests, no Docker (not yet part of `make test`)
make pcb         # place, route, DRC, order files (Docker, kicad/kicad:10.0.7); fab refuses an unfinished board
make cad         # case checks, exports, drawings, quick pictures (cad/.venv, about 7 min)
make cad-check   # case checks only
make firmware    # ZMK build in zmkfirmware/zmk-build-arm by digest -> firmware/dist/worxpad.uf2
make renders     # tools/render_all.sh -> docs/images/renders/ (Blender and FreeCAD flatpaks, about 15 min)
make order       # tools/order_package.py; exits 1 on any missing or disagreeing order file
pcb/kicad.sh python3 pcb/gen/build.py place      # the same PCB steps, image pinned by digest
bash tools/pull_images.sh kicad/kicad:10.0.7     # pull a pinned image by digest and tag it
```

Containers run with `--network none` unless a step must fetch. Images are pinned by digest in
`tools/images.lock`; `tools/kicad_env.sh` runs first in every KiCad container. The case venv is cad/.venv,
made with uv on Python 3.12, build123d pinned to 0.13.0 as in the siblings.

## Rules of the road

- Change a position, a level or a pin in `board.toml` first, run `make spec-check`, then rebuild PCB, case and
  firmware. Never put a number in a generator that belongs in `board.toml`.
- Every number in `board.toml` traces to a research record or a decision entry. A new decision gets a new
  entry in `docs/decisions.md`; do not rewrite an old one silently.
- Keep `MEASURE` tags until someone measures. Label every guess as a guess.
- Never remove or weaken a check or a test to get green. Add a check for what you add.
- Never write that a check passed unless you ran it. Status numbers in `README.md` are copied from check output
  and updated in the same change. Add a new entry to `CHANGELOG.md` under Unreleased.
- Generated files are produced by code in this repository and never hand-edited. Hand edits are lost on the next
  build. Change the generator. Generated trees and files:

  ```
  pcb/kicad/  pcb/fab/  pcb/production/  pcb/lib/3d/  pcb/lib/worxpad.pretty/  pcb/lib/worxpad.kicad_sym
  pcb/netlist.txt  pcb/routing.txt  cad/exports/  docs/images/  firmware/dist/  production/
  cad/production/jlccnc/worxpad_*  cad/production/jlccnc/hole_table.csv
  ```

  Hand-written despite the location: `cad/production/README.md`, `cad/production/hardware.csv` and both
  `ORDER_NOTES.md` files under `cad/production/`. `pcb/lib/SOURCES.txt` and `pcb/gen/route_order.txt` are
  hand-written too.
- Build scratch, ignored by git through `.build/`: `pcb/.build/` (DRC reports, drafts), `firmware/.build/`
  (the west workspace, about 3 GB), `tools/render/.build/`.
- Plain technical English, full sentences, short. No emoji, no marketing. British spelling as in the siblings.
- Run `make docs-check` after moving or renaming a file. Name a path in a code span only when it exists.
