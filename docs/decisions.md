# Design decisions

Date: 2026-11-13. Revision A. Nothing here has been built, measured or tested on hardware. Each entry settles one
conflict or disagreement listed in [research/COMPONENTS.md](../research/COMPONENTS.md) sections 6 to 8, or one
gap found while writing [board.toml](../board.toml). Numbers trace to the decision records in
[research/components/](../research/components/); "power 5.2" means section 5.2 of
[power.md](../research/components/power.md), and so on.

Order of priority used for every choice:

1. A working radio and a safe battery.
2. Manufacturability and cost at JLCPCB (PCBA) and JLCCNC (case).
3. Closeness to the GLYF look.

`tools/check_spec.py` checks the arithmetic of every decision that has a number in `board.toml`.

## Index

| Entry | Settles | Owner |
| --- | --- | --- |
| [D1](#d1-body-width-1284-mm) | Section 7 item 7 (width), section 6 item 3 | mcu-radio, enclosure |
| [D2](#d2-flank-scoops-end-by-y-35-and-the-rf-slot-is-30-mm) | Section 7 item 7 (scoops), section 6 item 7 | enclosure, mcu-radio |
| [D3](#d3-one-knob-plinth) | Section 7 item 7 (plinth) | rotary-buttons, enclosure |
| [D4](#d4-battery-cell-pocket-and-wedge-depth) | Section 7 item 1, section 6 item 4 | power, enclosure |
| [D5](#d5-battery-connector-position) | Section 7 item 5 | power, PCB |
| [D6](#d6-two-ground-screws-with-the-enclosure-numbers) | Section 7 item 3, section 6 item 5 | usb-io, enclosure |
| [D7](#d7-ground-screw-g2-moves-to-y-658) | Section 7 item 2 | enclosure, rotary-buttons |
| [D8](#d8-icon-flash-in-the-control-column) | Section 7 item 4 | PCB, mcu-radio, enclosure |
| [D9](#d9-double-sided-pcba) | Section 7 item 6, section 6 item 6 | display, rotary-buttons, PCB |
| [D10](#d10-display-web-080-mm) | Section 7 item 8, section 6 item 9 | display, enclosure |
| [D11](#d11-top-shell-over-the-rf-slot) | Section 7 item 9, section 6 item 8 | mcu-radio, enclosure |
| [D12](#d12-vbus-on-module-pad-66-while-the-rail-is-off) | Section 7 item 10 | power, mcu-radio |
| [D13](#d13-33-v-regulator-accuracy) | Section 7 item 11, section 6 item 10 | power, display |
| [D14](#d14-capacitance-on-the-33-v-rail) | Section 7 item 12 | power, PCB |
| [D15](#d15-i2c-pull-ups) | Section 7 item 13 | power |
| [D16](#d16-radio-module-bmd-340) | Section 6 item 1 | mcu-radio |
| [D17](#d17-backlight-current-figures) | Section 6 item 2 | power, display |
| [D18](#d18-rear-openings-wholly-in-the-bottom-shell) | Section 6 item 11 | usb-io, enclosure |
| [D19](#d19-clock-widget-from-host-time-no-hardware-rtc) | Section 8 item 18 | firmware, mcu-radio |
| [D20](#d20-encoder-names-and-pins) | Gap in the records | rotary-buttons, mcu-radio |
| [D21](#d21-pcb-left-edge-030-mm-from-the-wall) | Gap found by `tools/check_spec.py` | PCB, enclosure |
| [D22](#d22-antenna-keep-out-to-the-first-pad-column) | Gap found by `tools/check_spec.py`; review finding | mcu-radio, PCB |
| [D23](#d23-assembly-panel-routed-frame-with-mouse-bite-tabs) | Review: no panel rails | PCB, mcu-radio, usb-io |
| [D24](#d24-antenna-inset-against-the-outline-tolerance) | Review: inset below the fab tolerance | mcu-radio, PCB |
| [D25](#d25-knob-plinth-is-a-rounded-rectangle) | Review: plinth pockets break through the deck | rotary-buttons, enclosure |
| [D26](#d26-switches-go-in-on-an-insertion-jig) | Review: socket insertion load over the cell | keys, power, enclosure |
| [D27](#d27-fdm-bottom-shell-printed-on-the-ramp-plane) | Review: FDM bottom-shell plan broken by D4 | enclosure |
| [D28](#d28-build-order-cell-orientation-and-lead) | Review: assembly order and cell lead undefined | power, enclosure |
| [D29](#d29-corner-radii-for-jlccnc) | Review: pocket corner radii | enclosure |
| [D30](#d30-k-screws-m16) | Review: K countersink web under the JLCCNC minimum | enclosure, keys |
| [D31](#d31-rear-feet-and-the-c2-spot-face) | Review: rear feet cross the apex; C2 spot-face undefined | enclosure |
| [D32](#d32-ground-screw-g2-at-12125-666) | Review: top-shell void checks omitted the RF pocket | enclosure, usb-io |
| [D33](#d33-display-pocket-corners-and-right-edge) | Review: display pocket corners undefined | display, enclosure |
| [D34](#d34-bottom-wall-step-under-the-plate-lip) | Review: bottom wall step not in the spec | enclosure |
| [D35](#d35-bottom-face-positions-of-the-power-parts) | Review: power placement rules unchecked | power, usb-io, PCB |
| [D36](#d36-encoder-rc-filter-footprints) | Review: encoder RC footprints missing | rotary-buttons, PCB |
| [D37](#d37-usb-c-recess-kept-at-025-mm-pending-a-plug-test) | Review: USB recess against the overmold gap (rejected for now) | usb-io, enclosure |
| [D38](#d38-backlight-driven-by-display_powerc-not-zmkdisplay-led) | Gap: stock ZMK drives the backlight at 100 % | firmware, display, power |
| [D39](#d39-cell-bonded-to-the-pocket-floor-top-assembly-lowered-onto-the-bottom-shell) | Review: insert and cell loose in the D28 order | power, enclosure |
| [D40](#d40-third-setup-for-the-bottom-shell-foot-pockets) | Review: setup count against the foot pockets | enclosure |

## D1. Body width 128.4 mm

- **Context.** The module's PCB trace antenna needs a bay with no metal within 5 mm of the 4.4 mm antenna strip
  (mcu-radio 7.3.1, A4 to A6). In the GLYF plan no edge position meets this; the display edge or an encoder sits
  over the strip (mcu-radio 7.3.2). mcu-radio sized an 8.0 mm widening for a 1.4 inch panel and noted that 7.0 mm
  would do for the chosen 1.3 inch panel (mcu-radio 7.3.3 item 2).
- **Options.** (a) GLYF width 120.4 mm with the antenna under the lens margin, allowed only after an RF comparison
  test (mcu-radio 7.3.4 item 1). (b) 127.4 mm (7.0 mm wider). (c) 128.4 mm (8.0 mm wider).
- **Decision.** (c) 128.4 x 85.2 mm. The key field, knobs, lens and buttons keep their GLYF positions relative to
  the left face; the right margin grows from 4.0 to 12.0 mm.
- **Reason.** Radio first. Option (a) breaks the data sheet's "metal clear above" rule. Option (b) is not proven:
  the rule is LCD edge 9.4 mm or more from the board edge. With 7.0 mm the 26.16 mm module edge sits 2.52 mm inside
  the lens edge, at 4.0 + 7.0 + 2.52 = 13.52 mm from the right face against the 13.35 mm bay line: 0.17 mm, or
  0.07 mm after the module's +/-0.2 mm outline tolerance. The display pocket edge, 0.32 mm outside the module,
  would sit 0.15 mm inside the bay. 8.0 mm gives 1.17 mm and keeps a later 1.4 inch panel possible.
- **Consequences.** Body and lid 8 mm wider than the GLYF; PCB 120.65 mm wide (D21). `tools/check_spec.py` checks
  the LCD-to-edge rule (10.57 mm against 9.4). The width is `body.width` in `board.toml`; a smaller value must
  pass that check and the RF acceptance test in mcu-radio 7.3.4.

## D2. Flank scoops end by Y 35 and the RF slot is 30 mm

- **Context.** mcu-radio prefers a 40 mm wall slot (Y 33 to 73) and accepts 30 mm. The GLYF flank scoops keep the
  underside at Z -12.0 back to about Y 43, which leaves no wall under a slot bottom at Z -11.70 (enclosure 7.3).
- **Options.** (a) 40 mm slot, scoops end by Y 30. (b) 30 mm slot (Y 38 to 68), scoops end by Y 35. (c) GLYF
  scoops and a slot that wraps under the wall.
- **Decision.** (b). Both scoops (left too, for symmetry) reach full ramp depth by Y 35.
- **Reason.** 30 mm meets mcu-radio's minimum (A9) with plain 3-axis machining; (c) needs an undercut. (a) shortens
  the scoops by another 5 mm for a gain that is not measured.
- **Consequences.** Scoops about 8 mm shorter than the GLYF's (look change, accepted). With the D4 wedge the wall
  under the slot is 4.37 mm (`tools/check_spec.py`). If the RF acceptance test falls short, D11 gives the next step.

## D3. One knob plinth

- **Context.** The PEC12R body stands 6.10 mm above the PCB, 0.10 mm under the deck (0.20 mm above at tolerance),
  so a pocket from below cannot leave a roof (rotary-buttons 6.3). Two round bosses big enough for the pockets would
  overlap.
- **Options.** (a) One rounded plinth 36.1 x 17.4 x 1.8 mm over both encoders. (b) Alps EC11E with a cut shaft and
  GLYF bosses (look-only fallback, rotary-buttons 6.4 item 2).
- **Decision.** (a).
- **Reason.** (b) needs a cut, glued shaft and adds up to 508 uA per encoder in deep sleep, because half its detents
  rest with both contacts closed. That costs battery life for looks.
- **Consequences.** Visible change from the GLYF's two bosses. Knob top at +12.0 (GLYF 11.8). The plinth outline
  is a rounded rectangle, not the stadium of rotary-buttons 6.3 (D25). `tools/check_spec.py` checks the encoder in
  its pocket: 0.15 mm per side at the worst case across the mounting tabs (14.0 +/-0.5, rotary-buttons 6.3 item
  5), 0.70 mm at the nominal 13.4 mm body, and 0.05 mm under the ceiling at the body's maximum height. Revision A
  first stated 0.70 mm as the margin; that figure ignored the tabs.

## D4. Battery cell, pocket and wedge depth

- **Context.** power 5.2 asks for a 45.0 x 66.0 mm pocket with its floor top at Z -15.95 (5.0 mm cell) or -15.18
  (4.3 mm cell) and a 1.5 mm floor. On the GLYF wedge the body is thick enough only over 23.6 or 33.9 mm of Y
  (enclosure 6.6). The K1 and K2 posts at Y 11.0 need a 6.6 mm keep-out, so the pocket cannot start before
  Y 14.3. The left flank scoop (Z -12.0, 13 mm wide) bounds the pocket on the left.
- **Options.** (a) A cell 31 mm or less in Y (lower capacity, no part in the records). (b) A deeper body at the
  pocket front. (c) A 1.0 mm pocket floor. Cell choice: EEMB LP404261 (4.3 x 42.5 x 63, 1,000 mAh,
  quotation only) or Adafruit 258 (5.0 x 34 x 62, 1,200 mAh, in stock).
- **Decision.** Adafruit 258 class cell (1,200 mAh, PCM, JST PH, pin 1 positive) for batch 1, in a
  64 x 36 mm pocket at X 14.5 to 78.5, Y 14.5 to 50.5, floor top Z -15.95. The underside moves down: front
  thickness 14.6 mm (GLYF 13.0), apex 20.6 mm at Y 15.0 (GLYF 19.2 at Y 12.7), rear wall 12.0 mm unchanged. The
  ramp stays at 4.89 degrees (GLYF 4.95).
- **Reason.** Safe battery first: (c) puts a thin, bead-blasted 1.0 mm floor under the pouch. (a) has no sourced
  part. Both cells need the same body change (about 1.5 mm at the pocket front edge with the K post limit),
  so the in-stock cell with more capacity wins and one pocket depth serves it. The EEMB cell is quotation-only
  (power 16 risk 2).
- **Consequences.** The "19 mm thin" look becomes 20.6 mm at the apex and 14.6 mm at the front edge. The pocket
  floor is 1.62 mm at its thinnest (Y 50.5); `tools/check_spec.py` checks it. C2 sits on a deeper underside
  (about Z -15.3 against -13.7 in enclosure 6.4): a spot-face from below keeps the enclosure's 2.0 mm local floor
  and screw length (D31). The rear feet move off the apex (D31). The FDM bottom shell can no longer be a flat tray
  (D27). Eight sockets sit over the cell, so switch insertion needs the jig of D26. The EEMB 42.5 mm cell no
  longer fits; using it needs a new bottom shell. Runtime figures in power 4.3 used 850 mAh usable and remain
  conservative.

## D5. Battery connector position

- **Context.** The JST PH side-entry header is 5.5 mm tall below the PCB, needs a floor top at Z -13.60 or lower
  and 12 mm free in front of its mouth, under the control column, left of the RF bay, outside the flank scoops
  (power 11; COMPONENTS 7 item 5).
- **Options.** Behind the pocket under key column 3 (no room: sockets), or in the control column beside the pocket.
- **Decision.** Connector at X 93.5, Y 37.5, mouth facing the pocket (-X). A floor relief X 78.5 to 97.0,
  Y 31.5 to 43.5 at Z -13.60 joins the pocket and holds the plug and the wire bend. Placement is a guess within
  these rules; the PCB layout may move it inside the relief.
- **Reason.** The relief sits on the thick part of the wedge (18.16 mm at Y 43.5 against 15.10 needed), clear of
  both flank scoops and 18.6 mm from the RF bay.
- **Consequences.** The connector is reachable with the bottom shell off (power 14 rule 5). The charger stays at
  least 10 mm from the pocket in plan (power 6.4); `board.toml` holds its position and `tools/check_spec.py`
  checks the distance (D35).

## D6. Two ground screws with the enclosure numbers

- **Context.** usb-io rev 2 specifies one ground screw G1 into a 4.5 mm boss ending at Z -6.15 with 3.0 mm of
  thread. enclosure rev 2 specifies G1 and G2 on 4.6 mm posts ending at Z -6.20 with 2.7 mm of thread.
- **Options.** One screw (usb-io), two screws (enclosure).
- **Decision.** Two M2 x 4 ISO 7045 pan-head screws, G1 and G2, on 4.6 mm top-shell posts ending at the PCB top
  (Z -6.20), bare post faces, plated 2.2 mm holes with 4.6 mm GND rings, thread 2.7 mm.
- **Reason.** The posts also set the PCB height at both ends of the control column (keys 6.2: PCB top 2.20 +/-0.1
  below the plate top). Two contacts bond the top shell even if one face is not cleared well. The enclosure's
  arithmetic on drill depth and metal beyond the point (2.02 mm to the deck) is the later and more complete one.
- **Consequences.** One more screw and plated hole than usb-io rev 2. The usb-io "within 20 mm of the receptacle"
  wish for G1 is not met (G1 is about 35 mm away); the shell bonding does not depend on it.

## D7. Ground screw G2 moves to Y 65.8

Superseded by D32, which moves G2 again to (121.25, 66.6). The entry stays as the record of the first move.

- **Context.** G2 at (x_right 7.5, Y 70.0) and the 17.0 mm counterbore of the right button at (x_right 18.27,
  Y 71.20) leave 0.04 mm of wall in plan against the enclosure's 1.2 mm rule.
- **Options.** (a) Shrink the counterbore: it must clear the 15.0 mm cap flange, so at most about 0.45 mm can go;
  the wall stays under 1.2 mm. (b) Move G2 toward the wall: its GND ring then comes within 0.3 mm of the board
  edge. (c) Move G2 along Y toward the RF bay.
- **Decision.** (c): G2 at x_right 7.5, Y 65.8 (X 120.9 in `board.toml`).
- **Reason.** It gives a 1.25 mm wall to the counterbore and keeps the post 0.4 mm and the top-face keep-out
  0.1 mm outside the RF bay (bay ends at Y 63.1). Nothing else moves.
- **Consequences.** G2 now sits beside the RF wall slot (Y 38 to 68) but inside the top shell, 1.7 mm from the
  inner wall face, clear of the insert. Both margins are small; `tools/check_spec.py` checks them.

## D8. Icon flash in the control column

- **Context.** The SOIC-8 W25Q128JVSIQ reaches Z -9.96; under the key field the floor top is Z -9.95, and
  mcu-radio asks for 2.5 mm under the module and flash (floor top Z -10.30 or lower).
- **Options.** (a) Keep SOIC-8 and place it outside the key-field floor. (b) WSON-8 W25Q128JVPIQ (C190862,
  extended, height not read).
- **Decision.** (a): SOIC-8 on the bottom face at X 103.0, Y 53.0, left of the module, with the control-column floor
  top at Z -10.30.
- **Reason.** The SOIC part is a basic part (no loading fee) with a known height; the WSON is extended and its
  height was not read. The control column has the depth (17.35 mm body at Y 53).
- **Consequences.** QSPI traces stay short (the module's QSPI pads face that side). The position is a guess within
  the rule; the PCB layout may move it inside the control column.

## D9. Double-sided PCBA

- **Context.** keys, mcu-radio and usb-io assume one assembled face (bottom). rotary-buttons puts the B3FS switches
  on the top face; display puts the FH34SRJ connector on the top face.
- **Options.** (a) Double-sided Standard PCBA. (b) Move the top parts to the bottom. (c) Machine-place the bottom
  only and hand-solder the top SMD parts.
- **Decision.** (a): JLCPCB assembles both faces.
- **Reason.** Moving the parts costs function. The B3FS buttons must face up under their caps; on the bottom they
  could not be pressed through the stack in rotary-buttons 6.3. The panel's flex is drawn to fold 180 degrees back
  under the module onto a top-face connector (display 6.1); a bottom connector needs a PCB slot and a second fold
  of a 14.93 mm tail that the drawing does not allow for. (c) means hand-soldering a 24-pin 0.5 mm FPC connector
  on five boards, which loses on manufacturability.
- **Consequences.** About USD 51 setup and USD 16 stencil instead of the single-sided figures (COMPONENTS 2; price
  page, likely). The top face carries the FH34SRJ, two B3FS and the THT encoders; everything else stays on the
  bottom.

## D10. Display web 0.80 mm

- **Context.** display specifies a 0.60 mm aluminium web between the lens recess and the module pocket. enclosure
  asks for 0.80 mm, JLCCNC's recommended metal wall.
- **Options.** 0.60 mm web; 0.80 mm web with the module 0.20 mm lower.
- **Decision.** 0.80 mm. Web underside Z -1.95, module top Z -2.05, module back Z -3.55.
- **Reason.** Manufacturability: 0.60 mm is under JLCCNC's 0.8 mm recommendation and bead blasting makes thin webs
  worse (enclosure 5). The web is hidden under the painted lens, so the look does not change.
- **Consequences.** Air gap lens to panel grows from 0.85 to 1.05 mm (slightly more parallax). The foam pad between
  module back and PCB compresses to 2.65 mm instead of 2.85 mm. The module stays 1.65 mm above the connector top.
  FDM keeps its 0.8 mm web.

## D11. Top shell over the RF slot

- **Context.** enclosure reads mcu-radio as "the outer wall above the slot (Z 0 to -5.0) stays metal"; mcu-radio
  A7 asks only that the top shell over the bay be 2.80 mm or thinner. No confirmation from mcu-radio exists.
- **Options.** (a) Metal outer wall above the slot, top shell over the bay pocketed from below to Z -2.80.
  (b) Also notch the top-shell outer wall over the bay to Z -2.80 with a stepped insert.
- **Decision.** (a) for batch 1. Both rules hold together: the slot is in the bottom shell from the split face
  (Z -5.0) to Z -11.70, and inside the bay's plan the top shell ends at Z -2.80.
- **Reason.** (a) meets every written rule (A5, A7, A9) and keeps the outer face unbroken. (b) is the documented
  next step if the RF acceptance test fails (enclosure 7.2 item 5); it needs no PCB change.
- **Consequences.** The RF acceptance test of mcu-radio 7.3.4 decides on the first aluminium unit. A foil-lined FDM
  pre-test comes first; the FDM case alone predicts nothing about the radio.

## D12. VBUS on module pad 66 while the rail is off

- **Context.** With the slide switch off and USB plugged in, VBUS reaches module pad 66 while VDD is 0 V. Nobody
  checked the nRF52840 specification for this case (power 16 risk 5).
- **Options.** (a) Direct connection, as the records draw it. (b) A load switch from VBUS to pad 66 enabled by 3V3
  (no part chosen or sourced).
- **Decision.** (a), with a gate: before the schematic is frozen, the nRF52840 Product Specification is read for
  VBUS present with VDD absent. If it forbids it, (b) is designed by the power owner with a sourced part.
- **Reason.** Smallest design that works if the case is allowed. Adding an unsourced part now would invent a BOM
  line. The gate keeps the risk visible instead of hiding it.
- **Consequences.** Open item in the README until the specification is read. No board is ordered before that.

## D13. 3.3 V regulator accuracy

- **Context.** The panel's recommended VDD is 2.4 to 3.3 V (ZJY133T-IF05 sheet, section 4.2), absolute maximum
  4.6 V (section 4.1). display asked for a +/-1 % regulator. power chose the TPS7A0233 without stating its accuracy.
- **Datasheet numbers.** TPS7A02 (TI SBVS277C, table 6.5): nominal accuracy +/-1 % at TJ 25 °C for 1 uA to 1 mA;
  +/-1.5 % over TJ -40 to +125 °C. At 3.3 V that is 3.250 to 3.350 V.
- **Options.** (a) Keep the TPS7A0233. (b) A +/-1 % 3.3 V part. (c) A lower output, for example the TPS7A0230 (3.0 V).
- **Decision.** (a). Keep the TPS7A0233PDBVR and accept a worst-case VDD 50 mV (1.5 %) above the recommended
  maximum and 1.25 V under the absolute maximum.
- **Reason.** (b) does not solve it: 3.3 V +/-1 % still reaches 3.333 V. (c) keeps VDD in range but breaks the
  backlight: two parallel LEDs at 2.8 to 3.0 V through 15 Ohm from 2.955 to 3.045 V give 0 to 16 mA instead of
  about 27 mA. The excursion is within the absolute rating, and the GLYF likely runs the same class of panel from
  a 3.3 V LDO (DOSSIER 4 item 12).
- **Consequences.** Backlight worst case (3.350 - 2.8) / 15 = 36.7 mA, inside the 40 mA LED rating. Peak 3V3 load
  51 + 36.7 = about 88 mA against 200 mA. Risk recorded in the README.

## D14. Capacitance on the 3.3 V rail

- **Context.** TPS7A02 is specified for 1 to 22 uF on its output (power 7.3). The 22 uF is the maximum *derated*
  capacitance (TI SBVS277C, table 6.3, note 2). The BMD-340 data sheet notes an internal 4.7 uF bulk capacitor on
  both supply pads, VCC (pad 17) and VCCH (pad 65); in LV mode both pads are tied, so the module may hold 9.4 uF.
  The records place: module internal 4.7 uF (counted once), module bulk 10 uF, LDO output 10 uF, flash 100 nF,
  panel 1 uF + 100 nF. Sum 25.9 uF, over the limit even when counting one internal capacitor.
- **Options.** (a) Drop the LDO's 10 uF and use 1 uF at the LDO output. (b) Drop the module bulk. (c) Both at
  4.7 uF (a new part number).
- **Decision.** (a): LDO output 1 uF 0603 (C15849, the part already on its input), module bulk 10 uF 0603 (C19702)
  at VCC/VCCH. Counting both internal capacitors, the nominal total is 21.6 uF.
- **Reason.** The module data sheet asks for extra bulk at its supply; the LDO needs at least 1 uF near its pin.
  No new part number. Counting 9.4 uF inside the module follows the data sheet text for both pads; nobody has
  confirmed with u-blox whether the two notes describe one capacitor or two, so the larger figure is used.
- **Consequences.** Nominal 21.6 uF against the 22 uF derated limit. Nominal values bound the derated ones from
  above: X5R and X7R parts lose capacitance under the 3.3 V bias, so the derated total is lower still. Revision A
  stated 16.9 uF and a 5.1 uF margin; that counted one internal capacitor (review finding). If a later change adds
  capacitance on 3V3, the module bulk drops to 4.7 uF first. `tools/check_spec.py` sums
  `power.rail_3v3_caps_uf` against `power.rail_3v3_cap_max_derated_uf`.

## D15. I2C pull-ups

- **Context.** The power parts list carries two 4.7 kOhm pull-ups and asks who places them.
- **Decision.** The power subsystem owns and places both, to 3V3, near the gauge. The MCU does not enable its
  internal pull-ups on these pins.
- **Reason.** The gauge is the only I2C device. With the rail off the pull-ups hold SDA and SCL low, which lets the
  MAX17048 enter its sleep mode, consistent with the off-state budget (power 4.2: gauge sleep 0.5 uA).
- **Consequences.** None for other subsystems.

## D16. Radio module BMD-340

- **Context.** `research/raw/follow-radio-module-choice.md` recommends the Ebyte E73; mcu-radio chose the
  u-blox BMD-340-A-R.
- **Decision.** BMD-340-A-R (C5456944).
- **Reason.** 48 GPIO against 2 to 4 spare on the E73, 1.9 mm against 3.0 mm height beside 1.85 mm sockets,
  a dimensioned keep-out drawing, 349 in stock against 61 (mcu-radio 6).
- **Consequences.** USD 2.12 more per unit; LGA pads cannot be reworked with an iron. 2022 date code on an MSL 3
  part: ask JLCPCB about dry-pack and baking.

## D17. Backlight current figures

- **Context.** power budgets 60 mA backlight (1.4 inch panel) and a 111 mA peak; display gives 26.7 mA nominal
  for the chosen 1.3 inch panel.
- **Decision.** Use the display figures with the D13 rail limit: 26.7 mA nominal, 36.7 mA worst case, 3V3 peak
  about 88 mA. power's runtime table stays as a conservative bound.
- **Reason.** The panel is chosen; its LED data is confirmed (display 6.1).
- **Consequences.** None for parts. Runtime claims, when written, use the display figures and say so.

## D18. Rear openings wholly in the bottom shell

- **Context.** The GLYF's rear apertures look centred on the split line (geometry 4.8). usb-io and enclosure put
  worxpad's in the bottom shell.
- **Decision.** Bottom shell only: two 10.0 mm notches from the split face, Z -5.00 to -9.90.
- **Reason.** The USB-C contact centre is at Z -7.82 and the switch actuator at Z -8.55, both 2.8 mm or more below
  the split; a split-line aperture would need a top-shell half with no part behind it. Notches from the split face
  need no undercut.
- **Consequences.** Recorded so that nobody re-imports the GLYF value.

## D19. Clock widget from host time, no hardware RTC

- **Context.** The GLYF carries a DS3231 RTC with a coin cell for its clock widget. No worxpad record selects an
  RTC (COMPONENTS 8 item 18).
- **Options.** (a) Host time sync over the Raw HID widget channel, kept by the nRF52840 RTC on the 32.768 kHz
  crystal. (b) A hardware RTC on I2C with a backup cell.
- **Decision.** (a). No RTC part, no coin cell.
- **Reason.** Smallest design that still gives a clock widget. The Raw HID channel already exists for widgets
  (mcu-radio 1 item 6) and the crystal is already on the board (+/-20 ppm, about 1.7 s per day). The GLYF's own
  time and media widgets need its host app too ("Time & Media widgets TBD", DOSSIER 1 item 15).
- **Consequences.** The clock is blank after power-off or deep sleep until a host sends the time; firmware shows no
  time rather than a wrong one. No pins, no parts, no coin-cell safety rules.

## D20. Encoder names and pins

- **Context.** Two records assign the A/B pins by side and agree: rotary-buttons 2 ("Left encoder P0.28 / P0.30,
  right encoder P0.29 / P0.31") and mcu-radio 7.2 ("Encoder L A / B P0.28 / P0.30"). rotary-buttons also calls the
  encoder nearer the right edge "encoder 1", and keys puts encoder 1's push at C4 R0. Revision A of this entry
  cited only mcu-radio, put P0.28/P0.30 on the right encoder and so overrode both records without saying so
  (review finding).
- **Decision.** Follow both records. Left encoder (x_right 36.96): A P0.28, B P0.30, push C4 R1. Right encoder
  (x_right 18.27): A P0.29, B P0.31, push C4 R0. Right button C4 R2, left button C4 R3. `board.toml` names
  everything by side.
- **Reason.** The pin assignment then matches every record a schematic or firmware builder will read. The matrix
  positions come from keys 6.6 and are unchanged. All four encoder pins are low-frequency pins, so either
  assignment works electrically.
- **Consequences.** Firmware and the pin check read the names from `board.toml`.

## D21. PCB left edge 0.30 mm from the wall

- **Context.** With the PCB 0.45 mm from every inner wall (enclosure 6.5) the column-0 socket pads sit 0.275 mm
  from the left board edge (key centre 14.0, pad edge 9.775 to the left). That is under a 0.3 mm copper-to-edge
  value (guess; not re-read from JLCPCB).
- **Options.** Move the key field (changes the GLYF plan and the well), or move the left PCB edge out.
- **Decision.** Left PCB edge at X 3.80, 0.30 mm from the inner wall, the family's `pcb_gap`
  (`research/raw/conventions.md` 3.6). The other three edges stay 0.45 mm from the wall. PCB 120.65 x 77.3 mm
  plus the two rear tongues.
- **Reason.** Smallest change; the antenna rule fixes only the right edge.
- **Consequences.** Pad to edge 0.425 mm. The cavity tolerance on the left drops to 0.30 mm; the FDM print keeps
  0.3 mm as in the family. `tools/check_spec.py` checks both values.

## D22. Antenna keep-out to the first pad column

- **Context.** mcu-radio A3 sets a copper keep-out 4.4 mm deep from the board edge, the length of the antenna strip.
  The BMD-340 data sheet (UBX-19033353 R13, figure 12) hatches the RF keep-out up to 4.40 mm from the antenna end
  of the module, which is exactly where the first column of 0.50 mm land pads starts. With the antenna end inside
  the board edge, a keep-out of 4.4 mm from the edge leaves copper under the antenna; a fixed deeper value cuts
  the pads. Revision A used a fixed 4.6 mm with a 0.1 mm inset, which reached 0.10 mm into four pads (review
  finding).
- **Options.** (a) A fixed depth. (b) Depth = antenna strip + antenna inset, so the keep-out always runs from the
  board edge to the pad column.
- **Decision.** (b). Keep-out depth 4.40 + 0.20 = 4.60 mm at the D24 inset, 20.2 mm long, all layers.
- **Reason.** It covers the whole antenna strip and touches no pad at any inset. The keep-out and the footprint
  are drawn in the same copper data, so their relation does not depend on the outline tolerance.
- **Consequences.** The keep-out runs X 119.85 to 124.45 and the pads start at X 119.85. `tools/check_spec.py`
  checks that the depth equals strip plus inset and that the keep-out does not reach past the pad column.

## D23. Assembly panel: routed frame with mouse-bite tabs

- **Context.** JLCPCB needs edge rails for assembly, at least 5 mm wide, and asks for 2.5 mm from a part body to
  the panel edge (mcu-radio 4). The module sits 0.2 mm inside the right edge and the USB-C shell overhangs its
  tongue by 0.70 mm; the slide-switch actuator overhangs its tongue by 1.60 mm. mcu-radio 8 asks for a V-cut on
  the right edge with any mouse-bite tab 10 mm or more from the antenna strip; usb-io 7 asks for mouse-bites or a
  routed gap at the rear, because the tongues break the straight edge. Revision A had no panel at all (review
  finding).
- **Options.** (a) V-cut on the right, routed rear. (b) One board in a frame of four 5 mm rails, routed all round
  with mouse-bite tabs.
- **Decision.** (b). Rails 5.0 mm, routed gap 2.5 mm on every edge, eight 5.0 mm tabs: right edge at Y 15 and 75,
  left at Y 27 and 65.5, rear at X 40 and 115, front at X 40 and 100. Perforations of 0.5 mm at 0.8 mm pitch with
  their centres 0.25 mm inside the outline, so the break nub stays inside the board and does not touch the 0.30
  to 0.45 mm wall gap. The R2.0 corners are routed with the board.
- **Reason.** A straight V-cut cannot follow the R2.0 corners and would square the right-hand corners, and its
  position tolerance at JLCPCB is not recorded. One routed process gives one outline tolerance (D24). A gap of
  2.5 mm leaves 0.9 mm free in front of the switch actuator; 2.0 mm would leave 0.4.
- **Consequences.** The nearest tab is 14.4 mm from the antenna strip and 2.85 mm from any socket pad or ground
  ring. No edge is V-cut, so the 0.4 mm copper-to-V-cut rule does not bind; the check still runs for any edge set
  to "vcut". Tab nubs are sanded flush before fitting. Frame panel price not checked. This overrides the V-cut of
  mcu-radio 8 (request to the mcu-radio owner).

## D24. Antenna inset against the outline tolerance

- **Context.** mcu-radio A1 allows the antenna end 0 to 0.2 mm inside the board edge, never overhanging. The
  routed outline at JLCPCB is about +/-0.2 mm (usb-io risk 1, not re-read). A 0.2 mm window cannot hold a
  +/-0.2 mm process: revision A's nominal 0.1 mm could land anywhere from 0.1 mm overhang to 0.3 mm inset (review
  finding). Re-reading the BMD-340 data sheet, section 6.1 gives no number: "The module should be placed at the
  edge of the PCB with the antenna edge facing out." The 0.2 mm limit in A1 is the record's own choice.
- **Options.** (a) Order a tighter outline tolerance (no such offer is recorded; would need confirmation on the
  quote). (b) Nominal inset 0.2 mm and a window of 0.0 to 0.4 mm. (c) Keep 0.1 mm and accept a possible overhang.
- **Decision.** (b), and ask JLCPCB on the quote for +/-0.1 mm on the right edge. If they grant it the nominal
  stays 0.2 mm and the real inset falls in 0.1 to 0.3 mm.
- **Reason.** Radio first. An overhang puts the module body over the routed gap and against the case wall gap;
  an extra 0.2 mm of bare FR4 past the antenna end is small next to the 4.4 mm of FR4 the strip already sits on.
  The RF acceptance test of mcu-radio 7.3.4 runs on boards whose inset is measured.
- **Consequences.** Keep-out depth 4.60 mm (D22). The RF bay grows to 9.6 mm from the board edge (antenna end 0.2
  + strip 4.4 + 5.0) so the 5.0 mm metal-free margin is kept from the strip, not from the edge; the LCD keeps
  10.57 mm and the display pocket edge moves (D33). The module length tolerance (+/-0.3 mm, data sheet figure 11)
  is not in this window; how the module body sits relative to its pads is an open question for mcu-radio.
  `tools/check_spec.py` checks inset +/- tolerance against the window. Request to mcu-radio: update A1.

## D25. Knob plinth is a rounded rectangle

- **Context.** rotary-buttons 6.3 draws the plinth as a stadium (36.1 x 17.4 mm, R8.7) with each end arc centred on
  an encoder axis. The 14.8 mm pockets have R1.5 corners and are cut from below to Z +0.25, above the deck. Their
  corners reach 9.84 mm from the axis, 1.14 mm outside the plinth; the encoder body corners reach 9.13 mm. The
  CNC top shell would get four open holes at the plinth ends (review finding). The 1.3 mm wall holds only on the
  straight sides.
- **Options.** (a) Same box, corner radius 2.8 mm or less. (b) Keep the stadium and grow it to 22.3 mm in Y, which
  brings it within 0.65 mm of the lens recess.
- **Decision.** (a): 36.1 x 17.4 mm, R2.8.
- **Reason.** A pocket with R1.5 corners grown by the 1.3 mm wall is a rounded square of R2.8 and the same half
  size as the plinth (8.7 mm), so any plinth radius up to 2.8 mm holds the wall all round. (b) changes the look
  more and crowds the lens.
- **Consequences.** The plinth reads as a bar with small radii instead of a stadium. `tools/check_spec.py` samples
  the walled pocket outline and tests it against the rounded plinth. Request to rotary-buttons: update 6.3.

## D26. Switches go in on an insertion jig

- **Context.** Eight hot-swap sockets (rows 0 and 1, columns 0 to 3) lie over the battery pocket with only the cell
  under the 0.3 mm insulating sheet. Inserting a switch pushes its socket with up to 3.0 kgf (keys 6.4), which
  needs support within 0.3 mm. Through the PCB that load would reach the pouch, against power 14 rule 1 (review
  finding).
- **Options.** (a) Switches go in only on a printed insertion jig with the bottom shell off. (b) A rigid plate
  between the sockets and the cell. (c) Move the pocket out from under the sockets.
- **Decision.** (a). Every switch insertion, at build and by the user, happens with the cell unplugged, the bottom
  shell off and the top shell with the PCB resting on the jig. Jig ribs sit 0.2 mm under each socket underside,
  inside the socket zone (keys 6.4).
- **Reason.** (b) does not work: a 0.5 mm FR4 plate across the 36 mm pocket under a 29.4 N point load deflects
  about 7 mm (simply supported, 20 mm effective width, E 20 GPa, estimate), far past the 0.5 mm swelling gap, and
  its thickness would push the pocket floor under 1.5 mm. (c) has no room (D4). In use, key presses load the
  switch housing into the plate, not the socket.
- **Consequences.** Hot-swap is a bench job, not a closed-case one, unlike the GLYF. The jig is a new FDM part
  (request to the CAD builder). `board.toml` `[assembly]` holds the rule; `tools/check_spec.py` checks the rib gap.

## D27. FDM bottom shell printed on the ramp plane

- **Context.** enclosure 8.2 prints the bottom shell as a flat tray, floor down, with the wedge as a separate bar.
  After D4 the pocket floor needs an underside at Z -17.45, 2.85 mm below the front underside, so there is no flat
  tray underside (review finding).
- **Options.** (a) One piece with the wedge, printed with the ramp plane on the bed. (b) Split the wedge bar
  around a pocket box printed with the tray.
- **Decision.** (a). The ramp plane lies on the bed; supports under the rear slope (Y 0 to 15) and under both
  flank scoops (13 mm wide, Y 0 to 35). The separate
  wedge bar and its two extra screws go.
- **Reason.** The ramp is one plane and the pocket box lies above it (the wedge depth check proves it), so the part
  sits flat. Inner floors tilt 4.89 degrees and face up. Each flank scoop is open at the side and rear faces, so
  its roof hangs from two edges and cannot bridge; it needs supports (CAD print check). The foot pockets bridge
  8.4 mm, inside the 15 mm limit. (b) adds a joint and screws for nothing.
- **Consequences.** The part is 128.4 x 85.5 mm on the bed and 16.8 mm tall. The rear slope stands 34.7 degrees
  to the bed and needs supports, so its print finish is rough; the prototype accepts that. Request to the
  enclosure owner: update 8.2. `tools/check_spec.py` checks the bed fit, the bridge spans and that `[print.bottom_shell]` names both
  support zones.

## D28. Build order, cell orientation and lead

- **Context.** The records create order dependencies (button caps from below before the PCB, flex into the
  top-face connector before G1 and G2, RF insert before closing, D26 for switches) and the cell lies in the bottom
  shell while its plug goes into a header on the PCB, which hangs from the top shell (power 14 rules 3 to 5). No
  build order, lead length or cell orientation was written (review finding).
- **Decision.** Cell PCM end and lead toward +X (PCM end at X 77.5, the connector end, away from the wedge's
  thinnest point, power 14 rule 3). Lead exit Y 37.5 (guess; measure), inside the relief Y 31.5 to 43.5. Lead
  length 19 mm or more (9 mm path to the plug back plus the 10 mm loop of rule 4) and 60 mm or less (guess, the
  most that stows in the relief). The Adafruit 258 lead length is not recorded; measure it, and do not fit a cell
  whose lead is outside the range. The foam pad sits on the pocket floor and is not bonded to the cell. Build
  order:
  1. Bond the lens into the top-shell recess (display 6.4); let it cure.
  2. Top shell deck down on a soft mat. Fit the display module and tape frame against the web, flex toward the
     front.
  3. Drop both button caps into their holes from below (rotary-buttons 6.6).
  4. Hold the PCB top face toward the shell, insert the flex into the FH34SRJ and close its latch.
  5. Seat the PCB on the G posts; fit G1 and G2 from below.
  6. Turn the assembly deck up onto the insertion jig and press in the 16 switches (D26).
  7. Deck down on the mat. Lay the 0.3 mm insulating sheet over the sockets, lay the cell on it inside the pocket
     outline with the PCM end to +X, plug the lead into the header and dress the loop in the relief area.
  8. Slide the RF insert into the bottom-shell slot; place the foam pad on the pocket floor; stick the feet.
  9. Lower the bottom shell over the cell; fit C1 and C2 from below.
  10. Deck up; fit K1 to K4 from the top, then keycaps, knob shims and knobs.
  Disassembly runs backward. With the unit underside up, lifting the bottom shell leaves the cell lying on the
  PCB, and unplugging it is the first step (rule 5).
- **Reason.** The order follows the access each record needs. Fitting the cell onto the PCB and lowering the
  shell over it needs only a short lead, which keeps the loop inside the relief.
- **Consequences.** `board.toml` `[battery]` and `[assembly]` hold the values; `tools/check_spec.py` checks the
  lead exit and the lead length range.
- **Superseded in part by [D39](#d39-cell-bonded-to-the-pocket-floor-top-assembly-lowered-onto-the-bottom-shell).**
  Steps 7 to 10, the foam sentence and the disassembly note are replaced there. The cell orientation, the lead exit
  and steps 1 to 6 stand.

## D29. Corner radii for JLCCNC

- **Context.** enclosure 5: R >= H/10 + 0.5, and the table "R 1.5 or more in pockets up to 10 mm deep, R 2.0 to
  15 mm". The battery pocket is 10.95 mm deep from the split face with R1.5; the key well kept the GLYF R1.0
  against enclosure 6.2's R1.5; no cavity radius was given (review finding).
- **Decision.** Battery pocket R2.0 (cell corners still clear by 0.59 mm). Key well R1.5 (keycap corners clear).
  Cavity corners, battery relief, top RF pocket and plinth pockets R1.5. The display pocket keeps R1.0 and T-bones
  by waiver (D33).
- **Reason.** Manufacturability before the GLYF look; R1.0 to R1.5 on the well is hard to see under the caps.
- **Consequences.** `tools/check_spec.py` checks every pocket against the formula and the table, lists waivers by
  entry, and checks the PCB corner radius against the cavity radius and the left wall gap.

## D30. K screws M1.6

- **Context.** The 4.30 mm M2 countersinks on the column boundaries leave 0.375 mm of plate top to the neighbouring
  switch openings, under JLCCNC's 0.5 mm absolute minimum and the 0.8 mm recommendation, on a bead-blasted part
  (enclosure risk 5; review finding).
- **Options.** (a) Keep M2 and get JLCCNC to accept the knife edge on the quote. (b) M1.6 DIN 7991 (head 3.0 mm,
  countersink 3.30 mm).
- **Decision.** (b): M1.6 x 5 DIN 7991, countersink 3.30 mm, clearance hole 1.80 mm. Positions unchanged.
- **Reason.** (a) is under the absolute minimum; a DFM acceptance does not make the edge survive blasting. (b)
  gives 0.875 mm of web.
- **Consequences.** The case owner recomputes thread, drill depth and engagement for M1.6 x 0.35 (tap drill
  1.25 mm) in enclosure 6.4, and the FDM K boss screw (M1.6 x 8 self-tapping instead of M2 x 8). The PCB holes and
  keep-outs do not change. `tools/check_spec.py` checks the web against `case.min_metal_wall`.

## D31. Rear feet and the C2 spot-face

- **Context.** D4 moved the apex to Y 15.0 but kept the GLYF rear-foot centre Y 18.2; the Ø8.4 pockets then cross
  the apex, and the rear one is open toward the rear slope. D4 also said C2 gets a spot-face from below but gave no
  size; the front-right foot is close (review findings).
- **Decision.** Rear feet at Y 20.5: pockets Y 16.3 to 24.7, 1.3 mm in front of the apex, wholly on the ramp
  plane. C2 spot-face Ø4.8 mm, flat floor at Z -13.70 (1.60 mm deep at the 15.30 mm body), which is where the
  enclosure's 2.0 mm local floor ends. Front feet unchanged.
- **Reason.** Smallest moves. The spot-face restores enclosure 6.4's C2 seat, thread and screw unchanged.
- **Consequences.** Floor over the battery pocket under the rear-left foot 3.02 mm. Spot-face to front-right foot
  1.06 mm against a 1.0 mm limit (guess). `tools/check_spec.py` checks that each foot lies on one plane (apex and
  scoops) and the foot walls against the spot-face.

## D32. Ground screw G2 at (121.25, 66.6)

- **Context.** The top shell is pocketed over the RF bay up to Z -2.80 (D11). The void checks of revision A left
  that pocket out. G2 at (120.9, 65.8) sat 0.40 mm from it in plan against the 1.2 mm post-to-void rule that D7
  applied to the button counterbore; the FDM insert hole was 1.10 mm from it against 1.3 mm (review finding).
- **Options.** (a) A waiver: the post lies below the split and the pocket above it. (b) Move G2 so both rules hold.
- **Decision.** (b): G2 at X 121.25, Y 66.6 (x_right 7.15).
- **Reason.** (a) would apply the rule differently to two pockets of the same shell. At (121.25, 66.6) the post
  keeps 1.20 mm to the RF pocket and 1.23 mm to the counterbore; the FDM insert hole keeps 1.90 and 1.93 mm.
- **Consequences.** The GND ring is 0.90 mm from the board edge; the G2 head keeps 1.65 mm to the RF insert.
  `tools/check_spec.py` now includes the RF pocket and the display T-bones among the top-shell voids and checks
  the FDM insert walls. The 0.80 mm wall between the display pocket and the RF pocket is checked too (D33).

## D33. Display pocket corners and right edge

- **Context.** The display pocket is cut 3.05 mm deep from the split face; the formula needs R0.81 and enclosure
  6.5 asks for R1.0 corners or reliefs. With R1.0 corners the square module corner would lie 0.07 mm outside the
  arc. D24 moves the RF pocket 0.2 mm inward, so the display pocket edge at X 114.2 would leave 0.65 mm of wall
  to it (review finding plus the D24 change).
- **Decision.** Right pocket edge X 114.05 (display 6.5 had 114.2), leaving 0.17 mm to the module, the same as the
  rear edge. Rear corners: T-bone reliefs Ø2.1 centred on the rear edge, 1.05 mm in from each side, running into
  the area under the web. Front corners: R1.0, 3 mm clear of the module corners.
- **Reason.** T-bones along Y keep the wall to the RF pocket (side reliefs along X would cut into it) and keep the
  rear corners sharp for the module. A full R1.5 would need the pocket 0.44 mm wider per side.
- **Consequences.** Wall to the RF pocket 0.80 mm. The R1.0 and the T-bones are under the table's R1.5, by waiver
  in `tools/check_spec.py`; they need the 2.0 mm tool that the switch openings use anyway. The module tolerance of
  +/-0.1 mm per side fits. Request to display: update 6.5.

## D34. Bottom wall step under the plate lip

- **Context.** The CNC plate lip ends at Z -5.15, 0.15 mm below the split plane. enclosure 6.1 decided that the
  bottom wall stays 0.3 mm outboard of the plate edge or the top 0.5 mm of the wall is thinned to 3.0 mm.
  `board.toml` had no value (review finding).
- **Decision.** `body.bottom_wall_step = [0.5, 3.0]`: the top 0.5 mm of the bottom-shell wall is 3.0 mm thick along
  the key-well walls.
- **Consequences.** 0.50 mm between the wall and the plate edge against 0.3 mm. The FDM plate ends at the split and
  needs no step; the shared model keeps it. Checked by `tools/check_spec.py`.

## D35. Bottom-face positions of the power parts

- **Context.** power 6.4 and 14 rule 6 put the charger at least 10 mm from the pocket and not next to the LDO, and
  the NTC over the cell between socket zones; usb-io 6.3 puts the PTC at least 10 mm from the charger, the CC
  resistors within 5 mm of the receptacle and the ESD array within 3 mm of its pads. `board.toml` held only the
  10 mm value, with no position to check (review finding).
- **Decision.** Bottom-face positions in `[power.parts]`, all guesses inside the rules: ESD at (100.8, 10.0), CC1
  and CC2 at (95.6, 9.5) and (106.0, 9.5), PTC at (100.8, 18.5), gauge at (100.0, 30.0), charger at (106.0, 32.0),
  LDO at (108.0, 45.0), NTC at (43.5, 25.0). "Not next to" is taken as 5 mm or more (guess).
- **Consequences.** Charger 26.0 mm from the pocket, 10.0 mm from the LDO, 11.4 mm from the PTC; NTC 1.68 mm from
  the nearest socket zone and 1.25 mm tall against 2.15 mm. The layout may move parts if the checks still pass.

## D36. Encoder RC filter footprints

- **Context.** rotary-buttons asks for two unpopulated 0402 10 nF footprints per encoder, A and B to ground, in
  case the 13 kOhm internal pull-ups give double counts. `board.toml` had none (review finding).
- **Decision.** `[encoders.filter]`: 10 nF X7R 0402, not fitted, at the encoder centre +/-2.5 mm in X and 5.5 mm
  toward the rear, just in front of the A/C/B pin row, bottom face.
- **Consequences.** Four more footprints, no BOM line until fitted. The overlap check covers them.

## D37. USB-C recess kept at 0.25 mm pending a plug test

- **Context.** usb-io U3 allows the receptacle front 0.0 to 0.3 mm behind the rear face and cites USB Type-C R2.0
  figure 3-80: "product surface at the receptacle front, 0.05 mm minimum to the overmold". A reviewer read that as
  a 0.20 mm interference for a worst-case plug whose overmold is larger than the 10.0 x 4.9 mm notch. The cited
  figure (`_cache/usb-io/render-04/typec-p-136.png`) is not in the cache, so neither the reviewer nor this entry
  could re-read it.
- **Options.** (a) Front at 0.0 to 0.05 mm. (b) Widen the notch to the overmold envelope. (c) Keep 0.25 mm and gate
  the case order on a plug test.
- **Decision.** (c). The finding is not rejected on its merits; the fix is deferred because both changes it names
  break something that is checked.
- **Reason.** (a) moves the receptacle 0.20 mm rearward; its tongue then reaches Y 0.75 against the wall pocket
  front at Y 0.60, a 0.15 mm gap against +/-0.2 mm outline tolerance and +/-0.1 mm PCB location. (b) makes the
  notch about 6.5 mm tall, which crosses the split plane (D18) and leaves under 1.2 mm of wall below it (usb-io U4).
- **Consequences.** Gate before the case is ordered: the usb-io owner re-reads Type-C R2.0 section 3.10.3 and
  figure 3-80, and the FDM print is tried with a set of cables with large overmolds. If plugs do not seat, the
  next step is a 0.3 mm deep relief of the overmold size in the outer rear face around the notch.
  `tools/check_spec.py` checks the front against the U3 band only.

## D38. Backlight driven by display_power.c, not zmk,display-led

- **Context.** display 3 and mcu-radio name P0.24 as ZMK's `zmk,display-led`. Stock ZMK
  (`app/src/display/main.c`) calls `led_on` on that node when the panel unblanks, which sets a PWM LED to 100 %
  duty. power 15 asks for 25 to 50 % in use (24 to 39 mA for the lit panel against 69 mA at 100 %, estimate).
- **Options.** (a) Keep `zmk,display-led` and accept 100 % on every wake. (b) Leave the chosen node out and drive
  a `pwm-leds` node from `firmware/zmk/src/display_power.c`.
- **Decision.** (b). The board devicetree has a `pwm-leds` node `backlight` on P0.24 and no `zmk,display-led`.
  `display_power.c` sets the duty to `CONFIG_WORXPAD_BACKLIGHT_PERCENT` (default 40) on activity and turns it off
  on idle.
- **Reason.** With (a), ZMK and `display_power.c` would both write the LED, and every wake would start at full
  duty. (b) has one owner for the LED.
- **Consequences.** The P0.24 note in `board.toml` `[pinmap]` names the `pwm-leds` node. Request to the display
  record owner: update display 3 and the pin list, which still say `zmk,display-led`. Not measured on a board.

## D39. Cell bonded to the pocket floor, top assembly lowered onto the bottom shell

- **Context.** In the D28 order the RF insert and the foam pad go into the bottom shell open side up; the shell is
  then turned over and lowered onto the deck-down top assembly. Nothing holds either part. The insert's Ø1.90
  keys sit in Ø2.00 vertical reliefs open at the split face (enclosure 7.2 items 2 and 3), and the foam pad was
  not bonded. The cell lay loose with 0.5 mm free in Z and 1.0 mm a side in plan. power 14 rule 1 holds the cell
  with double-sided foam tape or a foam pad on the floor, and enclosure 7.2 item 3 has the insert go in from
  above and the top shell close it from above (review finding).
- **Options.** (a) Build into the open bottom shell: bond the foam tape to the floor and the cell onto it, plug
  the lead with the top assembly held over the shell, then lower the top assembly deck up. (b) Keep the D28
  order and hold the insert and the foam with tape or adhesive dots.
- **Decision.** (a). The build order from D28 step 7 on:
  7. Top assembly deck down on the mat. Stick the 0.3 mm insulating sheet (self-adhesive, 0.3 mm overall) onto
     the socket bodies so that it covers the pocket outline.
  8. Bottom shell open side up. Slide the RF insert into its slot from above, keys into the reliefs. Bond the
     0.2 mm double-sided foam tape to the pocket floor. Peel its liner, set the cell on it inside the pocket
     outline with the PCM end to +X and the lead in the relief, and press it down with a flat hand, no point load.
  9. Hold the top assembly deck up over the bottom shell, +X ends together, only as high as the lead allows. Push
     the plug into the header along +X. Lower the top assembly and dress the loop in the relief, clear of the
     split face and the posts. The split faces must meet all round without force.
  10. Fit K1 to K4 from the top. Underside up on the mat: fit C1 and C2 and stick the feet. Deck up: keycaps,
      knob shims and knobs.
  Disassembly: remove C1 and C2 from below and K1 to K4 from the top, lift the top assembly only as far as the
  lead allows, and unplug the cell first (rule 5). The cell stays bonded in the bottom shell.
- **Reason.** (a) meets power 14 rule 1: the tape on the floor holds the cell, and nothing clamps it (the 0.5 mm
  swelling allowance stays free above it). It also builds the insert as enclosure 7.2 item 3 says, with no glue
  and no fastener. At every step each loose part rests on the part below it. (b) puts an adhesive on the radio
  window insert, which 7.2 item 3 rules out. Under (b) the cell would also meet the floor tape only by gravity
  after the unit is turned over, so rule 1 is still not met.
- **Consequences.** Plugging with the top assembly held over the shell needs more lead than the closed unit. The
  D28 minimum of 19 mm (9 mm path plus the 10 mm loop) leaves no working gap. The extra length stows in the
  relief up to the 60 mm limit (guess). Nobody knows the gap a hand needs to push the plug home; the first build
  measures it (MEASURE). Requests to the `board.toml` owner: a guessed plug working gap in `[battery]` that the
  lead length check adds to the path, and new `[assembly]` `cell_fitting` text. The insulating sheet is now
  self-adhesive ([bom-hand.csv](bom-hand.csv)). Not tried on parts.

## D40. Third setup for the bottom-shell foot pockets

- **Context.** The JLCCNC order notes and [ordering-case.md](ordering-case.md) justified 3-axis milling with
  "two setups per shell" (enclosure 5). The case model cuts the foot pockets square to the 4.89 degree ramp. The
  bottom-shell drawing calls that the ramp setup, and the CAD checks judge the foot pockets in it. enclosure 5
  lists the foot pockets in underside setup B and says the ramp needs surfacing or a tilted setup. So the bottom
  shell needs a third setup, and the quote must include it (review finding).
- **Options.** (a) Make the foot pockets vertical, cut in level setup B; change the model, the drawing note and
  the checks. (b) Keep the model and state the third setup in the order documents.
- **Decision.** (b), until a quote shows what the third setup costs. Top shell: two setups. Bottom shell: three;
  the third holds the ramp plane level (a 4.89 degree fixture, or 3+2-axis) for the foot pockets, and the shop
  may cut the ramp face there instead of surfacing it.
- **Reason.** (b) states what the model, the drawing and the CAD checks already describe. (a) changes geometry
  whose checks pass, for a cost nobody has quoted.
- **Consequences.** Request to the owner of `cad/production/jlccnc/ORDER_NOTES.md`: the Process row says two
  setups per shell; make it match. If the JLCCNC quote for the bottom shell is high because of the third setup,
  (a) is the next step for the case owner. No quote has been asked for.
