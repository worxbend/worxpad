# Follow-up: battery cell and runtime

Date: 2026-11-13
Key: `follow-battery-cell-and-runtime`
Question: which 1,200 mAh class cell fits under the key field, and how long does it run?

Cache: `research/_cache/follow-battery-cell-and-runtime/` (frames, datasheets, scripts). Paths below that start with
`frames-`, `web-`, `ds-`, `zmk-`, `jlc-` or `scripts/` are inside that directory. The directory is gitignored, and the
video frames in it are for measurement only.

Confidence words: confirmed (stated by the maker or read from a primary source), likely (consistent indirect
evidence), guess.

## 1. Short answer

1. The real GLYF sample cell is labelled. The label reads "DTP404257 3.7V 1200mAh 4.44Wh". That is a Data Power
   Technology pouch cell of 4.0 x 42 x 57 mm. The two cells in the maker's illustrations (503562 and 653450) are
   stock pictures and are not the fitted cell.
2. The cell does not sit under the whole key field. It sits in a deeper pocket under the rear rows, where the wedge
   makes the body thicker. The pocket in the anodised prototype shell measures about 43 x 74 mm.
3. A height budget from the Kailh drawings shows why. A 4.0 mm cell under hot-swap sockets needs a body of about
   14.9 mm. The front edge is 13.1 mm. A 6.5 mm cell needs 17.65 mm, which is more than the 17.0 mm rear thickness.
4. No battery-life figure exists in any public source. The estimate from datasheet currents is about 23 hours of
   display-on time at full backlight (range 18 to 30 hours), about 52 hours at 30 % backlight, and several months
   with the display blanked and the Bluetooth link idle.
5. JLCPCB does not process consigned batteries. No PCBWay battery rule was found. Plan to buy the cell separately
   and plug it in by hand.

## 2. The real cell

| Fact | Source | Confidence |
| --- | --- | --- |
| The custom sample cell shown by the maker on 2024-11-05 carries the print "DTP404257 3.7V", "1200mAh 4.44Wh" and a third line "4MCT". The dot-matrix "7" looks like a "T"; the same glyph appears in "3.7V", so the model is 404257. | YouTube `Kp9UA2LNt6g` at about 18 s and 28 s; `frames-02/label.png`, `frames-01/a111.png`; earlier crop `research/_cache/youtube/crops-01/Kp9UA2LNt6g-f019-battery-3x.png` | confirmed |
| Two batches appear in that clip. The first had the wrong connector. The second has "the correct size connector to fit the smaller plug". Both batches show the same label. | Auto-subtitles of `Kp9UA2LNt6g` (`research/_cache/youtube/meta-01/Kp9UA2LNt6g.en-orig.vtt`); frames at 18 s and 28 s | confirmed |
| The maker says "these batteries are custom made". | same subtitles | confirmed |
| "DTP" is the prefix of Shenzhen Data Power Technology Ltd. Its model code is thickness, width, length. Its specification for DTP502535 gives "T Max 5.0", "W Max 25.0", "L Max 35.0", so the code is the maximum envelope of the finished pack. DTP404257 is therefore 4.0 x 42.0 x 57.0 mm maximum. | `web-02/dtp502535.pdf` (from `cdn.shopify.com/.../SPE-DTP502535-400mah-3.7V-En-1.0V.pdf`), section 4 | likely |
| DTP404257 is not in the maker's public catalogue. The 1000 to 3000 mAh page lists DTP503759, DTP103040 and DTP373580 at 1200 mAh. Custom cells have a minimum order of 3000 pieces; samples are paid in advance. | https://www.dtpbattery.com/category/1000-3000mahpolymer-batteries ; https://www.dtpbattery.com/productsdetail/DTP503759-1200mAh-Lipo-Battery-166756 | confirmed (absence on 2026-11-13) |
| The pack has a protection board under yellow polyimide tape at one short end and two wires (red, black). There is no third wire, so the pack has no thermistor lead. | `frames-01/a111.png` | confirmed |
| The plug is a small white 2-position housing. The two wires touch each other inside it, and each wire is about 1 mm thick. That fits a 1.25 mm pitch housing of the Molex PicoBlade style, and does not fit a 2.0 mm JST PH. | `frames-02/conn.png` | likely (pitch), guess (connector family) |
| Edge-on view: thickness is about 7.5 to 8.8 % of the visible length. With a 57 mm length that gives 4.3 to 5.0 mm. The cell is tilted toward the camera, so the true value is lower. This agrees with 4.0 mm and excludes 6.5 mm. | `frames-01/a107.png`, `frames-02/edge.png` | likely |
| The cell plugged into the December 2025 board is the same style: silver pouch, yellow tape at one end, red and black wires, small white plug. No label is visible on the side shown. | `research/_cache/youtube/frames-01/S9c5WuorsgQ/f060.jpg`, `f061.jpg`; sheet `frames-01/s9_sheet.jpg` | likely (same cell) |
| The product page states "1,200 mAh Li-Ion Battery". This matches the label. | `research/raw/official-site.md` section on tech specs | confirmed |
| Standard figures for the Data Power family, taken from the DTP502535 sheet: charge limit 4.20 V, cut-off 3.00 V, standard charge 0.2 C, maximum continuous charge and discharge 1.0 C, charge temperature 0 to 45 degrees C, 300 cycles to 80 % at 0.5 C. For 1200 mAh the product page of DTP503759 gives a standard discharge of "0.2C(240mA)". | `web-02/dtp502535.pdf`; `web-08/dtp503759.html` | likely (family values, not the 404257 sheet) |
| Mass: not found for DTP404257. A catalogue cell of nearly the same size, EEMB LP404261, is listed at 20 g and 1000 mAh. A 5 x 34 x 62 mm, 1200 mAh retail cell weighs 23 g. Expect 20 to 23 g. | https://www.eemb.com/products-55 ; https://www.adafruit.com/product/258 | likely |

## 3. Where the cell sits in the GLYF

Method: frame `frames-03/ly_0056.jpg` (YouTube `LyKoZR8Q888`, 1080 x 1920, anodised bottom shell held in a hand) was
mapped to millimetres with a four-point homography. The four outer rim corners were set to 84.9 x 120.0 mm, the
outline from `research/raw/official-site.md`. Script: `scripts/pocket.py`. The rim is the reference plane. The pocket
floor is further from the camera, so the true pocket is 2 to 4 % larger than the figures below. Error is about 2 mm.

Check of the method: the two notches in the rear wall map to centres 16.5 mm and 36.4 mm from the right end. The
side render gives 19 mm (USB-C) and 37 mm (slide switch).

| Fact | Value | Confidence |
| --- | --- | --- |
| Deep pocket size | about 43 mm (front to rear) x 74 mm (left to right) at rim scale; about 44 x 76 mm after the depth correction | likely |
| Pocket position, front to rear | 9 mm to 53 mm from the rear outer face. That is the rear half of the body. | likely |
| Pocket position, left to right | 12 mm to 86 mm from the left outer face. It ends about 34 mm from the right end, at the boundary of the control column. | likely |
| Relief notch | A shallow step at the right front corner of the pocket, about 11 mm x 15 mm, toward the control column. The battery connector on the PCB is in that area, so the notch is the wire path. | likely |
| Fit of a 42 x 57 mm pack | The 42 mm width fits the 43 to 44 mm dimension with about 1 mm play per side. The 57 mm length leaves about 18 mm for the wires and the plug. | likely |
| Shell generation | The shell belongs to the 2025 "GLYF MOCK v24" CAD shown in the same clip. The pocket of the shipped unit is not documented. | confirmed (prototype), guess (shipped unit) |

Conclusion: the pocket was cut for a pack about 42 mm wide and about 4 mm thick. The DTP404257 is the only cell seen
that matches. A 503562 (35 mm wide) or a 653450 (34 mm wide) would be loose in it by 8 to 9 mm. Confidence: likely.

## 4. Height budget

Inputs.

| Item | Value | Source | Confidence |
| --- | --- | --- | --- |
| Choc V2 (PG1353): plate top to PCB top | 2.20 mm | Kailh drawing CPG135301D03, `research/_cache/follow-switch-family-and-socket/pdf-render-01/PG135301D03-1.png` | confirmed |
| Choc V2: plate top to stem top | 6.40 mm (3.10 mm of it is stem above the housing) | same drawing | confirmed |
| Choc V2: pin length below PCB top | 3.00 +/- 0.2 mm | same drawing | confirmed |
| Hot-swap socket CPG135001S30: body height below the PCB | 1.80 +/- 0.1 mm (3.05 mm overall with the posts that enter the PCB) | Kailh specification KH-PS-1702-35 page 3, `web-06/sock-04.png` | confirmed |
| PCB | 1.60 mm (1.20 mm is an option and saves 0.4 mm) | design choice | - |
| Insulating sheet between the sockets and the cell | 0.3 mm | design choice | - |
| Cell swelling allowance | 10 % of thickness | common design rule; no datasheet value found for this cell | guess |
| Tape under the cell | 0.2 mm | design choice | - |
| Floor of the bottom shell | 1.5 mm aluminium; 1.6 mm for an FDM print | design choice | - |
| Plate top below the top face of the case (recess of the key well) | about 2.9 mm. Derived: cap top is 5.0 mm above the top face (side render); stem top is 6.4 mm above the plate; the cap adds about 1.5 mm above the stem. | `research/raw/official-site.md` section 7.2 and the drawing | guess |
| GLYF body thickness | 13.1 mm at the front edge, rising at about 4.9 degrees to 16.9 mm at 44.5 mm behind the front edge, then 17.0 mm | `research/raw/official-site.md` section 7.2 | likely |

Result (script `scripts/runtime.py`, second half).

| Cell thickness | Depth below plate top | Body thickness needed (with 2.9 mm recess) | Pocket floor below PCB underside |
| --- | --- | --- | --- |
| 4.0 mm | 12.00 mm | 14.90 mm | 6.70 mm |
| 4.5 mm | 12.55 mm | 15.45 mm | 7.25 mm |
| 5.0 mm | 13.10 mm | 16.00 mm | 7.80 mm |
| 6.0 mm | 14.20 mm | 17.10 mm | 8.90 mm |
| 6.5 mm | 14.75 mm | 17.65 mm | 9.45 mm |

Reading of the table against the GLYF profile.

- The front edge (13.1 mm) cannot hold any cell under the sockets. The socket bottoms are about 8.5 mm below the top
  face, which leaves 4.6 mm to the outside, and 1.5 mm of that is floor.
- The body reaches 14.9 mm at about 21 mm behind the front edge. A 4.0 mm cell fits from there to the rear wall.
  The measured pocket starts about 32 mm behind the front edge, where the body is about 15.8 mm. That is consistent.
- The body reaches 16.0 mm at about 34 mm behind the front edge. A 5.0 mm cell fits only in the last 48 mm.
- A 6.5 mm cell (653450) needs 17.65 mm and does not fit anywhere in a 17.0 mm body. A 6.0 mm cell (603450) needs
  17.1 mm and fits only with a thinner floor or a 1.2 mm PCB.

Confidence of the conclusions: likely. The recess value is the weakest input. Each 0.5 mm of error in it moves every
"body thickness needed" value by 0.5 mm.

Design notes that follow from the stack.

1. Put the pocket under the rear key rows, not under all four rows.
2. Keep through-hole pins (encoder legs, coin-cell holder, switch pins without sockets) out of the pocket outline,
   and put an insulating sheet over the socket bodies. Socket solder joints face the pouch.
3. A pocket envelope of 44 x 66 mm plus a wire relief, with the floor 7.8 mm below the PCB underside, accepts every
   candidate in section 5 up to 5.0 mm. If only the 4.0 mm class is wanted, 6.7 mm is enough.
4. The pack has no thermistor lead. A charger temperature input needs an NTC on the PCB next to the pocket.

## 5. Candidate cells for worxpad

Catalogue sizes are from the Lipol Battery list of 1000 mAh and larger cells (`web-03/`, parsed table). The list
gives thickness x width x length and capacity. Per-model sheets with protection-board length, connector and mass
were not fetched; see section 9.

| Model (size code) | Size, mm | Capacity | Fits the 4.0 mm stack | Fits a 44 x 66 x 5.0 pocket | Note | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| DTP404257 | 4.0 x 42 x 57 | 1200 mAh | yes | yes | The GLYF sample cell. Custom item, not a catalogue part. | confirmed (label) |
| LP404060 | 4.0 x 40 x 60 | 1400 mAh | yes | yes | Closest catalogue size to the GLYF cell. | confirmed (catalogue) |
| LP414361 | 4.1 x 43 x 61 | 1200 mAh | yes, tight | yes | 43 mm width needs a 45 mm pocket. | confirmed (catalogue) |
| LP454261 | 4.5 x 42 x 61 | 1200 mAh | no | yes | | confirmed (catalogue) |
| LP503560 / 503562 | 5.0 x 35 x 60 to 62 | 1200 mAh | no | yes | Retail stock with JST PH: 34 x 62 x 5 mm, 23 g, 500 mA charge advised. | confirmed (catalogue and retailer) |
| LP503759 | 5.0 x 37 x 59 | 1250 mAh | no | yes | EEMB lists 25 g. Retail stock with JST PH 2.0. | confirmed |
| LP504050 | 5.0 x 40 x 50 | 1200 mAh | no | yes | Shortest 5 mm option. | confirmed (catalogue) |
| LP603450 | 6.0 x 34 x 50 | 1200 mAh | no | no | Needs a 17.1 mm body. | confirmed (catalogue) |
| LP653450 | 6.5 x 34 x 50 | 1300 mAh in this catalogue; the maker's stock picture says 1200 mAh | no | no | Needs a 17.65 mm body. | confirmed (catalogue) |
| LP103040 | 10 x 30 x 40 | 1200 mAh | no | no | Too thick for a slim body. | confirmed (catalogue) |

Energy density check: 4.44 Wh in 4.0 x 42 x 57 mm is 464 Wh/l. The catalogue cell LP404060 gives 1400 mAh (5.18 Wh)
in 9.6 cm3, which is 540 Wh/l. A 1200 mAh rating for the 404257 size is therefore plausible. Confidence: likely.

Choice for worxpad: design the pocket for the 4.0 x 42 x 57 to 60 mm class (404257 or 404060) and leave the floor
depth for 5.0 mm if the body thickness at the pocket allows 16.0 mm. Retail 503562 cells then also fit, which makes
the prototype easy to source. Retail cells usually carry a JST PH 2.0 plug, so the board connector decides which
cells plug in without rework. This is a recommendation, not a finding.

## 6. Load figures

| Load | Value | Source | Confidence |
| --- | --- | --- | --- |
| Backlight of a 1.3 inch 240 x 240 IPS panel | 2 white LEDs in parallel, 30 to 40 mA at 2.8 to 3.0 V, 250 cd/m2 typical | DM-TFT13-377 panel datasheet, `ds-07/dm_tft13_377.pdf` | confirmed (for that panel) |
| Panel logic current, same panel | 8 mA typical, 10 mA maximum | same | confirmed |
| ST7789V controller alone | Normal mode 6.0 mA typical, 7.5 mA maximum. Sleep-in mode 15 uA typical, 30 uA maximum. | ST7789V datasheet section 7.3, `ds-07/st7789v.pdf` | confirmed |
| nRF5340 application core running | 3.3 mA (CoreMark from flash, 64 MHz, DC/DC, 3 V); 7.8 mA at 128 MHz | Nordic nRF5340 product specification, current consumption chapter | confirmed |
| nRF5340 network core running | 2.4 mA | same | confirmed |
| nRF5340 radio | 4.1 mA TX at 0 dBm, 3.7 mA RX, DC/DC, 3 V | same | confirmed |
| nRF5340 System ON idle with RTC | 1.5 uA per core entry; System OFF 0.9 to 1.0 uA | same | confirmed |
| nRF5340 as BLE peripheral in a connection, empty packets, 3.0 V, DC/DC on both cores, 0 dBm, LFXO | 389 uA at 7.5 ms interval; 196 uA at 15 ms; 100 uA at 30 ms; 68 uA at 45 ms; 32 uA at 100 ms; 9.5 uA at 15 ms with peripheral latency 30. Idle 3.1 uA. | Nordic Online Power Profiler back end, queried 2026-11-13, `web-09/content_10_*.html` | confirmed (model output, not a measurement) |
| nRF52840, same conditions | 297 uA at 15 ms; 101 uA at 45 ms; 12 uA at 15 ms with latency 30 | same, `web-09/content_2_*.html` | confirmed (model output) |
| ZMK measured values on nRF52840 | 23 uA per idle host connection; 315 uA while a key is held; 2 % of the time counted as typing; battery factor 0.85; self-discharge 5 % per month | ZMK source `docs/src/data/power.js` and `docs/src/components/power-estimate.js`, `zmk-04/` | confirmed |
| ZMK profiler display presets | E-paper, 128 x 32 OLED (10 mA active) and nice!view only. No backlit TFT preset exists, so the profiler cannot model this device. | same | confirmed |
| MAX17048 fuel gauge | 23 uA typical and 40 uA maximum in active mode; 3 to 4 uA in hibernate; 0.5 uA in sleep | MAX17048 datasheet, `ds-07/max17048_sf.pdf` | confirmed |
| DS3231M real-time clock on the main supply | Standby 130 uA and active 200 uA at 3.63 V, as returned by a search summary of the datasheet table. Typical or maximum: not verified. | search summary; the primary PDF did not load | likely |
| W25Q128JV flash | Standby 10 uA typical, 60 uA maximum; power-down 1 uA typical, 20 uA maximum | Winbond datasheet, `ds-07/w25q128jv.pdf` | confirmed |
| Regulator and charger quiescent current | Depends on the parts chosen. ZMK lists 15 uA for the nice!nano v2 regulator. | `zmk-04/power.js` | confirmed (reference only) |

Observations.

- The backlight and the panel logic are 43 mA of a 44 mA total. The radio and the SoC do not matter for display-on
  runtime.
- With the display blanked, the DS3231M on the main rail is the largest steady load if it draws near 130 uA. A clock
  that draws under 1 uA, or the SoC's own RTC, would remove most of the blanked-state current. This is a component
  choice for the design step.
- A switching regulator gains little. At an average cell voltage of 3.8 V an LDO to 3.3 V is 87 % efficient.

## 7. Runtime estimate

No public runtime figure exists. The maker did not answer the question "projected battery duration?" under video
`v9_v6v359Tw` (`research/raw/youtube.md`). The product page, the update articles, the firmware release notes and
the reviews searched by the other agents give none. Confidence: confirmed absence.

Assumptions: usable capacity 960 / 1020 / 1100 mAh (80 %, 85 %, 92 % of 1200 mAh; the 85 % value is the ZMK
profiler factor). LDO supply, so rail current equals cell current. SoC and firmware activity with the display lit is
0.3 / 0.8 / 2.0 mA, which is a guess because no measurement of LVGL on the nRF5340 was found. Always-on parts are
0.06 / 0.15 / 0.30 mA. Script: `scripts/runtime.py`.

| State | Current, best / mid / worst | Runtime, best / mid / worst |
| --- | --- | --- |
| Display lit, backlight 100 % | 36.4 / 43.9 / 52.3 mA | 30 / 23 / 18 hours |
| Display lit, backlight 50 % (needs PWM) | 21.4 / 26.4 / 32.3 mA | 51 / 39 / 30 hours |
| Display lit, backlight 30 % (needs PWM) | 15.4 / 19.4 / 24.3 mA | 72 / 52 / 40 hours |
| Display blanked, Bluetooth link idle | 0.06 / 0.15 / 0.30 mA | 708 / 283 / 142 days before self-discharge |

Self-discharge at 5 % per month equals about 83 uA for a 1200 mAh cell. With it, the blanked state lasts about four
to six months in the mid case.

Mixed use, mid case, days per charge.

| Display lit per day | Backlight 100 % | Backlight 30 % |
| --- | --- | --- |
| 2 hours | 11.2 days | 24.2 days |
| 4 hours | 5.7 days | 12.6 days |
| 8 hours | 2.9 days | 6.5 days |

Confidence of all runtime values: guess. They are arithmetic on datasheet currents of a comparable 1.3 inch panel,
not measurements of the GLYF. The GLYF panel is about 1.4 inch and its backlight current is not known.

Charge time: at 500 mA a 1200 mAh cell takes about 3 hours including the constant-voltage phase. At the 0.2 C
standard rate (240 mA) it takes about 6 hours. A retailer of a 1200 mAh cell advises 500 mA or less. The Data Power
family allows 1 C. Confidence: likely.

## 8. Maker firmware behaviour that affects runtime

| Fact | Source | Confidence |
| --- | --- | --- |
| Display blanking was added to production builds in v0.1.3 (2026-05-13). v0.1.4 (2026-06-18) fixed the setting and made it changeable at run time. The image stores it under `display_blank/state`. | `research/_cache/regulatory-software/github-04/glyf_releases.json`; `firmware-06/strings_v014.txt` lines 1874 to 1875 | confirmed |
| v0.1.4: "render the screen before we unblank the display" and "when screen blanking is disabled, continue to poll rtc". The clock is therefore not polled while the display is blanked. | same release notes | confirmed |
| Blanking follows the ZMK activity state (`zmk_activity_state_changed` is in both images). The timeout value in the product is not readable from strings. The maker's 2025 development shield set `CONFIG_ZMK_IDLE_TIMEOUT=180000`, which is 3 minutes. | `firmware-06/strings_v010.txt` line 2752; `research/_cache/regulatory-software/github-repos-05/zmk-config-test/boards/shields/ext_flash/ext_flash.conf` | confirmed (mechanism), guess (3 minutes in the product) |
| The backlight is driven as a GPIO LED (`led_gpio`). No PWM driver string is in either image. The backlight is on or off, with no dimming. | `firmware-06/strings_v010.txt` line 4329 | likely |
| An external power switch node exists (`EXT_POWER`, "External Power"). It can cut a peripheral rail. Which parts are on that rail is not known. | `firmware-06/strings_v010.txt` lines 2760 to 2763 | confirmed (node), not found (rail contents) |
| The ST7789V driver uses sleep-in and blanking calls ("Failed to turn blanking on", "Failed to exit the sleep mode"). | `firmware-06/strings_v010.txt` lines 4252 to 4254 | confirmed |
| Battery state comes from the MAX17048 and goes to the Bluetooth Battery Service and to a battery widget with charge-state images. | strings `sensor_max17048`, "Setting BAS GATT battery level"; v0.1.4 notes | confirmed |
| Deep sleep (ZMK `CONFIG_ZMK_SLEEP`) or a soft-off behaviour: no string proves or excludes it. The device has a hardware slide switch. | both string files | not found |

What this means for worxpad: copy the blank-on-idle behaviour, and add PWM dimming, which the maker firmware does
not have. Dimming to 30 % roughly doubles display-on runtime.

## 9. Assembly houses and lithium cells

| Fact | Source | Confidence |
| --- | --- | --- |
| JLCPCB consigned parts: "Batteries, ultracapacitors, materials from ECCN catalogue and non-machinable materials will not be processed and will be returned to customers or discarded by default." | https://jlcpcb.com/help/article/consignment-part-terms-conditions , item 4; copy in `web-05/jlc_consign.html` | confirmed |
| JLCPCB: "Unassembled consigned parts cannot be shipped with PCBs regarding customs clearance issue". | same page, item 13 | confirmed |
| JLCPCB global sourcing lists batteries among parts that need commodity inspection and certification fees. | https://jlcpcb.com/help/article/global-sourcing-parts-order-terms-conditions (search summary) | likely |
| The JLCPCB parts library does hold pouch cells. They are "Extended" parts, assembly type "Wave soldering", "Standard only", and "cannot be shipped separately". On 2026-11-13 the entries were FLY.502728.390 (390 mAh, stock 11), FLY.602535.500 (500 mAh, stock 187), FLY.502528.450 (stock 14), FLY.304466.1000 (stock 14), FLY.374668.1500 (stock 7) and FLY.505060AR (stock 4). No 1200 mAh cell is listed. | https://jlcpcb.com/partdetail/FLYOUNG-FLY_502728390/C5154896 ; library query saved in `jlc-10/FLYOUNG.json` | confirmed |
| Whether JLCPCB ships an assembled board with a lithium cell attached to a customer abroad: not found. | - | not found |
| PCBWay: no help-centre rule on batteries was found. The terms say that components are bought per project and are not sold alone. The assembly page asks customers to e-mail for requests outside the listed capabilities. | https://www.pcbway.com/terms_service.html ; https://www.pcbway.com/assembly-capabilities.html (search summaries); help search saved in `web-09/pcbway_help.html` | not found (rule) |

Plan: order the board without the cell. Fit a 2-pin battery connector on the board at the assembly house. Buy the
cell with a matching plug from a battery supplier or a retailer and plug it in during final assembly. Check the
polarity of every retail cell before the first connection, because plug polarity is not standard between sellers.

## 10. Sources read

Project files.

- `research/raw/official-site.md`, `youtube.md`, `social.md`, `regulatory-software.md`, `prior-art.md`,
  `community-press.md`, `conventions.md` (battery, power and geometry passages).
- `research/_cache/youtube/video-01/Kp9UA2LNt6g.mp4` and its subtitles; `research/_cache/geometry/yt-hd-01/LyKoZR8Q888.mp4`;
  `research/_cache/youtube/frames-01/S9c5WuorsgQ/`.
- `research/_cache/regulatory-software/firmware-06/strings_v010.txt`, `strings_v014.txt`;
  `github-04/glyf_releases.json`; `github-repos-05/zmk-config-test/`.
- `research/_cache/follow-switch-family-and-socket/pdf-render-01/PG135301D03-1.png` (Kailh Choc V2 drawing, fetched
  by another agent).

Web.

- https://www.dtpbattery.com/ , `/category/1000-3000mahpolymer-batteries`, `/category/500-100mahpolymer-batteries`,
  `/productsdetail/DTP503759-1200mAh-Lipo-Battery-166756`
- https://cdn.shopify.com/s/files/1/1040/8806/files/SPE-DTP502535-400mah-3.7V-En-1.0V.pdf
- https://www.lipolbattery.com/LiPo-Battery-1000mAh+.html , `/LiPo-Battery-900mAh+.html`
- https://www.eemb.com/products-55
- https://www.adafruit.com/product/258
- https://www.kailhswitch.com/Content/upload/pdf/202115927/CPG135001S30-data-sheet.pdf
- https://docs.nordicsemi.com/r/bundle/ps_nrf5340/page/chapters/current_consumption/doc/current_consumption.html
- https://devzone.nordicsemi.com/power/w/opp/2/online-power-profiler-for-bluetooth-le and its back end
  `https://power-profiler.azurewebsites.net/profiler/content/?prot=ble`
- https://zmk.dev/power-profiler ; https://raw.githubusercontent.com/zmkfirmware/zmk/main/docs/src/data/power.js ;
  `.../docs/src/components/power-estimate.js`
- https://newhavendisplay.com/content/datasheets/ST7789V.pdf
- https://cdn.shopify.com/s/files/1/0264/7629/files/DM-TFT13-377panel_Datasheet.pdf
- https://cdn.sparkfun.com/assets/b/b/2/c/b/MAX17048.pdf
- https://www.winbond.com/resource-files/W25Q128JV%20RevI%2008232021%20Plus.pdf
- https://jlcpcb.com/help/article/consignment-part-terms-conditions
- https://jlcpcb.com/partdetail/FLYOUNG-FLY_502728390/C5154896 and the JLCPCB parts-library search for "FLYOUNG"
- Web searches for "DTP404257", "404257", JLCPCB and PCBWay battery rules, nRF5340 currents, 1.3 inch panel
  backlights, MAX17048 and DS3231M currents.

## 11. Not reached or not found

- A datasheet for DTP404257. Web searches return nothing for the model. It is a custom item. Exact maximum
  dimensions, protection-board values, mass and cycle life of this cell are not found.
- The cell in shipped GLYF units. No teardown exists. The identification rests on 2024 samples and a 2025 shell.
- `https://www.analog.com/media/en/technical-documentation/data-sheets/DS3231M.pdf` and `MAX17048-MAX17049.pdf`:
  connection failed or timed out. The MAX17048 values come from a copy of the datasheet at SparkFun. The DS3231M
  values come from a search summary only.
- Lipol Battery per-model pages (LP503562, LP653450, LP603450, LP103040) with protection-board length, connector
  and mass: not fetched. The first two catalogue URLs tried returned HTTP 403; the list pages loaded later and gave
  size and capacity only.
- LCSC product data for the JLCPCB pouch cells (C5154896, C5154891, C49191534): the product API returned an empty
  result.
- Buydisplay ER-TFT013-2 datasheet: HTTP 403.
- A PCBWay statement on fitting or shipping lithium cells: not found.
- A JLCPCB statement on shipping assembled boards with a cell attached: not found.
- A measured current of ZMK with LVGL on an nRF5340: not found.
- The GLYF panel's own backlight current: depends on the panel identification in `display-module-sourcing`.
- The switch choice for worxpad is made in `switch-family-and-socket`. Section 4 assumes Kailh Choc V2 in
  CPG135001S30 sockets. Another switch or socket changes the 2.2 mm and 1.8 mm inputs.
