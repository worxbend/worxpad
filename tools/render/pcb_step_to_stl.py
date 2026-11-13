"""Convert the KiCad board STEP to meshes for the renders. FreeCAD script:

    flatpak run --command=freecadcmd org.freecad.FreeCAD tools/render/pcb_step_to_stl.py --pass STEP MANIFEST OUT_DIR

KiCad writes the board in board coordinates with Y flipped and the board bottom at Z 0, which is the assembly
frame of the case package apart from Z; the meshes are moved down to pcb_bottom_z from the manifest that
export_meshes.py wrote (board.toml pcb.bottom_z). The value is read from the file because freecadcmd takes any
negative number on its command line for an option.
Writes board.stl (the largest solid, the board itself) and, when the STEP holds part models, parts.stl.
"""

import json
import sys
from pathlib import Path

import Mesh
import MeshPart
import Part
from FreeCAD import Vector

LINEAR_DEFLECTION = 0.02  # mm


def write_mesh(shape, path: Path) -> None:
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=LINEAR_DEFLECTION, AngularDeflection=0.3)
    Mesh.Mesh(mesh).write(str(path))
    print(f"wrote {path} ({mesh.CountFacets} facets)")


def convert(step: Path, out: Path, bottom_z: float) -> None:
    shape = Part.read(str(step))
    if not shape.Solids:
        raise ValueError(f"{step} holds no solids")
    solids = sorted(shape.Solids, key=lambda solid: solid.Volume, reverse=True)
    lift = Vector(0, 0, bottom_z - solids[0].BoundBox.ZMin)  # parts hang below the board, so use the board
    for solid in solids:
        solid.translate(lift)
    out.mkdir(parents=True, exist_ok=True)
    write_mesh(solids[0], out / "board.stl")
    if len(solids) > 1:
        write_mesh(Part.makeCompound(solids[1:]), out / "parts.stl")
    else:
        print(f"{step} holds no part models; the renders keep the reference shapes")


# freecadcmd passes its own arguments first; ours are the last three
step_arg, manifest_arg, out_arg = sys.argv[-3:]
convert(Path(step_arg), Path(out_arg), json.loads(Path(manifest_arg).read_text())["pcb_bottom_z"])
