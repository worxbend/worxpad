"""The checks, checked: each one runs on a small solid with a known fault and must report it, and on a sound
solid and must stay quiet. A check that cannot fail proves nothing about the case.

Adapted from the macropad case (same owner): the CNC and print cases are the same idea with this case's limits,
plus the depth rule for corner radii, the support zones and the short-ledge rule of printsim.py.
"""

from math import radians, tan

from build123d import Axis, Box, Part, Plane, Polygon, Pos, extrude, fillet

from . import measure, printsim
from .spec import LIMITS
from .solids import overlap_volume

BLOCK = (30.0, 30.0, 10.0)
POCKET = (10.0, 10.0, 6.0)  # open at the top of the block


def _block() -> Part:
    return Pos(0, 0, BLOCK[2] / 2) * Box(*BLOCK)


def _pocket(corner_radius: float, depth: float = POCKET[2]) -> Part:
    pocket = Pos(0, 0, BLOCK[2] - depth / 2 + 1) * Box(POCKET[0], POCKET[1], depth + 2)
    return fillet(pocket.edges().filter_by(Axis.Z), corner_radius) if corner_radius else pocket


def _triangles(part: Part):
    return measure.mesh_of(part, measure.ANY_MATERIAL).triangles


def _leaning_wall(degrees_from_vertical: float) -> Part:
    """A 3 mm wall, 12 mm tall, leaning over by the given angle."""
    lean = 12 * tan(radians(degrees_from_vertical))
    profile = Plane.XZ * Polygon((0, 0), (3, 0), (3 + lean, 12), (lean, 12), align=None)
    return extrude(profile, 10)


def _ledge_on_wall() -> Part:
    """A wall standing on the bed with a 1 mm ledge along its whole 30 mm length, 5 mm up."""
    return Pos(0, 0, 5) * Box(3, 30, 10) + Pos(2, 0, 9) * Box(1, 30, 2)


def run() -> list[dict]:
    tool = LIMITS.cnc_tool
    sound = _block() - _pocket(1.5)
    sharp = _block() - _pocket(0)
    tight = _block() - _pocket(0.8)  # 6 deep needs R 1.1 by the depth rule
    slotted = _block() - Pos(0, 0, BLOCK[2]) * Box(20, tool - 1.0, 8)
    undercut = _block() - Pos(BLOCK[0] / 2, 0, BLOCK[2] / 2) * Box(10, 10, 3)  # a groove in the side
    sheet = Box(20, 20, LIMITS.fdm_wall - 0.3)
    table = Pos(0, 0, 5) * Box(24, 20, 2) + Pos(-11, 0, 2) * Box(2, 20, 4) + Pos(11, 0, 2) * Box(2, 20, 4)
    table_print = printsim.simulate(_triangles(table))
    shelf = Pos(0, 0, 5) * Box(4, 4, 10) + Pos(4, 0, 9) * Box(4, 4, 2)
    shelf_support = Pos(4, 0, -1) * Box(4, 4, 1)  # the zone the slicer would fill under the shelf
    loose = Box(5, 5, 5) + Pos(10, 0, 0) * Box(5, 5, 5)
    big = Box(LIMITS.bed + 5, 10, 2)
    tight_arcs = measure.concave_arcs(tight)
    sound_arcs = measure.concave_arcs(sound)
    square = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (5.0, 5.0), (10.0, 5.0)]
    rim_edges = [edge for edge in sharp.edges()
                 if all(abs(edge.position_at(t).Z - BLOCK[2]) < 1e-6 for t in (0.0, 1.0))
                 and abs(edge.position_at(0.5).X) < POCKET[0] / 2 + 1e-6
                 and abs(edge.position_at(0.5).Y) < POCKET[1] / 2 + 1e-6]
    rounded_rim = fillet(rim_edges, 0.5)
    cases = [
        ("overlap_found", overlap_volume(_block(), Pos(1, 0, 0) * _block()), "more than", LIMITS.clash_volume),
        ("thin_wall_found", measure.thinnest_wall(sheet), "less than", LIMITS.fdm_wall),
        ("sharp_corners_found", measure.sharp_internal_corners(sharp), "equal to", 4),
        ("sound_pocket_has_no_sharp_corner", measure.sharp_internal_corners(sound), "equal to", 0),
        ("radius_below_depth_rule_found", len(measure.radius_rule(tight_arcs)[0]), "equal to", 4),
        ("radius_on_depth_rule_passes", len(measure.radius_rule(sound_arcs)[0]), "equal to", 0),
        ("radius_below_table_found", len(measure.table_rule(tight_arcs, [])[0]), "equal to", 4),
        ("undercut_found", measure.unreachable_area(undercut), "more than", measure.UNDERCUT_NOISE),
        ("sound_pocket_has_no_undercut", measure.unreachable_area(sound), "less than", measure.UNDERCUT_NOISE),
        ("sharp_corner_not_cut", measure.uncut_area(sharp, tool)["above"], "more than", measure.UNCUT_NOISE),
        ("narrow_slot_not_cut", measure.uncut_area(slotted, tool)["above"], "more than", measure.UNCUT_NOISE),
        ("sound_pocket_is_cut", measure.uncut_area(sound, tool)["above"], "less than", measure.UNCUT_NOISE),
        ("long_bridge_found", table_print.longest_bridge, "more than", LIMITS.bridge),
        ("bridge_is_no_long_cantilever", table_print.deepest_cantilever, "less than", LIMITS.cantilever + 1e-6),
        ("cantilever_found", printsim.simulate(_triangles(shelf)).deepest_cantilever, "more than", LIMITS.cantilever),
        ("supported_shelf_prints", printsim.simulate(_triangles(shelf), _triangles(shelf_support)).deepest_cantilever,
         "less than", LIMITS.cantilever),
        ("short_ledge_is_no_bridge", printsim.simulate(_triangles(_ledge_on_wall())).longest_bridge, "less than",
         LIMITS.bridge),
        ("flat_slope_found", printsim.simulate(_triangles(_leaning_wall(60))).deepest_cantilever, "more than",
         LIMITS.cantilever),
        ("slope_of_45_degrees_prints", printsim.simulate(_triangles(_leaning_wall(45))).deepest_cantilever,
         "less than", 0.5),
        ("loose_pieces_found", measure.soundness_faults(loose), "more than", 0),
        ("one_box_is_sound", measure.soundness_faults(Box(5, 5, 5)), "equal to", 0),
        ("part_too_big_for_the_bed_found", measure.largest_extent(big), "more than", LIMITS.bed),
        ("point_inside_hull_has_its_margin", measure.inside_convex_hull(square, (5.0, 4.0)), "equal to", 4.0),
        ("point_outside_hull_found", measure.inside_convex_hull(square, (12.0, 5.0)), "less than", 0.0),
        ("sharp_rim_has_no_setback", _rim_setback(sharp), "less than", 0.01),
        ("rounded_rim_has_its_setback", _rim_setback(rounded_rim), "more than", 0.26),
    ]
    return [_verdict(*case) for case in cases]


def _rim_setback(part: Part) -> float:
    """Setback 0.05 below the pocket rim, on the +X wall, probed as checks._cell_rim_rows probes the cell pocket."""
    return measure.material_along(part, (POCKET[0] / 2 - 1.0, 0.0, BLOCK[2] - 0.05), (1, 0, 0)) - 1.0


def _verdict(name: str, found: float, relation: str, limit: float) -> dict:
    ok = {"more than": found > limit, "less than": found < limit, "equal to": found == limit}[relation]
    return {"name": name, "found": round(float(found), 3), "expected": f"{relation} {limit}", "ok": bool(ok)}
