"""Fit coupons to print before the full parts (family rule, conventions 3.6; enclosure 8.2), and the print pose
of every printed part.

Coupons: switch-plate fit (two lips, three openings each), keycap stem (resin), knob bore (three bores), the
USB-C opening (cut from the FDM bottom shell) and the lens recess (cut from the FDM top shell).
"""

from functools import cache
from math import atan, degrees

from build123d import Location, Part, Pos, Rot, extrude

from .parts import bottom_shell, top_shell
from .small_parts import case_parts, keycap_at_origin, knob_crush_ribs, top_print_ribs, top_print_skins
from .solids import CUT_OVERSHOOT, box, centred_box, cylinder, d_profile, rounded, slab
from .spec import BOARD, CASE, PRINT, centred, lens_centre

E = CUT_OVERSHOOT
PLATE_OPENINGS = (13.9, 14.0, 14.1)  # keys 6.2
PLATE_LIPS = (1.0, 1.2)  # keys 6.2: FDM lip 1.0 or 1.2 from the coupon
STEM_SLOTS = (1.30, 1.35, 1.40, 1.45)  # keys 6.5
STEM_POSTS = (5.00, 5.20, 5.40)  # keys 6.5
KNOB_BORES = (6.10, 6.20, 6.30)  # rotary-buttons 6.5
COUPON_BORDER = 4.0  # guess


# ---------------------------------------------------------------------------------------------------------
# Print poses: the transform that puts a part in the assembly frame onto the bed (Z = 0 at its lowest point)
# ---------------------------------------------------------------------------------------------------------
def ramp_on_bed() -> Rot:
    wedge = BOARD.wedge
    slope = (wedge.apex_height - wedge.front_height) / (BOARD.body.depth - wedge.apex_y)
    return Rot(X=degrees(atan(slope)))


def _on_bed(part: Part, turn: Location) -> Location:
    turned = turn * part
    return Pos(0, 0, -turned.bounding_box().min.Z) * turn


@cache
def print_pose(name: str) -> Location:
    """Bed pose of a printed part by name (see `printed_parts`)."""
    parts = printed_parts()
    turn = {
        "top_shell": Rot(),  # split face down, deck and plinth up (enclosure 8.2)
        "bottom_shell": ramp_on_bed(),  # the ramp plane on the bed (D27)
        "knob": Rot(X=180),  # top face down (rotary-buttons 6.5)
        "button_cap": Rot(X=180),  # top face down (rotary-buttons 6.6)
        "coupon_usb": Rot(X=-90),  # rear face down
    }.get(name, Rot())
    return _on_bed(parts[name], turn)


@cache
def printed_parts() -> dict[str, Part]:
    """FDM parts in the assembly frame, as they finish (no print aids), one of each kind."""
    parts = case_parts(PRINT)
    printed = {
        "top_shell": parts["top_shell"], "bottom_shell": parts["bottom_shell"], "knob": parts["knob_left"],
        "button_cap": parts["button_cap_left"], "g_spacer": _first_solid(parts["g_spacers"]),
    }
    return printed | coupons()


def print_aids(name: str) -> Part | None:
    """Break-away ribs and one-layer skins that print with a part and are removed afterwards."""
    if name == "top_shell":
        return top_print_ribs().fuse(top_print_skins())
    if name == "coupon_lens":
        return top_print_ribs() & _lens_box()
    return None


def as_printed(name: str) -> Part:
    """The part with its print aids, in its bed pose: what goes to the slicer."""
    part = printed_parts()[name]
    aids = print_aids(name)
    if aids is not None:
        part = part.fuse(aids)
    return print_pose(name) * part


def _first_solid(part: Part) -> Part:
    return Part(part.solids()[0].wrapped)


# ---------------------------------------------------------------------------------------------------------
# Coupons
# ---------------------------------------------------------------------------------------------------------
def plate_coupon(lip: float) -> Part:
    pitch, border = BOARD.keys.pitch, COUPON_BORDER
    length = pitch * len(PLATE_OPENINGS) + 2 * border - (pitch - max(PLATE_OPENINGS))
    width = max(PLATE_OPENINGS) + 2 * border
    plate = slab(rounded(((0, length), (0, width)), 2.0), (0, lip))
    first = border + max(PLATE_OPENINGS) / 2
    holes = [centred_box((first + index * pitch, width / 2), (size, size), (-E, lip + E))
             for index, size in enumerate(PLATE_OPENINGS)]
    return plate.cut(*holes)


def stem_coupon() -> Part:
    """Seven keycap posts on a plate: the four slot widths on a 5.20 post, then the three post diameters with the
    1.35 slot. Resin, as the keycaps."""
    pitch, base = 8.0, 1.5
    specs = [(CASE.keycap_post, slot) for slot in STEM_SLOTS] + [(post, 1.35) for post in STEM_POSTS]
    plate = slab(rounded(((0, pitch * len(specs)), (0, 12.0)), 1.5), (0, base))
    posts = []
    for index, (post, slot) in enumerate(specs):
        centre = (pitch / 2 + index * pitch, 6.0)
        top = base + CASE.keycap_post_length
        column = cylinder(centre, post, (base - E, top))
        length = CASE.keycap_slot[0]
        cross = centred_box(centre, (length, slot), (base + 0.3, top + E)) + \
            centred_box(centre, (slot, length), (base + 0.3, top + E))
        posts.append(column - cross)
    return plate.fuse(*posts)


def knob_bore_coupon() -> Part:
    """Three short knob sections in a row, each with a through D-bore of one size and the print crush ribs."""
    pitch, height = 14.0, 6.0
    diameter = BOARD.knobs.diameter
    strip = slab(rounded(((0, pitch * len(KNOB_BORES)), (0, 4.0)), 1.0), (0, 1.0))
    rings = []
    for index, bore in enumerate(KNOB_BORES):
        centre = (pitch / 2 + index * pitch, 2.0 + diameter / 2)
        ring = cylinder(centre, diameter, (0, height))
        flat = CASE.print_knob_bore[1] + (bore - CASE.print_knob_bore[0])
        ring = ring - Pos(centre[0], -centre[1], -E) * extrude(d_profile(bore, flat), height + 2 * E)
        ribs = [Pos(0, 0, -(BOARD.knobs.rim_z + CASE.knob_relief[1])) * rib for rib in knob_crush_ribs(centre)]
        ribs = [rib & cylinder(centre, bore + 0.4, (0, height)) for rib in ribs]
        rings.append(ring.fuse(*ribs))
    return strip.fuse(*rings)


def usb_coupon() -> Part:
    usb = BOARD.usb
    return bottom_shell(PRINT) & box((usb.pocket_x[0] - 6.0, usb.pocket_x[1] + 6.0), (0.0, 6.0),
                                     (-14.0, BOARD.body.split_z))


def _lens_box() -> Part:
    """Lens recess, web and display pocket, out to the right face so the RF pocket ceiling keeps both walls."""
    recess = BOARD.display.lens.recess
    (x0, _), (y0, _) = centred(lens_centre(), (recess + 4.0, recess + 4.0))
    return box((x0, BOARD.body.width), (y0, BOARD.display.pocket.bend_y1 + 3.0), (BOARD.body.split_z, 0.0))


def lens_coupon() -> Part:
    return top_shell(PRINT) & _lens_box()


@cache
def coupons() -> dict[str, Part]:
    return {
        "coupon_plate_1_0": plate_coupon(PLATE_LIPS[0]),
        "coupon_plate_1_2": plate_coupon(PLATE_LIPS[1]),
        "coupon_knob_bore": knob_bore_coupon(),
        "coupon_usb": usb_coupon(),
        "coupon_lens": lens_coupon(),
    }


def resin_parts() -> dict[str, Part]:
    """Parts ordered in resin (JLC3DP): the keycap and the stem coupon. Not checked against FDM rules."""
    return {"keycap": keycap_at_origin(), "coupon_stem": stem_coupon()}
