"""Mesh every case part and bought-part reference shape for the Blender renders.

Run with the case venv: `cad/.venv/bin/python tools/render/export_meshes.py OUT_DIR`. Writes one binary STL per
solid, in millimetres in the assembly frame of cad/exports/assembly.step (X right, Y = -board Y, Z up), for the
CNC and the FDM variant, and manifest.json with the standing pose and the display's active area.

The solids are the ones cad/worxpad_case/export.py puts into assembly.step. Meshing them here skips a STEP
round trip and keeps the part names.
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "cad"))

from build123d import export_stl  # noqa: E402
from worxpad_case.components import components  # noqa: E402
from worxpad_case.render import SLOPE, _standing  # noqa: E402
from worxpad_case.small_parts import case_parts  # noqa: E402
from worxpad_case.spec import BOARD, CNC, PRINT, lens_centre  # noqa: E402

# research/components/display.md 6.1: active area 23.40 x 23.40 mm, centred on the lens (display.md 6.5).
ACTIVE_AREA = 23.4
SCREEN_LIFT = 0.02  # the screen plane floats this far over the module top, so it never shares its face
LINEAR_TOLERANCE = 0.01
ANGULAR_TOLERANCE = 0.15


def export_variant(variant: str, folder: Path) -> dict:
    folder.mkdir(parents=True, exist_ok=True)
    parts = {}
    for name, solid in (case_parts(variant) | components(variant)).items():
        path = folder / f"{name}.stl"
        if not export_stl(solid, path, LINEAR_TOLERANCE, ANGULAR_TOLERANCE):
            raise RuntimeError(f"STL export failed for {variant}/{name}")
        box = solid.bounding_box()
        parts[name] = {"file": str(path.relative_to(folder.parent)),
                       "min": [box.min.X, box.min.Y, box.min.Z], "max": [box.max.X, box.max.Y, box.max.Z]}
        print(f"meshed {variant}/{name}")
    return {"parts": parts, "screen": screen_rect(parts["display_module"]["max"][2]), "lens_window": lens_window()}


def screen_rect(module_top: float) -> dict:
    x, y = lens_centre()
    half = ACTIVE_AREA / 2
    return {"x": [x - half, x + half], "y": [-y - half, -y + half], "z": module_top + SCREEN_LIFT}


def lens_window() -> dict:
    """The clear window in the painted lens underside (display 6.4), as centre and side length."""
    x, y = lens_centre()
    return {"centre": [x, -y], "size": BOARD.display.lens.window}


def standing_pose() -> dict:
    """Rotation about X and the lift that stand the unit on its feet, as the case package's own renders do."""
    _, offset = _standing()
    return {"rotation_x_rad": SLOPE, "offset_mm": [float(value) for value in offset]}


def main(arguments: list[str]) -> int:
    if len(arguments) != 1:
        print("usage: export_meshes.py OUT_DIR", file=sys.stderr)
        return 2
    out = Path(arguments[0]).resolve()
    manifest = {
        "units": "mm",
        "pose": standing_pose(),
        "body": {"width": BOARD.body.width, "depth": BOARD.body.depth},
        "pcb_bottom_z": BOARD.pcb.bottom_z,
        "variants": {variant: export_variant(variant, out / variant) for variant in (CNC, PRINT)},
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {out / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
