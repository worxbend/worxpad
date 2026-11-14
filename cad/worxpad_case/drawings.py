"""Drawings for the CNC shop and flat artwork, all computed from the model.

For each CNC shell: an A3 sheet (SVG, and PDF through rsvg-convert) with plans from above and below and a
section through the USB-C opening and the display, the overall sizes and pocket sizes measured on the solid, a
table of tapped and countersunk holes whose positions are read off the solid, and the notes. Also a DXF of the
same plan views for JLCCNC (it takes 2D as DWG or DXF, enclosure 1), and the hole tables as CSV.
Flat artwork: lens.dxf, lens_mask.dxf and engraving_underside.dxf (laser mark on the bottom shell).
"""

import csv
import shutil
import subprocess
from dataclasses import dataclass
from math import pi
from pathlib import Path
from xml.sax.saxutils import escape

from build123d import Compound, ExportDXF, GeomType, Part, Plane, Unit, section

from .measure import face_radius
from .parts import bottom_shell, c_seat_z, top_shell
from .small_parts import lens_mask_window, lens_outline
from .solids import legend, rounded, slab
from .spec import BOARD, CASE, CNC, body_span, c_holes, g_holes, k_holes

SHEET = (420.0, 297.0)  # A3 landscape, mm
SCALE = 1.0
FAR = 500.0
CURVE_STEP = 0.6
FONT = "DejaVu Sans, Arial, sans-serif"
SECTION_X = BOARD.usb.x  # the cut runs along Y through the USB-C centre (and the lens and display in the top shell)
SHEET_TITLES = {"top_shell": "TOP SHELL", "bottom_shell": "BOTTOM SHELL"}
SECTION_SHOWS = {"top_shell": "USB-C centre, lens, display", "bottom_shell": "USB-C pocket and notch, cavity, floor"}
SIZE_COLUMN = (210.0, 288.0)  # sheet X of the size table and of the notes column that follows it
SIZE_CHARACTERS = int((SIZE_COLUMN[1] - SIZE_COLUMN[0]) / 1.45)  # 2.5 px DejaVu Sans, about 1.45 mm a character
HOLE_CHARACTERS = int((SIZE_COLUMN[1] - 24.0) / 1.45)  # the hole table starts at sheet X 24 under the notes


@dataclass(frozen=True)
class Frame:
    """Sheet position of a view's origin (board X = 0 and Y = 0 for plans), in sheet mm."""

    x: float
    y: float
    scale: float = SCALE

    def place(self, across: float, down: float) -> tuple[float, float]:
        return self.x + self.scale * across, self.y + self.scale * down


ABOVE = Frame(24.0, 30.0)
BELOW = Frame(175.0, 30.0)  # the projection from below comes out mirrored in X: it is drawn as seen from below
CUT = Frame(24.0, 160.0, 2.0)  # board Y across, Z down from the deck, 2:1


def write_drawings(folder: Path) -> int:
    folder.mkdir(parents=True, exist_ok=True)
    converter = shutil.which("rsvg-convert")
    for name, part in (("top_shell", top_shell(CNC)), ("bottom_shell", bottom_shell(CNC))):
        holes = hole_table(name, part)
        _write_csv(folder / f"{name}_holes.csv", holes)
        drawing = folder / f"{name}.svg"
        drawing.write_text(sheet(name, part, holes))
        _write_dxf(folder / f"{name}.dxf", part)
        if converter:
            subprocess.run([converter, "-f", "pdf", "-o", str(drawing.with_suffix(".pdf")), str(drawing)], check=True)
        print(f"drew {drawing}" + (" and its PDF" if converter else "; rsvg-convert not found, no PDF"))
    for name, artwork in (("lens", lens_outline()), ("lens_mask", lens_mask_window()),
                          ("engraving_underside", laser_mark())):
        exporter = ExportDXF(unit=Unit.MM)
        exporter.add_shape(artwork)
        exporter.write(str(folder / f"{name}.dxf"))
        print(f"drew {folder / f'{name}.dxf'}")
    return 0


def laser_mark():
    """Name and revision on the ramp of the bottom shell, read from below, drawn as seen from above."""
    x, y = CASE.mark_centre
    first, second = CASE.mark_text
    return legend(first, CASE.mark_size, (x, y), read_from_below=True) + \
        legend(second, CASE.mark_size * 0.6, (x, y + CASE.mark_size * 1.2), read_from_below=True)


# ---------------------------------------------------------------------------------------------------------
# Hole table, read off the solid
# ---------------------------------------------------------------------------------------------------------
def hole_table(name: str, part: Part) -> list[dict]:
    """Every tapped or countersunk hole of a shell. Positions come from the vertical round faces of the solid
    whose radius is the tap drill (or the clearance under a countersink); the rest from the hole definitions."""
    rows = []
    if name == "top_shell":
        for holes in (c_holes(), g_holes()):
            for index, (x, y) in enumerate(_found(part, holes.tap_drill, holes.positions)):
                rows.append(_tapped(holes, index, x, y, "from the post end, underside up"))
        k = BOARD.holes.k
        for index, (x, y) in enumerate(_found(part, k.clearance_hole, k.positions)):
            rows.append({"hole": f"K{index + 1}", "x": x, "y": y, "callout":
                         f"clearance {k.clearance_hole} thru lip, csk {k.countersink} x 90 at the plate top (Z "
                         f"{BOARD.stack.plate_top})", "face": "deck side", "screw": k.screw})
    else:
        holes = k_holes()
        for index, (x, y) in enumerate(_found(part, holes.tap_drill, holes.positions)):
            rows.append(_tapped(holes, index, x, y, "from the post top, cavity side"))
        c = BOARD.holes.c
        for index, (x, y) in enumerate(_found(part, CASE.m2_clearance, c.positions)):
            seat = c_seat_z(index, CNC)
            spot = f"spot-face {c.spot_face.diameter} to Z {seat}, " if index == c.spot_face.index else ""
            rows.append({"hole": f"C{index + 1}", "x": x, "y": y, "callout":
                         f"{spot}clearance {CASE.m2_clearance} thru, csk {c.countersink} x 90 at Z {seat}",
                         "face": "underside", "screw": c.screw})
        reset = BOARD.reset
        rows.append({"hole": "RESET", "x": reset.x, "y": reset.y, "callout": f"{reset.pinhole} thru to Z "
                     f"{reset.floor_top_z}", "face": "underside", "screw": "-"})
    return rows


def _tapped(holes, index: int, x: float, y: float, face: str) -> dict:
    mouth = holes.mouth_z[index]
    depth = abs(holes.shoulder_z(index) - mouth)
    return {"hole": f"{holes.name}{index + 1}", "x": x, "y": y,
            "callout": f"{holes.thread}, {holes.tap}, full thread {holes.full_thread:.2f}, drill {holes.tap_drill} x "
                       f"{depth:.2f} (118 deg point to {abs(holes.point_z(index) - mouth):.2f}), mouth Z {mouth}",
            "face": face, "screw": holes.screw}


def _found(part: Part, diameter: float, expected) -> list[tuple[float, float]]:
    """Centres of vertical full-turn holes of this diameter, in the order of `expected` (board X, Y)."""
    centres = []
    for face in part.faces().filter_by(GeomType.CYLINDER):
        axis = face.axis_of_rotation
        if abs(axis.direction.Z) < 0.999 or abs(face_radius(face) - diameter / 2) > 1e-3:
            continue
        if face.area < 2 * pi * diameter / 2 * 0.05:
            continue
        centres.append((round(axis.position.X, 3), round(-axis.position.Y, 3)))
    unique = sorted(set(centres))
    ordered = []
    for x, y in expected:
        match = min(unique, key=lambda c: (c[0] - x) ** 2 + (c[1] - y) ** 2)
        if (match[0] - x) ** 2 + (match[1] - y) ** 2 > 1e-4:
            raise ValueError(f"hole of {diameter} expected at ({x}, {y}) not found on the solid")
        ordered.append(match)
    return ordered


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["hole", "x", "y", "callout", "face", "screw"])
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------------------------------------------------
# Measured sizes
# ---------------------------------------------------------------------------------------------------------
def measured(name: str, part: Part) -> list[tuple[str, float]]:
    """Sizes read off the solid for the sheet: overall, and the opening round a named point at named heights.
    The lens recess is read between the top chamfer (1.0 deep) and the recess floor (1.15 deep): above the
    chamfer bottom the void round the lens joins the chamfer ring and spans the whole shell."""
    bounds = part.bounding_box()
    sizes = [("overall X", bounds.size.X), ("overall Y", bounds.size.Y), ("overall Z", bounds.size.Z)]
    recess = -(BOARD.body.top_chamfer + BOARD.display.lens.recess_depth) / 2
    levels = {
        "top_shell": [("key well at Z -2.0", -2.0), (f"lens recess at Z {recess:.3f}", recess),
                      ("display pocket at Z -3.0", -3.0)],
        "bottom_shell": [("cavity at Z -7.0", -7.0), ("battery pocket at Z -14.0", -14.0)],
    }[name]
    for label, z in levels:
        x, y = _opening(part, z, label)
        if x >= bounds.size.X - 1.0 or y >= bounds.size.Y - 1.0:
            raise ValueError(f"{label}: measured {x:.2f} x {y:.2f}, as large as the part; the probe missed the opening")
        sizes += [(f"{label}, X", x), (f"{label}, Y", y)]
    return sizes


def _opening(part: Part, z: float, label: str) -> tuple[float, float]:
    """Plan size of the empty space at height z that contains the named feature: the outline prism minus the
    part, cut at z. Measuring the void, not the inner wires, still works where a notch opens a wall."""
    void = slab(rounded(body_span(), BOARD.body.corner_radius), (z - 0.5, z + 0.5)) - part
    cut = section(void, section_by=Plane.XY.offset(z))
    target = _target(label)
    sizes = []
    for face in cut.faces():
        bounds = face.bounding_box()
        if bounds.min.X <= target[0] <= bounds.max.X and bounds.min.Y <= -target[1] <= bounds.max.Y:
            sizes.append((bounds.size.X * bounds.size.Y, bounds.size.X, bounds.size.Y))
    if not sizes:
        raise ValueError(f"no opening found for {label} at Z {z}")
    _, x, y = min(sizes)  # the smallest void round the point: a ring round the part also holds it in its box
    return x, y


def _target(label: str) -> tuple[float, float]:
    """A board point inside each measured opening."""
    if "lens" in label or "display" in label:
        lens = BOARD.display.lens
        return (lens.x0 + lens.x1) / 2, (lens.y0 + lens.y1) / 2
    if "battery" in label:
        return (BOARD.battery.pocket_x[0] + BOARD.battery.pocket_x[1]) / 2, sum(BOARD.battery.pocket_y) / 2
    return BOARD.keys.first_x + BOARD.keys.pitch * 1.5, BOARD.keys.first_y + BOARD.keys.pitch * 1.5


# ---------------------------------------------------------------------------------------------------------
# The sheet
# ---------------------------------------------------------------------------------------------------------
def sheet(name: str, part: Part, holes: list[dict]) -> str:
    centre = (BOARD.body.width / 2, -BOARD.body.depth / 2)
    above = _view(part, (centre[0], centre[1], FAR), centre, ABOVE)
    below = _view(part, (centre[0], centre[1], -FAR), centre, BELOW)
    cut = _section(name, part)
    sizes = measured(name, part)
    body = [_frame(SHEET_TITLES[name], "CNC 6061-T6", "1:1"), above, below, cut, *_plan_dimensions(part),
            *_size_table(sizes), *_hole_table(holes, "from datum A"), *_notes(name)]
    return _svg(body)


def _view(part: Part, eye, look_at, frame: Frame) -> str:
    visible, hidden = Compound([part]).project_to_viewport(eye, (0, 1, 0), look_at=(*look_at, 0))
    origin = (look_at[0], look_at[1])

    def path(edges) -> str:
        return " ".join(_polyline([frame.place(x + origin[0], -(y + origin[1])) for x, y in _points(edge)])
                        for edge in edges)

    return f'<path class="hidden" d="{path(hidden)}"/><path class="visible" d="{path(visible)}"/>'


def _section(name: str, part: Part) -> str:
    cut = section(part, section_by=Plane.YZ.offset(SECTION_X))
    paths = []
    for face in cut.faces():
        for wire in [face.outer_wire(), *face.inner_wires()]:
            points = []
            for edge in wire.edges():
                points += [CUT.place(-point.Y, -point.Z) for point in _points3(edge)]
            paths.append(_polyline(points) + " Z")
    label = CUT.place(0.0, -5.0)
    return (f'<path class="cut" d="{" ".join(paths)}"/>'
            f'<text x="{label[0]:.1f}" y="{label[1]:.1f}" class="label">SECTION A-A at X {SECTION_X} '
            f'({SECTION_SHOWS[name]}), rear to the left, 2:1</text>')


def _points(edge, step: float = CURVE_STEP) -> list[tuple[float, float]]:
    steps = 1 if edge.geom_type == GeomType.LINE else max(4, int(edge.length / step))
    return [(p.X, p.Y) for p in (edge.position_at(k / steps) for k in range(steps + 1))]


def _points3(edge, step: float = CURVE_STEP):
    steps = 1 if edge.geom_type == GeomType.LINE else max(4, int(edge.length / step))
    return [edge.position_at(k / steps) for k in range(steps + 1)]


def _polyline(points) -> str:
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in points)


def _plan_dimensions(part: Part) -> list[str]:
    bounds = part.bounding_box()
    width, depth = bounds.size.X, bounds.size.Y
    items = [_dimension(ABOVE.place(0, -6), ABOVE.place(width, -6), f"{width:.2f}"),
             _vertical_dimension(ABOVE.place(-6, 0), ABOVE.place(-6, depth), f"{depth:.2f}"),
             _text(ABOVE.place(0, depth + 8), "PLAN FROM ABOVE, 1:1. Datum A: rear-left outer corner (X right, Y "
                   "toward the front).", "label"),
             _text(BELOW.place(0, depth + 8), "PLAN FROM BELOW, 1:1, seen from below (X runs right to left).",
                   "label")]
    return items


def _dimension(start, end, text: str) -> str:
    (x0, y0), (x1, _) = start, end
    return (f'<path class="dim" d="M{x0:.2f},{y0:.2f} L{x1:.2f},{y0:.2f} M{x0:.2f},{y0 - 2:.2f} L{x0:.2f},{y0 + 2:.2f} '
            f'M{x1:.2f},{y0 - 2:.2f} L{x1:.2f},{y0 + 2:.2f}"/>'
            + _text(((x0 + x1) / 2, y0 - 1.5), text, "dimtext", anchor="middle"))


def _vertical_dimension(start, end, text: str) -> str:
    (x0, y0), (_, y1) = start, end
    return (f'<path class="dim" d="M{x0:.2f},{y0:.2f} L{x0:.2f},{y1:.2f} M{x0 - 2:.2f},{y0:.2f} L{x0 + 2:.2f},{y0:.2f} '
            f'M{x0 - 2:.2f},{y1:.2f} L{x0 + 2:.2f},{y1:.2f}"/>'
            + f'<text x="{x0 - 1.5:.2f}" y="{(y0 + y1) / 2:.2f}" class="dimtext" text-anchor="middle" '
              f'transform="rotate(-90 {x0 - 1.5:.2f} {(y0 + y1) / 2:.2f})">{escape(text)}</text>')


def _size_table(sizes: list[tuple[str, float]]) -> list[str]:
    x, y = SIZE_COLUMN[0], 172.0
    rows = [_text((x, y), "SIZES MEASURED ON THE MODEL (mm)", "head")]
    for index, (label, value) in enumerate(sizes):
        line = f"{label}: {value:.2f}"
        if len(line) > SIZE_CHARACTERS:
            raise ValueError(f"size line '{line}' is longer than {SIZE_CHARACTERS} characters and runs into the notes")
        rows.append(_text((x, y + 4.2 * (index + 1)), line, "small"))
    return rows


def _hole_table(holes: list[dict], datum: str) -> list[str]:
    x, y = 24.0, 236.0
    rows = [_text((x, y), f"HOLES (positions read off the model, {datum})", "head")]
    for index, hole in enumerate(holes):
        line = f"{hole['hole']}  X {hole['x']:.3f}  Y {hole['y']:.3f}  {hole['callout']}; {hole['face']}; {hole['screw']}"
        if len(line) > HOLE_CHARACTERS:
            raise ValueError(f"hole line '{line}' is longer than {HOLE_CHARACTERS} characters and runs into the notes")
        rows.append(_text((x, y + 4.0 * (index + 1)), line, "small"))
    return rows


def _notes(name: str) -> list[str]:
    common = [
        "6061-T6. Bead blast, then Type II sulphuric anodise, black, appearance Strict (enclosure 1).",
        "General tolerance ISO 2768-m (a proposal, not a tested requirement). Break edges 0.05 unless drawn.",
        "Internal corners: R = depth/10 + 0.5 or more; the 2.0 mm tool is needed where R 1.0 or R 1.05 is drawn.",
        "Threads below M5 are plugged during anodise and stay bare (JLCCNC).",
        "Not ordered. Nothing has been milled. Check every fit on the first article before the batch.",
    ]
    per_part = {
        "top_shell": [
            "FIT-CRITICAL: 16 switch openings 14.00 +0.05/-0 AFTER anodise (machine 14.03 +/-0.02); lip 1.15 +/-0.05.",
            "FIT: split face; lens recess 31.4 square R2.1 x 1.15 deep; web 0.80 with 24.8 window.",
            f"Encoder pockets {BOARD.plinth.pocket} square: depth from the split face "
            f"{BOARD.plinth.pocket_ceiling_z - BOARD.body.split_z:.2f} +{CASE.encoder_pocket_depth_tolerance[0]:.2f}/"
            f"-{CASE.encoder_pocket_depth_tolerance[1]:.2f} (ceiling never below Z {BOARD.plinth.pocket_ceiling_z}).",
            "G1, G2 post end faces BARE after anodise (laser-clear or face-mill): case ground (D6).",
            f"G1, G2: BOTTOMING tap, chamfer {CASE.g_thread_run} or less; full thread {CASE.g_full_thread:.2f} is a "
            "minimum (D6, to confirm).",
            "Racking points on inner cavity faces only.",
        ],
        "bottom_shell": [
            "FIT: split face; K post tops at Z -5.20 +0/-0.05; RF slot Y 38.00 to 68.00 +0.10/0, key reliefs 2.00.",
            "Wedge: rear slope and 4.89 degree ramp are single planes; foot pockets square to the ramp (ramp setup).",
            "USB-C skin 0.60 thick in front of the inner pocket: below the 0.8 recommendation, ask on the DFM review.",
            f"Battery pocket and relief rims R{CASE.cell_rim_radius} min, deburred, no sharp edge (power 14 rule 3).",
            "Laser mark from engraving_underside.dxf on the ramp (drawn as seen from above, mirrored).",
        ],
    }[name]
    return _notes_column(per_part + common)


def _notes_column(notes: list[str]) -> list[str]:
    x, y = 290.0, 172.0
    lines = [_text((x, y), "NOTES", "head")]
    for index, note in enumerate(notes):
        lines.append(_text((x, y + 8.5 * (index + 1)), note, "small", wrap=60))
    return lines


def _text(at, text: str, css: str, anchor: str = "start", wrap: int = 0) -> str:
    if not wrap or len(text) <= wrap:
        return f'<text x="{at[0]:.2f}" y="{at[1]:.2f}" class="{css}" text-anchor="{anchor}">{escape(text)}</text>'
    words, lines, current = text.split(), [], ""
    for word in words:
        if len(current) + len(word) + 1 > wrap:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    lines.append(current)
    spans = "".join(f'<tspan x="{at[0]:.2f}" dy="{0 if i == 0 else 3.2}">{escape(line)}</tspan>'
                    for i, line in enumerate(lines))
    return f'<text x="{at[0]:.2f}" y="{at[1]:.2f}" class="{css}">{spans}</text>'


def _frame(title: str, material: str, scale: str) -> str:
    w, h = SHEET
    return (f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" class="frame"/>'
            f'<rect x="{w - 140}" y="{h - 28}" width="130" height="18" class="frame"/>'
            + _text((w - 136, h - 20), f"worxpad {title}, revision {BOARD.meta.revision}, {material}", "head")
            + _text((w - 136, h - 14), f"A3, {scale}, mm. Generated by cad/build.py draw; do not edit.", "small"))


def _svg(body: list[str]) -> str:
    w, h = SHEET
    style = (f"text{{font-family:{FONT};fill:#111}} .label{{font-size:3px}} .head{{font-size:3.2px;font-weight:bold}}"
             ".small{font-size:2.5px} .dimtext{font-size:2.6px} .frame{fill:none;stroke:#111;stroke-width:0.5}"
             ".visible{fill:none;stroke:#111;stroke-width:0.25} .hidden{fill:none;stroke:#999;stroke-width:0.12;"
             "stroke-dasharray:1,0.7} .cut{fill:#d9dce1;stroke:#111;stroke-width:0.25;fill-rule:evenodd}"
             ".dim{fill:none;stroke:#2050a0;stroke-width:0.18}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">'
            f'<style>{style}</style><rect width="{w}" height="{h}" fill="white"/>{"".join(body)}</svg>\n')


def _write_dxf(path: Path, part: Part) -> None:
    """Plan from above and the section, as lines, for the JLCCNC 2D drawing slot. The PDF carries the notes."""
    centre = (BOARD.body.width / 2, -BOARD.body.depth / 2)
    visible, _ = Compound([part]).project_to_viewport((centre[0], centre[1], FAR), (0, 1, 0), look_at=(*centre, 0))
    exporter = ExportDXF(unit=Unit.MM)
    exporter.add_layer("plan")
    exporter.add_shape(visible, layer="plan")
    exporter.write(str(path))
