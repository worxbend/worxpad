# JLCCNC order: the machined case parts

This folder is the CNC order for worxpad, case revision **A**: two aluminium shells, one POM insert and two
aluminium knobs per unit. Every file except this page is copied or merged by `tools/order_package.py`
(`make order`) from what `cad/build.py` writes into `cad/exports/`. Change the model, never these files. To
order the same files at PCBWay instead, see [`../pcbway/`](../pcbway/ORDER_NOTES.md). Screws and feet are in
[`../hardware.csv`](../hardware.csv). The guide for the whole case order is
[docs/ordering-case.md](../../../docs/ordering-case.md).

> **Not ready to order.** Nothing has been milled. Three things block this order today; the order index
> [`production/README.md`](../../../production/README.md) lists the files that are still missing.
>
> 1. The G1 and G2 threads now use a proposed bottoming tap: 3.00 mm full thread, 0.50 mm unthreaded run,
>    drill 1.6 x 3.50. The model's thread checks pass with it, but the owner has not yet recorded it in D6,
>    and the shop must confirm a bottoming tap with a chamfer of 0.5 mm or less. See the open items in
>    [cad/README.md](../../README.md#open-items).
> 2. The USB-C plug test of [D37](../../../docs/decisions.md#d37-usb-c-recess-kept-at-025-mm-pending-a-plug-test)
>    has not been done.
> 3. The case has only been checked against the PCB drawn from `board.toml`. The fit check against the PCB
>    STEP runs once the finished board is exported.

## Files: one upload per part

JLCCNC wants one part per STEP file and a 2D drawing with the **same file name** next to it. The STEP governs
the geometry; the drawing governs threads, tolerances and finish. Each drawing is given as a PDF and as a DXF
of the same plan views, because JLCCNC states DWG or DXF as its 2D format and has accepted PDF from other
customers (enclosure 4.1).

| Upload | STEP + drawing | Qty per unit | Size (mm) | Threads |
|---|---|---|---|---|
| Part 1 | `worxpad_top_shell` (`.step`, `.pdf`, `.dxf`) | 1 | 128.40 x 85.20 x 13.45 | 4 x M2 (C1, C2, G1, G2) |
| Part 2 | `worxpad_bottom_shell` (`.step`, `.pdf`, `.dxf`), plus `worxpad_bottom_shell_engraving_underside.dxf` | 1 | 128.40 x 85.20 x 15.60 | 4 x M1.6 (K1 to K4) |
| Part 3 | `worxpad_rf_insert` (`.step`, `.pdf`, `.dxf`) | 1 | 3.45 x 31.90 x 6.65 over the keys; bar 29.90 | none |
| Part 4 | `worxpad_knob` (`.step`, `.pdf`, `.dxf`) | **2** | dia. 10.50 x 9.10 | 1 x M2 (S1, set screw) |

All sizes are read off the drawings. `hole_table.csv` lists every tapped and countersunk hole: for the shells in
the drawings' coordinates (datum A, the rear-left outer corner, X to the right, Y to the front), for the knob's S1
the mouth from the knob axis; keep it for questions. Do not upload `cad/exports/assembly.step`: JLCCNC cannot
quote an assembly.

Quantities: order **one set first** (the drawings say "check every fit on the first article before the batch"),
then four more. If you order all five at once, you accept that a fit problem costs five sets.

## Form settings

| Option | Shells (parts 1, 2) | RF insert (part 3) | Knob (part 4) | Why |
|---|---|---|---|---|
| Process | CNC milling, 3-axis | CNC milling | CNC turning (the set-screw hole is a side operation) | enclosure 5: two setups per shell, no undercut |
| Material | Aluminium 6061-T6 | **POM (Delrin), black** | Aluminium 6061-T6 | enclosure 4.3; POM is on JLCCNC's plastic list (7.2) |
| Surface finish | Anodising **with** bead blasting, black, Type II | As machined. No paint, no plating, nothing metallic | Same as the shells | enclosure 6.2; the insert is the radio window (mcu-radio A9) |
| Appearance standard | **Strict** | Standard | **Strict** | Strict promises no visible colour variation inside a batch; the knobs must match the shells |
| Threads | Yes: top 4 x M2x0.4-6H; bottom 4 x M1.6x0.35-6H; all right-hand, all blind | No | Yes: 1 x M2x0.4-6H, through the wall to the bore | enclosure 6.4, D30, rotary-buttons 6.5 |
| Tolerance | ISO 2768-m; tighter only where the drawing notes say FIT-CRITICAL or FIT | ISO 2768-m, length 29.90 +0/-0.10 (see remark) | ISO 2768-m, bore per remark | the general tolerance is a proposal, not a tested requirement |
| Technical drawing | Yes: the PDF (and DXF) of the same name | Yes: the PDF (and DXF) | Yes: the PDF (and DXF) | |
| Laser marking | Bottom shell only: `worxpad_bottom_shell_engraving_underside.dxf` on the ramp | No | No | enclosure 5: laser on black anodise is cheap |
| Quantity | 1 each for the first article; 5 each for the batch | 1, then 5 | 2, then 10 | |

Add a remark that all parts must fit together and that every anodised part of the order (shells and knobs)
comes from one batch in one colour.

## Remarks (paste for the TOP SHELL)

```
worxpad top shell, revision A. 6061-T6, bead blast then Type II sulphuric anodise, black, appearance Strict.
Threads per the 2D drawing, ALL RIGHT-HAND, all blind, cut from the post end (underside up):
C1, C2: M2x0.4-6H, full thread 4.80, drill 1.6 x 5.80 (118 deg point to 6.28).
G1, G2: M2x0.4-6H, BOTTOMING TAP (chamfer 0.5 or less), full thread 3.00 minimum, drill 1.6 x 3.50
(118 deg point to 3.98).
STEP models every tapped hole at tap-drill size with the drill point.
K1, K2, K3, K4: clearance 1.8 through the plate lip, countersink 3.3 x 90 deg at the plate top (Z -4.0). No thread.
G1 and G2 post END FACES must be BARE metal after anodising (laser-clear or face-mill): they are the case
ground contact. All other faces anodised. Threads below M5 plugged during anodising as usual.
FIT-CRITICAL: 16 switch openings 14.00 +0.05/-0 AFTER anodising (machine 14.03 +/-0.02); plate lip 1.15 +/-0.05.
FIT: split face; lens recess 31.4 square R2.1 x 1.15 deep; web 0.80 with a 24.8 window.
Encoder pockets 14.8 square, depth from the split face 5.25 +0.10/-0 (ceiling never below Z +0.25).
Thin walls are intended: display web 0.80, display pocket to RF pocket 0.80, K countersink to switch opening 0.876.
Internal corners are modelled at R = depth/10 + 0.5 or more; a 2.0 mm tool is needed where R1.0 or R1.05 is drawn.
The display pocket has T-bone reliefs dia. 2.1 at its rear corners and R1.0 at the front: machine as modelled.
The RF pocket over the antenna bay runs 1.5 mm into the right wall on purpose; the outer wall stays 2.0 mm.
Cosmetic faces: deck, knob plinth, key well, outer walls. Rack marks on inner cavity faces only.
Dimensions apply after finishing. The parts of this order must fit together.
```

## Remarks (paste for the BOTTOM SHELL)

```
worxpad bottom shell, revision A. 6061-T6, bead blast then Type II sulphuric anodise, black, appearance Strict.
Threads per the 2D drawing, ALL RIGHT-HAND, all blind, cut from the post top (cavity side):
K1, K2, K3, K4: M1.6x0.35-6H, full thread 4.80, drill 1.25 x 5.60 (118 deg point to 5.98).
C1: clearance 2.2 through, countersink 4.3 x 90 deg at Z -12.0. C2: spot-face dia. 4.8 to Z -13.7, clearance 2.2
through, countersink 4.3 x 90 deg at Z -13.7. RESET: dia. 1.5 through to Z -9.5. No thread in C1, C2, RESET.
FIT: split face; K post tops at Z -5.20 +0/-0.05; RF slot Y 38.00 to 68.00 +0.10/0 with dia. 2.00 key reliefs.
Wedge: the rear slope and the 4.89 deg ramp are single planes; foot pockets are square to the ramp.
Battery pocket and wire relief rims: R0.5 minimum as modelled, deburred, no sharp edge (the battery pouch
slides past them during assembly).
USB-C skin 0.60 thick in front of the inner pocket: below your 0.8 recommendation, above the 0.5 minimum.
Please tell us in the DFM review if you cannot hold it.
A 3 mm trench runs along the inner side of the RF slot down to Z -11.70, and the RF bay pocket runs 1.5 mm into
the right wall: both intended, machine as modelled.
Laser mark from worxpad_bottom_shell_engraving_underside.dxf on the ramp (drawn as seen from above, mirrored).
Cosmetic faces: underside, ramp, outer walls. Rack marks on inner cavity faces only.
Dimensions apply after finishing. The parts of this order must fit together.
```

## Remarks (paste for the RF INSERT)

```
worxpad RF window insert, revision A. Black POM (Delrin), as machined. No paint, no plating, no metal of any kind:
it is a radio window.
Bar 29.90 x 3.45 x 6.65 with a dia. 1.90 half-round key on each end, per STEP. Length 29.90 +0/-0.10: it slides
into a 30.00 +0.10/0 slot in the bottom shell of the same order. Antenna pocket from the inner face, 14.2 long,
leaving a 1.45 outer skin: machine as modelled. Other sizes ISO 2768-m.
Cosmetic face: the outer face (flush with the case wall).
```

The 29.90 +0/-0.10 length is this page's proposal: the record gives 0.10 mm of total play and ISO 2768-m
(+/-0.2 at this length) could make the bar longer than the slot. The drawing carries it as a FIT note, from
`rf_insert_length_tolerance` in `cad/worxpad_case/spec.py`.

## Remarks (paste for the KNOB)

```
worxpad knob, revision A, quantity 2 per set. 6061-T6 turned, bead blast then Type II anodise, black, appearance
Strict, same batch and colour as the shells.
Outside dia. 10.50, height 9.10, top edge R1.25, per STEP. Counterbore dia. 8.40 x 1.20 from the rim.
D-bore dia. 6.05, 4.55 across the flat, to 6.90 above the rim: slip fit on a 6.0 mm D shaft.
S1: one M2x0.4-6H thread square to the flat, toward the rear, centre 3.00 above the rim, through the wall
into the bore (drill 1.6 through a 3.73 wall).
Mask the thread during anodising. Cosmetic: the outside and the top face.
```

## Prepared answers to engineering questions

| Likely question | Answer |
|---|---|
| Thread direction? | All right-hand. |
| Thread depth? | Drawing table and `hole_table.csv`: drill depth (full diameter; the 118 degree point is extra and modelled) and minimum full thread per hole. |
| Can the C threads be shallower? | No. An M2 x 6 ISO 7046-1 countersunk screw engages 3.95 mm and its tip stops 0.40 mm before the last full thread (computed for a 4.0 head; the 3.8 ISO head sits about 0.1 deeper, being re-checked). |
| The G threads are short (3.00 mm, bottoming tap). | Intended: the G posts end at the PCB top, and the screw is an M2 x 4 pan head. A plug tap leaves too little thread; a deeper drill leaves under 2.0 mm of metal past the point. Please confirm you can cut 3.00 mm of full thread in a 3.50 mm drill with a bottoming tap. The owner has still to confirm this choice (D6). |
| K threads are M1.6, small. | Intended (D30): an M1.6 x 5 ISO 7046-1 countersunk screw engages 3.80 to 4.25 mm; 4.88 mm or more of metal stays beyond the drill point. |
| Why must the G1 and G2 post faces be bare? | They press on a plated ground ring on the PCB and ground the top shell. Anodise insulates. |
| Thin walls under 0.8 mm? | Only the USB-C skin of the bottom shell (0.60). Everything else is 0.80 or more. |
| Sharp internal corners? | None. Every concave corner is at or above R = depth/10 + 0.5, checked on the model (0 faults on 26 arcs on the top shell). The display pocket uses T-bones, by our choice. |
| Side operations? | None on the shells: the USB-C, slide-switch and RF openings are notches cut from the split face. The knob's set-screw hole is a side operation. |
| Which faces may carry rack marks? | Inner cavity faces only. |
| Tolerances not given? | ISO 2768-m. The STEP is the reference geometry. FIT and FIT-CRITICAL values are in the drawing notes and apply after finishing. |
| Text or engraving? | Only the laser mark on the bottom shell ramp. |
