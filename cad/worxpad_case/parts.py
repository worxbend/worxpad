"""The two shells, CNC and FDM variants, built from board.toml.

Top shell: deck, key well with the integrated Choc V2 plate lip, lens recess and web, display, encoder, button
and RF pockets from below, knob plinth, C and G posts (CNC) or heat-set insert holes (FDM).
Bottom shell: tray with the wedge, flank scoops, cavity floors, battery pocket and relief, RF bay floor pocket,
RF window slot with key reliefs (CNC), USB-C and switch notches, reset pinhole, foot pockets, K posts and the C
countersinks.
"""

from math import atan, degrees, sqrt

from build123d import Align, Axis, Cylinder, GeomType, Part, Plane, Polygon, Pos, Rot, chamfer, extrude, fillet

from .solids import CUT_OVERSHOOT, box, countersink, cylinder, disc, drill, millable, rectangle, rounded, slab
from .spec import BOARD, CASE, CNC, PRINT, Span, body_span, button_centres, c_holes, centred, display_pocket_span
from .spec import encoder_centres, g_holes, inner_span, k_holes, key_centres, lens_centre, rf_bay_span
from .spec import scoop_fade_start, scoop_spans, thickness_at, well_span

E = CUT_OVERSHOOT
FAR = 40.0  # mm; reach of the cutters that shape the underside


# ---------------------------------------------------------------------------------------------------------
# Levels that depend on the variant
# ---------------------------------------------------------------------------------------------------------
def plate_underside(variant: str) -> float:
    return BOARD.stack.plate_underside if variant == CNC else BOARD.stack.plate_top - CASE.print_lip


def recess_floor(variant: str) -> float:
    return -BOARD.display.lens.recess_depth if variant == CNC else -CASE.print_recess


def web_underside(variant: str) -> float:
    return BOARD.display.web.underside_z if variant == CNC else -CASE.print_recess - CASE.print_web


def usb_skin(variant: str) -> float:
    """CNC: 0.6 mm skin in front of the inner pocket (usb-io 6.2 item 3). FDM: no skin. The 0.8 mm print skin of
    usb-io 6.2 item 6 assumed the tongue 0.05 mm further forward; with the frozen tongue at Y 0.95 it would leave
    0.15 mm to the PCB against the 0.30 mm wall gap, so the print uses the usb-io 6.2 item 5 fallback: the pocket
    runs through the wall and the prongs show in the opening."""
    return CASE.usb_skin_cnc if variant == CNC else -1.0


# ---------------------------------------------------------------------------------------------------------
# Plan shapes
# ---------------------------------------------------------------------------------------------------------
def outline():
    return rounded(body_span(), BOARD.body.corner_radius)


def switch_opening(centre: tuple[float, float], variant: str):
    """14.00 square; CNC adds dog-bone reliefs for a 2.0 mm tool at the corners (enclosure 5, keys 6.2)."""
    size = BOARD.keys.plate_opening
    shape = rectangle(centred(centre, (size, size)))
    if variant == CNC:
        radius = CASE.dogbone_diameter / 2
        inset = size / 2 - radius / sqrt(2)
        for sx in (-1, 1):
            for sy in (-1, 1):
                shape += disc((centre[0] + sx * inset, centre[1] + sy * inset), CASE.dogbone_diameter)
    return shape


def display_pocket_outline():
    """Module pocket: square rear corners with T-bone reliefs, R1.0 front corners (D33)."""
    pocket = BOARD.display.pocket
    (x0, x1), (y0, y1) = display_pocket_span()
    radius = pocket.front_corner_radius
    shape = rectangle(((x0, x1), (y0, y1 - radius))) + rectangle(((x0 + radius, x1 - radius), (y0, y1)))
    shape += disc((x0 + radius, y1 - radius), 2 * radius) + disc((x1 - radius, y1 - radius), 2 * radius)
    relief = pocket.rear_relief_diameter
    shape += disc((x0 + relief / 2, y0), relief) + disc((x1 - relief / 2, y0), relief)
    return shape


def rf_pocket_span(radius: float, variant: str) -> Span:
    """CNC: the RF bay pockets run one corner radius into the outer wall, so their corners on the wall side leave
    no metal within the A4 margin of the antenna (mcu-radio A4); the wall keeps 2.0 of its 3.5 mm there. FDM:
    plastic, no RF rule; the pockets stop at the inner wall, so the solid print wall has no recess to hang over."""
    (x0, x1), y = rf_bay_span()
    return ((x0, x1 + radius) if variant == CNC else (x0, x1)), y


def plinth_span() -> Span:
    plinth = BOARD.plinth
    return (plinth.x0, plinth.x1), (plinth.y0, plinth.y1)


def bottom_wall_step_span() -> Span:
    """Plan of the thinned top of the bottom-shell wall along the key-well walls (D34). It runs on past the
    well's right wall by one corner radius, so the full step holds up to X keys.well_x1."""
    depth, wall = BOARD.body.bottom_wall_step
    radius = BOARD.case.cavity_corner_radius
    return (wall, BOARD.keys.well_x1 + radius), (wall, BOARD.body.depth - wall)


# ---------------------------------------------------------------------------------------------------------
# Top shell
# ---------------------------------------------------------------------------------------------------------
def top_shell(variant: str) -> Part:
    body, keys, stack = BOARD.body, BOARD.keys, BOARD.stack
    shell = slab(outline(), (body.split_z, 0.0))
    shell = chamfer(shell.edges().group_by(Axis.Z)[-1], body.top_chamfer)
    if variant == CNC:  # the lip hangs 0.15 below the split plane (keys 6.2, D34)
        shell += slab(rounded(well_span(), keys.well_corner_radius), (plate_underside(CNC), body.split_z))
    shell += _plinth()
    cutters = [slab(rounded(well_span(), keys.well_corner_radius), (stack.plate_top, E))]
    through_plate = (plate_underside(variant) - E, stack.plate_top + E)
    cutters += [slab(switch_opening(centre, variant), through_plate) for centre in key_centres()]
    k = BOARD.holes.k
    for centre in k.positions:
        cutters.append(countersink(centre, k.countersink, stack.plate_top, -1, k.clearance_hole))
        cutters.append(cylinder(centre, k.clearance_hole, through_plate))
    cutters += _top_pockets(variant)
    shell = shell.cut(*cutters)
    if variant == CNC:
        shell = _cnc_top_posts(shell)
    else:
        shell = shell.cut(*_insert_holes())
    return shell


def _plinth() -> Part:
    plinth = BOARD.plinth
    block = slab(rounded(plinth_span(), plinth.corner_radius), (-E, plinth.top_z))
    return chamfer(block.edges().group_by(Axis.Z)[-1], CASE.plinth_chamfer)


def _top_pockets(variant: str) -> list[Part]:
    """Everything cut into the top shell from the lens side and from the split face."""
    split, lens, web, plinth, buttons = BOARD.body.split_z, BOARD.display.lens, BOARD.display.web, BOARD.plinth, BOARD.buttons
    centre = lens_centre()
    from_split = split - E
    cutters = [
        slab(rounded(centred(centre, (lens.recess, lens.recess)), BOARD.display.lens.corner_radius + 0.1),
             (recess_floor(variant), E)),
        slab(rounded(centred(centre, (web.window, web.window)), CASE.web_window_radius),
             (web_underside(variant) - E, recess_floor(variant) + E)),
        slab(display_pocket_outline(), (from_split, web_underside(variant))),
        slab(rounded(rf_pocket_span(BOARD.rf_bay.top_pocket_corner_radius, variant), BOARD.rf_bay.top_pocket_corner_radius),
             (from_split, BOARD.rf_bay.top_z)),
    ]
    for axis in encoder_centres():
        cutters.append(slab(rounded(centred(axis, (plinth.pocket, plinth.pocket)), plinth.pocket_corner_radius),
                            (from_split, plinth.pocket_ceiling_z)))
        cutters.append(cylinder(axis, plinth.shaft_hole, (plinth.pocket_ceiling_z - E, plinth.top_z + E)))
    for axis in button_centres():
        cutters.append(cylinder(axis, buttons.counterbore, (from_split, BOARD.stack.button_counterbore_top)))
        cutters.append(cylinder(axis, buttons.hole, (BOARD.stack.button_counterbore_top - E, E)))
    return cutters


def _cnc_top_posts(shell: Part) -> Part:
    split = BOARD.body.split_z
    c, g = BOARD.holes.c, BOARD.holes.g
    posts = [cylinder(p, c.post, (end, split + E)) for p, end in zip(c.positions, c.post_bottom_z)]
    posts += [cylinder(p, g.post, (g.post_bottom_z, split + E)) for p in g.positions]
    shell = shell.fuse(*posts)
    drills = []
    for holes in (c_holes(), g_holes()):
        for index, position in enumerate(holes.positions):
            drills.append(drill(position, holes.tap_drill, holes.mouth_z[index], holes.shoulder_z(index)))
    return shell.cut(*drills)


def _insert_holes() -> list[Part]:
    split = BOARD.body.split_z
    positions = list(BOARD.holes.c.positions) + list(BOARD.holes.g.positions)
    return [cylinder(p, CASE.print_insert_hole, (split - E, split + CASE.print_insert_depth)) for p in positions]


# ---------------------------------------------------------------------------------------------------------
# Bottom shell
# ---------------------------------------------------------------------------------------------------------
def bottom_shell(variant: str) -> Part:
    shell = _bottom_body()
    shell = shell.cut(*_cavity(variant), *_rear_openings(variant), *_underside_cuts(variant))
    shell = _round_cell_rims(shell)
    if variant == CNC:
        shell = shell.cut(*_rf_slot())
    shell = shell.fuse(*_bottom_bosses(variant))
    shell = shell.cut(*_bottom_holes(variant))
    return shell


def side_profile(points: list[tuple[float, float]], x: tuple[float, float]) -> Part:
    """A prism across X from a polygon in board (y, z)."""
    face = Plane.YZ * Polygon(*[(-y, z) for y, z in points], align=None)
    return Pos(x[0], 0, 0) * extrude(face, x[1] - x[0], dir=(1, 0, 0))


def _bottom_body() -> Part:
    body, wedge = BOARD.body, BOARD.wedge
    depth, width = body.depth, body.width
    tall = slab(outline(), (-wedge.apex_height - 1.0, body.split_z))
    rear_slope = (wedge.apex_height - wedge.rear_height) / wedge.apex_y
    ramp = (wedge.apex_height - wedge.front_height) / (depth - wedge.apex_y)
    keep = side_profile([
        (-1.0, body.split_z), (-1.0, -wedge.rear_height + rear_slope), (wedge.apex_y, -wedge.apex_height),
        (depth + 1.0, -wedge.front_height + ramp), (depth + 1.0, body.split_z)], (-1.0, width + 1.0))
    shell = _bottom_chamfer(tall & keep)
    scoops = BOARD.wedge.scoops
    fade, end = scoop_fade_start(), scoops.end_y
    cutter = [(-1.0, scoops.underside_z), (fade, scoops.underside_z), (end, -thickness_at(end)),
              (end, -FAR), (-1.0, -FAR)]
    for (x0, x1), _ in scoop_spans():
        shell = shell - side_profile(cutter, (x0 - (1.0 if x0 == 0 else 0), x1 + (1.0 if x1 == width else 0)))
    return shell


def _bottom_chamfer(shell: Part) -> Part:
    """0.4 mm on the outer edges of the rear slope and the ramp (geometry 4.1, a guess). Cut before the flank
    scoops: OCCT cannot run one chamfer round the scoop steps, so the scoop edges stay sharp."""
    sides = [face for face in shell.faces() if abs(face.normal_at().Z) < 1e-6 and _on_outline(face)]
    side_edges = {edge for face in sides for edge in face.edges()}
    under = [face for face in shell.faces() if face.normal_at().Z < -0.2]
    edges = [edge for face in under for edge in face.edges() if edge in side_edges]
    return chamfer(edges, BOARD.body.bottom_chamfer)


def _on_outline(face) -> bool:
    centre = face.center()
    width, depth, radius = BOARD.body.width, BOARD.body.depth, BOARD.body.corner_radius
    x, y = centre.X, -centre.Y
    near_side = min(abs(x), abs(x - width), abs(y), abs(y - depth)) < 1e-3
    if face.geom_type == GeomType.CYLINDER:
        near_side = abs(face.radius - radius) < 1e-6 and (x < radius + 1e-3 or x > width - radius - 1e-3)
    return near_side


def _cavity(variant: str) -> list[Part]:
    body, floors, case = BOARD.body, BOARD.floors, BOARD.case
    split, radius = body.split_z, case.cavity_corner_radius
    key_floor, column_floor = floors.key_field_top_z, floors.control_column_top_z
    (ix0, ix1), (iy0, iy1) = inner_span()
    column = rounded(((floors.control_column_x0 - 2 * radius, ix1), (iy0, iy1)), radius) \
        & rectangle(((floors.control_column_x0, ix1 + E), (iy0 - E, iy1 + E)))
    c1_pad = disc(BOARD.holes.c.positions[0], CASE.c_pad_diameter)
    lower_column = millable(column - c1_pad, radius)
    c_floor = c_holes().mouth_z[0] - 0.05  # 0.05 under the C1 post end, the 2.0 local floor (enclosure 6.4)
    battery, relief = BOARD.battery, BOARD.battery.relief
    cutters = [
        slab(rounded(inner_span(), radius), (key_floor, split + E)),
        slab(rounded(bottom_wall_step_span(), radius), (split - body.bottom_wall_step[0], split + E)),
        slab(millable(column, radius), (c_floor, key_floor + E)),
        slab(lower_column, (column_floor, c_floor + E)),
        slab(rounded((tuple(battery.pocket_x), tuple(battery.pocket_y)), battery.pocket_corner_radius),
             (battery.pocket_floor_top_z, key_floor + E)),
        # The relief starts inside the pocket so its rounded left end leaves no sliver at the pocket wall.
        slab(rounded(((relief.x[0] - 2 * relief.corner_radius, relief.x[1]), tuple(relief.y)), relief.corner_radius),
             (relief.floor_top_z, key_floor + E)),
        slab(rounded(rf_pocket_span(radius, variant), radius), (BOARD.rf_bay.floor_top_z, column_floor + E)),
    ]
    if variant == CNC:
        index = BOARD.holes.c.spot_face.index
        cutters.append(cylinder(BOARD.holes.c.positions[index], CASE.c_post_well,
                                (BOARD.holes.c.post_bottom_z[index] - 0.05, column_floor + E)))
    return cutters


def in_cell_pocket_plan(x: float, y: float, slack: float = 1e-3) -> bool:
    """True on or inside the battery pocket or the relief rectangle, in board coordinates."""
    battery, relief = BOARD.battery, BOARD.battery.relief
    spans = ((battery.pocket_x, battery.pocket_y), (relief.x, relief.y))
    return any(x0 - slack <= x <= x1 + slack and y0 - slack <= y <= y1 + slack for (x0, x1), (y0, y1) in spans)


def cell_rim_levels() -> tuple[float, float]:
    """Floor tops the pocket and relief rims lie on: the key field and the control column."""
    return BOARD.floors.key_field_top_z, BOARD.floors.control_column_top_z


def _round_cell_rims(shell: Part) -> Part:
    """R0.5 on the convex rims of the battery pocket and the relief (power 14 rule 3): the bottom shell is
    lowered over the cell (D28), so these edges slide past the pouch. The rim edges are the level edges on the
    pocket outline at the two floor tops, plus the two short vertical edges where the relief crosses the 0.35 mm
    step between the floors; OCCT needs those to run the fillet down the step."""
    levels = cell_rim_levels()
    step = abs(levels[0] - levels[1])

    def on_outline(edge) -> bool:
        points = [edge.position_at(t) for t in (0.0, 0.5, 1.0)]
        return all(in_cell_pocket_plan(p.X, -p.Y) for p in points)

    def is_rim(edge) -> bool:
        start, end = edge.position_at(0.0), edge.position_at(1.0)
        level = abs(start.Z - end.Z) < 1e-6 and any(abs(start.Z - z) < 1e-6 for z in levels)
        upright = abs(start.X - end.X) < 1e-6 and abs(start.Y - end.Y) < 1e-6
        at_step = abs(start.X - BOARD.floors.control_column_x0) < 1e-6
        riser = upright and at_step and abs(abs(start.Z - end.Z) - step) < 1e-6
        return (level or riser) and on_outline(edge)

    edges = [edge for edge in shell.edges() if is_rim(edge)]
    if not edges:
        raise ValueError("no battery pocket rim edges found to round")
    return fillet(edges, CASE.cell_rim_radius)


def _rear_openings(variant: str) -> list[Part]:
    usb, switch, split, wall = BOARD.usb, BOARD.power_switch, BOARD.body.split_z, BOARD.body.wall
    pocket = rectangle((tuple(usb.pocket_x), (usb_skin(variant), wall + 2.0)))
    if variant == CNC:  # T-bones along X at the front corners: square corners for the tongue, the skin untouched
        radius = CASE.usb_pocket_radius
        for x in usb.pocket_x:
            pocket += disc((x, usb_skin(variant) + radius), 2 * radius)
    return [
        slab(pocket, (usb.pocket_z[1], split + E)),
        box(tuple(usb.notch_x), (-1.0, wall + E), (usb.notch_z[1], split + E)),
        box(tuple(switch.notch_x), (-1.0, wall + E), (switch.notch_z[1], split + E)),
    ]


def _rf_slot() -> list[Part]:
    """Slot through the right wall, key reliefs in its ends, and a trench along its inner side below the cavity
    floor: without it the slot's lower 1.4 mm would end in square corners against the floor that no mill cuts."""
    window, body = BOARD.rf_window, BOARD.body
    split, width, radius = body.split_z, body.width, BOARD.case.cavity_corner_radius
    relief_x = width - body.wall / 2
    trench = rounded(((width - body.wall - CASE.rf_trench_width, width + 2 * radius), (window.y0, window.y1)), radius)
    cutters = [box((width - body.wall - E, width + 1.0), (window.y0, window.y1), (window.bottom_z, split + E)),
               slab(trench, (window.bottom_z, BOARD.floors.control_column_top_z + E))]
    for y in (window.y0, window.y1):
        cutters.append(cylinder((relief_x, y), window.relief_diameter, (split - window.relief_depth, split + E)))
    return cutters


def ramp_normal_rotation() -> Rot:
    """Turns +Z onto the inward normal of the ramp plane (model frame)."""
    wedge = BOARD.wedge
    slope = (wedge.apex_height - wedge.front_height) / (BOARD.body.depth - wedge.apex_y)
    return Rot(X=-degrees(atan(slope)))


def on_ramp(position: tuple[float, float], diameter: float, depth: float, outside: float = 1.0) -> Part:
    """A round pocket cut square to the ramp plane, `depth` into the part, starting `outside` below it."""
    x, y = position
    pocket = Pos(0, 0, -outside) * Cylinder(diameter / 2, depth + outside, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return Pos(x, -y, -thickness_at(y)) * (ramp_normal_rotation() * pocket)


def _underside_cuts(variant: str) -> list[Part]:
    feet = BOARD.feet
    return [on_ramp(tuple(p), feet.pocket_diameter, feet.pocket_depth) for p in feet.positions]


def _bottom_bosses(variant: str) -> list[Part]:
    """Material added after the cavity: K posts (CNC) or K and C bosses (FDM), and the reset pad."""
    floors, k, reset = BOARD.floors, BOARD.holes.k, BOARD.reset
    added = [cylinder((reset.x, reset.y), CASE.reset_pad_diameter, (floors.control_column_top_z - E, reset.floor_top_z))]
    if variant == CNC:
        added += [cylinder(p, k.post, (floors.key_field_top_z - E, k.post_top_z)) for p in k.positions]
    else:
        boss_top = CASE.print_k_boss_top_z
        added += [cylinder(p, CASE.print_k_boss, (floors.key_field_top_z - E, boss_top)) for p in k.positions]
        added += [cylinder(p, k.post, (boss_top - E, CASE.print_k_post_top_z)) for p in k.positions]
        added += [cylinder(p, CASE.print_c_boss, (floors.control_column_top_z - E, boss_top))
                  for p in BOARD.holes.c.positions]
    return added


def _bottom_holes(variant: str) -> list[Part]:
    c, k, reset = BOARD.holes.c, BOARD.holes.k, BOARD.reset
    holes = [cylinder((reset.x, reset.y), reset.pinhole, (-FAR, reset.floor_top_z + E))]
    spot = c.spot_face
    for index, position in enumerate(c.positions):
        seat = c_seat_z(index, variant)
        if variant == PRINT or index == spot.index:
            holes.append(cylinder(position, spot.diameter, (-FAR, seat)))
        holes.append(countersink(position, c.countersink, seat, 1, CASE.m2_clearance))
        holes.append(cylinder(position, CASE.m2_clearance, (seat, BOARD.body.split_z)))
    if variant == CNC:
        tapped = k_holes()
        holes += [drill(p, tapped.tap_drill, tapped.mouth_z[i], tapped.shoulder_z(i)) for i, p in enumerate(k.positions)]
    else:
        top = CASE.print_k_post_top_z
        holes += [cylinder(p, CASE.print_k_clearance, (CASE.print_k_boss_top_z, top + E)) for p in k.positions]
        holes += [cylinder(p, CASE.print_k_pilot, (print_k_pilot_end(), CASE.print_k_boss_top_z + E))
                  for p in k.positions]
    return holes


def c_seat_z(index: int, variant: str) -> float:
    """Face the C countersink is cut into: the scoop at C1, the spot-face floor at C2 (CNC); Z -12.0 in print."""
    if variant == PRINT:
        return CASE.print_c_seat_z
    c = BOARD.holes.c
    return c.spot_face.floor_z if index == c.spot_face.index else BOARD.wedge.scoops.underside_z


def print_k_head_top() -> tuple[float, float]:
    sink = (BOARD.holes.k.countersink - CASE.m16_head) / 2
    return BOARD.stack.plate_top - sink, BOARD.stack.plate_top - sink - CASE.head_undersize / 2


def print_k_tip() -> tuple[float, float]:
    """Highest and lowest tip of the M1.6 x 8 self-tapping screw in the FDM K boss."""
    high, low = print_k_head_top()
    return high - CASE.print_k_screw_length + CASE.length_tolerance, low - CASE.print_k_screw_length - CASE.length_tolerance


def print_k_pilot_end() -> float:
    return print_k_tip()[1] - 0.5  # 0.5 mm of pilot past the deepest tip. guess
