# Follow-up: switch family, footprint and hot-swap socket

Date: 2026-11-13
Key: `follow-switch-family-and-socket`
Cache: `research/_cache/follow-switch-family-and-socket/` (gitignored)

Question: which Kailh series is the "Kailh Low Profile V2, fully POM" switch of the GLYF, and what are its
plate cut-out, plate thickness, height above the plate, travel, PCB hole pattern and matching hot-swap socket?

Confidence words: **confirmed** means stated by the maker of the part (Kailh) or measured from a primary source.
**likely** means consistent indirect evidence. **guess** means an inference without direct support.

## 1. Answer in short

1. The switch is the Kailh **PG1353D** series. Kailh sells it as "Kailh Choc V2 Full POM Shadow Series Low Profile
   Keyboard Switch". It is a member of the Choc V2 (PG1353) family and uses the Choc V2 footprint. (confirmed)
2. The PCB pattern is: one 5.00 mm centre hole, two contact pins at the Choc positions (5.90 mm on the axis, and
   3.80 mm along the axis with 5.00 mm sideways), and one small third hole at 5.15 mm and 5.00 mm on the opposite
   diagonal. (confirmed, Kailh drawing)
3. The hot-swap socket is the Kailh **CPG135001S30** ("PG1350 KeySwitches Contact", LCSC `C5333465`). The PG1353D
   drawing itself shows a "PCB hole pattern with connector" that has the same two 3.00 mm holes and 2.60 mm pads as
   the socket datasheet. (confirmed for the geometry; the PG1353D drawing does not print the socket part number)
4. Plate data: body 13.95 +/-0.05 mm square under a 15.00 mm square flange; the gap between flange and snap hook is
   1.35 +0/-0.10 mm; the plate top face is 2.20 mm above the PCB top face. (confirmed)
5. Heights above the plate top face: housing collar 3.50 mm, stem top 6.40 mm at rest. Total travel 2.8 +/-0.25 mm.
   (confirmed)
6. Two problems for this project. First, `C5333465` has zero stock at LCSC and JLCPCB today and JLCPCB marks it as
   not purchasable. Second, both Kailh PG1353D drawings carry the note "this product only fits plastic plates".
   The GLYF nevertheless puts the switches into an aluminium shell. (confirmed facts; the consequence is a design risk)

## 2. Identity of the switch family

| Fact | Source | Confidence |
| --- | --- | --- |
| Kailh's product page is titled "Kailh Choc V2 Full POM Low Profile Keyboard Switch". The summary line reads "Kailh Choc V2 Full POM Shadow Series Low Profile Keyboard Switch ... Hot Swappable Total Travel:2.8±0.25mm, Operation Force:50±10gf, Lifetest:50 millions". | https://www.kailhswitch.com/mechanical-keyboard-switches/low-profile-key-switches/kailh-choc-v2-full-pom-low-profile-keyboard.html (`pages-03/fullpom.html`) | confirmed |
| The datasheet linked from that page is headed "PG1353D Push Switch", part number `CPG1353D01D01-16`, drawing number `KHA-PG1353D-***`, dated 2024-05-02. The part list gives base POM, cover POM, keystroke (stem) POM. | https://www.kailhswitch.com/uploads/15927/files/CPG1353D01D01-16-data-sheet.pdf (`pdf-01/`, pages 1 and 2) | confirmed |
| The same page names three variants, the "Elements series": White Rain (linear, 50 +/-10 gf, pre-travel 1.2 +/-0.30 mm), Black Cloud (tactile, 45 +/-10 gf operating, 55 +/-10 gf tactile, pre-travel 1.6 +/-0.30 mm), Hide Mountain (clicky, 50 +/-10 gf operating, 55 +/-10 gf tactile, pre-travel 1.2 +/-0.30 mm). All three: total travel 2.8 +/-0.25 mm, spring 15.5 mm, 50 million cycles. | Images on the Kailh page (`img-02/sheet-fullpom.png`) | confirmed |
| A second PG1353D datasheet exists: `CPG1353D01D01-31`, "Choc V2 Low Profile Ice Cream Switch", linear, 38 +/-8 gf on the drawing (40 +/-8 gf in the page text), dated 2024-11-29. Same outline and same PCB pattern. | https://www.kailhswitch.com/uploads/15927/files/CPG1353D01D01-31-data-sheet.pdf | confirmed |
| The Lofree x Kailh "Shadow" switches (Ghost linear, Phantom tactile, and later Specter, Hades, Pulse, Surfer, Void) are the same full-POM low-profile family. Lofree lists Ghost with actuation force 50 +/-15 gf, total travel 2.8 +/-0.25 mm, pre-travel 1.2 +/-0.3 mm, spring 15.5 mm. | https://lofree.co/products/lofree-ghost-switches and https://lofree.co/products.json (`pages-01/`, `pages-02/lofree-products.json`) | confirmed (Lofree specs), likely (same PG1353D tooling) |
| The three switch pictures in the maker's Update 03 (`research/_cache/social/blog-images-01/16...png`, `17...png`, `18...png`) are Lofree product renders with the "Lofree x Kailh" footer cropped off. Image 16 matches the Phantom render, image 17 matches the Ghost render, image 18 matches the Specter render (solid grey). | Comparison with `lofree-01/sheet-lofree.jpg` (built from Lofree product images) | confirmed (visual match) |
| Production GLYF units carry a white full-POM switch with two LED slots at one end of the top housing and a cross stem inside a round collar. This is the PG1353D housing shape shown on the Kailh page (White Rain is the white linear type). | `research/_cache/youtube/frames-01/Q6CKpc6AK0o/f017.jpg`, `research/_cache/social/tiktok-frames-hd-01/cal_sheet.jpg`, `img-01/fullpom--...92a1c.png` | likely |
| The standard Choc V2 is headed "PG1353 Push Switch" (for example `CPG135301D03`, blue, dated 2019-10-25; `CPG1353S01D01-01`, silent linear, dated 2023-05-12). It has the same 15.00 mm flange, 13.95 mm body, centre post and pin positions. | https://www.kailhswitch.com/Content/upload/pdf/202015927/PG135301D03.pdf and https://www.kailhswitch.com/uploads/15927/files/CPG1353S01D01-01-data-sheet.pdf | confirmed |

Differences between PG1353 (standard Choc V2) and PG1353D (full POM), from the drawings:

- PG1353 has three metal legs ("3-3.00±0.2"). PG1353D has two ("2-3.00±0.2"). The third position stays in the
  PG1353D PCB pattern as a "clearance hole". (confirmed)
- Total travel: 3.2 +/-0.25 mm on the 2019 blue PG1353 drawing; 2.8 +/-0.25 mm on the silent PG1353 and on both
  PG1353D drawings. (confirmed)
- The PG1353D drawings carry a plate-material note (section 6). The two PG1353 drawings do not. (confirmed)

## 3. Switch dimensions (Kailh drawing `CPG1353D01D01-16`, sheet 1 of 2)

All values in millimetres. Rendered pages: `pdf-render-02/pom16-1-view.png`, crops `c1-bottom.png`, `c1-side.png`,
`c1-front.png`.

| Dimension | Value | Confidence |
| --- | --- | --- |
| Top flange, square | 15.00 x 15.00 | confirmed |
| Body below the flange (the part that enters the plate) | 13.95 +/-0.05 x 13.95 +/-0.05 | confirmed |
| Gap between flange underside and snap hook (controlled dimension 04) | 1.35 +0/-0.10 | confirmed |
| Flange underside (plate top face) down to housing bottom (PCB top face) | 2.20 | confirmed |
| Plate top face up to the top of the housing collar | 3.50 | confirmed |
| Plate top face up to the stem top, switch at rest | 6.40 | confirmed |
| Housing height without the collar rim / with the collar rim | 5.30 / 5.70 | confirmed |
| Housing top face above the plate top face | 3.10 (5.30 minus 2.20; printed as 3.10 on the silent PG1353 drawing) | likely |
| Total travel / pre-travel | 2.8 +/-0.25 / 1.2 +/-0.30 | confirmed |
| Centre post below the housing bottom | diameter 4.80, length 3.30 | confirmed |
| Contact pins below the housing bottom | 2 pins, length 3.00 +/-0.2, width 0.80 | confirmed |
| Stem: MX-type cross, arm length 4.00 +/-0.05, arm thickness 1.30 +0/-0.05 | confirmed |
| Round stem wall: diameter 5.50 marked in the top view (5.70 on the `-31` drawing), diameter 6.50 in the side view. Reading: inner 5.50 or 5.70, outer 6.50. | likely (the drawing does not label inner and outer) |
| LED window in the base: 2.95 wide, 5.50 long, centre line 4.93 from the switch centre, on the side opposite the pins | confirmed |
| Operating force of this part number | 40 +/-10 gf (return force 15 gf minimum) | confirmed |
| Rating | 12 V DC, 10 mA; contact resistance 200 mOhm maximum; life 50,000,000 cycles | confirmed |

Derived stack for the case design (PCB 1.6 mm thick, as the socket datasheet assumes):

| Level | Height relative to PCB top face |
| --- | --- |
| Stem top at rest | +8.60 |
| Stem top fully pressed (travel 2.8) | +5.80 |
| Collar rim of the housing | +5.70 |
| Housing top face | +5.30 |
| Plate top face (flange seat) | +2.20 |
| Plate bottom face with a 1.2 mm plate | +1.00 |
| PCB top face | 0.00 |
| PCB bottom face | -1.60 |
| Pin tips | -3.00 +/-0.2 (1.40 below the PCB bottom) |
| Centre post tip | -3.30 (1.70 below the PCB bottom) |
| Socket body underside | -3.45 +/-0.1 (1.85 +/-0.1 below the PCB bottom) |

The clear height needed under the PCB at each key is therefore 1.85 mm plus the tolerance of the bottom shell. (likely)

## 4. Plate cut-out and plate thickness

| Fact | Source | Confidence |
| --- | --- | --- |
| No Kailh drawing prints a recommended plate cut-out. The value has to be taken from the body size 13.95 +/-0.05 mm. | All five datasheets in `pdf-01/` | confirmed (absence) |
| A 14.00 mm square cut-out (tolerance +0.05/-0) gives 0.00 to 0.15 mm total clearance on the body. This is the same cut-out the sibling projects use for MX switches. | Derived from the body size; `research/raw/conventions.md` (14.0 mm square, 14.00 +0.05/-0) | likely |
| The maker's caliper reads 14.06 mm on a switch opening of a machined sample. That is consistent with a 14.00 mm nominal opening. | `research/_cache/social/tiktok-frames-hd-01/cal_sheet.jpg` | confirmed (reading), likely (nominal) |
| The plate thickness at the snap edges must be below the 1.25 to 1.35 mm hook gap. A plate of 1.2 mm (1.15 to 1.25) fits. A thicker shell needs a relief pocket from below so that only a 1.2 mm lip remains at the cut-out edge. | Dimension 04 on the PG1353D drawing | confirmed (gap), likely (1.2 mm nominal) |
| The snap hooks sit on the two housing edges that do not carry the LED window or the "kailh" mark. With the LED window to the rear, the hooks are on the left and right edges. | Top and bottom views of the PG1353D drawing | likely |
| The plate top face must be 2.20 mm above the PCB top face. With a 1.2 mm lip the free gap between lip underside and PCB is 1.00 mm. | PG1353D drawing | confirmed |
| Neighbouring flanges are 15.00 mm wide. At 19.05 mm pitch the web between two cut-outs is 5.05 mm. | Derived | confirmed (arithmetic) |

## 5. PCB hole pattern

### 5.1 Kailh drawing, with socket

Source: `CPG1353D01D01-16` sheet 2 of 2, titled "PCB hole pattern with connector, view from the pad side (for
reference)" (`pdf-render-02/c2-pcb.png`). The `-31` datasheet shows the identical pattern
(`pdf-render-02/pom31-2-pcb.png`). View is from the solder side. Origin is the switch centre. (confirmed)

| Feature | Position in the Kailh pad-side view | Size |
| --- | --- | --- |
| Centre hole | 0, 0 | diameter 5.00 |
| Socket hole A (on the axis) | 6.00 to the right | diameter 3.00 |
| Socket hole B | 3.80 to the right, 5.00 up | diameter 3.00 |
| Third hole ("clearance hole") | 5.15 to the left, 5.00 down | slot 2 x 1.5 |
| LED position | 4.93 to the left | not a hole |
| Socket pads | one beyond each socket hole, on the socket's long axis | width 2.60 |

Kailh's note on the 6.00 dimension says: "This dimension differs from the product centre distance by 0.1 mm; this
does not affect use." The switch pin is at 5.90 mm. The socket barrels are 5.00 mm and 2.20 mm apart, so one hole
is drawn at 6.00 mm. (confirmed)

### 5.2 Kailh drawing, soldered (no socket)

Source: `PG135301D03.pdf` and `CPG1353S01D01-01-data-sheet.pdf`, "Recommended PCB Layout (Pattern Side)". (confirmed)

- Two pin holes, diameter 1.20, at 5.90 on the axis and at 3.80 with 5.00 sideways.
- Centre hole, diameter 5.00.
- Third hole at 5.15 and 5.00 on the opposite diagonal: diameter 1.60 on the 2019 drawing; a 2 x 1.5 slot on the
  2023 drawing, with the note "this hole has this shape so that all switches of this series can share it".

### 5.3 The same pattern in a top-view footprint frame

Frame: viewed from the switch side, x to the right, y towards the front edge of the device, LED window towards the
rear edge. This is the orientation the GLYF uses (section 7). Derived from 5.1 by mirroring and rotating. (likely)

| Feature | x | y |
| --- | --- | --- |
| Centre hole, 5.00 | 0 | 0 |
| Pin 2 (socket hole 3.00) | 0 | +5.90 (socket hole at +6.00) |
| Pin 1 (socket hole 3.00) | -5.00 | +3.80 |
| Third hole | +5.00 | -5.15 |
| LED window centre | 0 | -4.93 |

### 5.4 Cross-check with open footprint libraries

| Library | Values | Agreement |
| --- | --- | --- |
| kiswitch `SW_Hotswap_Kailh_Choc_V2.kicad_mod` (descr "Kailh Choc keyswitch V2 CPG1353 V2 Hotswap", last commit 2023-05-21) | NPTH 3.05 at (0, -5.9) and (5, -3.8); NPTH 5.05 at (0, 0); NPTH 1.6 at (-5, 5.15); SMD pads 2.55 x 2.5 on the back at (-3.5, -6) and (8.5, -3.8) | Same pattern as Kailh, rotated 180 degrees relative to 5.3 |
| kiswitch `SW_Kailh_Choc_V2.kicad_mod` (soldered) | Pads with 1.2 drill at (0, -5.9) and (5, -3.8); NPTH 5.05 centre; plated hole 1.6 drill at (-5, 5.15) | Same as Kailh 5.2 |
| ceoloide `switch_choc_v1_v2.js` (last commit 2026-10-07) | Socket holes 3.0 at (0, -5.95) and (5, -3.75); centre hole 5.0 when Choc V2 support is on; corner hole 1.6 drill at (5.00, 5.15) offsets; socket pads 2.6 x 2.6 at (3.275, -5.95) offsets | Same pattern, holes placed midway between pin and socket positions |

Sources: https://github.com/kiswitch/kiswitch (tree `library/footprints/Switch_Keyboard_Hotswap_Kailh.pretty/`),
https://github.com/ceoloide/ergogen-footprints (`switch_choc_v1_v2.js`); copies in `footprints-01/`. (confirmed)

The repository https://github.com/kiswitch/keyswitch-kicad-library returns the same file tree as
https://github.com/kiswitch/kiswitch. (confirmed)

### 5.5 Check against the maker's board

Measured on `research/_cache/youtube/frames-01/S9c5WuorsgQ/f020.jpg` (bottom side of the GLYF board). Scale taken
from the centre-hole pitch, assumed 19.05 mm (the maker's footprint carries a "19.05" outline, see
`research/raw/youtube.md`). Blob centres found with ImageMagick connected components; working files in
`measure-01/`.

| Measurement | Result | Kailh value | Confidence |
| --- | --- | --- | --- |
| Centre-hole diameter | 4.7 to 4.9 mm (33 to 35 px at 7.09 px/mm) | 5.00 (Choc V1 would be 3.4) | confirmed |
| Small plated hole relative to its centre hole, bottom view, sockets on the +y side | (-5.0, -5.0) mm, +/-0.3 | (-5.00, -5.15) | confirmed |
| Socket position | Below the centre hole, the barrel on the axis is farther from the centre than the offset barrel | Holes at (0, 6.00) and (5.00, 3.80) | likely (rough reading; the socket top is raised above the board) |

The maker's board therefore has the Choc V2 pattern: 5 mm centre hole, third hole on the diagonal opposite the
contacts, and a two-barrel socket with terminals at both ends. (confirmed)

## 6. Kailh's plate-material note

| Fact | Source | Confidence |
| --- | --- | --- |
| The `CPG1353D01D01-16` drawing has a boxed note on both sheets: "'Linear' feel. This product only fits plastic plates." | `pdf-render-02/pom16-1-view.png`, `pom16-2-view.png` (Chinese: 此产品只适配塑胶面板) | confirmed |
| The `CPG1353D01D01-31` drawing has the same note and adds: "This switch must not go through wave soldering." | `pdf-render-02/pom31-1-view.png` | confirmed |
| The two PG1353 (non-POM housing) drawings have no plate-material note. Their boxed note only says "provisional version". | `pdf-render-02/v2-1-view.png`, `s01-1-view.png` | confirmed |
| Kailh does not give a reason. A plausible reason is that the POM snap hooks and the 13.95 mm POM body wear or loosen against a hard metal edge. | none | guess |
| The GLYF mounts these switches in the CNC aluminium top shell, which has no separate plate. | `research/raw/youtube.md`, `research/raw/official-site.md` | confirmed |
| Datasheets for the tactile (Black Cloud) and clicky (Hide Mountain) PG1353D types: not found. Whether they carry the same note is unknown. | Kailh sitemap (`pages-02/kailhswitch-sitemap.xml`, 1058 URLs) | not found |

Design consequence: an aluminium plate is used by the reference product but is outside Kailh's stated use for
PG1353D. The design should either accept that risk with clean, deburred 14.00 mm edges and a 1.2 mm lip, or allow
standard PG1353 Choc V2 switches as the documented alternative. Both fit the same footprint and cut-out. (likely)

## 7. Switch orientation in the GLYF

| Fact | Source | Confidence |
| --- | --- | --- |
| On the switch, the LED window is on the side opposite the two pins. | Top and bottom views of the PG1353D drawing | confirmed |
| On a production unit with one keycap removed, the two LED slots face the rear edge (the edge with the USB-C opening). | `research/_cache/youtube/frames-01/Q6CKpc6AK0o/f017.jpg` | confirmed |
| On the board, the sockets sit on the front side of each centre hole and the third hole sits on the rear side. This agrees with the row above. | `research/_cache/youtube/frames-01/S9c5WuorsgQ/f020.jpg` (the slide switch marks the rear edge) | likely |
| The GLYF orientation is the kiswitch Choc V2 footprint rotated by 180 degrees. | Derived from sections 5.3 and 5.4 | likely |

## 8. Hot-swap socket CPG135001S30

Source: Kailh product specification `KH-PS-1702-35` revision D (2024-01-09), drawing `KHA-PG1350-005EN`, title
"PG1350 KeySwitches Contact", https://www.kailhswitch.com/uploads/15927/files/CPG135001S30.pdf (`pdf-01/`, rendered
in `pdf-render-02/sock-01-view.png` and `sock9-crop.png`). All rows confirmed unless marked.

| Item | Value |
| --- | --- |
| Overall length, terminal tip to terminal tip | 13.45 +/-0.1 (side view gives 13.15 +/-0.15) |
| Body length / body width | 9.55 +/-0.1 (side view 9.95 +/-0.15) / 6.85 +/-0.1 |
| Barrel spacing | 5.00 +/-0.1 along the socket, 2.20 +/-0.1 across |
| Barrel outer diameter | 2.90 +/-0.1 |
| Height below the PCB surface | 1.85 +/-0.1 |
| Total height including the barrels that enter the PCB | 3.15 +/-0.1 |
| Terminal width | 1.68 +/-0.1 |
| Recommended PCB layout | Two holes, diameter 3.00, spaced 5.00 and 2.20; two pads 2.60 x 2.60; "Single face board T=1.6mm" |
| Pad position, scaled from the raster drawing | Pad centre about 3.6 from its hole centre along the socket (kiswitch uses 3.5) - likely |
| Materials | Base nylon, black; two contacts, copper alloy, nickel then gold on the contact area, tin on the solder area |
| Rating | 12 V AC/DC maximum, 10 mA maximum, contact resistance 100 mOhm maximum |
| Mating force / unmating force | 3.0 kgf maximum / 200 gf minimum |
| Mechanical life | 100 cycles |
| Soldering | Reflow, 260 +/-5 degC, 5 +/-0.5 s; packaged on reel, 26,000 pieces per carton |

Statements about compatibility:

- Kailh's socket page says: "The Choc socket only works with Kailh's low profile Choc V1 switches."
  Source: https://www.kailhswitch.com/mechanical-keyboard-switches/box-switches/choc-type-hot-swap-socket.html (confirmed quote)
- Kailh's own PG1353D drawing shows a socket layout with the CPG135001S30 hole and pad dimensions (section 5.1).
  (confirmed)
- Keebio states that Choc V1 and Choc V2 "share the same hotswap socket" and that V2 needs the larger centre hole.
  Source: https://blog.keeb.io/kailh-choc-v2-switch-comparison/ (confirmed quote)
- The maker's board uses a two-barrel socket of this shape with these switches (section 5.5). (likely)

Conclusion: CPG135001S30 is the matching socket. The sentence on the Kailh socket page is out of date. (likely)

### 8.1 Availability on 2026-11-13

| Fact | Source | Confidence |
| --- | --- | --- |
| LCSC part number `C5333465`, brand Kailh, model CPG135001S30, tape and reel, minimum order 5. | LCSC product API `https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=C5333465` (`lcsc-01/lcsc-detail-C5333465.json`) | confirmed |
| LCSC stock is 0 in all warehouses. The record has `productCycle: sold_out` and `isForeignOnsale: false`. No alternative part is listed. | same | confirmed |
| JLCPCB assembly library: `C5333465`, library type "expand" (extended part), stock 0, pre-sale 0, flagged "This product is no longer manufactured" and not purchasable. Last price ladder 0.1617 USD (1 to 49) down to 0.0805 USD (4000 and more). | JLCPCB parts API `selectSmtComponentList`, keyword CPG135001S30 (`lcsc-01/jlc-135001.json`) | confirmed |
| The "no longer manufactured" flag is a JLCPCB catalogue state. Kailh still publishes the socket page and a datasheet PDF created in August 2025. | PDF metadata of `pdf-01/CPG135001S30.pdf`; Kailh page above | likely |
| No other low-profile (Choc) hot-swap socket with stock was found in the JLCPCB library. The in-stock keyboard sockets are MX types only: HanElectricity `CPG151101S11-16` (`C41430893`, stock 202,244) and `CPG151101S11-2` (`C49352235`, stock 29,626). | JLCPCB parts API, keywords listed in `lcsc-01/` | confirmed (for the keywords tried) |
| Gateron low-profile sockets `KS-2P02B01-02` (`C18212911`) and `KS-2P02B01-01` (`C2803487`) are listed with stock 0. They are for the Gateron low-profile footprint and were not checked against the Choc pattern. | same | confirmed (stock), not checked (fit) |
| PG1353 and PG1353D switches are not stocked at JLCPCB: `CPG135301D01` (`C45350823`), `CPG135301D02` (`C5142796`), `CPG1353S01D02-01` (`C55213859`) all show stock 0. No PG1353D part number is listed. | JLCPCB parts API, keyword CPG1353 | confirmed |
| Kailh's own web shop (kailh.net, 42 products) lists a "Kailh Choc V2 Low Profile Switch Set" (`CPG135301D01`, `D02`, `D03`, 110 pieces) but no full-POM low-profile set and no Choc socket. | https://www.kailh.net/products.json (`pages-01/kailhnet-products.json`) | confirmed |
| Lofree sells Ghost and Phantom switch packs: 106 pieces for 59.00 in the shop's base currency. | https://lofree.co/products.json | confirmed |

Consequence for the order: the 16 sockets cannot be placed from the JLCPCB library today. The options are to buy
the sockets elsewhere and consign them to the assembler, to solder them by hand (32 joints), or to ask the
assembler to source them. PCBWay sourcing was not checked. (likely)

## 9. Recommended design values

These are the values that follow from the confirmed facts above. They are recommendations, not maker data.

1. Footprint: Choc V2 hot-swap, sockets on the bottom side. Centre NPTH 5.00 to 5.05 mm. Socket NPTH 3.00 to
   3.05 mm at the positions in section 5.3. Third hole 1.6 mm round or a 2.0 x 1.5 mm slot. Socket pads 2.55 to
   2.60 mm square, centres 3.5 mm outside each socket hole. PCB thickness 1.6 mm.
2. Plate (top shell): 14.00 +0.05/-0 mm square openings; 1.2 mm lip at each opening; lip top face 2.20 mm above the
   PCB top face; pocket for the 15.00 mm flanges if the key well is recessed.
3. Height above the plate: keep 3.5 mm for the housing and plan for a stem top at 6.4 mm. Travel is 2.8 mm.
4. Under the PCB: keep at least 1.85 mm plus tolerance free under every socket.
5. Bill of materials: socket Kailh CPG135001S30 (`C5333465`), supplied outside the JLCPCB library until stock returns.

## 10. Sources read

- https://www.kailhswitch.com/mechanical-keyboard-switches/low-profile-key-switches/kailh-choc-v2-full-pom-low-profile-keyboard.html
- https://www.kailhswitch.com/uploads/15927/files/CPG1353D01D01-16-data-sheet.pdf (8 pages; pages 1 and 2 are drawings)
- https://www.kailhswitch.com/mechanical-keyboard-switches/low-profile-key-switches/choc-v2-low-profile-ice-cream-switch.html
- https://www.kailhswitch.com/uploads/15927/files/CPG1353D01D01-31-data-sheet.pdf
- https://www.kailhswitch.com/mechanical-keyboard-switches/key-switches/kailh-low-profile-switch-choc-v2.html
- https://www.kailhswitch.com/Content/upload/pdf/202015927/PG135301D03.pdf
- https://www.kailhswitch.com/mechanical-keyboard-switches/low-profile-key-switches/choc-v2-low-profile-silent-linear-switch.html
- https://www.kailhswitch.com/uploads/15927/files/CPG1353S01D01-01-data-sheet.pdf
- https://www.kailhswitch.com/mechanical-keyboard-switches/box-switches/choc-type-hot-swap-socket.html
- https://www.kailhswitch.com/uploads/15927/files/CPG135001S30.pdf
- https://www.kailhswitch.com/sitemap.xml
- https://www.kailhswitch.com/news/kailh-choc-v-32057417.html, https://www.kailhswitch.com/news/kailh-choc-switch-v-49526099.html
- https://www.kailhswitch.com/info/kailh-choc-v2-feature-44841625.html, https://www.kailhswitch.com/info/kailh-low-profile-choc-v2-switch-advantage-44843911.html
- https://www.kailh.net/products.json
- https://lofree.co/products/lofree-ghost-switches, https://lofree.co/products.json, Lofree product images
- https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=C5333465
- https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList (keywords: CPG135001S30, C5333465, CPG1350, PG1350, CPG1353, PG1353, CPG13, Choc, Kailh, Gateron, KS-2P02B01, HanElectricity, CPG151101S11, C41430893, Mechanical Keyboard Shaft, hot swap socket, keyboard socket, hot-plug, low profile hot swap)
- https://github.com/kiswitch/kiswitch, https://github.com/kiswitch/keyswitch-kicad-library, https://github.com/ceoloide/ergogen-footprints
- https://blog.keeb.io/kailh-choc-v2-switch-comparison/
- https://kbd.news/switch/Kailh-Choc-V2-White-Rain-231.html
- https://deskauthority.saberkeebs.com/wiki.themk.org/index.php/Kailh_Choc_V2.html (mirror of the Deskthority wiki page)
- https://mechkeys.com/blogs/news/lofree-kalih-announces-shadow-worlds-first-series-of-full-pom-material-low-profile-switches (downloaded, not used for any value)
- https://focusattack.com/kailh-white-rain-linear-full-pom-low-profile-mx-switch/, https://www.rtings.com/keyboard-switch/reviews/kailh/white-rain (downloaded; no footprint or plate data found in the static HTML)
- Local evidence: `research/_cache/youtube/frames-01/S9c5WuorsgQ/f020.jpg`, `research/_cache/youtube/frames-01/Q6CKpc6AK0o/f017.jpg`, `research/_cache/social/tiktok-frames-hd-01/cal_sheet.jpg`, `research/_cache/social/blog-images-01/` files 16 to 18, `research/_cache/official-site/04-previews/files__2_93486fad-42cb-4bad-9493-b398f9209306.jpg`
- Existing notes: `research/raw/social.md`, `youtube.md`, `official-site.md`, `regulatory-software.md`, `community-press.md`, `prior-art.md`, `conventions.md`

## 11. Not reached, not found

- https://deskthority.net/wiki/Kailh_Shadow and https://deskthority.net/wiki/Kailh_PG1353_series: HTTP 403 for a
  plain client. A mirror of the PG1353 page was read instead; the mirror of the Shadow page had no useful text.
- https://www.kailh.com/: no connection.
- LCSC keyword search API (`wmsc.lcsc.com/ftps/wm/search/...`): HTTP 404 body. The product-detail API worked.
- https://jlcsearch.tscircuit.com/api/search: returned an empty list for every keyword.
- Kailh datasheets for the tactile and clicky PG1353D types (Black Cloud, Hide Mountain) and for the Lofree-branded
  part numbers: not found.
- A Kailh statement of the recommended plate cut-out or plate thickness: not found in any drawing. The values in
  section 4 are derived from the body size and the hook gap.
- The exact part number of the switch in production GLYF units: not found. Only the family (PG1353D) is established.
- The reason for the "plastic plates only" note: not found.
- Socket availability at PCBWay and at other distributors: not checked.
