# Conventions brief for worxpad: what the sibling hardware repositories do

Date: 2026-11-13. Key: `conventions`. Scope: local files only, no web sources.

This brief records how the owner's existing hardware repositories are laid out, built and documented,
so that worxpad looks and builds like its family. Every finding names its source file and a confidence:
**confirmed** (read in the file, or measured by running a command), **likely** (consistent indirect
evidence), **guess**. Recommendations are marked as recommendations; they are not facts.

Repositories read:

| Short name | Path | Remote | What it is |
|---|---|---|---|
| macropad | `/home/worxbend/Projects/macropad` | `worxbend/macropad` | 12-key macropad, RP2354A, generated 4-layer PCB, build123d case (print and CNC), Rust embassy firmware. Closest sibling. |
| worxboard | `/home/worxbend/Projects/worxboard` | `w0rxbend/worxboard` | Split ErgoDox-style keyboard, RP2040, KiCad 10 in Docker, ZMK, CNC case, order packages for JLCPCB, PCBWay, JLCCNC, JLC3DP. |
| worxboard-ergo | `/home/worxbend/Projects/worxboard-ergo` | `w0rxbend/worxboard-ergo` | One-piece split Planck, revision A0. Case printable, PCB placed but not routed. |
| macropad-nyxilab | `/home/worxbend/Projects/macropad-nyxilab` | `worxbend/macropad-nyxilab` | Hand-wired printed macropad, two editions, PlatformIO firmware, 3D viewer, website. |
| plastic-lighthouse | `/home/worxbend/Projects/plastic-lighthouse` | not read | Printed softbox. Source of the printer facts. |
| camx | `/home/worxbend/Projects/camx` | not read | Printed pan/tilt camera. Print settings, fit coupon. |

Two GitHub owners are in use: `worxbend` for the two macropads and `w0rxbend` for the two worxboards
(confirmed, `git remote -v` in each repository). The request says "worxbend org", and the macropad
silkscreen prints `github.com/worxbend/macropad` (`macropad/pcb/gen/silk.py:100`), so `worxbend` is the
likely owner for worxpad (likely).

---

## 1. Repository layout, naming, licences, documentation tone

### 1.1 Top-level layout of the closest sibling

Source: `macropad/` tree, `macropad/README.md` section "Where things are", `macropad/CLAUDE.md`. Confirmed.

```
board.toml            single source of truth: positions (mm) and GPIO numbers
Makefile              top-level tasks; `make help` greps the `##` comments
CLAUDE.md             agent guidance: commands, rules, generated-file list
README.md             status table, what it is, gallery, build one, what is checked, before you order
pcb/
  kicad.sh            runs a command in the pinned KiCad container
  gen/                the generator (circuit, layout, router, routing plan, schematic, fab, tests)
  kicad/              GENERATED KiCad project (pcb, sch, sym lib, lib tables)
  fab/                GENERATED order files (gerbers/, <name>-gerbers.zip, bom-jlcpcb.csv, cpl-jlcpcb.csv)
  lib/                project footprints (<name>.pretty), SOURCES.txt, 3d/ GENERATED block models
  netlist.txt         GENERATED netlist dump
  routing.txt         GENERATED per-net length and via report
  README.md
cad/
  build.py            `check | export | render | draw | all`
  pyproject.toml      package metadata and dependencies
  macropad_case/      the build123d package
  exports/            GENERATED STEP, STL, drawings, checks.json (committed)
  README.md
firmware/             Rust workspace: core, fw, sim, uf2; Makefile; dist/<name>.uf2 (committed)
tools/                check_pins.py, check_hid.py
docs/                 ordering.md, parts.md, assembly.md, flashing.md, keymap.md, hardware.md, images/{cad,pcb,ui}/
.github/workflows/ci.yml, .github/scripts/check_docs.py
```

The worxboard layout is wider (`layout/`, `pcb/`, `case/`, `plates/`, `firmware/`, `zephyr/`, `site/`,
`tests/`, `tools/`, `docs/`, `build.yaml`, `justfile`, `pyproject.toml`, `uv.lock`, `CHANGELOG.md`,
`LICENSE`, `LICENSE-HARDWARE`, `THIRD_PARTY.md`). Source: `worxboard/` tree. Confirmed.

### 1.2 Naming

- Lower-case, hyphenated repository names; the product name is used as the file stem everywhere:
  `macropad.kicad_pcb`, `macropad-gerbers.zip`, `macropad.uf2`, Python package `macropad_case`,
  KiCad library `macropad`. Source: `macropad/pcb/gen/build.py:25-29`, `macropad/pcb/gen/fab.py:86`. Confirmed.
- JLCPCB files are named `bom-jlcpcb.csv` and `cpl-jlcpcb.csv` (macropad) or `bom.csv`, `cpl.csv`,
  `gerbers.zip` inside `pcb/production/<side>/` (worxboard). Confirmed.
- British spelling in macropad prose and identifiers: "colour", "centre", "millimetres". Source:
  `macropad/README.md`, `macropad/cad/macropad_case/spec.py`. Confirmed.
- Board coordinates: millimetres, origin at the top-left corner of the PCB seen from the key side, X to the
  right, Y toward the front. Source: `macropad/board.toml:4-6`. Confirmed.
- PCB silkscreen carries `<name> rev <letter>` and the repository URL. Source: `macropad/pcb/gen/silk.py:99-108`. Confirmed.

### 1.3 Licences

| Repository | State | Source | Confidence |
|---|---|---|---|
| macropad | No licence file. The README says so and says nobody may reuse it until one is added. | `macropad/README.md` section "License" | confirmed |
| worxboard | Code GPL-3.0 (`LICENSE`), hardware CERN-OHL-S-2.0 (`LICENSE-HARDWARE`), `THIRD_PARTY.md` table, SPDX headers `GPL-3.0-or-later` on scripts. | `worxboard/LICENSE`, `LICENSE-HARDWARE`, `THIRD_PARTY.md`, `tools/kicad_env.sh:2` | confirmed |
| worxboard-ergo | GPL-3.0-or-later only, `THIRD_PARTY.md` with pinned upstream commits. | `worxboard-ergo/pyproject.toml`, `THIRD_PARTY.md` | confirmed |

Consequence: any file copied from worxboard or worxboard-ergo brings GPL-3.0-or-later with it. Files
copied from macropad have no licence, but the same owner holds the rights. Recommendation: worxpad takes
the worxboard pair (GPL-3.0-or-later for code, CERN-OHL-S-2.0 for hardware) plus a `THIRD_PARTY.md`; the
owner must confirm this. Every third-party footprint gets a line in `pcb/lib/SOURCES.txt`, as in
`macropad/pcb/lib/SOURCES.txt`.

### 1.4 README and documentation structure

macropad README order (`macropad/README.md`, confirmed): one-paragraph description, hero render and
simulator GIF with a caption that says they are not photos, a quoted **Status** block, Contents, Status
table (part, state, how it was checked, with the date), What it is (spec table and a mermaid block
diagram), Gallery, Build one (5 numbered steps linking to the guides), Stock keymap, Work on the design
(tools table, commands table with needs and time), What is checked (area, check, result, dated), Where
things are (path table), Before you order (open points grouped Electrical, Mechanical, Firmware, Review),
License.

Each sub-tree has its own README (`pcb/README.md`, `cad/README.md`, `firmware/README.md`) that opens with
a bold "not built" sentence, then commands, a file table, the design, the checks, and "What a person
still has to look at". Confirmed.

Builder guides in `macropad/docs/`: `ordering.md` (numbered JLCPCB steps, option table with a "Why"
column, placement-preview checklist per part, "Before you pay", "Other board houses"), `parts.md`
(machine-placed, hand-soldered, plugged-in, case hardware, substitutions, with JLCPCB number, basic or
extended type and stock on a dated lookup), `assembly.md` (numbered, bare-board test before the case),
`flashing.md` (first flash, updates, troubleshooting by symptom), `keymap.md`, `hardware.md` (circuit in
words, pin map, test pads, layer stack, mechanical stack). Confirmed.

worxboard adds: `docs/design.md` (frozen specification), `docs/deviations.md` (every departure from the
spec under an identifier such as `WS0-1`, `REVB-8`, `CASE-10`, `ORDER-9`, each with Spec, Problem, Change,
Consumers), `docs/verification.md` (dated gate results, open items, "Not verified until a board is
built"), `docs/ordering-jlcpcb.md`, `docs/ordering-pcbway.md`, `docs/shopping-list.md`, `docs/bom.md`,
`CHANGELOG.md`. Source: `worxboard/docs/`. Confirmed.

### 1.5 Tone and status honesty

- macropad: plain technical English, short sentences, no emoji, no badges. Every page states what has
  not been built. Typical lines: "Status: design files only. Nothing has been built.", "No check here
  replaces a prototype.", "A clean DRC does not make a working board.", "These are open. None is hidden
  by a green check." Source: `macropad/README.md`. Confirmed.
- worxboard: the same honesty, but with emoji headings, badges and a centred hero block
  (`worxboard/README.md:1-45`). worxboard-ergo: plain, with a `[!WARNING]` block and a "What you can do
  today" table. macropad-nyxilab: deliberately playful slang. Confirmed.
- Recommendation: follow macropad's tone; it is the closest sibling and the newest.

Rules written in `macropad/CLAUDE.md` (confirmed) that worxpad should carry over word for word:

1. "Nothing has been fabricated, printed or run on hardware. Every document must say so where it matters."
2. "Keep `MEASURE` tags until someone measures. Label every guess as a guess."
3. "Never remove or weaken a check or a test to get green. Add a check for what you add."
4. Generated trees are listed by name; "Hand edits are lost on the next build. Change the generator."
5. Status numbers in the README (tracks, vias, test counts, pairs checked) are copied from check output
   and updated in the same change. `make docs-check` runs after moving or renaming a file.
6. "Do not add Claude or AI attribution to commits or PRs." The same rule is in
   `macropad-nyxilab/CLAUDE.md`. worxboard-ergo uses `AGENTS.md` for the same purpose.

`MEASURE` tag: a comment on any dimension that comes from a datasheet, a community footprint or a photo
and not from a caliper. It appears in `board.toml`, in `cad/macropad_case/spec.py` and in the README
table "Assumptions to measure" (`macropad/cad/README.md`). "guess" marks a value chosen with no part or
print to check it against. Confirmed. For worxpad this matters at once: every dimension taken from GLYF
renders is a `MEASURE` or a guess.

Pictures: every image is generated by code in the repository and captioned as a render, not a photo
(`macropad/README.md` Gallery). Part models in renders are "reference shapes drawn from datasheets, not
vendor models" (`macropad/cad/README.md`). This matches the project rule against copying vendor models.

### 1.6 Generated-file rules

- Generated outputs are committed: `pcb/kicad/`, `pcb/fab/`, `pcb/lib/3d/`, `cad/exports/`,
  `docs/images/`, `firmware/dist/*.uf2` (macropad, confirmed by `git ls-files` layout and CLAUDE.md).
- Scratch is ignored: `.build/`, `.venv/`, `target/`, `*.kicad_prl`, `*-backups/`, `fp-info-cache`,
  `*.lck`, `_autosave-*` (`macropad/.gitignore`). Confirmed.
- worxboard marks generated files in `.gitattributes` (`linguist-generated=true`, `-diff` on KiCad and
  STEP, `binary` on STL, zip, uf2, png, pdf) and CI rebuilds them and requires a byte-identical result
  (`just pcb-production-check`, `just production-check`, `pcb-sch-all` with `git diff --exit-code`).
  Source: `worxboard/.gitattributes`, `worxboard/pcb/pcb.just`. Confirmed.
- `macropad/.github/scripts/check_docs.py` fails when a Markdown link, image, `#anchor` or a code span
  naming a repository path does not exist. It has its own self-check. `TOP_LEVEL` in that file lists the
  directories whose paths are checked. Confirmed.

---

## 2. PCB toolchain

### 2.1 macropad `pcb/gen`: module by module

Total 3 769 lines of Python (`wc -l`, confirmed). Inputs: `board.toml` and `circuit.py`. Entry point:
`pcb/gen/build.py place | order | fab`, run inside the container through `pcb/kicad.sh`.

| Module | Lines | What it does | Needs KiCad | Reuse for another circuit and MCU |
|---|---|---|---|---|
| `circuit.py` | 417 | The circuit as data: `Part(ref, value, footprint_key, x, y, rotation, side, nets)`, tables `LCSC` (value to JLCPCB number), `FOOTPRINT` (key to KiCad footprint), `HAND_SOLDERED`, `NOT_A_PART`. Reads `board.toml`. `check_netlist` fails on a net with one pad. `python3 circuit.py` prints the netlist. | No | The `Part` class, the tables' shape, `all_parts`, `nets_to_pads`, `check_netlist`, `key_centre`, mounting holes and fiducials are generic. Everything from "MCU geometry" to `_core_regulator` and `_clock_and_reset` is RP2354A QFN-60 only: `mcu_pin_xy`, `gpio_pin`, `MCU_POWER_PINS`, `DECOUPLING_CAPS`, `DECOUPLING_SHIFT`, the 1.1 V regulator, the 12 MHz crystal. Rewrite those for a module. |
| `layout.py` | 319 | Builds the unrouted board with `pcbnew`: loads footprints from `/usr/share/kicad/footprints` or `pcb/lib`, places and flips, sets nets, LCSC field, outline (rounded rectangle from `board.toml`), four copper layers, inner planes, fiducial keep-outs, design rules, `check_placement`. | Yes | Mostly generic. Hard-wired: library name `"macropad"` (line 61), a plain rounded-rectangle outline only, `V3_ISLAND` and `V1_ISLAND` rectangles, the plane assignment In1 = GND and In2 = +5V with 3.3 V and 1.1 V islands, `SILK_LABELLED` keys, and every assert in `check_placement` (MCU pins, hot-swap mirror, USB mouth, side LEDs, crystal). |
| `router.py` | 559 | Grid router. Pure Python, standard library only. | No | Fully generic; see 2.2. |
| `route.py` | 344 | The routing plan: stage order, hand-placed vias, sensitive nets, length limits, writing tracks and vias to the board. | Yes | `_load_obstacles`, `fan_out`, `net`, `plane_fan_out`, `signals`, `write_copper`, `RoutingResult` are generic. `mcu_supply`, `_decouple`, `regulator_output`, `crystal_ground`, `mcu_escapes`, `EARLY_ESCAPES`, `SENSITIVE_NETS`, `LENGTH_LIMIT`, `NO_VIA_NETS`, `usb_path_length` name RP2354A pins and references (`U1.44`, `C33.1`, `L1.2`, `Y1.2`). Rewrite the plan. |
| `route_order.txt` | 16 | Nets routed first, written by `build.py order`. | - | Regenerated per board. |
| `schematic.py` | 445 | Writes a real `.kicad_sch` from `circuit.py` using KiCad's own library symbols; deterministic UUIDs (uuid5); checks each part's pins against its symbol and the MCU pins against `MCU_RaspberryPi:RP2354A`; writes the project symbol library and the library tables. | Reads KiCad symbol files | Generic engine. Hard-wired: `_SYMBOL_BY_FOOTPRINT`, `_SYMBOL_BY_VALUE`, `_POWER_SYMBOL` (GND, +3V3, +5V, +1V1, VBUS), `check_mcu_pins`, `MCU_INTERNAL_FLASH_PINS`, the two box symbols, the project name `"macropad"` in six places, file format `version 20250114`, `generator_version "9.0"`. |
| `sheet_layout.py` | 236 | Data only: where each part sits on the A3 sheet (grid steps of 1.27 mm), which wires are drawn, rails, power flags, notes, in 13 `Block`s. | No | Rewrite completely for a new circuit; the dataclasses (`Place`, `Wire`, `Rail`, `Flag`, `Note`, `Block`) stay. |
| `symlib.py`, `sexpr.py` | 197, 54 | S-expression parser and writer; reads KiCad symbol libraries, resolves `extends`, pin positions under rotation; `box_symbol` draws a box symbol for a part KiCad has none for. | No | Generic. `box_symbol` is the way to draw a radio module, a display connector or a fuel-gauge chip that has no stock symbol. |
| `models.py` | 198 | Block 3D models (boxes and cylinders) per footprint, written as VRML to `pcb/lib/3d/`, because the plain container has no 3D library. Heights are nominal. Checks that no bottom-side part is taller than `stack.underside_clearance`. | Yes | Generic engine; the `_ONE_BLOCK` and `_SHAPED` tables are per part. |
| `silk.py` | 135 | Silkscreen text and outlines. | Yes | Rewrite positions and strings. |
| `fab.py` | 117 | `bom-jlcpcb.csv` (Comment, Designator, Footprint, LCSC Part #), `cpl-jlcpcb.csv` (Designator, Mid X, Mid Y, Layer, Rotation; Y negated; position = centre of the SMD pads), `check_outputs`. | Yes | Generic except the `macropad-` file prefix and the four-layer `GERBER_SUFFIXES`. It applies no JLCPCB rotation or offset correction (see 2.4). |
| `build.py` | 201 | Orchestrates: schematic, ERC, netlist compare, models, place, route, connectivity without pours, outer pours, fill, DRC with parity, routing report, length checks, renders. `order` searches a routing order for up to 12 rounds. | Yes | Generic except file names and `ACCEPTED_FINDINGS`. |
| `test_router.py`, `test_schematic.py` | 252, 170 | 15 router tests and 19 schematic-writer tests, `unittest`, no KiCad and no symbol libraries needed. | No | Keep; they test the engines, not the circuit. |

Source: the files named, read in full or by outline. Confirmed.

What is hard-wired to the old board, in one list (confirmed by `grep -n macropad pcb/gen/*.py` and by
reading): the name `macropad` in `build.py` (3), `fab.py` (2), `layout.py` (1), `schematic.py` (8),
`silk.py` (3), `circuit.py` (3 footprint names); the RP2354A pin geometry and supply scheme; four copper
layers with that plane assignment; a rectangular outline; one USB receptacle on the back edge; the
nice!view 5-pin socket; SK6812 side LEDs; direct-wired keys with no matrix and no diodes; all parts on
the bottom face except three hand-soldered ones.

### 2.2 The router's limits

Source: `macropad/pcb/gen/router.py` header and constants, `macropad/pcb/README.md` "How the routing
works". Confirmed.

- Two routing layers only (F.Cu and B.Cu). Inner layers are planes, reached by vias; a via "fits" only
  where the plan's plane test says the right plane is underneath.
- 0.1 mm grid, 45 degree moves, A* with a greedy factor of 1.5, turn costs, via cost equal to 3 mm of
  track, search limit 3 000 000 nodes per connection.
- Obstacles are axis-aligned rectangles: every pad is fed in as its KiCad bounding box
  (`route.py:_load_obstacles`). A round or rotated pad is treated as its box.
- No rip-up and no negotiation. A net that ends up walled in stays unrouted; `build.py order` reruns the
  whole board with that net moved to the front, up to 12 rounds, about 10 minutes, and it can fail.
- No differential pairs, no length matching, no impedance. The USB pair is two separately routed tracks
  with a 2 mm mismatch limit.
- No teardrops. No via-in-pad except the MCU exposed pad.
- Rules: track 0.15 mm, wide track 0.3 mm, clearance 0.15 mm (the router keeps 0.17), via 0.6/0.3 mm,
  copper to edge 0.3 mm, copper to hole 0.25 mm.
- Result on the old board: 797 tracks, 160 vias, 0 unrouted, 51 nets, 71 machine-placed parts on 84 x 82.5 mm.

Note: `macropad/pcb/.build/` (ignored) still holds `freerouting.jar`, a `.dsn` file and backup routing
plans, and `worxboard/pcb/.tools/` holds `freerouting-2.5.0.jar`. Both projects tried Freerouting and
then dropped it ("no Freerouting", `worxboard/README.md`; "no third-party autorouter",
`macropad/CLAUDE.md`). Confirmed that the files exist; likely that the tool was rejected for results.

### 2.3 Checks: ERC, DRC, parity, connectivity

Source: `macropad/pcb/gen/build.py`, `macropad/Makefile`, `macropad/pcb/README.md` "Checks". Confirmed.

1. `circuit.py` netlist self-check (no single-pad net, no duplicate reference).
2. Each part's pad numbers against its KiCad symbol; the MCU's GPIO, supply and fixed pins against
   KiCad's own MCU symbol; each chip's footprint against the footprint the symbol names.
3. `kicad-cli sch erc --severity-all --exit-code-violations`: zero errors and zero warnings.
4. `kicad-cli sch export netlist --format kicadsexpr`, then every pin's net compared with `circuit.py`.
5. `layout.check_placement`: flips and rotations.
6. DRC of the board saved without outer ground pours (`--severity-error`), so a ground pad with no via
   cannot hide behind a pour.
7. `kicad-cli pcb drc --severity-all --schematic-parity`: every finding must be in `ACCEPTED_FINDINGS`
   (one entry, named and explained), "Found 0 unconnected pads", "Found 0 Footprint errors".
8. `route.check_sensitive_lengths`.
9. `make pcb-check`: `kicad-cli pcb drc --severity-error --schematic-parity --exit-code-violations --format report`.
10. `fab.check_outputs` after the Gerber export.

Schematic parity works because the board's footprints carry the schematic symbol's UUID path
(`footprint.SetPath(KIID_PATH(...))`, `layout.py:86`), net names follow KiCad's convention (labels get a
leading slash, power symbols do not; `schematic.board_net_name`), and open pins get KiCad's own
`unconnected-(...)` net names read back from the exported netlist. Confirmed.

### 2.4 Gerbers, BOM and CPL for JLCPCB

macropad (`macropad/Makefile` target `pcb-fab`, confirmed):

```
kicad-cli pcb export gerbers --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts --subtract-soldermask -o pcb/fab/gerbers/ <board>
kicad-cli pcb export drill --format excellon --excellon-units mm --excellon-separate-th -o pcb/fab/gerbers/ <board>
zip -q -r -FS <name>-gerbers.zip gerbers
python3 pcb/gen/build.py fab        # BOM, CPL, check_outputs
```

`check_outputs` requires: all 11 Gerbers present, non-empty and newer than the board; one via drill
size; drill hits equal the via count; BOM, CPL and `circuit.py` name the same machine-placed parts;
every BOM line has a `C<digits>` number.

Known gap in macropad: the CPL carries KiCad's rotations unchanged. `macropad/docs/ordering.md` step 6
tells the builder to check every part in JLCPCB's preview. No panel, no PCBWay files, no stock check.
Confirmed.

worxboard closes that gap (`worxboard/pcb/scripts/stage_d.sh`, `stage_p.sh`, `pcb/pcb.just`, confirmed):

- KiKit 1.8.1: `python3 -m kikit.ui fab jlcpcb --assembly --missingError --no-drc --schematic <sch> --field LCSC --correctionpatterns pcb/scripts/jlc_rotations.csv <pcb> <out>`.
- `pcb/scripts/jlc_rotations.csv`: per-footprint X, Y and rotation corrections. Rows that matter for
  worxpad: SOT-23-5 and SOT-23-6 rotation -90; `USB_C_Receptacle_HRO_TYPE-C-31-M-12` Y -1.394;
  the project's MX hot-swap socket X 0.635, Y 3.81, rotation 180.
- `cpl_check.py` places JLCPCB's own footprint of every part (`jlc_footprints.json`, 148 kB) from the CPL
  on the KiCad pads and requires agreement within 0.1 mm with pin 1 on pin 1.
- `netcmp.py --board` checks LCSC fields on the board, the BOM and the CPL against `design.py`, and fails
  on a number in the `RETIRED` table.
- `stage_p.sh` builds the order package: KiKit panel (`panel.json`: tight frame, 6 mm rails, 2 mm slot,
  mouse bites, 3 fiducials, 4 tooling holes), panel DRC, panel and bare-board Gerbers, BOM, CPL, a
  generated README with the remark text for JLCPCB's engineers, an order zip, and `pcbway/` with KiCad's
  own position files, an MPN BOM (`mpn.json`, fetched by `mpn.py` from LCSC) and a README.
- `jlc_check.py check <side> <package> --stock <n>` is the live stock check run on the order day.
- The package is byte-reproducible (`PYTHONHASHSEED=0`, seeded KIIDs, date-free Gerbers) and CI compares it.

JLCPCB order facts recorded in the siblings (from the owner's own notes, not re-checked here; treat as
likely and re-verify on the order day):

| Fact | Source |
|---|---|
| 4-layer default stack-up JLC04161H-7628, 1.6 mm, 1 oz outer, 0.5 oz inner | `worxboard/docs/ordering-jlcpcb.md` section 2 |
| ENIG chosen for 0.4 mm pitch QFN and USB-C pads | same; `macropad/docs/ordering.md` section 3 |
| Vias 0.3 mm drill, 0.6 mm pad are inside the default "min via" option | same |
| Economic PCBA places one side only; Standard is needed for both sides | `worxboard/docs/ordering-jlcpcb.md` section 3 |
| "Basic" parts have no setup fee; "Extended" parts have a one-time fee per distinct part | `macropad/docs/parts.md` |
| Fiducials: 1.0 mm copper in a 2.0 mm opening, JLCPCB asks for 3.85 mm from the edge; rails 6 mm or wider | `worxboard/docs/ordering-jlcpcb.md` section 3 |
| Pad hole-to-hole spacing limit 0.45 mm | same |
| Track and space limit 0.09 mm, drill limit 0.3 mm on 4 layers (design uses 0.15 and 0.3) | comment in `macropad/pcb/gen/layout.py:27` |
| The two siblings disagree on the order-number mark: macropad says choose "Specify a location" and prints `JLCJLCJLCJLC`; worxboard says the option was dropped in 2026-05 | `macropad/docs/ordering.md` section 3, `worxboard/docs/ordering-jlcpcb.md` section 2 |

JLCPCB part numbers already chosen and stock-checked on 2026-11-12 in `macropad/pcb/gen/circuit.py`
`LCSC` and `macropad/docs/parts.md` that worxpad can reuse as a starting point (confirmed as written
there; stock moves): USB-C TYPE-C-31-M-12 `C165948`; USBLC6-2SC6 `C7519`; AP2112K-3.3 `C51118`;
nSMD050 fuse `C69688`; TS-1187A tact switch `C318884` (basic); Kailh hot-swap socket CPG151101S11-2
`C49352235`; Alps EC11E18244AU `C202365`; passives 100 nF `C1525`, 1 uF `C52923`, 4.7 uF `C23733`,
2.2 uF `C23630`, 10 uF 0603 `C19702`, 5.1 k `C25905`, 10 k `C25744`, 1 k `C11702`. worxboard adds
SOD-123 diodes and a second-source socket `C41430893` (`worxboard/pcb/scripts/design.py`).

### 2.5 Docker images and how they are invoked

| Repository | Image | Pinned by | Invocation | Source | Confidence |
|---|---|---|---|---|---|
| macropad | `kicad/kicad:9.0.9` | tag only | `pcb/kicad.sh <cmd>`: `docker run --rm --user $(id -u):$(id -g) -e HOME=/tmp -v $repo:$repo -w $repo kicad/kicad:9.0.9 "$@"` (the repository is mounted at its own path) | `macropad/pcb/kicad.sh` | confirmed |
| worxboard | `kicad/kicad:10.0.7` and `kicad/kicad:10.0.7-full` (3D models, used for STEP and renders only) | digest in `tools/images.lock`; `tools/pull_images.sh <tag>` pulls by digest and tags | `docker run --rm --network none -u $(id -u):$(id -g) -e HOME=/tmp -e PYTHONHASHSEED=0 -v $PWD:/w -w /w -e PYTHONPATH=/w:/w/pcb/.tools/site313 <image>` | `worxboard/pcb/pcb.just`, `tools/images.lock`, `tools/pull_images.sh` | confirmed |
| worxboard-ergo | same KiCad digest | `toolchain.lock.json` (`images.kicad`, `kicad_version` 10.0.7) | `tools/pcb.sh`, same flags | `worxboard-ergo/tools/pcb.sh`, `toolchain.lock.json` | confirmed |
| worxboard, worxboard-ergo | `zmkfirmware/zmk-build-arm:stable` | digest in the same lock files | `firmware/firmware.just`, `tools/firmware.sh` | as named | confirmed |

Digests (confirmed, `worxboard/tools/images.lock`):

```
kicad/kicad:10.0.7        kicad/kicad@sha256:3224d1bf143185ecc1bd3a1082a36f37f0f4e59d707983a16515a845e3737fc6
kicad/kicad:10.0.7-full   kicad/kicad@sha256:347d5b7d5d88207ba4217cdf594eeccd142279600d023e7a7e426f8599c77708
zmkfirmware/zmk-build-arm:stable   zmkfirmware/zmk-build-arm@sha256:edb1c953438c6f720ddb79c3762f3972013b7fbbaf4fff3592fc869983e7afc5
```

`tools/kicad_env.sh` runs first in every KiCad 10 container. It copies the stock library tables from
`/usr/share/kicad/template` into `$HOME/.config/kicad/10.0/` and appends the project library
(`${KIPRJMOD}/../lib/<name>.pretty` and `.kicad_sym`). It is needed because `HOME=/tmp` is empty in the
container. Confirmed, `worxboard/tools/kicad_env.sh`.

Container Python dependencies for worxboard are installed on the host into `pcb/.tools/site313` with
`uv pip install --python-version 3.13 --target ...` (kikit 1.8.1, kicad-sch-api 0.5.6, shapely 2.2.0) and
put on `PYTHONPATH`; the KiCad 10 image's Python is 3.13. worxboard-ergo uses a hash-locked
`pcb/requirements.lock`. Confirmed.

All of these images are already present on this machine (`docker images`, confirmed 2026-11-13):
`kicad/kicad:9.0.9`, `kicad/kicad:10.0.7`, `kicad/kicad:10.0.7-full`, and the ZMK image by digest.

### 2.6 Probe: macropad `pcb/gen` does not run unchanged on KiCad 10.0.7

A scratch copy of `macropad/board.toml` and `macropad/pcb/` was run with
`docker run --rm --network none ... kicad/kicad:10.0.7 python3 pcb/gen/build.py place`. It stopped at the
first library check:

```
AssertionError: J1: Connector:USB_C_Receptacle_USB2.0_16P has no pins ['S1']
```

KiCad 10's stock USB-C symbol names its shield pin differently from KiCad 9's. This is the first
difference only; the run did not get as far as `pcbnew`, so API differences (for example
`FLIP_DIRECTION_TOP_BOTTOM`, `SetField`, the schematic file version `20250114`) are untested. Confirmed
by the run on 2026-11-13; the scratch copy was deleted afterwards. worxboard's `pcb/scripts/place.py`
is a working reference for `pcbnew` use under KiCad 10.

### 2.7 What worxboard and worxboard-ergo use instead

worxboard (`worxboard/pcb/scripts/`, `pcb/pcb.just`, confirmed):

- `layout/` Python package is the source of truth (key positions, holes, outline, `pins.py` GPIO map);
  `pcb/scripts/design.py` is the circuit as data (parts, nets, LCSC numbers, `RETIRED` table).
- Stage A: `gen_footprints.py`, `gen_sch.py` (with the `kicad-sch-api` library), ERC as JSON, netlist
  export, `netcmp.py`.
- Stages 7-8: `place.py`, `route_critical.py` (locked hand-scripted routes for matrix and LED cells).
- Stage C: `route.py` and `complete_routes.py`, an in-house maze router on shapely and numpy with A*,
  45 degree moves, grids of 0.1 and 0.05 mm, F.Cu, B.Cu and one inner layer at a cost, and a
  transactional rip-up (`negotiate`); GND stitching vias; `gnd_ties.py`, `prune.py`,
  `pin_in_paste.py`; DRC gate with `--schematic-parity`; `checks.py`.
- Stage D on the `-full` image: KiKit JLCPCB outputs, `cpl_check.py`, renders, Edge.Cuts DXF, board STEP
  (`kicad-cli pcb export step --subst-models --no-dnp`), which the case fit check reads.
- Stage P: order package (2.4).
- Size: about 400 kB of Python in `pcb/scripts/` (`route_critical.py` 50 kB, `complete_routes.py` 40 kB,
  `checks.py` 36 kB, `pcbway.py` 31 kB, `netcmp.py` 27 kB, `place.py` 26 kB, `jlc_check.py` 24 kB).
  It is written for a two-half keyboard with a diode matrix and per-key LEDs.

worxboard-ergo (`worxboard-ergo/tools/pcb.sh`, `README.md`, confirmed): the same approach cut down
(`gen_sch.py`, `place.py`, `check.py`, `maze.py`, `route.py`, `rules.py`), reports committed to
`pcb/reports/`. Its boards have zero tracks; `make check-fabrication` fails on purpose. It is not a
working base for routing.

### 2.8 Which base for an nRF- or ESP-class board with a module, battery and display

Recommendation (reasoned from the findings above; not a fact):

1. **Structure and generator: start from macropad `pcb/gen`.** It is the closest device, it is small,
   its engines (`router.py`, `schematic.py`, `symlib.py`, `sexpr.py`, `models.py`, `fab.py`, `build.py`)
   are generic, and its tests run without KiCad. A castellated radio module removes the hardest part of
   the old routing plan: there is no QFN escape comb, no on-chip switching regulator, no crystal, and
   few decoupling capacitors. What is left of `route.py` is the generic part: sensitive nets first (USB
   pair, battery and charger power, antenna keep-out), plane fan-out, then signals shortest first.
2. **Toolchain pinning and order outputs: take them from worxboard.** Move to `kicad/kicad:10.0.7` by
   digest with `tools/images.lock`, `tools/pull_images.sh` and `tools/kicad_env.sh`, run with
   `--network none` and `PYTHONHASHSEED=0`. Add a JLCPCB rotation-correction table to `fab.py` (seeded
   from `jlc_rotations.csv`), a committed order package with a README and remark text, and a `pcbway/`
   folder with an MPN BOM. This costs a port of `pcb/gen` to KiCad 10 (2.6): symbol pin names, the file
   format version, and possibly `pcbnew` calls. The alternative, staying on 9.0.9, works today but
   leaves the family on two KiCad versions.
3. **Do not start from worxboard's `pcb/scripts`.** It is five times larger, tied to a split keyboard,
   and GPL-3.0-or-later. Borrow single files instead (see section 6).

New work that neither sibling has (confirmed by absence; `grep` finds no battery, charger, antenna or
FPC connector part in either circuit file):

- LiPo cell connector, charger, power-path or load switch, battery voltage sensing, soft power switch.
- A radio module footprint with an antenna keep-out zone in all copper layers. `layout.py` has
  `add_fiducial_keepouts` as the pattern for a rule area.
- A colour TFT on an FPC connector with backlight drive. Both siblings use the nice!view on a 2.54 mm socket.
- A key matrix with diodes if the module has too few GPIOs for 16 keys, 2 encoders with push, 2 buttons,
  the display bus and battery sensing. macropad wires one GPIO per key and has no diodes; worxboard has
  the matrix-with-diodes pattern (`layout/pins.py`, SOD-123 in `design.py`).
- Two round buttons (or flat dials) that are neither MX keys nor EC11 encoders.
- Parts on both faces. macropad puts every machine-placed part on the bottom so that JLCPCB assembles
  one side; a display connector and battery connector may force the choice again.
- A non-rectangular outline if the case needs one. `layout._outline` and `Router._close_board_edge`
  handle a rounded rectangle only.

---

## 3. CAD toolchain

### 3.1 Package layout (macropad)

Source: `macropad/cad/README.md` table "Module / Holds", the files in `macropad/cad/macropad_case/`
(3 761 lines). Confirmed.

| Module | Lines | Holds |
|---|---|---|
| `spec.py` | 351 | Loads `board.toml` into a namespace (`BOARD`); frozen dataclass `Case` with every case-only dimension, each commented with its reason and tagged `MEASURE` or "guess"; `Levels` (Z heights, PCB top face = 0); span helpers. Variant constants `PRINT`, `CNC`. Frame: X as the board, model Y = minus board Y, Z = 0 on the PCB top. |
| `solids.py` | 160 | Helpers that take board coordinates: `box`, `slab`, `chamfered_slab`, `rounded_rectangle`, `stadium`, `legend`, `millable(pocket, variant)`, `case_outline(variant)`, `overlap_volume`. |
| `parts.py` | 337 | `base(variant)` and `top(variant)`. |
| `small_parts.py` | 194 | Light bars, knobs, lens, foot strips, centre pad, tilt bar; `case_parts(variant)` returns the dictionary of all parts. |
| `components.py` | 222 | Reference shapes of bought parts (PCB, MX switch, keycap, hot-swap socket, EC11, display, USB receptacle and plug, LED, button, screw), drawn from datasheets. |
| `checks.py`, `measure.py` | 345, 307 | Interference of every pair, named clearances, measurements on finished solids, CNC tool-reach, printability. `PRINT_POSES` holds the bed orientation of each printed part. |
| `printsim.py` | 127 | Layer-by-layer print check: 0.2 mm layers on a 0.1 mm grid; tells a bridge from a cantilever. |
| `selftest.py` | 116 | Known-bad and sound shapes that each measuring check must judge correctly before the case is judged. |
| `raster.py`, `render.py` | 547, 295 | A numpy software renderer and the list of views. |
| `drawings.py` | 594 | General arrangement and two machine-shop sheets as SVG (A3), PDF and PNG through `rsvg-convert`; four DXF outlines. |
| `signature.py` | 117 | Engraving on the base underside (work in progress in the working tree). |
| `export.py` | 48 | STEP and STL writing. |

`cad/build.py` runs `check`, `export`, `render`, `draw` or `all`; `check` writes
`cad/exports/checks.json` and exits non-zero on any failure. Confirmed.

The macropad working tree has uncommitted CAD changes and the last two commits are "WIP: case redesign
in progress" and "WIP: add the signature engraving" (`git status`, `git log`). Treat
`macropad/cad/README.md` numbers as a snapshot. Confirmed.

### 3.2 Virtual environment

```
cd cad
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -e .
.venv/bin/python build.py all
```

Source: `macropad/cad/README.md` "Build". `pyproject.toml` gives floors only: `build123d>=0.13`,
`trimesh>=4.0`, `numpy>=1.26`, `matplotlib>=3.8` (for the DejaVu font), `scipy>=1.11`, `pillow>=10.0`;
ruff line length 110; no lock file. Installed in `macropad/cad/.venv` today: Python 3.12.16,
build123d 0.13.0, cadquery-ocp-novtk 8.0.1.1.0, numpy 2.5.4, matplotlib 3.11.2, pillow 13.0.0.
Confirmed by listing `site-packages`.

worxboard and worxboard-ergo pin exactly (`build123d==0.13.0`, `shapely==2.2.0`, `ezdxf==1.4.5`,
`trimesh==4.12.2`) with a root `pyproject.toml`, `uv.lock`, `requires-python = "==3.12.*"` and
`uv sync --locked`. Confirmed. Recommendation: keep macropad's `cad/.venv` layout but add exact pins or
a lock file.

Tools on this machine: `uv` 0.13.7, `just` 1.59.0, `rsvg-convert`, `magick`, `cargo` with target
`thumbv8m.main-none-eabihf`. Not on PATH: `freecadcmd`, `pio`, `west`. Confirmed.

### 3.3 Export formats

| Repository | Formats | Layout | Source |
|---|---|---|---|
| macropad | STEP (assembled position) and STL (lying the way it prints) per part; one `assembly.step` with labelled children; `checks.json`; drawings as SVG, PDF, PNG; DXF for lens, lens mask, engravings | `cad/exports/print/{base,top}.*`, `cad/exports/cnc/{base,top}.*`, shared small parts at `cad/exports/*.{step,stl}`, `cad/exports/drawings/` | `macropad/cad/macropad_case/export.py` |
| macropad-nyxilab | STEP, STL, 3MF (named, coloured, oriented), GLB for the web viewer, FreeCAD document, PDF blueprints, `manifest.json`, `checks.json`, fit-test coupons | `<edition>/cad/exports/{step,stl,3mf,gltf,freecad,drawings}/`, `3mf/fit-tests/` | `macropad-nyxilab/common/cad/macropad_cad/export.py` |
| worxboard-ergo | STEP, STL, 3MF, FreeCAD; meshes checked watertight; STEP volume round-trip; `SHA256SUMS` manifest | `cad/exports/{mx,choc}/` | `worxboard-ergo/tools/cad.py`, `AGENTS.md` |
| worxboard | STEP, STL, DXF plates, PDF drawings, `hole_table.csv` | `case/exports/` (ignored), `case/production/` (committed) | `worxboard/case/case.just` |

Confirmed. macropad does not export 3MF or GLB. Bambu Studio opens STEP and 3MF directly, so a 3MF
export in print orientation (the nyxilab `_write_3mf` pattern with `build123d.Mesher`) is the useful
addition for the owner's printer (recommendation).

### 3.4 Renders

- macropad: its own numpy z-buffer rasteriser with a shadow map, contact shadow, edge inking, section
  hatching, a "metal" material term for anodised aluminium and decals. 1600 x 1100 pixels, 2x
  supersampling, 4 worker processes at about 1 GB each. No GPU, no window system. Materials and four
  colourways are tables in `render.py`. The display in the render shows
  `docs/images/ui/media.png` (640 x 272), the firmware simulator's own picture. Views produced: hero,
  hero_aluminium, colourways, exploded, side_profile, top_plan, underside, back_usb, two sections,
  shells_inside, print_plate, details. Source: `macropad/cad/macropad_case/raster.py`, `render.py`,
  `macropad/CLAUDE.md`. Confirmed.
- macropad-nyxilab: headless OpenGL through moderngl and EGL (`common/cad/macropad_cad/render.py`). Needs
  a GPU or Mesa. Confirmed.
- worxboard: `case/tools/zrender.py` on STL files with trimesh and matplotlib. Confirmed.
- worxboard-ergo: `uv run --with pyvista==0.46.3 python -m tools.render`; the latest commit says
  "path-traced renders with real keycaps". Confirmed from `README.md` and `git log`.
- PCB renders: `kicad-cli pcb render --width 1600 --height 1600 --quality high --background opaque`,
  top, bottom and two perspective views, of a bare copy (models stripped) and of the populated board;
  `kicad-cli pcb export svg` per copper layer and per assembly face; schematic as SVG and PDF.
  Source: `macropad/pcb/gen/build.py:write_images`. Confirmed.

The macropad renderer has no clear material: the lens is drawn as its mask only
(`macropad/cad/README.md`). A black anodised body with a glass-fronted colour display will need either
that workaround or the pyvista route (lead).

### 3.5 FDM and CNC variants

Source: `macropad/cad/README.md` sections "What the design is", "Printing", "CNC";
`macropad/cad/macropad_case/parts.py`, `solids.py`, `spec.py`. Confirmed.

One model, a `variant` argument (`"print"` or `"cnc"`) on `base`, `top`, `case_outline` and `millable`.

| Aspect | Print variant | CNC variant |
|---|---|---|
| Outline corners | plain R 6.4 arcs (the top prints standing on a side wall) | quintic Bezier corners with continuous curvature, minimum radius 4.71 mm |
| Pockets | as drawn | every pocket opened with a 1.5 mm corner radius (`millable`), for a 3 mm end mill; gaps under 3 mm left solid |
| Switch cut-outs | 14.0 mm square | 14.0 mm square with dog-bone corner reliefs |
| Printer-only features | 45 degree fillers, boss webs, fins, engraved legends 0.4 mm deep | none; parts stay plain for laser marking; engraving DXFs are exported |
| Screw holes in the top | 1.7 mm, self-tapping in plastic | drill 1.6 mm and tap M2 |
| Edges | 45 degree chamfers only (0.5, 1.5, 0.3 mm), no fillets, in both variants | same; cut with a 90 degree chamfer mill |
| Checks | layer-by-layer bridge (limit 15 mm) and cantilever (limit 1.5 mm, a guess), bed contact at least 100 mm2, face overhang patches | 3 mm tool run over a 0.1 mm height map from above and below, no sharp internal vertical edge, smallest concave radius 1.5 mm, no undercut |
| Setups | no supports; STL already oriented | 3-axis, two setups per shell |

Small parts (light bars, knobs, feet, tilt bar) are printed in both variants.

### 3.6 Tolerances and fits in use

All from `macropad/cad/macropad_case/spec.py` unless noted. Confirmed as written; none has been printed.

| Fit | Value |
|---|---|
| PCB to case wall (`pcb_gap`) | 0.3 mm per side |
| Minimum wall (`min_wall`) | 0.8 mm (two passes of a 0.4 mm nozzle) |
| Side wall, floor | 2.7 mm, 2.4 mm |
| Lap joint (`lap_fit`) | 0.2 mm on size; flanks 0.14 mm apart |
| Lens in recess (`lens_fit`) | 0.1 mm per side |
| Light bar in channel (`diffuser_fit`) | 0.15 mm |
| Foot in recess (`foot_recess_fit`) | 0.2 mm per side |
| Knob bore (`knob_bore_clearance`) | 0.2 mm |
| USB opening margin (`usb_margin`) | 0.25 mm around a 12.5 x 6.5 mm plug overmould |
| MX plate | 1.5 mm thick, 14.0 mm cut-out |
| Plate top above PCB, hot-swap socket below PCB | 5.0 mm, 1.85 mm (`board.toml [stack]`) |
| Underside clearance PCB to case floor | 5.0 mm (`board.toml [stack]`) |
| Screws | M2 x 10 socket-head cap, ISO 4762, 3.8 mm head, counterbore 4.4 mm; minimum engagement 3.0 mm |
| Interference threshold | 0.05 mm3 shared volume counts as a clash (`checks.CLASH_VOLUME`) |
| nyxilab print tolerances | `PrintTol.pocket` 0.25 mm, `PrintTol.fit` 0.20 mm, knob bore 0.10 mm, switch hole 13.9 to 14.1 mm coupons (`macropad-nyxilab/docs/printing.md`) |
| nyxilab inserts | M3 x 5.7 x 4.6 mm heat-set, hole 4.0 x 6.2 mm (`macropad-nyxilab/docs/printing.md`) |
| CNC drawing note | ISO 2768-m, "a proposal, not a tested requirement" (`macropad/cad/README.md`) |

Slimness reference: the macropad body is 17.5 mm tall with MX switches, a 5.0 mm plate height and 5.0 mm
under the PCB (`macropad/README.md`). A 19 mm body with keycaps standing proud by a quarter of the body
height cannot be met with the same MX stack; that is a design question for the mechanical step, noted
here because the macropad `[stack]` values are the family's only worked example (likely).

---

## 4. Firmware conventions

### 4.1 macropad: Rust with embassy

Source: `macropad/firmware/Cargo.toml`, `firmware/Makefile`, `firmware/fw/Cargo.toml`,
`firmware/fw/src/board.rs`, `firmware/README.md`. Confirmed.

- Workspace members `core` (hardware-free logic: engine, keymap, debounce, quadrature, HID, display
  driver, UI, lighting), `fw` (the embassy binary, built from its own directory), `sim` (PC simulator
  that renders the real display and LED code to PNG and a demo GIF), `uf2` (ELF to UF2 converter that
  refuses an unbootable image). `default-members` excludes `fw`.
- `embassy-rp 0.10` with feature `rp235xa`, `embassy-executor 0.10`, `embassy-usb 0.6`, `embassy-time 0.5`,
  target `thumbv8m.main-none-eabihf`, release profile `opt-level = "s"`, LTO, one codegen unit.
- `make -C firmware all` = `cargo test`, `cargo fmt --check`, `cargo clippy -D warnings` (host crates and
  `fw`), `check-pins`, `check-hid`, UF2 into `firmware/dist/`. 220 unit tests.
- Docs: `firmware/README.md` (what it does, controls, display, lighting, build and flash, timing, checks,
  "What the review found", "Untested"), `firmware/KEYMAP.md`, `docs/keymap.md`, `docs/flashing.md`.
- USB IDs are the pid.codes test pair `1209:0001`, flagged as not for distribution.

Pin-map check (`macropad/tools/check_pins.py`, 170 lines, standard library only): parses
`firmware/fw/src/board.rs` with regular expressions (the `keys: [...]` list and each field initialiser in
`Board::take`) and compares the `PIN_<n>` numbers with `board.toml`; also checks the encoder detent
constant against the encoder part name, the key and LED positions in `core/src/geometry.rs` (micrometres)
and the outline, knob and display positions in `sim/src/board.rs`. `tools/check_hid.py` (221 lines)
parses the USB report descriptors as a host would. Both run in `make test` and in CI. Confirmed.

### 4.2 worxboard: ZMK

Source: `worxboard/firmware/firmware.just`, `firmware/zmk/`, `zephyr/module.yml`, `build.yaml`,
`layout/pins.py`. Confirmed.

- The repository is a Zephyr module: `zephyr/module.yml` at the root points `board_root` at
  `firmware/zmk`. Board definition in `firmware/zmk/boards/worxbend/<board>/` (hardware model v2 files:
  `board.yml`, `<board>.dtsi`, `<board>-pinctrl.dtsi`, `<board>-layouts.dtsi`, `Kconfig.*`,
  `*_defconfig`, `<board>.zmk.yml`, `<board>.keymap`); `firmware/zmk/config/` holds `west.yml`, `.conf`
  and the keymap; `firmware/zmk/src/` holds custom C (display rotation, status screen).
- ZMK is pinned to commit `4dd95d7840eb3d5a3f59bb29fbf1ab054715ef85` in `config/west.yml`; the build image
  is pinned by digest; Zephyr SDK 0.16.9 (`worxboard-ergo/toolchain.lock.json`).
- `build.yaml` is the build matrix (board, snippet `studio-rpc-usb-uart`, cmake args, artifact name),
  read by `just fw` and by the firmware workflow.
- `just fw` runs in the container with a west workspace in `build/fw-ws` and a ccache directory.
- Pin and layout checks: `layout/pins.py` is the frozen GPIO contract (pin names are KiCad symbol pin
  names) and feeds `design.py`, so the netlist compare (`netcmp.py`) ties the board to it;
  `gen_layouts.py --check` fails if the committed physical-layout dtsi is stale against `layout.json`;
  `check_keymap.py` checks binding counts and base-layer legends; `fw_check.py` inspects the built
  images (symbols, flash budget); a host C test covers the display pixel map.

Neither sibling has Bluetooth, a battery, or a colour display in firmware (confirmed by absence:
worxboard's `fw_check` asserts "no BLE/battery symbols" on the peripheral; macropad is USB only). The
only colour-display firmware in the family is macropad-nyxilab's C++ PlatformIO code for ST7789 panels
(`macropad-nyxilab/common/firmware/lib/nyx_ui`), with a UI simulator in `tools/ui_sim`.

Recommendation for worxpad firmware layout, whichever stack is chosen: keep the macropad rule that a
host-runnable simulator draws the real UI code and produces `docs/images/ui/`, and keep one script in
`tools/` that fails when the firmware pin map disagrees with `board.toml`. For ZMK the script compares
the generated or hand-written `.dtsi` and `-pinctrl.dtsi` with `board.toml` (worxboard's
`gen_layouts.py --check` is the pattern); for Rust it is `check_pins.py` with new field names.

---

## 5. Printer, print settings, CNC notes, ordering documents

### 5.1 Printer

- Bambu Lab A1 mini, build volume 180 x 180 x 180 mm. Source: `plastic-lighthouse/softbox.py:4` and
  `:211` (`assert (size <= 180).all()`), `plastic-lighthouse/README.md:4,14,116`. Confirmed.
- macropad-nyxilab states "All parts print without supports and fit a 180 x 180 mm bed"
  (`macropad-nyxilab/docs/printing.md:3`). Confirmed.
- macropad has no bed-size check in `cad/` (searched; none found). Its parts are 90 mm, so none was
  needed. worxpad should add one, as plastic-lighthouse does (recommendation).
- No slicer profile, filament brand or Bambu project file is committed in any sibling. camx and
  worxboard-ergo say their 3MF files carry geometry only. Confirmed by search; "not found" for a profile.

### 5.2 Print settings the owner writes down

| Source | Settings |
|---|---|
| `macropad/cad/README.md` "Printing" | 0.2 mm layers, 3 walls, 0.4 mm nozzle; PLA or PETG; no supports; STL already oriented; 8 mm brim on the tall top; light bars 100 % infill; feet in TPU |
| `macropad-nyxilab/docs/printing.md` | 0.2 mm layers; 3 to 4 walls; 15 to 20 % gyroid; 5 top and bottom layers; knob at 0.12 to 0.16 mm; PLA or PETG; textured PEI for a matte top face; 0.5 mm bottom chamfer against elephant's foot; bridges up to 8 mm on default settings |
| `camx/docs/assembly.md` | PETG, 0.2 mm layers, 4 perimeters, 5 top and bottom layers, 35 to 45 % infill; print the fit coupon first |
| `worxboard-ergo/docs/printing.md` | PETG or ASA, 0.2 mm, 4 perimeters, 20 % infill, plate 100 %; print test pieces first; "No slicer run backs these values" |

Confirmed. Common convention: no supports, parts exported in print orientation, a table of part,
orientation and notes, fit coupons printed first (nyxilab `fit-tests/`, camx `fit_coupon`, ergo test
pieces), and the instruction to change the model value and regenerate, never to file the print.
macropad has no fit coupons yet.

### 5.3 CNC vendor notes

Source: `worxboard/case/production/jlccnc/ORDER_NOTES.md`, `pcbway/ORDER_NOTES.md`,
`jlc3dp/ORDER_NOTES.md`, `hardware.csv`, `worxboard/case/case.just`. These are the owner's notes from
JLCCNC's published guidelines; confirmed as written there, not re-checked against the vendor today.

- One part per STEP file, with a 2D PDF drawing of the same file name next to it. The STEP governs
  geometry; the PDF governs threads, tolerances and finish. JLCCNC cannot quote an assembly STEP.
- Material aluminium 6061-T6. Finish: the anodising option that includes bead blasting. Appearance
  standard "Strict" (or Premium) so that parts of one order match in colour.
- Tolerance ISO 2768-m by default; tighter values only on the drawing's "FIT-CRITICAL" notes (hole
  patterns +/-0.1, switch cut-outs 14.00 +0.05/-0).
- Internal corner rule: R = H/10 + 0.5 with a tool of diameter H/5; past 10 mm depth the minimum radius
  of the tool that reaches. `just corners` checks every internal corner of the STEP against it.
- Minimum wall for metal 0.8 mm. Threads: blind holes keep at least D/2 unthreaded at the bottom; holes
  are modelled at tap-drill size with the drill point; mask threads during anodising or re-tap.
- Remark blocks to paste per part, and a table of prepared answers to engineering questions.
- State the cosmetic faces and where rack marks are allowed. Ask for a uniform anodise colour and that
  the parts must fit together.
- PCBWay CNC takes the same STEP and PDF; the page lists only differences and a "please confirm" block.
  It says PCBWay's current rules, form and prices were not checked.
- JLC3DP: TPU 95A is FDM only with a minimum part size of 30 x 30 x 10 mm (or 15); wall 1.6 mm standard,
  1.2 mm minimum; MJF PA12 for rigid parts.
- `hardware.csv` columns: item, qty, spec, where, note.
- macropad's own CNC notes (`macropad/cad/README.md` "CNC"): 3-axis, two setups per shell, 3 mm end
  mill, 1.5 mm pocket radius, 90 degree chamfer mill for every 45 degree face, no undercuts, dog-bones
  in switch cut-outs. Its three drawing sheets carry a hole and recess table from datum A.

The two rules differ: macropad uses a fixed 1.5 mm radius; worxboard uses JLCCNC's depth rule. For a
slim shell (pockets under 10 mm) the depth rule gives R 1.0 at 4 mm and R 1.5 at up to 10 mm, so
macropad's fixed 1.5 mm satisfies it for pockets up to 10 mm deep (derived from the two sources, likely).

### 5.4 Ordering documents that exist and can be mirrored

| Document | Use for worxpad |
|---|---|
| `macropad/docs/ordering.md` | Template for a single-board JLCPCB order: files table, numbered steps, options with reasons, placement-preview checklist, "Before you pay", "Order the rest", "Other board houses". |
| `macropad/docs/parts.md` | Template for the parts page: machine-placed, hand-soldered, plugged-in, case hardware, substitutions, dated stock. |
| `worxboard/docs/ordering-jlcpcb.md` (31 kB) | Full option-by-option table for a 4-layer two-sided Standard PCBA order, out-of-stock procedure, cost estimate, after-order and arrival checks. |
| `worxboard/docs/ordering-pcbway.md` | PCBWay turnkey counterpart: own BOM with MPNs and KiCad centroid file, coordinates and rotations section. |
| `worxboard/pcb/production/<side>/README.md` and `pcbway/README.md` | Generated per-package README with the remark text for the fab's engineers. |
| `worxboard/case/production/{jlccnc,pcbway,jlc3dp}/ORDER_NOTES.md`, `hardware.csv`, `README.md` | Template for the case order package. |
| `worxboard/docs/shopping-list.md`, `docs/bom.md` | Everything the fab does not supply. |
| `worxboard-ergo/docs/printing.md` | Template for a numbered local print guide with test pieces and "Known limits". |
| `macropad-nyxilab/docs/printing.md` | Template for the per-part print table and coupon table. |

---

## 6. Recommended skeleton for worxpad

A recommendation. It follows macropad's shape and adds the worxboard pieces that the request needs
(order packages for JLCPCB, PCBWay and CNC, pinned images, a print guide). Directory names for the
existing research tree are kept.

```
worxpad/                         (this repository: /home/worxbend/Projects/prota-clone)
  board.toml                     single source of truth: outline, key grid, knobs, buttons, display, USB, battery, holes, stack, GPIO map
  Makefile                       help, test, pcb, pcb-place, pcb-check, pcb-fab, pcb-test, cad, firmware, ui-images, docs-check, order
  README.md                      status block first; macropad section order
  CLAUDE.md                      what this is, commands, rules of the road, generated-file list, no AI attribution in commits
  LICENSE, LICENSE-HARDWARE      GPL-3.0-or-later and CERN-OHL-S-2.0 (owner to confirm)
  THIRD_PARTY.md                 every borrowed footprint, script and reference, with licence and source commit
  CHANGELOG.md                   one entry per revision letter
  .gitignore, .gitattributes     scratch ignored; generated files marked linguist-generated, binaries marked binary
  research/                      evidence for the design; _cache/ ignored
    raw/                         one notes file per research agent (this file)
    components/                  component option studies
  tools/
    images.lock                  container tags and digests
    pull_images.sh               pull by digest, tag locally
    kicad_env.sh                 seed KiCad library tables in the container
    check_pins.py                firmware pin map against board.toml
    check_docs.py                Markdown links, images, anchors and code-span paths exist
  pcb/
    kicad.sh                     run a command in the pinned KiCad container
    gen/                         circuit.py, layout.py, router.py, route.py, route_order.txt, schematic.py,
                                 sheet_layout.py, symlib.py, sexpr.py, models.py, silk.py, fab.py, build.py, test_*.py
    lib/worxpad.pretty/          project footprints (module, display connector, sockets); SOURCES.txt
    lib/3d/                      GENERATED block models
    kicad/                       GENERATED KiCad project
    fab/                         GENERATED: gerbers/, worxpad-gerbers.zip, bom-jlcpcb.csv, cpl-jlcpcb.csv
    production/                  GENERATED order packages: jlcpcb/ (zip, bom, cpl, README with remark), pcbway/ (MPN bom, centroid, README)
    netlist.txt, routing.txt     GENERATED reports
    README.md                    commands, files, layers, rules, routing, checks, what a person must still look at
  cad/
    pyproject.toml               pinned build123d, trimesh, numpy, scipy, pillow, matplotlib
    build.py                     check | export | render | draw | all
    worxpad_case/                spec.py, solids.py, parts.py, small_parts.py, components.py, checks.py, measure.py,
                                 printsim.py, selftest.py, raster.py, render.py, drawings.py, export.py, coupons.py
    exports/                     GENERATED: print/ (STEP, STL, 3MF), cnc/ (STEP), drawings/ (SVG, PDF, DXF),
                                 coupons/, assembly.step, checks.json
    production/                  GENERATED CNC order package: jlccnc/ (STEP + same-name PDF, hole_table.csv, ORDER_NOTES.md),
                                 pcbway/ORDER_NOTES.md, hardware.csv, README.md
    README.md                    design, parts, build, checks, printing, CNC, assembly, assumptions to measure
  firmware/                      layout depends on the stack chosen: Rust workspace (core, fw, sim, uf2) as macropad,
                                 or zmk/ (boards/worxbend/worxpad/, config/, src/) plus zephyr/module.yml and build.yaml at the root
    README.md, dist/             what it does, controls, display, checks, untested; built image
  docs/
    hardware.md                  circuit in words, pin map, power tree, layer stack, mechanical stack
    parts.md                     every part, JLCPCB number, type, dated stock, alternatives considered
    ordering.md                  JLCPCB assembled board, step by step
    ordering-pcbway.md           PCBWay counterpart
    ordering-case.md             CNC shells at JLCCNC or PCBWay; links to cad/production/
    printing.md                  local FDM prototype on a 180 mm bed: coupons, orientation, settings
    assembly.md, flashing.md, keymap.md
    reference-device.md          what is known about the reference product, each fact with source and confidence
    images/{cad,pcb,ui}/         GENERATED pictures
  .github/workflows/ci.yml       pcb-test, docs-check, firmware host tests and pin check
```

### Files to copy and adapt

| Copy from | To | Changes needed |
|---|---|---|
| `macropad/pcb/gen/router.py`, `test_router.py` | `pcb/gen/` | None for a rounded-rectangle board. A different outline needs `_close_board_edge` extended. |
| `macropad/pcb/gen/sexpr.py`, `symlib.py` | `pcb/gen/` | None. Use `box_symbol` for the radio module, the display connector and any chip without a stock symbol. |
| `macropad/pcb/gen/schematic.py`, `test_schematic.py` | `pcb/gen/` | Replace `macropad` (8 places); new `_SYMBOL_BY_FOOTPRINT`, `_SYMBOL_BY_VALUE`, `_POWER_SYMBOL` (add battery and switched rails); replace `check_mcu_pins` and `MCU_INTERNAL_FLASH_PINS` with a check of the module's pin table; set the file format version for the KiCad version chosen. |
| `macropad/pcb/gen/sheet_layout.py` | `pcb/gen/` | Keep the dataclasses; rewrite every `Block`. |
| `macropad/pcb/gen/circuit.py` | `pcb/gen/` | Keep `Part`, the `LCSC` and `FOOTPRINT` tables' shape, `all_parts`, `nets_to_pads`, `check_netlist`, `key_centre`, `_keys`, `_encoders`, `_mounting_holes`, `_fiducials`, the USB block. Delete all MCU geometry, decoupling, core regulator and crystal code. Add module, charger, battery, display, buttons, matrix diodes if used. |
| `macropad/pcb/gen/layout.py` | `pcb/gen/` | Library name; plane islands; `check_placement` asserts for the new parts (module orientation, antenna at the edge, display connector pin 1, socket mirror, USB mouth); add an antenna keep-out rule area modelled on `add_fiducial_keepouts`. |
| `macropad/pcb/gen/route.py` | `pcb/gen/` | Keep `_load_obstacles`, `Setup`, `RoutingResult`, `_Plan.pair`, `fan_out`, `net`, `plane_fan_out`, `signals`, `write_copper`. Rewrite `route()` and the sensitive-net tables. |
| `macropad/pcb/gen/models.py`, `silk.py` | `pcb/gen/` | New tables and strings. |
| `macropad/pcb/gen/fab.py` | `pcb/gen/` | File prefix; add a rotation and offset correction table seeded from `worxboard/pcb/scripts/jlc_rotations.csv`; write the PCBWay BOM and centroid file. |
| `macropad/pcb/gen/build.py`, `macropad/pcb/kicad.sh`, `macropad/Makefile` | same paths | File names; image tag or digest; add `--network none`; Gerber layer list if the layer count changes. |
| `worxboard/tools/images.lock`, `pull_images.sh`, `kicad_env.sh` | `tools/` | Library name `worxboard` to `worxpad`. GPL-3.0-or-later headers stay. |
| `worxboard/pcb/scripts/jlc_rotations.csv` | data for `fab.py` | Keep the rows for footprints worxpad uses; verify each in JLCPCB's preview. |
| `worxboard/pcb/scripts/cpl_check.py`, `jlc_footprints.py`, `mpn.py`, `jlc_check.py` | optional, `pcb/gen/` or `tools/` | Larger adaptation (they read worxboard's `design.py` and package layout). Worth it only if the placement preview check is to be automated. GPL-3.0-or-later. |
| `macropad/cad/build.py`, `pyproject.toml`, `macropad_case/solids.py`, `measure.py`, `printsim.py`, `selftest.py`, `raster.py`, `export.py` | `cad/`, `cad/worxpad_case/` | Package name; pin dependency versions; add 3MF export and a 180 mm bed check to `export.py` and `checks.py`. |
| `macropad/cad/macropad_case/spec.py`, `parts.py`, `small_parts.py`, `components.py`, `checks.py`, `render.py`, `drawings.py` | `cad/worxpad_case/` | Rewrite the geometry and the dimension tables; keep the structure (`Case` dataclass with reasons and tags, `Levels`, `case_parts(variant)`, `PRINT_POSES`, the five check groups, the materials table, the sheet builders). |
| `macropad-nyxilab/common/cad/macropad_cad/export.py` (`_write_3mf`), `fit_tests.py` | patterns for `export.py`, `coupons.py` | Reimplement for the new parts; the nyxilab repository has no licence file in the paths read, same owner. |
| `macropad/tools/check_pins.py` | `tools/` | New field names; parse the new firmware's pin file. |
| `macropad/.github/scripts/check_docs.py`, `.github/workflows/ci.yml` | `tools/` or `.github/` | `TOP_LEVEL` directory list; job steps. |
| `macropad/CLAUDE.md`, `README.md`, `pcb/README.md`, `cad/README.md`, `docs/*.md` | same paths | Structure and tone only; all content is new. |
| `worxboard/case/production/jlccnc/ORDER_NOTES.md`, `pcbway/ORDER_NOTES.md`, `hardware.csv` | `cad/production/` | Structure, form settings and remark style; all part data is new. |
| `worxboard/firmware/firmware.just`, `firmware/zmk/config/west.yml`, `zephyr/module.yml`, `build.yaml` | `firmware/`, root | Only if ZMK is chosen: board name, matrix rows, ZMK revision. |

---

## Sources read

macropad: `CLAUDE.md`, `README.md`, `Makefile`, `board.toml`, `.gitignore`, `.github/workflows/ci.yml`,
`.github/scripts/check_docs.py`, `pcb/README.md`, `pcb/kicad.sh`, `pcb/lib/SOURCES.txt`,
`pcb/gen/build.py`, `circuit.py`, `layout.py`, `fab.py` (in full), `route.py` (most), `router.py`,
`schematic.py`, `sheet_layout.py`, `symlib.py`, `models.py`, `silk.py`, `test_schematic.py` (headers and
outlines), `route_order.txt`, `routing.txt`, `cad/README.md`, `cad/build.py`, `cad/pyproject.toml`,
`cad/macropad_case/spec.py`, `export.py` (in full), `printsim.py`, `render.py`, `raster.py`, `parts.py`,
`checks.py`, `measure.py` and the other modules (headers and outlines), `docs/ordering.md`,
`docs/parts.md`, `docs/hardware.md` (first part), headings of `docs/assembly.md`, `flashing.md`,
`keymap.md`, `firmware/README.md` (first part), `firmware/Makefile`, `firmware/Cargo.toml`,
`firmware/fw/Cargo.toml`, `firmware/fw/src/board.rs`, `tools/check_pins.py`, `git log`, `git status`.

worxboard: `justfile`, `pyproject.toml`, `build.yaml`, `.gitignore`, `.gitattributes`, `THIRD_PARTY.md`,
`README.md` (first 45 lines and headings), `tools/images.lock`, `tools/kicad_env.sh`,
`tools/pull_images.sh`, `pcb/pcb.just`, `pcb/scripts/stage_a.sh`, `stage_c.sh`, `stage_d.sh`,
`stage_p.sh`, `design.py`, `route.py`, `complete_routes.py` (headers), `jlc_rotations.csv`, `panel.json`,
`firmware/firmware.just`, `firmware/zmk/config/west.yml`, `firmware/zmk/scripts/gen_layouts.py`,
`check_keymap.py` (headers), `zephyr/module.yml`, `layout/pins.py`, `case/case.just`,
`case/ORDER_NOTES.md`, `case/production/jlccnc/ORDER_NOTES.md`, `pcbway/ORDER_NOTES.md`,
`jlc3dp/ORDER_NOTES.md`, `hardware.csv`, `docs/ordering-jlcpcb.md` (sections 1 to 5),
`docs/ordering-pcbway.md` (first part), `docs/deviations.md` (first part), headings of
`docs/verification.md`, `docs/firmware.md`, `docs/case.md`, `.github/workflows/pcb.yml` (first part).

worxboard-ergo: `README.md`, `AGENTS.md`, `Makefile`, `pyproject.toml`, `toolchain.lock.json`,
`build.yaml`, `.gitignore`, `THIRD_PARTY.md`, `tools/pcb.sh`, `tools/firmware.sh`, `tools/native.sh`,
`tools/cad.py` (first part), `docs/printing.md`, `docs/cnc.md`.

macropad-nyxilab: `CLAUDE.md`, `README.md` (first 60 lines), `Makefile` (first 80 lines),
`docs/printing.md`, `common/cad/pyproject.toml`, `common/cad/macropad_cad/export.py` (matches),
`tools/build_viewer.py` (first part).

plastic-lighthouse: `softbox.py` (first 30 lines and line 211), `README.md` (lines 80 to 116).
camx: `docs/assembly.md` (printing section), search hits in `README.md` and `docs/`.

Commands run: `docker images`, `git remote -v`, `git log`, `git status`, listing of
`macropad/cad/.venv/lib/python3.12/site-packages`, `which` for local tools, and one container run of a
scratch copy of the macropad generator under `kicad/kicad:10.0.7` (section 2.6).

## What could not be reached or was not read

- Nothing was blocked. This task used no network.
- Not read in full: worxboard `README.md` (82 kB), `docs/design.md`, `docs/deviations.md` (184 kB),
  `docs/verification.md`, `docs/electrical.md`, `pcb/scripts/place.py`, `route_critical.py`, `checks.py`,
  `netcmp.py`, `cpl_check.py`, `package.py`, `pcbway.py`, `case/worxboard_case.py` (100 kB),
  `case/drawings.py`, `site/`; macropad `cad/macropad_case/parts.py`, `drawings.py`, `raster.py` bodies,
  `firmware/core` sources, `tools/check_hid.py`; macropad-nyxilab firmware and CAD bodies; camx CAD.
- Not run: `make test`, `make cad`, `make pcb` in macropad; no build was executed in any sibling
  repository. The status numbers quoted from the READMEs are the owner's, dated 2026-11-13 there.
- The KiCad 10 probe stopped at the first failed assertion. How many further changes a port needs is unknown.
- No slicer profile or filament choice for the owner's printer exists in any repository read.
- JLCPCB, JLCCNC, JLC3DP and PCBWay rules quoted here are the owner's notes in the siblings. They were
  not checked against the vendors' current pages in this task.
