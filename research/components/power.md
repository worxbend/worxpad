# Power subsystem: battery, charging, power path, 3.3 V rail, fuel gauge, power switch

Date: 2026-11-13
Key: `power`
Status: decision record, revision 1.

Cache: `research/_cache/power/` (gitignored). Batches: `ds-01/` and `ds-02/` (datasheets), `jlc-01/` and `jlc-02/`
(JLCPCB parts-library answers), `lcsc-01/` and `lcsc-02/` (LCSC product details), `zmk-01/` (ZMK sources),
`cell-02/` (EEMB cell specification). `cell-01/` holds two empty files from a failed earlier download and can be
ignored.

Confidence words: confirmed (stated by the maker or read from a primary source), likely (consistent indirect
evidence), guess.

## 1. Decision in short

1. **Cell:** a single-cell LiPo pouch with its own protection board (PCM), 4.3 mm class, 42.5 x 63 mm, 1,000 to
   1,200 mAh, with a 2-pin JST PH 2.0 plug. The production cell is the EEMB LP404261-PCM-LD (1,000 mAh,
   4.3 x 42.5 x 63 mm maximum). The bring-up cell is the Adafruit 258 (1,200 mAh, 5.0 x 34 x 62 mm, JST PH,
   in stock). The pocket accepts both.
2. **Charger and power path:** TI **BQ24072RGTR** (C140288), a linear charger with dynamic power-path management.
   Its system output tracks the battery (VBAT + 225 mV) while USB is present. The input is set to USB500 mode. The
   charge current is set to **about 400 mA** (RISET 2.2 kOhm). A 10 kOhm B3950 NTC on the board feeds TS. The
   pin-compatible **BQ24075RGTR** (C15464, 27,184 in stock) is the drop-in fallback.
3. **3.3 V rail:** TI **TPS7A0233PDBVR** (C2887324), a 200 mA LDO with 25 nA quiescent current and 6.0 V input
   rating. A buck or buck-boost converter gains less than 5 % here and is rejected.
4. **Battery measurement:** Analog Devices (Maxim) **MAX17048G+T10** (C2682616), an I2C ModelGauge fuel gauge at
   0x36. The pinned ZMK has the driver `zmk,maxim-max17048`. A resistor divider is rejected.
5. **Power switch:** an SMD side-actuated slide switch **MSK12C02** (C431540) on the **enable pin of the LDO**. It
   is not in the battery line. Off means the 3.3 V rail is down, the cell draws about 8 uA, and USB still charges.
   ZMK deep sleep and soft-off stay available in firmware.
6. **On-board protection:** reverse-polarity P-MOSFET **AO3401A** (C15127, JLCPCB basic) in the battery line, the
   charger's own 6.6 V input OVP, thermal regulation and safety timers, the NTC, and the pack PCM.
7. **Indication:** /CHG and /PGOOD from the charger go to two GPIOs with internal pull-ups, and the gauge gives
   the state of charge. Charging shows on the display. There is no LED, because a closed aluminium body would hide it.

## 2. Context

- The GLYF states a "1,200 mAh Li-Ion" battery (`research/raw/official-site.md`, confirmed). Its sample cell is the
  custom pack DTP404257, 4.0 x 42 x 57 mm, with a PCM, two wires and a small plug of about 1.25 mm pitch
  (`research/raw/follow-battery-cell-and-runtime.md` section 2, confirmed label, likely size). The cell sits in a
  pocket of about 43 x 74 mm, 9 to 53 mm from the rear face, under the rear key rows where the wedge thickens the
  body (same file, section 3, likely).
- The GLYF uses a MAX17048 gauge at 0x36 (`research/raw/regulatory-software.md`, confirmed from firmware strings),
  a linear power-path charger in a 3 x 3 mm QFN-16 with the best fit in the TI BQ2407x family, an XC6220-class
  3.3 V LDO and an MSK12C02-type slide switch at the rear edge (`research/raw/follow-maker-bom-part-numbers.md`;
  charger family likely, LDO and switch likely). Its backlight is on or off with no PWM dimming
  (`follow-battery-cell-and-runtime.md` section 8, likely).
- Settled earlier and binding here: nRF52840 on the BMD-340-A-R in LV mode with a single 3.3 V rail into VCC and
  VCCH. MCU subsystem peak current 44 mA typical, 51 mA maximum, including panel logic and flash. The regulator must
  supply at least about 110 mA with the backlight, so it is rated at 150 mA or more. Connected idle is about 44 uA
  typical with the two worxpad power hooks, and deep sleep is about 21 uA typical
  (`research/components/mcu-radio.md` sections 7.6 and 8). Pin plan: charger status P0.03, gauge interrupt P0.26,
  I2C SDA P0.07 and SCL P0.11, battery ADC P0.05 only if there is no gauge.
- Settled earlier and binding here: all SMD parts and sockets sit on the PCB bottom. PCB bottom face at Z -7.80
  below the deck. Socket undersides at Z -9.65. A 2.15 mm clear depth below the PCB under each socket zone
  (Z -9.95). The battery fits only outside the socket zones or below that depth (`research/components/keys.md`,
  interfaces).
- The display panel is not settled yet. Backlight figures in hand: 60 mA at 3.3 V for the 1.4 inch same-glass
  panel (3 LEDs in parallel), 30 to 40 mA at 2.8 to 3.0 V for the 1.3 inch DM-TFT13-377
  (`research/raw/follow-display-module-sourcing.md`, confirmed per panel). This record sizes for the 60 mA case.

## 3. Requirements

| # | Requirement | Source |
| --- | --- | --- |
| P1 | A work week (5 days) on one charge with the display lit 4 hours a day at a usable brightness, and weeks of connected standby. | task; GLYF class |
| P2 | Rail current at least 111 mA (51 mA MCU subsystem maximum plus a 60 mA backlight). Rate the regulator at 150 mA or more. | `mcu-radio.md` section 8 |
| P3 | Charge from USB-C without Power Delivery negotiation, so the input draws at most 500 mA. | USB 2.0 default power (judgement) |
| P4 | Charging and running at the same time (power path), and booting at once on USB with an empty cell. | task |
| P5 | Cell in a slim body, outside the RF bay, accessible and unpluggable. | `mcu-radio.md` A6; prior-art complaints (`prior-art.md`) |
| P6 | True off for storage and shipping, and charging still works while off. | task; GLYF slide switch |
| P7 | Battery level on the display and in the Bluetooth Battery Service with the pinned ZMK. | task; `mcu-radio.md` |
| P8 | Parts JLCPCB can place, with stock for 5 units today. The cell is fitted by hand. | task; JLCPCB does not process consigned batteries (`follow-battery-cell-and-runtime.md` section 9, confirmed) |
| P9 | Charge only between 0 and 45 to 50 degC, with the charge current inside the cell and PCM ratings. | cell specifications (section 5) |

## 4. Current budget

### 4.1 Inputs

| Load | Value | Source | Confidence |
| --- | --- | --- | --- |
| MCU subsystem, deep sleep (System OFF, panel SLPIN, flash DPD) | 21 uA typ, 61 uA max | `mcu-radio.md` 7.6 | confirmed inputs, guess total |
| MCU subsystem, connected idle, display blanked, with the worxpad hooks | 44 uA typ, 83 uA max | `mcu-radio.md` 7.6 | same |
| MCU subsystem, connected idle without the hooks | unknown, likely milliamperes (ST7789V DISPOFF current not given) | `mcu-radio.md` 7.6 | not found |
| MCU subsystem peak (icon upload over BLE) | 44 mA typ, 51 mA max, including panel logic 6.0/7.5 mA | `mcu-radio.md` 7.6 | confirmed inputs |
| Panel logic while lit | ST7789V normal mode 6.0 mA typ, 7.5 mA max; 1.3 inch module 8 mA typ, 10 mA max | `follow-battery-cell-and-runtime.md` 6 | confirmed |
| CPU and SPI while LVGL draws | 1 to 3 mA average | none measured | guess |
| BLE link while typing (7.5 ms interval) | about 0.6 mA (nRF52840 model output 297 uA at 15 ms, doubled) | Nordic Online Power Profiler via `follow-battery-cell-and-runtime.md` 6 | likely |
| Key held, matrix scanning | 315 uA | ZMK `power.js` via `follow-battery-cell-and-runtime.md` 6 | confirmed (ZMK value) |
| Backlight at 100 % | 60 mA (1.4 inch, 3 LEDs) or 35 mA (1.3 inch) | `follow-display-module-sourcing.md` | confirmed per panel |
| Charger BQ24072, battery only | 4.3 uA typ, 6.5 uA max (IBAT(PDWN), input absent, no load) | `ds-01/bq24074.txt` lines 607-610 | confirmed (sleep figure; assumed to hold while OUT is loaded, guess) |
| LDO TPS7A02, on / shut down | 25 nA typ / 3 nA typ | `ds-01/tps7a02.txt` lines 4-9, 319 | confirmed |
| Gauge MAX17048 | active 23 uA typ, 40 max; hibernate 3 uA typ; sleep 0.5 uA typ, 2 max | `_cache/follow-battery-cell-and-runtime/ds-07/max17048_sf.pdf` lines 94-102 | confirmed |
| Pack PCM | 3 uA typ, 7 uA max (EEMB LP404261-PCM-LD) | `cell-02/LP404261.txt` section 6.1 | confirmed (for that pack) |

Battery current equals rail current, because the LDO passes its load current straight through.

### 4.2 Budget by state (battery current)

Fixed overhead with the switch on and no USB: charger 4.3 + gauge in hibernate 3 + PCM 3 + LDO 0.03 = **about
10 uA typ** (6.5 + 5 + 7 + 0.05 = about 19 uA max; the 5 uA gauge maximum in hibernate is a guess).

| State | Current, typ (max) | Note |
| --- | --- | --- |
| Off (slide switch off, rail down) | **about 8 uA** (charger 4.3 + gauge sleep 0.5 + PCM 3) (16 uA) | The I2C pull-ups lose their supply, SDA and SCL fall, and the gauge enters sleep after 2.5 s (datasheet note 6, confirmed). |
| Deep sleep (System OFF, link dropped) | **31 uA** (80 uA) | 21 + 10 |
| Connected idle, display blanked, hooks in place | **54 uA** (102 uA) | 44 + 10 |
| Connected idle without the hooks | unknown, likely 1 to 6 mA | The power hooks in `mcu-radio.md` 7.7 are a requirement of this budget. |
| Display lit, backlight off (dim UI or e.g. reading) | **about 9 mA** (7 to 12) | 6 panel + 2 CPU + 0.6 BLE + 0.3 scan |
| Display lit, 1.4 inch panel, backlight 100 / 50 / 25 / 10 % | **69 / 39 / 24 / 15 mA** | 9 + 60 x duty |
| Display lit, 1.3 inch panel, backlight 100 / 50 / 25 / 10 % | **44 / 27 / 18 / 12.5 mA** | 9 + 35 x duty |
| Peak, rail | **111 mA** (51 + 60) | sizing value for the LDO and the PCM |

PWM duty is a proxy for brightness. LED light output is close to linear in current, so 25 % duty gives roughly a
quarter of full brightness (guess for the panels in question, not measured).

### 4.3 Runtime and capacity

Usable capacity is taken as 85 % of rated capacity, the ZMK profiler factor. That gives 850 mAh for 1,000 mAh and
1,020 mAh for 1,200 mAh.

| Case | 1,000 mAh (850 usable) | 1,200 mAh (1,020 usable) |
| --- | --- | --- |
| Display lit continuously, 1.4 inch, 100 % | 12.3 h | 14.8 h |
| Same, 50 % | 21.8 h | 26.2 h |
| Same, 25 % | 35.4 h | 42.5 h |
| Same, 10 % | 56.7 h | 68 h |
| Connected idle with hooks (54 uA) | about 650 days on paper | about 790 days on paper |
| Day of 4 h lit at 25 % plus 20 h connected idle (97 mAh/day) | **8.8 days** | **10.5 days** |
| Day of 4 h lit at 50 % plus 20 h idle (157 mAh/day) | **5.4 days** | **6.5 days** |
| GLYF-like day: 4 h lit at 100 %, no dimming (277 mAh/day) | 3.1 days | 3.7 days |

In the standby rows, cell self-discharge is the real limit: a few percent a month, so months, not years. Every value
in this table is arithmetic on datasheet currents and a guessed CPU share, not a measurement.

Capacity choice: P1 (5 days, 4 h a day at 50 %) needs 157 x 5 = 785 mAh usable, so about 920 mAh rated. A 1,000 mAh
cell meets P1. A 1,200 mAh cell gives 20 % margin. A 4.3 mm cell of 42.5 x 63 mm holds 1,000 to 1,400 mAh (section 5),
so the body thickness, not the budget, sets the size. PWM dimming does more for runtime than any cell that fits.

## 5. Cell

### 5.1 Candidates

| Cell | Size T x W x L, mm (pack maximum) | Capacity | PCM | Plug | Seller and availability | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **EEMB LP404261-PCM-LD** | 4.3 x 42.5 x 63; wires 50 +/-3 mm, AWG26 | 1,000 mAh (950 min) | yes: overcharge 4.28 +/-0.05 V, release 4.175 V; over-discharge 3.0 +/-0.1 V, release 3.5 V; 0.5 A continuous, 1 A for 3 s; short-circuit; RDS <= 70 mOhm; 3/7 uA | Molex 5264-0200 in the drawing, marked "kind in prevail" (connector set by the order, likely) | EEMB, request for quotation (https://www.eemb.com/products-55, https://www.eemb.com/product-219); stock not confirmed | **Chosen for production.** Closest catalogue match to the GLYF cell, and the only one found with a full datasheet. Order it with a JST PHR-02 plug and the polarity of section 7.4. |
| **Adafruit 258** | 5.0 x 34 x 62 | 1,200 mAh | yes, cut-off 3.0 V, short-circuit | JST PH 2.0, cable rated 2 A | adafruit.com, in stock, USD 9.95 (read 2026-11-13) | **Chosen for bring-up and the FDM prototype.** Retail stock and the right plug; 0.7 mm thicker. |
| Lipol LP404060 | 4.0 x 40 x 60 | 1,400 mAh | not stated | not stated | lipolbattery.com catalogue, quotation only (`follow-battery-cell-and-runtime.md` 5) | Alternative if EEMB lead time is too long. No datasheet read. |
| DTP404257 (GLYF) | 4.0 x 42 x 57 | 1,200 mAh | yes | about 1.25 mm pitch | custom item, minimum order 3,000 | Rejected: not sold in small numbers. |
| Olimex BATTERY-LIPO1400mAh | 8 x 34 x 50 | 1,400 mAh | yes | JST, pitch not stated | olimex.com, in stock, EUR 5.95 | Rejected: 8 mm thick. |
| LP503562 / LP503759 class | 5.0 x 35-37 x 59-62 | 1,200-1,250 mAh | usually | JST PH from retailers | several retailers | Same envelope as the Adafruit cell. Acceptable substitute. |
| LP603450, LP653450 | 6.0-6.5 x 34 x 50 | 1,200-1,300 mAh | usually | JST PH | many | Rejected: need a body of 17.1 to 17.65 mm under the sockets. |

Cell ratings for the charger (EEMB LP404261, `cell-02/LP404261.txt` sections 2 and 6, confirmed): charge 4.200 +/-
0.020 V, maximum charge current 1,000 mA (1 C), end-of-charge current 20 mA, maximum discharge 2,000 mA, charge
temperature 0 to 45 degC, discharge -20 to +60 degC, impedance <= 80 mOhm, mass about 20 g, 500 cycles at 0.5 C. The
PCM, not the cell, limits continuous current to 0.5 A, and that limit sets the charge current in section 6.4.
Adafruit 258 (https://www.adafruit.com/product/258, confirmed): 23 g, charge at 500 mA or less, no thermistor.

Neither pack has a thermistor lead, so the NTC goes on the PCB (section 6.4).

### 5.2 Pocket envelope (for the case subsystem)

Stack under the key field, from the settled key stack (`keys.md`): PCB bottom Z -7.80; socket undersides Z -9.65;
socket keep-out depth 2.15 mm below the PCB, Z -9.95.

| Layer | Thickness | Z after the layer, 5.0 mm class | Z after the layer, 4.3 mm class only |
| --- | --- | --- | --- |
| Socket keep-out (from PCB bottom) | 2.15 | -9.95 | -9.95 |
| Insulating sheet over the socket bodies (polyimide or PET, 0.3 mm) | 0.30 | -10.25 | -10.25 |
| Cell plus 10 % swelling allowance | 5.50 / 4.73 | -15.75 | -14.98 |
| Foam or double-sided tape under the cell | 0.20 | -15.95 | -15.18 |
| Pocket floor (CNC aluminium) | 1.50 | **-17.45 underside** | **-16.68 underside** |

- Plan: **45.0 x 66.0 mm** (both cells plus at least 1.0 mm a side), corner radii at least 1.5 mm, long side
  along X under key columns 1 to 4, plus a wire relief of about 15 x 12 mm at the end next to the battery connector.
- Depth: floor top at **Z -15.95** to take both cells. If the case cannot reach a 17.45 mm underside over the whole
  pocket, use **Z -15.18** (4.3 mm class only; the Adafruit cell then needs a thinner print floor in the prototype).
- Position: under the rear key rows, inside the wedge zone, like the GLYF (9 to 53 mm from the rear face there).
  Nowhere inside the RF bay (`mcu-radio.md` A6). The case subsystem checks the wedge profile against these Z values.
- The 1.5 mm floor is the case subsystem's value. Each 0.1 mm less floor or swelling allowance raises every Z above
  by 0.1 mm.

## 6. Charger and power path

### 6.1 Candidates

| Part | LCSC, class, stock (2026-11-13) | Power path | Settings | Battery drain, no input | Firmware need | Package | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **TI BQ24072RGTR** | C140288, extended, 1,216 (JLCPCB), 1,216 (LCSC), USD 1.06 | yes, DPPM; OUT = VBAT + 225 mV with input, battery supplement | resistors: ISET, ILIM, EN1/EN2, TMR, TS | 4.3 / 6.5 uA | none | VQFN-16 3 x 3, EP | **Chosen** |
| TI BQ24075RGTR | C15464, extended, 27,702 (JLCPCB), 27,184 (LCSC), USD 1.07 | yes; OUT fixed at 5.5 V with input; SYSOFF | same | 4.3 / 6.5 uA | none | same footprint | **Fallback, drop-in.** Pin 15 is SYSOFF instead of TD; both are tied to GND here, so the board is the same. OUT up to 5.6 V raises LDO loss on USB to about 0.25 W. |
| TI BQ24073RGTR | C15220, extended, 500 | yes; OUT fixed at 4.4 V | same | same | none | same | Acceptable; thinner stock. |
| TI BQ25180YBGR | C3682423, extended, 3,593, USD 1.87 | yes | I2C only; ICHG_CTRL resets to 0x05, i.e. 10 mA (datasheet line 1783 and 2241, likely) | 3 uA; ship mode 15 nA | needs a charger driver; Zephyr has `charger_bq25180.c`, ZMK does not use it | DSBGA-8, 0.4 mm-class pitch | Rejected: a firmware-dependent charge current is a failure mode on a dead board, and the BGA adds layout risk. Its ship mode is not needed with the switch of section 8. |
| TI BQ25185DLHR | C19725033, 0 stock | yes; button ship mode | resistor | 4/5 uA | none | WSON-10 | Rejected: no stock. |
| Nordic nPM1300 | C25346894 (JLCPCB 191, LCSC 0); QFN variants 0 | yes, plus two bucks, fuel gauging in software | I2C | low | Nordic fuel-gauge library from nRF Connect SDK; not in ZMK | WLCSP-35 | Rejected: brings an NCS dependency into a ZMK build, WLCSP only in stock. |
| Microchip MCP73871T-2CCI/ML | C511310, extended, 4,241, USD 2.13 | yes, load sharing | resistors | not checked | none | QFN-20 4 x 4 | Rejected: twice the price and larger, no gain over BQ2407x. |
| MCP73831T-2ACI/OT or TP4057 plus load-share P-MOSFET and Schottky | C424093 (8,854) / C12044 (preferred extended, 26,420) | only with extra parts | resistor | low | none | SOT-23-5 / -6 | Rejected: no NTC input on TP4057, no input current limit, the load-share network drops 0.3 to 0.5 V and needs three more parts. |

### 6.2 Why BQ24072

It is the GLYF's probable family, needs no firmware, limits input current to USB500, boots the system from USB with an
empty or missing cell, and has an NTC input, safety timers and 125 degC thermal regulation. Against the BQ24075 it
keeps OUT near the battery voltage on USB (at most about 4.5 V), so the LDO dissipates less, and the LDO never sees
more than 4.5 V. Stock is 1,216, enough for 5 boards. If it runs out, the BQ24075 fits the same footprint, nets and
values.

### 6.3 Pins and values

Pin numbers are for the RGT package (`ds-01/bq24074.txt` table 7-1, confirmed).

| Pin | Connection | Value and reason |
| --- | --- | --- |
| IN (13) | VBUS after the usb-io protection | 1 uF 50 V X5R 0603 to GND (C15849, basic). Input 4.35 to 6.6 V; survives 26 V with operation suspended (confirmed). |
| OUT (10, 11) | VSYS: LDO input and gauge-free loads | 10 uF 10 V X5R 0603 (C19702, basic); datasheet range 4.7 to 47 uF (confirmed). |
| BAT (2, 3) | cell via the reverse-polarity FET (section 9) | 10 uF 0603 (C19702). |
| EN2 (5) | GND | USB500 with EN1 high. |
| EN1 (6) | 100 kOhm (C25741, basic) from IN | EN1 high only when USB is present. With the internal 285 kOhm pull-down it sits at about 3.7 V on 5 V and stays under the 7 V absolute maximum up to about 9.4 V on VBUS. Input limit 450 / 475 / 500 mA (min/typ/max, confirmed). |
| ILIM (12) | 3.3 kOhm (C25890, basic) to GND | Not used in USB500 mode, but "leaving ILIM unconnected disables all charging" (confirmed). 3.3 kOhm gives about 460 mA if EN1/EN2 are ever restrapped to ILIM mode. |
| ISET (16) | **2.2 kOhm 1 %** (C25879, basic) to GND | ICHG = KISET / RISET = 797 / 890 / 975 AOhm over 2.2 kOhm = **362 / 405 / 443 mA**. Pre-charge = 88 / 2,200 = 40 mA. Termination at 10 % = about 40 mA. |
| TS (1) | NTC 10 kOhm, B 3950, 0805 (CMFB103F3950FANT, C51597, extended, 30,680 at LCSC) to GND | The TS window is 0 and 50 degC for a Vishay curve-2 NTC (confirmed). A B3950/4021 part is close to that curve; a B3380 part (Murata NCP15XH103) would move the window to about -4 and 55 degC (calculated). |
| TMR (14) | open | Default timers: pre-charge 30 min, fast charge 5 h (confirmed). A 1,200 mAh cell at about 400 mA needs about 3.5 h. |
| TD (15) on BQ24072 / SYSOFF (15) on BQ24075 | GND | Termination enabled / battery FET on. Same net for both parts. |
| CE (4) | GND | Always enabled. |
| /CHG (9) | P0.03, internal pull-up | Low while charging. The pull-up costs 254 uA only while charging, when USB powers the board. |
| /PGOOD (7) | **P0.04** (new claim on a spare pin), internal pull-up | Low while USB input is valid. Gives a firmware-visible VBUS signal independent of the USB stack. |
| VSS (8), thermal pad | GND, with at least 5 thermal vias 0.3 mm into a copper pour | |

### 6.4 Charge current and thermal notes

- **Charge current about 400 mA (362 to 443 mA).** This is 0.40 C for 1,000 mAh and 0.34 C for 1,200 mAh. It stays
  under the EEMB PCM's 0.5 A continuous limit at the worst-case KISET and under Adafruit's "500 mA or less". The
  USB500 input limit caps the total at 500 mA anyway, so a lit display slows charging slightly. Expected charge time
  from empty is about 3 to 3.5 hours (judgement from a constant-current share of about 75 %).
- Charger dissipation, USB at 5.0 V, cell at 3.6 V, system at 115 mA: input FET (5.0 - 3.83) V x 0.475 A = 0.56 W,
  plus charge FET 0.225 V x 0.405 A = 0.09 W, so **about 0.65 W** at the start of constant-current charge, falling
  to about 0.4 W at 4.1 V. With RthJA 44.5 K/W (JEDEC board, confirmed) the junction is about 29 K above the board,
  or about 40 K on this smaller board (guess). Thermal regulation at 125 degC reduces current before damage.
- LDO dissipation on USB: (4.45 - 3.3) V x 0.115 A = 0.13 W, about 25 K rise at 180 to 200 K/W (confirmed RthJA).
  On battery it is below 0.1 W.
- **Inside the closed aluminium case:** total heat while charging with the display lit is at most about 0.9 W. Spread
  over an aluminium shell of about 0.03 m2 with natural convection (h about 8 to 10 W/m2K) the whole body warms by
  about 3 to 4 K (estimate). The risk is local: the cell must stay below 45 degC while charging.
  - Place the charger at least 10 mm from the pocket edge in plan and never over the cell.
  - Do not put the charger and the LDO next to each other.
  - Optional: a 1.0 mm thermal gap pad from the charger's PCB area to the aluminium floor (case subsystem decides).
  - Mount the NTC over the cell, on the PCB bottom, between socket zones, within the pocket outline. An 0805 is
    1.25 mm thick, inside the 2.15 mm clear depth. It sees the cell through the 0.3 mm insulator.

## 7. 3.3 V rail

### 7.1 Candidates

| Part | LCSC, class, stock | Iout | Iq / shutdown | VIN max | Dropout at load | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **TI TPS7A0233PDBVR** | C2887324, extended, JLCPCB 5,309, LCSC 1,871, USD 1.14 | 200 mA (limit 240 to 750 mA) | 25 nA / 3 nA | 6.0 V | 310 mV max at 200 mA for 3.3 V; about 170 mV at 111 mA (scaled) | **Chosen.** Lowest standby loss, takes the BQ24075 fallback's 5.6 V. |
| Richtek RT9080-33GJ5 | C841192, extended, 30,941, USD 0.12 | 600 mA | 2 uA / 0.1 uA | 5.5 V recommended | 0.31 V at 600 mA | Runner-up: ten times cheaper, 2 uA more; rejected only because the BQ24075 fallback's OUT reaches 5.6 V. With the BQ24072 it would also work. |
| Torex XC6220B331MR (GLYF's probable LDO) | C86534 etc., extended, about 10,000 each | 700 mA (1 A) | about 8 uA | 6.0 V | 20 mV at 100 mA | Rejected: 8 uA is 15 % of the connected-idle budget. |
| Microchip MCP1700T-3302E/TT | C39051, 963 | 250 mA | 1.6 uA | 6.0 V | 178 mV at 250 mA | Rejected: no enable pin, so the switch cannot act on it. |
| TI TPS62840 buck | C2071139 DSBGA 2,961 / C2071859 VSON 1,748 | 750 mA | 60 nA | 6.5 V | buck | Rejected: at 3.8 V average cell voltage an LDO is 87 % efficient; the buck gains under 5 % of display-on time, adds an inductor and a BGA or USD 4.22 part. |
| Buck-boost (TPS63802 class) | not queried | | | | | Rejected: it would keep 3.3 V below a 3.4 V cell, where less than about 10 % of capacity remains, at higher quiescent current and cost. |

### 7.2 Behaviour at low cell voltage

On battery the BQ OUT pin follows the cell minus a few millivolts, and the LDO drops out below about 3.45 V. Then
the rail follows the cell down. Every load still works: nRF52840 down to 1.7 V, W25Q128JV down to 2.7 V, ST7789V
VDD down to 2.4 V (`mcu-radio.md`). The pack PCM cuts off at 3.0 V. Backlight brightness falls as the rail sags if
the LEDs are fed from the 3.3 V rail through a resistor. Firmware warns at 10 % state of charge and may enter
soft-off at 3 %.

### 7.3 Values

IN: 1 uF (C15849). OUT: 1 to 22 uF required (`ds-01/tps7a02.txt` line 259, confirmed). Use 4.7 or 10 uF at the LDO
and keep the **total ceramic capacitance on the 3.3 V net at or under 22 uF**, including module, flash and display
decoupling. EN: from the slide switch (section 8). Pin order DBV: IN 1, GND 2, EN 3, NC 4, OUT 5 (confirmed). The
"P" suffix adds an active output discharge, so the rail falls quickly when switched off.

## 8. Power switch

| Option | Off current | Charges while off | Switch current | Verdict |
| --- | --- | --- | --- | --- |
| **Slide switch on LDO EN** (SPDT: common to EN, one throw to VSYS, other to GND) | about 8 uA (section 4.2) | yes, the charger is untouched | nanoamperes | **Chosen** |
| Slide switch in series with the cell (likely the GLYF) | PCM only | no | up to 0.44 A charge and 0.11 A load | Rejected: MSK12C02 is rated 50 mA at 12 V DC (datasheet section 2.5, confirmed), and charging stops while off. |
| Slide switch on BQ24075 SYSOFF | about 5 uA | no: "When an adapter is connected, charging is also disabled" (confirmed) | none | Rejected: off plus USB runs the board but never charges. |
| Soft latch (push button plus MOSFET latch) | about 1 uA | yes | | Rejected: more parts and another opening. ZMK soft-off covers the use. |
| Charger ship mode (BQ25180/BQ25185) | 15 nA | depends | | Rejected with those chargers (section 6.1). |
| Firmware only (ZMK soft-off, no switch) | 31 uA plus overhead | yes | | Kept as an extra, not as the only off. |

Behaviour: switch on, no USB: runs from the cell. Switch on, USB: runs from USB, charges, ZMK skips deep sleep.
Switch off, USB: the board is dark and the cell charges. Switch off, no USB: about 8 uA.

Part: Shouhan **MSK12C02** (C431540, extended, 172,615 at JLCPCB, USD 0.054). SPDT, rated 12 V DC 50 mA, travel 1.6
+/-0.2 mm, operating force 150 +/-100 gf, one reflow at 260 degC peak (`ds-02/msk12c02.pdf`, confirmed). Footprint
(KiCad `SW_SPDT_Shouhan_MSK12C02`): body 6.7 x 2.8 mm on the fabrication layer, contact pads at X -2.25, +0.75,
+2.25, four shield tabs at X +/-3.675, two 0.85 mm NPTH locating pegs at X +/-1.5 (confirmed from the library file).
Body height about 1.5 mm and actuator reach beyond the body edge about 1.4 mm (LCSC attribute "1.4mm"; likely, the
outline drawing was not in the specification PDF). The pegs go through the PCB and come out on the top face.

Placement: on the PCB bottom at the rear edge with the actuator facing out through the rear wall, near the
GLYF position (37.5 mm from the right edge of the GLYF, so about 45.5 mm from the right outer face of the 8 mm wider
worxpad body; likely). The actuator centre is at about Z -8.55 (PCB bottom -7.80 minus half of a 1.5 mm body). This is
**below the GLYF's split line at Z -5.0**, so the rear-wall aperture moves down into the bottom shell (case
subsystem). Aperture at least 1.6 mm travel plus actuator width plus 1.0 mm long, and 2.0 mm high.

## 9. Protection

| Layer | Part | What it covers |
| --- | --- | --- |
| Pack PCM | in the cell (EEMB values in 5.1) | overcharge 4.28 V, over-discharge 3.0 V, overcurrent 0.5 A continuous / 1 A for 3 s, short circuit |
| Reverse polarity | **AO3401A** P-MOSFET (C15127, **basic**, 1,121,575 at LCSC, USD 0.08) in the positive battery line: drain to the connector, source to BAT, gate to GND (through 10 kOhm C25744 optional) | A retail cell with swapped wires would otherwise destroy the charger and the gauge. With correct polarity Vgs = -VBAT turns the channel on in both directions, so charging works; RDS(on) 85 mOhm at 2.5 V gives about 35 mV at 0.4 A. |
| Input | BQ2407x OVP at 6.6 V, 26 V tolerant; ESD and surge parts on VBUS belong to usb-io | input faults |
| Charge | NTC window 0 to 50 degC, 125 degC thermal regulation, 30 min / 5 h safety timers, 4.2 V +/-0.5 % regulation | cell temperature and charge faults |
| Output | BQ OUT short-circuit detection; TPS7A02 current limit 240 to 750 mA | rail faults |

The gauge's CELL and VDD pins go to BAT, after the FET, so a reversed cell never reaches them.

## 10. Fuel gauge

| Option | Accuracy | Current | ZMK support at 4dd95d78 | Parts | Verdict |
| --- | --- | --- | --- | --- | --- |
| **MAX17048G+T10** | ModelGauge state of charge; voltage +/-7.5 mV | 3 uA hibernate, auto entry and exit; 0.5 uA sleep | yes: `zmk,maxim-max17048` in `app/module/drivers/sensor/max17048/` (confirmed in the pinned workspace); battery chosen node `zmk,battery` | 1 IC, 1 capacitor | **Chosen**, same as the GLYF |
| Divider on AIN with a switch (`zmk,battery-voltage-divider`, `power-gpios`) | voltage curve only, poor under a 60 mA backlight load | about 1 uA plus samples | yes | 2 resistors, FET | Rejected: the state of charge jumps with backlight load, and the display shows a number. |
| nRF VDDH divider (`zmk,battery-nrf-vddh`) | | | yes | none | Not possible: LV mode (`mcu-radio.md` 7.1). |
| nPM1300 fuel gauge | good | | no | PMIC | Rejected with the nPM1300. |

Connections: VDD and CELL to BAT (after the FET), 2.5 to 4.5 V (confirmed). 0.1 uF (C1525) at VDD. SDA P0.07, SCL
P0.11 with 4.7 kOhm pull-ups (C25900, basic) to 3.3 V, unless another subsystem already places them. ALRT open-drain
to P0.26 with internal pull-up. QSTRT to GND. Address 0x36. The ZMK driver wakes the gauge at init and never commands
sleep. The gauge relies on its automatic hibernate, so the 3 uA figure is likely, not measured. Package DFN-8 2 x 2 mm,
0.5 mm pitch, KiCad footprint `DFN-8-1EP_2x2mm_P0.5mm_EP0.8x1.6mm` (check the EP size against the Maxim land
pattern).

Devicetree sketch for the board files:

```dts
/ { chosen { zmk,battery = &fuel_gauge; }; };
&i2c0 { fuel_gauge: max17048@36 { compatible = "zmk,maxim-max17048"; reg = <0x36>; }; };
```

## 11. Battery connector

| Option | LCSC, class, stock | Height below PCB | Rating | Retail cells | Verdict |
| --- | --- | --- | --- | --- | --- |
| **JST S2B-PH-SM4-TB** (PH 2.0, side entry) | C295747, extended, 743 (JLCPCB) / 540 (LCSC), USD 0.20 | **5.5 mm**; footprint 7.9 x 6.0 mm plus 2.6 mm tabs | 2 A (AWG24) | Adafruit, SparkFun and most retail packs | **Chosen** |
| XY-S2B-PH-SM4-TB clone | C54582899, 3,225, USD 0.05 | same | | same | Acceptable second source. |
| JST SM02B-SRSS-TB (SH 1.0) | C160402, 51,525 | 2.9 mm | 1 A | rare | Rejected: retail cells do not use it. Keep it in mind if the case cannot spare 5.5 mm. |
| Molex PicoBlade 53261-0271 (1.25 mm, likely the GLYF's plug size) | C177225, 7,136 | not read | | some | Rejected: no gain over PH. |

Height from the JST PH drawing, SMT side entry: 5.5 mm high, 6.0 mm deep, plus 1.6 and 2.6 mm tab dimensions
(`ds-01/jst_ph.pdf` page 3, confirmed). KiCad footprint `JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal`.

Placement: PCB bottom, outside every socket zone, **under the control column between key column 4 and the display
area, left of the RF bay**, mouth facing the pocket. Its underside is at Z -13.30; floor clearance at least 0.3 mm,
so the floor there is at Z -13.60 or lower, which the pocket's wire relief already gives. Leave at least 12 mm in
front of the mouth for the plug and the wire bend.

Polarity: JST PH pin 1 = positive on Adafruit packs (Adafruit's documented convention). Print "+" at pin 1 on the
silkscreen and state the polarity on every cell order. Check each retail cell with a meter before first connection.

## 12. Numbers the design needs

| Item | Value |
| --- | --- |
| Rails | VBUS 4.35 to 6.6 V in; VSYS 3.0 to 4.5 V (BQ24072) or to 5.6 V (BQ24075 fallback); 3V3 200 mA from TPS7A02; BAT 3.0 to 4.2 V |
| Rail capacitance | 3V3 total 1 to 22 uF ceramic |
| Charge | about 400 mA (362 to 443); input limit 475 mA typ; pre-charge 40 mA; termination about 40 mA; 4.20 V; timers 30 min / 5 h; 0 to 50 degC |
| Currents | off 8 uA; deep sleep 31 uA; connected idle 54 uA; lit 9 mA plus backlight; peak 111 mA |
| GPIO | P0.03 /CHG in, pull-up; **P0.04 /PGOOD in, pull-up (new)**; P0.26 gauge ALRT in, pull-up; I2C P0.07/P0.11; P0.05 left free (no divider) |
| Heights below PCB (PCB bottom at Z -7.80) | BQ24072 VQFN 1.0 mm max; TPS7A02 SOT-23-5 1.45 mm max; MAX17048 DFN 0.8 mm max; AO3401A SOT-23 about 1.2 mm; NTC 0805 1.25 mm; MSK12C02 about 1.5 mm; **JST PH 5.5 mm** |
| Pocket | 45.0 x 66.0 mm plus 15 x 12 mm wire relief; floor top Z -15.95 (or -15.18 for 4.3 mm cells only) |
| Cell | 1,000 to 1,200 mAh, 4.3 x 42.5 x 63 mm max (production) or 5.0 x 34 x 62 mm (bring-up), PCM, JST PH 2-pin, pin 1 positive |

## 13. Parts list

| Role | MPN | LCSC | Class | Stock read 2026-11-13 | USD (qty 1) | Datasheet |
| --- | --- | --- | --- | --- | --- | --- |
| Charger, power path | TI BQ24072RGTR | C140288 | extended | 1,216 JLCPCB API; 1,216 LCSC detail | 1.06 | https://www.ti.com/lit/ds/symlink/bq24072.pdf (`ds-01/bq24074.pdf`, SLUS810N) |
| Charger fallback | TI BQ24075RGTR | C15464 | extended | 27,702 JLCPCB; 27,184 LCSC | 1.07 | same |
| 3.3 V LDO | TI TPS7A0233PDBVR | C2887324 | extended | 5,309 JLCPCB; 1,871 LCSC | 1.14 | https://www.ti.com/lit/ds/symlink/tps7a02.pdf (`ds-01/tps7a02.pdf`) |
| LDO alternative | Richtek RT9080-33GJ5 | C841192 | extended | 30,941 JLCPCB; 28,260 LCSC | 0.12 | `ds-01/rt9080.pdf` (DS9080-05) |
| Fuel gauge | ADI MAX17048G+T10 | C2682616 | extended | 20,372 JLCPCB and LCSC | 1.94 | https://www.analog.com/media/en/technical-documentation/data-sheets/MAX17048-MAX17049.pdf (copy read: SparkFun, `_cache/follow-battery-cell-and-runtime/ds-07/max17048_sf.pdf`) |
| Power switch | Shouhan MSK12C02 | C431540 | extended | 172,615 JLCPCB; 163,990 LCSC | 0.055 | `ds-02/msk12c02.pdf` (LCSC copy) |
| Reverse-polarity FET | AOS AO3401A | C15127 | **basic** | 1,557,906 JLCPCB; 1,121,575 LCSC | 0.08 | LCSC datasheet link in `lcsc-02/C15127.json` |
| Battery connector | JST S2B-PH-SM4-TB(LF)(SN) | C295747 | extended | 743 JLCPCB; 540 LCSC | 0.20 | `ds-01/jst_ph.pdf` (JST ePH) |
| NTC 10 k B3950 | Fenghua CMFB103F3950FANT | C51597 | extended | 41,619 JLCPCB; 30,680 LCSC | 0.07 | LCSC link in `lcsc-02/C51597.json` |
| RISET 2.2 k 1 % 0402 | UNI-ROYAL 0402WGF2201TCE | C25879 | basic (LCSC data; class not re-queried) | 1,281,100 LCSC | <0.01 | |
| RILIM 3.3 k 0402 | 0402WGF3301TCE | C25890 | basic | 1,276,960 JLCPCB | <0.01 | |
| EN1 100 k 0402 | 0402WGF1003TCE | C25741 | basic | 8,504,096 JLCPCB | <0.01 | |
| I2C pull-ups 4.7 k 0402 | 0402WGF4701TCE | C25900 | basic | 14,337,612 JLCPCB | <0.01 | |
| 1 uF 50 V 0603 (IN, LDO in) | Samsung CL10A105KB8NNNC | C15849 | basic | 13,688,502 JLCPCB | <0.01 | |
| 10 uF 10 V 0603 (OUT, BAT, LDO out) | Samsung CL10A106KP8NNNC | C19702 | basic | 11,723,415 JLCPCB | <0.01 | |
| 100 nF 0402 (gauge VDD) | Samsung CL05B104KO5NNNC | C1525 | basic | 31,981,075 JLCPCB | <0.01 | |
| Cell, production | EEMB LP404261-PCM-LD | not at LCSC | hand-fitted | stock not confirmed (quotation) | not found | `cell-02/LP404261.pdf` (from macrogroup.ru) |
| Cell, bring-up | Adafruit 258 | not at LCSC | hand-fitted | in stock at adafruit.com | 9.95 | https://www.adafruit.com/product/258 |

Note on class: the JLCPCB API marks every IC above as "expand" (extended) and none as preferred. Five extended ICs
plus the connector add JLCPCB extended-part fees, accepted per "function beats fee savings".

KiCad 10.0.7 stock libraries (checked in the image):

| Part | Symbol | Footprint | 3D model |
| --- | --- | --- | --- |
| BQ24072 / BQ24075 | yes, `Battery_Management:BQ24072RGT`, `BQ24075RGT` | `Package_DFN_QFN:VQFN-16-1EP_3x3mm_P0.5mm_EP1.68x1.68mm` (symbol default; `_ThermalVias` variant exists) | referenced by the footprint; the image ships no 3D library, so not verified |
| TPS7A02 DBV | no; use `Regulator_Linear:AP2112K-3.3` (same IN-GND-EN-NC-OUT order, verify) or draw one | `Package_TO_SOT_SMD:SOT-23-5` | as above |
| MAX17048 | no; draw one | `Package_DFN_QFN:DFN-8-1EP_2x2mm_P0.5mm_EP0.8x1.6mm` | as above |
| MSK12C02 | `Switch:SW_SPDT` | `Button_Switch_SMD:SW_SPDT_Shouhan_MSK12C02` | footprint references `SW_SPDT_Shouhan_MSK12C02.step` |
| JST PH | `Connector_Generic:Conn_01x02` | `Connector_JST:JST_PH_S2B-PH-SM4-TB_1x02-1MP_P2.00mm_Horizontal` | referenced |
| AO3401A | `Transistor_FET:AO3401A` | `Package_TO_SOT_SMD:SOT-23` | referenced |
| NTC | `Device:Thermistor_NTC` | `Resistor_SMD:R_0805_2012Metric` | referenced |

## 14. Battery safety rules for the case

1. **No pressure on the pouch.** The pocket is larger than the cell on every side (at least 1.0 mm a side in plan,
   0.5 mm swelling allowance in Z above the cell). Nothing clamps the cell. Hold it with one layer of thin
   double-sided foam tape or a soft foam pad on the floor, not by squeezing it between the PCB and the floor.
2. **Swelling allowance.** At least 10 % of the cell thickness free above the cell (0.5 mm for 5.0 mm cells,
   0.43 mm for 4.3 mm). Bosses, ribs and screws stay outside the pocket outline.
3. **No sharp edges or points** facing the pouch: deburr the pocket edges, radius at least 0.5 mm on every pocket
   edge, no screw tips, no through-hole leads or socket solder joints without the 0.3 mm insulating sheet between
   them and the cell. The cell's PCM end and its taped tabs sit at the connector end, away from the wedge's thinnest
   point.
4. **Strain relief.** Route the wires through the wire relief, not across a shell split line or a screw. Leave a
   loose loop of at least 10 mm. A tab or a dab of tape holds the wires so that the solder joints on the PCM do not
   carry the plug force.
5. **Connector access.** With the bottom shell off, the plug is reachable and pulls straight out of the
   side-entry header. The first step of every disassembly is to unplug the cell. Nothing else has to be removed
   first.
6. **Heat.** Keep the charger at least 10 mm from the pocket in plan. No part that runs warm sits above the cell.
7. **Not in the RF bay,** and no metal tape or foil on the cell near the bay (`mcu-radio.md` A6).
8. **Venting.** The case needs no seal. A swollen cell must be able to push the bottom shell before it bursts;
   do not glue the shells.
9. **FDM prototype.** PLA softens near 55 to 60 degC. Charge the prototype at room temperature and not in sun.
10. **Shipping.** Ship with the switch off and the cell at 30 to 50 % charge. EEMB ships at 3.72 to 3.78 V for air
    freight (`cell-02/LP404261.txt` section 8, confirmed). UN38.3 certification is the cell vendor's (EEMB claims
    UN38.3; search summary of eemb.com/product-219, likely).

## 15. Consequences for other subsystems

- **Case:** pocket of section 5.2, depth under the wedge, 17.45 mm (or 16.68 mm) deck to underside over the pocket.
  Rear-wall aperture for the slide switch at about Z -8.55, not on the Z -5.0 split line. Floor clearance at
  least 5.8 mm below the PCB bottom at the battery connector. No metal clamp over the cell. Optional thermal pad at
  the charger.
- **MCU and firmware:** P0.04 is now /PGOOD. The worxpad power hooks are a requirement, because without them
  connected standby is milliamperes. Add PWM dimming (`zmk,display-led`) with a default near 25 to 50 %.
  `CONFIG_ZMK_BATTERY_REPORTING=y` with the MAX17048 node, a charging icon from /CHG and /PGOOD, a low-battery
  warning at 10 %, optional soft-off at 3 %. With the switch off and USB plugged in, VBUS reaches module pad 66 while
  VDD is 0 V (see risk 5).
- **Display:** backlight current comes from the 3V3 rail (at most 60 mA) through a low-side transistor. If the chosen
  panel uses LEDs in series (6.4 V), it needs its own boost driver from VSYS, and this record must be revised.
- **USB and I/O:** VBUS after ESD and surge protection goes to BQ IN with 1 uF there. Default USB-C sink (5.1 kOhm on
  each CC line) is enough, because the input stays at or under 500 mA.
- **Keys:** the 0.3 mm insulating sheet covers the socket bodies over the pocket. The NTC sits between socket zones
  above the cell.

## 16. Risks

1. **Connected standby depends on firmware hooks (high).** Without the panel SLPIN and flash power-down hooks, idle is
   milliamperes and runtime falls to days. Measure on the first board.
2. **Cell supply (medium).** EEMB is quotation-only. Stock not confirmed. Mitigation: the Adafruit 258 fits the
   5.0 mm pocket depth; Lipol LP404060 and 5.0 mm 503759-class retail cells are alternatives.
3. **Body thickness over the pocket (medium).** 17.45 mm for 5.0 mm cells is close to the GLYF's 17 to 19 mm wedge
   zone. If the case cannot give it, use 4.3 mm cells only (16.68 mm).
4. **BQ24072 stock is thin (low).** 1,216 units. The BQ24075 drops in with the same nets; the TPS7A02 already accepts
   its 5.6 V output.
5. **VBUS on the nRF while VDD is off (low).** With the switch off and USB plugged in, the module's USB regulator
   sees VBUS with VDD at 0 V. The nRF52840 specification was not checked for this case. If it is not allowed, feed
   pad 66 from VBUS through a load switch enabled by 3V3, or accept that USB charging happens with the switch on.
6. **3V3 capacitance limit (low).** TPS7A02 is specified for 1 to 22 uF. The display module's own capacitors count.
7. **NTC window 50 degC against the cell's 45 degC (low).** Charging stops at 50 degC, 5 K above the cell rating.
   Low charge current and the thermal placement rules keep the cell far below. A stricter window needs a different
   NTC network and was not designed.
8. **MAX17048 automatic hibernate under the ZMK driver (low).** Not measured. Worst case 23 uA active adds 20 uA to
   standby.
9. **Retail cell polarity (low after mitigation).** The AO3401A blocks a reversed cell. A cell with a different plug
   still needs rework.
10. **Runtime figures are arithmetic.** The CPU share while LVGL draws is a guess, and the panel is not chosen yet.

## 17. Sources

Datasheets (read in the cache):

- TI BQ24072/3/4/5/9, SLUS810N, October 2021: https://www.ti.com/lit/ds/symlink/bq24074.pdf; `ds-01/bq24074.pdf`,
  text `ds-01/bq24074.txt` (pin table lines 400-466, electrical lines 600-760, SYSOFF section 9.3.5.5).
- TI TPS7A02: https://www.ti.com/lit/ds/symlink/tps7a02.pdf; `ds-01/tps7a02.pdf`.
- Richtek RT9080 DS9080-05: `ds-01/rt9080.pdf`.
- Torex XC6220: `ds-01/xc6220.pdf`.
- TI BQ25180 and BQ25185: `ds-01/bq25180.pdf`, `ds-01/bq25185.pdf`.
- Maxim MAX17048/MAX17049 (SparkFun copy): `_cache/follow-battery-cell-and-runtime/ds-07/max17048_sf.pdf`.
- JST PH catalogue: `ds-01/jst_ph.pdf`, page 3 (SMT side entry), crop `ds-02/jst_smt_crop.png`.
- Shouhan MSK12C02 specification, 2024-12-14: https://datasheet.lcsc.com/datasheet/pdf/5162155576bfd231c35aa9a893d25c8c.pdf?productCode=C431540; `ds-02/msk12c02.pdf`.
- EEMB LP404261-PCM-LD specification, 2017-12-25: https://macrogroup.ru/upload/iblock/bb0/2b58zuj4c8et674fb98ouxpn6l1fq88h/LP404261.pdf; `cell-02/LP404261.pdf`.

Stock and prices (2026-11-13):

- JLCPCB parts-library API, `selectSmtComponentList/v2`: `jlc-01/*.json`, `jlc-02/*.json`.
- LCSC product detail API, `wmsc.lcsc.com/ftps/wm/product/detail`: `lcsc-01/*.json`, `lcsc-02/*.json`.
- https://www.adafruit.com/product/258; https://www.olimex.com/dev/battery-lipo1400mah.html;
  https://www.eemb.com/products-55; https://www.eemb.com/product-219 (search summary only).

Firmware:

- ZMK at 4dd95d7840eb3d5a3f59bb29fbf1ab054715ef85 in `/home/worxbend/Projects/worxboard/build/fw-ws/zmk`:
  `app/module/drivers/sensor/max17048/max17048.c`, `app/module/drivers/sensor/max17048/Kconfig`,
  `app/module/dts/bindings/sensor/zmk,maxim-max17048.yml`, `app/src/battery.c` (chosen `zmk,battery`),
  `docs/docs/config/battery.md`; copies in `zmk-01/`.
- Zephyr in the same workspace: `drivers/charger/charger_bq25180.c`, `drivers/fuel_gauge/max17048/`.

KiCad: `kicad/kicad:10.0.7` image, `/usr/share/kicad/symbols` and `/usr/share/kicad/footprints`, listed on
2026-11-13. The image has no `3dmodels` directory.

Project records: `research/components/mcu-radio.md`, `research/components/keys.md`,
`research/raw/follow-battery-cell-and-runtime.md`, `follow-display-module-sourcing.md`,
`follow-maker-bom-part-numbers.md`, `regulatory-software.md`, `official-site.md`, `prior-art.md`.

## 18. Not checked or not found

- No current was measured. Every runtime figure is arithmetic.
- The MSK12C02 outline drawing (body height, actuator length): not in the specification PDF; height taken as about
  1.5 mm from the LCSC attribute and common use (likely).
- The nRF52840 rule for VBUS present with VDD unpowered (risk 5): not read.
- EEMB price, lead time and whether it fits a JST PH plug for small orders: not found (quotation only).
- The pinout of the 1.4 inch panel's backlight (parallel or series LEDs): not found; it changes the backlight supply.
- PCBWay sourcing for these parts: not checked.
- Self-discharge rate of the chosen cells: not stated in the EEMB sheet beyond a 28-day storage test.
