"""Fabrication outputs from the routed board. Runs inside the KiCad container (pcbnew, kicad-cli).

    pcb/fab/                         the single board: Gerbers and drill files (gerbers/), their zip,
                                     the KiCad position file, the drill report
    pcb/production/jlcpcb/           the panel (D23): Gerber zip, BOM, CPL with the rotation table applied,
                                     README with the order-form settings and the remark text
    pcb/production/pcbway/           MPN BOM, centroid file (KiCad's own positions and angles), README
    pcb/production/worxpad-pcb.step  the board with block models, for the case fit check and renders

Every output is reproducible: KiCad's creation dates are cut out of the Gerbers and drill files, and the
zips carry a fixed time and order. Nothing here has been sent to a manufacturer.
"""

from __future__ import annotations

import csv
import io
import json
import math
import re
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

import pcbnew

import circuit
import layout
import models
from circuit import BOARD_SPEC, BOTTOM, Part

PCB_DIR = circuit.REPO_ROOT / "pcb"
BUILD_DIR = PCB_DIR / ".build"
NAME = circuit.LIBRARY
PANEL = BOARD_SPEC["panel"]
# The board STEP carries the solder mask skins, so its envelope is the finished board and not only the body
# between the outer copper layers. The tolerance covers the stack-up sum (layout.STACKUP, 1.606 mm) and the
# mask placement: the trial export on 2026-11-14 measured 1.616 mm.
STEP_BOARD_OPTIONS = ("--include-soldermask",)
STEP_THICKNESS_TOLERANCE = 0.02

GERBER_LAYERS = ("F.Cu", "In1.Cu", "In2.Cu", "B.Cu", "F.Paste", "B.Paste", "F.Silkscreen", "B.Silkscreen",
                 "F.Mask", "B.Mask", "Edge.Cuts")
GERBER_SUFFIXES = ("-F_Cu.gtl", "-In1_Cu.g1", "-In2_Cu.g2", "-B_Cu.gbl", "-F_Paste.gtp", "-B_Paste.gbp",
                   "-F_Silkscreen.gto", "-B_Silkscreen.gbo", "-F_Mask.gts", "-B_Mask.gbs", "-Edge_Cuts.gm1",
                   "-PTH.drl", "-NPTH.drl")
ZIP_TIME = (2026, 1, 1, 0, 0, 0)
_DATE_LINES = (
    (re.compile(r"^G04 #@! TF\.CreationDate,.*\n", re.M), ""),
    (re.compile(r"^; #@! TF\.CreationDate,.*\n", re.M), ""),
    (re.compile(r"^%TF\.CreationDate,.*\n", re.M), ""),
    (re.compile(r"^(G04 Created by KiCad \([^)]*\)) date [^*]*\*$", re.M), r"\1*"),
    (re.compile(r"^(; DRILL file .*?) date \S+$", re.M), r"\1"),
    (re.compile(r"^; #@! TF\.GenerationSoftware.*\n", re.M), ""),
)

# JLCPCB rotation corrections: (footprint pattern, degrees added to the KiCad angle, reason). Seeded from
# worxboard/pcb/scripts/jlc_rotations.csv (SOT-23-5/6, SOIC-8 5.3 mm) where it has a row. Every other row is
# reasoned from the footprint's zero orientation and has NOT been checked against JLCPCB's library models:
# the README tells the person ordering to check each designator in JLCPCB's placement preview.
ROTATIONS = (
    (r"^Package_TO_SOT_SMD:SOT-23-[56]$", -90, "worxboard row; KiCad zero has pin 1 top left, pins in columns"),
    (r"^Package_SO:SOIC-8_5\.3x5\.3mm_P1\.27mm$", 270, "worxboard row, same footprint"),
    (r"^Package_TO_SOT_SMD:SOT-23$", 180, "not in worxboard; the common community table value for SOT-23. CHECK"),
    (r"^Package_DFN_QFN:(VQFN|DFN)-", 270, "not in worxboard; same pin-1 corner rule as SOIC. CHECK"),
    (r"^Connector_JST:JST_PH_S2B-PH-SM4-TB", 180, "not in worxboard; KiCad has the pins at -Y, mouth at +Y. CHECK"),
)
# JLCPCB places the part centre. A footprint whose origin is not the body centre gets the centre of its
# fabrication outline instead (J1 edge line, J2 rear edge, J3 pin row).
CENTRE_FROM_FAB = True


# --- small file helpers ------------------------------------------------------------------------------------

def _kicad_cli(*arguments: str) -> None:
    subprocess.run(["kicad-cli", *arguments], check=True, stdout=subprocess.DEVNULL)


def _strip_dates(path: Path) -> None:
    text = path.read_text()
    for pattern, replacement in _DATE_LINES:
        text = pattern.sub(replacement, text)
    assert not re.search(r"20\d\d-\d\d-\d\d", text), f"{path.name}: a date survived"
    path.write_text(text)


def _zip(files: dict[str, bytes], path: Path) -> None:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            info.create_system = 3
            archive.writestr(info, files[name], compresslevel=9)
    path.write_bytes(buffer.getvalue())


def _csv(rows: list[list[str]], path: Path) -> None:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerows(rows)
    path.write_text(buffer.getvalue())


def export_gerbers(board_path: Path, out_dir: Path) -> dict[str, bytes]:
    """Gerbers (Protel names) and Excellon drills, PTH and NPTH apart. Returns {file name: bytes}."""
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    _kicad_cli("pcb", "export", "gerbers", "--layers", ",".join(GERBER_LAYERS), "--no-x2", "--no-netlist",
               "--subtract-soldermask", "-o", str(out_dir), str(board_path))
    _kicad_cli("pcb", "export", "drill", "--format", "excellon", "--excellon-separate-th", "--excellon-units", "mm",
               "--generate-map", "--map-format", "pdf", "-o", f"{out_dir}/", str(board_path))
    files = {}
    stem = board_path.stem
    for suffix in GERBER_SUFFIXES:
        path = out_dir / f"{stem}{suffix}"
        assert path.is_file() and path.stat().st_size > 0, f"missing or empty {path.name}"
        _strip_dates(path)
        files[path.name] = path.read_bytes()
    return files


def drill_hits(drill: bytes) -> dict[str, int]:
    """Excellon file -> hole count per tool diameter ("0.300")."""
    diameter_of_tool: dict[str, str] = {}
    hits: dict[str, int] = defaultdict(int)
    current = ""
    for line in drill.decode().splitlines():
        tool = re.fullmatch(r"(T\d+)(?:C([\d.]+))?", line)
        if tool and tool.group(2):
            diameter_of_tool[tool.group(1)] = f"{float(tool.group(2)):.3f}"
        elif tool:
            current = diameter_of_tool.get(tool.group(1), "")
        elif line.startswith("X") or line.startswith("Y"):
            hits[current] += 1
    return dict(hits)


# --- the panel (D23) ---------------------------------------------------------------------------------------

def _poly(points: list[tuple[float, float]]) -> pcbnew.SHAPE_POLY_SET:
    poly = pcbnew.SHAPE_POLY_SET()
    poly.NewOutline()
    for x, y in points:
        poly.Append(layout.mm(x), layout.mm(y))
    return poly


def _rect_points(left: float, top: float, right: float, bottom: float) -> list[tuple[float, float]]:
    return [(left, top), (right, top), (right, bottom), (left, bottom)]


def tab_spans() -> list[tuple[str, float, tuple[float, float, float, float]]]:
    """(edge, centre, rectangle) of every tab: the strip of board material across the routed gap."""
    pcb, gap, half = BOARD_SPEC["pcb"], PANEL["routed_gap"], PANEL["tab_width"] / 2
    spans = []
    for edge, centre in PANEL["tabs"]:
        rect = {"left": (pcb["x0"] - gap - 0.5, centre - half, pcb["x0"] + 0.5, centre + half),
                "right": (pcb["x1"] - 0.5, centre - half, pcb["x1"] + gap + 0.5, centre + half),
                "rear": (centre - half, pcb["y0"] - gap - 0.5, centre + half, pcb["y0"] + 0.5),
                "front": (centre - half, pcb["y1"] - 0.5, centre + half, pcb["y1"] + gap + 0.5)}[edge]
        spans.append((edge, centre, rect))
    return spans


def panel_frame() -> tuple[float, float, float, float]:
    """Outer edge of the frame: the board's box grown by the routed gap and one rail on every side."""
    pcb = BOARD_SPEC["pcb"]
    grow = PANEL["routed_gap"] + PANEL["rail_width"]
    rear = min([pcb["y0"]] + [tongue["y0"] for tongue in pcb["tongues"]])
    return pcb["x0"] - grow, rear - grow, pcb["x1"] + grow, pcb["y1"] + grow


def mouse_bites() -> list[tuple[float, float]]:
    """Perforation centres: one row per tab, centres 0.25 mm inside the board outline (D23)."""
    pcb, pitch = BOARD_SPEC["pcb"], PANEL["tab_hole_pitch"]
    inset = PANEL["tab_hole"] / 2
    count = int((PANEL["tab_width"] - PANEL["tab_hole"]) / pitch) + 1
    offsets = [(k - (count - 1) / 2) * pitch for k in range(count)]
    holes = []
    for edge, centre, _ in tab_spans():
        for offset in offsets:
            holes.append({"left": (pcb["x0"] + inset, centre + offset), "right": (pcb["x1"] - inset, centre + offset),
                          "rear": (centre + offset, pcb["y0"] + inset),
                          "front": (centre + offset, pcb["y1"] - inset)}[edge])
    return holes


def build_panel(board_path: Path, panel_path: Path) -> dict:
    """The board in a frame of four rails, joined by the [panel] tabs. Returns the facts the README quotes."""
    assert all(kind == "routed" for kind in PANEL["edges"].values()), "only routed edges are drawn (D23)"
    board = pcbnew.LoadBoard(str(board_path))
    for item in list(board.GetDrawings()):
        if item.GetLayer() == pcbnew.Edge_Cuts:
            board.Remove(item)
    outline = _poly(layout.outline_points())
    clear = _poly(layout.outline_points())
    for notch in BOARD_SPEC["pcb"]["notches"]:   # the receptacle sits in its notch: no frame finger there
        clear.BooleanAdd(_poly(_rect_points(notch["x0"], notch["y0"], notch["x1"], notch["y1"])))
    clear.Simplify()
    clear.Inflate(layout.mm(PANEL["routed_gap"]), pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS, layout.mm(0.005))
    slot = pcbnew.SHAPE_POLY_SET(clear)
    slot.BooleanSubtract(outline)
    for _, _, rect in tab_spans():
        slot.BooleanSubtract(_poly(_rect_points(*rect)))
    slot.Simplify()
    for index in range(slot.OutlineCount()):
        _edge_polygon(board, slot, index)
        assert slot.HoleCount(index) == 0, "a routed slot piece has a hole"
    frame = panel_frame()
    _edge_polygon(board, _poly(_rect_points(*frame)), 0)
    holder = pcbnew.FOOTPRINT(board)
    holder.SetReference("MB1")
    holder.SetValue("mouse bites")
    holder.SetExcludedFromBOM(True)
    holder.SetExcludedFromPosFiles(True)
    holder.SetBoardOnly(True)
    board.Add(holder)
    for x, y in mouse_bites():
        pad = pcbnew.PAD(holder)
        pad.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
        pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        size = layout.mm(PANEL["tab_hole"])
        pad.SetSize(pcbnew.F_Cu, pcbnew.VECTOR2I(size, size))
        pad.SetDrillSize(pcbnew.VECTOR2I(size, size))
        pad.SetLayerSet(pcbnew.LSET.AllCuMask())
        pad.SetPosition(layout.point(x, y))
        holder.Add(pad)
    pieces = slot.OutlineCount()
    pcbnew.SaveBoard(str(panel_path), board)
    return {"pieces": pieces, "frame": frame, "bites": len(mouse_bites())}


def _edge_polygon(board: pcbnew.BOARD, poly: pcbnew.SHAPE_POLY_SET, outline: int) -> None:
    """One outline of a polygon set as Edge.Cuts segments."""
    count = poly.VertexCount(outline, -1)
    for index in range(count):
        start, end = poly.CVertex(index, outline, -1), poly.CVertex((index + 1) % count, outline, -1)
        if start == end:
            continue
        line = pcbnew.PCB_SHAPE(board, pcbnew.SHAPE_T_SEGMENT)
        line.SetStart(start)
        line.SetEnd(end)
        line.SetLayer(pcbnew.Edge_Cuts)
        line.SetWidth(layout.mm(0.05))
        board.Add(line)


def check_panel(panel_path: Path, board_unconnected: int) -> dict:
    """Panel DRC (errors only; parity is checked on the board) and the D23 distances. The panel may add no
    error and no unconnected item to the board's own (zero for a finished board)."""
    rules = PCB_DIR / "kicad" / f"{NAME}.kicad_dru"
    shutil.copyfile(rules, panel_path.with_suffix(".kicad_dru"))
    report_path = BUILD_DIR / "panel-drc.json"
    _kicad_cli("pcb", "drc", "--severity-error", "--format", "json", "-o", str(report_path), str(panel_path))
    report = json.loads(report_path.read_text())
    errors = [f"{v['type']}: {[i['description'] for i in v['items']]}" for v in report["violations"]]
    unconnected = len(report["unconnected_items"])
    assert not errors and unconnected == board_unconnected, \
        f"panel DRC: {errors[:8]}, {unconnected} unconnected (board {board_unconnected}); see {report_path}"
    nearest = _nearest_tab_to_antenna()
    assert nearest >= PANEL["tab_to_antenna_min"], f"a tab is {nearest:.1f} mm from the antenna strip"
    return {"tab_to_antenna": nearest}


def _nearest_tab_to_antenna() -> float:
    """Plan distance from any tab span to the antenna strip: the last antenna_strip of the module body, the
    module's width across (D23 quotes 14.4 mm)."""
    module, pcb = BOARD_SPEC["module"], BOARD_SPEC["pcb"]
    left = pcb["x1"] - module["antenna_inset"] - module["antenna_strip"]
    top = module["centre_y"] - module["width"] / 2
    bottom = module["centre_y"] + module["width"] / 2
    best = math.inf
    for _, _, (x0, y0, x1, y1) in tab_spans():
        dx = max(left - x1, x0 - pcb["x1"], 0.0)
        dy = max(top - y1, y0 - bottom, 0.0)
        best = min(best, math.hypot(dx, dy))
    return best


# --- BOM and placement ---------------------------------------------------------------------------------------

def _rotation_correction(footprint_name: str) -> tuple[float, str]:
    for pattern, degrees, reason in ROTATIONS:
        if re.search(pattern, footprint_name):
            return degrees, reason
    return 0.0, ""


def _part_centre(footprint: pcbnew.FOOTPRINT) -> tuple[float, float]:
    """Body centre: the box round the fabrication-layer drawing, or the footprint origin when it has none."""
    layer = pcbnew.B_Fab if footprint.IsFlipped() else pcbnew.F_Fab
    boxes = [item.GetBoundingBox() for item in footprint.GraphicalItems()
             if item.GetLayer() == layer and item.GetClass() == "PCB_SHAPE"]
    if not boxes:
        return layout.pcbnew_xy(footprint)
    return (pcbnew.ToMM(min(b.GetLeft() for b in boxes) + max(b.GetRight() for b in boxes)) / 2,
            pcbnew.ToMM(min(b.GetTop() for b in boxes) + max(b.GetBottom() for b in boxes)) / 2)


def placement_rows(board: pcbnew.BOARD, parts: list[Part], jlc: bool) -> list[list[str]]:
    """One row per machine-placed part. JLCPCB: body centre, top view, Y up, rotation table applied, bottom angle
    as 180 minus the KiCad angle plus the correction (KiKit and kicad-jlcpcb-tools convention). PCBWay: the
    footprint origin and KiCad's own angle, as KiCad's position file gives them."""
    assembled = {part.ref: part for part in parts if part.machine_assembled}
    rows = []
    for footprint in sorted(board.GetFootprints(), key=lambda fp: fp.GetReference()):
        ref = footprint.GetReference()
        if ref not in assembled:
            continue
        bottom = assembled[ref].side == BOTTOM
        assert footprint.IsFlipped() == bottom, f"{ref}: face differs from circuit.py"
        angle = footprint.GetOrientationDegrees()
        if jlc:
            x, y = _part_centre(footprint)
            correction, _ = _rotation_correction(assembled[ref].footprint)
            rotation = ((180 - angle if bottom else angle) + correction) % 360
        else:
            x, y = layout.pcbnew_xy(footprint)
            rotation = angle % 360
        rows.append([ref, f"{x:.3f}mm", f"{-y:.3f}mm", "Bottom" if bottom else "Top", f"{rotation:.0f}"])
    return rows


def bom_groups(parts: list[Part]) -> dict[tuple[str, str, str], list[str]]:
    groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for part in parts:
        if part.machine_assembled:
            groups[(part.value, part.footprint.split(":")[1], part.lcsc)].append(part.ref)
    return dict(sorted(groups.items()))


def write_jlc_bom(parts: list[Part], path: Path) -> list[list[str]]:
    rows = [["Comment", "Designator", "Footprint", "LCSC Part #"]]
    for (value, package, lcsc), refs in bom_groups(parts).items():
        rows.append([value, ",".join(sorted(refs, key=_ref_key)), package, lcsc])
    _csv(rows, path)
    return rows


# Manufacturer part numbers from the research records (research/components/*.md tables). Values that are
# already an MPN in circuit.py are used as they are. "" means the records name only the LCSC number.
RECORDED_MPN = {
    "C1525": ("Samsung", "CL05B104KO5NNNC"), "C19702": ("Samsung", "CL10A106KP8NNNC"),
    "C15849": ("Samsung", "CL10A105KB8NNNC"), "C25741": ("UNI-ROYAL", "0402WGF1003TCE"),
    "C25890": ("UNI-ROYAL", "0402WGF3301TCE"), "C25879": ("UNI-ROYAL", "0402WGF2201TCE"),
    "C25900": ("UNI-ROYAL", "0402WGF4701TCE"), "C51597": ("Fenghua", "CMFB103F3950FANT"),
    "C99563": ("Littelfuse", "1206L075THYR"), "C32346": ("Epson", "Q13FC1350000400"),
    "C81598": ("Semtech", "1N4148W"), "C1554": ("", ""), "C52923": ("", ""), "C25083": ("", ""),
    "C25905": ("", ""),
}
MANUFACTURER = {
    "BMD-340-A-R": "u-blox", "W25Q128JVSIQ": "Winbond", "AO3400A": "Alpha & Omega", "AO3401A": "Alpha & Omega",
    "BQ24072RGTR": "Texas Instruments", "TPS7A0233PDBVR": "Texas Instruments", "MAX17048G+T10": "Analog Devices",
    "USBLC6-2SC6": "STMicroelectronics", "TYPE-C-31-M-13C": "HRO", "FH34SRJ-24S-0.5SH(50)": "Hirose",
    "S2B-PH-SM4-TB": "JST", "MSK12C02": "Shouhan", "TS-1187A-B-A-B": "XKB", "B3FS-1000P": "Omron",
    "PEC12R-4215F-S0024": "Bourns", "1206L075THYR": "Littelfuse",
}


def write_pcbway_bom(parts: list[Part], path: Path) -> list[list[str]]:
    rows = [["Item", "Designator", "Qty", "Manufacturer", "Manufacturer Part Number", "Description", "Package",
             "LCSC (reference)"]]
    for item, ((value, package, lcsc), refs) in enumerate(bom_groups(parts).items(), start=1):
        if lcsc in RECORDED_MPN:
            maker, mpn = RECORDED_MPN[lcsc]
        else:
            maker, mpn = MANUFACTURER.get(value, ""), value
        description = value if mpn != value else ""
        if not mpn:
            description = f"{value}; no MPN in the records, any part to the LCSC number's data"
        rows.append([str(item), ",".join(sorted(refs, key=_ref_key)), str(len(refs)), maker, mpn, description,
                     package, lcsc])
    _csv(rows, path)
    return rows


def _ref_key(ref: str) -> tuple[str, int]:
    match = re.fullmatch(r"([A-Z]+)(\d+)", ref)
    return (match.group(1), int(match.group(2))) if match else (ref, 0)


# --- STEP with block models ----------------------------------------------------------------------------------

def write_step(board_path: Path, step_path: Path) -> int:
    """The board as STEP with the block models. kicad-cli exports only STEP models, so every VRML block model
    is written again as a STEP prism set (same solids, models.solids) into pcb/.build/step-models/, and a copy of
    the board that points at them is exported. Returns the number of model files."""
    model_dir = BUILD_DIR / "step-models"
    model_dir.mkdir(parents=True, exist_ok=True)
    keys = sorted({part.footprint_key for part in circuit.all_parts()} & models.MODELLED)
    for key in keys:
        (model_dir / f"{key}.step").write_text(step_text(key, models.solids(key, models.load_footprint(key))))
    board = pcbnew.LoadBoard(str(board_path))
    for footprint in board.GetFootprints():
        keys_here = [Path(model.m_Filename).stem for model in footprint.Models()]
        footprint.Models().clear()   # iterating Models() gives copies: rebuild the list instead
        for key in keys_here:
            model = pcbnew.FP_3DMODEL()
            model.m_Filename = str(model_dir / f"{key}.step")
            footprint.Models().push_back(model)
    copy_path = BUILD_DIR / "step-copy.kicad_pcb"
    pcbnew.SaveBoard(str(copy_path), board)
    _kicad_cli("pcb", "export", "step", "--force", "--no-dnp", *STEP_BOARD_OPTIONS, "-o", str(step_path),
               str(copy_path))
    check_step_thickness(copy_path)
    text = step_path.read_text(errors="replace")
    text = re.sub(r"FILE_NAME\('([^']*)','[^']*'", r"FILE_NAME('\1','2026-01-01T00:00:00'", text, count=1)
    step_path.write_text(text)
    return len(keys)


def check_step_thickness(board_path: Path) -> float:
    """Exports the board alone with the same options and asserts that its Z extent is pcb.thickness. Returns
    the extent. KiCad's board body runs between the outer copper layers only (1.516 mm for this stack-up); the
    solder mask option adds both outer skins, so the envelope is the finished board."""
    check_path = BUILD_DIR / "board-only.step"
    _kicad_cli("pcb", "export", "step", "--force", "--no-components", *STEP_BOARD_OPTIONS, "-o", str(check_path),
               str(board_path))
    heights = [float(z) for z in re.findall(r"CARTESIAN_POINT\('[^']*',\(\s*[-0-9.E+]+,\s*[-0-9.E+]+,\s*([-0-9.E+]+)\)",
                                            check_path.read_text(errors="replace"))]
    assert heights, f"{check_path.name}: no points"
    extent = max(heights) - min(heights)
    thickness = BOARD_SPEC["pcb"]["thickness"]
    assert abs(extent - thickness) <= STEP_THICKNESS_TOLERANCE, \
        f"board STEP is {extent:.3f} mm thick, pcb.thickness is {thickness} mm"
    print(f"STEP board envelope {extent:.3f} mm (pcb.thickness {thickness})")
    return extent


def step_text(name: str, solids: list[models.Solid]) -> str:
    """A STEP AP214 file of faceted prisms, millimetres, in the footprint frame KiCad expects of a model
    (X right, Y up, Z out of the footprint's face)."""
    entities: list[str] = []

    def add(text: str) -> int:
        entities.append(text)
        return len(entities)

    origin = add("CARTESIAN_POINT('',(0.,0.,0.))")
    z_axis = add("DIRECTION('',(0.,0.,1.))")
    x_axis = add("DIRECTION('',(1.,0.,0.))")
    placement = add(f"AXIS2_PLACEMENT_3D('',#{origin},#{z_axis},#{x_axis})")
    breps = []
    for solid in solids:
        polygon = models._footprint_polygon(solid)
        count = len(polygon)
        bottom = [add(f"CARTESIAN_POINT('',({x:.5f},{y:.5f},{solid.z_bottom:.5f}))") for x, y in polygon]
        top = [add(f"CARTESIAN_POINT('',({x:.5f},{y:.5f},{solid.z_top:.5f}))") for x, y in polygon]
        loops = [list(reversed(bottom)), top]
        loops += [[bottom[i], bottom[(i + 1) % count], top[(i + 1) % count], top[i]] for i in range(count)]
        faces = []
        for loop in loops:
            poly_loop = add("POLY_LOOP('',(" + ",".join(f"#{p}" for p in loop) + "))")
            bound = add(f"FACE_OUTER_BOUND('',#{poly_loop},.T.)")
            faces.append(add(f"FACE('',(#{bound}))"))
        shell = add("CLOSED_SHELL('',(" + ",".join(f"#{f}" for f in faces) + "))")
        breps.append(add(f"FACETED_BREP('',#{shell})"))
    length = add("(LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.))")
    angle = add("(NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.))")
    solid_angle = add("(NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT())")
    uncertainty = add(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-05),#{length},'distance_accuracy_value','')")
    context = add("(GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#"
                  f"{uncertainty})) GLOBAL_UNIT_ASSIGNED_CONTEXT((#{length},#{angle},#{solid_angle})) "
                  "REPRESENTATION_CONTEXT('',''))")
    items = ",".join(f"#{b}" for b in breps)
    representation = add(f"FACETED_BREP_SHAPE_REPRESENTATION('{name}',(#{placement},{items}),#{context})")
    app = add("APPLICATION_CONTEXT('automotive design')")
    add(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#{app})")
    product_context = add(f"PRODUCT_CONTEXT('',#{app},'mechanical')")
    product = add(f"PRODUCT('{name}','{name}','',(#{product_context}))")
    formation = add(f"PRODUCT_DEFINITION_FORMATION('','',#{product})")
    definition_context = add(f"PRODUCT_DEFINITION_CONTEXT('part definition',#{app},'design')")
    definition = add(f"PRODUCT_DEFINITION('design','',#{formation},#{definition_context})")
    shape = add(f"PRODUCT_DEFINITION_SHAPE('','',#{definition})")
    add(f"SHAPE_DEFINITION_REPRESENTATION(#{shape},#{representation})")
    body = "\n".join(f"#{index}={text};" for index, text in enumerate(entities, start=1))
    return ("ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('worxpad block model'),'2;1');\n"
            f"FILE_NAME('{name}.step','2026-01-01T00:00:00',(''),(''),'','worxpad pcb/gen/fab.py','');\n"
            "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n"
            f"{body}\nENDSEC;\nEND-ISO-10303-21;\n")


# --- everything ----------------------------------------------------------------------------------------------

def check_outputs(board: pcbnew.BOARD, parts: list[Part], board_files: dict[str, bytes],
                  bom: list[list[str]], cpl: list[list[str]]) -> dict:
    """The order files agree with the board, with circuit.py and with each other."""
    vias = [track for track in board.GetTracks() if track.GetClass() == "PCB_VIA"]
    drills = {f"{pcbnew.ToMM(via.GetDrillValue()):.3f}" for via in vias}
    assert len(drills) == 1, f"vias with different drills: {drills}"
    plated = drill_hits(board_files[f"{NAME}-PTH.drl"])
    via_drill = drills.pop()
    pth_pads = [pad for fp in board.GetFootprints() for pad in fp.Pads()
                if pad.GetAttribute() == pcbnew.PAD_ATTRIB_PTH
                and abs(pcbnew.ToMM(pad.GetDrillSize().x) - float(via_drill)) < 1e-3]
    assert plated.get(via_drill, 0) == len(vias) + len(pth_pads), \
        f"{len(vias)} vias on the board, {plated.get(via_drill, 0)} {via_drill} mm holes in the drill file"
    machine = sorted(part.ref for part in parts if part.machine_assembled)
    listed = sorted(ref for row in bom[1:] for ref in row[1].split(","))
    placed = sorted(row[0] for row in cpl[1:])
    assert listed == placed == machine, "BOM, placement list and circuit.py differ"
    missing = [row[0] for row in bom[1:] if not re.fullmatch(r"C\d+", row[3])]
    assert not missing, f"no JLCPCB part number for {missing}"
    return {"vias": len(vias), "via_drill": via_drill, "parts": len(machine), "bom_lines": len(bom) - 1,
            "bottom": sum(row[3] == "Bottom" for row in cpl[1:])}


def board_is_finished(drc_report: Path) -> tuple[bool, str]:
    """The last `build.py place` DRC: no error, no unconnected item, no parity finding."""
    if not drc_report.exists():
        return False, "no DRC report; run build.py place first"
    report = json.loads(drc_report.read_text())
    errors = sum(v["severity"] == "error" for v in report["violations"])
    unconnected, parity = len(report["unconnected_items"]), len(report["schematic_parity"])
    return (errors == unconnected == parity == 0,
            f"DRC {errors} errors, {unconnected} unconnected, {parity} parity findings")


def write_all(board_path: Path, draft: bool = False) -> None:
    """The order files. Refuses an unfinished board; draft=True writes the same files under pcb/.build/draft/
    instead, so the generator can be exercised on a board that is not done. A draft is never an order."""
    finished, state = board_is_finished(BUILD_DIR / "drc.json")
    assert draft or finished, f"the board is not finished ({state}); no order files written"
    root = BUILD_DIR / "draft" if draft else PCB_DIR
    fab_dir, production_dir = root / "fab", root / "production"
    jlc_dir, pcbway_dir = production_dir / "jlcpcb", production_dir / "pcbway"
    parts = circuit.all_parts()
    board = pcbnew.LoadBoard(str(board_path))
    fab_dir.mkdir(parents=True, exist_ok=True)
    board_files = export_gerbers(board_path, fab_dir / "gerbers")
    _zip(board_files, fab_dir / f"{NAME}-gerbers.zip")
    _kicad_cli("pcb", "export", "pos", "--format", "csv", "--units", "mm", "--side", "both", "--smd-only",
               "--exclude-dnp", "-o", str(fab_dir / f"{NAME}-pos.csv"), str(board_path))

    for directory in (jlc_dir, pcbway_dir):
        directory.mkdir(parents=True, exist_ok=True)
    panel_path = BUILD_DIR / f"{NAME}-panel.kicad_pcb"
    # Own processes: pcbnew cannot load a second project's board next to one it holds. The fill runs on the
    # freshly loaded panel, as build.py fills the board: in memory the fill ignores the new holes.
    subprocess.run([sys.executable, __file__, "panel", str(board_path), str(panel_path)], check=True)
    subprocess.run([sys.executable, __file__, "fill", str(panel_path)], check=True)
    panel = json.loads((BUILD_DIR / "panel-facts.json").read_text())
    board_unconnected = len(json.loads((BUILD_DIR / "drc.json").read_text())["unconnected_items"])
    panel |= check_panel(panel_path, board_unconnected)
    panel_files = export_gerbers(panel_path, BUILD_DIR / "panel-gerbers")
    _zip(panel_files, jlc_dir / f"{NAME}-panel-gerbers.zip")
    bom = write_jlc_bom(parts, jlc_dir / "bom.csv")
    cpl = [["Designator", "Mid X", "Mid Y", "Layer", "Rotation"]] + placement_rows(board, parts, jlc=True)
    _csv(cpl, jlc_dir / "cpl.csv")
    facts = check_outputs(board, parts, board_files, bom, cpl) | panel
    _zip({name: (jlc_dir / name).read_bytes() for name in ("bom.csv", "cpl.csv")}
         | {f"{NAME}-panel-gerbers.zip": (jlc_dir / f"{NAME}-panel-gerbers.zip").read_bytes()},
         jlc_dir / f"{NAME}-jlcpcb-order.zip")

    write_pcbway_bom(parts, pcbway_dir / "bom-mpn.csv")
    centroid = [["Designator", "Mid X", "Mid Y", "Layer", "Rotation"]] + placement_rows(board, parts, jlc=False)
    _csv(centroid, pcbway_dir / "centroid.csv")
    _zip(panel_files, pcbway_dir / f"{NAME}-panel-gerbers.zip")

    models_written = write_step(board_path, production_dir / f"{NAME}-pcb.step")
    print(f"fab: {facts['parts']} machine-placed parts in {facts['bom_lines']} BOM lines ({facts['bottom']} on the "
          f"bottom), {facts['vias']} vias of {facts['via_drill']} mm, panel {panel['pieces']} slot pieces and "
          f"{panel['bites']} mouse-bite holes, nearest tab {panel['tab_to_antenna']:.1f} mm from the antenna, "
          f"panel DRC 0 errors; STEP with {models_written} block model types")
    readme_facts = facts | {"frame": panel["frame"]}
    (jlc_dir / "README.md").write_text(jlc_readme(readme_facts))
    (pcbway_dir / "README.md").write_text(pcbway_readme(readme_facts))


def _size(frame: tuple[float, float, float, float]) -> str:
    return f"{frame[2] - frame[0]:.2f} x {frame[3] - frame[1]:.2f} mm"


def _board_size() -> str:
    pcb = BOARD_SPEC["pcb"]
    rear = min([pcb["y0"]] + [t["y0"] for t in pcb["tongues"]])
    return f"{pcb['x1'] - pcb['x0']:.2f} x {pcb['y1'] - rear:.2f} mm"


def _rotation_table() -> str:
    lines = ["| Footprint pattern | Correction | Source |", "|---|---|---|"]
    lines += [f"| `{pattern}` | {degrees:+d} | {reason} |" for pattern, degrees, reason in ROTATIONS]
    return "\n".join(lines)


def jlc_readme(facts: dict) -> str:
    return f"""# worxpad PCB: JLCPCB order

Generated by `pcb/gen/build.py fab` (`make pcb-fab`). Do not edit; change the generator. **Nothing has been
ordered.** These files have passed the checks named below and nothing else; no board has been made from them.

## Files

| Upload as | File | Contents |
|---|---|---|
| Gerber file | `{NAME}-panel-gerbers.zip` | the panel, {_size(facts['frame'])}: 4 copper layers, mask, silk, paste, outline, PTH and NPTH drills |
| BOM file | `bom.csv` | {facts['bom_lines']} lines, one JLCPCB part number on every line |
| CPL file | `cpl.csv` | {facts['parts']} placements, {facts['bottom']} on the bottom, rotation table applied |

`{NAME}-jlcpcb-order.zip` holds the same three files. The single board without the frame is in `pcb/fab/`.

## Order form (PCB)

| Field | Setting | Why |
|---|---|---|
| Base material | FR-4 | |
| Layers | 4 | board.toml pcb.layers |
| Dimensions | {_size(facts['frame'])} (panel) | board {_board_size()} in a frame (D23) |
| PCB qty | 5 | first batch |
| Product type | Industrial/Consumer electronics | |
| Different design | 1 | |
| Delivery format | Panel by Customer | one board in a frame of four {PANEL['rail_width']:.0f} mm rails, {PANEL['routed_gap']} mm routed gap, {len(PANEL['tabs'])} mouse-bite tabs |
| PCB thickness | 1.6 mm | board.toml pcb.thickness |
| Impedance control / layer stack-up | JLC04161H-7628 (default) | no impedance calculation was made (USB is full speed) |
| Via covering | Tented | |
| Min via hole size / diameter | {facts['via_drill']} mm / 0.6 mm | |
| Surface finish | ENIG | flat pads for the 0.5 mm LGA module and 0.5 mm FPC connector |
| Outer / inner copper weight | 1 oz / 0.5 oz | |
| Board outline tolerance | ask for +/-0.1 mm (see remark) | D24 |
| Mark on PCB | Remove mark | |
| Castellated holes, edge plating | No | |

## Order form (PCB assembly)

| Field | Setting |
|---|---|
| PCBA type | Standard |
| Assembly side | Both sides (D9) |
| PCBA qty | 5 |
| Edge rails / fiducials | Added by customer (frame rails; three fiducials per face are on the board) |
| Tooling holes | Added by JLCPCB, on the rails only |
| Confirm parts placement | Yes |

Remark text, paste as it is:

> Customer panel: one board in a frame of four 5 mm rails, 2.5 mm routed gap, eight mouse-bite tabs, no V-cut.
> Please keep tooling holes on the rails only. Please route the right board edge (X max of the board, next to
> the U1 radio module antenna) to +/-0.1 mm if possible and tell us if not: U1's antenna end is 0.2 mm inside
> that edge and must not overhang. J1 (USB-C) and SW18 (slide switch) overhang their board tongues into the
> routed gap; no tab or rail is in front of them. J1's signal pads and SW18's shield tabs end at the board
> edge on purpose. U1 is a u-blox BMD-340 LGA module: please confirm its pad 1 corner in the placement preview.

## Check before paying

- **Placement preview, every designator.** The rotation table below is partly reasoned, not checked against
  JLCPCB's part models. Look at U1 (pad 1 corner and the antenna end at the right edge), J1, J2 (contact 1
  toward the right), J3 (mouth toward the left), SW18 (actuator out of the rear edge), U2, U3, U4, U5, U6, Q1,
  Q2 and the diodes D1 to D20 (cathode bar toward the row net). Ask for a correction in the placement
  confirmation instead of editing the files.
- **Bottom parts.** The bottom rows use top-view X and Y and 180 degrees minus the KiCad angle plus the
  correction (the convention of KiKit and kicad-jlcpcb-tools). JLCPCB does not document its bottom side.
- **Not on the BOM:** the 16 Kailh hot-swap sockets (CPG135001S30, hand-soldered, keys 6.7), the four encoder
  filter capacitors C13 to C16 (footprints only, D36), test pads, holes and fiducials.
- **D12 gate:** VBUS on module pad 66 while 3V3 is off is not yet checked against the nRF52840 Product
  Specification. Do not order before it is.

## Rotation table

{_rotation_table()}

All other footprints: 0. Two-pin parts and the symmetric switches need none; the project footprints (U1, J1,
J2, ENC1, ENC2) have no JLCPCB reference to compare with.
"""


def pcbway_readme(facts: dict) -> str:
    return f"""# worxpad PCB: PCBWay order (fallback)

Generated by `pcb/gen/build.py fab`. Do not edit. **Nothing has been ordered.**

| File | Contents |
|---|---|
| `{NAME}-panel-gerbers.zip` | the same panel as the JLCPCB order, {_size(facts['frame'])} |
| `bom-mpn.csv` | {facts['bom_lines']} lines with manufacturer part numbers where the research records give one |
| `centroid.csv` | {facts['parts']} placements: KiCad footprint origin, top-view X and Y (Y up), KiCad's own angle |

The JLCPCB `cpl.csv` has JLCPCB's rotation table and body centres in it: do not send it to PCBWay.

Order form: 4 layers, FR-4, 1.6 mm, ENIG, 1 oz outer, panel by customer (frame and tabs drawn), quantity 5,
assembly on both sides, tented vias, minimum hole {facts['via_drill']} mm. Ask for the right board edge at
+/-0.1 mm (D24). Lines whose MPN column is empty name only the LCSC number in the research records: PCBWay
sources an equivalent part to that number's data sheet, or the line is consigned.
Not on the BOM: the 16 hot-swap sockets (hand-soldered) and the four encoder filter capacitors (not fitted).
"""


def fill(board_path: Path) -> None:
    board = pcbnew.LoadBoard(str(board_path))
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(str(board_path), board)


if __name__ == "__main__":
    if sys.argv[1:2] == ["panel"]:
        (BUILD_DIR / "panel-facts.json").write_text(json.dumps(build_panel(Path(sys.argv[2]), Path(sys.argv[3]))))
    elif sys.argv[1:2] == ["fill"]:
        fill(Path(sys.argv[2]))
    else:
        sys.exit("usage: fab.py panel <board> <panel> | fab.py fill <board>")
