"""Builds the placed, unrouted KiCad board from circuit.py and board.toml. Needs pcbnew (KiCad container).

Positions: a part with an x and y in circuit.py sits where board.toml puts it; the rest sit at the spots in
PLACEMENT below, chosen here because board.toml holds no position for them. Every spot is a layout choice,
not a measurement. check_placement() asserts the rules that are easy to get backwards: the antenna end at
the right edge, the RF keep-out on every copper layer, the display connector's contact 1 and FPC entry,
the socket mirroring, the USB mouth, the cell connector's mouth, the switch actuator, and the faces (D9).

Stack-up (4 layers): F.Cu signal, In1.Cu ground plane, In2.Cu 3.3 V plane, B.Cu signal. Ground pours on
F.Cu and B.Cu after routing.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import pcbnew

import circuit
import models
import schematic
from circuit import BOARD_SPEC, BOTTOM, GND, NO_NET, V3, Part
from router import BACK, FRONT, GROUND_INNER, INNER, Rules

STOCK_FOOTPRINTS = Path("/usr/share/kicad/footprints")
PROJECT_FOOTPRINTS = circuit.REPO_ROOT / "pcb" / "lib"
POSITION_TOLERANCE = 0.02
PCB = BOARD_SPEC["pcb"]

# JLCPCB 4-layer capability is 0.09 mm track and space (fab.py README). 0.10 mm is needed to leave the
# inner pad rings of the BMD-340 (0.40 mm gaps between rows); everything else uses the same rule.
TRACK_WIDTH = 0.10
CLEARANCE = 0.10
POWER_TRACK_WIDTH = 0.30     # pcb/README.md net classes: the floor for supply nets
VIA_DIAMETER = 0.60
VIA_DRILL = 0.30
EDGE_CLEARANCE = BOARD_SPEC["case"]["copper_to_edge"]
SILK_EDGE_CLEARANCE = 0.2
ROUTING_RULES = Rules(track_width=TRACK_WIDTH, wide_track_width=POWER_TRACK_WIDTH, clearance=CLEARANCE,
                      via_diameter=VIA_DIAMETER, via_drill=VIA_DRILL, edge_clearance=EDGE_CLEARANCE,
                      search_limit=200_000,   # then the coarse-map search (router._find_way) takes over
                      # short hops on In2.Cu, the 3.3 V plane, and dearer ones on In1.Cu, the ground plane (route.py)
                      layers=(FRONT, BACK, INNER, GROUND_INNER))

# Parts board.toml gives no position: (x, y, rotation in degrees), top-view board coordinates.
# Rotation is the part's own turn before the bottom-face mirror (see _place).
PLACEMENT: dict[str, tuple[float, float, float]] = {
    # Module bulk, crystal and load capacitors in front of the module, left of the RF bay (x < 114.85).
    # Module bulk, crystal and load capacitors in front of the module, left of the module's front-row signal
    # pads (X 112 to 117), which need the way out toward the front.
    "C3": (107.4, 59.0, 0), "Y1": (110.2, 61.0, 90), "C1": (107.9, 62.5, 0), "C2": (107.9, 61.0, 0),
    "C4": (99.0, 52.0, 90),                                                       # flash VCC
    # Display backlight and supply parts on the bottom, behind the connector (display 7).
    "Q1": (98.6, 45.8, 0), "R2": (98.6, 48.6, 0), "R1": (101.6, 45.0, 0), "C5": (102.9, 46.6, 0),
    "C6": (105.0, 47.8, 0),
    # Charger ring (power 6.3), LDO capacitors, gauge parts, reverse FET at the cell connector.
    "C7": (106.0, 28.6, 0), "C8": (102.4, 32.6, 90), "C9": (109.6, 32.0, 90), "R5": (106.0, 35.4, 0),
    "R6": (108.2, 35.4, 0), "R7": (103.8, 35.4, 0), "C10": (111.2, 44.0, 90), "C11": (104.4, 44.2, 90),
    "C12": (100.0, 27.6, 0), "R8": (97.3, 29.4, 0), "R9": (97.3, 30.6, 0), "Q2": (101.6, 39.6, 0),
    # Column-4 diodes under their switches.
    "D17": (110.13, 24.6, 0), "D18": (91.44, 24.6, 0), "D19": (110.13, 71.2, 0),
    "D20": (91.44, 67.0, 0),   # in front of SW20, outside J4's 3 mm low zone (swd.low_zone)
    # Test pads on the bottom, outside the RF bay, reachable with the bottom shell off (usb-io 6.8).
    "TP1": (96.0, 64.5, 0), "TP2": (99.0, 64.5, 0), "TP3": (102.0, 64.5, 0), "TP4": (105.0, 64.5, 0),
    "TP5": (108.0, 64.5, 0), "TP6": (99.0, 77.5, 0), "TP7": (96.0, 67.5, 0), "TP8": (99.0, 67.5, 0),
    "TP9": (102.0, 67.5, 0), "TP10": (105.0, 67.5, 0), "TP11": (108.0, 67.5, 0),
    # Fiducials: three per face, not on one line (D9). FID1-3 bottom, FID4-6 top.
    "FID1": (42.575, 30.5, 0), "FID2": (80.0, 76.0, 0), "FID3": (117.5, 39.0, 0),
    "FID4": (23.525, 23.525, 0), "FID5": (61.625, 61.625, 0), "FID6": (100.0, 40.0, 0),
}
# Turns for parts that board.toml does place. The asserts in check_placement say why each one is right.
# U2 turns a quarter so its pin rows run along Y: the module's left pad column (rows, USB, VBUS_SYS) then has
# 4.4 mm to the flash instead of 2.25 mm. board.toml flash.size lists the lead span first.
ROTATION = {"U2": 90, "J3": 270, "SW18": 180, "R3": 90, "R4": 90, "F1": 90, "C13": 90, "C14": 90, "C15": 90, "C16": 90}
# board.toml points that are a body centre while the footprint origin is elsewhere: offset of the origin
# from the body centre in the part's own frame (before rotation and mirror). J3: the fab outline of the
# stock PH footprint runs Y -3.25 to 4.45 about its origin.
ORIGIN_OFFSET = {"J3": (0.0, -0.6)}
# Layout moves from a board.toml guess, each with its reason. tools/check_spec.py checked the board.toml
# value; check_placement re-checks the rule at the moved spot. Request: copy these into board.toml.
MOVED = {
    "U6": ((100.8, 11.2), "J1's twelve pads need a band to spread out in before the ESD array; its pads stay "
                          "within 3 mm of J1's pads"),
    "J4": ((92.0, 76.6), "TC2030 locating holes clear SW20's top-face courtyard (Y 74.64)"),
}
# Parts whose body overhangs a tongue edge: their silkscreen outside the board is cut.
OVERHANGING = {"J1", "SW18"}
# Encoder pin pads near the USB-C shell slots. With the stock 1.8 mm pads (A square) the left encoder's A pin
# shorts J1's rear shell slot and the right encoder's B pin keeps 0.08 mm (encoder pin rows at Y 7.60,
# rotary-buttons 6.2; slots at X 100.8 +/- 5.62, Y 6.35). Round 1.6 mm pads on the 1.1 mm hole keep 0.25 mm of
# ring and 0.18 mm of clearance. Request: move this into footprints.pec12r_4.
ENCODER_PIN_PAD = 1.6
# Hole keep-outs from board.toml, as (top diameter, bottom diameter). The stock MountingHole_4mm courtyard
# (8.6 mm) is replaced by these checks: a hole keep-out and a switch's empty 14.6 mm square may overlap.
HOLE_KEEPOUT = {
    "K M1.6": (BOARD_SPEC["holes"]["k"]["keepout_top"], BOARD_SPEC["holes"]["k"]["keepout_bottom"]),
    "C M2": (BOARD_SPEC["holes"]["c"]["keepout"], BOARD_SPEC["holes"]["c"]["keepout"]),
    "G M2": (BOARD_SPEC["holes"]["g"]["keepout_top"], BOARD_SPEC["holes"]["g"]["ring"]),
}

# JLCPCB's default 4-layer 1.6 mm stack-up JLC04161H-7628, the one the order notes name (fab.py README), top
# to bottom: (layer name, KiCad type, thickness mm, material, epsilon_r). Thicknesses are JLCPCB's published
# table as remembered, not re-read for this board: check them on JLCPCB's stack-up page before ordering.
# Written into the board so that the STEP and any impedance figure use the real stack (pcb.thickness).
STACKUP = (
    ("F.Mask", "Top Solder Mask", 0.01, None, None),
    ("F.Cu", "copper", 0.035, None, None),
    ("dielectric 1", "prepreg", 0.2104, "7628", 4.4),
    ("In1.Cu", "copper", 0.0152, None, None),
    ("dielectric 2", "core", 1.065, "FR4", 4.6),
    ("In2.Cu", "copper", 0.0152, None, None),
    ("dielectric 3", "prepreg", 0.2104, "7628", 4.4),
    ("B.Cu", "copper", 0.035, None, None),
    ("B.Mask", "Bottom Solder Mask", 0.01, None, None),
)
STACKUP_TOLERANCE = 0.01   # mm between the stack-up sum and pcb.thickness

# Battery polarity at J3 (power 11): retail JST-PH cells come wired either way, so "+" at pin 1 and "-" at
# pin 2 on the bottom silkscreen. Each mark sits in the gap the stock silk outline leaves past its pad: GAP
# from the pad edge along the pin row (to the mark centre), INSET along the pad toward the connector body.
# The gap is 1.16 x 1.48 mm, so the text is 0.8 mm; DRC's silk_overlap check covers the fit.
POLARITY_MARKS = (("1", "+"), ("2", "-"))
POLARITY_MARK_GAP = 0.9
POLARITY_MARK_INSET = 0.35
POLARITY_MARK_SIZE = 0.8
POLARITY_MARK_STROKE = 0.12

# Every reference on the silkscreen would not fit between the parts. The assembly drawings (F.Fab, B.Fab)
# carry all of them; the silkscreen names the connectors, the module and the hand-fitted parts.
SILK_LABELLED = {"U1", "J1", "J2", "J3", "J4", "SW17", "SW18"}


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


def point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(mm(x), mm(y))


def pad_xy(pad: pcbnew.PAD) -> tuple[float, float]:
    position = pad.GetPosition()
    return pcbnew.ToMM(position.x), pcbnew.ToMM(position.y)


def _load_footprint(name: str) -> pcbnew.FOOTPRINT:
    library, footprint_name = name.split(":")
    root = PROJECT_FOOTPRINTS if library == circuit.LIBRARY else STOCK_FOOTPRINTS
    footprint = pcbnew.FootprintLoad(str(root / f"{library}.pretty"), footprint_name)
    assert footprint is not None, f"footprint not found: {name}"
    footprint.SetFPID(pcbnew.LIB_ID(library, footprint_name))
    return footprint


def _board_net(board: pcbnew.BOARD, board_name: str) -> pcbnew.NETINFO_ITEM:
    existing = board.FindNet(board_name)
    if existing is not None:
        return existing
    net = pcbnew.NETINFO_ITEM(board, board_name)
    board.Add(net)
    return net


def _net(board: pcbnew.BOARD, name: str) -> pcbnew.NETINFO_ITEM:
    return _board_net(board, schematic.board_net_name(name))


# --- where each part goes ----------------------------------------------------------------------------------

def target(part: Part) -> tuple[float, float, float]:
    """(x, y, rotation) of the board.toml reference point of a part."""
    if part.ref in PLACEMENT:
        assert part.x is None, f"{part.ref}: board.toml places it; remove it from PLACEMENT"
        return PLACEMENT[part.ref]
    assert part.x is not None, f"{part.ref}: no position in board.toml and none in PLACEMENT"
    x, y = MOVED.get(part.ref, ((part.x, part.y), ""))[0]
    return x, y, ROTATION.get(part.ref, 0)


def _turned(dx: float, dy: float, orientation: float, bottom: bool) -> tuple[float, float]:
    """A vector in footprint coordinates as it lands on the board (KiCad turns counter-clockwise, Y down)."""
    if bottom:
        dy = -dy
    a = math.radians(orientation)
    return dx * math.cos(a) + dy * math.sin(a), -dx * math.sin(a) + dy * math.cos(a)


def _place(board: pcbnew.BOARD, part: Part, open_pin_nets: dict[str, str]) -> pcbnew.FOOTPRINT:
    footprint = _load_footprint(part.footprint)
    models.attach(part.footprint_key, footprint)
    board.Add(footprint)  # pcbnew crashes when it flips a footprint that has no board
    footprint.SetReference(part.ref)
    footprint.SetPath(pcbnew.KIID_PATH(f"/{schematic.symbol_uuid(part.ref)}"))
    footprint.SetValue(part.value)
    x, y, rotation = target(part)
    bottom = part.side == BOTTOM
    # A top-bottom flip mirrors Y; the extra half turn makes it the X mirror seen from the top. A bottom-face
    # project footprint is drawn as seen from its own face, so this mirror puts it where board.toml has it.
    orientation = rotation + 180 if bottom else rotation
    ox, oy = _turned(*ORIGIN_OFFSET.get(part.ref, (0.0, 0.0)), orientation, bottom)
    footprint.SetPosition(point(x + ox, y + oy))
    if bottom:
        footprint.Flip(footprint.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
    footprint.SetOrientationDegrees(orientation)
    footprint.SetField("LCSC", part.lcsc)   # empty where the schematic symbol has it empty
    footprint.GetField("LCSC").SetVisible(False)
    footprint.Value().SetVisible(False)
    footprint.Reference().SetVisible(part.ref in SILK_LABELLED)
    if part.ref in OVERHANGING:
        _remove_silkscreen_off_the_board(footprint)
    if part.footprint_key == "PEC12R4":
        _shrink_encoder_pins(footprint)
    if part.value in HOLE_KEEPOUT:
        _drop_courtyard(footprint)
    if not part.machine_assembled:
        footprint.SetExcludedFromPosFiles(True)
    if part.footprint_key in circuit.NOT_A_PART - {"TESTPAD", "FIDUCIAL"} or not part.fitted:
        footprint.SetExcludedFromBOM(True)
    if not part.fitted:
        footprint.SetDNP(True)
    _connect(board, footprint, part, open_pin_nets)
    return footprint


def _remove_silkscreen_off_the_board(footprint: pcbnew.FOOTPRINT) -> None:
    """The USB receptacle and the slide switch overhang their tongues and their outlines with them."""
    for item in list(footprint.GraphicalItems()):
        if item.GetLayer() not in (pcbnew.F_SilkS, pcbnew.B_SilkS):
            continue
        box = item.GetBoundingBox()
        inside = (box.GetLeft() >= mm(PCB["x0"] + SILK_EDGE_CLEARANCE)
                  and box.GetTop() >= mm(PCB["y0"] + SILK_EDGE_CLEARANCE)
                  and box.GetRight() <= mm(PCB["x1"] - SILK_EDGE_CLEARANCE)
                  and box.GetBottom() <= mm(PCB["y1"] - SILK_EDGE_CLEARANCE))
        if not inside:
            footprint.Remove(item)


def _shrink_encoder_pins(footprint: pcbnew.FOOTPRINT) -> None:
    for pad in footprint.Pads():
        if pad.GetNumber() in ("A", "B", "C", "S1", "S2"):
            pad.SetShape(pcbnew.F_Cu, pcbnew.PAD_SHAPE_CIRCLE)
            pad.SetSize(pcbnew.F_Cu, pcbnew.VECTOR2I(mm(ENCODER_PIN_PAD), mm(ENCODER_PIN_PAD)))


def _drop_courtyard(footprint: pcbnew.FOOTPRINT) -> None:
    for item in list(footprint.GraphicalItems()):
        if item.GetLayer() in (pcbnew.F_CrtYd, pcbnew.B_CrtYd):
            footprint.Remove(item)
    footprint.SetAllowMissingCourtyard(True)


def _connect(board: pcbnew.BOARD, footprint: pcbnew.FOOTPRINT, part: Part, open_pin_nets: dict[str, str]) -> None:
    """Nets from circuit.py. An open pin gets the one-pad net KiCad's netlist names for it."""
    pad_numbers = {pad.GetNumber() for pad in footprint.Pads()}
    unknown = set(part.nets) - pad_numbers
    assert not unknown, f"{part.ref}: no such pads {sorted(unknown)}"
    for pad in footprint.Pads():
        net_name = part.nets.get(pad.GetNumber(), NO_NET)
        open_net = open_pin_nets.get(f"{part.ref}.{pad.GetNumber()}")
        if net_name != NO_NET:
            pad.SetNet(_net(board, net_name))
        elif open_net is not None:
            pad.SetNet(_board_net(board, open_net))


# --- outline -----------------------------------------------------------------------------------------------

_ARC_STEPS = 8


def outline_pieces() -> list[list[tuple[float, float]]]:
    """The board outline, clockwise on screen, as pieces: two points for a straight side, _ARC_STEPS + 1
    points for an R corner. Main rectangle with rounded corners; the rear edge (Y = pcb.y0) carries the
    tongues, and the USB notch is cut into its tongue (board.toml [pcb], [[pcb.tongues]], [[pcb.notches]])."""
    x0, y0, x1, y1, r = PCB["x0"], PCB["y0"], PCB["x1"], PCB["y1"], PCB["corner_radius"]

    def corner(cx: float, cy: float, start: float) -> list[tuple[float, float]]:
        return [(cx + r * math.cos(math.radians(start + 90 * k / _ARC_STEPS)),
                 cy + r * math.sin(math.radians(start + 90 * k / _ARC_STEPS))) for k in range(_ARC_STEPS + 1)]

    rear = [(x0 + r, y0)]
    notches = {n["name"]: n for n in PCB["notches"]}
    for tongue in sorted(PCB["tongues"], key=lambda t: t["x0"]):
        rear += [(tongue["x0"], y0), (tongue["x0"], tongue["y0"])]
        notch = notches.get(tongue["name"])
        if notch is not None:
            assert notch["y0"] == tongue["y0"], f"notch {notch['name']} does not open on its tongue edge"
            rear += [(notch["x0"], tongue["y0"]), (notch["x0"], notch["y1"]),
                     (notch["x1"], notch["y1"]), (notch["x1"], tongue["y0"])]
        rear += [(tongue["x1"], tongue["y0"]), (tongue["x1"], y0)]
    rear.append((x1 - r, y0))
    pieces = [corner(x0 + r, y0 + r, 180)] + [list(side) for side in zip(rear, rear[1:], strict=False)]
    pieces += [corner(x1 - r, y0 + r, 270), [(x1, y0 + r), (x1, y1 - r)], corner(x1 - r, y1 - r, 0),
               [(x1 - r, y1), (x0 + r, y1)], corner(x0 + r, y1 - r, 90), [(x0, y1 - r), (x0, y0 + r)]]
    return pieces


def outline_points() -> list[tuple[float, float]]:
    """The outline as one closed polygon (corners cut into segments), for zones and the router."""
    points = [p for piece in outline_pieces() for p in piece[:-1]]
    return [(round(x, 4), round(y, 4)) for x, y in points]


def _outline(board: pcbnew.BOARD) -> None:
    """Edge.Cuts: straight sides as lines, R corners as true arcs."""
    for piece in outline_pieces():
        if len(piece) == 2:
            shape = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
            shape.SetStart(point(*piece[0]))
            shape.SetEnd(point(*piece[1]))
        else:
            shape = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_ARC)
            shape.SetArcGeometry(point(*piece[0]), point(*piece[len(piece) // 2]), point(*piece[-1]))
        _add_edge(board, shape)


def _add_edge(board: pcbnew.BOARD, shape: pcbnew.PCB_SHAPE) -> None:
    shape.SetLayer(pcbnew.Edge_Cuts)
    shape.SetWidth(mm(0.05))
    board.Add(shape)


# --- copper zones ------------------------------------------------------------------------------------------

def _zone(board: pcbnew.BOARD, net_name: str, layer: int, polygon: list[tuple[float, float]],
          priority: int = 0) -> None:
    zone = pcbnew.ZONE(board)
    zone.SetLayer(layer)
    zone.SetNet(_net(board, net_name))
    zone.SetAssignedPriority(priority)
    # Solid connections: the USB-C shell slots sit at the notch edge where thermal spokes cannot form, and the
    # G holes bond the case. The encoder ground pins are the only other through-hole ground pads.
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    zone.SetMinThickness(mm(0.2))
    zone.SetLocalClearance(mm(0.2))
    outline = zone.Outline()
    outline.NewOutline()
    for x, y in polygon:
        outline.Append(mm(x), mm(y))
    board.Add(zone)


def add_inner_planes(board: pcbnew.BOARD) -> None:
    """In1.Cu ground and In2.Cu 3.3 V over the whole board; the module's rule area keeps both off the antenna."""
    _zone(board, GND, pcbnew.In1_Cu, outline_points())
    _zone(board, V3, pcbnew.In2_Cu, outline_points())


def add_outer_ground_pours(board: pcbnew.BOARD) -> None:
    _zone(board, GND, pcbnew.F_Cu, outline_points())
    _zone(board, GND, pcbnew.B_Cu, outline_points())


def fiducial_keepouts(parts: list[Part]) -> list[tuple[float, float, float, int]]:
    """(x, y, radius, layer) of the bare copper-free circle round each fiducial's mask opening."""
    radius = 1.0 + 0.1   # Fiducial_1mm_Mask2mm: 2.0 mm mask opening
    return [(*target(part)[:2], radius, pcbnew.B_Cu if part.side == BOTTOM else pcbnew.F_Cu)
            for part in parts if part.footprint_key == "FIDUCIAL"]


def add_fiducial_keepouts(board: pcbnew.BOARD, parts: list[Part]) -> None:
    for x, y, radius, layer in fiducial_keepouts(parts):
        area = pcbnew.ZONE(board)
        area.SetIsRuleArea(True)
        area.SetLayer(layer)
        area.SetDoNotAllowZoneFills(True)
        area.SetDoNotAllowTracks(True)
        area.SetDoNotAllowVias(True)
        area.SetDoNotAllowPads(False)
        area.SetDoNotAllowFootprints(False)
        outline = area.Outline()
        outline.NewOutline()
        for step in range(16):
            angle = math.radians(step * 22.5)
            outline.Append(mm(x + radius * math.cos(angle)), mm(y + radius * math.sin(angle)))
        board.Add(area)


def _rules(board: pcbnew.BOARD) -> None:
    settings = board.GetDesignSettings()
    settings.m_TrackMinWidth = mm(TRACK_WIDTH)
    settings.m_MinClearance = mm(CLEARANCE)
    settings.m_ViasMinSize = mm(VIA_DIAMETER)
    settings.m_MinThroughDrill = mm(VIA_DRILL)
    settings.m_CopperEdgeClearance = mm(EDGE_CLEARANCE)
    settings.m_HoleClearance = mm(0.2)
    default_class = settings.m_NetSettings.GetDefaultNetclass()
    default_class.SetTrackWidth(mm(TRACK_WIDTH))
    default_class.SetClearance(mm(CLEARANCE))
    default_class.SetViaDiameter(mm(VIA_DIAMETER))
    default_class.SetViaDrill(mm(VIA_DRILL))


# --- stack-up ----------------------------------------------------------------------------------------------

def stackup_thickness() -> float:
    return sum(thickness for _, _, thickness, _, _ in STACKUP)


def stackup_text() -> str:
    """The (stackup ...) block of the board setup. pcbnew's Python binding cannot build a stack-up, so it is
    written into the saved file; pcbnew keeps it on every later load and save."""
    assert abs(stackup_thickness() - PCB["thickness"]) <= STACKUP_TOLERANCE, \
        f"stack-up sums to {stackup_thickness():.4f} mm, pcb.thickness is {PCB['thickness']}"
    lines = ['\t\t(stackup', '\t\t\t(layer "F.SilkS" (type "Top Silk Screen"))',
             '\t\t\t(layer "F.Paste" (type "Top Solder Paste"))']
    for name, kind, thickness, material, epsilon in STACKUP:
        extra = f' (material "{material}") (epsilon_r {epsilon}) (loss_tangent 0.02)' if material else ""
        lines.append(f'\t\t\t(layer "{name}" (type "{kind}") (thickness {thickness}){extra})')
    lines += ['\t\t\t(layer "B.Paste" (type "Bottom Solder Paste"))',
              '\t\t\t(layer "B.SilkS" (type "Bottom Silk Screen"))',
              '\t\t\t(copper_finish "HAL lead-free")', '\t\t\t(dielectric_constraints no)', '\t\t)']
    return "\n".join(lines) + "\n"


def write_stackup(board_path: Path) -> None:
    """Puts the stack-up into a saved board file that has none."""
    text = board_path.read_text()
    assert "(stackup" not in text, f"{board_path.name} already has a stack-up"
    head = "\t(setup\n"
    assert text.count(head) == 1, f"{board_path.name}: no single setup block"
    board_path.write_text(text.replace(head, head + stackup_text(), 1))


def check_stackup(board: pcbnew.BOARD, board_path: Path) -> None:
    """The board loaded from board_path has a stack-up, and the file lists every STACKUP layer with its
    thickness, in order: pcbnew kept what write_stackup wrote."""
    assert board.GetDesignSettings().m_HasStackup, f"{board_path.name} has no stack-up"
    text = board_path.read_text()
    found = re.findall(r'\(layer "([^"]+)"\s*\(type "[^"]+"\)\s*\(thickness ([0-9.]+)\)', text)
    wanted = [(name, thickness) for name, _, thickness, _, _ in STACKUP]
    assert [(name, float(value)) for name, value in found] == wanted, f"{board_path.name} stack-up is {found}"


# --- silkscreen --------------------------------------------------------------------------------------------

def add_polarity_marks(board: pcbnew.BOARD, j3: pcbnew.FOOTPRINT) -> list[tuple[str, tuple[float, float]]]:
    """"+" and "-" past J3's signal pads, on the bottom silkscreen, mirrored to read from below."""
    pads = {number: _pads(j3, number)[0] for number, _ in POLARITY_MARKS}
    (x1, y1), (x2, y2) = pads["1"], pads["2"]
    length = math.dist(pads["1"], pads["2"])
    ux, uy = (x1 - x2) / length, (y1 - y2) / length   # along the pin row, from pin 2 toward pin 1
    tabs = _centre(_pads(j3, "MP"))
    vx, vy = -uy, ux                                   # along the pads, turned to point at the mounting tabs
    if (tabs[0] - x1) * vx + (tabs[1] - y1) * vy < 0:
        vx, vy = -vx, -vy
    box = next(pad for pad in j3.Pads() if pad.GetNumber() == "1").GetBoundingBox()
    pad_half = (pcbnew.ToMM(box.GetWidth()) * abs(ux) + pcbnew.ToMM(box.GetHeight()) * abs(uy)) / 2
    marks = []
    for number, label in POLARITY_MARKS:
        sign = 1 if number == "1" else -1
        along = sign * (pad_half + POLARITY_MARK_GAP)
        x = pads[number][0] + ux * along + vx * POLARITY_MARK_INSET
        y = pads[number][1] + uy * along + vy * POLARITY_MARK_INSET
        text = pcbnew.PCB_TEXT(board)
        text.SetText(label)
        text.SetLayer(pcbnew.B_SilkS)
        text.SetMirrored(True)
        text.SetTextSize(pcbnew.VECTOR2I(mm(POLARITY_MARK_SIZE), mm(POLARITY_MARK_SIZE)))
        text.SetTextThickness(mm(POLARITY_MARK_STROKE))
        text.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        text.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
        text.SetPosition(point(x, y))
        board.Add(text)
        marks.append((label, (round(x, 3), round(y, 3))))
    return marks


def check_polarity_marks(marks: list[tuple[str, tuple[float, float]]], j3: pcbnew.FOOTPRINT) -> None:
    """Each mark sits nearer its own pad than the other one: "+" at pin 1 (BAT_IN), "-" at pin 2 (GND)."""
    pin1, pin2 = _pads(j3, "1")[0], _pads(j3, "2")[0]
    by_label = dict(marks)
    assert math.dist(by_label["+"], pin1) < math.dist(by_label["+"], pin2), '"+" is not at J3 pin 1'
    assert math.dist(by_label["-"], pin2) < math.dist(by_label["-"], pin1), '"-" is not at J3 pin 2'
    assert dict(POLARITY_MARKS)["1"] == "+" and "BAT" in j3.FindPadByNumber("1").GetNetname(), \
        "J3 pin 1 is not the cell's positive line"


# --- placement self-checks ---------------------------------------------------------------------------------

def _pads(footprint: pcbnew.FOOTPRINT, number: str) -> list[tuple[float, float]]:
    return [pad_xy(pad) for pad in footprint.Pads() if pad.GetNumber() == number]


def _centre(points: list[tuple[float, float]]) -> tuple[float, float]:
    return sum(p[0] for p in points) / len(points), sum(p[1] for p in points) / len(points)


def _close(actual: tuple[float, float], expected: tuple[float, float]) -> bool:
    return math.dist(actual, expected) < POSITION_TOLERANCE


def rf_keepout_rect(footprint: pcbnew.FOOTPRINT) -> tuple[float, float, float, float]:
    """The module's RF rule area in board coordinates (left, top, right, bottom); asserts it covers all layers."""
    zones = [zone for zone in footprint.Zones() if zone.GetIsRuleArea()]
    assert len(zones) == 1, "U1 must carry exactly one rule area, the RF keep-out"
    zone = zones[0]
    for layer in (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu):
        assert zone.IsOnLayer(layer), f"RF keep-out misses {pcbnew.LayerName(layer)}"
    assert zone.GetDoNotAllowTracks() and zone.GetDoNotAllowVias() and zone.GetDoNotAllowZoneFills(), \
        "RF keep-out lets copper in"
    box = zone.GetBoundingBox()
    return tuple(round(pcbnew.ToMM(v), 3) for v in (box.GetLeft(), box.GetTop(), box.GetRight(), box.GetBottom()))


def check_placement(placed: dict[str, pcbnew.FOOTPRINT], parts: list[Part]) -> None:
    by_ref = {part.ref: part for part in parts}
    for ref, footprint in placed.items():
        bottom = by_ref[ref].side == BOTTOM
        assert footprint.IsFlipped() == bottom, f"{ref} is on the wrong face (D9)"

    module, keepout = BOARD_SPEC["module"], BOARD_SPEC["module"]["keepout"]
    u1 = placed["U1"]
    pads = [pad_xy(pad) for pad in u1.Pads()]
    right_edge = PCB["x1"]
    # Antenna toward +X: the pad field sits at the left end, the strip between it and the right edge.
    first_column = max(x for x, _ in pads) + footprints_pad_half()
    assert abs(first_column - (right_edge - keepout["depth"])) < POSITION_TOLERANCE, \
        f"module pad column at X {first_column:.3f}, keep-out depth wants {right_edge - keepout['depth']:.3f}"
    left, top, right, bottom = rf_keepout_rect(u1)
    assert abs(right - right_edge) < POSITION_TOLERANCE and abs(left - (right_edge - keepout["depth"])) < 0.01, \
        f"RF keep-out X {left}..{right} is not the {keepout['depth']} mm from the right edge"
    assert abs((bottom - top) - keepout["length"]) < 0.01 and abs((top + bottom) / 2 - module["centre_y"]) < 0.01, \
        "RF keep-out length or centre differ from board.toml"
    body_right = pcbnew.ToMM(u1.GetPosition().x) + module["length"] / 2
    assert abs(right_edge - body_right - module["antenna_inset"]) < POSITION_TOLERANCE, "antenna inset is wrong"

    connector = BOARD_SPEC["display"]["connector"]
    j2 = placed["J2"]
    pin1, pin24 = _pads(j2, "1")[0], _pads(j2, "24")[0]
    assert pin1[0] > pin24[0] and abs(pin1[0] - connector["pin1_x"]) < 1.5, "J2 contact 1 is not at the +X end"
    mounts = _centre(_pads(j2, "MP"))
    assert mounts[1] > pin1[1] and pin1[1] > connector["y_back"], "J2 FPC entry does not face +Y"

    key = BOARD_SPEC["keys"]
    for ref, (dx, dy) in (("1", key["footprint"]["socket_pads"][1]), ("2", key["footprint"]["socket_pads"][0])):
        expected = (key["first_x"] + dx, key["first_y"] + dy)
        assert _close(_pads(placed["SW1"], ref)[0], expected), f"SW1 socket pad {ref} is mirrored"

    j1 = placed["J1"]
    usb = BOARD_SPEC["usb"]
    a6 = _pads(j1, "A6")[0]
    assert abs(max(y for _, y in (pad_xy(p) for p in j1.Pads() if p.GetNumber() == "A1")) + 0.55
               - usb["signal_pad_end_y"]) < POSITION_TOLERANCE, "J1 signal pads do not end at usb.signal_pad_end_y"
    assert a6[1] > pcbnew.ToMM(j1.GetPosition().y), "USB-C mouth faces into the board"
    assert abs(pcbnew.ToMM(j1.GetPosition().y) - usb["front_y"]) < POSITION_TOLERANCE, "J1 is off the edge line"

    j3 = placed["J3"]
    signal, tabs = _centre(_pads(j3, "1") + _pads(j3, "2")), _centre(_pads(j3, "MP"))
    assert tabs[0] < signal[0] and abs(tabs[1] - signal[1]) < 0.01, "J3 mouth does not face -X (battery.connector)"

    sw18 = placed["SW18"]
    switch = BOARD_SPEC["power_switch"]
    assert min(y for _, y in (_pads(sw18, n)[0] for n in "123")) > switch["body_y0"] + switch["body"][1] / 2, \
        "SW18 pads are on the actuator side; the actuator must point out of the rear edge"

    for ref in ("U6",):
        x, y = MOVED[ref][0]
        u6_pads = [pad_xy(p) for p in placed[ref].Pads()]
        j1_pads = [pad_xy(p) for p in j1.Pads() if p.GetNumber()[0] in "AB"]
        gap = min(math.dist(a, b) for a in u6_pads for b in j1_pads)
        assert gap <= BOARD_SPEC["power"]["esd_to_connector_max"], f"{ref} {gap:.2f} mm from J1's pads"
        assert _close(pcbnew_xy(placed[ref]), (x, y)), f"{ref} is not at its moved spot"

    battery = BOARD_SPEC["battery"]["connector"]
    fab = [item.GetBoundingBox() for item in j3.GraphicalItems() if item.GetLayer() == pcbnew.B_Fab
           and item.GetClass() == "PCB_SHAPE"]
    body = (pcbnew.ToMM(min(b.GetLeft() for b in fab) + max(b.GetRight() for b in fab)) / 2,
            pcbnew.ToMM(min(b.GetTop() for b in fab) + max(b.GetBottom() for b in fab)) / 2)
    assert math.dist(body, (battery["x"], battery["y"])) < 0.06, f"J3 body centre {body}, board.toml has it elsewhere"

    _check_hole_keepouts(placed, by_ref)
    _check_swd_low_zone(placed, by_ref)

    bay_x = right_edge - BOARD_SPEC["rf_bay"]["inset"]
    bay_y0 = module["centre_y"] - BOARD_SPEC["rf_bay"]["length"] / 2
    bay_y1 = module["centre_y"] + BOARD_SPEC["rf_bay"]["length"] / 2
    for ref, footprint in placed.items():
        if ref == "U1":
            continue
        box = footprint.GetBoundingBox(False)
        inside = (pcbnew.ToMM(box.GetRight()) > bay_x and pcbnew.ToMM(box.GetBottom()) > bay_y0
                  and pcbnew.ToMM(box.GetTop()) < bay_y1)
        assert not inside, f"{ref} reaches into the RF bay (X > {bay_x}, Y {bay_y0} to {bay_y1})"


def _check_hole_keepouts(placed: dict[str, pcbnew.FOOTPRINT], by_ref: dict[str, Part]) -> None:
    """No other part's courtyard inside a hole keep-out, per face. A switch's top-face square is the empty
    key keep-out, not a part, and may overlap a hole keep-out."""
    for ref, hole in placed.items():
        if by_ref[ref].value not in HOLE_KEEPOUT:
            continue
        centre = hole.GetPosition()
        for layer, diameter in zip((pcbnew.F_CrtYd, pcbnew.B_CrtYd), HOLE_KEEPOUT[by_ref[ref].value], strict=True):
            for other_ref, other in placed.items():
                if other_ref == ref or (by_ref[other_ref].footprint_key == "CHOC_HOTSWAP" and layer == pcbnew.F_CrtYd):
                    continue
                other.BuildCourtyardCaches()
                courtyard = other.GetCourtyard(layer)
                if courtyard.OutlineCount() and courtyard.Collide(centre, mm(diameter / 2)):
                    raise AssertionError(f"{other_ref} is inside the {diameter} mm keep-out of {ref} "
                                         f"on {pcbnew.LayerName(layer)}")


def _check_swd_low_zone(placed: dict[str, pcbnew.FOOTPRINT], by_ref: dict[str, Part]) -> None:
    """usb-io 6.5: no bottom part taller than 1.0 mm within swd.low_zone of the TC2030 pad field."""
    zone = BOARD_SPEC["swd"]["low_zone"]
    j4 = placed["J4"]
    j4.BuildCourtyardCaches()
    field = j4.GetCourtyard(pcbnew.B_CrtYd)
    for ref, footprint in placed.items():
        part = by_ref[ref]
        if ref == "J4" or part.side != BOTTOM or part.footprint_key in circuit.NOT_A_PART:
            continue
        height = max((solid.z_top for solid in models.solids(part.footprint_key, models.load_footprint(
            part.footprint_key))), default=0.0)
        if height <= 1.0:
            continue
        footprint.BuildCourtyardCaches()
        courtyard = footprint.GetCourtyard(pcbnew.B_CrtYd)
        for index in range(courtyard.OutlineCount()):
            outline = courtyard.Outline(index)
            for k in range(outline.PointCount()):
                corner = outline.CPoint(k)
                assert not field.Collide(corner, mm(zone)), f"{ref} ({height} mm) is within {zone} mm of J4"


def pcbnew_xy(footprint: pcbnew.FOOTPRINT) -> tuple[float, float]:
    position = footprint.GetPosition()
    return pcbnew.ToMM(position.x), pcbnew.ToMM(position.y)


def footprints_pad_half() -> float:
    import footprints
    return footprints.BMD340_PAD / 2


def build_board(board_path: Path, open_pin_nets: dict[str, str]) -> pcbnew.BOARD:
    """open_pin_nets: "U1.21" -> the net name KiCad's schematic netlist gives that open pin."""
    parts = circuit.all_parts()
    circuit.check_netlist(parts)
    board = pcbnew.NewBoard(str(board_path))
    board.SetCopperLayerCount(PCB["layers"])
    _rules(board)
    _outline(board)
    placed = {part.ref: _place(board, part, open_pin_nets) for part in parts}
    check_placement(placed, parts)
    check_polarity_marks(add_polarity_marks(board, placed["J3"]), placed["J3"])
    add_inner_planes(board)
    add_fiducial_keepouts(board, parts)
    return board
