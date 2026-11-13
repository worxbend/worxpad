#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Builds the order index in production/ and the CNC order package in cad/production/. Standard library only.

It does not make any order file itself. The PCB generator (pcb/gen/fab.py) writes the board files, the case
builder (cad/build.py) writes the STEP files, drawings and hole tables. This script:

- copies each CNC part's STEP, PDF and DXF into cad/production/jlccnc/ under one shared name, as JLCCNC wants
  them, and merges the hole tables into cad/production/jlccnc/hole_table.csv;
- writes production/README.md (what to order where, every file with its state) and production/manifest.csv
  (size and SHA-256 of every file that exists);
- fails when a listed file is missing or empty, when the BOM and the placement list name different
  designators, when the JLCPCB and PCBWay files disagree, when the case checks have a failure, or when a
  hand-written list is malformed.

It writes the index even when it fails, so production/README.md always says what is missing.

    python3 tools/order_package.py           build, then check; exit 1 on any problem
    python3 tools/order_package.py --draft   check only, with the PCB files from pcb/.build/draft; writes nothing

A draft is never an order: pcb/gen/build.py fab-draft writes it from an unfinished board.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NAME = "worxpad"
INDEX_DIR = REPO_ROOT / "production"
CAD_EXPORTS = REPO_ROOT / "cad" / "exports"
CAD_PRODUCTION = REPO_ROOT / "cad" / "production"
JLCCNC_DIR = CAD_PRODUCTION / "jlccnc"
JLCCNC_HAND_WRITTEN = {"ORDER_NOTES.md"}
LCSC_NUMBER = re.compile(r"^C\d+$")


@dataclass(frozen=True)
class CncPart:
    stem: str          # file stem in cad/exports/cnc and cad/exports/drawings
    material: str
    per_unit: int
    has_holes: bool    # the drawing step writes <stem>_holes.csv
    extra_dxf: tuple[str, ...] = ()   # flat artwork for this part, in cad/exports/drawings

    @property
    def order_name(self) -> str:
        return f"{NAME}_{self.stem}"


CNC_PARTS = (
    CncPart("top_shell", "6061-T6, bead blast, black anodise", 1, True),
    CncPart("bottom_shell", "6061-T6, bead blast, black anodise", 1, True, ("engraving_underside",)),
    CncPart("rf_insert", "black POM, as machined", 1, False),
    CncPart("knob", "6061-T6 turned, bead blast, black anodise", 2, False),
)


@dataclass(frozen=True)
class Listed:
    path: Path
    role: str


@dataclass(frozen=True)
class Order:
    title: str
    vendor: str
    guide: str          # repository path of the guide, from the root
    files: tuple[Listed, ...]


# --------------------------------------------------------------------------------------------------------
# What is ordered, file by file
# --------------------------------------------------------------------------------------------------------
def pcb_orders(pcb_root: Path) -> list[Order]:
    jlc, pcbway = pcb_root / "production" / "jlcpcb", pcb_root / "production" / "pcbway"
    return [
        Order("Assembled PCB, 5 boards", "JLCPCB", "docs/ordering.md", (
            Listed(jlc / f"{NAME}-panel-gerbers.zip", "Gerber file: the D23 panel"),
            Listed(jlc / "bom.csv", "BOM file"),
            Listed(jlc / "cpl.csv", "CPL file, rotation table applied"),
            Listed(jlc / "README.md", "order form and remark text, generated"),
            Listed(jlc / f"{NAME}-jlcpcb-order.zip", "the three upload files in one zip"),
            Listed(pcb_root / "fab" / f"{NAME}-gerbers.zip", "single board without the frame, for questions"),
            Listed(pcb_root / "production" / f"{NAME}-pcb.step", "board with block models, for the case fit"),
        )),
        Order("Assembled PCB, fallback", "PCBWay", "docs/ordering-pcbway.md", (
            Listed(pcbway / f"{NAME}-panel-gerbers.zip", "Gerber file: the same panel"),
            Listed(pcbway / "bom-mpn.csv", "BOM with manufacturer part numbers"),
            Listed(pcbway / "centroid.csv", "centroid file, KiCad angles"),
            Listed(pcbway / "README.md", "order form, generated"),
        )),
    ]


def case_orders() -> list[Order]:
    cnc_files: list[Listed] = []
    for part in CNC_PARTS:
        cnc_files += [Listed(JLCCNC_DIR / f"{part.order_name}{suffix}", f"{part.stem}, {role}")
                      for suffix, role in ((".step", "geometry"), (".pdf", "drawing"), (".dxf", "2D plan"))]
        cnc_files += [Listed(JLCCNC_DIR / f"{part.order_name}_{extra}.dxf", f"{part.stem}, laser-mark artwork")
                      for extra in part.extra_dxf]
    cnc_files += [Listed(JLCCNC_DIR / "hole_table.csv", "every tapped and countersunk hole"),
                  Listed(JLCCNC_DIR / "ORDER_NOTES.md", "form settings, remarks, prepared answers")]
    resin, drawings = CAD_EXPORTS / "resin", CAD_EXPORTS / "drawings"
    return [
        Order("Case, CNC", "JLCCNC", "docs/ordering-case.md", tuple(cnc_files)),
        Order("Case, CNC, fallback", "PCBWay CNC", "docs/ordering-case.md", (
            Listed(CAD_PRODUCTION / "pcbway" / "ORDER_NOTES.md", "what differs at PCBWay; same files"),
        )),
        Order("Keycaps, button caps, stem coupon (resin)", "JLC3DP", "docs/ordering-case.md", (
            Listed(resin / "keycap.stl", "keycap, 16 per unit"),
            Listed(resin / "button_cap.stl", "button cap, 2 per unit"),
            Listed(resin / "coupon_stem.stl", "stem fit coupon, order first"),
        )),
        Order("Display lens (laser-cut PMMA)", "laser shop", "docs/ordering-case.md", (
            Listed(drawings / "lens.dxf", "cut outline"),
            Listed(drawings / "lens_mask.dxf", "painted mask and window"),
        )),
        Order("Hand-fitted parts and hardware", "several shops", "docs/parts.md", (
            Listed(REPO_ROOT / "docs" / "bom-hand.csv", "every part not machine-placed, 1 and 5 units"),
            Listed(CAD_PRODUCTION / "hardware.csv", "screws and feet per unit"),
        )),
    ]


# --------------------------------------------------------------------------------------------------------
# CSV checks
# --------------------------------------------------------------------------------------------------------
def read_rows(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(text)))


def designators(rows: list[dict[str, str]], label: str, problems: list[str]) -> set[str]:
    """Every designator in the rows, split at commas. A designator named twice is a problem."""
    seen: set[str] = set()
    for row in rows:
        for ref in (part.strip() for part in row.get("Designator", "").split(",")):
            if not ref:
                problems.append(f"{label}: a row has an empty designator")
            elif ref in seen:
                problems.append(f"{label}: {ref} is named twice")
            seen.add(ref)
    return seen


def compare_designators(first: set[str], second: set[str], labels: tuple[str, str]) -> list[str]:
    problems = []
    for only, label in ((first - second, labels[0]), (second - first, labels[1])):
        if only:
            problems.append(f"only in {label}: {', '.join(sorted(only))}")
    return problems


def check_bom_against_placements(bom_text: str, cpl_text: str, labels: tuple[str, str]) -> list[str]:
    problems: list[str] = []
    bom = designators(read_rows(bom_text), labels[0], problems)
    cpl = designators(read_rows(cpl_text), labels[1], problems)
    return problems + compare_designators(bom, cpl, labels)


def check_lcsc_numbers(bom_text: str, label: str) -> list[str]:
    return [f"{label}: line {row.get('Designator')} has no JLCPCB number"
            for row in read_rows(bom_text) if not LCSC_NUMBER.match(row.get("LCSC Part #", "").strip())]


def self_check() -> None:
    """The designator check must fail on each broken case, or the gate is not live."""
    bom = "Comment,Designator,Footprint,LCSC Part #\n10k,\"R1,R2\",R_0402,C25744\n"
    good = "Designator,Mid X,Mid Y,Layer,Rotation\nR1,1,1,Bottom,0\nR2,2,2,Bottom,0\n"
    extra = good + "R3,3,3,Bottom,0\n"
    twice = good + "R2,2,2,Bottom,0\n"
    assert not check_bom_against_placements(bom, good, ("bom", "cpl")), "a matching pair must pass"
    assert check_bom_against_placements(bom, extra, ("bom", "cpl")), "an extra placement must fail"
    assert check_bom_against_placements(bom, twice, ("bom", "cpl")), "a repeated placement must fail"
    missing = "Designator,Mid X,Mid Y,Layer,Rotation\nR1,1,1,Bottom,0\n"
    assert check_bom_against_placements(bom, missing, ("bom", "cpl")), "a missing placement must fail"
    assert check_lcsc_numbers(bom.replace("C25744", ""), "bom"), "a line without a number must fail"


# --------------------------------------------------------------------------------------------------------
# PCB checks
# --------------------------------------------------------------------------------------------------------
def check_pcb(pcb_root: Path) -> tuple[list[str], dict[str, int]]:
    jlc, pcbway = pcb_root / "production" / "jlcpcb", pcb_root / "production" / "pcbway"
    needed = [jlc / "bom.csv", jlc / "cpl.csv", pcbway / "bom-mpn.csv", pcbway / "centroid.csv"]
    if not all(path.is_file() for path in needed):
        return ["PCB: BOM and placement files missing; designators not compared"], {}
    text = {path.name: path.read_text(encoding="utf-8") for path in needed}
    problems = check_bom_against_placements(text["bom.csv"], text["cpl.csv"], ("JLCPCB bom.csv", "cpl.csv"))
    problems += check_bom_against_placements(text["bom-mpn.csv"], text["centroid.csv"],
                                             ("PCBWay bom-mpn.csv", "centroid.csv"))
    ignored: list[str] = []
    problems += compare_designators(designators(read_rows(text["bom.csv"]), "", ignored),
                                    designators(read_rows(text["bom-mpn.csv"]), "", ignored),
                                    ("the JLCPCB BOM", "the PCBWay BOM"))
    problems += check_lcsc_numbers(text["bom.csv"], "JLCPCB bom.csv")
    problems += check_order_zip(jlc)
    problems += same_bytes(jlc / f"{NAME}-panel-gerbers.zip", pcbway / f"{NAME}-panel-gerbers.zip")
    counts = {"bom_lines": len(read_rows(text["bom.csv"])), "placements": len(read_rows(text["cpl.csv"]))}
    return problems, counts


def check_order_zip(jlc: Path) -> list[str]:
    order_zip = jlc / f"{NAME}-jlcpcb-order.zip"
    if not order_zip.is_file():
        return []
    problems = []
    with zipfile.ZipFile(order_zip) as archive:
        for member in ("bom.csv", "cpl.csv", f"{NAME}-panel-gerbers.zip"):
            if member not in archive.namelist():
                problems.append(f"{order_zip.name} lacks {member}")
            elif (jlc / member).is_file() and archive.read(member) != (jlc / member).read_bytes():
                problems.append(f"{order_zip.name}: {member} differs from the loose file")
    return problems


def same_bytes(first: Path, second: Path) -> list[str]:
    if first.is_file() and second.is_file() and first.read_bytes() != second.read_bytes():
        names = (f"{path.parent.name}/{path.name}" for path in (first, second))
        return [f"{' and '.join(names)} differ; both must be the same panel"]
    return []


# --------------------------------------------------------------------------------------------------------
# Case checks and the CNC package
# --------------------------------------------------------------------------------------------------------
def failed_case_checks() -> list[str]:
    checks_file = CAD_EXPORTS / "checks.json"
    if not checks_file.is_file():
        return [f"{rel(checks_file)} missing: run make cad"]
    results = json.loads(checks_file.read_text(encoding="utf-8"))
    return [f"case check {entry['name']} fails: {entry['value']} {entry.get('unit', '')} against "
            f"{entry['limit']} ({entry.get('note', '')})"
            for group in results.values() if isinstance(group, list)
            for entry in group if isinstance(entry, dict) and entry.get("ok") is False]


def cnc_package() -> dict[Path, bytes]:
    """The generated files of cad/production/jlccnc/, from the case exports that exist."""
    drawings = CAD_EXPORTS / "drawings"
    files: dict[Path, bytes] = {}
    for part in CNC_PARTS:
        sources = {f"{part.order_name}.step": CAD_EXPORTS / "cnc" / f"{part.stem}.step",
                   f"{part.order_name}.pdf": drawings / f"{part.stem}.pdf",
                   f"{part.order_name}.dxf": drawings / f"{part.stem}.dxf"}
        sources.update({f"{part.order_name}_{extra}.dxf": drawings / f"{extra}.dxf" for extra in part.extra_dxf})
        files.update({JLCCNC_DIR / name: source.read_bytes() for name, source in sources.items()
                      if source.is_file()})
    files[JLCCNC_DIR / "hole_table.csv"] = hole_table()
    return files


def hole_table() -> bytes:
    """The drawings' hole tables in one file, with the order file name in front of each row."""
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["part", "hole", "x", "y", "callout", "face", "screw"])
    for part in CNC_PARTS:
        source = CAD_EXPORTS / "drawings" / f"{part.stem}_holes.csv"
        if part.has_holes and source.is_file():
            for row in read_rows(source.read_text(encoding="utf-8")):
                writer.writerow([part.order_name, row["hole"], row["x"], row["y"], row["callout"], row["face"],
                                 row["screw"]])
    return out.getvalue().encode()


def check_hole_sources() -> list[str]:
    return [f"{rel(CAD_EXPORTS / 'drawings' / f'{part.stem}_holes.csv')} missing" for part in CNC_PARTS
            if part.has_holes and not (CAD_EXPORTS / "drawings" / f"{part.stem}_holes.csv").is_file()]


def check_order_notes_name_holes() -> list[str]:
    """Every hole of the hole table must be named in the JLCCNC remarks, so the notes cannot drift silently."""
    notes = JLCCNC_DIR / "ORDER_NOTES.md"
    if not notes.is_file():
        return []
    text = notes.read_text(encoding="utf-8")
    holes = {row["hole"] for row in read_rows(hole_table().decode())}
    return [f"{rel(notes)} does not name hole {hole}" for hole in sorted(holes)
            if not re.search(rf"\b{re.escape(hole)}\b", text)]


# --------------------------------------------------------------------------------------------------------
# Hand-written lists
# --------------------------------------------------------------------------------------------------------
HAND_BOM_COLUMNS = ("item", "part", "qty_per_unit", "qty_1_unit", "qty_5_units", "seller", "link", "note")
HARDWARE_COLUMNS = ("item", "qty_per_unit", "spec", "where", "note")


def check_columns(path: Path, columns: tuple[str, ...], counts: tuple[str, ...]) -> tuple[list[str], list[dict]]:
    if not path.is_file():
        return [], []
    rows = read_rows(path.read_text(encoding="utf-8"))
    header = tuple(rows[0].keys()) if rows else ()
    if header != columns:
        return [f"{rel(path)}: columns {header} instead of {columns}"], []
    problems = [f"{rel(path)}: {row['item']}: {column} is not a whole number"
                for row in rows for column in counts if not row[column].strip().isdigit()]
    return problems, rows


def check_hand_lists(machine_placed_numbers: set[str]) -> list[str]:
    hand_path = REPO_ROOT / "docs" / "bom-hand.csv"
    problems, rows = check_columns(hand_path, HAND_BOM_COLUMNS, ("qty_per_unit", "qty_1_unit", "qty_5_units"))
    for row in rows:
        if not (row["link"].startswith("https://") or row["link"] == "-"):
            problems.append(f"{rel(hand_path)}: {row['item']}: link must be https:// or '-'")
        if any(number in row["part"].split() for number in machine_placed_numbers):
            problems.append(f"{rel(hand_path)}: {row['item']} is also on the JLCPCB BOM")
    hardware_problems, _ = check_columns(CAD_PRODUCTION / "hardware.csv", HARDWARE_COLUMNS, ("qty_per_unit",))
    return problems + hardware_problems


def jlc_bom_numbers(pcb_root: Path) -> set[str]:
    bom = pcb_root / "production" / "jlcpcb" / "bom.csv"
    if not bom.is_file():
        return set()
    return {row["LCSC Part #"].strip() for row in read_rows(bom.read_text(encoding="utf-8"))}


# --------------------------------------------------------------------------------------------------------
# The index
# --------------------------------------------------------------------------------------------------------
def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def file_state(path: Path) -> str:
    if not path.is_file():
        return "missing"
    return "empty" if path.stat().st_size == 0 else "present"


def missing_files(orders: list[Order]) -> list[str]:
    return [f"{rel(listed.path)} {file_state(listed.path)}" for order in orders for listed in order.files
            if file_state(listed.path) != "present"]


def index_markdown(orders: list[Order], problems: list[str], counts: dict[str, int]) -> str:
    """production/README.md. Only files that exist are linked, so docs-check stays meaningful."""
    verdict = ("**Not ready to order.** The problems below must be cleared first." if problems else
               "All listed files exist and agree. The gates a person must clear are listed below.")
    lines = [
        "# Order index",
        "",
        "Generated by `tools/order_package.py` (`make order`). Do not edit; change the script or the builders.",
        "**Nothing has been ordered, fabricated, printed or fitted.**",
        "",
        verdict,
        "",
    ]
    for order in orders:
        lines += [f"## {order.title}: {order.vendor}", "", f"Guide: [{order.guide}](../{order.guide}).", "",
                  "| File | Role | State |", "|---|---|---|"]
        for listed in order.files:
            state = file_state(listed.path)
            name = f"[{rel(listed.path)}](../{rel(listed.path)})" if state == "present" else rel(listed.path)
            lines.append(f"| {name} | {listed.role} | {state} |")
        lines.append("")
    if counts:
        lines += [f"JLCPCB BOM: {counts['bom_lines']} lines; placement list: {counts['placements']} placements.",
                  ""]
    lines += ["## Problems found by the script", ""]
    lines += [f"- {problem}" for problem in problems] or ["- none"]
    lines += [
        "",
        "## Gates the script cannot check",
        "",
        "- D12: VBUS on module pad 66 while 3V3 is off, read in the nRF52840 Product Specification.",
        "- D37: USB-C plug test with large-overmould cables before the case order.",
        "- JLCPCB placement preview of every designator; the rotation table is partly reasoned.",
        "- Stock of every BOM line on the order day.",
        "",
    ]
    return "\n".join(lines)


def manifest_csv(orders: list[Order]) -> str:
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["path", "bytes", "sha256"])
    for listed in (listed for order in orders for listed in order.files):
        if listed.path.is_file():
            writer.writerow([rel(listed.path), listed.path.stat().st_size,
                             hashlib.sha256(listed.path.read_bytes()).hexdigest()])
    return out.getvalue()


# --------------------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------------------
def write_cnc_package(files: dict[Path, bytes]) -> None:
    """Writes the generated files and removes generated files that the exports no longer back."""
    JLCCNC_DIR.mkdir(parents=True, exist_ok=True)
    for stale in JLCCNC_DIR.iterdir():
        if stale.is_file() and stale.name not in JLCCNC_HAND_WRITTEN and stale not in files:
            stale.unlink()
    for path, content in files.items():
        if not path.is_file() or path.read_bytes() != content:
            path.write_bytes(content)


def collect_problems(pcb_root: Path, orders: list[Order]) -> tuple[list[str], dict[str, int]]:
    pcb_problems, counts = check_pcb(pcb_root)
    problems = missing_files(orders)
    problems += pcb_problems + failed_case_checks() + check_hole_sources() + check_order_notes_name_holes()
    problems += check_hand_lists(jlc_bom_numbers(pcb_root))
    return problems, counts


def main(argv: list[str]) -> int:
    self_check()
    draft = argv == ["--draft"]
    if argv and not draft:
        print(__doc__)
        return 2
    pcb_root = REPO_ROOT / "pcb" / ".build" / "draft" if draft else REPO_ROOT / "pcb"
    if not draft:
        write_cnc_package(cnc_package())
    orders = pcb_orders(pcb_root) + case_orders()
    problems, counts = collect_problems(pcb_root, orders)
    if not draft:
        INDEX_DIR.mkdir(exist_ok=True)
        (INDEX_DIR / "README.md").write_text(index_markdown(orders, problems, counts), encoding="utf-8")
        (INDEX_DIR / "manifest.csv").write_text(manifest_csv(orders), encoding="utf-8")
    for problem in problems:
        print(f"order_package: {problem}")
    listed = sum(len(order.files) for order in orders)
    state = "draft checked, nothing written" if draft else "production/ and cad/production/jlccnc/ written"
    print(f"order_package: {listed} files listed, {len(problems)} problems; {state}"
          + (f"; {counts['bom_lines']} BOM lines, {counts['placements']} placements" if counts else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
