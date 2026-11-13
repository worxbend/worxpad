#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Arithmetic self-check of board.toml. Standard library only.

It checks the numbers against each other, not against the world: holes inside the board, parts inside the
outline, keys on pitch, no two bodies overlapping in plan where they share a Z range, the battery pocket
against the wedge, the stack-up order, the RF bay, the named clearances and the pin map. A pass here says
the spec is self-consistent. It says nothing about a real part.

Bodies are plan rectangles or circles with a Z range. Bodies in the same group may nest (a keycap around
its own switch); every other pair must not overlap where both the plan shapes and the Z ranges overlap.
Touching faces do not count as overlap.
"""
from __future__ import annotations

import math
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EPS = 1e-6


# --------------------------------------------------------------------------------------------------------
# Plan geometry
# --------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Rect:
    x0: float
    y0: float
    x1: float
    y1: float

    @staticmethod
    def centred(cx: float, cy: float, sx: float, sy: float) -> "Rect":
        return Rect(cx - sx / 2, cy - sy / 2, cx + sx / 2, cy + sy / 2)


@dataclass(frozen=True)
class Circle:
    cx: float
    cy: float
    r: float


Shape = Rect | Circle


def _rect_point_distance(rect: Rect, x: float, y: float) -> float:
    dx = max(rect.x0 - x, 0.0, x - rect.x1)
    dy = max(rect.y0 - y, 0.0, y - rect.y1)
    return math.hypot(dx, dy)


def gap(a: Shape, b: Shape) -> float:
    """Edge-to-edge distance in plan; negative or zero means the shapes touch or overlap."""
    if isinstance(a, Rect) and isinstance(b, Rect):
        dx = max(a.x0 - b.x1, b.x0 - a.x1)
        dy = max(a.y0 - b.y1, b.y0 - a.y1)
        if dx > 0 and dy > 0:
            return math.hypot(dx, dy)
        return max(dx, dy)
    if isinstance(a, Circle) and isinstance(b, Circle):
        return math.hypot(a.cx - b.cx, a.cy - b.cy) - a.r - b.r
    rect, circle = (a, b) if isinstance(a, Rect) else (b, a)
    inside = rect.x0 <= circle.cx <= rect.x1 and rect.y0 <= circle.cy <= rect.y1
    if inside:
        return -circle.r
    return _rect_point_distance(rect, circle.cx, circle.cy) - circle.r


def bounds(shape: Shape) -> Rect:
    if isinstance(shape, Rect):
        return shape
    return Rect(shape.cx - shape.r, shape.cy - shape.r, shape.cx + shape.r, shape.cy + shape.r)


def inside_rounded(shape: Shape, outline: Rect, radius: float, margin: float = 0.0) -> bool:
    """Shape lies inside a rounded rectangle, at least `margin` from its edge."""
    box = bounds(shape)
    if (box.x0 < outline.x0 + margin - EPS or box.x1 > outline.x1 - margin + EPS
            or box.y0 < outline.y0 + margin - EPS or box.y1 > outline.y1 - margin + EPS):
        return False
    corners = [(outline.x0 + radius, outline.y0 + radius), (outline.x1 - radius, outline.y0 + radius),
               (outline.x0 + radius, outline.y1 - radius), (outline.x1 - radius, outline.y1 - radius)]
    for cx, cy in corners:
        for px, py in _extreme_points(shape):
            in_corner_x = (px < cx) if cx < (outline.x0 + outline.x1) / 2 else (px > cx)
            in_corner_y = (py < cy) if cy < (outline.y0 + outline.y1) / 2 else (py > cy)
            if in_corner_x and in_corner_y and math.hypot(px - cx, py - cy) > radius - margin + EPS:
                return False
    return True


def point_in_rounded(px: float, py: float, outline: Rect, radius: float) -> bool:
    """Point lies inside a rounded rectangle (boundary included)."""
    if not (outline.x0 - EPS <= px <= outline.x1 + EPS and outline.y0 - EPS <= py <= outline.y1 + EPS):
        return False
    cx = min(max(px, outline.x0 + radius), outline.x1 - radius)
    cy = min(max(py, outline.y0 + radius), outline.y1 - radius)
    return math.hypot(px - cx, py - cy) <= radius + EPS


def rounded_points(outline: Rect, radius: float, per_corner: int = 24) -> list[tuple[float, float]]:
    """Points on the boundary of a rounded rectangle, corners sampled finely."""
    centres = [(outline.x1 - radius, outline.y1 - radius, 0.0), (outline.x0 + radius, outline.y1 - radius, 90.0),
               (outline.x0 + radius, outline.y0 + radius, 180.0), (outline.x1 - radius, outline.y0 + radius, 270.0)]
    points = []
    for cx, cy, start in centres:
        for i in range(per_corner + 1):
            angle = math.radians(start + 90.0 * i / per_corner)
            points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return points


def grow(rect: Rect, by: float) -> Rect:
    return Rect(rect.x0 - by, rect.y0 - by, rect.x1 + by, rect.y1 + by)


def _extreme_points(shape: Shape) -> list[tuple[float, float]]:
    if isinstance(shape, Rect):
        return [(shape.x0, shape.y0), (shape.x1, shape.y0), (shape.x0, shape.y1), (shape.x1, shape.y1)]
    steps = 16
    return [(shape.cx + shape.r * math.cos(2 * math.pi * i / steps),
             shape.cy + shape.r * math.sin(2 * math.pi * i / steps)) for i in range(steps)]


@dataclass(frozen=True)
class Body:
    name: str
    shape: Shape
    z0: float  # lower face
    z1: float  # upper face
    group: str
    on_pcb: bool = True  # mounted on the PCB: must lie inside the PCB outline


# --------------------------------------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------------------------------------
class Report:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.passes = 0

    def check(self, name: str, ok: bool, detail: str) -> None:
        if ok:
            self.passes += 1
            print(f"check_spec: PASS {name}: {detail}")
        else:
            self.failures.append(name)
            print(f"check_spec: FAIL {name}: {detail}")


# --------------------------------------------------------------------------------------------------------
# Spec access
# --------------------------------------------------------------------------------------------------------
def load(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def key_centres(spec: dict) -> list[tuple[int, int, float, float]]:
    keys = spec["keys"]
    return [(row, col, keys["first_x"] + col * keys["pitch"], keys["first_y"] + row * keys["pitch"])
            for row in range(keys["rows"]) for col in range(keys["columns"])]


def pcb_rect(spec: dict) -> Rect:
    pcb = spec["pcb"]
    return Rect(pcb["x0"], pcb["y0"], pcb["x1"], pcb["y1"])


def body_rect(spec: dict) -> Rect:
    return Rect(0.0, 0.0, spec["body"]["width"], spec["body"]["depth"])


def thickness_at(spec: dict, y: float) -> float:
    """Body thickness, deck to underside, on the wedge planes (no scoops)."""
    wedge, depth = spec["wedge"], spec["body"]["depth"]
    if y <= wedge["apex_y"]:
        return wedge["rear_height"] + (wedge["apex_height"] - wedge["rear_height"]) * y / wedge["apex_y"]
    span = depth - wedge["apex_y"]
    return wedge["apex_height"] + (wedge["front_height"] - wedge["apex_height"]) * (y - wedge["apex_y"]) / span


def min_thickness(spec: dict, y0: float, y1: float) -> tuple[float, float]:
    """Thinnest point of the wedge over [y0, y1]. Both pieces are linear, so it is at an end."""
    candidates = [(thickness_at(spec, y), y) for y in (y0, y1)]
    return min(candidates)


def rf_bay_rect(spec: dict) -> Rect:
    pcb, bay, module = spec["pcb"], spec["rf_bay"], spec["module"]
    half = bay["length"] / 2
    return Rect(pcb["x1"] - bay["inset"], module["centre_y"] - half, spec["body"]["width"],
                module["centre_y"] + half)


def module_rect(spec: dict) -> Rect:
    module, pcb = spec["module"], spec["pcb"]
    x1 = pcb["x1"] - module["antenna_inset"]
    return Rect(x1 - module["length"], module["centre_y"] - module["width"] / 2, x1,
                module["centre_y"] + module["width"] / 2)


def keepout_rect(spec: dict) -> Rect:
    pcb, module = spec["pcb"], spec["module"]
    half = module["keepout"]["length"] / 2
    return Rect(pcb["x1"] - module["keepout"]["depth"], module["centre_y"] - half, pcb["x1"], module["centre_y"] + half)


def antenna_strip_rect(spec: dict) -> Rect:
    rect = module_rect(spec)
    return Rect(rect.x1 - spec["module"]["antenna_strip"], rect.y0, rect.x1, rect.y1)


def usb_rect(spec: dict) -> Rect:
    usb = spec["usb"]
    return Rect(usb["x"] - usb["width"] / 2, usb["front_y"], usb["x"] + usb["width"] / 2, usb["front_y"] + usb["length"])


def socket_pad_rects(spec: dict) -> list[Rect]:
    pad = spec["keys"]["footprint"]
    return [Rect.centred(x + px, y + py, *pad["socket_pad_size"])
            for _, _, x, y in key_centres(spec) for px, py in pad["socket_pads"]]


def ground_rings(spec: dict) -> list[Circle]:
    g = spec["holes"]["g"]
    return [Circle(x, y, g["ring"] / 2) for x, y in g["positions"]]


def display_pocket(spec: dict) -> tuple[Rect, list[Circle]]:
    """Display module pocket as its rectangle (to the bend line) and the two rear T-bone reliefs."""
    pocket = spec["display"]["pocket"]
    rect = Rect(pocket["x0"], pocket["y0"], pocket["x1"], pocket["bend_y1"])
    r = pocket["rear_relief_diameter"] / 2
    return rect, [Circle(rect.x0 + r, rect.y0, r), Circle(rect.x1 - r, rect.y0, r)]


def part_rect(part: dict) -> Rect:
    return Rect.centred(part["x"], part["y"], *part["size"])


def counterbores(spec: dict) -> list[tuple[str, Circle]]:
    buttons = spec["buttons"]
    return [(f"button_{side}_counterbore", Circle(buttons[side]["x"], buttons[side]["y"], buttons["counterbore"] / 2))
            for side in ("right", "left")]


def plinth_pockets(spec: dict) -> list[tuple[str, Rect]]:
    size = spec["plinth"]["pocket"]
    return [(f"plinth_pocket_{side}", Rect.centred(spec["encoders"][side]["x"], spec["encoders"][side]["y"], size, size))
            for side in ("right", "left")]


# --------------------------------------------------------------------------------------------------------
# Bodies
# --------------------------------------------------------------------------------------------------------
def build_bodies(spec: dict) -> list[Body]:
    bodies: list[Body] = []
    pcb_top, pcb_bottom = spec["pcb"]["top_z"], spec["pcb"]["bottom_z"]
    keys, keepout, diode = spec["keys"], spec["keys"]["keepout"], spec["keys"]["diode"]
    stack = spec["stack"]

    for row, col, x, y in key_centres(spec):
        group = f"key_r{row}c{col}"
        bodies += [
            Body(f"{group}_housing", Rect.centred(x, y, keys["housing"], keys["housing"]), pcb_top, stack["plate_top"], group),
            Body(f"{group}_flange", Rect.centred(x, y, keys["flange"], keys["flange"]), stack["plate_top"], keys["collar_z"], group),
            Body(f"{group}_cap", Rect.centred(x, y, keys["cap_base"], keys["cap_base"]), keys["cap_skirt_pressed_z"],
                 keys["cap_height"], group, on_pcb=False),
        ]
        zx0, zy0, zx1, zy1 = keepout["socket_zone"]
        bodies.append(Body(f"{group}_socket", Rect(x + zx0, y + zy0, x + zx1, y + zy1),
                           pcb_bottom - keepout["socket_depth"], pcb_bottom, group))
        bodies.append(Body(f"{group}_centre_post", Circle(x, y, keepout["centre_post_diameter"] / 2),
                           pcb_bottom - keepout["centre_post_depth"], pcb_bottom, group))
        tx, ty = keys["footprint"]["third_hole"]
        bodies.append(Body(f"{group}_third_leg", Circle(x + tx, y + ty, keepout["third_leg_diameter"] / 2),
                           pcb_bottom - keepout["third_leg_depth"], pcb_bottom, group))
        dx, dy = diode["offset"]
        bodies.append(Body(f"diode_r{row}c{col}", Rect.centred(x + dx, y + dy, *diode["size"]),
                           pcb_bottom - diode["height"], pcb_bottom, f"diode_r{row}c{col}"))

    enc = spec["encoders"]
    knobs = spec["knobs"]
    for side in ("right", "left"):
        ex, ey, group = enc[side]["x"], enc[side]["y"], f"encoder_{side}"
        half = enc["pin_half_span"] + 0.5
        below = pcb_bottom - enc["pin_depth"]
        bodies += [
            Body(f"{group}_body", Rect.centred(ex, ey, *enc["body"]), pcb_top, enc["body_top_z"], group),
            Body(f"{group}_pins_rear", Rect(ex - half, enc["pin_row_rear_y"] - 0.5, ex + half, enc["pin_row_rear_y"] + 0.5),
                 below, pcb_bottom, group),
            Body(f"{group}_pins_front", Rect(ex - half, enc["pin_row_front_y"] - 0.5, ex + half, enc["pin_row_front_y"] + 0.5),
                 below, pcb_bottom, group),
            Body(f"{group}_leg_a", Rect.centred(ex - enc["leg_offset"], ey, 2.1, 2.0), below, pcb_bottom, group),
            Body(f"{group}_leg_b", Rect.centred(ex + enc["leg_offset"], ey, 2.1, 2.0), below, pcb_bottom, group),
            Body(f"knob_{side}", Circle(ex, ey, knobs["diameter"] / 2), knobs["rim_pressed_z"], knobs["top_z"],
                 group, on_pcb=False),
        ]
        rc = enc["filter"]
        for index, (dx, dy) in enumerate(rc["offsets"]):
            bodies.append(Body(f"{group}_filter_{index}", Rect.centred(ex + dx, ey + dy, *rc["size"]),
                               pcb_bottom - rc["height"], pcb_bottom, f"{group}_filter_{index}"))

    # The plinth is pocketed from below over each encoder, so only its roof spans the full plan.
    plinth = spec["plinth"]
    bodies.append(Body("plinth_roof", Rect(plinth["x0"], plinth["y0"], plinth["x1"], plinth["y1"]),
                       plinth["pocket_ceiling_z"], plinth["top_z"], "plinth", on_pcb=False))

    buttons = spec["buttons"]
    for side in ("right", "left"):
        bx, by, group = buttons[side]["x"], buttons[side]["y"], f"button_{side}"
        bodies += [
            Body(f"{group}_switch", Rect.centred(bx, by, *buttons["switch_body"]), pcb_top, buttons["switch_top_z"], group),
            Body(f"{group}_cap", Circle(bx, by, buttons["cap_flange"] / 2), buttons["cap_bottom_z"],
                 buttons["cap_top_z"], group, on_pcb=False),
        ]

    display = spec["display"]
    lens, module, conn, flex = display["lens"], display["module"], display["connector"], display["flex"]
    bodies += [
        Body("display_lens", Rect(lens["x0"], lens["y0"], lens["x1"], lens["y1"]), stack["lens_underside"],
             stack["deck"], "display", on_pcb=False),
        Body("display_module", Rect(module["x0"], module["y0"], module["x1"], module["y1"]), module["back_z"],
             module["top_z"], "display", on_pcb=False),
        Body("display_flex_bend", Rect(flex["x0"], flex["y0"], flex["x1"], flex["y1"]), flex["bottom_z"],
             module["top_z"], "display", on_pcb=False),
        Body("display_connector", Rect(conn["x0"], conn["y_back"], conn["x1"], conn["y_entry"]), pcb_top,
             conn["top_z"], "display"),
    ]

    bodies.append(Body("module", module_rect(spec), pcb_bottom - spec["module"]["height"], pcb_bottom, "rf"))
    bay = spec["rf_bay"]
    bodies.append(Body("rf_bay", rf_bay_rect(spec), bay["floor_top_z"], bay["top_z"], "rf", on_pcb=False))
    window, width, wall = spec["rf_window"], spec["body"]["width"], spec["body"]["wall"]
    insert_length = window["insert"][0]
    centre = (window["y0"] + window["y1"]) / 2
    bodies.append(Body("rf_insert", Rect(width - wall, centre - insert_length / 2, width, centre + insert_length / 2),
                       window["bottom_z"] + 0.05, window["top_z"], "rf", on_pcb=False))

    flash = spec["flash"]
    bodies.append(Body("flash", Rect.centred(flash["x"], flash["y"], *flash["size"]), pcb_bottom - flash["height"],
                       pcb_bottom, "flash"))

    usb = spec["usb"]
    bodies.append(Body("usb_receptacle", Rect(usb["x"] - usb["width"] / 2, usb["front_y"], usb["x"] + usb["width"] / 2,
                                              usb["front_y"] + usb["length"]), usb["bottom_z"], usb["top_z"], "usb",
                       on_pcb=False))

    sw = spec["power_switch"]
    sw_body = Rect(sw["x"] - sw["body"][0] / 2, sw["body_y0"], sw["x"] + sw["body"][0] / 2, sw["body_y0"] + sw["body"][1])
    bodies += [
        Body("power_switch_body", sw_body, pcb_bottom - sw["height"], pcb_bottom, "power_switch"),
        Body("power_switch_actuator", Rect(sw["x"] - sw["actuator"][0] / 2, sw["body_y0"] - sw["actuator"][1],
                                           sw["x"] + sw["actuator"][0] / 2, sw["body_y0"]),
             pcb_bottom - sw["height"], pcb_bottom, "power_switch", on_pcb=False),
    ]

    reset = spec["reset"]
    bodies.append(Body("reset", Rect.centred(reset["x"], reset["y"], *reset["body"]), pcb_bottom - reset["height"],
                       pcb_bottom, "reset"))

    swd = spec["swd"]
    pads = Rect.centred(swd["x"], swd["y"], *swd["size"])
    zone = Rect(pads.x0 - swd["low_zone"], pads.y0 - swd["low_zone"], pads.x1 + swd["low_zone"], pads.y1 + swd["low_zone"])
    bodies += [
        Body("swd_pads", pads, pcb_bottom - 0.1, pcb_bottom, "swd"),
        Body("swd_low_zone", zone, spec["stack"]["rf_bay_floor_top"], pcb_bottom - 1.0, "swd", on_pcb=False),
    ]

    battery = spec["battery"]
    conn = battery["connector"]
    conn_rect = Rect.centred(conn["x"], conn["y"], *conn["body"])
    mouth = Rect(conn_rect.x0 - conn["mouth_clear"], conn_rect.y0, conn_rect.x0, conn_rect.y1)
    bodies += [
        Body("battery_connector", conn_rect, pcb_bottom - conn["height"], pcb_bottom, "battery_connector"),
        Body("battery_plug_space", mouth, pcb_bottom - conn["height"], pcb_bottom, "battery_connector", on_pcb=False),
        Body("cell", cell_rect(spec), cell_bottom_z(spec), cell_top_z(spec), "cell", on_pcb=False),
    ]

    for name, part in spec["power"]["parts"].items():
        bodies.append(Body(f"power_{name}", part_rect(part), pcb_bottom - part["height"], pcb_bottom, f"power_{name}"))

    k = spec["holes"]["k"]
    for index, (x, y) in enumerate(k["positions"], start=1):
        group = f"k{index}"
        bodies += [
            Body(f"{group}_top", Circle(x, y, k["keepout_top"] / 2), pcb_top, stack["plate_top"], group),
            Body(f"{group}_bottom", Circle(x, y, k["keepout_bottom"] / 2), stack["key_field_floor_top"], pcb_bottom, group),
        ]
    c = spec["holes"]["c"]
    for index, ((x, y), z0) in enumerate(zip(c["positions"], c["post_bottom_z"]), start=1):
        bodies.append(Body(f"c{index}", Circle(x, y, c["keepout"] / 2), z0, stack["split"], f"c{index}"))
    g = spec["holes"]["g"]
    for index, (x, y) in enumerate(g["positions"], start=1):
        group = f"g{index}"
        bodies += [
            Body(f"{group}_post", Circle(x, y, g["keepout_top"] / 2), pcb_top, stack["split"], group),
            Body(f"{group}_head", Circle(x, y, g["head"] / 2), g["head_bottom_z"], pcb_bottom, group),
        ]
    return bodies


def cell_rect(spec: dict) -> Rect:
    battery = spec["battery"]
    clearance = battery["pocket_clearance"]
    x0, y0 = battery["pocket_x"][0] + clearance, battery["pocket_y"][0] + clearance
    return Rect(x0, y0, x0 + battery["cell_size"][0], y0 + battery["cell_size"][1])


def cell_top_z(spec: dict) -> float:
    return spec["stack"]["key_field_floor_top"] - spec["battery"]["insulation"]


def cell_bottom_z(spec: dict) -> float:
    battery = spec["battery"]
    return cell_top_z(spec) - battery["cell_size"][2] - battery["swelling"]


# --------------------------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------------------------
def check_keys(spec: dict, report: Report) -> None:
    keys = spec["keys"]
    centres = key_centres(spec)
    xs = sorted({round(x, 6) for _, _, x, _ in centres})
    ys = sorted({round(y, 6) for _, _, _, y in centres})
    steps = [b - a for a, b in zip(xs, xs[1:])] + [b - a for a, b in zip(ys, ys[1:])]
    on_pitch = len(centres) == keys["rows"] * keys["columns"] and all(abs(s - keys["pitch"]) < EPS for s in steps)
    report.check("keys on pitch", on_pitch,
                 f"{len(centres)} keys, {len(xs)} columns x {len(ys)} rows, every step {keys['pitch']} mm")

    well = Rect(keys["well_x0"], keys["well_y0"], keys["well_x1"], keys["well_y1"])
    half = keys["cap_base"] / 2
    margins = [min(x - half - well.x0, well.x1 - x - half, y - half - well.y0, well.y1 - y - half) for _, _, x, y in centres]
    smallest = min(margins)
    report.check("keycaps inside the key well", smallest >= keys["cap_to_well_min"] - EPS,
                 f"smallest cap-to-well gap {smallest:.2f} mm, limit {keys['cap_to_well_min']}")
    cap_gap = keys["pitch"] - keys["cap_base"]
    report.check("keycap gap", cap_gap > 0, f"{cap_gap:.2f} mm between neighbouring caps")
    grid_centre = keys["first_x"] + (keys["columns"] - 1) * keys["pitch"] / 2
    well_centre = (well.x0 + well.x1) / 2
    report.check("key grid centred in the well", abs(grid_centre - well_centre) < 0.05,
                 f"grid centre x {grid_centre:.3f}, well centre x {well_centre:.3f}")


def check_outline(spec: dict, report: Report) -> None:
    body, pcb, case = spec["body"], spec["pcb"], spec["case"]
    inner = Rect(body["wall"], body["wall"], body["width"] - body["wall"], body["depth"] - body["wall"])
    gaps = {"left": pcb["x0"] - inner.x0, "right": inner.x1 - pcb["x1"], "rear": pcb["y0"] - inner.y0,
            "front": inner.y1 - pcb["y1"]}
    smallest = min(gaps.values())
    detail = ", ".join(f"{side} {value:.2f}" for side, value in gaps.items())
    report.check("PCB inside the cavity", smallest >= case["pcb_gap_min"] - EPS,
                 f"gap to the inner wall: {detail} mm, limit {case['pcb_gap_min']}")
    report.check("body fits the printer bed", body["width"] <= case["bed"] and body["depth"] <= case["bed"],
                 f"{body['width']} x {body['depth']} mm on a {case['bed']} mm bed")

    for tongue in pcb["tongues"]:
        ok = tongue["y0"] >= 0 and pcb["x0"] < tongue["x0"] < tongue["x1"] < pcb["x1"] and tongue["y0"] < pcb["y0"]
        report.check(f"PCB tongue {tongue['name']}", ok,
                     f"x {tongue['x0']} to {tongue['x1']}, reaches Y {tongue['y0']} (body face at Y 0)")
    usb, sw = spec["usb"], spec["power_switch"]
    usb_tongue = next(t for t in pcb["tongues"] if t["name"] == "usb")
    sw_tongue = next(t for t in pcb["tongues"] if t["name"] == "power_switch")
    usb_margin = min(usb_tongue["x0"] - usb["pocket_x"][0], usb["pocket_x"][1] - usb_tongue["x1"])
    report.check("USB tongue inside the wall pocket", usb_margin > 0,
                 f"{usb_margin:.2f} mm each side in the {usb['pocket_x'][1] - usb['pocket_x'][0]:.1f} mm pocket")
    sw_margin = min(sw_tongue["x0"] - sw["notch_x"][0], sw["notch_x"][1] - sw_tongue["x1"])
    report.check("switch tongue inside its wall notch", sw_margin > 0, f"{sw_margin:.2f} mm each side")
    notch = pcb["notches"][0]
    usb_rect = Rect(usb["x"] - usb["width"] / 2, usb["front_y"], usb["x"] + usb["width"] / 2, usb["front_y"] + usb["length"])
    report.check("USB receptacle inside its board notch",
                 notch["x0"] < usb_rect.x0 and usb_rect.x1 < notch["x1"] and usb_rect.y1 < notch["y1"],
                 f"receptacle x {usb_rect.x0:.2f} to {usb_rect.x1:.2f}, notch x {notch['x0']} to {notch['x1']}; "
                 f"receptacle ends Y {usb_rect.y1:.2f}, notch ends Y {notch['y1']}")
    usb_open = usb["notch_x"][0] < usb_rect.x0 and usb_rect.x1 < usb["notch_x"][1]
    report.check("USB receptacle inside its wall notch", usb_open,
                 f"receptacle x {usb_rect.x0:.2f} to {usb_rect.x1:.2f}, notch x {usb['notch_x'][0]} to {usb['notch_x'][1]}")
    contact_ok = usb["notch_z"][1] < usb["contact_z"] < usb["notch_z"][0] and usb["notch_z"][0] <= body["split_z"]
    report.check("rear openings wholly in the bottom shell", contact_ok,
                 f"USB contact Z {usb['contact_z']}, notch Z {usb['notch_z'][0]} to {usb['notch_z'][1]}, split {body['split_z']}")


def on_pcb(shape: Shape, spec: dict, margin: float = 0.0) -> bool:
    """Inside the PCB outline: the rounded main board or one of the tongues, and not in a notch."""
    pcb = spec["pcb"]
    box = bounds(shape)
    main = pcb_rect(spec)
    if inside_rounded(shape, main, pcb["corner_radius"], margin):
        inside = True
    else:
        inside = False
        for tongue in pcb["tongues"]:
            region = Rect(tongue["x0"] + margin, tongue["y0"] + margin, tongue["x1"] - margin, main.y1 - margin)
            if (box.x0 >= region.x0 - EPS and box.x1 <= region.x1 + EPS and box.y0 >= region.y0 - EPS
                    and box.y1 <= region.y1 + EPS):
                inside = True
    for notch in pcb["notches"]:
        if gap(shape, Rect(notch["x0"], notch["y0"], notch["x1"], notch["y1"])) < -EPS:
            return False
    return inside


def check_holes(spec: dict, report: Report) -> None:
    holes = spec["holes"]
    rows = []
    for kind, keepout_key in (("k", "keepout_bottom"), ("c", "keepout"), ("g", "ring")):
        for index, (x, y) in enumerate(holes[kind]["positions"], start=1):
            rows.append((f"{kind.upper()}{index}", Circle(x, y, holes[kind][keepout_key] / 2)))
    bad = [name for name, circle in rows if not on_pcb(circle, spec)]
    report.check("every hole inside the board", not bad,
                 f"{len(rows)} holes with their keep-out rings inside the PCB outline" if not bad else f"outside: {bad}")
    feet = spec["feet"]
    foot_shapes = [Circle(x, y, feet["pocket_diameter"] / 2) for x, y in feet["positions"]]
    feet_ok = all(inside_rounded(c, body_rect(spec), spec["body"]["corner_radius"], 1.0) for c in foot_shapes)
    report.check("feet inside the underside", feet_ok, f"{len(foot_shapes)} foot pockets at least 1.0 mm from the edge")
    c = holes["c"]
    c_seats = [Circle(x, y, c["countersink"] / 2) for x, y in c["positions"]]
    spot = c["spot_face"]
    sx, sy = c["positions"][spot["index"]]
    c_seats[spot["index"]] = Circle(sx, sy, spot["diameter"] / 2)
    seat_gap = min(gap(f, o) for f in foot_shapes for o in c_seats)
    report.check("feet clear of the C countersinks and the C2 spot-face", seat_gap >= c["foot_wall_min"] - EPS,
                 f"smallest wall {seat_gap:.2f} mm, limit {c['foot_wall_min']} (guess)")
    pin = Circle(spec["reset"]["x"], spec["reset"]["y"], spec["reset"]["pinhole"] / 2)
    pin_gap = min(gap(f, pin) for f in foot_shapes)
    report.check("feet clear of the reset pinhole", pin_gap > 0, f"smallest gap {pin_gap:.2f} mm")
    underside = -thickness_at(spec, sy)
    floor_bottom = c["post_bottom_z"][spot["index"]] - 0.05 - c["local_floor"]
    report.check("C2 spot-face restores the enclosure seat",
                 abs(spot["floor_z"] - floor_bottom) < EPS and spot["floor_z"] > underside,
                 f"underside Z {underside:.2f} at Y {sy}, spot-face floor Z {spot['floor_z']} "
                 f"({spot['floor_z'] - underside:.2f} deep), post end {c['post_bottom_z'][spot['index']]} - 0.05 - "
                 f"{c['local_floor']} floor = {floor_bottom:.2f}")
    wedge, scoops = spec["wedge"], spec["wedge"]["scoops"]
    width = spec["body"]["width"]
    scoop_rects = [Rect(0, 0, scoops["width"], scoops["end_y"]), Rect(width - scoops["width"], 0, width, scoops["end_y"])]
    split = []
    for (x, y), foot in zip(feet["positions"], foot_shapes):
        crosses_apex = foot.cy - foot.r - feet["apex_margin"] < wedge["apex_y"] < foot.cy + foot.r + feet["apex_margin"]
        in_scoop = any(gap(foot, s) < feet["apex_margin"] for s in scoop_rects)
        if crosses_apex or in_scoop:
            split.append(f"({x}, {y})")
    report.check("every foot pocket lies on one underside plane", not split,
                 f"pockets at least {feet['apex_margin']} mm from the apex line Y {wedge['apex_y']} and the scoops"
                 if not split else f"crossing a plane edge: {split}")


def check_parts_inside(spec: dict, bodies: list[Body], report: Report) -> None:
    outside_pcb = [b.name for b in bodies if b.on_pcb and not on_pcb(b.shape, spec)]
    report.check("every PCB-mounted part inside the PCB outline", not outside_pcb,
                 f"{sum(b.on_pcb for b in bodies)} bodies checked" if not outside_pcb else f"outside: {outside_pcb}")
    outside_body = [b.name for b in bodies if not inside_rounded(b.shape, body_rect(spec), spec["body"]["corner_radius"])]
    report.check("every part inside the body outline", not outside_body,
                 f"{len(bodies)} bodies checked" if not outside_body else f"outside: {outside_body}")

    pad = spec["keys"]["footprint"]
    sx, sy = pad["socket_pad_size"]
    smallest = math.inf
    for _, _, x, y in key_centres(spec):
        for px, py in pad["socket_pads"]:
            shape = Rect.centred(x + px, y + py, sx, sy)
            main = pcb_rect(spec)
            smallest = min(smallest, shape.x0 - main.x0, main.x1 - shape.x1, shape.y0 - main.y0, main.y1 - shape.y1)
    limit = spec["case"]["copper_to_edge"]
    report.check("socket pads clear of the board edge", smallest >= limit - EPS,
                 f"smallest pad-to-edge {smallest:.3f} mm, limit {limit} (guess)")


def check_overlaps(bodies: list[Body], report: Report) -> None:
    clashes = []
    for i, a in enumerate(bodies):
        for b in bodies[i + 1:]:
            if a.group == b.group:
                continue
            z_overlap = min(a.z1, b.z1) - max(a.z0, b.z0)
            if z_overlap <= EPS:
                continue
            if gap(a.shape, b.shape) < -EPS:
                clashes.append(f"{a.name} / {b.name}")
    pairs = len(bodies) * (len(bodies) - 1) // 2
    report.check("no two bodies overlap in plan where they share a Z range", not clashes,
                 f"{len(bodies)} bodies, {pairs} pairs" if not clashes else "; ".join(clashes))


def check_stack(spec: dict, report: Report) -> None:
    levels = list(spec["stack"].items())
    disorder = [f"{a} {za} above {b} {zb}" for (a, za), (b, zb) in zip(levels, levels[1:]) if zb > za + EPS]
    report.check("stack-up listed top to bottom", not disorder,
                 f"{len(levels)} levels" if not disorder else "; ".join(disorder))
    stack, pcb, display = spec["stack"], spec["pcb"], spec["display"]
    pairs = {
        "pcb_top": pcb["top_z"], "pcb_bottom": pcb["bottom_z"], "split": spec["body"]["split_z"],
        "web_underside": display["web"]["underside_z"], "display_module_top": display["module"]["top_z"],
        "display_module_back": display["module"]["back_z"], "rf_bay_top": spec["rf_bay"]["top_z"],
        "rf_bay_floor_top": spec["rf_bay"]["floor_top_z"], "pocket_floor_top": spec["battery"]["pocket_floor_top_z"],
        "battery_relief_floor_top": spec["battery"]["relief"]["floor_top_z"],
        "control_column_floor_top": spec["floors"]["control_column_top_z"],
        "key_field_floor_top": spec["floors"]["key_field_top_z"], "fpc_connector_top": display["connector"]["top_z"],
        "front_underside": -spec["wedge"]["front_height"], "apex_underside": -spec["wedge"]["apex_height"],
        "knob_top": spec["knobs"]["top_z"], "plinth_top": spec["plinth"]["top_z"],
        "rf_slot_bottom": spec["rf_window"]["bottom_z"], "g_head_underside": spec["holes"]["g"]["head_bottom_z"],
        "cell_bottom": cell_bottom_z(spec), "insulation_bottom": cell_top_z(spec),
    }
    mismatch = [f"{name} {stack[name]} vs {value}" for name, value in pairs.items() if abs(stack[name] - value) > EPS]
    report.check("stack-up agrees with the part sections", not mismatch,
                 f"{len(pairs)} levels cross-checked" if not mismatch else "; ".join(mismatch))
    web = display["lens"]["recess_depth"] + display["web"]["thickness"]
    report.check("display web", abs(-web - display["web"]["underside_z"]) < EPS and display["web"]["thickness"] >= spec["case"]["min_metal_wall"],
                 f"recess {display['lens']['recess_depth']} + web {display['web']['thickness']} = underside Z {-web:.2f}")
    flex_ok = display["flex"]["bottom_z"] < display["connector"]["top_z"] + 1.0 and display["module"]["back_z"] > display["connector"]["top_z"]
    report.check("display module above its connector", flex_ok,
                 f"module back Z {display['module']['back_z']}, connector top Z {display['connector']['top_z']}")


def check_wedge(spec: dict, report: Report) -> None:
    wedge, depth = spec["wedge"], spec["body"]["depth"]
    ramp = math.degrees(math.atan((wedge["apex_height"] - wedge["front_height"]) / (depth - wedge["apex_y"])))
    rear = math.degrees(math.atan((wedge["apex_height"] - wedge["rear_height"]) / wedge["apex_y"]))
    report.check("wedge shape", 4.0 < ramp < 6.0 and 25.0 < rear < 35.0,
                 f"ramp {ramp:.2f} degrees (GLYF 4.95), rear slope {rear:.1f} degrees (GLYF 29), "
                 f"apex {wedge['apex_height']} at Y {wedge['apex_y']}, front {wedge['front_height']}, rear {wedge['rear_height']}")

    battery, case = spec["battery"], spec["case"]
    floor_needed = -battery["pocket_floor_top_z"] + case["min_floor"]
    thinnest, at_y = min_thickness(spec, *battery["pocket_y"])
    report.check("battery pocket depth against the wedge", thinnest >= floor_needed - EPS,
                 f"pocket floor top Z {battery['pocket_floor_top_z']} + {case['min_floor']} floor needs {floor_needed:.2f}; "
                 f"thinnest body over Y {battery['pocket_y'][0]} to {battery['pocket_y'][1]} is {thinnest:.2f} at Y {at_y}")
    relief = battery["relief"]
    floor_needed = -relief["floor_top_z"] + case["min_floor"]
    thinnest, at_y = min_thickness(spec, *relief["y"])
    report.check("battery connector relief against the wedge", thinnest >= floor_needed - EPS,
                 f"needs {floor_needed:.2f}, thinnest {thinnest:.2f} at Y {at_y}")
    bay = rf_bay_rect(spec)
    floor_needed = -spec["rf_bay"]["floor_top_z"] + case["min_floor"]
    thinnest, at_y = min_thickness(spec, bay.y0, bay.y1)
    report.check("RF bay floor against the wedge", thinnest >= floor_needed - EPS,
                 f"needs {floor_needed:.2f}, thinnest {thinnest:.2f} at Y {at_y}")
    scoops = spec["wedge"]["scoops"]
    scoop_floor = -scoops["underside_z"] - case["min_floor"]
    report.check("floors above the flank scoops", -spec["floors"]["control_column_top_z"] <= scoop_floor + EPS
                 and -spec["floors"]["key_field_top_z"] <= scoop_floor + EPS,
                 f"scoop underside Z {scoops['underside_z']} leaves room for floors down to Z {-scoop_floor:.2f}")
    slot_wall = min_thickness(spec, spec["rf_window"]["y0"], spec["rf_window"]["y1"])[0] + spec["rf_window"]["bottom_z"]
    report.check("wall under the RF slot", spec["rf_window"]["y0"] > scoops["end_y"] and slot_wall >= case["min_floor"],
                 f"slot starts Y {spec['rf_window']['y0']} behind the scoop end Y {scoops['end_y']}; {slot_wall:.2f} mm of wall below it")

    feet = spec["feet"]
    pocket = Rect(battery["pocket_x"][0], battery["pocket_y"][0], battery["pocket_x"][1], battery["pocket_y"][1])
    worst = math.inf
    for x, y in feet["positions"]:
        r = feet["pocket_diameter"] / 2
        if gap(Circle(x, y, r), pocket) < 0:
            thinnest = min_thickness(spec, max(y - r, pocket.y0), min(y + r, pocket.y1))[0]
            worst = min(worst, thinnest + battery["pocket_floor_top_z"] - feet["pocket_depth"])
    report.check("floor under foot pockets below the battery", worst >= case["min_floor"],
                 f"thinnest {worst:.2f} mm" if worst < math.inf else "no foot under the pocket")


def check_battery(spec: dict, report: Report) -> None:
    battery, case, scoops = spec["battery"], spec["case"], spec["wedge"]["scoops"]
    pocket = Rect(battery["pocket_x"][0], battery["pocket_y"][0], battery["pocket_x"][1], battery["pocket_y"][1])
    cell = cell_rect(spec)
    margins = [cell.x0 - pocket.x0, pocket.x1 - cell.x1, cell.y0 - pocket.y0, pocket.y1 - cell.y1]
    report.check("cell inside its pocket", min(margins) >= battery["pocket_clearance"] - EPS,
                 f"cell {battery['cell_size'][0]} x {battery['cell_size'][1]} in {pocket.x1 - pocket.x0:.1f} x "
                 f"{pocket.y1 - pocket.y0:.1f}, smallest side clearance {min(margins):.2f}")
    depth = cell_top_z(spec) - battery["cell_size"][2] - battery["swelling"] - battery["foam"]
    report.check("pocket depth holds cell, swelling and foam", depth >= battery["pocket_floor_top_z"] - EPS,
                 f"stack reaches Z {depth:.2f}, floor top Z {battery['pocket_floor_top_z']}")
    k = spec["holes"]["k"]
    k_gap = min(gap(Circle(x, y, k["keepout_bottom"] / 2), pocket) for x, y in k["positions"])
    report.check("pocket clear of the K posts", k_gap >= -EPS, f"smallest gap {k_gap:.2f} mm to the {k['keepout_bottom']} keep-out")
    left_scoop = Rect(0, 0, scoops["width"], scoops["end_y"])
    right_scoop = Rect(spec["body"]["width"] - scoops["width"], 0, spec["body"]["width"], scoops["end_y"])
    s_gap = min(gap(pocket, left_scoop), gap(pocket, right_scoop))
    report.check("pocket clear of the flank scoops", s_gap >= case["min_floor"] - EPS, f"{s_gap:.2f} mm of wall")
    bay_gap = gap(pocket, rf_bay_rect(spec))
    report.check("pocket outside the RF bay", bay_gap > 0, f"{bay_gap:.2f} mm")
    conn = battery["connector"]
    conn_rect = Rect.centred(conn["x"], conn["y"], *conn["body"])
    relief = Rect(battery["relief"]["x"][0], battery["relief"]["y"][0], battery["relief"]["x"][1], battery["relief"]["y"][1])
    mouth = Rect(conn_rect.x0 - conn["mouth_clear"], conn_rect.y0, conn_rect.x0, conn_rect.y1)
    in_relief = all(relief.x0 - EPS <= r.x0 and r.x1 <= relief.x1 + EPS and relief.y0 - EPS <= r.y0 and r.y1 <= relief.y1 + EPS
                    for r in (conn_rect, Rect(max(mouth.x0, pocket.x1), mouth.y0, mouth.x1, mouth.y1)))
    joined = relief.x0 <= pocket.x1 + EPS and relief.y0 >= pocket.y0 and relief.y1 <= pocket.y1
    report.check("battery connector and plug space in the floor relief", in_relief and joined,
                 f"connector x {conn_rect.x0:.2f} to {conn_rect.x1:.2f}, {conn['mouth_clear']} mm in front of the mouth")
    floor_ok = battery["relief"]["floor_top_z"] <= spec["pcb"]["bottom_z"] - conn["height"] - 0.3 + EPS
    report.check("floor under the battery connector", floor_ok,
                 f"connector underside Z {spec['pcb']['bottom_z'] - conn['height']:.2f}, floor top Z {battery['relief']['floor_top_z']}")
    rf_gap = gap(conn_rect, rf_bay_rect(spec))
    report.check("battery connector outside the RF bay", rf_gap > 0, f"{rf_gap:.2f} mm")


def check_rf(spec: dict, report: Report) -> None:
    pcb, module, bay = spec["pcb"], spec["module"], spec["rf_bay"]
    rect = module_rect(spec)
    inset = pcb["x1"] - rect.x1
    tol = pcb["outline_tolerance"]
    low, high = module["inset_window"]
    report.check("antenna inset inside its window after the outline tolerance",
                 inset - tol >= low - EPS and inset + tol <= high + EPS,
                 f"inset {inset:.2f} +/- {tol} = {inset - tol:.2f} to {inset + tol:.2f} mm, window {low} to {high} (D24)")
    keep = keepout_rect(spec)
    strip = antenna_strip_rect(spec)
    covers = keep.x0 <= strip.x0 + EPS and keep.y0 < strip.y0 and keep.y1 > strip.y1 and keep.x1 >= rect.x1
    report.check("copper keep-out covers the antenna strip", covers,
                 f"keep-out x {keep.x0:.2f} to {keep.x1:.2f}, Y {keep.y0:.2f} to {keep.y1:.2f}; strip x {strip.x0:.2f} "
                 f"to {strip.x1:.2f}")
    depth_rule = module["antenna_strip"] + module["antenna_inset"]
    first_pads = rect.x1 - module["antenna_strip"]
    report.check("copper keep-out stops at the first pad column",
                 abs(module["keepout"]["depth"] - depth_rule) < EPS and keep.x0 >= first_pads - EPS,
                 f"depth {module['keepout']['depth']} = strip {module['antenna_strip']} + inset {module['antenna_inset']}; "
                 f"keep-out starts X {keep.x0:.2f}, pads start X {first_pads:.2f}")
    bay_rule = module["antenna_inset"] + module["antenna_strip"] + bay["margin"]
    report.check("RF bay depth follows the antenna end", bay["inset"] >= bay_rule - EPS,
                 f"bay {bay['inset']} mm from the board edge, antenna end {module['antenna_inset']} + strip "
                 f"{module['antenna_strip']} + margin {bay['margin']} = {bay_rule:.2f}")
    lens = spec["display"]["module"]
    lcd_gap = pcb["x1"] - lens["x1"]
    report.check("LCD at least the bay depth from the board edge", lcd_gap >= bay["inset"] - EPS,
                 f"{lcd_gap:.2f} mm, rule {bay['inset']} (mcu-radio 7.3.3)")
    window = spec["rf_window"]
    centre = (window["y0"] + window["y1"]) / 2
    length = window["y1"] - window["y0"]
    report.check("RF slot centred on the module", abs(centre - module["centre_y"]) < EPS and length >= 30.0 - EPS,
                 f"slot Y {window['y0']} to {window['y1']} ({length:.1f} mm), module centre Y {module['centre_y']}")
    shell_ok = bay["top_z"] <= -2.80 + EPS and window["top_z"] >= -5.20 - EPS and window["bottom_z"] <= -11.70 + EPS
    report.check("RF slot and bay heights", shell_ok,
                 f"bay Z {bay['top_z']} to {bay['floor_top_z']}, slot Z {window['top_z']} to {window['bottom_z']}")


def check_clearances(spec: dict, report: Report) -> None:
    case = spec["case"]
    posts = []
    for kind in ("c", "g"):
        holes = spec["holes"][kind]
        posts += [(f"{kind.upper()}{i}", Circle(x, y, holes["post"] / 2)) for i, (x, y) in enumerate(holes["positions"], start=1)]
    lens = spec["display"]["lens"]
    lens_recess = Rect.centred((lens["x0"] + lens["x1"]) / 2, (lens["y0"] + lens["y1"]) / 2, lens["recess"], lens["recess"])
    module_pocket, reliefs = display_pocket(spec)
    # Pockets in the top shell with the Z range they occupy; the shell ends at the split plane.
    split, stack = spec["body"]["split_z"], spec["stack"]
    voids = ([(name, shape, split, stack["button_counterbore_top"]) for name, shape in counterbores(spec)]
             + [(name, shape, split, spec["plinth"]["pocket_ceiling_z"]) for name, shape in plinth_pockets(spec)]
             + [("lens_recess", lens_recess, stack["lens_recess_floor"], stack["deck"]),
                ("display_pocket", module_pocket, split, stack["web_underside"]),
                ("rf_pocket", rf_bay_rect(spec), split, spec["rf_bay"]["top_z"])]
             + [(f"display_relief_{i}", c, split, stack["web_underside"]) for i, c in enumerate(reliefs)])
    worst = min(((gap(post, void), f"{pname} to {vname}") for pname, post in posts for vname, void, _, _ in voids))
    report.check("screw posts clear of top-shell pockets", worst[0] >= case["post_to_void"] - EPS,
                 f"smallest wall {worst[0]:.2f} mm ({worst[1]}), limit {case['post_to_void']}")
    walls = [(gap(a, b), f"{an} to {bn}") for i, (an, a, az0, az1) in enumerate(voids)
             for bn, b, bz0, bz1 in voids[i + 1:]
             if min(az1, bz1) - max(az0, bz0) > EPS and not (an.startswith("display") and bn.startswith("display"))]
    worst_wall = min(walls)
    report.check("walls between top-shell pockets", worst_wall[0] >= case["min_metal_wall"] - EPS,
                 f"smallest wall {worst_wall[0]:.2f} mm ({worst_wall[1]}), limit {case['min_metal_wall']} (JLCCNC)")
    inserts = []
    for kind in ("c", "g"):
        inserts += [(f"{kind.upper()}{i}", Circle(x, y, case["fdm_insert_hole"] / 2))
                    for i, (x, y) in enumerate(spec["holes"][kind]["positions"], start=1)]
    worst_insert = min((gap(hole, void), f"{name} to {vname}") for name, hole in inserts for vname, void, _, _ in voids)
    report.check("FDM insert holes clear of top-shell pockets", worst_insert[0] >= case["fdm_insert_wall"] - EPS,
                 f"smallest wall {worst_insert[0]:.2f} mm ({worst_insert[1]}), limit {case['fdm_insert_wall']} "
                 f"(Ø{case['fdm_insert_hole']} hole)")
    g_bay = min(gap(Circle(x, y, spec["holes"]["g"]["keepout_top"] / 2), rf_bay_rect(spec))
                for x, y in spec["holes"]["g"]["positions"])
    report.check("ground screws outside the RF bay", g_bay > 0, f"smallest gap {g_bay:.2f} mm")
    check_plinth(spec, report)
    check_display_pocket(spec, module_pocket, reliefs, report)
    check_countersink_web(spec, report)
    check_usb_behind_encoders(spec, report)


def check_plinth(spec: dict, report: Report) -> None:
    enc, plinth, case = spec["encoders"], spec["plinth"], spec["case"]
    body_side = (plinth["pocket"] - max(enc["body"])) / 2
    tab_side = (plinth["pocket"] - (enc["tab_span"] + enc["tab_tolerance"])) / 2
    head = plinth["pocket_ceiling_z"] - enc["body_top_z"]
    report.check("encoder bodies inside the plinth pockets", min(body_side, tab_side, head) > 0,
                 f"worst case {tab_side:.2f} mm per side at the mounting tabs ({enc['tab_span']} + {enc['tab_tolerance']}), "
                 f"{body_side:.2f} mm at the nominal body, {head:.2f} mm under the ceiling at the body maximum")
    outline = Rect(plinth["x0"], plinth["y0"], plinth["x1"], plinth["y1"])
    wall = case["plinth_wall"]
    outside = []
    for name, pocket in plinth_pockets(spec):
        walled = rounded_points(grow(pocket, wall), plinth["pocket_corner_radius"] + wall)
        if not all(point_in_rounded(px, py, outline, plinth["corner_radius"]) for px, py in walled):
            outside.append(name)
    reach = math.hypot(plinth["pocket"] / 2 - plinth["pocket_corner_radius"],
                       plinth["pocket"] / 2 - plinth["pocket_corner_radius"]) + plinth["pocket_corner_radius"]
    report.check("plinth pockets keep their wall inside the plinth outline", not outside,
                 f"pocket R{plinth['pocket_corner_radius']} plus {wall} wall inside the R{plinth['corner_radius']} plinth; "
                 f"pocket corner reaches {reach:.2f} mm from the axis" if not outside else f"wall broken at {outside}")


def check_display_pocket(spec: dict, rect: Rect, reliefs: list[Circle], report: Report) -> None:
    display = spec["display"]
    module, pocket = display["module"], display["pocket"]
    tol = pocket["module_tolerance"]
    worst = Rect(module["x0"] - tol, module["y0"] - tol, module["x1"] + tol, module["y1"] + tol)
    r = pocket["front_corner_radius"]
    corners = [(worst.x0, worst.y0), (worst.x1, worst.y0), (worst.x0, worst.y1), (worst.x1, worst.y1)]
    # The rear corners are sharp thanks to the T-bones; the front corners carry the radius.
    rear_ok = all(rect.x0 - EPS <= x <= rect.x1 + EPS and rect.y0 - EPS <= y for x, y in corners)
    front_ok = all(point_in_rounded(x, y, rect, r) or y < rect.y1 - r for x, y in corners)
    relief_ok = all(abs(math.hypot(c.cx - x, c.cy - rect.y0) - c.r) < EPS for c, x in zip(reliefs, (rect.x0, rect.x1)))
    report.check("display module corners inside the pocket shape", rear_ok and front_ok and relief_ok,
                 f"module +/-{tol} in X {rect.x0} to {rect.x1}, Y from {rect.y0}; rear T-bones Ø{pocket['rear_relief_diameter']} "
                 f"pass through the corners; front R{r}")


def check_countersink_web(spec: dict, report: Report) -> None:
    k, keys, case = spec["holes"]["k"], spec["keys"], spec["case"]
    openings = [Rect.centred(x, y, keys["plate_opening"], keys["plate_opening"]) for _, _, x, y in key_centres(spec)]
    web = min(gap(Circle(x, y, k["countersink"] / 2), o) for x, y in k["positions"] for o in openings)
    report.check("K countersink to switch opening web", web >= case["min_metal_wall"] - EPS,
                 f"{web:.3f} mm of plate top, limit {case['min_metal_wall']} (JLCCNC); {k['screw']}")


def check_usb_behind_encoders(spec: dict, report: Report) -> None:
    usb, enc = spec["usb"], spec["encoders"]
    usb_end = usb["front_y"] + usb["length"]
    enc_front = min(enc[s]["y"] for s in ("right", "left")) - enc["body"][1] / 2
    report.check("USB-C behind the encoder bodies", usb_end <= enc_front - 0.2 + EPS,
                 f"receptacle ends Y {usb_end:.2f}, encoder bodies start Y {enc_front:.2f}")


def check_pins(spec: dict, report: Report) -> None:
    pads = spec["module"]["pads"]
    slow = set(spec["module"]["low_frequency"]["pins"])
    pinmap = spec["pinmap"]
    gpio = [name for name in pads if name.startswith("P")]
    report.check("module pad table", len(gpio) == 48 and len(set(pad for name, pad in pads.items() if name != "GND"))
                 + len(pads["GND"]) == 68, f"{len(gpio)} GPIO, {len(pads) - 1 + len(pads['GND'])} pads")
    unknown = [pin for pin in pinmap if pin not in pads]
    report.check("pin map names real pads", not unknown, f"{len(pinmap)} entries" if not unknown else f"unknown {unknown}")
    nets = [entry[0] for pin, entry in pinmap.items() if pin.startswith("P")]
    report.check("one net per GPIO", len(nets) == len(set(nets)), f"{len(nets)} GPIO nets, all distinct")
    fast_on_slow = [pin for pin, entry in pinmap.items() if entry[2] == "fast" and pin in slow]
    report.check("fast nets on full-speed pins", not fast_on_slow,
                 "no fast net on a low-frequency pin" if not fast_on_slow else f"on slow pins: {fast_on_slow}")
    spare = spec["pinmap_spare"]["pins"]
    used = [pin for pin in pinmap if pin.startswith("P")]
    every = sorted(used + spare) == sorted(gpio)
    report.check("used plus spare is all 48 GPIO", every and not set(used) & set(spare),
                 f"{len(used)} used, {len(spare)} spare")
    matrix = spec["matrix"]
    matrix_ok = (all(pinmap[p][0] == f"ROW{i}" for i, p in enumerate(matrix["rows"]))
                 and all(pinmap[p][0] == f"COL{i}" for i, p in enumerate(matrix["columns"])))
    report.check("matrix pins agree with the pin map", matrix_ok,
                 f"{len(matrix['rows'])} rows, {len(matrix['columns'])} columns, {matrix['diode_direction']}")
    c4 = {spec["encoders"]["right"]["matrix"]: "encoder_right_push", spec["encoders"]["left"]["matrix"]: "encoder_left_push",
          spec["buttons"]["right"]["matrix"]: "button_right", spec["buttons"]["left"]["matrix"]: "button_left"}
    c4_ok = all(c4.get(f"C4R{i}") == name for i, name in enumerate(matrix["c4"]))
    report.check("column 4 positions agree", c4_ok, ", ".join(f"C4R{i} {n}" for i, n in enumerate(matrix["c4"])))
    enc_ok = all(pinmap[spec["encoders"][s][k]][0] == f"ENC_{s[0].upper()}_{k[-1].upper()}"
                 for s in ("right", "left") for k in ("gpio_a", "gpio_b"))
    report.check("encoder pins agree with the pin map", enc_ok, "A and B of both encoders")
    fpc = spec["display"]["fpc_pins"]
    lcd_nets = {"LCD_SCK", "LCD_MOSI", "LCD_CS", "LCD_DC", "LCD_RESET"}
    fpc_ok = len(fpc) == 24 and lcd_nets <= set(fpc.values()) and lcd_nets <= set(nets)
    report.check("display connector nets reach the module", fpc_ok, f"{len(fpc)} connector pins, {len(lcd_nets)} bus nets")


def check_power(spec: dict, report: Report) -> None:
    power = spec["power"]
    total = sum(power["rail_3v3_caps_uf"])
    report.check("3V3 capacitance under the LDO limit", total <= power["rail_3v3_cap_max_derated_uf"] + EPS,
                 f"{total:.1f} uF nominal (bounds the derated value), limit {power['rail_3v3_cap_max_derated_uf']} uF derated")
    parts = {name: part_rect(part) for name, part in power["parts"].items()}
    battery = spec["battery"]
    pocket = Rect(battery["pocket_x"][0], battery["pocket_y"][0], battery["pocket_x"][1], battery["pocket_y"][1])
    to_pocket = gap(parts["charger"], pocket)
    report.check("charger away from the battery pocket", to_pocket >= power["charger_to_pocket_min"] - EPS,
                 f"{to_pocket:.2f} mm, limit {power['charger_to_pocket_min']}")
    to_ldo = gap(parts["charger"], parts["ldo"])
    report.check("charger not next to the LDO", to_ldo >= power["charger_to_ldo_min"] - EPS,
                 f"{to_ldo:.2f} mm, limit {power['charger_to_ldo_min']} (guess)")
    to_ptc = gap(parts["charger"], parts["ptc"])
    report.check("PTC away from the charger", to_ptc >= power["ptc_to_charger_min"] - EPS,
                 f"{to_ptc:.2f} mm, limit {power['ptc_to_charger_min']}")
    receptacle = usb_rect(spec)
    cc = max(gap(parts[name], receptacle) for name in ("cc1", "cc2"))
    report.check("CC resistors near the receptacle", cc <= power["cc_to_receptacle_max"] + EPS,
                 f"farthest {cc:.2f} mm, limit {power['cc_to_receptacle_max']}")
    pads = Rect(receptacle.x0, receptacle.y0, receptacle.x1, spec["usb"]["signal_pad_end_y"])
    esd = gap(parts["esd"], pads)
    report.check("ESD array next to the connector pads", esd <= power["esd_to_connector_max"] + EPS,
                 f"{esd:.2f} mm, limit {power['esd_to_connector_max']}")
    ntc, ntc_part = parts["ntc"], power["parts"]["ntc"]
    cell = cell_rect(spec)
    over_cell = cell.x0 <= ntc.x0 and ntc.x1 <= cell.x1 and cell.y0 <= ntc.y0 and ntc.y1 <= cell.y1
    zone = spec["keys"]["keepout"]["socket_zone"]
    zones = [Rect(x + zone[0], y + zone[1], x + zone[2], y + zone[3]) for _, _, x, y in key_centres(spec)]
    zone_gap = min(gap(ntc, z) for z in zones)
    low = ntc_part["height"] <= spec["keys"]["keepout"]["socket_depth"] + EPS
    report.check("NTC over the cell between socket zones", over_cell and zone_gap > 0 and low,
                 f"inside the cell outline; {zone_gap:.2f} mm from the nearest socket zone; "
                 f"{ntc_part['height']} mm tall against {spec['keys']['keepout']['socket_depth']} clear depth")


def edge_spans(spec: dict) -> dict[str, tuple[str, float, float, float]]:
    """Each board edge as (axis along the edge, fixed coordinate, start, end)."""
    pcb = spec["pcb"]
    return {"left": ("y", pcb["x0"], pcb["y0"], pcb["y1"]), "right": ("y", pcb["x1"], pcb["y0"], pcb["y1"]),
            "rear": ("x", pcb["y0"], pcb["x0"], pcb["x1"]), "front": ("x", pcb["y1"], pcb["x0"], pcb["x1"])}


def tab_rect(spec: dict, edge: str, centre: float) -> Rect:
    axis, fixed, _, _ = edge_spans(spec)[edge]
    half = spec["panel"]["tab_width"] / 2
    if axis == "y":
        return Rect(fixed, centre - half, fixed, centre + half)
    return Rect(centre - half, fixed, centre + half, fixed)


def check_panel(spec: dict, report: Report) -> None:
    panel, pcb = spec["panel"], spec["pcb"]
    report.check("panel rails wide enough", panel["rail_width"] >= 5.0 - EPS,
                 f"{panel['rail_width']} mm rails, {panel['routed_gap']} mm routed gap, joins {panel['edges']}")
    spans = edge_spans(spec)
    blocked = [(t["x0"], t["x1"]) for t in pcb["tongues"]] + [(n["x0"], n["x1"]) for n in pcb["notches"]]
    radius = pcb["corner_radius"]
    misplaced = []
    for edge, centre in panel["tabs"]:
        axis, _, start, end = spans[edge]
        half = panel["tab_width"] / 2
        if not (start + radius <= centre - half and centre + half <= end - radius):
            misplaced.append(f"{edge} {centre}")
        if edge == "rear" and any(lo - 1.0 < centre + half and centre - half < hi + 1.0 for lo, hi in blocked):
            misplaced.append(f"{edge} {centre} on a tongue")
    report.check("panel tabs on straight board edges", not misplaced,
                 f"{len(panel['tabs'])} tabs, clear of the corners and the rear tongues" if not misplaced else f"{misplaced}")
    strip = antenna_strip_rect(spec)
    to_antenna = min(gap(tab_rect(spec, e, c), strip) for e, c in panel["tabs"])
    report.check("panel tabs away from the antenna", to_antenna >= panel["tab_to_antenna_min"] - EPS,
                 f"nearest tab {to_antenna:.2f} mm from the antenna strip, limit {panel['tab_to_antenna_min']}")
    copper: list[Shape] = list(socket_pad_rects(spec)) + list(ground_rings(spec))
    to_copper = min(gap(tab_rect(spec, e, c), shape) for e, c in panel["tabs"] for shape in copper)
    report.check("panel tabs away from edge copper", to_copper >= panel["tab_to_copper_min"] - EPS,
                 f"nearest {to_copper:.2f} mm to a socket pad or ground ring, limit {panel['tab_to_copper_min']} (guess)")
    vcut = [edge for edge, join in panel["edges"].items() if join == "vcut"]
    vcut_bad = []
    for edge in vcut:
        axis, fixed, _, _ = spans[edge]
        line = Rect(fixed, -1e3, fixed, 1e3) if axis == "y" else Rect(-1e3, fixed, 1e3, fixed)
        if radius > 0 or any(gap(line, shape) < panel["vcut_copper_min"] for shape in copper):
            vcut_bad.append(edge)
    report.check("V-cut edges straight and clear of copper", not vcut_bad,
                 f"V-cut edges: {vcut or 'none'}; copper limit {panel['vcut_copper_min']} mm"
                 if not vcut_bad else f"failing edges: {vcut_bad}")
    usb, sw = spec["usb"], spec["power_switch"]
    tongues = {t["name"]: t for t in pcb["tongues"]}
    overhangs = {"usb_receptacle": tongues["usb"]["y0"] - usb["front_y"],
                 "power_switch_actuator": tongues["power_switch"]["y0"] - (sw["body_y0"] - sw["actuator"][1])}
    room = panel["routed_gap"] - panel["overhang_margin"]
    report.check("parts overhanging the board edge sit over a routed gap",
                 panel["edges"]["rear"] == "routed" and max(overhangs.values()) <= room + EPS,
                 ", ".join(f"{n} {v:.2f} mm" for n, v in overhangs.items()) + f"; room {room:.2f} mm in the rear gap")
    module_to_edge = pcb["x1"] - module_rect(spec).x1 + panel["routed_gap"] + panel["rail_width"]
    report.check("module body far enough from the panel edge", module_to_edge >= panel["body_to_panel_edge_min"] - EPS,
                 f"{module_to_edge:.2f} mm, limit {panel['body_to_panel_edge_min']}")


def check_radii(spec: dict, report: Report) -> None:
    """Internal corner radii against JLCCNC: R >= H/10 + 0.5 always; the table value or a named waiver."""
    split, deck = spec["body"]["split_z"], 0.0
    battery, display, plinth = spec["battery"], spec["display"], spec["plinth"]
    pockets = [
        ("battery pocket", split - battery["pocket_floor_top_z"], battery["pocket_corner_radius"], None),
        ("battery relief", split - battery["relief"]["floor_top_z"], battery["relief"]["corner_radius"], None),
        ("bottom cavity", split - spec["rf_bay"]["floor_top_z"], spec["case"]["cavity_corner_radius"], None),
        ("key well", deck - spec["stack"]["plate_top"], spec["keys"]["well_corner_radius"], None),
        ("plinth pocket", plinth["pocket_ceiling_z"] - split, plinth["pocket_corner_radius"], None),
        ("top RF pocket", spec["rf_bay"]["top_z"] - split, spec["rf_bay"]["top_pocket_corner_radius"], None),
        ("display pocket front", display["web"]["underside_z"] - split, display["pocket"]["front_corner_radius"], "D33"),
        ("display pocket T-bone", display["web"]["underside_z"] - split, display["pocket"]["rear_relief_diameter"] / 2, "D33"),
        ("lens recess", display["lens"]["recess_depth"], 2.1, None),
    ]
    bad = []
    for name, depth, radius, waiver in pockets:
        formula = depth / 10 + 0.5
        table = 1.5 if depth <= 10 else 2.0 if depth <= 15 else 2.5
        if radius < formula - EPS or (radius < table - EPS and waiver is None):
            bad.append(f"{name} R{radius} at {depth:.2f} deep")
    waived = [f"{n} ({w})" for n, d, r, w in pockets if w and r < (1.5 if d <= 10 else 2.0) - EPS]
    report.check("pocket corner radii meet JLCCNC", not bad,
                 f"{len(pockets)} pockets meet H/10 + 0.5 and the table; table waived: {', '.join(waived) or 'none'}"
                 if not bad else "; ".join(bad))
    gap_min = min(spec["pcb"]["x0"] - spec["body"]["wall"], spec["case"]["pcb_gap_min"])
    need = spec["case"]["cavity_corner_radius"] - gap_min / (1 - 1 / math.sqrt(2))
    report.check("PCB corners clear the cavity corners", spec["pcb"]["corner_radius"] >= need - EPS,
                 f"PCB R{spec['pcb']['corner_radius']}, cavity R{spec['case']['cavity_corner_radius']}, gap {gap_min:.2f}: "
                 f"needs R{max(need, 0):.2f} or more")
    pocket = Rect(battery["pocket_x"][0], battery["pocket_y"][0], battery["pocket_x"][1], battery["pocket_y"][1])
    corner_ok = inside_rounded(cell_rect(spec), pocket, battery["pocket_corner_radius"])
    report.check("cell corners clear the pocket radius", corner_ok, f"cell in the R{battery['pocket_corner_radius']} pocket")


def check_seam(spec: dict, report: Report) -> None:
    body, keys, case, stack = spec["body"], spec["keys"], spec["case"], spec["stack"]
    depth, wall = body["bottom_wall_step"]
    clearance = body["wall"] - wall
    lip = stack["split"] - stack["plate_underside"]
    report.check("bottom-shell wall clears the plate lip", clearance >= case["seam_clearance"] - EPS and depth > lip,
                 f"wall thinned to {wall} for {depth} mm below the split: {clearance:.2f} mm to the plate edge, "
                 f"lip {lip:.2f} mm below the split")


def check_usb(spec: dict, report: Report) -> None:
    usb = spec["usb"]
    low, high = usb["front_y_band"]
    report.check("USB-C front inside the U3 band", low - EPS <= usb["front_y"] <= high + EPS,
                 f"front {usb['front_y']} mm behind the rear face, band {low} to {high}; plug test gate (D37)")


def check_assembly(spec: dict, report: Report) -> None:
    assembly, battery = spec["assembly"], spec["battery"]
    report.check("switch insertion supported", assembly["switch_insertion"] == "jig"
                 and assembly["jig_support_gap"] <= assembly["jig_support_gap_max"] + EPS,
                 f"{assembly['switch_insertion']}, rib {assembly['jig_support_gap']} mm under each socket, "
                 f"limit {assembly['jig_support_gap_max']}")
    cell = cell_rect(spec)
    relief_y = battery["relief"]["y"]
    exit_ok = (battery["pcm_end"] == "+X" and relief_y[0] <= battery["lead_exit_y"] <= relief_y[1]
               and cell.y0 <= battery["lead_exit_y"] <= cell.y1 and abs(cell.x1 - battery["relief"]["x"][0]) <= 1.0 + EPS)
    report.check("cell lead exits into the relief", exit_ok,
                 f"PCM end at X {cell.x1:.2f}, lead exit Y {battery['lead_exit_y']}, relief Y {relief_y[0]} to {relief_y[1]}")
    conn = battery["connector"]
    plug_back = conn["x"] - conn["body"][0] / 2 - battery["plug_protrusion"]
    path = (plug_back - cell.x1) + abs(battery["lead_exit_y"] - conn["y"])
    need = path + battery["lead_loop_min"]
    report.check("cell lead length", need <= battery["lead_length"] <= battery["lead_length_max"],
                 f"needs {need:.1f} mm ({path:.1f} path + {battery['lead_loop_min']} loop), lead {battery['lead_length']} "
                 f"(guess), most that stows {battery['lead_length_max']}")


def check_print(spec: dict, report: Report) -> None:
    """FDM bottom shell printed on the ramp plane (D27)."""
    body, wedge, case = spec["body"], spec["wedge"], spec["case"]
    depth = body["depth"]
    profile = [(0.0, body["split_z"]), (depth, body["split_z"]), (depth, -wedge["front_height"]),
               (wedge["apex_y"], -wedge["apex_height"]), (0.0, -wedge["rear_height"])]
    angle = math.atan((wedge["apex_height"] - wedge["front_height"]) / (depth - wedge["apex_y"]))
    turned = [(y * math.cos(angle) + z * math.sin(angle), -y * math.sin(angle) + z * math.cos(angle)) for y, z in profile]
    along = max(p[0] for p in turned) - min(p[0] for p in turned)
    height = max(p[1] for p in turned) - min(p[1] for p in turned)
    fits = body["width"] <= case["bed"] and along <= case["bed"] and height <= case["bed"]
    report.check("FDM bottom shell fits the bed on the ramp plane", fits,
                 f"{body['width']} x {along:.1f} mm, {height:.1f} mm tall, ramp tilted {math.degrees(angle):.2f} degrees")
    rear_to_bed = math.degrees(math.atan((wedge["apex_height"] - wedge["rear_height"]) / wedge["apex_y"])) + math.degrees(angle)
    # Each flank scoop is open at the side and rear faces, so its roof hangs from two edges and cannot bridge:
    # it is supported, like the rear slope. The foot pockets are the only bridges left.
    pocket = spec["feet"]["pocket_diameter"]
    report.check("FDM bottom shell bridges within the limit", pocket <= case["fdm_bridge_max"] + EPS,
                 f"foot pocket {pocket} mm, limit {case['fdm_bridge_max']}; rear slope {rear_to_bed:.1f} degrees "
                 "to the bed and both flank scoops supported")
    supports = spec["print"]["bottom_shell"]["supports"]
    report.check("FDM bottom shell supports name the rear slope and the scoops",
                 "rear slope" in supports and "flank scoops" in supports, f"supports = {supports!r}")


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / "board.toml"
    spec = load(path)
    report = Report()
    bodies = build_bodies(spec)
    check_keys(spec, report)
    check_outline(spec, report)
    check_holes(spec, report)
    check_parts_inside(spec, bodies, report)
    check_overlaps(bodies, report)
    check_stack(spec, report)
    check_wedge(spec, report)
    check_battery(spec, report)
    check_rf(spec, report)
    check_clearances(spec, report)
    check_pins(spec, report)
    check_power(spec, report)
    check_panel(spec, report)
    check_radii(spec, report)
    check_seam(spec, report)
    check_usb(spec, report)
    check_assembly(spec, report)
    check_print(spec, report)
    total = report.passes + len(report.failures)
    if report.failures:
        print(f"check_spec: {len(report.failures)} of {total} checks failed: {', '.join(report.failures)}")
        return 1
    print(f"check_spec: all {total} checks pass on {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
