"""Block models of the parts, for the 3D renders. Needs pcbnew.

The plain KiCad container ships no 3D library, so every part is drawn here as a few boxes and cylinders and
written to pcb/lib/3d/ as VRML. The outline of a body comes from the footprint's own fabrication-layer
drawing; heights are the board.toml values where it has one and nominal datasheet values otherwise (named
below). These models are pictures. The case model in cad/ and tools/check_spec.py hold the real clearance
checks.

Adapted from macropad/pcb/gen/models.py.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import pcbnew

import circuit
from circuit import BOARD_SPEC

MODEL_DIR = circuit.REPO_ROOT / "pcb" / "lib" / "3d"
# As KiCad resolves it from pcb/kicad/, where the board file lives.
_MODEL_REFERENCE = "${KIPRJMOD}/../lib/3d"
_STOCK_FOOTPRINTS = Path("/usr/share/kicad/footprints")
_PROJECT_FOOTPRINTS = circuit.REPO_ROOT / "pcb" / "lib" / f"{circuit.LIBRARY}.pretty"
_VRML_UNIT = 2.54  # KiCad reads one VRML unit as a tenth of an inch
_ROUND_FACETS = 32
_THICKNESS = BOARD_SPEC["pcb"]["thickness"]
_PCB_TOP = BOARD_SPEC["pcb"]["top_z"]
_PARTS = BOARD_SPEC["power"]["parts"]

Colour = tuple[float, float, float]
BLACK: Colour = (0.08, 0.08, 0.09)
DARK_GREY: Colour = (0.25, 0.25, 0.27)
METAL: Colour = (0.55, 0.55, 0.54)
CERAMIC: Colour = (0.62, 0.52, 0.40)
GREEN: Colour = (0.15, 0.35, 0.22)
WHITE: Colour = (0.93, 0.93, 0.88)
CAP: Colour = (0.12, 0.12, 0.13)

Rect = tuple[float, float, float, float]  # left, top, right, bottom in footprint coordinates, Y down


@dataclass(frozen=True)
class Solid:
    """A box, or a cylinder standing on the board when `round` is set. Heights are above the
    footprint's own face; negative values reach through the board to the other face."""
    footprint_rect: Rect
    z_bottom: float
    z_top: float
    colour: Colour
    round: bool = False


def _centred(x: float, y: float, size_x: float, size_y: float) -> Rect:
    return x - size_x / 2, y - size_y / 2, x + size_x / 2, y + size_y / 2


def _fab_outline(footprint: pcbnew.FOOTPRINT) -> Rect:
    """The box around the footprint's fabrication-layer drawing, with the footprint at the origin."""
    shapes = [item for item in footprint.GraphicalItems()
              if item.GetLayer() == pcbnew.F_Fab and item.GetClass() == "PCB_SHAPE"]
    assert shapes, f"{footprint.GetFPIDAsString()}: no fabrication outline to build a model from"
    box = shapes[0].GetBoundingBox()
    for shape in shapes[1:]:
        box.Merge(shape.GetBoundingBox())
    return tuple(pcbnew.ToMM(edge) for edge in (box.GetLeft(), box.GetTop(), box.GetRight(), box.GetBottom()))


# Body height above the board and colour, for parts that are one block on their fabrication outline.
_ONE_BLOCK = {
    "C0402": (0.5, CERAMIC),                                   # nominal
    "C0603": (0.8, CERAMIC),                                   # nominal
    "R0402": (0.35, BLACK),                                    # nominal
    "R0805": (_PARTS["ntc"]["height"], BLACK),
    "SOT23": (1.2, BLACK),                                     # power 12: AO3401A about 1.2
    "SOT23-5": (_PARTS["ldo"]["height"], BLACK),
    "SOT23-6": (_PARTS["esd"]["height"], BLACK),
    "SOIC8W": (BOARD_SPEC["flash"]["height"], BLACK),
    "VQFN16": (_PARTS["charger"]["height"], BLACK),
    "DFN8": (_PARTS["gauge"]["height"], BLACK),
    "XTAL3215": (0.9, METAL),                                  # guess, nominal for 3215 crystals
    "F1206": (_PARTS["ptc"]["height"], GREEN),
    "SOD123": (BOARD_SPEC["keys"]["diode"]["height"], BLACK),
    "TACT": (BOARD_SPEC["reset"]["height"], METAL),
    "B3FS": (BOARD_SPEC["buttons"]["switch_top_z"] - _PCB_TOP, DARK_GREY),
    "SLIDE": (BOARD_SPEC["power_switch"]["height"], METAL),
    "JST_PH2": (BOARD_SPEC["battery"]["connector"]["height"], WHITE),
    "BMD340": (BOARD_SPEC["module"]["height"], METAL),
    "FH34SRJ24": (BOARD_SPEC["display"]["connector"]["top_z"] - _PCB_TOP, BLACK),
}


def _usb_receptacle(footprint: pcbnew.FOOTPRINT) -> list[Solid]:
    """Mid-mount shell: it sits in the board notch, from the far face out past the mounting face."""
    usb = BOARD_SPEC["usb"]
    outward = BOARD_SPEC["pcb"]["bottom_z"] - usb["bottom_z"]          # below the mounting (bottom) face
    return [Solid(_fab_outline(footprint), -_THICKNESS, outward, METAL)]


def _key_switch(footprint: pcbnew.FOOTPRINT) -> list[Solid]:
    """Socket on the footprint's face (the bottom); Choc V2 switch and keycap through the board on the key side."""
    keys, stack = BOARD_SPEC["keys"], BOARD_SPEC["stack"]
    socket = BOARD_SPEC["pcb"]["bottom_z"] - stack["socket_underside"]
    housing_top = keys["collar_z"] - _PCB_TOP
    cap_bottom, cap_top = stack["deck"] - _PCB_TOP, keys["cap_height"] - _PCB_TOP

    def key_side(low: float, high: float) -> tuple[float, float]:
        return -_THICKNESS - high, -_THICKNESS - low

    return [
        Solid(_fab_outline(footprint), 0.0, socket, DARK_GREY),
        Solid(_centred(0.0, 0.0, keys["housing"], keys["housing"]), *key_side(0.0, housing_top), DARK_GREY),
        Solid(_centred(0.0, 0.0, keys["cap_base"], keys["cap_base"]), *key_side(cap_bottom, cap_top), CAP),
    ]


def _encoder(footprint: pcbnew.FOOTPRINT) -> list[Solid]:
    knobs = BOARD_SPEC["knobs"]
    body_top = -0.10 - _PCB_TOP     # nominal body top (rotary-buttons 6.3); board.toml holds the 0.20 maximum
    shaft_top = 15.0                                        # rotary-buttons 6.1: L 15.0 above the PCB top
    knob_bottom, knob_top = knobs["rim_z"] - _PCB_TOP, knobs["top_z"] - _PCB_TOP
    return [
        Solid(_fab_outline(footprint), 0.0, body_top, METAL),
        Solid(_centred(0.0, 0.0, 6.0, 6.0), body_top, shaft_top, BLACK, round=True),
        Solid(_centred(0.0, 0.0, knobs["diameter"], knobs["diameter"]), knob_bottom, knob_top, DARK_GREY, round=True),
    ]


_SHAPED = {"USBC_M13C": _usb_receptacle, "CHOC_HOTSWAP": _key_switch, "PEC12R4": _encoder}
MODELLED = set(_ONE_BLOCK) | set(_SHAPED)


def solids(footprint_key: str, footprint: pcbnew.FOOTPRINT) -> list[Solid]:
    if footprint_key in _ONE_BLOCK:
        height, colour = _ONE_BLOCK[footprint_key]
        return [Solid(_fab_outline(footprint), 0.0, height, colour)]
    return _SHAPED[footprint_key](footprint)


def _footprint_polygon(solid: Solid) -> list[tuple[float, float]]:
    """The solid seen from above, counter-clockwise in model coordinates (footprint Y points down, model Y up)."""
    left, top, right, bottom = solid.footprint_rect
    assert right > left and bottom > top and solid.z_top > solid.z_bottom, f"empty solid {solid}"
    if not solid.round:
        return [(left, -bottom), (right, -bottom), (right, -top), (left, -top)]
    centre_x, centre_y, radius = (left + right) / 2, -(top + bottom) / 2, (right - left) / 2
    return [(centre_x + radius * math.cos(2 * math.pi * step / _ROUND_FACETS),
             centre_y + radius * math.sin(2 * math.pi * step / _ROUND_FACETS)) for step in range(_ROUND_FACETS)]


def _vrml_shape(solid: Solid) -> str:
    """A prism as a face set. KiCad's VRML reader draws boxes but skips cylinders, so both are written this way."""
    polygon = _footprint_polygon(solid)
    count = len(polygon)
    points = [(x, y, z) for z in (solid.z_bottom, solid.z_top) for x, y in polygon]
    faces = [list(range(count, 2 * count)), list(range(count - 1, -1, -1))]
    faces += [[i, (i + 1) % count, count + (i + 1) % count, count + i] for i in range(count)]
    coordinates = ", ".join(" ".join(f"{value / _VRML_UNIT:.5f}" for value in point) for point in points)
    indices = " ".join(" ".join(map(str, face)) + " -1" for face in faces)
    red, green, blue = solid.colour
    return ("Shape {\n"
            f"  appearance Appearance {{ material Material {{ diffuseColor {red} {green} {blue} "
            "specularColor 0.1 0.1 0.1 shininess 0.2 } }\n"
            f"  geometry IndexedFaceSet {{ solid FALSE coord Coordinate {{ point [ {coordinates} ] }} "
            f"coordIndex [ {indices} ] }}\n}}\n")


def vrml(parts: list[Solid]) -> str:
    return "#VRML V2.0 utf8\n" + "".join(_vrml_shape(part) for part in parts)


def load_footprint(footprint_key: str) -> pcbnew.FOOTPRINT:
    """A fresh copy from its library: KiCad's stock libraries or pcb/lib/worxpad.pretty."""
    library, name = circuit.FOOTPRINT[footprint_key].split(":")
    directory = _PROJECT_FOOTPRINTS if library == circuit.LIBRARY else _STOCK_FOOTPRINTS / f"{library}.pretty"
    footprint = pcbnew.FootprintLoad(str(directory), name)
    assert footprint is not None, f"{footprint_key}: {name} not found in {directory}"
    return footprint


def write_models(model_dir: Path = MODEL_DIR) -> list[str]:
    """One model file per footprint type in the circuit. Returns the keys written."""
    model_dir.mkdir(parents=True, exist_ok=True)
    keys = sorted({part.footprint_key for part in circuit.all_parts()} & MODELLED)
    for key in keys:
        (model_dir / f"{key}.wrl").write_text(vrml(solids(key, load_footprint(key))))
    stale = {path.stem for path in model_dir.glob("*.wrl")} - set(keys)
    assert not stale, f"model files no part uses: {sorted(stale)}"
    return keys


def attach(footprint_key: str, footprint: pcbnew.FOOTPRINT) -> None:
    """For layout.py: replaces the stock model references, which point into a library the container lacks."""
    footprint.Models().clear()
    if footprint_key not in MODELLED:
        return
    model = pcbnew.FP_3DMODEL()
    model.m_Filename = f"{_MODEL_REFERENCE}/{footprint_key}.wrl"
    footprint.Models().push_back(model)
