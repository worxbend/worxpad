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
  and PCBWay order files. The board is not fully routed: 36 pads on 25 nets remain.
- `tools/check_pins.py` and `tools/check_pins_firmware.py`: the pin map against the circuit and the firmware.
- Case package `cad/worxpad_case` (build123d 0.13.0): CNC and FDM shells, RF insert, knobs, button caps,
  keycap, lens, switch insertion jig, coupons, exports, drawings and checks. Two checks fail: the G1 and G2
  thread margin (D6).
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
