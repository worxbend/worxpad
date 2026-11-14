# Ordering the assembled board from JLCPCB

How to order five assembled worxpad boards from [JLCPCB](https://jlcpcb.com): JLCPCB makes the 4-layer board,
buys the parts, places both faces (D9), solders the two through-hole encoders and ships the boards in their
panel. The hot-swap sockets, the display, the cell and the case are separate orders: see
[parts.md](parts.md) and [ordering-case.md](ordering-case.md). The PCBWay fallback is
[ordering-pcbway.md](ordering-pcbway.md).

> **Nobody has placed this order, and the board cannot be ordered yet.** On 2026-11-14 the board is placed and
> routed with a clean DRC ([pcb/README.md](../pcb/README.md#routing)), and `make pcb-fab` wrote the order files
> from it: 61 placements (56 on the bottom), 30 BOM lines, panel 135.65 x 95.30 mm. The gates in the
> [README](../README.md#before-you-order) are still open. Re-read the
> generated README in pcb/production/jlcpcb/ when the real package exists; where it and this page disagree,
> the generated README wins, because it is written from the board.

Form fields are named as the JLCPCB form showed them in the siblings' notes (worxboard, 2026-11-04). JLCPCB
renames options now and then; pick the closest match. The values are what matters.

## Contents

- [What you upload](#what-you-upload)
- [Before you order](#before-you-order)
- [1. Upload the Gerbers](#1-upload-the-gerbers)
- [2. PCB options](#2-pcb-options)
- [3. PCB assembly options](#3-pcb-assembly-options)
- [4. Upload the BOM and the CPL](#4-upload-the-bom-and-the-cpl)
- [5. Check the parts list](#5-check-the-parts-list)
- [6. Check the placement preview](#6-check-the-placement-preview)
- [7. Before you pay](#7-before-you-pay)
- [If a part is out of stock](#if-a-part-is-out-of-stock)
- [Cost](#cost)
- [When the boards arrive](#when-the-boards-arrive)

## What you upload

All three files are written by `pcb/gen/fab.py` into pcb/production/jlcpcb/ once the board is finished.
[production/README.md](../production/README.md) lists them with their state.

| JLCPCB field | File | Contents |
|---|---|---|
| Gerber file | worxpad-panel-gerbers.zip | the **panel**: the board in a frame of four 5 mm rails, 2.5 mm routed gap, eight mouse-bite tabs (D23); 4 copper layers, mask, silk, paste, outline, PTH and NPTH drills |
| BOM file | bom.csv | one JLCPCB part number on every line (30 lines in the draft) |
| CPL file | cpl.csv | every machine placement, both faces, with the rotation table of `pcb/gen/fab.py` applied (61 in the draft) |

worxpad-jlcpcb-order.zip holds the same three files. The README next to them repeats the form in short and
holds the remark text. The bare board without the frame is in pcb/fab/; do not upload it here.

## Before you order

1. **Gates.** The [D12](decisions.md#d12-vbus-on-module-pad-66-while-the-rail-is-off) question (VBUS on module
   pad 66 while 3V3 is off) is read in the nRF52840 Product Specification and closed. Until then, do not order.
2. **The package is complete.** `python3 tools/order_package.py` exits 0. It fails when a listed file is
   missing, when bom.csv and cpl.csv name different designators, when the JLCPCB and PCBWay files disagree, or
   when a case check fails.
3. **Stock on the day.** Search each BOM line on the JLCPCB parts page for 5 boards plus attrition. The thin
   lines on 2026-11-13: the BMD-340 module C5456944 (JLCPCB 349), the PEC12R encoders C22385080 (JLCPCB 28 for
   10 needed), the JST PH header C295747 (743) and the BQ24072 charger C140288 (1,216). See
   [If a part is out of stock](#if-a-part-is-out-of-stock).
4. **The hot-swap sockets are not in this order.** JLCPCB cannot buy them (CPG135001S30, discontinued). Buy
   them from a keyboard shop ([bom-hand.csv](bom-hand.csv)) and solder them by hand.
5. Optionally run the Gerbers through JLCDFM first: it shows what JLCPCB's engineers will see.

## 1. Upload the Gerbers

On jlcpcb.com, open the instant quote and upload worxpad-panel-gerbers.zip. JLCPCB should read **4 layers**
and about **135.65 x 95.30 mm** (the panel). If it reads about 120.65 x 80.30 mm, you uploaded the bare board.

In the Gerber viewer, inner layer 1 (In1.Cu) is the ground plane and inner layer 2 (In2.Cu) the 3.3 V plane,
both nearly solid, with short signal tracks on each where the outer layers are full. The right-hand strip of
the board, over the radio module's antenna, has no copper on any layer. Compare with
[the copper pictures](images/pcb/copper-top.svg); they show the routed board of 2026-11-14.

## 2. PCB options

| Option | Value | Why |
|---|---|---|
| Base material | FR-4 | |
| Layers | **4** | F.Cu signal, In1.Cu ground, In2.Cu 3.3 V, B.Cu signal (`board.toml` `[pcb]`) |
| Dimensions | read from the Gerbers, about 135.65 x 95.30 mm | the panel; the board is 120.65 x 80.30 mm |
| PCB qty | **5** | the first batch; JLCPCB's minimum is 5 |
| Product type | Industrial/Consumer electronics | |
| Different design | 1 | one board per panel |
| Delivery format | **Panel by Customer** (1 column x 1 row if asked) | the frame is in the Gerbers (D23) |
| PCB thickness | **1.6 mm** | the case stack-up assumes it: PCB top Z -6.20, bottom Z -7.80 |
| Impedance control / stack-up | No; **JLC04161H-7628**, JLCPCB's default 4-layer 1.6 mm stack | full-speed USB only; no impedance was calculated for this board |
| PCB colour | black if the case matters to you, otherwise any | the board edge shows in the USB-C and slide-switch openings; the colour changes nothing else |
| Silkscreen | the default for the colour | |
| Material type | FR-4 TG135, the default | |
| Surface finish | **ENIG** | flat pads for the 0.5 mm pitch LGA module, the 0.5 mm FPC connector and the 3 x 3 mm QFN charger; HASL is not flat enough |
| Outer copper weight | 1 oz | |
| Inner copper weight | 0.5 oz, the default | the planes carry under 0.5 A |
| Via covering | **Tented** | some vias sit under the module |
| Min via hole size / diameter | 0.3 mm / 0.6 mm (the default option) | every via is 0.3 / 0.6 mm |
| Min track / spacing | 0.09 mm option if the form asks | the design uses 0.10 mm, needed between the module's inner pad rows; JLCPCB's 4-layer limit is 0.09 mm (sibling notes, not re-read) |
| Board outline tolerance | ask for **+/-0.1 mm** in the remark; select the regular +/-0.2 mm if there is no option | the antenna end sits 0.2 mm inside the right edge and must not overhang (D24) |
| Confirm production file | **Yes** | you approve the panel and the edge exceptions before production |
| Mark on PCB | **Remove mark** if the option exists | the siblings disagree whether the option still exists (worxboard says it was dropped in 2026-05) |
| Electrical test | flying probe, the default | |
| Gold fingers, castellated holes, edge plating, press-fit | No | |
| Build time | standard | |

## 3. PCB assembly options

Turn on **PCB Assembly**.

| Option | Value | Why |
|---|---|---|
| PCBA type | **Standard** | Economic places one face only |
| Assembly side | **Both sides** | top: FPC connector J2, buttons SW19 and SW20, encoders ENC1 and ENC2 (through-hole); bottom: everything else (D9) |
| PCBA qty | **5** for the batch, or **2** for a test run first | JLCPCB's minimum is 2; the cost section gives both |
| Edge rails / fiducials | **Added by Customer** | the frame has 5 mm rails; three fiducials per face are on the board |
| Tooling holes | **Added by JLCPCB**, on the rails only | the generated README asks for this in the remark |
| Confirm parts placement | **Yes** | an engineer sends the placement for approval; the rotation table is partly reasoned |
| Depanel / remove edge rails | No | break the tabs yourself and sand the nubs flush ([below](#when-the-boards-arrive)) |
| Through-hole parts | let JLCPCB solder ENC1 and ENC2 | about USD 4 for the batch (cost table); they are on the BOM |
| X-ray | accept it if offered or charged | the LGA module and the QFN charger have hidden joints |
| Other advanced options | defaults | |

**Remark.** Paste the remark from the generated README of pcb/production/jlcpcb/ as it is. In the draft it
reads:

```
Customer panel: one board in a frame of four 5 mm rails, 2.5 mm routed gap, eight mouse-bite tabs, no V-cut.
Please keep tooling holes on the rails only. Please route the right board edge (X max of the board, next to
the U1 radio module antenna) to +/-0.1 mm if possible and tell us if not: U1's antenna end is 0.2 mm inside
that edge and must not overhang. J1 (USB-C) and SW18 (slide switch) overhang their board tongues into the
routed gap; no tab or rail is in front of them. J1's signal pads and SW18's shield tabs end at the board
edge on purpose. U1 is a u-blox BMD-340 LGA module: please confirm its pad 1 corner in the placement preview.
```

The board has a -0.1 mm copper-to-edge exception for J1 and SW18 only (`pcb/kicad/worxpad.kicad_dru`).
Whether JLCPCB accepts copper at a routed edge there is not confirmed: if the engineer objects, stop and ask
the PCB owner; do not let JLCPCB trim the pads.

## 4. Upload the BOM and the CPL

1. Upload bom.csv as the BOM. Columns: `Comment, Designator, Footprint, LCSC Part #`.
2. Upload cpl.csv as the placement file. Columns: `Designator, Mid X, Mid Y, Layer, Rotation`.
3. JLCPCB lists the designators it found in the BOM and not in the CPL, and the other way round. There must be
   none: `tools/order_package.py` checks the same thing before you upload.

## 5. Check the parts list

Every line must be matched, in stock and confirmed. Extended parts carry a loading fee each; that is
expected. Compare each line with [parts.md](parts.md#machine-placed-jlcpcb-assembly). Do not let the site pick
a replacement on its own: the module, the charger, the gauge, the LDO, the FPC connector, the USB-C
receptacle and the encoders have no drop-in substitute. The 10 nF encoder filter capacitors C13 to C16 are
not on the BOM on purpose (D36). Neither are the 16 hot-swap sockets, the test pads, the holes or the
fiducials.

## 6. Check the placement preview

This step matters most. Bottom-face rows use top-view X and Y and 180 degrees minus the KiCad angle plus the
correction; JLCPCB does not document its bottom-side convention. Only the SOT-23-5, SOT-23-6 and SOIC-8 rows
of the rotation table come from a sibling board that JLCPCB has built; the SOT-23, VQFN/DFN and JST PH rows
are community values. Nobody has seen this board in the preview yet.

Compare the preview with the assembly drawings ([top](images/pcb/assembly-top.svg),
[bottom](images/pcb/assembly-bottom.svg)):

| Part | What must be right |
|---|---|
| U1 (BMD-340, bottom) | Pad 1 corner on the board's pad 1 mark; the antenna end at the right edge, 0.2 mm inside it |
| U2 (W25Q128JV flash, SOIC-8) | Pin 1; the part is turned 90 degrees, pin rows along Y |
| U3 (BQ24072, VQFN-16) | Pin 1 dot; the thermal pad centred |
| U4 (TPS7A02, SOT-23-5) | Pin 1. A SOT-23 turned 180 degrees still fits its pads and is wrong |
| U5 (MAX17048, DFN-8) | Pin 1; the exposed pad centred |
| U6 (USBLC6-2SC6, SOT-23-6) | Pin 1 |
| Q1 (AO3400A), Q2 (AO3401A) | Gate and source on the right pads |
| D1 to D20 (1N4148W) | Cathode bar toward the row net |
| J1 (USB-C) | Mouth at the rear notch, shell legs in their slots |
| J2 (FH34SRJ, top) | Contact 1 toward the right |
| J3 (JST PH, bottom) | Mouth toward the left |
| SW17 (reset), SW18 (slide switch) | SW18's actuator out of the rear edge |
| SW19, SW20 (B3FS, top) | All four legs on their pads |
| ENC1, ENC2 (top, through-hole) | Body inside the outline, pins in their holes |
| Y1 (crystal) | On its two pads, next to U1 |

Ask for a correction in the placement confirmation instead of editing the files. Write down what you changed
and tell the PCB owner: the lasting fix belongs in the rotation table of `pcb/gen/fab.py`; the CSV is
generated.

## 7. Before you pay

1. 4 layers, about 135.65 x 95.30 mm, 1.6 mm, ENIG, Panel by Customer, quantity 5.
2. Standard PCBA, both sides, the quantity you chose.
3. Every BOM line confirmed and in stock.
4. The remark is pasted, including the +/-0.1 mm request for the right edge.
5. You looked at every row of the table in step 6.
6. You accept that this is an untested design: nothing has been built or powered.

## If a part is out of stock

- **Module, encoders, charger, gauge, LDO, FPC connector, USB-C:** no substitute without a design change. Wait,
  use JLCPCB's part pre-order (global sourcing) if offered, or order fewer assembled boards.
- **Passives, diodes, the two MOSFETs:** pick a part with the same value, package, voltage and dielectric (X5R
  or X7R for capacitors, C0G for the 20 pF crystal capacitors) and note the change in [parts.md](parts.md).
- **Encoders:** JLCPCB had 28 on 2026-11-13 with a six-month use-by note. If short, leave ENC1 and ENC2 off the
  order and solder them by hand.

## Cost

From [parts.md, Cost](parts.md#cost). The PCB assembly block for one unit (5 boards, 2 assembled) is about USD
235 to 315; for five units (5 boards, 5 assembled) about USD 320 to 400. **None of these is a quote.** The
frame panel's price was not checked.

## When the boards arrive

1. Break the boards out of the frame at the tabs. Sand the nubs flush with the edge: the board sits 0.30 mm
   from the left case wall, so a nub can stop it seating.
2. Look at U1's antenna end against the right edge under a loupe: it must not overhang. Note the inset of each
   board; the RF test (mcu-radio 7.3.4) uses it.
3. Continue with [assembly.md](assembly.md): bare-board tests before any hand-soldering.
