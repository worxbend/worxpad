# PCBWay CNC order: the machined case parts (fallback)

PCBWay machines the same four parts from the same files as JLCCNC. Nothing is generated into this folder:
upload the STEP and drawing files of [`../jlccnc/`](../jlccnc/ORDER_NOTES.md) (case revision **A**) and use
that page's remarks and prepared answers. This page lists only what differs. Order from one shop, not both:
the parts must fit each other and share one anodising batch.

Not checked for this revision: PCBWay's current design rules, form options and prices. The record read on
2026-11-13 says PCBWay takes STEP, IGES or SLDPRT, refuses STL for CNC, and that "3D file and options take
priority over your technical drawing" (enclosure 4.1). That last point matters: write the threads and the bare
G faces into the form and the remark, not only into the drawing.

The same blockers apply as on the JLCCNC page: the owner's confirmation of the G1 and G2 bottoming tap (D6), the
D37 plug test and the fit check against the PCB STEP.

## Files

| Upload | Files (in `../jlccnc/`) | Qty per unit |
|---|---|---|
| Part 1 | `worxpad_top_shell.step` + `.pdf` | 1 |
| Part 2 | `worxpad_bottom_shell.step` + `.pdf`, laser artwork `worxpad_bottom_shell_engraving_underside.dxf` | 1 |
| Part 3 | `worxpad_rf_insert.step` + `.pdf` | 1 |
| Part 4 | `worxpad_knob.step` + `.pdf` | **2** |

Attach the PDF as the technical drawing of each part. `hole_table.csv` answers questions about hole positions.

## Form settings

| Option | Value | Why |
|---|---|---|
| Service | CNC machining: 3-axis milling for parts 1 to 3, turning for part 4 | |
| Material | Aluminium 6061-T6 (parts 1, 2, 4); POM black (part 3) | same as JLCCNC |
| Surface finish | Bead blast + anodized colour, black, one batch for parts 1, 2 and 4; part 3 as machined | PCBWay warns that colour may vary between batches |
| Threads and tapped holes | Top shell 4 (M2, right-hand, blind); bottom shell 4 (M1.6, right-hand, blind); knob 1 (M2); insert none | |
| Tolerance | ISO 2768-m, tighter where the drawing notes say FIT or FIT-CRITICAL; PCBWay's own default is ISO 2768-1 and +/-0.125 mm | |
| Tightest tolerance | Switch openings 14.00 +0.05/-0 after anodising; plate lip 1.15 +/-0.05; K post tops +0/-0.05 | |
| Roughness | as bead blasted | |
| Technical drawing | Yes, the PDF of each part | |
| Quantity | 1 set first, then 5 | |

## What the model assumes about the shop

The model follows JLCCNC's published design guideline. Put these in the remark and wait for the engineer's
answer before paying:

```
Please confirm before production:
1. Internal corners are modelled at R = depth/10 + 0.5 or more (R1.5 in the key well and cavities, R2.0 in the
   10.95 mm battery pocket, T-bones dia. 2.1 in the display pocket). Machine them as modelled, not enlarged.
2. Blind threads, all right-hand: top shell C1, C2 M2 drill 1.6 x 5.80 / full thread 4.80; G1, G2 M2 drill 1.6 x
   3.50 / full thread 3.00 with a bottoming tap (chamfer 0.5 or less). Bottom shell K1-K4 M1.6 drill 1.25 x 5.60 / full thread 4.80. Knob: one M2 to the bore.
3. Thinnest walls: 0.60 mm USB-C skin (bottom shell), 0.80 mm display web and display-to-RF wall (top shell).
4. G1 and G2 post end faces BARE after anodising (case ground). Threads masked or re-tapped.
5. The shells and knobs must fit together and be anodised in one batch, one colour. Dimensions apply after
   finishing. Rack marks on inner cavity faces only.
6. RF insert: black POM, no paint or metal, length 29.90 +0/-0.10 into a 30.00 +0.10/0 slot.
```

Then paste the part remarks from [`../jlccnc/ORDER_NOTES.md`](../jlccnc/ORDER_NOTES.md). Where those say
"your 0.8 recommendation", they mean JLCCNC's rule quoted above.

## Hardware

Screws, set screws and feet: [`../hardware.csv`](../hardware.csv).
