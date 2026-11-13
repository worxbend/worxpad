# Decision record: microcontroller, radio and firmware stack

Date: 2026-11-13. Subsystem key: `mcu-radio`. Status: decided for prototype batch 1 (5 units).
Revision 2 (2026-11-13): corrected after a review. The part choice is unchanged. The antenna placement
(section 7.3), the standby figures (7.6), the firmware hooks (7.7), the PCB edge rules (8) and several dates and
module facts changed. Section 13 lists every review point and what was done with it.

Confidence labels: **confirmed** (stated by the maker of the part or project, or measured here from a primary
source), **likely** (consistent indirect evidence), **guess** (judgement or arithmetic without a measurement).
"Not found" means the item was looked for and not found. Catalogue stock and prices were read on 2026-11-13 and
change daily. Paths that start with `_cache/` are relative to `research/`.

## 1. Decision in short

1. **SoC: Nordic nRF52840**, not the nRF5340 that the GLYF uses. An offline ZMK build made today for an
   nRF52840 with every framework feature the product needs (5 BLE profiles, USB HID, ZMK Studio over USB and
   BLE, 240 x 240 RGB565 ST7789V with LVGL 9.3, 16 MB QSPI NOR flash with LittleFS, two EC11 encoders, deep
   sleep) links at **124,942 bytes of RAM (47.7 %)** and **374,568 bytes of flash (46.2 %)**. A full-frame LVGL
   buffer still fits (217,102 bytes RAM, 82.8 %). The RAM argument for the nRF5340 is gone. (confirmed, section 4)
2. **Module: u-blox BMD-340-A-R** (JLCPCB/LCSC C5456944, extended part, 349 at JLCPCB and 190 at LCSC, USD 9.81).
   It is an LGA module of 15.0 x 10.2 x 1.9 mm with an on-module PCB trace antenna, 48 GPIO, on-module 32 MHz
   crystal and DC/DC, and modular radio approvals (FCC ID 2AA9B10, ISED 12208A-10, CE RED, MIC, KC, RCM,
   Bluetooth QDID 95452). The only current type number is BMD-340-A-R-10; the LCSC catalogue photo shows that
   type with date code 22/29. (confirmed; stock type likely)
3. **Antenna: the module's own PCB trace antenna, no coaxial connector, in a defined RF bay.** The module sits
   on the PCB bottom face at the right board edge, antenna end at the edge, centre 53 mm from the rear face. The
   bay around the antenna holds no metal within 5 mm (section 7.3). The GLYF control column leaves no such
   place, so **the worxpad body grows 8.0 mm on the right side (128.4 x 85.2 mm instead of 120.4 x 85.2 mm)**,
   which moves the display edge away from the antenna. The case gives a non-metal window in the right wall
   (a plastic insert in a slot). A non-metal bottom shell is the fallback. (decision; RF performance in aluminium
   is not measured)
4. **Icon storage: Winbond W25Q128JVSIQ**, 16 MB quad-SPI NOR (C97521, JLCPCB basic part, 68,924 in stock,
   USD 2.26), on the nRF52840 QSPI peripheral, LittleFS. (confirmed)
5. **Low-frequency clock: Epson Q13FC1350000400 32.768 kHz crystal** (C32346, basic part, 12.5 pF, +/-20 ppm)
   with two 20 pF C0G capacitors (C1554, basic). (confirmed part data; capacitor value is calculated)
6. **Firmware: ZMK** pinned to the commit worxboard already uses (`4dd95d7840eb3d5a3f59bb29fbf1ab054715ef85`,
   which is also ZMK `main` HEAD today), Zephyr 4.1, LVGL 9.3, built in the digest-pinned
   `zmkfirmware/zmk-build-arm` image. Stock ZMK does not put the panel or the flash to sleep while a host stays
   connected, so a small worxpad module adds two power hooks (section 7.7). Bootloader: **Adafruit nRF52 UF2
   bootloader 0.11.0** (released 2026-05-21; drag-and-drop flashing, double-reset entry), flashed once over SWD.
   Keymap editing: stock ZMK Studio over USB and BLE. Host widget channel: a **Raw HID** interface on USB and on
   BLE HID, written as an own worxpad module after the `zmk-raw-hid` pattern. Icon sets upload over USB; BLE
   carries widget updates. (decision)
7. RMK stays a compatible alternative: the same board runs RMK without hardware changes (nRF52840 BLE
   multi-device, ST7789 through `lcd-async`). Nothing on the board may depend on ZMK. (decision)

## 2. Context

worxpad is an open-hardware macropad in the class of the GLYF: 16 keys (4 x 4), two rotary encoders with push,
two round push buttons, a 1.4 inch 240 x 240 IPS colour display, USB-C, Bluetooth multi-host, a LiPo cell and a
slim CNC aluminium body (two shells). The GLYF reference board uses a Holyiot HOLYIOT-21069 nRF5340 module, ZMK
with LVGL 9, an ST7789V panel at 20 MHz SPI, a W25Q128 NOR flash, a MAX17048 gauge, a DS3231 RTC, a 5 x 4 direct
GPIO matrix, MCUboot with MCUmgr over USB CDC-ACM, and a ZMK Studio protocol fork for widgets
(`research/raw/regulatory-software.md` section 2, confirmed). The decoded GLYF v0.1.4 image needs at least
373,140 bytes of static RAM (`research/raw/follow-radio-module-choice.md` section 2, likely lower bound), which
is why the earlier note kept the nRF5340 open. Its radio module has no designed RF exit in the aluminium body
(`research/raw/follow-rf-exit-in-aluminium.md`, confirmed for the filmed samples).

Family conventions (`research/raw/conventions.md`): worxboard builds ZMK from a pinned commit in a pinned image
and checks the pin map against `board.toml`; macropad puts all machine-placed parts on the PCB bottom; the
macropad PCB router works on two layers only; KiCad moves to 10.0.7. The key stack is fixed in
`research/components/keys.md` section 6.3 (Kailh Choc V2): PCB top face 6.20 mm and PCB bottom face 7.80 mm
below the deck. Section 7.3 uses these heights.

## 3. Requirements

| # | Requirement | Source |
| --- | --- | --- |
| R1 | BLE HID with at least 4 bonded hosts and fast switching between them. GLYF claims 4. | task; `official-site.md` |
| R2 | USB device: HID, plus drag-and-drop or DFU flashing. | task |
| R3 | Weeks of standby on a small LiPo (reference cell 1,200 mAh). | task; `follow-battery-cell-and-runtime.md` |
| R4 | Drive the 240 x 240 RGB565 ST7789V-class panel at a usable refresh. | task; `follow-display-module-sourcing.md` |
| R5 | About 30 GPIO: 16 keys, 2 encoders with push, 2 buttons, display SPI with DC, reset and backlight PWM, battery sense, charger status, VBUS detect, spare I2C. | task |
| R6 | Host channel for widgets (clock, now playing, per-app icon sets) over USB and BLE. | task |
| R7 | Icon storage: 16 layers x 16 icons, megabytes. | task |
| R8 | Radio must work inside a two-shell aluminium body. | task; `follow-rf-exit-in-aluminium.md` |
| R9 | JLCPCB can place it; a first batch of 5 units; function beats fee savings. | task |

## 4. New evidence gathered for this record

### 4.1 RAM and flash measurement on the nRF52840 (offline ZMK build)

Method: a throw-away ZMK shield `wpprobe` on the in-tree `nice_nano@2.0.0//zmk` board (nRF52840, Adafruit UF2
partition layout). Built with worxboard's existing west workspace (`/home/worxbend/Projects/worxboard/build/fw-ws`,
mounted read-only) in the image pinned in worxboard `tools/images.lock`
(`zmkfirmware/zmk-build-arm@sha256:edb1c953...`), with `--network none`, snippet `studio-rpc-usb-uart` and
`CONFIG_ZMK_STUDIO=y`. The shield declares a 4 x 5 col2row matrix with a physical layout (Studio requirement),
two `alps,ec11` encoders, `sitronix,st7789v` 240 x 240 RGB565 on `zephyr,mipi-dbi-spi` over SPIM3, a
`nordic,qspi-nor` W25Q128JV (JEDEC `ef 40 18`, `has-dpd`) with an 8 MB LittleFS partition, deep sleep and
blank-on-idle. Inputs, logs and `.config`: `_cache/mcu-radio/probe-06/`. Resolved configuration includes
`CONFIG_BT_MAX_CONN=5`, `CONFIG_BT_MAX_PAIRED=5`, `CONFIG_ZMK_STUDIO_TRANSPORT_BLE=y`,
`CONFIG_ZMK_STUDIO_TRANSPORT_UART=y`, `CONFIG_BT_LL_SW_SPLIT=y`, `CONFIG_NRF52_ANOMALY_198_WORKAROUND=y`,
`CONFIG_PM_DEVICE=y`, `CONFIG_ZMK_PM_DEVICE_SUSPEND_RESUME=y` and `# CONFIG_PM_DEVICE_RUNTIME is not set`.

| Build | LVGL draw buffer | LVGL pool | RAM used (of 262,144) | Flash used (of 811,008) |
| --- | --- | --- | --- | --- |
| A | 20 % single (23,040 B) | 32 KB | 124,942 B (47.66 %) | 374,568 B (46.19 %) |
| B | 100 % single (115,200 B, as GLYF) | 32 KB | 217,102 B (82.82 %) | 374,568 B |
| C | 25 % double (2 x 28,800 B) | 64 KB | 192,270 B (73.35 %) | 374,568 B |

Largest RAM objects in build A: LVGL pool 32,768 B, draw buffer 23,040 B, Studio RPC thread stack 4,096 B, system
work queue stack 3,072 B, display work queue stack 3,072 B, Bluetooth connection pool 2,200 B
(`_cache/mcu-radio/probe-06/ram-top-a.txt`).

What it shows: ZMK with the full framework feature set leaves 137 KB (A) or 70 KB (C) of RAM for the worxpad UI,
widget state, image cache and the Raw HID module. Confidence: confirmed for the framework; the product UI code
and the Raw HID module were not in the build, so the final figure is not measured. The flash region of
811,008 B (0x26000 to 0xEC000) is confirmed from the ZMK nice_nano board file.

### 4.2 Upstream state checked today

| Fact | Source | Confidence |
| --- | --- | --- |
| ZMK `main` HEAD is commit `4dd95d78...` of 2026-10-09, the commit worxboard pins. | https://github.com/zmkfirmware/zmk/commits/main.atom (`_cache/mcu-radio/zmk-03/zmk_main.atom`); `git log` in the worxboard workspace | confirmed |
| ZMK defaults to 5 BLE profiles; `CONFIG_BT_MAX_CONN` and `CONFIG_BT_MAX_PAIRED` default to 5 and should be equal. | `docs/docs/features/bluetooth.md`, `docs/docs/config/system.md` at main | confirmed |
| ZMK Studio has a BLE GATT transport (`CONFIG_ZMK_STUDIO_TRANSPORT_BLE`, default y with BLE) and a serial transport. Over BLE it works with the Linux web app and the native apps only. | `app/src/studio/Kconfig`, `docs/docs/features/studio.md` | confirmed |
| Studio RPC subsystems are fixed by the protobuf `oneof` in `zmk-studio-messages` (core, behaviors, keymap, plus meta). A custom subsystem needs a fork of the messages and of the Studio client, which is what the GLYF did. | `app/include/zmk/studio/rpc.h`; https://github.com/zmkfirmware/zmk-studio-messages `proto/zmk/studio.proto` | confirmed |
| Deep sleep (`CONFIG_ZMK_SLEEP`, default timeout 900,000 ms) and soft off exist; idle (display off, BLE kept) after 30,000 ms by default. Deep sleep is skipped while USB power is present. | `docs/docs/config/power.md`, `docs/docs/features/low-power-states.md`; `app/src/activity.c` lines 77-93 | confirmed |
| On idle, ZMK only calls `display_blanking_on()` and switches off the optional `zmk,display-led`. The Zephyr ST7789V driver maps blanking to DISPOFF (0x28). SLPIN (0x10) is sent only by the driver's PM SUSPEND action. | `zmk/app/src/display/main.c` lines 76-86; `zephyr/drivers/display/display_st7789v.c` lines 116-124 and 440-458, worxboard workspace at `4dd95d78` | confirmed |
| `zmk,display-led` is "the LED device to use for on/off blanking ... Can be a PWM or GPIO LED device." | `zmk/docs/docs/config/displays.md` line 75 | confirmed |
| The nRF QSPI NOR driver deactivates the QSPI peripheral after every access, but puts the flash into deep power-down only from its PM SUSPEND action. With `CONFIG_PM_DEVICE_RUNTIME` off, no idle path reaches it. ZMK suspends all devices only before deep sleep and soft off. | `zephyr/drivers/flash/nrf_qspi_nor.c` lines 297-350 and 1274-1345; `zmk/app/src/activity.c` lines 77-88; `zmk/app/src/pm.c` lines 23-75 and 91-130 | confirmed |
| The ZMK EC11 driver configures A and B as plain inputs with the devicetree flags and has no PM action, so internal pull-ups stay on in idle and in soft off. | `zmk/app/module/drivers/sensor/ec11/ec11.c` lines 128-133 | confirmed |
| `zmk-raw-hid` gives bidirectional Raw HID "over USB and BT", usage page 0xFF60, usage 0x61, 32-byte reports by default. Its USB receive path is SET_REPORT on the control endpoint (no interrupt OUT); its BLE path defines a second HID service. Its CI and west manifest were pinned to ZMK v0.3 on 2026-05-11. The cached `main` snapshot has no licence file. | https://github.com/zzeneg/zmk-raw-hid README, `src/usb_hid.c`, `src/hog.c`, commit e25e325 (`_cache/mcu-radio-sceptic/src-05/zmk-raw-hid/zmk-raw-hid-main/`, `_cache/mcu-radio-sceptic/gh-04/zmk_raw_hid_pin_v03.patch`) | confirmed |
| Zephyr's legacy USB HID class offers `CONFIG_ENABLE_HID_INT_OUT_EP` (interrupt OUT endpoint, global for all HID instances). The probe uses the legacy stack with `CONFIG_USB_HID_POLL_INTERVAL_MS=1`. | `zephyr/subsys/usb/device/class/hid/Kconfig` line 29; probe `.config` lines 42, 254, 2930 | confirmed |
| RMK: BLE multi-device on nRF52, nRF54, ESP32, Pico W; tested on nRF52840. Vial and the experimental Rynk protocol, also over BLE. Colour panels including ST7789 through `lcd-async`; colour needs a custom renderer; no LVGL. | https://github.com/rmk-rs/rmk README; `docs/docs/main/docs/features/display.md` (`_cache/mcu-radio/gh-02/`, `web-04/`) | confirmed (project claims) |
| Adafruit nRF52 bootloader: latest release 0.11.0 of 2026-05-21 (0.10.0 is of 2026-02-03). 0.11.0 adds ACL write protection of the MBR and bootloader (#384) and a jump to the application when USB disconnects (#390). UF2 and CDC; double reset within 500 ms enters DFU on nRF52840; UF2 family 0xADA52840; application at 0x26000 with S140 v6. | https://github.com/adafruit/Adafruit_nRF52_Bootloader/releases/tag/0.11.0 and README (`_cache/mcu-radio-sceptic/gh-04/adafruit_bl_releases.atom`, `adafruit_bl_0.11.0.html`) | confirmed |
| nRF52840 SPIM0 to SPIM2 do not support more than 8 Mbps; SPIM3 offers the 32 Mbps setting. | https://docs.nordicsemi.com/bundle/ps_nrf52840/page/spim.html | confirmed (32 Mbps setting); likely (instance mapping, read from the configuration table) |
| ST7789V serial write cycle minimum 66 ns, which is about 15.2 MHz. In Sleep In mode "the MCU interface and memory works with VDDI power supply. Contents of the memory are safe." | ST7789V datasheet, `_cache/follow-battery-cell-and-runtime/ds-07/st.txt` lines 2237 and 5943-5945 | confirmed |
| ESP32-S3 in Espressif's BLE power-save example: 230 uA light sleep with 32 kHz crystal, 3.3 mA with main crystal. | https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/nimble/power_save/README.md (`_cache/mcu-radio/web-04/`) | confirmed (vendor example figure) |
| JLCPCB: "Edge rails and fiducials are required for standard PCB assembly"; rails are at least 5 mm wide and are delivered attached by default. The assembly terms ask for a component body at least 2.5 mm from the board edge; copper at least 0.4 mm from a V-cut centre line. | https://jlcpcb.com/help/article/how-to-add-edge-rails-fiducials-for-pcb-assembly-order (read 2026-11-13); assembly terms and V-cut guide via search summary | confirmed (rails); likely (2.5 mm, 0.4 mm) |
| JLCPCB stores MSL parts dry and re-dries parts that exceed their exposure limit. | https://jlcpcb.com/help/article/moisture-sensitivity-level-msl-for-electronic-parts (search summary) | likely |

## 5. Candidates

### 5.1 SoC and platform

| Option | USB device | RAM | ZMK | Standby with a BLE link | JLCPCB module today | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **nRF52840** | yes | 256 KB | main target, UF2 | 23 uA per idle host connection (ZMK measured value) | BMD-340 349; E73-S1C 61; E73-S1CX 974 | **chosen** |
| nRF5340 (GLYF) | yes | 512 KB app core | one DK board; needs a network-core image and two board definitions | 32 uA at 100 ms interval (Nordic profiler, from the battery note) | Holyiot-21069 not sold (customer records C9900280684, C9900154256); NORA-B106 0; MDBT53-1M 0; NORA-B100 7 (U.FL only); E83-2G4M03S 1 | rejected |
| nRF52833 | yes | 128 KB | yes | as nRF52840 | modules 0 | rejected: build A already needs 125 KB |
| nRF54L15 | **no** | 256 KB | no board | low | E73-2G4M08S1F 106 | rejected: no USB device |
| nRF54LM20A | yes | 512 KB | no upstream board (RMK tested) | low | all records 0 (C52078754, ME54BS13 C55387124) | rejected: no stock |
| ESP32-S3 (MINI-1, WROOM-1) | yes (OTG) | 512 KB + PSRAM | no | 230 uA light sleep, vendor example | MINI-1-N8 C2913206 21,084; WROOM-1-N16R8 C2913202 22,336 | rejected |
| ESP32-C6 | no (USB Serial/JTAG only) | 512 KB | no | 34 uA, vendor example | MINI-1-H4 C6553337 1,790 | rejected: no HID over USB |
| RP2350 plus radio | yes | 520 KB | yes, but no BLE | depends on radio | RP2350A C42411118 5,430 (no radio) | rejected |
| WCH CH582 / CH592 | yes | about 32 KB | no | low | CH582F C3001175 1,183; CH592F C39831287 26,183 | rejected: RAM |

### 5.2 nRF52840 module

| Module | LCSC / JLCPCB | Class | Stock JLCPCB (LCSC) | USD | Size, height | Pads | GPIO | Antenna | Approvals | KiCad 10 stock lib |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **u-blox BMD-340-A-R** | C5456944 | extended | 349 (190) | 9.81 | 15.0 x 10.2 x 1.9 mm | 68 LGA, 0.50 mm square, 1.10 mm pitch, staggered rows | 48 | PCB trace, -1 dBi | FCC, ISED, CE, MIC, KC, RCM, BT QDID | none |
| Ebyte E73-2G4M08S1C | C356849 | extended | 61 (no LCSC record) | 7.69 | 18.0 x 13.0 x 3.0 mm | 43: 28 castellated at 1.27 mm plus 15 inner | 32 (29 usable with LFXO) | ceramic chip | not stated in the manual | none (only E73-2G4M04S) |
| Ebyte E73-2G4M08S1CX | C2764963 | extended | 974 | 6.37 | as S1C | as S1C | as S1C | IPEX connector | not stated | none |
| u-blox NINA-B306-00B | C6127317 | extended | 31 (31) | 19.96 | 10 x 15 mm | 55 LGA | not read | PCB trace | not read | none |
| Raytac MDBT50Q-1MV2 / -P1MV2 | C5118826 / C5119772 | extended | 0 / 0 | 19.06 / 7.96 | 10.5 x 15.5 mm | 61 | 48 | chip / PCB | not read | symbol, footprint and 3D model |
| Minew MS88SF2 / MS88SF3 | C2836129 / C20416747 | extended | 0 / 0 | n/a | 23.2 x 17.4 / 18.5 x 12.5 mm | | | | | none |
| Fanstel BT840, BT840E, BT840F | C5182373, C5162133, C5441442 | extended | 0 | 10 to 21 | | | | | | none |
| Holyiot 18010 | C9900042076 | customer record | 0, not sold | n/a | 18 x 13.5 mm | LCC-LGA 55 | | | | none |
| Seeed XIAO nRF52840 (SMD) | C37327670 | extended | 0 | 29.96 | 21 x 17.8 mm | | 11 | chip | | none |
| Bare nRF52840-QIAA-R | C190794 | extended | 43,491 | 7.58 | aQFN-73, 7 x 7 mm | | 48 | own design | own certification | symbol only |

Stock and prices: `_cache/mcu-radio/jlc-01/*.json` (JLCPCB parts API v2) and `_cache/mcu-radio/lcsc-05/*.json`
(LCSC product API), both read 2026-11-13. The review re-read the BMD-340, flash, crystal, capacitor and E73
records the same day and found the same figures (`_cache/mcu-radio-sceptic/jlc-01/`, `lcsc-02/`). KiCad: listing
of `kicad/kicad:10.0.7` and `10.0.7-full` (`/usr/share/kicad/footprints/RF_Module.pretty`,
`symbols/RF_Module.kicad_sym`, `3dmodels/RF_Module.3dshapes`). The E73 pad count above is my reading of the S1CX
drawing (`_cache/follow-radio-module-choice/datasheets-04/e73cx_p-08.png`); `follow-radio-module-choice.md` says
26 castellated plus 17 inner, so one of the two readings is wrong.

### 5.3 Firmware stack

| Option | BLE multi-host | Colour display | Host widget channel | Flashing | Family fit | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **ZMK (pinned main)** | 5 profiles, years of field use | Zephyr ST7789V driver plus LVGL 9.3; custom status screen needed | own Raw HID module on USB and BLE; Studio for keymaps | UF2 | worxboard uses it, pinned | **chosen** |
| RMK | yes, nRF52840 tested | ST7789 via `lcd-async`, custom Rgb565 renderer, no LVGL | Rynk (experimental) or custom | UF2 or probe | owner writes embassy in macropad | alternative, same hardware |
| Custom Zephyr or embassy application | to be written | free | free | free | partial | rejected for batch 1 |
| KMK (CircuitPython) | limited | displayio | custom | UF2 | none | rejected |

### 5.4 Host widget channel

| Option | USB | BLE | Host side | Verdict |
| --- | --- | --- | --- | --- |
| **Raw HID (usage page 0xFF60), own module after the `zmk-raw-hid` pattern** | IN on the interrupt endpoint; OUT by SET_REPORT, or an interrupt OUT endpoint if `CONFIG_ENABLE_HID_INT_OUT_EP` is used | a vendor report in a second HID-over-GATT service | hidapi on Windows, macOS, Linux | **chosen**; untested against the pinned ZMK; BLE host access not yet verified |
| ZMK Studio protocol fork (GLYF route) | CDC-ACM | Studio GATT | forked Studio client | rejected: forks two upstream repositories |
| Custom GATT service plus CDC-ACM | CDC-ACM | own service | two code paths | fallback if Raw HID over BLE fails on a host OS |
| USB mass storage for icons | MSC | none | file copy | not chosen; no BLE path |

The `zmk-raw-hid` code is not copied: its cached snapshot carries no licence file. The worxpad module is written
from the Zephyr USB HID and Bluetooth GATT APIs. Upload speed (guess, not measured): SET_REPORT with 32-byte
reports at about one control transfer per 1 ms frame gives about 32 KB/s, so one 1.77 MB icon set takes about a
minute over USB; BLE with 62-byte GATT payloads at a 7.5 to 15 ms interval is several times slower. Icon sets
therefore upload over USB in batch 1; BLE carries widget updates (clock, now playing text, small images).

### 5.5 Antenna type

| Option | Assembly | Certification | Verdict |
| --- | --- | --- | --- |
| **On-module PCB trace antenna at a board edge, in a metal-free bay behind a non-metal wall window** | JLCPCB places the whole radio | module grant unchanged | **chosen** |
| On-module ceramic chip antenna (E73-S1C, Holyiot) | same | depends on module | equal in function; module rejected on other grounds |
| U.FL (IPEX) plus FPC antenna at the window | cable and antenna fitted by hand | antenna change outside a module grant | rejected; still needs the window |
| No exit, rely on shell seam leakage (GLYF) | none | | rejected: no range data exists |

## 6. Decision and reasons

The nRF52840 is the SoC because it meets every requirement at the lowest risk. Build A shows that RAM and flash
are sufficient with room left. ZMK treats the nRF52840 as its main target, gives UF2 drag-and-drop updates
(R2), 5 BLE profiles (R1), deep sleep, and the radio can transmit at up to +8 dBm, which helps in a metal body.
The nRF5340 would add a network-core image, two board definitions, MCUboot instead of UF2, and a module that
JLCPCB does not sell.

The BMD-340-A-R is the module. Against the Ebyte E73-2G4M08S1C, the second choice, it has:

- deeper stock (349 at JLCPCB, 190 more at LCSC, against 61);
- lower height (1.9 mm against 3.0 mm), close to the 1.85 mm hot-swap sockets on the same face;
- 48 GPIO against 29 usable, so QSPI, the 32.768 kHz crystal and the full pin list fit with 14 spare pins;
- a dimensioned RF keep-out drawing and a statement on metal enclosures;
- modular approvals in six regions.

It costs USD 2.12 more per unit, and its LGA pads cannot be reworked with an iron. Both modules need reflow.

The antenna needs a metal-free bay that the GLYF layout cannot give (section 7.3.2). Moving the display 8 mm away
from the right edge is the cheapest change that gives it: one dimension of the case and the PCB grows, nothing
else moves relative to the key field, and the radio part stays fully machine-placed.

Icon storage goes to a 16 MB QSPI NOR because it is a JLCPCB basic part at the same price as smaller parts, the
reference product proves the size, and the nRF52840 QSPI reads at 32 MHz quad. 256 icons of 48 x 48 pixels in
RGB565 with an 8-bit alpha plane take about 1.77 MB, so 16 MB leaves room for several icon sets (arithmetic).

ZMK is the firmware because it is the family's wireless stack and it already covers multi-host BLE, USB/BLE
output switching, encoders, Studio and sleep. The UI, the widget channel and the two power hooks are ZMK
modules. The hardware stays firmware-neutral so that RMK remains an option.

## 7. Numbers the design needs

### 7.1 BMD-340-A-R module facts

Source: u-blox BMD-340 data sheet UBX-19033353 R13 (20-Jun-2022), cached at
`_cache/follow-radio-module-choice/datasheets-04/bmd-340.pdf` and, byte-identical from LCSC,
`_cache/mcu-radio-sceptic/ds-03/bmd340.pdf` (LCSC link:
https://datasheet.lcsc.com/datasheet/pdf/aa3b9fb89c9758337cc45b4faf24ab9d.pdf?productCode=C5456944).
All rows confirmed unless marked.

| Item | Value |
| --- | --- |
| Type numbers | BMD-340-A-R-00 and -01 are Obsolete; -10 is in mass production (data sheet product table, p.2). -01 and newer use nRF52840 silicon rev 2 or newer (table 9). The LCSC catalogue photo of C5456944 (dated 2025-12-04) shows an "A-R-10" label with date code 22/29, that is 2022 week 29 (likely for the stock; the reel itself is not seen). |
| Outline | 15.0 x 10.2 mm, +/-0.3 mm |
| Height above the host PCB | 1.9 +/-0.1 mm (module PCB 0.5 mm plus shield can) |
| Pads | 68 LGA pads, 0.50 x 0.50 mm, 1.10 mm pitch, outer row plus two staggered inner rows (datasheet figure 12). JLCPCB lists the package as "LGA-60"; the footprint follows the datasheet. |
| Mass | 0.676 g (LCSC record) |
| Antenna | Integrated PCB trace antenna in the last 4.40 mm of the 15.0 mm length, across the full 10.2 mm width (pad 45 to 47 side). Max gain -1 dBi. |
| RF keep-out | "The area under and extending out from the antenna portion of the module should be kept clear of copper and other metal. The module should be placed at the edge of the PCB with the antenna edge facing out." "Metal should be kept clear from the antenna area, both above and below." No distance is given. Figure 12 hatches the keep-out past both long sides of the module. Evaluation board: 4.4 mm copper-free strip along the whole 50 mm board edge. |
| Radio | +8 dBm max; TX 14.8 mA at +8 dBm and 4.8 mA at 0 dBm with DC/DC at 3 V; RX 4.6 mA; CPU 3.3 mA; sensitivity -96 dBm |
| Sleep | System OFF 0.4 uA; System ON idle 0.97 uA without RAM retention, 2.35 uA with full 256 KB retention |
| GPIO pull resistors | Pull-up and pull-down 11 / 13 / 16 kOhm min / typ / max (table 10) |
| Supply, LV mode | VCC (pad 17) and VCCH (pad 65) tied to one 1.7 to 3.6 V source. 4.7 uF bulk capacitor inside the module. |
| Supply, HV mode | VCCH 2.5 to 5.5 V in, VCC becomes an output; REG0 gives at most 25 mA in System ON, 1 mA in System OFF, and external loads should stay under 5 mA. Not usable on -00 (silicon rev 1). Not used here: LV mode is chosen for every type. |
| USB | VBUS pad 66 (4.35 to 5.5 V, powers only the USB PHY), D- pad 67, D+ pad 68 |
| Reset | P0.18 (pad 39) when PSELRESET is programmed; internal pull-up |
| SWD | SWCLK pad 43, SWDIO pad 44 |
| 32.768 kHz crystal | Not on the module. XL1 = P0.00 (pad 13), XL2 = P0.01 (pad 14). CL max 12.5 pF, ESR max 100 kOhm, C0 max 2 pF, pin capacitance 4 pF. LFXO 0.23 uA against LFRC 0.7 uA. |
| 32 MHz crystal, DC/DC | On the module |
| Low-frequency-only pins (< 10 kHz, standard drive) | P0.02, P0.03, P0.09, P0.10, P0.28 to P0.31, P1.01 to P1.07, P1.10 to P1.15 (21 pins) |
| Full-speed pins | P0.00, P0.01, P0.04 to P0.08, P0.11 to P0.27 (P0.18 is reset), P1.00, P1.08, P1.09 (27 pins) |
| Analog inputs | AIN0 to AIN7 on P0.02 to P0.05 and P0.28 to P0.31 |
| NFC pins | P0.09, P0.10 (need `CONFIG_NFCT_PINS_AS_GPIOS` to be GPIO) |
| Peripheral pin mux | Any GPIO for UART, I2C, SPI, QSPI, PWM, I2S, PDM |
| Moisture | MSL 3: mount within 168 h of opening at no more than 30 C / 60 %RH, or bake per J-STD-033B if the humidity card reads over 10 % (section 10.3). A 2022 date code means the dry pack must be checked before reflow. |
| JLCPCB placement | Stocked extended part, placeable (confirmed by catalogue); LGA cannot be hand-reworked (likely) |

### 7.2 Proposed pin allocation (BMD-340)

This is a proposal for the schematic step. Pad position: O = outer row, 2 = second row, 3 = third row, as read
from datasheet figure 2. Rule: high-speed and I2C signals on full-speed pins, matrix and encoders on
low-frequency pins, as many outer and second-row pads as possible to ease escape routing.

| Function | nRF pin | Pad | Row | Note |
| --- | --- | --- | --- | --- |
| QSPI SCK | P0.19 | 37 | O | nRF52840 DK QSPI pin set |
| QSPI CSN | P0.17 | 35 | O | |
| QSPI IO0 | P0.20 | 38 | 2 | |
| QSPI IO1 | P0.21 | 36 | 2 | |
| QSPI IO2 | P0.22 | 40 | 2 | |
| QSPI IO3 | P0.23 | 41 | O | |
| Display SCK (SPIM3) | P0.13 | 31 | O | |
| Display MOSI (SPIM3) | P0.15 | 33 | O | |
| Display CS | P0.14 | 32 | 2 | |
| Display DC | P0.16 | 34 | 2 | |
| Display RESET | P1.00 | 56 | 3 | static signal |
| Backlight PWM | P0.24 | 42 | 2 | drives a transistor or LED driver, not the LEDs; declared as the `zmk,display-led` PWM LED |
| I2C SDA | P0.07 | 23 | 2 | 400 kHz needs a full-speed pin |
| I2C SCL | P0.11 | 27 | 2 | |
| Battery ADC (if no gauge) | P0.05 / AIN3 | 21 | 2 | |
| Charger status | P0.03 | 19 | 2 | input |
| Gauge or RTC interrupt | P0.26 | 7 | O | |
| Peripheral rail enable | P1.07 | 50 | 3 | optional |
| Encoder L A / B | P0.28 / P0.30 | 9 / 11 | O | |
| Encoder R A / B | P0.29 / P0.31 | 10 / 12 | 2 | |
| Matrix rows (4) | P1.12, P1.13, P1.14, P1.15 | 61 to 64 | O | col2row, inputs with pull-down |
| Matrix columns (5) | P0.02, P0.25, P0.27, P1.05, P1.06 | 15, 6, 8, 48, 49 | O, 2, 2, 3, 3 | |
| LFXO | P0.00 / P0.01 | 13 / 14 | O / 2 | crystal within a few mm |
| Reset | P0.18 | 39 | O | to reset button or pad |
| SWD | SWCLK / SWDIO | 43 / 44 | O / 2 | to programming pads |
| USB | D- / D+ / VBUS | 67 / 68 / 66 | O | 90 Ohm differential pair |

Used: 34 GPIO including reset and crystal. Spare: P0.04, P0.06, P0.08, P0.09, P0.10, P0.12, P1.01 to P1.04,
P1.08 to P1.11 (14). Direct wiring of all 20 switches without diodes would use 45 of 48 pins and is possible,
at the cost of 11 more traces into the module footprint. VBUS detection needs no GPIO: the nRF52840 USB
peripheral detects VBUS on pad 66 (likely; Zephyr USB device stack reports the connection state).

### 7.3 Antenna bay and the case window

Coordinates in this section: X from the right outer face of the body (positive inward), Y from the rear outer
face, Z from the deck (the top face of the top shell), negative downward. The board edge sits 3.95 mm inside the
outer face (GLYF: 112.5 mm board in a 120.4 mm body, `geometry.md` 4.6; likely). PCB top face Z = -6.20 and PCB
bottom face Z = -7.80 (`keys.md` 6.3, Choc V2 stack). The module hangs under the PCB: module PCB Z -7.80 to
-8.30, shield bottom Z -9.70 (-9.80 max).

#### 7.3.1 What the antenna needs (requirement for PCB and case)

| # | Rule | Value | Basis |
| --- | --- | --- | --- |
| A1 | Module orientation | On the PCB bottom face, long axis square to the board edge, antenna end 0 to 0.2 mm inside the board outline, never overhanging | Datasheet 6.1 (confirmed); no overhang because of the edge rails in section 8 |
| A2 | Antenna strip | Last 4.40 mm of the module, full 10.2 mm width | Datasheet figures 11 and 12 (confirmed) |
| A3 | Copper keep-out, all layers | 4.4 mm deep from the board edge, 20.2 mm along it (strip plus 5.0 mm each side). No traces, pours, vias or parts inside. Ground stitching vias along the border. | Datasheet 6.1 and figure 16 (confirmed for the depth); the 5 mm sides are GLYF practice (likely) |
| A4 | RF bay, plan | From the outer face to 9.4 mm inside the board edge (strip plus 5.0 mm), 20.2 mm along the edge, centred on the module | Datasheet 6.2 "both above and below" (confirmed, no distance given); 5 mm is the project's starting value from `follow-rf-exit-in-aluminium.md` (guess) |
| A5 | RF bay, height | From 5.0 mm above the PCB bottom face to 5.5 mm below it: Z -2.80 to -13.30 | as A4 |
| A6 | Inside the bay | No metal and no parts: no display module, frame or flex, no encoder, button, battery, screw, boss, USB-C shell or shield. Only FR4, the plastic insert and air. | as A4 |
| A7 | Top shell over the bay | The deck may stay but must be pocketed from below to 2.80 mm thickness or less, so that its underside lies at Z -2.80 or higher | follows from A5 |
| A8 | Floor under the bay | Floor top face at Z -13.30 or lower, or the floor under the bay is part of the non-metal insert | follows from A5 |
| A9 | Wall window | Through slot in the outer wall in front of the strip, at least 30 mm long (40 mm preferred), centred on the module, from Z -5.20 to -11.70 (1 mm above the PCB top face to 2 mm below the module bottom). Closed by a non-metal insert (PC, ABS or POM; not metallised, no metallic paint). With the shell split at Z -5.0 (`geometry.md` 4.2) the slot lies wholly in the bottom shell and can be a notch from its top edge. | `follow-rf-exit-in-aluminium.md` rank 1 (guess for the sizes) |

#### 7.3.2 Check against the GLYF control column

Obstacles near the right edge, from `geometry.md` 4.4, 4.5, 4.7 and 7.6 (likely unless marked):

- Right encoder: centre X 10.27, Y 15.10; body about 13 mm square (guess), so Y 8.6 to 21.6. It stands on the
  PCB top face, 1.6 mm above the PCB bottom face, which is inside the bay height.
- Display: lens X 4.0 to 35.2, Y 27.0 to 58.2. The LCD outline is about 1.6 mm inside the lens at the sides, so
  X 5.6 and more, Y about 26.9 to 58.3 (the 31.35 mm module length slightly exceeds the 31.2 mm lens). With a
  2.95 mm stack and the lens level with the deck (assumed), the LCD back lies at Z about -2.95, 4.85 mm above
  the PCB bottom face, which is inside the bay height.
- Right button: tactile switch on the PCB top face, centre X 10.27, Y 71.2, body about 6 x 6 mm (guess).
- Right flank scoop: the body is only 11.7 to 12.0 mm thick within 13 mm of the side up to Y about 43 (+/-3).
  With a 1.5 to 1.8 mm floor the floor top lies at Z -10.2 to -10.5, only 2.4 to 2.7 mm under the PCB bottom
  face and 0.5 to 0.8 mm under the module shield.
- Under the key field the switch plate (part of the top shell) lies at Z -4.00 to -5.20 (`keys.md` 6.3), inside
  the bay height.

Result: within 13.35 mm of the right face the free Y spans are 21.6 to 26.9 (5.3 mm), 58.3 to 68.2 (9.9 mm) and
74.2 to 81.7 (7.5 mm). The bay needs 20.2 mm. The rear, left and front edges fail on the plate, and the rear edge
of the control column also holds both encoders and the USB-C receptacle. **The GLYF layout has no antenna
position that meets A4 to A8.** (confirmed arithmetic on likely inputs.) Revision 1 of this record placed the
module centre 25 to 32 mm from the rear face. That put the antenna strip under the encoder edge (centre 25) or
under the LCD (centre 32) and contradicted its own 5 mm rule. It is withdrawn.

#### 7.3.3 Decision: an 8 mm wider body

1. Add 8.0 mm of body width on the right side. The key field, knobs, lens and buttons keep their positions
   relative to the key field; the margin between the lens and the right face grows from 4.0 to 12.0 mm. Body
   128.4 x 85.2 mm; PCB 120.5 mm wide. The LCD outline moves to X 13.6, outside the bay (13.35). (decision)
2. Rule for any later layout: along the bay, the LCD outline, its frame, flex and connector stay at least 9.4 mm
   (in plan) from the board edge. With the 1.4 inch GLYF-type module (1.6 mm inside the lens) that needs the
   lens edge 11.75 mm or more from the right face; with the 1.3 inch DM-TFT13 panel (26.16 mm wide, 2.5 mm
   inside a 31.2 mm lens) 7.0 mm of extra width would do. The display subsystem chooses the panel; 8.0 mm covers
   both. (arithmetic on `follow-display-module-sourcing.md` and `geometry.md`)
3. Module centre 53 mm from the rear face, antenna end at the right board edge (bay Y 42.9 to 63.1). This keeps
   the bay behind the end of the flank scoop. On the GLYF ramp the body is 16.6 to 14.85 mm thick there
   (`geometry.md` section 5), so A8 holds with a local floor of 1.5 mm or less at the front end of the bay.
   After the shift the encoder bodies (X 12.3 and more, Y 21.6 and less) and the button switches (X 15.3 and
   more) lie outside the bay. (arithmetic)
4. Wall slot per A9 in the right wall, centred at Y 53: Y 38 to 68 for 30 mm, Y 33 to 73 for 40 mm. Where the
   slot reaches into the scoop region (Y below about 43) the wall is only 12 mm tall, so the case subsystem
   either ends the right scoop before the slot or extends the insert round the lower edge. (guess for the fix)
5. The battery, the display flex and the shell screws keep out of the bay (A6). The GLYF cell pocket under the
   rear key rows (`follow-battery-cell-and-runtime.md`) is far from it.

#### 7.3.4 Fallbacks and the acceptance test

1. If the case subsystem keeps the 120.4 mm width: module centre still 53 mm from the rear face (behind the
   flank scoop), antenna under the lens margin. The LCD then lies 4.85 mm above 2.75 mm of the 4.4 mm strip, which breaks the datasheet's
   "metal clear above" rule. Use it only after a comparison test (item 4) shows it within about 3 dB of the bay
   layout. (guess for the margin)
2. Plastic bottom shell with the aluminium top shell (rank 2 in the RF note). No board change is needed.
3. Firmware lever: expose `CONFIG_BT_CTLR_TX_PWR_PLUS_8` (or a lower step) for the aluminium build.
4. Pre-test before the CNC order: line the inner faces of the FDM prototype shells with aluminium foil tape,
   leave the slot open, and compare RSSI against the bare PCB. The FDM case alone is radio-transparent and
   predicts nothing. (engineering judgement, guess)
5. Acceptance test for the aluminium build: a stable link to a laptop and to a phone at 3 m with a hand over the
   device; RSSI loss against the bare PCB at the same distance of no more than about 10 dB; test at 0 dBm and at
   +8 dBm. (from the RF note)

### 7.4 Support parts owned by this subsystem

| Part | Value | Code | Class, stock | Package and height | Datasheet |
| --- | --- | --- | --- | --- | --- |
| W25Q128JVSIQ | 128 Mbit NOR, 2.7 to 3.6 V, 133 MHz, QE bit fixed to 1 for "IQ" (quad ready). Standby 10 uA typ / 60 uA max; power-down 1 / 20 uA; read 8 to 12 mA typ (15 to 20 max); page program and erase 20 mA typ (25 max); tDP 3 us, tRES1 3 us | C97521 | basic, 68,924 | SOIC-8 208 mil, body 5.28 x 5.28 mm, span 7.90 mm, height 2.16 mm max | Winbond W25Q128JV Rev J, `_cache/mcu-radio-sceptic/ds-03/w25q128jv.pdf` (p.62 DC table, AC table); earlier copy Rev I `_cache/follow-battery-cell-and-runtime/ds-07/w25q128jv.pdf`; https://datasheet.lcsc.com/datasheet/pdf/d009d960f1daec6149edaa35b7dae856.pdf?productCode=C97521 |
| Q13FC1350000400 | 32.768 kHz, +/-20 ppm, CL 12.5 pF, ESR 70 kOhm | C32346 | basic, 417,813 | 3.2 x 1.5 mm | https://datasheet.lcsc.com/datasheet/pdf/d4d1bd2e87b2e72a8e8e7fe7d590f4c0.pdf?productCode=C32346 |
| Crystal load capacitors | 20 pF C0G 0402, two | C1554 | basic, 1,176,118 | 0402 | Calculated: C = 2 x CL - Cpin - Cpcb = 25 - 4 - 1 = 20 pF (Cpcb 1 pF is a guess) |
| Flash decoupling | 100 nF 0402 | C1525 | basic | 0402 | |
| Module bulk | 10 uF 0603 at VCC/VCCH | C19702 | basic | 0603 | datasheet advises extra bulk beyond the internal 4.7 uF |

The flash is the tallest part of this subsystem on the bottom face (2.16 mm max, Z -9.96). If the floor
clearance is less than about 2.5 mm, use the WSON-8 5 x 6 mm version W25Q128JVPIQ (C190862, extended, 8,389 in
stock; height not read).

### 7.5 Display bus numbers

- Use SPIM3, the only nRF52840 SPI master above 8 Mbps. Available rates: 8, 16 or 32 MHz.
- ST7789V spec limit: 66 ns write cycle, about 15.2 MHz. 8 MHz is inside the spec; 16 MHz is 6 % faster than the
  spec (the GLYF runs 20 MHz); 32 MHz is common practice but twice the spec. Start at 16 MHz and test 32 MHz on
  the chosen panel. (confirmed limits, guess for the margin)
- Full-frame transfer time for 240 x 240 x 16 bit (921,600 bits): 115.2 ms at 8 MHz, 57.6 ms at 16 MHz, 28.8 ms at
  32 MHz, so a bus ceiling of 8.7, 17 or 34 full frames per second. Widget updates redraw small areas and need
  much less. (arithmetic)
- A 20 % draw buffer holds 48 lines and is flushed five times per full frame. The Zephyr nRF SPIM driver handles
  the EasyDMA length limit; anomaly 198 workaround is on by default (confirmed in build `.config`).

### 7.6 Power numbers (MCU subsystem share)

Inputs: ZMK idle connection 23 uA (ZMK measured value); ST7789V sleep-in IDD 15 uA typ (30 max) plus IDDI 5 uA
typ (10 max), normal mode IDD 6.0 mA typ (7.5 max), no display-off figure in the datasheet (table 3); W25Q128JV
values from 7.4; BMD-340 values from 7.1. Backlight current belongs to the power subsystem and is excluded.

| State | Stock ZMK at the pinned commit | With the worxpad hooks of 7.7 | Confidence |
| --- | --- | --- | --- |
| Idle, display blanked, one host connected (30 s to 15 min after the last input, or longer with USB power) | 23 uA link, plus the panel in sleep-out with DISPOFF (not given; up to the 6.0 mA normal-mode figure, likely milliamperes), plus flash standby 10 uA typ (60 max) | 23 + 20 + 1 = **about 44 uA typ** (83 uA max) | confirmed inputs; total guess |
| Deep sleep (System OFF), link dropped | 0.4 + 20 + 1 = **about 21 uA typ** (61 uA max): stock ZMK suspends the panel (SLPIN) and the flash (DPD) before power-off | same | confirmed path; total guess |
| Peak during an icon upload over BLE | +8 dBm TX 14.8 mA, CPU 3.3 mA, flash program or erase 20 mA typ (25 max), panel logic 6.0 mA typ (7.5 max): **about 44 mA typ, 51 mA max** | same | confirmed inputs |

Add up to 254 uA (3.3 V / 13 kOhm) per encoder contact that rests closed, in idle and in deep sleep, because the
EC11 driver keeps the internal pull-ups on (section 4.2). An encoder whose contacts are both open at every
detent adds nothing (section 8).

Standby arithmetic with a usable 1,020 mAh and about 10 uA for regulator and gauge (guess): with the hooks, the
connected idle state draws about 54 uA, over 2 years on paper, so cell self-discharge limits standby. With stock
ZMK the connected idle state lasts only until deep sleep after 15 minutes on battery; if the panel's display-off
current were 1 mA, a device kept connected (deep sleep disabled) would last about 6 weeks, and at 6 mA about one
week. R3 therefore holds with stock ZMK only because deep sleep drops the link; connected standby needs the
hooks. (arithmetic; the panel current is not known)

### 7.7 Firmware configuration the board must support

- ZMK board definition `worxpad` (hardware model v2, nRF52840 QIAA), Adafruit UF2 partition layout: SoftDevice
  area 0x00000 to 0x26000, code 0x26000 to 0xEC000 (811,008 B), settings storage 0xEC000 to 0xF4000 (32 KB),
  bootloader 0xF4000 to 0x100000. (confirmed from ZMK `nice_nano.dts`)
- LV power mode, REG1 DC/DC on, LFXO as the low-frequency clock source.
- `CONFIG_BT_MAX_CONN=5`, `CONFIG_BT_MAX_PAIRED=5` (default), ZMK Studio with the `studio-rpc-usb-uart` snippet,
  `CONFIG_ZMK_DISPLAY_WORK_QUEUE_DEDICATED=y`, `CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM=y`,
  `CONFIG_LV_Z_VDB_SIZE` 20 to 25, LVGL pool 32 to 96 KB, `CONFIG_ZMK_SLEEP=y`, `wakeup-source` on the kscan,
  `CONFIG_PM_DEVICE=y` and `CONFIG_ZMK_PM_DEVICE_SUSPEND_RESUME=y` (both on in the probe).
- Power hooks (new; stock ZMK lacks them, section 4.2):
  1. Backlight: declare the backlight driver as a `pwm-leds` child and set it as chosen `zmk,display-led`; stock
     ZMK then switches it off on blank and on at full brightness on unblank. Dimming needs own code.
  2. Panel sleep: a worxpad module listens for `zmk_activity_state_changed`. On idle, after blanking, it calls
     `pm_device_action_run(display, PM_DEVICE_ACTION_SUSPEND)` (SLPIN); on activity it calls RESUME (SLPOUT)
     before unblanking. It runs on the display work queue so that no LVGL flush meets a sleeping panel. The panel
     keeps its frame memory in sleep-in (datasheet section 9.1.11).
  3. Flash power-down: `CONFIG_PM_DEVICE_RUNTIME=y` and `zephyr,pm-device-runtime-auto` on the flash node, so
     the driver's `pm_device_runtime_put()` puts the W25Q128 into deep power-down after each access (tDP and
     tRES1 3 us each; the probe node already sets `has-dpd`). ZMK's own suspend loop skips runtime-managed
     devices (`pm.c` line 46), which is consistent. Alternative: suspend the flash in hook 2.
  4. Measure the connected idle current on the first board; target 100 uA or less with the display off. (guess)
- Transmit power: expose `CONFIG_BT_CTLR_TX_PWR_PLUS_8` (or a lower step) for the aluminium build.
- Adafruit bootloader 0.11.0 built for a `worxpad` board header with its LED and DFU pins set to unused or
  harmless pins, so that the bootloader does not drive display or flash lines. Changes #384 and #390 are not
  tested with ZMK; 0.10.0 is the fallback.
- Raw HID module: own code (section 5.4), built and tested against the pinned ZMK before the UI depends on it.
  `CONFIG_ENABLE_HID_INT_OUT_EP` would speed uploads but applies to every HID instance, so ZMK's keyboard
  interface would also gain an OUT endpoint; test it before use.
- USB IDs: use a test pair (pid.codes 1209:0001, as macropad) until own IDs exist; the GLYF beta ships the ZMK
  default 1D50:615E.

## 8. Consequences for other subsystems

| Subsystem | Consequence |
| --- | --- |
| PCB | Draw the BMD-340 footprint, symbol and a simple 3D body from datasheet figure 12; KiCad 10 has none. Check pad count 68 on a 1:1 print. Board 120.5 mm wide (8.0 mm wider than the GLYF board). Module per A1 to A3, centre 53 mm from the rear body face. A 4-layer board with an inner ground plane is recommended for the LGA escape and the USB pair (judgement). The macropad router is 2-layer only, so module escape may need hand routing or router work. Module on the bottom face with all other SMD parts (single-side assembly). JLCPCB edge rails stay attached on the right edge, joined by V-cut; any mouse-bite tab stays at least 10 mm from the antenna strip (guess). The module body is flush with the edge, under the 2.5 mm body-to-edge rule, so rails are required on that side. SWD and reset pads (VCC, SWDIO, SWCLK, RESET, GND), for example a Tag-Connect TC2030-NL pattern or five 1.27 mm pads. Reset button or pad for double-reset UF2 entry. |
| Case | Body 128.4 x 85.2 mm (8.0 mm added on the right). RF bay per A4 to A8: top shell pocketed to 2.80 mm or less over it, floor top at Z -13.30 or lower (or part of the insert), right-wall slot and insert per A9 at Y 38 to 68 or 33 to 73. End the right flank scoop before the slot or extend the insert. No screw, boss or battery in the bay. Floor clearance under the PCB at least 2.5 mm where the module (2.0 mm max) and the SOIC flash (2.16 mm max) sit. The FDM prototype does not test the radio; see 7.3.4 item 4. |
| Display | LCD outline, frame, flex and connector at least 9.4 mm in plan from the board edge along the bay (7.3.3 item 2). 4-wire SPI on SPIM3 at 16 MHz to start; RESET on a GPIO; backlight PWM on P0.24 as `zmk,display-led`. Keep the panel logic powered and use sleep-in instead of cutting its rail, because ZMK documents a blank display after an external power cut (issue 674). |
| Power | One 3.3 V rail into VCC and VCCH (LV mode); the flash needs 2.7 to 3.6 V. The MCU subsystem peaks at about 44 mA typ and 51 mA max; with a 30 to 60 mA backlight on the same rail the regulator needs at least about 110 mA, so choose 150 mA or more (judgement). Quiescent current a few microamps. USB VBUS (after protection) to module pad 66. Battery state through the fuel gauge on I2C or a divider on AIN3; the nRF VDDH battery driver cannot be used in LV mode. Backlight current comes from a switched rail through a transistor, not from a GPIO. |
| Keys and encoders | 4 x 5 col2row matrix with one diode per switch (16 keys, 2 encoder pushes, 2 buttons), or direct wiring if the PCB step prefers it. Encoder A/B on low-frequency pins with internal 13 kOhm pull-ups. Choose an encoder whose phase diagram shows both A and B open at every detent; otherwise each closed contact costs about 254 uA in idle and in deep sleep. Encoder and button bodies stay outside the RF bay. |
| Firmware | ZMK module repository layout as worxboard; custom LVGL screen; own Raw HID module; power hooks of 7.7; pin-map check against `board.toml`. |
| Ordering | BMD-340 is an extended part (one extended-part fee). Order the PCBA without the cell. Ask JLCPCB to confirm the module's dry-pack state and bake it per J-STD-033B if needed (2022 date code, MSL 3). Each board needs one SWD session to load the bootloader; the owner needs a CMSIS-DAP or J-Link class probe. |

## 9. Risks

1. **Radio in aluminium (high).** No measurement exists for this layout. The RF bay, the wall window, the
   transmit power option and the plastic-bottom fallback reduce it; the pre-test and the acceptance test in
   7.3.4 decide. The 5 mm bay distance is a starting value, not a datasheet number.
2. **Wider body rejected by the case subsystem (medium).** Then the antenna sits under the display edge
   (7.3.4 item 1) and the pre-test must pass before the CNC order.
3. **Connected-standby current (medium).** It depends on the two power hooks, which do not exist yet, and on the
   encoder detent type. Without them the panel stays in sleep-out while a host is connected.
4. **Old stock and moisture (low to medium).** The catalogue photo shows a 2022 date code on an MSL 3 part. Baking
   is routine but must be confirmed. The silicon-revision risk of BMD-340-A-R-00 does not apply to -10, and LV
   mode avoids REG0 in any case.
5. **RAM growth (low to medium).** The probe has no worxpad UI, image cache or Raw HID module. 70 to 137 KB stay
   free depending on buffer choice; a full-frame buffer is not needed.
6. **Display clock above the ST7789V spec (medium).** Panels differ. 8 MHz is the in-spec fallback at about
   9 full frames per second.
7. **Stock (medium).** 349 units today at JLCPCB plus 190 at LCSC; a sell-out before ordering forces global
   sourcing, consignment or a respin to the E73-2G4M08S1C (61 units, different footprint). Types -00 and -01 are
   obsolete; -10 is in mass production and a distributor index lists the part as active (search summary, likely).
8. **LGA yield (medium).** A bad joint under the module cannot be fixed by hand. Order spare assembled boards.
9. **Raw HID (medium).** The own module is not written or built yet; the reference module tracks ZMK v0.3, not the
   pinned main. Raw HID over BLE as a second HID service is not verified on macOS or Windows; the fallback is a
   custom GATT service. Upload speed is estimated, not measured. ZMK Studio over BLE works only in the Linux web
   app and native apps.
10. **Footprint errors (medium).** The footprint is hand-made; JLCPCB names the package "LGA-60" while the
    datasheet shows 68 pads.
11. **ZMK main is not a tagged release (low).** The pin is the same commit worxboard builds today.

## 10. Rejected options and why

| Option | Reason |
| --- | --- |
| Holyiot HOLYIOT-21069 nRF5340 (GLYF module) | JLCPCB does not sell it (only customer records C9900280684, C9900154256); needs consignment or hot air; ZMK supports the nRF5340 with one DK board, a separately built network-core image and MCUboot instead of UF2; +3 dBm maximum; the RAM reason is removed by build A. |
| Other nRF5340 modules | NORA-B106 (C5438434) 0, MDBT53-1M (C5355663) 0, MDBT53-P1M (C5796572) 0, E83-2G4M03S 1, NORA-B100 (C3030983) 7 with U.FL only. |
| nRF52833 modules or chip | 128 KB RAM is below the 125 KB measured for the framework alone. |
| nRF54L15 (E73-2G4M08S1F, C54337734, 106 in stock) | No USB device peripheral; no ZMK board. |
| nRF54LM20A | USB and 512 KB RAM, but every JLCPCB record is at 0 and ZMK has no upstream board. |
| Ebyte E73-2G4M08S1C (second choice) | 61 in stock, 3.0 mm tall, 29 usable GPIO with the crystal (the full pin list does not fit without sharing the flash on the display bus), no approvals stated, and its manual says the antenna must never be inside a metal case. Kept as the respin fallback. |
| Ebyte E73-2G4M08S1CX | IPEX antenna needs a cable and an antenna fitted by hand and still needs a window. |
| Raytac MDBT50Q-1MV2 / P1MV2 | 0 in stock at JLCPCB. KiCad 10 has its symbol, footprint and 3D model, so it is the best second source if stock returns. |
| Minew MS88SF2 / MS88SF3, Fanstel BT840 family | 0 in stock. |
| Holyiot 18010 | Customer record only, not sold. |
| u-blox NINA-B306 | 31 in stock at twice the price, no advantage. |
| Seeed XIAO nRF52840 as an SMD part | 11 edge GPIO; 0 in stock at JLCPCB today. |
| Bare nRF52840 aQFN-73 | Own RF layout, matching network, crystals, antenna tuning and certification; 0.5 mm aQFN escape. Not worth it for 5 units. |
| ESP32-S3 (MINI-1, WROOM-1) | Stocked and cheap with USB OTG and much RAM, but Espressif's own BLE light-sleep figure is 230 uA against 23 uA per idle ZMK connection on the nRF52840; no ZMK target; larger modules. |
| ESP32-C6 | USB Serial/JTAG controller is fixed-function and cannot be a HID device (Espressif ESP-IDF documentation, search summary, likely). |
| RP2350 plus a radio | Two chips and two firmware images; no BLE in ZMK for this path. |
| WCH CH582 / CH592 | About 32 KB RAM (WeAct board repository, search summary, likely), no ZMK or RMK support. |
| RMK as the first stack | Viable on this hardware, but colour UI needs a custom renderer without LVGL and the widget channel would be new protocol work; the family's wireless boards use ZMK. Kept as an alternative. |
| Custom embassy or Zephyr application | Multi-host BLE HID bonding and reconnection, the top complaint in prior art, would have to be rebuilt. |
| KMK | CircuitPython runtime; standby and multi-host behaviour do not meet R1 and R3 (judgement). |
| ZMK Studio protocol fork for widgets | Needs forks of `zmk-studio-messages` and the Studio client. |
| Copying `zmk-raw-hid` code | No licence file in the repository snapshot; the pattern is reused, not the code. |
| MCUboot plus MCUmgr updates (GLYF) | Needs signing keys and a host tool; UF2 drag-and-drop meets R2 more simply. |
| No RF exit (GLYF) | No range data exists; module makers require metal clearance. |
| Antenna along the right edge at the GLYF width, module centre 25 to 32 mm from the rear (revision 1) | The strip lies under the encoder edge or the LCD and inside the flank scoop; no 20.2 mm free span exists (7.3.2). Kept only as the tested fallback of 7.3.4 item 1, moved to 53 mm. |
| Antenna along the rear, left or front edge | The switch plate lies 2.6 to 3.8 mm above the PCB bottom face under the key field; the rear of the control column holds both encoders and the USB-C receptacle. |

## 11. Sources

Primary documents (read for this record):

- u-blox BMD-340 data sheet UBX-19033353 R13: `_cache/follow-radio-module-choice/datasheets-04/bmd-340.pdf`
  and `_cache/mcu-radio-sceptic/ds-03/bmd340.pdf` (text `bmd340.txt`: product table p.2, table 9 lines 712-727,
  table 10 lines 809-810, section 6 lines 1110-1124, MSL lines 1494-1505; renders `p-23.png`, `p-26.png`).
  LCSC copy: https://datasheet.lcsc.com/datasheet/pdf/aa3b9fb89c9758337cc45b4faf24ab9d.pdf?productCode=C5456944
- LCSC catalogue photo of C5456944:
  https://assets.lcsc.com/images/lcsc/900x900/20251204_U-BLOX-BMD-340-A-R_C5456944_front.jpg
  (`_cache/mcu-radio-sceptic/img-06/front.jpg`)
- Ebyte E73-2G4M08S1C and S1CX manuals: `_cache/follow-radio-module-choice/datasheets-04/e73c.pdf`, `e73cx.pdf`
  (https://datasheet.lcsc.com/datasheet/pdf/b8aaa43fc58f1d9f85ede318a8f9cb6b.pdf?productCode=C356849,
  https://datasheet.lcsc.com/datasheet/pdf/e00fad48164a836ee9b0b584b43d7300.pdf?productCode=C2764963).
- Winbond W25Q128JV Rev J: `_cache/mcu-radio-sceptic/ds-03/w25q128jv.pdf` (DC table lines 3080-3101, AC table
  lines 3215-3217); Rev I: `_cache/follow-battery-cell-and-runtime/ds-07/w25q128jv.pdf` (package 10.1, QE 7.1.4).
- Sitronix ST7789V: `_cache/follow-battery-cell-and-runtime/ds-07/st7789v.pdf` (text `st.txt`: table 3 lines
  2135-2152, serial timing line 2237, sleep-in lines 5943-5945).
- Nordic nRF52840 product specification, SPIM chapter: https://docs.nordicsemi.com/bundle/ps_nrf52840/page/spim.html
- Epson Q13FC1350000400 parameters: LCSC record C32346 (`_cache/mcu-radio/lcsc-05/C32346.json`).
- JLCPCB edge rails: https://jlcpcb.com/help/article/how-to-add-edge-rails-fiducials-for-pcb-assembly-order
  (read 2026-11-13).

Upstream firmware sources (read 2026-11-13):

- ZMK at `4dd95d7840eb3d5a3f59bb29fbf1ab054715ef85` in the worxboard workspace
  (`/home/worxbend/Projects/worxboard/build/fw-ws/zmk`): `app/src/display/main.c`, `app/src/activity.c`,
  `app/src/pm.c`, `app/module/drivers/sensor/ec11/ec11.c`, `docs/docs/config/displays.md`; and from
  https://github.com/zmkfirmware/zmk at `main`: `app/src/studio/Kconfig`, `app/include/zmk/studio/rpc.h`,
  `app/src/ble.c`, `docs/docs/config/bluetooth.md`, `docs/docs/config/system.md`, `docs/docs/config/power.md`,
  `docs/docs/config/studio.md`, `docs/docs/features/studio.md`, `docs/docs/features/bluetooth.md`,
  `docs/docs/features/low-power-states.md`, commits feed https://github.com/zmkfirmware/zmk/commits/main.atom
  (`_cache/mcu-radio/zmk-03/`).
- Zephyr 4.1 in the same workspace: `drivers/display/display_st7789v.c`, `drivers/flash/nrf_qspi_nor.c`,
  `subsys/usb/device/class/hid/Kconfig` and `core.c`.
- https://github.com/zmkfirmware/zmk-studio-messages `proto/zmk/studio.proto`
- https://github.com/zzeneg/zmk-raw-hid README, `src/usb_hid.c`, `src/hog.c`, `Kconfig`, commit
  https://github.com/zzeneg/zmk-raw-hid/commit/e25e325adc90fccb60cc08393b8c2b0ba6d647c7
  (`_cache/mcu-radio/gh-02/`, `_cache/mcu-radio-sceptic/src-05/`, `_cache/mcu-radio-sceptic/gh-04/`)
- https://github.com/rmk-rs/rmk README, `docs/docs/main/docs/features/display.md`, releases feed
- https://github.com/adafruit/Adafruit_nRF52_Bootloader README, releases feed and release pages 0.10.0, 0.11.0
  (`_cache/mcu-radio-sceptic/gh-04/`)
- https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/nimble/power_save/README.md

Measurements and catalogue reads made for this record:

- Offline ZMK probe builds A, B, C: `_cache/mcu-radio/probe-06/` (shield sources, logs, `.config`, RAM symbol list).
- JLCPCB parts API v2 responses: `_cache/mcu-radio/jlc-01/` (40 keyword queries); review re-reads in
  `_cache/mcu-radio-sceptic/jlc-01/`, `jlc-02/`.
- LCSC product API: `_cache/mcu-radio/lcsc-05/` (C5456944, C356849, C2764963, C97521, C32346, C6127317, C2913206);
  review re-reads in `_cache/mcu-radio-sceptic/lcsc-02/`.
- KiCad 10.0.7 library listings from `kicad/kicad:10.0.7` and `kicad/kicad:10.0.7-full` (run locally, no download).

Search summaries (lower weight, confidence likely at best):

- ESP32-C6 USB Serial/JTAG: https://docs.espressif.com/projects/esp-idf/en/v5.1/esp32c6/api-guides/usb-serial-jtag-console.html
- CH582 / CH592 RAM: https://github.com/WeActStudio/WeActStudio.WCH-BLE-Core
- BMD-340 lifecycle: https://www.findchips.com/detail/bmd-340-a-r/u--blox-AG
- JLCPCB assembly terms (2.5 mm body to edge):
  https://jlcpcb.com/help/article/Terms-and-Conditions-of-JLCPCB-Assembly-Service; V-cut copper distance:
  https://jlcpcb.com/blog/technical-guidance-v-cut-panelization-standards
- JLCPCB MSL handling: https://jlcpcb.com/help/article/moisture-sensitivity-level-msl-for-electronic-parts

Earlier research notes used: `research/raw/follow-radio-module-choice.md`, `follow-rf-exit-in-aluminium.md`,
`follow-battery-cell-and-runtime.md`, `regulatory-software.md`, `prior-art.md`, `conventions.md`, `geometry.md`,
`follow-display-module-sourcing.md`; `research/components/keys.md` section 6.3.

## 12. Not checked or not found

- Range or RSSI of the BMD-340 inside any aluminium body, with or without the RF bay: not measured.
- The 5 mm bay distance: a starting value; no u-blox or Nordic number was found.
- The type number and date code of the reel JLCPCB holds: not seen; the catalogue photo shows -10, 22/29.
- ST7789V current with DISPOFF in sleep-out: not given in the datasheet.
- Connected idle current with the power hooks: not measured; the hooks are not written.
- Raw HID: the own module is not written; upload speed not measured; BLE access from macOS and Windows host
  applications not verified; `CONFIG_ENABLE_HID_INT_OUT_EP` side effects on ZMK's keyboard interface not tested.
- RAM of the final worxpad UI: not measured; the probe has no custom screen.
- Adafruit bootloader 0.11.0 changes #384 and #390 with ZMK: not tested.
- Encoder part and its detent rest state: not chosen yet (keys or encoder subsystem).
- Exact LCD outline, frame material and lens recess of the chosen panel: not fixed; 7.3 uses the GLYF values.
- The BMD-341 variant (C5360631, 0 in stock): antenna type and footprint compatibility not read.
- W25Q128JVPIQ (WSON) height: not read.
- Approvals of the Ebyte E73 modules: not checked.
- ESP32-S3 current with a live HID connection: no primary measurement found.

## 13. Review response (revision 2)

| # | Review point | Verdict | Action |
| --- | --- | --- | --- |
| 1 | Antenna position contradicts the 5 mm rule; no free strip along the right edge of the GLYF layout. | Accepted. Re-measured in 7.3.2 with the decided key stack: the largest free span is 9.9 mm against 20.2 mm needed. One nuance: the LCD back lies about 4.85 mm above the PCB bottom face, so the display alone is at the 5 mm line in three dimensions; the encoder (1.6 mm above) and the flank scoop floor (2.4 to 2.7 mm below) fail clearly. | RF bay defined (7.3.1); body 8.0 mm wider and module centre 53 mm from the rear (7.3.3); old placement withdrawn and kept as a tested fallback at 53 mm. |
| 2 | Idle figure of about 39 uA needs SLPIN and flash DPD, which stock ZMK does not do. | Accepted for the mechanism (source lines in 4.2). Partly wrong on the effect: the flash share of the gap is 9 uA typ (10 against 1 uA), not milliamperes; the milliampere part comes from the panel, whose display-off current the datasheet does not give. Stock ZMK does suspend both before deep sleep, so R3 still holds with stock ZMK when the link may drop after 15 minutes; connected standby fails without hooks. | Power table split into stock and hooked (7.6); hooks listed (7.7); ST7789V sleep-in corrected to 20 uA typ including IDDI. |
| 3 | Type number known; -00 and -01 obsolete; old stock in MSL 3. | Accepted. The photo is a catalogue image, so the stock type is likely, not confirmed. Data sheet table 9 confirms rev 2 or newer silicon for -01 and later. | 7.1 type and moisture rows; risk 4; ordering note. |
| 4 | Bootloader 0.11.0 date wrong. | Accepted: 2026-05-21; 0.10.0 is 2026-02-03. | 1, 4.2, 7.7 corrected; 0.10.0 named as fallback. |
| 5 | Raw HID path untested with the pinned ZMK; SET_REPORT only; second HID service on BLE. | Accepted. Also found: no licence file in the module snapshot. | Own module (5.4, 7.7); icon sets over USB; risk 9. |
| 6 | Subsystem peak leaves out the flash. | Accepted. | Peak 44 mA typ, 51 mA max (7.6); regulator note (8). |
| 7 | Module flush with the edge needs edge rails. | Accepted. The revision 1 allowance of a 0.3 mm overhang is withdrawn. | A1 and PCB row in 8. |
| 8 | Encoder pull-ups cost 254 uA per closed contact. | Accepted; the EC11 driver has no PM action, so the cost also applies in deep sleep. | 7.6 note; encoder rule in 8. |
| 9 | Module in the thinnest part of the body (flank scoop). | Accepted. | Module moved behind the scoop (Y 53); floor rule A8. |
