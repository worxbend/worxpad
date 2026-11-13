# Prior art: engineering lessons from comparable devices

Date: 2026-11-13. Agent key: `prior-art`.

Scope: commercial and open-hardware devices in the same class as the target macropad (16 keys, 2 knobs, 2 buttons,
portrait colour display, USB-C plus Bluetooth, battery, slim aluminium body). This file records facts with sources.
It does not copy vendor artwork, firmware or models.

Confidence labels:

- **confirmed**: stated by the maker, or read directly from a primary source (maker page, maker firmware source, FCC filing).
- **likely**: consistent indirect evidence (retailer listing, review, search-engine summary of a page that could not be opened).
- **guess**: inference by this agent.
- **not found**: looked for and not located. No filler value is given.

Cached downloads are under `research/_cache/prior-art/` (gitignored). File names are given where a fact was read from a cached copy.

---

## 1. Closest analogues

### 1.1 Work Louder Knob1 (keyboard with IPS display, two knobs, two aluminium shells)

This is the nearest commercial match for the construction of the target: two CNC aluminium shells, an IPS display,
two rotary encoders, Bluetooth and a battery.

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Case | "CNC Aluminum bottom shell", "CNC Aluminum top shell", "CNC Aluminum dials" | https://worklouder.cc/shop/keyboards/knob1 (cache `04-pages/wl-shop-knob1.html`) | confirmed |
| Display | "310x100px IPS display" | same | confirmed |
| Encoders | "2x Rotary encoders" | same | confirmed |
| Radio | "Bluetooth" (version, chip and host count not stated) | same | confirmed |
| Battery | "3000mAh battery" (life not stated) | same | confirmed |
| Feet | "4° Magnetic rubber feet" | same | confirmed |
| Switches | Low profile, MX stem, POM / POK, 55 g linear. The maker's loose switch pack states "Gateron KS-33 2.0 footprint". | same, and https://worklouder.cc/shop/miscellaneous/wrk-lp1-switches | confirmed |
| Keycaps | MX stem, single-shot injection, ABS + PC, laser-etched icons, low profile | same | confirmed |
| Tools in box | "Opening tool", keycap puller, 2 spare switches, USB-C cable | same | confirmed |
| Software | Maker's "Input" desktop app. "Widget & SDK kit", "Open for custom widget creation". Mac, Windows, Linux. | same | confirmed |
| Price | USD 439.00 | same | confirmed |
| MCU, display driver, charger, antenna path | not found | - | - |

Notes:

- The box includes an "opening tool". That suggests the shells are not opened with ordinary exposed screws. This is a guess.
- How the radio leaves two aluminium shells is not documented by the maker. No teardown was found.

### 1.2 Work Louder Creator Micro 2 (macropad, wired "Base" and wireless "Pro")

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Inputs | 13 programmable keys, 1 clickable encoder, 1 touch sensor, 1 planar joystick | https://worklouder.cc/shop/keyboards/creator-micro-2 (cache `04-pages/wl-shop-cm2.html`) | confirmed |
| Pro model case | "CNC Aluminum bottom shell", "CNC Aluminum frame", "Injection PC body" | same | confirmed |
| Base model case | "CNC PC body + frame", USB-C only | same | confirmed |
| Radio | Pro: "Bluetooth & USB-C". Base: wired only. | same | confirmed |
| Battery | Pro: "2100mAh battery" | same | confirmed |
| Tilt | "4° Magnetic incliner (ruler)" | same | confirmed |
| Layers | "6 discreet layers, each with 13 keys, a 7 slot radial menu and a dial to map per layer" | https://worklouder.cc/creator-micro-2 | confirmed |
| Price | USD 168.00 | shop page | confirmed |
| Storage | "onboard memory for profile storage" | shop page | confirmed |

Design reading: the wireless Pro model has a polycarbonate body between an aluminium frame and an aluminium bottom.
The maker markets the polycarbonate as an RGB diffuser. It also gives the radio a non-metal path. That second purpose
is a guess. The maker does not state it.

Reported problem: a user thread on the maker's feedback board reports that the Creator Micro 2 "repeatedly fails to
reconnect over Bluetooth after sleep", with 15 to 20 minutes of re-pairing and duplicate device entries in the host.
The maker replied that firmware 0.6.2 targets the issue. Later replies report continued lag and drops on 0.6.2.
Source: https://worklouder.featurebase.app/p/creator-micro-v2-repeatedly-fails-to-reconnect-over-bluetooth-after
(read through a page summariser). Confidence: likely.

### 1.3 Work Louder Creator Micro (first generation) and Figma Creator Micro

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| MCU | ATmega32U4 | QMK `keyboards/work_louder/micro/keyboard.json` (cache `02-qmk/`) | confirmed |
| Layout | "16 key" pad with dual encoders, per-key RGB, underglow. 4 x 4 matrix. | QMK `keyboards/work_louder/micro/readme.md` | confirmed |
| Firmware | QMK, wired USB only | same | confirmed |
| Figma edition | 12 keys, 2 rotary encoders, USB-C wired, VIA remapping, launch price USD 139 pre-order | https://www.gizmochina.com/2023/12/14/figma-launches-creator-micro-macro-pad-with-12-customizable-keys-priced-at-139/ and https://www.figma.com/blog/figma-work-louder-custom-keyboard/ (search summary) | likely |

### 1.4 Keychron Q0 Max (wireless aluminium number pad with knob)

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| MCU | STM32F401 | Keychron QMK fork, branch `wireless_playground`, `keyboards/keychron/q0_max/info.json` (cache `02-qmk/`) | confirmed |
| Radio | Separate wireless module named `LKBT51` in firmware (reset and interrupt pins). 3 Bluetooth hosts (`BT_HOST_DEVICES_COUNT 3`) plus a 2.4 GHz mode. | same repo, `config.h` | confirmed |
| LED driver | SNLED27351 over SPI | same, `info.json` | confirmed |
| Encoder | One quadrature encoder on two GPIO pins. Part number not found. | same | confirmed |
| Connectivity | "2.4 GHz, Bluetooth, wired; 1000 Hz polling rate". Bluetooth 5.1. | https://www.keychron.com/products/keychron-q0-max-qmk-custom-number-pad (cache `01-vendor/keychron-q0max.json`) | confirmed |
| Bluetooth polling | 90 Hz on Bluetooth, 1000 Hz on 2.4 GHz and wired | maker listing, by search summary | likely |
| Battery | "1800 mAh, up to 50 hours" (the 50 hour figure is with RGB at lowest brightness, by search summary) | maker page | confirmed |
| Build | "Aluminum, gasket mount, Steel plate". 6063 aluminium, CNC machined. | maker page | confirmed |
| Size and weight | 118 x 137 mm footprint, 684 g assembled. Height not found. | maker page | confirmed |
| Switches | Gateron Jupiter (full-height MX), hot-swappable | maker page | confirmed |
| Price | USD 129.99 assembled, USD 119.99 barebone | maker product JSON | confirmed |
| Antenna path | not found for the Q0 Max. See 3.1 for the Q1 Pro. | - | - |

Lesson: Keychron does not run the keyboard and the radio on one chip. An STM32 runs QMK and a separate module carries
Bluetooth and 2.4 GHz. That keeps QMK but costs board area and standby current. A single nRF52840 with ZMK or RMK is
the simpler route for a small pad.

### 1.5 DOIO KB16 / Megalodon Triple Knob (16 keys, 3 knobs, OLED, aluminium, wired)

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| MCU | Rev 1: ATmega32U4. Rev 2: STM32F103 class (the QMK readme names APM32F103CBT6). | QMK `keyboards/doio/kb16/rev1/keyboard.json`, `rev2/keyboard.json` (cache `02-qmk/`); rev 2 readme by search summary | confirmed |
| Matrix | 4 rows x 5 columns. The fifth column carries the encoder push switches. This reading of the fifth column is a guess. | same | confirmed (matrix), guess (use) |
| Encoders | 3 quadrature encoders, each on two GPIO pins, all clickable | same, and seller page | confirmed |
| LEDs | 16 WS2812 on one pin | same | confirmed |
| Display | 0.91 inch OLED. 4 layers shown on screen. | https://www.keebmonkey.com/products/megalodon-triple-knob-macro-pad (cache `03-pages/doio-kb16.json`) | confirmed |
| Case | "Housing Material: Aluminum 6063", "Translucent Acrylic Base", CNC, anodised or electrophoresis coated | same | confirmed |
| Size and weight | 142 x 96 x 32 mm, 320 g | same | confirmed |
| Switches | Hot-swappable, 16 Gateron Yellow (full-height MX) included | same | confirmed |
| Firmware | QMK with VIA | same | confirmed |
| Price | USD 59.00 | same | confirmed |

Lesson: an aluminium frame over an acrylic base is the cheapest proven case stack in this class. The device is wired,
so the acrylic base is there for underglow, not for the radio.

Complaints (Drop reviews, read through a search summary; confidence likely): the firmware supported only an old VIA
version at review time, one buyer bricked the pad while configuring it, one unit lost its under-LEDs after a month,
and the pad ships with almost no default keymap. Source: https://drop.com/buy/megalodon-doio-hot-swappable-rgb-30-keyboard/reviews
and https://green-keys.info/en/doio-kb16-macro-pad-review%ef%bd%9cexplanation-of-effective-use/.

---

## 2. Commercial display consoles

### 2.1 Logitech MX Creative Console (Keypad plus Dialpad)

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Keypad size and weight | 91.7 x 77.8 x 25.5 mm, 96 g | https://support.logi.com/hc/en-au/articles/24727157859351-Specification-MX-Creative-Console | confirmed |
| Keypad display | 9 LCD keys. Panel "480 (RGB) * 480" at 200 ppi. One panel behind nine keys. | same | confirmed |
| Keypad link | "USB 2.0 High Speed", corded. No radio, no battery. | same | confirmed |
| Dialpad size and weight | 92.1 x 93.7 x 33.8 mm, 128.7 g with cells | same | confirmed |
| Dialpad link | "BLE 5.1 & Logi Bolt USB", range "Up to 10 meters" | same | confirmed |
| Dialpad power | 2 x AAA alkaline in series, user replaceable, "18 months" life | same | confirmed |
| Dialpad radio chip | Nordic nRF52820. The package marking in the FCC internal photo reads "N52820 QDAAD0". | FCC ID JNZYR0097 internal photos, page 4, https://fccid.io/JNZYR0097 (cache `06-fcc/dialpad-internal.pdf`) | confirmed |
| Dialpad antenna | A small chip antenna at the PCB edge, labelled "Antenna" in the filing. Plastic housing. | same, pages 5 and 10 | confirmed |
| Dialpad dial sensing | Magnetic Hall sensor. Main source MLX90393, second source MLX90394. | same, pages 1 and 6 (text) | confirmed |
| Dialpad rating | 3 V, 30 mA on the product label | same, page 1 | confirmed |
| Price | USD 200 at launch for the pair | https://engadget.com/computing/accessories/logitech-mx-creative-console-review-an-affordable-entry-point-into-edit-panels-070101321.html | likely |

Lessons:

- Logitech kept the display unit wired. Only the display-free dial unit is wireless. A backlit LCD and a long battery
  life did not fit in one small unit at that price.
- The dial uses a contactless magnetic sensor with two approved sources. Logitech qualifies a second source for the
  one critical sensor.
- A chip antenna at the board edge inside a plastic body passed with a 10 m claim.

Complaints (Engadget review; confidence likely): too few buttons and dials for many Adobe apps, no haptic feedback on
the dial, AAA cells are an odd choice, page switching slows the workflow, moving a setting between pages is not easy.

### 2.2 Elgato Stream Deck + and Stream Deck Neo

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Stream Deck + size and weight | 140 x 138 x 110 mm (with fixed stand), 465 g | https://www.elgato.com/us/en/p/stream-deck-plus-black | confirmed |
| Stream Deck + inputs | 8 LCD keys, 4 push encoders, touch strip 108 x 14 mm | same | confirmed |
| Stream Deck + panel | One 800 x 480 px panel. Key images 120 x 120 px. Touch strip image 800 x 100 px. | https://docs.elgato.com/streamdeck/hid/stream-deck-plus (cache `05-misc/elgato-hid-plus.html`) | confirmed |
| Stream Deck + link | USB 2.0 only. No radio, no battery. | maker page | confirmed |
| Stream Deck + price | USD 179.99 now. USD 199.99 at launch (review). | maker page; review mirror at https://blog.kowatek.com/?p=1758 | confirmed / likely |
| Key mechanism | "membrane switch with a tactile bump" | review mirror (The Verge text) | likely |
| Stream Deck Neo | 107 x 26 x 78 mm, 210 g, 8 LCD keys, 2 touch points, info bar, USB-C | https://help.elgato.com/hc/en-us/articles/25920614901261-Elgato-Stream-Deck-Neo-Technical-Specifications (search summary) | likely |
| Stream Deck Classic construction | Front cover held by clips and adhesive. One screen module on a ribbon cable. Metal housing tabs bent to open. Fragile ribbon cables. | https://www.ifixit.com/Teardown/Elgato+Stream+Deck+Classic+Teardown/194063 | confirmed |
| MCU | not found | - | - |

Lessons:

- Elgato puts one LCD panel behind all keys and the strip. It does not use one display per key.
- The display region is addressed by fixed pixel rectangles. The same idea fits the target: one portrait panel, a
  4 x 4 icon grid drawn by firmware.

Complaints (The Verge review, read from a mirror; confidence likely): dial and touch-strip functions had very few
plug-ins at launch, the touch strip only acts on the dial functions, the stand is fixed at 45 degrees and screwed on,
the plug-in marketplace is hard to search.

### 2.3 Loupedeck Live, Loupedeck CT, Razer Stream Controller

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Loupedeck Live display | 4.3 inch, 480 x 272 px LCD with capacitive touch | retailer spec tables, e.g. https://foto-erhardt.com/accessories/other-photo-accessories/more-photo-accessories/loupedeck-live_technik.html (search summary) | likely |
| Loupedeck Live inputs | 8 RGB buttons, 6 push dials | same | likely |
| Loupedeck Live size and weight | 150 x 110 x 30 mm, 230 g | https://www.pcgamer.com/loupedeck-live-review/ (search summary) | likely |
| Loupedeck CT size and weight | 160 x 150 x 30 mm, 365 g, aluminium cover and dials | retailer listings (search summary) | likely |
| Loupedeck CT Bluetooth | A Bluetooth chip is fitted. A review says it was not enabled for host connection. | https://forums.appleinsider.com/discussion/230578 (search summary) | likely |
| Razer Stream Controller | Same hardware as Loupedeck Live: not verified. The Razer page could not be parsed. | - | not found |
| MCU and teardown | not found | - | - |

Lesson: Loupedeck shipped a radio that the firmware never used. Hardware without firmware support has no value to the buyer.

### 2.4 Mountain DisplayPad

12 display keys at 104 x 104 px each, aluminium frame, stand with anti-slip base, maker software "Base Camp".
Source: https://www.guru3d.com/articles-pages/mountain-display-and-macro-pad-for-keyboard-review,1.html (search summary).
Confidence: likely. Dimensions, weight and price: not found.

### 2.5 Monogram Creative Console

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Construction | "CNC -machined aluminum, neodymium magnets and gold-plated connections" | https://monogramcc.com/ (cache `03-pages/monogram.html`) | confirmed |
| Modules | Core, Essential Keys, Dial, Slider, Orbiter. Modules snap together and can be rearranged. | https://www.provideocoalition.com/review-monogram-creative-console/ (search summary) | likely |
| Core module | 240 x 240 px IPS display, ARM Cortex-M processor, 2 buttons | same | likely |
| Link | Wired USB. No radio found. | - | likely |

### 2.6 TourBox Elite

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Size and weight | 116 x 101 x 44 mm, 376 g without cells, cells 48 g | https://www.cliftoncameras.co.uk/uploads/specifications/TourBox%20Elite.pdf (cache `04-pages/tourbox.pdf`) | likely (retailer copy of maker sheet) |
| Body | ABS shell, PC buttons, PC and TPU dials | same | likely |
| Link | "Dual-channel BLE5.0 & USB-C cable". Two paired hosts. | same | likely |
| Power | 2 x AA. Bluetooth mode 3 V DC, 50 mA rating. "Battery Life: Up to 2 months". | same | likely |
| Haptics | Linear motor | same | likely |

Complaint (buyer review, search summary; confidence likely): the use of AA cells and not a rechargeable cell.

### 2.7 Summary of the commercial display consoles

No commercial console found in this survey combines all three of: colour LCD, battery, and a full aluminium body.

- Colour LCD consoles are wired: Stream Deck +, Stream Deck Neo, Loupedeck Live, MX Creative Keypad, Mountain DisplayPad, Monogram.
- Wireless consoles have no LCD and a plastic body: MX Creative Dialpad, TourBox Elite.
- The Work Louder Knob1 is the one product found with an IPS display, Bluetooth, a battery and two aluminium shells.
  It carries a 3000 mAh cell and costs USD 439.

The target sits in the same corner as the Knob1 and the GLYF. Battery size and display power management are the main risks.

---

## 3. Wireless aluminium keyboards and how the radio gets out

### 3.1 Keychron Q1 Pro (first full-aluminium wireless Keychron)

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Radio path | "It's able to do this because of a small, camouflage, piece of plastic on the back that allows the signal to escape." | https://appleinsider.com/articles/23/01/21/keychron-q1-pro-review-finally-a-wireless-metal-mechanical-keyboard (cache `04-pages/appleinsider-q1pro.html`) | confirmed (reviewer observation of the product) |
| Radio | Broadcom Bluetooth 5.1 | same | likely |
| MCU | STM32L432, ARM Cortex-M4, 128 K flash | same | likely |
| Polling | 1000 Hz wired, 90 Hz Bluetooth | same | likely |
| Battery | 4000 mAh. "up to 300 hours" with no backlight. 90 hours at lowest backlight. | same | likely |

Lesson: the standard commercial answer is a plastic insert in the rear wall, colour-matched to the anodising, with the
antenna directly behind it. The rear wall also holds the USB-C port and the mode switch, so the insert hides among them.

### 3.2 NuPhy Air75 V2

Aluminium frame with an ABS bottom case. 4000 mAh. "220hrs RGB off, 35-57 hrs RGB on". 2.4 GHz, Bluetooth 5.1 and USB-C.
QMK/VIA. Gateron low-profile KS-33 switches. Thickness 13.5 mm by one review, 16 mm by retailer listings.
Source: https://www.creativebloq.com/reviews/nuphy-air75-v2 (search summary). Confidence: likely. MCU and radio chip: not found.

Lesson: aluminium top frame plus plastic bottom is the low-risk radio path. The antenna looks down and sideways through plastic.

### 3.3 Lofree Flow

"The all-aluminum body from top to bottom", "slim 10mm thickness and 3.9-degree tilt", 568 g, Kailh low-profile POM
switches, gasket mount. Source: https://www.lofree.co/products/lofree-flow-the-smoothest-mechanical-keyboard
(cache `04-pages/lofree-flow.json`). Confidence: confirmed (maker claims). Battery 2000 mAh and Bluetooth 5.0: retailer
spec listing by search summary, confidence likely. The 10 mm figure is the thinnest point. A review measures
24.5 mm overall height for the 84-key model (https://thephonograph.net/electronics-tech-reviews/lofree-flow-review, search summary).
How the radio leaves the all-aluminium body: not found.

### 3.4 Cornix (CNC aluminium low-profile wireless split)

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Case | CNC aluminium, bead-blasted and anodised, with a frosted acrylic part. Hidden screws. Six screws hold the plate, foam and PCB stack to the bottom case. | https://kbd.news/Cornix-review-2715.html | likely (independent review) |
| Stack | 1.2 mm PCB, FR4 plate, Choc V2 hot-swap sockets | same | likely |
| Thickness | 15 mm case, 21 mm with keycaps, 24 mm with encoder. Footprint 142 x 91 mm per half. 278 g per half. | same | likely |
| Battery | 650 mAh per half | same | likely |
| Firmware | RMK with Vial. 3 Bluetooth slots. | same | likely |
| Price | USD 173 barebone, USD 185 built | same | likely |
| Certification | CE, FCC, TELEC | same | likely |
| Radio path | Not stated by the review. The frosted acrylic part and the controller cover are the candidate non-metal areas. | same | guess |

Complaints: hard to disassemble (keycaps off first, tiny unusual screws), battery cannot be reached or disconnected
without full disassembly, the power switch does nothing while the cable is plugged in, NKRO bug in stock firmware, thin documentation.

### 3.5 LP44 Split (open design, CNC aluminium, ZMK)

CNC aluminium case, 12 mm thick, two Seeed XIAO nRF52840 controllers, ZMK, Choc switches soldered, power switch on
the underside. Repository: https://github.com/juncho26/LP44_Split. Source: https://kbd.news/LP44-Split-2870.html.
Confidence: likely. Radio path and battery size: not stated in the post.

### 3.6 Community reports on aluminium cases and nRF52840 boards

- A ZMK community thread titled "Mitigating poor Bluetooth performance with aluminium case" reports dropouts on an
  aluminium Corne case, both between halves and to the host. Advice in the thread: make a non-metal cutout directly
  above the controller antenna, even a small slot helps, and do not point the antenna end at a metal wall.
  On the nice!nano v2 the antenna is the meander trace at the USB-C end. If the board is mounted face down the antenna
  sits directly under the case. Source: https://www.answeroverflow.com/m/1417715438372126720 (search-engine summary only;
  the page returned HTTP 429). Confidence: likely.
- A keyboard vendor's engineering blog gives rules of thumb: window thickness under 2 mm (model uses 1.5 to 2.0 mm),
  polycarbonate relative permittivity about 2.9, antenna less than 5 mm from the inner face of the window, keep copper
  ground and components out of the antenna area, and Bluetooth may need a larger keep-out than a 2.4 GHz dongle link.
  The article cites no measurements. Source: https://attackshark.com/blogs/knowledges/wireless-windows-cnc-metal-keyboard-cases-engineering.
  Confidence: guess (unsupported vendor numbers). Use as a starting point and measure on the prototype.

### 3.7 CNC case guidance from the intended supplier

JLCCNC's own article on keyboard cases recommends 6061-T6 as the starting alloy, larger internal corner radii
(a 3 mm end mill leaves about 1.5 mm radius), no blanket tight tolerances (±0.05 mm may be enough, reserve tight
tolerances for PCB locators, connector openings, threads and mating faces), allowance for anodising build-up on holes,
threads and mating faces, masking where electrical contact is needed, and few setups. It gives no minimum wall
thickness and says nothing about antennas. Source: https://jlccnc.com/blog/custom-keyboard-case. Confidence: confirmed (supplier statement).

---

## 4. Open hardware references

### 4.1 Prospector (ZMK dongle with colour LCD)

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| MCU board | Seeed Studio XIAO nRF52840 | https://github.com/carrefinho/prospector | confirmed |
| Display | Waveshare 1.69 inch LCD module with touch (part 27057). The non-touch version has a different hole pattern. | same | confirmed |
| Driver | ST7789V, RGB565, 16-bit colour, LVGL. The module ships its own `display_st7789v.c` driver. | https://github.com/carrefinho/prospector-zmk-module, `Kconfig.defconfig` (cache `05-misc/prosp.defconfig`) | confirmed |
| LVGL settings | Dedicated display thread with 4096 byte stack, `LV_Z_VDB_SIZE` 100, memory pool 10000 bytes, refresh period 20 ms, `LV_COLOR_16_SWAP` on | same | confirmed |
| Backlight | PWM LED. Optional APDS9960 ambient light sensor for automatic brightness. Fixed brightness is a Kconfig option. | repo README | confirmed |
| Case | 3D printed. Four M2 x 6 and four M2.5 x 4 screws. Curved cover glass comes with the Waveshare module. | hardware repo README | confirmed |
| Power | USB powered dongle. No battery. | hardware repo README | confirmed |
| Firmware state | Main branch targets ZMK v0.3 (Zephyr 3.5). A work-in-progress branch targets ZMK main (Zephyr 4.1). | module README | confirmed |
| Licence | CERN-OHL-P-2.0 (hardware) | hardware repo | confirmed |

Lessons:

- A colour ST7789 screen on an nRF52840 under ZMK works today. The proof runs on USB power, as a dongle.
- It needs a custom status screen, a dedicated display thread and its own driver file. Stock ZMK does not provide a colour status screen.
- Ambient-light dimming is already solved in open firmware. Reuse the idea, not the code or fonts.

### 4.2 YADS (Yet Another Dongle Screen)

ST7789V display shield on a Seeed XIAO BLE, ZMK module with LVGL. Widgets: active layer, modifiers, connection state,
WPM, battery. It has brightness control and automatic dimming after inactivity. The author wrote it after the
Prospector module hung on keyboard disconnect and reconnect. Repository: https://github.com/janpfischer/zmk-dongle-screen.
Source: https://kbd.news/YADS-dongle-screen-2683.html. Confidence: likely.

### 4.3 nice!view (memory LCD for battery boards)

Sharp LS011B7DH03, 160 x 68 px, 1.08 inch diagonal, 30 Hz, 3-wire SPI, 36 x 14 x 2.9 mm. "<10uA typical power draw",
">1,000x power savings" against SSD1306 OLED. Source: https://nicekeyboards.com/docs/nice-view/. Confidence: confirmed (maker).

Lesson: battery ZMK boards use a monochrome memory LCD because it costs microamps. A backlit colour TFT costs
milliamps. A general ST7789 summary gives about 4 mA for the controller and 20 to 40 mA for the backlight
(https://done.land/components/humaninterface/display/tft/st7789/, search summary; confidence likely). The backlight is the load to manage.

### 4.4 ZMK display support

- The ZMK feature page calls displays "a proof of concept" and "not yet considered production-ready", because the
  display can stay blank after an external power cut-off (issue zmkfirmware/zmk #674). It names OLED and ePaper only.
  Source: https://zmk.dev/docs/features/displays. Confidence: confirmed.
- Configuration options that matter here: `CONFIG_ZMK_DISPLAY_BLANK_ON_IDLE`, `CONFIG_ZMK_DISPLAY_STATUS_SCREEN_CUSTOM`,
  `CONFIG_ZMK_DISPLAY_WORK_QUEUE_DEDICATED` (prevents slow displays from delaying key scanning), and the `zmk,display-led`
  chosen node, "The LED device to use for on/off blanking". Source: https://zmk.dev/docs/config/displays
  (cache `04-pages/zmk-display-config.html`). Confidence: confirmed.

### 4.5 RMK (Rust firmware)

Supports nRF52840, nRF54L15, ESP32 variants, RP2040 and Pi Pico W. BLE with automatic reconnection and multiple hosts.
Keymap editing through Vial, also over BLE. The README claims that a 2000 mAh battery can run a keyboard for several
months with the `async_matrix` feature, about 2 ms latency wired and 10 ms wireless. Licence MIT or Apache-2.0.
Source: https://github.com/HaoboGu/rmk. Confidence: confirmed (project claims).
Display: the crate has `display` and `ssd1306` feature flags (https://docs.rs/rmk, search summary; confidence likely).
ST7789 or colour display support in RMK: not found. The Cornix ships RMK on a commercial aluminium wireless board (see 3.4).

### 4.6 Adafruit MacroPad RP2040

RP2040, 8 MB flash. 128 x 64 SH1106 monochrome OLED on hardware SPI. 12 MX-compatible keys, snap-in without solder,
each key on its own GPIO (no matrix). Rotary encoder with 20 detents and push switch. 12 NeoPixels. 8 mm speaker with
class D amplifier. USB-C. STEMMA QT I2C port. Four M3 mounting bosses. The enclosure kit is two PCBs used as bottom
plate and key plate with M3 screws. Source: https://learn.adafruit.com/adafruit-macropad-rp2040/overview.
Confidence: confirmed. Price: not found. Wired only.

Lesson: FR4 plates are an accepted enclosure material at this size. One GPIO per key removes diodes when pins allow.

### 4.7 Pimoroni Keybow 2040

RP2040, 2 MB flash. 16 keys in a 4 x 4 grid, each on its own GPIO. Kailh hot-swap sockets for MX-compatible switches.
Per-key RGB through an IS31FL3731 matrix driver. BOOTSEL and reset buttons. USB-C. About 76 x 76 x 30 mm with
switches, keycaps and feet. Listed at 32.50 with switches and 25.00 bare in the shop's base currency.
Source: https://shop.pimoroni.com/products/keybow-2040 (cache `03-pages/pimoroni-keybow2040.json`). Confidence: confirmed.

Lesson: a 4 x 4 MX pad needs about 76 x 76 mm. That is the size floor for the key field of the target with 19 mm pitch.

### 4.8 Ploopy Knob

Open hardware knob with QMK. Hardware under CERN-OHL-S-2.0, firmware GPLv3. Production files and build documents are
public. Source: https://github.com/ploopyco/knob (cache `02-qmk/ploopyco__knob__master__README.md`). Confidence: confirmed.
MCU and sensor part: not found in the pages read. The documentation site lists appendices for PCBs and 3D printed parts.

### 4.9 Ocreeb MK2

Not reached. The guessed repository URL returned HTTP 404.

---

## 5. Comparison table

Values repeat the sections above. Empty cells mean not found.

| Device | Display | Radio | Battery | Body | Thickness | Price |
| --- | --- | --- | --- | --- | --- | --- |
| Work Louder Knob1 | 310 x 100 IPS | Bluetooth | 3000 mAh | Aluminium top and bottom shells | | USD 439 |
| Work Louder Creator Micro 2 Pro | none | Bluetooth | 2100 mAh | Aluminium frame and bottom, PC body | | USD 168 |
| Keychron Q0 Max | none | BT 5.1 x 3 hosts + 2.4 GHz | 1800 mAh, up to 50 h with RGB low | 6063 aluminium, steel plate | | USD 129.99 |
| Keychron Q1 Pro | none | BT 5.1 | 4000 mAh, up to 300 h unlit | Aluminium, plastic insert at rear | | |
| NuPhy Air75 V2 | none | BT 5.1 + 2.4 GHz | 4000 mAh, 220 h unlit | Aluminium frame, ABS bottom | 13.5 to 16 mm | |
| Lofree Flow | none | BT 5.0 | 2000 mAh | All aluminium | 10 mm thinnest | |
| Cornix | none | BLE x 3 hosts | 650 mAh per half | Aluminium with acrylic part | 15 mm case | USD 173 to 185 |
| DOIO KB16 / Megalodon | 0.91 in OLED | none | none | 6063 aluminium, acrylic base | 32 mm | USD 59 |
| MX Creative Keypad | 480 x 480 LCD under 9 keys | none | none | Plastic | 25.5 mm | USD 200 pair |
| MX Creative Dialpad | none | BLE 5.1 + Bolt (nRF52820) | 2 x AAA, 18 months | Plastic | 33.8 mm | (pair) |
| Stream Deck + | 800 x 480 LCD | none | none | Plastic with fixed stand | | USD 179.99 |
| Loupedeck Live | 4.3 in 480 x 272 touch | none | none | Aluminium cover | 30 mm | |
| TourBox Elite | none | Dual BLE 5.0 | 2 x AA, up to 2 months | ABS | 44 mm | |
| Prospector | 1.69 in ST7789V colour | BLE (dongle) | none (USB) | 3D printed | | DIY |
| Target class (GLYF claim) | Portrait colour | BT, 4 hosts | not stated | Aluminium | 19 mm | UAH 7,331 pre-order |

---

## 6. Design rules these devices agree on

1. **Give the antenna a non-metal exit.** Every wireless aluminium product with a known radio path uses one of three:
   a plastic insert in the rear wall (Keychron Q1 Pro), a plastic bottom (NuPhy Air75 V2), or a plastic or acrylic
   body section (Creator Micro 2 Pro, Cornix). Community reports show dropouts when a controller antenna sits under solid aluminium.
2. **Put the antenna at a board edge, next to the exit, and keep copper and metal away from it.** The Logitech Dialpad
   places a chip antenna at the PCB edge. The ZMK thread says to avoid pointing the antenna end at a metal wall.
3. **Use the rear wall for the exit.** The rear wall already has the USB-C opening and switches. A plastic insert there is easy to hide.
4. **Use one LCD panel and draw the key grid in firmware.** Stream Deck + and the MX Creative Keypad both put one panel
   behind several keys. Fixed pixel rectangles per icon keep the firmware simple.
5. **Treat the backlight as the main battery load.** Makers with a backlit LCD either stay wired or fit a large cell
   (3000 mAh in the Knob1). Open firmware blanks or dims the display on idle and uses an ambient light sensor.
6. **Use a single-chip BLE SoC from Nordic for the radio.** Logitech uses an nRF52820 in the Dialpad. The open boards
   use nRF52840 modules. Keychron's two-chip design exists to keep QMK and a 2.4 GHz dongle mode.
7. **Use low-profile switches with hot-swap sockets for a slim body.** Work Louder and NuPhy use the Gateron KS-33
   low-profile footprint. Cornix uses Kailh Choc V2 sockets. Full-height MX pads end at 30 mm or more (DOIO 32 mm, Keybow about 30 mm).
8. **Stack: aluminium shell, plate, PCB, bottom, held by screws from below.** Cornix uses six screws through the plate,
   foam and PCB stack. FR4 is an accepted plate and bottom material (Adafruit, Cornix).
9. **Offer about three or four Bluetooth hosts and a wired mode.** Keychron and Cornix give 3 hosts. TourBox gives 2. The GLYF claims 4.
10. **Add a small tilt.** Work Louder uses 4 degree magnetic feet. Lofree builds in 3.9 degrees. Elgato's fixed 45 degree stand draws criticism.
11. **Use a contactless or well-detented encoder and qualify a second source.** Logitech uses a Hall sensor with two
    approved parts. Adafruit uses a 20 detent encoder with push. Reviewers praise clear steps and a firm click (Stream Deck +).
12. **Design the CNC parts for the shop.** JLCCNC asks for 6061-T6, internal radii of 1.5 mm or more, tight tolerances
    only on locating features, and an allowance for anodising on threads and mating faces.

## 7. Mistakes reviewers and users complain about

1. **Bluetooth that fails to reconnect after host sleep, lags or drops** (Creator Micro 2 feedback thread). Reconnect
   behaviour needs a test plan on macOS, Windows and Linux before release.
2. **Duplicate device entries after re-pairing** (same thread). Keep a stable device identity per host slot.
3. **Low Bluetooth polling rate against wired** (Keychron: 90 Hz Bluetooth, 1000 Hz wired). State the wireless rate honestly.
4. **Battery life that collapses with lighting on** (Keychron Q0 Max: 50 h with RGB low on 1800 mAh; NuPhy: 220 h unlit, 35 to 57 h lit).
5. **Battery that cannot be inspected, disconnected or replaced without full disassembly** (Cornix review).
   Give the cell a connector and an access path.
6. **Power switch that does nothing while the cable is plugged in, so the cell sits on charge permanently** (Cornix review).
7. **Hard disassembly: hidden screws under keycaps, unusual screw heads, clips and adhesive, fragile ribbon cables**
   (Cornix review, iFixit Stream Deck Classic teardown).
8. **Disposable cells in a premium device** (Logitech Dialpad AAA, TourBox Elite AA).
9. **Display unit left wired while the companion unit is wireless** (MX Creative Console). Buyers expect one behaviour.
10. **Fitted hardware that firmware never enables** (Loupedeck CT Bluetooth chip).
11. **Too few controls, and page switching that slows work** (MX Creative Console review).
12. **No haptic or tactile feedback on a dial** (MX Creative Dialpad against TourBox Elite).
13. **Fixed stand angle** (Stream Deck +).
14. **Immature or outdated companion software at launch: few plug-ins, old VIA version, no default keymap, bricking
    during configuration, firmware update not offered** (Stream Deck +, DOIO KB16, Creator Micro 2).
15. **Thin documentation** (Cornix, DOIO KB16).
16. **Display that stays blank after power is restored** (ZMK issue #674). Test power cut and resume on the chosen firmware.

---

## 8. Sources read

Maker and primary sources:

- https://worklouder.cc/shop/keyboards/knob1
- https://worklouder.cc/shop/keyboards/creator-micro-2
- https://worklouder.cc/creator-micro-2
- https://worklouder.cc/shop/miscellaneous/wrk-lp1-switches
- https://worklouder.featurebase.app/p/creator-micro-v2-repeatedly-fails-to-reconnect-over-bluetooth-after
- https://www.keychron.com/products/keychron-q0-max-qmk-custom-number-pad (product JSON)
- https://github.com/Keychron/qmk_firmware (branch `wireless_playground`, `keyboards/keychron/q0_max/`)
- https://github.com/qmk/qmk_firmware (`keyboards/doio/kb16/`, `keyboards/work_louder/micro/`)
- https://www.keebmonkey.com/products/megalodon-triple-knob-macro-pad (product JSON)
- https://support.logi.com/hc/en-au/articles/24727157859351-Specification-MX-Creative-Console
- https://fccid.io/JNZYR0097 (Logitech Dialpad filing, internal photos PDF)
- https://www.elgato.com/us/en/p/stream-deck-plus-black
- https://docs.elgato.com/streamdeck/hid/stream-deck-plus
- https://www.ifixit.com/Teardown/Elgato+Stream+Deck+Classic+Teardown/194063
- https://monogramcc.com/
- https://www.lofree.co/products/lofree-flow-the-smoothest-mechanical-keyboard (product JSON)
- https://github.com/carrefinho/prospector and https://github.com/carrefinho/prospector-zmk-module
- https://nicekeyboards.com/docs/nice-view/
- https://zmk.dev/docs/features/displays and https://zmk.dev/docs/config/displays
- https://github.com/HaoboGu/rmk
- https://learn.adafruit.com/adafruit-macropad-rp2040/overview
- https://shop.pimoroni.com/products/keybow-2040 (product JSON)
- https://github.com/ploopyco/knob
- https://jlccnc.com/blog/custom-keyboard-case

Reviews and secondary sources:

- https://appleinsider.com/articles/23/01/21/keychron-q1-pro-review-finally-a-wireless-metal-mechanical-keyboard
- https://engadget.com/computing/accessories/logitech-mx-creative-console-review-an-affordable-entry-point-into-edit-panels-070101321.html
- https://blog.kowatek.com/?p=1758 (mirror of The Verge review of the Stream Deck +)
- https://kbd.news/Cornix-review-2715.html
- https://kbd.news/LP44-Split-2870.html
- https://kbd.news/YADS-dongle-screen-2683.html
- https://www.cliftoncameras.co.uk/uploads/specifications/TourBox%20Elite.pdf
- https://attackshark.com/blogs/knowledges/wireless-windows-cnc-metal-keyboard-cases-engineering
- https://forum.devtalk.com/t/built-a-420g-truly-wireless-cnc-split-keyboard-to-fix-my-coding-posture-zmk/240557 (no hardware detail)
- https://docs.bastardkb.com/help/bluetooth.html (no antenna detail)

Read only as search-engine summaries (lower confidence):

- https://www.answeroverflow.com/m/1417715438372126720
- https://www.creativebloq.com/reviews/nuphy-air75-v2
- https://thephonograph.net/electronics-tech-reviews/lofree-flow-review
- https://help.elgato.com/hc/en-us/articles/25920614901261-Elgato-Stream-Deck-Neo-Technical-Specifications
- https://www.pcgamer.com/loupedeck-live-review/
- https://forums.appleinsider.com/discussion/230578
- https://www.guru3d.com/articles-pages/mountain-display-and-macro-pad-for-keyboard-review,1.html
- https://www.provideocoalition.com/review-monogram-creative-console/
- https://www.gizmochina.com/2023/12/14/figma-launches-creator-micro-macro-pad-with-12-customizable-keys-priced-at-139/
- https://drop.com/buy/megalodon-doio-hot-swappable-rgb-30-keyboard/reviews
- https://done.land/components/humaninterface/display/tft/st7789/
- https://docs.rs/rmk

## 9. Not reached

- https://www.logitech.com/en-us/products/keyboards/mx-creative-console.html: HTTP 403. The support specification page was used.
- https://fcc.report/FCC-ID/JNZYR0097: HTTP 403. The fccid.io mirror was used.
- https://www.answeroverflow.com/m/1417715438372126720: HTTP 429 and a browser check. Only the search summary was read.
- https://www.pcgamesn.com/elgato-stream-deck-plus-review: HTTP 403.
- https://www.pcgamer.com/loupedeck-live-review/ and https://creativebloq.com/reviews/tourbox-elite: body not returned to the fetch tool.
- https://nuphy.com/products/air75-v2.json: HTTP 429. NuPhy QMK source path guessed and returned 404.
- https://www.razer.com/streaming-accessories/razer-stream-controller: page downloaded, no product specification text in the static HTML.
- https://www.tourboxtech.com/en/tourbox-elite.html: returned a short Japanese pre-order page. A retailer copy of the spec sheet was used.
- https://github.com/sb-ocr/ocreeb-mk2: HTTP 404 (guessed URL). Ocreeb was not covered.
- No teardown was found for: Work Louder Knob1 or Creator Micro 2, Keychron Q0 Max, Stream Deck +, Loupedeck Live or CT,
  MX Creative Keypad. MCU, display driver, charger IC and antenna details for these are not found.
- Not covered: Megalodon as a product separate from DOIO KB16 (same device), Stream Deck Neo internals, Ploopy Knob
  sensor part, charger or PMIC part numbers for any commercial device, YouTube teardown videos (no video search was run for this key).
