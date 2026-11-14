"""The board contract (`board.toml`) and the dimensions that belong to the case alone.

Frames: `board.toml` puts the origin at the rear-left outer corner of the body, X to the right, Y toward the
front (the user) and Z up from the deck (the top face of the top shell), negative downward. The model keeps X
and Z and flips Y (model Y = -board Y), so the frame stays right-handed and the rear of the case points to +Y.
Every helper in `solids.py` takes board coordinates.

Tags on the case-only values: "enclosure 6.4" is section 6.4 of research/components/enclosure-manufacturing.md
(the same for keys, rotary-buttons, display, usb-io, power, mcu-radio); "D30" is an entry in docs/decisions.md;
MEASURE is a value from a drawing or a photo, not a caliper; "guess" is chosen with nothing to check it against.
"""

from dataclasses import dataclass, field
from math import atan, degrees, radians, tan
from pathlib import Path
from types import SimpleNamespace
import tomllib

BOARD_TOML = Path(__file__).resolve().parents[2] / "board.toml"

PRINT = "print"
CNC = "cnc"
VARIANTS = (CNC, PRINT)

Span = tuple[tuple[float, float], tuple[float, float]]  # ((x0, x1), (y0, y1)) in board coordinates


def _namespace(value):
    if isinstance(value, dict):
        return SimpleNamespace(**{key: _namespace(item) for key, item in value.items()})
    if isinstance(value, list):
        return [_namespace(item) for item in value]
    return value


def load_board() -> SimpleNamespace:
    with BOARD_TOML.open("rb") as toml_file:
        return _namespace(tomllib.load(toml_file))


BOARD = load_board()


@dataclass(frozen=True)
class Case:
    """Case-only dimensions in millimetres. Everything that the PCB, the firmware or check_spec also needs lives
    in board.toml; these numbers are read by the case alone."""

    # JLCCNC rules (enclosure 5).
    corner_rule_slope: float = 0.1  # internal corner radius R >= depth / 10 + 0.5
    corner_rule_offset: float = 0.5
    table_radius: float = 1.5  # "R 1.5 or more in pockets up to 10 mm deep" (D29); waivers listed in checks.py
    small_tool: float = 2.0  # the smallest end mill the drawings call for: switch dog-bones, display pocket (D33)
    shallow_depth: float = 3.0  # R 0.5 is allowed only in pockets this shallow or shallower (enclosure 5)
    metal_wall_absolute: float = 0.5  # JLCCNC absolute minimum metal wall (enclosure 5)
    drill_point_angle: float = 118.0
    drill_point_margin: float = 2.0  # metal beyond a tap-drill point (enclosure 5)
    thread_tip_margin: float = 0.4  # screw tip short of the last full thread (enclosure 6.4)
    length_tolerance: float = 0.15  # screw length, assumed (enclosure 6.4)

    # Screws. DIN 7991 heads: M2 d2 4.0, k 1.2 (enclosure 5, boltsparts read 2026-11-13); M1.6 d2 3.0 (D30),
    # k 0.96 (DIN 7991 table, not re-read). Smallest head allowed by the standard taken as 0.3 under d2 (guess),
    # which sinks the head 0.15 deeper, as enclosure 6.4 assumes.
    m2_pitch: float = 0.4
    m2_tap_drill: float = 1.6
    m2_clearance: float = 2.2
    m2_head: float = 4.0
    m2_head_height: float = 1.2
    m16_pitch: float = 0.35
    m16_tap_drill: float = 1.25  # D30
    m16_head: float = 3.0
    m16_head_height: float = 0.96
    head_undersize: float = 0.3
    k_length: float = 5.0  # M1.6 x 5 DIN 7991 (D30)
    c_length: float = 6.0  # M2 x 6 DIN 7991 (enclosure 6.4)
    g_length: float = 4.0  # M2 x 4 ISO 7045 (enclosure 6.4, D6)
    g_head_height: float = 1.6  # ISO 7045 M2 k (enclosure 6.4)
    # Tapped depths. K: recomputed for M1.6 x 0.35 (D30 asks the case owner): 3 x D = 4.8 mm of full thread,
    # D/2 = 0.8 mm unthreaded to the drill shoulder. C: enclosure 6.4, D/2 = 1.0 unthreaded.
    # G: proposed answer to the D6 thread margin, not yet confirmed by the owner. A plug tap with D/2 run cannot
    # meet both enclosure 6.4 rules in the G post: 2.7 mm of thread leaves the M2 x 4 tip 0.15 mm from the last
    # full thread (rule 0.4), and 3.0 mm leaves 1.72 mm of metal past the drill point (rule 2.0). A bottoming
    # tap with 0.5 mm unthreaded run and 3.0 mm of full thread meets both, and departs from the enclosure 5
    # "D/2 unthreaded" guideline in this one hole pair. The shop must confirm a bottoming tap whose chamfer is
    # 0.5 mm (1.25 pitches) or shorter.
    k_full_thread: float = 4.8
    c_full_thread: float = 4.8
    g_full_thread: float = 3.0
    k_thread_run: float = 0.8
    c_thread_run: float = 1.0
    g_thread_run: float = 0.5
    c_pad_diameter: float = 6.0  # C1: raised floor pad that keeps the 2.0 mm local floor (enclosure 6.4). guess
    c_post_well: float = 4.2  # C2: well in the floor round the post end at Z -11.65. guess (0.3 per side)
    reset_pad_diameter: float = 4.0  # floor pad under the reset button, top at reset.floor_top_z. guess

    # Switch plate: dog-bone reliefs for a 2.0 mm tool (enclosure 5: relief 2.1).
    dogbone_diameter: float = 2.1
    web_window_radius: float = 1.0  # display web window corners; the mask window gets the same radius (guess)
    lens_mask_radius: float = 1.0
    plinth_chamfer: float = 0.5  # rotary-buttons 6.3 (judgement there)
    usb_pocket_radius: float = 1.0  # T-bones of a 2.0 mm tool at the front corners of the 2.9 mm wide pocket
    usb_skin_cnc: float = 0.6  # usb-io 6.2 item 3
    rf_insert_pocket_radius: float = 1.0  # POM insert, side pocket corners. guess
    rf_insert_skin: float = 1.45  # enclosure 7.2 item 4
    # Length tolerances (upper, lower) of the insert bar and of the slot it slides into. The record gives 0.10
    # total play; ISO 2768-m (+/-0.2) could make the bar longer than the slot. Proposal of
    # cad/production/jlccnc/ORDER_NOTES.md, not a tested fit.
    rf_insert_length_tolerance: tuple[float, float] = (0.0, 0.10)
    rf_slot_length_tolerance: tuple[float, float] = (0.10, 0.0)
    rf_trench_width: float = 3.0  # floor trench along the slot's inner side, wide enough for a 3 mm tool

    # FDM variant (enclosure 8.2, D27, D30).
    print_lip: float = 1.0  # 5 layers; the coupon decides between 1.0 and 1.2 (keys 6.2)
    print_recess: float = 1.2  # 6 layers (display 7)
    print_web: float = 0.8  # 4 layers
    print_k_screw_length: float = 8.0  # M1.6 x 8 self-tapping (D30)
    print_k_pilot: float = 1.3  # M1.6 self-tap pilot in PETG. guess (coupon)
    print_k_clearance: float = 1.8  # board holes.k.clearance_hole
    print_k_boss: float = 6.0  # enclosure 8.2
    print_k_boss_top_z: float = -8.10  # enclosure 8.2: the boss stays under the PCB bottom
    print_k_post_top_z: float = -5.05  # enclosure 8.2
    print_insert_hole: float = 3.2  # CNC Kitchen M2 x 3 (enclosure 6.3; board case.fdm_insert_hole)
    print_insert_depth: float = 3.5  # enclosure 8.2
    print_insert_length: float = 3.0
    print_c_screw_length: float = 10.0  # M2 x 10 DIN 7991, both C screws seat at Z -12.0 in print
    print_c_seat_z: float = -12.2  # both C seats spot-faced to this Z in print, so one M2 x 10 fits both
    print_c_boss: float = 6.0  # under the PCB, like the K boss
    print_g_spacer: tuple[float, float] = (4.6, 2.3)  # outer, inner; 1.2 tall (enclosure 8.2). guess on the bore
    print_support_rib: float = 0.6  # break-away ribs under the display web front ledge (print top shell)
    print_support_x: tuple[float, float] = (96.0, 105.6)  # rib centres: spans of 8.6 to 9.6 mm. guess
    print_skin: float = 0.2  # one layer closes a hole in a ceiling; cut out after printing (macropad practice)
    print_supported_zones: str = "rear slope (Y 0 to apex) and both flank scoops"

    # Knob (rotary-buttons 6.5). CNC turned; the print variant follows the FDM paragraph there.
    knob_counterbore: tuple[float, float] = (8.40, 1.20)
    knob_relief: tuple[float, float] = (6.05, 2.20)  # diameter, top above the rim
    knob_bore: tuple[float, float, float] = (6.05, 4.55, 6.90)  # diameter, across the flat, top above the rim
    knob_top_radius: float = 1.25
    knob_set_screw_z: float = 3.00  # above the rim, M2 tapped, toward the rear
    knob_set_screw_thread: str = "M2x0.4-6H"
    knob_set_screw: str = "M2 x 3 ISO 4029 cup point"  # rotary-buttons 6.5
    knob_bore_tolerance: float = 0.03  # D-bore, its flat and the round relief, +0.03/0 after anodise (rotary-buttons 6.5)
    knob_counterbore_tolerance: tuple[float, float] = (0.10, 0.05)  # diameter, depth; each +x/0 (rotary-buttons 6.5)
    print_knob_bore: tuple[float, float] = (6.20, 4.70)
    print_knob_rib: tuple[float, float, float] = (5.90, 0.15, 1.0)  # ribs reach Ø5.90; flat rib 0.15; width 1.0
    shim: float = 1.10  # BOARD.knobs.shim

    # Button cap (rotary-buttons 6.6).
    button_top: float = 10.30
    button_crown: float = 0.3
    button_flange_thickness: float = 0.80
    button_nub: float = 2.5
    # Flange top under the counterbore ceiling at nominal heights. rotary-buttons 6.6 gives 0.25, which the
    # tolerance stack below can close and so preload the plunger; 0.60 leaves 0.10 at the worst case. The flange
    # moves down on the cap; the counterbore and the cap top stay where board.toml puts them.
    button_flange_gap: float = 0.60
    button_switch_tolerance: float = 0.2  # B3FS-1000P height 3.1 +/-0.2 (rotary-buttons, part table)
    button_cap_tolerance: float = 0.2  # resin, +/-0.2 (keys 6.5)
    counterbore_depth_tolerance: float = 0.1  # 3.5 mm counterbore depth under ISO 2768-m
    # Encoder pockets: depth from the split face called +0.10/0 on the drawing, so the ceiling is never lower
    # than board.toml plinth.pocket_ceiling_z over the encoder body at its maximum height.
    encoder_pocket_depth_tolerance: tuple[float, float] = (0.10, 0.0)
    # Battery pocket and relief rims: power 14 rule 3, radius at least 0.5 mm on every pocket edge.
    cell_rim_radius: float = 0.5

    # Keycap (keys 6.5). Our own low square dished cap, printed in resin.
    keycap_dish: tuple[float, float, float] = (12.0, 1.7, 0.6)  # square, corner radius, depth
    keycap_base_radius: float = 1.0  # guess
    keycap_top_radius: float = 1.5  # guess
    keycap_edge_radius: float = 0.5
    keycap_skirt_inner: float = 16.0
    keycap_inner_top: float = 14.4  # inner opening at the roof; keeps a 1.0 mm side wall under the taper. guess
    keycap_post: float = 5.20
    keycap_slot: tuple[float, float] = (4.10, 1.35)  # cross slot length, width (coupon 1.30 to 1.45)
    keycap_post_length: float = 3.0  # guess
    keycap_seat: float = 6.80
    keycap_stem_top: float = 2.40
    keycap_roof_relief: float = 0.50

    # Switch insertion jig (D26).
    jig_plate: tuple[float, float] = (-16.0, -14.0)  # base plate Z range, under the battery connector (Z -13.30)
    jig_rib: float = 3.0  # square rib under each socket barrel. guess
    jig_margin: float = 0.5  # rib inside the socket zone
    jig_rim_width: float = 2.0  # rim under the top-shell split face, inside the outline (guess)
    jig_rim_notch_margin: float = 0.5  # rim notches round the USB-C and switch notches, per side (guess)

    # Reference shapes of bought parts (fit only).
    encoder_collar: tuple[float, float] = (7.3, 1.9)  # diameter guess (rotary-buttons 6.3), top nominal
    encoder_shaft: tuple[float, float, float] = (6.0, 4.5, 8.8)  # diameter, across the flat, tip Z
    encoder_flat_z: float = 3.8
    switch_upper: float = 13.95  # housing above the flange: taken as the body size (guess)
    switch_flange_top: float = -3.20  # keys 6.3
    switch_housing_top: float = -0.90
    switch_collar: tuple[float, float, float] = (8.4, 7.7, -0.50)  # outer, inner, rim Z (keys 6.5, likely)
    switch_stem: tuple[float, float] = (6.5, 5.5)  # stem column outer, bore (keys 6.5)
    switch_cross: tuple[float, float] = (4.00, 1.30)  # Kailh MX cross arms
    switch_travel: float = 2.80
    switch_travel_tolerance: float = 0.25
    socket_depth: float = 1.85  # keys 6.3
    foam_pad: tuple[float, float] = (12.0, 10.0)  # display foam, plan (display 7), rear of the module
    lens_tape: float = 0.13  # display 6.4
    plug_overmold: tuple[float, float] = (12.0, 6.5)  # USB-C plug overmold, a common size. guess
    display_active_area: float = 23.4  # square, display 6.1
    display_glass_depth: float = 0.35  # pixels under the module's top glass. guess, for the parallax estimate
    viewing_angles: tuple[float, ...] = (30.0, 45.0)  # degrees from the deck normal, a seated user. guess
    pcb_step_thickness_tolerance: float = 0.1  # KiCad exports the board body without copper and mask

    # Laser mark on the underside (enclosure 5: on the outer underside by laser).
    mark_text: tuple[str, str] = ("worxpad", "rev A")
    mark_size: float = 5.0
    mark_centre: tuple[float, float] = (64.2, 66.0)

    @property
    def drill_point_length(self) -> float:
        return 1.0 / tan(radians(self.drill_point_angle / 2))  # per mm of diameter, halved below


CASE = Case()


# ---------------------------------------------------------------------------------------------------------
# Positions from board.toml
# ---------------------------------------------------------------------------------------------------------
def key_centres() -> list[tuple[float, float]]:
    keys = BOARD.keys
    return [(keys.first_x + column * keys.pitch, keys.first_y + row * keys.pitch)
            for row in range(keys.rows) for column in range(keys.columns)]


def encoder_centres() -> list[tuple[float, float]]:
    return [(BOARD.encoders.left.x, BOARD.encoders.left.y), (BOARD.encoders.right.x, BOARD.encoders.right.y)]


def button_centres() -> list[tuple[float, float]]:
    return [(BOARD.buttons.left.x, BOARD.buttons.left.y), (BOARD.buttons.right.x, BOARD.buttons.right.y)]


def body_span() -> Span:
    return (0.0, BOARD.body.width), (0.0, BOARD.body.depth)


def inner_span() -> Span:
    wall = BOARD.body.wall
    return (wall, BOARD.body.width - wall), (wall, BOARD.body.depth - wall)


def well_span() -> Span:
    keys = BOARD.keys
    return (keys.well_x0, keys.well_x1), (keys.well_y0, keys.well_y1)


def grown(span: Span, by: float) -> Span:
    (x0, x1), (y0, y1) = span
    return (x0 - by, x1 + by), (y0 - by, y1 + by)


def centred(centre: tuple[float, float], size: tuple[float, float]) -> Span:
    return (centre[0] - size[0] / 2, centre[0] + size[0] / 2), (centre[1] - size[1] / 2, centre[1] + size[1] / 2)


def lens_span() -> Span:
    lens = BOARD.display.lens
    return (lens.x0, lens.x1), (lens.y0, lens.y1)


def lens_centre() -> tuple[float, float]:
    (x0, x1), (y0, y1) = lens_span()
    return (x0 + x1) / 2, (y0 + y1) / 2


def display_pocket_span() -> Span:
    pocket = BOARD.display.pocket
    return (pocket.x0, pocket.x1), (pocket.y0, pocket.bend_y1)


def module_span() -> Span:
    module, pcb = BOARD.module, BOARD.pcb
    x1 = pcb.x1 - module.antenna_inset
    return (x1 - module.length, x1), (module.centre_y - module.width / 2, module.centre_y + module.width / 2)


def rf_bay_span() -> Span:
    """The RF bay in plan, inside the inner wall (D11: the outer wall above the slot stays metal)."""
    bay, module = BOARD.rf_bay, BOARD.module
    return ((BOARD.pcb.x1 - bay.inset, BOARD.body.width - BOARD.body.wall),
            (module.centre_y - bay.length / 2, module.centre_y + bay.length / 2))


def keepout_span() -> Span:
    keepout, module = BOARD.module.keepout, BOARD.module
    return ((BOARD.pcb.x1 - keepout.depth, BOARD.pcb.x1),
            (module.centre_y - keepout.length / 2, module.centre_y + keepout.length / 2))


def battery_pocket_span() -> Span:
    return tuple(BOARD.battery.pocket_x), tuple(BOARD.battery.pocket_y)


def cell_span() -> Span:
    battery = BOARD.battery
    x0, y0 = battery.pocket_x[0] + battery.pocket_clearance, battery.pocket_y[0] + battery.pocket_clearance
    return (x0, x0 + battery.cell_size[0]), (y0, y0 + battery.cell_size[1])


def cell_z() -> tuple[float, float]:
    """The cell swollen by 10 %: top under the insulation sheet, as check_spec places it."""
    top = BOARD.stack.key_field_floor_top - BOARD.battery.insulation
    return top - BOARD.battery.cell_size[2] - BOARD.battery.swelling, top


def scoop_spans() -> list[Span]:
    scoops, width = BOARD.wedge.scoops, BOARD.body.width
    return [((0.0, scoops.width), (0.0, scoops.end_y)), ((width - scoops.width, width), (0.0, scoops.end_y))]


# ---------------------------------------------------------------------------------------------------------
# Underside
# ---------------------------------------------------------------------------------------------------------
def thickness_at(y: float) -> float:
    """Deck to underside on the wedge planes (no scoops), as tools/check_spec.py computes it."""
    wedge, depth = BOARD.wedge, BOARD.body.depth
    if y <= wedge.apex_y:
        return wedge.rear_height + (wedge.apex_height - wedge.rear_height) * y / wedge.apex_y
    return wedge.apex_height + (wedge.front_height - wedge.apex_height) * (y - wedge.apex_y) / (depth - wedge.apex_y)


def ramp_angle() -> float:
    """Degrees between the ramp plane and the deck."""
    wedge = BOARD.wedge
    return degrees(atan((wedge.apex_height - wedge.front_height) / (BOARD.body.depth - wedge.apex_y)))


def scoop_fade_start() -> float:
    """Y where a flank scoop's flat ends: from there a 45 degree face reaches the ramp at scoops.end_y."""
    scoops = BOARD.wedge.scoops
    return scoops.end_y - (thickness_at(scoops.end_y) + scoops.underside_z)


# ---------------------------------------------------------------------------------------------------------
# Screw holes
# ---------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class TappedHole:
    """A tapped blind hole as the drawing calls it out, and the screw that goes in it.

    `mouth_z` is where the screw enters the thread (post end or face), `direction` +1 when the hole runs upward
    from the mouth (screw from below), -1 when it runs downward (screw from above)."""

    name: str
    shell: str
    positions: list[tuple[float, float]]
    thread: str
    pitch: float
    major: float
    tap_drill: float
    mouth_z: list[float]
    direction: int
    full_thread: float
    run: float  # unthreaded length from the last full thread to the drill shoulder
    tap: str
    screw: str
    head_top_z: list[tuple[float, float]]  # range of the head top (or the bearing face) per position
    length: float
    notes: list[str] = field(default_factory=list)

    def thread_end_z(self, index: int) -> float:
        return self.mouth_z[index] + self.direction * self.full_thread

    def shoulder_z(self, index: int) -> float:
        return self.thread_end_z(index) + self.direction * self.run

    def point_z(self, index: int) -> float:
        return self.shoulder_z(index) + self.direction * self.tap_drill / 2 * CASE.drill_point_length

    def tip_z(self, index: int) -> tuple[float, float]:
        """Shortest and longest reach of the screw tip, with the head seat range and the length tolerance."""
        tops = self.head_top_z[index]
        reach = [top + self.direction * (self.length + sign * CASE.length_tolerance) for top in tops
                 for sign in (-1, 1)]
        return (min(reach), max(reach)) if self.direction > 0 else (max(reach), min(reach))

    def engagement(self, index: int) -> tuple[float, float]:
        short, long = self.tip_z(index)
        return abs(short - self.mouth_z[index]), abs(long - self.mouth_z[index])

    def tip_margin(self, index: int) -> float:
        """Distance from the deepest screw tip to the last full thread."""
        return abs(self.thread_end_z(index) - self.tip_z(index)[1])


def _countersunk_head_tops(surface_z: float, countersink: float, head: float, direction: int) -> tuple[float, float]:
    """Head top range in a 90 degree countersink: flush minus (countersink - head) / 2, deeper for a small head."""
    sink = (countersink - head) / 2
    deepest = sink + CASE.head_undersize / 2
    return surface_z + direction * sink, surface_z + direction * deepest


def k_holes() -> TappedHole:
    k = BOARD.holes.k
    tops = _countersunk_head_tops(BOARD.stack.plate_top, k.countersink, CASE.m16_head, -1)
    return TappedHole(
        "K", "bottom shell", [tuple(p) for p in k.positions], "M1.6x0.35-6H", CASE.m16_pitch, 1.6, CASE.m16_tap_drill,
        [k.post_top_z] * 4, -1, CASE.k_full_thread, CASE.k_thread_run, "plug tap", k.screw, [tops] * 4, CASE.k_length,
        ["thread and drill recomputed for M1.6 (D30)"])


def c_holes() -> TappedHole:
    c = BOARD.holes.c
    seats = []
    for index, (x, y) in enumerate(c.positions):
        surface = -thickness_at(y) if index != c.spot_face.index else c.spot_face.floor_z
        if index != c.spot_face.index and any(x0 <= x <= x1 and y0 <= y <= y1 for (x0, x1), (y0, y1) in scoop_spans()):
            surface = BOARD.wedge.scoops.underside_z
        seats.append(_countersunk_head_tops(surface, c.countersink, CASE.m2_head, 1))
    return TappedHole(
        "C", "top shell", [tuple(p) for p in c.positions], "M2x0.4-6H", CASE.m2_pitch, 2.0, CASE.m2_tap_drill,
        list(c.post_bottom_z), 1, CASE.c_full_thread, CASE.c_thread_run, "plug tap", c.screw, seats, CASE.c_length)


def g_holes() -> TappedHole:
    g = BOARD.holes.g
    bearing = BOARD.pcb.bottom_z  # the pan head bears on the bottom GND ring
    return TappedHole(
        "G", "top shell", [tuple(p) for p in g.positions], "M2x0.4-6H", CASE.m2_pitch, 2.0, CASE.m2_tap_drill,
        [g.post_bottom_z] * 2, 1, CASE.g_full_thread, CASE.g_thread_run, "bottoming tap", g.screw,
        [(bearing, bearing)] * 2, CASE.g_length,
        ["post end face bare after anodise (laser-cleared or face-milled), case ground (D6)",
         "bottoming tap, 0.5 unthreaded run: proposed for D6, owner to confirm"])


def c_seat_surface(index: int) -> float:
    """Z of the face the C countersink is cut into: the scoop, the ramp, or the C2 spot-face floor."""
    return c_holes().head_top_z[index][0] - (BOARD.holes.c.countersink - CASE.m2_head) / 2


@dataclass(frozen=True)
class Limits:
    """Limits the checks hold the model to. Each names its source; "guess" where none exists."""

    clash_volume: float = 0.05  # mm^3 of shared volume that counts as a clash (macropad)
    cnc_tool: float = CASE.small_tool  # the tool run uses the smallest end mill on the drawings
    metal_wall: float = BOARD.case.min_metal_wall  # JLCCNC recommended (enclosure 5)
    metal_wall_absolute: float = CASE.metal_wall_absolute  # JLCCNC absolute (enclosure 5)
    floor: float = BOARD.case.min_floor  # aluminium floor under a pocket (enclosure 5, power 5.2)
    tool_reach: float = 5.0  # depth over tool diameter; above 5 x needs special tools (enclosure 5)
    fdm_wall: float = 0.8  # two passes of a 0.4 mm nozzle (macropad); JLC3DP plastic minimum is 1.0 to 1.5
    bridge: float = BOARD.case.fdm_bridge_max
    cantilever: float = 1.5  # macropad, a guess: about three 0.45 mm lines
    bed: float = BOARD.case.bed
    bed_contact: float = 100.0  # mm^2 on the bed (macropad)
    pcb_gap: float = BOARD.case.pcb_gap_min
    engagement_k: float = 1.5  # x D; steel screw in tapped aluminium, a common rule (guess)
    engagement_c: float = 1.5
    engagement_g: float = 1.0  # x D; G only holds the PCB (enclosure 6.4: 1.2 x D)
    print_self_tap: float = 2.0  # x D into the PETG boss, a guess
    print_insert_engagement: float = 2.5  # mm in the M2 x 3 insert (enclosure 8.2)
    print_tip_to_hole_end: float = 0.1  # mm; the screw must not bottom in the insert hole (guess)
    keycap_gap: float = 0.45  # neighbouring caps at the resin tolerance (keys 6.5)
    knob_rim_pressed: float = 0.30  # rotary-buttons 6.3: 0.25 worst plus the 0.05 shim tolerance
    knob_collar_pressed: float = 0.75  # collar 0.6 over nominal at its maximum, plus 0.15 plinth stack (rotary-buttons 6.3)
    knob_collar_radial: float = 0.5  # counterbore round the collar; rotary-buttons 6.3 gives about 0.55 (guess)
    post_in_pcb_hole: float = 0.15  # Ø3.6 post in a Ø4.0 NPTH: 0.2 drawn, 0.05 for drill position (guess)
    pressed_cap_to_shell: float = 0.30  # keys 6.3 item 3: 0.3 mm margin over anything on the plate
    pressed_cap_to_switch: float = 0.30  # keys 6.5: 0.35 at worst-case travel over the collar rim
    module_to_web: float = 0.10  # the tape frame (display 6.4, D10)
    lens_fit: float = 0.10  # per side (conventions 3.6)
    jig_ribs_in_zone: float = CASE.jig_margin
    jig_centroid_margin: float = 5.0  # mm from the assembly centroid to the edge of the jig support (guess)
    button_worst_gap: float = 0.10  # flange to counterbore ceiling at the worst tolerance stack (guess margin)
    encoder_to_ceiling: float = 0.0  # encoder body at its maximum to the shallowest pocket ceiling
    cell_rim_tessellation: float = 0.02  # mesh error allowed on the rim setback measurement (guess)


LIMITS = Limits()
