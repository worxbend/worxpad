"""Project footprints for parts KiCad 10.0.7 has no footprint for. Pure Python: writes .kicad_mod text.

    python3 pcb/gen/footprints.py      writes pcb/lib/worxpad.pretty/

Every number comes from board.toml or from the datasheet named in pcb/lib/SOURCES.txt; a value read off a
drawing by scaling, not printed on it, is marked MEASURE here and there. Coordinates are millimetres in
KiCad's footprint frame (X right, Y down), seen from the face the footprint is drawn on. A footprint for a
bottom-face part is drawn as seen from the bottom; KiCad mirrors it in X when the layout flips it.

build.py loads every file written here with pcbnew and compares its pads with what this module meant to write.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import circuit
from circuit import BOARD_SPEC

LIBRARY_DIR = circuit.REPO_ROOT / "pcb" / "lib" / f"{circuit.LIBRARY}.pretty"
FORMAT_VERSION = 20260206   # KiCad 10.0.7 stock footprints
SMD_LAYERS = ("F.Cu", "F.Mask", "F.Paste")
SMD_NO_PASTE = ("F.Cu", "F.Mask")
THT_LAYERS = ("*.Cu", "*.Mask")
COPPER_LAYERS = ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu")   # pcb.layers = 4
FAB_WIDTH, SILK_WIDTH, COURTYARD_WIDTH = 0.1, 0.12, 0.05
COURTYARD_MARGIN = 0.25


def _n(value: float) -> str:
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return "0" if text in ("-0", "") else text


@dataclass(frozen=True)
class Pad:
    number: str
    kind: str                       # smd, thru_hole, np_thru_hole
    shape: str                      # rect, circle, oval, roundrect
    x: float
    y: float
    size: tuple[float, float]
    layers: tuple[str, ...]
    drill: tuple[float, float] | None = None   # (d, d) round, (w, h) oval

    def text(self) -> str:
        drill = ""
        if self.drill is not None:
            w, h = self.drill
            drill = f" (drill {_n(w)})" if w == h else f" (drill oval {_n(w)} {_n(h)})"
        layers = " ".join(f'"{layer}"' for layer in self.layers)
        extra = " (roundrect_rratio 0.25)" if self.shape == "roundrect" else ""
        return (f'(pad "{self.number}" {self.kind} {self.shape} (at {_n(self.x)} {_n(self.y)}) '
                f'(size {_n(self.size[0])} {_n(self.size[1])}){drill} (layers {layers}){extra})')


@dataclass
class Footprint:
    name: str
    description: str
    attribute: str                  # smd or through_hole
    pads: list[Pad] = field(default_factory=list)
    graphics: list[str] = field(default_factory=list)
    zones: list[str] = field(default_factory=list)

    def rect(self, layer: str, x0: float, y0: float, x1: float, y1: float, width: float) -> None:
        self.graphics.append(f'(fp_rect (start {_n(x0)} {_n(y0)}) (end {_n(x1)} {_n(y1)}) '
                             f'(stroke (width {_n(width)}) (type solid)) (fill no) (layer "{layer}"))')

    def line(self, layer: str, x0: float, y0: float, x1: float, y1: float, width: float) -> None:
        self.graphics.append(f'(fp_line (start {_n(x0)} {_n(y0)}) (end {_n(x1)} {_n(y1)}) '
                             f'(stroke (width {_n(width)}) (type solid)) (layer "{layer}"))')

    def circle(self, layer: str, x: float, y: float, radius: float, width: float) -> None:
        self.graphics.append(f'(fp_circle (center {_n(x)} {_n(y)}) (end {_n(x + radius)} {_n(y)}) '
                             f'(stroke (width {_n(width)}) (type solid)) (fill no) (layer "{layer}"))')

    def label(self, layer: str, text: str, x: float, y: float, size: float = 0.8) -> None:
        self.graphics.append(f'(fp_text user "{text}" (at {_n(x)} {_n(y)} 0) (layer "{layer}") '
                             f'(effects (font (size {_n(size)} {_n(size)}) (thickness {_n(size * 0.15)}))))')

    def keepout(self, name: str, x0: float, y0: float, x1: float, y1: float) -> None:
        """Rule area on every copper layer: no track, via, pad or pour. Parts may sit above it."""
        layers = " ".join(f'"{layer}"' for layer in COPPER_LAYERS)
        corners = " ".join(f"(xy {_n(x)} {_n(y)})" for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)))
        self.zones.append(
            f'(zone (net 0) (net_name "") (layers {layers}) (name "{name}") (hatch full 0.5) '
            '(connect_pads (clearance 0)) (min_thickness 0.25) '
            '(keepout (tracks not_allowed) (vias not_allowed) (pads not_allowed) (copperpour not_allowed) '
            '(footprints allowed)) (placement (enabled no) (sheetname "")) '
            '(fill (thermal_gap 0.5) (thermal_bridge_width 0.5) (island_removal_mode 0)) '
            f'(polygon (pts {corners})))')

    def text(self) -> str:
        top = min((p.y - p.size[1] / 2 for p in self.pads), default=0.0) - 1.5
        bottom = max((p.y + p.size[1] / 2 for p in self.pads), default=0.0) + 1.5
        font = "(effects (font (size 1 1) (thickness 0.15)))"
        lines = [
            f'(footprint "{self.name}" (version {FORMAT_VERSION}) (generator "worxpad_gen") '
            '(generator_version "10.0") (layer "F.Cu")',
            f'(descr "{self.description}")',
            f'(property "Reference" "REF**" (at 0 {_n(top)} 0) (layer "F.SilkS") {font})',
            f'(property "Value" "{self.name}" (at 0 {_n(bottom)} 0) (layer "F.Fab") {font})',
            f'(property "Datasheet" "" (at 0 0 0) (layer "F.Fab") (hide yes) {font})',
            f'(property "Description" "" (at 0 0 0) (layer "F.Fab") (hide yes) {font})',
            f"(attr {self.attribute})",
            *self.graphics,
            *(pad.text() for pad in self.pads),
            *self.zones,
            ")",
        ]
        return "\n".join(lines) + "\n"


def _courtyard(fp: Footprint, x0: float, y0: float, x1: float, y1: float, layer: str = "F.CrtYd") -> None:
    m = COURTYARD_MARGIN
    fp.rect(layer, x0 - m, y0 - m, x1 + m, y1 + m, COURTYARD_WIDTH)


# --- u-blox BMD-340 (data sheet UBX-19033353 R13, figure 2 pin assignment, figure 12 land pads) -------------

def bmd340_pad_positions() -> dict[str, tuple[float, float]]:
    """Pad number -> centre, module top view, origin at the module centre, antenna toward -X.

    Figure 12 dimensions: outer rows at Y -/+4.40, inner rows 0.90 apart; columns on a 1.10 mm pitch from
    X -2.85; right-hand columns at X 6.85, 5.95, 5.05 and 4.15. Figure 2 gives the numbering."""
    pitch, step = 1.10, 0.90
    outer = [-2.85 + pitch * k for k in range(9)]
    second = [-2.30 + pitch * k for k in range(7)]
    third = [-1.75 + pitch * k for k in range(5)]
    rows = {
        -4.40: (outer, (45, 43, 41, 39, 37, 35, 33, 31, 30)),
        -4.40 + step: (second, (44, 42, 40, 38, 36, 34, 32)),
        -4.40 + 2 * step: (third, (60, 59, 58, 57, 56)),
        4.40 - 2 * step: (third, (48, 49, 50, 51, 52)),
        4.40 - step: (second, (2, 4, 6, 8, 10, 12, 14)),
        4.40: (outer, (1, 3, 5, 7, 9, 11, 13, 15, 16)),
    }
    columns = {
        6.85: ([-3.85 + pitch * k for k in range(8)], (68, 67, 66, 65, 64, 63, 62, 61)),
        6.85 - step: ([-3.30 + pitch * k for k in range(7)], (29, 27, 25, 23, 21, 19, 17)),
        6.85 - 2 * step: ([-2.75 + pitch * k for k in range(6)], (28, 26, 24, 22, 20, 18)),
        6.85 - 3 * step: ([-1.10, 0.0, 1.10], (55, 54, 53)),
    }
    positions = {}
    for y, (xs, numbers) in rows.items():
        positions |= {str(n): (x, y) for x, n in zip(xs, numbers, strict=True)}
    for x, (ys, numbers) in columns.items():
        positions |= {str(n): (x, y) for y, n in zip(ys, numbers, strict=True)}
    positions["46"], positions["47"] = (-2.85, -1.65), (-2.85, 1.65)
    assert sorted(map(int, positions)) == list(range(1, 69)), "BMD-340 pads are not 1 to 68"
    return {n: (round(x, 3), round(y, 3)) for n, (x, y) in positions.items()}


BMD340_PAD = 0.50


def bmd340() -> Footprint:
    module, keepout = BOARD_SPEC["module"], BOARD_SPEC["module"]["keepout"]
    half_x, half_y = module["length"] / 2, module["width"] / 2
    strip_end = -half_x + module["antenna_strip"]          # first pad column edge, X -3.10
    fp = Footprint("BMD-340", "u-blox BMD-340 nRF52840 module, LGA 68 pads, antenna toward -X, "
                   "RF keep-out to the first pad column (UBX-19033353 R13 figure 12; D22)", "smd")
    for number, (x, y) in sorted(bmd340_pad_positions().items(), key=lambda item: int(item[0])):
        fp.pads.append(Pad(number, "smd", "rect", x, y, (BMD340_PAD, BMD340_PAD), SMD_LAYERS))
    fp.rect("F.Fab", -half_x, -half_y, half_x, half_y, FAB_WIDTH)
    fp.line("F.Fab", strip_end, -half_y, strip_end, half_y, FAB_WIDTH)
    fp.label("F.Fab", "ANT", -half_x + module["antenna_strip"] / 2, 0)
    silk = 0.11
    fp.rect("F.SilkS", -half_x - silk, -half_y - silk, half_x + silk, half_y + silk, SILK_WIDTH)
    fp.circle("F.SilkS", -2.85, half_y + 0.5, 0.15, SILK_WIDTH)   # pin 1 mark beside pad 1
    _courtyard(fp, -half_x, -half_y, half_x, half_y)
    # D22: depth = antenna strip + antenna inset, from the board edge to the first pad column.
    depth = module["antenna_strip"] + module["antenna_inset"]
    assert abs(depth - keepout["depth"]) < 1e-9, "board.toml module.keepout.depth is not strip + inset (D22)"
    fp.keepout("RF keep-out", strip_end - depth, -keepout["length"] / 2, strip_end, keepout["length"] / 2)
    return fp


# --- Hirose FH34SRJ-24S-0.5SH(50) (Hirose FH34SRJ catalogue, recommended PCB mounting pattern) --------------

FH34_PITCH, FH34_CONTACTS = 0.5, 24
FH34_PAD, FH34_MOUNT_PAD = (0.3, 0.8), (0.4, 0.8)
FH34_B, FH34_E, FH34_F = 11.5, 13.1, 13.9     # table values for 24 contacts
FH34_A, FH34_DEPTH = 14.0, 3.8                # body width and overall depth (catalogue A and (3.8))
FH34_PAD_INSET = 0.35                         # MEASURE: part rear to the contact pad outer end, scaled
FH34_PAD_TO_MOUNT = 2.5                       # contact pad centre to mounting pad centre (3.3 - 0.4 - 0.4)


def fh34srj_24() -> Footprint:
    """Origin at the centre of the part's rear edge (board.toml display.connector y_back), FPC entry toward +Y,
    contact 1 toward +X (the end nearest the right face, display 6.5)."""
    fp = Footprint("FH34SRJ-24S-0.5SH", "Hirose FH34SRJ-24S-0.5SH(50) FPC connector, 24 contacts 0.5 mm, "
                   "top and bottom contact, FPC entry toward +Y, contact 1 at +X", "smd")
    pad_y = FH34_PAD_INSET + FH34_PAD[1] / 2
    for n in range(1, FH34_CONTACTS + 1):
        fp.pads.append(Pad(str(n), "smd", "rect", FH34_B / 2 - FH34_PITCH * (n - 1), pad_y, FH34_PAD, SMD_LAYERS))
    mount_x = (FH34_E + FH34_F) / 4
    for x in (-mount_x, mount_x):
        fp.pads.append(Pad("MP", "smd", "rect", x, pad_y + FH34_PAD_TO_MOUNT, FH34_MOUNT_PAD, SMD_LAYERS))
    fp.rect("F.Fab", -FH34_A / 2, 0, FH34_A / 2, FH34_DEPTH, FAB_WIDTH)
    fp.label("F.Fab", "FPC entry", 0, FH34_DEPTH - 0.6, 0.6)
    fp.circle("F.SilkS", FH34_B / 2 + 0.6, -0.3, 0.15, SILK_WIDTH)   # contact 1 mark
    _courtyard(fp, -FH34_F / 2, 0, FH34_F / 2, FH34_DEPTH)
    return fp


# --- HRO TYPE-C-31-M-13C (HRO drawing, recommended PCB layout, component side) ------------------------------

USB_SIGNAL_PADS = {   # pad -> X, seen from the component side with the board edge at Y 0 and the board at +Y
    "A1": 3.20, "B12": 3.20, "A4": 2.40, "B9": 2.40, "B8": 1.75, "A5": 1.25, "B7": 0.75, "A6": 0.25,
    "A7": -0.25, "B6": -0.75, "A8": -1.25, "B5": -1.75, "B4": -2.40, "A9": -2.40, "B1": -3.20, "A12": -3.20,
}
USB_WIDE_PADS = {"A1", "B12", "A4", "B9", "B4", "A9", "B1", "A12"}   # 0.60 wide; the others 0.30
USB_PAD_Y = (6.70, 7.80)        # pad row from the notch end (2.10 + 4.60) to 2.10 + 5.70 from the edge line
USB_SLOT_X = 11.24 / 2
USB_SLOTS = ((2.10, 1.80), (6.10, 1.40))   # (centre from the edge line, drill length); drill width 0.60
USB_SLOT_WIDTH, USB_SLOT_RING = 0.60, 0.20  # MEASURE: copper ring scaled from the drawing hatch


def usb_c_m13c() -> Footprint:
    """Origin on the board edge line at the receptacle centre (board.toml usb.x, usb.front_y). The signal pads
    end at the notch edge, as the drawing shows: they need a local copper-to-edge exception there."""
    usb = BOARD_SPEC["usb"]
    fp = Footprint("USB_C_HRO_TYPE-C-31-M-13C", "HRO TYPE-C-31-M-13C mid-mount USB-C receptacle, 1.60 mm sink, "
                   "16 pins, in a 9.24 x 6.70 mm board notch; origin on the edge line", "smd")
    y0, y1 = USB_PAD_Y
    for number, x in USB_SIGNAL_PADS.items():
        width = 0.60 if number in USB_WIDE_PADS else 0.30
        fp.pads.append(Pad(number, "smd", "rect", x, (y0 + y1) / 2, (width, y1 - y0), SMD_LAYERS))
    for y, length in USB_SLOTS:
        for x in (-USB_SLOT_X, USB_SLOT_X):
            copper = (USB_SLOT_WIDTH + 2 * USB_SLOT_RING, length + 2 * USB_SLOT_RING)
            fp.pads.append(Pad("SH", "thru_hole", "oval", x, y, copper, THT_LAYERS, (USB_SLOT_WIDTH, length)))
    half = usb["width"] / 2
    fp.rect("F.Fab", -half, 0, half, usb["length"], FAB_WIDTH)
    fp.label("F.Fab", "edge", 0, 0.6, 0.6)
    _courtyard(fp, -half - 0.4, 0, half + 0.4, y1)
    return fp


# --- Kailh Choc V2 hot-swap socket CPG135001S30 (board.toml [keys.footprint]; keys 6.1) ---------------------

def choc_hotswap() -> Footprint:
    """Drawn as seen from the socket face (the PCB bottom): board.toml's top-view X is negated here, so the
    layout's flip puts every hole and pad back where board.toml has it. Origin at the switch centre."""
    spec, keepout = BOARD_SPEC["keys"]["footprint"], BOARD_SPEC["keys"]["keepout"]
    fp = Footprint("Choc_V2_Hotswap", "Kailh Choc V2 (PG1353) switch with CPG135001S30 hot-swap socket; "
                   "drawn on the socket face, origin at the switch centre", "smd")
    hole = spec["centre_hole"]
    fp.pads.append(Pad("", "np_thru_hole", "circle", 0, 0, (hole, hole), THT_LAYERS, (hole, hole)))
    barrel = spec["barrel_hole_diameter"]
    for x, y in spec["barrel_holes"]:
        fp.pads.append(Pad("", "np_thru_hole", "circle", -x, y, (barrel, barrel), THT_LAYERS, (barrel, barrel)))
    (x3, y3), d3 = spec["third_hole"], spec["third_hole_diameter"]
    fp.pads.append(Pad("", "np_thru_hole", "circle", -x3, y3, (d3, d3), THT_LAYERS, (d3, d3)))
    # Pad 1 beside the switch pin-1 barrel (-5.00, 3.80), pad 2 beside the pin-2 barrel (0, 6.00).
    pad_2, pad_1 = spec["socket_pads"]
    for number, (x, y) in (("1", pad_1), ("2", pad_2)):
        fp.pads.append(Pad(number, "smd", "rect", -x, y, tuple(spec["socket_pad_size"]), SMD_NO_PASTE))
    x0, y0, x1, y1 = keepout["socket_zone"]
    fp.rect("F.Fab", -x1, y0, -x0, y1, FAB_WIDTH)
    fp.rect("F.CrtYd", -x1, y0, -x0, y1, COURTYARD_WIDTH)
    # The switch sits on the other face: its flange on B.Fab, the 14.6 mm top-face keep-out on B.CrtYd.
    flange, clear = BOARD_SPEC["keys"]["flange"] / 2, keepout["top_clear"] / 2
    fp.rect("B.Fab", -flange, -flange, flange, flange, FAB_WIDTH)
    fp.rect("B.CrtYd", -clear, -clear, clear, clear, COURTYARD_WIDTH)
    return fp


# --- Bourns PEC12R-4xxxF-Sxxxx (rotary-buttons 6.1, datasheet REV. 07/21, -4 drawing) ------------------------

PEC12R_PIN_DRILL, PEC12R_PIN_PAD = 1.1, 1.8          # hole 1.0 +0.2/-0: middle of the band
PEC12R_LEG_DRILL = (2.1, 2.2)                        # slot 2.1 +0.2 x 2.0 +0.2 (X x Y), middle of the band
PEC12R_LEG_RING = 0.4


def pec12r_4() -> Footprint:
    """Origin at the shaft. A/C/B row toward -Y (the rear), switch pins toward +Y, legs at +/-X.
    The pin pattern is the stock PEC12R-3x17F footprint turned a quarter; only the leg spacing differs."""
    enc = BOARD_SPEC["encoders"]
    row_a = enc["pin_row_rear_y"] - enc["right"]["y"]       # -7.5
    row_s = enc["pin_row_front_y"] - enc["right"]["y"]      # +7.0
    span = enc["pin_half_span"]
    fp = Footprint("PEC12R-4xxxF-S", "Bourns PEC12R-4xxxF-Sxxxx encoder with push switch, no bushing; "
                   "legs 13.2 mm apart; origin at the shaft", "through_hole")
    pins = (("A", span, row_a), ("C", 0.0, row_a), ("B", -span, row_a), ("S1", span, row_s), ("S2", -span, row_s))
    for number, x, y in pins:
        shape = "rect" if number == "A" else "circle"
        fp.pads.append(Pad(number, "thru_hole", shape, x, y, (PEC12R_PIN_PAD, PEC12R_PIN_PAD), THT_LAYERS,
                           (PEC12R_PIN_DRILL, PEC12R_PIN_DRILL)))
    leg_copper = (PEC12R_LEG_DRILL[0] + 2 * PEC12R_LEG_RING, PEC12R_LEG_DRILL[1] + 2 * PEC12R_LEG_RING)
    for x in (-enc["leg_offset"], enc["leg_offset"]):
        fp.pads.append(Pad("MP", "thru_hole", "oval", x, 0, leg_copper, THT_LAYERS, PEC12R_LEG_DRILL))
    bx, by = enc["body"][0] / 2, enc["body"][1] / 2
    fp.rect("F.Fab", -bx, -by, bx, by, FAB_WIDTH)
    fp.circle("F.Fab", 0, 0, 3.0, FAB_WIDTH)
    pocket = BOARD_SPEC["plinth"]["pocket"] / 2       # 14.8 mm top-face keep-out (rotary-buttons 7)
    fp.rect("F.CrtYd", -pocket, -pocket, pocket, pocket, COURTYARD_WIDTH)
    return fp


# --- G screw hole: plated, GND ring on both faces (board.toml [holes.g]; D6) --------------------------------

def hole_g() -> Footprint:
    g = BOARD_SPEC["holes"]["g"]
    fp = Footprint("Hole_G_M2_Plated", "Plated M2 hole with a GND ring on both faces for case bonding (D6)",
                   "through_hole")
    fp.pads.append(Pad("1", "thru_hole", "circle", 0, 0, (g["ring"], g["ring"]), THT_LAYERS,
                       (g["pcb_hole"], g["pcb_hole"])))
    fp.circle("F.CrtYd", 0, 0, g["keepout_top"] / 2, COURTYARD_WIDTH)
    fp.circle("F.Fab", 0, 0, g["head"] / 2, FAB_WIDTH)
    return fp


ALL = {"BMD340": bmd340, "FH34SRJ24": fh34srj_24, "USBC_M13C": usb_c_m13c, "CHOC_HOTSWAP": choc_hotswap,
       "PEC12R4": pec12r_4, "HOLE_G": hole_g}


def footprints() -> dict[str, Footprint]:
    """Footprint key (as in circuit.FOOTPRINT) -> footprint. The names must match circuit.FOOTPRINT."""
    made = {key: make() for key, make in ALL.items()}
    for key, fp in made.items():
        assert circuit.FOOTPRINT[key] == f"{circuit.LIBRARY}:{fp.name}", f"{key}: name {fp.name}"
    return made


def write(directory: Path = LIBRARY_DIR) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    written = []
    for fp in footprints().values():
        path = directory / f"{fp.name}.kicad_mod"
        path.write_text(fp.text())
        written.append(path)
    stale = {p.name for p in directory.glob("*.kicad_mod")} - {p.name for p in written}
    assert not stale, f"footprints in {directory} that no generator writes: {sorted(stale)}"
    return written


if __name__ == "__main__":
    for written_path in write():
        print(written_path.relative_to(circuit.REPO_ROOT))
