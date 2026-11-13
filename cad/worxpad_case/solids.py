"""Small build123d helpers that take board coordinates (X right, Y toward the front, Z up from the deck).

Some helpers follow the macropad case (same owner): `box`, `cylinder`, `millable`, `overlap_volume`.
"""

from math import radians, tan
from pathlib import Path

import matplotlib
from build123d import Circle, Cone, Cylinder, Box, Part, Plane, Pos, Rectangle, RectangleRounded, Sketch
from build123d import Text, extrude, mirror, offset

from .spec import CASE, Span

CUT_OVERSHOOT = 0.01  # cuts run past the face they open, so no zero-thickness skin is left
# DejaVu Sans Bold ships inside matplotlib, so the laser-mark text is the same on every machine.
LEGEND_FONT = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSans-Bold.ttf"


def box(x: tuple[float, float], y: tuple[float, float], z: tuple[float, float]) -> Part:
    size = (x[1] - x[0], y[1] - y[0], z[1] - z[0])
    return Pos((x[0] + x[1]) / 2, -(y[0] + y[1]) / 2, (z[0] + z[1]) / 2) * Box(*size)


def span_box(span: Span, z: tuple[float, float]) -> Part:
    return box(span[0], span[1], z)


def centred_box(centre: tuple[float, float], size: tuple[float, float], z: tuple[float, float]) -> Part:
    return box((centre[0] - size[0] / 2, centre[0] + size[0] / 2), (centre[1] - size[1] / 2, centre[1] + size[1] / 2), z)


def cylinder(centre: tuple[float, float], diameter: float, z: tuple[float, float]) -> Part:
    return Pos(centre[0], -centre[1], (z[0] + z[1]) / 2) * Cylinder(diameter / 2, z[1] - z[0])


def rectangle(span: Span) -> Sketch:
    (x0, x1), (y0, y1) = span
    return Pos((x0 + x1) / 2, -(y0 + y1) / 2) * Rectangle(x1 - x0, y1 - y0)


def rounded(span: Span, radius: float) -> Sketch:
    (x0, x1), (y0, y1) = span
    if radius <= 0:
        return rectangle(span)
    return Pos((x0 + x1) / 2, -(y0 + y1) / 2) * RectangleRounded(x1 - x0, y1 - y0, radius)


def disc(centre: tuple[float, float], diameter: float) -> Sketch:
    return Pos(centre[0], -centre[1]) * Circle(diameter / 2)


def slab(profile: Sketch, z: tuple[float, float]) -> Part:
    return Pos(0, 0, z[0]) * extrude(profile, z[1] - z[0])


def millable(pocket: Sketch, tool_radius: float) -> Sketch:
    """The part of a pocket outline a 3-axis end mill of this radius cuts: every concave corner of the pocket
    gets the tool radius, and any gap the tool cannot enter stays solid (a morphological opening)."""
    return offset(offset(pocket, amount=-tool_radius), amount=tool_radius)


def countersink(centre: tuple[float, float], diameter: float, surface_z: float, direction: int, hole: float) -> Part:
    """A 90 degree countersink cone opening at `surface_z`, narrowing in `direction` (+1 up, -1 down) to the
    clearance hole, with a short overshoot outside the surface."""
    depth = (diameter - hole) / 2
    cone = Cone(diameter / 2 + CUT_OVERSHOOT, hole / 2, depth + CUT_OVERSHOOT, align=None)
    if direction > 0:
        return Pos(centre[0], -centre[1], surface_z - CUT_OVERSHOOT) * cone
    return Pos(centre[0], -centre[1], surface_z + CUT_OVERSHOOT) * (Plane.XY.rotated((180, 0, 0)) * cone)


def drill(centre: tuple[float, float], diameter: float, mouth_z: float, shoulder_z: float) -> Part:
    """A tap-drill hole from `mouth_z` to its full-diameter shoulder, with the 118 degree point beyond it."""
    direction = 1 if shoulder_z > mouth_z else -1
    point = diameter / 2 / tan(radians(CASE.drill_point_angle / 2))
    start = mouth_z - direction * CUT_OVERSHOOT
    body = cylinder(centre, diameter, tuple(sorted((start, shoulder_z))))
    tip = Cone(diameter / 2, 0.0, point, align=None)
    if direction < 0:
        tip = Plane.XY.rotated((180, 0, 0)) * tip
    return body + Pos(centre[0], -centre[1], shoulder_z) * tip


def d_profile(diameter: float, across_flat: float) -> Sketch:
    """A D-shaft cross-section at the origin, flat toward the rear of the board (model +Y)."""
    radius = diameter / 2
    keep = Pos(0, (across_flat - diameter) / 2) * Rectangle(diameter, across_flat)
    return Circle(radius) & keep


def legend(text: str, size: float, centre: tuple[float, float], read_from_below: bool = False) -> Sketch:
    """Laser-mark artwork at a board position. Text read from below is mirrored left to right."""
    artwork = Text(text, size, font_path=str(LEGEND_FONT))
    if read_from_below:
        artwork = mirror(artwork, Plane.YZ)
    return Pos(centre[0], -centre[1]) * artwork


def overlap_volume(first: Part, second: Part) -> float:
    if not _boxes_overlap(first.bounding_box(), second.bounding_box()):
        return 0.0
    common = first & second
    return 0.0 if common is None else sum(solid.volume for solid in common.solids())


def _boxes_overlap(first, second) -> bool:
    return all(
        low_a < high_b and low_b < high_a
        for low_a, high_a, low_b, high_b in zip(first.min, first.max, second.min, second.max)
    )


def z_extent(part: Part) -> tuple[float, float]:
    bounds = part.bounding_box()
    return bounds.min.Z, bounds.max.Z
