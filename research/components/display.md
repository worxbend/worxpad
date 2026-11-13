# Decision record: display, connector, backlight and cover lens

Key: `display`
Date: 2026-11-13
Status: decided, revision 1
Cache: `research/_cache/display/` (batches `01-jlc` to `09-dm-render`)

Confidence words: **confirmed** (stated by a maker, or read from a primary drawing, datasheet or source file),
**likely** (consistent indirect evidence), **guess**. "Not found" means a search was made and returned nothing usable.

Coordinates follow `mcu-radio.md` section 7.3: X from the right outer face of the body (positive inward), Y from the
rear outer face (positive toward the user), Z from the deck (the top face of the top shell), negative downward.
PCB top face Z -6.20, PCB bottom face Z -7.80 (`keys.md` 6.3). The body is 128.4 x 85.2 mm after the 8.0 mm
widening in `mcu-radio.md` 7.3.3, so the lens sits 12.0 mm from the right face.

## 1. Decision in short

1. **Panel:** 1.3 inch 240 x 240 IPS TFT, ST7789VW, 24-pin 0.5 mm plug-in flex: DisplayModule DM-TFT13-377p24
   (maker part LH133T-IF05 / ZJY133T-IF05). Outline 26.16 x 29.22 x 1.5 mm, active area 23.4 x 23.4 mm. USD 7.90,
   60 available at DisplayModule today. The same glass is sold as Adafruit 4520 (USD 12.50, 26 in stock today).
   It is the only 240 x 240 panel with a public drawing and a plug-in flex that can be bought in single units today.
   The GLYF's 1.4 inch panel (25.2 mm active area) has no small-quantity source.
2. **Connector:** Hirose FH34SRJ-24S-0.5SH(50), LCSC C324726, extended, 12,971 at JLCPCB and 12,735 at LCSC today,
   about USD 0.25. It is 1.0 mm tall, back-flip, with **top and bottom contacts**, so the panel works whichever way
   the flex is folded. It sits on the PCB **top** face under the module, and the flex folds back 180 degrees under
   the module, as the panel drawing intends.
3. **Backlight:** low-side N-MOSFET AO3400A (C20917, basic) switched by PWM from P0.24 (`zmk,display-led`), with a
   15 Ohm series resistor (C25083, extended) from the 3.3 V rail into LEDA, and a 100 kOhm gate pull-down. The
   current is 22 to 38 mA at full duty and about 27 mA nominal. No driver IC.
4. **Cover lens:** 31.2 x 31.2 mm, R2.0 corners, 1.0 mm clear cast PMMA, laser cut, with the underside painted black
   and the 24.4 mm window laser-ablated. It sits flush in a recess in the top shell on a 0.13 mm adhesive ring.
   The GLYF-style printed tempered glass (1.1 mm) is the route for larger batches (minimum order 100 pieces).
5. **Mounting:** the module hangs under a 0.6 mm aluminium web with a 24.8 mm window, held by a black 0.10 mm double-sided tape frame (0.5 mm wide) on the glass rim, backed by a foam pad on the PCB. The flex exits toward
   the front of the device, toward the round buttons.
6. **Firmware:** stock Zephyr 4.1 `sitronix,st7789v` on `zephyr,mipi-dbi-spi`, SPIM3, as settled in
   `mcu-radio.md`. Nothing new is needed.
7. **Antenna window:** the display window does not double as the radio exit. The right-wall slot in `mcu-radio.md`
   stays. Section 9 says what a combined window would need.

## 2. Context

- The GLYF uses a 1.4 inch 240 x 240 ST7789V-class IPS module with a bonded 31.20 mm square lens (R2), a 2.95 mm
  stack and a 20-pin 0.5 mm flex. The window is square, not portrait (`geometry.md` 4.5, supplier drawing
  `_cache/youtube/crops-01/sr0MIYEi678-f010-lcd-drawing-2x.png`; confirmed). The maker paid USD 210 for five
  modules with bonded glass (`youtube.md`, `social.md`; confirmed).
- The GLYF UI is a status bar, two rows of knob labels and a 4 x 4 icon grid in 240 x 240 pixels
  (`official-site.md`). A square 240 x 240 panel gives the same UI pixel for pixel.
- `mcu-radio.md` (settled) fixes the bus and the power budget: SPIM3 with SCK P0.13, MOSI P0.15, CS P0.14,
  DC P0.16, RESET P1.00, backlight PWM P0.24 as `zmk,display-led`, 16 MHz to start; a single 3.3 V rail rated
  150 mA or more; panel SLPIN through PM suspend on idle. It also fixes the RF bay: the LCD outline, frame, flex and
  connector stay at least 9.4 mm in plan from the board edge along the bay (X >= 13.35 for Y 42.9 to 63.1), and
  no metal from Z -2.80 to -13.30 in the bay.
- `follow-display-module-sourcing.md` found no shop that sells the bare 1.4 inch 28.0 x 31.35 mm panel in single
  units, no LCSC or JLCPCB stock of any 240 x 240 panel, and no printed glass lens below 100 pieces.

## 3. Requirements

| # | Requirement | Source |
| --- | --- | --- |
| D1 | 240 x 240 colour, so the GLYF UI (4 x 4 icon grid) maps one to one | `official-site.md`, task |
| D2 | Fits under a 31.2 mm square lens in the 38.6 mm control column, between knob bosses and button holes (glass envelope 31.7 x 37.8 mm) | `geometry.md` 7.3 |
| D3 | LCD outline at X >= 13.35 along the RF bay; no flex or connector in the bay | `mcu-radio.md` A6, 7.3.3 |
| D4 | SPI interface with a driver in the pinned Zephyr 4.1 / ZMK 4dd95d78 | `mcu-radio.md` |
| D5 | Sleep current in the tens of microamperes; backlight dimmable by PWM and fully off on idle | `mcu-radio.md` 7.6, 7.7 |
| D6 | Buyable in 5 to 10 pieces today, with a public drawing | task |
| D7 | Black UI readable indoors: IPS, all-angle viewing | task |
| D8 | Connector placeable by JLCPCB; the panel itself is hand-fitted | `follow-display-module-sourcing.md` 5.3 |

## 4. Candidates

### 4.1 Panels

| Candidate | Active area (mm) | Outline W x H x T (mm) | Flex | Interface, driver | Backlight | Sleep | Zephyr 4.1 driver | Small-quantity source, price today | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **1.3 in 240 x 240 IPS, DM-TFT13-377p24 (LH133T-IF05 / ZJY133T-IF05)** | 23.4 x 23.4, pitch 0.0975 | 26.16 x 29.22 x 1.5 max | 24 x 0.5 mm plug-in, 12.5 mm wide, 14.93 mm long unfolded; folds under the module | 4-line SPI or 8080, ST7789VW | 2 white LEDs in parallel, VLED 2.8 to 3.0 V, 30 to 40 mA, 250 cd/m2 | VDD 15 uA + VDDIO 5 uA typ (30 + 10 max) | yes, `sitronix,st7789v` | DisplayModule USD 7.90, 60 available (variant JSON read today); Adafruit 4520 USD 12.50, 26 in stock (page read today) | **chosen** |
| 1.4 in 240 x 240 IPS, GLYF type (Yousee YX14011A has the same glass) | 25.2 x 25.2 | 28.0 x 31.35 x 1.65 | 15 x 0.5 mm (Yousee) or 20 x 0.5 mm (GLYF, pin table not found) | SPI, ST7789V | 3 LEDs parallel, 3.3 V, 60 mA (Yousee) | not read | yes | quotation only; DigiKey DLC0140AZP03SF-1 (USD 36.03) is a PCB breakout | rejected for batch 1: no single-unit source with a drawing; kept as the upgrade path (section 10) |
| 1.54 in 240 x 240 IPS, ZJY154KC-IF17 | 27.72 x 27.72 | 31.52 x 33.72 x 1.9 | 12 x 0.5 mm, 25.0 mm | SPI, ST7789V3 | 3 LEDs parallel, 60 mA (90 max) | 15 uA typ | yes | price not found; Adafruit 1.54 in is retired | rejected: needs a lens of about 34.7 mm, which breaks D2 and pushes the LCD toward the bay (D3) |
| 1.47 in 172 x 320, 1.69 in 240 x 280 (ST7789V2/V3) | portrait, about 17.4 x 32.4 and 28.0 x 32.6 (calculated, `geometry.md` 7.3) | outlines not read | various | SPI, ST7789 | not read | not read | yes | common on AliExpress, not verified | rejected: portrait breaks the square 4 x 4 mirror of the keys; 1.69 in is "tight" in the 37.8 mm envelope (`geometry.md` 7.3) |
| 1.9 in 170 x 320, 2.0 in 240 x 320 | 22.6 x 42.6 and larger | larger | various | SPI, ST7789 | not read | not read | yes | common | rejected: too tall for the column unless the buttons move (`geometry.md` 7.3) |
| AMOLED 1.64 in, 1.78 in, 1.91 in (QSPI; CO5300, SH8601, RM67162 class) | true black | about 1.0 mm thinner glass (not read) | QSPI flex | QSPI | none (emissive), current scales with lit pixels | low | **no**: Zephyr 4.1 has `rm67162` for MIPI DSI only; `chipone,co5300` with SPI/MSPI exists only on Zephyr main (file `display_co5300.c`, cached `04-zephyr/`) | modules on AliExpress, not verified | rejected: no driver in the pinned stack, the one nRF52840 QSPI is taken by the flash, larger frame buffers than 240 x 240, and the sizes are portrait or round |
| JDI LPM013M126C colour memory LCD | 176 x 176, 8 colours | not read | separate LCD and backlight flexes | SPI at 1 to 2 MHz | optional front/back light, 30 mA max | 2 uW static, 10 uW updating (datasheet 4.1) | **no**: `jdi,lpm013m126` is on Zephyr main only (2025 binding, cached) | not checked | rejected: 8 colours and 176 x 176 cannot show the icon grid; kept as an "always-on" idea |
| Sharp mono memory LCD (LS013B7DH03 class) | 128 x 128 mono | not read | 10-pin | SPI | none | microwatts | yes, `ls0xx` | common | rejected: monochrome fails D1 |
| GC9A01 round 1.28 in 240 x 240 | round | not read | various | SPI | not read | not read | yes, `gc9x01x` | common | rejected: round window does not match the GLYF and wastes corners of the icon grid |

### 4.2 Connection

| Option | Code, class, stock and price today | Height | Contacts | KiCad 10 stock footprint | Verdict |
| --- | --- | --- | --- | --- | --- |
| **Hirose FH34SRJ-24S-0.5SH(50)** | C324726, extended, 12,971 (JLCPCB), 12,735 (LCSC), USD 0.2461 | 1.0 mm | top **and** bottom, back-flip | no; draw from the datasheet pattern | **chosen**: dual contact removes the risk of a wrong contact side after the fold; lowest profile under the module |
| Jushuo AFC07-S24FCA-00 | C262567, extended, 46,028, USD 0.1311 | not read (datasheet download returned an HTML page) | not read | yes (`Jushuo_AFC07-S24FCA-00_1x24-1MP_P0.50_Horizontal`) | rejected: height and contact side not confirmed |
| Jushuo AFC01-S24FCA-00 | C262669, extended, 74,934, USD 0.1208 | 2.0 mm | bottom only (datasheet "翻盖下接 H2.0") | not found | rejected: bottom contact only and 1 mm taller |
| HC-FPC-05-09-24RLTAG | C5213757, extended, 43,806, USD 0.1321 | 1.0 mm | not read | no | runner-up second source if the FH34SRJ goes out of stock; contact side must be checked first |
| Hirose FH12-24S-0.5SH(55) | C202112, extended, 3,192, USD 0.5154 | 2.0 mm | bottom | yes | rejected: taller, dearer, one contact side |
| Molex 502244-2430 | C587894, extended, 94, USD 1.85 | not read | not read | yes | rejected: low stock, price |
| Solder-down flex (12-pin DM-TFT13-377p12) | panel USD 7.90 | none | soldered | n/a | rejected: hand soldering 0.5 mm flex on an assembled board; panel cannot be replaced |

Adafruit states for the same panel: "you'll need a 24-pin 0.5mm pitch bottom contact FPC connector" when the flex
is plugged in unfolded (https://www.adafruit.com/product/4520; confirmed). After a 180 degree fold under the
module the contacts face the other way. The FH34SRJ contacts on both sides, so both cases work (datasheet title
"Top and Top/Bottom Contact", ordering code "RJ: Top and Bottom contact"; confirmed).

### 4.3 Backlight drive

| Option | Parts | Verdict |
| --- | --- | --- |
| **Low-side N-MOSFET with series resistor, PWM** | AO3400A C20917 basic (VGS(th) 0.65 to 1.45 V, RDS(on) < 48 mOhm at 2.5 V), 15 Ohm 0402 C25083 extended, 100 kOhm C25741 basic | **chosen**: two parallel LEDs at 2.8 to 3.0 V need no boost; three parts |
| Constant-current LED driver IC | not chosen, so no part searched | rejected: the 3.3 V rail leaves only 0.3 to 0.5 V of headroom; a linear sink would drop out, and a boost driver adds an inductor and EMI for a 40 mA load |
| GPIO drives the LED directly | none | rejected: 30 to 40 mA exceeds nRF52840 high-drive GPIO limits; `mcu-radio.md` already says "drives a transistor" |
| NPN bipolar (MMBT3904 class) | not searched | rejected: needs a base resistor and wastes base current; the MOSFET is a basic part |

### 4.4 Cover lens

| Route | Who | Minimum | Thickness | Verdict |
| --- | --- | --- | --- | --- |
| **Laser-cut clear cast PMMA, underside painted black, window ablated** | any CO2 laser shop or makerspace (no catalogue supplier confirmed; PCBWay's laser-cut page does not list PMMA thickness, search summary) | 1 | 1.0 mm (+/- 0.1 typical sheet tolerance, guess) | **chosen** for the FDM prototype and the first aluminium batch; family convention (`macropad/cad/README.md`) |
| Printed tempered glass, 1.1 mm, from a glass maker | Saida Glass and similar | 100 pieces | 1.1 mm | rejected for batch 1; the volume route |
| Lens bonded by the display vendor (GLYF route) | GLYF's vendor (not found); DisplayModule offers no bonding service on its page | 5 (GLYF paid USD 210 for five) | 1.1 + 0.2 OCA | rejected: vendor unknown for this panel |
| CNC-machined and polished PMMA at JLCCNC | JLCCNC | 1 | 1.5 mm or more advised | rejected: thicker than the stack allows; no mask |
| Lens printed in clear resin at JLC3DP | not checked | 1 | - | rejected: optical clarity not proven |

## 5. Decision

The panel is the 1.3 inch DM-TFT13-377p24. It matches the GLYF in pixels and UI, it is the only 240 x 240 panel
with a public drawing and a plug-in flex that is buyable in units today, it fits the GLYF's 31.2 mm lens with a
wider (3.9 mm) black border, and it costs USD 7.90 against USD 42 for the GLYF's custom module. The active area
is 23.4 mm against 25.2 mm (86 % of the area). That is the price of single-unit availability. A second retail
source (Adafruit 4520) sells the same glass.

The lens stays at 31.2 mm square so that the top shell, the control column and the RF bay numbers already in
`mcu-radio.md` hold, and so that a later 1.4 inch panel needs only a new lens mask and a new module pocket.

## 6. Numbers the design needs

### 6.1 Panel data (DM-TFT13-377p24; drawing `_cache/display/09-dm-render/crop-flex.png`, datasheet `DM-TFT13-377P24.pdf`, ZJY133T-IF05 `_cache/display/05-alt-panels/adafruit-4520.pdf`; confirmed)

| Item | Value |
| --- | --- |
| Backlight outline | 26.16 +/- 0.2 (W) x 29.22 +/- 0.2 (H) mm, 1.5 mm max thick (1.30 mm body shown on the side view) |
| LCD glass | 25.80 x 25.80 mm; polariser 25.50 x 25.40 mm |
| Active area | 23.40 x 23.40 mm; 1.33 mm from the edge opposite the flex, about 1.38 mm from each side, so 4.49 mm from the flex edge (the active area is not centred along H) |
| Flex | 24 contacts, 0.5 +/- 0.03 mm pitch, 0.3 mm pads, contact span 11.5, tail width 12.5 +/- 0.1, contact length 3 +/- 0.3, stiffener 4 +/- 0.3 mm (PI, 0.3 +/- 0.05 mm total), tail end 14.93 mm from the module edge unfolded; tail offset 9.64 mm from the left module edge viewed from the front (not centred: the tail centre is 2.81 mm right of the module centre); pin 24 on the left, pin 1 on the right |
| Fold | Designed single-sided bend zone; folded flat, the bend stands out at most 0.8 mm and the tail end lies 12.8 +/- 0.5 mm in from the module edge; solder bumps on the flex back up to 0.45 mm, covered by 0.05 mm insulating tape |
| Supply | VDD 2.4 to 3.3 V (2.8 typ), VDDIO 1.65 to 3.3 V; IDD 8 mA typ, 10 mA max in normal mode |
| Sleep-in | VDD 15 uA typ (30 max), VDDIO 5 uA typ (10 max) |
| Backlight | 2 white LEDs in parallel, VLED 2.8 to 3.0 V, ILED 30 to 40 mA total, 200 to 250 cd/m2 |
| Viewing | IPS, all directions, normally black |
| Window advice | case window 0.5 mm per side larger than the active area: 24.4 mm |

Correction to `follow-display-module-sourcing.md` 5.1: "tail 12.8 +/- 0.5 mm from the module edge" is the
position of the tail end after the fold. Unfolded, the tail reaches 14.93 mm from the module edge.

### 6.2 Pin table and wiring (confirmed pin table; wiring is the decision)

| Pin | Symbol | Net |
| --- | --- | --- |
| 1 | LEDA | 3V3 through R_BL 15 Ohm |
| 2 | LEDK | Q_BL drain (AO3400A), source to GND |
| 3 | GND | GND |
| 4 | VDD | 3V3, 1 uF + 100 nF at the connector |
| 5 | VDDIO | 3V3 (tied to VDD) |
| 6 | IM1/2 | 3V3 (selects 4-line SPI) |
| 7 | RESET | P1.00 |
| 8 | CS | P0.14 |
| 9 | D/C (parallel name) | SCK, P0.13 |
| 10 | WR (parallel name) | DC, P0.16 |
| 11 | RD | GND |
| 12 | SDA | MOSI, P0.15 |
| 13 to 20 | DB0 to DB7 | GND |
| 21 | TE | test pad only (no Zephyr use) |
| 22 | NC | open |
| 23, 24 | GND | GND |

Backlight gate: P0.24 to the AO3400A gate directly, 100 kOhm gate to GND so the backlight stays off while the
bootloader leaves P0.24 floating. Declare a `pwm-leds` child on PWM0 channel 0, period 100 us (10 kHz), as chosen
`zmk,display-led`.

### 6.3 Electrical numbers (arithmetic on confirmed inputs)

| State | Panel logic | Backlight | Total |
| --- | --- | --- | --- |
| Full brightness | 8 mA typ (10 max) | (3.30 - 2.90) / 15 = 26.7 mA nominal; 22 mA at 3.234 V and VLED 2.9; 37.7 mA worst at 3.366 V and VLED 2.8 (inside the 40 mA rating) | about 35 mA typ, 48 mA max |
| Indoor level (PWM about 40 %) | 8 mA | about 11 mA average | about 19 mA (guess for the readable duty) |
| Idle, blanked, SLPIN hook active | 20 uA typ (40 max) | 0 (FET off; AO3400A IDSS 1 uA max at 30 V) | about 20 uA |

Resistor dissipation at worst case: 37.7 mA x 0.566 V = 21 mW, within 62.5 mW for 0402. The 3.3 V regulator
sees the MCU peak 51 mA max plus 38 mA backlight, 89 mA; the 150 mA rating in `mcu-radio.md` holds.

### 6.4 Mechanical stack (decision; inputs confirmed unless marked)

| Level | Z (mm from deck) | Above PCB top (mm) | Note |
| --- | --- | --- | --- |
| Deck and lens top | 0.00 | +6.20 | lens flush (0 to 0.05 below) |
| Lens underside | -1.00 | +5.20 | 1.0 mm PMMA, black paint on the underside |
| Lens recess floor | -1.15 | +5.05 | 0.13 mm adhesive ring, 1.5 mm wide, on the floor ring |
| Web underside (top of module pocket) | -1.75 | +4.45 | aluminium web 0.60 mm, window 24.8 mm square, centred on the lens |
| Module top (polariser) | -1.85 | +4.35 | 0.10 mm black tape frame, 0.5 mm wide, on the glass and polariser rim between 24.8 and 25.8 mm (the only band where web and glass overlap) |
| Module back | -3.35 | +2.85 | 1.5 mm max |
| Flex at the connector | about -5.65 | about +0.55 | FPC seated in the connector |
| Connector top | -5.20 | +1.00 | FH34SRJ, 1.0 mm |
| PCB top | -6.20 | 0 | |

Air gap lens to polariser: 0.85 mm (0.15 lens ring and allowance, 0.60 web, 0.10 tape frame); the Yousee drawing asks for at least
0.3 mm when the lens is not bonded. Total display height above the PCB top: 6.20 mm to the lens top, with the
module back 2.85 mm above the PCB and the connector 1.0 mm.

### 6.5 Plan positions (X from the right face, Y from the rear face)

| Item | X | Y | Note |
| --- | --- | --- | --- |
| Lens | 12.0 to 43.2 (centre 27.6) | 27.0 to 58.2 (centre 42.6) | GLYF positions plus the 8.0 mm widening |
| Lens recess | 11.9 to 43.3 | 26.9 to 58.3 | 31.4 mm square, R2.1 |
| Mask window and web window | mask 24.4 mm, web 24.8 mm, both centred on the lens | | the web edge hides behind the mask |
| Module (active area centred on the lens) | 14.52 to 40.68 | 29.57 to 58.79 | the module is offset 1.58 mm toward the front because its active area is off-centre |
| Module pocket | 14.2 to 41.0 (26.8 wide) | 29.4 to 59.1, then open to Y 61.8 for the bend | depth from Z -1.75 to the shell bottom |
| Flex bend | X 18.5 to 31.0 (12.5 wide) | 58.8 to about 61.0 | bend radius about 1.6 mm |
| Connector FH34SRJ-24S | 17.8 to 31.8 (14.0 wide, centred at X 24.8) | entry face about Y 51.8, body to about Y 48.0 | entry faces the front; set the Y position on a fold mock-up (risk 3) |
| Connector pin 1 | at the end nearest the right face (X 17.8) | | panel pin 1 (LEDA) sits on the right side of the tail; the fold keeps X |

Orientation: the panel is upright for the user with its flex toward the front (toward the round buttons). The
native ST7789 orientation then needs no rotation (likely; check MADCTL and the 80-line RAM offset on the first
board: the ST7789 RAM is 240 x 320, so a 180 degree rotation needs `y-offset = <80>`).

Clearances that follow: module X 14.52 is 1.17 mm outside the bay line X 13.35 (D3 holds; worst case with
tolerance 0.8 mm). Encoder bodies end at Y 21.6, 7.8 mm behind the module pocket. Button holes start at Y 64.95,
3.1 mm in front of the bend pocket.

## 7. Consequences for other subsystems

- **PCB:** FH34SRJ-24S on the **top** face (an exception to "all SMD on the bottom" in `keys.md`; JLCPCB must
  place top and bottom, which the BMD-340 on the bottom already requires). Project-drawn footprint from the Hirose
  pattern (0.3 x 0.8 mm pads at 0.5 mm pitch, two 3.3 mm-pitch mounting pads; datasheet page 4). Keep-out on the
  PCB top inside X 14.2 to 41.0, Y 29.4 to 61.8: nothing taller than 1.0 mm except the connector, and a free area
  of at least 12 x 10 mm at the rear of the module for the foam pad. AO3400A, 15 Ohm, 100 kOhm and the decoupling
  go on the bottom face.
- **Case (CNC):** lens recess 31.4 mm square, R2.1, 1.15 mm deep; web 0.60 mm with a 24.8 mm window; module pocket
  per 6.5, open from below; the shell material at X < 13.35 under the lens must end at Z -2.80 or higher
  (`mcu-radio.md` A7). FDM: recess 1.2 mm (6 layers), web 0.8 mm (4 layers).
- **Power:** the panel VDD maximum is 3.3 V. A regulator at 3.3 V +/- 2 % can reach 3.366 V; choose one with
  +/- 1 % output or accept the 2 % excursion (absolute maximum 4.6 V). Backlight 38 mA worst case on the 3.3 V rail.
- **Firmware:** `sitronix,st7789v`, width 240, height 240, inversion on (driver default), RGB565, on SPIM3 at
  16 MHz; `pwm-leds` as `zmk,display-led`; SLPIN hook from `mcu-radio.md` 7.7. Zephyr 4.1 driver confirmed in
  `zephyr/drivers/display/display_st7789v.c` (SLPIN 0x10 on PM suspend).
- **Assembly:** the panel, lens, tapes and foam are hand-fitted after JLCPCB assembly.

## 8. Bill of materials

| Role | Part | Code | Class, stock today | Price | Note |
| --- | --- | --- | --- | --- | --- |
| Panel | DisplayModule DM-TFT13-377p24 (LH133T-IF05) | not at LCSC | hand-fit | USD 7.90 | 60 available at DisplayModule; Adafruit 4520 USD 12.50, 26 in stock |
| FPC connector | Hirose FH34SRJ-24S-0.5SH(50) | C324726 | extended, 12,971 JLCPCB | USD 0.2461 | top face |
| Backlight switch | AO3400A, SOT-23 | C20917 | basic, 1,025,527 | USD 0.0789 | |
| LED resistor | 15 Ohm 1 % 0402 | C25083 | extended, 68,147 | USD 0.0011 | |
| Gate pull-down | 100 kOhm 0402 | C25741 | basic, 8,506,214 | USD 0.0011 | |
| VDD decoupling | 1 uF 0402 | C52923 | basic, 10,476,293 | USD 0.0057 | |
| VDD decoupling | 100 nF 0402 | C1525 | basic, 31,982,532 | USD 0.0024 | |
| Lens | 1.0 mm cast PMMA, 31.2 mm square, R2, painted underside | n/a | laser shop | not found | |
| Tapes, foam | 0.13 mm adhesive ring; 0.10 mm black tape frame; 3.0 mm open-cell foam pad, compressed to 2.85 mm | n/a | hand-fit | not found | product choice open (guess) |

KiCad 10.0.7 stock libraries: no FH34SRJ footprint (`Connector_FFC-FPC.pretty` holds FH12-24S and
Jushuo AFC07-S24 only); `Conn_01x24` generic symbol exists; `Transistor_FET` holds an AO3400A symbol;
`Package_TO_SOT_SMD:SOT-23` exists. The image ships no 3D model directory, so 3D models were not confirmed.

## 9. Can the display window be the antenna window?

No, not as drawn. The lens covers X 12.0 to 43.2, and only its outer 1.35 mm strip (X 12.0 to 13.35) lies over
the RF bay. Everything under the active part of the lens is the LCD module, whose backlight frame, reflector and
ITO layers block the signal. To make the window the exit, the design would need: (1) a lens extended to within
about 1.5 mm of the right face over Y 42.9 to 63.1, so a non-metal path exists above the full 9.4 mm bay (a lens
about 41 mm wide, which changes the GLYF look); (2) the black mask printed with a non-metallic ink; (3) the top
shell removed under the lens extension down to the PCB, not only to Z -2.80; (4) a range test against the wall
slot, because the antenna is on the PCB bottom face and radiates mostly through the board edge. The wall slot in
`mcu-radio.md` A9 does all of this with no change to the look, so it stays. The 1.35 mm lens strip over the bay is
a small bonus (non-metal above that part of the bay).

## 10. Risks

1. **Smaller active area (medium, accepted).** 23.4 mm against the GLYF's 25.2 mm, with a 3.9 mm black border
   instead of 3.0 mm. Upgrade path: a 1.4 inch 28.0 x 31.35 mm panel (Yousee YX14011A, quotation) needs a new
   module pocket and lens mask only; its flex (15 or 20 pins) needs a new connector footprint.
2. **Single shop (medium).** DisplayModule and Adafruit sell the same glass; AliExpress sellers are not verified.
   Buy 10 panels for 5 units.
3. **Flex path to a top-face connector (medium).** The drawing folds the flex flat against the module back; here
   it must drop 3.2 mm more. The connector Y position depends on the flex length tolerance (+/- 0.5 mm) and the
   bend radius. Make a fold mock-up with a real panel and a printed spacer before the PCB is released; the
   connector entry is placed about 7 mm in from the module front edge (guess until the mock-up).
4. **Panel VDD at its maximum (low).** 3.3 V supply against a 3.3 V maximum rating.
5. **Backlight brightness spread (low).** The resistor sets 22 to 38 mA depending on VLED and the rail; PWM
   evens it out in use.
6. **SPI clock (low).** 16 MHz is 6 % above the ST7789V 66 ns write cycle; 8 MHz is the in-spec fallback
   (`mcu-radio.md` 7.5).
7. **Acrylic lens (low).** Scratches more easily than glass; thickness tolerance of cast sheet is about
   +/- 10 % (guess), absorbed by the 0.15 mm recess allowance. Glass is the volume route.
8. **Connector contact side (resolved).** Dual-contact FH34SRJ.

## 11. Sources

- DisplayModule product JSON, read 2026-11-13: `_cache/display/06-dm-live/dm13.js`
  (https://www.displaymodule.com/products/1-3-inch-ips-display-240x240-with-spi); datasheet
  `_cache/follow-display-module-sourcing/04-stock-panels/DM-TFT13-377P24.pdf`, drawing page rendered to
  `_cache/display/09-dm-render/p4-half.png` and `crop-flex.png`.
- ZJY133T-IF05 (LH133T-IF05) specification from Adafruit: `_cache/display/05-alt-panels/adafruit-4520.pdf`;
  https://www.adafruit.com/product/4520 (price, stock, connector note).
- JDI LPM013M126C specification: `_cache/display/05-alt-panels/LPM013M126C.pdf`.
- Hirose FH34SRJ datasheet: `_cache/display/03-datasheets/FH34SRJ.pdf`
  (https://www.lcsc.com/datasheet/lcsc_datasheet_1811071030_HRS-Hirose-FH34SRJ-24S-0-5SH-50_C324726.pdf).
- Jushuo AFC01 datasheet: `_cache/display/03-datasheets/AFC01.pdf`; HC-FPC-05-09: `_cache/display/03-datasheets/HC-FPC-05-09.pdf`.
- AO3400A datasheet: `_cache/display/03-datasheets/AO3400A.pdf`
  (https://www.lcsc.com/datasheet/lcsc_datasheet_1811081213_Alpha---Omega-Semicon-AO3400A_C20917.pdf).
- JLCPCB parts API queries, 2026-11-13: `_cache/display/01-jlc/`, `_cache/display/07-jlc-final/`; LCSC product
  detail: `_cache/display/02-lcsc/`.
- Zephyr 4.1 sources in `/home/worxbend/Projects/worxboard/build/fw-ws/zephyr` (`drivers/display/`,
  `dts/bindings/display/sitronix,st7789v.yaml`); Zephyr main listing and CO5300 / LPM013M126 files:
  `_cache/display/04-zephyr/`.
- KiCad 10.0.7 image `kicad/kicad:10.0.7`, `/usr/share/kicad/footprints/Connector_FFC-FPC.pretty`.
- Project notes: `research/raw/follow-display-module-sourcing.md`, `geometry.md`, `conventions.md`;
  `research/components/mcu-radio.md`, `keys.md`.

## 12. Not checked

- AFC07-S24FCA-00 datasheet (LCSC returned an HTML page instead of the PDF).
- Hirose's recommended FPC width for 24 contacts (the table row was not read); the panel tail is 12.5 +/- 0.1 mm.
- Outlines of the 1.47, 1.69, 1.9 and 2.0 inch panels and the AMOLED modules (rejected on fit or driver first).
- BuyDisplay and AliExpress stock (blocked or not read earlier).
- Lens supplier price.
