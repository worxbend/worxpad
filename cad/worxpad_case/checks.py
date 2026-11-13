"""Every check on the case, written to cad/exports/checks.json by `build.py check`.

Groups:
0. self_test: the measuring checks run on known-bad and sound solids (selftest.py).
1. validity: every part is one valid solid with a volume.
2. interference: every pair of case parts and bought parts in the assembled stack, both variants.
3. clearances: named gaps measured on the solids (keys, knobs, cell, display, lens, USB, PCB) and the screw
   arithmetic (engagement, thread, drill point), both variants where they differ.
4. cnc: JLCCNC rules on the two CNC shells (corner radius against depth, wall, floor, tool run, reach).
5. fdm: bed fit, contact, aspect, layer-by-layer overhangs and the thinnest wall of every printed part.
6. rf: no metal in the RF bay and over the window, the window over the antenna keep-out.
7. jig: the switch insertion jig against the sockets and the PCB assembly (D26).
8. pcb_step: the generated PCB STEP, if the PCB builder has written it.
"""

from itertools import combinations
from math import radians, tan
from pathlib import Path

from build123d import CenterOf, Compound, Pos, import_step

from . import measure, printsim, selftest
from .components import components, pcb
from .coupons import as_printed, print_aids, print_pose, printed_parts, resin_parts
from .measure import row
from .parts import bottom_shell, cell_rim_levels, in_cell_pocket_plan, print_k_tip, top_shell, usb_skin, web_underside
from .small_parts import case_parts, insertion_jig, jig_rim, jig_ribs, keycap, knob_crush_ribs, rf_insert
from .solids import box, overlap_volume, rounded, slab, span_box
from .spec import BOARD, CASE, CNC, LIMITS, PRINT, VARIANTS, button_centres, c_holes, cell_z, display_pocket_span
from .spec import encoder_centres
from .spec import g_holes, inner_span, k_holes, key_centres, keepout_span, module_span, rf_bay_span, scoop_spans, thickness_at

PCB_STEP = Path(__file__).resolve().parents[2] / "pcb" / "production" / "worxpad-pcb.step"
# Pockets under the R 1.5 table radius, by decision (D29 lists waivers by entry).
WAIVERS = [
    {"span": ((86.0, 115.5), (58.0, 63.0)), "reason": "D33: display pocket front corners R1.0, 3.05 deep, 2.0 mm tool"},
]
PRESS_FITS = {("knob_left", "encoder_shafts"), ("knob_right", "encoder_shafts")}  # print knobs: crush ribs
DENSITY = {"top_shell": 2.70, "on_pcb": 1.85}  # g/cm^3: 6061; FR4 taken for every part on the PCB (guess)
ON_PCB = ["pcb", "switch_bodies", "switch_stems", "sockets", "diodes", "encoders", "encoder_shafts", "button_switches",
          "display_module", "display_flex", "fpc_connector", "display_foam", "module", "flash", "usb_receptacle",
          "battery_connector", "reset_button", "power_switch", "power_parts", "g_screws"]


def run_all() -> dict:
    return {
        "status": "model checks only; nothing printed, milled or fitted",
        "self_test": selftest.run(),
        "validity": validity(),
        "interference": [interference(variant) for variant in VARIANTS],
        "clearances": clearances(),
        "cnc": cnc_rules(),
        "fdm": fdm_rules(),
        "rf": rf_rules(),
        "jig": jig_rules(),
        "pcb_step": pcb_step_fit(),
    }


def failures(report: dict) -> list[str]:
    problems = [f"self-test {item['name']}" for item in report["self_test"] if not item["ok"]]
    problems += [f"validity {item['name']}" for item in report["validity"] if not item["ok"]]
    for result in report["interference"]:
        problems += [f"{result['variant']} clash {c['a']} / {c['b']} {c['volume_mm3']} mm^3" for c in result["clashes"]]
        problems += [f"{result['variant']} press fit {p['a']} / {p['b']}" for p in result["press_fits"] if not p["ok"]]
    for group in ("clearances", "cnc", "fdm", "rf", "jig", "pcb_step"):
        problems += [f"{group} {item['name']}: {item['value']} ({item['kind']} {item['limit']})"
                     for item in report[group] if item.get("ok") is False]
    return problems


def _info(name: str, value: float, unit: str = "mm", note: str = "") -> dict:
    """A number reported for the reader, held to no limit."""
    return {"name": name, "value": round(float(value), 3), "limit": None, "kind": "info", "unit": unit, "ok": None,
            "note": note}


def _noted(item: dict, note: str) -> dict:
    return item | {"note": note}


# ---------------------------------------------------------------------------------------------------------
# 1. Validity
# ---------------------------------------------------------------------------------------------------------
def validity() -> list[dict]:
    """One valid solid with a volume per part; the two FDM ground spacers are one entry of two solids."""
    parts = {f"{variant}_{name}": part for variant in VARIANTS for name, part in case_parts(variant).items()
             if name != "keycaps"}
    parts |= {name: part for name, part in printed_parts().items() if name.startswith("coupon")}
    parts |= resin_parts() | {"insertion_jig": insertion_jig()}
    rows = []
    for name, part in parts.items():
        expected = 2 if name.endswith("g_spacers") else 1
        faults = abs(len(part.solids()) - expected) + (not part.is_valid) + (part.volume <= 0)
        rows.append(row(name, faults, 0, kind="max", unit="faults") | {"volume_mm3": round(part.volume, 1)})
    return rows


# ---------------------------------------------------------------------------------------------------------
# 2. Interference
# ---------------------------------------------------------------------------------------------------------
def interference(variant: str) -> dict:
    solids = case_parts(variant) | components(variant)
    clashes, press_fits, pairs = [], [], 0
    for (a, part_a), (b, part_b) in combinations(solids.items(), 2):
        pairs += 1
        volume = overlap_volume(part_a, part_b)
        if (a, b) in PRESS_FITS and variant == PRINT:
            allowed = _rib_overlap(a)
            press_fits.append({"a": a, "b": b, "volume_mm3": round(volume, 3), "allowed_mm3": round(allowed, 3),
                               "ok": bool(volume <= allowed + LIMITS.clash_volume)})
        elif volume > LIMITS.clash_volume:
            clashes.append({"a": a, "b": b, "volume_mm3": round(volume, 3)})
    return {"variant": variant, "parts": len(solids), "pairs": pairs, "clashes": clashes, "press_fits": press_fits,
            "limit_mm3": LIMITS.clash_volume}


def _rib_overlap(knob_name: str) -> float:
    axis = encoder_centres()[0 if knob_name.endswith("left") else 1]
    ribs = knob_crush_ribs(axis)
    shaft = components(PRINT)["encoder_shafts"]
    return sum(overlap_volume(rib, shaft) for rib in ribs)


# ---------------------------------------------------------------------------------------------------------
# 3. Clearances
# ---------------------------------------------------------------------------------------------------------
def clearances() -> list[dict]:
    rows = []
    for variant in VARIANTS:
        rows += _key_clearances(variant) + _knob_clearances(variant) + _cell_clearances(variant)
        rows += _display_clearances(variant) + _port_clearances(variant) + _button_clearances(variant)
        rows += _encoder_clearances(variant) + _cell_rim_rows(variant)
    rows += _screw_rows() + _parallax_rows()
    return rows


def _travel() -> float:
    return CASE.switch_travel + CASE.switch_travel_tolerance


def _key_clearances(variant: str) -> list[dict]:
    parts, comps = case_parts(variant), components(variant)
    top = parts["top_shell"]
    caps = parts["keycaps"]
    pressed = Pos(0, 0, -_travel()) * caps
    first, second = key_centres()[0], key_centres()[1]
    shell_and_heads = Compound([top, comps["k_screws"]])
    return [
        _noted(row(f"{variant}_keycap_to_well_wall", caps.distance_to(top), BOARD.keys.cap_to_well_min),
               "caps at rest to the top shell (keys 6.5)"),
        _noted(row(f"{variant}_keycap_gap", keycap(first).distance_to(keycap(second)), LIMITS.keycap_gap),
               "neighbouring caps; 0.45 is the gap left at the +/-0.2 resin tolerance (keys 6.5)"),
        _noted(row(f"{variant}_pressed_keycap_to_shell_and_k_heads", pressed.distance_to(shell_and_heads),
                   LIMITS.pressed_cap_to_shell),
               f"caps pressed {_travel():.2f} mm (PG1353D travel plus tolerance) to the plate, well and K heads"),
        _noted(row(f"{variant}_pressed_keycap_to_switch", pressed.distance_to(comps["switch_bodies"]),
                   LIMITS.pressed_cap_to_switch), "pressed caps to the flange, housing and collar (keys 6.3 item 4)"),
        _noted(row(f"{variant}_k_head_below_plate_top", BOARD.stack.plate_top - k_holes().head_top_z[0][0], 0.0),
               "keys 6.3 item 3: heads flush or recessed"),
    ]


def _knob_clearances(variant: str) -> list[dict]:
    parts, comps = case_parts(variant), components(variant)
    travel = BOARD.knobs.rim_z - BOARD.knobs.rim_pressed_z
    pressed = Compound([Pos(0, 0, -travel) * parts["knob_left"], Pos(0, 0, -travel) * parts["knob_right"]])
    knobs = Compound([parts["knob_left"], parts["knob_right"]])
    tip_max = CASE.encoder_shaft[2] + 0.5  # rotary-buttons 6.3: tip +0.5 at most
    bore_bottom = BOARD.knobs.rim_z + CASE.knob_bore[2]
    return [
        _noted(row(f"{variant}_knob_rim_to_plinth_pressed", pressed.distance_to(parts["top_shell"]),
                   LIMITS.knob_rim_pressed), f"knobs pushed {travel:.2f} mm (maximum travel)"),
        _noted(row(f"{variant}_knob_ceiling_to_collar_pressed",
                   BOARD.knobs.rim_pressed_z + CASE.knob_counterbore[1] - CASE.encoder_collar[1], LIMITS.knob_collar_pressed),
               "counterbore ceiling at maximum travel over the nominal collar top; the limit holds a maximum collar on "
               "the lowest plinth (rotary-buttons 6.3 item 2)"),
        _noted(row(f"{variant}_knob_to_collar_pressed", pressed.distance_to(comps["encoders"]), LIMITS.knob_collar_radial),
               "measured on the solids: the counterbore round the collar (collar diameter a guess)"),
        _noted(row(f"{variant}_knob_to_top_shell_at_rest", knobs.distance_to(parts["top_shell"]), 1.0),
               "rim over the plinth top: the 1.10 mm shim (rotary-buttons 6.5), less 0.1 mm"),
        _noted(row(f"{variant}_knob_bore_bottom_over_longest_shaft", bore_bottom - tip_max, 0.35),
               "arithmetic on the model levels: bore bottom against the shaft tip at +0.5 (rotary-buttons 6.3 item 3)"),
    ]


def _cell_clearances(variant: str) -> list[dict]:
    parts, comps = case_parts(variant), components(variant)
    cell, shell = comps["cell"], parts["bottom_shell"]
    z0, z1 = cell_z()
    walls = shell & box((0, BOARD.body.width), (0, BOARD.body.depth), (z0 + 0.1, z1))
    return [
        _noted(row(f"{variant}_cell_to_pocket_walls", cell.distance_to(walls), BOARD.battery.pocket_clearance),
               "swollen cell (power 14) to the pocket walls in plan"),
        _noted(row(f"{variant}_cell_to_pocket_floor", cell.distance_to(shell), BOARD.battery.foam),
               "room for the foam pad under the swollen cell"),
        _noted(row(f"{variant}_cell_to_sockets", cell.distance_to(comps["sockets"]), BOARD.battery.insulation),
               "swollen cell to the socket undersides: room for the insulation sheet"),
    ]


def _button_clearances(variant: str) -> list[dict]:
    """Cap flange to the counterbore ceiling, measured on the solids, then with the tolerance stack that closes
    it: a tall switch, a tall resin cap and a shallow counterbore. A closed gap preloads the plunger, and the
    B3FS pretravel can be as small as 0.15 mm (rotary-buttons, part table), so the button would read held."""
    top = case_parts(variant)["top_shell"]
    flange_top = BOARD.stack.button_counterbore_top - CASE.button_flange_gap
    reach = (BOARD.buttons.hole + BOARD.buttons.cap_flange) / 4  # over the flange ring, outside the hole
    stack = CASE.button_switch_tolerance + CASE.button_cap_tolerance + CASE.counterbore_depth_tolerance
    rows = []
    for side, (x, y) in zip(("left", "right"), button_centres(), strict=True):
        gap = measure.material_along(top, (x + reach, y, flange_top), (0, 0, 1))
        rows += [
            _info(f"{variant}_button_{side}_flange_to_ceiling_nominal", gap,
                  note="flange top to the counterbore ceiling at nominal heights, measured on the solid"),
            _noted(row(f"{variant}_button_{side}_flange_to_ceiling_worst", gap - stack, LIMITS.button_worst_gap),
                   f"less {stack:.2f}: switch +{CASE.button_switch_tolerance}, cap +{CASE.button_cap_tolerance}, "
                   f"counterbore -{CASE.counterbore_depth_tolerance} (ISO 2768-m)"),
        ]
    return rows


def _encoder_clearances(variant: str) -> list[dict]:
    """Encoder body at its maximum height (board.toml body_top_z) to the plinth pocket ceiling, beside the shaft
    hole, with the depth tolerance the drawing calls (deeper only)."""
    top = case_parts(variant)["top_shell"]
    beside = (BOARD.plinth.shaft_hole + min(BOARD.encoders.body)) / 4
    deeper, shallower = CASE.encoder_pocket_depth_tolerance
    rows = []
    for side, (x, y) in zip(("left", "right"), encoder_centres(), strict=True):
        gap = measure.material_along(top, (x + beside, y, BOARD.encoders.body_top_z), (0, 0, 1))
        rows.append(_noted(row(f"{variant}_encoder_{side}_body_to_pocket_ceiling", gap - shallower,
                               LIMITS.encoder_to_ceiling),
                           f"pocket depth +{deeper:.2f}/-{shallower:.2f} on the drawing; a ceiling on the body bends "
                           "the PCB away from the G posts"))
    return rows


def _cell_rim_rows(variant: str) -> list[dict]:
    """Setback of the battery pocket and relief rims, 0.05 mm below each rim, at the middle of every straight
    rim edge: a ray from 1.0 mm inside the pocket toward the wall, less that 1.0. A sharp rim gives 0; R0.5
    gives 0.28."""
    shell = case_parts(variant)["bottom_shell"]
    battery, relief = BOARD.battery, BOARD.battery.relief
    key_floor, column_floor = cell_rim_levels()
    (px0, px1), (py0, py1) = battery.pocket_x, battery.pocket_y
    (_, rx1), (ry0, ry1) = relief.x, relief.y
    column_x = (BOARD.floors.control_column_x0 + rx1) / 2
    near_x = (px1 + BOARD.floors.control_column_x0) / 2
    # (wall point, inward direction toward the wall from the pocket, rim level)
    walls = [((px0, (py0 + py1) / 2), (-1, 0), key_floor), ((px1, (py0 + ry0) / 2), (1, 0), key_floor),
             (((px0 + px1) / 2, py0), (0, -1), key_floor), (((px0 + px1) / 2, py1), (0, 1), key_floor),
             ((near_x, ry0), (0, -1), key_floor), ((near_x, ry1), (0, 1), key_floor),
             ((column_x, ry0), (0, -1), column_floor), ((column_x, ry1), (0, 1), column_floor),
             ((rx1, (ry0 + ry1) / 2), (1, 0), column_floor)]
    depth, start = 0.05, 1.0
    setbacks = []
    for (x, y), (dx, dy), level in walls:
        origin = (x - dx * start, y - dy * start, level - depth)
        if not in_cell_pocket_plan(origin[0], origin[1]):
            raise ValueError(f"rim probe start {origin} is not inside the battery pocket or relief")
        setbacks.append(measure.material_along(shell, origin, (dx, dy, 0)) - start)
    radius = CASE.cell_rim_radius
    expected = radius - (radius ** 2 - (radius - depth) ** 2) ** 0.5
    limit = round(expected - LIMITS.cell_rim_tessellation, 3)
    return [_noted(row(f"{variant}_cell_pocket_rim_setback", min(setbacks), limit),
                   f"smallest of {len(setbacks)} rim edges; R{radius} gives {expected:.3f} at {depth} below the rim "
                   "(power 14 rule 3)")]


def _parallax_rows() -> list[dict]:
    """Estimate only: how far the mask edge hides the active area when seen off the normal. The mask is on the
    lens underside, the pixels under the module top and its glass. Nothing here is measured."""
    stack = BOARD.stack
    height = stack.lens_underside - stack.display_module_top + CASE.display_glass_depth
    margin = (BOARD.display.lens.window - CASE.display_active_area) / 2
    return [_info(f"display_mask_parallax_at_{angle:g}_deg", height * tan(radians(angle)) - margin,
                  note=f"active area hidden under the mask edge, mm: {height:.2f} mm of depth x tan(angle) less the "
                       f"{margin:.2f} mm window margin. Estimate; check on the lens coupon")
            for angle in CASE.viewing_angles]


def _display_clearances(variant: str) -> list[dict]:
    parts, comps = case_parts(variant), components(variant)
    top, module = parts["top_shell"], comps["display_module"]
    below_web = top & box((80, 120), (25, 65), (BOARD.body.split_z, web_underside(variant) - 0.01))
    return [
        _noted(row(f"{variant}_display_module_to_top_shell", module.distance_to(top), LIMITS.module_to_web),
               "module top to the web underside: the 0.10 mm tape frame (D10)"),
        _noted(row(f"{variant}_display_module_to_pocket_walls", module.distance_to(below_web),
                   BOARD.display.pocket.module_tolerance), "module outline in its pocket (D33)"),
        _noted(row(f"{variant}_lens_to_recess", parts["lens"].distance_to(top), LIMITS.lens_fit), "conventions 3.6"),
        _noted(row(f"{variant}_display_flex_to_pocket_walls", comps["display_flex"].distance_to(below_web), 0.3),
               "flex bend in the pocket opened to Y 61.8 (display 6.5), in plan; 0.3 mm a guess"),
    ]


def _port_clearances(variant: str) -> list[dict]:
    parts, comps = case_parts(variant), components(variant)
    shell = parts["bottom_shell"]
    top_below_pcb = parts["top_shell"] & box((0, BOARD.body.width), (0, BOARD.body.depth),
                                             (-30.0, BOARD.pcb.top_z - 0.001))
    if top_below_pcb is None or not top_below_pcb.solids():
        top_below_pcb = shell
    (ix0, ix1), (iy0, iy1) = inner_span()
    walls = shell - box((ix0 + 2.0, ix1 - 2.0), (iy0 + 2.0, iy1 - 2.0), (-30.0, 0.0))  # walls and what is on them
    rows = [
        _noted(row(f"{variant}_pcb_outline_to_bottom_shell", pcb(with_holes=False).distance_to(walls), LIMITS.pcb_gap),
               "PCB outline and tongues to the walls and the USB pocket (D21)"),
        _noted(row(f"{variant}_posts_in_pcb_holes", comps["pcb"].distance_to(Compound([shell, top_below_pcb])),
                   LIMITS.post_in_pcb_hole),
               "K and C posts through the 4.0 mm NPTH (enclosure 6.4); the G post ends seat on the board by design"),
        _noted(row(f"{variant}_usb_receptacle_to_bottom_shell", comps["usb_receptacle"].distance_to(shell), 0.5),
               "usb-io 6.2 item 1 draws 0.53 mm at the sides"),
        _noted(row(f"{variant}_power_switch_to_bottom_shell", comps["power_switch"].distance_to(shell), 0.3),
               "actuator in its notch; 0.3 mm a guess"),
    ]
    if variant == CNC:
        usb = BOARD.usb
        skin_x = usb.x + (usb.notch_x[1] - usb.x + usb.pocket_x[1] - usb.x) / 2
        skin = measure.material_along(shell, (skin_x, 0.0, (usb.pocket_z[0] + usb.pocket_z[1]) / 2), (0, 1, 0))
        rows.append(_noted(row("cnc_usb_c_skin", skin, LIMITS.metal_wall_absolute),
                           f"usb-io 6.2 item 3; JLCCNC recommends {LIMITS.metal_wall} mm, absolute minimum "
                           f"{LIMITS.metal_wall_absolute} mm; a skin {usb_skin(CNC)} mm thick needs the JLCCNC DFM "
                           "check and a first article"))
    else:
        rows.append(_info("print_usb_c_skin", 0.0, note="no skin in print: usb-io 6.2 item 5 fallback (parts.usb_skin)"))
    plug_room = min(abs(BOARD.usb.x - edge) for edge in BOARD.power_switch.notch_x)
    rows.append(_noted(row(f"{variant}_rear_face_clear_of_plug", plug_room, 6.5),
                       "nearest other rear opening to the USB-C centre (usb-io 6.2 item 7)"))
    return rows


def _screw_rows() -> list[dict]:
    rows = []
    top_cnc, bottom_cnc = top_shell(CNC), bottom_shell(CNC)
    for holes, factor, shell, toward in ((k_holes(), LIMITS.engagement_k, bottom_cnc, -1),
                                         (c_holes(), LIMITS.engagement_c, top_cnc, 1),
                                         (g_holes(), LIMITS.engagement_g, top_cnc, 1)):
        for index, (x, y) in enumerate(holes.positions):
            tag = f"cnc_{holes.name}{index + 1}"
            short, long = holes.engagement(index)
            beyond = measure.material_along(shell, (x, y, holes.point_z(index) + toward * 0.01), (0, 0, toward)) + 0.01
            rows += [
                _noted(row(f"{tag}_engagement", short, factor * holes.major),
                       f"{holes.screw}: {short:.2f} to {long:.2f} mm in {holes.thread}, full thread {holes.full_thread} "
                       f"from Z {holes.mouth_z[index]} to {holes.thread_end_z(index):.2f}"),
                _noted(row(f"{tag}_tip_to_last_full_thread", holes.tip_margin(index), CASE.thread_tip_margin),
                       f"deepest tip Z {holes.tip_z(index)[1]:.2f}"),
                _noted(row(f"{tag}_metal_beyond_drill_point", beyond, CASE.drill_point_margin),
                       f"tap drill {holes.tap_drill} to shoulder Z {holes.shoulder_z(index):.2f}, point Z "
                       f"{holes.point_z(index):.2f}; measured on the solid (enclosure 5)"),
            ]
    rows += _print_screw_rows()
    return rows


def _print_screw_rows() -> list[dict]:
    high, low = print_k_tip()
    boss_top = CASE.print_k_boss_top_z
    rows = [_noted(row("print_k_self_tap_engagement", boss_top - high, LIMITS.print_self_tap * 1.6),
                   f"M1.6 x 8 self-tapping (D30) into the {CASE.print_k_boss} mm boss: {boss_top - high:.2f} to "
                   f"{boss_top - low:.2f} mm")]
    split = BOARD.body.split_z
    insert_top = split + CASE.print_insert_length
    hole_end = split + CASE.print_insert_depth
    head_top = CASE.print_c_seat_z + (BOARD.holes.c.countersink - CASE.m2_head) / 2
    tips = [head_top + CASE.print_c_screw_length + sign * CASE.length_tolerance for sign in (-1, 1)]
    deepest = max(tips) + CASE.head_undersize / 2
    rows += [
        _noted(row("print_c_insert_engagement", min(insert_top, min(tips)) - split, LIMITS.print_insert_engagement),
               f"M2 x {CASE.print_c_screw_length:g} from the Z {CASE.print_c_seat_z} seats into the M2 x 3 insert"),
        _noted(row("print_c_tip_to_insert_hole_end", hole_end - deepest, LIMITS.print_tip_to_hole_end),
               f"insert hole {CASE.print_insert_depth} mm deep, deepest tip Z {deepest:.2f}"),
        _noted(row("print_g_insert_engagement", BOARD.pcb.bottom_z + CASE.g_length - CASE.length_tolerance - split, 1.0),
               "M2 x 4 through the 1.2 mm spacer into the insert; holds the PCB only, no grounding (guess limit)"),
    ]
    return rows


# ---------------------------------------------------------------------------------------------------------
# 4. CNC
# ---------------------------------------------------------------------------------------------------------
def cnc_rules() -> list[dict]:
    rows = []
    feet = [(x, -y, BOARD.feet.pocket_diameter / 2 + 0.5) for x, y in BOARD.feet.positions]
    for name, part in (("top_shell", top_shell(CNC)), ("bottom_shell", bottom_shell(CNC))):
        arcs = measure.concave_arcs(part)
        faults, margin = measure.radius_rule(arcs)
        table_faults, waived = measure.table_rule(arcs, WAIVERS)
        uncut = measure.uncut_area(part, LIMITS.cnc_tool, skip=feet if name == "bottom_shell" else ())
        rows += [
            _noted(row(f"cnc_{name}_corner_radius_rule_faults", len(faults), 0, kind="max", unit="arcs"),
                   f"R >= depth/10 + 0.5 on {len(arcs)} concave arcs; smallest margin {margin:.3f} mm; arcs of 180 "
                   "degrees or more are drilled or plunged and left out"),
            _noted(row(f"cnc_{name}_table_radius_faults", len(table_faults), 0, kind="max", unit="arcs"),
                   "R 1.5 in pockets deeper than 3 mm (D29); waived: "
                   + ("; ".join(sorted({w['waiver'] for w in waived})) or "none")),
            row(f"cnc_{name}_sharp_internal_corners", measure.sharp_internal_corners(part), 0, kind="max", unit="edges"),
            _noted(row(f"cnc_{name}_thinnest_wall", measure.thinnest_wall(part), LIMITS.metal_wall_absolute),
                   f"3000 sampled points; JLCCNC absolute minimum, recommended {LIMITS.metal_wall}"),
            _noted(row(f"cnc_{name}_undercut_area", measure.unreachable_area(part, skip=feet if name == "bottom_shell" else ()),
                       measure.UNDERCUT_NOISE, kind="max", unit="mm^2"),
                   "tool straight down or up; the foot pockets are judged in the ramp setup" if name == "bottom_shell" else ""),
            _noted(row(f"cnc_{name}_not_cut_from_above", uncut["above"], measure.UNCUT_NOISE, kind="max", unit="mm^2"),
                   f"a {LIMITS.cnc_tool} mm flat end mill run over a 0.1 mm height map"),
            _noted(row(f"cnc_{name}_not_cut_from_below", uncut["below"], measure.UNCUT_NOISE, kind="max", unit="mm^2"),
                   "level setup; the foot pockets belong to the ramp setup" if name == "bottom_shell" else ""),
            _noted(row(f"cnc_{name}_tool_reach", measure.tool_reach(arcs), LIMITS.tool_reach, kind="max", unit="x D"),
                   "deepest concave arc over the diameter of the tool that cuts it"),
        ]
    bottom = bottom_shell(CNC)
    ramp_setup = print_pose("bottom_shell") * bottom
    ramp_feet = [_posed_xy(tuple(p)) + (BOARD.feet.pocket_diameter / 2 + 0.5,) for p in BOARD.feet.positions]
    ramp_uncut = measure.uncut_area(ramp_setup, LIMITS.cnc_tool, only=ramp_feet)
    floor, where = measure.thinnest_floor(bottom)
    rows.append(_noted(row("cnc_bottom_shell_foot_pockets_undercut_ramp_setup",
                           measure.unreachable_area(ramp_setup, only=ramp_feet), measure.UNDERCUT_NOISE, kind="max",
                           unit="mm^2"), "the four foot pockets with the ramp plane level"))
    rows += [
        _noted(row("cnc_bottom_shell_foot_pockets_not_cut_ramp_setup", ramp_uncut["below"], measure.UNCUT_NOISE,
                   kind="max", unit="mm^2"), "the four foot pockets with the ramp plane level"),
        _noted(row("cnc_bottom_shell_thinnest_floor", floor, LIMITS.floor),
               f"vertical, over every floor seen from below; thinnest at X {where[0]}, Y {where[1]}"),
    ]
    rows += _named_walls()
    return rows


def _posed_xy(position: tuple[float, float]) -> tuple[float, float]:
    point = print_pose("bottom_shell") * Pos(position[0], -position[1], -thickness_at(position[1]))
    return point.position.X, point.position.Y


def _named_walls() -> list[dict]:
    top = top_shell(CNC)
    lens = BOARD.display.lens
    web_x = (lens.x0 + lens.x1) / 2 - BOARD.display.web.window / 2 - 0.4
    k = BOARD.holes.k
    k_x, k_y = k.positions[0]
    opening_edge = BOARD.keys.first_x + BOARD.keys.plate_opening / 2
    (rf_x0, _), _ = rf_bay_span()
    (_, pocket_x1), _ = display_pocket_span()
    walls = [
        ("display_web", measure.material_along(top, (web_x, 42.6, -BOARD.display.lens.recess_depth), (0, 0, -1)), "D10"),
        ("display_pocket_to_rf_pocket", measure.material_along(top, (pocket_x1, 53.0, -3.0), (1, 0, 0)),
         f"D33 (pocket edge X {pocket_x1}, RF pocket X {rf_x0:.2f})"),
        ("k_countersink_to_switch_opening", measure.material_along(top, (opening_edge, k_y, BOARD.stack.plate_top - 0.001),
                                                                   (1, 0, 0)), "D30, at the plate top"),
        ("plate_lip", measure.material_along(top, (k_x, BOARD.keys.first_y + 9.0, BOARD.stack.plate_top), (0, 0, -1)),
         "keys 6.2: 1.15 +/-0.05 after anodise"),
    ]
    return [_noted(row(f"cnc_wall_{name}", value, LIMITS.metal_wall), source) for name, value, source in walls]


# ---------------------------------------------------------------------------------------------------------
# 5. FDM
# ---------------------------------------------------------------------------------------------------------
def fdm_rules() -> list[dict]:
    rows = []
    for name, part in printed_parts().items():
        posed = as_printed(name)
        size = posed.bounding_box().size
        support = _support_triangles() if name == "bottom_shell" else None
        report = printsim.simulate(measure.mesh_of(posed, measure.ANY_MATERIAL).triangles, support)
        plan = max(size.X, size.Y)
        aspect = size.Z / max(min(size.X, size.Y), 1e-6)
        rows += [
            row(f"print_{name}_largest_extent", measure.largest_extent(posed), LIMITS.bed, kind="max"),
            _noted(row(f"print_{name}_longest_bridge", report.longest_bridge, LIMITS.bridge, kind="max"),
                   f"at bed {report.bridge_at}" + ("; with print aids" if print_aids(name) is not None else "")),
            _noted(row(f"print_{name}_deepest_cantilever", report.deepest_cantilever, LIMITS.cantilever, kind="max"),
                   f"at bed {report.cantilever_at}" + (f"; supports under the {CASE.print_supported_zones}"
                                                       if support is not None else "")),
            _noted(row(f"print_{name}_thinnest_wall", measure.thinnest_wall(part), LIMITS.fdm_wall),
                   "finished part, print aids removed"),
            _noted(row(f"print_{name}_height_over_narrow_side", aspect, 6.0, kind="max", unit="ratio"),
                   "above 6 a brim is needed (macropad)"),
        ]
        if plan >= 30.0:
            rows.append(row(f"print_{name}_bed_contact", measure.bed_contact(posed), LIMITS.bed_contact, unit="mm^2"))
    jig = insertion_jig()
    jig_report = printsim.simulate(measure.mesh_of(jig, measure.ANY_MATERIAL).triangles)
    rows += [
        row("print_insertion_jig_largest_extent", measure.largest_extent(jig), LIMITS.bed, kind="max"),
        row("print_insertion_jig_longest_bridge", jig_report.longest_bridge, LIMITS.bridge, kind="max"),
        row("print_insertion_jig_deepest_cantilever", jig_report.deepest_cantilever, LIMITS.cantilever, kind="max"),
    ]
    for name, part in resin_parts().items():
        rows.append(_info(f"resin_{name}_thinnest_wall", measure.thinnest_wall(part),
                          note="JLC3DP resin recommends over 0.8 mm; the post wall at the cross slot is 0.55 mm by "
                               "design (keys 6.5), so the stem coupon decides"))
    return rows


def _support_triangles():
    """Plan zones where the slicer builds supports under the FDM bottom shell: the rear slope and the scoops."""
    zones = [box((0, BOARD.body.width), (0, BOARD.wedge.apex_y), (-25.0, -11.0))]
    zones += [box(x, y, (-25.0, -11.0)) for x, y in scoop_spans()]
    region = zones[0].fuse(*zones[1:])
    return measure.mesh_of(print_pose("bottom_shell") * region, measure.ANY_MATERIAL).triangles


# ---------------------------------------------------------------------------------------------------------
# 6. RF
# ---------------------------------------------------------------------------------------------------------
def rf_rules() -> list[dict]:
    top, bottom = top_shell(CNC), bottom_shell(CNC)
    window, wall, width = BOARD.rf_window, BOARD.body.wall, BOARD.body.width
    bay_z = (BOARD.rf_bay.floor_top_z, BOARD.rf_bay.top_z)
    bay = span_box(rf_bay_span(), bay_z)
    (mx0, mx1), (my0, my1) = module_span()
    strip = ((mx1 - BOARD.module.antenna_strip, mx1), (my0, my1))
    margin = BOARD.rf_bay.margin
    inner_wall = width - wall
    clear = slab(rounded(((strip[0][0] - margin, strip[0][1] + margin), (strip[1][0] - margin, strip[1][1] + margin)),
                         margin), bay_z) & box((0, inner_wall), (0, BOARD.body.depth), bay_z)
    (_, _), (ky0, ky1) = keepout_span()
    over_window = box((width - wall, width), (ky0, ky1), (window.bottom_z, BOARD.body.split_z))
    metal_bay = overlap_volume(top, bay) + overlap_volume(bottom, bay)
    metal_margin = overlap_volume(top, clear) + overlap_volume(bottom, clear)
    insert = rf_insert()
    bounds = insert.bounding_box()
    insert_y0, insert_y1 = -bounds.max.Y, -bounds.min.Y
    (_, antenna_x1), _ = module_span()
    pocket_face = width - CASE.rf_insert_skin
    return [
        _noted(row("rf_metal_within_margin_of_antenna", metal_margin, LIMITS.clash_volume, kind="max", unit="mm^3"),
               f"both CNC shells within {margin} mm of the antenna strip in plan (mcu-radio A4), from Z -13.30 to "
               "-2.80 (A5, A7, A8), inside the inner wall (D11)"),
        _info("rf_metal_in_bay_rectangle_corners", metal_bay, unit="mm^3",
              note="the R1.5 corners of the two bay pockets, all more than the margin from the strip"),
        _noted(row("rf_metal_over_window", overlap_volume(bottom, over_window), LIMITS.clash_volume, kind="max",
                   unit="mm^3"), "right wall over the keep-out length, from the slot bottom to the split face"),
        _noted(row("rf_insert_covers_keepout", min(ky0 - insert_y0, insert_y1 - ky1), 0.0),
               f"insert Y {insert_y0:.2f} to {insert_y1:.2f} against the keep-out Y {ky0:.2f} to {ky1:.2f}"),
        _noted(row("rf_window_below_module", BOARD.stack.module_bottom - window.bottom_z, 0.0),
               "slot bottom below the module underside"),
        _noted(row("rf_window_top_at_or_above_a9", window.top_z - (-5.20), 0.0), "mcu-radio A9: from Z -5.20 or higher"),
        _noted(row("rf_insert_to_pcb", insert.distance_to(components(CNC)["pcb"]), LIMITS.pcb_gap),
               "nothing of the insert enters the cavity (enclosure 7.2 item 3)"),
        _info("rf_antenna_end_to_insert_plastic", pocket_face - antenna_x1,
              note="air from the antenna end to the POM (enclosure 7.2 item 4 gives 2.45 to 2.65); not quantified for RF"),
        _info("print_rf", 0.0, note="the FDM shells are plastic: no RF rule applies, and they predict nothing for RF"),
    ]


# ---------------------------------------------------------------------------------------------------------
# 7. Jig
# ---------------------------------------------------------------------------------------------------------
def jig_rules() -> list[dict]:
    jig = insertion_jig()
    comps = components(CNC)
    sockets = comps["sockets"]
    gap = jig.distance_to(sockets)
    assembly = [top_shell(CNC)] + [comps[name] for name in ON_PCB]
    clash = sum(overlap_volume(jig, part) for part in assembly)
    zx0, zy0, zx1, zy1 = BOARD.keys.keepout.socket_zone
    half = CASE.jig_rib / 2
    margins = []
    for (x, y), (rx, ry) in zip([c for c in key_centres() for _ in BOARD.keys.footprint.barrel_holes], jig_ribs()):
        margins.append(min(rx - half - (x + zx0), (x + zx1) - rx - half, ry - half - (y + zy0), (y + zy1) - ry - half))
    return [
        _noted(row("jig_rib_to_socket_min", gap, BOARD.assembly.jig_support_gap), "D26, keys 6.4"),
        _noted(row("jig_rib_to_socket_max", gap, BOARD.assembly.jig_support_gap_max, kind="max"),
               "support within 0.3 mm (keys 6.4)"),
        _noted(row("jig_clash_with_shell_and_pcb", clash, LIMITS.clash_volume, kind="max", unit="mm^3"),
               "CNC top shell, PCB and every part on it, deck up on the jig"),
        _noted(row("jig_ribs_inside_socket_zones", min(margins), LIMITS.jig_ribs_in_zone),
               "rib footprint to the socket-zone edge, smallest of 32"),
        _noted(row("jig_rim_at_split_face", abs(jig_rim().bounding_box().max.Z - BOARD.body.split_z), 1e-3, kind="max"),
               "the top shell rests on the rim, not on the PCB"),
        _noted(row("jig_centroid_inside_support", _centroid_margin(comps), LIMITS.jig_centroid_margin),
               f"CNC top shell ({DENSITY['top_shell']} g/cm^3) plus PCB and parts ({DENSITY['on_pcb']}, a guess), "
               "deck up: distance in plan from the centroid to the edge of the rim's convex hull"),
    ]


def _centroid_margin(comps: dict) -> float:
    weighted = [(top_shell(CNC), DENSITY["top_shell"])] + [(comps[name], DENSITY["on_pcb"]) for name in ON_PCB]
    mass = sum(part.volume * density for part, density in weighted)
    cx = sum(part.center(CenterOf.MASS).X * part.volume * density for part, density in weighted) / mass
    cy = sum(part.center(CenterOf.MASS).Y * part.volume * density for part, density in weighted) / mass
    rim = jig_rim()
    top = rim.bounding_box().max.Z
    points = [(p.X, p.Y) for face in rim.faces() if abs(face.center().Z - top) < 1e-6
               for edge in face.edges() for p in (edge.position_at(t / 8) for t in range(9))]
    return measure.inside_convex_hull(points, (cx, cy))


# ---------------------------------------------------------------------------------------------------------
# 8. PCB STEP from the PCB builder
# ---------------------------------------------------------------------------------------------------------
def pcb_step_fit(path: Path = PCB_STEP) -> list[dict]:
    """The KiCad STEP has the board bottom at Z 0; it is moved down to pcb.bottom_z before the clash rows. The
    board body is the solid with the largest volume; its thickness is checked, and the file must hold more
    solids than the body, or the part models are missing and the clash rows say nothing about them."""
    if not path.exists():
        return [_info("pcb_step_present", 0, unit="files",
                      note=f"{path.name} not found; the clash and clearance checks use the PCB drawn from board.toml")]
    imported = import_step(str(path))
    board = Pos(0, 0, BOARD.pcb.bottom_z) * imported
    solids = board.solids()
    body = max(solids, key=lambda solid: solid.volume)
    bounds = body.bounding_box()
    spec = components(CNC)["pcb"].bounding_box()
    rows = [_info("pcb_step_present", 1, unit="files", note=str(path.name))]
    plan_error = max(abs(bounds.min.X - spec.min.X), abs(bounds.max.X - spec.max.X), abs(bounds.min.Y - spec.min.Y),
                     abs(bounds.max.Y - spec.max.Y))
    rows.append(_noted(row("pcb_step_outline_vs_spec", plan_error, 0.05, kind="max"),
                       "bounding box of the board body against the spec PCB in plan"))
    rows.append(_noted(row("pcb_step_body_bottom_at_spec", abs(bounds.min.Z - BOARD.pcb.bottom_z), 1e-3, kind="max"),
                       "board body bottom after the move to pcb.bottom_z (KiCad puts it at Z 0)"))
    rows.append(_noted(row("pcb_step_body_thickness", abs(bounds.size.Z - BOARD.pcb.thickness),
                           CASE.pcb_step_thickness_tolerance, kind="max"),
                       f"body {bounds.size.Z:.3f} mm against pcb.thickness {BOARD.pcb.thickness}"))
    rows.append(_noted(row("pcb_step_solids", len(solids), 2, unit="solids"),
                       "the board body and at least one part model; a body alone means the parts were not exported"))
    for variant in VARIANTS:
        for name in ("top_shell", "bottom_shell"):
            rows.append(_noted(row(f"pcb_step_clash_{variant}_{name}", overlap_volume(board, case_parts(variant)[name]),
                                   LIMITS.clash_volume, kind="max", unit="mm^3"),
                               "every solid in the STEP, at its seat"))
    return rows
