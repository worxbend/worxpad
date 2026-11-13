# Decision record: USB-C, protection, debug, indicators and small I/O (key `usb-io`)

Status: decided, revision 2, 2026-11-13.
Scope: USB-C receptacle, CC resistors, ESD protection, VBUS fuse, shield and case grounding, SWD access,
reset button and bootloader entry, power slide switch, status LED, test points, mounting-hole rules and the
dock question.
Settled inputs: `research/components/mcu-radio.md` (BMD-340, USB on module pads 66/67/68, reset P0.18 on pad
39, SWD pads 43/44, single-side assembly on the PCB bottom face) and `research/components/keys.md` (PCB 1.6 mm,
bottom face at Z -7.80, top face at Z -6.20, deck at Z 0, all SMD on the bottom face).
Other records read for interfaces: `enclosure-manufacturing.md` (revision 1), `power.md` (revision 1),
`rotary-buttons.md` (revision 2).

## 0. Revision 2: what changed and why

A reviewer challenged revision 1. Each point was checked against the primary drawing or record:

| # | Reviewer point | Check | Result |
| --- | --- | --- | --- |
| 1 | The M-13B board notch is 6.70 mm deep, not 5.70; the shell front is flush with the PCB edge, not 0.8 mm past it | HRO M-13B layout re-rendered at 600 dpi. The front slot centre is 2.10 from the line marked "P.C.B EDGE"; from that centre the drawing gives 4.00 to the rear slot, 4.60 to the notch end and 5.70 to the outer end of the signal pads. The side view gives the front leg 2.10 from the shell front. The M-13C drawing has the same layout. | **Reviewer right.** Notch 2.10 + 4.60 = 6.70 mm. Shell front flush with the PCB edge. Section 6.1 corrected. |
| 2 | With a 3.5 mm wall and 0.45 mm gap the receptacle front sits 3.95 mm behind the face; the fix needs a wall pocket and a PCB tongue | Arithmetic from `enclosure-manufacturing.md` 6.5 and USB Type-C R2.0 figure 3-80 (product surface at the receptacle front, 0.05 mm minimum gap to the overmold). | **Reviewer right.** Revision 2 adds a local PCB tongue, a notch through the wall and a 0.6 mm skin with an inner pocket (6.1, 6.2). |
| 3 | Case bonding through clamped plated holes contradicts the enclosure (NPTH Ø4.0, standoffs pass through and carry no load) | `enclosure-manufacturing.md` 6.4 items 3 and 6, 6.5. | **Reviewer right.** The boss-face scheme is dropped. A dedicated ground screw G1 into a bare tapped hole of the top shell replaces it (4.4, 6.4). The six enclosure standoff holes stay NPTH. |
| 4 | The enclosure makes every side opening a notch from the split face; then the 0.67 mm bridge reason against M-13C falls away | `enclosure-manufacturing.md` 5 ("Undercuts") and 6.5. | **Reviewer right.** The opening is now a notch from the split face, wholly in the bottom shell, and the receptacle changes to **M-13C** (C2848620): deeper stock, shell ends 0.58 mm higher, more metal under the opening (4.1). |
| 5 | The 0.70 dimension in the M-13B front view could put the contact centre at 0.70, not 0.60, from the mounting face | Front view at 600 dpi: the 0.70 arrows end on the wing seat line and on the leg tips, not on the centre line of the 2.56 cavity. The same 0.70 appears at the same place on the M-13C drawing. It is the leg length into the board. Pixel ratio in the M-13B front view gives 0.62 mm from seat to cavity centre, against 0.60 from the side view. | **Reviewer wrong on this point.** The centre stays 1.58 - sink. With M-13C the sink is 1.60, so the centre lies 0.02 mm inside the board face. |
| 6 | Several cited local datasheets are empty files or HTML wrappers | `file` on the cache: `ds-06/*` are 0 bytes and `ds-10/*` are HTML pages, as stated. But `ds-11/` holds the real PDFs (USBLC6-2SC6 14 pages, MSK12C02 7 pages, MSK12C02G15-B drawing, TS-1187A, LTST-S270, nSMD075, PCM12) and `ds-13/1206l.pdf` (136 pages). Revision 1 cited `ds-11` and `ds-13`, not `ds-10`. | **Partly right.** The numbers came from `ds-11`; the USBLC6 values (3.5 pF max, VRM 5.25 V, 1.2 to 1.7 pF line to line) and the MSK12C02 rating (12 V DC 50 mA, full travel 1.6 +/-0.2 mm) are re-read there. The MSK12C02 PDF has no outline drawing, so the actuator length stays uncertain (1.4 in `power.md` and LCSC, 1.6 in the JLCPCB listing); 6.6 now allows for both. `ds-06` and `ds-10` are not cited. |
| 7 | `CONFIG_GPIO_AS_PINRESET` is deprecated; use the devicetree property | Zephyr binding `nordic,nrf-uicr` has `gpio-as-nreset`. | **Reviewer right.** 6.5 corrected. |
| 8 | PTC hold current derates with temperature | Littelfuse 1206L datasheet, `ds-13/1206l.txt` line 112: 1206L075TH holds 0.75 A at 20 °C, 0.65 at 40, 0.59 at 50, 0.54 at 60, 0.49 at 70 °C. | **Reviewer right on derating.** The budget changes too: `power.md` caps the charger input at USB500 (500 mA max), so VBUS draws at most about 0.51 A. The 0.75 A part still holds up to about 60 °C inside the case. Kept, with the derating stated (4.3, 6.2). |
| 9 | Stock and identity confirmed | Re-read live 2026-11-13 for C2848620 (4,695), C2848619 (2,562), C99563 (10,807), C431540 (172,615) in `_cache/usb-io/jlc-15/`. | Agreed. |

Two further changes come from records written after revision 1:

- **Status LED removed.** `power.md` section 1 item 7 routes the charger /CHG and /PGOOD outputs to GPIOs with
  internal pull-ups to 3.3 V and decides "no LED". An LED from VBUS into the same open-drain node would pull the
  GPIO towards about 3 V while the slide switch holds VDD at 0 V, which back-feeds the nRF through its input
  protection. Charge state shows on the display. This also removes one hole from the aluminium.
- **Encoder clash resolved.** `rotary-buttons.md` section 7 item 3 asks usb-io to keep the receptacle wholly
  behind the encoder bodies (less than 8.2 mm from the rear outer face). The receptacle in revision 2 ends 6.75 mm
  from the face, and its notch ends at 6.95 mm (6.1).

## 1. Summary

1. USB-C receptacle: HRO TYPE-C-31-M-13C (LCSC C2848620), a 16-pin mid-mount receptacle with a 1.60 mm sink,
   placed on the PCB bottom face in a 9.24 x 6.70 mm board notch at the rear edge, on a local PCB tongue that
   brings the shell front to 0.25 mm behind the outer rear face. Contact centre line at Z -7.82. Case opening:
   10.0 mm wide notch from the split face, Z -5.00 to -9.90, wholly in the bottom shell, with an inner pocket and
   a 0.6 mm skin either side. Runner-up: TYPE-C-31-M-13B (C2848619), same footprint, needs the notch to Z -10.30.
2. CC: two 5.1 kOhm 1 % 0402 resistors (C25905, basic), one per CC pin, to GND.
3. ESD: STMicroelectronics USBLC6-2SC6 (C7519) at the connector, on D+, D- and VBUS.
4. Fuse: Littelfuse 1206L075THYR PTC (C99563), 0.75 A hold at 20 °C (0.54 A at 60 °C), 1.50 A trip, 8 V,
   after the ESD clamp. The charger input limit (500 mA max, `power.md`) keeps the load below the hold current.
5. Shield: receptacle shell slots straight to GND. Case: one dedicated M2 ground screw (G1) from the PCB
   bottom face into a bare tapped boss of the top shell; the screw head bears on an exposed GND ring. No RC
   network, no bare boss faces, enclosure standoff holes unchanged (NPTH).
6. SWD: Tag-Connect TC2030-NL footprint (stock KiCad) on the bottom face; the pads also take pogo pins or wires.
7. Reset: XKB TS-1187A-B-A-B tact switch (C318884, basic) on the bottom face, pressed through a 1.5 mm pinhole
   in the floor. Double reset within 500 ms enters the UF2 bootloader. A keymap `&bootloader` binding is the
   everyday route. P0.18 reset is set by `gpio-as-nreset` on `&uicr`.
8. Power switch: SHOU HAN MSK12C02 side-actuated SPDT (C431540), rated 50 mA, on the LDO enable pin as settled
   in `power.md`. Opening: the same 10.0 mm notch style, Z -5.00 to -9.90; a local PCB tongue puts the actuator
   tip 0.3 to 0.5 mm behind the outer face.
9. Status LED: none (aligned with `power.md`). Charge state shows on the display.
10. Dock: none. The research shows the GLYF has no dock (`research/raw/geometry.md`, "Dock or base plate").
    No pogo pads or magnets are added.

## 2. Context

The GLYF puts USB-C and a slide power switch on the rear wall, each in a 10.0 x 4.3 mm stadium aperture
centred on the shell split line 5.0 mm below the top face, USB-C 19.6 mm and the switch 37.5 mm from the
right edge (`research/raw/geometry.md` rows "USB-C aperture", "Slide switch"; likely). The maker's board shows
a SOT-23-6 part (U5) beside fuse F1 behind USB-C, probably a USB ESD array, a side-actuated MSK12C02-type
slide switch, a reset button and SWD pads (`research/raw/follow-maker-bom-part-numbers.md`; guess for U5,
likely for the switch). The GLYF board is assembled at JLCPCB with all SMD parts on the bottom face
(`research/raw/youtube.md`; confirmed by maker footage).

The worxpad differs in four ways that matter here:

1. The settled stack puts the PCB lower than the GLYF split: PCB top face Z -6.20, bottom face Z -7.80
   (`keys.md` section 6.3). A part on the bottom face hangs below Z -7.80.
2. Single-side assembly: every SMD part sits on the bottom face (`keys.md`, `mcu-radio.md` section 9).
3. The body is 8.0 mm wider on the right for the RF bay (`mcu-radio.md`). The rear-wall ports keep their
   position relative to the knob pair, so they move 8.0 mm away from the right edge.
4. The enclosure has 3.5 mm walls and keeps the general PCB outline 0.45 mm or more from the inner wall, so the
   general board edge is 3.95 mm behind the outer face (`enclosure-manufacturing.md` 6.5). Every side opening
   is a notch cut from the split face at Z -5.00 (`enclosure-manufacturing.md` 5, "Undercuts").

## 3. Requirements

| ID | Requirement | Source |
| --- | --- | --- |
| U1 | USB 2.0 full speed device, USB-C receptacle, 5 V sink, default USB power only (no PD). | task; `mcu-radio.md` R2 |
| U2 | Receptacle on the PCB bottom face (single-side assembly). | `keys.md`, `mcu-radio.md` |
| U3 | Receptacle front 0.0 to 0.3 mm behind the outer rear face, so that every cable plug seats fully. | USB Type-C R2.0 section 3.10.3, figure 3-80 (product surface at the receptacle front, 0.05 mm minimum to the overmold); 0.3 mm limit is judgement |
| U4 | Rear-wall opening as a notch from the split face (two setups per shell), leaving at least 1.2 mm of aluminium under it. | `enclosure-manufacturing.md` 5; judgement |
| U5 | ESD protection at the connector to IEC 61000-4-2 level 4 on the data pair and VBUS. | task; common practice |
| U6 | Overcurrent protection on VBUS that holds the worst-case input (charger USB500 limit 500 mA max plus the module's VBUS sense) at the expected internal temperature. | `power.md` P3 and section 7; Littelfuse derating |
| U7 | CC pull-downs so that a USB-C source turns VBUS on. | USB Type-C specification Release 2.0 (Rd = 5.1 kOhm) |
| U8 | Programming access for one SWD session per board (bootloader load) and for debugging, with no part fitted. | `mcu-radio.md` section 9 |
| U9 | Bootloader entry without opening the case. | task |
| U10 | Power switch reachable on the rear wall; it drives the LDO enable only. | `power.md` section 8 |
| U11 | Receptacle and notch wholly behind the encoder bodies: less than 8.2 mm from the rear outer face. | `rotary-buttons.md` 7 item 3 |
| U12 | Anodised case bonded to GND without clamping the PCB at the enclosure standoffs. | `enclosure-manufacturing.md` 6.4 item 6; judgement on ESD |
| U13 | Every part placeable by JLCPCB, except where noted. | task |

## 4. Candidates

Stock, class and price were read from the JLCPCB parts API on 2026-11-13 (files under
`research/_cache/usb-io/jlc-01`, `jlc-07`, `jlc-08`, `jlc-09`, `jlc-14`, `jlc-15`, and the reviewer's
`sceptic-stock-01`). "ext" means extended part.

### 4.1 USB-C receptacle

Heights are for the part mounted on the PCB bottom face, in the deck frame (Z 0 at the deck, PCB bottom face
Z -7.80, top face Z -6.20). "Sink" is how far the shell reaches into the board from the mounting face. The
notch column is the opening needed with 0.5 mm clearance under the shell, cut from the split face at Z -5.00.

| Part | LCSC | Class, stock, price | Shell (W x H) | Sink | Centre line, Z | Shell span, Z | Notch Z (from split) | Metal under notch (wall to Z -12.0) | KiCad 10 footprint | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HRO TYPE-C-31-M-12 (top mount) | C165948 | ext, 537,821, USD 0.187 | 8.94 x 3.26 | 0 | -9.43 | -7.80 to -11.06 | -5.00 to -11.56 | 0.44 | yes | rejected: the opening nearly cuts through the wall bottom |
| **HRO TYPE-C-31-M-13C (sink 1.60)** | **C2848620** | **ext, 4,695, USD 0.266** | 8.94 x 3.16 | 1.60 | -7.82 | -6.20 to -9.36 | **-5.00 to -9.90** | **2.10** | no, draw | **chosen** |
| HRO TYPE-C-31-M-13B (sink 0.98) | C2848619 | ext, 2,562, USD 0.242 | 8.94 x 3.16 | 0.98 | -8.40 | -6.82 to -9.98 | -5.00 to -10.48 | 1.52 | no, draw | runner-up: same layout and notch, 1.8 mm of dark gap above the shell in the opening, less stock |
| Hanxia HX TYPE-C 16P CB1.6 | C5178543 | ext, 4,161, USD 0.100 | 8.94 x 3.16 | 1.60 | -7.82 | -6.20 to -9.36 | -5.00 to -9.90 | 2.10 | no | rejected: rated 5,000 cycles against 10,000; its layout was not re-checked for the flush-front question |
| HRO TYPE-C-31-M-14 (sink 1.1) | C223907 | ext, 2,768, USD 0.364 | 8.94 x about 3.26 | 1.10 | about -8.33 | -6.70 to -9.96 | -5.00 to -10.46 | 1.54 | no | rejected: rated 1.0 A on VBUS, dearer, no gain |
| Hirose CX90M-16P | C2889324 | ext, 1,731, USD 0.985 | 8.34 opening, 2.96 high | about 1.36 | -7.92 | -6.44 to -9.40 | -5.00 to -9.90 | 2.10 | no | fallback only: four times the price; its front overhang and notch were not re-checked in revision 2 |

Revision 1 rejected M-13C because a stadium opening centred on its contact line left 0.67 mm of aluminium
between the split line and the opening. Under the enclosure rule the opening is a notch that starts at the split
face, so that bridge does not exist (reviewer point 4). Against M-13B, M-13C then wins on three counts: its shell
top is flush with the PCB top face, so the opening shows only 1.2 mm of gap above the shell instead of 1.8 mm; its
shell ends at Z -9.36 instead of -9.98, which leaves 2.1 mm of wall under the notch instead of 1.5 mm; and JLCPCB
holds 4,695 against 2,562. It costs USD 0.024 more. Both parts share the board notch, pads and slot positions;
only the slot lengths differ (M-13C front slots 1.80, rear 1.40; M-13B front 1.60, rear 1.20).

Mounting the receptacle on the bottom face turns it 180 degrees about its insertion axis. The USB-C pin-out
is symmetric under that turn (A1 to B1 and so on), and KiCad mirrors the pad numbers with the footprint, so
the netlist does not change (confirmed from the HRO pin table; the electrical claim is likely).

The top-side alternative (M-12 on the PCB top face, centre line Z -4.57, opening on the split line like the
GLYF) needs a second assembly side. It is rejected because it breaks the single-side rule in `keys.md` and
`mcu-radio.md`.

### 4.2 ESD protection

| Part | LCSC | Class, stock, price | Lines | I/O capacitance | VBUS clamp | Package | KiCad symbol / footprint | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ST USBLC6-2SC6 | C7519 | ext, 43,069, USD 0.157 | 2 data + VBUS | 3.5 pF max line to GND; 1.2 to 1.7 pF line to line (`ds-11/usblc6.pdf`) | yes, VRM 5.25 V | SOT-23-6 | yes / yes | **chosen**; original maker; same package as the GLYF U5 |
| TECH PUBLIC USBLC6-2SC6 | C2827654 | ext, 214,122, USD 0.045 | as above | 0.35 pF (JLC listing) | yes | SOT-23-6 | yes / yes | fallback, pin compatible; second-source datasheet not checked |
| TI TPD4E05U06DQA (TECH PUBLIC) | C2827646 | ext, 38,214, USD 0.072 | 4, no VBUS rail | 0.3 to 0.6 pF (JLC listing) | no | USON-10 1.0 x 2.5 mm | yes / yes | rejected: VBUS needs a second part; fine-pitch USON |
| Nexperia PRTR5V0U2X (TECH PUBLIC) | C2827688 | ext, 132,438, USD 0.063 | 2 data + VBUS | 0.3 to 0.8 pF (JLC listing) | yes | SOT-143 | yes / yes | rejected: no advantage over USBLC6 at 12 Mbit/s |
| SRV05-4 (Semtech) | C13612 | ext, 59,891, USD 0.157 | 4 + VBUS | 3 pF | yes | SOT-23-6 | not checked | rejected: same function as USBLC6, no gain |

At USB full speed (12 Mbit/s) any of these capacitances is harmless; the choice is on VBUS clamping, single
part count and maker documentation.

### 4.3 VBUS fuse

Load: the BQ24072 input limit in USB500 mode is 450 / 475 / 500 mA min/typ/max (`power.md` section 7,
confirmed there), plus a few milliamperes into module pad 66. Worst case about 0.51 A.

| Part | LCSC | Class, stock, price | Hold / trip at 20 °C | Hold at 40 / 50 / 60 °C | Vmax | R min / R1 max | Size | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Littelfuse 1206L075THYR | C99563 | ext, 10,807, USD 0.054 | 0.75 / 1.50 A | 0.65 / 0.59 / 0.54 A | 8 V | 0.090 / 0.290 Ohm | 1206, 0.40 to 0.75 mm thick | **chosen**: holds 0.51 A up to about 60 °C |
| TECHFUSE nSMD075 | C70078 | ext, 10,254, USD 0.040 | 0.75 / 1.50 A | not read | 6 V | 0.090 / 0.500 Ohm | 1206 | rejected: R1 max 0.5 Ohm drops up to 0.25 V at 0.5 A |
| TECHFUSE nSMD050 | C69688 | ext, 20,179, USD 0.042 | 0.50 / 1.00 A | below 0.5 A | 6 V | 0.15 / 0.70 Ohm (JLC listing) | 1206 | rejected: hold below the load |
| Bourns MF-PSMF050X-2 | C116170 | ext, 15,751, USD 0.039 | 0.50 A | below 0.5 A | 6 V | 0.15 / 0.90 Ohm (JLC listing) | 0805 | rejected: hold and resistance |
| No fuse | none | none | none | none | none | none | none | rejected: a shorted cell path or charger fault would load the host port |

The JLCPCB listing gives 16 V for C99563; the Littelfuse datasheet gives 8 V for the "TH" variant
(`ds-13/1206l.txt` line 67). The datasheet value is used. 8 V covers a 5 V default-power source; the charger
survives 26 V behind it (`power.md`), but the PTC does not, so a faulty 9 V+ source is outside the design.

### 4.4 Case and shield grounding

| Option | Parts | Verdict |
| --- | --- | --- |
| **Ground screw G1**: M2 x 4 button-head screw (ISO 7380) from the PCB bottom face through a plated Ø2.2 hole with an exposed GND ring, into a tapped boss of the top shell. Threads below M5 are left bare by JLCCNC's blasting plug rule, so the thread bonds the shell; the screw head bonds the ring. | one screw, one boss | **chosen**: no bare-face masking, no clamping at the enclosure standoffs, stock KiCad footprint `MountingHole:MountingHole_2.2mm_M2_ISO7380_Pad` |
| Bare boss faces clamping plated GND rings at the case screws (revision 1) | none | rejected: the enclosure standoffs pass through NPTH Ø4.0 holes and clamp nothing (`enclosure-manufacturing.md` 6.4 item 6) |
| Make one enclosure standoff clamp the PCB (stop at the PCB top, bottom boss below) | none | rejected: the case screw only passes through a clearance hole, so contact to the PCB copper is not guaranteed unless a boss face is made bare after anodising |
| SMD grounding spring finger on the PCB bottom pressing a laser-cleared spot on the floor | spring finger | rejected for batch 1: no stocked spring finger in the JLCPCB library. Searches "spring finger", "EMI finger", "grounding spring", "shield contact", "SMT spring contact": zero stocked results or customer records only. "S1751-46R" (Harwin, C3345122, 5,533) is listed as a test point, not checked as a spring (`jlc-14`). It would also bond only the bottom shell. |
| Shell to GND through 1 MOhm parallel 4.7 nF | two 0402 parts | rejected: this network separates chassis and logic ground in mains-referenced products; a battery and bus-powered pad has no such loop |
| Leave the anodised case floating | none | rejected: an 8 kV discharge that breaks through the anodise to a floating shell arcs on to the nearest conductor inside (switch sockets 2.2 mm under the plate, encoder frames); a bonded top shell gives it a defined path |

The bottom shell is held by the six countersunk case screws, whose threads sit bare in the top-shell standoffs and
whose heads lie exposed on the underside. The bottom shell therefore touches GND only through the thin anodise of
the countersinks (guess: it breaks down well below ESD levels). No separate bond is planned for it.

### 4.5 SWD access

| Option | Board cost | Tool cost | Verdict |
| --- | --- | --- | --- |
| Tag-Connect TC2030-NL footprint (6 pads at 1.27 mm, 3 NPTH alignment holes) | copper only | TC2030-IDC-NL cable, owner may own one (not checked) | **chosen**; stock KiCad footprint `Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical` (also fetched upstream by the reviewer, `sceptic-kicad-03/tc.kicad_mod`, 6 pads, 3 NPTH) |
| Five 1.27 mm test pads in a row for a pogo jig | copper only | 3D-printed pogo jig | fallback; the TC2030 pads already serve |
| 2 x 5 1.27 mm Cortex header | header part, height on the bottom face | standard cable | rejected: a 2.0 mm-tall part under the PCB and an extra part |

### 4.6 Reset button

| Part | LCSC | Class, stock, price | Size | Verdict |
| --- | --- | --- | --- | --- |
| XKB TS-1187A-B-A-B | C318884 | **basic**, 815,200, USD 0.022 | 5.1 x 5.1 x 1.5 mm, 2.0 mm plunger, 160 gf, 0.25 mm travel (`ds-11/ts1187a.pdf`, image PDF; JLC attributes agree on 5.1 x 5.1 x 1.5 mm, 1.6 N, 50 mA 12 V) | **chosen** |
| JXTCONN TS-1187A-S16 | C42420254 | ext, 55,192, USD 0.020 | 5.2 x 5.2 mm | rejected: extended fee for the same part |
| XKB TS-1187A-C-E-B | C318887 | ext, 78,124, USD 0.039 | 5.1 x 5.1 x 2.5 mm | rejected: taller, extended |
| No button, keymap only | none | none | rejected as sole route: a bad firmware image leaves only SWD |

### 4.7 Power slide switch

The switch part and its circuit belong to `power.md` (MSK12C02 on the LDO enable). This record only sets its
placement and opening. Candidates as in revision 1:

| Part | LCSC | Class, stock, price | Rating | Size | KiCad footprint | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| SHOU HAN MSK12C02 | C431540 | ext, 172,615, USD 0.054 | 12 V DC, 50 mA; full travel 1.6 +/-0.2 mm (`ds-11/msk12c02.pdf` sections 2.5 and 4.2) | 6.7 x 2.8 x 1.4 to 1.5 mm body; actuator 1.3 mm wide, 1.4 (LCSC, `power.md`) or 1.6 mm (JLC listing) past the body | yes, `Button_Switch_SMD:SW_SPDT_Shouhan_MSK12C02` | **chosen**, as settled in `power.md` |
| HanElectricity MSK12C02G15-B | C22435661 | ext, 28,084, USD 0.028 | 12 V DC, 0.1 A; 160 +/-50 gf (`ds-11/msk12c02g15.pdf`) | actuator height option "15" = 1.5 mm | no | fallback: has a drawing, needs a drawn footprint |
| C&K PCM12SMTR | C221841 | ext, 8,748, USD 1.270 | 0.3 A at 6 V DC | ultraminiature | yes, `SW_SPDT_PCM12` | rejected: 23 times the price; not needed on an enable line |
| No switch, ZMK soft off | none | none | none | none | none | rejected as sole route: the GLYF has a switch; a hard off is wanted for shipping (`power.md` 8) |

### 4.8 Status LED

| Option | Part | Verdict |
| --- | --- | --- |
| No LED; charge state on the display from /CHG and /PGOOD | none | **chosen** (aligned with `power.md` 1 item 7) |
| Side-view LED on charger /CHG through 1 kOhm, rear-wall hole (revision 1) | Lite-On LTST-S270KGKT, C125113, ext, 45,674, USD 0.027 (30 mA DC max, `ds-11/ltst-s270.txt` lines 64-84) | rejected: /CHG also feeds a GPIO pulled up to 3.3 V; an LED from VBUS into that node back-feeds the nRF while the switch holds VDD at 0 V; one more hole in the aluminium |
| LED from 3V3 driven by a GPIO | same LED | rejected: dark when the switch is off, so it adds nothing over the display |
| Top LED with a light pipe | LED plus a pipe part | rejected: no stocked pipe for a 7.8 mm drop; extra hand part |

Consequence: with the slide switch off, a charging pad shows nothing. Switching it on shows the charge state. This
relaxes revision 1's requirement U10 ("charge indication while switched off") by decision, not by oversight.

## 5. Decision

The receptacle is the HRO TYPE-C-31-M-13C, mounted on the PCB bottom face in a 9.24 x 6.70 mm board notch. Its
shell front is flush with the board edge (HRO layout), so the board carries a local tongue that reaches to
0.25 mm behind the outer rear face. The rear wall gets a 10.0 mm notch from the split face, Z -5.00 to -9.90,
wholly in the bottom shell, and an inner pocket that leaves a 0.6 mm skin on each side to hide the tongue
prongs. The receptacle ends 6.75 mm from the rear face, clear of the encoder bodies. M-13B is the runner-up on the
same footprint.

Protection is the usual pair: USBLC6-2SC6 (ST original) at the connector and a 0.75 A PTC behind it, which still
holds the 0.51 A worst-case input at about 60 °C. Each CC pin gets 5.1 kOhm to GND. The receptacle shell goes
straight to GND. The top shell is bonded to GND by one dedicated M2 screw whose head bears on an exposed GND ring
and whose thread runs in a bare tapped boss.

Debug is a TC2030-NL footprint. The reset button is the basic-part TS-1187A behind a floor pinhole, and
double reset enters the Adafruit UF2 bootloader. A `&bootloader` key binding is the daily route.

The MSK12C02 slide switch sits on its own PCB tongue behind an identical 10.0 mm notch. There is no LED.

## 6. Numbers the design needs

Coordinates: Z is height from the deck (top face), negative downward. "Rear face" is the outer face of the
rear wall. D is the distance from the outer rear face into the body (D 0 = outer face, D 3.50 = inner wall
face). X positions are from the right outer face.

### 6.1 USB-C receptacle (TYPE-C-31-M-13C)

| Item | Value | Confidence and source |
| --- | --- | --- |
| Shell outside | 8.94 mm wide, 3.16 mm high, 6.50 mm long | confirmed, HRO M-13C drawing, `_cache/usb-io/ds-03/hro-type-c-31-m-13c.pdf` |
| Opening (plug cavity) | 8.34 +0.06/-0.02 x 2.56 +/-0.04 mm | confirmed, same drawing |
| Sink below the mounting face | 1.60 mm (shell flush with the far face of a 1.6 mm board) | confirmed, side view |
| Contact centre line | 0.02 mm inside the mounting face (1.58 - 1.60): Z -7.82 | likely, derived |
| Shell span | Z -6.20 to -9.36 (PCB thickness tolerance can lift the shell top up to 0.16 above Z -6.20) | likely, derived |
| Board notch | 9.24 mm wide, **6.70 mm** deep from the board edge line (2.10 + 4.60) | confirmed, HRO layout (reviewer point 1) |
| Shell front | flush with the board edge line (front slot centre 2.10 from both the shell front and the PCB edge) | confirmed, HRO side view and layout |
| Shell slots | 4 plated slots 0.60 mm wide; front pair 1.80 long at 2.10 from the edge line, rear pair 1.40 long at 6.10; centres 11.24 mm apart in X | confirmed, HRO M-13C layout |
| Signal pads | 16 (8 at 0.30, 4 at 0.60 mm wide), outer pad end 7.80 from the edge line (2.10 + 5.70) | confirmed, HRO layout |
| Legs | 0.70 mm long into the board from the wing seat (the front-view 0.70) | likely, front view |
| Ratings | 5 A, 20 V, 10,000 cycles, insertion 0.5 to 2.0 kgf | confirmed, HRO drawing |
| Mated plug | product surface at the receptacle front, overmold at least 0.05 mm clear | confirmed, USB Type-C R2.0 figure 3-80 (`_cache/usb-io/render-04/typec-p-136.png`) |

Placement (all likely, arithmetic on the numbers above):

| Item | Value |
| --- | --- |
| X | 27.6 mm from the right outer face (knob-pair centre line, `rotary-buttons.md` 7 item 3) |
| Receptacle front (board edge line) | D 0.25 (allowed 0.0 to 0.3; PCB outline tolerance is the main error) |
| Receptacle rear end | D 6.75 |
| Board notch end | D 6.95 |
| Signal pad row outer end (bottom face) | D 8.05 (bottom face only; the encoder bodies are on the top face) |
| Local PCB tongue | 13.0 mm wide (X 21.1 to 34.1), from the general outline at D 3.95 out to D 0.95 (3.0 mm past the general outline); the 9.24 mm notch is centred in it, leaving two prongs of about 1.9 mm |
| Prong front edge | D 0.95, i.e. 0.70 behind the receptacle front: front slot copper ends about 1.00 behind the edge line (2.10 - 0.90 - 0.20 ring), plus 0.30 copper to board edge |
| Wing and leg zone | |X - 27.6| up to 5.95, Z -7.80 to -8.25, D 1.45 to 3.35 |

### 6.2 Rear-wall opening for USB-C (bottom shell)

1. Through-notch from the split face: 10.0 mm wide (X 22.6 to 32.6), Z -5.00 to -9.90, through the full wall.
   The top edge of the opening is the top shell's split face. Rear view: 10.0 x 4.90 mm, corner treatment per
   the enclosure record. Clearance to the shell: 0.53 mm each side, 0.54 mm below, 1.20 mm above.
2. Inner pocket from the split face: 13.6 mm wide (X 20.8 to 34.4), Z -5.00 to -8.60, from D 0.60 to the inner
   wall face (D 3.50). It clears the PCB prongs (Z -6.20 to -7.80) and the wings (to Z -8.25) by 0.30 mm in X and
   0.35 mm in Z.
3. Skin: D 0.00 to 0.60 at 5.0 < |X - 27.6| < 6.8, Z -5.00 to -8.60. Clearance from the skin to the prong front
   edge: 0.35 mm nominal. JLCCNC metal walls: 0.8 mm recommended, 0.5 mm absolute (`enclosure-manufacturing.md`
   5); the skin is two 1.8 x 3.6 mm tabs held on two edges.
4. Metal under the notch: 2.10 mm if the rear-wall underside stays at Z -12.0 (GLYF rear wall,
   `geometry.md`); the enclosure owns that value.
5. Fallback if JLCCNC refuses the skin: widen the through-notch to 13.6 mm and drop the pocket. The prongs then
   show in the opening.
6. FDM variant: skin 0.8 mm (two 0.4 mm perimeters), receptacle front at D 0.30, prong front at D 1.00:
   clearance 0.20 mm. Check on the USB coupon (6.11).
7. Plug overmold clearance outside the case: no feature within 6.5 mm of the opening centre on the rear face
   (common overmold sizes, guess).

### 6.3 Protection and CC

| Net or part | Value | Placement |
| --- | --- | --- |
| CC1, CC2 | 5.1 kOhm 1 % 0402 to GND each (C25905) | within 5 mm of the connector |
| USBLC6-2SC6 | I/O1 = D-, I/O2 = D+ (pins 1/6 and 3/4 as flow-through), pin 5 = connector VBUS, pin 2 = GND | within 3 mm of the connector pads, before the fuse, GND via straight to the plane |
| PTC | 1206L075THYR between connector VBUS and the system VBUS node | after the ESD clamp; keep it at least 10 mm from the charger IC so it does not share the charger's heat (judgement) |
| VBUS to charger | system VBUS node to BQ24072 IN with 1 uF (`power.md`) | per `power.md` |
| VBUS to module | system VBUS node to BMD-340 pad 66 (4.35 to 5.5 V) | per `mcu-radio.md`; `power.md` risk 5 owns the switch-off case |
| D+/D- | 90 Ohm differential pair to pads 68/67, no stubs, ESD part in line | per `mcu-radio.md` |
| SBU1, SBU2 | not connected | none |
| VBUS bulk capacitance | at most 10 uF total on VBUS at attach | USB 2.0 rule; owned by the power subsystem |

PTC margin: worst-case input 0.51 A against 0.59 A hold at 50 °C and 0.54 A at 60 °C (`ds-13/1206l.txt` line
112). Above about 60 °C local temperature the PTC may trip during full-rate charging; the charger's thermal
regulation and the NTC window (50 °C, `power.md`) stop charging before that in normal use.

### 6.4 Shield and case bonding

1. Receptacle shell slots: plated, tied to GND with vias next to each slot.
2. Ground screw G1: footprint `MountingHole:MountingHole_2.2mm_M2_ISO7380_Pad` (stock KiCad 10.0.7), plated
   Ø2.2 hole, pad tied to GND with at least two vias, exposed copper (no mask) on the bottom face. Screw M2 x 4
   ISO 7380 button head (head Ø3.5, height 1.1), steel black or A2, from the bottom face. Threadlocker optional.
3. Top-shell boss for G1: Ø4.5 mm, end face at Z -6.15 (0.05 mm short of the PCB top, so the screw pulls the board
   up by that much at most and never pushes it down), tapped M2 x 0.4, 3.0 mm thread from the end face, drill Ø1.6
   with point to 4.0 mm, at least 1.0 mm of material left under the deck. JLCCNC leaves threads below M5 bare
   (`enclosure-manufacturing.md` 5, "Thread finish").
4. Position: in the control column, outside the RF bay and its wall slot, the lens pocket and display flex, the
   knob plinth pockets (14.8 x 14.8 mm), the button counterbores (Ø17.0), C1/C2 and the encoder pins; preferably
   within 20 mm of the receptacle. Floor clearance under the head: floor top at Z -9.30 or lower (head to
   Z -8.90 plus 0.4 mm). Part keep-out Ø5.0 on the bottom face, Ø5.0 on the top face for the boss.
5. G1 is fitted after reflow and before the bottom shell closes; it does not hold the case together.
6. FDM case: the boss takes the M2 screw self-tapping (Ø1.7 hole) and bonds nothing; that is acceptable for the
   prototype.

### 6.5 SWD

1. Footprint: `Connector:Tag-Connect_TC2030-IDC-NL_2x03_P1.27mm_Vertical` on the bottom face, outside the
   switch-socket keep-outs and outside the RF bay.
2. Pin use (Tag-Connect Cortex pin-out, likely): 1 VCC (3.3 V, sense only), 2 SWDIO (module pad 44), 3 nRESET
   (P0.18, pad 39), 4 SWCLK (pad 43), 5 GND, 6 SWO not connected (P1.00 carries display RESET in
   `mcu-radio.md`).
3. The board must be reachable with the bottom shell off. No component taller than 1.0 mm within 3 mm of the
   pads (judgement for the cable head).

### 6.6 Reset and bootloader entry

1. TS-1187A-B-A-B on the bottom face between P0.18 and GND. Pad layout: four pads, 7.0 mm outer span,
   rows 4.5 mm apart (datasheet).
2. Body below the PCB: Z -7.80 to -9.30 (1.5 mm). Floor top under the button at Z -9.5 or lower, with a
   1.5 mm through hole in the floor on the plunger axis (2.0 mm plunger, 0.25 mm travel).
3. Bootloader: Adafruit nRF52 bootloader 0.11.0 enters UF2 mode on a double reset within 500 ms
   (`mcu-radio.md` source list).
4. Pin reset: the board devicetree sets `&uicr { gpio-as-nreset; };` (Zephyr binding `nordic,nrf-uicr`), not the
   deprecated `CONFIG_GPIO_AS_PINRESET`. UICR is not rewritten by UF2 updates, so PSELRESET must be programmed once
   over SWD when the bootloader is loaded (for example `nrfjprog --pinresetenable`). Check on the first board.
5. Keymap: a `&bootloader` and `&sys_reset` binding on a function layer, so the pinhole is only for recovery.

### 6.7 Power slide switch placement

1. MSK12C02 on the bottom face at the rear, actuator pointing out of the rear face, X about 45.5 mm from the right
   outer face (`power.md`; the GLYF spacing of 18 mm from USB-C kept).
2. Body 6.7 x 2.8 x 1.4 to 1.5 mm, Z -7.80 to -9.30; actuator centre about Z -8.55 (`power.md`).
3. Local PCB tongue: 9.0 mm wide (X 41.0 to 50.0), board edge at D 1.90, i.e. 2.05 mm past the general outline.
   The switch body front sits on that edge. Actuator tip at D 0.30 (1.6 mm actuator) to D 0.50 (1.4 mm): behind
   the face, reachable with a fingernail.
4. Rear-wall opening: through-notch from the split face, 10.0 mm wide (X 40.5 to 50.5), Z -5.00 to -9.90, the
   same as the USB-C notch. The tongue and the switch body sit inside it with 0.5 mm side clearance. No skin and
   no pocket are needed. Actuator travel 1.6 mm plus 1.3 mm width fits.
5. The switch carries only the LDO enable (nanoamperes, `power.md` 8).

### 6.8 Test points

`TestPoint:TestPoint_Pad_D1.0mm` on the bottom face, no part fitted: VBUS (after the fuse), VBAT, VSYS (charger
OUT), 3V3, GND (two), /CHG, /PGOOD, gauge SDA/SCL. D+ and D- get none (stubs on the pair). All reachable with
the bottom shell off; none inside the RF bay.

### 6.9 Mounting holes

1. The six enclosure standoff holes stay as the enclosure record sets them: NPTH Ø4.0, no copper, track or part
   within Ø4.6 on either side (`enclosure-manufacturing.md` 6.4). Revision 1's plated holes with GND rings are
   withdrawn.
2. G1 is the only plated, grounded mounting hole (6.4).
3. No hole inside the RF bay, the switch-socket keep-outs (`keys.md`), the USB-C notch or either tongue.

### 6.10 Dock

Not needed. No public source shows a GLYF dock or charging contacts; the "dock" in the hero render is a
second unit upside down (`geometry.md`, likely). If a dock is wanted later, the rule would be two or three
gold pogo landing pads on the bottom face behind a non-metal floor window, fed into VBUS through the same PTC,
plus two magnets in floor pockets. Not designed now.

### 6.11 Coupon

Before the CNC order: print a 1:1 coupon of the rear wall section (both notches, pocket, skin) and a 1.6 mm FR4
offcut or printed dummy board with the tongue outline. Fit one M-13C and one MSK12C02 and test the thickest
cables at hand for full seating.

## 7. Consequences for other subsystems

| Subsystem | Consequence |
| --- | --- |
| Enclosure (**change request**, not applied here) | (a) Bottom shell: two 10.0 mm through-notches from the split face, Z -5.00 to -9.90, at X 22.6 to 32.6 and 40.5 to 50.5 from the right face; the openings lie wholly in the bottom shell, unlike `enclosure-manufacturing.md` 6.5 ("notches in both shells") and unlike the GLYF. (b) Inner pocket 13.6 mm wide, Z -5.00 to -8.60, D 0.60 to 3.50 behind the USB-C notch, leaving a 0.6 mm skin. (c) Top shell: one extra tapped boss G1 (6.4) in the control column. (d) 1.5 mm reset pinhole in the floor, floor top at Z -9.5 or lower under the reset button and Z -9.3 under G1. (e) No bare boss faces and no masking are needed. |
| PCB | Custom footprint for TYPE-C-31-M-13C (KiCad 10 holds only M-12 and M-17). Board notch 9.24 x 6.70 mm. Two local tongues on the rear edge: 13.0 mm wide reaching D 0.95 for USB-C, 9.0 mm wide reaching D 1.90 for the switch; the general outline stays at D 3.95. Copper at least 0.30 mm from every tongue edge. G1 plated hole. TC2030-NL footprint. Single-side assembly kept. Panel: the rear edge is no longer straight, so the rear rail needs mouse-bites or a routed gap around the tongues, not a V-cut (the right-edge V-cut of `mcu-radio.md` is unaffected). |
| Power | No LED; /CHG and /PGOOD only to GPIOs as `power.md` decides. VBUS after the PTC is the charger input; PTC hold 0.54 A at 60 °C against the 0.51 A worst case. Keep the PTC away from the charger IC. The slide switch placement in 6.7 replaces the "rear-wall aperture at about Z -8.55" note with a notch from the split face. |
| Rotary and buttons | Conflict in `rotary-buttons.md` 7 item 3 resolved: receptacle ends at D 6.75 and its notch at D 6.95, both less than 8.2. The signal pads reach D 8.05 on the bottom face only; encoder pins (bottom side, Y 7.6, X 15.8 to 20.8 and 34.5 to 39.5) stay clear of the pad span X 24.1 to 31.1 (outer pads at +/-3.20, 0.60 wide). |
| MCU and radio | No conflict. USB on pads 66/67/68, reset P0.18, SWD pads 43/44 as settled. The receptacle is about 27.6 mm from the right face and far from the RF bay at 33 to 73 mm from the rear. |
| Firmware | `&uicr { gpio-as-nreset; };` in the board devicetree; PSELRESET written once over SWD; `&bootloader` binding. |

No conflict with `keys.md` or `mcu-radio.md` was found. The conflicts with `enclosure-manufacturing.md` are
reported above as change requests: openings only in the bottom shell, the pocket and skin, the G1 boss.

## 8. Risks

1. **Skin and tongue tolerance.** The 0.6 mm skin is near JLCCNC's 0.5 mm limit and sits in a bead-blasted part;
   the prong clearance is 0.35 mm nominal against a PCB outline tolerance of about +/-0.2 mm. Coupon first
   (6.11). Fallback: 13.6 mm notch without skin.
2. **Receptacle position depends on the PCB position.** The PCB is located by the switches, so the receptacle
   front lands within about +/-0.2 mm of D 0.25. A front proud of the face (D below 0) would stop the shells
   closing; the coupon checks this.
3. **M-13C stock** is 4,695, ample for 5 boards. M-13B uses the same footprint (slot lengths differ by 0.2 mm;
   draw the slots at 1.80/1.40 and both fit) but needs the notch bottom at Z -10.48.
4. **G1 position.** The control column is crowded; if no spot meets 6.4 item 4, the fallback is a short wire from
   a GND pad to a laser-cleared spot or tapped hole, fitted by hand (enclosure option a or b).
5. **Bottom-shell bond is only through countersink anodise** (guess). An ESD test on the first aluminium unit
   decides whether one countersink needs laser clearing.
6. **PTC near a warm charger.** Above about 60 °C local temperature the PTC may trip during charging; keep it
   away from the charger IC.
7. **MSK12C02 actuator length** is 1.4 or 1.6 mm by source; the tip lands at D 0.30 to 0.50. Both are behind the
   face.
8. **No charge indication with the switch off** (decision, 4.8).
9. Tag-Connect cable cost if the owner does not have one; pogo pins or soldered wires on the same pads are the
   cheap route.

## 9. Sources

Datasheets and drawings:

- HRO TYPE-C-31-M-13C: LCSC datasheet link in `research/_cache/usb-io/lcsc-02/*.json`; local copy
  `research/_cache/usb-io/ds-03/hro-type-c-31-m-13c.pdf` (rendered at 600 dpi in this revision)
- HRO TYPE-C-31-M-13B: https://datasheet.lcsc.com/datasheet/pdf/3abe47025e046bb5de853a0bce03dc99.pdf?productCode=C2848619
  (`research/_cache/usb-io/ds-03/hro-type-c-31-m-13b.pdf`, renders in `render-04`)
- HRO TYPE-C-31-M-12: https://datasheet.lcsc.com/datasheet/pdf/9e56b777c022540fcce7c7f67825f55e.pdf?productCode=C165948
- HRO M-14 and Hanxia CB1.6: `research/_cache/usb-io/ds-03/`
- Hirose CX90M-16P: https://datasheet.lcsc.com/datasheet/pdf/8ade79e9745a1225b23e9dbc35379144.pdf?productCode=C2889324
- USB Type-C Cable and Connector Specification Release 2.0, August 2019, section 3.10.3, figure 3-80
  (`research/_cache/usb-io/usbif-05/`, page render `render-04/typec-p-136.png`)
- ST USBLC6-2SC6: https://www.lcsc.com/datasheet/lcsc_datasheet_2410121836_STMicroelectronics-USBLC6-2SC6_C7519.pdf (`ds-11/usblc6.pdf`)
- Littelfuse 1206L series, derating table: https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_Littelfuse-1206L075THYR_C99563.pdf (`ds-13/1206l.pdf`, text `ds-13/1206l.txt` lines 67 and 112)
- TECHFUSE nSMD series: https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_TECHFUSE-nSMD075_C70078.pdf (`ds-11/nsmd075.pdf`)
- XKB TS-1187A: https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_XKB-Connection-TS-1187A-B-A-B_C318884.pdf (`ds-11/ts1187a.pdf`, image only)
- SHOU HAN MSK12C02: https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_SHOU-HAN-MSK12C02_C431540.pdf (`ds-11/msk12c02.pdf`; ratings and travel, no outline drawing)
- HanElectricity MSK12C02G15-B: https://www.lcsc.com/datasheet/lcsc_datasheet_2409292233_HanElectricity-MSK12C02G15-B_C22435661.pdf (`ds-11/msk12c02g15.pdf`)
- C&K PCM12: https://www.lcsc.com/datasheet/lcsc_datasheet_1912111437_C-K-PCM12SMTR_C221841.pdf (`ds-11/pcm12.pdf`)
- Lite-On LTST-S270KGKT (rejected LED): https://www.lcsc.com/datasheet/lcsc_datasheet_1810231513_Lite-On-LTST-S270KGKT_C125113.pdf (`ds-11/ltst-s270.pdf`)
- Zephyr devicetree binding `nordic,nrf-uicr` (`gpio-as-nreset`): https://docs.zephyrproject.org/latest/build/dts/api/bindings/arm/nordic%2Cnrf-uicr.html

`research/_cache/usb-io/ds-06/` (empty files) and `ds-10/` (LCSC HTML wrapper pages) are failed downloads and are
not sources.

Stock and class: JLCPCB parts API, read 2026-11-13: `research/_cache/usb-io/jlc-01`, `jlc-07`, `jlc-08`,
`jlc-09`, `jlc-14` (spring-finger search), `jlc-15` (re-check of C2848620, C2848619, C99563, C431540), and the
reviewer's `sceptic-stock-01`; LCSC product API for the receptacles, `lcsc-02`.

KiCad 10.0.7 stock libraries (image `kicad/kicad:10.0.7`): footprints present for HRO TYPE-C-31-M-12 and M-17,
Tag-Connect TC2030-IDC-NL, XKB TS-1187A, Shouhan MSK12C02, C&K PCM12, SOT-23-6, Fuse 1206, TestPoint pads,
`MountingHole_2.2mm_M2_ISO7380_Pad`; symbols `USB_C_Receptacle_USB2.0_16P`, `USBLC6-2SC6`, `TPD4E05U06DQA`,
`PRTR5V0U2X`, `SW_Push`, `SW_SPDT`. Not present: TYPE-C-31-M-13C/M-13B, CX90M-16P and MSK12C02G15-B footprints.
3D model files are referenced by the footprints but not shipped in the image.

Project notes: `research/raw/geometry.md`, `research/raw/follow-maker-bom-part-numbers.md`,
`research/raw/youtube.md`, `research/components/keys.md`, `research/components/mcu-radio.md`,
`research/components/enclosure-manufacturing.md`, `research/components/power.md`,
`research/components/rotary-buttons.md`.
