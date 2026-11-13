"""Reference shapes of the bought parts, for fit and clash checks only. Drawn from board.toml and the
datasheet numbers in research/components/, not from vendor models. Screws are drawn at their core
diameter (just under the tap drill), so a screw in its tapped hole does not count as a clash.

Each entry is one solid or a fused group of identical parts (all 16 switches are one entry).
"""

from functools import cache

from build123d import Part, Pos, extrude

from .parts import c_seat_z, on_ramp, print_k_head_top, print_k_tip, recess_floor, web_underside
from .solids import box, centred_box, countersink, cylinder, d_profile, rectangle, rounded, slab
from .spec import BOARD, CASE, CNC, PRINT, battery_pocket_span, button_centres, c_holes, cell_span, cell_z, centred
from .spec import encoder_centres, g_holes, k_holes, key_centres, lens_centre, module_span

SHANK_UNDERSIZE = 0.05  # a screw is drawn this much under its tap drill or pilot


def _fused(parts: list[Part]) -> Part:
    return parts[0].fuse(*parts[1:]) if len(parts) > 1 else parts[0]


# ---------------------------------------------------------------------------------------------------------
# PCB
# ---------------------------------------------------------------------------------------------------------
@cache
def pcb(with_holes: bool = True) -> Part:
    board = BOARD.pcb
    shape = rounded(((board.x0, board.x1), (board.y0, board.y1)), board.corner_radius)
    for tongue in board.tongues:
        shape += rectangle(((tongue.x0, tongue.x1), (tongue.y0, board.y0 + 1.0)))
    for notch in board.notches:
        shape -= rectangle(((notch.x0, notch.x1), (notch.y0 - 0.01, notch.y1)))
    z = (board.bottom_z, board.top_z)
    plate = slab(shape, z)
    if not with_holes:
        return plate
    holes = [cylinder(p, BOARD.holes.k.pcb_hole, (z[0] - 1, z[1] + 1)) for p in BOARD.holes.k.positions]
    holes += [cylinder(p, BOARD.holes.c.pcb_hole, (z[0] - 1, z[1] + 1)) for p in BOARD.holes.c.positions]
    holes += [cylinder(p, BOARD.holes.g.pcb_hole, (z[0] - 1, z[1] + 1)) for p in BOARD.holes.g.positions]
    footprint = BOARD.keys.footprint
    for x, y in key_centres():
        holes.append(cylinder((x, y), footprint.centre_hole, (z[0] - 1, z[1] + 1)))
        holes += [cylinder((x + bx, y + by), footprint.barrel_hole_diameter, (z[0] - 1, z[1] + 1))
                  for bx, by in footprint.barrel_holes]
    return plate.cut(*holes)


# ---------------------------------------------------------------------------------------------------------
# Keys
# ---------------------------------------------------------------------------------------------------------
def switch_body(centre: tuple[float, float]) -> Part:
    """Housing, flange and collar: the parts that do not move."""
    keys = BOARD.keys
    housing = centred_box(centre, (keys.housing, keys.housing), (BOARD.pcb.top_z, BOARD.stack.plate_top))
    flange = centred_box(centre, (keys.flange, keys.flange), (BOARD.stack.plate_top, CASE.switch_flange_top))
    upper = centred_box(centre, (CASE.switch_upper, CASE.switch_upper), (CASE.switch_flange_top, CASE.switch_housing_top))
    outer, inner, rim = CASE.switch_collar
    collar = cylinder(centre, outer, (CASE.switch_housing_top, rim)) - cylinder(centre, inner, (CASE.switch_housing_top - 1, rim + 1))
    # The stem column runs down into the housing as the key travels: an open channel of the collar's inner
    # diameter, deep enough for the stem at full travel (a guess at the hidden shape).
    channel_bottom = CASE.switch_housing_top - 1.0 - (CASE.switch_travel + CASE.switch_travel_tolerance) - 0.2
    channel = cylinder(centre, inner, (channel_bottom, CASE.switch_housing_top + 1))
    return housing.fuse(flange, upper, collar).cut(channel)


def switch_stem(centre: tuple[float, float], lowered: float = 0.0) -> Part:
    """Stem column with its bore and the MX cross inside, at rest or pressed by `lowered`."""
    outer, bore = CASE.switch_stem
    top = CASE.keycap_stem_top
    bottom = CASE.switch_housing_top - 1.0
    tube = cylinder(centre, outer, (bottom, top)) - cylinder(centre, bore, (bottom + 0.2, top + 1))
    length, width = CASE.switch_cross
    cross = centred_box(centre, (length, width), (bottom + 0.1, top - 0.1)) + \
        centred_box(centre, (width, length), (bottom + 0.1, top - 0.1))
    return Pos(0, 0, -lowered) * tube.fuse(cross)


def socket(centre: tuple[float, float]) -> Part:
    zx0, zy0, zx1, zy1 = BOARD.keys.keepout.socket_zone
    x, y = centre
    bottom = BOARD.pcb.bottom_z
    return box((x + zx0, x + zx1), (y + zy0, y + zy1), (bottom - CASE.socket_depth, bottom))


def diode(centre: tuple[float, float]) -> Part:
    d = BOARD.keys.diode
    bottom = BOARD.pcb.bottom_z
    return centred_box((centre[0] + d.offset[0], centre[1] + d.offset[1]), tuple(d.size), (bottom - d.height, bottom))


# ---------------------------------------------------------------------------------------------------------
# Controls and display
# ---------------------------------------------------------------------------------------------------------
def encoder(axis: tuple[float, float]) -> Part:
    """Body, mounting tabs and collar: the parts that stay put when the knob is pushed."""
    enc = BOARD.encoders
    top = BOARD.pcb.top_z
    body = centred_box(axis, tuple(enc.body), (top, enc.body_top_z))
    tabs = [centred_box((axis[0] + side * (enc.tab_span / 2 - 0.4), axis[1]), (0.8, 2.0), (top, top + 3.0))
            for side in (-1, 1)]
    collar_d, collar_top = CASE.encoder_collar
    collar = cylinder(axis, collar_d, (enc.body_top_z - 0.01, collar_top))
    return body.fuse(*tabs, collar)


def encoder_shaft(axis: tuple[float, float], lowered: float = 0.0) -> Part:
    """Round below the flat start, D-shaped above it, tip at the nominal height."""
    collar_top = CASE.encoder_collar[1]
    shaft_d, flat, tip = CASE.encoder_shaft
    round_part = cylinder(axis, shaft_d, (collar_top, CASE.encoder_flat_z))
    d_part = Pos(axis[0], -axis[1], CASE.encoder_flat_z - 0.01) * extrude(d_profile(shaft_d, flat), tip - CASE.encoder_flat_z)
    return Pos(0, 0, -lowered) * round_part.fuse(d_part)


def button_switch(axis: tuple[float, float]) -> Part:
    b = BOARD.buttons
    top = BOARD.pcb.top_z
    body = centred_box(axis, tuple(b.switch_body), (top, b.switch_top_z - 0.4))
    plunger = cylinder(axis, 3.0, (b.switch_top_z - 0.41, b.switch_top_z))
    return body + plunger


def display_parts(variant: str) -> dict[str, Part]:
    """The module hangs on its 0.10 mm tape frame under the web (D10), so it follows the web: in print the web
    underside is 0.05 lower (whole layers) and the module with it; the foam takes the difference."""
    d = BOARD.display
    module_top = web_underside(variant) - (BOARD.display.web.underside_z - d.module.top_z)
    module_back = module_top - d.module.thickness
    module = box((d.module.x0, d.module.x1), (d.module.y0, d.module.y1), (module_back, module_top))
    flex = d.flex
    bend = box((flex.x0, flex.x1), (d.module.y1, flex.y1), (flex.bottom_z, module_top))
    tail = box((flex.x0, flex.x1), (d.connector.y_entry, d.module.y1), (flex.bottom_z, flex.bottom_z + 0.2))
    connector = box((d.connector.x0, d.connector.x1), (d.connector.y_back, d.connector.y_entry),
                    (BOARD.pcb.top_z, d.connector.top_z))
    foam_x = (d.module.x0 + d.module.x1) / 2
    foam = centred_box((foam_x, d.module.y0 + 1.0 + CASE.foam_pad[1] / 2), CASE.foam_pad, (BOARD.pcb.top_z, module_back))
    return {"display_module": module, "display_flex": bend.fuse(tail), "fpc_connector": connector,
            "display_foam": foam}


def lens_tape(variant: str) -> Part:
    """0.13 mm adhesive ring on the recess floor, 1.5 mm wide (display 6.4)."""
    recess = BOARD.display.lens.recess
    floor = recess_floor(variant)
    ring = rounded(centred(lens_centre(), (recess - 0.2, recess - 0.2)), 2.0) \
        - rounded(centred(lens_centre(), (recess - 3.2, recess - 3.2)), 1.0)
    return slab(ring, (floor, floor + CASE.lens_tape))


# ---------------------------------------------------------------------------------------------------------
# PCB bottom face
# ---------------------------------------------------------------------------------------------------------
def bottom_face_parts() -> dict[str, Part]:
    bottom = BOARD.pcb.bottom_z
    (mx0, mx1), (my0, my1) = module_span()
    usb, switch, conn, reset, flash = BOARD.usb, BOARD.power_switch, BOARD.battery.connector, BOARD.reset, BOARD.flash
    parts = {
        "module": box((mx0, mx1), (my0, my1), (bottom - BOARD.module.height, bottom)),
        "flash": centred_box((flash.x, flash.y), tuple(flash.size), (bottom - flash.height, bottom)),
        "usb_receptacle": box((usb.x - usb.width / 2, usb.x + usb.width / 2), (usb.front_y, usb.front_y + usb.length),
                              (usb.bottom_z, usb.top_z)),
        "battery_connector": centred_box((conn.x, conn.y), tuple(conn.body), (bottom - conn.height, bottom)),
        "reset_button": centred_box((reset.x, reset.y), tuple(reset.body), (bottom - reset.height, bottom)),
    }
    body_y0 = switch.body_y0
    switch_body_part = box((switch.x - switch.body[0] / 2, switch.x + switch.body[0] / 2),
                           (body_y0, body_y0 + switch.body[1]), (bottom - switch.height, bottom))
    width, reach = switch.actuator
    actuator = box((switch.x - width / 2, switch.x + width / 2), (body_y0 - reach, body_y0 + 0.01),
                   (switch.actuator_z - 0.4, switch.actuator_z + 0.4))
    parts["power_switch"] = switch_body_part + actuator
    plug_x1 = conn.x - conn.body[0] / 2
    parts["battery_plug"] = box((plug_x1 - BOARD.battery.plug_protrusion, plug_x1), (conn.y - 3.0, conn.y + 3.0),
                                (bottom - conn.height + 0.3, bottom - 0.7))
    power = [centred_box((p.x, p.y), tuple(p.size), (bottom - p.height, bottom)) for p in vars(BOARD.power.parts).values()]
    parts["power_parts"] = _fused(power)
    return parts


def battery_parts() -> dict[str, Part]:
    battery = BOARD.battery
    floor = battery.pocket_floor_top_z
    z0, z1 = cell_z()
    cell = slab(rounded(cell_span(), 1.0), (z0, z1))
    sheet = slab(rounded(battery_pocket_span(), battery.pocket_corner_radius),
                 (BOARD.stack.insulation_bottom, BOARD.stack.key_field_floor_top))
    foam = slab(rounded(cell_span(), 1.0), (floor, floor + battery.foam))
    return {"cell": cell, "insulation_sheet": sheet, "cell_foam": foam}


# ---------------------------------------------------------------------------------------------------------
# Screws, feet, inserts
# ---------------------------------------------------------------------------------------------------------
def k_screws(variant: str) -> Part:
    k = k_holes()
    shank = k.tap_drill - SHANK_UNDERSIZE if variant == CNC else CASE.print_k_pilot - SHANK_UNDERSIZE
    head_top = k.head_top_z[0][0] if variant == CNC else print_k_head_top()[0]
    tip = k.tip_z(0)[0] if variant == CNC else print_k_tip()[0]
    screws = []
    for position in k.positions:
        head = countersink(position, CASE.m16_head, head_top, -1, shank) - cylinder(position, 10, (head_top, head_top + 1))
        screws.append(head + cylinder(position, shank, (tip, head_top - 0.1)))
    return _fused(screws)


def c_screws(variant: str) -> Part:
    c = c_holes()
    shank = c.tap_drill - SHANK_UNDERSIZE
    screws = []
    for index, position in enumerate(c.positions):
        seat = c_seat_z(index, variant)
        head_top = seat + (BOARD.holes.c.countersink - CASE.m2_head) / 2
        length = CASE.c_length if variant == CNC else CASE.print_c_screw_length
        head = countersink(position, CASE.m2_head, head_top, 1, shank) - cylinder(position, 10, (head_top - 1, head_top))
        screws.append(head + cylinder(position, shank, (head_top + 0.1, head_top + length)))
    return _fused(screws)


def g_screws() -> Part:
    g = g_holes()
    bearing = g.head_top_z[0][0]
    shank = g.tap_drill - SHANK_UNDERSIZE
    screws = [cylinder(p, CASE.m2_head, (bearing - CASE.g_head_height, bearing)) +
              cylinder(p, shank, (bearing - 0.1, bearing + CASE.g_length)) for p in g.positions]
    return _fused(screws)


def inserts() -> Part:
    """CNC Kitchen M2 x 3 heat-set inserts in the FDM top shell, drawn as pressed (outer = hole)."""
    split = BOARD.body.split_z
    positions = list(BOARD.holes.c.positions) + list(BOARD.holes.g.positions)
    parts = [cylinder(p, CASE.print_insert_hole, (split, split + CASE.print_insert_length))
             - cylinder(p, CASE.m2_tap_drill, (split - 1, split + 4)) for p in positions]
    return _fused(parts)


def feet() -> Part:
    """3M Bumpon SJ5076 in their pockets: top on the pocket floor, the rest proud of the ramp."""
    f = BOARD.feet
    return _fused([on_ramp(tuple(p), f.diameter, f.pocket_depth, outside=f.height - f.pocket_depth) for p in f.positions])


# ---------------------------------------------------------------------------------------------------------
# All components of one variant
# ---------------------------------------------------------------------------------------------------------
@cache
def components(variant: str) -> dict[str, Part]:
    centres = key_centres()
    parts = {
        "pcb": pcb(),
        "switch_bodies": _fused([switch_body(c) for c in centres]),
        "switch_stems": _fused([switch_stem(c) for c in centres]),
        "sockets": _fused([socket(c) for c in centres]),
        "diodes": _fused([diode(c) for c in centres]),
        "encoders": _fused([encoder(a) for a in encoder_centres()]),
        "encoder_shafts": _fused([encoder_shaft(a) for a in encoder_centres()]),
        "button_switches": _fused([button_switch(a) for a in button_centres()]),
        "lens_tape": lens_tape(variant),
        "k_screws": k_screws(variant),
        "c_screws": c_screws(variant),
        "g_screws": g_screws(),
        "feet": feet(),
    }
    parts |= display_parts(variant) | bottom_face_parts() | battery_parts()
    if variant == PRINT:
        parts["inserts"] = inserts()
    return parts
