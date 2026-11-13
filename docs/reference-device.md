# Reference device: what is known about the GLYF

worxpad is an original design with the function set of the Prota Designs GLYF. The GLYF is a reference only.
No name, logo, artwork, firmware, software, 3D model or file of the GLYF is used in this repository; only facts
and measurements are. Nobody outside the maker has measured, opened or reviewed a GLYF (as of 2026-11-13), so
every dimension below comes from images.

Summary of [research/DOSSIER.md](../research/DOSSIER.md). Confidence words: **confirmed** (stated by the maker or
measured from a primary source), **likely** (consistent indirect evidence), **guess**. "Maker" means a claim by
Prota Designs; "ours" means measured or decoded in the research phase.

## Facts

| Fact | Source | Confidence |
| --- | --- | --- |
| Wireless macro pad: 16 keys (4 x 4), two knobs with push, two round push buttons, 240 x 240 colour LCD, USB-C, Bluetooth, battery, aluminium body | Maker product page; DOSSIER 1.1 | confirmed |
| Switches Kailh low-profile Choc V2 family (PG1353D full-POM class), hot-swap; exact model not found | Maker page; ours from a Kailh drawing; DOSSIER 1.4, 1.5 | confirmed (family) |
| Display 1.4 inch 240 x 240 IPS, ST7789V-compatible, SPI at 20 MHz, 31.2 mm square lens | Supplier drawing in a maker video; firmware decode; DOSSIER 1.8, 1.9 | confirmed |
| Bluetooth to 4 hosts, no 2.4 GHz dongle | Maker page; DOSSIER 1.11, 1.12 | confirmed |
| Battery "1,200 mAh Li-Ion"; real cell about 4.0 x 42 x 57 mm | Maker page; ours from video frames; DOSSIER 1.13, 4.21 | confirmed (claim), likely (size) |
| 16 layers of 16 keys, macros stored on the device; time and media widgets "TBD" | Maker page; DOSSIER 1.14, 1.15 | confirmed (claim) |
| Body 120.4 x 85.2 mm, 19.2 mm at the wedge apex, 13.0 mm at the front, 12.0 mm at the rear | Ours from maker drawings and CAD frames; DOSSIER 3 | likely |
| Key pitch 19.05 mm; keycap 18.4 mm base, 4.4 mm above the deck | Ours; DOSSIER 3 | confirmed (pitch), likely |
| Knobs 10.5 mm, top 11.8 mm above the deck, on two round 16.1 mm bosses | Ours; DOSSIER 3 | likely |
| Two CNC 6061 shells split 5.0 mm below the deck, four M2-class screws from the top under keycaps | Maker videos; ours; DOSSIER 4.24, 3 | confirmed (process), likely (screws) |
| SoC nRF5340 in a Holyiot HOLYIOT-21069 module with a chip antenna; no radio window in the case | Ours from firmware and video frames; DOSSIER 4.1 to 4.4 | confirmed (SoC, module), likely (no window) |
| Firmware ZMK on Zephyr with LVGL 9, MCUboot, update over USB CDC-ACM; modified ZMK Studio as companion app | Ours from published beta images; DOSSIER 4.5 to 4.7 | confirmed |
| W25Q128 flash for icons, MAX17048 fuel gauge, DS3231 RTC with a coin cell, linear charger with power path | Ours; DOSSIER 4.8 to 4.11 | confirmed (flash, gauge, RTC), guess (charger family) |
| 5 x 4 diode matrix: 16 keys, 2 knob pushes, 2 buttons | Ours from firmware; DOSSIER 4.13 | confirmed (driver), likely (pins) |
| Status: pre-order, "Shipping Early Q4 2026"; no review or teardown exists | Maker page; DOSSIER 2 | confirmed |

## GLYF versus worxpad

Only the rows where worxpad differs. Each reason links to the decision entry or the research record.

| Item | GLYF | worxpad | Why |
| --- | --- | --- | --- |
| Body plan | 120.4 x 85.2 mm | 128.4 x 85.2 mm, 8.0 mm wider on the right | Antenna bay clear of the display ([D1](decisions.md#d1-body-width-1284-mm)) |
| Body height | 19.2 mm apex at Y 12.7, 13.0 mm front | 20.6 mm apex at Y 15.0, 14.6 mm front | Battery pocket depth ([D4](decisions.md#d4-battery-cell-pocket-and-wedge-depth)) |
| Radio | nRF5340 Holyiot module, hand-soldered, chip antenna, no RF exit | nRF52840 u-blox BMD-340, machine-placed, PCB antenna in a metal-free bay, 30 mm wall slot with a POM insert | RAM fits the nRF52840; stock and placement at JLCPCB; a designed RF exit ([D16](decisions.md#d16-radio-module-bmd-340), [D2](decisions.md#d2-flank-scoops-end-by-y-35-and-the-rf-slot-is-30-mm)) |
| Flank scoops | to about Y 43 | end by Y 35 | Wall under the RF slot ([D2](decisions.md#d2-flank-scoops-end-by-y-35-and-the-rf-slot-is-30-mm)) |
| Knob covers | two round bosses | one rounded-rectangle plinth (R2.8) over both encoders | Stock encoder is taller than the deck allows ([D3](decisions.md#d3-one-knob-plinth), [D25](decisions.md#d25-knob-plinth-is-a-rounded-rectangle)) |
| Display | 1.4 inch, 25.2 mm active, 20-pin flex, printed tempered glass | 1.3 inch DM-TFT13, 23.4 mm active, 24-pin flex, painted 1.0 mm PMMA lens of the same 31.2 mm size | Only 240 x 240 panel sold in single units with a drawing ([display](../research/components/display.md) 1) |
| Backlight | on/off | PWM dimming | Battery life ([display](../research/components/display.md) 6.2) |
| Battery | 1,200 mAh, 4.0 mm pouch, about 1.25 mm plug | 1,200 mAh retail cell, 5.0 x 34 x 62 mm, JST PH 2.0 | Buyable in small numbers ([D4](decisions.md#d4-battery-cell-pocket-and-wedge-depth)) |
| Power switch | slide switch, likely in the battery line | slide switch on the LDO enable; charging works while off | 50 mA switch rating; charge while off ([power](../research/components/power.md) 8) |
| RTC | DS3231 with a coin cell | none; host sends the time | Smallest design with a clock widget ([D19](decisions.md#d19-clock-widget-from-host-time-no-hardware-rtc)) |
| Rear openings | stadiums on the split line | notches wholly in the bottom shell | Parts sit below the split; no undercut ([D18](decisions.md#d18-rear-openings-wholly-in-the-bottom-shell)) |
| Bootloader | MCUboot, update over SMP | Adafruit nRF52 UF2 0.11.0, drag-and-drop | Family convention, ZMK default for the nRF52840 ([mcu-radio](../research/components/mcu-radio.md) 1) |
| Feet | four moulded 22.5 mm silicone stadiums | four round 3M Bumpon SJ5076; front pair at the GLYF centres, rear pair 2.3 mm further forward | Stock part, no tooling for 5 units ([enclosure](../research/components/enclosure-manufacturing.md) 10); rear pockets off the apex ([D31](decisions.md#d31-rear-feet-and-the-c2-spot-face)) |
| Keycaps | injection-moulded PBT | project cap printed in black resin | Batch of 5 ([keys](../research/components/keys.md) 6.5) |
| Assembly | bottom-side SMT, rest by hand | both faces machine-placed | Buttons and FPC connector must sit on top ([D9](decisions.md#d9-double-sided-pcba)) |
| Top screws | four M2-class countersunk | four M1.6 DIN 7991 | 0.8 mm plate web to the switch openings ([D30](decisions.md#d30-k-screws-m16)) |
| Switch swap | not documented | on a printed jig with the bottom shell off | Sockets sit over the cell ([D26](decisions.md#d26-switches-go-in-on-an-insertion-jig)) |

Everything not listed follows the GLYF: 4 x 4 keys at 19.05 mm pitch, Choc V2 class switches, two knobs with push,
two round buttons, 240 x 240 colour display in a 31.2 mm lens, USB-C, multi-host Bluetooth, W25Q128 icon flash,
MAX17048 gauge, two CNC aluminium shells split 5.0 mm below the deck, four screws from the top under the caps.
