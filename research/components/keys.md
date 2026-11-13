# Decision record: key switches, sockets, keycaps and key matrix

Key: `keys`
Date: 2026-11-13
Status: proposed for the design phase; revised on 2026-11-13 after review (section 12)
Cache for this record: `research/_cache/keys/` (gitignored; sub-directories `jlc-01`, `lcsc-01`, `caps-01`,
`gateron-01` to `gateron-03`, `cherry-01`, `ds-01`, `shops-01`, `gh-01`, and `rev-01` for the revision).
The reviewer's own lookups are in `research/_cache/keys-sceptic/`.

Confidence words: **confirmed** means stated by the maker of the part or read from a primary source (datasheet,
drawing, live catalogue record). **likely** means consistent indirect evidence. **guess** means an inference
without direct support. "Not found" means the item was looked for and not found.

## 1. Decision in short

1. Switch family: Kailh Choc V2 (PG1353 footprint), MX cross stem, on a 19.05 mm pitch in both axes. Default
   part is a linear full-POM PG1353D (the GLYF part), bought as Lofree Ghost. The standard PG1353 is the
   documented alternative for the aluminium shell, because Kailh's PG1353D drawings say "this product only fits
   plastic plates". The standard PG1353 travels 3.2 mm instead of 2.8 mm and its hooks catch 1.65 mm below the
   flange instead of 1.35 mm; the shell rules below are set so that it fits without a change.
2. Hot-swap socket: Kailh CPG135001S30 (LCSC `C5333465`) on the PCB bottom side. JLCPCB cannot place it today
   (stock 0, "This product is no longer manufactured"), so the first batch of five is hand-soldered from
   sockets bought at a keyboard shop. The footprint stays placeable for a later consigned order.
3. Electrical scheme: a 5-column by 4-row matrix with one 1N4148W diode per position (JLCPCB basic part
   `C81598`), `col2row`, 20 positions: 16 keys, 2 encoder pushes, 2 round buttons. Nine GPIO. ZMK
   `zmk,kscan-gpio-matrix` with `wakeup-source`.
4. Plate: integrated in the top shell as the floor of the key well, a 1.15 +/-0.05 mm lip at each switch
   opening, plate top 2.20 mm above the PCB top face, openings 14.00 +0.05/-0 mm square. Lip and openings are
   stated after anodising. No separate plate.
5. Keycap: a project-drawn blank black low cap with a square spherical dish (GLYF look), MX stem, resin-printed
   in JLC3DP "JLC Black Resin" after a stem-fit coupon. The bought fallback is the Tai-Hao THT blank black PBT
   cap with MX stem (18.1 mm square, cylindrical dish).
6. Runner-up switch: Gateron KS-33 Low Profile 2.0. Its stack is 0.37 mm thicker than Choc V2 at the same cap
   height above the deck (section 6).

## 2. Context

The GLYF uses Kailh "Low Profile V2" full-POM hot-swap switches. The follow-up research identifies them as the
Kailh PG1353D series on Choc V2 footprints with two-barrel Kailh Choc sockets, per-key diodes, a 5 x 4
`col2row` matrix on direct GPIO, 19.05 mm pitch and switches clipped into the CNC aluminium top shell
(`research/raw/follow-switch-family-and-socket.md`, `research/raw/regulatory-software.md`,
`research/raw/youtube.md`; confirmed for pitch, matrix driver and diodes; likely for the PG1353D identity in
production units).

Measured GLYF geometry that the key stack must reconcile (`research/raw/geometry.md`, all likely unless marked):

| Quantity | GLYF value |
| --- | --- |
| Key pitch, X and Y | 19.05 mm (confirmed) |
| Keycap base, square / top face, square | 18.4 mm / 15.7 mm |
| Gap between caps | 0.64 mm |
| Keycap top above the top face (deck) | 4.4 mm |
| Keycap total height; side angle | 4.6 mm; 16.5 degrees from vertical |
| Dish | square 12.0 x 12.0 mm, corner radius about 1.7, depth about 0.6 (guess) |
| Key well depth, deck to plate top | 3.7 mm (guess, range 3.3 to 4.2) |
| Switch cut-out | 13.9 mm with dog-bone corners (likely); maker caliper 14.06 mm (confirmed reading) |
| Body thickness: front edge / rear wall / wedge apex ("19 mm") | 13.0 / 12.0 / 19.2 mm |
| Cap clearance to the key-well wall | 0.8 mm |

The "19 mm" claim is the thickest point of the body (19.2 mm at the wedge apex), not the height over the keys
(`research/raw/geometry.md` section 6, likely). The key stack below fits the 13.0 mm front edge with about
1.5 mm to spare (section 6.3), which agrees with that reading.

## 3. Requirements

1. Match the GLYF look: 4 x 4 blank black low square caps with a dished top, standing about 4.4 mm above the
   deck, on a 19.05 mm pitch.
2. Fit a body of 13 mm at the front edge without the wedge.
3. Hot-swap: switches can be changed without soldering. With the plate in the shell, hot-swap is also what lets
   the switches go in after the PCB is mounted.
4. Parts orderable today in quantities for five units (80 keys plus spares). Prefer parts JLCPCB can place.
5. Work with ZMK on an nRF52840 or nRF5340 module, including wake from deep sleep by any key, and fit the GPIO
   budget of the radio module (27 GPIO before extras, `research/raw/follow-radio-module-choice.md`).
6. Same switch footprint and cut-out for the FDM print and the CNC shell.

## 4. Candidates

### 4.1 Switch family

Heights are relative to the PCB top face. Stem top is the free (unpressed) position.

| Candidate | Plate top above PCB | Stem top above PCB | Travel | Stem | Hot-swap socket and JLCPCB stock today | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Kailh Choc V2 PG1353 / PG1353D | 2.20 (confirmed) | 8.60 (confirmed) | 2.8 +/-0.25 (PG1353D, PG1353 silent); 3.2 +/-0.25 on the standard PG1353 (D02 2020 and D03 2019 drawings, confirmed) | MX cross | Kailh CPG135001S30, `C5333465`, stock 0, not purchasable (confirmed) | **Chosen** |
| Gateron KS-33 Low Profile 2.0 | 2.50 (confirmed) | 8.95 (likely, derived) | 3.0 +/-0.2 | MX cross | Gateron KS-2P02B01-02, `C18212911`, stock 0 (confirmed) | **Runner-up** |
| Cherry MX (full height) with Kailh-type MX socket | 5.00 | 15.20 | 4.0 | MX cross | HanElectricity CPG151101S11-16, `C41430893`, JLCPCB stock 202,224 (confirmed) | Rejected |
| Kailh Choc V1 PG1350 | not checked | not checked | not checked | Choc (two prongs) | Same CPG135001S30, stock 0 | Rejected |
| Cherry MX Low Profile | not checked | 11.9 mm overall (maker) | not checked | short-skirt MX mount | No hot-swap socket found | Rejected |
| Kailh X-switch PG1425 | not checked | about half of a Choc V1 package (secondary) | 2.0 to 2.5 (sources disagree) | proprietary scissor | No hot-swap found; `C19712244` stock 0 | Rejected |

Reasons:

- **Choc V2 chosen.** It is the GLYF's family, so look and feel match. It is the thinnest MX-stem stack with a
  public drawing (0.35 mm lower stem top than KS-33). Kailh's PG1353D drawing prints the switch outline, the
  PCB pattern and the socket pattern (`research/raw/follow-switch-family-and-socket.md` sections 3 to 5,
  confirmed). Switches are on sale today (section 7.1).
- **KS-33 runner-up.** MX stem, cheap (keeb.io lists KS-33 Red at 0.25 each, in stock today), Gateron publishes
  the switch and socket drawings. It loses on stack height (+0.37 mm body), on travel (3.0 mm against 2.8 mm,
  which also costs cap clearance) and on GLYF parity. Its socket is also out of stock at JLCPCB, so it brings no
  sourcing gain. Gateron's UK store says the KS-33 2.0 suits only keyboards designed for it (search summary of
  https://www.gateron.uk/products/gateron-ks-33-low-profile-2-0-mechanical-switch-black-bottom-housing; likely).
- **Cherry MX rejected.** It is the only family whose socket JLCPCB can place today, but the plate sits 2.8 mm
  higher and the stem top 6.6 mm higher than Choc V2 (family values: MX plate top 5.0 mm above the PCB, stem
  top 10.2 mm above the plate, `macropad/board.toml` `[stack]` and `macropad/cad/macropad_case/components.py`;
  Cherry MX2A datasheet total height 18.5 mm, https://cdn.sparkfun.com/assets/a/9/b/6/2/MX2A_RED-Datasheet-EN_US.pdf;
  confirmed). The body over a socket grows from 11.45 mm to about 18 mm (section 6.3), so a 13 mm front edge is
  impossible. Function (slim body) beats the placement fee.
- **Choc V1 rejected.** Its Choc stem rules out MX-stem caps, including a printed MX-stem cap. It uses the same
  out-of-stock socket, so it brings no sourcing gain. Choc 1u caps such as MBK are 17.5 x 16.5 mm
  (https://splitkb.com/products/blank-mbk-choc-low-profile-keycaps, confirmed), which leaves uneven 1.55 and
  2.55 mm gaps on a 19.05 mm grid. Its height was not checked.
- **Cherry MX Low Profile rejected.** Cherry gives 11.9 mm height
  (https://www.cherry.de/en-us/products/switches/mx-low-profile, search summary, likely). It is not
  pin-compatible with MX, and the cap mount takes short-skirt caps only
  (https://deskthority.net/wiki/Cherry_MX_Low_Profile, search summary, likely). No hot-swap socket was found.
- **Kailh X-switch PG1425 rejected.** A scissor switch with a proprietary cap mount, so no GLYF-style cap
  exists for it (https://deskthority.net/wiki/Kailh_PG1425_series, search summary, likely). No hot-swap socket
  was found, and `C19712244` (CPG142501D02) shows stock 0 at JLCPCB today (confirmed).

### 4.2 Hot-swap socket

| Candidate | Fits Choc V2 | Below PCB | Availability today | Verdict |
| --- | --- | --- | --- | --- |
| Kailh CPG135001S30 (Choc socket) | Yes: the PG1353D drawing shows its two 3.00 mm holes and 2.60 mm pads (confirmed) | 1.85 +/-0.1 mm | JLCPCB `C5333465`: stock 0, `isBuyComponent 0`, `noBuyReason` "This product is no longer manufactured". LCSC: stock 0, `productCycle sold_out`. splitkb.com "Kailh Hotswap Sockets", Choc / Black, 50 pieces, 6.57 in the shop's base currency, available. (all confirmed) | **Chosen** |
| Kailh-type MX socket (HanElectricity CPG151101S11-16, `C41430893`) | No (MX pin pattern) | 1.85 mm (family value) | JLCPCB stock 202,224, LCSC 141,410, 0.0449 USD | Rejected with MX |
| Gateron KS-2P02B01-02 ("KS-27 Keyswitch Connector (2.0)") | No (KS-27/KS-33 pattern: 5.1 mm centre, holes 3.0 mm) | 1.87 +/-0.05 mm, 3.00 with barrels | JLCPCB `C18212911`: stock 0 | Runner-up's socket |
| Mill-Max hot-swap receptacles (splitkb "Mill-Max Hot Swap Sockets", 40 pieces, 16.49, available) | Not checked for the Choc V2 blade pins | not checked | Hand-soldered through-hole, two per key | Rejected: two parts per key, fit not checked, more cost |
| No socket, switches soldered | n/a | 1.4 mm pin tips | n/a | Rejected: the plate is in the shell, so soldered switches would weld shell and PCB together, and JLCPCB cannot place THT switches anyway |

JLCPCB also lists three customer-consigned records for this socket: `C9900009224` and `C9900248317`
("CPG135001S30") and `C9900010116` ("Kailh Low-Profile Hot-Swappable Socket"), all stock 0 and owned by
"JLCPCB Assembly". That pattern shows other customers consign Choc sockets for SMT assembly (likely). Source:
JLCPCB parts API, keywords `CPG135001S30` and `low profile hot swap` (`jlc-01/`).

### 4.3 Electrical scheme

| Candidate | GPIO for 16 keys + 2 pushes + 2 buttons | Parts | Wake from ZMK deep sleep and soft off | Verdict |
| --- | --- | --- | --- | --- |
| 5 x 4 matrix, one diode per position, `col2row` | 9 | 20 diodes | `zmk,kscan-gpio-matrix` has `wakeup-source`; for soft off, the column pins go in `extra-gpios` (https://zmk.dev/docs/config/kscan, https://zmk.dev/docs/config/power, confirmed) | **Chosen** |
| One GPIO per key (`zmk,kscan-gpio-direct`) | 20 | none | `wakeup-source` supported (same pages, confirmed) | Rejected: 11 more pins. The radio note's E73 module has 2 to 4 spare pins with a 9-pin matrix in the 27-pin budget (`research/raw/follow-radio-module-choice.md`, confirmed pin table) |
| Matrix without diodes | 9 | none | as above | Rejected: ghosting with three or more keys held, which macros and layer keys make likely |
| GPIO expander (the GLYF prototype 2 used an MCP23S17 class part) | 2 to 4 bus pins | expander IC | depends on the expander driver; not checked | Rejected: more parts; the GLYF dropped it for production (`research/raw/regulatory-software.md`, likely) |

The 4 x 4 key grid plus a fifth column for the control column matches the GLYF's decoded firmware: 5 outputs,
4 pull-down inputs, 20 positions (`research/raw/regulatory-software.md`, likely for the pin decode, confirmed
for the matrix driver).

Diode candidates (JLCPCB parts API and LCSC product detail API, read 2026-11-13, confirmed):

| Part | Package | LCSC | Class | JLCPCB stock | LCSC stock | Price (1+) | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1N4148W, Semtech | SOD-123 | `C81598` | basic | 3,288,334 | 1,867,300 | 0.0124 USD | **Chosen**: basic part, family convention (worxboard uses SOD-123), easy hand rework |
| 1N4148WS, JSCJ | SOD-323 | `C2128` | basic | 4,129,458 | 2,137,000 | 0.0110 USD | Acceptable substitute; smaller, harder to rework |
| 1N4148W, Changjing | SOD-123 | `C2099` | extended | 823,238 | not read | 0.0108 USD | Rejected: extended part fee for no gain |

### 4.4 Plate

| Candidate | Effect on the stack | Verdict |
| --- | --- | --- |
| Integrated in the top shell: the key-well floor is the plate, 1.15 mm lip at each opening | No extra part; the GLYF does this (`research/raw/geometry.md` 7.5, likely) | **Chosen** for both the CNC shell and the FDM print |
| Separate 1.2 mm FR4 or aluminium plate (for example a JLCPCB plate panel) | Needs its own support and screws inside the shell; the shell floor above it must be cut away anyway | Rejected: one more part and fastening path for no gain at this size |
| Thicker shell floor with relief pockets from below, leaving a 1.15 mm lip | Stiffer floor between keys | Allowed locally (for example round screw bosses), not needed across the key field |

The lip must fit the switch hook gap. PG1353D: flange underside to snap hook 1.35 +0/-0.10 mm, so 1.25 to
1.35 mm (confirmed, Kailh drawing `CPG1353D01D01-16`). Standard PG1353: 1.65 mm, no tolerance printed
(confirmed, drawings `CPG135301D02` rev A and `PG135301D03`; 1.62 mm when scaled on the side view). The lip is
1.15 +/-0.05 mm after anodising (1.10 to 1.20 mm). It leaves 0.05 to 0.25 mm slack under the PG1353D hooks and
0.45 to 0.55 mm under the PG1353 hooks. The first version used 1.20 +/-0.05 mm; its upper limit equals the
1.25 mm minimum hook gap before any anodic film is counted, so it was moved down (review issue 5). The task's
"1.2 to 1.3 mm for Choc" range is too wide: a 1.30 mm lip exceeds the 1.25 mm minimum gap.

### 4.5 Keycap

| Candidate | Stem | Size | Top | Blank black | Availability today | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| Project-drawn cap, resin-printed in JLC3DP "JLC Black Resin" | MX cross | 18.2 base, 15.6 top, 4.4 tall (section 6.5) | square spherical dish, like the GLYF | yes | Made to order. JLC Black Resin, page read on 2026-11-13: heat deflection 54 to 65 degC (ASTM D648 at 66 psi), +/-0.2 mm within 100 mm, "Recommended Wall Thickness: > 0.8mm", "From $1.0" (https://jlc3dp.com/help/article/jlc-black-resin, confirmed). Imagine Black: heat deflection 46 degC, "from 2.00 USD" (https://jlc3dp.com/fr/help/article/Imagine-Black---Photosensitive-Resin, search summary, likely), rejected for the lower heat deflection | **Chosen** |
| Tai-Hao THT ("Tai-Hao Thins"), PBT, MX stem | MX cross | 18.1 x 18.1 mm (https://kbd.news/THT-Tai-Hao-low-profile-keycaps-2276.html, confirmed) | uniform cylindrical dish | yes | keeb.io "Tai-Hao THT PBT Blank Keyset", Black, 37.99, available; mechanicalkeyboards.com "Tai-Hao Black THT Blank 18 Key PBT", MX, 8.49, not available today (Shopify `.js` and `products.json`, confirmed) | **Fallback**, bought |
| FKcaps LPF, MX stem | MX cross | not found | uniform, "ultra low profile" | Shops checked sell legended sets only (keeb.io "LPF Legend Glow MX Keycap Set" Black 54.99, available) | Rejected: no blank black set found |
| MBK (Choc stem) | Choc V1 only | 17.5 x 16.5 mm | scooped | yes | keeb.io and splitkb, available | Rejected: Choc V1 stem, rectangular |
| NuPhy nSA, Keychron LSA (low-profile spherical sets) | MX cross | not found | spherical | Legended sets found; blank not found | nSA height 5.5 mm per a secondary article (https://www.pulse.bot/..., guess) | Rejected: no blank set found |

Keebio states that THT and LPF MX caps are "Compatible with: Kailh Choc V2, Gateron KS-33 (MX stem)"
(https://blog.keeb.io/low-profile-keycap-options-what-works-with-what/, 2026-03-23, confirmed quote).

Why the printed cap leads: the GLYF look is a square spherical dish and an 18.4 mm cap; no bought blank set
with that dish was found. The CAD package can draw the cap from the measured GLYF numbers without copying any
vendor model. THT is the safe bought cap: PBT, a known fit on Choc V2, close in size, but cylindrical.

## 5. Decision

1. **Switch:** Kailh Choc V2 footprint (PG1353 family). Buy a linear full-POM PG1353D for GLYF parity: Lofree
   Ghost (linear, 106 for 59.00, available on 2026-11-13), or Kailh White Rain where a shop has it. The only
   PG1353D drawing on file is the linear type, and production GLYF units show a white full-POM switch
   (`research/raw/follow-switch-family-and-socket.md` line 41, likely). keeb.io's Black Cloud is the tactile
   variant of the same family: a valid choice, but not the parity part. For the CNC shell, test PG1353D
   retention in the first machined shell. If it fails, use the standard PG1353 (Kailh "Choc V2 Low Profile
   Switch Set", CPG135301D01/D02/D03). It carries no plate-material note and fits the same footprint and
   opening, but it travels 3.2 +/-0.25 mm and its hooks catch 1.65 mm below the flange. Its stack is in
   section 6.3, and the shell rules in section 8 already allow for it.
2. **Pitch:** 19.05 mm in X and Y.
3. **Socket:** Kailh CPG135001S30, PCB bottom side, hand-soldered for the first five units. Buy 100 (two
   50-packs). Keep the footprint and rotation data ready for JLCPCB consignment.
4. **Matrix:** 5 x 4, `col2row`, one 1N4148W (`C81598`) per position, 20 diodes on the bottom side.
5. **Plate:** integrated, 1.15 +/-0.05 mm lip and 14.00 +0.05/-0 mm openings, both stated after anodising.
6. **Keycap:** project-drawn cap printed in JLC Black Resin (section 6.5), ordered after a stem-fit coupon; THT
   blank black as the bought fallback.
7. **Runner-up for the stack comparison:** Gateron KS-33 Low Profile 2.0 with the KS-2P02B01-02 socket.

## 6. Numbers the design needs

### 6.1 Choc V2 footprint (top view, origin at the switch centre, x to the right, y towards the front edge)

Orientation as on the GLYF: sockets on the front side of each centre hole, the switch LED window towards the
rear edge (`research/raw/follow-switch-family-and-socket.md` 5.3 and 7, likely). No per-key LEDs are planned.

| Feature | Position (mm) | Size (mm) | Source, confidence |
| --- | --- | --- | --- |
| Centre hole, NPTH | (0, 0) | 5.00 to 5.05 | Kailh drawing; kiswitch uses 5.05. Confirmed |
| Socket barrel hole at switch pin 2, NPTH | (0, +6.00) | 3.05 | Kailh's socket pattern puts this barrel at 6.00, 0.10 mm from the switch pin at 5.90, with the note "此尺寸与产品中心距差0.1mm,不影响使用" ("differs from the product centre distance by 0.1 mm, does not affect use"). Confirmed (PG1353D sheet 2). Diameter: barrels 2.90 +/-0.1 (confirmed); 3.05 (kiswitch value) gives 0.075 mm radial clearance nominal and 0.025 mm at the largest barrel (derived) |
| Socket barrel hole at switch pin 1, NPTH | (-5.00, +3.80) | 3.05 | Kailh pattern and switch pin agree here. Confirmed |
| Third hole (PG1353 third leg, PG1353D clearance) | (+5.00, -5.15) | 1.6 round or 2.0 x 1.5 slot | Confirmed |
| Socket pads, bottom copper | (+3.50, +6.00) and (-8.50, +3.80): 3.50 mm outside each barrel hole on the socket's long axis | 2.55 x 2.50 (kiswitch) to 2.60 square (Kailh) | Kailh 2.60; kiswitch 2.55 x 2.5 at 3.5 mm, its pad already on the 6.00 line. Confirmed (size), likely (position). Pad extents: x +2.225 to +4.775 and -9.775 to -7.225 |
| PCB thickness | n/a | 1.6 | Kailh socket drawing "Single face board T=1.6mm". Confirmed |

Do not combine a 5.90 mm hole position with a 3.00 mm hole. The barrels are 2.20 mm apart across the socket,
holes at 5.90 and 3.80 are 2.10 mm apart, and the 0.10 mm offset uses all of the 0.05 mm radial clearance of
a 3.00 mm hole (review issue 3). Kailh's own pattern (3.00 at 6.00) and kiswitch (3.05 at 5.90) avoid that
combination; ceoloide (3.00 at 5.95) halves the offset. This record takes Kailh's barrel position with the
kiswitch diameter, which gives the most clearance of these options.

A Choc V1/V2 hybrid adds two 1.9 mm NPTH at (+/-5.5, 0) for V1 side posts (kiswitch
`SW_Hotswap_Kailh_Choc_V1V2`, confirmed). Not needed here, because V1 cannot take MX-stem caps.

### 6.2 Plate, openings and webs

| Item | Value | Basis |
| --- | --- | --- |
| Plate top face above PCB top face | 2.20 mm | Kailh drawing, confirmed |
| Lip thickness at each opening, CNC | 1.15 +/-0.05 mm after anodising, marked FIT-CRITICAL on the CNC drawing | PG1353D hook gap 1.25 to 1.35 mm, PG1353 1.65 mm (confirmed). Type II anodic growth of about 0.005 to 0.0125 mm per surface (general practice, guess) can push a lip machined to its upper limit past 1.25 mm, so the value is stated after finish and centred 0.10 mm under the minimum hook gap |
| Lip thickness, FDM | 1.0 or 1.2 mm (whole 0.2 mm layers), chosen on the fit coupon | Print layers are 0.2 mm (`research/raw/conventions.md`); 1.15 mm is not a layer multiple |
| Free gap, lip underside to PCB top | 1.05 mm (the snap hooks live here) | Derived, confirmed arithmetic |
| Opening | 14.00 +0.05/-0 mm square after anodising | Body 13.95 +/-0.05 (confirmed); opening derived (likely); maker caliper 14.06 (confirmed reading). Stated after finish because the anodic film narrows the opening |
| CNC corners | dog-bones, tool 1.0 to 1.5 mm | Family convention (`research/raw/conventions.md` 3.5, 5.3) |
| FDM openings | 14.0 mm nominal; print 13.9 / 14.0 / 14.1 coupons | Family convention |
| Web between openings | 5.05 mm; about 4.6 mm at 1.5 mm dog-bones | 19.05 - 14.00; dog-bone bite 0.29 x tool radius per side (derived) |
| Minimum web anywhere in the key field | 4.0 mm (recommendation for 1.2 mm aluminium; FDM rule is 0.8 mm) | guess |
| Gap between neighbouring switch flanges | 4.05 mm (flanges 15.00 square) | Confirmed arithmetic |
| PCB seat | The case must hold the PCB top face 2.20 mm below the plate top, +/-0.1 (1.05 mm below the lip underside) | Derived |

### 6.3 Vertical stack-up

Heights in millimetres. Column "PCB" is relative to the PCB top face. Column "deck" is relative to the top face
of the shell (the deck), which is placed level with the cap skirt bottom at rest, as on the GLYF. The cap is
the project cap of section 6.5: skirt bottom 2.40 mm below the stem top, cap top 2.00 mm above the stem top,
so the cap stands 4.40 mm above the deck in both columns. The Choc V2 columns use the PG1353D; the standard
PG1353 fallback follows in the second table.

| Level | Choc V2, PCB | Choc V2, deck | KS-33, PCB | KS-33, deck | Source |
| --- | --- | --- | --- | --- | --- |
| Keycap top, at rest | +10.60 | +4.40 | +10.95 | +4.40 | derived from cap rule |
| Stem top, at rest | +8.60 | +2.40 | +8.95 | +2.40 | Kailh: 6.40 above plate (confirmed). Gateron: 12.2 overall minus 5.75 below plate = 6.45 above plate (likely; the drawing scales to the same value) |
| Keycap top, pressed (nominal; with travel tolerance) | +7.80 (7.55 to 8.05) | +1.60 | +7.95 (7.75 to 8.15) | +1.40 | travel 2.8 +/-0.25 (Kailh, confirmed); 3.0 +/-0.2 (Gateron, confirmed) |
| Deck = cap skirt bottom at rest | +6.20 | 0 | +6.55 | 0 | design choice |
| Switch housing top / collar rim | +5.30 / +5.70 | -0.90 / -0.50 | +5.85 | -0.70 | Kailh 5.30 and 5.70 above the housing bottom (PG1353D side view, confirmed); Gateron 3.35 above plate (confirmed) |
| Stem top, pressed | +5.80 | -0.40 | +5.95 | -0.60 | derived |
| Cap skirt bottom, pressed (worst case) | +3.40 (3.15) | -2.80 | +3.55 (3.35) | -3.00 | derived |
| Switch flange top | +3.00 | -3.20 | not read | not read | Kailh flange about 0.8 mm thick, scaled on the PG1353D and PG1353 side views (likely) |
| Plate top face | +2.20 | -4.00 | +2.50 | -4.05 | Kailh, Gateron drawings, confirmed |
| Plate underside (Choc V2: 1.15 lip; KS-33: 1.20 plate) | +1.05 | -5.15 | +1.30 | -5.25 | Choc V2 lip from section 6.2; Gateron prints 1.20 +/-0.05 plate (confirmed) |
| Snap hook catch | +0.85 (0.85 to 0.95) | -5.35 | not read | not read | Kailh 1.35 +0/-0.10 below the flange underside (confirmed) |
| PCB top face | 0 | -6.20 | 0 | -6.55 | |
| PCB bottom face | -1.60 | -7.80 | -1.60 | -8.15 | |
| Switch pin tips | -3.00 +/-0.2 | -9.20 | -2.60 | -9.15 | Kailh 3.00 below housing (confirmed); Gateron 2.60 (confirmed) |
| Centre post tip (inside the 5 mm hole) | -3.30 | -9.50 | -3.25 | -9.80 | Kailh 3.30 (confirmed); Gateron 5.75 - 2.50 (confirmed) |
| Socket underside | -3.45 (+/-0.10) | -9.65 | -3.47 (+/-0.05) | -10.02 | Kailh 1.85 +/-0.1 (confirmed); Gateron 1.87 +/-0.05 (confirmed) |
| Clearance 0.30 below the nominal socket underside | -3.75 | -9.95 | -3.77 | -10.32 | recommendation |
| Underside of a 1.5 mm floor | -5.25 | -11.45 | -5.27 | -11.82 | floor value is the case subsystem's; 1.5 is an example |

Result: minimum body thickness over a socket, deck to underside, is **11.45 mm for Choc V2** and **11.82 mm for
KS-33** with a 1.5 mm floor and 0.3 mm clearance. Each extra 0.1 mm of floor or clearance adds 0.1 mm. The
GLYF front edge is 13.0 mm, so the Choc V2 stack leaves about 1.55 mm there (likely, from the GLYF geometry).

For comparison only, full-height MX with the same cap rule: plate top +5.00, stem top +15.20, deck +12.80,
socket underside -3.45; deck to underside 18.05 mm with the same floor and clearance (derived from family
values; the macropad body is 17.5 mm with a different stack, `research/raw/conventions.md` 3.6).

Standard PG1353 fallback in the same shell and footprint, with the same project cap (only the levels that
differ from the PG1353D; review issue 2):

| Level | PG1353, PCB | PG1353, deck | Source |
| --- | --- | --- | --- |
| Stem top, at rest | +8.60 | +2.40 | 6.40 above the plate (`CPG135301D02` drawing, confirmed) |
| Keycap top, pressed | +7.40 (7.15 to 7.65) | +1.20 (0.95 to 1.45) | total travel 3.2 +/-0.25 (`CPG135301D02` rev A 2020 and `PG135301D03` 2019, confirmed) |
| Stem top, pressed | +5.40 (5.15 to 5.65) | -0.80 | derived |
| Housing top | +5.30 | -0.90 | 3.10 above the plate (`CPG135301D02`, confirmed) |
| Cap skirt bottom, pressed (worst case) | +3.00 (2.75) | -3.20 | derived |
| Switch flange top | +3.00 | -3.20 | about 0.8 mm flange, scaled (likely) |
| Plate top face | +2.20 | -4.00 | confirmed |
| Plate underside, 1.15 lip | +1.05 | -5.15 | section 6.2 |
| Snap hook catch | +0.55 | -5.65 | 1.65 below the flange underside, no tolerance printed (confirmed) |

The socket, PCB, pin and floor levels are the same as for the PG1353D, so the body thickness does not change.

Pressed clearance budget:

1. PG1353D: the cap skirt bottom comes down to 1.20 mm above the plate top (0.95 mm worst case). The pressed
   cap top is 1.60 mm above the deck.
2. PG1353 fallback: the cap skirt bottom comes down to 0.80 mm above the plate top (0.55 mm worst case), and
   up to 0.25 mm below the flange top, so the skirt opening must clear the flange (section 6.5). The pressed
   cap top is 1.20 mm above the deck.
3. Design rule, set by the fallback because it must stay possible in the same shell: anything standing on
   the plate top inside a cap's footprint must stay at or below 0.25 mm, leaving 0.3 mm margin. In practice
   the plate top under the caps is flat, and screw heads in the key field sit flush with it or below it.
   An M2 head does not fit on a 1.15 mm lip; screws in the key field need a recess in a local boss or a
   different position (case subsystem). With the PG1353D only, the limit would be 0.65 mm.
4. Cap roof: at full travel the stem top comes to 0.10 mm above the PG1353D collar rim (+5.70) and 0.10 mm
   above the PG1353 housing top (+5.30), and passes both at worst-case travel. A cap roof that is flat at the
   stem-top level would bottom on the switch housing. The project cap therefore has a roof relief (section
   6.5).

Retention of the fallback: with the 1.15 mm lip the PG1353 hooks catch 0.45 to 0.55 mm below the lip
underside. The flange rests on the plate top and the housing bottom on the PCB top, so the switch does not
move in use. Under a keycap pull it can lift about 0.5 mm before the hooks catch, and the socket grip holds
it. The plate top sets the switch height; the PCB seat tolerance (+/-0.1) decides whether the flange or the
housing bottom carries the load.

### 6.4 Keep-outs

Top side of the PCB (switch side):

1. No component inside a 14.6 mm square around each switch centre: the housing bottom sits on the PCB top
   face and the snap hooks need the 1.05 mm gap under the lip (derived). The GLYF has all SMD parts on the
   bottom side (`research/raw/youtube.md`, confirmed), and the same is recommended here.

Bottom side of the PCB, per key (top-view frame of section 6.1; the socket is mirrored onto the bottom copper):

1. Socket zone: x -10.1 to +5.1 mm, y +1.0 to +8.7 mm. No PCB component may sit in it except the socket.
   Clear depth below the PCB bottom: at least 2.15 mm (1.85 + 0.1 tolerance + 0.2 margin). Basis: on the Kailh
   socket drawing each 4.65 mm body section is centred on its barrel, so the body edge lies 2.30 to 2.33 mm
   outside the barrel centre (measured at 57 px/mm on the top view and 66 px/mm on the bottom view). With the
   barrels at y +3.80 and +6.00, the body spans y +1.47 to +8.33 nominal, and +1.30 to +8.50 with the
   6.85 +/-0.1 tolerance and 0.075 mm hole play. The kiswitch courtyard, moved 0.10 mm with the barrel, ends at
   +8.55. In x the pads set the limits (-9.775 to +4.775). The first version ended the zone at +7.9 mm, which
   cut up to 0.6 mm off the socket (review issue 1).
2. Centre post: a 5.5 mm circle at (0, 0), depth 1.70 mm below the PCB bottom plus margin (confirmed post
   length).
3. Third leg of the standard PG1353: a 3.0 mm circle at (+5.00, -5.15), depth 1.40 mm below the PCB bottom
   plus margin (PG1353 has three legs of 3.00 +/-0.2 mm, confirmed).
4. Soldering access: keep 1.0 mm free beyond each socket pad end, because the sockets are hand-soldered.
5. Diodes (SOD-123, 3.55 to 3.85 x 1.55 to 1.65 mm, at most 1.15 mm tall, Semtech datasheet, confirmed) go
   behind the centre post: the band y -10.0 to -3.0 mm, x -9.0 to +3.0 mm in each key's frame. The band is
   bounded by the previous row's socket zone (front edge at 8.7 - 19.05 = -10.35 mm), the centre-post circle
   (y -2.75 mm) and the third-leg circle at (+5.00, -5.15). Example: a horizontal SOD-123 centred at
   (-3.0, -6.5). The gap between neighbouring socket zones in a row is only 19.05 - 15.2 = 3.85 mm, and about
   2.5 mm after the 1.0 mm soldering access at each pad end. A SOD-123 turned 90 degrees still fits there, but
   it is not the default. The first version called this a 4.5 mm gap; that is the pad-end to pad-end distance
   (review issue 7).

Insertion support: inserting a switch pushes the socket away from the PCB with up to 3.0 kgf (Kailh socket
mating force, confirmed). The PCB needs support under each socket while switches go in: either insert switches
only with the bottom shell closed and a floor or ribs within 0.3 mm of the socket undersides, or use an
insertion jig. A support rib sits under the socket body, inside the zone outline and 0.2 to 0.4 mm below the
socket underside. A rib or part beside the zone must stay outside y +8.7 mm. Unsupported insertion can tear the pads off (guess, common keyboard-builder advice; not checked
against a primary source).

### 6.5 Project keycap

Drawn in the project CAD package from the GLYF measurements. No vendor model is used.

| Item | Value | Basis |
| --- | --- | --- |
| Base, square, at the skirt bottom | 18.20 mm | GLYF 18.4 (likely); reduced 0.2 for the +/-0.2 mm resin tolerance. Gap 0.85 mm nominal, 0.45 mm worst |
| Top face, square | 15.60 mm | GLYF 15.7 (likely), same 16.5 degree side angle |
| Height, skirt bottom to top edge | 4.40 mm | GLYF cap top 4.4 above the deck (likely) |
| Dish | square 12.0 x 12.0 mm, corner radius 1.7, spherical, 0.6 mm deep | GLYF (likely; depth a guess) |
| Top edge radius | 0.5 mm | GLYF (likely) |
| Stem socket | MX cross for arms 4.00 +/-0.05 long and 1.30 +0/-0.05 thick (Kailh, confirmed); slot width set by a printed coupon at 1.30 / 1.35 / 1.40 / 1.45 mm | Resin tolerance +/-0.2 mm |
| Cross slot length | 4.10 mm | Arms 4.00 +/-0.05 (Kailh, confirmed) |
| Stem socket position | a roof ring from the post out to Ø6.8 seats on the stem top; skirt bottom 2.40 mm below the stem top | Section 6.3 |
| Roof relief | outside Ø6.8 the roof underside sits 0.50 mm above the stem top | Keeps 0.35 mm at worst-case travel over the PG1353D collar rim (+5.70) and the PG1353 housing top (+5.30) (section 6.3, item 4). The seat ring stays inside the collar opening (inner about Ø7.7, outer about Ø8.4, scaled on the PG1353D top view, likely). The roof stays at least 0.9 mm thick under the dish (derived) |
| Post outer diameter | 5.20 mm nominal; coupon at 5.00 / 5.20 / 5.40 against a real switch | The post enters the stem bore, Ø5.50 on the PG1353D top view. Ø6.50 is the stem column outer (side view), and 5.70 is a height, housing bottom to collar top (side view), not a diameter (review issue 4). 5.20 plus the 0.2 mm resin tolerance still leaves 0.05 mm radial clearance (derived) |
| Post wall at the slot ends | 0.55 mm at a 5.20 mm post and 4.10 mm slot | Below JLC3DP's "> 0.8mm" recommendation. Any MX-stem cap for this bore has at most (5.50 - 4.05) / 2 = 0.72 mm here, so the coupon decides (derived) |
| Skirt inner opening | 16.0 mm square | With the PG1353 fallback the pressed skirt passes up to 0.25 mm below the flange top, so it must clear the 15.00 mm flange: 0.5 mm per side, 0.4 mm at the resin tolerance (derived) |
| Wall | 1.1 mm at the skirt bottom, (18.20 - 16.0) / 2 | JLC3DP "Recommended Wall Thickness: > 0.8mm" (confirmed, read on 2026-11-13) |
| Clearance, cap base to key-well wall | at least 0.8 mm | GLYF 0.8 (likely). With 18.2 mm caps the GLYF well of 78.15 mm lip to lip gives 1.4 mm |
| Quantity | 96 (80 plus one spare set) | |

With the THT fallback the deck height must be checked on a real cap: THT height was not found. The stack rule
still holds: with c the wanted clearance above the plate top, the cap skirt bottom may sit at most
6.40 - 3.45 - c mm below the stem top at rest for the standard PG1353 (worst-case travel 3.45 mm), or
6.40 - 3.05 - c mm for the PG1353D alone. If the THT skirt opening does not clear the 15.00 mm flange, measure
c from the flange top (about 0.8 mm above the plate top, likely) instead of the plate top.

### 6.6 Matrix and firmware

| Item | Value | Source, confidence |
| --- | --- | --- |
| Shape | 5 columns (outputs) x 4 rows (inputs) | design; same as the GLYF (likely) |
| Positions | C0 to C3 x R0 to R3: the 4 x 4 keys. C4: R0 encoder 1 push, R1 encoder 2 push, R2 button 1, R3 button 2 | design |
| Diode direction | `col2row`: anode on the column side of the switch, cathode towards the row | ZMK docs, confirmed |
| Inputs | rows with internal pull-down | ZMK matrix default for `col2row` (likely); GLYF uses pull-downs (likely) |
| Driver | `zmk,kscan-gpio-matrix`, `diode-direction = "col2row"`, `wakeup-source`; debounce defaults 5 ms press and release | https://zmk.dev/docs/config/kscan, confirmed |
| Deep sleep | `CONFIG_ZMK_SLEEP=y`, `CONFIG_ZMK_IDLE_SLEEP_TIMEOUT` (default 900000 ms) | https://zmk.dev/docs/config/power, confirmed |
| Soft off | GPIO key wakeup trigger with `wakeup-source`; for a `col2row` matrix, the column pins go in `extra-gpios` | same page, confirmed |
| GPIO supply | at least 2.7 V. A pressed key presents VDD minus the diode drop at the row input. 1N4148W drop is at most 0.715 V at 1 mA (confirmed). The nRF52840 input high threshold is 0.7 x VDD (likely, nRF52840 Product Specification, not re-read). At 3.0 V: 2.29 V against 2.10 V. At 1.8 V the scheme fails | derived |
| Current with one key held | about 0.23 mA through the internal pull-down (3.0 V / about 13 kOhm) | pull resistance from the nRF52840 Product Specification, likely, not re-read |
| Encoder rotation | not in the matrix; A/B pins are separate and do not wake the device unless configured | interface to the encoder subsystem |

### 6.7 Bill of materials for five units

| Item | Part | Code | Class | Stock / availability read on 2026-11-13 | Price read | Qty for 5 units |
| --- | --- | --- | --- | --- | --- | --- |
| Switch, full POM, linear | Kailh PG1353D class: Lofree Ghost (parity part); Kailh White Rain if a shop has it; keeb.io Black Cloud is the tactile option | none at LCSC | hand-fit | Lofree Ghost 106-pack: available (re-read on 2026-11-13, `rev-01/`). keeb.io Black Cloud: available in the catalogue read earlier the same day; the reviewer's re-read hit a Cloudflare challenge and was not retried | Lofree 59.00 per 106; keeb.io 0.70 each, 100 for 69.99 (shop base currencies) | 80 + 16 spare (one 106-pack) |
| Switch, fallback | Kailh Choc V2 set CPG135301D01/D02/D03 (standard PG1353) | none at LCSC. JLCPCB library codes: `C45350823` (D01, stock 0, purchasable flag 1, no LCSC record), `C5142796` (D02, stock 0, flagged discontinued) | hand-fit | kailh.net 110-switch set: available | 66.00 per 110 (shop base currency) | only if the aluminium retention check fails |
| Hot-swap socket | Kailh CPG135001S30 | `C5333465` | extended; not purchasable | JLCPCB 0, LCSC 0 (`sold_out`); splitkb 50-pack available | JLCPCB last 0.1617 USD (1+); splitkb 6.57 per 50 (shop base currency) | 80 + 20 spare |
| Diode | 1N4148W, SOD-123, Semtech | `C81598` | basic | JLCPCB 3,288,334; LCSC 1,867,300 | 0.0124 USD | 100 (machine-placed) |
| Keycap | project cap, JLC3DP black resin | none | 3D print order | made to order | not quoted | 96 |
| Keycap fallback | Tai-Hao THT PBT blank keyset, black, MX | none | bought | keeb.io: available | 37.99 per keyset | 1 set per unit if used; set contents not stated |

## 7. KiCad libraries

Checked in `kicad/kicad:10.0.7` (confirmed by listing):

1. Footprint: no Choc, Kailh or hot-swap footprint in the stock libraries. `Button_Switch_Keyboard.pretty`
   holds 29 footprints, all Cherry MX. The project needs its own Choc V2 hot-swap footprint in
   `pcb/lib/worxpad.pretty`, written from the Kailh drawing numbers in section 6.1 and checked against kiswitch
   `SW_Hotswap_Kailh_Choc_V2` (repository carries a CC-BY-SA licence file, so its file is not copied).
2. Symbols: `Switch:SW_Push` and `Diode:1N4148W` exist. `Diode_SMD:D_SOD-123` exists.
3. 3D models: the image has no `/usr/share/kicad/3dmodels` directory. Stock footprints point at
   `${KICAD10_3DMODEL_DIR}`. Switch, socket and cap shapes for the case checks come from the CAD package's
   datasheet-based components (`research/raw/conventions.md`, `components.py` pattern).

## 8. Consequences for other subsystems

1. **PCB:** 1.6 mm board. Sockets and all SMD parts on the bottom side, so JLCPCB assembles one side. Socket
   barrel holes 3.05 mm at (0, +6.00) and (-5.00, +3.80) in the key frame. 20 diodes on the bottom, behind each
   centre post (6.4 item 5). Socket zone x -10.1 to +5.1, y +1.0 to +8.7 mm. The sockets are hand-soldered
   after assembly, so their pads must stay reachable (6.4 item 4). Nine GPIO for the matrix, preferably
   low-drive, low-frequency pins.
2. **Radio module:** the matrix needs 9 GPIO and a GPIO supply of at least 2.7 V. The direct-GPIO option would
   need 20 and is not used.
3. **Case, CNC:** key-well floor = 1.15 +/-0.05 mm lip, plate top 4.00 mm below the deck. Openings
   14.00 +0.05/-0 with dog-bones. Lip and openings are FIT-CRITICAL and stated after anodising. PCB top 2.20 mm
   below the plate top, +/-0.1. Clear depth 2.15 mm below the PCB bottom over each socket zone
   (y +1.0 to +8.7 mm). Support under the sockets during switch insertion. Nothing taller than 0.25 mm on the
   plate top inside a cap footprint, so screw heads in the key field sit flush or below. Run a PG1353D
   retention check on the first shell; the PG1353 fallback needs no shell change.
4. **Case, FDM:** same footprint and stack, lip 1.0 or 1.2 mm in whole layers, chosen on the fit coupon. The
   print is plastic, so the PG1353D plate note does not apply.
5. **Battery:** the cell can only sit outside the socket zones or below them with 2.15 mm clear depth plus its
   insulator; at the 13 mm front edge only about 1.5 mm remains (section 6.3).
6. **Firmware:** `zmk,kscan-gpio-matrix`, `col2row`, `wakeup-source`; columns in the soft-off `extra-gpios`.
7. **Encoders and buttons:** their push contacts are matrix positions on column C4, each with its own diode.

## 9. Risks

1. **Socket supply.** JLCPCB marks `C5333465` as no longer manufactured and LCSC has none. Shops still sell
   Kailh Choc sockets today, but a later batch may find none. Mitigation: buy 100 now; the Kailh datasheet PDF
   was regenerated in August 2025, so Kailh still documents the part (likely).
2. **Full-POM switches in aluminium.** Kailh's PG1353D drawings say the part "only fits plastic plates", and no
   reason is given. The GLYF ignores the note. Mitigation: retention check in the first CNC shell; standard
   PG1353 fallback on the same footprint.
3. **Printed cap fit and durability.** Resin tolerance is +/-0.2 mm against a 1.30 mm cross arm, and the post
   wall at the slot ends is only 0.55 mm, under JLC3DP's 0.8 mm recommendation; the bore geometry allows no
   more than 0.72 mm. Mitigation: JLC Black Resin (heat deflection 54 to 65 degC), a stem-fit coupon order
   before the 96-cap order, THT fallback.
4. **Cap post and roof against the Choc V2 stem.** The Ø5.50 bore is the only reading consistent with the
   Ø6.50 stem column, but the leader on the drawing is hard to resolve; the collar diameters and flange
   thickness are scaled, not printed. Mitigation: measure one switch and print the coupon before the cap
   order.
5. **Pressed clearance.** With the PG1353 fallback only 0.55 mm (worst case) remains between the pressed cap
   skirt and the plate, and the skirt passes the flange top. Screw heads and any raised feature in the key
   field must stay at or below 0.25 mm.
6. **Socket retention force on the PCB.** Up to 3.0 kgf per insertion; unsupported boards can lose pads.
7. **Matrix logic levels.** If the module runs its GPIO at 1.8 V, silicon diodes make the matrix unreadable.
8. **Socket life.** 100 mating cycles (Kailh, confirmed). Fine for occasional swaps, not for a switch tester.
9. **KS-33 stem height** in the runner-up stack is derived from a reseller's 12.2 mm overall height and a
   scaled drawing, not from a printed dimension.
10. **Anodising on fit-critical features.** The film thickens the lip and narrows the openings. Mitigation:
    lip and openings are dimensioned after finish on the CNC drawing, and the lip is centred 0.10 mm under the
    minimum hook gap. The growth figure is general practice, not a supplier value.
11. **Fallback retention.** In the 1.15 mm lip the PG1353 hooks have 0.45 to 0.55 mm of slack. The switch
    cannot move in use, but it lifts about 0.5 mm under a keycap pull until the hooks catch.

## 10. Sources

Primary documents read in this run:

- Gateron KS-33 Low Profile 2.0 Red drawing `KS-33H10B050NN-Y24`, 2023-01-03:
  https://gateron.com/u_file/2311/10/file/GATERONKS-33LowProfile20RedSwitchBlackBottomHousing-KS-33H10B050NN-Y24.pdf
  (`gateron-02/`, rendered in `gateron-03/ks33hi-6.png`). Read: flange 15.00, bottom housing 14.00 +/-0.05,
  hook extent 14.70, plate 1.20 +/-0.05, housing top 3.35 above plate, housing bottom 2.50 below plate, centre
  post 5.75 below plate, pins 2.60 below PCB top, travel 3.0 +/-0.2, pre-travel 1.7 +/-0.4, PCB layout with
  5.25 mm centre and 3.00 mm socket holes.
- Gateron "Low profile hot swap 2.0" `KS-2P02B01-02` drawing, 2023-12-07:
  https://www.gateron.com/u_file/2601/16/file/GATERONUpgradeLowProfileswitchHot-swapPCB20SocketKS-2P02B01-02.pdf
  (`gateron-03/lpsock8-8.png`). Read: 1.87 +/-0.05 below PCB, 3.00 with barrels, 15.1 x 5.40 body, 5.1 mm centre
  hole, 50,000 cycles, push force 3.0 kgf maximum.
- Gateron `KS-2P02B01-01-a` drawing (MX pattern, not used):
  https://gateron.com/u_file/2311/22/file/GATERONUpgradeHot-swapPCB20Socket-KS-2P02B01-01-a.pdf
- Gateron product specification index: https://www.gateron.com/pages/product-specification (`gateron-01/`).
- Semtech 1N4148W datasheet (via LCSC):
  https://datasheet.lcsc.com/datasheet/pdf/8abd7fc00ebe41ffb03ad1383c10753b.pdf?productCode=C81598 (`ds-01/`).
- Cherry MX2A Red datasheet, total height 18.5 mm:
  https://cdn.sparkfun.com/assets/a/9/b/6/2/MX2A_RED-Datasheet-EN_US.pdf (`cherry-01/`).
- JLCPCB parts API `selectSmtComponentList/v2`, keywords CPG135001S30, C5333465, Choc, choc socket,
  low profile hot swap, hot swap socket, CPG151101S11, KS-2P02B01, Gateron socket, PG1353, Kailh (4 pages),
  KS-33, 1N4148W, 1N4148WS, C81598 (`jlc-01/`).
- LCSC product detail API for C5333465, C81598, C2128, C41430893:
  https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=... (`lcsc-01/`).
- Shop catalogues (Shopify `products.json` and product `.js`): https://keeb.io, https://splitkb.com,
  https://www.kailh.net, https://lofree.co, https://mechanicalkeyboards.com (`shops-01/`, `caps-01/`).
- ZMK documentation: https://zmk.dev/docs/config/kscan, https://zmk.dev/docs/config/power.
- Keycap compatibility: https://blog.keeb.io/low-profile-keycap-options-what-works-with-what/ ;
  THT size and shape: https://kbd.news/THT-Tai-Hao-low-profile-keycaps-2276.html (`caps-01/`).
- Footprint licences: GitHub API for kiswitch/kiswitch (licence file `LICENSE-CC-BY-SA`) and
  ceoloide/ergogen-footprints (MIT) (`gh-01/`).
- KiCad 10 stock libraries: `docker run --rm kicad/kicad:10.0.7` listing of `/usr/share/kicad`.

Read again on 2026-11-13 for the revision:

- Kailh `CPG1353D01D01-16`, sheets 1 and 2 (side view, top view, PCB pattern with connector), Kailh
  `CPG135001S30` rev C and Kailh `CPG135301D02` rev A, as rendered by the reviewer in
  `research/_cache/keys-sceptic/render-01/` (`c-side.png`, `c-top.png`, `c-pat.png`, `cp-side.png`,
  `vd02.png`, `cs-top.png`, `hi-socket-01.png`). `CPG135301D02` source:
  https://datasheet.lcsc.com/datasheet/pdf/cc1444bf26188c5fc5f70ef78aa546b8.pdf. My own pixel scans of these
  renders gave: flange 15.00 mm = 608.5 px on `c-top.png` (40.6 px/mm); rings around the cross at Ø5.8, Ø6.6,
  Ø7.7 and Ø8.4 by line centre; socket body edge 2.30 to 2.33 mm outside the barrel centre.
- kiswitch `SW_Hotswap_Kailh_Choc_V2` and ceoloide `switch_choc_v1_v2` footprints
  (`research/_cache/follow-switch-family-and-socket/footprints-01/`): kiswitch holes 3.05 at (0, -5.9) and
  (5, -3.8), pads at (-3.5, -6) and (8.5, -3.8), B.CrtYd y -8.452 to -1.248; ceoloide holes 3.0 at y -5.95.
- JLCPCB parts API for `C45350823` and `C5333465`, LCSC product detail API for the same codes, and
  https://lofree.co/products.json (`rev-01/`). Read: `C45350823` CPG135301D01 stock 0, purchasable flag 1, LCSC
  result null; `C5333465` stock 0, not purchasable, "This product is no longer manufactured", LCSC stock 0
  `sold_out`; Lofree Ghost and Phantom 106 pieces, 59.00, available.
- https://jlc3dp.com/help/article/jlc-black-resin (WebFetch): heat deflection 54 to 65 degC, +/-0.2 mm,
  recommended wall above 0.8 mm, from 1.0 USD.

From earlier research notes (their sources and confidences apply):

- `research/raw/follow-switch-family-and-socket.md`: Kailh PG1353D and PG1353 drawings, CPG135001S30 drawing
  (https://www.kailhswitch.com/uploads/15927/files/CPG1353D01D01-16-data-sheet.pdf,
  https://www.kailhswitch.com/Content/upload/pdf/202015927/PG135301D03.pdf,
  https://www.kailhswitch.com/uploads/15927/files/CPG135001S30.pdf), footprint cross-checks, GLYF board
  measurements, plate-material note.
- `research/raw/geometry.md`: GLYF dimensions and the derived internal stack.
- `research/raw/regulatory-software.md`: GLYF 5 x 4 `col2row` matrix decode.
- `research/raw/follow-radio-module-choice.md`: GPIO budget and E73 pin table.
- `research/raw/conventions.md`: family plate, cut-out, CNC and print conventions; macropad MX stack.
- Sibling source read directly: `/home/worxbend/Projects/macropad/board.toml` `[stack]`,
  `/home/worxbend/Projects/macropad/cad/macropad_case/components.py` (MX housing top 6.6, stem top 10.2 above
  the plate).

Search summaries used only for rejection reasons (likely at best): Cherry MX Low Profile height and mount
(cherry.de, deskthority), Kailh PG1425 (deskthority, Tom's Hardware), Gateron KS-33 12.2 mm overall height
(gateron.uk, ozokeyboards), JLC3DP resin data (jlc3dp.com help pages), NuPhy nSA height (pulse.bot).

## 11. Not checked, not found

1. The exact switch model in shipped GLYF units: not found (family only).
2. Kailh's reason for the "plastic plates only" note: not found.
3. A Kailh or Gateron recommended plate opening: not printed on any drawing; values are derived.
4. Tai-Hao THT cap height and skirt depth: not found. FKcaps LPF dimensions: not found.
5. PCBWay sourcing of CPG135001S30 and JLCPCB's consignment fee for it: not checked.
6. Choc V1 and Cherry MX Low Profile stack heights: not checked (both rejected for other reasons).
7. Mill-Max receptacle fit with Choc V2 pins: not checked.
8. The ozokeyboards KS-33 page and the mechanicalkeyboards product page: HTTP 429 to the fetch tool; Shopify
   JSON endpoints were used for the latter.
9. nRF52840 pull resistance and input threshold were not re-read from the Nordic specification in this run.
10. JLC3DP resin prices are "from" prices from help pages; no quote was made.
11. keeb.io Black Cloud stock was not re-read after the morning catalogue read: the reviewer's request hit a
    Cloudflare challenge, and it was not retried.
12. Kailh White Rain stock at any shop today: not checked.
13. PG1353D collar diameters and the Kailh flange thickness: scaled from the drawings, not printed.
14. JLCPCB drill tolerance for 3.05 mm NPTH holes: not checked.
15. The bore depth of the Choc V2 stem and the height of the cross inside it: not printed; the coupon must
    show whether the cap seats on the roof ring or on the post end.

## 12. Review of 2026-11-13 and response

A reviewer re-checked this record on the same day (cache `research/_cache/keys-sceptic/`). The switch family,
the default PG1353D, the CPG135001S30 socket and the 5 x 4 `col2row` matrix with 1N4148W diodes were upheld.
Each issue was checked again for this revision:

| # | Issue | Verdict | Change |
| --- | --- | --- | --- |
| 1 | Socket zone too short at the front (+7.9 mm) | Correct. The socket body reaches +8.2 to +8.5 mm; the kiswitch courtyard maps to +1.25 to +8.45 mm | Zone y +1.0 to +8.7 mm (0.1 mm more than the reviewer's +8.6 because the barrel hole moved to +6.00); rib and diode rules restated (6.4) |
| 2 | Fallback PG1353 numbers not carried into the stack | Correct: travel 3.2 +/-0.25 mm, hook catch 1.65 mm below the flange (1.62 mm when scaled). One refinement: the plate top, not the PCB seat, sets the switch height; the PCB seat tolerance decides which face carries the load | Fallback stack table, 0.25 mm plate-top rule, retention note (6.3); roof relief and 16.0 mm skirt opening added (6.5) |
| 3 | Socket hole position mixed 5.90 mm with 3.00 mm holes | Correct | Holes 3.05 mm at Kailh's barrel position (0, +6.00) (6.1) |
| 4 | Cap post diameter misread | Correct for Ø6.50 (stem column) and 5.70 (a height). For Ø5.50 my scan puts the leader end near the second ring, so the drawing alone is ambiguous; it is the only reading consistent with the Ø6.50 stem column, so it is kept as the bore (likely) | Post 5.20 mm nominal, coupon 5.00 / 5.20 / 5.40; slot wall 0.55 mm recorded as a risk; JLC Black Resin chosen (6.5, 4.5) |
| 5 | Lip and opening tolerances silent on anodising | Correct in principle; the growth figure is general practice | Lip 1.15 +/-0.05 and opening 14.00 +0.05/-0, both after finish (4.4, 6.2) |
| 6 | Example switch was the tactile Black Cloud | Correct. The PG1353D drawing on file is the linear type, and the units show a white full-POM switch | Lofree Ghost (linear) named as the parity buy, live stock read today (5, 6.7) |
| 7 | Diode gap stated as 4.5 mm | Correct: 3.85 mm between zones, about 2.5 mm after soldering access | Diodes moved behind the centre post (6.4 item 5) |
| 8 | `C45350823` listed as an LCSC code | Correct: the LCSC detail API returns null today | Marked as a JLCPCB library code (6.7) |

Found during the revision and not raised by the reviewer: at full travel the stem top comes within 0.10 mm of
the PG1353D collar rim and the PG1353 housing top, so a flat cap roof would bottom on the switch at
worst-case travel. The 0.50 mm roof relief in section 6.5 fixes this.
