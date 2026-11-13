# GLYF research notes: regulatory filings, company records, software and firmware

Date: 2026-11-13
Agent key: `regulatory-software`
Cache root: `research/_cache/regulatory-software/` (gitignored, static inspection only, nothing was executed)

Confidence scale used below: **confirmed** (stated by the maker, or read directly from a primary source such as a
maker-published firmware binary or repository), **likely** (consistent indirect evidence), **guess**.

## 0. Headline

No radio approval, trademark or company-registry record for the GLYF could be found. No public companion-software
download exists yet. The decisive technical evidence came from a different place: the public GitHub account of the
maker's CTO (`noahbei`, profile bio "CTO @ Prota Designs") holds a repository `glyf-releases` with five signed beta
firmware images. Static inspection of those images, plus the maker's six development-update articles, identifies the
SoC, display controller and resolution, external flash, fuel gauge, real-time clock, key-matrix shape, firmware stack,
host protocol and firmware-update method.

## 1. Maker-stated specifications (product page and development updates)

| Fact | Source | Confidence |
| --- | --- | --- |
| Price USD 159 pre-order, regular USD 189. Three variants: Tactile, Clicky, Linear. | https://protadesigns.com/products/glyf.js | confirmed |
| Shopify shipping weight is 442 g for every variant. This is a shipping weight, so it may include packaging. | https://protadesigns.com/products/glyf.js (`weight: 442`) | confirmed (value), likely (meaning) |
| Chassis: "CNC Aluminum, Anodized Black". | https://protadesigns.com/products/glyf (Tech Specs) | confirmed |
| Switches: "Kailh Low Profile V2's (hot-swappable)". | same | confirmed |
| Keycaps and knobs: injection-moulded PBT. | same | confirmed |
| Screen: "240 x 240 px Full Color LCD". Cover: "Tempered Glass with Black Screen Print". | same | confirmed |
| Bluetooth: "Bluetooth 5.2 at 2.4 GHz", up to 4 devices. | same | confirmed |
| Battery: "1,200 mAh Li-Ion Battery". | same | confirmed |
| In the box: GLYF, USB-C to USB-C cable, Quick Start Guide. | same | confirmed |
| 16 layers of 16 keys ("256 customizable macros"). | same | confirmed |
| Widgets: icons (keymap), time with custom wallpaper, media. The page marks time and media as "TBD". | same | confirmed |
| Operating systems: Windows, Linux, Android, macOS, iOS. The companion app is not available on iOS or Android. | same (FAQ) | confirmed |
| VIA and QMK are not supported; the maker wrote its own software. Configuration is stored on the device. | same (FAQ) | confirmed |
| Users can upload their own image for every macro icon. | same (FAQ) | confirmed |
| Status on 2026-10-09: beta testing finished, production being prepared, "still on track to ship in Q4". The store still shows "Pre-order Now, Shipping Early Q4 2026". No evidence of retail units in customer hands. | https://protadesigns.com/blogs/updates/update-06-glyf-development-gearing-up-for-production | confirmed |
| The tech-spec block has not changed between the 2025-11-16 archive snapshot and today. No dimensions other than "19 mm thin" and no weight are published. | https://web.archive.org/web/20251116160353/https://protadesigns.com/products/glyf | confirmed |

Development history, from the maker's update articles (https://protadesigns.com/blogs/updates.atom):

| Fact | Source | Confidence |
| --- | --- | --- |
| Prototype 1 (2024) reused the Printed Pad hardware (STM32F072, QMK, VIA) and added two knobs, an LCD, and "two buttons to control the screen". The two round buttons are therefore screen/navigation buttons. | Update 01 | confirmed |
| Prototype 1 could not run LVGL (not enough flash and RAM), so it used QMK Quantum Painter. | Update 01, Update 02 | confirmed |
| The firmware moved from QMK to ZMK (Zephyr) for Bluetooth. | Update 01 | confirmed |
| Prototype 2 added "memory, a battery management system, an on and off switch, a GPIO expander, and pull up resistors", and a real-time clock was a design consideration. The battery management handles USB-C charging, battery temperature and system power. | Update 01 | confirmed |
| The Nordic microcontroller has no factory bootloader; the maker flashed one with a Blue Pill running Black Magic Probe firmware. | Update 01 | confirmed |
| The first LCD was 120 x 120 (the article's wording; the firmware of that prototype uses 128 x 128, ST7735). It was replaced by a 240 x 240 LCD made by a display manufacturer, with tempered cover glass. | Update 03, Update 05 | confirmed |
| The prototype used "Alps Alpine rotary encoders". | Update 03 | confirmed |
| Switches changed from MX to Kailh low-profile (the article says they are all-POM, with clicky, tactile and linear options). A custom low-profile keycap was designed and resin-printed for testing. | Update 03 | confirmed |
| The case was first designed in Fusion 360 and then redesigned in SolidWorks for machining. | Update 03 | confirmed |
| Final hardware: "We've moved away from using a generic MCU board and instead adopted an nRF53 series module". Case is CNC aluminium. Screens have a tempered-glass layer. | Update 05 (2026-03-09) | confirmed |
| Firmware has a "UI router", normal widgets (keymap, time, media) and system widgets (layer menu, widget menu, Bluetooth, settings). A file system on external flash stores images and fonts. | Update 04 (2025-11-01) | confirmed |
| Firmware features complete by March 2026: user-uploaded icons, recorded macros stored on the device, configurable encoder rotation, firmware upgrade from the companion software. | Update 05 | confirmed |
| Beta-test sign-up was a Google Form (https://forms.gle/UCMDKHLhcwEUwXY6A). | Update 05 | confirmed |

## 2. Firmware evidence (beta images published by the CTO)

Repository: https://github.com/noahbei/glyf-releases ("Firmware releases for the Glyf keyboard").
Releases: v0.1.0 (2026-03-29), v0.1.1 and v0.1.2 (2026-04-07), v0.1.3 (2026-05-13), v0.1.4 (2026-06-18). Each has one
asset, `zmk.signed.bin`. Download counts were between 1 and 4, which fits a small beta group.
Local copies: `research/_cache/regulatory-software/firmware-06/` (SHA-256 of v0.1.4:
`328a36852e5f6b3268ae08b6f15d1fb92b01bead90c0d8fd05bc28b058611ae4`).

Method: MCUboot header parsing, `strings`, and decoding of Zephyr device-configuration tables with small Python
scripts run with `-I`. Nothing was executed. v0.1.0 was built with logging enabled and is the richest in strings.

| Fact | Evidence | Confidence |
| --- | --- | --- |
| The firmware is ZMK on Zephyr with LVGL 9. | Strings `zmk_*` events, `WEST_TOPDIR/app/src/...`, `*** Booting Zephyr OS build 58a5874a446a ***`, LVGL 9 API names (`lv_display_*`, `lv_bin_decoder.c`). | confirmed |
| The SoC is a Nordic nRF5340 (dual core, Bluetooth controller on the network core). | Strings `nRF5340 anomaly 159 conditions detected`, `bt_hci_nrf53_support`, `bt_hci_ipc0`, `mbox@2a000`, `flash-controller@39000`, `gpio@842500`, `gpio@842800`, OpenAMP/libmetal strings, `hfclk192m`. Initial stack pointer 0x2004a658 is above the 256 KB RAM of an nRF52840. | confirmed |
| The image is an MCUboot image: magic 0x96f3b83d, header 0x200 bytes, SHA-256 TLV, key-hash TLV and a 256-byte signature TLV (RSA-2048). The application is linked at 0x10000 (slot 0 after a 64 KB bootloader). | Header and TLV parse; pointer cross-references resolve with base 0x10000. | confirmed (format), likely (64 KB bootloader) |
| Application image size is 547 KB in v0.1.4 (656 KB in the logging build v0.1.0). | File sizes. | confirmed |
| The display controller is an ST7789V-compatible part at 240 x 240, RGB565, colour inversion on, on a 4-wire SPI MIPI-DBI bus at 20 MHz. | v0.1.0 strings `display_st7789v`, `WEST_TOPDIR/zephyr/drivers/display/display_st7789v.c`, node `glyf_display@0`, bus `mipi_dbi_glyf_display`. Decoded config: width 240, height 240, COLMOD 0x05, porch `0c 0c 00 33 33`, VCOM 0x19, GCTRL 0x35, VRH 0x12, VDV 0x20, MADCTL 0x00, SPI frequency 20,000,000 Hz, ready time 40 ms. | confirmed |
| External flash is a Winbond W25Q128 (16 MB) on the nRF5340 QSPI peripheral, with a LittleFS volume mounted at `/c`. | Node `w25q128@0`, driver `qspi_nor`, strings `littlefs`, `/c/macros/%u`, `/c/dic/01.bin`. Dev-rig overlays use JEDEC ID `ef 40 18` (W25Q128JV). | confirmed |
| The fuel gauge is a Maxim MAX17048 at I2C address 0x36. | Node `max17048@36`, driver `sensor_max17048`, strings `failed to read vcell`. | confirmed |
| The real-time clock is a DS3231 at I2C address 0x68 (present from v0.1.4, when the time widget was added). | Node `ds3231@68`, `ds3231_rtc`, event `zmk_rtc_time_changed`; release note "add git patch for rtc driver changes". | confirmed |
| Keys are scanned as a direct GPIO matrix, 5 columns by 4 rows, col2row, inputs with pull-downs. That gives 20 positions: 16 keys, 2 encoder push switches and 2 navigation buttons. The GPIO expander of prototype 2 is gone. | Driver `kscan_gpio_matrix.c`; decoded table has 5 output pins (P1.14, P1.13, P1.12, P1.11, P0.31) and 4 input pins with pull-down (P0.21, P0.19, P0.29, P0.25). The dev-rig shield `imptest` has the same 4 x 5 matrix with 20 mapped positions. No expander driver string in the image. | likely (pin decode), confirmed (matrix driver) |
| Two incremental quadrature encoders use the ZMK EC11 driver. | Driver `app/module/drivers/sensor/ec11/ec11.c`, nodes `encoder_left`, `encoder_right`. Decoded A/B pins: P0.28 and P1.10 (left), P1.07 and P1.09 (right), pull-ups enabled. Dev-rig shield: `steps = <80>`, `triggers-per-rotation = <20>`. | confirmed (driver), likely (pins) |
| Display pins: chip select P0.11 (active low), data/command P0.12, reset P1.02 (active low). | Decoded `mipi_dbi_spi` and SPI config tables. | likely |
| There is a GPIO LED node (probably the backlight or a status LED) and an `EXT_POWER` control (switchable peripheral power rail). | Strings `led_gpio`, `EXT_POWER`, `External Power`. No PWM driver string was found, so backlight dimming by PWM is not evidenced. | likely |
| USB identity in beta firmware: VID 0x1D50, PID 0x615E (the ZMK default pair), bcdDevice 0x0401, composite device class EF/02/01, manufacturer string "ZMK Project", product string "GLYF". The maker has not yet assigned its own IDs. | USB device descriptor found in v0.1.0 and v0.1.4. | confirmed |
| USB interfaces: HID keyboard and consumer control, plus two CDC-ACM serial ports. One carries ZMK Studio RPC and one is labelled "GLYF Firmware Update". | Strings `HID_0`, `snippet_studio_rpc_usb_uart`, `Zephyr USB CDC-ACM`, `GLYF Firmware Update`; release notes for v0.1.1 ("USB CDC-ACM labels for GLYF Console and Studio RPC") and v0.1.4 ("update names of com ports"). | confirmed |
| Host protocol: ZMK Studio RPC (protobuf messages framed over a serial byte stream) extended with maker-specific subsystems `display` (widgets, key icons, asset list/upload/download/delete with CRC32 and chunking) and `macros` (slot upload/download). The ZMK Studio Bluetooth GATT service UUID is also in the image. | Strings `app/src/studio/rpc.c`, `RPC display.set_keymap_icon`, `RPC display.asset_upload_start`, `RPC macros.upload_start`, `zmk_studio_rpc_notification`; UUID `00000000-0196-6107-c967-c5cfb1c2482a` present. | confirmed |
| Firmware update: MCUmgr SMP over the serial (CDC-ACM) transport into the MCUboot secondary slot. No SMP Bluetooth service is present, and the build does not produce UF2. | Strings `mcumgr smp`, `mcumgr_img_grp`, `mcumgr_os_grp`, `mgmt/mcumgr/transport/src/serial_util.c`; SMP BLE UUID absent. | confirmed |
| Bluetooth: HID over GATT, Battery Service, Device Information Service, multiple profiles with a Bluetooth menu screen (select, clear, clear all), and a USB/BLE output toggle. | Strings `HID Over GATT Send Work`, `BAS Notifications`, `bt_dis`, `ble/profiles/%d`, `Status: Pairing - Profile %d`, `Output Toggle`. | confirmed |
| Stored data: runtime macros in `/c/macros/<slot>`, default icons in `/c/dic/*.bin` (LVGL binary image format), per-layer icon blobs, a time-widget background image, widget order in settings. | Strings and v0.1.4 release notes. | confirmed |
| Custom behaviours: widget next/previous/select, layer next/previous/select, layer menu, widget menu, Bluetooth menu, runtime macro, encoder variants for layer, widget and Bluetooth menus, hold-tap on the navigation buttons. | Behaviour name strings; release note "increase time required to hold nav buttons". | confirmed |
| Display blanking (sleep) is enabled in production builds and can be changed at run time. | Release notes v0.1.3 and v0.1.4; strings `display_blank/state`. | confirmed |
| Icon pixel size: not found. No embedded LVGL image descriptors remain in the images; icons are loaded from the file system. | Header scan of the three images. | not found |
| Network-core (Bluetooth controller) image: not published. Only the application-core image is in the releases. | Release assets. | confirmed |

## 3. Other repositories from the same account (development rigs, not the product)

Account: https://github.com/noahbei (42 public repositories). Clones: `research/_cache/regulatory-software/github-repos-05/`.

| Fact | Source | Confidence |
| --- | --- | --- |
| `zmk-config-test` (2025): ZMK shield `imptest` for a nice!nano v2 with a 4-row by 5-column matrix, 20 key positions (4 x 4 grid plus two at the top right and two at the bottom right), two `alps,ec11` encoders, ZMK Studio enabled, `CONFIG_ZMK_BEHAVIORS_QUEUE_SIZE=512` for long macros, 3-minute idle timeout. Commit "remove raw hid" then "add zmk studio" shows the move from Raw HID to Studio RPC. | https://github.com/noahbei/zmk-config-test | confirmed |
| Same repository, shield `ext_flash`: W25Q128JV on SPI with JEDEC ID `ef 40 18`, 16 MB. | same | confirmed |
| `littlefs` (2025-06): LittleFS test on nice!nano v2 and nRF52840 DK with W25Q128 (128 KB settings partition plus 6 MB LittleFS partition, deep power-down enabled). | https://github.com/noahbei/littlefs | confirmed |
| `zmk-config-iptest` (2024): custom board `improvedpad` on nRF52833 with a Microchip MCP23S17-class SPI GPIO expander (`microchip,mcp23sxx`) driving a 4 x 4 matrix, battery voltage divider on ADC, external power switch. This is prototype 2. | https://github.com/noahbei/zmk-config-iptest | confirmed |
| `840dk-shield`, `zephyr_st7735s_display_example`, `lvgl_hello_world` (2024): nRF52840 DK tests with a 128 x 128 ST7735 display and LVGL. | https://github.com/noahbei | confirmed |
| `qmk_firmware` fork, branch `improved_pad`: prototype 1. STM32F072, VID 0x5064, PID 0x0002, 4 rows by 6 columns, two encoders (resolution 4), 128 x 128 LCD on SPI via Quantum Painter, 64 dynamic macros. | https://github.com/noahbei/qmk_firmware/tree/improved_pad/keyboards/improvedpad | confirmed |
| `magnetic-encoder-test` (2024-07): AS5600 magnetic angle sensor experiment. Nothing in the 2026 firmware indicates that it shipped. | https://github.com/noahbei/magnetic-encoder-test | confirmed (experiment), likely (not shipped) |
| `Adafruit_nRF52_Bootloader` fork (2025-05) with no extra branches: the UF2 bootloader was used on nRF52 prototypes. The nRF5340 product uses MCUboot. | https://github.com/noahbei/Adafruit_nRF52_Bootloader | likely |
| `Glyf_App` (created 2024-11-18) is an empty public repository. The companion-app source is not public. | https://github.com/noahbei/Glyf_App | confirmed |
| Starred repositories include `boogie/mcumgr-web`, `zmkfirmware/zmk-studio-messages`, `zzeneg/zmk-raw-hid`, `carrefinho/prospector` and `W-Mai/icu` (an LVGL image converter). This fits a browser or desktop tool that uses MCUmgr for updates and LVGL binary images for icons. | https://api.github.com/users/noahbei/starred | likely |
| The earlier product, Printed Pad, is in upstream QMK: STM32F072RBT6, stm32-dfu bootloader, VID 0x5064, PID 0x0001, 4 x 3 matrix, I2C OLED. The VIA preset files on the site carry `vendorProductId` 1348730881 (0x50640001). | https://github.com/qmk/qmk_firmware/tree/master/keyboards/printedpad , https://protadesigns.com/pages/presets | confirmed |

## 4. Photos in the update articles

| Fact | Source | Confidence |
| --- | --- | --- |
| Prototype 2 PCB (KiCad screenshots): bare Nordic QFN with a chip antenna, SSOP expander, SOIC-8 flash, MX hot-swap footprints, slide power switch, JST battery connector, two encoders with push switch and two tactile buttons below the display cut-out. | `blog-images-10/asdfjkasdfjkljasdfk.png`, `geradfasdfasdf.png` (from Update 01) | confirmed (photo of an old prototype) |
| Flex-cable markings on sample LCDs: `ENH-TV0144006A` (the first, 1.44-inch class, 8-pin panel) and `FPC-TFT014H030-A0` (a later square panel). Whether the second marking belongs to the final panel is not stated. | `blog-images-10/Mini_Update_10.jpg`, `P2P_4_LCD0.jpg` (from Update 03) | likely (reading of the markings), guess (final panel) |
| In the launch render, the lit area is square and sits inside a taller black glass. The "portrait display" is a square 240 x 240 panel behind a larger printed cover glass. | `blog-images-10/u05_blog_post_image.jpg`, firmware resolution | likely |

## 5. Radio approvals

| Check | Result | Confidence |
| --- | --- | --- |
| FCC ID, by grantee or applicant name "Prota", "Prota Designs", "GLYF" on fccid.io | No grantee and no filing for Prota Designs or the GLYF. Hits are unrelated companies (SystemBase, Naran, Protac, Protap). | confirmed for this mirror on 2026-11-13 |
| FCC official search (apps.fcc.gov) and fcc.report | Blocked with HTTP 403. | not reached |
| Bluetooth SIG qualification listings ("Prota", "GLYF", "Glyf") | 27 hits for "Prota", none from Prota Designs. Zero hits for GLYF. | confirmed |
| Japan MIC technical-conformity database (name "Prota", "Prota Designs"; type "GLYF") | Zero records. | confirmed |
| ISED Canada, EU declaration of conformity, UKCA | Not found. The ISED search needs a session and was not queried. No declaration is published on the maker's site. | not found |
| Interpretation | The maker says it uses a pre-certified "nRF53 series module" and had not shipped by 2026-10-09. A device that reuses a certified module can ship in the US under the module's FCC ID with supplier's declaration for the unintentional radiator part, so the absence of an own FCC ID is expected. The module vendor and part number are not identified. | likely |

## 6. Trademarks and company

| Fact | Source | Confidence |
| --- | --- | --- |
| USPTO has no application or registration for "PROTA DESIGNS". | https://tmsearch.uspto.gov (search backend queried 2026-11-13) | confirmed |
| USPTO has three live records matching GLYF, none from the maker. GLYF, serial 98193466, class 9, belongs to Radians, Inc. for protective eyewear (registered 2025-06-03). GLYF, serial 90097495, class 5, belongs to Zestrade LLC. | same | confirmed |
| TMview (EUIPO and partner offices) has no "PROTA DESIGNS" mark. GLYF marks there belong to unrelated owners (cosmetics, food, an expired UK software mark of Glyfco Limited). | https://www.tmdn.org/tmview/ | confirmed |
| The site names the seller only as "Prota Designs" or "PROTA DESIGNS", described as "a California based tech company". No legal suffix, registration number or postal address is published. Contact: business@protadesigns.com. Founders are named on the About page as Ben (CEO) and Noah (CTO). | https://protadesigns.com/pages/about-us , terms and privacy pages | confirmed |
| California Secretary of State business search and OpenCorporates | Both blocked automated access. | not reached |
| The working name "worxpad" does not collide with anything found here. "GLYF" should not be used as a product name: it is the maker's product name and a registered class 9 mark of another company. | this section | likely |

## 7. Companion software

| Fact | Source | Confidence |
| --- | --- | --- |
| No public download exists. The site has no download page, and certificate transparency shows only `protadesigns.com` and `www`. | https://crt.sh/?q=%25.protadesigns.com , site crawl | confirmed |
| No package named for the product or maker was found on npm, PyPI, Flathub, AUR, Snap, Homebrew, the Apple App Store search, or GitLab. Same-named packages (`glyf` on npm and PyPI, glyf.app) are unrelated. | registry queries on 2026-11-13 | confirmed |
| The companion app targets desktop only (no iOS or Android). It configures keys, encoders, icons, widgets and macros, and performs firmware upgrades. | product FAQ, Update 04, Update 05 | confirmed |
| On the wire, the app speaks ZMK Studio RPC with extra `display` and `macros` subsystems over a CDC-ACM serial port, and MCUmgr SMP over a second CDC-ACM port for updates. | section 2 | confirmed |
| The media widget and some other widgets need the desktop app to push data to the device. | product FAQ | confirmed |
| Installer contents, HID usage pages beyond standard keyboard and consumer, and feature flags for unreleased hardware | No installer is available to inspect. | not found |

## 8. Support material

| Fact | Source | Confidence |
| --- | --- | --- |
| No GLYF manual, quick-start PDF or help-centre article is published. The only guide on the site is for the Printed Pad (VIA). | https://protadesigns.com/pages/instructions | confirmed |
| Support runs through a Discord server (help-ticket channel) and e-mail. | https://protadesigns.com/pages/refund-policy | confirmed |
| Not published anywhere found: charge time, battery life, exact dimensions, device weight without packaging, keycap profile name, encoder part number, charger IC, module part number. | all sources above | not found |

## 9. Implications for the worxpad design

These follow from the evidence above and are offered as input for the component-selection step.

1. The reference architecture is: nRF5340 module, ST7789V 240 x 240 SPI LCD, 16 MB QSPI NOR flash with LittleFS,
   MAX17048 fuel gauge, DS3231 RTC, 4 x 5 diode matrix on direct GPIO, two EC11-type encoders, MCUboot plus MCUmgr
   over USB serial, ZMK with ZMK Studio RPC, LVGL 9.
2. An nRF52840 would not have been enough for the maker: the application image is about 550 KB and uses more than
   256 KB of RAM address space. A 1 MB flash, 512 KB RAM application core is the proven sizing for ZMK plus LVGL 9
   plus a widget system.
3. The display is square. A portrait-looking front can be achieved with a taller printed cover glass.
4. The two round buttons are navigation buttons in the key matrix, not dials.
5. Vendor firmware, icons and protocol definitions were inspected for facts only. None of it is in the repository.

## 10. Sources read

- https://protadesigns.com/ , `/products/glyf` , `/products/glyf.js` , `/products.json` , `/pages.json` , `/pages/about-us` , `/pages/presets` , `/pages/instructions` , `/pages/refund-policy` , `/pages/terms-and-conditions` , `/pages/terms-of-services` , `/policies/privacy-policy` , `/sitemap.xml`
- https://protadesigns.com/blogs/updates.atom (Updates 01 to 06) and the images embedded in Updates 01, 03 and 05
- https://github.com/noahbei and its repositories `glyf-releases` (five release binaries), `zmk-config-test`, `zmk-config-iptest`, `840dk-shield`, `littlefs`, `lvgl_hello_world`, `zephyr_st7735s_display_example`, `magnetic-encoder-test`, `Glyf_App`, `qmk_firmware` (branch `improved_pad`), `keyboards`, `Adafruit_nRF52_Bootloader`
- https://github.com/qmk/qmk_firmware/tree/master/keyboards/printedpad
- https://fccid.io/search.php (queries Prota, Prota Designs, GLYF) and https://fccid.io/company.php
- https://qualificationapi.bluetooth.com/api/Platform/Listings/Search (Bluetooth SIG listing search)
- https://www.tele.soumu.go.jp/giteki/list (Japan MIC)
- https://tmsearch.uspto.gov (USPTO trademark search backend), https://www.tmdn.org/tmview/ (TMview)
- https://crt.sh/?q=%25.protadesigns.com , DNS lookups of likely subdomains
- https://web.archive.org CDX index and snapshots of `/products/glyf` (2025-09-08, 2025-11-16, 2026-02-05, 2026-07-19) and `/products/glyf-alpha-testing` (2025-05-23)
- npm, PyPI, Flathub, AUR, Snapcraft, Homebrew cask, iTunes Search API, GitLab API

## 11. Not reached

- FCC official equipment-authorization search (apps.fcc.gov): HTTP 403 for automated clients.
- fcc.report: HTTP 403.
- California Secretary of State bizfile search: blocked by its security service (HTTP 429).
- OpenCorporates: reCAPTCHA wall.
- ISED Canada radio equipment list: session-based search, not queried.
- EUIPO eSearch direct API: HTTP 500. TMview was used instead.
- The maker's Discord server (beta builds of the companion app are probably distributed there): requires an account and was not accessed.
- The companion application itself: no public installer.
- GitHub code search (needs authentication), so references to the product inside other people's repositories were not searched.
