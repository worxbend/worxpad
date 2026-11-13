"""STEP, STL and 3MF files for every part, and one assembly STEP.

exports/cnc/    STEP of the parts milled or turned at JLCCNC, in the assembly frame
exports/print/  STEP in the assembly frame; STL and 3MF in the bed pose, print aids included
exports/resin/  keycap, stem coupon and button cap for JLC3DP resin: STEP and STL
exports/assembly.step   CNC variant with every bought part, one labelled solid per entry
"""

from pathlib import Path

from build123d import Compound, Mesher, Part, export_step, export_stl

from .components import components
from .coupons import as_printed, printed_parts, resin_parts
from .small_parts import case_parts, insertion_jig
from .spec import CNC, PRINT

CNC_PARTS = {"top_shell": "top_shell", "bottom_shell": "bottom_shell", "rf_insert": "rf_insert", "knob_left": "knob"}


def export_all(exports: Path) -> int:
    cnc, printed, resin = exports / CNC, exports / PRINT, exports / "resin"
    for folder in (cnc, printed, resin):
        folder.mkdir(parents=True, exist_ok=True)
    for name, file_name in CNC_PARTS.items():
        export_step(case_parts(CNC)[name], cnc / f"{file_name}.step")
    for name, part in printed_parts().items():
        export_step(part, printed / f"{name}.step")
        _mesh(as_printed(name), printed / name)
    jig = insertion_jig()
    export_step(jig, printed / "insertion_jig.step")
    _mesh(jig, printed / "insertion_jig")
    resin_set = resin_parts() | {"button_cap": case_parts(CNC)["button_cap_left"]}
    for name, part in resin_set.items():
        export_step(part, resin / f"{name}.step")
        export_stl(part, resin / f"{name}.stl")
    export_step(case_parts(CNC)["lens"], exports / "lens.step")
    export_step(_assembly(), exports / "assembly.step")
    print(f"exported to {exports}")
    return 0


def _mesh(part: Part, stem: Path) -> None:
    export_stl(part, stem.with_suffix(".stl"))
    mesher = Mesher()
    mesher.add_shape(part)
    mesher.write(str(stem.with_suffix(".3mf")))


def _assembly() -> Compound:
    labelled = []
    for name, solid in (case_parts(CNC) | components(CNC)).items():
        solid.label = name
        labelled.append(solid)
    return Compound(label="worxpad", children=labelled)
