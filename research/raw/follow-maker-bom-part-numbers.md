# Follow-up: part numbers on the maker's December 2025 board

Date: 2026-11-13
Key: `follow-maker-bom-part-numbers`
Cache: `research/_cache/follow-maker-bom-part-numbers/` (gitignored)

Question: what are the part numbers of the reference board's charger with power path (U2, a QFN beside inductor L1),
U3, U4, U5, flash U8, the display connector J2, the battery connector, the slide switch and the hot-swap sockets?

## 1. Answer in short

1. The JLCPCB parts list in `kOclb0i9bug` never scrolls. From 1.0 s to 4.5 s it shows the same three rows only
   (`C107410` SOIC-8, `C11702` 0402, `C11702` 0402, all "bottom"). After that the viewer covers the list. The same
   three rows appear in the JLCPCB clip inside `S9c5WuorsgQ`. No other `C<digits>` number is shown in any frame of
   either video. Every frame of both sections was extracted at 1080 x 1920 (format 270) and checked. (confirmed)
2. The charger U2 cannot be named from public sources. The frames show a 3.0 x 3.0 mm QFN-16 (four pads per side,
   exposed pad). L1 beside it is an 0402-size part (a ferrite bead or small RF inductor). It is not a power
   inductor, so U2 is a linear charger, not a switching charger. Five resistors, a small LED-size diode D1 and four
   capacitors surround it. No laser marking is readable at 1080p. The best match is the TI BQ2407x family in VQFN-16
   RGT (BQ24072, BQ24073, BQ24074, BQ24075 or BQ24079). (package: confirmed; family: likely; exact part: not found)
3. Parts identified with good confidence:
   - Flash U8: Winbond W25Q128 (128 Mbit, 16 MB) in the 208-mil SOIC-8 body. (confirmed)
   - Fuel gauge U3: MAX17048, 2 x 2 mm DFN-8. (confirmed for the part, likely for the reference designator)
   - RTC: DS3231MZ+TRL, LCSC `C107410`. (confirmed)
   - J2: 20-contact, 0.5 mm, bottom-side FPC connector with a flip actuator. (confirmed)
   - Hot-swap sockets: Kailh Choc sockets, CPG135001S30 class. (likely)
4. Parts identified only by package and position:
   - U4: SOT-23-5, probably a 3.3 V LDO of the XC6220B331 type. (likely)
   - U5: SOT-23-6 behind the USB-C fuse, probably a USB ESD array. (guess)
   - Slide switch: side-actuated SMD switch with 1.5 mm pitch, MSK12C02 type. (likely for the type; exact part not
     found)
   - Battery connector: a 2-pin side-entry SMD connector with a pitch of about 1.1 to 1.2 mm. This is not the
     2.0 mm JST PH that the May 2025 layout named. (likely)
5. The power failures the maker reported happened on the April 2025 prototype, around the AO3401A P-MOSFET switch,
   before the integrated charger existed. The December 2025 board is the version that works: the beta firmware
   reads the MAX17048 and the product shipped. Its exact charger part number is not public, so no "proven part"
   can be copied. Choose a BQ2407x part from the list in section 3.

## 2. JLCPCB order evidence (kOclb0i9bug, S9c5WuorsgQ)

| Finding | Source | Confidence |
| --- | --- | --- |
| Format 270 (1080 x 1920) was pulled for `kOclb0i9bug` (23.976 fps, 45.2 s), `S9c5WuorsgQ` (30 fps, 68.8 s) and `ScYz1Z_T1UY` (23.976 fps, 35.0 s). Every frame of the parts-list and viewer section (`kO`, frames 1 to 840) and of the board close-ups was extracted as PNG. | `yt-270-01/`, `frames-03/kO`, `frames-03/S9a`, `S9b`, `S9c`, `Sc` | confirmed |
| Parts-list header: "Footprint, Part #, Assembly Side, Assembly ...". Order line "SMT0251107601..." (clipped). Rows: `SOIC-8 / C107410 / bottom / SMT`, `0402 / C11702 / bottom / SMT`, `0402 / C11702 / bottom / SMT`. The rows are identical in frames 30, 50, 70 and 90 and never scroll. | `frames-03/kO/k00030.png` to `k00100.png` | confirmed |
| `C107410` resolves to Maxim DS3231MZ+TRL, SOIC-8, Real Time Clocks, stock 18,073. `C11702` resolves to UNI-ROYAL 0402WGF1001TCE (1 kOhm 0402). | LCSC product API `https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=C107410` and `=C11702`; `lcsc-06/C107410.json`, `C11702.json` | confirmed |
| The JLCPCB 3D viewer shows generic models. U2's model has a faint, unreadable top marking. U8's model is a square 8-lead body. No model carries a readable part number. | `crops-05/jlc-k40-power.png`, `u2-jlc-k40.png`, `k100.png` | confirmed |
| The 18 extended part types cannot be listed from the video. The extended fee was USD 54.00, which is 18 x USD 3.00. | `kOclb0i9bug` frames 28 to 40 (already in `youtube.md`) | confirmed |

## 3. Charger U2

| Finding | Source | Confidence |
| --- | --- | --- |
| Maker's words: "This charging IC safely charges our battery and automatically manages power between the battery and an external power source." | `S9c5WuorsgQ` narration (already in `youtube.md`) | confirmed |
| U2 is a square QFN, 3.0 x 3.0 mm, with four pads per side and corner-bracket silkscreen. Scale: the 20 contacts of J2 span 9.5 mm in the same frame, which gives about 16.9 px/mm at full resolution. U2 measures 150 px at 3x zoom, which is 3.0 mm. | `frames-03/S9c/c00160.png`; crops `crops-05/u2-c160.png`, `stack-u2.png`, `u2-real-pair.png` | confirmed |
| No laser marking is readable on U2 in any frame (glare-free frames `c00060`, `c00160` and the S9a sequence were compared). | `crops-05/u2-c060.png`, `u2-c160.png`, `m-u2.png`, `cl-u2.png` | confirmed (not readable) |
| L1 is an 0402-size part, about 0.5 x 1.0 mm, next to the 0603 capacitor C12. It is too small to be the inductor of a switching charger. It is probably a ferrite bead. | Scale crop from `frames-03/S9c/c00160.png` | likely |
| Around U2: R2, R7, R8, R9, R11, C1, C6, C11, C12 and an orange 0402 diode D1 (a status LED by look). A BQ2407x needs ISET, ILIM, TMR or TS resistors, and a CHG LED with its resistor. This matches. | `crops-05/stack-u2.png`; `jlc-k40-power.png` | likely |
| The May 2025 layout (ScYz1Z_T1UY) has no charger. Its "U2" is the display FPC connector. That board relied on the nice!nano's own charger. Reference designators were renumbered for the December 2025 board. | `crops-05/sc-C-flop.png` (FPC footprint labelled U2, "MP GND" pads) | confirmed |
| The beta firmware has no charger driver or node. That fits a pin-strapped linear charger such as a BQ2407x, and rules out an I2C charger such as BQ2589x or nPM1300. | `research/_cache/regulatory-software/firmware-06/strings_v014.txt`: nodes are only `glyf_display@0`, `w25q128@0`, `ds3231@68`, `max17048@36` | confirmed (no I2C charger) |
| Candidates in QFN-16 3 x 3 with power path, from LCSC: BQ24074RGTR `C54313` (input up to 10.2 V, stock 4,194); BQ24073RGTR `C15220` (stock 531); BQ24079RGTR `C140287` (stock 36); BQ24072TRGTT `C139632` (stock 5); BQ24075RGTT `C2865459` (stock 230 at JLCPCB). All are extended parts. The MCP73871 (QFN-20 4 x 4) and the MP2617 (switching) do not fit the package or the missing power inductor. | `lcsc-06/C54313.json`, `C15220.json`, `C140287.json`, `C139632.json`; `lcsc-06/js2-BQ24075RGT.json` | confirmed (LCSC data), likely (family fit) |

## 4. Other parts on the December 2025 board

| Part | Finding | Source | Confidence |
| --- | --- | --- | --- |
| U8, flash | Beta firmware node `w25q128@0`, driver `qspi_nor`. The maker's development overlays give JEDEC ID `ef 40 18` (W25Q128JV). The board package measures about 5.3 x 5.3 mm at 1.27 mm pitch, which is the 208-mil SOIC-8. The matching ordering code is W25Q128JVSIQ, LCSC `C97521`, which has 0 stock today. | `regulatory-software.md` section 2; `crops-05/stack-u8.png` | confirmed (W25Q128, package), likely (JVSIQ suffix) |
| U3, fuel gauge | Firmware node `max17048@36`. U3 sits next to the battery connector. It measures about 2.2 mm with eight pads at 0.5 mm pitch, four per side, which is the MAX17048G+T10 DFN-8-EP 2 x 2 (LCSC `C2682616`, stock 20,409). | `regulatory-software.md`; scale crop from `frames-03/S9c/c00160.png`; `crops-05/stack-u3batt.png` | confirmed (MAX17048), likely (U3 is it) |
| U6 and U7 | These are two narrow SOIC-8 parts near the reset button. One is the DS3231MZ+TRL (`C107410`). The other has the marking "...H433B / ?2DM / lot". The May 2025 layout labels the footprint next to DS3231MZ_TRL as "AT24C?2D-SSHM-T", with the third character hidden. That makes it a Microchip AT24C32D or AT24C02D I2C EEPROM (AT24C32D-SSHM-T is LCSC `C60583`). The firmware has no EEPROM node, so the part is fitted but not used. | `crops-05/stack-u6u7.png`, `u6-compare.png`; `crops-05/sc-kicad-mean.png`; firmware strings | confirmed (two SOIC-8, DS3231), likely (AT24C EEPROM), guess (32 vs 02) |
| U4 | SOT-23-5 with a pin-1 triangle, beside Q1 and the slide switch. No marking can be read. The May 2025 layout carries an "XC6220B331" value, a 3.3 V LDO in SOT-25 (`C86534`). The battery note concludes that the board uses an LDO supply. | `crops-05/stack-u4q1sw.png`; `crops-05/sc-A-flop.png` | likely (3.3 V LDO), guess (exact part) |
| Q1 | SOT-23 beside the slide switch, so probably the power switch MOSFET. The April 2025 prototype used AO3401A (`C15127`), whose marking starts "X1". Q1 shows a faint mark that may begin with "X". | `crops-05/stack-u4q1sw.png`; `z8-jlc-116c.png` | likely |
| U5 | SOT-23-6 behind the USB-C socket, next to fuse F1. No marking can be read. The V4 layout prints "BSD3C051V" (a SOD-323 TVS) near the socket, which is probably D2 on the VBUS line. U5 is then probably a two-line USB ESD array such as USBLC6-2SC6 (`C7519`). | `crops-05/stack-u5.png`, `jlc-k40-top.png`; `youtube.md` | guess |
| J2, display connector | Bottom-side FPC connector: white body, black flip actuator, 20 contacts counted at 0.5 mm pitch (9.5 mm span). Same-size LCSC parts are JUSHUO AFC01-S20FCA-00 `C262667` and AFC01-S20FCC-00 `C262274` (20 position, 0.5 mm, bottom contact). The brand cannot be read. | `crops-05/stack-j2.png` (contact count by profile and by eye) | confirmed (20 contacts, 0.5 mm), guess (brand) |
| Battery connector | White 2-pin side-entry SMD connector with two side tabs, about 7.4 mm wide including the tabs. The pin pitch measures about 1.1 to 1.2 mm against the J2 scale in two frames. That fits a 1.25 mm series (JST GH or Molex PicoBlade class) better than 1.0 mm JST SH. It is clearly not a 2.0 mm JST PH. The May 2025 layout used "S2B-PH-SM4-TB(LF)(SN)" (JST PH, `C295747`), so the connector changed. | `frames-03/S9c/c00100.png`, `c00160.png`, `c00230.png`; `crops-05/sc-E-flop.png` | likely (not PH, about 1.25 mm), not found (series) |
| Slide switch | Side-actuated SMD slide switch with a metal cover. Three signal pads sit at about 1.5 mm pitch plus corner tabs, and the lever points through the rear edge. That matches the MSK12C02 (`C431540`, "Right Angle 8mm", stock 164,000), the usual choice on nice!nano-class boards. The cover marking "780" is not a part number. | `crops-05/stack-u4q1sw.png`, `m-sw.png` | likely (type), not found (exact part) |
| Hot-swap sockets | The socket outline has a stepped body and two contacts on opposite ends. That is the Kailh Choc socket, which the sibling note identifies as CPG135001S30 (`C5333465`, 0 stock today). | `crops-05/stack-sock.png`; `follow-switch-family-and-socket.md` | likely |
| USB-C | TYPE-C-31-M-12 class, 16-pin mid-mount (`C165948`). | `youtube.md` | likely |

## 5. What this means for worxpad

1. The maker's proven charger part is not public. Use a BQ2407x part in VQFN-16 3 x 3: BQ24074RGTR (`C54313`) has
   the deepest stock and a 10.2 V input rating. Strap it with resistors and route CHG and PGOOD to GPIOs, because the
   maker firmware does not read them.
2. Copy the parts that are confirmed: W25Q128JV flash, MAX17048 gauge, DS3231MZ RTC (optional), and a 20-pin 0.5 mm
   bottom-contact FPC connector chosen together with the display.
3. Leave out the AT24C EEPROM, because the maker firmware never uses it.
4. Check the stock of every extended part at order time. Two of the maker's likely parts, W25Q128JVSIQ `C97521` and
   CPG135001S30 `C5333465`, show 0 stock at LCSC today.

## 6. Sources read

- `research/raw/youtube.md`, `social.md`, `regulatory-software.md`, `follow-switch-family-and-socket.md`,
  `follow-battery-cell-and-runtime.md`, `follow-display-module-sourcing.md`.
- YouTube `kOclb0i9bug`, `S9c5WuorsgQ`, `ScYz1Z_T1UY` at format 270, plus `TZLxTVbzH28` (format 270) and
  `Z8-k1frnIJM` (format 616): `research/_cache/follow-maker-bom-part-numbers/yt-270-01/`, `yt-alt-02/`, `yt-extra-07/`.
- Frames: `frames-03/kO` (kOclb0i9bug, frames 1 to 840), `frames-03/S9a`, `S9b`, `S9c` (S9c5WuorsgQ board close-up and
  KiCad sections), `frames-03/Sc` (ScYz1Z_T1UY). Contact sheets in `sheets-04/`, crops in `crops-05/`.
- LCSC product detail API `https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=<C number>` for C107410,
  C11702, C54313, C15220, C139632, C140287, C2682616, C97521, C60583, C722467, C86534, C7519, C15127, C431540,
  C431542, C128955, C295747, C262272, C262273, C262274, C262666, C262667, C262669, C165948, C5333465, C964818 and
  others (`lcsc-06/`). JLCPCB part searches by name are cached as `lcsc-06/js*.json`.
- Maker beta firmware strings (`research/_cache/regulatory-software/firmware-06/strings_v010.txt`, `strings_v014.txt`).

## 7. What could not be reached or answered

- The JLCPCB parts list beyond its first three rows. It is not shown in any public video.
- Laser markings on U2, U4, U5, U8 and the battery connector. They cannot be read at 1080p, and no 4K source exists.
- LCSC search endpoint `https://wmsc.lcsc.com/ftps/wm/search/global`: "Access Denied" (Akamai). Product detail lookups
  by C number work.
- No published schematic, BOM, Gerber or KiCad project for the GLYF board was found. The maker's public GitHub
  repositories hold only development rigs and firmware binaries.
