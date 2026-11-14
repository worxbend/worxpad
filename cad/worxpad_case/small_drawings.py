"""Drawings of the small CNC parts, computed from the model on the same A3 sheet as the shells (drawings.py).

knob       turned 6061-T6: plan from above, section through the axis, views from below and from the rear; the
           bore steps and the set-screw hole read off the solid; knob_holes.csv (S1, the M2 thread)
rf_insert  black POM: elevations from outside and inside, plan from above, section through the antenna pocket;
           bar, keys and pocket read off the solid

Each part is drawn as exported to exports/cnc (the left knob and the insert in the assembly frame): an SVG, its
PDF through rsvg-convert, and a DXF of two views for the JLCCNC 2D slot. The PDF carries the notes.
"""

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from build123d import BoundBox, Compound, ExportDXF, GeomType, Part, Plane, Pos, Unit, Vector, section

from .drawings import (CURVE_STEP, FAR, SIZE_CHARACTERS, _dimension, _frame, _hole_table, _notes_column, _points,
                       _points3, _polyline, _size_table, _svg, _text, _vertical_dimension, _write_csv)
from .measure import face_radius
from .small_parts import case_parts
from .solids import box, cylinder
from .spec import BOARD, CASE, CNC

ABOVE, BELOW = ((0, 0, 1), (0, 1, 0)), ((0, 0, -1), (0, 1, 0))
FROM_REAR, FROM_OUTSIDE, FROM_INSIDE = ((0, 1, 0), (0, 0, 1)), ((1, 0, 0), (0, 0, 1)), ((-1, 0, 0), (0, 0, 1))
PLAN_ALONG_Y = ((0, 0, 1), (-1, 0, 0))  # from above, the insert's length running across the sheet
GENERAL = [
    "General tolerance ISO 2768-m (a proposal, not a tested requirement). Break edges 0.05 unless drawn.",
    "Not ordered. Nothing has been milled. Check every fit on the first article before the batch.",
]
HOLE_ROW_Y = 236.0
STEP = CURVE_STEP / 5  # curve sampling at 4:1 and 5:1, as fine on paper as the 1:1 shell sheets
NOTE_CHARACTERS = 112  # two lines of the notes column; a third runs into the next note
KNOB_DATUM = "X, Y of the mouth from the knob axis, Y toward the front"


@dataclass(frozen=True)
class View:
    """One view as polylines in its own plane: u to the right, v up, model mm."""

    label: str
    outlines: list[list[tuple[float, float]]]  # visible edges, or the closed wires of a section
    hidden: list[list[tuple[float, float]]]
    is_section: bool
    extent: tuple[float, float, float, float]  # u0, u1, v0, v1 of the exact edges, not of the sampled polylines


def write_small_drawings(folder: Path) -> int:
    folder.mkdir(parents=True, exist_ok=True)
    parts = case_parts(CNC)
    knob, insert = parts["knob_left"], parts["rf_insert"]
    holes = knob_holes(knob)
    _write_csv(folder / "knob_holes.csv", holes)
    sheets = {"knob": (knob, knob_sheet(knob, holes), (ABOVE, FROM_REAR)),
              "rf_insert": (insert, insert_sheet(insert), (FROM_OUTSIDE, PLAN_ALONG_Y))}
    converter = shutil.which("rsvg-convert")
    for name, (part, drawing_text, dxf_views) in sheets.items():
        drawing = folder / f"{name}.svg"
        drawing.write_text(drawing_text)
        _write_dxf(folder / f"{name}.dxf", part, dxf_views)
        if converter:
            subprocess.run([converter, "-f", "pdf", "-o", str(drawing.with_suffix(".pdf")), str(drawing)], check=True)
        print(f"drew {drawing}" + (" and its PDF" if converter else "; rsvg-convert not found, no PDF"))
    return 0


# ---------------------------------------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------------------------------------
def projected(part: Part, label: str, direction) -> View:
    visible, hidden = _projection(part, direction)
    return View(label, [_points(edge, STEP) for edge in visible], [_points(edge, STEP) for edge in hidden], False,
                _plane_extent(Compound(visible)))


def _projection(part: Part, direction):
    (look, up), centre = direction, part.bounding_box().center()
    eye = centre + Vector(*look) * FAR
    return Compound([part]).project_to_viewport(tuple(eye), up, look_at=tuple(centre))


def sectioned(part: Part, label: str, plane: Plane) -> View:
    cut = section(part, section_by=plane)
    outlines = []
    for face in cut.faces():
        for wire in [face.outer_wire(), *face.inner_wires()]:
            local = [plane.to_local_coords(point) for edge in wire.edges() for point in _points3(edge, STEP)]
            outlines.append([(point.X, point.Y) for point in local])
    return View(label, outlines, [], True, _plane_extent(plane.to_local_coords(cut)))


def _plane_extent(shape) -> tuple[float, float, float, float]:
    bounds = shape.bounding_box(optimal=True)
    return bounds.min.X, bounds.max.X, bounds.min.Y, bounds.max.Y


def placed(view: View, at: tuple[float, float], scale: float) -> list[str]:
    """The view with its top-left corner at `at` (sheet mm), its overall sizes and its label under it."""
    u0, u1, v0, v1 = view.extent

    def path(lines) -> str:
        return " ".join(_polyline([(at[0] + scale * (u - u0), at[1] + scale * (v1 - v)) for u, v in line])
                        + (" Z" if view.is_section else "") for line in lines)

    right, bottom = at[0] + scale * (u1 - u0), at[1] + scale * (v1 - v0)
    shapes = (f'<path class="cut" d="{path(view.outlines)}"/>' if view.is_section else
              f'<path class="hidden" d="{path(view.hidden)}"/><path class="visible" d="{path(view.outlines)}"/>')
    return [shapes,
            _dimension((at[0], at[1] - 6), (right, at[1] - 6), f"{u1 - u0:.2f}"),
            _vertical_dimension((at[0] - 6, at[1]), (at[0] - 6, bottom), f"{v1 - v0:.2f}"),
            _text((at[0], bottom + 7), view.label, "label", wrap=34)]


def _write_dxf(path: Path, part: Part, directions) -> None:
    """The visible edges of the given views side by side, 1:1, one layer each, for the JLCCNC 2D slot."""
    exporter = ExportDXF(unit=Unit.MM)
    cursor = 0.0
    for index, direction in enumerate(directions):
        visible = Compound(_projection(part, direction)[0])
        bounds = visible.bounding_box()
        layer = f"view{index + 1}"
        exporter.add_layer(layer)
        exporter.add_shape(Pos(cursor - bounds.min.X, -bounds.min.Y) * visible, layer=layer)
        cursor += bounds.size.X + 10.0
    exporter.write(str(path))


def sheet(title: tuple[str, str, str], views: list[str], sizes: list[tuple[str, float]], holes: list[dict],
          notes: list[str]) -> str:
    too_long = [note for note in notes if len(note) > NOTE_CHARACTERS]
    if too_long:
        raise ValueError(f"notes longer than {NOTE_CHARACTERS} characters overlap the next one: {too_long}")
    hole_rows = (_hole_table(holes, KNOB_DATUM) if holes else
                 [_text((24.0, HOLE_ROW_Y), "HOLES: none. No thread.", "head")])
    return _svg([_frame(*title), *views, *_size_table(sizes), *hole_rows, *_notes_column(notes)])


# ---------------------------------------------------------------------------------------------------------
# Knob
# ---------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Step:
    """One step of the bore, read off the solid: Z above the rim and its plan size."""

    z0: float
    z1: float
    across_x: float
    across_y: float

    @property
    def is_round(self) -> bool:
        return abs(self.across_x - self.across_y) < 0.01


def knob_sheet(part: Part, holes: list[dict]) -> str:
    scale, axis = 5.0, part.bounding_box().center()
    cut = Plane(origin=(axis.X, axis.Y, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    views = [*placed(projected(part, "PLAN FROM ABOVE, 5:1 (flat toward the rear, up the sheet)", ABOVE),
                     (30, 35), scale),
             *placed(sectioned(part, "SECTION A-A on the axis, front to the left, 5:1", cut), (110, 35), scale),
             *placed(projected(part, "FROM BELOW, 5:1 (X runs right to left)", BELOW), (190, 35), scale),
             *placed(projected(part, "FROM THE REAR, 5:1: S1 on the flat side", FROM_REAR), (270, 35), scale)]
    steps = bore_steps(part)
    hole = _set_screw(part)
    sizes = _overall(part) + _step_sizes(steps) + [
        ("S1 tap drill diameter", 2 * hole.radius), ("S1 centre above the rim", hole.z),
        ("S1 wall, outside to the flat", hole.wall)]
    return sheet(("KNOB", "CNC 6061-T6 turned", "5:1"), views, sizes, holes, _knob_notes(part, steps, hole))


def bore_steps(part: Part) -> list[Step]:
    """The bore between consecutive flat levels of the knob (rim, steps, bore top, top face), from the rim up."""
    bounds = part.bounding_box()
    levels = sorted({round(face.center().Z, 4) for face in part.faces().filter_by(GeomType.PLANE)
                     if abs(face.normal_at().Z) > 0.999})
    steps = []
    for z0, z1 in zip(levels, levels[1:]):
        size = _bore_at(part, (z0 + z1) / 2)
        if size:
            steps.append(Step(round(z0 - bounds.min.Z, 4), round(z1 - bounds.min.Z, 4), *size))
    if len(steps) != 3:
        raise ValueError(f"knob: {len(steps)} bore steps read off the solid, expected counterbore, relief, D-bore")
    return steps


def _bore_at(part: Part, z: float) -> tuple[float, float] | None:
    """Plan size of the empty space round the knob axis at height z, or None where the knob is solid."""
    bounds = part.bounding_box()
    axis = bounds.center()
    void = cylinder((axis.X, -axis.Y), bounds.size.X + 2.0, (z - 0.5, z + 0.5)) - part
    sizes = []
    for face in section(void, section_by=Plane.XY.offset(z)).faces():
        face_box = face.bounding_box()
        if face_box.min.X <= axis.X <= face_box.max.X and face_box.min.Y <= axis.Y <= face_box.max.Y:
            sizes.append((face_box.size.X * face_box.size.Y, face_box.size.X, face_box.size.Y))
    _, x, y = min(sizes)  # the ring round the outside also holds the axis in its box; it is the largest
    return None if x > bounds.size.X else (x, y)


def _step_sizes(steps: list[Step]) -> list[tuple[str, float]]:
    sizes = []
    for step in steps:
        heights = f"Z {step.z0:.2f} to {step.z1:.2f}"
        if step.is_round:
            sizes.append((f"round bore {heights}, diameter", step.across_x))
        else:
            sizes += [(f"D-bore {heights}, diameter", step.across_x),
                      (f"D-bore {heights}, across the flat", step.across_y)]
    return sizes


@dataclass(frozen=True)
class SetScrew:
    """The tapped side hole, read off the solid; positions from the knob axis and the rim."""

    across: float  # axis offset in X from the knob axis
    entry_y: float  # board Y (toward the front) of the mouth on the outside, from the knob axis
    z: float
    radius: float
    wall: float


def _set_screw(part: Part) -> SetScrew:
    radius, bounds = CASE.m2_tap_drill / 2, part.bounding_box()
    faces = [face for face in part.faces().filter_by(GeomType.CYLINDER)
             if abs(face.axis_of_rotation.direction.Y) > 0.999 and abs(_axis_distance(face) - radius) < 1e-3]
    if not faces:
        raise ValueError(f"knob: no side hole of dia. {CASE.m2_tap_drill} found on the solid")
    centre, hole = bounds.center(), Compound(faces).bounding_box()
    mouth = hole.max.Y if abs(hole.max.Y - centre.Y) > abs(hole.min.Y - centre.Y) else hole.min.Y
    axis = faces[0].axis_of_rotation.position
    return SetScrew(round(axis.X - centre.X, 3), round(-(mouth - centre.Y), 3), round(axis.Z - bounds.min.Z, 3),
                    _axis_distance(faces[0]), round(hole.size.Y, 3))


def _axis_distance(face) -> float:
    """Radius of a cylinder face of any axis direction."""
    axis = face.axis_of_rotation
    return (face.position_at(0.5, 0.5) - axis.position).cross(axis.direction).length


def knob_holes(part: Part) -> list[dict]:
    hole = _set_screw(part)
    return [{"hole": "S1", "x": hole.across, "y": hole.entry_y, "callout":
             f"{CASE.knob_set_screw_thread}, drill {2 * hole.radius:.2f} thru the {hole.wall:.2f} wall to the bore, "
             f"square to the flat, centre {hole.z:.2f} above the rim", "face": "side, rear",
             "screw": CASE.knob_set_screw}]


def _knob_notes(part: Part, steps: list[Step], hole: SetScrew) -> list[str]:
    counterbore, relief, bore = steps
    bounds, fit = part.bounding_box(), CASE.knob_bore_tolerance
    diameter_tolerance, depth_tolerance = CASE.knob_counterbore_tolerance
    return [
        f"S1: {CASE.knob_set_screw_thread} square to the flat, toward the rear, centre {hole.z:.2f} above the rim. "
        "Mask it during anodise.",
        f"FIT, after anodise: D-bore {bore.across_x:.2f} +{fit:.2f}/0, flat {bore.across_y:.2f} +{fit:.2f}/0 "
        f"across, to Z {bore.z1:.2f}: slip fit on the encoder shaft.",
        f"FIT: round relief {relief.across_x:.2f} +{fit:.2f}/0, Z {relief.z0:.2f} to {relief.z1:.2f}. Counterbore "
        f"{counterbore.across_x:.2f} +{diameter_tolerance:.2f}/0 x {counterbore.z1:.2f} +{depth_tolerance:.2f}/0.",
        "Anodise grows the bore by about 0.01 to 0.02: mask the bore or allow for it. Z is above the rim.",
        f"Outside {bounds.size.X:.2f}, height {bounds.size.Z:.2f}, top edge R{CASE.knob_top_radius} as modelled. "
        "Cosmetic: outside and top face.",
        "6061-T6 turned. Bead blast, Type II anodise, black, appearance Strict; same batch and colour as the shells.",
        "Two per set, both this part. The STEP is the left knob in the assembly frame.",
        *GENERAL,
    ]


# ---------------------------------------------------------------------------------------------------------
# RF window insert
# ---------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class InsertSizes:
    bar_length: float
    key_diameter: float
    key_from_outside: float
    pocket: BoundBox  # the antenna pocket, read off the solid
    pocket_radius: float
    skin: float  # outer face to the pocket floor


def insert_sheet(part: Part) -> str:
    scale, found = 4.0, insert_sizes(part)
    middle = found.pocket.center().Y
    cut = Plane(origin=(0, middle, 0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    views = [*placed(projected(part, "FROM OUTSIDE (cosmetic face), rear to the right, 4:1", FROM_OUTSIDE),
                     (30, 35), scale),
             *placed(projected(part, "FROM INSIDE (antenna pocket), rear to the left, 4:1", FROM_INSIDE),
                     (30, 85), scale),
             *placed(projected(part, "PLAN FROM ABOVE, outer face down, rear to the right, 4:1", PLAN_ALONG_Y),
                     (30, 135), scale),
             *placed(sectioned(part, "SECTION B-B at the pocket centre, outer face to the right, 4:1", cut),
                     (200, 35), scale)]
    return sheet(("RF WINDOW INSERT", "CNC black POM", "4:1"), views, _insert_size_rows(part, found), [],
                 _insert_notes(found))


def insert_sizes(part: Part) -> InsertSizes:
    bounds = part.bounding_box()
    thickness = BOARD.rf_window.insert[1]
    strip = part & box((bounds.min.X + 0.1, bounds.min.X + 0.3), (-bounds.max.Y, -bounds.min.Y),
                       (bounds.min.Z, bounds.max.Z))
    bar = strip.bounding_box()
    if abs(bar.size.Y - BOARD.rf_window.insert[0]) > 1e-3 or abs(bounds.size.X - thickness) > 1e-3:
        raise ValueError(f"RF insert: bar {bar.size.Y:.3f} x {bounds.size.X:.3f} read off the solid, board.toml "
                         f"gives {BOARD.rf_window.insert[0]} x {thickness}")
    solid_bar = box((bounds.min.X, bounds.max.X), (-bar.max.Y, -bar.min.Y), (bounds.min.Z, bounds.max.Z))
    pocket = (solid_bar - part).bounding_box()
    keys = [face for face in part.faces().filter_by(GeomType.CYLINDER)
            if abs(face.axis_of_rotation.direction.Z) > 0.999]
    corners = [face for face in part.faces().filter_by(GeomType.CYLINDER)
               if abs(face.axis_of_rotation.direction.X) > 0.999]
    if not keys or not corners:
        raise ValueError("RF insert: keys or pocket corners not found on the solid")
    return InsertSizes(bar.size.Y, 2 * face_radius(keys[0]), bounds.max.X - keys[0].axis_of_rotation.position.X,
                       pocket, _axis_distance(corners[0]), bounds.max.X - pocket.max.X)


def _insert_size_rows(part: Part, found: InsertSizes) -> list[tuple[str, float]]:
    bounds, pocket = part.bounding_box(), found.pocket
    rows = [("overall X (thickness)", bounds.size.X), ("overall Y (length over the keys)", bounds.size.Y),
            ("overall Z (height)", bounds.size.Z), ("bar length", found.bar_length),
            ("key diameter", found.key_diameter), ("key centre from the outer face", found.key_from_outside),
            ("antenna pocket, length", pocket.size.Y), ("antenna pocket, height", pocket.size.Z),
            ("antenna pocket, top below the bar top", bounds.max.Z - pocket.max.Z),
            ("antenna pocket, depth from the inner face", pocket.max.X - bounds.min.X),
            ("outer skin at the pocket", found.skin),
            ("pocket corner radius", found.pocket_radius)]
    too_long = [label for label, value in rows if len(f"{label}: {value:.2f}") > SIZE_CHARACTERS]
    if too_long:
        raise ValueError(f"size lines too long for the column: {too_long}")
    return rows


def _insert_notes(found: InsertSizes) -> list[str]:
    window = BOARD.rf_window
    bar_upper, bar_lower = CASE.rf_insert_length_tolerance
    slot_upper, slot_lower = CASE.rf_slot_length_tolerance
    slot = window.y1 - window.y0
    play = (slot - slot_lower - (found.bar_length + bar_upper), slot + slot_upper - (found.bar_length - bar_lower))
    if play[0] < 0:
        raise ValueError(f"RF insert: bar {found.bar_length:.2f} +{bar_upper} can be longer than the slot {slot:.2f}")
    pocket = found.pocket
    return [
        "Black POM (Delrin), as machined. No paint, no plating, no metal of any kind: it is the radio window.",
        f"FIT: bar length {found.bar_length:.2f} +{bar_upper:.2f}/-{bar_lower:.2f}. It slides into the {slot:.2f} "
        f"+{slot_upper:.2f}/{slot_lower:.0f} slot of the bottom shell: play {play[0]:.2f} to {play[1]:.2f}.",
        f"Keys: dia. {found.key_diameter:.2f} half-round on each end, centre {found.key_from_outside:.2f} from the "
        f"outer face; the slot has dia. {window.relief_diameter:.2f} reliefs.",
        f"Antenna pocket from the inner face, {pocket.size.Y:.2f} long, corners R{found.pocket_radius:.2f}, outer "
        f"skin {found.skin:.2f}. Machine as modelled.",
        "Cosmetic face: the outer face, flush with the case wall. The STEP is in the assembly frame.",
        *GENERAL,
    ]


def _overall(part: Part) -> list[tuple[str, float]]:
    size = part.bounding_box().size
    return [("overall X", size.X), ("overall Y", size.Y), ("overall Z", size.Z)]
