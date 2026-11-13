"""Made parts besides the shells, and the assembled set of case parts per variant.

RF window insert (CNC only), knobs, button caps, keycaps, lens, FDM ground spacers, the switch insertion jig
(D26), and the FDM print aids of the top shell (break-away ribs and one-layer skins).
"""

from functools import cache
from math import sqrt

from build123d import Axis, Box, Cone, Cylinder, Part, Plane, Pos, Rot, Sphere, extrude, fillet, loft

from .parts import bottom_shell, top_shell, web_underside
from .solids import CUT_OVERSHOOT, box, centred_box, cylinder, d_profile, rounded, slab
from .spec import BOARD, CASE, CNC, PRINT, body_span, button_centres, centred, encoder_centres, grown, key_centres
from .spec import lens_centre

E = CUT_OVERSHOOT


# ---------------------------------------------------------------------------------------------------------
# RF window insert (enclosure 7.2, black POM)
# ---------------------------------------------------------------------------------------------------------
def rf_insert() -> Part:
    window, body, module = BOARD.rf_window, BOARD.body, BOARD.module
    length, thickness, height = window.insert
    width = body.width
    y_mid = (window.y0 + window.y1) / 2
    z = (window.bottom_z, window.bottom_z + height)
    bar = box((width - thickness, width), (y_mid - length / 2, y_mid + length / 2), z)
    key_x = width - body.wall / 2
    for y in (window.y0, window.y1):
        bar += cylinder((key_x, y), window.key_diameter, z)
    pocket = box((width - thickness - 1.0, width - CASE.rf_insert_skin),
                 (module.centre_y - window.antenna_pocket_length / 2, module.centre_y + window.antenna_pocket_length / 2),
                 tuple(sorted(window.antenna_pocket_z)))
    pocket = fillet(pocket.edges().filter_by(Axis.X), CASE.rf_insert_pocket_radius)
    return bar - pocket


# ---------------------------------------------------------------------------------------------------------
# Knob (rotary-buttons 6.5)
# ---------------------------------------------------------------------------------------------------------
def knob(variant: str, axis: tuple[float, float]) -> Part:
    knobs = BOARD.knobs
    rim = knobs.rim_z
    body = cylinder(axis, knobs.diameter, (rim, knobs.top_z))
    body = fillet(body.edges().group_by(Axis.Z)[-1], CASE.knob_top_radius)
    counterbore, cb_depth = CASE.knob_counterbore
    relief, relief_top = CASE.knob_relief
    bore, flat, bore_top = CASE.knob_bore
    if variant == PRINT:
        bore, flat = CASE.print_knob_bore
    cutters = [
        cylinder(axis, counterbore, (rim - E, rim + cb_depth)),
        cylinder(axis, relief, (rim + cb_depth - E, rim + relief_top)),
        Pos(axis[0], -axis[1], rim + relief_top - E) * extrude(d_profile(bore, flat), bore_top - relief_top + E),
    ]
    if variant == CNC:  # M2 set screw square to the flat, toward the rear (tap drill 1.6)
        hole = Pos(axis[0], -axis[1] + knobs.diameter / 4, rim + CASE.knob_set_screw_z) * (
            Rot(X=90) * Cylinder(CASE.m2_tap_drill / 2, knobs.diameter / 2 + 1.0))
        cutters.append(hole)
    result = body.cut(*cutters)
    if variant == PRINT:
        result = result.fuse(*knob_crush_ribs(axis))
    return result


def knob_crush_ribs(axis: tuple[float, float]) -> list[Part]:
    """Three ribs in the printed D-bore: two on the round side reaching Ø5.90, one on the flat (0.15 mm)."""
    reach, flat_rib, width = CASE.print_knob_rib
    bore, flat = CASE.print_knob_bore
    rim, relief_top, bore_top = BOARD.knobs.rim_z, CASE.knob_relief[1], CASE.knob_bore[2]
    z0, z1 = rim + relief_top, rim + bore_top
    height = z1 - z0
    ribs = []
    for angle in (210.0, 330.0):  # on the round side, away from the flat (flat faces +Y)
        radial = (bore - reach) / 2 + 0.3
        rib = Pos((reach / 2 + radial / 2), 0, 0) * Box(radial, width, height)
        ribs.append(Pos(axis[0], -axis[1], (z0 + z1) / 2) * (Rot(Z=angle) * rib))
    flat_y = flat - bore / 2  # flat face position from the axis, toward +Y
    rib = Pos(0, flat_y - flat_rib / 2 + 0.15, 0) * Box(width, flat_rib + 0.3, height)
    ribs.append(Pos(axis[0], -axis[1], (z0 + z1) / 2) * rib)
    return ribs


# ---------------------------------------------------------------------------------------------------------
# Button cap (rotary-buttons 6.6)
# ---------------------------------------------------------------------------------------------------------
def button_cap(axis: tuple[float, float], variant: str = CNC) -> Part:
    """Resin (or turned) cap with a 0.3 mm crown. The FDM prototype cap has a flat top: it prints top face down,
    and a crown on the bed would start as a small disc that grows by about 1 mm a layer."""
    buttons = BOARD.buttons
    flange_top = BOARD.stack.button_counterbore_top - CASE.button_flange_gap
    flange = cylinder(axis, buttons.cap_flange, (flange_top - CASE.button_flange_thickness, flange_top))
    nub = cylinder(axis, CASE.button_nub, (buttons.cap_bottom_z, flange_top - CASE.button_flange_thickness + E))
    cone_start = buttons.cap_top_z - CASE.button_crown - 0.3
    shank = cylinder(axis, buttons.cap_diameter, (flange_top - E, cone_start))
    cone = Pos(axis[0], -axis[1], cone_start) * (
        _frustum(buttons.cap_diameter / 2, CASE.button_top / 2, 0.3))
    crown = CASE.button_crown
    dome_base = buttons.cap_top_z - crown
    if variant == PRINT:
        dome = cylinder(axis, CASE.button_top, (dome_base - E, buttons.cap_top_z))
    else:
        radius = ((CASE.button_top / 2) ** 2 + crown ** 2) / (2 * crown)
        dome = (Pos(axis[0], -axis[1], buttons.cap_top_z - radius) * Sphere(radius)) & \
            cylinder(axis, CASE.button_top, (dome_base - E, buttons.cap_top_z + 1.0))
    return flange.fuse(nub, shank, cone, dome)


def _frustum(bottom: float, top: float, height: float) -> Part:
    return Cone(bottom, top, height, align=None)


# ---------------------------------------------------------------------------------------------------------
# Keycap (keys 6.5): our own low square cap with a square spherical dish, printed in resin
# ---------------------------------------------------------------------------------------------------------
@cache
def keycap_at_origin() -> Part:
    keys = BOARD.keys
    outer = loft([
        Plane.XY * rounded(((-keys.cap_base / 2, keys.cap_base / 2),) * 2, CASE.keycap_base_radius),
        Plane.XY.offset(keys.cap_height) * rounded(((-keys.cap_top / 2, keys.cap_top / 2),) * 2, CASE.keycap_top_radius),
    ])
    outer = fillet(outer.edges().group_by(Axis.Z)[-1], CASE.keycap_edge_radius)
    dish_size, dish_radius, dish_depth = CASE.keycap_dish
    corner = (dish_size / 2 - dish_radius) * sqrt(2) + dish_radius
    sphere_radius = (corner ** 2 + dish_depth ** 2) / (2 * dish_depth)
    dish = slab(rounded(((-dish_size / 2, dish_size / 2),) * 2, dish_radius), (keys.cap_height - 1.0, keys.cap_height + 1.0)) \
        & (Pos(0, 0, keys.cap_height - dish_depth + sphere_radius) * Sphere(sphere_radius))
    roof = CASE.keycap_stem_top + CASE.keycap_roof_relief
    inner = loft([
        Plane.XY.offset(-E) * rounded(((-CASE.keycap_skirt_inner / 2, CASE.keycap_skirt_inner / 2),) * 2, 0.5),
        Plane.XY.offset(roof) * rounded(((-CASE.keycap_inner_top / 2, CASE.keycap_inner_top / 2),) * 2, 0.5),
    ])
    cap = outer.cut(dish, inner)
    seat_top = CASE.keycap_stem_top
    post_bottom = seat_top - CASE.keycap_post_length
    stem = cylinder((0, 0), CASE.keycap_seat, (seat_top, roof + E)) + cylinder((0, 0), CASE.keycap_post, (post_bottom, seat_top + E))
    length, width = CASE.keycap_slot
    slot = centred_box((0, 0), (length, width), (post_bottom - E, seat_top)) + \
        centred_box((0, 0), (width, length), (post_bottom - E, seat_top))
    return cap.fuse(stem - slot)


def keycap(centre: tuple[float, float], lowered: float = 0.0) -> Part:
    return Pos(centre[0], -centre[1], -lowered) * keycap_at_origin()


# ---------------------------------------------------------------------------------------------------------
# Lens (display 6.4)
# ---------------------------------------------------------------------------------------------------------
def lens() -> Part:
    lens_spec = BOARD.display.lens
    return slab(rounded(((lens_spec.x0, lens_spec.x1), (lens_spec.y0, lens_spec.y1)), lens_spec.corner_radius),
                (BOARD.stack.lens_underside, 0.0))


def lens_outline():
    lens_spec = BOARD.display.lens
    return rounded(((lens_spec.x0, lens_spec.x1), (lens_spec.y0, lens_spec.y1)), lens_spec.corner_radius)


def lens_mask_window():
    window = BOARD.display.lens.window
    return rounded(centred(lens_centre(), (window, window)), CASE.lens_mask_radius)


# ---------------------------------------------------------------------------------------------------------
# FDM ground spacers (enclosure 8.2) and the switch insertion jig (D26)
# ---------------------------------------------------------------------------------------------------------
def g_spacer(position: tuple[float, float]) -> Part:
    outer, inner = CASE.print_g_spacer
    z = (BOARD.pcb.top_z, BOARD.body.split_z)
    return cylinder(position, outer, z) - cylinder(position, inner, (z[0] - E, z[1] + E))


def jig_ribs() -> list[tuple[float, float]]:
    """One rib under each socket barrel, in board coordinates."""
    barrels = BOARD.keys.footprint.barrel_holes
    return [(x + bx, y + by) for x, y in key_centres() for bx, by in barrels]


def insertion_jig() -> Part:
    """Base plate under the whole case outline, a square rib under each socket barrel jig_support_gap under the
    socket underside (keys 6.4, D26), and a rim under the top-shell split face along all four walls. The top
    shell with the PCB rests deck up on the rim, so its weight and the insertion load go into the shell, not
    into the G1 and G2 screws, and the ribs only back the sockets. The rim stays outside the PCB outline and is
    notched round the USB-C receptacle and the power switch, which reach into the rear wall."""
    assembly = BOARD.assembly
    plate = slab(rounded(body_span(), BOARD.body.corner_radius), CASE.jig_plate)
    rib_top = BOARD.stack.socket_underside - assembly.jig_support_gap
    ribs = [centred_box(p, (CASE.jig_rib, CASE.jig_rib), (CASE.jig_plate[1] - E, rib_top)) for p in jig_ribs()]
    return plate.fuse(*ribs, jig_rim())


def jig_rim() -> Part:
    """The rim the top shell stands on: the outline less an inset of jig_rim_width, top at the split face."""
    width = CASE.jig_rim_width
    band = rounded(body_span(), BOARD.body.corner_radius) - rounded(grown(body_span(), -width), 0.5)
    rim = slab(band, (CASE.jig_plate[1] - E, BOARD.body.split_z))
    margin = CASE.jig_rim_notch_margin
    notches = [box((x0 - margin, x1 + margin), (-1.0, width + 1.0), (CASE.jig_plate[1], BOARD.body.split_z + 1.0))
               for x0, x1 in (BOARD.usb.pocket_x, BOARD.power_switch.notch_x)]
    return rim.cut(*notches)


# ---------------------------------------------------------------------------------------------------------
# FDM print aids of the top shell
# ---------------------------------------------------------------------------------------------------------
def top_print_ribs() -> Part:
    """Break-away ribs: under the front ledge of the display web, which would otherwise bridge 26.65 mm, and
    across each button counterbore under its skin, which would otherwise bridge 17 mm."""
    lens_y1 = lens_centre()[1] + BOARD.display.web.window / 2
    pocket_y1 = BOARD.display.pocket.bend_y1
    half = CASE.print_support_rib / 2
    z = (BOARD.body.split_z, web_underside(PRINT))
    ribs = [box((x - half, x + half), (lens_y1 + 0.2, pocket_y1 - 0.4), z) for x in CASE.print_support_x]
    reach = BOARD.buttons.counterbore / 2 - 0.4
    ribs += [box((x - reach, x + reach), (y - half, y + half), (BOARD.body.split_z, BOARD.stack.button_counterbore_top))
             for x, y in button_centres()]
    return ribs[0].fuse(*ribs[1:])


def top_print_skins() -> Part:
    """One layer closing each hole in a printed ceiling (shaft holes, button holes); drilled out after printing."""
    skins = [cylinder(axis, BOARD.plinth.shaft_hole + 2 * E, (BOARD.plinth.pocket_ceiling_z,
                                                                BOARD.plinth.pocket_ceiling_z + CASE.print_skin))
             for axis in encoder_centres()]
    top = BOARD.stack.button_counterbore_top
    skins += [cylinder(axis, BOARD.buttons.hole + 2 * E, (top, top + CASE.print_skin)) for axis in button_centres()]
    return skins[0].fuse(*skins[1:])


# ---------------------------------------------------------------------------------------------------------
# The case parts of one variant, in the assembly pose
# ---------------------------------------------------------------------------------------------------------
@cache
def case_parts(variant: str) -> dict[str, Part]:
    parts = {"top_shell": top_shell(variant), "bottom_shell": bottom_shell(variant), "lens": lens()}
    (left, right) = encoder_centres()
    parts["knob_left"], parts["knob_right"] = knob(variant, left), knob(variant, right)
    (b_left, b_right) = button_centres()
    parts["button_cap_left"], parts["button_cap_right"] = button_cap(b_left, variant), button_cap(b_right, variant)
    caps = [keycap(centre) for centre in key_centres()]
    parts["keycaps"] = caps[0].fuse(*caps[1:])
    if variant == CNC:
        parts["rf_insert"] = rf_insert()
    else:
        spacers = [g_spacer(tuple(p)) for p in BOARD.holes.g.positions]
        parts["g_spacers"] = spacers[0].fuse(spacers[1])
    return parts
