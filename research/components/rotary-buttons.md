# Rotary knobs and round buttons (key `rotary-buttons`)

Decision record, revision 2, 2026-11-13. Status: proposed.

Revision 2 answers a review of revision 1. The part choices stand. The knob underside, its bore, its fitted
height and the plinth pocket change. Section 11 lists each review point and what was done with it.

## 1. Summary

1. Encoder: **Bourns PEC12R-4215F-S0024** (LCSC and JLCPCB `C22385080`, extended, through-hole). It has
   24 detents and 24 pulses, a push switch, an insulated D-flat shaft of 6.0 mm, and a total height of 15.0 mm
   from the PCB top face to the shaft tip. At every detent both contacts are open, so the encoder adds no
   pull-up current in idle or deep sleep. This meets the rule in `mcu-radio.md`.
2. Fallback encoder: **PEC12R-4217F-S0024** (`C49671241`). It has the same body and footprint and a 17.5 mm
   shaft. Its knob is 11.60 mm tall and stands 2.50 mm higher than the main knob (section 6.4).
3. Knob: CNC 6061 aluminium from the case vendor, black anodised, 10.50 mm in diameter and 9.10 mm tall. Its
   underside has a Ø8.40 x 1.20 mm counterbore over the encoder collar, then a short round relief, then a
   D-bore with one M2 set screw on the shaft flat. The knob height is set at assembly with a 1.10 mm shim
   between the knob rim and the plinth, because neither the collar nor the shaft tip is a usable seat. The
   knob top sits at deck +12.0. The FDM and resin versions have the same outline and a crush-rib bore.
4. The encoder body is 6.10 mm tall. The deck sits 6.20 mm above the PCB top, so the top shell cannot cover
   the body. The top shell therefore carries one raised **knob plinth**, 1.80 mm tall, over both encoders. It
   replaces the two round 16.1 mm bosses of the GLYF. This is a visible change from the GLYF look, and section
   6.3 explains why it is needed.
5. The round controls are **buttons, not dials** (confirmed, section 3). Each one is an **Omron B3FS-1000P**
   SMD tactile switch (`C271750`, 0.98 N, 3.1 mm tall, 1,000,000 operations). It sits under a round plunger
   cap, 12.30 mm across, in a 12.50 mm hole. The cap stands 1.00 mm proud and travels 0.25 mm to actuate.
   The first batch uses resin caps. CNC aluminium caps are optional.

## 2. Context and requirements

The settled records fix these inputs.

| Input | Value | Source |
| --- | --- | --- |
| Deck above the PCB top face | +6.20 mm | `research/components/keys.md`, stack table |
| PCB | 1.6 mm. SMD parts sit on the bottom side; the top side keeps a 14.6 mm square clear per key switch | `keys.md` interfaces |
| Encoder and button pushes | Matrix column C4: R0 encoder 1 push, R1 encoder 2 push, R2 button 1, R3 button 2, one 1N4148W diode each | `keys.md` |
| Encoder A/B pins | Left encoder P0.28 / P0.30, right encoder P0.29 / P0.31, internal 13 kOhm pull-ups, ZMK `alps,ec11` driver | `mcu-radio.md` pin table |
| Encoder rest state | Both contacts must be open at every detent, or each closed contact costs about 254 uA | `mcu-radio.md` sections 7.6 and 8 |
| Body | 128.4 x 85.2 mm. 8.0 mm was added on the right side, so every control moves 8.0 mm further from the right face | `mcu-radio.md` 7.3.3 |
| RF bay | Y 42.9 to 63.1 mm from the rear face, 9.4 mm in from the right face. No encoder, button or metal is allowed inside it | `mcu-radio.md` A4 to A6 |

The GLYF measurements below are taken from `research/raw/geometry.md` section 4.4. All are "likely".

| GLYF quantity | Value |
| --- | --- |
| Knob diameter | 10.5 mm. Top flat 8.0 mm, edge radius 1.25 mm |
| Knob top above the deck | 11.8 mm (11.5 to 12.1) |
| Knob cap height | 9.1 mm, from deck +2.7 to +11.8 |
| Boss around each knob | 16.1 mm at the base, 1.8 mm tall, 0.85 mm gap to the knob |
| Knob centres | 15.10 mm from the rear face. 10.27 and 28.96 mm from the right face on the GLYF; 18.27 and 36.96 mm on worxpad. 18.68 mm apart |
| Round button | Skirt 12.30 mm in a 12.50 mm hole, top face 10.3 mm, 1.0 mm proud, 14.0 mm from the front face, same X as the knobs |

The task asks for these requirements.

| ID | Requirement |
| --- | --- |
| R1 | The knob looks like the GLYF knob: 10.5 mm across, top about 11.8 mm above the deck. |
| R2 | The encoder has a push switch and a detent. |
| R3 | At every detent both contacts are open. |
| R4 | JLCPCB can source it in the quantity needed: 10 encoders and 10 buttons for 5 units, plus spares. |
| R5 | The encoder fits under the deck. Body top at +6.20 or lower, with a shell roof above it. |
| R6 | The shaft tip is low enough for a knob top at about +18.0 above the PCB, with a roof of at least 1 mm. |
| R7 | The round buttons are 12.3 mm across, stand about 1 mm proud, and have a short, light travel. |

## 3. What the GLYF uses (evidence)

| Fact | Source | Confidence |
| --- | --- | --- |
| The prototype used "Alps Alpine rotary encoders", and the photos show a metal body on a green base | `research/raw/regulatory-software.md` (Update 03); `research/raw/social.md` section 4 | confirmed (prototype), likely (production) |
| The encoder footprint name contains "RotaryEncoder ... Switch" | `research/raw/official-site.md` (Update 01 KiCad frame) | confirmed |
| The firmware runs two encoders on the ZMK `alps,ec11` driver. The dev shield uses `steps = <80>` and `triggers-per-rotation = <20>` | `regulatory-software.md` | confirmed (driver) |
| The bottom round controls are 2 navigation buttons in the 5 x 4 matrix, with hold-tap. They are not dials | `regulatory-software.md`; `official-site.md` ("two buttons to control the screen") | confirmed |
| Button footprint "SW_Omron_B3FS" | `youtube.md`; `geometry.md` section 6 | likely |
| Knobs are injection-moulded PBT | product page, `official-site.md` | confirmed |
| A 2024 AS5600 magnetic-encoder experiment did not ship | `regulatory-software.md` | likely |
| Exact encoder model, detent count and push force | none | not found |

Note on the GLYF stack. The GLYF knob top is about 17.7 mm above its board. Every standard EC11 with push
that was checked has a shaft tip 19.5 to 24.5 mm above the PCB, and the Alps EC12D with push has 17.5 mm. The GLYF may therefore use a shortened shaft,
a special variant or a different board level. This was not resolved (guess).

## 4. Candidates: encoders

All stock and price figures are from the JLCPCB parts API (`research/_cache/rotary-buttons/jlc-01`, `jlc-02`,
`jlc-03`) and the LCSC product-detail API (`lcsc-02`, `lcsc-03`), read on 2026-11-13. Heights are measured
from the PCB top face, which is the encoder's mounting surface.

| Candidate | Body top | Shaft tip | Detent / pulse, rest state | Push | Stock (JLCPCB / LCSC) | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **Bourns PEC12R-4215F-S0024** `C22385080` | 6.1 | 15.0 +/-0.5 | 24 / 24; both open at the detent (datasheet quadrature table) | 0.5 +/-0.3 mm (general table; the drawing prints 0.4 +0.3/-0.2), 610 +/-306 gf | 28 / 28, USD 2.95 / 2.97 | **Chosen** |
| Bourns PEC12R-4217F-S0024 `C49671241` | 6.1 | 17.5 +/-0.5 | 24 / 24, open | same | 75 / 75, USD 2.44 | **Fallback**. The knob grows to 11.60 mm and its top to deck +14.50, with a 3.90 mm counterbore over the 5.0 mm collar (section 6.4) |
| Alps EC11E15244G1 `C370970` (EC11E, 30/15, 0.5 mm push) | 4.5 | 24.5 | 30 / 15: the rest state alternates between both open and both closed (half-pulse per detent) | 0.5 mm | 2,700 / 2,700, USD 2.39 | Rejected. The tip is 6.5 mm too high, and half the detents rest closed (2 x 254 uA). It only fits if the shaft is cut by 8 mm, which leaves 2 mm of flat |
| Alps EC11E09244BS `C470742` (18/9) and EC11E18244AU `C202365` (36/18) | 4.5 | 24.5 | half-pulse detents | 0.5 mm | 6,392 / 4,655 and 2,544 / 632 | Rejected for the same reasons |
| Alps EC11J1525402 `C209762` (SMD, reflow) | not read | 24.5 (20 mm actuator, same frame as the EC11E) | 30 / 15 | 1.5 mm, 4 +/-2 N | 1,461 / 1,461, USD 3.06 | Rejected. Too tall, half-pulse detents, heavy push. Its only advantage (reflow) does not matter here |
| Bourns PEC11R-4215F-S0024 `C143790` | 6.5 | 21.5 (L is measured from the bushing face) | 24 / 24, open | 0.5 mm | 4,141 / 3,884, USD 2.33 | Rejected. Tip 4.5 mm too high, and the body sits above the deck |
| Bourns PEC11L-4x15F-S (low profile) `C22402273`, `C20882995` | 4.5 | 19.5 (L from the bushing face) | 30 / 15 or 20 / 20 | 0.5 mm | 9 and 248 | Rejected. Tip 2.5 mm too high; the 15 mm variant has no stock |
| Alps EC12E (e.g. `C351238`) | low | 15 to 30, or hollow shaft | 24 / 24 | **none** | 1,164 | Rejected. No push switch in the series (Alps EC12E list) |
| Alps EC12D with push, e.g. EC12D1524403 `C112349` (2,400), EC12D1524406 `C470461` (1,208), EC12D1564404 `C470462` (1,597), EC12D1564402 `C444933` (336); all JLCPCB extended | not read | LM1 17.5 | 30 / 15 per the Alps table. The Alps phase diagram marks the detent stability positions ON, OFF, ON, so the rest state alternates. LCSC lists `C444933` as 24 / 24, which conflicts with the Alps table | 0.5 mm, 5 +/-3 or 10 +/-5 N | as listed | Rejected. Half-step detents (R3 fails), a tip no lower than the fallback PEC12R, and a push force up to 15 N. Added in revision 2; the review found it |
| Alps EC09E1524417 `C398936` (9 mm) | not read | 20 mm actuator | 30 / 15 | 0.5 mm, 6 N | 703 / 688 | Rejected. Tall shaft and half-pulse detents |
| CUI / Same Sky ACZ11, ACZ09 | not read | 15 to 25 | 12C, 20C, 30C15P | ACZ11BR only | 0 at JLCPCB (all records) | Rejected. No stock |
| Bourns PES12 `C49672973` | not read | not read | no detent (N) | no | 20 | Rejected. No push, no detent |
| Magnetic: MT6701 `C2913974` (QFN, 2,455) or `C3003196` (SOP-8, 1,279); AS5600 `C55240803` (1,046) under a bearing-mounted knob | sensor 0.75 to 1.75 | n/a | no detent | no | as listed | Rejected. The magnet would sit about 6 mm above the PCB, so it needs a spigot down to about 2 mm. It also needs a bearing in the shell and a separate push mechanism. Zephyr has an `ams_as5600` sensor driver that reports an absolute angle on SENSOR_CHAN_ROTATION, but ZMK sensor bindings expect deltas, so an adapter module is needed, and I2C polling costs standby current. No MT6701 driver was found. Kept as a later upgrade for a smooth or haptic knob |

How the detent rest state was checked: the PEC12R and PEC11R quadrature tables mark the detent D at A OFF and B
OFF (`_cache/rotary-buttons/ds-02/pec12r-qot.png`, confirmed). For Alps parts with twice as many detents as
pulses, each detent is half a cycle, so the rest state alternates. This follows from the 2:1 ratio in the Alps
product lists, and the EC12D phase diagram in the Alps catalogue marks the detent stability positions ON, OFF, ON
(`_cache/rotary-buttons-sceptic/b4/ec12d1524403.txt`). This is now confirmed for the EC12D and likely for the
EC11E, EC11J and EC09E, whose phase diagrams were not read.

## 5. Candidates: round buttons

| Candidate | Height above PCB | Force, travel, life | Stock | Verdict |
| --- | --- | --- | --- | --- |
| **Omron B3FS-1000P** `C271750` (6.0 x 6.3 mm, flat plunger) | 3.1 +/-0.2 | 0.98 +/-0.29 N, pretravel 0.25 +0.2/-0.1 mm, 1,000,000 operations | JLCPCB 67,955, USD 0.21; LCSC 67,955 | **Chosen**. The GLYF footprint, the lightest force and the longest life in the series |
| Omron B3FS-1010P `C231324` (4.3 mm plunger) | 4.3 +/-0.2 | same | 2,544 / 2,445, USD 0.29 | Second choice. Its 1.2 mm extra height leaves only 0.4 mm for the cap flange |
| XKB TS-1187A-B-A-B `C318884` (5.1 x 5.1 mm) | 1.5 | 1.6 N, 100,000 operations | JLCPCB **basic**, 815,200 | Rejected. Its only gain is the basic-part fee. It is 63 % heavier and has a tenth of the life |
| Alps SKRPACE010 `C139797` (4.2 x 3.2 mm) | 2.5 | 2.6 N, 50,000 operations | 155,368 / 154,820, USD 0.07 | Rejected. Too heavy for a thumb button next to light keys |
| Kailh Choc V2 (PG1353D) under a round cap, hot-swap | cap top at least deck +3.4 | about 2.8 mm travel, same feel as the keys | socket `C5333465`: 0 stock (`keys.md`) | Rejected. The 14.0 mm plate opening is wider than the 12.3 mm cap and would show around it. A round cap needs at least 15.5 mm. The stem top at rest is deck +2.4, so the cap stands at least 3.4 mm proud, not 1.0. The socket is out of stock and would be hand-soldered |

## 6. Decision and the numbers the design needs

### 6.1 Encoder: PEC12R-4215F-S0024

Values from the datasheet drawing "PEC12R-4xxxF-Sxxxx (Horizontal Mount - Axial PC Pin/No Bushing, Push
Momentary Switch)", REV. 07/21 (`_cache/rotary-buttons/ds-02/PEC12R.pdf`, render `pec12r-hi-4.png`). In Bourns
terms "horizontal mount" means a flat PCB with the shaft upright. LCSC labels the part "Right-Angle"; that is a
catalogue label only.

| Item | Value | Confidence |
| --- | --- | --- |
| Body | 12.4 mm (across the pin rows) x 13.4 mm, 6.1 mm above the PCB top | confirmed |
| Shaft | Ø6.0 +0/-0.1, insulated (plastic), flat 4.5 +0/-0.1 across, flat length F 5.0 from the tip, tip chamfer | confirmed |
| Shaft tip | L 15.0 +/-0.5 above the PCB top | confirmed |
| Push switch | Travel 0.5 +/-0.3 mm in the general table (0.4 +0.3/-0.2 on the -4xxxF-S drawing). The design uses the wider band, 0.2 to 0.8 mm. Force 610 +/-306 gf | confirmed |
| Tolerances | General: below 10 mm +/-0.3, 10 mm and above +/-0.5. So body height 6.1 +/-0.3, LB 2.0 +/-0.3, L 15.0 +/-0.5, F 5.0 +/-0.3 | confirmed |
| Collar | Its top is at body + LB = +8.1. Worst case +8.7 if both tolerances stack (+/-0.42 root-sum-square). Diameter not printed: about 7.3 mm scaled from the front view against the 12.4 mm body | guess for the diameter |
| Storage | "Use product within 6 months from the date of delivery" (datasheet caution) | confirmed |
| Rotation | 24 detents, 24 pulses, detent torque 30 to 90 gf-cm, bounce 2.0 ms max at 15 RPM | confirmed |
| Pins | A, C, B at 2.5 mm pitch in one row 7.5 mm from the shaft centre. Switch pins 1 and 2, 5.0 mm apart, 7.0 mm on the opposite side. Holes Ø1.0 +0.2/-0, 5 places | confirmed |
| Mounting legs | Two slots 2.1 +0.2 x 2.0 +0.2 mm, 13.2 mm apart, on the axis between the pin rows | confirmed |
| Below the PCB | Pins 3.5 mm below the mounting surface, so they stand 1.9 mm proud of the PCB bottom before trimming | confirmed (drawing), derived |
| Soldering | Wave soldering is specified. The datasheet says hand soldering is "Not recommended" | confirmed |

ZMK: on each encoder node, `compatible = "alps,ec11"` and `steps = <96>` (24 pulses x 4 quadrature edges; the
driver counts every edge). On the `zmk,keymap-sensors` node, `triggers-per-rotation = <24>`, so one event per
detent. The two properties live on different nodes (ZMK `docs/docs/config/encoders.md`). Bourns suggests a 10 kOhm and 10 nF RC filter on A and B. Add two 0402 10 nF footprints from
A and B to ground, unpopulated by default, in case the internal 13 kOhm pull-ups give double counts (judgement).

KiCad 10.0.7 stock library: the symbol `Device:RotaryEncoder_Switch` exists. The footprint
`Rotary_Encoder:RotaryEncoder_Bourns_Vertical_PEC12R-3x17F-Sxxxx` exists, but it is drawn for the bushing
version: its mounting slots are 11.2 mm apart, while the -4 drawing gives 13.2 mm. **Draw a project footprint**
from the -4 drawing. The pin pattern (A/C/B at 2.5 mm, switch pins 7.0 mm opposite, 14.5 mm between rows)
matches the stock one. The footprint references a STEP model, but the image has no `3dmodels` directory, so
no model was checked (not found). An Alps EC11E footprint is also in the library, for reference only.

JLCPCB: extended, through-hole. JLCPCB places it in its THT step. Stock is 28 at JLCPCB and 28 at LCSC (re-read
by the review on 2026-11-13), against 10 needed plus 2 spares; JLCPCB reports a pre-order minimum of 4.
**Order the encoders for the first batch now, or buy them at LCSC as a consigned part**, but no more than
about six months before assembly, because of the Bourns storage note. If stock runs out,
switch to `C49671241` (section 6.4). The footprint is unchanged.

### 6.2 Placement

Coordinates are from the right outer face (X) and the rear outer face (Y) of the 128.4 mm body.

| Part | Centre X | Centre Y | Footprint in plan |
| --- | --- | --- | --- |
| Encoder 1 (right, nearer the edge) | 18.27 | 15.10 | Body X 12.07 to 24.47, Y 8.40 to 21.80 |
| Encoder 2 | 36.96 | 15.10 | Body X 30.76 to 43.16, Y 8.40 to 21.80 |
| Encoder pin rows | | A/C/B row at Y 7.60 (rear); switch pins at Y 22.10 (front) | Pins at X centre +/-2.5 (A/B) and +/-2.5 (switch) |
| Button 1 | 18.27 | 71.20 | B3FS pads about 9.6 x 6.4 mm |
| Button 2 | 36.96 | 71.20 | same |

Both encoders sit on the PCB top face. Both buttons are SMD on the **top** face, the only top-side SMD parts.
Every part is outside the RF bay: the bay starts at Y 42.9 and reaches 9.4 mm in from the right face, while the
nearest part edge is at X 12.07.

### 6.3 Height stack (PCB top = 0; deck = +6.20)

| Level | Above PCB | Above deck |
| --- | --- | --- |
| Encoder body top, nominal (max) | +6.10 (+6.40) | -0.10 (+0.20) |
| Plinth pocket ceiling (0.35 mm over the maximum body) | +6.45 | +0.25 |
| Plinth top face (plinth roof 1.55 mm) | +8.00 | +1.80 |
| Encoder collar top, nominal (max) | +8.10 (+8.70) | +1.90 (+2.50) |
| Knob rim underside at rest, set with a 1.10 mm shim on the plinth | +9.10 | +2.90 |
| Knob rim underside pressed, 0.5 nominal / 0.8 max travel | +8.60 / +8.30 | +2.40 / +2.10 |
| Knob counterbore ceiling at rest / pressed at max travel (Ø8.40, 1.20 deep) | +10.30 / +9.50 | +4.10 / +3.30 |
| Start of the D-flat in the bore (round relief below it) | +11.30 | +5.10 |
| Shaft flat lower end, nominal (max) | +10.00 (+10.80) | +3.80 (+4.60) |
| Shaft tip, nominal (min / max) | +15.00 (+14.50 / +15.50) | +8.80 |
| Knob bore bottom (6.90 from the rim underside) | +16.00 | +9.80 |
| Knob top | +18.20 | **+12.00** (GLYF 11.8, range 11.5 to 12.1) |
| Button switch top | +3.10 +/-0.2 | -3.10 |
| Cap flange underside / top | +3.65 / +4.45 | -2.55 / -1.75 |
| Top shell underside around the button hole | +4.70 | -1.50 |
| Button cap top at rest / actuated | +7.20 / +6.95 | **+1.00** / +0.75 |

**Clearance checks (revision 2).** The shim sets the knob from the plinth top, so the PCB-to-shell stack
(taken as +/-0.15 mm) drops out of the rim gap. Worst cases:

1. Rim to plinth at maximum travel (0.8 mm): 1.10 - 0.80 - 0.05 (shim) = 0.25 mm. Nominal travel leaves 0.60 mm.
2. Counterbore ceiling to collar at maximum travel: plinth at its lowest (+7.85) + 2.30 - 0.80 = +9.35, against a
   collar of +8.70 at most: 0.65 mm. In plan the Ø8.40 counterbore and roof hole leave about 0.55 mm
   per side around a collar of about 7.3 mm (guess), so the collar does not touch the knob sideways either.
3. Bore bottom to shaft tip: +15.85 at the lowest plinth against a tip of +15.50 at most: 0.35 mm. The knob
   never seats on the tip, by design.
4. D-flat start to shaft flat end: the D-face begins at +11.15 or higher, and the shaft flat begins at +10.80 or
   lower, so a round shaft section never meets the bore flat. Flat engagement is 3.2 mm at the shortest tip
   (+14.50 minus +11.30).
5. Pocket: 0.35 mm over the maximum body height. In plan the pocket is 14.8 x 14.8 mm against 14.0 +/-0.5
   across the mounting tabs and 13.4 +/-0.5 for the body, so 0.15 mm per side remains at the worst case.
   Check both on a sample before the shell is cut.

**Why the review was right on the height datum.** In revision 1 the knob had no counterbore and no seat. Its
bore bottom (+15.80) lay above the tip (+15.00 +/-0.5), so a knob pushed home would stop on the collar with the
switch held at the end of its travel. Seating the bore on the tip instead would move the rim by +/-0.5 mm,
which at 0.8 mm travel would put the rim on the plinth. A fitting shim referenced to the plinth is the only
datum that removes both tolerances, so revision 2 uses it. The collar top stands up to 0.70 mm above the plinth
top inside the Ø8.40 roof hole, hidden by the knob; the case drawing should state this.

**Why a plinth.** The encoder body top is 0.10 mm below the deck (0.20 mm above it at the tolerance limit), so
a pocket from below cannot leave a roof. The cover has to rise above the deck. The body plus clearance needs a
14.8 x 14.8 mm pocket with R1.5 corners, which reaches 9.8 mm from the shaft at its corners. A round boss would
need about Ø22 mm, and two of them 18.68 mm apart would overlap. **Decision: one rounded-rectangle plinth over
both encoders**:

- Plan: X 9.57 to 45.66, Y 6.40 to 23.80 (36.1 x 17.4 mm), corner radius 8.7 (stadium ends). Each pocket wall
  is 1.3 mm in plan. The gap to the lens edge (Y 27.0) is 3.2 mm; the GLYF boss-to-lens gap is 3.8 mm.
- Height 1.80 mm above the deck. Top flat, 0.5 mm edge chamfer to match the deck chamfer language (judgement).
- Pockets from below: 14.8 x 14.8 mm, R1.5, ceiling at deck +0.25, so the roof is 1.55 mm thick. Shaft holes
  Ø8.40 through the roof clear the collar (about 7.3, guess). The 10.5 mm knob covers the hole.
- The case subsystem may shape the plinth differently. It must keep the pocket, the 1.55 mm roof, a flat
  plinth top under the knob rim (the shim datum) and the 1.10 mm rim gap.

Cost and benefit: the GLYF's two separate round bosses are lost, and in exchange the knob height matches the
GLYF range with a stock part and no shaft cutting. The alternative, an Alps EC11E with an 8 mm cut shaft and
round bosses, is the fallback for the look only (section 6.4).

### 6.4 Encoder fallbacks

1. **PEC12R-4217F-S0024** (`C49671241`, 75 in stock). It uses the same footprint, plinth and 1.10 mm shim.
   LB is 5.0, so the collar top is at +11.1 (+11.7 max), and F is 5.0, so the flat starts at +12.5 (+13.3
   max). The tip is at +17.5 (+17.0 to +18.0). Knob for this encoder, from the rim underside (+9.10):
   counterbore Ø8.40 x 3.90 (ceiling 0.35 mm clear of the highest collar at maximum travel and the lowest
   plinth), round relief to 4.60, D-bore to 9.40 (bore bottom 0.35 mm over the highest tip), set screw centre
   at 5.40, top wall 2.20. The knob is 11.60 mm tall and its top sits at +20.70, deck +14.50, which is 2.40 mm
   above the GLYF range. Revision 1 gave deck +12.50 for this case; that
   left only 0.7 mm of top wall over a 0.3 mm tip clearance and was wrong. Flat engagement is 3.3 mm. A lower
   knob is possible only by cutting the plastic shaft by 2.5 mm, which leaves 2.5 mm of flat and a glued knob.
2. **Alps EC11E15244G1** (`C370970`) with the shaft cut to +16.5. This is a look-only fallback that allows
   round bosses: the 4.5 mm body leaves a 1.7 mm roof under the deck. Only 2 mm of D-flat remains, so the
   knob must be glued. Half of the detents rest with both contacts closed, which adds up to 508 uA per encoder
   in deep sleep. Use it only if the plinth is unacceptable.

### 6.5 Knob

CNC version (JLCCNC or PCBWay, the same vendor and anodise batch as the shells):

| Feature | Value |
| --- | --- |
| Material, finish | 6061-T6, bead-blast, black anodise (matches `keys.md` and the case) |
| Outline | Ø10.50 x 9.10 mm tall. Top flat Ø8.0 with an R1.25 edge. Straight side, optionally with a fine vertical knurl (0.4 mm pitch) or plain |
| Underside | Flat annular rim, Ø10.50 outside, Ø8.40 inside. This rim is the height datum: it rests on the 1.10 mm shim during fitting |
| Counterbore | Ø8.40 +0.1/0 x 1.20 +0.05/0 deep from the rim, over the encoder collar |
| Round relief | Ø6.05 +0.03/0 round bore from 1.20 to 2.20 above the rim, so a round shaft section never meets the bore flat |
| Bore | D-bore Ø6.05 +0.03/0, flat 4.55 +0.03/0 across (from the far side of the bore), from 2.20 to 6.90 above the rim. This is a slip fit on the Bourns shaft (6.0 +0/-0.1, 4.5 +0/-0.1). The bore bottom stays at least 0.35 mm above the shaft tip, so the knob never seats on the tip |
| Retention | One M2 x 0.4 tapped hole square to the flat, centre 3.00 above the rim (+12.10 above the PCB). The cup point lands on the flat between about +11.55 and +12.65, above the highest flat start (+10.80) and below the lowest tip (+14.50). Wall length 3.75 mm. Use an M2 x 3 cup-point set screw (ISO 4029), placed toward the rear. Removing it lets the knob come off for disassembly, which beats the GLYF on serviceability |
| Fitting | Slide a 1.10 +/-0.05 mm fork shim (printed or shim stock, about 12 mm wide with a 6.5 mm slot) between the plinth top and the knob rim. Rest the knob on it under light finger pressure: the slip-fit bore does not load the shaft, so the push switch is not pressed. Tighten the set screw, then pull the shim out. Check that the knob clicks and returns |
| Index | Optional laser-engraved index line, 0.3 mm wide, on the top flat (it shows grey on black anodise) |
| Tolerance and check | Bore after anodise. Anodise grows the bore by about 0.01 to 0.02 mm, so mask it or allow for it (vendor note). First article: fit on a real PEC12R before the batch |

Variant without the set screw (clean side): press-fit D-bore Ø5.97 +0.02/0, flat 4.47 +0.02/0, pressed down onto
the same 1.10 mm shim. The press force must be carried by a support under the shaft end below the PCB, or it
will go through the push switch. The interference on a plastic shaft with a 0.1 mm tolerance band is 0 to
0.13 mm, which is uncertain. Decide on a coupon only.

FDM prototype (Bambu A1 mini, 0.2 mm layers, PETG preferred): the same outline, counterbore and relief, printed
top face down with no supports, fitted on the same 1.10 mm shim. Bore Ø6.20 with three crush ribs reaching to Ø5.90, flat 4.70 with a 0.15 mm rib. Coupon at bore
6.10 / 6.20 / 6.30. Resin version (JLC3DP Black Resin, as for the keycaps): Ø6.05 bore without ribs, plus a
drop of cyanoacrylate if it is loose.

Bought knob: no stocked knob of 10.5 mm diameter and 9.1 mm height with a 6 mm D-bore was identified. Generic
"10 mm aluminium D-shaft knob" listings have no stable part number and were **not checked**. Rejected for lack
of a traceable part.

### 6.6 Round button cap

| Feature | Value |
| --- | --- |
| Visible part | Top face Ø10.30, slightly domed (0.3 mm crown), conical side to a skirt of Ø12.30. 1.00 mm proud of the deck, then a straight Ø12.30 shank through the shell |
| Shell hole | Ø12.50 +0.05/-0 after anodise, 1.50 mm long. The top shell is pocketed from below to +4.70 in a Ø17.0 counterbore around the hole |
| Flange | Ø15.0 x 0.80 mm, top face at +4.45. That leaves a 0.25 mm gap to the shell underside at the nominal switch height, so the cap is captive with 0.25 mm play when the pad is upside down |
| Actuator nub | Ø2.5, from the flange underside down to +3.10, resting on the B3FS plunger (Ø3 flat). The cap rests on the plunger under its own weight and does not preload it |
| Travel | 0.25 +0.2/-0.1 mm to the click (pretravel), then a hard stop on the switch |
| Material | First batch: JLC3DP Black Resin, as for the keycaps. Optional: 6061 black anodised, turned (the same JLCCNC order). FDM prototype: printed top face down, flange and nub up, no supports, flange 4 layers |
| Assembly | The cap drops into the hole from below before the PCB is fitted |

Risk: one central nub under a 12.3 mm cap with 0.1 mm radial clearance in a 1.5 mm hole lets the cap rock
about 7 degrees when pressed at the edge. Check this on a coupon. If it feels poor, lengthen the guide with a
1.0 mm downward ring on the shell underside (hole length 2.5 mm) and lower the flange to suit, or switch to
the 4.3 mm B3FS-1010P with a ring nub.

Footprint: KiCad stock `Button_Switch_SMD:SW_SPST_Omron_B3FS-100xP` and symbol `Switch:SW_Omron_B3FS`. Both
exist; the 3D model was not checked. JLCPCB: extended (`C271750`). The buttons are the only top-side SMD parts.
For 5 units, **hand-solder them** (4 gull-wing pads each). Order top-side assembly only if the PCB step adds
other top-side SMD parts.

## 7. Interfaces and consequences for other subsystems

1. **PCB:** two PEC12R through-hole footprints (project-drawn) and two B3FS-1000P on the top face, at the
   positions in 6.2. Top-side keep-out per encoder: 14.8 x 14.8 mm square (the plinth pocket). Below the PCB, keep 2.0 mm clear under the encoder pins (1.9 mm protrusion; trim to
   1.0 mm after soldering). Encoder push pins 1/2 go to matrix C4 R0/R1, and the button pads to C4 R2/R3, each
   through its own diode (`keys.md`). A/B pins go to P0.28/P0.30 and P0.29/P0.31, with C on GND. Two optional
   unpopulated 10 nF footprints per encoder. Top-side keep-out: nothing taller than 0 mm under the encoder
   bodies (14.8 x 14.8 mm square per encoder) except the encoder itself, and nothing inside Ø15.4 around each
   button except the switch.
2. **Case, CNC top shell:** the knob plinth from 6.3: pockets 14.8 x 14.8 to deck +0.25, roof 1.55, Ø8.40 shaft
   holes, a flat top under each knob rim, and a drawing note that the encoder collar may stand up to 0.70 mm
   above the plinth top inside the hole. Button holes Ø12.50 at X 18.27/36.96, Y 71.20, with the
   Ø17.0 underside counterbore to +4.70. Nothing taller than the deck around the button holes.
3. **USB-C (conflict to resolve in usb-io):** the GLYF places USB-C centred between the knobs (X 27.6 on
   worxpad). The free gap between the encoder bodies is only X 24.47 to 30.76 (6.29 mm), which is narrower
   than a USB-C receptacle (about 8.9 mm). The receptacle must therefore lie wholly behind the encoder bodies
   (Y below 8.2 mm from the rear outer face, with 0.2 mm clearance), for example a mid-mount part in a board
   notch, or it must move sideways. The encoder pin rows at Y 7.6 lie at X 15.8 to 20.8 and 34.5 to 39.5, clear
   of the USB-C span.
4. **Firmware:** `steps = <96>` on each `alps,ec11` node and `triggers-per-rotation = <24>` on the
   `zmk,keymap-sensors` node. No extra power hooks are needed, because the
   encoder rests open.
5. **Power:** the encoders add 0 uA at rest. The B3FS switches are normally open. Nothing changes in
   `mcu-radio.md` section 7.6.
6. **Keycaps and resin order:** add 2 button caps to the JLC3DP resin order. Add 2 knobs to the JLCCNC order.
7. **Assembly:** a 1.10 mm fork shim is a project tool; print it with the coupons (0.2 mm layers do not give
   1.10 mm, so print it at 0.1 mm layers or use 1.10 mm shim stock).

## 8. Risks

1. **JLCPCB stock of the chosen encoder is 28.** If it runs out, use the fallback `C49671241` with a 2.50 mm
   taller knob (deck +14.50). Both share one footprint, so the PCB does not change. Bourns asks for use within
   six months of delivery, so buy for one batch at a time.
2. The PEC12R push force is 610 +/-306 gf, about 6 N, which is firm next to light linear keys. The GLYF's
   force is unknown. Check this on a sample. No lighter push encoder of this height was found.
3. The plinth changes the look from two round bosses to one stadium island. If the owner rejects it, only
   fallback 2 remains (cut EC11E shaft), and it costs deep-sleep current.
4. The collar diameter (about 7.3 mm) is scaled, not printed. Measure it on a sample before the shell is cut;
   the Ø8.40 roof hole and knob counterbore assume 8.0 mm or less.
4a. The knob height depends on the fitting shim. A knob fitted without it lands with its rim on the plinth and
   the push switch cannot travel. The 0.25 mm worst-case rim gap at full travel also assumes the plinth top is
   flat under the rim.
5. The shaft is plastic. A set screw on a plastic flat can creep. Torque it lightly, or move to the
   press-fit variant after the coupon.
6. Bourns does not recommend hand soldering. JLCPCB THT assembly is the planned route. If parts are consigned
   and hand-soldered, keep the iron contact short.
7. The button cap may rock (section 6.6). Coupon first.
8. The USB-C position conflicts with the encoder bodies (section 7, item 3). The usb-io subsystem must resolve it.
9. All GLYF numbers used here are "likely" measurements from renders. No unit was measured.

## 9. Sources

Datasheets and drawings (read):

- Bourns PEC12R: https://www.bourns.com/docs/product-datasheets/pec12r.pdf (URL as cited in the KiCad stock
  footprint description) and the LCSC copy
  https://datasheet.lcsc.com/datasheet/pdf/7028c811ba34d12d818d369fe91bc235.pdf?productCode=C22385080. Cached:
  `research/_cache/rotary-buttons/ds-02/PEC12R.pdf`, `pec12r-hi-4.png`, `pec12r-qot.png`; LCSC copy in `ds-05/pec12r_lcsc.pdf`.
- Bourns PEC11R: LCSC copy
  https://datasheet.lcsc.com/datasheet/pdf/d03351e7540e40c99d70acd6e8986132.pdf?productCode=C143790; cached
  `ds-02/PEC11R.pdf`, `pec11r-4S.png`.
- Bourns PEC11L: cached `ds-02/pec11l.pdf`, `pec11l-2.png` (REV. 04/26).
- Alps EC11E catalogue (Update 2510): cached `ds-01/alps_ec11e_catalog.pdf`, `hi-2.png`, `d2-side.png`.
- Alps EC11 Chinese catalogue (LCSC copy for C361165):
  https://datasheet.lcsc.com/datasheet/pdf/e2bff97de883671230ffbfe4ac480be6.pdf?productCode=C361165; cached `ds-05/ec11e1834403.pdf`.
- Alps EC11J1525402: https://datasheet.lcsc.com/datasheet/pdf/3358ec822187e9212730cac20f8e02d4.pdf?productCode=C209762; cached `ds-05/ec11j.pdf`.
- Alps EC09E1524417: https://datasheet.lcsc.com/datasheet/pdf/0cf8d3ed13a082d8d3c00e613c360f5c.pdf?productCode=C398936; cached `ds-05/ec09e17.pdf`.
- Alps EC12E catalogue (Update 2510): cached `ds-03/alps_ec12e_catalog.pdf`.
- CUI / Same Sky ACZ11 and ACZ09: cached `ds-04/acz11.pdf`, `ds-04/acz09.pdf`.
- Omron B3FS (Chinese edition):
  https://datasheet.lcsc.com/datasheet/pdf/77b034333be1413cfda69a177f4f8355.pdf?productCode=C231324; English edition
  https://omronfs.omron.com/en_US/ecb/products/pdf/en-b3fs.pdf (cited in the KiCad footprint, not downloaded).
  Cached `ds-05/b3fs.pdf`, `b3fs-p-2.png`.
- The 2.6 N SKRPACE010 and 1.6 N TS-1187A figures come from LCSC parameter tables only (`lcsc-03`). Their datasheets were not read.

Availability (live, 2026-11-13): JLCPCB parts API, `research/_cache/rotary-buttons/jlc-01`, `jlc-02`, `jlc-03`;
LCSC product-detail API, `lcsc-01`, `lcsc-02`, `lcsc-03`.

KiCad: `docker run --rm kicad/kicad:10.0.7`, listings of `Rotary_Encoder.pretty` and `Button_Switch_SMD.pretty`
and a grep of `Device.kicad_sym` and `Switch.kicad_sym`.

Project records: `research/raw/geometry.md` 4.4 and 7; `research/raw/regulatory-software.md`;
`research/raw/official-site.md`; `research/raw/social.md`; `research/components/keys.md`;
`research/components/mcu-radio.md`.

## 10. Not checked

1. The GLYF encoder part and the way it gets a 17.7 mm knob top with an EC11-class encoder.
2. The PEC12R collar diameter, the push force and the real switch travel on a sample, and the pocket fit in plan.
3. The KiCad 3D models (not present in the image).
4. Any bought knob part number. PCBWay stock was not checked.
5. The Alps half-pulse rest state was read from the EC12D phase diagram only. For the EC11E, EC11J and EC09E it is
   inferred from the 2:1 ratio.

## 11. Review of revision 1 and what changed

The review was checked against the cached Bourns drawing (`_cache/rotary-buttons/ds-02/pec12r-hi-4.png`), its
text (`_cache/rotary-buttons-sceptic/b1/pec12r.txt`), the Alps EC12D catalogue
(`_cache/rotary-buttons-sceptic/b4/ec12d1524403.txt`) and the JLCPCB search
(`_cache/rotary-buttons-sceptic/b4/jlc_EC12D15_.json`).

| Review point | Verdict | Change |
| --- | --- | --- |
| Push stroke against the collar: 0.8 mm gap against up to 0.8 mm travel | Correct. The general table gives 0.5 +/-0.3 mm; revision 1 quoted only the drawing value | Ø8.40 x 1.20 counterbore; knob rim moved up 0.20 mm to +9.10; worst-case clearances in 6.3 |
| No height datum for the knob | Correct. Seating on the tip would also fail, because its +/-0.5 mm would put the rim on the plinth at full travel | 1.10 mm fitting shim from the plinth top; bore bottom 0.35 mm over the highest tip; round relief under the D-flat |
| Pocket clearance below the body tolerance | Correct | Pocket 14.8 x 14.8 to deck +0.25, roof 1.55, plinth grown to keep 1.3 mm walls |
| Collar top above the plinth top | Correct; with tolerances it is up to 0.70 mm, not 0.10 | Case drawing note; roof hole Ø8.40. The collar diameter is re-scaled to about 7.3 mm (still a guess) |
| Alps EC12D missing | Correct; it does not change the pick | Row added in section 4. The Alps phase diagram confirms the alternating rest state |
| Magnetic option: "driver does not exist" overstated | Correct | Reason reworded: Zephyr `ams_as5600` exists, ZMK needs a delta adapter |
| Thin stock margin | Correct, already noted | Six-month storage limit and pre-order minimum added |
| `triggers-per-rotation` on the wrong node | Correct | Sections 6.1 and 7 name the node for each property |

The review did not cover the fallback knob. Checking it with the same method showed that revision 1 was also
wrong there: deck +12.50 left too little top wall. The fallback knob is now 11.60 mm tall, top at deck +14.50.
