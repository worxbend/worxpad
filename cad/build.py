"""Build the worxpad case: `python build.py check | export | render | draw | all` (run from cad/).

check   every check, written to exports/checks.json; exits 1 on any failure
export  STEP, STL and 3MF files to exports/
render  quick pictures to ../docs/images/cad/
draw    CNC drawings of shells, knob and RF insert (SVG, PDF, DXF), hole tables, lens and laser-mark DXF
        to exports/drawings/
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from worxpad_case import checks, drawings, export, render, small_drawings  # noqa: E402

EXPORTS = Path(__file__).resolve().parent / "exports"
IMAGES = Path(__file__).resolve().parents[1] / "docs" / "images" / "cad"


def check() -> int:
    report = checks.run_all()
    EXPORTS.mkdir(exist_ok=True)
    (EXPORTS / "checks.json").write_text(json.dumps(report, indent=2) + "\n")
    passed = sum(item["ok"] for item in report["self_test"])
    print(f"self-test: {passed} of {len(report['self_test'])} known faults and sound shapes judged right")
    print(f"validity: {sum(item['ok'] for item in report['validity'])} of {len(report['validity'])} parts sound")
    for result in report["interference"]:
        fits = ", ".join(f"{p['a']} {p['volume_mm3']} mm^3 (allowed {p['allowed_mm3']})" for p in result["press_fits"])
        print(f"interference {result['variant']}: {result['parts']} solids, {result['pairs']} pairs, "
              f"{len(result['clashes'])} clashes" + (f"; press fits: {fits}" if fits else ""))
    for group in ("clearances", "cnc", "fdm", "rf", "jig", "pcb_step"):
        for item in report[group]:
            if item["ok"] is None:
                print(f"  {group} {item['name']}: {item['value']} {item['unit']} (info)")
            else:
                print(f"  {group} {item['name']}: {item['value']} {item['unit']} ({item['kind']} {item['limit']})")
    problems = checks.failures(report)
    for problem in problems:
        print(f"FAIL {problem}")
    counted = sum(item["ok"] is not None for group in ("clearances", "cnc", "fdm", "rf", "jig", "pcb_step")
                  for item in report[group])
    print(f"{counted} limit checks, {len(problems)} failures")
    return 1 if problems else 0


COMMANDS = {
    "check": check,
    "export": lambda: export.export_all(EXPORTS),
    "render": lambda: render.render_all(IMAGES),
    "draw": lambda: max(drawings.write_drawings(EXPORTS / "drawings"),
                        small_drawings.write_small_drawings(EXPORTS / "drawings")),
}


def main(arguments: list[str]) -> int:
    command = arguments[0] if arguments else "all"
    if command == "all":
        return max(run() for run in COMMANDS.values())
    if command not in COMMANDS:
        print(f"usage: build.py [{' | '.join([*COMMANDS, 'all'])}]", file=sys.stderr)
        return 2
    return COMMANDS[command]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
