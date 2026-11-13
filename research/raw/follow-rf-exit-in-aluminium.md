# Follow-up: how 2.4 GHz leaves a body made of two aluminium shells

Date: 2026-11-13. Research key: `follow-rf-exit-in-aluminium`.

Cache root for this note: `research/_cache/follow-rf-exit-in-aluminium/` (short form `_cache/F/` below).
Paths that start with `_cache/` are relative to `research/`.

Confidence levels: **confirmed** (stated by the maker, or read or measured from a primary source such as an FCC
exhibit or a maker photo), **likely** (consistent indirect evidence), **guess**.

## 0. Answer in short

1. The reference device (GLYF) has no designed radio exit. Its radio module carries a ceramic chip antenna that
   sits at the right PCB edge, about 1 to 3 mm from a solid aluminium side wall. The PCB has a copper keep-out under
   the antenna. Neither shell has a slot, a window or a plastic insert near the module. (confirmed for the board and
   the shells as filmed; see sections 1 and 2)
2. Whatever signal leaves the GLYF leaves by leakage: through the seam between the two anodised shells, the display
   window, the 16 switch openings and the rear openings. Nobody has published a range figure, and the maker has made
   no range claim. (likely for the mechanism, confirmed for the missing data; see section 3)
3. Every commercial aluminium keyboard whose FCC internal photos were read has a designed exit. Keychron screws a
   separate antenna board over a slot in the rear wall and feeds it by coaxial cable. Even with that exit the measured
   antenna efficiency is only 18 to 27 percent (minus 5.7 to minus 7.4 dB). (confirmed; see section 4)
4. Decision for worxpad: do not copy the GLYF arrangement. Give the antenna a non-metal exit in the aluminium
   build. A module with an external-antenna connector is not an alternative to an exit. It is only a way to move the
   antenna to the exit. Section 6 ranks the options.

## 1. The radio module on the reference board

| Fact | Source | Confidence |
| --- | --- | --- |
| Module: Holyiot HOLYIOT-21069, Nordic nRF5340 (QKAA), FCC ID 2ALGY21069. | Shield marking in `_cache/youtube/frames-01/S9c5WuorsgQ/f023.jpg`; 1080p crop `_cache/F/02-hd-frames/pcb_013_module.png` | confirmed |
| Module size 19.0 x 13.5 mm. Pads occupy 1.5 to 14.7 mm from one short edge. The remaining 4.3 mm strip at the other short edge carries the antenna and has no pads. | Datasheet filed as FCC user manual, section 3.1, https://fccid.io/2ALGY21069 (`_cache/F/03-fcc-holyiot/5961970.pdf`, rendered `img/manual-08.png`) | confirmed |
| Antenna: a ceramic chip antenna on the module, not replaceable. Gain 1.0 dBi ("The best case gain of the antenna is 1.0dBi"). | FCC test report CTB220607047RF, sections 4.1 and 12 (`_cache/F/03-fcc-holyiot/5961966.pdf`); FCC internal photo with the "ANT" call-out (`5961963.pdf`, `img/internal-1.png`) | confirmed |
| Certified output: maximum conducted power minus 0.301 dBm (grant lists 0.00093 W), 2402 to 2480 MHz, Bluetooth 5.2, single modular approval. The nRF5340 can transmit at up to plus 3 dBm, so the module was certified below the chip maximum. | Grant text and test report, same filing | confirmed (grant), likely (chip maximum, from memory of the Nordic specification) |
| Grant condition: "Only those antennas tested with the device or similar antennas with equal or lesser gain may be used with this transmitter." | Grant comments, https://fccid.io/2ALGY21069 | confirmed |
| Maker's mounting rule: "the antenna of the area needs to extend about several mm without ground under the antenna of the edge of the host PCB." Second choice: module at a corner with the antenna outside the ground plane. The drawing marks antenna overhang as "best", antenna inside the ground plane as "bad". No clearance to a metal enclosure is given anywhere in the datasheet. | Datasheet section 4 (`img/manual-13.png`) | confirmed |
| No variant of the 21069 with an external-antenna connector is listed. The Holyiot module table in the same datasheet lists connector ("IPX") variants only for other chips, for example "YJ-18039-nRF52840: IPX antenna & PCB antenna". | Datasheet section 7 | confirmed (for this datasheet, dated 2022-04-07) |

## 2. How the maker placed the module, and what the shells show

### 2.1 Board

| Fact | Source | Confidence |
| --- | --- | --- |
| The module (U1) is on the bottom side of the PCB, at the right board edge (right as the user sees the device), under the rear half of the display. Its centre is about 27 mm from the rear board edge. The antenna end points at the right side wall and is flush with the board edge or overhangs it by about 1 mm. | `_cache/youtube/frames-01/S9c5WuorsgQ/f023.jpg`; `_cache/F/02-hd-frames/pcb_013_module.png`, `pcb_sheet.jpg` (from the 1080p TikTok copy dated 2025-12-30) | confirmed (side and edge), likely (27 mm, flush or 1 mm) |
| The KiCad layout ("GLYF V4 2025") has a hatched copper keep-out rule area at the right board edge under the antenna end. Scaled from the 2.5 mm encoder pin pitch (27.6 px per mm in the 2x crop) it is about 3.4 mm wide and 23.5 mm long. It starts just in front of the right encoder. The module is 13.5 mm wide, so the keep-out extends about 5 mm beyond each side of the antenna strip. | `_cache/youtube/crops-01/S9c5WuorsgQ-f044-kicad-2x.png`, `S9c5WuorsgQ-f046-kicad-2x.png` | confirmed (keep-out exists), likely (dimensions) |
| The maker therefore followed the module datasheet for the board. | Comparison of the two rows above with section 1 | confirmed |
| Gap between the antenna and the aluminium wall: the case is about 120 mm wide and the PCB is 112.5 mm wide. That leaves about 3.8 mm per side between the board edge and the outer face. With a 2 to 3 mm wall the board edge is 1 to 2 mm from the inner wall face. The chip antenna is therefore 1 to 3 mm from solid aluminium. | Widths from `research/raw/official-site.md` (section on the top-view drawing) and `research/raw/youtube.md` (112.5 mm dimension); wall thickness is an assumption | guess |

### 2.2 Shells

All frames below were checked for a slot, a window, a thinned wall or a part of another material near the right
wall and under the display.

| Image | What it shows | Result |
| --- | --- | --- |
| `_cache/official-site/03-media/files__Desktop_Size_Grid_1_46ae2ac8-...jpg` (exploded render, from the rear), crops `_cache/F/01-crops/exploded-left.png`, `exploded-display-pocket.png` | Top shell: display pocket with a through window and a glass ledge, two knob holes, two button holes. Bottom shell: closed tray, two notches in the rear wall (USB-C and slide switch). | No opening in the right wall. The narrow feature along the right side of the display pocket is the glass ledge, not a slot through the wall. |
| `_cache/official-site/03-media/files__Untitled_design_10.jpg`, crop `_cache/F/01-crops/edge-topshell-display.png` | Both shells on edge. | Same result. |
| `_cache/youtube/crops-01/LyKoZR8Q888-f012-015-019-021.jpg`; 1080p frames `_cache/F/02-hd-frames/ly_010_raw.png` (raw machined tray), `ly_019_tray.png` (anodised tray), `ly_sheet.jpg` (underside) | Real bottom shell, October 2025 samples. Closed floor, closed side walls, four screw bosses, pockets for battery and parts. Underside: four foot slots, no window. | No opening other than the two rear notches. |
| `_cache/youtube/crops-01/wLHIWHExL-k-f032-034-035-036.jpg`; `_cache/F/02-hd-frames/q6_003_pocket.png`, `q6_009_edge.png` (1080p, video `Q6CKpc6AK0o`, March 2026) | Real top shell from the inside and both shells edge on. | The display pocket has a deep notch on its front side for the display flex tail. The right wall is solid. |
| `_cache/youtube/crops-01/Nk6MD9QS8VA-f042-043-044-047.jpg`, `Nk6MD9QS8VA-f039-040-041-045.jpg` | Finished unit, rear edge and underside. | Rear edge: USB-C opening and slide switch only. Underside: solid aluminium with silicone feet. A split line between the shells runs around the whole body. |

Finding: as filmed between October 2025 and March 2026, the GLYF shells have no non-metal exit for the radio.
The maker also states that the device is "made fully out of aluminum besides the keycaps, knobs and buttons"
(maker comment, `research/raw/youtube.md`). Confidence: confirmed for the filmed samples. A later, unpublished
change to the shells cannot be excluded, because nothing was published after 2026-03-14.

### 2.3 What the maker has said about range

Nothing. All cached subtitles and comments were searched for "range", "antenna", "signal", "wireless" and
"Bluetooth" (`_cache/youtube/digest-01/*.txt`). The maker says the device has Bluetooth and never states a distance,
never shows a range test and never mentions the antenna or the case as a radio problem. No shipped unit and no
third-party test exists. Confidence: confirmed absence in the sources read.

## 3. How the signal can leave the GLYF anyway

This section is engineering reasoning, not a measurement. Wavelength at 2.44 GHz is 123 mm, so half a wavelength is
61 mm.

| Path | Size | Rule-of-thumb attenuation | Remark |
| --- | --- | --- | --- |
| Seam between the two shells | Runs around the whole perimeter (about 400 mm). Unbroken lengths between the four screw bosses are roughly 60 to 110 mm. | About 0 dB if the seam is not conductive, because each segment is at or above half a wavelength. | Both shells are anodised. Anodic oxide is an insulator, so the mating faces do not make metal-to-metal contact unless the maker masks them, and nothing suggests that. The antenna sits within a few millimetres of this seam. This is the most probable main exit. |
| Display through-window | About 27 x 30 mm, covered by glass | About 6 dB | The LCD module and the PCB lie between the antenna and the window, and small LCD modules usually have a metal backlight frame. Probably a weak path. |
| 16 switch openings | 14 mm squares | About 13 dB each, less in total because there are many | The PCB ground plane lies between the antenna and the openings. |
| USB-C opening, switch slot | About 9 x 3 mm each | About 17 dB | Far from the module. |

The rule used is the common worst-case slot formula SE = 20 log10(wavelength / 2L), valid for a slot length L up to
half a wavelength. Source: https://www.electronicdesign.com/home/article/21200214/shielding-the-hole-problem. The
statement that an insulating finish on mating faces turns a seam into an open slot comes from a vendor knowledge
base found by search and is standard practice in shielding design. The formula is a far-field rule. The antenna is
in the near field of the seam, so the real coupling can be better or worse. Confidence for the whole section: guess
for the numbers, likely for the conclusion that the seam is the main path.

Two consequences follow.

- A closed anodised two-shell case is not a sealed shield at 2.4 GHz. A link at desk distance is plausible. A
  free-space path at 2.44 GHz loses 40 dB at 1 m and 60 dB at 10 m. A Bluetooth LE link at 0 dBm with a receiver
  sensitivity near minus 95 dBm has about 95 dB of budget, so it tolerates 20 to 30 dB of enclosure loss at 1 to 2 m.
- The result is not controlled. A chip antenna 1 to 3 mm from a metal wall is detuned, and a module antenna cannot
  be retuned by the host designer. A Nordic forum answer gives the working rule: "you should keep metal parts > 5mm
  from the antenna" and "you can't compensate for detuning of the antenna by nearby metal"
  (https://devzone.nordicsemi.com/f/nordic-q-a/71797/placement-of-nrf-module-inside-enclosure-with-surrounding-metal-components,
  a single forum reply, confidence likely). The ZMK documentation names "a metal enclosure on the keyboard or host"
  as a cause of poor connections (https://zmk.dev/docs/troubleshooting/connection-issues, confirmed).

## 4. What shipping aluminium products do (FCC exhibits)

### 4.1 Keychron Q1 Max (FCC ID 2ASF4-Q1MAX), aluminium 75 percent keyboard

| Fact | Source | Confidence |
| --- | --- | --- |
| The antenna is a separate small PCB marked "HY-Q1PRO-BT-V01". Two screws hold it across a through slot in the rear wall of the aluminium top frame. The slot is longer than the board. A soldered coaxial cable feeds it. The exhibit labels it "Bluetooth/SRD Antenna". | FCC internal photos, Fig. 4, https://fccid.io/2ASF4-Q1MAX (`_cache/F/06-fcc-peers/2ASF4-Q1MAX/img/int-001.png`) | confirmed |
| The radio is a separate shielded module on the main PCB. The keyboard MCU is a different chip. | Same exhibit, Fig. 5 and 6 | confirmed (module), likely (separate MCU, consistent with the Q0 Max firmware facts in `prior-art.md`) |
| Measured antenna performance in the assembled keyboard (anechoic chamber, by the antenna design house): efficiency minus 6.33 to minus 5.66 dB (23.3 to 27.2 percent) from 2400 to 2480 MHz. Peak gain 1.2 to 2.83 dBi. | Exhibit "Antenna specification", dated 2023-10-30 (`Antenna-specification-7210790.pdf`, text in `.txt`) | confirmed |
| The test report lists "Integral Antenna / 3.09dBi(Max)". | BLE test report, same filing | confirmed |
| The slot is covered from outside by a colour-matched plastic piece. | Reviewer statement for the sister model Q1 Pro, already in `research/raw/prior-art.md` section 3.1; the FCC photo shows the slot but not the cover | likely |

### 4.2 Keychron Q0 Max (FCC ID 2BGKB-Q0MAX), aluminium number pad, the closest size class

| Fact | Source | Confidence |
| --- | --- | --- |
| Same construction on a small body. An antenna board with the same marking "HY-Q1PRO-BT-V01", about 31 x 10 mm, sits inside the bottom case against the rear wall, beside the port area. The exhibit labels it "Bluetooth antenna". | FCC internal photos, Fig. 4, https://fccid.io/2BGKB-Q0MAX (`_cache/F/06-fcc-peers/2BGKB-Q0MAX/img/int-001.png`) | confirmed (position and label), likely (size, scaled from the ruler in the photo) |
| A separate radio board "Q0 MAX RF 1.0" carries the radio module and a miniature coaxial connector marked "ANT". A cable links it to the antenna board. | Same exhibit, Fig. 5 (`img/int-002.png`) | confirmed |
| The rear face has a recessed panel around the mode switch and the USB-C socket. | FCC external photos, Fig. 3 (`img/ext-000.png`) | confirmed (panel visible), likely (that the panel is the plastic radio window) |
| Measured antenna performance in the assembled device: efficiency minus 7.41 to minus 7.07 dB (18.2 to 19.6 percent) from 2400 to 2480 MHz. Peak gain minus 0.45 to minus 0.04 dBi. | Exhibit "antenna Specifications" (`antenna-Specifications-7418241.pdf`) | confirmed |
| The test report lists "PCB Antenna, -0.04dBi". | Test report, same filing | confirmed |

### 4.3 Lofree Flow 84 (FCC ID 2AC59-OE915), low-profile aluminium keyboard

| Fact | Source | Confidence |
| --- | --- | --- |
| The antenna is a printed trace on the main PCB, 21.67 mm long, at a board edge beside a board cut-out, with a copper-free area around it. The radio chip is a Beken part. | FCC internal photos, page 7 ("Chip", "ANT"), https://fccid.io/2AC59-OE915 (`_cache/F/06-fcc-peers/2AC59-OE915/img/intp-7.png`); antenna specification exhibit | confirmed |
| Peak gain minus 1.66 dBi. Average gain minus 8.0 to minus 9.8 dBi (horizontal) and minus 10.6 to minus 13.5 dBi (vertical). Summing both polarisations gives an efficiency of about minus 6 to minus 8 dB. | Antenna specification exhibit (`Antenna-Specification-6641806.pdf`) | confirmed (table values), likely (the efficiency sum, and that the values were taken in the product) |
| The rear underside has a separate bar-shaped section that carries the switch and the USB-C socket. Reviews describe the case as aluminium, including the bottom. Which part is non-metal could not be read from the exhibit photos. | FCC external photos (`external-sheet.png`); review summaries found by search | not found (material of the bar section) |

### 4.4 Work Louder (Knob1, Creator Micro 2 Pro)

No filing found. The fccid.io full-text search for "Work Louder" returned 81 documents from unrelated companies and
the search for "Creator Micro" returned 62, none from this maker. Confidence: confirmed absence on this mirror on
2026-11-13. The official FCC search was not queried (it returned HTTP 403 to an earlier agent).

### 4.5 LP44 Split (open design, https://github.com/juncho26/LP44_Split)

| Fact | Source | Confidence |
| --- | --- | --- |
| The case is not all aluminium. The "Top" STEP part is the machined aluminium frame. The "Bottom" STEP part is a flat plate 102.2 x 81.8 x 1.8 mm. In the gallery photo the fitted bottom plate is white and translucent: the PCB holes show through it as grey shadows. It is held by four M2 screws. | STEP bounding boxes read from `_cache/F/05-lp44/LP_Split44-V2-L-Bottom.step`; `LP_Split44-V2-L-Thread.jpg`; gallery photo `g3.jpg` | confirmed (plate geometry and appearance), likely (non-metal; the README does not name the material) |
| The README says only "Case: CNC-machined aluminum" and gives no radio information. Controllers are two Seeed XIAO nRF52840 boards (BOM). | `README.md`, `bom.csv` in the same directory | confirmed |
| The LP44 Split therefore follows the rule: aluminium top, non-metal bottom. It is not an example of a radio inside closed aluminium. | Rows above | likely |

### 4.6 Summary of the evidence

| Device | Body | Antenna | Exit | Measured efficiency |
| --- | --- | --- | --- | --- |
| Keychron Q1 Max | Aluminium top and bottom | Separate PCB antenna, coax-fed | Slot in rear wall | minus 5.7 to minus 6.3 dB |
| Keychron Q0 Max | Aluminium top and bottom | Separate PCB antenna, coax-fed | Rear wall at the port panel | minus 7.1 to minus 7.4 dB |
| Lofree Flow 84 | Aluminium | PCB trace at board edge | Not identified | about minus 6 to minus 8 dB |
| LP44 Split | Aluminium top | XIAO nRF52840 on-board antenna | Non-metal bottom plate | not measured |
| GLYF | Aluminium top and bottom | Ceramic chip antenna on module | None designed | not measured |

Design consequence: even a deliberately engineered exit in an aluminium body costs 6 to 8 dB against an ideal
antenna. A design with no exit starts below that. The exit is not optional for a product that claims multi-host
Bluetooth at room range.

## 5. Module variants with an external-antenna connector

| Fact | Source | Confidence |
| --- | --- | --- |
| Nordic's third-party module list shows the Holyiot 21069 only with a ceramic antenna, and the Holyiot 20046 (nRF5340) with a PCB antenna. No Holyiot nRF5340 module with a connector was found. | Search summary of https://www.nordicsemi.com/Nordic-Partners/3rd-party-modules | likely |
| nRF5340 modules with a miniature coaxial connector exist from other makers: Raytac MDBT53-U1M and Fanstel BT40E (14 x 16 x 2.0 mm). | Same search summary and distributor listings | likely |
| nRF52840 modules with a connector: Raytac MDBT50Q-U1MV2, Fanstel BT840E, Holyiot 18039 (connector plus PCB antenna). | Search summary; Holyiot datasheet section 7 | likely |
| Availability of any of these in the JLCPCB assembly library was not checked. | - | not found |
| An external antenna inside a closed aluminium shell gains nothing by itself. The Keychron filings show the real use: the connector lets the antenna sit at the wall slot while the radio stays on the PCB. It adds a cable, a hand-assembly step and an antenna part that the assembly house cannot fit. | Section 4.1 and 4.2 | confirmed (Keychron construction), likely (assembly consequence) |
| For a module certified with its own chip antenna, fitting a different antenna type falls outside the module grant. This matters only if the owner wants to rely on the module's certification. | Grant condition in section 1 | confirmed (condition), likely (interpretation) |
| Firmware lever: ZMK exposes `CONFIG_BT_CTLR_TX_PWR_PLUS_8` for the nRF52840 (default 0 dBm, up to plus 8 dBm). The page says "the power consumption difference is negligible". The nRF5340 stops at plus 3 dBm. This is an argument for the nRF52840 in a metal body. It helps transmit only. | https://zmk.dev/docs/troubleshooting/connection-issues | confirmed (option and range), likely (nRF5340 limit, from memory) |

## 6. Options for worxpad, ranked

The FDM prototype case is plastic and is transparent to 2.4 GHz. It will work with any antenna position and will
not reveal the problem. The aluminium build needs its own range test. Avoid carbon-fibre-filled filament around the
antenna if the prototype is meant to predict anything (engineering judgement, no source).

| Rank | Option | Evidence | Cost and risk |
| --- | --- | --- | --- |
| 1 | **Wall slot with a plastic insert, on-board module antenna directly behind it.** Put the module so that its antenna strip lies along the rear wall (or the right wall) and cut a through slot in the wall in front of it. Close the slot with a printed or machined plastic insert, colour-matched. Keep the PCB copper keep-out as the GLYF does. | Keychron Q1 Max and Q0 Max (section 4), Keychron Q1 Pro review (`prior-art.md`). | One extra milled feature and one small plastic part. No cable, so JLCPCB can place the whole radio. Starting dimensions (guess, to be tested): slot at least 30 mm long and 3 mm high, longer is better because a slot shorter than 61 mm is still below half a wavelength; antenna within 5 mm of the insert; no aluminium within 5 mm of the antenna on the other sides. The rear wall already has the USB-C and switch openings, so the insert can be one part that frames all three. |
| 2 | **Non-metal bottom.** Aluminium top shell with the integrated plate, bottom tray in plastic (printed for the prototype, machined POM or polycarbonate, or moulded later). | LP44 Split (section 4.5), NuPhy Air75 V2 (`prior-art.md`). | Lowest radio risk and the cheapest machining, because only one aluminium part remains. Loses mass and the all-metal feel. The antenna radiates down and sideways into the desk. A steel or aluminium weight can restore mass if it stays away from the antenna. |
| 3 | **Exit through the display cover glass.** Extend the glass pocket over the antenna keep-out so that the antenna sits under the black-printed border of the cover lens, with no aluminium above it. | No prior art found in this research. Ordinary black ink on glass is not conductive. | No visible plastic part. Needs the antenna strip under the pocket and a cut in the top shell there, and ties the radio position to the display position. Untested idea. Confidence: guess. |
| 4 | **Module with a coaxial connector plus a flexible or PCB antenna at the slot.** | Keychron (section 4). | Use only if the module cannot be placed at a wall. Adds a cable and hand assembly. Still needs option 1 or 2 for the exit. |
| 5 | **Copy the GLYF: closed shells, rely on leakage.** | No range data exists for it. | Not recommended. If it is chosen anyway, do not mask the anodising on the mating faces and keep the antenna beside the seam. |

Additional rules that apply to every option:

- Keep the module antenna at a board edge with a copper keep-out in all layers, at least 3.4 mm deep and 5 mm
  beyond each side of the antenna strip (the GLYF values in section 2.1).
- Keep the battery, the display frame and screw bosses out of the 5 mm zone around the antenna.
- Leave the transmit power configurable and test the aluminium build at 0 dBm and at the chip maximum.
- Acceptance test for the aluminium build: stable link to a laptop and a phone at 3 m with a hand over the device,
  and RSSI compared with the bare PCB at the same distance. A loss of more than about 10 dB against the bare PCB
  means the exit is too small or the antenna is detuned.

## 7. Sources read

- https://fccid.io/2ALGY21069 (Holyiot 21069: grant, test report, user manual and datasheet, internal and external photos)
- https://fccid.io/2ASF4-Q1MAX (Keychron Q1 Max: internal photos, external photos, antenna specification, BLE test report)
- https://fccid.io/2BGKB-Q0MAX (Keychron Q0 Max: internal photos, external photos, antenna specification, test report)
- https://fccid.io/2AC59-OE915 (Lofree Flow 84: internal photos, external photos, antenna specification, test report)
- https://fccid.io/2BGKB, https://fccid.io/2ASF4, https://fccid.io/2AC59 (grantee listings)
- https://fccid.io/search.php (queries "Work Louder", "Creator Micro")
- https://github.com/juncho26/LP44_Split (README, BOM, two STEP files, thread drawing, three gallery photos)
- https://zmk.dev/docs/troubleshooting/connection-issues
- https://devzone.nordicsemi.com/f/nordic-q-a/71797/placement-of-nrf-module-inside-enclosure-with-surrounding-metal-components
- https://www.electronicdesign.com/home/article/21200214/shielding-the-hole-problem
- Search summaries only: Nordic third-party module list, Microchip, Infineon and Murata module placement notes
  (clearances of 3 to 15 mm between antenna and metal), reviews of the Lofree Flow 84 case material.
- Existing notes: `research/raw/prior-art.md`, `youtube.md`, `social.md`, `official-site.md`, `regulatory-software.md`.
- Cached images and videos listed in section 2, including 1080p frames re-extracted from
  `_cache/geometry/yt-hd-01/LyKoZR8Q888.mp4`, `_cache/geometry/yt-hd-01/Q6CKpc6AK0o.mp4` and
  `_cache/social/tiktok-videos-hd-01/20251230_7589532575031381279.mp4`.

## 8. Not reached

- https://www.answeroverflow.com/m/1417715438372126720 (ZMK thread on aluminium cases): HTTP 429 again, by curl and
  by WebFetch. The Wayback Machine has no snapshot. Only the earlier search summary in `prior-art.md` exists.
- https://e2e.ti.com/support/wireless-connectivity/bluetooth-group/bluetooth/f/bluetooth-forum/327200/chassis-antenna: HTTP 403.
- https://community.element14.com/.../pan1770-ble-data-throughput-rate-and-metal-enclosures-...: timed out. It
  reportedly contains a measured comparison of a module inside and outside a metal enclosure.
- FCC filings for Work Louder: none found on the mirror. The official FCC search was not tried.
- Any measurement of the GLYF radio: none exists in public.
- The material of the Lofree Flow 84 rear bar section and the plastic cover of the Keychron slots: not visible in
  the FCC photos.
- JLCPCB or LCSC stock for connector-type nRF modules: not checked.

## 9. Cache directories

- `_cache/follow-rf-exit-in-aluminium/01-crops/` (crops of cached renders and frames)
- `_cache/follow-rf-exit-in-aluminium/02-hd-frames/` (1080p frames re-extracted from cached videos)
- `_cache/follow-rf-exit-in-aluminium/03-fcc-holyiot/` (FCC exhibits for 2ALGY21069)
- `_cache/follow-rf-exit-in-aluminium/04-community/` (failed thread fetch, LP44 file listing)
- `_cache/follow-rf-exit-in-aluminium/05-lp44/` (LP44 Split files; the gallery JPEG originals carry EXIF location data and must stay in the cache)
- `_cache/follow-rf-exit-in-aluminium/06-fcc-peers/` (FCC exhibits for Keychron and Lofree, search pages)
