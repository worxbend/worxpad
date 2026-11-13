# Follow-up: radio module choice (nRF5340, nRF52840 or nRF54L15)

Date: 2026-11-13
Research key: `follow-radio-module-choice`
Question: which Nordic module should the worxpad board carry, the Holyiot-21069 nRF5340 module used by the GLYF maker, or a module that JLCPCB stocks and places? What is the state of ZMK for each SoC with an LVGL colour display?

Confidence scale: **confirmed** (stated by the maker of the part, or measured from a primary source), **likely** (consistent indirect evidence), **guess**. "Not found" means the item was looked for and not found.

All catalogue numbers (stock, price) were read on 2026-11-13 and change daily. Prices are USD for one piece unless stated.

---

## 1. Short answer

1. No nRF5340 module with an on-board antenna is in usable stock at JLCPCB. The Holyiot-21069 exists in the JLCPCB library only as non-purchasable records, which is the pattern of a customer-supplied (consigned) part. An nRF5340 design therefore needs consignment, JLCPCB pre-order (Global Sourcing), or hand soldering.
2. Three nRF52840 modules are in JLCPCB stock: Ebyte E73-2G4M08S1CX (974 pieces), u-blox BMD-340-A-R (349 pieces) and Ebyte E73-2G4M08S1C (61 pieces).
3. The nRF54L15 is ruled out: it has no USB device peripheral, and ZMK has no nRF54L board. The nRF54LM20A has USB, but its ZMK ports are experimental and outside upstream.
4. The maker's firmware links at least 373 KB of static RAM, so it does not fit an nRF52840 as built. 115.2 KB of that is one full-frame LVGL buffer, which is a configuration choice and not a requirement.
5. Recommendation: carry an nRF52840 module from JLCPCB stock, with the Ebyte E73-2G4M08S1C / S1CX footprint as first choice and the u-blox BMD-340 as the alternative. Use the Holyiot-21069 (consigned) only if the firmware plan needs more than 256 KB of RAM. Section 7 gives the reasons and the decision rule.

---

## 2. Maker firmware sizing (decoded from the v0.1.4 image)

Source file: `research/_cache/regulatory-software/firmware-06/zmk.signed.v0.1.4.bin` (and v0.1.0 to v0.1.3 beside it).
Method: static reading only. MCUboot header parse, disassembly with `llvm-objdump` (Thumb, load address 0x10000), then reading the literal pools of the reset handler, `z_bss_zero` and `z_data_copy`. Nothing was executed. Scripts are in `research/_cache/follow-radio-module-choice/scripts-06/`.

| Fact | Evidence | Confidence |
| --- | --- | --- |
| Initialised data occupies 0x20000000 to 0x200020B4 (8,372 bytes), copied from flash address 0x934B4. | Literal pool of the data-copy routine at 0x44948: `20000000 200020b4 000934b4`. | confirmed |
| BSS occupies 0x200020B8 to 0x2003C018 (237,408 bytes). | Literal pool of the bss-zero routine at 0x434F4: `200020b8 2003c018`. | confirmed |
| The interrupt stack is 2,048 bytes at 0x20047D18. The main stack is 8,192 bytes and ends at 0x2004A658, which is the initial stack pointer. | Reset handler at 0x1D354 loads `2004a658` into MSP and `20047d18 + 0x800` into PSP. | confirmed |
| Static RAM reaches at least 0x2005B194, that is 373,140 bytes (364 KiB). The earlier figure "more than 256 KB" rested on the stack pointer only (304,728 bytes); the real static footprint is larger. | Highest RAM address referenced from a code literal is 0x2005B193. Buffer descriptors in the data section end at 0x2005AD8C + 0x400. Addresses above that were seen only as unverified data words. | likely (lower bound) |
| One object of exactly 115,200 bytes sits at 0x20019884 to 0x20035A84 with no reference inside it. 115,200 = 240 x 240 x 2, one full frame in RGB565. This is the LVGL draw buffer at `CONFIG_LV_Z_VDB_SIZE=100`. | Gap between consecutive code-referenced RAM addresses. | likely |
| Two kernel heaps are defined: 20,480 bytes at 0x2004C658 and 8,192 bytes at 0x20043798. | Pointer and size pairs in the data section at flash 0x94DCC and 0x94DE0. | likely |
| Two 6,000-byte buffers and three 1,024-byte buffers sit at 0x200572AC to 0x2005B18C. They are probably the ring buffers of the two USB CDC-ACM ports. | Size and pointer pairs at flash 0x94248 to 0x943A8. | guess (purpose) |
| The size of the LVGL memory pool was not isolated. An unreferenced span of 45,810 bytes at 0x2000800E to 0x20013300 is a candidate. | Same gap analysis. | guess |
| The application core RAM region is 0x20000000 to 0x20070000 (448 KiB). A further 64 KiB at 0x20070000 is the region shared with the network core. | Literal `20070000` beside `20000000` in the memory-protection setup at 0x1D76C; table entry `20070000 00010000` at flash 0x94304. | confirmed |
| Earlier builds were already above 256 KB: v0.1.1 and v0.1.2 have BSS 205,104 bytes and stack pointer 0x20042B88 (273,288 bytes); v0.1.3 has BSS 208,860 bytes and stack pointer 0x20043570. | Same literals in each image. | confirmed |
| Flash: the v0.1.4 image is 547,276 bytes (0x200 header, 546,428 bytes of code and data, 336 bytes of trailer), linked at 0x10000. Two such slots plus a 64 KB bootloader do not fit in 1 MB, so the MCUboot secondary slot is probably on the external W25Q128. | Header parse; arithmetic. | confirmed (sizes), likely (external secondary slot) |

Reading for the design:

- The maker's build as configured cannot run on an nRF52840 (256 KB RAM). This is now shown from the region sizes and not from one stack-pointer value.
- Without the full-frame buffer the build still links about 258 KB, and an nRF52840 must also hold the Bluetooth controller that the nRF5340 keeps on its second core. A port of the same feature set would need a partial draw buffer and smaller heaps, stacks and USB buffers. This is feasible in principle and not proven. Confidence: likely.
- Evidence that an nRF52840 can run the core of the product: the maker's own prototypes up to November 2025 used a plug-in nRF52840 board and already showed the icon grid and the modified ZMK Studio (`research/raw/social.md` section 4.1, `research/raw/youtube.md`). The Prospector project runs ZMK with a 240 x 280 RGB565 ST7789V and a 100 % draw buffer (134,400 bytes) on an nRF52840 (`research/raw/prior-art.md`, Prospector section). Confidence: confirmed for both observations.
- A 547 KB image fits the application area of an nRF52840 that uses the Adafruit UF2 bootloader (about 811 KB in the nice!nano partition layout of ZMK). The figure of 811 KB is from memory of the ZMK board files and was not re-read today. Confidence: likely.

---

## 3. Holyiot-21069 (nRF5340), the maker's module

Primary source: the module datasheet filed with the FCC as the user manual, FCC ID 2ALGY21069 (https://fccid.io/2ALGY21069/User-Manual/User-Manual-5961970.pdf, 23 pages, datasheet version 1 dated 2022-04-07). Cached with rendered pages in `research/_cache/follow-radio-module-choice/holyiot-02/`.

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| SoC | nRF5340 QKAA. Application core 1 MB flash and 512 KB RAM, network core 256 KB flash and 64 KB RAM. | Datasheet page 3 and 4 | confirmed |
| Outline | 19.00 x 13.50 mm | Datasheet page 8, mechanical drawing | confirmed |
| Height | 2.4 mm in two retailer listings. Nordic's module list gives "19x13.5x0.8mm", which matches a bare PCB thickness and not the height with shield can. The datasheet gives no height. | https://electropeak.com/holyiot-nrf5340-microcontroller-breakout-board-with-ceramic-antenna ; https://www.nordicsemi.com/Products/nRF5340/Modules | likely (2.4 mm) |
| Pads | 58 in total. 36 castellated edge pads: 12 on the left side (pins 1 to 12), 11 on the bottom side (13 to 23), 13 on the right side (24 to 36). 22 inner pads under the module in two columns of 11 (pins 37 to 47 and 48 to 58). | Datasheet pages 8 and 9 | confirmed |
| Pad pitch | 1.10 mm on every row. Side rows start 1.50 mm from the bottom edge (1.50, 2.60, 3.70 ...). The bottom row runs from 1.25 mm to 12.25 mm from the left edge. | Datasheet page 8 | confirmed |
| Pad size | Edge pads 0.70 x 0.90 mm. Inner pads 1.00 x 0.70 mm. Inner columns lie 2.50 mm and 11.30 mm from the left edge. | Datasheet page 8 | confirmed (sizes), likely (the two distances are to pad centres) |
| Usable GPIO | 46: P0.02 to P0.31 (30 pins) and P1.00 to P1.15 (16 pins). P0.00 and P0.01 are not brought out, which indicates an on-module 32.768 kHz crystal. | Datasheet pin table, pages 10 to 12; Nordic module list ("46") | confirmed (46), likely (crystal) |
| Other pads | VBUS, VDDH, DCCH, VDD, USB D+ and D-, SWDIO, SWDCLK, RESET, 3 x GND. | Datasheet pin table | confirmed |
| Dedicated pins present | QSPI: P0.13 to P0.18 (IO0, IO1, IO2, IO3 on P0.16, SCK, CSN). High-speed SPI: P0.08 to P0.12. 1 Mbps TWI: P1.02 and P1.03. NFC: P0.02 and P0.03. | Datasheet pin table | confirmed |
| Antenna | Ceramic chip antenna at one short end, gain 1 dBi. The last 4.3 mm of the length (from the top pad at 14.70 mm to the edge at 19.00 mm) carries no pads. | Datasheet page 8; FCC text in the same PDF; FCC internal photo (`holyiot-02/int-1.png`) | confirmed |
| Antenna keep-out | No dimensioned keep-out is given. The text asks for the antenna end to extend "several mm" past the host ground at a board edge or corner, with no ground under the antenna. | Datasheet page 13 | confirmed (text), not found (numbers) |
| Assembly limits | At most two reflow cycles. "No opposite side re-flow is allowed due to module weight." | Datasheet page 13 | confirmed |
| Certification | FCC modular grant 2ALGY21069 (Part 15.247). CE and RoHS are claimed by retailers. | FCC manual text; Electropeak listing | confirmed (FCC), likely (CE) |
| Price | USD 13.95 for one, 12.86 at 100, 12.32 at 500 (listing names the module but is titled "breakout board"). INR 1,031.36 plus tax at an Indian retailer. An AliExpress or holyiot.com price was not found. | https://electropeak.com/holyiot-nrf5340-microcontroller-breakout-board-with-ceramic-antenna ; https://hubtronics.in/holyiot-21069-nrf5340 (search summary) | likely |
| JLCPCB status | Two library records, `C9900280684` "Holyiot-21069-nRF5340" and `C9900154256` "HOLYIOT-21069-5340", brand "JLCPCB Assembly", stock 0, not purchasable. This is the pattern of parts that customers supplied themselves. JLCPCB does not sell the module. | JLCPCB parts search, `jlc-01/jlc_nRF5340.json`, `jlc_HOLYIOT.json` | confirmed (records), likely (meaning) |

The pin map decoded from the maker's firmware (`research/raw/regulatory-software.md`) sits on neighbouring pads of this module, which supports both the decode and the module identification: matrix outputs P1.14, P1.13, P1.12, P1.11, P0.31 are pins 42 to 38; matrix inputs P0.21, P0.19, P0.29, P0.25 are pins 29 to 26; encoder pins P1.07, P1.09, P0.28, P1.10 are pins 24, 25, 33, 34; display chip select P0.11 and data/command P0.12 are pins 52 and 53. Confidence: likely.

Several matrix pins are on the inner pad rows. The inner rows cannot be soldered with an iron, so this module needs reflow or hot air.

---

## 4. JLCPCB catalogue on 2026-11-13

Source: JLCPCB parts search API (`https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList`), responses in `jlc-01/`. LCSC product API (`https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=...`) for cross-checks, responses in `lcsc-03/`. Every part below is in the extended library (none is a basic part). Confidence for the rows: confirmed as read on this date.

### 4.1 nRF5340

| Part | JLCPCB number | Package | Stock | Price | Note |
| --- | --- | --- | --- | --- | --- |
| u-blox NORA-B100-00B | C3030983 | LGA-82, 10.4 x 14.3 x 1.7 mm | 7 | 14.80 | U.FL connector only, no antenna on the module. 48 GPIO. |
| u-blox NORA-B120-00B | C6344850 | 94 pads | 8 | 20.96 | Version with power amplifier, U.FL. |
| u-blox NORA-B106-00B | C5438434 | LGA-82, 10.4 x 14.3 x 1.7 mm | 0 | 16.17 | PCB antenna. LCSC stock 0. |
| Ebyte E83-2G4M03S | C5333991 | 16 x 16 mm | 1 | 11.06 | Not listed on LCSC international. |
| Raytac MDBT53-1M | C5355663 | LGA-65, 9.3 x 14.3 x 1.9 mm | 0 | 15.00 | Chip antenna, 48 GPIO. LCSC stock 0. |
| Raytac MDBT53-P1M | C5796572 | 65 pads, 9.3 x 14.3 x 1.6 mm | 0 | 9.89 | PCB antenna. LCSC stock 0. |
| MinewSemi MS45SF1 | C19712196 | LGA-66, 18 x 12.5 mm | 0 | no price | |
| Holyiot-21069 | C9900280684, C9900154256 | | 0 | not sold | Customer-supplied records only. |
| Nordic NRF5340-QKAA-R (bare SoC) | C3015611 | aQFN-94, 7 x 7 mm | 4,296 | 7.23 | Chip-down design; needs own antenna, matching, crystals and certification. R7 reel variant C3606967 has 4,339. |

Sizes and GPIO counts in the notes column are from Nordic's third-party module list (https://www.nordicsemi.com/Products/nRF5340/Modules).

### 4.2 nRF52840

| Part | JLCPCB number | Package | Stock | Price | Note |
| --- | --- | --- | --- | --- | --- |
| Ebyte E73-2G4M08S1CX | C2764963 | 13 x 18 x 3.0 mm, 43 pads | 974 | 6.37 | IPEX connector, needs an external antenna. |
| Ebyte E73-2G4M08S1C | C356849 | 13 x 18 x 3.0 mm, 43 pads | 61 | 7.69 | Ceramic antenna. |
| u-blox BMD-340-A-R | C5456944 | LGA, 15.0 x 10.2 x 1.9 mm | 349 | 9.81 | PCB antenna, 48 GPIO. LCSC stock 190. |
| u-blox NINA-B306-00B | C6127317 | 55 pads | 31 | 19.96 | PCB antenna. |
| Seeed XIAO nRF52840 | C17209540 | 21 x 17.8 mm board | 115 | 10.75 | 11 GPIO on the edge; too few pins. |
| Raytac MDBT50Q-1MV2 | C5118826 | 61 pads, 10.5 x 15.5 mm | 0 | 19.06 | Chip antenna. |
| Raytac MDBT50Q-P1MV2 | C5119772 | 61 pads | 0 | 7.96 | PCB antenna. |
| Minew MS88SF3 | C20416747 | 18.5 x 12.5 mm | 0 | 2.50 (price looks unreliable) | |
| Holyiot-18010 | C9900042076 | 18 x 13.5 mm | 0 | not sold | Customer-supplied record only. |
| Nordic NRF52840-QIAA-R (bare SoC) | C190794 | aQFN-73, 7 x 7 mm | 43,491 | 7.58 | Chip-down design. |

### 4.3 nRF54L15

| Part | JLCPCB number | Package | Stock | Price | Note |
| --- | --- | --- | --- | --- | --- |
| Ebyte E73-2G4M08S1F | C54337734 | 12.0 x 17.2 mm, PCB antenna | 106 | 5.69 | nRF54L15-QFAA, 1,524 KB flash, 256 KB RAM, 29 GPIO. Interfaces listed: UART, SPI, I2C, GPIO, ADC, PWM. No USB. |
| Ebyte E73-2G4M08S1FX | C54582385 | 12.0 x 12.0 mm, IPEX | 1 | 7.17 | Same SoC. |
| Minewsemi ME54BS01, ME54BS12 | C53447275, C53430462 | 12 x 15.8 mm | 0 | no price | |
| Holyiot-24005 | C9900176029 | 15.6 x 24 mm | 0 | not sold | Customer-supplied record only. |
| Nordic NRF54L15-QFAA-R (bare SoC) | C42458750 | QFN-48, 6 x 6 mm | 0 | 4.13 | NRF54L05 has 811, NRF54L10 has 156. |

Source for the E73-2G4M08S1F data: Ebyte user manual, `datasheets-04/e73f.pdf` (https://atta.szlcsc.com/upload/public/pdf/source/20260507/996BBAC66F31C57B7A15BAEEE2D73A21.pdf). Confidence: confirmed.

---

## 5. Candidate comparison

Pin budget from the task: 9 matrix, 4 encoder, 5 display (SCK, MOSI, CS, DC, RST), 6 QSPI, 2 I2C, 1 backlight. Total 27 GPIO. USB D+ and D- are dedicated pads on the nRF52840 and nRF5340 and do not count. A real design will add 2 to 4 more (charger status, fuel-gauge alert, switched-rail enable, RTC interrupt).

| | Holyiot-21069 | Ebyte E73-2G4M08S1C / S1CX | u-blox BMD-340-A-R | Ebyte E73-2G4M08S1F |
| --- | --- | --- | --- | --- |
| SoC | nRF5340 | nRF52840 | nRF52840 | nRF54L15 |
| Flash / RAM | 1 MB / 512 KB (application core) | 1 MB / 256 KB | 1 MB / 256 KB | 1.5 MB / 256 KB |
| USB device | yes | yes | yes | no |
| Outline | 19.0 x 13.5 mm | 18.0 x 13.0 mm | 15.0 x 10.2 mm | 17.2 x 12.0 mm |
| Height | 2.4 mm (retailer) | 3.00 mm | 1.9 mm | not read |
| Pads | 58: 36 castellated plus 22 inner | 43: 26 castellated plus 17 inner | 68 LGA, no castellation | not read |
| Pitch | 1.10 mm | 1.27 mm | 1.10 mm, three staggered rows | not read |
| Pad size | 0.70 x 0.90 edge, 1.00 x 0.70 inner | 0.80 x 1.00 edge (bottom), 0.80 x 0.80 inner | 0.50 x 0.50 | not read |
| GPIO on pads | 46 | 32, of which P0.18 is reset and P0.00/P0.01 are the optional 32.768 kHz crystal pins: 31 usable without the crystal, 29 with it | 48 | 29 |
| Pin budget 27 | fits, 19 spare | fits, 2 to 4 spare | fits, 21 spare | fits, but no USB |
| Antenna | ceramic, on module | S1C: ceramic on module. S1CX: IPEX connector | PCB trace, on module | PCB trace |
| Antenna zone on module | last 4.3 mm of length | last 4.6 mm of length (3.97 mm from pad edge) | last 4.40 mm of length | not read |
| Keep-out rule from the maker of the part | text only: no ground under the antenna, antenna end past the host ground at an edge | text only: keep the antenna exposed, never inside a metal case | drawing: "RF keepout" under the 4.40 mm antenna section and outward from it; metal clear above and below | not read |
| JLCPCB stock | none (supply it yourself) | 61 (S1C), 974 (S1CX) | 349 | 106 |
| Price | about 12 to 14 | 7.69 (S1C), 6.37 (S1CX) | 9.81 | 5.69 |
| Hand solderable | no (inner rows) | no (inner rows), edge pads yes | no | not read |

Sources: Holyiot datasheet (section 3). Ebyte manuals `datasheets-04/e73c.pdf` (https://datasheet.lcsc.com/datasheet/pdf/b8aaa43fc58f1d9f85ede318a8f9cb6b.pdf?productCode=C356849) and `e73cx.pdf` (https://datasheet.lcsc.com/datasheet/pdf/e00fad48164a836ee9b0b584b43d7300.pdf?productCode=C2764963), drawing on manual page 7 of the S1CX manual. u-blox BMD-340 data sheet UBX-19033353 R13, `datasheets-04/bmd-340.pdf`, pages 23 and 26. Confidence: confirmed for values read from the drawings, likely for the Holyiot height.

Notes on the E73 pin map (from the S1CX manual pin table, confirmed): pads 1 P1.11, 2 P1.10, 3 P0.03, 4 P0.28, 6 P1.13, 7 P0.02, 8 P0.29, 9 P0.31, 10 P0.30, 11 P0.00, 12 P0.26, 13 P0.01, 14 P0.06, 15 P0.05, 16 P0.08, 17 P1.09, 18 P0.04, 20 P0.12, 22 P0.07, 26 P0.18/RESET, 28 P0.15, 30 P0.17, 32 P0.20, 33 P0.13, 34 P0.22, 35 P0.24, 36 P1.00, 38 P1.02, 40 P1.04, 41 P0.09, 42 P1.06, 43 P0.10. Power and debug: 5, 21, 24 GND, 19 VCC, 23 VDDH, 25 DCCH, 27 VBUS, 29 D-, 31 D+, 37 SWDIO, 39 SWCLK. The manual marks P0.02, P0.03, P0.28 to P0.31, P1.04, P1.06, P1.10, P1.11, P1.13 and the NFC pins as low-frequency, standard-drive pins. These suit the matrix and the encoders. The 16 remaining pins cover QSPI (6), display SPI (4), I2C (2) and the backlight.

The S1C and S1CX share one outline and one pad pattern, so a single footprint accepts either antenna option. The 32.768 kHz crystal is not on the E73 module ("32.768KHz crystal needs external connection").

Raytac MDBT53 (datasheet `datasheets-04/mdbt53.pdf`) asks for a "No Ground Pad" area under the antenna in every layer and placement at the board edge. Its drawings were not measured.

---

## 6. ZMK support

Sources: ZMK repository tree at `main` (commit `4dd95d7840eb3d5a3f59bb29fbf1ab054715ef85`, 2026-10-09, the same commit that worxboard pins), `app/west.yml`, board files, documentation sources and the Zephyr 4.1 blog post. Cached in `zmk-05/`.

| Fact | Source | Confidence |
| --- | --- | --- |
| ZMK `main` builds on Zephyr `v4.1.0+zmk-fixes` with LVGL 9.3.0. | `app/west.yml`; https://zmk.dev/blog/2025/12/09/zephyr-4-1 | confirmed |
| nRF52840 is the main ZMK target. Most in-tree wireless boards use it (nice!nano, XIAO BLE, nRF52840 DK, Glove80, Adv360 Pro and others). | `app/boards/` tree, 44 board directories | confirmed |
| nRF5340: exactly one in-tree board, the nRF5340 DK (`nrf5340dk/nrf5340/cpuapp`), with USB and BLE outputs. It is listed among boards "implemented and tested by contributors". Its files only raise two stack sizes and an I2C buffer. | `app/boards/nordic/nrf5340dk/*`; https://zmk.dev/docs/hardware | confirmed |
| On the nRF5340, ZMK runs on the application core. A separate controller image for the network core must be built from a Zephyr sample and flashed, and again after each Zephyr upgrade. A custom board needs two board definitions, one per core. | ZMK documentation, `docs/docs/development/local-toolchain/build-flash.mdx`, section "Multi-CPU and Dual-Chip Bluetooth Boards" | confirmed |
| The same page still names the sample `hci_rpmsg` and the board `nrf5340dk_nrf5340_cpunet`, which are names from before Zephyr 4.1. The nRF5340 path is documented but not kept current. The ZMK tree holds no sysbuild or network-core files. | Same file; tree search for `sysbuild`, `hci_ipc`, `cpunet` returned nothing | confirmed (text), likely (maintenance level) |
| The Zephyr 4.1 move brought Hardware Model v2, "providing better support for SoCs which have multiple cores on the same chip, such as the nRF5340". | https://zmk.dev/blog/2025/12/09/zephyr-4-1 | confirmed |
| A shipping product proves ZMK with LVGL 9 and a colour ST7789V on an nRF5340: the GLYF firmware itself. | `research/raw/regulatory-software.md` section 2 | confirmed |
| nRF54L15: no board in the ZMK tree, and no issue or pull request about it (searches for `nrf54`, `nrf54l`, `54L15` returned no board work). | GitHub issue search, `zmk-05/iss_*.json` | confirmed (absence on this date) |
| The nRF54L15 has no USB device peripheral. High-speed USB exists only on the nRF54LM20A and nRF54LM20B. | https://www.nordicsemi.com/products/nrf54l15 (search summary); Ebyte E73-2G4M08S1F manual interface list | likely |
| nRF54LM20A: two community repositories from November 2026 port ZMK v0.3.0 to a newer Zephyr on a Minew ME54BS13 module. The author calls it experimental and "not a claim of upstream nRF54LM20A support". | https://github.com/freather-keyspensory/zmk-nrf54lm20a (README) | confirmed |
| Displays in ZMK: the documentation still says the feature "is not yet considered production-ready" and speaks of OLED and e-paper panels. The built-in status screen defaults to a monochrome theme and a 4,096-byte LVGL pool. Colour screens come from external modules (Prospector and others, see `research/raw/prior-art.md`). | `docs/docs/features/displays.md`; `app/src/display/Kconfig` | confirmed |

Summary by SoC:

- nRF52840: first-class in ZMK. Colour LVGL works through a module and is proven on this SoC (Prospector). Firmware update by UF2 drag and drop once a bootloader is flashed over SWD.
- nRF5340: works, proven by the maker's product and by one tested development kit. It costs a second firmware image, two board definitions, SWD access for the network core, and MCUboot in place of a UF2 bootloader.
- nRF54L15: not usable for this product (no USB, no ZMK board).

---

## 7. Recommendation and decision rule

Recommended: an nRF52840 module from JLCPCB stock.

1. First choice: the Ebyte E73-2G4M08S1C / S1CX footprint (C356849 or C2764963). Reasons: in stock and placed by JLCPCB, 1.27 mm pitch, the lowest price, and one footprint for two antenna options. The S1CX with an external antenna matters for a body made of two aluminium shells, where an on-module antenna is enclosed by metal. The pin budget of 27 fits in 29 to 31 usable pins.
2. Alternative: u-blox BMD-340-A-R (C5456944). Reasons: 48 GPIO, 1.9 mm height, documented keep-out drawing and certifications. Costs: LGA pads of 0.5 mm in three rows need via fan-out and cannot be reworked by hand.
3. Conditions for the nRF52840 route: the LVGL draw buffer must be partial (for example 20 to 25 % of the frame), and heaps, stacks and USB buffers must be sized with care. A 32.768 kHz crystal is optional on the E73 and costs two pins. If the pin count is short, the flash can share the display SPI bus in place of QSPI, which frees four pins.

Use the Holyiot-21069 only if the firmware plan needs more than 256 KB of RAM, for example a full-frame buffer together with the maker's whole feature set. It then has to be bought separately and consigned to JLCPCB, or soldered with hot air as the maker did. NORA-B106 or MDBT53-1M are the nRF5340 modules that JLCPCB lists with a price, both at stock 0, so they need pre-order.

This recommendation is a judgement, not a measured result. The open risk is RAM on the nRF52840: no build of the planned worxpad firmware exists yet to measure. Confidence: likely.

Design consequences that hold for every candidate:

- Place the module at a board edge with the antenna end outward, with a copper-free zone in all layers under the antenna section (4.3 to 4.6 mm of module length) and several millimetres beyond it. Metal of the case must stay clear above and below that zone, or the antenna must leave the metal body through an IPEX lead.
- Every candidate has pads under the body. All need reflow; none can be fitted with a soldering iron alone.
- The Holyiot datasheet forbids a second reflow with the module hanging on the lower side. Keep the module on the side that is soldered last, or use one-sided assembly as the maker did.
- All modules ship blank. An SWD header is needed on the board for the first programming.

---

## 8. Conflict found in earlier notes

`research/raw/social.md` section 4.1 states that JLCPCB did not place the module and the maker soldered it by hot air. `research/raw/youtube.md` (assembly table) states that "The Holyiot module is in the JLCPCB placement". The JLCPCB library records for this module show that some customers do have it placed from their own supply, so both are possible. The two notes should be reconciled from the source frames.

---

## 9. Sources read

- Maker firmware images `research/_cache/regulatory-software/firmware-06/zmk.signed.v0.1.0.bin` to `v0.1.4.bin` (static analysis only).
- Existing notes: `research/raw/regulatory-software.md`, `social.md`, `youtube.md`, `prior-art.md`, `conventions.md`, `official-site.md`, `community-press.md`.
- https://fccid.io/2ALGY21069 and its files: User Manual 5961970 (Holyiot-21069 datasheet), Internal Photos 5961963, External Photos 5961962 (downloaded, not examined in detail).
- https://www.nordicsemi.com/Products/nRF5340/Modules (third-party module list).
- https://electropeak.com/holyiot-nrf5340-microcontroller-breakout-board-with-ceramic-antenna
- JLCPCB parts search API, 27 keyword queries (nRF5340, nRF52840, nRF54L15, nRF54L, nRF52833, MDBT50Q, MDBT53, E73-2G4, E83-2G4, MS88SF, MS45SF, MS50SF, ME54BS, HOLYIOT, NORA-B1, NINA-B3, BMD-340, BL654, BT840, MK08, ISP1807, XIAO and others).
- LCSC product API for C5355663, C5796572, C20416747, C5119772, C5118826, C5456944, C3030983, C5438434, C3015611, C190794, C6904155, C2688382, C17209540.
- Datasheets: Ebyte E73-2G4M08S1C, E73-2G4M08S1CX, E73-2G4M08S1F; u-blox BMD-340 (UBX-19033353 R13); Raytac MDBT53 (text scan only); Raytac MDBT50Q, Minew MS88SF3 and u-blox NORA-B1 (downloaded, not read in detail).
- https://www.cdebyte.com/products/E73-2G4M08S1C and https://www.cdebyte.com/products/E83-2G4M03S
- ZMK: https://github.com/zmkfirmware/zmk tree at `main`, `app/west.yml`, `app/boards/nordic/nrf5340dk/*`, `app/src/display/Kconfig`, `docs/docs/development/local-toolchain/build-flash.mdx`, `docs/docs/features/displays.md`, `docs/docs/config/displays.md`; pull requests 1562, 1578, 3060; issue 3381; https://zmk.dev/docs/hardware ; https://zmk.dev/blog/2025/12/09/zephyr-4-1
- https://github.com/freather-keyspensory/zmk-nrf54lm20a (README).

## 10. Not reached or not done

- `https://hubtronics.in/docs/Holyiot-21069-nRF5340.pdf` and `https://fcc.report/FCC-ID/2ALGY21069/5961970.pdf`: HTTP 403. The same document was read from fccid.io.
- holyiot.com product page for model 21069: the home page loaded, the product page was not located; a guessed PDF path returned 404.
- AliExpress listing and price for the Holyiot-21069: not found by search; AliExpress pages were not fetched.
- LCSC international has no record for the Ebyte parts C356849, C2764963, C5333991, C54337734 (the API returns an empty result). Their stock figures are JLCPCB figures only.
- GitHub code search needs a login, so ZMK source was searched through the file tree and by direct file reads only.
- The meaning of the `C99...` library records as customer-supplied parts is inferred from their brand, price placeholder and non-purchasable flag. JLCPCB documentation on this was not read.
- Heights and pad drawings of the E73-2G4M08S1F, MDBT53, MDBT50Q, MS88SF3, NORA-B1 and E83-2G4M03S were not measured.
- Certification status (FCC, CE) of the Ebyte E73 modules: not checked.
- No RAM measurement of ZMK with a colour display on an nRF52840 was made; the Prospector settings are the only data point.
- The exact size of the maker's LVGL memory pool and the purpose of each stack were not decoded.
