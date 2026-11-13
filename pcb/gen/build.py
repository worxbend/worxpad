"""PCB build steps.

    build.py test        no KiCad: netlist self-checks, the 3V3 capacitance sum (D14), the pin-map check and
                         the unit tests of the generator
    build.py schematic   in the KiCad container: project footprints (written, then loaded back with pcbnew),
                         the schematic, KiCad's rule check, the netlist compared with circuit.py, PDF and SVG
                         of the sheet, block 3D models
    build.py place       schematic, then the placed and routed board with filled planes (layout.py, route.py),
                         KiCad's DRC with schematic parity, the routing report, the board pictures
    build.py order       search for a routing order that connects every net; rewrites route_order.txt
    build.py fab         Gerbers, drill files, JLCPCB and PCBWay order files, board STEP (fab.py)

The container steps run through pcb/kicad.sh or the Makefile.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

import circuit
import footprints
import schematic
import sexpr

GEN_DIR = Path(__file__).resolve().parent
PCB_DIR = GEN_DIR.parent
REPO_ROOT = PCB_DIR.parent
KICAD_DIR = PCB_DIR / "kicad"
BUILD_DIR = PCB_DIR / ".build"
SCHEMATIC_PATH = KICAD_DIR / schematic.SCHEMATIC_NAME
NETLIST_REPORT_PATH = PCB_DIR / "netlist.txt"
IMAGE_DIR = REPO_ROOT / "docs" / "images" / "pcb"
ERC_REPORT_PATH = BUILD_DIR / "erc.json"
# ERC findings that are meant: (type, explanation). Anything else fails the build, error or warning.
ACCEPTED_ERC_WARNINGS: dict[str, str] = {}
BOARD_PATH = KICAD_DIR / f"{circuit.LIBRARY}.kicad_pcb"
RULES_PATH = KICAD_DIR / f"{circuit.LIBRARY}.kicad_dru"
DRC_REPORT_PATH = BUILD_DIR / "drc.json"
ROUTING_REPORT_PATH = PCB_DIR / "routing.txt"
ROUTE_ORDER_PATH = GEN_DIR / "route_order.txt"
ORDER_SEARCH_ROUNDS = 12
# Camera for the angled renders, as kicad-cli wants it: degrees about X, Y, Z.
ANGLED_VIEW_ROTATION = "-50,0,25"
UNDERSIDE_VIEW_ROTATION = "-130,0,-25"
# DRC warnings that are meant: (type, first item) -> reason. Any other warning fails the build; every error does.
ACCEPTED_DRC_WARNINGS = {
    ("lib_footprint_mismatch", "Footprint SW18"):
        "layout.py cuts the silkscreen of the slide switch that hangs over the tongue edge",
    ("lib_footprint_mismatch", "Footprint ENC1"):
        "layout.py gives the encoder pins 1.6 mm round pads to clear the USB-C shell slots",
    ("lib_footprint_mismatch", "Footprint ENC2"):
        "layout.py gives the encoder pins 1.6 mm round pads to clear the USB-C shell slots",
    **{("lib_footprint_mismatch", f"Footprint H{n}"):
        "layout.py replaces the stock 8.6 mm hole courtyard with the board.toml keep-out check" for n in range(1, 9)},
}
# Copper allowed at the routed edge: J1's signal pads end at the notch edge as the HRO drawing shows, and the
# MSK12C02 shield tabs sit on the tongue edge with the body front (board.toml power_switch.body_y0). The pads
# touch the 0.05 mm edge line, so the minimum is negative: -0.1 mm, these two parts only.
DESIGN_RULES = """\
(version 1)
(rule "J1 signal pads end at the notch edge (HRO drawing)"
  (constraint edge_clearance (min -0.1mm))
  (condition "A.memberOfFootprint('J1')"))
(rule "SW18 shield tabs on the tongue edge (power_switch.body_y0)"
  (constraint edge_clearance (min -0.1mm))
  (condition "A.memberOfFootprint('SW18') && A.Pad_Number == 'SH'"))
"""
_ORDER_HEADER = """\
# Nets routed before the others, first line first.
# Written by `build.py order`. Run it again after moving parts or pins, when `build.py place`
# reports unrouted pads.
"""


def _kicad_cli(*arguments: str) -> None:
    subprocess.run(["kicad-cli", *arguments], check=True, stdout=subprocess.DEVNULL)


# --- test: no KiCad --------------------------------------------------------------------------------------

def test() -> None:
    parts = circuit.all_parts()
    circuit.check_netlist(parts)
    total = circuit.check_rail_capacitance(parts)
    nets = circuit.nets_to_pads(parts)
    print(f"circuit: {len(parts)} parts, {len(nets)} nets, no single-pad net; 3V3 capacitance {total:.1f} uF",
          flush=True)
    subprocess.run([sys.executable, str(REPO_ROOT / "tools" / "check_pins.py")], check=True)
    suite = unittest.defaultTestLoader.discover(str(GEN_DIR), pattern="test_*.py", top_level_dir=str(GEN_DIR))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        sys.exit(1)


# --- schematic: in the container -------------------------------------------------------------------------

def write_footprints() -> int:
    """Writes pcb/lib/worxpad.pretty and loads every file back with pcbnew: same pads, same places."""
    import pcbnew

    footprints.write()
    for wanted in footprints.footprints().values():
        loaded = pcbnew.FootprintLoad(str(footprints.LIBRARY_DIR), wanted.name)
        assert loaded is not None, f"{wanted.name}: pcbnew cannot read it"
        got = sorted((pad.GetNumber(), round(pcbnew.ToMM(pad.GetPosition().x), 3),
                      round(pcbnew.ToMM(pad.GetPosition().y), 3)) for pad in loaded.Pads())
        meant = sorted((pad.number, round(pad.x, 3), round(pad.y, 3)) for pad in wanted.pads)
        assert got == meant, f"{wanted.name}: pcbnew reads other pads than footprints.py wrote"
        assert len(list(loaded.Zones())) == len(wanted.zones), f"{wanted.name}: rule areas lost"
    return len(footprints.ALL)


def _exported_nets() -> dict[str, str]:
    """"U1.5" -> net as KiCad names it ("/ROW0", "GND", "unconnected-(...)"), read back from the netlist KiCad
    exports for the schematic."""
    netlist_path = BUILD_DIR / "schematic.net"
    _kicad_cli("sch", "export", "netlist", "--format", "kicadsexpr", "-o", str(netlist_path), str(SCHEMATIC_PATH))
    tree = sexpr.parse(netlist_path.read_text())
    nets = {}
    for net in sexpr.children(sexpr.child(tree, "nets"), "net"):
        name = sexpr.unquoted(sexpr.child(net, "name")[1])
        for node in sexpr.children(net, "node"):
            pin = f"{sexpr.unquoted(sexpr.child(node, 'ref')[1])}.{sexpr.unquoted(sexpr.child(node, 'pin')[1])}"
            nets[pin] = name
    return nets


def _check_erc() -> tuple[int, list[str]]:
    """KiCad's rule check at every severity: no error; every warning named in ACCEPTED_ERC_WARNINGS."""
    _kicad_cli("sch", "erc", "--severity-all", "--format", "json", "-o", str(ERC_REPORT_PATH), str(SCHEMATIC_PATH))
    report = json.loads(ERC_REPORT_PATH.read_text())
    findings = [item for sheet in report["sheets"] for item in sheet["violations"]]
    errors = [f"{item['type']}: {item['description']}" for item in findings if item["severity"] == "error"]
    warnings = [item for item in findings if item["severity"] != "error"]
    unexplained = sorted({f"{item['type']}: {item['description']}" for item in warnings
                          if item["type"] not in ACCEPTED_ERC_WARNINGS})
    assert not errors, f"ERC errors {errors}; see {ERC_REPORT_PATH}"
    assert not unexplained, f"ERC warnings without an explanation {unexplained}; see {ERC_REPORT_PATH}"
    return len(errors), [item["type"] for item in warnings]


def write_netlist_report() -> None:
    lines = [f"{net:14} {' '.join(pads)}" for net, pads in sorted(circuit.nets_to_pads(circuit.all_parts()).items())]
    NETLIST_REPORT_PATH.write_text("# Generated by pcb/gen/build.py from pcb/gen/circuit.py. Do not edit.\n"
                                   + "\n".join(lines) + "\n")


def write_schematic() -> dict[str, str]:
    """Schematic from circuit.py, then KiCad's own view of it: rule check, and the netlist compared pin by pin.

    Returns the nets of the open pins ("U1.21" -> "unconnected-(U1-P0.05-Pad21)") for the board."""
    import models

    BUILD_DIR.mkdir(exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    count = write_footprints()
    schematic.write(KICAD_DIR)
    errors, warnings = _check_erc()
    exported, wanted = _exported_nets(), schematic.nets_by_pin()
    open_pin_nets = {pin: net for pin, net in exported.items() if net.startswith(schematic.OPEN_PIN_NET_PREFIX)}
    drawn = {pin: schematic.circuit_net_name(net) for pin, net in exported.items() if pin not in open_pin_nets}
    wrong = sorted(pin for pin in drawn.keys() | wanted.keys() if drawn.get(pin) != wanted.get(pin))
    assert not wrong, f"schematic and circuit.py disagree on {wrong}"
    _kicad_cli("sch", "export", "svg", "--exclude-drawing-sheet", "-o", str(BUILD_DIR), str(SCHEMATIC_PATH))
    (BUILD_DIR / f"{circuit.LIBRARY}.svg").replace(IMAGE_DIR / "schematic.svg")
    _kicad_cli("sch", "export", "pdf", "-o", str(IMAGE_DIR / "schematic.pdf"), str(SCHEMATIC_PATH))
    write_netlist_report()
    modelled = models.write_models()
    print(f"footprints: {count} written and read back")
    print(f"schematic: ERC {errors} errors, {len(warnings)} warnings {sorted(set(warnings))}; "
          f"{len(drawn)} pins match circuit.py, {len(open_pin_nets)} open pins")
    print(f"models: {len(modelled)} block models in pcb/lib/3d")
    return open_pin_nets


def _read_route_order() -> tuple[str, ...]:
    if not ROUTE_ORDER_PATH.exists():
        return ()
    lines = ROUTE_ORDER_PATH.read_text().splitlines()
    return tuple(line.strip() for line in lines if line.strip() and not line.startswith("#"))


def _plan(head_start: tuple[str, ...], open_pin_nets: dict[str, str], board_path: Path = BOARD_PATH):
    """Builds and routes a board at board_path. pcbnew writes that path as soon as the board is made."""
    import layout
    import route

    board = layout.build_board(board_path, open_pin_nets)
    return board, route.route(board, route.Setup(layout.ROUTING_RULES, head_start))


def place() -> None:
    """Schematic first, then the board: placed, routed, planes filled, checked against the schematic."""
    import layout
    import route

    open_pin_nets = write_schematic()
    RULES_PATH.write_text(DESIGN_RULES)
    board, result = _plan(_read_route_order(), open_pin_nets)
    nets = board.GetNetCount() - 1 - len(open_pin_nets)
    print(f"placed {len(board.GetFootprints())} footprints, {nets} nets, {len(open_pin_nets)} open pins", flush=True)
    route.write_copper(board, result.router)
    ROUTING_REPORT_PATH.write_text("# Generated by pcb/gen/build.py place. Do not edit.\n"
                                   + "\n".join(result.report_lines()) + "\n")
    print(result.report_lines()[0])
    for line in result.unrouted:
        print("UNROUTED", line)
    layout.add_outer_ground_pours(board)
    _save_filled(board, BOARD_PATH)
    summary = check_drc(strict=not result.unrouted)
    check_keepout_copper(BOARD_PATH)
    check_ground_vias(BOARD_PATH)
    write_images()   # also for an unfinished board: the pictures show where it stands
    if result.unrouted:
        sys.exit(f"{len(result.unrouted)} pads unrouted; see {ROUTING_REPORT_PATH.relative_to(REPO_ROOT)}. "
                 "The board is not done.")
    route.check_sensitive_lengths(result.router)
    print(summary)


def _save_filled(board, path: Path) -> None:
    import pcbnew

    import layout

    pcbnew.SaveBoard(str(path), board)
    layout.write_stackup(path)
    # Filled on a freshly loaded board: on the board still in memory the fill ignores the holes.
    reloaded = pcbnew.LoadBoard(str(path))
    pcbnew.ZONE_FILLER(reloaded).Fill(reloaded.Zones())
    pcbnew.SaveBoard(str(path), reloaded)
    layout.check_stackup(pcbnew.LoadBoard(str(path)), path)


def check_drc(strict: bool = True) -> str:
    """kicad-cli DRC at every severity with schematic parity. Fails on any error, any unconnected item, any
    parity finding and any warning not in ACCEPTED_DRC_WARNINGS. Returns a one-line summary."""
    subprocess.run(["kicad-cli", "pcb", "drc", "--severity-all", "--schematic-parity", "--format", "json",
                    "-o", str(DRC_REPORT_PATH), str(BOARD_PATH)], check=True, stdout=subprocess.DEVNULL)
    report = json.loads(DRC_REPORT_PATH.read_text())
    findings = report["violations"]
    errors = [f"{v['type']}: {[i['description'] for i in v['items']]}" for v in findings if v["severity"] == "error"]
    warnings = [(v["type"], v["items"][0]["description"]) for v in findings if v["severity"] != "error"]
    unexplained = sorted(set(warnings) - set(ACCEPTED_DRC_WARNINGS))
    unconnected = report["unconnected_items"]
    parity = report["schematic_parity"]
    summary = (f"DRC: {len(errors)} errors, {len(warnings)} warnings ({len(unexplained)} not accepted), "
               f"{len(unconnected)} unconnected, {len(parity)} parity findings; report {DRC_REPORT_PATH.name}")
    print(summary, flush=True)
    if strict:
        assert not errors, f"DRC errors {errors[:10]}; see {DRC_REPORT_PATH}"
        assert not unconnected, f"{len(unconnected)} unconnected items; see {DRC_REPORT_PATH}"
        assert not parity, f"schematic parity {[p['description'] for p in parity][:10]}; see {DRC_REPORT_PATH}"
        assert not unexplained, f"DRC warnings without a reason {unexplained}; see {DRC_REPORT_PATH}"
    return summary


def check_keepout_copper(board_path: Path) -> None:
    """No track, via, pad or zone fill of the board inside the module's RF keep-out, on any copper layer.
    Independent of KiCad's rule-area check: it reads the filled copper back from the saved file."""
    import pcbnew

    import layout

    board = pcbnew.LoadBoard(str(board_path))
    module = next(fp for fp in board.GetFootprints() if fp.GetReference() == "U1")
    left, top, right, bottom = layout.rf_keepout_rect(module)
    area = pcbnew.SHAPE_POLY_SET()
    area.NewOutline()
    for x, y in ((left, top), (right, top), (right, bottom), (left, bottom)):
        area.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
    copper_layers = (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu)
    inside = []
    for track in board.GetTracks():
        box = track.GetBoundingBox()
        if area.Collide(box.Centre(), 0) or _box_overlaps(box, (left, top, right, bottom)):
            inside.append(f"{track.GetClass()} {track.GetNetname()}")
    for footprint in board.GetFootprints():
        for pad in footprint.Pads():
            if _box_overlaps(pad.GetBoundingBox(), (left, top, right, bottom)):
                inside.append(f"pad {footprint.GetReference()}.{pad.GetNumber()}")
    for zone in board.Zones():
        if zone.GetIsRuleArea():
            continue
        for layer in copper_layers:
            if zone.IsOnLayer(layer) and zone.HasFilledPolysForLayer(layer):
                fill = zone.GetFilledPolysList(layer)
                clipped = pcbnew.SHAPE_POLY_SET(fill)
                clipped.BooleanIntersection(area)
                if clipped.OutlineCount():
                    inside.append(f"{zone.GetNetname()} fill on {pcbnew.LayerName(layer)}")
    assert not inside, f"copper inside the RF keep-out: {inside}"
    print(f"RF keep-out {left:.2f}..{right:.2f} x {top:.2f}..{bottom:.2f}: no copper on any layer")


def check_ground_vias(board_path: Path) -> None:
    """The hand-placed ground vias are on the saved board: the charger's thermal vias inside its exposed pad,
    and the fence along the antenna keep-out, each one inside the filled ground on F.Cu, In1.Cu and B.Cu so it
    stitches the outer pours to the plane. check_keepout_copper already fails on a via inside the keep-out."""
    import pcbnew

    import layout
    import route

    board = pcbnew.LoadBoard(str(board_path))
    ground_vias = {(round(pcbnew.ToMM(via.GetPosition().x), 2), round(pcbnew.ToMM(via.GetPosition().y), 2))
                   for via in board.GetTracks() if via.GetClass() == "PCB_VIA" and via.GetNetname() == "GND"}
    reference, number = route.THERMAL_PAD.split(".")
    pad = next(p for fp in board.GetFootprints() if fp.GetReference() == reference for p in fp.Pads()
               if p.GetNumber() == number)
    x, y = layout.pad_xy(pad)
    thermal = [(round(x + dx, 2), round(y + dy, 2)) for dx, dy in route.THERMAL_VIA_OFFSETS]
    missing = [spot for spot in thermal if spot not in ground_vias]
    assert not missing, f"thermal vias missing in {route.THERMAL_PAD} at {missing}"
    outside_pad = [spot for spot in thermal if not pad.HitTest(pcbnew.VECTOR2I(*map(pcbnew.FromMM, spot)))]
    assert not outside_pad, f"thermal vias outside {route.THERMAL_PAD}: {outside_pad}"
    fence = route.rf_stitch_points(layout.ROUTING_RULES)
    missing = [spot for spot in fence if (round(spot[0], 2), round(spot[1], 2)) not in ground_vias]
    assert not missing, f"RF keep-out fence vias missing at {missing}"
    fills = {layer: pcbnew.SHAPE_POLY_SET() for layer in (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.B_Cu)}
    for zone in board.Zones():
        for layer, fill in fills.items():
            if not zone.GetIsRuleArea() and zone.GetNetname() == "GND" and zone.HasFilledPolysForLayer(layer):
                fill.BooleanAdd(zone.GetFilledPolysList(layer))
    unstitched = [f"({x}, {y}) {pcbnew.LayerName(layer)}" for x, y in fence for layer, fill in fills.items()
                  if not fill.Collide(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)), 0)]
    assert not unstitched, f"fence vias outside the ground fill: {unstitched}"
    print(f"ground vias: {len(thermal)} in {route.THERMAL_PAD}, {len(fence)} in the RF keep-out fence, "
          "each in the ground fill on F.Cu, In1.Cu and B.Cu")


def _box_overlaps(box, rect: tuple[float, float, float, float]) -> bool:
    import pcbnew

    left, top, right, bottom = rect
    return (pcbnew.ToMM(box.GetRight()) > left and pcbnew.ToMM(box.GetLeft()) < right
            and pcbnew.ToMM(box.GetBottom()) > top and pcbnew.ToMM(box.GetTop()) < bottom)


def order() -> None:
    """Routes again and again; the nets that ended up walled in go to the front of the next round. Writes the
    order of the best round to route_order.txt, and fails when no round connects every pad."""
    head_start = _read_route_order()
    open_pin_nets = write_schematic()
    best: tuple[int, tuple[str, ...]] | None = None
    for round_number in range(1, ORDER_SEARCH_ROUNDS + 1):
        _, result = _plan(head_start, open_pin_nets, BUILD_DIR / "order.kicad_pcb")
        walled_in = list(dict.fromkeys(line.split(":")[0] for line in result.unrouted))
        print(f"round {round_number}: {len(result.unrouted)} unrouted {walled_in}", flush=True)
        if best is None or len(result.unrouted) < best[0]:
            best = (len(result.unrouted), head_start)
        if not walled_in:
            break
        head_start = tuple(walled_in) + tuple(net for net in head_start if net not in walled_in)
    unrouted, chosen = best
    ROUTE_ORDER_PATH.write_text(_ORDER_HEADER + f"# Best round left {unrouted} pads unrouted.\n"
                                + "".join(f"{net}\n" for net in chosen))
    if unrouted:
        sys.exit(f"no complete routing order in {ORDER_SEARCH_ROUNDS} rounds; best left {unrouted} pads unrouted")


def _render(board_path: Path, name: str, *view: str) -> None:
    _kicad_cli("pcb", "render", *view, "--width", "1600", "--height", "1200", "--quality", "high",
               "--background", "opaque", "-o", str(IMAGE_DIR / f"{name}.png"), str(board_path))


def _write_bare_copy() -> Path:
    """The board without its part models, so the bare-board renders show the silkscreen."""
    import pcbnew

    board = pcbnew.LoadBoard(str(BOARD_PATH))
    for footprint in board.GetFootprints():
        footprint.Models().clear()
    bare_path = BUILD_DIR / "bare.kicad_pcb"
    pcbnew.SaveBoard(str(bare_path), board)
    return bare_path


def write_images() -> None:
    """Renders of the bare and the populated board, one drawing per copper layer, two assembly drawings."""
    bare_path = _write_bare_copy()
    for side in ("top", "bottom"):
        _render(bare_path, f"bare-{side}", "--side", side)
        _render(BOARD_PATH, f"assembled-{side}", "--side", side)
    _render(BOARD_PATH, "assembled-angle", "--rotate", ANGLED_VIEW_ROTATION, "--perspective", "--zoom", "0.8")
    _render(BOARD_PATH, "assembled-underside", "--rotate", UNDERSIDE_VIEW_ROTATION, "--perspective", "--zoom", "0.8")
    drawings = {"copper-top": "F.Cu", "copper-ground": "In1.Cu", "copper-3v3": "In2.Cu", "copper-bottom": "B.Cu",
                "assembly-top": "F.Fab,F.SilkS", "assembly-bottom": "B.Fab,B.SilkS"}
    for name, layers in drawings.items():
        mirror = ["--mirror"] if name in ("assembly-bottom", "copper-bottom") else []
        _kicad_cli("pcb", "export", "svg", "--layers", f"{layers},Edge.Cuts", "--exclude-drawing-sheet",
                   "--page-size-mode", "2", *mirror, "-o", str(IMAGE_DIR / f"{name}.svg"), str(BOARD_PATH))


def fab_step() -> None:
    import fab

    fab.write_all(BOARD_PATH)


def fab_draft() -> None:
    """The fab step on an unfinished board, into pcb/.build/draft/. For testing the generator only."""
    import fab

    fab.write_all(BOARD_PATH, draft=True)


STEPS = {"test": test, "schematic": write_schematic, "place": place, "order": order, "fab": fab_step,
         "fab-draft": fab_draft,
         "drc": check_drc, "images": write_images}

if __name__ == "__main__":
    step = STEPS.get(sys.argv[1] if len(sys.argv) > 1 else "")
    if step is None:
        sys.exit(__doc__)
    step()
