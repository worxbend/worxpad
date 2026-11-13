"""Quick pictures of the case through the package's own software renderer (raster.py), into docs/images/cad/.

Views: hero, exploded, underside, side profile, a section through the display and the USB-C opening, and the
FDM print plates. The CNC variant is drawn standing on its feet (ramp plane level). Colours are proposals; the
lens is drawn as opaque black glass, so the display under it does not show. Bought parts are the reference
shapes of components.py, not vendor models.
"""

import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field, replace
from math import atan, cos, sin
from pathlib import Path

import numpy as np
from build123d import Box, Part, Pos
from PIL import Image

from .components import components
from .coupons import as_printed, print_pose, printed_parts
from .raster import Camera, Lighting, Material, Mesh, Scene, mesh_of, render
from .small_parts import case_parts
from .spec import BOARD, CNC, thickness_at

IMAGE_SIZE = (1400, 950)
WORKERS = int(os.environ.get("CAD_RENDER_WORKERS", "3"))  # each view holds about 1 GB while it renders
ANODISED = Material((0.11, 0.11, 0.12), gloss=0.5, metal=0.7, ceiling=0.6)  # bead-blasted black anodise
MATERIALS = {
    "top_shell": ANODISED, "bottom_shell": ANODISED, "knob": ANODISED,
    "button_cap": Material((0.07, 0.07, 0.08), gloss=0.2),
    "keycaps": Material((0.84, 0.83, 0.80), gloss=0.12, ceiling=0.83),  # a proposal; resin colour not chosen
    "lens": Material((0.02, 0.02, 0.03), gloss=0.0, sheen=0.12),
    "rf_insert": Material((0.05, 0.05, 0.05), gloss=0.15),  # black POM
    "g_spacers": Material((0.2, 0.2, 0.2)),
    "pcb": Material((0.05, 0.25, 0.12), gloss=0.3),  # JLCPCB green, the default
    "switch": Material((0.16, 0.16, 0.17), gloss=0.3),
    "socket": Material((0.30, 0.31, 0.33)),
    "encoder": Material((0.70, 0.71, 0.73), gloss=0.6),
    "display": Material((0.10, 0.16, 0.30)),
    "fpc_connector": Material((0.85, 0.85, 0.80)),
    "cell": Material((0.75, 0.76, 0.78), gloss=0.5),
    "feet": Material((0.05, 0.05, 0.05), gloss=0.05),
    "screws": Material((0.10, 0.10, 0.10), gloss=0.6),
    "printed": Material((0.30, 0.32, 0.36), gloss=0.15),  # PETG
    "aid": Material((0.85, 0.55, 0.20), gloss=0.1),  # break-away ribs and skins
    "bed": Material((0.22, 0.22, 0.24), gloss=0.2),
    "other": Material((0.40, 0.40, 0.42), gloss=0.2),
}
ALIASES = {"switch_": "switch", "sockets": "socket", "encoder": "encoder", "display_": "display", "_screws": "screws"}
CUT_TINT = 0.45
CENTRE = (BOARD.body.width / 2, -BOARD.body.depth / 2, -5.0)
SLOPE = atan((BOARD.wedge.apex_height - BOARD.wedge.front_height) / (BOARD.body.depth - BOARD.wedge.apex_y))
SECTION_X = BOARD.usb.x
BED = 180.0
EXPLODED = {"keycaps": 75.0, "knob": 85.0, "button_cap": 55.0, "lens": 45.0, "top_shell": 30.0, "switch": 55.0,
            "k_screws": 100.0, "bottom_shell": -40.0, "feet": -60.0, "c_screws": -75.0, "cell": -22.0,
            "cell_foam": -30.0, "insulation_sheet": -12.0, "rf_insert": -40.0}


@dataclass
class View:
    name: str
    camera: Camera
    scene: str = "standing"
    lighting: Lighting = field(default_factory=Lighting)
    ground: float | None = 0.0
    outlined: bool = False


def _camera(offset, target=CENTRE, **options) -> Camera:
    return Camera(tuple(np.add(target, offset)), tuple(target), **options)


FROM_BELOW = Lighting(key_direction=(-0.45, -0.35, -0.82), key=1.15, ambient=0.6, fill=0.35)
VIEWS = [
    View("hero", _camera((-110, -200, 170), target=(CENTRE[0], CENTRE[1], 6.0), field_of_view=27)),
    View("exploded", _camera((-230, -380, 230), target=(CENTRE[0], CENTRE[1], 15.0), field_of_view=24),
         scene="exploded", ground=None, outlined=True),
    View("underside", _camera((0, -180, -260), target=(CENTRE[0], CENTRE[1], 0.0), field_of_view=28, up=(0.0, 1.0, 0.0)),
         lighting=FROM_BELOW, ground=None),
    View("side_profile", _camera((-500, 0, 10), target=(0.0, CENTRE[1], 6.0), field_of_view=10.5)),
    View("section_display_usb", _camera((330, -70, 120), target=(SECTION_X, CENTRE[1], -2.0), field_of_view=15),
         scene="section", outlined=True),
    View("print_plate", _camera((150, -420, 330), target=(BED, -BED / 2, 5.0), field_of_view=32), scene="beds",
         outlined=True),
]


def render_all(images: Path) -> int:
    images.mkdir(parents=True, exist_ok=True)
    scenes = _scenes()
    with ProcessPoolExecutor(WORKERS) as pool:
        jobs = {view.name: pool.submit(_render, view, scenes[view.scene]) for view in VIEWS}
        for view in VIEWS:
            path = images / f"{view.name}.png"
            Image.fromarray(jobs[view.name].result()).save(path, optimize=True)
            print(f"rendered {path}")
    return 0


def _render(view: View, meshes: list[Mesh]) -> np.ndarray:
    scene = Scene(meshes=list(meshes), ground_z=view.ground)
    lighting = view.lighting if view.outlined else replace(view.lighting, edge_ink=0.0)
    return render(scene, view.camera, IMAGE_SIZE, lighting)


def material_of(name: str) -> Material:
    for key, alias in ALIASES.items():
        if key in name:
            return MATERIALS[alias]
    return MATERIALS[max((key for key in MATERIALS if name.startswith(key)), key=len, default="other")]


# ---------------------------------------------------------------------------------------------------------
# Scenes
# ---------------------------------------------------------------------------------------------------------
def _scenes() -> dict[str, list[Mesh]]:
    solids = case_parts(CNC) | components(CNC)
    standing = _standing()
    return {
        "standing": [_moved(mesh_of(solid, material_of(name)), standing) for name, solid in solids.items()],
        "exploded": [_shifted(mesh_of(solid, material_of(name)), name) for name, solid in solids.items()
                     if not name.startswith(("power_", "battery_plug"))],
        "section": _cut(solids, standing),
        "beds": _beds(),
    }


def _standing() -> tuple[np.ndarray, np.ndarray]:
    """Rotation and offset that stand the CNC unit on its feet: the ramp plane level, feet on Z = 0."""
    rotation = np.array(((1, 0, 0), (0, cos(SLOPE), -sin(SLOPE)), (0, sin(SLOPE), cos(SLOPE))))
    foot = BOARD.feet.positions[2]
    proud = BOARD.feet.height - BOARD.feet.pocket_depth
    point = np.array((foot[0], -foot[1], -thickness_at(foot[1])))
    lowest = (rotation @ point)[2] - proud
    return rotation, np.array((0.0, 0.0, -lowest))


def _moved(mesh: Mesh, pose: tuple[np.ndarray, np.ndarray]) -> Mesh:
    rotation, offset = pose
    return mesh.moved(rotation, offset)


def _shifted(mesh: Mesh, name: str) -> Mesh:
    lift = next((value for key, value in EXPLODED.items() if name.startswith(key)), 0.0)
    return mesh.moved(np.eye(3), np.array((0.0, 0.0, lift)))


def _cut(solids: dict[str, Part], pose) -> list[Mesh]:
    """Everything left of the cut plane at the USB-C centre, cut faces lighter."""
    keep = Pos(SECTION_X - 250, 0, 0) * Box(500, 500, 500)
    meshes = []
    for name, solid in solids.items():
        kept = solid & keep
        if kept is None or not kept.solids():
            continue
        mesh = mesh_of(kept, material_of(name))
        on_cut = (np.abs(mesh.triangles[..., 0] - SECTION_X) < 1e-3).all(axis=1)
        tint = tuple(c + (1 - c) * CUT_TINT for c in mesh.material.colour)
        meshes.append(_moved(mesh.only(~on_cut, mesh.material), pose))
        if on_cut.any():
            meshes.append(_moved(mesh.only(on_cut, Material(tint, gloss=0.0, hatch=1.1)), pose))
    return meshes


def _beds() -> list[Mesh]:
    """Two 180 mm beds of the Bambu A1 mini: the bottom shell on one; the top shell and the small parts and
    coupons on the other. Print aids in orange."""
    meshes = [mesh_of(Pos(x + BED / 2, -BED / 2, -0.5) * Box(BED, BED, 1.0), MATERIALS["bed"]) for x in (0.0, BED + 20)]
    layout = {"bottom_shell": (5.0, 5.0), "top_shell": (BED + 25.0, 5.0), "knob": (BED + 30.0, 100.0),
              "button_cap": (BED + 50.0, 100.0), "g_spacer": (BED + 72.0, 100.0),
              "coupon_plate_1_0": (BED + 30.0, 120.0), "coupon_plate_1_2": (BED + 30.0, 147.0),
              "coupon_knob_bore": (BED + 100.0, 100.0), "coupon_usb": (BED + 150.0, 100.0),
              "coupon_lens": (BED + 100.0, 120.0)}
    for name, (x, y) in layout.items():
        posed = as_printed(name)
        bounds = posed.bounding_box()
        placed = Pos(x - bounds.min.X, -y - bounds.max.Y, 0) * posed
        finished = Pos(x - bounds.min.X, -y - bounds.max.Y, 0) * (print_pose(name) * printed_parts()[name])
        meshes.append(mesh_of(finished, MATERIALS["printed"]))
        aids = placed - finished
        if aids is not None and aids.solids() and aids.volume > 0.01:
            meshes.append(mesh_of(aids, MATERIALS["aid"]))
    return meshes
