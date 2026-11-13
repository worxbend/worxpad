# Enclosure manufacturing: CNC aluminium for the real unit, FDM for the prototype

Key: `enclosure-manufacturing`. Date of research: 2026-11-13. Status: decision record, revision 2.

Confidence labels: **confirmed** (stated by the maker or vendor, or measured from a primary source),
**likely** (consistent indirect evidence), **guess** (judgement or arithmetic on uncertain inputs).
Cache for this key: `research/_cache/enclosure-manufacturing/01-jlccnc` to `08-prices`.

Revision 2 answers a review of revision 1. The vendor choice stands. The fastening scheme, the RF insert, the
FDM print plan, the lens numbers and several smaller facts were corrected. Section 13 lists every review point
and what was done with it.

Coordinates: X from the **right** outer face (positive inward) for control-column features, as in `mcu-radio.md`
7.3; X from the **left** outer face where stated for key-field features; Y from the rear outer face; Z from the
deck (top face of the top shell), negative downward. Key-relative offsets (x, y) follow `keys.md`: y positive
toward the front.

## 1. Decision in short

1. **Vendor.** Both aluminium shells at **JLCCNC**, 6061-T6, "Bead blasting + Anodizing" in black (Type II),
   appearance level "Strict". Each part is ordered as one STEP plus a **DXF** 2D drawing (JLCCNC takes 2D as DWG
   or DXF), with a PDF copy of the same drawing for reading. PCBWay CNC is the fallback with the same files.
   Xometry and RapidDirect are not used for a batch of five. (decision)
2. **Part breakdown.** Six made parts per unit: top shell (deck, key well, plate, lens recess and web, knob
   plinth, button holes), bottom shell (tray with the wedge), RF window insert (black POM), display lens (per
   `display.md`), two knobs, two button caps. Bought parts: four M2 x 5 and two M2 x 6 countersunk screws, two
   M2 x 4 pan-head screws, four 3M Bumpon SJ5076 feet, insulation sheet. No dock: the GLYF has none
   (`research/raw/geometry.md`). (decision)
3. **Fastening (changed).** Three screw groups, section 6.4:
   - **K1 to K4, from the top, GLYF style.** M2 x 5 countersunk screws sit flush in the plate between key columns
     1-2 and 3-4, in the gap between keycaps, and thread into posts that rise from the bottom-shell floor through
     the PCB. The thread is in the thick wedge floor, so length and drill-point margin are no longer tight.
   - **C1, C2, from below** in the control column, at the right rear and right front corners, into blind tapped
     posts of the top shell. They clamp the right side, where the RF insert sits.
   - **G1, G2, PCB to top shell.** M2 x 4 pan-head screws through plated GND holes into short top-shell posts.
     They bond the case to ground (the K and C screws do not touch PCB copper) and fix the PCB height at the
     control column.
4. **Radio exit.** Keep the settled `mcu-radio.md` solution: a slot in the right wall of the bottom shell, closed
   by a non-metal insert. Revision 2 makes it the **30 mm slot (Y 38 to 68)**, ends the flank scoops by Y 35 so
   the slot has wall under it, and holds the insert by two round keys in the slot ends instead of an inner flange
   that collided with the PCB edge (section 7). A plastic bottom shell remains the second fallback.
5. **Prototype.** Bambu Lab A1 mini (confirmed from the siblings), PETG, 0.2 mm layers. The top shell prints
   split face down with nothing below the split plane, because the K posts now belong to the bottom shell. The
   bottom shell prints as a flat tray with the wedge as a separate bar. JLC3DP MJF PA12 is the option for a
   stiffer second prototype. (decision)
6. **Expected cost** (guess, section 9): about USD 200 to 350 for one complete case set and about USD 560 to
   1,030 for five sets (USD 110 to 205 per set), shipping included, after JLCCNC's May 2026 price rise. **No live
   quote exists**; it needs an account and the STEP files.

## 2. Context

- The GLYF case is two CNC 6061 shells, bead-blasted and black anodised, split 5.0 mm below the top face, four
  M2-class screws from the top through the key-well floor hidden under keycaps, a wedge machined into the bottom
  shell, and moulded silicone stadium feet (`research/raw/geometry.md`, `youtube.md`, `social.md`; likely).
- Settled earlier: body 128.4 x 85.2 mm, PCB 120.5 mm wide, PCB bottom face at Z -7.80, RF bay and right-wall
  slot (`mcu-radio.md` 7.3); plate in the top shell, lip 1.15 +/-0.05 mm and openings 14.00 +0.05/-0 mm after
  anodising, plate top 4.00 mm below the deck, nothing taller than 0.25 mm on the plate top under a cap, "so
  screw heads are flush or recessed" (`keys.md`).
- Later records that set case numbers: `display.md` (lens, recess, web), `rotary-buttons.md` (knob plinth,
  button holes and counterbores), `usb-io.md` (USB-C opening, case bonding to GND), `power.md` (battery pocket,
  slide-switch aperture).
- Body profile used for every underside value below (`geometry.md`, likely): thickness 12.0 mm at the rear face,
  19.2 mm at the wedge apex 12.7 mm from the rear face (rear slope 29 degrees to the top face), then a 4.95 degree
  ramp to 13.0 mm at the front face (0.0855 mm per mm). Flank scoops 13 mm wide per side keep the underside at
  Z -11.7 to -12.0 near the rear corners.
- Family conventions: one build123d model with `print` and `cnc` variants, M2 screws, ISO 2768-m on drawings,
  internal corners checked against JLCCNC's depth rule, fit coupons first (`research/raw/conventions.md` 3.5, 3.6,
  5).

## 3. Requirements

| # | Requirement | Source |
| --- | --- | --- |
| R1 | Two-shell aluminium body, black, bead-blasted, slim, GLYF look | Task; `geometry.md` |
| R2 | Plate integral with the top shell; lip and openings as in `keys.md` after anodising | `keys.md` |
| R3 | Nothing taller than 0.25 mm on the plate top inside a cap footprint; screw heads flush or recessed | `keys.md` 6.3 |
| R4 | RF bay free of metal, screws and bosses; right-wall slot with a non-metal insert | `mcu-radio.md` A4 to A9 |
| R5 | Support under the hot-swap sockets during switch insertion (up to 3.0 kgf each) | `keys.md` |
| R6 | Case bonded to PCB ground for ESD | `usb-io.md` 4.4, 6.3 |
| R7 | Batch of 5 units; the same files must work at a second vendor | Task |
| R8 | FDM prototype on a 180 x 180 x 180 mm bed with the same geometry where possible | Task; `conventions.md` 5.1 |
| R9 | Each fact sourced; no vendor artwork copied | Task |

## 4. CNC vendors

### 4.1 Candidates

| Vendor | Upload and drawings | Materials | Tolerance | Finishes and masking | Lead time | Size limits | Source, confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **JLCCNC** (jlccnc.com, the CNC arm of JLCPCB) | "JLCCNC accepts 3D files in STEP format and 2D drawings in DWG or DXF format"; 2D required for threads, tolerances, laser marking or UV printing. One part per STEP (owner's notes). One blogger's PDF drawing was accepted, but DXF is the stated format. | 6061-T6, 7075, plus POM, PC, ABS, FR4, PMMA, PA6, Bakelite | ISO 2768-m default; +/-0.1, +/-0.05, down to +/-0.02 on drawing | As machined, bead blasting, brushing, anodizing, hardcoat, conductive anodizing, UV printing, laser marking, polishing. During anodising "protective rubber plugs will be used, and threaded holes below M5 will not undergo anodizing treatment". Other bare areas by post-machining or laser removal. Racking points on non-cosmetic faces at "Strict". | From 3 business days | Up to 950 x 560 x 120 mm (3-axis), min 5 x 5 x 1 mm | `_cache/enclosure-manufacturing/01-jlccnc/cap.html`, `jlccnc.com_help_article_appearance-standard-guidelines.html`, `electroplating-vs-anodizing.html`, `jlccnc.com_help_article_CNC-Machining-Design-Guideline.html`; confirmed (re-read 2026-11-13) |
| **PCBWay CNC** | STEP, IGES, IGS, SLDPRT, X_T; STL refused for CNC. "3D file and options take priority over your technical drawing". | 6061, 7075 and many more | ISO 2768-1 unless a drawing says otherwise; +/-0.125 mm up to 300 mm; down to +/-0.01 mm on drawing | "Bead blast + Anodized color", hard anodizing Type III and others; colour may vary between batches | "As fast as 2 days"; a sponsored keyboard case took about 7 days | Max 1000 mm, min 2 mm | `03-vendors/www.pcbway.com_rapid-prototyping_cnc-machining_.html`, `..._manufacture__type_2.html`; `02-community/beekeeb.html`; confirmed |
| **Xometry** | Instant quote from CAD; drawings for GD&T | Wide | +/-0.127 mm metals per ISO 2768 unless specified | Type II or III anodize (MIL-A-8625), bead blast | 3 to 7 business days | 2,032 x 1,219 x 610 mm | `03-vendors/www.xometry.com_capabilities_cnc-machining-service_.html`; confirmed. US-centric; free shipping only inside the US |
| **RapidDirect** | Instant quote; drawings for GD&T | Wide | ISO 2768-m metals, ISO 2768-c plastics | Anodizing, sand blasting and others | About 5 to 8 business days per material | Milling 4000 x 1500 x 600 mm; min wall 0.5 mm | `03-vendors/www.rapiddirect.com_services_cnc-machining_.html`; confirmed |
| Keyboard-scene small shops (bestcreating.com, a geekhack group-buy machinist) | E-mail quote | 6061 | Not stated | Anodised | Not stated | Not stated | `02-community/jorne-wiki-cases.html` (Corne case about USD 200 each, USD 800 for 10); likely |

### 4.2 Price examples found (all before or around the May 2026 price change; none is for this part)

| Example | Vendor | Price | Source, confidence |
| --- | --- | --- | --- |
| One-piece tray-mount keyboard case, 6061, bead blast + anodise | JLCPCB CNC (now JLCCNC), 2023 | "under USD 100 including shipping" | `02-community/note-copkbd.html`; confirmed for that order |
| Same author: bead blast + anodise added about USD 9 to an about USD 90 part; hardcoat about USD 18 | JLCPCB CNC | as stated | search summary of the same article; likely |
| Brass weight: fillet 2.5 mm quoted just under USD 30 and 5 days; fillet 2.25 mm about USD 10 more and 2 more days | JLCPCB CNC | as stated | `note-copkbd.html`; confirmed |
| Engraving inside a deep case floor quoted about USD 10 more than outside | JLCPCB CNC | as stated | `note-copkbd.html`; confirmed |
| daditto case, anodised dark grey | JLCPCB CNC | "under USD 100.00 including shipping" | `02-community/green-keys.html`; confirmed |
| Corne v3 aluminium case | JLCCNC | USD 139.95 without shipping | `02-community/jorne-wiki-cases.html` (link to r/crkbd post); likely |
| Ergonaut One, two upper halves | JLCPCB CNC, 2024 | about USD 130 | `02-community/jorne-wiki-cases.html`; likely |
| JLCCNC price increase from 2026-05-08: aluminium +20 %; further changes may go online without notice | JLCCNC | n/a | `01-jlccnc/price-adjust-2026-05.html`; confirmed |

**No live price for the worxpad shells was obtained.** A JLCCNC or PCBWay quote needs an account and the STEP
files, which do not exist yet. Every case cost in this record is a guess scaled from the rows above.

### 4.3 Vendor decision

JLCCNC is chosen: lowest community-reported prices for keyboard cases, the family's order packages already target
it (`worxboard/case/production/jlccnc`), and the same company makes the PCB. PCBWay CNC is the fallback with the
same STEP and DXF. Xometry and RapidDirect are rejected for this batch: no keyboard-community order reports were
found, and US-centric shipping (Xometry) and industrial quoting give no advantage for five units; their prices
were not compared live (guess on cost). 7075 is rejected: JLCCNC lists 6061-T6 at tensile 290 MPa and 7075 at
560 MPa, but this case is limited by stiffness, tool access and finish, not strength; 7075 costs more and
anodises less evenly (JLCCNC keyboard-case blog: "6061-T6 is usually the sensible starting point";
`01-jlccnc/jlccnc.com_blog_custom-keyboard-case.html`, confirmed).

## 5. Design rules for cheap, good parts (JLCCNC)

| Topic | Rule for worxpad | Source, confidence |
| --- | --- | --- |
| Internal corner radius | R = H/10 + 0.5 mm, tool D = H/5; R 0.5 only at depth 3 mm or less. JLCCNC's table: tool Ø2.0 reaches 10 mm with min R 1.5; Ø3.0 reaches 15 mm, R 2.0; Ø4.0 reaches 20 mm, R 2.5. Use **R 1.5 or more** in pockets up to 10 mm deep, R 2.0 to 15 mm. | `01-jlccnc/...CNC-Machining-Design-Guideline.html`; confirmed |
| Fillet cost | A 1 mm change of a fillet did not change a quote; going below the tool radius (R 2.5 to R 2.25) added about USD 10 and 2 days. Avoid radii just below a standard tool radius. | `note-copkbd.html`; confirmed |
| Pocket depth | Best at 2 to 3 x tool diameter; above 5 x needs special tools. Key well 4.0 mm and the plate openings are fine with a Ø2 tool. The RF-insert key reliefs (Ø2.0 x 6.7 mm) are 3.35 x D. | design guideline; confirmed |
| Wall and floor | Metal walls: "recommended wall thickness of metal parts should be 0.8 mm (absolute minimum 0.5 mm)". Bead blasting: "recommended to increase the wall thickness to above 1.5 mm, or alternatively select a process without sandblasting". Plastic: 1.5 mm recommended, 1.0 absolute. The plate lip (1.15 mm, `keys.md`) and the display web (0.60 mm, `display.md`) are below the bead-blast advice; see risks 1 and 2. Floors 2.0 mm at each countersink. | design guideline; appearance guideline; confirmed |
| Threads | Model the tap-drill hole with its 118-degree point (adds 0.48 mm for Ø1.6). M2 x 0.4: drill 1.6; M2.5 x 0.45: drill 2.05. Thread length at most 3 x D; in blind holes keep at least D/2 (1.0 mm for M2) unthreaded between the last full thread and the drill shoulder. Keep **at least 2.0 mm of metal beyond the drill point** (JLCCNC support to copkbd: "it would be better to have a margin of at least 2mm", where 1.2 mm was the case). Call out full-thread depth and drill depth, for example "M2x0.4-6H, full thread 4.8, drill Ø1.6 x 5.8". Every tapped hole in section 6.4 is checked against these rules. | design guideline; `02-community/copkbd.txt` lines 155 and 273; confirmed |
| Thread finish | Threads below M5 are plugged and not anodised (bare aluminium). No re-tap needed. | appearance guideline; confirmed |
| Countersinks | DIN 7991 M2: head Ø4.0 (d2), head height 1.2 max (k), hex 1.25. ISO 10642 starts at M3, so only DIN 7991 applies at M2. Countersink Ø4.30 x 90 degrees: the head sits (4.30 - 4.00)/2 = 0.15 mm below the surface, up to 0.30 mm for a 3.7 mm head. Material under the cone at least 0.8 mm. On a sloped face (the 4.95 degree ramp) the countersink axis stays square to the deck and is cut 0.20 mm deeper, so the head is 0.05 to 0.40 mm below the surface all round. | https://boltsparts.github.io/en/parts/standards/DIN7991.html (fetched 2026-11-13); confirmed; arithmetic |
| Undercuts | None. Every side opening (USB-C, power switch, RF slot) is a notch cut from the split face, and the RF key reliefs are vertical holes from the split face. A stadium-shaped side opening seen from the side needs a third setup or 5-axis; accept a rectangle with R corners and a 0.3 mm chamfer, or pay for it. | design rule (guess on cost) |
| Setups | Top shell: A deck side (deck, plinth, key well, plate top, countersinks, lens recess, holes, top chamfer); B underside (plate underside, cavities, RF pocket over the bay, C and G posts, split face, notches). Bottom shell: A cavity side (floor, K posts, ribs, notches, RF key reliefs, battery pocket); B underside (wedge, ramp, scoops, foot pockets, C countersinks, laser-mark area). | `conventions.md` 5.3 (macropad: 3-axis, two setups per shell); likely |
| Sloped faces | The wedge rear slope and the 4.95 degree ramp need surfacing or a tilted setup and are the main cost driver of the bottom shell. Keep each one a single plane, with 45-degree chamfers instead of blends. | guess |
| Chamfers and fillets | 45-degree chamfers (GLYF top edge 1.0, bottom 0.4) with a chamfer mill are cheap. Outer vertical corner radius (GLYF R2) is free. 3D blends and variable fillets on outer edges need ball-mill surfacing. Model every chamfer in the STEP: JLCCNC told copkbd to put even a C0.2 edge break in the 3D data. | `note-copkbd.html`; guess on cost |
| Engraving | Laser marking on black anodise is cheap and needs a 2D artwork file; milled engraving inside deep cavities costs more (about USD 10 in one quote). Put serial and project marks on the outer underside by laser. | cap.html FAQ; `note-copkbd.html`; confirmed |
| Switch cut-outs | Dimension **after anodising**: 14.00 +0.05/-0. Machine 14.03 +/-0.02 before anodising. Dog-bone reliefs for a Ø2.0 tool (relief Ø2.1, webs 4.6 mm at the reliefs per `keys.md`). Mark them FIT-CRITICAL on the drawing; the rest ISO 2768-m. | `keys.md`; `conventions.md` 5.3; arithmetic |
| Anodise build-up | Typical thickness: decorative 5 to 10 um, standard Type II 10 to 25 um, heavy Type II 25 to 50 um, Type III 25 to 100+ um. About half grows outward ("50/50 rule", not guaranteed). Type II shrinks a hole by about 10 to 25 um on diameter. Fits with 0.1 mm clearance or more need no correction; only the switch openings and the lip are compensated. | `01-jlccnc/jlccnc.com_blog_sulfuric-acid-anodizing.html`, `electroplating-vs-anodizing.html`; confirmed |
| Flatness | No flatness callout by default. Split faces may bow after pocketing; a gap at the seam is the symptom. If the first parts show it, call out flatness 0.1 on the split faces only (cost not checked). | guess |
| Appearance | "Strict": no tool marks after bead blast + anodise, minor scratches 5 mm and below (at most 2), no visible colour variation inside a batch. State cosmetic faces and allowed racking-point locations (inner cavity faces) on the drawing. | appearance guideline; confirmed |
| Bare metal and grounding | Anodise insulates. Bare areas come from (a) tapped holes below M5 (plugged, so bare) and (b) laser or CNC removal of a marked area after anodising. **A bare thread grounds a shell only if the screw in it also touches PCB ground.** The K and C screws pass through copper-free NPTH holes and their heads sit in anodised countersinks, so they do not ground anything. Grounding is done by G1 and G2 (section 6.4, item 3). | `electroplating-vs-anodizing.html`; appearance guideline; confirmed for the process, arithmetic for the path |
| Hanging points | Add a non-functional hole or face for racking on each shell, inside the cavity, so marks stay hidden. | surface-treatment help article; confirmed |

## 6. Case part breakdown and the numbers the design needs

### 6.1 Z levels (deck = 0, down is negative)

| Level | Z (mm) | Source |
| --- | --- | --- |
| Plate top | -4.00 | `keys.md` |
| Split plane (top shell / bottom shell) | -5.00 | `geometry.md` 4.2; `mcu-radio.md` A9 |
| Plate (lip) underside, CNC | -5.15 (lip 1.15) | `keys.md` |
| PCB top / bottom | -6.20 / -7.80 | `keys.md`, `mcu-radio.md` |
| Socket underside | -9.65 | `keys.md` |
| Floor top under sockets (0.3 mm clear) | -9.95 | `keys.md` |
| Underside: rear face / wedge apex (Y 12.7) / front face | -12.0 / -19.2 / -13.0 | `geometry.md` |
| Underside in a flank scoop | -12.0 (ends by Y 35, section 7.3) | `geometry.md`, this record |
| RF bay | -2.80 to -13.30 | `mcu-radio.md` A5 |

The plate underside lies 0.15 mm below the split plane. The bottom-shell wall therefore stays 0.3 mm or more
outboard of the plate edge at its top, or the top 0.5 mm of the bottom wall is thinned to 3.0 mm (top wall 3.5
mm). (decision, arithmetic)

### 6.2 Made parts

| Part | Material and finish | Vendor | Notes |
| --- | --- | --- | --- |
| Top shell | 6061-T6, bead blast + black anodise Type II, Strict | JLCCNC (PCBWay CNC) | Deck, knob plinth (`rotary-buttons.md`), key well (corner R 1.5 or more), plate with 16 openings and 4 flush countersinks (K1 to K4), lens recess and web (`display.md`), button holes and counterbores, RF pocket over the bay to Z -2.80 (A7), C1 and C2 tapped posts, G1 and G2 tapped posts with bare end faces, upper halves of the USB-C notch if any. Stock about 8 to 10 mm. |
| Bottom shell | same | JLCCNC (PCBWay CNC) | Tray, wedge and ramp, flank scoops ending by Y 35, K1 to K4 tapped posts, socket support ribs (`keys.md`: 0.2 to 0.4 mm below socket undersides), battery pocket (`power.md`, see 6.6), C1 and C2 countersinks in 2.0 mm local floor, four foot pockets, RF slot notch with two key reliefs, USB-C and slide-switch apertures (`usb-io.md`, `power.md`), reset pinhole, laser-mark area. |
| RF window insert | Black POM (Delrin), as machined | JLCCNC (same order); MJF PA12 black at JLC3DP as alternative | Section 7.2. |
| Display lens | Per `display.md`: 1.0 mm clear cast PMMA, laser cut, 31.2 mm square, R2.0 corners, underside painted black with a 24.4 mm window ablated | Laser-cutting service, or JLCCNC PMMA with UV printing (1.5 mm minimum plastic wall there, so CNC is the fallback only) | Recess 31.4 mm square, R2.1, 1.15 mm deep; web 0.60 mm with a 24.8 mm window (risk 2). The display record owns these numbers. |
| Knobs (2) | 6061-T6, CNC turned, bead blast + black anodise | JLCCNC (CNC turning), same anodise batch | Outline, D-bore and M2 set screw per `rotary-buttons.md`. |
| Button caps (2) | JLC Black resin (SLA) | JLC3DP, with the keycaps (`keys.md`) | Per `rotary-buttons.md`. |

### 6.3 Bought parts

| Part | Spec | Qty per unit | Where | Status |
| --- | --- | --- | --- | --- |
| K screws | M2 x 0.4 x 5, DIN 7991 countersunk hex socket, A2 stainless black or 10.9 steel black | 4 | Accu-Components SSK-M2-5-A2 (plain A2), Aspen Fasteners DIN 7991 black, or any shop | Listings found by search; stock not confirmed |
| C screws | M2 x 0.4 x 6, DIN 7991, as above | 2 | same | stock not confirmed |
| G screws | M2 x 0.4 x 4, ISO 7045 pan head (dk 4.0, k 1.6) or ISO 14583 Torx pan head, A2 or zinc-plated steel (must conduct; no black oxide coating under the head is needed but plain finish is preferred) | 2 | any | stock not confirmed |
| Feet | 3M Bumpon SJ5076, black polyurethane, Ø8.00 x 2.79 mm, flat top | 4 (pack of 56 covers 14 units) | DigiKey 570288 | **Active, 1,222,328 in stock, 56 at USD 0.12839 = USD 7.19** (DigiKey page read 2026-11-13); confirmed |
| Insulation | Polyimide or PET, 0.3 mm over the socket bodies at the battery pocket (`power.md` 5.2) | 1 sheet | any | Battery record sets it |
| Heat-set inserts (FDM only) | CNC Kitchen M2 x 3.0, OD 3.6, hole 3.2, min wall 1.3 mm | 2 (C1, C2) plus 2 (G1, G2, optional) | Würth eShop 4954617301 or 3DJake | Specs from the Würth listing via search; stock not confirmed |

None of these hardware items is in the JLCPCB assembly library with stock: keyword searches for M2 screws,
inserts, rubber or silicone feet and Bumpon returned 0 stock or no records (`_cache/enclosure-manufacturing/
04-jlc-parts/*.json`, confirmed). They are bought separately and fitted by hand.

### 6.4 Fastening scheme (revision 2)

Screw-reach arithmetic used throughout: a DIN 7991 M2 head (d2 4.0 max, k 1.2 max) in a Ø4.30 x 90 degree
countersink sits 0.15 to 0.30 mm below the surface; the screw tip lies one nominal length (+/-0.15 mm assumed
length tolerance) from the head top. Every tapped hole below keeps the screw tip at least 0.4 mm short of the last
full thread, D/2 = 1.0 mm unthreaded to the drill shoulder, and 2.0 mm or more of metal beyond the drill point.

**1. K1 to K4: from the top, into bottom-shell posts.**

- Positions: on the key-column boundaries 1-2 and 3-4 (X 23.5 and 61.6 from the left outer face), at y = -3.0
  from the key centre of the rear row (K1, K2: Y 11.0) and of the front row (K3, K4: Y 68.2). y = -3.0 is the only
  window on the boundary that keeps the countersink clear of the dog-bone reliefs at the opening corners
  (y = +/-7) and the post clear of the right-hand key's socket zone (y +1.0 and beyond).
- Top shell: Ø4.30 x 90 degree countersink from the plate top and a Ø2.20 clearance hole. The cone reaches Ø2.20 at
  Z -5.05, inside the 1.15 mm lip; the post below supports the remaining 0.10 mm. The countersink edge (X 7.375 to
  11.675 from the left key centre) leaves 0.375 mm of plate top to each neighbouring opening (openings end at 7.00
  and 12.05); that strip lies under the switch flanges (15.0 mm square). Head top 0.15 to 0.30 mm below the plate
  top, so R3 holds. It sits in the 0.85 mm gap between keycaps, as on the GLYF.
- Bottom shell: post Ø3.6 rising from the floor through a PCB NPTH Ø4.0 to Z -5.20 +0/-0.05 (0.05 to 0.10 mm
  below the plate underside), so the perimeter seam closes first and the screw then pulls the plate down by at most
  0.10 mm at the post. Mark the post top and the split faces FIT on the drawing.
- Thread: M2 x 0.4, full thread 4.8 mm from the post top (to Z -10.00), drill Ø1.6 to Z -11.00 at the shoulder,
  point to Z -11.48.
- Screw M2 x 5: head top Z -4.15 to -4.30, tip Z -9.15 to -9.45. Engagement 3.95 to 4.25 mm (2 x D); the tip stays
  0.55 mm or more short of the last full thread. Metal under the drill point: underside at Y 68.2 is Z -14.45
  (ramp), leaving 2.97 mm; at Y 11.0 it is Z -18.24 (rear slope), leaving 6.76 mm.
- The underside stays free of K screws, so the wedge and ramp carry no screw heads, as on the GLYF.

**2. C1 and C2: from below, into top-shell posts.**

| | C1 | C2 |
| --- | --- | --- |
| Position (X from right face, Y) | 7.5, 12.0 (right flank scoop) | 7.5, 77.0 (ramp) |
| Underside at the screw | Z -12.00, flat | Z -13.70, 4.95 degree face; countersink 0.20 mm deeper |
| Local floor and floor top | 2.0 mm, Z -10.00 | 2.0 mm along the axis, Z -11.70 |
| Top-shell post | Ø3.6, from the split plane to Z -9.95 (0.05 above the floor top) | Ø3.6, to Z -11.65 |
| Thread | full 4.8 from the post end (to Z -5.15); drill shoulder Z -4.15, point Z -3.67 | full 4.8 (to Z -6.85); drill shoulder Z -5.85, point Z -5.37 |
| Metal beyond the drill point (to the deck) | 3.67 mm | 5.37 mm |
| Screw | M2 x 6: head top Z -11.70 to -11.85, tip Z -5.55 to -6.00 | M2 x 6: head top about Z -13.30 to -13.45, tip Z -7.15 to -7.60 |
| Engagement, margin to last full thread | 3.95 to 4.40 mm, 0.40 mm or more | 4.05 to 4.50 mm, 0.30 to 0.75 mm |
| PCB | NPTH Ø4.0, keep-out Ø4.6 both faces; the hole edge is 1.55 mm from the board edge (X 3.95) | same |
| Clearances | Right encoder body starts X 12.07, pin row at Y 7.60 from X 15.77 (`rotary-buttons.md` 6.1): 2.3 mm or more | Button-1 counterbore Ø17 at (18.27, 71.20) starts X 9.77: 1.27 mm from the thread major diameter. Bay ends Y 63.1 and the slot Y 68: 9 mm |

**3. G1 and G2: PCB to top shell, case ground.**

- Positions: G1 at X 7.5, Y 32.0 (between the right encoder and the RF bay, outside the lens at X 11.9); G2 at
  X 7.5, Y 70.0 (between the bay end at Y 63.1 and C2). Both lie outside the RF bay (A6).
- Top shell: post Ø4.6 from the split plane down to Z -6.20 (the PCB top), end face **bare**: laser-cleared or
  face-milled after anodising, stated on the drawing. Thread M2 full 2.7 mm from the post end (to Z -3.50), drill
  shoulder Z -2.50, point Z -2.02: 2.02 mm to the deck.
- PCB: plated hole Ø2.20, exposed GND ring Ø4.6 on both faces (as `usb-io.md` 6.3 item 2 asks), stitched to the
  ground plane.
- Screw M2 x 4 pan head from below: the head (dk 4.0, k 1.6) bears on the bottom GND ring, the tip reaches
  Z -3.80, engagement 2.4 mm (1.2 x D; it only holds the PCB). The head bottom is at Z -9.40, so the floor top at
  G1 and G2 must be at Z -9.70 or lower (it is: the floor there is under the 14 to 17 mm thick part of the body).
- Ground paths: PCB GND ring to the bare post face, and PCB GND ring to screw head to screw to the bare (plugged)
  thread. The bottom shell is bonded only through the anodic film: a Type II layer of 10 to 25 um breaks down at
  a few hundred volts (guess from typical dielectric strength), so an 8 kV discharge to the bottom shell crosses
  at the C screw heads or the seam into the top shell and reaches GND through G1 and G2 (likely). No part at
  JLCPCB is needed, which keeps `usb-io.md`'s "no part, one machining note" choice.
- The G posts also set the PCB top at Z -6.20 at the control column, consistent with `keys.md` (PCB top 2.20 +/-0.1
  below the plate top).

**4. PCB demands from the fastening.**

- K1 to K4: NPTH Ø4.0, keep-out Ø4.6 on the top face. On the bottom face, keep-out **Ø6.6** (the FDM boss of 8.2 is
  Ø6.0 and the board is shared). For the four keys to the right of K1 to K4, the diode and its pads therefore stay
  at x -6.2 or more (relative to that key). Margins on the bottom face, arithmetic: left key third-leg circle 0.21
  mm, right key socket zone (y +1.0) 0.70 mm, right key pad solder access 1.5 mm. This is a request to the PCB
  layout, not an override of `keys.md`; the diode band rule there (x -9.0 to +3.0) already allows x -6.2 to +3.0.
- C1, C2: NPTH Ø4.0, keep-out Ø4.6 both faces.
- G1, G2: plated Ø2.2, GND ring Ø4.6 both faces, keep-out Ø5.2 on the top face around the Ø4.6 post.

### 6.5 Interfaces this record demands

| To | Demand |
| --- | --- |
| PCB | Holes and keep-outs of 6.4 item 4. Board outline 0.45 mm or more from the inner wall (cavity 128.4 - 2 x 3.5 = 121.4 against 120.5 PCB). No bottom-side part within 1.0 mm of the board edge along the RF slot is needed any more (the insert has no inner flange). |
| Keys | Plate lip 1.15 mm is below JLCCNC's 1.5 mm bead-blast advice (risk 1). The K countersinks leave 0.375 mm of plate top beside two openings each, under the switch flanges. |
| MCU-radio | Split plane at Z -5.00; slot Y 38 to 68 (30 mm) from Z -5.00 to -11.70 in the bottom shell; insert per 7.2. Flank scoops end by Y 35. No screw, post or boss in the bay. |
| USB-IO | Case bonding by G1 and G2 (6.4 item 3) instead of plated holes at the case screws. USB-C and slide-switch apertures are notches or rectangles with R corners; a stadium outline seen from the rear costs a third setup. |
| Display | Recess 31.4 mm square, R2.1, 1.15 mm deep; web 0.60 mm with 24.8 mm window; module pocket per `display.md` 6.5 with R 1.0 corners or reliefs. Request: a 0.80 mm web (risk 2). |
| Power | Battery pocket against the wedge profile: see 6.6. K1 and K2 posts at Y 11.0 need the pocket outline to clear Ø6.6 around them. |
| Rotary-buttons | Knob plinth and counterbores as specified there; C1, C2, G1, G2 keep 1.2 mm or more from them. |
| Geometry / CAD | Underside: wedge and ramp as planar faces; scoops end by Y 35; four Ø8.4 x 0.8 mm foot pockets (SJ5076, 2.79 mm tall, about 2.0 mm proud like the GLYF foot). |

### 6.6 Check of the battery pocket against the wedge (requested by `power.md` 5.2)

`power.md` asks for a 45.0 x 66.0 mm pocket (long side along X) with its floor top at Z -15.95 (5.0 mm cells)
or -15.18 (4.3 mm cells) and a 1.5 mm floor, so an underside at Z -17.45 or -16.68 over the whole pocket. With the
GLYF profile of section 2 (likely):

| Cell class | Underside needed | Y range where the body is thick enough | Span | Pocket needs |
| --- | --- | --- | --- | --- |
| 5.0 mm | Z -17.45 | Y 9.6 to 33.2 | 23.6 mm | 45.0 mm |
| 4.3 mm | Z -16.68 | Y 8.3 to 42.2 | 33.9 mm | 45.0 mm |

**Conflict, reported, not resolved here:** the pocket does not fit the GLYF wedge in Y by 11 to 21 mm. Options
for the power and geometry owners: a cell of 31 mm or less in Y (lower capacity); a body about 1.1 mm thicker at
the front of the pocket (the 4.3 mm class then fits Y 9.5 to 54.5); or a pocket floor of 1.0 mm (bead-blast
deformation risk on a 45 x 66 mm floor). The K1 and K2 posts at Y 11.0 also sit at the rear edge of any such
pocket and need a Ø6.6 clearance.

## 7. Radio exit through the case

### 7.1 Candidates

| Option | Numbers | Assessment |
| --- | --- | --- |
| **Plastic insert in a right-wall slot** (settled) | Slot 30 mm (Y 38 to 68), Z -5.00 to -11.70, notch from the split face | Chosen in `mcu-radio.md` (rank 1 in `follow-rf-exit-in-aluminium.md`; Keychron Q1 Pro uses a plastic insert in the rear wall). Keeps the aluminium look; the top shell closes the notch; no undercut. |
| FR4 bottom plate ordered with the PCB at JLCPCB | 1.6 mm FR4, black mask, 128 x 85 mm; FR4 dielectric constant up to 5.5 at 1 MHz per JLCCNC's FR4 page | Rejected as a fallback for this body: the wedge, ramp, feet and battery pocket all live in the bottom shell, and a flat 1.6 mm plate loses them. Price not checked. |
| Plastic (or printed) bottom shell with aluminium top | Same outline as the CNC bottom shell, MJF PA12 or POM | Second fallback in `mcu-radio.md`; no board change. Cheaper bottom part, weaker look and feel. |
| Display lens as the window | Lens 31.2 mm square on the top face | Rejected: the lens sits over the LCD's metal frame and backlight, and `mcu-radio.md` A4 keeps the LCD 9.4 mm or more from the bay. The antenna is on the PCB bottom, 4.85 mm below the LCD back. |

### 7.2 Insert design (decision, revised)

1. Material black POM, machined at JLCCNC in the same order. POM is on JLCCNC's plastic list; plastic walls 1.5
   mm recommended, 1.0 absolute. Alternatives: PC (JLCCNC) or MJF PA12 dyed black (JLC3DP, tolerance +/-0.3 mm).
   No metallic paint or plating (`mcu-radio.md` A9).
2. Slot in the bottom-shell right wall: Y 38.00 to 68.00 (+0.10/0), through the 3.5 mm wall, from the split face
   down to Z -11.70. At each slot end a vertical Ø2.00 relief is drilled or milled from the split face, centred on
   the end face at 1.75 mm from the outer face, 6.7 mm deep (3.35 x D). Each relief makes a half-round recess 1.0
   mm deep in the end face.
3. Insert: a bar 29.90 mm long, 3.45 mm thick (outer face flush with the wall, inner face 0.05 mm short of the inner
   wall plane), 6.65 mm tall, with a Ø1.90 half-round key on each end that
   drops into the reliefs. It slides in from above before the top shell goes on; the keys lock it against
   in-and-out movement in both directions, and the top shell closes it from above. Nothing projects into the
   cavity, so it cannot meet the PCB edge (0.45 mm from the inner wall), which was the fault of revision 1's inner
   flange. No glue, no fastener.
4. Antenna pocket: from the inner face, 14.2 mm long (the 10.2 mm strip plus 2.0 mm each side) centred on Y 53,
   from Z -6.00 to -10.50, leaving a 1.45 mm outer skin. Air from the antenna end to the plastic: 0.45 mm board
   edge gap + 0 to 0.2 mm antenna inset + 2.0 mm pocket = 2.45 to 2.65 mm (arithmetic; the detuning effect of POM
   at this distance was not quantified, risk 4).
5. The top-shell wall above the slot (Z 0 to -5.00) stays metal: `mcu-radio.md` A9 sets the window from Z -5.20
   down. If the acceptance test in `mcu-radio.md` 7.3.4 falls short, the next step is to notch the top-shell wall
   over Y 42.9 to 63.1 up to Z -2.80 (A7 level) and make the insert stepped; that needs no change to the PCB.
6. The FDM prototype cannot test this (all plastic). The foil-tape pre-test and the acceptance test in
   `mcu-radio.md` 7.3.4 apply.

### 7.3 Right flank scoop and the slot

The GLYF flank scoops are 13 mm wide per side and keep the underside at Z -11.7 to -12.0 back to about Y 43
(+/-3) (`geometry.md` line 218). A slot bottom at Z -11.70 inside the scoop would leave 0 to 0.3 mm of wall under
it. Decision: the **30 mm slot** (Y 38 to 68, centred on the module at Y 53) and **both flank scoops reach the full
ramp depth by Y 35** (left side too, for symmetry). At Y 38 the ramp underside is Z -17.0, so 5.3 mm of wall
stays below the slot end; at Y 68 it is Z -14.47, leaving 2.77 mm. The 40 mm slot (Y 33 to 73) is dropped: it
would need the scoops to end by Y 30. The visual change is a scoop about 8 mm shorter than the GLYF's. (decision;
arithmetic on likely geometry)

The bay floor rule A8 (floor top at Z -13.30 or lower) then holds with a floor of 1.62 mm at Y 63.1 and more
further back.

## 8. FDM prototype

### 8.1 Printer and settings

- Bambu Lab A1 mini, 180 x 180 x 180 mm (`plastic-lighthouse/softbox.py` assert and README, via
  `research/raw/conventions.md` 5.1; confirmed). Both shells (128.4 x 85.2 mm) fit flat.
- Family settings: 0.2 mm layers, 0.4 mm nozzle, 3 to 4 walls, 15 to 20 % gyroid, 5 top and bottom layers, PETG
  (PLA for fit checks), textured PEI for a matte face, 0.5 mm bottom chamfer against elephant's foot
  (`conventions.md` 5.2; confirmed as written). Knobs and caps at 0.12 to 0.16 mm.

### 8.2 How the geometry is adapted (print variant of the same model)

Orientation first. The top shell prints **split face down**: the plate (lip 1.0 mm, five layers) and the split
face share the bed, and the deck and knob plinth face up. That works only if no top-shell feature hangs below the
split plane, which revision 2 now guarantees: the K posts belong to the bottom shell, and the C and G posts are
replaced by inserts set into the split face. Deck-down printing was rejected: the knob plinth stands 1.80 mm above
the deck, and the plate would bridge a 78 mm key well.

| Feature | CNC variant | Print variant | Reason |
| --- | --- | --- | --- |
| Plate lip | 1.15 mm, underside Z -5.15 | 1.0 mm (5 layers), underside Z -5.00 = split plane | Plate on the bed; openings exact |
| Switch openings | 14.00 +0.05/-0 after anodise | from the 13.9 to 14.1 mm coupon | nyxilab coupon practice (`conventions.md` 3.6) |
| K countersink | Ø4.30 in the 1.15 lip | same Ø4.30; the cone reaches Ø2.30 at the plate underside | Head bears on the cone; the post top below carries the load |
| K posts (bottom shell) | Ø3.6, tapped M2 | Ø3.6 with a Ø2.2 clearance hole through the PCB zone, top at Z -5.05; below Z -8.10 a Ø6.0 boss with a Ø1.7 hole; M2 x 8 self-taps 4.0 mm into it (wall 2.15 mm). The hole may run through to the underside. | Replaces the Ø3.6 self-tap post of revision 1 (0.95 mm wall, split risk) |
| C1, C2 | Top-shell tapped posts | CNC Kitchen M2 x 3 inserts pressed into the split face of the solid control column (hole Ø3.2 x 3.5, 1.5 mm to the deck); bottom-shell posts Ø3.6 with Ø2.2 clearance rise to the split plane; screw length from the model, 2.5 to 3.0 mm in the insert | Nothing below the split on the top shell |
| G1, G2 | Top-shell posts, bare faces | Optional: the same inserts with a loose printed 1.2 mm spacer; no grounding function | The print has no metal to bond |
| Under-deck cavities (display, encoders, RF pocket) | as drawn | ceilings printed as bridges up to 15 mm; the button counterbores (Ø17) get a 45-degree chamfer or a sacrificial layer | macropad checks: bridge limit 15 mm |
| Lens recess and web | 1.15 mm recess, 0.60 mm web | 1.2 mm recess (6 layers), 0.8 mm web (4 layers) | `display.md` 7 |
| Bottom shell | one part with the wedge | flat tray printed floor down, plus the wedge as a separate bar printed on its flat face, held by two extra M2 screws | A tray with a protruding wedge cannot print without supports |
| C countersinks | 90 degrees in 2.0 mm floor | same, floor 2.4 mm (12 layers) | Plastic floor strength |
| RF insert | POM, keyed ends | printed as part of the tray wall (no slot) | The print is radio-transparent anyway |
| Feet | SJ5076 in Ø8.4 x 0.8 pockets | same | Same feet |
| PCB to wall | 0.45 mm | 0.3 mm or more per side | `conventions.md` pcb_gap |
| Lens | 0.1 mm per side | 0.1 mm per side | `conventions.md` lens_fit |

Fit coupons first (family rule): switch hole and lip, K countersink with a flush head, lens corner, knob bore,
K boss self-tap pull-out, insert fit, RF key relief fit (CNC first article only).

### 8.3 What a print can and cannot validate

Can: PCB fit and outline, switch retention in a plastic plate (the PG1353D is drawn for plastic plates), cap and
knob clearances, K screw heads flush in the cap gaps, stack heights and tilt, display window alignment, screw
access and assembly order, USB-C and switch access, battery space against the wedge, ergonomics.

Cannot: radio through aluminium (a print is transparent; `mcu-radio.md`), PG1353D retention in an aluminium lip,
anodise build-up and bead-blast distortion of the lip and the display web, case grounding, mass and feel (GLYF
claims 265 g), cosmetic finish, tolerances tighter than about +/-0.2 mm, seam flatness, the tapped-post fits.

### 8.4 Other processes, one line each

- **JLC3DP MJF PA12:** max 370 x 276 x 360 mm, tolerance +/-0.3 mm (within 100 mm) or +/-0.4 %, min wall 1.5 to
  2.0 mm at this size, assembly clearance 0.2 to 0.4 mm. Good for a stiff second prototype or a plastic bottom
  shell; the 1.0 mm lip is below its minimum wall (`06-jlc3dp/...3D-Printing-Design-Guideline.html`; confirmed).
- **JLC3DP SLA resin:** tolerance +/-0.2 mm within 100 mm, min wall 1.5 mm at 100 mm size, 2.0 mm at 200 mm. Best
  surface; brittle for a 1.0 mm lip and screw bosses. Used for keycaps and button caps (same source).

## 9. Cost (guess, anchored on section 4.2)

Shell prices are scaled from community orders of similar or larger keyboard cases (USD 100 to 140 per part or
pair at JLCPCB/JLCCNC, 2023 to 2025) plus the May 2026 increase. **They are not quotes.**

| Item | 1 set (USD) | 5 sets, total (USD) | Vendor |
| --- | --- | --- | --- |
| Top shell + bottom shell, 6061, bead blast + black anodise | 140 to 240 | 450 to 800 | JLCCNC |
| RF insert, POM | 5 to 10 | 10 to 25 | JLCCNC |
| Lens, laser-cut PMMA, painted mask | 5 to 15 | 15 to 40 | laser service or JLCCNC |
| Knobs, 6061 turned, anodised, 2 per set | 15 to 30 | 40 to 80 | JLCCNC |
| Button caps, resin, 2 per set | 2 to 5 | 5 to 10 | JLC3DP |
| Feet SJ5076, pack of 56 | 7.19 | 7.19 | DigiKey (read 2026-11-13) |
| Screws: M2 x 5 and M2 x 6 DIN 7991, M2 x 4 pan head, packs | 8 to 12 | 8 to 12 | any |
| Shipping (one JLC parcel) | 20 to 40 | 30 to 60 | |
| **Total** | **about 200 to 350** | **about 560 to 1,030 (110 to 205 per set)** | |
| FDM prototype (PETG, about 80 to 120 g, inserts) | under 5 | n/a | own printer |

Cost levers: two setups per shell, single-plane wedge and ramp, R 1.5 or larger everywhere, tight tolerances only
on the switch openings, the lens recess and the K post tops, laser marking instead of milled engraving.

## 10. Rejected options

| Option | Reason |
| --- | --- |
| Xometry, RapidDirect for the batch | No keyboard-community order reports found; US-centric shipping (Xometry) and industrial quoting add nothing for five sets; not price-checked live. |
| 7075 aluminium | Strength is not the limit; higher cost; 6061 is the vendor's and community's default. |
| Type III hardcoat | 25 to 100+ um coating disturbs the 1.15 mm lip and 14.00 mm openings; extra cost. |
| Revision 1: six screws from below into top-shell standoffs hanging from the plate (K at y = -6.9) | The 5.45 mm metal column above the standoff end cannot hold both a 3 mm thread and a 2 mm margin beyond the drill point (1.45 mm was left); the M2 x 5 tip ran 0.15 to 0.30 mm past the last thread; the K1/K2 countersinks would land on the 29 degree rear slope of the wedge; the standoffs made the FDM top shell unprintable split face down. |
| Through-tapped plate standoffs with screws from below | Fixes the thread length, but leaves a bare tapped hole open in the cap gap and still puts countersinks on the wedge slope. |
| Screws only around the perimeter (corners) | The 3.5 mm top rim is only 5.0 mm tall above the split, too short for a blind M2 thread with a 2 mm margin; corner posts below the split would show on the outside. |
| Grounding through plated holes at the case screws (`usb-io.md` 6.3 as written) | The K and C screws pass through posts and do not clamp the PCB; clamping it would stack the PCB thickness tolerance (+/-0.16 mm) against the shell seam. Dedicated G screws do the job. |
| SMD spring finger to a bare spot | No stocked part at JLCPCB (`usb-io.md` 4.4); G screws need no part. |
| RF insert with an inner flange (revision 1) | The 1.0 mm flange behind the wall over Z -5.0 to -11.6 overlaps the PCB edge (0.45 mm from the wall, Z -6.20 to -7.80) by 0.55 mm along the slot. |
| 40 mm RF slot | Needs the flank scoops to end by Y 30. |
| FDM top shell printed deck down | Knob plinth 1.80 mm above the deck, and the plate would bridge the 78 mm key well. |
| Magnets or snap fits instead of screws | Magnets near the RF bay are metal; aluminium snap fits need undercuts. |
| Separate plate | Rejected in `keys.md`. |
| Lens as RF window | Section 7.1. |
| FR4 bottom plate | Section 7.1. |
| Custom moulded silicone stadium feet (GLYF) | Tooling cost for 5 units; no stock part of 22.5 x 5.2 mm found. TPU printed stadium feet stay possible later. |
| 3M Bumpon SJ5302 (Ø7.9 x 2.2, clear) | Clear, not black; 2.2 mm leaves 1.4 mm proud in the same pocket (catalogue `07-feet/rs-bumpon.pdf`). |
| Tempered glass printed lens | Saida Glass 100-piece minimum (`follow-display-module-sourcing.md`). |
| Printing the bottom shell upside down or on its rear face | Needs supports under a 120 mm floor, or tall thin layers across the cosmetic underside. |

## 11. Risks

1. **Thin plate and bead blasting.** JLCCNC recommends walls above 1.5 mm for bead blasting "or alternatively
   select a process without sandblasting"; the lip is 1.15 mm across a 78 mm key field with 16 openings and four
   countersinks. Mitigation: order one top shell first and measure the lip, opening size and plate flatness; if it
   distorts, order the next top shells anodised without blasting (vendor-stated alternative). The GLYF uses a
   similar lip (likely).
2. **Display web 0.60 mm.** `display.md` puts a 0.60 mm aluminium web with a 24.8 mm window under the lens. That is
   above JLCCNC's 0.5 mm absolute minimum but below its 0.8 mm recommendation and far below the bead-blast advice.
   It is a ledge 0.8 to 4.1 mm wide supported along its outer edge, not a free wall, and it hides behind the
   24.4 mm mask window, so it is not cosmetic. Request to the display subsystem: a 0.80 mm web by lowering the
   module 0.20 mm (module back at Z -3.55, 1.65 mm above the connector top), if the flex fold allows. Otherwise
   inspect web flatness (0.05 mm) on the first article.
3. **No live price.** All case costs are estimates; JLCCNC can change prices without notice since May 2026.
4. **Plastic insert close to the antenna.** Dielectric loading of the chip antenna by POM 2.45 to 2.65 mm away is
   not quantified. Covered by the `mcu-radio.md` acceptance test; the stepped insert of 7.2 item 5 is the next move.
5. **K countersinks close to the switch openings.** 0.375 mm of plate top remains between each countersink and two
   openings. Burrs there would lift a switch flange. Mitigation: deburr callout, check on the first top shell; the
   PCB keep-outs leave no room to move K along x.
6. **K post fit.** The post top is set 0.05 to 0.10 mm below the plate underside so the seam closes; out of
   tolerance the plate is pulled down more near four switches. FIT callouts on the post tops and split faces.
7. **Battery pocket against the wedge** (6.6). Not solvable inside this record.
8. **Wedge cost.** Sloped faces on the bottom shell may dominate its price.
9. **Colour match between shells and knobs.** Batches can differ; order all anodised parts in one order.
10. **Feet supply.** Farnell Japan lists SJ5076 as no longer manufactured while DigiKey lists it Active with
    1,222,328 in stock (read 2026-11-13); buy the 56-pack with the first order.
11. **Bare G post faces.** JLCCNC offers masking for threads; a bare flat face needs laser removal or
    post-machining. Not confirmed at order. The thread path (screw head on the GND ring, screw in a bare thread)
    still bonds the top shell if the faces come back anodised.

## 12. Sources

- JLCCNC capabilities: https://jlccnc.com/cnc-machining-capabilities (cached `01-jlccnc/cap.html`; 3D STEP, 2D DWG
  or DXF)
- JLCCNC CNC design guideline: https://jlccnc.com/help/article/CNC-Machining-Design-Guideline (metal walls 0.8 mm
  recommended, 0.5 mm minimum)
- JLCCNC appearance standard: https://jlccnc.com/help/article/appearance-standard-guidelines (bead blast above 1.5
  mm or no blasting; rubber plugs, threads below M5 not anodised)
- JLCCNC surface treatment: https://cnc.jlcpcb.com/help/article/Surface-Treatment-for-CNC-Machining
- JLCCNC anodising and masking: https://jlccnc.com/blog/electroplating-vs-anodizing, https://jlccnc.com/blog/sulfuric-acid-anodizing
- JLCCNC keyboard case guide: https://jlccnc.com/blog/custom-keyboard-case
- JLCCNC materials: 6061, 7075, FR4, PMMA, PC, POM help articles (cached in `01-jlccnc/`)
- JLCCNC price adjustment 2026-05-08 (cached `01-jlccnc/price-adjust-2026-05.html`); JLC3DP CNC notice https://jlc3dp.com/news/cnc-service-price-adjustment-notice
- PCBWay CNC: https://www.pcbway.com/rapid-prototyping/cnc-machining/ and order form `manufacture/?type=2`
- Xometry: https://www.xometry.com/capabilities/cnc-machining-service/
- RapidDirect: https://www.rapiddirect.com/services/cnc-machining/
- JLC3DP design guideline: https://jlc3dp.com/help/article/3D-Printing-Design-Guideline
- Community: https://note.com/copkbd/n/n7063aaa7e778 (cached `02-community/note-copkbd.html`, text `copkbd.txt`); https://green-keys.info/en/talk-about-ordering-aluminum-keyboard-parts-from-jlcpcb/ ; Jorne wiki case list (cached `02-community/jorne-wiki-cases.html`); beekeeb PCBWay case post (cached `02-community/beekeeb.html`); PCBWay Fun 60 and Ferris Sweep aluminium case projects (cached, no price stated)
- 3M Bumpon catalogue (cached `07-feet/rs-bumpon.pdf`); DigiKey SJ5076: https://www.digikey.com/en/products/detail/3m/SJ5076/570288 (read 2026-11-13: Active, 1,222,328 in stock, 56 at USD 0.12839, 8.00 x 2.79 mm, polyurethane, black)
- DIN 7991 M2 dimensions: https://boltsparts.github.io/en/parts/standards/DIN7991.html (read 2026-11-13: d2 4.0, k max 1.2, s 1.25)
- CNC Kitchen M2 x 3 insert: https://eshop.wuerth.de/Original-CNC-Kitchen-thread-insert-THRINRT-SHORT-M2X3MM-100-PCS-/4954617301.sku/en/US/EUR (search summary)
- JLCPCB parts API searches for case hardware: cached `04-jlc-parts/*.json`
- Project records: `research/components/keys.md`, `mcu-radio.md`, `display.md`, `rotary-buttons.md`, `usb-io.md`, `power.md`; notes `research/raw/geometry.md` (body profile, scoops line 218), `conventions.md`, `follow-rf-exit-in-aluminium.md`, `follow-display-module-sourcing.md`
- KiCad 10.0.7 stock library listing of `MountingHole.pretty` (local Docker image): M2 holes are Ø2.2 only, so
  the Ø4.0 NPTH footprints are project-drawn; the G holes can use the stock `MountingHole_2.2mm_M2_ISO14580_Pad`
  footprint (plated Ø2.2 with a pad on both faces; pad diameter to be checked against the Ø4.6 ring).

Not checked: live quotes at any vendor; whether JLCCNC can skip blasting on one face or laser-clear an inside
face in the same order; JLCMC as a source for screws and inserts; PCBWay and Xometry prices; stock of the screws
and inserts by direct page read.

## 13. Review of revision 1 and what changed

| # | Review point | Verdict | Change |
| --- | --- | --- | --- |
| 1 | M2 x 5 reaches past the 3.0 mm thread and jams | Accepted. Head sits 0.15 to 0.30 mm deep, so the tip landed at Z -6.30 to -6.15, past the thread end at -6.45. | K screws now enter from the top into bottom-shell posts with 4.8 mm full thread and a 0.55 mm margin; C screws have 4.8 mm full thread with 0.3 mm or more margin (6.4). |
| 2 | Standoff drill left 1.45 mm against the 2 mm rule | Accepted; with the 0.48 mm drill point it was about 0.97 mm. | Every tapped hole now keeps 2.02 mm (G) to 6.76 mm (K1) beyond the drill point (6.4). |
| 3 | Insert flange hits the PCB edge | Accepted. | Flange removed; insert keyed by two vertical Ø2.0 reliefs in the slot ends; nothing enters the cavity (7.2). |
| 4 | FDM top shell cannot print plate down | Accepted. | K posts moved to the bottom shell; C and G use inserts in the split face; the print top shell has nothing below the split plane (8.2). |
| 5 | Lens and web numbers contradict `display.md`; 0.60 mm web not covered | Accepted. | Lens, recess and web now follow `display.md`; the web is risk 2 with a request for 0.80 mm. |
| 6 | JLCCNC takes DWG or DXF, not PDF | Accepted (cap.html re-read). | Drawings ordered as DXF, PDF copy for reading. |
| 7 | Countersunk head misquoted | Accepted (boltsparts DIN 7991 read: d2 4.0, k 1.2). ISO 10642 has no M2. | Section 5 corrected; reach arithmetic uses these values. |
| 8 | Bare-thread grounding overstated | Accepted. | Dedicated G1, G2 PCB screws with bare post faces; this also replaces `usb-io.md`'s plated case-screw holes (reported in the output). |
| 9 | Foot stock and price out of date | Accepted; DigiKey read today matches the reviewer's figures. | 6.3, 9 and risk 10 updated. |
| 10 | Right flank scoop not handled | Accepted. | 30 mm slot and scoops ending by Y 35 (7.3). |
| 11 | FDM K posts Ø3.6 with Ø1.7 hole split risk | Accepted. | Print K posts self-tap into a Ø6.0 boss below the PCB (2.15 mm wall). |
| 12 | No live quote | Accepted; still none. | Stated as a guess in 1, 4.2, 9 and risk 3. |

Found during this revision, not raised by the review: revision 1's K1/K2 countersinks would have sat on the 29
degree rear slope of the wedge; the battery pocket of `power.md` does not fit the wedge profile (6.6).
