# Parts and sourcing

Every part of one worxpad, where it comes from and what it cost on the day it was looked up. Stock and prices
were read on 2026-11-13 by the research records ([research/COMPONENTS.md](../research/COMPONENTS.md) section
1); they change daily. Check them again on the order day.

> **Nothing has been ordered.** The machine-placed list below is the draft BOM that `pcb/gen/build.py fab-draft`
> wrote from the unfinished board: 30 lines, 61 placements, 56 on the bottom face and 5 on the top. The real
> BOM is written with the finished board.

Shopping list for 1 and 5 units, with links: [bom-hand.csv](bom-hand.csv). Case hardware per unit:
[cad/production/hardware.csv](../cad/production/hardware.csv).

## Contents

- [Machine-placed (JLCPCB assembly)](#machine-placed-jlcpcb-assembly)
- [Hand-soldered](#hand-soldered)
- [Plugged in or fitted, no solder](#plugged-in-or-fitted-no-solder)
- [Made case parts](#made-case-parts)
- [Case hardware](#case-hardware)
- [Tools](#tools)
- [Substitutions](#substitutions)
- [Cost](#cost)

## Machine-placed (JLCPCB assembly)

Class: **basic** has no loading fee in Economic PCBA; **ext** (extended) has a fee per distinct part. Standard
PCBA (needed for two faces) charges both kinds as in [Cost](#cost).

| Designators | Part | JLCPCB | Class | Stock 2026-11-13 | Face |
|---|---|---|---|---|---|
| U1 | u-blox BMD-340-A-R (nRF52840 module) | C5456944 | ext | JLCPCB 349, LCSC 190 | bottom |
| U2 | Winbond W25Q128JVSIQ, 16 MB QSPI flash | C97521 | basic | 69,913 | bottom |
| U3 | TI BQ24072RGTR charger | C140288 | ext | 1,216 | bottom |
| U4 | TI TPS7A0233PDBVR 3.3 V LDO | C2887324 | ext | 5,309 | bottom |
| U5 | ADI MAX17048G+T10 fuel gauge | C2682616 | ext | 20,372 | bottom |
| U6 | ST USBLC6-2SC6 ESD array | C7519 | ext | 43,069 | bottom |
| Y1 | Epson Q13FC1350000400, 32.768 kHz | C32346 | basic | 419,369 | bottom |
| J1 | HRO TYPE-C-31-M-13C, USB-C | C2848620 | ext | 4,695 | bottom |
| J2 | Hirose FH34SRJ-24S-0.5SH(50), display FPC | C324726 | ext | 12,971 | **top** |
| J3 | JST S2B-PH-SM4-TB, battery | C295747 | ext | 743 | bottom |
| ENC1, ENC2 | Bourns PEC12R-4215F-S0024 encoder, through-hole | C22385080 | ext | 28 | **top** |
| SW17 | XKB TS-1187A-B-A-B, reset | C318884 | basic | 815,200 | bottom |
| SW18 | Shouhan MSK12C02, power slide switch | C431540 | ext | 172,615 | bottom |
| SW19, SW20 | Omron B3FS-1000P, round buttons | C271750 | ext | 67,955 | **top** |
| Q1 | AO3400A, backlight switch | C20917 | basic | 1,025,527 | bottom |
| Q2 | AO3401A, reverse-polarity FET | C15127 | basic | 1,557,883 | bottom |
| F1 | Littelfuse 1206L075THYR PTC | C99563 | ext | 10,807 | bottom |
| TH1 | NTC 10k B3950 0805 | C51597 | ext | 41,619 | bottom |
| D1 to D20 | 1N4148W SOD-123, matrix | C81598 | basic | 3,287,205 | bottom |
| C1, C2 | 20 pF C0G 0402, crystal | C1554 | basic | 1,196,204 | bottom |
| C3, C8, C9 | 10 uF 0603 | C19702 | basic | millions | bottom |
| C4, C6, C12 | 100 nF 0402 | C1525 | basic | millions | bottom |
| C5 | 1 uF 0402, display VDD | C52923 | basic | millions | bottom |
| C7, C10, C11 | 1 uF 50 V 0603 | C15849 | basic | millions | bottom |
| R1 | 15 Ohm 1 % 0402, backlight | C25083 | ext | 68,147 | bottom |
| R2, R5 | 100 kOhm 0402 | C25741 | basic | 8,506,214 | bottom |
| R3, R4 | 5.1 kOhm 1 % 0402, USB CC | C25905 | basic | not stated | bottom |
| R6 | 3.3 kOhm 0402, ILIM | C25890 | basic | millions | bottom |
| R7 | 2.2 kOhm 1 % 0402, ISET | C25879 | basic | millions | bottom |
| R8, R9 | 4.7 kOhm 0402, I2C pull-ups | C25900 | basic | millions | bottom |

Not on the BOM on purpose: the 10 nF encoder filter capacitors C13 to C16 (footprints only, D36), the 16
hot-swap sockets SW1 to SW16 (hand-soldered), the TC2030-NL SWD pad set (copper only), test pads, holes and
fiducials.

## Hand-soldered

| Part | Qty per unit | Buy | Why not machine-placed |
|---|---|---|---|
| Kailh CPG135001S30 Choc hot-swap socket (SW1 to SW16, bottom face) | 16 | splitkb, 50-pack 6.57 in the shop's currency, available | Discontinued: JLCPCB 0 and not purchasable, LCSC 0 (keys 6.7). The footprint has no paste |

## Plugged in or fitted, no solder

| Part | Qty per unit | Buy | Note |
|---|---|---|---|
| Lofree Ghost switch (Kailh PG1353D class, linear, full POM) | 16 | lofree.co, 106-pack 59.00 in the shop's currency | Fallback: Kailh PG1353 set from kailh.net, only if the retention coupon fails |
| DisplayModule DM-TFT13-377p24, 1.3 inch 240 x 240 IPS | 1 | DisplayModule, USD 7.90, 60 available | Flex into J2. Buy two for the first unit, ten for five (display 8) |
| Adafruit 258 LiPo, 1,200 mAh, JST PH | 1 | adafruit.com, USD 9.95 | Bring-up and FDM cell. Measure the lead (19 to 60 mm allowed, D28). Production cell EEMB LP404261-PCM-LD is quotation only |
| Insulating sheet 0.3 mm, polyimide or PET | 1 | any | Over the sockets at the battery pocket (power 5.2) |
| Lens adhesive ring 0.13 mm, black tape frame 0.10 mm, display foam pad 3.0 mm, battery foam 0.2 mm | 1 set | not chosen | Product choice open (display 8) |

## Made case parts

| Part | Material, finish | Vendor (fallback) | Qty per unit | Order page |
|---|---|---|---|---|
| Top shell | 6061-T6, bead blast, black anodise Type II, Strict | JLCCNC (PCBWay CNC) | 1 | [ordering-case.md](ordering-case.md) |
| Bottom shell | same, laser mark | JLCCNC (PCBWay CNC) | 1 | same |
| RF window insert | black POM, as machined | JLCCNC | 1 | same |
| Knob | 6061-T6 turned, black anodise, M2 set screw | JLCCNC | 2 | same |
| Keycap | JLC Black Resin | JLC3DP | 16 | same |
| Button cap | JLC Black Resin | JLC3DP | 2 | same |
| Lens | 1.0 mm cast PMMA, painted underside | laser shop (not chosen) | 1 | same |
| Switch insertion jig, knob fork shim, FDM prototype shells | PETG | own printer | tools | [printing.md](printing.md) |

## Case hardware

| Item | Qty per unit | Spec | Where |
|---|---|---|---|
| K screw | 4 | M1.6x5 DIN 7991, black (D30) | plate lip into the bottom-shell posts |
| C screw | 2 | M2x6 DIN 7991, black | underside into the top-shell posts |
| G screw | 2 | M2x4 ISO 7045 pan head, conductive finish (D6) | PCB into the top-shell G posts; case ground |
| Set screw | 2 | M2x3 ISO 4029 cup point | one per knob |
| Foot | 4 | 3M Bumpon SJ5076, dia. 8.00 x 2.79; DigiKey 570288, 56 for USD 7.19 | foot pockets |

None of these is in the JLCPCB assembly library with stock (enclosure 6.3). The FDM prototype takes other
screws and heat-set inserts: [printing.md](printing.md#inserts-and-screws).

## Tools

- Tag-Connect TC2030 cable and a CMSIS-DAP or J-Link probe, for the first bootloader flash
  ([flashing.md](flashing.md)).
- The printed switch insertion jig (D26) and a 1.10 mm fork shim for the knobs (rotary-buttons 7).
- Soldering iron for the sockets; a loupe for the antenna inset.

## Substitutions

| Part | Allowed substitute | Check |
|---|---|---|
| Passives, diodes | same value, tolerance, package, voltage and dielectric | C1 and C2 must be C0G; the 3V3 capacitance sum of D14 must not grow |
| AO3400A, AO3401A | a SOT-23 MOSFET with the same pinout, Vgs threshold and Rds(on) class | gate, drain and source on the same pads |
| Switch | Kailh PG1353 Choc V2 | only if the Ghost fails the retention coupon |
| Cell | EEMB LP404261-PCM-LD for production; nothing thicker than 5.0 mm | pin 1 positive, JST PH plug, lead length per D28 |
| Module, charger, gauge, LDO, FPC connector, USB-C, encoders, sockets | none without a design change | ask the design owner |

## Cost

From [research/COMPONENTS.md](../research/COMPONENTS.md) section 2, updated with what the builders changed. All
USD, before duty and VAT. **None of these is a quote.** JLCPCB's minimum is 5 bare boards with 2 assembled, so
the one-unit column is that minimum order.

| Block | Line | 1 unit (5 PCBs, 2 assembled) | 5 units (5 PCBs, 5 assembled) | Basis |
| --- | --- | --- | --- | --- |
| PCB assembly | PCB fabrication, 4-layer, ENIG, in the D23 frame panel (135.65 x 95.30 mm) | 40 to 80 | 40 to 80 | guess; the frame adds area that was not in the research estimate; not quoted |
| | Setup, Standard, double-sided | 51.12 | 51.12 | price page (likely) |
| | Stencil, double-sided | 16.42 | 16.42 | price page (likely) |
| | Part loading, 30 x 1.53 | 45.90 | 45.90 | price page; 30 lines is now the draft BOM's count |
| | THT hand soldering (2 encoders) | about 3.8 | about 4.2 | price page (likely) |
| | X-ray, 1.64 per board | 3.28 | 8.20 | price page (likely) |
| | SMT joints, about 250 per board x 0.0016 | 0.80 | 2.00 | guess on the joint count (61 placements) |
| | Parts, 24.3 per board plus about 5 % attrition | 51 | 128 | COMPONENTS 1.1; the draft BOM has the same parts |
| | Confirm placement, packing, fixtures | 1 to 17 | 1 to 17 | price page; fixture charge conditional |
| | Shipping, one parcel | 20 to 45 | 20 to 45 | guess |
| | **Subtotal PCB assembly** | **about 235 to 315** | **about 320 to 400** | |
| Hand-fitted | Switches, one Lofree 106-pack | 59.00 | 59.00 | pack minimum dominates |
| | Sockets, splitkb 50-packs | 6.57 (1 pack) | 13.14 (2 packs) | |
| | Display panels (two for the first unit; ten for five) | 15.80 | 79.00 | display 8 |
| | Cells, Adafruit 258 | 9.95 | 49.75 | |
| | Keycaps, resin, 16 per unit (96 for five) | 16 to 32 | 96 to 192 | guess at USD 1 to 2 per cap |
| | Tapes, foam, insulation sheet | not found | not found | products not chosen |
| | Tools: TC2030 cable and probe | not priced | not priced | new in this list |
| | Shop shipping for the above | not found | not found | several shops |
| | **Subtotal hand-fitted** | **about 107 to 123 plus shipping** | **about 297 to 393 plus shipping** | |
| Case | Shells, insert, lens, knobs, button caps, feet, screws (now M1.6 K screws and M2 set screws), shipping | 200 to 350 | 560 to 1,030 | enclosure 9, guess; [ordering-case.md](ordering-case.md#cost) |
| | FDM prototype and the insertion jig (PETG, inserts) | under 5 | n/a | own printer |
| **Total** | | **about 540 to 790** | **about 1,175 to 1,820 (235 to 364 per unit)** | |

What changed against the research table: the board sits in a frame panel (D23), so the fabrication line
covers a larger area and its price is less certain; the BOM line count is now from the draft BOM instead of a
guess; the K screws are M1.6 (D30) and the knobs need M2 set screws; the insertion jig (D26) and the SWD tools
are new; the knob and insert drawings are still missing, so the case line has no quote behind it. What moves
the total most is unchanged: the case (no live quote), the double-sided PCBA setup, and the keycap price.
