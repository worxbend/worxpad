# GLYF dossier: what the reference device is

Date: 2026-11-13. Summary of the research phase for worxpad. Inputs: every note in `research/raw/` and every
decision record in `research/components/`. Paths are relative to `research/`. Nothing in this file was copied from
the maker's artwork, firmware, software or 3D models; it holds facts, measurements and judgements only.

## 0. How to read this file

Every fact row carries two labels.

**Kind** says who makes the statement:

- **M**: maker claim. Stated by Prota Designs on its store, blog, videos, comments or published firmware.
- **O**: our measurement. Measured or decoded by this project from a primary source (a maker drawing, a video
  frame, a firmware image, a catalogue record). No unit has been handled.
- **G**: our guess or inference. Judgement, arithmetic on uncertain inputs, or reading of indirect evidence.

**Confidence** follows the project rule: **confirmed** (stated by the maker, or measured from a primary source),
**likely** (consistent indirect evidence), **guess**. "Not found" means the item was looked for and not found.

A maker claim can be "confirmed" as a claim and still be untested. Nobody outside the maker has measured or
opened a GLYF (section 7).

## 1. What the GLYF is

| # | Fact | Kind | Confidence | Source |
| --- | --- | --- | --- | --- |
| 1 | A wireless macro pad: 16 keys in a 4 x 4 grid, two rotary knobs with push, two round push buttons, a 240 x 240 colour LCD, USB-C and Bluetooth, battery, aluminium body | M | confirmed | https://protadesigns.com/products/glyf ; `raw/official-site.md` 4.2 |
| 2 | Store title: "Aluminum Wireless Bluetooth Macro Pad with LCD and Two Rotary Encoders"; three variants Tactile, Clicky, Linear; one finish, anodised black | M | confirmed | https://protadesigns.com/products/glyf.js ; `raw/official-site.md` 3.1 |
| 3 | Chassis "CNC Aluminum, Anodized Black"; alloy stated as 6061 in videos | M | confirmed | product page tech specs; `raw/youtube.md` 3; `raw/social.md` 7 |
| 4 | Switches "Kailh Low Profile V2's (hot-swappable)", full POM, clicky, tactile or linear | M | confirmed | product page; blog Update 03 (`raw/social.md` 6) |
| 5 | Switch family is Kailh Choc V2 (PG1353D full-POM series, MX cross stem on the Choc V2 footprint); exact model not found | O | confirmed (family), not found (model) | Kailh drawing KHA-PG1353D; maker board frame; `raw/follow-switch-family-and-socket.md` |
| 6 | Keycaps and knobs "Injection Molded PBT Plastic"; keycap is an own low-profile design, prototyped in resin | M | confirmed | product page; `raw/youtube.md` 2.7 |
| 7 | Screen "240 x 240 px Full Color LCD" under "Tempered Glass with Black Screen Print" | M | confirmed | product page |
| 8 | Display is a 1.4 inch 240 x 240 IPS module, cover lens 31.20 mm square R2, active area 25.20 mm, stack 2.95 mm, 20-pin 0.5 mm flex | M | confirmed | supplier drawing shown in video `sr0MIYEi678`; `raw/youtube.md` 2.4 |
| 9 | Display controller is ST7789V-compatible, RGB565, 4-wire SPI at 20 MHz | O | confirmed | beta firmware v0.1.0 decode; `raw/regulatory-software.md` 2 |
| 10 | The display window is square, not portrait as the renders suggest | O | confirmed (drawing), likely (real units) | `raw/geometry.md` 4.5; `raw/youtube.md` 2.4 |
| 11 | Bluetooth "5.2 at 2.4 GHz", up to 4 hosts; profile choice on a Bluetooth layer on the display | M | confirmed | product page; maker comment on `Lgr_0N7SrDY` |
| 12 | No 2.4 GHz dongle | M | confirmed (absence in all sources read) | `raw/youtube.md` 2.1 |
| 13 | Battery "1,200 mAh Li-Ion" | M | confirmed | product page |
| 14 | 16 layers of 16 keys, "Up to 256 Macros"; macros recorded and stored on the device | M | confirmed | product page; blog Update 05 |
| 15 | Widgets: keymap icons, time, media; "Time & Media widgets TBD" | M | confirmed | product page asterisk; `raw/official-site.md` 4.2 |
| 16 | Host OS: Windows, macOS, Linux, Android, iOS; companion app on desktop only; no VIA or QMK | M | confirmed | product FAQ |
| 17 | "Ultra-Slim Design, just 19 mm thin" | M | confirmed (claim) | product page; meaning in section 3 |
| 18 | Weight 265 g | M | confirmed (claim) | on-screen text, video `Nk6MD9QS8VA` |
| 19 | Store shipping weight 442 g per variant (most likely with box and cable) | M (value), G (meaning) | confirmed / guess | `products/glyf.js`; `raw/official-site.md` 3.1 |
| 20 | In the box: GLYF, USB-C to USB-C cable, Quick Start Guide; no dock or accessory product exists | M | confirmed | product page; `raw/official-site.md` 3.3 |
| 21 | Price USD 159, compare-at USD 189 (UAH 7,331 is the store's localisation of USD 159) | M | confirmed | `products/glyf.js` |
| 22 | Status on 2026-11-13: "Pre-order Now", "Shipping Early Q4 2026" | M | confirmed | product page |
| 23 | Not published anywhere: outer dimensions, battery life, charge time, MCU part number, display size in inches, encoder model, warranty, software download | O | confirmed (absence) | `raw/official-site.md` 4.4; `raw/regulatory-software.md` 8 |

## 2. Maker and timeline

| # | Fact | Kind | Confidence | Source |
| --- | --- | --- | --- | --- |
| 1 | Prota Designs, Lake Elsinore, California; two founders (CEO hardware, CTO firmware); self-funded ("No investors") | M | confirmed | `/pages/about-us`, `/meta.json`; `raw/official-site.md` 2 |
| 2 | Legal form, registration number: not found. California registry and OpenCorporates blocked automated access | O | not found | `raw/regulatory-software.md` 6 |
| 3 | Earlier product: the Printed Pad (3 x 3 keys, OLED, STM32, QMK/VIA, printed case); GLYF is "version two" | M | confirmed | `raw/youtube.md` 1 |
| 4 | No trademark for "PROTA DESIGNS"; "GLYF" is a registered class 9 mark of an unrelated company (eyewear) | O | confirmed | USPTO, TMview; `raw/regulatory-software.md` 6 |
| 5 | No own FCC ID, Bluetooth SIG listing or MIC record; consistent with a pre-certified module and no shipment yet | O | confirmed (absence on fccid.io, SIG, MIC); official FCC search blocked | `raw/regulatory-software.md` 5 |

| Date | Event | Kind | Source |
| --- | --- | --- | --- |
| 2024-04 | Prototype 1: wired, Printed Pad hardware (STM32, QMK), small SPI LCD, two encoders, two screen buttons | M | blog Update 01 |
| 2024-07 | Prototype 2: first Bluetooth board, bare nRF52 QFN (most probably nRF52833) with chip antenna, GPIO expander, flash, BMS | M (board), G (nRF52833, from a bootloader filename) | Update 01; `raw/social.md` 4.1 |
| 2024-12-28 | Move from QMK to ZMK | M | Update 01 |
| 2025-01-15 | LVGL 9 display tests; ZMK on an nRF52840 DK | M | Update 02 |
| 2025-03-15 | 240 x 240 LCD chosen; Kailh low-profile switches; own keycaps | M | Update 03 |
| 2025-03 to 2025-11 | Prototypes on a plug-in nRF52840 board (nice!nano form) in printed cases | M | `raw/youtube.md` 2.1, 4 |
| 2025-06-24 | First CNC aluminium samples | M | TikTok 7519406476465589535 |
| 2025-10-14 | Pre-orders open on the own store at USD 189, free worldwide shipping | M | maker comments; Wayback 2025-10-17 (`raw/official-site.md` 9) |
| 2025-11-21 | Price quoted as USD 159 from this date | M | maker comments (`raw/youtube.md` 5) |
| 2025-11-13/14 | Integrated PCB ordered: 5 assembled boards, USD 284.66 merchandise, USD 503.88 landed | M | TikTok 7572377900821777694; `raw/social.md` 4.4 |
| 2025-12-30 | Integrated PCB with the Holyiot nRF5340 module shown | M | TikTok 7589532575031381279 |
| 2026-01 to 2026-03 | Working metal units; Founders, Inc. residency; launch video 2026-01-30 | M | Update 05 |
| 2026-03-09 | "Final production hardware is complete"; beta test opens | M | Update 05 |
| 2026-03-29 to 2026-06-18 | Five signed beta firmware images v0.1.0 to v0.1.4 published by the CTO | O | https://github.com/noahbei/glyf-releases |
| 2026-03-14 | Last TikTok post; last YouTube upload 2026-03-05 | O | yt-dlp listings (`raw/youtube.md` 1) |
| 2026-10-09 | Update 06: beta done, production ramp, "still on track to ship in Q4" | M | https://protadesigns.com/blogs/updates/update-06-glyf-development-gearing-up-for-production |
| 2026-11-13 | Still pre-order; no review, unboxing or teardown anywhere reachable | O | `raw/community-press.md` 1 |

## 3. Measured geometry

Source for every row: `raw/geometry.md` section 4 (scale fixed by the 31.20 mm lens and the 19.05 mm KiCad pitch,
which agree to 0.02 %). All rows are **O** (our measurement from maker drawings, renders and CAD frames), except
those marked G. Plan origin: rear left outer corner; "right edge" is the knob side. Heights are square to the
top face (deck = 0).

| Dimension | Value (mm) | Range | Kind | Confidence |
| --- | --- | --- | --- | --- |
| Overall width (X) | 120.4 | 120.1 to 120.7 | O | likely |
| Overall depth (Y) | 85.2 | 84.7 to 85.5 | O | likely |
| Maximum body thickness, wedge apex 12.7 mm from the rear face (the "19 mm") | 19.2 | 18.6 to 19.3 | O | likely |
| Body thickness at the front edge / rear wall | 13.0 / 12.0 | 12.8 to 13.2 / 11.8 to 12.2 | O | likely |
| Underside ramp (thickness = 12.94 + 0.0866 x distance from front face); rear slope 29 degrees | 4.95 degrees | | O | likely |
| Top face tilt on the desk | 5.0 degrees | 4.7 to 5.2 | O | likely |
| Top face above the desk, front / rear edge | 14.9 / 22.3 | 14.4 to 15.2 / 21.6 to 22.6 | O | likely |
| Overall height on the desk (knob tops) | 32.8 | 32.0 to 33.5 | O | likely |
| Height over keycaps / over knobs, square to the top face, no feet | 23.6 / 31.0 | 22.8 to 23.9 / 30.1 to 31.4 | O | likely |
| Key pitch, X and Y | 19.05 | 19.03 to 19.07 | O | confirmed |
| Keycap base / top face, square | 18.4 / 15.7 | 18.3 to 18.5 / 15.5 to 15.8 | O | likely |
| Keycap top above the deck | 4.4 | 4.2 to 4.6 | O | likely |
| Gap between keycaps | 0.64 | 0.55 to 0.75 | O | likely |
| Key well, lip to lip | 78.15 | 78.0 to 78.3 | O | likely |
| Key well depth, deck to plate top | 3.7 | 3.3 to 4.2 | G | guess |
| Switch opening (maker caliper reading) | 14.06 | | M | likely |
| Knob diameter / cap height | 10.5 / 9.1 | 10.3 to 10.6 / 8.8 to 9.4 | O | likely |
| Knob top above the deck | 11.8 | 11.5 to 12.1 | O | likely |
| Knob boss base diameter | 16.1 | 15.9 to 16.3 | O | likely |
| Knob centres from the rear edge; from the right edge | 15.1; 10.27 and 28.96 | 15.0 to 15.2 | O | likely |
| Round button cap diameter (in a 12.5 mm hole); proud height | 12.3; 1.0 | 12.2 to 12.5; 0.7 to 1.2 | O | likely |
| Round button centres from the front edge (same X as the knobs) | 14.0 | 13.9 to 14.1 | O | likely |
| Display lens, square side, R2 corners | 31.2 | 31.1 to 31.3 | M (supplier drawing) | confirmed |
| Display active area (1.4 inch, 240 x 240) | 25.2 | 25.1 to 25.3 | M (supplier drawing) | confirmed |
| Display module stack | 2.95 | 2.8 to 3.1 | M (supplier drawing) | confirmed |
| Lens edge from the right body edge | 4.0 | 3.9 to 4.1 | O | likely |
| Top shell wall, edge to key well lip | 3.5 | 3.3 to 3.6 | O | likely |
| Vertical corner radius / top edge chamfer / bottom chamfer | 2.0 / 1.0 / 0.4 | | O / O / G | likely / likely / guess |
| Shell split below the top face | 5.0 | 4.8 to 5.1 | O | likely |
| Wedge height below the wall line / width at its base | 7.2 / 94 | 6.6 to 7.3 / 92 to 100 | O | likely |
| Feet: four domed silicone stadiums, length x width x proud | 22.5 x 5.2 x 2.0 | 22 to 24 long | O | likely |
| Rear feet centres from the rear face; front feet from the front face | 18.2; 5.6 | | O | likely |
| USB-C aperture, 10.0 x 4.3 stadium on the split line; centre from the right edge | 10.0; 19.6 | 19.1 to 19.9 | O | likely |
| Slide switch aperture centre from the right edge | 37.5 | 37.0 to 38.0 | O | likely |
| Shell screws (four, under keycaps), X from the left edge; Y about 7.1 from rear and front | 23.5 and 61.6 | | O | likely |
| PCB width (KiCad dimension label) | 112.5 | | M (layout frame) | likely |
| Mass split: about 130 to 160 g aluminium plus about 115 g internals matches 265 g | | | G | guess |

## 4. Inferred internals

| # | Item | Finding | Kind | Confidence | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | SoC | Nordic nRF5340 (dual core). Static RAM use of the beta firmware reaches at least 373,140 bytes, including a 115,200-byte full-frame 240 x 240 RGB565 buffer | O | confirmed | firmware strings and decode; `raw/regulatory-software.md` 2; `raw/follow-radio-module-choice.md` |
| 2 | Radio module | Holyiot HOLYIOT-21069 (nRF5340, FCC ID 2ALGY21069), 19.0 x 13.5 mm, 58 pads, ceramic chip antenna, 1.0 dBi; maker says "nRF53 series module" | O (can marking), M (family) | confirmed | video `S9c5WuorsgQ` frames; https://fccid.io/2ALGY21069 |
| 3 | Module placement | PCB underside, right board edge, antenna 1 to 3 mm from a solid aluminium side wall; copper keep-out about 3.4 x 23.5 mm | O | likely | `raw/follow-rf-exit-in-aluminium.md` |
| 4 | Radio exit | No slot, window or plastic insert anywhere; signal can leave only through the shell seam, the display window and the switch openings. No range figure exists | O (no opening seen), G (leak path) | likely / guess | same |
| 5 | Firmware | ZMK on Zephyr (nRF Connect SDK), LVGL 9, MCUboot RSA-2048 signed images, update by MCUmgr SMP over CDC-ACM, no UF2 | O | confirmed | `raw/regulatory-software.md` 2 |
| 6 | Host protocol | ZMK Studio RPC with added `display` and `macros` subsystems over CDC-ACM; ZMK Studio GATT UUID present; USB IDs still ZMK default 1D50:615E | O | confirmed | same |
| 7 | Companion app | Modified ZMK Studio with Layers and Widgets tabs | O | confirmed | video `v9_v6v359Tw` frames |
| 8 | Icon storage | Winbond W25Q128 (16 MB, JEDEC ef 40 18) on QSPI, LittleFS mounted at `/c`; SOIC-8 208 mil (U8) | O | confirmed | firmware nodes; `raw/follow-maker-bom-part-numbers.md` |
| 9 | Fuel gauge | MAX17048 at I2C 0x36 (2 x 2 mm DFN-8, U3) | O | confirmed | firmware node `max17048@36` |
| 10 | Real-time clock | DS3231MZ+TRL (LCSC C107410) at 0x68 with a coin cell (picture shows Panasonic ML1220; May 2025 layout says CR2032) | O | confirmed (part), likely (cell) | maker JLCPCB parts list frame; firmware v0.1.4 |
| 11 | Charger | 3.0 x 3.0 mm QFN-16 with power path, beside an 0402 bead: a linear charger, best fit TI BQ2407x; exact part not found | O (size), G (family) | confirmed / guess | `raw/follow-maker-bom-part-numbers.md` 3 |
| 12 | 3.3 V regulator | SOT-23-5 U4, probably Torex XC6220B331 (named on the May 2025 layout) | O | likely | same; `raw/youtube.md` 2.5 |
| 13 | Key matrix | Direct GPIO matrix 5 columns x 4 rows, col2row, pull-down inputs: 16 keys, 2 encoder pushes, 2 navigation buttons; one SOD-123 diode per position; no GPIO expander in production | O | confirmed (driver), likely (pins) | firmware decode |
| 14 | Sockets | Kailh Choc hot-swap socket outline (CPG135001S30), PCB bottom | O | likely | `raw/follow-maker-bom-part-numbers.md` |
| 15 | Encoders | Two through-hole EC11-style encoders with push (Alps Alpine on the March 2025 prototype); dev-rig ZMK values steps 80, triggers 20 | M (Alps), O (footprint, values) | confirmed / likely | Update 03; `raw/regulatory-software.md` 2 |
| 16 | Round buttons | SMD tactile switches, footprint SW_Omron_B3FS; one is the "widget-cycle button" | O / M | confirmed | layout frame `ScYz1Z_T1UY`; Update 04 |
| 17 | Display connection | 20-pin 0.5 mm flip-lock FPC connector J2 on the PCB bottom; the flex passes through a 4 x 12 mm slot in the PCB; Q2 probably switches the backlight | O | confirmed (slot, connector), guess (Q2) | `raw/youtube.md` 2.4 |
| 18 | Backlight dimming | No PWM driver in the firmware; display blanks on idle from v0.1.3 | O | likely | `raw/regulatory-software.md` 2 |
| 19 | USB-C | 16-pin mid-mount receptacle (TYPE-C-31-M-12 class) in a rear board notch between the encoders; fuse F1 and SOT-23-6 U5 (ESD, guess) behind it | O | likely / guess | `raw/youtube.md` 2.7; `raw/social.md` 4.2 |
| 20 | Power switch | Side-actuated SMD slide switch (MSK12C02 type) at the rear edge with MOSFET Q1 | O | confirmed (switch), likely (type) | `raw/follow-maker-bom-part-numbers.md` |
| 21 | Battery | Real sample cell labelled DTP404257 3.7 V 1200 mAh 4.44 Wh: about 4.0 x 42 x 57 mm pouch with PCM and a plug of about 1.25 mm pitch; sits in a bottom-shell pocket about 43 x 74 mm, 9 to 53 mm from the rear face | O | likely | `raw/follow-battery-cell-and-runtime.md` |
| 22 | Other parts | SOIC-8 EEPROM (AT24C32D or AT24C02D) beside the RTC, unused by the firmware; reset button SW1; SWD pads J3 (2 x 3) | O | likely / confirmed | `raw/follow-maker-bom-part-numbers.md`; `raw/social.md` 4.2 |
| 23 | Assembly | All SMD parts, sockets, module, FPC connector and battery connector on the PCB bottom; encoders, buttons, switches and display on top; bottom-side SMT at JLCPCB, rest hand-fitted. 18 extended part types | O | confirmed | `raw/youtube.md` 2.8; `raw/social.md` 4.4 |
| 24 | Case construction | Two 6061 CNC shells, bead-blasted, black anodised; top shell carries the plate; bottom shell is a tray with the wedge and two rear scoops; four M2-class screws from the top under keycaps | M (process), O (screws) | confirmed / likely | `raw/youtube.md` 3; `raw/geometry.md` 7.5 |
| 25 | Internal stack | Plate top -3.7, split -5.0, board top -5.9, board bottom -7.5, socket underside -9.3 | G | guess | `raw/geometry.md` 7.8 |
| 26 | Battery life | Not published. Our arithmetic: about 23 h display-on at full backlight (18 to 30), about 3 days on a 4 h/day lit pattern without dimming | G | guess | `raw/follow-battery-cell-and-runtime.md`; `components/power.md` 4.3 |

## 5. Contradictions between sources

| # | Topic | Side A | Side B | Evidence favours |
| --- | --- | --- | --- | --- |
| 1 | Body size | 120.0 x 84.9 mm at 19.0 mm pitch (`raw/official-site.md` 7.1); about 116 x 88 or 125 x 94 mm from a hand-held photo (`raw/youtube.md` 3); about 115 mm wide on the March 2025 CAD (`raw/social.md` 7) | 120.4 x 85.2 mm with two independent scale references (`raw/geometry.md`) | B. A used one assumed scale or an older revision (84.694 mm depth was prototype v17). |
| 2 | What "19 mm" measures | 18.8 mm at the rear on feet, 17.0 mm at the rear riser (`raw/official-site.md` 7.2, perspective render) | 19.2 mm body apex without feet (`raw/geometry.md` 6, orthographic CAD frame) | B. The perspective reading had no pitch correction and the apex was in shadow. |
| 3 | Foot size | One foot 24.04 mm long (caliper, `raw/youtube.md` 3) | 22.5 x 5.2 mm; 24.04 mm is the width of a moulded strip of feet (`raw/geometry.md` 4.7, three methods) | B. The caliper jaws sit on the strip edges in the frame. |
| 4 | Display shape | Portrait window in marketing renders | Square 31.2 mm lens on the supplier drawing and on filmed units | B (confirmed drawing). |
| 5 | Display flex pin count | 20 contacts on the maker's supplier drawing and on J2 | 15 pins on the Yousee YX14011A with the same glass | Not a contradiction about the GLYF: the same glass exists with different flexes. GLYF is 20-pin. |
| 6 | Launch price | Pre-orders opened at USD 159, regular 189 (`raw/social.md` 3) | Opened at USD 189 on 2025-10-14; USD 159 from 2025-11-21 (`raw/youtube.md` 5; Wayback 2025-10-17 in `raw/official-site.md` 9) | B. Two independent sources and an archived page. |
| 7 | Module placement by JLCPCB | "The Holyiot module is in the JLCPCB placement" (`raw/youtube.md` 2.8) | Board arrived with U1 empty, maker hot-air soldered it (`raw/social.md` 4.1); JLCPCB holds the Holyiot only as non-purchasable customer records (`raw/follow-radio-module-choice.md`) | B. Maker's own words plus the catalogue pattern. |
| 8 | Module vendor known | "The module vendor is not identified" (`raw/regulatory-software.md` 5) | Holyiot HOLYIOT-21069 read off the can (`raw/youtube.md` 2.1, `raw/social.md` 4.1) | B. A did not see the video frames. |
| 9 | Charger type | "Inductor-size part L1 beside U2" (`raw/youtube.md` 2.5) | L1 is 0402 size, a bead, so U2 is linear (`raw/follow-maker-bom-part-numbers.md` 3) | B. Measured against J2's 0.5 mm pitch in the same frame. |
| 10 | U6/U7 role | One is the GPIO expander of prototype 2 (`raw/social.md` 4.2) | No expander driver in the firmware (`raw/regulatory-software.md` 2); marking "2DM" and layout text read as an AT24C EEPROM (`raw/follow-maker-bom-part-numbers.md`) | B. |
| 11 | Battery connector | JST PH S2B-PH-SM4-TB on the May 2025 layout; "JST style" | About 1.1 to 1.2 mm pitch on the December 2025 board; cell plug about 1.25 mm | B for production (finer pitch); A was an earlier revision. |
| 12 | RTC backup cell | CR2032 label on the May 2025 layout | Panasonic ML1220 picture in the December 2025 video | B for the later board, but the picture is an inserted illustration (likely only). |
| 13 | Battery pictures | LP-503562 and UFX 653450 cells in maker illustrations | DTP404257 label on the real cell (`raw/follow-battery-cell-and-runtime.md`) | B. The illustrations are stock pictures. |
| 14 | Shipment | "the product shipped" (`raw/follow-maker-bom-part-numbers.md`, intro) | Store still pre-order, Update 06 says not yet shipped, no customer report anywhere (`raw/community-press.md`, `raw/official-site.md`) | B. The phrase in A is an error in that note. |
| 15 | "Dock" in the hero render | A dock or base plate with a silver block (initial brief) | A second unit upside down; no accessory exists (`raw/geometry.md` 7.7, S13) | B. |
| 16 | Rear port position | Ports cut half into each shell, centred on the split line (`raw/geometry.md` 4.8) | Notches in the bottom shell rear wall (`raw/youtube.md` 3, bottom-shell photo) | Not settled. Renders show a stadium on the split line; the bottom-shell photo shows notches. Both can be true if the top shell carries the upper half. |
| 17 | Bluetooth version | "5.2" (store) | nRF5340 supports 5.4; no version stated in videos | Not a contradiction: 5.2 is the claim, the silicon allows more. |

## 6. Where worxpad departs from the GLYF (decisions, not facts)

Listed so that no reader takes a worxpad number for a GLYF number. Details in `COMPONENTS.md`.

| Item | GLYF | worxpad | Record |
| --- | --- | --- | --- |
| SoC and module | nRF5340, Holyiot-21069, hand-soldered | nRF52840, u-blox BMD-340-A-R, placed by JLCPCB | `components/mcu-radio.md` |
| Radio exit | none (leakage) | RF bay plus a 30 mm right-wall slot with a POM insert | `components/mcu-radio.md` 7.3, `components/enclosure-manufacturing.md` 7 |
| Body | 120.4 x 85.2 mm | 128.4 x 85.2 mm (8.0 mm added on the right) | `components/mcu-radio.md` 7.3.3 |
| Display | 1.4 inch, 20-pin, bonded glass | 1.3 inch DM-TFT13 (23.4 mm active), 24-pin, painted PMMA lens of the same 31.2 mm size | `components/display.md` |
| Knob covers | two round bosses | one plinth over both encoders | `components/rotary-buttons.md` 6.3 |
| Bootloader | MCUboot, SMP | Adafruit UF2 0.11.0 | `components/mcu-radio.md` |
| Rear-face flank scoops | to about Y 43 | end by Y 35 | `components/enclosure-manufacturing.md` 7.3 |
| RTC | DS3231 with coin cell | none chosen (open question) | `COMPONENTS.md` 8 |
| Backlight | on/off, no PWM | PWM dimming | `components/display.md` 6.2 |

## 7. Unknowns

1. No unit has been measured, opened or reviewed by anyone outside the maker. Every geometry value comes from
   images; the shipped product may differ from the August 2025 drawing.
2. Whether any unit has reached a customer (no evidence as of 2026-11-13).
3. Exact switch model for each of the three variants (production units show a white PG1353D-style switch; blog
   images are Lofree x Kailh Shadow renders).
4. Charger part number, LDO confirmation, ESD part, battery connector series, encoder part number and detent count.
5. Keycap dish depth, plate and floor thickness, lens pocket depth, screw thread and head type, knob boss top
   diameter; the purpose of a small step in the key-well rear wall near the rear right key.
6. Battery life, charge time and charge current; radio range in the aluminium body.
7. Network-core firmware (not published); icon pixel size; the companion app itself (no installer public).
8. Legal entity and registration; any FCC, ISED or CE filing for the product.
9. Content of the maker's Discord, Instagram grid, X timelines and Reddit threads (login walls or bot blocks).
10. Whether a second colour (gunmetal or grey top) exists (guess from a few frames).

## 8. Sources

Maker sources (primary):

- Product page and catalogue: https://protadesigns.com/products/glyf , https://protadesigns.com/products/glyf.js ,
  https://protadesigns.com/products.json (cache `_cache/official-site/01-shopify`, `02-pages`).
- Development blog feed: https://protadesigns.com/blogs/updates.atom (Updates 01 to 06), Update 06:
  https://protadesigns.com/blogs/updates/update-06-glyf-development-gearing-up-for-production
- Plan drawing: https://protadesigns.com/cdn/shop/files/GLYFCABLESVG3.svg?v=1755130377 (`_cache/official-site/03-media/`).
- Product renders S5 to S8 and S13 in `_cache/official-site/03-media/`.
- YouTube channel https://www.youtube.com/@PROTADESIGNS ; key videos `sr0MIYEi678` (display drawing),
  `ScYz1Z_T1UY` (KiCad layout), `S9c5WuorsgQ` (December 2025 board), `kOclb0i9bug` (JLCPCB order), `Q6CKpc6AK0o`
  (Fusion side view), `Nk6MD9QS8VA` (weight), `LyKoZR8Q888` (bottom shell), `4mGhEPTLoSA` (feet), Autodesk
  interview `8WrTUNELp2U`. Cache `_cache/youtube/`, `_cache/geometry/yt-*`.
- TikTok https://www.tiktok.com/@protadesigns (cache `_cache/social/tiktok-*`).
- Beta firmware: https://github.com/noahbei/glyf-releases (cache `_cache/regulatory-software/firmware-06/`).
- Owner screenshots: `_cache/user/site-hero-and-essentials.png`, `_cache/user/site-side-profile-19mm.png`.

Third-party and registry sources:

- FCC mirror: https://fccid.io/2ALGY21069 (Holyiot-21069 filing and user manual).
- USPTO trademark search https://tmsearch.uspto.gov ; TMview https://www.tmdn.org/tmview/
- Kailh PG1353D drawing and socket CPG135001S30 drawing (`_cache/follow-switch-family-and-socket/pdf-01`).
- Yousee YX14011A datasheet (same glass as the GLYF panel):
  https://pdf.directindustry.com/pdf/shenzhen-yousee-technology-co-ltd/yousee-display-module-tft-lcd-yx14011a/4621447-1146135.html
- Hacker News comment https://hn.algolia.com/api/v1/items/44252387 (opinion only).

Research notes (each lists its own sources and blocked endpoints): `raw/official-site.md`, `raw/youtube.md`,
`raw/social.md`, `raw/community-press.md`, `raw/regulatory-software.md`, `raw/prior-art.md`,
`raw/conventions.md`, `raw/geometry.md`, `raw/follow-display-module-sourcing.md`,
`raw/follow-switch-family-and-socket.md`, `raw/follow-rf-exit-in-aluminium.md`,
`raw/follow-radio-module-choice.md`, `raw/follow-battery-cell-and-runtime.md`,
`raw/follow-maker-bom-part-numbers.md`.

Blocked or unreachable (summary): Wayback rate limits on most product-page snapshots; Instagram, X, Discord,
TikTok comments and Reddit behind logins or bot checks; official FCC search, fcc.report, California business
registry and OpenCorporates blocked; panelook, buydisplay and analog.com datasheet hosts blocked or failing.
