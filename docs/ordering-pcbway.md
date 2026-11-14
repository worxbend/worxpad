# Ordering the assembled board from PCBWay (fallback)

PCBWay is the fallback if JLCPCB cannot build the board, for example when the module or the encoders are out
of stock there. PCBWay buys the parts from distributors (turnkey), so it gets its own BOM with manufacturer
part numbers and KiCad's own centroid file. Never send it the JLCPCB `cpl.csv`: that file has JLCPCB's rotation
table and body centres in it. The JLCPCB page is [ordering.md](ordering.md); read it first, because the board
options and the gates are the same.

> **Nobody has placed this order, and the board cannot be ordered yet** (routed on 2026-11-14, order files written,
> gates open; see [ordering.md](ordering.md)). This page follows the files `make pcb-fab` wrote. PCBWay's
> current form, rules and prices were not checked.

## What you upload

Written by `pcb/gen/fab.py` into pcb/production/pcbway/ once the board is finished:

| PCBWay field | File | Contents |
|---|---|---|
| Gerber file | worxpad-panel-gerbers.zip | the same panel as the JLCPCB order, about 135.65 x 95.30 mm; byte-identical, which `tools/order_package.py` checks |
| BOM | bom-mpn.csv | 30 lines in the draft: designators, quantity, manufacturer, manufacturer part number, description, package, LCSC number for reference |
| Centroid | centroid.csv | 61 placements in the draft: KiCad footprint origin, top-view X and Y (Y up), KiCad's own angle |

`tools/order_package.py` checks that bom-mpn.csv and centroid.csv name the same designators, and that they name
the same designators as the JLCPCB files.

## Coordinates and rotations

- **Mid X, Mid Y** is each footprint's KiCad origin, seen from the top, Y up. For the project footprints (U1,
  J1, J2, ENC1, ENC2) the origin is the one `pcb/gen/footprints.py` draws, not necessarily the body centre.
- **Rotation** is KiCad's angle, counter-clockwise, with KiCad's library footprint as 0 degrees. No correction
  table is applied.
- **Bottom side:** X and Y are seen from the top, not negated.

Ask PCBWay to send the placement of both sides for confirmation, and check it against the table in
[ordering.md, step 6](ordering.md#6-check-the-placement-preview): the same parts, the same pin 1 marks.

## Step by step

1. Open PCBWay's PCB assembly quote (turnkey) and upload the Gerber zip.
2. Board options as on the JLCPCB page: 4 layers, FR-4, 1.6 mm, ENIG, 1 oz outer and 0.5 oz inner copper,
   tented vias, minimum hole 0.3 mm, minimum track and space 0.10 mm, quantity 5, panel by customer (the frame
   and the tabs are drawn), solder mask colour as you like.
3. Assembly: turnkey, **both sides**, quantity 5 (or 2 for a test run), the two encoders as through-hole parts.
4. Upload bom-mpn.csv and centroid.csv.
5. Paste this remark:

```
One board in a customer panel: frame of four 5 mm rails, 2.5 mm routed gap, eight mouse-bite tabs, no V-cut.
Please route the right board edge (next to the U1 BMD-340 antenna) to +/-0.1 mm if possible and tell us if not:
the antenna end is 0.2 mm inside that edge and must not overhang. J1 (USB-C) and SW18 (slide switch) overhang
their board tongues into the routed gap on purpose; their pads end at the board edge.
Centroid: KiCad origin and angle, X and Y seen from the top for both sides. Please send the placement of both
sides for confirmation before production.
Lines without an MPN: please source a part to the data sheet of the LCSC number given, or ask us.
The 16 hot-swap sockets (SW1-SW16 footprints) and C13-C16 are NOT fitted.
```

6. Answer the parts review. PCBWay may propose alternatives; accept only the passives (next section).

## Substitutions

Four lines of the draft BOM have no manufacturer part number in the research records: R1 (15 Ohm 1 %, LCSC
C25083), C5 (1 uF 0402, C52923), C1 and C2 (20 pF C0G 0402, C1554), R3 and R4 (5.1 kOhm 1 %, C25905). Any part
of the same value, tolerance, package, voltage and dielectric is fine; the crystal capacitors must be C0G. No
substitute is acceptable for U1 to U6, J1, J2, J3, SW18, SW19, SW20, ENC1, ENC2, Y1 or F1 without asking the
design owner.

## Not on this order

The hot-swap sockets, the display, the cell and the case: [parts.md](parts.md), [bom-hand.csv](bom-hand.csv),
[ordering-case.md](ordering-case.md). PCBWay sourcing of the Kailh CPG135001S30 socket was not checked
(keys 11 item 5).
