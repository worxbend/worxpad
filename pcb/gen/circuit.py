"""The worxpad circuit: every part, its JLCPCB part number, its face, its board.toml position and its nets.

Pure Python, no KiCad import, so the netlist can be checked anywhere. `python3 circuit.py` prints it.

Positions are top-view board coordinates in millimetres (board.toml frame). A part's x and y are the
position board.toml gives for it (the reference point named in its comment there); `None` means board.toml
holds no position and the layout places the part. layout.py maps these points to footprint origins.
Rotation is left to the layout. The face is a circuit decision (D9): the FPC connector, the two B3FS
buttons and the two encoders on the top face, everything else on the bottom.

Sources: the decision records in research/components/ and docs/decisions.md. Each block names its source.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BOARD_SPEC = tomllib.loads((REPO_ROOT / "board.toml").read_text())

TOP = "top"
BOTTOM = "bottom"
NO_NET = ""

# Rail and signal net names. Names that board.toml uses are taken from it unchanged.
GND = "GND"
VBUS = "VBUS"          # USB-C VBUS pins, before the PTC
VBUS_SYS = "VBUS_SYS"  # after the PTC: charger IN and module pad 66 (board.toml pinmap)
VSYS = "VSYS"          # charger OUT: LDO input
BAT = "BAT"            # cell after the reverse-polarity FET
BAT_IN = "BAT_IN"      # battery connector pin 1, before the FET
V3 = "3V3"             # LDO output (board.toml pinmap and display.fpc_pins)
LIBRARY = "worxpad"

# JLCPCB part numbers from the decision records (read there on 2026-11-13; stock moves daily).
LCSC = {
    "BMD-340-A-R": "C5456944",            # mcu-radio 7.1
    "W25Q128JVSIQ": "C97521",             # mcu-radio 7.4
    "Q13FC1350000400": "C32346",          # mcu-radio 7.4, 32.768 kHz
    "20pF": "C1554",                      # mcu-radio 7.4, C0G 0402
    "10uF": "C19702",                     # 0603, mcu-radio 7.4 and power 13
    "100nF": "C1525",                     # 0402
    "1uF": "C52923",                      # 0402, display 8
    "1uF 50V": "C15849",                  # 0603, power 13 (charger IN, LDO IN and OUT, D14)
    "15R 1%": "C25083",                   # display 8
    "100k": "C25741",                     # display 8, power 13
    "5.1k 1%": "C25905",                  # usb-io 6.3
    "3.3k": "C25890",                     # power 13
    "2.2k 1%": "C25879",                  # power 13
    "4.7k": "C25900",                     # power 13, D15
    "NTC 10k B3950": "C51597",            # power 13
    "AO3400A": "C20917",                  # display 8
    "AO3401A": "C15127",                  # power 9
    "BQ24072RGTR": "C140288",             # power 13
    "TPS7A0233PDBVR": "C2887324",         # power 13, D13
    "MAX17048G+T10": "C2682616",          # power 13
    "USBLC6-2SC6": "C7519",               # usb-io 4.2
    "1206L075THYR": "C99563",             # usb-io 4.3
    "TYPE-C-31-M-13C": "C2848620",        # usb-io 6.1
    "FH34SRJ-24S-0.5SH(50)": "C324726",   # display 8
    "S2B-PH-SM4-TB": "C295747",           # power 11
    "MSK12C02": "C431540",                # power 8
    "TS-1187A-B-A-B": "C318884",          # usb-io 4.6
    "B3FS-1000P": "C271750",              # rotary-buttons 5
    "PEC12R-4215F-S0024": "C22385080",    # rotary-buttons 6.1
    "1N4148W": "C81598",                  # keys 6.7
    "CPG135001S30": "C5333465",           # keys 6.7: zero stock, discontinued; bought from a keyboard shop
}

_P = LIBRARY + ":"
FOOTPRINT = {
    "C0402": "Capacitor_SMD:C_0402_1005Metric",
    "C0603": "Capacitor_SMD:C_0603_1608Metric",
    "R0402": "Resistor_SMD:R_0402_1005Metric",
    "R0805": "Resistor_SMD:R_0805_2012Metric",
    "SOT23": "Package_TO_SOT_SMD:SOT-23",
    "SOT23-5": "Package_TO_SOT_SMD:SOT-23-5",
    "SOT23-6": "Package_TO_SOT_SMD:SOT-23-6",
    "SOIC8W": "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm",
    "VQFN16": "Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.6x1.6mm",
    "DFN8": "Package_DFN_QFN:DFN-8-1EP_2x2mm_P0.5mm_EP0.8x1.6mm",
    "XTAL3215": "Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm",
    "F1206": "Fuse:Fuse_1206_3216Metric",
    "SOD123": "Diode_SMD:D_SOD-123",
    "TACT": "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A",
    "B3FS": "Button_Switch_SMD:SW_SPST_Omron_B3FS-100xP",
    "SLIDE": "Button_Switch_SMD:SW_SPDT_Shouhan_MSK12C02",
    "JST_PH2": "Connector_JST:JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal",
    "TC2030": "Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical",
    "TESTPAD": "TestPoint:TestPoint_Pad_D1.0mm",
    "FIDUCIAL": "Fiducial:Fiducial_1mm_Mask2mm",
    "HOLE_NPTH4": "MountingHole:MountingHole_4mm",
    # Drawn for this project by footprints.py (pcb/lib/SOURCES.txt).
    "BMD340": _P + "BMD-340",
    "FH34SRJ24": _P + "FH34SRJ-24S-0.5SH",
    "USBC_M13C": _P + "USB_C_HRO_TYPE-C-31-M-13C",
    "CHOC_HOTSWAP": _P + "Choc_V2_Hotswap",
    "PEC12R4": _P + "PEC12R-4xxxF-S",
    "HOLE_G": _P + "Hole_G_M2_Plated",
}

HAND_SOLDERED = {"CHOC_HOTSWAP"}          # sockets are not purchasable at JLCPCB (keys 6.7)
NOT_A_PART = {"TESTPAD", "HOLE_NPTH4", "HOLE_G", "FIDUCIAL", "TC2030"}   # copper or holes only


@dataclass(frozen=True)
class Part:
    ref: str
    value: str
    footprint_key: str
    side: str = BOTTOM
    nets: dict[str, str] = field(default_factory=dict)
    x: float | None = None
    y: float | None = None
    fitted: bool = True       # False: footprint only, no BOM line (D36)

    @property
    def footprint(self) -> str:
        return FOOTPRINT[self.footprint_key]

    @property
    def lcsc(self) -> str:
        if self.footprint_key in NOT_A_PART or not self.fitted:
            return ""
        return LCSC[self.value]

    @property
    def machine_assembled(self) -> bool:
        return self.fitted and self.footprint_key not in HAND_SOLDERED | NOT_A_PART


def _two(a: str, b: str) -> dict[str, str]:
    return {"1": a, "2": b}


def _at(entry: dict) -> dict[str, float]:
    return {"x": entry["x"], "y": entry["y"]}


# --- radio module, crystal, flash (mcu-radio 7.1, 7.2, 7.4) -------------------------------------------------

def module_pad_nets() -> dict[str, str]:
    """BMD-340 pad number -> net, from board.toml [module.pads] and [pinmap]. Spare pins stay open."""
    pads, pinmap = BOARD_SPEC["module"]["pads"], BOARD_SPEC["pinmap"]
    nets: dict[str, str] = {}
    for pin, pad in pads.items():
        for number in pad if isinstance(pad, list) else [pad]:
            nets[str(number)] = pinmap[pin][0] if pin in pinmap else NO_NET
    return nets


def module_centre() -> tuple[float, float]:
    """Module body centre: antenna end `antenna_inset` inside the right board edge (D24)."""
    module = BOARD_SPEC["module"]
    return BOARD_SPEC["pcb"]["x1"] - module["antenna_inset"] - module["length"] / 2, module["centre_y"]


def _module() -> list[Part]:
    x, y = module_centre()
    flash = BOARD_SPEC["flash"]
    return [
        Part("U1", "BMD-340-A-R", "BMD340", nets=module_pad_nets(), x=x, y=y),
        # Module bulk at VCC/VCCH (D14: 10 uF, not more).
        Part("C3", "10uF", "C0603", nets=_two(V3, GND)),
        Part("Y1", "Q13FC1350000400", "XTAL3215", nets=_two("XL1", "XL2")),
        Part("C1", "20pF", "C0402", nets=_two("XL1", GND)),
        Part("C2", "20pF", "C0402", nets=_two("XL2", GND)),
        # W25Q128JVSIQ, KiCad pin order: 1 /CS, 2 IO1, 3 IO2, 4 GND, 5 IO0, 6 CLK, 7 IO3, 8 VCC.
        Part("U2", "W25Q128JVSIQ", "SOIC8W", x=flash["x"], y=flash["y"], nets={
            "1": "QSPI_CSN", "2": "QSPI_IO1", "3": "QSPI_IO2", "4": GND, "5": "QSPI_IO0", "6": "QSPI_SCK",
            "7": "QSPI_IO3", "8": V3}),
        Part("C4", "100nF", "C0402", nets=_two(V3, GND)),
    ]


# --- display connector and backlight (display 6.2) ----------------------------------------------------------

def _display() -> list[Part]:
    connector = BOARD_SPEC["display"]["connector"]
    pins = {str(pin): (NO_NET if net == "NC" else net) for pin, net in BOARD_SPEC["display"]["fpc_pins"].items()}
    pins["MP"] = NO_NET   # solder tabs, mechanical only
    return [
        Part("J2", "FH34SRJ-24S-0.5SH(50)", "FH34SRJ24", side=TOP, nets=pins,
             x=(connector["x0"] + connector["x1"]) / 2, y=connector["y_back"]),
        Part("R1", "15R 1%", "R0402", nets=_two(V3, "BL_A")),
        # Low-side switch, KiCad pin order 1 G, 2 S, 3 D. 100k holds the gate low while P0.24 floats.
        Part("Q1", "AO3400A", "SOT23", nets={"1": "BL_PWM", "2": GND, "3": "BL_K"}),
        Part("R2", "100k", "R0402", nets=_two("BL_PWM", GND)),
        Part("C5", "1uF", "C0402", nets=_two(V3, GND)),
        Part("C6", "100nF", "C0402", nets=_two(V3, GND)),
    ]


# --- USB-C, protection (usb-io 6.1, 6.3, 6.4) ----------------------------------------------------------------

def _usb() -> list[Part]:
    usb, parts = BOARD_SPEC["usb"], BOARD_SPEC["power"]["parts"]
    nets = {pad: GND for pad in ("A1", "A12", "B1", "B12", "SH")}   # shell slots to GND (usb-io 6.4)
    nets |= {pad: VBUS for pad in ("A4", "A9", "B4", "B9")}
    nets |= {"A5": "CC1", "B5": "CC2", "A6": "USB_DP", "B6": "USB_DP", "A7": "USB_DN", "B7": "USB_DN",
             "A8": NO_NET, "B8": NO_NET}
    return [
        Part("J1", "TYPE-C-31-M-13C", "USBC_M13C", nets=nets, x=usb["x"], y=usb["front_y"]),
        Part("R3", "5.1k 1%", "R0402", nets=_two("CC1", GND), **_at(parts["cc1"])),
        Part("R4", "5.1k 1%", "R0402", nets=_two("CC2", GND), **_at(parts["cc2"])),
        # USBLC6-2SC6 flow-through: 1/6 I/O1 = D-, 3/4 I/O2 = D+, 5 VBUS before the fuse, 2 GND.
        Part("U6", "USBLC6-2SC6", "SOT23-6", **_at(parts["esd"]), nets={
            "1": "USB_DN", "6": "USB_DN", "3": "USB_DP", "4": "USB_DP", "2": GND, "5": VBUS}),
        Part("F1", "1206L075THYR", "F1206", nets=_two(VBUS, VBUS_SYS), **_at(parts["ptc"])),
    ]


# --- power: charger, LDO, gauge, reverse FET, switch, cell connector (power 6 to 11, D13 to D15) ------------

def _power() -> list[Part]:
    parts = BOARD_SPEC["power"]["parts"]
    battery = BOARD_SPEC["battery"]["connector"]
    switch = BOARD_SPEC["power_switch"]
    return [
        # BQ24072RGT pins (power 6.3): USB500 (EN1 high from IN, EN2 low), CE low, TD low, TMR open.
        Part("U3", "BQ24072RGTR", "VQFN16", **_at(parts["charger"]), nets={
            "1": "CHG_TS", "2": BAT, "3": BAT, "4": GND, "5": GND, "6": "CHG_EN1", "7": "PGOOD_N", "8": GND,
            "9": "CHG_N", "10": VSYS, "11": VSYS, "12": "CHG_ILIM", "13": VBUS_SYS, "14": NO_NET, "15": GND,
            "16": "CHG_ISET", "17": GND}),
        Part("C7", "1uF 50V", "C0603", nets=_two(VBUS_SYS, GND)),
        Part("C8", "10uF", "C0603", nets=_two(VSYS, GND)),
        Part("C9", "10uF", "C0603", nets=_two(BAT, GND)),
        Part("R5", "100k", "R0402", nets=_two(VBUS_SYS, "CHG_EN1")),
        Part("R6", "3.3k", "R0402", nets=_two("CHG_ILIM", GND)),
        Part("R7", "2.2k 1%", "R0402", nets=_two("CHG_ISET", GND)),
        Part("TH1", "NTC 10k B3950", "R0805", nets=_two("CHG_TS", GND), **_at(parts["ntc"])),
        # P-FET in the positive line: drain to the connector, source to BAT, gate to GND (power 9).
        Part("Q2", "AO3401A", "SOT23", nets={"1": GND, "2": BAT, "3": BAT_IN}),
        # JST PH pin 1 positive (power 11). MP: solder tabs, mechanical only.
        Part("J3", "S2B-PH-SM4-TB", "JST_PH2", nets={"1": BAT_IN, "2": GND, "MP": NO_NET},
             x=battery["x"], y=battery["y"]),
        # TPS7A0233 DBV: 1 IN, 2 GND, 3 EN, 4 NC, 5 OUT (power 7.3).
        Part("U4", "TPS7A0233PDBVR", "SOT23-5", **_at(parts["ldo"]),
             nets={"1": VSYS, "2": GND, "3": "LDO_EN", "4": NO_NET, "5": V3}),
        Part("C10", "1uF 50V", "C0603", nets=_two(VSYS, GND)),
        Part("C11", "1uF 50V", "C0603", nets=_two(V3, GND)),   # D14: 1 uF at the LDO output
        # SPDT on the LDO enable: common (2) to EN, one throw to VSYS, the other to GND (power 8).
        Part("SW18", "MSK12C02", "SLIDE", nets={"1": VSYS, "2": "LDO_EN", "3": GND},
             x=switch["x"], y=switch["body_y0"] + switch["body"][1] / 2),
        # MAX17048 TDFN-8: 1 CTG, 2 CELL, 3 VDD, 4 GND, 5 ALRT, 6 QSTRT, 7 SCL, 8 SDA, 9 EP (power 10).
        Part("U5", "MAX17048G+T10", "DFN8", **_at(parts["gauge"]), nets={
            "1": GND, "2": BAT, "3": BAT, "4": GND, "5": "GAUGE_ALRT_N", "6": GND, "7": "I2C_SCL",
            "8": "I2C_SDA", "9": GND}),
        Part("C12", "100nF", "C0402", nets=_two(BAT, GND)),
        Part("R8", "4.7k", "R0402", nets=_two(V3, "I2C_SDA")),   # D15: power owns both pull-ups
        Part("R9", "4.7k", "R0402", nets=_two(V3, "I2C_SCL")),
    ]


# --- reset and SWD (usb-io 6.5, 6.6) ------------------------------------------------------------------------

def _debug() -> list[Part]:
    reset, swd = BOARD_SPEC["reset"], BOARD_SPEC["swd"]
    return [
        Part("SW17", "TS-1187A-B-A-B", "TACT", nets=_two("RESET_N", GND), **_at(reset)),
        # Tag-Connect Cortex pin-out: 1 VCC (sense), 2 SWDIO, 3 nRESET, 4 SWCLK, 5 GND, 6 SWO open.
        Part("J4", "TC2030-NL", "TC2030", **_at(swd), nets={
            "1": V3, "2": "SWDIO", "3": "RESET_N", "4": "SWCLK", "5": GND, "6": NO_NET}),
    ]


# --- key matrix (keys 6.6, D20) -----------------------------------------------------------------------------

def key_centre(row: int, column: int) -> tuple[float, float]:
    keys = BOARD_SPEC["keys"]
    return keys["first_x"] + column * keys["pitch"], keys["first_y"] + row * keys["pitch"]


def row_net(row: int) -> str:
    return f"ROW{row}"


def column_net(column: int) -> str:
    return f"COL{column}"


def matrix_position(row: int, column: int, diode_ref: str, switch_pins: tuple[str, str] = ("1", "2"),
                    diode_at: dict[str, float] | None = None) -> tuple[dict[str, str], Part]:
    """col2row: column -> switch -> diode anode, cathode -> row. 1N4148W: pin 1 K, pin 2 A.
    Returns the switch's two nets and the diode."""
    node = f"K{row}{column}"
    switch_nets = {switch_pins[0]: column_net(column), switch_pins[1]: node}
    return switch_nets, Part(diode_ref, "1N4148W", "SOD123", nets=_two(row_net(row), node), **(diode_at or {}))


def _keys() -> list[Part]:
    keys, diode = BOARD_SPEC["keys"], BOARD_SPEC["keys"]["diode"]
    parts = []
    for row in range(keys["rows"]):
        for column in range(keys["columns"]):
            index = row * keys["columns"] + column + 1
            x, y = key_centre(row, column)
            nets, diode_part = matrix_position(row, column, f"D{index}", diode_at={
                "x": x + diode["offset"][0], "y": y + diode["offset"][1]})
            parts += [Part(f"SW{index}", "CPG135001S30", "CHOC_HOTSWAP", nets=nets, x=x, y=y), diode_part]
    return parts


# Column C4 (D20): encoder pushes and the round buttons, in board.toml matrix.c4 order (rows 0 to 3).
# ENC1 is the right encoder ("encoder 1" in rotary-buttons), ENC2 the left; SW19 the right button, SW20 the
# left; D17 to D20 their diodes.
_C4_REFS = {"encoder_right_push": ("ENC1", "D17"), "encoder_left_push": ("ENC2", "D18"),
            "button_right": ("SW19", "D19"), "button_left": ("SW20", "D20")}


def _encoders_and_buttons() -> list[Part]:
    encoders, buttons = BOARD_SPEC["encoders"], BOARD_SPEC["buttons"]
    column = len(BOARD_SPEC["matrix"]["columns"]) - 1
    row_of = {name: row for row, name in enumerate(BOARD_SPEC["matrix"]["c4"])}
    parts: list[Part] = []
    for ref, name, side, push in (("ENC1", "ENC_R", "right", "encoder_right_push"),
                                  ("ENC2", "ENC_L", "left", "encoder_left_push")):
        encoder = encoders[side]
        # RotaryEncoder_Switch_MP: A, B, C the encoder, S1/S2 the push switch, MP the mounting legs.
        push_nets, diode = matrix_position(row_of[push], column, _C4_REFS[push][1], switch_pins=("S1", "S2"))
        parts += [Part(ref, "PEC12R-4215F-S0024", "PEC12R4", side=TOP, x=encoder["x"], y=encoder["y"],
                       nets={"A": f"{name}_A", "B": f"{name}_B", "C": GND, "MP": GND} | push_nets), diode]
    for ref, side, push in (("SW19", "right", "button_right"), ("SW20", "left", "button_left")):
        push_nets, diode = matrix_position(row_of[push], column, _C4_REFS[push][1])
        parts += [Part(ref, "B3FS-1000P", "B3FS", side=TOP, nets=push_nets, **_at(buttons[side])), diode]
    return parts


def _encoder_filters() -> list[Part]:
    """10 nF from A and B to GND, footprints only (rotary-buttons 6.1, D36)."""
    flt, parts, number = BOARD_SPEC["encoders"]["filter"], [], 13
    for name, side in (("ENC_R", "right"), ("ENC_L", "left")):
        encoder = BOARD_SPEC["encoders"][side]
        for channel, (dx, dy) in zip(("A", "B"), flt["offsets"], strict=True):
            parts.append(Part(f"C{number}", "10nF", "C0402", nets=_two(f"{name}_{channel}", GND),
                              x=encoder["x"] + dx, y=encoder["y"] + dy, fitted=flt["populate"]))
            number += 1
    return parts


# --- test points, holes, fiducials (usb-io 6.8, 6.9; enclosure 6.4) ----------------------------------------

TEST_POINT_NETS = (VBUS_SYS, BAT, VSYS, V3, GND, GND, "CHG_N", "PGOOD_N", "I2C_SDA", "I2C_SCL", "LCD_TE")


def _test_points() -> list[Part]:
    return [Part(f"TP{n}", net, "TESTPAD", nets={"1": net}) for n, net in enumerate(TEST_POINT_NETS, start=1)]


def _holes() -> list[Part]:
    holes = BOARD_SPEC["holes"]
    parts = [Part(f"H{n}", "K M1.6", "HOLE_NPTH4", side=TOP, x=x, y=y)
             for n, (x, y) in enumerate(holes["k"]["positions"], start=1)]
    parts += [Part(f"H{n}", "C M2", "HOLE_NPTH4", side=TOP, x=x, y=y)
              for n, (x, y) in enumerate(holes["c"]["positions"], start=5)]
    parts += [Part(f"H{n}", "G M2", "HOLE_G", side=TOP, nets={"1": GND}, x=x, y=y)
              for n, (x, y) in enumerate(holes["g"]["positions"], start=7)]
    return parts


def _fiducials() -> list[Part]:
    """Three per assembled face (D9: both faces are machine-placed). Positions: layout."""
    return [Part(f"FID{n}", "fiducial", "FIDUCIAL", side=BOTTOM if n <= 3 else TOP) for n in range(1, 7)]


def all_parts() -> list[Part]:
    parts = (_module() + _display() + _usb() + _power() + _debug() + _keys() + _encoders_and_buttons()
             + _encoder_filters() + _test_points() + _holes() + _fiducials())
    refs = [part.ref for part in parts]
    assert len(refs) == len(set(refs)), "duplicate reference designator"
    return parts


def nets_to_pads(parts: list[Part]) -> dict[str, list[str]]:
    connections: dict[str, list[str]] = {}
    for part in parts:
        for pad, net in part.nets.items():
            if net != NO_NET:
                connections.setdefault(net, []).append(f"{part.ref}.{pad}")
    return connections


def check_netlist(parts: list[Part]) -> None:
    """Every net needs at least two pads; a single-pad net is a wiring mistake."""
    dangling = sorted(net for net, pads in nets_to_pads(parts).items() if len(pads) < 2)
    assert not dangling, f"nets with a single pad: {dangling}"


_MICROFARADS = {"10uF": 10.0, "1uF": 1.0, "1uF 50V": 1.0, "100nF": 0.1, "20pF": 20e-6, "10nF": 0.01}


def check_rail_capacitance(parts: list[Part]) -> float:
    """D14: the fitted capacitors on 3V3 plus the module's internal ones are the board.toml list, and stay
    under the TPS7A02 limit. Returns the nominal sum in microfarads."""
    power = BOARD_SPEC["power"]
    internal = power["rail_3v3_caps_uf"][:2]   # VCC and VCCH bulk inside the module (D14)
    fitted = sorted(_MICROFARADS[p.value] for p in parts
                    if p.ref.startswith("C") and p.fitted and V3 in p.nets.values())
    listed = sorted(power["rail_3v3_caps_uf"][2:])
    assert fitted == listed, f"3V3 capacitors {fitted} differ from board.toml power.rail_3v3_caps_uf {listed}"
    total = sum(internal) + sum(fitted)
    assert total <= power["rail_3v3_cap_max_derated_uf"], f"3V3 capacitance {total} uF over the LDO limit"
    return total


if __name__ == "__main__":
    circuit = all_parts()
    check_netlist(circuit)
    check_rail_capacitance(circuit)
    for net_name, pad_names in sorted(nets_to_pads(circuit).items()):
        print(f"{net_name:14} {' '.join(pad_names)}")
