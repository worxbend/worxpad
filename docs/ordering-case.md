# Ordering the case

The case is four orders: the machined parts at [JLCCNC](https://jlccnc.com) (PCBWay CNC as the fallback), the
resin keycaps and button caps at [JLC3DP](https://jlc3dp.com), the lens at a laser-cutting shop, and screws and
feet from any hardware shop. The FDM prototype is printed at home: [printing.md](printing.md).

> **Nothing has been milled, printed or cut, and the CNC order is not ready.** On 2026-11-14 the case model
> passes 177 of its 177 limit checks, but G1 and G2 pass only with a proposed bottoming tap that needs a
> decision by the owner before any shell is ordered ([cad/README.md](../cad/README.md#open-items)). The
> order index [production/README.md](../production/README.md) lists every file.

## Contents

- [Order in this sequence](#order-in-this-sequence)
- [Machined parts at JLCCNC](#machined-parts-at-jlccnc)
- [Machined parts at PCBWay](#machined-parts-at-pcbway)
- [Resin parts at JLC3DP](#resin-parts-at-jlc3dp)
- [Lens](#lens)
- [Hardware](#hardware)
- [Cost](#cost)
- [When the parts arrive](#when-the-parts-arrive)

## Order in this sequence

1. **Coupons first.** Print the FDM coupons ([printing.md](printing.md#coupons-first)) and order the resin stem
   coupon with the first keycaps. The README lists the coupons that gate the CNC order: switch retention in the
   1.15 mm anodised lip, keycap stem fit, display flex fold, encoder in its plinth pocket, USB-C skin.
2. **USB-C plug test** ([D37](decisions.md#d37-usb-c-recess-kept-at-025-mm-pending-a-plug-test)): plugs with
   large overmoulds against the 0.25 mm recess, on the FDM print.
3. **The PCB is final.** The case fit check against the PCB STEP runs once pcb/production/worxpad-pcb.step
   exists; until then the case is checked against the PCB drawn from `board.toml`.
4. **One CNC set**, the first article. Fit it with a real board before the other four.
5. The batch: four more sets, in one anodising batch with the first if JLCCNC can match it; otherwise all five
   again.

## Machined parts at JLCCNC

Files and remarks: [cad/production/jlccnc/ORDER_NOTES.md](../cad/production/jlccnc/ORDER_NOTES.md). That page
has one paste-ready remark per part and a table of prepared answers. In short:

| Part | File in cad/production/jlccnc/ | Qty per unit | Material and finish |
|---|---|---|---|
| Top shell | `cad/production/jlccnc/worxpad_top_shell.step`, `.pdf`, `.dxf` | 1 | 6061-T6, bead blast, Type II black anodise, Strict |
| Bottom shell | `cad/production/jlccnc/worxpad_bottom_shell.step`, `.pdf`, `.dxf`, engraving DXF | 1 | same, laser mark on the ramp |
| RF window insert | `cad/production/jlccnc/worxpad_rf_insert.step`, `worxpad_rf_insert.pdf` | 1 | black POM, as machined |
| Knob | `cad/production/jlccnc/worxpad_knob.step`, `worxpad_knob.pdf` | 2 | 6061-T6 turned, same finish and batch as the shells |

### Form settings, field by field

| Field | Value | Why |
|---|---|---|
| Upload | one STEP per part, a drawing of the same name | JLCCNC cannot quote an assembly; the drawing carries threads and tolerances |
| Process | CNC milling, 3-axis (shells, insert); CNC turning (knob) | no undercut (enclosure 5). Top shell: two setups. Bottom shell: three; the third holds the 4.89 degree ramp level for the foot pockets, which are square to the ramp ([D40](decisions.md#d40-third-setup-for-the-bottom-shell-foot-pockets)). Expect it in the quote |
| Material | Aluminium 6061-T6; POM black for the insert | 7075 costs more and anodises less evenly; stiffness, not strength, limits this case (enclosure 4.3) |
| Surface finish | anodising with bead blasting, black | plain anodising has no blasting; the insert stays bare plastic (radio window) |
| Anodise type | Type II sulphuric | the switch openings are compensated for Type II growth only; hardcoat (Type III) grows 25 to 100 um (enclosure 5) |
| Appearance standard | **Strict** | no visible colour variation inside a batch, racking on non-cosmetic faces |
| Threads | **Yes.** Top shell: C1, C2, G1, G2, M2x0.4-6H. Bottom shell: K1 to K4, M1.6x0.35-6H. Knob: one M2x0.4-6H. All right-hand, all blind | drawing table and `cad/production/jlccnc/hole_table.csv` |
| Thread masking | threads below M5 are plugged during anodising (JLCCNC's own rule); say so anyway | a bare thread does not ground anything by itself (enclosure 5) |
| Bare faces | **G1 and G2 post end faces bare** after anodising (laser-clear or face-mill) | they ground the top shell through the PCB's plated G holes (D6) |
| Tolerance class | ISO 2768-m, with FIT and FIT-CRITICAL values on the drawings | the general class is a proposal; only the fits are tight |
| FIT-CRITICAL | switch openings 14.00 +0.05/-0 after anodising (machine 14.03 +/-0.02); plate lip 1.15 +/-0.05 | switch retention (keys) |
| FIT | K post tops Z -5.20 +0/-0.05; RF slot 38.00 to 68.00 +0.10/0; lens recess 31.4 square R2.1 x 1.15 | PCB clamp, insert fit, lens fit |
| Cosmetic sides | top shell: deck, plinth, key well, outer walls; bottom shell: underside, ramp, outer walls; knob: outside and top | |
| Racking | inner cavity faces only | |
| Laser marking | bottom shell only, from the engraving DXF | |
| Quantity | 1 set first, then 5 | |
| Remark | the part remark from ORDER_NOTES.md, plus: the parts must fit together; one anodising batch and colour for shells and knobs | |

Thin features the DFM review may ask about, all intended and named in the remarks: the 0.60 mm USB-C skin
of the bottom shell (above the 0.5 mm minimum, under the 0.8 mm recommendation), the 0.80 mm display web and
display-to-RF wall, the RF bay pockets that run 1.5 mm into the right wall, and the trench along the RF slot.

## Machined parts at PCBWay

Same files, same parts: [cad/production/pcbway/ORDER_NOTES.md](../cad/production/pcbway/ORDER_NOTES.md) lists
the differences and a "please confirm" block. PCBWay says its 3D file and form options take priority over the
drawing, so put the threads and the bare G faces in the form and the remark too. Order from one shop only, so
the shells and knobs share one anodising batch.

## Resin parts at JLC3DP

| Part | File | Qty per unit | 1 unit | 5 units |
|---|---|---|---|---|
| Keycap | `cad/exports/resin/keycap.stl` | 16 | 16 | 96 (80 plus 16 spare) |
| Button cap | `cad/exports/resin/button_cap.stl` | 2 | 2 | 10 |
| Stem fit coupon | `cad/exports/resin/coupon_stem.stl` | - | 1 | 1 |

| Field | Value | Why |
|---|---|---|
| Technology | SLA resin | the keycap's dish and cross stem need resin detail (keys 6.5) |
| Material | JLC Black Resin | keys 6.5, rotary-buttons 6.6 |
| Finish | default (sanded), no paint | |
| Quantity | as above; the coupon in the first order | |
| Remark | "Cross stem: please do not fill or sand the stem slot. Thin walls (0.44 mm at the stem cross slot) are intended." | the keycap's thinnest wall is 0.44 mm against the 0.8 mm JLC3DP recommends; keys 6.5 accepts it and leaves it to the coupon |

Order the coupon and a few caps first if the stem fit is unknown; the batch follows the coupon result.

## Lens

1.0 mm clear cast PMMA, 31.2 mm square with R2.0 corners, the underside painted black with a 24.4 mm window
(display 6.4). Files: `cad/exports/drawings/lens.dxf` (cut outline) and `cad/exports/drawings/lens_mask.dxf`
(mask and window). No shop has been chosen. JLCCNC also machines PMMA with UV printing, but its 1.5 mm
minimum plastic wall makes that a fallback only (enclosure 6.2). Ask the shop for cast (not extruded) PMMA,
the paint on the underside, and the window clear.

## Hardware

Per unit, from [cad/production/hardware.csv](../cad/production/hardware.csv): 4 x M1.6x5 DIN 7991 (K), 2 x M2x6
DIN 7991 (C), 2 x M2x4 ISO 7045 pan head with a conductive finish (G), 2 x M2x3 ISO 4029 cup-point set screws
(knobs), 4 x 3M Bumpon SJ5076 feet. Quantities for 1 and 5 units and the links: [bom-hand.csv](bom-hand.csv).
None of these is in the JLCPCB assembly library.

## Cost

The case block of [parts.md, Cost](parts.md#cost). **Guesses scaled from community orders; no live JLCCNC or
PCBWay quote was made.** A JLCCNC quote needs an account and the STEP files, which now exist. The guesses assume
two setups per shell (enclosure 5 cost levers); the bottom shell's third setup (D40) is not in them.

| Item | 1 set (USD) | 5 sets, total (USD) |
|---|---|---|
| Top and bottom shell, 6061, bead blast, black anodise | 140 to 240 | 450 to 800 |
| RF insert, POM | 5 to 10 | 10 to 25 |
| Lens, laser-cut PMMA, painted | 5 to 15 | 15 to 40 |
| Knobs, 6061 turned, anodised, 2 per set | 15 to 30 | 40 to 80 |
| Button caps, resin, 2 per set | 2 to 5 | 5 to 10 |
| Feet SJ5076, pack of 56 | 7.19 | 7.19 |
| Screws and set screws, packs | 8 to 12 | 8 to 12 |
| Shipping, one parcel | 20 to 40 | 30 to 60 |
| **Total** | **about 200 to 350** | **about 560 to 1,030** |

Keycaps are counted with the hand-fitted parts in [parts.md](parts.md#cost).

## When the parts arrive

1. Measure the 16 switch openings with a pin gauge or a switch: 14.00 to 14.05 mm.
2. Check that the G1 and G2 post faces are bare: a multimeter reads under 1 Ohm from the post face to bare
   metal elsewhere, and open on an anodised face.
3. Check the RF insert in its slot: it drops in from above and sits flush with the outer wall.
4. Fit the first article with a real board before you order or accept the rest ([assembly.md](assembly.md)).
