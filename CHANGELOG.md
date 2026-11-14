# Changelog

This project will use [Semantic Versioning](https://semver.org/). Hardware releases will be tagged with the board
revision, `v<version>-rev<X>`, as in the sibling repositories. Nothing has been released, ordered or built.

## [Unreleased]

The first design pass. Nothing in it has been fabricated, printed or run on hardware.

### Added

- Research: seven decision records in `research/components/`, the parts summary `research/COMPONENTS.md` and
  the GLYF dossier `research/DOSSIER.md`.
- `board.toml`, the single source of truth, and `tools/check_spec.py` with 91 checks. Design decisions D1 to
  D37 in [docs/decisions.md](docs/decisions.md), including the fixes from one specification review.
- PCB generator in `pcb/gen/` for KiCad 10.0.7 by digest: circuit (107 parts, 74 nets), six project
  footprints, a generated schematic with ERC at 0 errors and 0 warnings, placement of every part on four
  layers, a router, DRC with schematic parity, an RF keep-out copper check, the D23 frame panel and the JLCPCB
  and PCBWay order files. The board is routed (see Changed) and its order files are written.
- `tools/check_pins.py` and `tools/check_pins_firmware.py`: the pin map against the circuit and the firmware.
- Case package `cad/worxpad_case` (build123d 0.13.0): CNC and FDM shells, RF insert, knobs, button caps,
  keycap, lens, switch insertion jig, coupons, exports, drawings and checks. The G1 and G2 thread checks pass
  only with a proposed bottoming tap (D6).
- ZMK firmware in `firmware/zmk` with `firmware/build.sh`: four layers, four Bluetooth profiles, ZMK Studio,
  own status screen and a display power hook.
- Renders: `tools/render_all.sh` and `tools/render/` write the stills and the turntable in
  `docs/images/renders/`.
- Order tooling: `tools/order_package.py`, `production/README.md`, the JLCCNC and PCBWay order notes, and the
  guides [docs/ordering.md](docs/ordering.md), [docs/ordering-pcbway.md](docs/ordering-pcbway.md),
  [docs/ordering-case.md](docs/ordering-case.md), [docs/parts.md](docs/parts.md),
  [docs/assembly.md](docs/assembly.md), [docs/printing.md](docs/printing.md),
  [docs/flashing.md](docs/flashing.md) and [docs/keymap.md](docs/keymap.md).
- [README.md](README.md) with the status table, gallery, build steps and the list of open points before an
  order.

### Changed

- D39 replaces steps 7 to 10 of the D28 build order. The cell is bonded to the pocket floor with 0.2 mm
  double-sided foam tape (power 14 rule 1), and the RF insert sits in the open bottom shell until the top shell
  closes it (enclosure 7.2). The top assembly is lowered deck up onto the bottom shell. Before, the bottom shell
  was turned over onto the top assembly, and the insert, the foam and the cell had nothing to hold them.
  [docs/assembly.md](docs/assembly.md), [docs/bom-hand.csv](docs/bom-hand.csv) and [docs/parts.md](docs/parts.md)
  follow it. The insulating sheet is now self-adhesive.
- D40 records that the bottom shell needs a third CNC setup for the foot pockets, which are square to the ramp.
  [docs/ordering-case.md](docs/ordering-case.md) said two setups per shell.
- [docs/assembly.md](docs/assembly.md) step 5 gives the expected report for every control on the Edit layer. The
  buttons send no key code, so they are tested by the layer they select.
- The decision index lists D38 to D40.
- The PCB is routed: `make pcb-place` reports 0 unrouted pads (36 on 25 nets before) and `make pcb-check` 0
  violations, 0 unconnected items and 0 parity issues; 1,980 tracks, 280 vias. The router changed, the
  placement did not. Module pads escape to vias (deep pads under the module's middle), the flash and backlight
  FET pins escape to vias, signals may hop on both inner layers (never the supply nets, never under the USB pair
  or the crystal), a 3.3 V via cut off from its plane is moved, the USB D- gets a meander to match D+ within
  2 mm, ripped-up nets keep their escapes, junctions are cut into track ends, and J2's and J3's solder tabs are
  joined. The diagnosis of the old failures is in [pcb/README.md](pcb/README.md#routing). Nothing was built.
- `make pcb-fab` wrote pcb/fab and pcb/production from the routed board: 61 placements in 30 BOM lines, panel
  DRC 0 errors, board STEP 1.616 mm. `tools/order_package.py` exits 0 with 34 files and 0 problems.
- Knob and RF insert drawings (SVG, PDF, DXF) and `knob_holes.csv`, generated from the model by
  `cad/worxpad_case/small_drawings.py` and copied into the JLCCNC package.
