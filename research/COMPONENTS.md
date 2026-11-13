# worxpad components: selected parts, cost, budgets and open conflicts

Date: 2026-11-13. Summary of the seven decision records in `research/components/`. Each row links to its record;
the record holds the reasons, the rejected candidates and the datasheet sources. Stock and prices were read on
2026-11-13 from the JLCPCB parts API, LCSC and shop pages, as stated in each record; they change daily.

Confidence words as in the records: **confirmed** (maker of the part, or read from a primary source), **likely**,
**guess**. "Not found" means looked for and not found. Coordinates: X from the right outer face, Y from the rear
outer face, Z from the deck (top face of the top shell), negative downward.

Records: [mcu-radio](components/mcu-radio.md) (rev 2), [keys](components/keys.md),
[display](components/display.md), [power](components/power.md), [rotary-buttons](components/rotary-buttons.md)
(rev 2), [usb-io](components/usb-io.md) (rev 2), [enclosure-manufacturing](components/enclosure-manufacturing.md)
(rev 2).

## 1. Selected parts

JLC class: **basic** (no loading fee in Economic PCBA), **ext** (extended), **hand** (not in the JLCPCB library,
fitted by hand), **made** (custom part from a CNC or print vendor). Unit price is USD at quantity 1 unless stated.
"Shop currency" means the shop's base currency as read by the record; the record does not state it.

### 1.1 Machine-placed at JLCPCB (PCBA)

| Subsystem | Role | Part | LCSC | JLC class | Stock as checked | Unit price | Qty / board | Record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mcu-radio | MCU and radio module, PCB trace antenna | u-blox BMD-340-A-R (nRF52840, LGA 68 pads, 15.0 x 10.2 x 1.9 mm) | C5456944 | ext | JLCPCB 349, LCSC 190 | 9.8079 | 1 | [mcu-radio 7.1](components/mcu-radio.md) |
| mcu-radio | Icon flash, 16 MB QSPI NOR | Winbond W25Q128JVSIQ (SOIC-8 208 mil, 2.16 mm max) | C97521 | basic | JLCPCB 69,913, LCSC 1,000 | 2.26 | 1 | [mcu-radio 7.4](components/mcu-radio.md) |
| mcu-radio | 32.768 kHz crystal, 12.5 pF | Epson Q13FC1350000400 | C32346 | basic | JLCPCB 419,369 | not read | 1 | [mcu-radio 7.4](components/mcu-radio.md) |
| mcu-radio | Crystal load caps 20 pF C0G 0402 | generic | C1554 | basic | 1,196,204 | <0.01 | 2 | [mcu-radio 7.4](components/mcu-radio.md) |
| mcu-radio | Module bulk 10 uF 0603; flash 100 nF 0402 | Samsung | C19702, C1525 | basic | millions | <0.01 | 1 + 1 | [mcu-radio 7.4](components/mcu-radio.md) |
| keys | Matrix diode | 1N4148W SOD-123 (Semtech) | C81598 | basic | JLCPCB 3,287,205, LCSC 1,867,300 | 0.0124 | 20 | [keys 6.7](components/keys.md) |
| rotary-buttons | Rotary encoder with push, 24/24, open at detent, THT | Bourns PEC12R-4215F-S0024 | C22385080 | ext | JLCPCB 28, LCSC 28 | 2.95 | 2 | [rotary-buttons 6.1](components/rotary-buttons.md) |
| rotary-buttons | Round button switch, 0.98 N | Omron B3FS-1000P (top face) | C271750 | ext | 67,955 each | 0.21 | 2 | [rotary-buttons 5](components/rotary-buttons.md) |
| display | FPC connector 24-pin 0.5 mm, top and bottom contact | Hirose FH34SRJ-24S-0.5SH(50) (top face) | C324726 | ext | JLCPCB 12,971 | 0.2461 | 1 | [display 8](components/display.md) |
| display | Backlight low-side switch | AO3400A SOT-23 | C20917 | basic | 1,025,527 | 0.0789 | 1 | [display 8](components/display.md) |
| display | LED resistor 15 Ohm 1 % 0402; gate pull-down 100k; VDD 1 uF and 100 nF | generic | C25083, C25741, C52923, C1525 | ext, basic, basic, basic | 68,147 and more | <0.01 | 1 each | [display 8](components/display.md) |
| power | Linear charger with power path, USB500, ~400 mA | TI BQ24072RGTR (VQFN-16) | C140288 | ext | 1,216 | 1.06 | 1 | [power 13](components/power.md) |
| power | 3.3 V LDO, 200 mA, 25 nA | TI TPS7A0233PDBVR | C2887324 | ext | JLCPCB 5,309, LCSC 1,871 | 1.14 | 1 | [power 13](components/power.md) |
| power | Fuel gauge, I2C 0x36 | ADI MAX17048G+T10 | C2682616 | ext | 20,372 | 1.94 | 1 | [power 13](components/power.md) |
| power, usb-io | Power slide switch on LDO EN | Shouhan MSK12C02 | C431540 | ext | 172,615 | 0.055 | 1 | [power 8](components/power.md), [usb-io 6.7](components/usb-io.md) |
| power | Reverse-polarity P-FET | AOS AO3401A | C15127 | basic | 1,557,883 | 0.08 | 1 | [power 13](components/power.md) |
| power | Battery connector, JST PH 2-pin side entry (5.5 mm tall) | JST S2B-PH-SM4-TB | C295747 | ext | 743 | 0.20 | 1 | [power 11](components/power.md) |
| power | NTC 10k B3950 0805 | Fenghua CMFB103F3950FANT | C51597 | ext | 41,619 | 0.07 | 1 | [power 13](components/power.md) |
| power | RISET 2.2k, RILIM 3.3k, EN1 100k, I2C pull-ups 4.7k x2, 1 uF 0603, 10 uF 0603, 100 nF | generic 0402/0603 | C25879, C25890, C25741, C25900, C15849, C19702, C1525 | basic | millions | <0.01 | 9 | [power 13](components/power.md) |
| usb-io | USB-C receptacle, mid-mount 1.60 mm sink, 16-pin | HRO TYPE-C-31-M-13C | C2848620 | ext | 4,695 | 0.266 | 1 | [usb-io 6.1](components/usb-io.md) |
| usb-io | USB ESD array (D+, D-, VBUS) | ST USBLC6-2SC6 | C7519 | ext | 43,069 | 0.157 | 1 | [usb-io 4.2](components/usb-io.md) |
| usb-io | VBUS PTC, 0.75 A hold at 20 °C, 0.54 A at 60 °C | Littelfuse 1206L075THYR | C99563 | ext | 10,807 | 0.054 | 1 | [usb-io 4.3](components/usb-io.md) |
| usb-io | CC pull-downs 5.1k 1 % 0402 | generic | C25905 | basic | not stated | <0.01 | 2 | [usb-io 6.3](components/usb-io.md) |
| usb-io | Reset tact switch (bottom face, floor pinhole) | XKB TS-1187A-B-A-B | C318884 | basic | 815,200 | 0.022 | 1 | [usb-io 4.6](components/usb-io.md) |
| usb-io | SWD | Tag-Connect TC2030-NL footprint, copper only | none | none | n/a | 0 | 1 | [usb-io 6.5](components/usb-io.md) |

Parts cost per board (arithmetic on the rows above, crystal taken as about USD 0.15, guess): **about USD 24.3**, of
which the module is 9.81 and the two encoders 5.90.

### 1.2 Hand-fitted or bought outside JLCPCB

| Subsystem | Role | Part | LCSC | JLC class | Stock as checked | Unit price | Qty / unit | Record |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| keys | Switch, linear full POM, Choc V2 PG1353D class | Lofree Ghost (Lofree x Kailh) | none | hand | lofree.co 106-pack available | 59.00 per 106 (shop currency) | 16 | [keys 6.7](components/keys.md) |
| keys | Switch fallback for the aluminium shell | Kailh PG1353 Choc V2 set CPG135301D01/D02/D03 | C45350823 / C5142796 (stock 0) | hand | kailh.net 110-set available | 66.00 per 110 (shop currency) | 16 if needed | [keys 6.7](components/keys.md) |
| keys | Hot-swap socket, Choc | Kailh CPG135001S30 | C5333465 | ext, not purchasable, discontinued | JLCPCB 0, LCSC 0; splitkb 50-pack available | 6.57 per 50 (shop currency) | 16 | [keys 4.2, 6.7](components/keys.md) |
| keys | Keycap, project design, 18.20 base, 4.40 tall | JLC3DP JLC Black Resin print | none | made | made to order | not quoted ("From $1.0" per print) | 16 | [keys 6.5](components/keys.md) |
| keys | Keycap fallback | Tai-Hao THT PBT blank black (MX) | none | hand | keeb.io available | 37.99 per set | 1 set | [keys 6.7](components/keys.md) |
| display | Panel 1.3 inch 240 x 240 IPS ST7789VW, 24-pin | DisplayModule DM-TFT13-377p24 (LH133T-IF05) | none | hand | 60 at DisplayModule; Adafruit 4520 26 at USD 12.50 | 7.90 | 1 | [display 8](components/display.md) |
| display | Cover lens 31.2 mm square R2, 1.0 mm cast PMMA, painted underside, 24.4 mm window | laser shop | none | made | shop not found | not found | 1 | [display 6.4](components/display.md) |
| display | Adhesive ring, black tape frame, foam pad | generic | none | hand | product not chosen | not found | 1 set | [display 8](components/display.md) |
| power | Cell, production: 1,000 mAh, 4.3 x 42.5 x 63 mm, PCM | EEMB LP404261-PCM-LD | none | hand | quotation only | not found | 1 | [power 5.1](components/power.md) |
| power | Cell, bring-up and FDM: 1,200 mAh, 5.0 x 34 x 62 mm, JST PH | Adafruit 258 | none | hand | in stock | 9.95 | 1 | [power 5.1](components/power.md) |
| power | Insulating sheet 0.3 mm over sockets at the pocket | polyimide or PET | none | hand | any | not priced | 1 | [power 5.2](components/power.md) |
| enclosure | K screws M2 x 5 DIN 7991 | any | none | hand | not confirmed | in screw packs | 4 | [enclosure 6.3](components/enclosure-manufacturing.md) |
| enclosure | C screws M2 x 6 DIN 7991 | any | none | hand | not confirmed | in screw packs | 2 | [enclosure 6.3](components/enclosure-manufacturing.md) |
| enclosure | G screws M2 x 4 pan head, conductive finish | any | none | hand | not confirmed | in screw packs | 2 | [enclosure 6.3](components/enclosure-manufacturing.md) |
| enclosure | Feet, Ø8.00 x 2.79 mm | 3M Bumpon SJ5076 | none (DigiKey 570288) | hand | DigiKey 1,222,328 | 7.19 per 56 | 4 | [enclosure 6.3](components/enclosure-manufacturing.md) |
| enclosure | Heat-set inserts, FDM only | CNC Kitchen M2 x 3.0 | none | hand | not confirmed | not priced | 2 to 4 | [enclosure 6.3](components/enclosure-manufacturing.md) |

### 1.3 Made case parts

| Part | Material, finish | Vendor (fallback) | Record |
| --- | --- | --- | --- |
| Top shell (deck, plate, lens recess and web, knob plinth, button holes, C and G posts) | 6061-T6, bead blast, black anodise Type II, Strict | JLCCNC (PCBWay CNC) | [enclosure 6.2](components/enclosure-manufacturing.md) |
| Bottom shell (tray, wedge, K posts, battery pocket, RF slot, rear notches) | same | JLCCNC (PCBWay CNC) | same |
| RF window insert | black POM, machined | JLCCNC (JLC3DP MJF PA12) | [enclosure 7.2](components/enclosure-manufacturing.md) |
| Knobs (2), Ø10.50 x 9.10 mm, Ø8.40 x 1.20 counterbore, M2 set screw | 6061-T6 turned, black anodise | JLCCNC | [rotary-buttons 6.5](components/rotary-buttons.md) |
| Button caps (2), Ø12.30 | JLC Black Resin | JLC3DP | [rotary-buttons 6.6](components/rotary-buttons.md) |
| 1.10 mm fork shim (assembly tool) | print at 0.1 mm layers or shim stock | own | [rotary-buttons 7](components/rotary-buttons.md) |
| FDM prototype shells | PETG, 0.2 mm layers, Bambu A1 mini | own printer | [enclosure 8](components/enclosure-manufacturing.md) |

## 2. Cost roll-up

All figures USD, before import duty and VAT. **None of these is a quote.** The PCBA fee lines use the JLCPCB
price-page figures recorded on 2026-11-04 in the sibling repository (`/home/worxbend/Projects/worxboard/docs/
ordering-jlcpcb.md`, cost estimate section; owner's notes, likely). The case lines are the enclosure record's
guesses. JLCPCB's minimum is 5 bare boards with 2 assembled, so the one-unit column is that minimum order.

Assumptions: 4-layer board 120.5 x 85.2 mm, ENIG; Standard PCBA, **double-sided** (top-side FH34SRJ connector and
B3FS switches, section 7 conflict 6); about 30 distinct part numbers at USD 1.53 loading each; two THT encoders
hand-soldered by JLCPCB; X-ray for the LGA module and the QFN charger.

| Block | Line | 1 unit (5 PCBs, 2 assembled) | 5 units (5 PCBs, 5 assembled) | Basis |
| --- | --- | --- | --- | --- |
| PCB assembly | PCB fabrication, 4-layer, ENIG | 40 to 80 | 40 to 80 | guess; the maker paid 73.92 for 5 boards with options (`raw/social.md` 4.4) |
| | Setup, Standard, double-sided | 51.12 | 51.12 | price page (likely) |
| | Stencil, double-sided | 16.42 | 16.42 | price page (likely) |
| | Part loading, 30 x 1.53 | 45.90 | 45.90 | price page; part count is ours (guess) |
| | THT hand soldering (2 encoders) | about 3.8 | about 4.2 | price page (likely) |
| | X-ray, 1.64 per board | 3.28 | 8.20 | price page (likely) |
| | SMT joints, about 250 per board x 0.0016 | 0.80 | 2.00 | guess on the joint count |
| | Parts, 24.3 per board plus about 5 % attrition | 51 | 128 | section 1.1 |
| | Confirm placement, packing, fixtures | 1 to 17 | 1 to 17 | price page; fixture charge conditional |
| | Shipping, one parcel | 20 to 45 | 20 to 45 | guess |
| | **Subtotal PCB assembly** | **about 235 to 315** | **about 320 to 400** | |
| Hand-fitted | Switches, one Lofree 106-pack | 59.00 | 59.00 | pack minimum dominates |
| | Sockets, splitkb 50-packs | 6.57 (1 pack) | 13.14 (2 packs, 100 with spares) | |
| | Display panels (two per unit for the first one; ten for five) | 15.80 | 79.00 | display record buys 10 for 5 units |
| | Cells, Adafruit 258 | 9.95 | 49.75 | EEMB production cell not quoted |
| | Keycaps, resin print, 16 per unit | 16 to 32 | 96 to 192 (96 caps) | guess at USD 1 to 2 per cap |
| | Tapes, foam, insulation sheet | not found | not found | |
| | Shop shipping for the above | not found | not found | several shops |
| | **Subtotal hand-fitted** | **about 107 to 123 plus shipping** | **about 297 to 393 plus shipping** | |
| Case | Shells, insert, lens, knobs, button caps, feet, screws, shipping | 200 to 350 | 560 to 1,030 | [enclosure 9](components/enclosure-manufacturing.md), guess |
| | FDM prototype (PETG, inserts) | under 5 | n/a | own printer |
| **Total** | | **about 540 to 790** | **about 1,175 to 1,820 (235 to 364 per unit)** | |

What moves the total most: the case (no live JLCCNC quote; needs an account and STEP files), the double-sided
PCBA setup (a single-sided board would save part of the setup and stencil), and the keycap print price.

## 3. Pin budget against the BMD-340 (48 GPIO)

Allocation from [mcu-radio 7.2](components/mcu-radio.md) with the changes in [power 12](components/power.md),
[display 6.2](components/display.md), [keys 6.6](components/keys.md), [rotary-buttons 7](components/rotary-buttons.md)
and [usb-io 6.6](components/usb-io.md).

| Function | Pins | Count | Pin class | Owner |
| --- | --- | --- | --- | --- |
| QSPI flash: SCK, CSN, IO0 to IO3 | P0.19, P0.17, P0.20, P0.21, P0.22, P0.23 | 6 | full speed | mcu-radio |
| Display SPIM3: SCK, MOSI, CS, DC; RESET | P0.13, P0.15, P0.14, P0.16; P1.00 | 5 | full speed | display |
| Backlight PWM (`zmk,display-led`) | P0.24 | 1 | full speed | display |
| I2C SDA, SCL (gauge) | P0.07, P0.11 | 2 | full speed | power |
| Charger /CHG, /PGOOD; gauge ALRT | P0.03, P0.04, P0.26 | 3 | low freq / full / full | power |
| Encoder 1 A/B, encoder 2 A/B | P0.28/P0.30, P0.29/P0.31 | 4 | low frequency | rotary-buttons |
| Matrix rows (inputs, pull-down) | P1.12, P1.13, P1.14, P1.15 | 4 | low frequency | keys |
| Matrix columns (outputs) | P0.02, P0.25, P0.27, P1.05, P1.06 | 5 | mixed | keys |
| 32.768 kHz crystal XL1, XL2 | P0.00, P0.01 | 2 | | mcu-radio |
| Reset (`gpio-as-nreset`) | P0.18 | 1 | | usb-io |
| **Committed** | | **33** | | |
| Optional peripheral rail enable | P1.07 | (1) | | mcu-radio |
| **Spare** | P0.05, P0.06, P0.08, P0.09, P0.10 (NFC, need config), P0.12, P1.01 to P1.04, P1.07, P1.08 to P1.11 | **15** | | |

Not counted as GPIO: USB D-/D+/VBUS (pads 67/68/66), SWDIO/SWCLK (pads 44/43), VCC/VCCH (pads 17/65). The
matrix needs a GPIO supply of at least 2.7 V (silicon diode drop, [keys 6.6](components/keys.md)); LV mode on a
3.3 V rail meets it. For soft-off wake, the five column pins go into `extra-gpios`.

## 4. Power rails and current budget

### 4.1 Rails

| Rail | Source | Range | Consumers | Record |
| --- | --- | --- | --- | --- |
| VBUS | USB-C, after USBLC6 and the 1206L075 PTC | 4.35 to 6.6 V at BQ IN; worst-case input 0.51 A (USB500 limit) | BQ24072 IN; module pad 66 (USB PHY only) | [usb-io 6.3](components/usb-io.md), [power 12](components/power.md) |
| BAT | Cell through the pack PCM and AO3401A | 3.0 to 4.2 V | BQ24072 BAT, MAX17048 | [power 9](components/power.md) |
| VSYS | BQ24072 OUT | 3.0 to 4.5 V (to 5.6 V with the BQ24075 fallback) | TPS7A02 IN, slide switch high throw | [power 6.3](components/power.md) |
| 3V3 | TPS7A02, enabled by the slide switch | 3.3 V, 200 mA rating; total ceramic capacitance 1 to 22 uF | Module VCC and VCCH (LV mode), flash, panel VDD/VDDIO, backlight through 15 Ohm, I2C pull-ups | [power 7](components/power.md) |

Charge: about 400 mA (362 to 443), 4.20 V, timers 30 min / 5 h, NTC on the PCB, 0 to 50 °C window.

### 4.2 Current budget (battery current)

| State | Current, typ (max) | Basis |
| --- | --- | --- |
| Off (slide switch off, rail down) | about 8 uA (16) | charger 4.3 + gauge sleep 0.5 + PCM 3 ([power 4.2](components/power.md)) |
| Deep sleep (System OFF, link dropped) | 31 uA (80) | MCU subsystem 21 + overhead 10 |
| Connected idle, display blanked, with the two firmware hooks | 54 uA (102) | 44 + 10; hooks in [mcu-radio 7.7](components/mcu-radio.md) |
| Connected idle without the hooks | unknown, likely 1 to 6 mA | ST7789V DISPOFF current not given |
| Display lit, backlight off | about 9 mA (7 to 12) | panel 6 to 8 + CPU 2 (guess) + BLE 0.6 + scan 0.3 |
| Display lit, chosen 1.3 inch panel, backlight 100 / 50 / 25 / 10 % | 44 / 27 / 18 / 12.5 mA (power record, 35 mA backlight) or 36 mA at 100 % with the display record's 26.7 mA nominal | [power 4.2](components/power.md), [display 6.3](components/display.md) |
| Peak on 3V3 | 89 mA with the chosen panel (51 MCU subsystem max + 38 backlight worst); 111 mA in the power record (60 mA backlight for the 1.4 inch panel) | both under the 200 mA LDO rating |
| Encoders at rest | 0 uA (both contacts open at every detent) | [rotary-buttons 7](components/rotary-buttons.md) |

Runtime (arithmetic, [power 4.3](components/power.md)): with 850 mAh usable, 4 h a day lit at 25 % plus 20 h
connected idle gives about 8.8 days; at 50 % about 5.4 days; a GLYF-like day at 100 % without dimming about 3 days.
These rows used the 60 mA backlight of the 1.4 inch panel, so they are conservative for the chosen panel.

## 5. Vertical stack-up

Z from the deck, negative downward. Sources in the last column.

| Z (mm) | Level | Record |
| --- | --- | --- |
| +12.00 | Knob top (fallback encoder: +14.50) | [rotary-buttons 6.3](components/rotary-buttons.md) |
| +4.40 | Keycap top at rest (pressed +1.60 with PG1353D, +1.20 with PG1353) | [keys 6.3](components/keys.md) |
| +2.90 | Knob rim underside at rest, 1.10 mm shim above the plinth | rotary-buttons |
| +1.80 | Knob plinth top | rotary-buttons |
| +1.00 | Round button cap top at rest | rotary-buttons |
| 0.00 | Deck; display lens top flush; keycap skirt bottom at rest | keys, display |
| -1.00 / -1.15 | Lens underside / lens recess floor | [display 6.4](components/display.md) |
| -1.75 | Web underside (0.60 mm web; 0.80 requested) | display, enclosure |
| -2.80 | Top of the RF bay; top-shell underside over the bay at or above this | [mcu-radio 7.3.1](components/mcu-radio.md) |
| -3.35 | Display module back | display |
| -4.00 | Plate top | keys |
| -5.00 | Shell split plane | [enclosure 6.1](components/enclosure-manufacturing.md) |
| -5.15 | Plate (lip) underside, 1.15 mm lip | keys |
| -5.20 | FPC connector top; K post tops; top of RF wall slot | display, enclosure, mcu-radio |
| -6.20 | PCB top face | keys |
| -7.80 | PCB bottom face | keys |
| -7.82 | USB-C contact centre line | [usb-io 6.1](components/usb-io.md) |
| -8.55 | Slide switch actuator (inside the Z -5.00 to -9.90 rear notch) | [power 8](components/power.md), usb-io |
| -9.20 / -9.50 | Switch pin tips / centre post tip | keys |
| -9.40 | G screw head underside (floor top at G at -9.70 or lower) | enclosure |
| -9.65 | Socket underside | keys |
| -9.70 (-9.80 max) | BMD-340 shield bottom; encoder pin ends before trimming | mcu-radio, rotary-buttons |
| -9.90 | Bottom of the USB-C and switch notches | usb-io |
| -9.95 | Floor top under sockets (0.3 mm clear); flash body bottom -9.96 | keys, mcu-radio |
| -9.95 to -10.25 | Insulating sheet over sockets at the pocket | power |
| -11.45 | Underside over a socket with a 1.5 mm floor | keys |
| -11.70 | Bottom of the RF wall slot | mcu-radio |
| -12.00 | Underside at the rear wall and in the flank scoops | enclosure |
| -13.00 | Underside at the front edge | enclosure |
| -13.30 | Floor top under the RF bay (or lower); JST PH underside | mcu-radio, power |
| -13.60 | Floor top under the battery connector (or lower) | power |
| -15.18 / -15.95 | Battery pocket floor top, 4.3 mm cell / 5.0 mm cell | [power 5.2](components/power.md) |
| -16.68 / -17.45 | Underside needed over the pocket with a 1.5 mm floor | power |
| -19.20 | Underside at the wedge apex (Y 12.7) | enclosure |

Plan: body 128.4 x 85.2 mm; PCB 120.5 mm wide with its outline 0.45 mm or more from the 3.5 mm walls; local PCB
tongues at the rear for USB-C (13.0 wide, to D 0.95) and the switch (9.0 wide, to D 1.90).

## 6. Disagreements between records and research notes

Each line names both sides. None is smoothed over.

1. **Module choice.** `raw/follow-radio-module-choice.md` recommends the Ebyte E73-2G4M08S1C/S1CX with the
   BMD-340 as the alternative. [mcu-radio](components/mcu-radio.md) chose the BMD-340: 48 GPIO against 2 to 4
   spare on the E73, a measured RAM fit, and 349 in stock against 61 for the E73 with a ceramic antenna.
2. **Backlight current.** [power](components/power.md) budgets 60 mA (1.4 inch, 3 LEDs) and a 111 mA peak.
   [display](components/display.md) chose a panel with 26.7 mA nominal, 37.7 mA worst case, and an 89 mA peak.
   Both fit the 200 mA LDO; the power runtime table is conservative, not wrong.
3. **Panel size and body width.** [mcu-radio 7.3.3](components/mcu-radio.md) sized the 8.0 mm widening for the
   1.4 inch panel; with the chosen 1.3 inch panel 7.0 mm would do. The records keep 8.0 mm.
4. **Battery cell.** `raw/follow-battery-cell-and-runtime.md` puts the GLYF's 4.0 x 42 x 57 mm cell in a
   43 x 74 mm pocket; [power](components/power.md) asks for a 45 x 66 mm pocket for a 4.3 x 42.5 x 63 or a
   5.0 x 34 x 62 mm cell. [enclosure 6.6](components/enclosure-manufacturing.md) shows the wedge gives the needed
   depth only over 23.6 mm (5.0 mm cell) or 33.9 mm (4.3 mm cell) in Y, against 45.0 mm.
5. **Case bonding.** [usb-io](components/usb-io.md) rev 2 specifies one ground screw G1 into a Ø4.5 boss ending at
   Z -6.15 with 3.0 mm of thread. [enclosure 6.4](components/enclosure-manufacturing.md) rev 2 specifies two, G1
   and G2, on Ø4.6 posts ending at Z -6.20 with 2.7 mm of thread. The enclosure open list still asks usb-io to
   adopt dedicated G screws, which usb-io rev 2 already did.
6. **Assembly sides.** [mcu-radio 8](components/mcu-radio.md) and [usb-io 7](components/usb-io.md) say
   "single-side assembly", and [keys](components/keys.md) puts all SMD on the bottom. [rotary-buttons 6.2](components/rotary-buttons.md)
   puts the B3FS switches on the top face and calls them the only top-side SMD parts. [display 7](components/display.md)
   also puts the FH34SRJ connector on the top face. The board is double-sided SMT.
7. **RF slot length.** [mcu-radio](components/mcu-radio.md) prefers 40 mm (Y 33 to 73) and accepts 30 mm;
   [enclosure](components/enclosure-manufacturing.md) fixes 30 mm (Y 38 to 68) so the scoops can end by Y 35.
8. **Top shell over the slot.** [enclosure](components/enclosure-manufacturing.md) reads mcu-radio A7 and A9 as
   "wall above the slot (Z 0 to -5.0) stays metal"; mcu-radio A7 asks only for the top shell over the bay to be
   2.80 mm or thinner. Confirmation from mcu-radio is open.
9. **Display web.** [display](components/display.md) specifies a 0.60 mm web; [enclosure](components/enclosure-manufacturing.md)
   lists it as below the 0.8 mm recommendation and requests 0.80 mm, which needs the module 0.20 mm lower.
10. **Regulator accuracy.** [display 7](components/display.md) asks for a ±1 % 3.3 V regulator because the panel
    VDD maximum is 3.3 V. [power 7](components/power.md) chose the TPS7A02 without stating its output accuracy.
11. **Shell interfaces in the GLYF notes.** `raw/geometry.md` 4.8 puts the GLYF rear apertures half in each shell;
    [usb-io](components/usb-io.md) and [enclosure](components/enclosure-manufacturing.md) put worxpad's wholly in
    the bottom shell. This is a design choice, recorded so that nobody re-imports the GLYF value.

## 7. Cross-subsystem conflicts the design phase must settle

1. **Battery pocket against the wedge.** 45.0 mm of pocket in Y against 23.6 or 33.9 mm of usable wedge depth.
   Options from enclosure 6.6: a cell 31 mm or less in Y; a body about 1.1 mm thicker at the pocket front
   (4.3 mm cell then fits Y 9.5 to 54.5); a 1.0 mm pocket floor. K1 and K2 posts at Y 11.0 also need Ø6.6
   clearance at the pocket's rear edge. Owners: power, enclosure.
2. **G2 against the right button counterbore** (our arithmetic on the records). G2 post Ø4.6 at (7.5, 70.0) and
   the Ø17.0 counterbore of button 1 at (18.27, 71.20) are 10.84 mm apart, against 2.3 + 8.5 = 10.80 mm of radii:
   0.04 mm of wall in plan, against the enclosure's own 1.2 mm rule. Move G2 or shrink the counterbore. Owners:
   enclosure, rotary-buttons.
3. **One or two ground screws, and their boss numbers** (disagreement 5). Owners: usb-io, enclosure.
4. **Flash under the key field.** The SOIC-8 flash reaches Z -9.96; the floor top under sockets is Z -9.95, and
   mcu-radio asks for 2.5 mm floor clearance under the module and flash (floor top at -10.30 or lower). Place the
   flash outside the key-field floor or use the WSON-8 W25Q128JVPIQ (C190862, height not read). Owners: PCB
   layout, mcu-radio, enclosure.
5. **Battery connector depth.** The JST PH needs a floor top at Z -13.60 or lower and 12 mm free in front of its
   mouth, under the control column left of the RF bay. In the flank scoops (to Y 35) the underside is Z -12.0,
   so the connector must sit at Y 35 or more, where the ramp is thick enough. Not yet placed. Owners: power, PCB.
6. **Double-sided PCBA** (disagreement 6). Accept two-sided Standard PCBA, or move the FH34SRJ and the B3FS
   switches to the bottom face (the B3FS cannot move without changing the button stack). Owners: display,
   rotary-buttons, PCB.
7. **Body width 128.4 mm, flank scoops ending by Y 35, one knob plinth instead of two bosses.** All three change
   the GLYF look and need the owner's approval. If the width is refused, the antenna sits under the display edge
   and the comparison test must pass before the CNC order. Owners: owner, mcu-radio, enclosure.
8. **Display web 0.60 or 0.80 mm** (disagreement 9). Owners: display, enclosure.
9. **Top-shell metal above the RF slot** (disagreement 8). Owners: mcu-radio, enclosure.
10. **VBUS on module pad 66 while VDD is 0 V** (switch off, USB charging). Not checked against the nRF52840
    specification; the fix is a load switch on pad 66. Owners: power, mcu-radio.
11. **Regulator accuracy for panel VDD** (disagreement 10). Owners: power, display.
12. **Total 3V3 capacitance at or under 22 uF** for TPS7A02 stability, counting the module's internal 4.7 uF,
    the 10 uF bulk, the flash, panel and LDO capacitors. Not yet summed. Owners: power, PCB.
13. **I2C pull-up ownership.** The power parts list carries two 4.7k pull-ups; the power record still asks who
    places them. Owners: power, mcu-radio.

## 8. Open questions

Parts and supply:

1. Kailh CPG135001S30 sockets: zero stock at JLCPCB and LCSC, flagged discontinued. Buy 100 from a keyboard shop
   now; consignment fee and PCBWay sourcing not checked.
2. PEC12R-4215F encoder: 28 in stock against 12 needed, with a six-month use-by note. Order timing. Bourns
   specifies wave soldering and calls hand soldering "Not recommended"; ask how JLCPCB solders it in its THT step.
3. EEMB production cell: price, lead time, small quantity and JST PH plug option not confirmed.
4. BMD-340 stock carries a 2022 date code on an MSL 3 part: dry-pack and baking to be confirmed with JLCPCB.
5. Laser shop and price for the painted PMMA lens; tapes and foam products.
6. No live JLCCNC quote; account and STEP files needed. Can JLCCNC laser-clear the G post faces?

Mechanical tests before the CNC order:

7. Does the PG1353D hold in a 1.15 mm anodised aluminium lip, given Kailh's "only fits plastic plates" note?
   Fallback PG1353 has 0.55 mm worst-case pressed clearance.
8. Keycap stem-fit coupon (0.55 mm post wall against JLC3DP's 0.8 mm advice); button cap rocking coupon.
9. Display flex fold mock-up to set the connector Y position.
10. Encoder sample: real switch travel, collar diameter (about 7.3 mm scaled), pocket fit.
11. USB-C skin coupon (0.6 mm skin, 0.35 mm prong clearance).
12. Plate lip under bead blast (JLCCNC advises 1.5 mm or more).

Radio and firmware:

13. RF range in aluminium: foil-lined FDM pre-test, then the 3 m acceptance test on the first aluminium unit.
14. The two power hooks (panel SLPIN, flash runtime PM) are not written; connected standby depends on them.
15. Own Raw HID module not written; second HID-over-GATT service on macOS and Windows unverified.
16. Adafruit bootloader 0.11.0 changes #384 and #390 with ZMK on this board.
17. ST7789 orientation and the 80-line RAM offset on the first board; 16 MHz SPI is 6 % over the write-cycle spec.

Scope:

18. Real-time clock. The GLYF carries a DS3231 with a coin cell for its clock widget; no worxpad record selects
    an RTC. Decide between host time sync over Raw HID and a hardware RTC (pins are spare).
19. Does the owner have a TC2030-IDC-NL cable and a CMSIS-DAP or J-Link probe?

## 9. Not checked in this summary

The cost roll-up re-uses price-page figures from a sibling repository dated 2026-11-04 and the enclosure record's
guesses; nothing was re-quoted today. The crystal price and the JLCPCB X-ray and THT rules were not re-read. The
G2 clearance in section 7 item 2 and the flash clearance in item 4 are this summary's own arithmetic on record
values; the records' owners have not reviewed them.
