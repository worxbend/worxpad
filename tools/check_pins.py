#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Fail when the circuit disagrees with the pin map in board.toml. Standard library only.

board.toml is the source of truth for which module pad carries which signal. pcb/gen/circuit.py builds the
netlist from it, so this check reads the netlist back and compares it with board.toml from the other side:

- every [pinmap] pin sits on the module pad [module.pads] gives it and carries its net;
- every spare pin is open, and pinmap plus spares cover all 48 GPIOs exactly once;
- no "fast" signal sits on a low-frequency pin;
- matrix rows and columns, encoder A/B pins and the C4 assignments reach the parts board.toml names;
- each FPC connector pin carries the net of [display.fpc_pins].

Then it runs the firmware half, tools/check_pins_firmware.py: the ZMK board files against board.toml.
Adapted from macropad/tools/check_pins.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "pcb" / "gen"))

import circuit  # noqa: E402  (needs the path above)
import check_pins_firmware  # noqa: E402  (tools/, next to this file)

MODULE_REF = "U1"
FPC_REF = "J2"
C4_SWITCH = {"encoder_right_push": "ENC1", "encoder_left_push": "ENC2", "button_right": "SW19", "button_left": "SW20"}


def _pads(entry) -> list[str]:
    return [str(pad) for pad in (entry if isinstance(entry, list) else [entry])]


def check_module(board: dict, parts: dict[str, circuit.Part], errors: list[str]) -> None:
    pads, pinmap = board["module"]["pads"], board["pinmap"]
    spare = board["pinmap_spare"]["pins"]
    module = parts[MODULE_REF].nets
    for pin, (net, _function, speed) in pinmap.items():
        if pin not in pads:
            errors.append(f"pinmap {pin}: no such module pin in [module.pads]")
            continue
        for pad in _pads(pads[pin]):
            if module.get(pad) != net:
                carried = module.get(pad) or "nothing"
                errors.append(f"pinmap {pin} = {net}, but {MODULE_REF} pad {pad} carries {carried}")
        if speed == "fast" and pin in board["module"]["low_frequency"]["pins"]:
            errors.append(f"pinmap {pin} carries fast signal {net} on a low-frequency pin")
    for pin in spare:
        for pad in _pads(pads[pin]):
            if module.get(pad, circuit.NO_NET) != circuit.NO_NET:
                errors.append(f"spare {pin}: {MODULE_REF} pad {pad} carries {module[pad]}")
    gpios = sorted(name for name in pads if name.startswith("P"))
    claimed = sorted([name for name in pinmap if name.startswith("P")] + list(spare))
    if claimed != gpios:
        twice = sorted({name for name in claimed if claimed.count(name) > 1})
        missing = sorted(set(gpios) - set(claimed))
        errors.append(f"GPIOs not covered exactly once by pinmap and spares: twice {twice}, missing {missing}")


def _net_of_pin(board: dict, pin: str) -> str:
    return board["pinmap"][pin][0]


def check_matrix(board: dict, parts: dict[str, circuit.Part], errors: list[str]) -> None:
    matrix = board["matrix"]
    for row, pin in enumerate(matrix["rows"]):
        if _net_of_pin(board, pin) != circuit.row_net(row):
            errors.append(f"matrix row {row} on {pin} carries {_net_of_pin(board, pin)}, "
                          f"circuit wants {circuit.row_net(row)}")
    for column, pin in enumerate(matrix["columns"]):
        if _net_of_pin(board, pin) != circuit.column_net(column):
            errors.append(f"matrix column {column} on {pin} carries {_net_of_pin(board, pin)}")
    nets = circuit.nets_to_pads(list(parts.values()))
    column = len(matrix["columns"]) - 1
    for row, name in enumerate(matrix["c4"]):
        ref = C4_SWITCH[name]
        node = nets.get(f"K{row}{column}", [])
        on_column = {pad.split(".")[0] for pad in nets[circuit.column_net(column)]}
        if not any(pad.startswith(f"{ref}.") for pad in node) or ref not in on_column:
            errors.append(f"matrix C4 R{row} ({name}) does not reach {ref}")
    for side in ("left", "right"):
        if board["encoders"][side]["matrix"] != f"C{column}R{matrix['c4'].index(f'encoder_{side}_push')}":
            errors.append(f"encoders.{side}.matrix disagrees with matrix.c4")
    for side in ("left", "right"):
        if board["buttons"][side]["matrix"] != f"C{column}R{matrix['c4'].index(f'button_{side}')}":
            errors.append(f"buttons.{side}.matrix disagrees with matrix.c4")


def check_encoders(board: dict, parts: dict[str, circuit.Part], errors: list[str]) -> None:
    for side, ref in (("right", "ENC1"), ("left", "ENC2")):
        encoder = board["encoders"][side]
        for channel in ("a", "b"):
            wanted = _net_of_pin(board, encoder[f"gpio_{channel}"])
            got = parts[ref].nets.get(channel.upper())
            if got != wanted:
                errors.append(f"encoders.{side}.gpio_{channel} carries {wanted}, {ref}.{channel.upper()} is on {got}")


def check_display(board: dict, parts: dict[str, circuit.Part], errors: list[str]) -> None:
    connector = parts[FPC_REF].nets
    for pin, net in board["display"]["fpc_pins"].items():
        wanted = circuit.NO_NET if net == "NC" else net
        if connector.get(str(pin), circuit.NO_NET) != wanted:
            carried = connector.get(str(pin)) or "nothing"
            errors.append(f"display.fpc_pins {pin} = {net}, {FPC_REF}.{pin} is on {carried}")
    module_nets = set(parts[MODULE_REF].nets.values())
    for net in set(board["display"]["fpc_pins"].values()) - {"NC", "GND", "3V3", "BL_A", "BL_K", "LCD_TE"}:
        if net not in module_nets:
            errors.append(f"display signal {net} reaches no module pad")


def main() -> int:
    board = circuit.BOARD_SPEC
    parts = {part.ref: part for part in circuit.all_parts()}
    errors: list[str] = []
    for check in (check_module, check_matrix, check_encoders, check_display):
        check(board, parts, errors)
    for error in errors:
        print(f"FAIL {error}")
    pins = len(board["pinmap"])
    print(f"check_pins: {pins} pinmap entries, {len(board['pinmap_spare']['pins'])} spares, "
          f"{len(board['display']['fpc_pins'])} FPC pins against circuit.py: {len(errors)} failures")
    firmware_failures = check_pins_firmware.run(board)
    return 1 if errors or firmware_failures else 0


if __name__ == "__main__":
    sys.exit(main())
