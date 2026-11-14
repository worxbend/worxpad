# PCB

**Not built.** No board has been ordered, assembled or powered. This page says what the design files hold
and which automatic checks ran on them, nothing more. A clean rule check does not make a working board.

The PCB is generated. Nothing in `pcb/kicad/` is drawn by hand: `pcb/gen/` writes the schematic, the project
footprints and symbols, and the pictures from two inputs, `board.toml` (positions, pin map) and
`pcb/gen/circuit.py` (parts and nets).

State on 2026-11-14: circuit, footprints, symbols and schematic are done (PCB part 1). The board is placed
and **routed**: `make pcb-place` reports no unrouted pad, and `make pcb-check` finds 0 violations, 0 unconnected
items and 0 schematic parity issues. `make pcb-fab` wrote pcb/fab and pcb/production from it (2026-11-14). See [Board](#board-pcb-part-2) and [Routing](#routing).

<a href="../docs/images/pcb/schematic.pdf"><img src="../docs/images/pcb/schematic.svg" alt="schematic, one A2 sheet"></a>

The schematic, one A2 sheet in 14 blocks. [PDF](../docs/images/pcb/schematic.pdf),
[SVG](../docs/images/pcb/schematic.svg). It is a drawing of `pcb/gen/circuit.py`, not a second source of truth.

## Commands

| Command | Needs | What it does |
|---|---|---|
| `make pcb-test` | Python 3.11+ | Netlist self-checks, the 3V3 capacitance sum (D14), `tools/check_pins.py`, 73 unit tests. |
| `pcb/kicad.sh python3 pcb/gen/build.py schematic` | Docker | Footprints written and read back, schematic, ERC, netlist compare, PDF and SVG, block models. About 7 s. |
| `make pcb-place` | Docker | Schematic step, placed and routed board, planes filled, DRC with schematic parity, RF keep-out copper check, pictures in `docs/images/pcb/`, `pcb/routing.txt`. About 6 min (372 s on 2026-11-14, another job running). Fails while any pad is unrouted. |
| `pcb/kicad.sh python3 pcb/gen/build.py order` | Docker | Routes again and again, moving walled-in nets to the front; writes the best order to `pcb/gen/route_order.txt`. Several minutes per round. |
| `make pcb-fab` | Docker | Gerbers, drills, panel, JLCPCB and PCBWay files, board STEP. Refuses a board whose last DRC has an error, an unconnected item or a parity finding. |
| `pcb/kicad.sh python3 pcb/gen/build.py fab-draft` | Docker | The same files under `pcb/.build/draft/`, for testing the generator on an unfinished board. Never an order. |

`pcb/kicad.sh` runs `kicad/kicad:10.0.7` by the digest in `tools/images.lock`, with `--network none` and
`PYTHONHASHSEED=0`, and runs `tools/kicad_env.sh` first.

## Files

| Path | What |
|---|---|
| `pcb/gen/circuit.py` | Every part: value, JLCPCB number, footprint, face, board.toml position, nets. Pure Python. |
| `pcb/gen/footprints.py` | Writes the six project footprints into `pcb/lib/worxpad.pretty/`. Pure Python. |
| `pcb/gen/schematic.py` | Writes the KiCad 10 schematic, the project symbol library and the library tables. |
| `pcb/gen/sheet_layout.py` | Where each part sits on the sheet and which wires are drawn. Data only. |
| `pcb/gen/symlib.py`, `pcb/gen/sexpr.py` | Read KiCad symbol libraries; draw box symbols. From macropad, unchanged. |
| `pcb/gen/layout.py` | Placement: board.toml positions, the spots board.toml leaves open, outline, planes, placement asserts. |
| `pcb/gen/route.py` | Routing order and stages, rip-up and reroute, plane island repair, the copper writer. |
| `pcb/gen/router.py` | Grid router from macropad: outer layers plus short hops on both inner layers, escapes, rip-up with history costs, meanders, plane area check, `close_outside` for this outline. |
| `pcb/gen/route_order.txt` | Nets routed first: the key matrix, seeded by hand. |
| `pcb/gen/fab.py` | Gerbers, drills, the D23 panel, BOM, CPL with the rotation table, PCBWay files, STEP. |
| `pcb/kicad/worxpad.kicad_pcb` | Generated board. `pcb/kicad/worxpad.kicad_dru`: the two edge-clearance exceptions. |
| `pcb/routing.txt` | Generated routing report: tracks, vias, length per net, unrouted pads. |
| `pcb/gen/models.py` | Block 3D models (VRML) per footprint type, into `pcb/lib/3d/`. |
| `pcb/gen/build.py` | The steps above. |
| `pcb/gen/test_*.py` | Router (26), schematic writer (21) and circuit, footprint and pin-map tests (26). |
| `pcb/lib/SOURCES.txt` | Where every project footprint number comes from. |
| `pcb/kicad/` | Generated KiCad 10 project: schematic, library tables. |
| `pcb/netlist.txt` | Generated netlist, one line per net. |

## The circuit

Sources are the records in `research/components/` and `docs/decisions.md`. In short:

- **Radio:** u-blox BMD-340 in LV mode, VCC and VCCH on 3V3, 10 uF bulk, 32.768 kHz crystal with 2 x 20 pF,
  pin reset on P0.18, SWD on a TC2030-NL pad set. USB D+/D- and VBUS (pad 66) after the ESD array and PTC.
- **Flash:** W25Q128JVSIQ on QSPI with 100 nF.
- **Display:** FH34SRJ-24S, pin map from `board.toml` `display.fpc_pins`; AO3400A low-side backlight switch
  with 100k gate pull-down, 15 Ohm to LEDA, 1 uF and 100 nF at VDD.
- **USB-C:** HRO TYPE-C-31-M-13C, 5.1k on CC1 and CC2, USBLC6-2SC6 before the 1206L075 PTC, shell to GND.
- **Power:** BQ24072 (USB500, ISET 2.2k, ILIM 3.3k, EN1 100k from IN, TMR open, NTC on TS), AO3401A in the
  cell's positive line, JST PH (pin 1 positive), TPS7A0233 with its EN on the MSK12C02 slide switch,
  MAX17048 on BAT with 4.7k pull-ups to 3V3. 3V3 holds 21.6 uF nominal including the module's 9.4 uF (D14);
  the build fails if a capacitor is added or removed on 3V3 without changing `board.toml`.
- **Inputs:** 4 x 5 col2row matrix, one 1N4148W per position. Column 4: right encoder push R0, left encoder push
  R1, right button R2, left button R3 (D20). PEC12R-4215F encoders with A/B on P0.29/P0.31 (right) and
  P0.28/P0.30 (left); 10 nF filter footprints, not fitted (D36).
- **Other:** 11 test pads, eight holes (K and C NPTH 4.0, G plated with GND rings), six fiducials.

107 parts: 61 machine-placed (31 distinct JLCPCB numbers, the two THT encoders included), 16 hand-fitted
sockets, 4 not-fitted footprints, 26 pads, holes and fiducials.

## Symbols and footprints

Stock KiCad 10.0.7 symbols for every part that has one. Three box symbols are drawn in `pcb/gen/schematic.py`
and written to the generated `pcb/lib/worxpad.kicad_sym`: BMD-340 (pins from `board.toml` `[module.pads]`),
TPS7A02 (DBV pin order) and MAX17048 (TDFN pin table).

Stock footprints where KiCad has one, including the TC2030-NL pad set and the MSK12C02 switch. Six project
footprints in `pcb/lib/worxpad.pretty/`, sources in `pcb/lib/SOURCES.txt`: BMD-340 with its RF keep-out rule
area, FH34SRJ-24S, TYPE-C-31-M-13C, Choc V2 hot-swap, PEC12R-4 and the plated G hole.

## Checks

| Check | Where | Result (2026-11-13 and 2026-11-14, real runs) |
|---|---|---|
| No single-pad net, no duplicate reference | `circuit.check_netlist` | pass, 107 parts, 74 nets |
| 3V3 capacitors equal `power.rail_3v3_caps_uf`, sum under 22 uF | `circuit.check_rail_capacitance` | pass, 21.6 uF |
| Pin map: pads, nets, spares, fast pins, matrix, encoders, FPC pins | `tools/check_pins.py` | pass, 41 entries, 15 spares, 24 FPC pins |
| Each part's pins exist on its symbol; footprint matches the symbol's | `schematic.check_part_against_symbol` | pass |
| BMD-340 symbol (pin table) and footprint (figures 2, 12) name the same 68 pads | `schematic.check_module_symbol` | pass |
| Every project footprint loads in pcbnew with the pads that were meant | `build.write_footprints` | pass, 6 footprints |
| `kicad-cli sch erc --severity-all` | `build.py schematic` | 0 errors, 0 warnings |
| KiCad's exported netlist against `circuit.py`, pin by pin | `build.py schematic` | pass, 309 pins, 23 open pins |
| Unit tests | `make pcb-test` | 73 pass (2026-11-14) |
| Placement asserts: faces, antenna end and keep-out, J2 contact 1 and entry, socket mirroring, J1 edge and mouth, J3 mouth and body centre, SW18 actuator, hole keep-outs, J4 low zone, RF bay | `layout.check_placement` | pass |
| Router closes the USB notch and keeps the board middle open | `route.new_router` | pass |
| Routing | `build.py place` | pass: 0 pads unrouted; 1,980 tracks, 280 vias, 3,303 mm, of it 89 mm on In1.Cu and 119 mm on In2.Cu (2026-11-14). Commit 2d364fd left 36 pads on 25 nets |
| `kicad-cli pcb drc --severity-all --schematic-parity` | `build.py place` | pass: 0 errors, 0 unconnected, 0 parity findings, 11 warnings, all accepted (`ACCEPTED_DRC_WARNINGS`) (2026-11-14) |
| `kicad-cli pcb drc --severity-error --schematic-parity --exit-code-violations` | `make pcb-check` | pass: 0 violations, 0 unconnected items, 0 schematic parity issues (2026-11-14) |
| Crystal tracks within 8 mm, USB D+ and D- within 2 mm, no supply track on an inner layer | `route.check_sensitive_lengths` | pass: XL1 7.83 mm, XL2 6.55 mm, D+ 60.58 mm, D- 60.52 mm (2026-11-14) |
| No copper of any kind inside the RF keep-out on any of the 4 layers | `build.check_keepout_copper` | pass (X 119.85 to 124.45, Y 42.90 to 63.10) |
| Five thermal vias in U3's exposed pad; the 8-via fence outside both ends of the RF keep-out, each inside the ground fill on F.Cu, In1.Cu and B.Cu | `build.check_ground_vias` | pass (2026-11-14). A copy with one fence via removed failed |
| Stack-up written and kept by pcbnew, layers and thicknesses as `layout.STACKUP`, sum within 0.01 mm of `pcb.thickness` | `layout.check_stackup`, `layout.stackup_text` | pass (2026-11-14). A copy with the core changed failed |
| `+` nearer J3 pin 1, `-` nearer pin 2; no silk overlap (DRC) | `layout.check_polarity_marks` | pass (2026-11-14) |
| Board STEP envelope equals `pcb.thickness` within 0.02 mm | `fab.check_step_thickness` | pass on `fab-draft`: 1.616 mm. Without the mask skins it is 1.562 mm and fails |
| Order files from the board | `build.py fab` | pass (2026-11-14): 61 placements (56 on the bottom), 30 BOM lines, 280 vias of 0.300 mm, panel 8 slot pieces and 48 mouse-bite holes, panel DRC 0 errors, nearest tab 14.4 mm from the antenna strip, STEP 1.616 mm with 22 model types |

ERC runs with KiCad's default rule settings, which ignore four checks: single global label, four-way junction,
simulation model and footprint filter. Any other error fails the build, and so does any warning that is not
listed with a reason in `ACCEPTED_ERC_WARNINGS` in `pcb/gen/build.py`; that list is empty. A scratch copy with
the VBUS_SYS power flag removed failed on `power_pin_not_driven`, so the gate is live.

## What a person still has to look at

- **D12 gate:** VBUS on module pad 66 while 3V3 is off is not checked against the nRF52840 Product
  Specification. No board is ordered before it is.
- **MAX17048 exposed pad:** the stock DFN-8 2 x 2 footprint has a 0.8 x 1.6 mm pad; Maxim land pattern 90-0065
  was not read.
- **Scaled numbers (MEASURE):** BMD-340 inner-row step and 4.15 column; FH34SRJ pad inset 0.35 mm; USB-C slot
  copper ring. Print each footprint 1:1 and lay the part on it.
- **USB-C pads end at the notch edge** as the HRO drawing shows; the layout needs a local copper-to-edge
  exception there.
- **Encoder direction:** A and B follow KiCad's stock PEC12R pattern; if the knob counts backwards, swap them
  in firmware, not on the board.
- **Choc socket pads** have no paste: they are hand-soldered.
- No impedance calculation for the USB pair was made. Tracks are 0.10 mm; D+ is 60.58 mm and D- 60.52 mm
  (D- carries a meander to match), with vias where J1's alternating pads force them.
- **Signals on the inner layers:** 87 track pieces (89 mm) on In1.Cu and 112 (119 mm) on In2.Cu, all signals
  (list in [Routing](#result)). They cut the planes locally. Both planes stay whole under
  the USB pair and the crystal and the supply nets stay off them. In2.Cu fills as one piece; In1.Cu has one
  8.4 mm2 island under the module's middle, joined to ground only through vias. The return path of a signal
  that crosses a cut was not analysed. Fast nets on the inner layers: QSPI_IO0 (9.5 mm) and QSPI_IO2 (24.0 mm)
  on In1.Cu, QSPI_CSN, QSPI_IO1 and QSPI_IO3 (17.3 mm) on In2.Cu, LCD_DC (11.1 mm) on In1.Cu.
- **Via ring round the module:** the module escapes put a via about 1 mm outside the pad field for most outer
  pads, about 1.1 mm apart, and a group of vias under the module's middle. The planes fill round them; check
  the vias under the module against the BMD-340's keep-out guidance, which was not re-read for this.
- **Router rules:** 0.10 mm track and space everywhere (JLCPCB 4-layer limit 0.09), needed between the
  BMD-340's inner pad rows; 0.30 mm for the supply nets; 0.6/0.3 mm vias, some under the module; short signal
  hops on In2.Cu and In1.Cu.
- **Layout moves from board.toml guesses:** U6 to Y 11.2, J4 to Y 76.6 (`layout.MOVED`, reasons there).
  U2 is turned 90 degrees. Encoder pin pads are 1.6 mm round because J1's shell slots collide with the
  stock 1.8 mm pads at encoder pin rows Y 7.60.
- **Planes:** In1.Cu ground, In2.Cu 3.3 V over the whole board, cut locally by the signal hops above. Zones
  connect pads solid, no thermal spokes.
- **Rotation table** in `fab.py`: only the SOT-23-5/6 and SOIC-8 rows come from worxboard; check every
  designator in JLCPCB's placement preview.

## Board (PCB part 2)

`layout.place` is not used: `build.py place` calls `layout.build_board` and `route.route` directly, with the
open-pin nets from the schematic step. Faces follow D9. Bottom parts are flipped and turned half a turn, so
every bottom project footprint lands as `board.toml` draws it; `check_placement` asserts the cases that are
easy to get backwards.

**Net classes.** Widths are judgement, not computed: the router's 0.3 mm wide track is the floor for supply.

| Class | Nets | Rule |
|---|---|---|
| Input and battery power | VBUS, VBUS_SYS, VSYS, BAT, BAT_IN | up to about 0.5 A (USB500 input, 405 mA charge): 0.4 mm where it fits, 0.3 mm minimum |
| 3V3 | 3V3 | about 90 mA peak (D13): 0.3 mm |
| Ground | GND | plane; five 0.3 mm vias in the charger U3 exposed pad (power 6.3, `route.THERMAL_VIA_OFFSETS`); a via fence 0.5 mm outside both ends of the antenna keep-out (mcu-radio A3, `route.rf_stitch_points`) |
| USB pair | USB_DP, USB_DN | full-speed USB, impedance not controlled: two 0.10 mm tracks, lengths within 2 mm (`route.USB_PAIR_MISMATCH_LIMIT`). J1 to U6 to U1 pads 68/67, no stubs, no test pads, U6 within 3 mm of J1's pads. At 12 Mbit/s the edges are slow and the run is short, so no coupled 90 Ohm pair was routed |
| Crystal | XL1, XL2 | Y1, C1, C2 within a few mm of U1 pads 13/14, ground around them |
| Fast | QSPI_*, LCD_SCK, LCD_MOSI, LCD_CS, LCD_DC | short; U2 next to the QSPI pads (D8) |
| Signal | everything else | 0.15 mm |

The router only knows "signal" (0.10 mm) and "wide" (0.30 mm). Supply nets are routed wide;
`pcb/routing.txt` lists any pad that had to fall back to signal width (none in the last run).

**Stack-up.** F.Cu signal, In1.Cu ground plane, In2.Cu 3.3 V plane, B.Cu signal, ground pours on both outer
layers. The module's rule area keeps all four layers out of the antenna keep-out; `check_keepout_copper`
reads the filled board back and fails on any copper there. The board file carries JLCPCB's JLC04161H-7628
stack-up (`layout.STACKUP`): 35 um outer copper, 0.2104 mm 7628 prepreg, 15.2 um inner copper, 1.065 mm core,
10 um mask, 1.606 mm in all. These numbers are JLCPCB's table as remembered, not re-read: check them on the
order page. The board STEP includes the mask skins, so its envelope is the finished board; `fab.py` exports
the board alone and fails if that envelope is more than 0.02 mm off `pcb.thickness`.

**Battery polarity.** `+` at J3 pin 1 and `-` at pin 2 on the bottom silkscreen (power 11), in the gaps of the
stock connector outline; `layout.check_polarity_marks` asserts each mark is nearer its own pin.

**Panel (D23).** `fab.py` draws the frame from `[panel]`: board outline grown by the 2.5 mm routed gap (the
USB notch kept open), eight 5 mm tabs, one row of 0.5 mm mouse bites per tab, 0.25 mm inside the outline.

**Next steps.** `make pcb-fab` on the routed board (not run yet), then the review points under
[Routing](#routing) and [What a person still has to look at](#what-a-person-still-has-to-look-at).

## Routing

Nothing here was built. The numbers come from real runs of `make pcb-place` and `make pcb-check` on
2026-11-14; a clean DRC says the copper meets the rules, not that the board works.

### Why 36 pads stayed unrouted at commit 2d364fd

Diagnosis made on 2026-11-14 with the router of that commit on the same obstacles, outside KiCad (the placed
board's pads, holes and rule areas dumped once from pcbnew; the run reproduced the commit's 1,137 tracks, 176
vias and 36 unrouted pads exactly). For each unrouted pad a search was run on the finished board that may cross
other nets' copper at a price (`Router.reach`); the nets it had to cross are the ones that walled the pad in.

| Unrouted pads | Copper a crossing search had to cross | Cause |
|---|---|---|
| USB_DP U6.3 | none: a free way existed on the finished board | Search limit. VBUS (0.30 mm) was routed between the pair's first and second half and closed the short way round U6; the 1,000,000-node search gave up on the long way, and a failed search was final. |
| BAT U3.2, U3.3 | USB_DP | Order. The USB pair, routed on the empty board, ran past the charger's BAT pins and closed them in. |
| QSPI_CSN, QSPI_SCK, QSPI_IO0 to IO3 (U2 pins 1, 2, 3, 5, 6, 7) | VSYS, VBUS_SYS, LCD bus, ROW0 to ROW2, COL0, COL4, ENC_R_B, plane fan-outs | Escape and order. The flash pins had no escape stage; the 0.30 mm supply nets and the key matrix (head start in `pcb/gen/route_order.txt`) crossed the control column first and boxed the flash in. |
| CHG_N (U3.9, TP7), PGOOD_N U3.7, CHG_TS U3.1, LDO_EN U4.3 | VSYS, VBUS_SYS, BAT, USB pair, LCD_CS, LCD_SCK, ROW0, ROW1 | Order. The charger's and the LDO's signal pins sit between supply pins; the supply rings went first and these long nets came last. |
| I2C_SDA, I2C_SCL (U5, R8, R9, TP9, TP10), GAUGE_ALRT_N U5.5 | BAT, VSYS, VBUS_SYS, ROW1, ROW3, BL_PWM, 3.3 V and ground fan-outs | Order. The gauge's pins were walled in by the supply tracks and the fan-out vias before the signals came. |
| LCD_RESET J2.7, LCD_TE TP11, BL_K Q1.3, BL_PWM R2.1 | VBUS_SYS, VSYS, BL_A, LCD_CS, LCD_SCK, ROW0 to ROW2 | Order. The supply nets passed under J2 and the backlight parts first. |
| SWDIO, SWCLK, RESET_N (J4, SW17) | COL1 to COL4, ROW2, ENC_R_B | Order. The key matrix head start boxed J4 in at the front edge. |
| ENC_R_A, ENC_L_A, ENC_L_B (encoder pins and filter pads) | ENC_R_B, COL2, COL4, CC1, USB_DN, LCD_DC, QSPI_CSN, QSPI_IO1 | Order. Routed last; the encoder pin rows sit by the USB-C shell, and A and B cross at the pin row (each A filter pad sits in front of the B pin). |

Behind all of it: one greedy pass in a fixed order and no rip-up, so the first net to take a corridor kept it.
The module escapes only had to leave a 10.8 mm square round the module centre, which takes in none of the left
pad column, and ended in plain track ends that later copper sealed. Two more DRC items were not routing at all:
J2's and J3's two solder tabs each share one open-pin net in KiCad ("MP"), and DRC wants each pair joined.

### What changed

Placement did not move: no `board.toml` position, no part in `layout.py`. All of it is in the router.

1. **Base.** The uncommitted work saved on branch `wip-route-1` (router rework) was taken as the start and
   re-run: rip-up and reroute by branch with history costs (`Router.reach`, `rip_up_crossings`, `_Plan.repair`),
   a second search guided by a coarse map, short hops on In2.Cu, pin escapes to vias for U3, U4, U5 and J2,
   and `prune_dangling`. Run alone outside KiCad, it left 7 pads unrouted and the USB pair 5.8 mm apart.
   Branch `wip-route-2` (placement moves, D41 and D42) was read but not used: this strategy keeps the placement.
2. **Module escapes.** A pad on the outer ring of the BMD-340's pad field gets a track to a via just outside
   the field; a deeper pad gets a via in the empty middle under the module (`route._empty_middle`,
   `Router.escape_to_via_inside`). Innermost first, up to `MODULE_ESCAPE_ROUNDS` orders, keeping the order that
   leaves the fewest pads walled in; no escape longer than 3 mm. Plain track ends were the main failure: the
   copper laid later sealed them, while a via can be reached on any layer.
3. **More pin escapes.** The flash (U2) and the backlight FET (Q1) join `ESCAPE_PARTS`.
4. **Inner layers.** Signals may also hop on In1.Cu (four times the cost of an outer step; In2.Cu three
   times). Both planes stay clear of tracks for 0.9 mm round the USB pair and the crystal; the supply nets
   keep off both inner layers (`route.check_sensitive_lengths` fails on a supply track there).
5. **Plane islands.** After routing, every 3.3 V via must sit in the main area of the In2.Cu plane
   (`Router.plane_area`); a via cut off by inner tracks and vias gets a new fan-out, and the signals that cut it
   off are routed again off In2.Cu (`_Plan.plane_islands`). The first routed board had one 0.6 mm2 3.3 V island.
6. **USB lengths.** When D+ and D- differ by more than 2 mm, the shorter one gets a meander on its longest
   straight track while the board round it is still empty (`Router.lengthen`).
7. **Rip-up fixes.** A net ripped up whole keeps its escapes, and its next pad starts the tree again; before,
   ripping a net threw its escape away for good. Escapes are keyed by pad name and place, since two pads can
   share a name (J2 and J3 "MP").
8. **Solder tabs.** An open-pin net that several pads share is routed under KiCad's own name
   (`route._router_net`).

The repair stage (rip-up and reroute) did not have to run in the final routing: the stages above connect every
pad in the first pass. A second rip-up scheme that let every crossing push its victims (negotiated
congestion without undo) was tried on the saved board state and diverged from 4 to about 100 unjoined pads; it
was dropped. Putting the three last failing nets first in `route_order.txt` was tried too and left 4 or 5 pads.

### Result

`make pcb-place` exit 0 and `make pcb-check` exit 0 on 2026-11-14:

| | Commit 2d364fd | Now |
|---|---|---|
| Unrouted pads | 36 on 25 nets | 0 |
| Tracks, vias, length | 1,137, 176, 2,267 mm | 1,980, 280, 3,303 mm |
| DRC errors, unconnected, parity | 0, 39, 0 | 0, 0, 0 |
| DRC warnings | 25 (14 not accepted) | 11, all accepted |
| USB D+, D- | 56.21 mm, 53.97 mm | 60.58 mm, 60.52 mm |
| Track on In1.Cu, In2.Cu | none, none | 89 mm, 119 mm |
| Plane fills | | In2.Cu one piece; In1.Cu one 8.4 mm2 island under the module, joined through vias |

The same code run outside KiCad on the dumped obstacles gave the same 1,980 tracks, 280 vias and 3,303 mm, and
lost no pad at any stage, so the rip-up stage had nothing to do. RF keep-out: no copper on any layer. Ground
vias: 5 in U3's pad and the 8-via fence, each in the ground fill.

Signals on the inner layers (mm): In1.Cu CHG_N 11.3, ENC_L_A 15.4, ENC_L_B 3.3, ENC_R_A 7.1, LCD_DC 11.1,
QSPI_IO0 9.5, QSPI_IO2 24.0, SWCLK 7.1; In2.Cu BL_A 2.6, BL_PWM 3.4, ENC_L_B 2.0, ENC_R_B 8.6, I2C_SCL 17.8,
I2C_SDA 26.0, LDO_EN 10.9, PGOOD_N 7.9, QSPI_CSN 2.7, QSPI_IO1 3.2, QSPI_IO3 11.4, RESET_N 6.7, SWCLK 5.0,
SWDIO 6.8, J2's solder tab link 3.8.

Placement did not move, so nothing changes for the case.
