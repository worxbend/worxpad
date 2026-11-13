"""Where everything sits on the schematic sheet. Data only; schematic.py draws it.

Units are grid steps of 1.27 mm. Inside a block, positions count from the block's top-left corner,
X to the right and Y down. A point is either a pin ("R7.1") or a position (x, y).

What is not listed here is drawn by rule (see schematic.py): a pin on a supply-symbol net gets a short
wire and the supply symbol, a pin on any other net gets a short wire and the net's label, an open pin
gets a no-connect mark.
"""

from __future__ import annotations

from dataclasses import dataclass

import circuit
from circuit import BOARD_SPEC, GND, VBUS, VBUS_SYS


@dataclass(frozen=True)
class Place:
    ref: str
    x: int
    y: int
    rotation: int = 0  # degrees counter-clockwise


@dataclass(frozen=True)
class Wire:
    """A chain of straight wires through the points. Every pin on it must be on this net in circuit.py."""
    net: str
    points: tuple
    label: tuple | None = None  # (x, y) on the wire, text to the right; (x, y, "left") for text to the left


@dataclass(frozen=True)
class Rail:
    """A supply symbol at this point."""
    net: str
    point: tuple[int, int]


@dataclass(frozen=True)
class Flag:
    """KiCad's PWR_FLAG: tells the rule check that this net is driven from outside the sheet's symbols
    (through the fuse, or from the USB plug)."""
    point: tuple[int, int]


@dataclass(frozen=True)
class Note:
    text: str
    x: int
    y: int


@dataclass(frozen=True)
class Block:
    title: str
    x: int
    y: int
    width: int
    height: int
    places: tuple[Place, ...]
    wires: tuple[Wire, ...] = ()
    rails: tuple[Rail, ...] = ()
    flags: tuple[Flag, ...] = ()
    notes: tuple[Note, ...] = ()


PAPER = "A2"
SHEET_WIDTH, SHEET_HEIGHT = 467, 330  # A2 landscape in grid steps


def _row(refs: list[str], x: int, y: int, pitch: int = 8) -> tuple[Place, ...]:
    return tuple(Place(ref, x + pitch * n, y) for n, ref in enumerate(refs))


# --- radio module ------------------------------------------------------------------------------------------

_U1 = (62, 54)
_U1_BOTTOM = _U1[1] + 37   # bottom pin row of the module symbol
_GROUND_PADS = sorted(BOARD_SPEC["module"]["pads"]["GND"])
_MODULE = Block(
    "Radio module: u-blox BMD-340 (nRF52840), LV mode", 4, 6, 124, 110,
    places=(Place("U1", *_U1),),
    wires=(
        # The 13 ground pads along the bottom edge of the symbol, then down to one ground symbol.
        Wire(GND, tuple(f"U1.{pad}" for pad in _GROUND_PADS)),
        Wire(GND, (f"U1.{_GROUND_PADS[len(_GROUND_PADS) // 2]}", (_U1[0], _U1_BOTTOM + 4),
                   (_U1[0] + 8, _U1_BOTTOM + 4))),
    ),
    rails=(Rail(GND, (_U1[0], _U1_BOTTOM + 4)),),
    flags=(Flag((_U1[0] + 8, _U1_BOTTOM + 4)),),
    notes=(Note("VCC and VCCH tied to 3V3 (LV mode). Spare GPIOs open.", 2, 104),
           Note("D12: VBUS on pad 66 with 3V3 off is not yet checked against the nRF52840 specification.", 2, 107)),
)

_CRYSTAL = Block(
    "32.768 kHz crystal, module bulk", 132, 6, 60, 36,
    places=(Place("Y1", 24, 14), Place("C1", 16, 21), Place("C2", 34, 21), Place("C3", 52, 21)),
    wires=(
        Wire("XL1", ("Y1.1", (16, 14), "C1.1")),
        Wire("XL1", ((16, 14), (10, 14)), label=(10, 14, "left")),
        Wire("XL2", ("Y1.2", (34, 14), "C2.1")),
        Wire("XL2", ((34, 14), (40, 14)), label=(40, 14)),
    ),
    notes=(Note("C3: 10 uF bulk at VCC/VCCH (D14).", 2, 34),),
)

_FLASH = Block(
    "Icon flash: 16 MB QSPI NOR", 196, 6, 64, 40,
    places=(Place("U2", 36, 22), Place("C4", 54, 22)),
)

# --- display -----------------------------------------------------------------------------------------------

_J2 = (100, 36)
_J2_GROUND_BUS = (13, 14, 15, 16, 17, 18, 19, 20, 23, 24)


def _fpc_pin_y(pin: int) -> int:
    return _J2[1] - 22 + 2 * (pin - 1)


_BUS_X = 90
_DISPLAY = Block(
    "Display: FH34SRJ-24S connector, backlight switch", 264, 6, 120, 72,
    places=(Place("J2", *_J2), Place("R1", 10, 22), Place("Q1", 34, 22), Place("R2", 20, 42),
            Place("C5", 34, 42), Place("C6", 44, 42)),
    wires=(
        *(Wire(GND, (f"J2.{pin}", (_BUS_X, _fpc_pin_y(pin)))) for pin in _J2_GROUND_BUS),
        Wire(GND, ((_BUS_X, _fpc_pin_y(13)), (_BUS_X, _fpc_pin_y(20)), (_BUS_X, _fpc_pin_y(23)),
                   (_BUS_X, _fpc_pin_y(24)))),
        Wire(GND, ("J2.3", (80, _fpc_pin_y(3)))),
        Wire(GND, ("J2.11", (80, _fpc_pin_y(11)))),
        Wire("LCD_TE", ("J2.21", (_BUS_X - 4, _fpc_pin_y(21))), label=(_BUS_X - 4, _fpc_pin_y(21), "left")),
    ),
    rails=(Rail(GND, (_BUS_X, _fpc_pin_y(24))), Rail(GND, (80, _fpc_pin_y(3))), Rail(GND, (80, _fpc_pin_y(11)))),
    notes=(Note("Panel DM-TFT13-377p24, 4-line SPI (IM1/2 high). Pins 13 to 20 (DB0 to DB7) and RD to GND.", 2, 64),
           Note("Q1 gate pulled low by R2: backlight off while P0.24 floats.", 2, 67)),
)

# --- USB-C -------------------------------------------------------------------------------------------------

_USB = Block(
    "USB-C: CC pull-downs, ESD array, PTC", 4, 118, 104, 56,
    places=(Place("J1", 16, 28), Place("F1", 66, 12, 90), Place("U6", 66, 34), Place("R3", 88, 34),
            Place("R4", 96, 34)),
    wires=(
        Wire(VBUS, ((44, 12), (53, 12), "F1.1")),
        Wire(VBUS_SYS, ("F1.2", (80, 12), (88, 12)), label=(88, 12)),
    ),
    rails=(Rail(VBUS, (44, 12)),),
    flags=(Flag((53, 12)), Flag((80, 12))),
    notes=(Note("USB 2.0 device. SBU open. Shell to GND.", 2, 54),),
)

# --- power -------------------------------------------------------------------------------------------------

_CHARGER = Block(
    "Charger with power path: BQ24072, USB500, 405 mA", 112, 118, 92, 82,
    places=(Place("U3", 44, 30), *_row(["C7", "C8", "C9", "R5"], 8, 60), *_row(["R6", "R7", "TH1"], 58, 60)),
    wires=(
        Wire(GND, ("U3.15", (30, 22), (30, 26), "U3.4")),
        Wire(GND, ((30, 24), (26, 24))),
        Wire(GND, ("U3.5", (22, 32))),
    ),
    rails=(Rail(GND, (26, 24)), Rail(GND, (22, 32))),
    notes=(Note("ISET 2.2k: 362 / 405 / 443 mA. TMR open: 30 min / 5 h timers.", 2, 78),),
)

_BATTERY = Block(
    "Cell connector, reverse-polarity FET", 208, 118, 64, 34,
    places=(Place("J3", 22, 14), Place("Q2", 54, 16)),
    notes=(Note("J3 pin 1 positive. Check each cell with a meter.", 2, 32),),
)

_LDO = Block(
    "3.3 V regulator, power switch on EN", 276, 118, 80, 44,
    places=(Place("U4", 24, 14), Place("SW18", 24, 32), Place("C10", 52, 16), Place("C11", 62, 16)),
    notes=(Note("D14: 1 uF at the LDO output.", 2, 42),),
)

_GAUGE = Block(
    "Fuel gauge: MAX17048, I2C 0x36", 360, 118, 84, 44,
    places=(Place("U5", 30, 20), Place("C12", 58, 20), Place("R8", 66, 20), Place("R9", 74, 20)),
    wires=(
        Wire(GND, ("U5.6", (18, 20), (18, 22), "U5.1")),
        Wire(GND, ("U5.4", "U5.9")),
    ),
    rails=(Rail(GND, (18, 22)), Rail(GND, (30, 27))),
)

_DEBUG = Block(
    "Reset button, SWD (Tag-Connect TC2030-NL)", 132, 50, 76, 40,
    places=(Place("SW17", 14, 16), Place("J4", 50, 20)),
    wires=(Wire(GND, ("SW17.2", (26, 16))),),
    rails=(Rail(GND, (26, 16)),),
    notes=(Note("Pin reset on P0.18: program PSELRESET once over SWD.", 2, 38),),
)

# --- inputs ------------------------------------------------------------------------------------------------

_KEY_PITCH = 22


def _key_cell(row: int, column: int) -> tuple[list[Place], list[Wire]]:
    index = row * BOARD_SPEC["keys"]["columns"] + column + 1
    x, y = 16 + _KEY_PITCH * column, 12 + _KEY_PITCH * row
    places = [Place(f"SW{index}", x, y), Place(f"D{index}", x + 4, y + 7, 90)]
    return places, [Wire(f"K{row}{column}", (f"SW{index}.2", f"D{index}.2"), label=(x + 4, y + 2))]


def _keys() -> Block:
    places, wires = [], []
    keys = BOARD_SPEC["keys"]
    for row in range(keys["rows"]):
        for column in range(keys["columns"]):
            cell_places, cell_wires = _key_cell(row, column)
            places += cell_places
            wires += cell_wires
    return Block("Key matrix: 16 Choc V2 hot-swap sockets, col2row", 4, 206, 96, 104, tuple(places), tuple(wires),
                 notes=(Note("Column -> switch -> diode -> row. Rows pulled down inside the module.", 2, 102),))


def _encoder(ref: str, diode: str, x: int, y: int) -> tuple[list[Place], list[Wire], list[Rail]]:
    places = [Place(ref, x, y), Place(diode, x + 6, y + 7, 90)]
    wires = [Wire(f"K{_C4_ROW[ref]}4", (f"{ref}.S2", f"{diode}.2"), label=(x + 6, y + 3)),
             Wire(GND, (f"{ref}.C", (x - 20, y), (x - 20, y + 6)))]
    return places, wires, [Rail(GND, (x - 20, y + 6))]


def _button(ref: str, diode: str, x: int, y: int) -> tuple[list[Place], list[Wire]]:
    return ([Place(ref, x, y), Place(diode, x + 4, y + 7, 90)],
            [Wire(f"K{_C4_ROW[ref]}4", (f"{ref}.2", f"{diode}.2"), label=(x + 4, y + 2))])


_C4_ROW = {"ENC1": 0, "ENC2": 1, "SW19": 2, "SW20": 3}


def _column_four() -> Block:
    places, wires, rails = [], [], []
    for ref, diode, x in (("ENC1", "D17", 28), ("ENC2", "D18", 88)):
        p, w, r = _encoder(ref, diode, x, 18)
        places, wires, rails = places + p, wires + w, rails + r
    places += [Place("C13", 46, 20), Place("C14", 54, 20), Place("C15", 106, 20), Place("C16", 114, 20)]
    for ref, diode, x in (("SW19", "D19", 28), ("SW20", "D20", 88)):
        p, w = _button(ref, diode, x, 50)
        places, wires = places + p, wires + w
    return Block("Encoders and round buttons: matrix column 4", 104, 206, 124, 72, tuple(places), tuple(wires),
                 tuple(rails), notes=(Note("C13 to C16: footprints only, not fitted (D36).", 2, 70),))


# --- test points and mechanical parts ----------------------------------------------------------------------

_TEST_POINTS = Block(
    "Test pads (bottom face)", 232, 206, 106, 26,
    places=_row([f"TP{n}" for n in range(1, len(circuit.TEST_POINT_NETS) + 1)], 6, 10, 9),
)

_MECHANICAL_REFS = [f"H{n}" for n in range(1, 9)] + [f"FID{n}" for n in range(1, 7)]
_MECHANICAL = Block(
    "Holes: K1-K4 H1-H4, C1-C2 H5-H6, G1-G2 H7-H8 (plated, GND). Fiducials", 232, 236, 120, 24,
    places=_row(_MECHANICAL_REFS, 6, 10, 8),
)

BLOCKS = (_MODULE, _CRYSTAL, _FLASH, _DISPLAY, _DEBUG, _USB, _CHARGER, _BATTERY, _LDO, _GAUGE, _keys(),
          _column_four(), _TEST_POINTS, _MECHANICAL)

