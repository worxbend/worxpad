# GLYF by Prota Designs: video research notes

Date of research: 2026-11-13. Agent key: `youtube`.

Scope: every video found about the GLYF macro pad or Prota Designs on YouTube and TikTok, with subtitles, comments and frame analysis.
All downloads are in `/home/worxbend/Projects/prota-clone/research/_cache/youtube/` (gitignored). No vendor artwork, firmware or models were copied into the repository.

Confidence labels used below:

- **confirmed**: stated by the maker (speech, caption, maker comment), or read directly from a primary frame (silkscreen, part marking, drawing, order page).
- **likely**: consistent indirect evidence.
- **guess**: plausible reading with weak evidence.

Who is speaking: "maker" means the official PROTA channel (`@PROTADESIGNS`), its two founders on camera, or a comment flagged by YouTube as written by the uploader. "Commenter" means any other YouTube user. No independent reviewer video exists (see section 1).

Video references use the YouTube id. The URL is `https://www.youtube.com/watch?v=<id>` (shorts also open as `https://www.youtube.com/shorts/<id>`). Frame references such as `S9c5WuorsgQ/f023` mean the file `frames-01/S9c5WuorsgQ/f023.jpg` in the cache, extracted at one frame per second (frame N is second N-1 to N of the video).

---

## 1. Coverage and state of the product

| Fact | Source | Confidence |
| --- | --- | --- |
| The official YouTube channel is "PROTA", handle `@PROTADESIGNS`, channel id `UCzhfE9Rx01Av1zrOAv4u-8w`, 47,200 subscribers. It has 2 long-form videos and 148 shorts. It has no community posts tab, no live streams tab and no playlists tab. | yt-dlp channel listing, `channel-01/*.jsonl` | confirmed |
| The official TikTok account is `@protadesigns` with 201 public posts. Most YouTube shorts are cross-posts of the TikTok videos. | yt-dlp listing, `social-01/tiktok-protadesigns.jsonl` | confirmed |
| The last YouTube upload is dated 2026-03-05 (`Q6CKpc6AK0o`). The last TikTok post is dated 2026-03-14 (`7617023441199287582`). Nothing was published on either account between then and 2026-11-13. | same listings | confirmed |
| No third-party review, unboxing or teardown video of the GLYF was found on YouTube. Thirty-eight search queries were run (search-01 to search-04). The only non-maker videos are a 42-minute Autodesk interview with the founders (`8WrTUNELp2U`) and a 16-second fan animation (`PJ_84kYPAT4`, channel "supnovaco", 94 views). | `search-01..04/*.jsonl` | confirmed (for the queries run) |
| No comment on any official video reports receiving a GLYF. Commenters in November 2025 to March 2026 say they pre-ordered and ask about the wait. | `digest-01/comments.txt` | confirmed |
| At pre-order launch (October 2025) the shop page read "Shipping starting Q4 2026". A commenter quoted it; another wrote "Way too far out for shipping". | commenters on `CqwCjghqUu0` | likely |
| The maker planned a beta test between pre-order and shipping: "it will go into production and then ship out and then probably a beta test a little bit in between". | maker, `8WrTUNELp2U` at 41:30 | confirmed |
| The product name is written "GLYF" by the maker in comments and on the PCB silkscreen. Auto-subtitles write "Glyph", "Glip" or "Cliff". | maker comments; `S9c5WuorsgQ/f044` | confirmed |
| The predecessor product is the "Printed Pad": 3 x 3 keys, monochrome OLED, 4 layers (36 keys), 3D-printed case, hot-swap, QMK firmware with VIA. The maker calls the GLYF "version two of the Printed Pad". | maker, `8WrTUNELp2U` at 17:30 and 21:08; `uN9ZiunZy_U` | confirmed |

## 2. Electronics

### 2.1 Microcontroller and radio

| Fact | Source | Confidence |
| --- | --- | --- |
| The December 2025 PCB carries a Holyiot module marked "Chip: nRF5340", "Model: HOLYIOT-21069", "FCC ID: 2ALGY21069", with CE and FCC marks. Its reference designator is U1. The module sits at the board edge under the display area with its antenna end pointing at the board edge. | `S9c5WuorsgQ/f023`, `f029` | confirmed |
| The maker states the MCU family as "Nrf!" and "we use nrf. Esp would consume too much power and is not great for a product like this." One nRF device does both the keyboard function and the radio. | maker comments on `Wt_-N3kfbMI`, `CqwCjghqUu0`, `Q0jl11n2_AY` | confirmed |
| The maker chose a pre-certified radio module to avoid FCC intentional-radiator testing: "you could purchase a pre certified FCC 5 layer module". The maker rejected modules with their own USB-C socket because of size. | maker comments on `Wt_-N3kfbMI` | confirmed |
| The nRF is configured in DC/DC mode. | maker comment on `ScYz1Z_T1UY` | confirmed |
| Earlier prototypes (March to November 2025) used a plug-in nRF52840 development board of nice!nano form factor that overhangs the right side of a 3D-printed case. A maker diagram shows a board labelled "nice!nano". | `Z8-k1frnIJM/f017`; `S9c5WuorsgQ/f006`, `f065`; `sr0MIYEi678/f002` | confirmed (dev board use), likely (nRF52840) |
| The maker's reply "We use the stm mcu" on video `L4MqWy5PSd0` is about the Printed Pad (the video is about the Printed Pad). It does not describe the GLYF. | maker comment on `L4MqWy5PSd0` | likely |
| Bluetooth version: not found. A 2.4 GHz dongle: not found, never mentioned. All wireless statements say "Bluetooth". | all subtitles and comments | confirmed absence in the sources read |
| Multi-host: "can easily connect up to 4 devices". Profile selection is done on a dedicated "Bluetooth layer" shown on the display. | maker comment on `Lgr_0N7SrDY`; maker, TikTok `7557263230071033118` | confirmed |

### 2.2 Firmware

| Fact | Source | Confidence |
| --- | --- | --- |
| Firmware is based on ZMK (Zephyr). The maker chose ZMK over QMK for battery management and for Bluetooth. | maker, `8WrTUNELp2U` at 39:30; video description of `8WrTUNELp2U` | confirmed |
| The display uses a Zephyr display driver and LVGL. ZMK's display code, written for OLEDs, was modified for the LCD (widget spacing, size, orientation). | maker, `Hzb1XL3zzrw`; maker comment "yes" to "Is that the lvgl starter screen?" on `kTnqYrpr2v8` | confirmed |
| Custom ZMK behaviours exist to select a widget or cycle widgets forwards and backwards, and the same for layers. The custom behaviours were made to work with ZMK Studio. | maker, `Hzb1XL3zzrw`, `SVFJb6qEKMQ` | confirmed |
| The display system has "normal widgets" (keymap icons, time, media, volume) and "system widgets" tied to system layers: a layer-select layer, a widget-select layer and a Bluetooth-profile layer. The matching system widget appears when the layer is entered. Users can remove and reorder normal widgets. | maker, TikTok `7557263230071033118` (2025-10-04) | confirmed |
| The knobs scroll through layers in the layer-select screen. A volume widget follows the knobs. | maker, `LWd2-QYQFss` | confirmed |
| The two round buttons below the display "control the screen". | maker, `8WrTUNELp2U` at 26:50 | confirmed |
| Macros and configuration are stored on the device. No host software is needed for macros. Host software is needed for host-fed widgets such as Spotify now-playing. | maker comments on `LWd2-QYQFss`, `wIC3IPEvYTs` | confirmed |
| The maker claims "an unlimited amount of layers with 16 macros possible on each layer" (March 2025). The shop page says "Up to 256 Macros", which equals 16 layers of 16 keys. | maker comment on `Wt_-N3kfbMI`; shop page (not a video source) | confirmed (statements), guess (16 layers) |
| Firmware is flashed over USB-C. The PCB also has exposed programming points (J3, a 2 x 3 pad group) and a reset tactile button (SW1). | maker comment on `CqwCjghqUu0`; maker, `S9c5WuorsgQ`; `S9c5WuorsgQ/f023` | confirmed |
| Open-source status: not stated by the maker. Commenters ask several times and get no answer. | comments on `v9_v6v359Tw`, `_7-Ndv3M_C4`, `77L_fMnvAtk` | confirmed absence |
| Known firmware bug during development: the external flash failed intermittently for months because the devicetree `size` property was given in bytes where bits were required, so the flash was declared at one eighth of its size. | maker, `8WrTUNELp2U` at 36:40 | confirmed |

### 2.3 Companion software

| Fact | Source | Confidence |
| --- | --- | --- |
| The configurator shown in November 2025 is a modified ZMK Studio. The window title bar reads "ZMK Studio" with tabs "Layers", "Widgets" and a device entry "GLYF". The Widgets tab lists "keymap", "media", "time". | `v9_v6v359Tw` frames 15 to 17 and 40 to 42 | confirmed |
| Protocol detail: on connect the device sends the full widget list with properties; the widget order is sent separately on each update event; the app maps widget ids to the list. Undo, redo, save and discard exist. | maker, `v9_v6v359Tw` | confirmed |
| Planned: a web-browser version and a downloadable version. Icons are assigned by drag and drop of image files. Wallpapers are planned. Linux, Windows and macOS are claimed. | maker comments on `v9_v6v359Tw`, `Qzn6t-ihyvc`; maker, `Nk6MD9QS8VA` | confirmed (as maker claims) |
| Macros are created by recording a key sequence in the app and saving it to the device. | maker, `Nk6MD9QS8VA`, `wLHIWHExL-k` | confirmed |

### 2.4 Display

| Fact | Source | Confidence |
| --- | --- | --- |
| The maker showed the supplier drawing of the display bought in November 2025. It reads: 1.4 inch, "240 x RGB x 240", viewing direction "ALL O'clock". Cover lens 31.20 +/- 0.1 mm square with four R2.00 corners. Backlight outline 28.00 +/- 0.15 by 31.35 +/- 0.15 mm. LCD glass 27.20 by 29.93 mm. Viewing area 25.80 mm. Active area 25.20 by 25.20 mm. Stack: lens 1.100 mm, OCA 0.200 mm, LCM 1.65 +/- 0.15 mm, total 2.950 +/- 0.15 mm. FPC tail length 17.30 +/- 0.5 mm, 20 contacts at 0.50 mm pitch (9.50 mm across contacts, 10.50 mm tail width), contact length 3.50 mm inside a 5.00 mm stiffened end, FPC plus stiffener 0.30 mm thick. The tail is offset: 8.75 mm from one LCD edge, then 10.50 mm of tail. Rear: 3M adhesive 0.15 mm on two side strips, black single-sided tape 0.05 mm on the non-reflective face. | `sr0MIYEi678/f010` to `f013`; 2x crop `crops-01/sr0MIYEi678-f010-lcd-drawing-2x.png` | confirmed (read from the drawing) |
| Five of these displays with bonded cover glass cost USD 210 as samples. The maker calls it "a high resolution screen with tempered glass attached". | maker, `sr0MIYEi678` | confirmed |
| The physical units filmed in January to March 2026 show a square display window with rounded corners, consistent with the 31.2 mm lens. The marketing renders make it look portrait, but the render in `CqwCjghqUu0/f018` also shows a near-square window. | `Q6CKpc6AK0o/f024`, `f059`; `Nk6MD9QS8VA/f044` | likely |
| The display controller: not found. A 1.4 inch 240 x 240 IPS panel with a 20-pin 0.5 mm FPC is normally an ST7789-class SPI panel. | inference | guess |
| On the PCB the display FPC passes through a milled slot (about 4 by 12 mm, rounded ends) to a bottom-side 0.5 mm flip-lock FPC connector J2. Transistor Q2 next to J2 is probably the backlight switch. | `S9c5WuorsgQ/f023`, `f021` | confirmed (slot and connector), guess (Q2 role) |
| Display history: prototype 1 used a hobby 1.8 inch-class TFT breakout ("super pixely"). A custom sample with glued tempered glass bought in November 2024 was rejected as too low resolution; its FPC is marked "ENH-TV0144006A" and the order page reads "128 Resolution TFT lcd display". One early screen was dead on arrival and the supplier gave a wrong specification. | `Kp9UA2LNt6g` frames 3, 28 to 33; `kTnqYrpr2v8`; crop `crops-01/Kp9UA2LNt6g-f031-lcd-fpc-3x.png` | confirmed |
| The maker rejected e-ink because of refresh rate and animations. | maker comment on `LWd2-QYQFss` | confirmed |
| Screen layout seen on real units: status row (application name, settings gear, battery icon; USB and charge icons on prototypes), then two knob label pairs (for example "<Zm+ >Zm-" and "<Brsh+ >Brsh-") with one icon each, then a 4 x 4 icon grid. | `Q6CKpc6AK0o/f024`; `S9c5WuorsgQ/f065` | confirmed |

### 2.5 Power, battery, clock

| Fact | Source | Confidence |
| --- | --- | --- |
| The PCB has two battery connectors: a 2-pin wire-to-board connector for a lithium-polymer pouch cell, and a through-hole coin-cell holder for the real-time clock. | maker, `S9c5WuorsgQ`; `S9c5WuorsgQ/f023`, `f060` | confirmed |
| Fuel gauge: "an extra chip communicating via i2c and connected to the battery". The May 2025 layout shows a footprint value starting "MAX170", read as MAX17048. | maker comment on `CqwCjghqUu0`; `ScYz1Z_T1UY/f014` | confirmed (I2C gauge), likely (MAX17048) |
| Real-time clock: DS3231MZ. The May 2025 layout shows "DS3231MZ_TRL". The November 2025 JLCPCB order lists LCSC part C107410 in SOIC-8 on the bottom side, which LCSC resolves to Maxim DS3231MZ+TRL. | `ScYz1Z_T1UY/f014`; `kOclb0i9bug/f008`; LCSC product API for C107410 | confirmed |
| A second SOIC-8 sits next to the RTC (U6 and U7). The May 2025 layout shows text starting "AT24C" and ending "SHM-T", read as an AT24C32 EEPROM. The maker says there are "2 other components for rtc". | `ScYz1Z_T1UY/f014`; maker comment on `ScYz1Z_T1UY` | likely |
| The coin cell shown for the December 2025 board is a Panasonic ML1220 (3 V rechargeable). The May 2025 layout labels the holder area "CR2032". | `S9c5WuorsgQ/f031` (inserted product picture); `ScYz1Z_T1UY/f014` | likely (the picture is an illustration added in editing) |
| Charger: "This charging IC safely charges our battery and automatically manages power between the battery and an external power source". The device can charge with the power switch on or off. The part is a small QFN (U2) with an inductor-size part L1 beside it. Part number: not found. | maker, `S9c5WuorsgQ`; maker comment on `ScYz1Z_T1UY`; `S9c5WuorsgQ/f023` | confirmed (function), not found (part number) |
| 3.3 V regulator: the May 2025 layout shows "XC6220B331MR" (Torex LDO, 3.3 V). | `ScYz1Z_T1UY/f014` | likely |
| Power switch: a side-actuated SMD slide switch on the rear edge. On the April 2025 prototype it gated a P-channel MOSFET (AO3401A, JLCPCB library page shown) between battery and system. A resistor placed by mistake between battery and MOSFET source dropped the rail to 0.9 V. | maker, `Z8-k1frnIJM`; `Z8-k1frnIJM/f012`, `f017`; `Nk6MD9QS8VA/f042` | confirmed |
| USB protection: silkscreen text "BSD3C051V" (ESD diode) near the USB-C socket in the V4 layout; a fuse F1, a SOT-23-6 part U5 and ferrite-size parts L2 and L3 sit behind the socket. | `S9c5WuorsgQ/f044`; `S9c5WuorsgQ/f023` | likely |
| Battery capacity: not stated. Two maker illustrations show 1200 mAh cells ("LP-503562 1200mAh 3.7V" and "UFX 653450 3.7V 1200mAh 4.44Wh"). The real cell plugged in at `S9c5WuorsgQ/f060` is an unlabelled silver pouch roughly the size of four key positions. | `Z8-k1frnIJM/f017`; `S9c5WuorsgQ/f029`, `f060` | guess (about 1200 mAh) |
| Batteries are custom-made samples with a small 2-pin plug. The first batch arrived with the wrong connector size. | maker, `Kp9UA2LNt6g` | confirmed |
| Battery life: not found. A commenter asked "projected battery duration?" and got no reply. | comments on `v9_v6v359Tw` | confirmed absence |

### 2.6 Storage

| Fact | Source | Confidence |
| --- | --- | --- |
| External NOR flash stores "macro icons and larger images". It is the reason the Printed Pad architecture could not be reused. | maker, `S9c5WuorsgQ`; maker, `8WrTUNELp2U` at 36:45 | confirmed |
| The flash is probably U8, a wide 8-pin package beside the module. Part number and capacity: not found. | `S9c5WuorsgQ/f023` | guess |

### 2.7 Keys, encoders, buttons

| Fact | Source | Confidence |
| --- | --- | --- |
| 16 keys in a 4 x 4 matrix with one SMD diode per key (D4 to D22 visible), all hot-swap. Sockets are Kailh-style SMD hot-swap sockets on the bottom side. | maker ("hot-swap sockets"), `S9c5WuorsgQ`; `S9c5WuorsgQ/f020` | confirmed |
| Key pitch is 19.05 mm in both directions. The May 2025 KiCad layout shows key footprints tiled edge to edge, each with silkscreen outlines labelled "19.05 spacing" and "18x17 spacing" and an "LED" marker box. | `ScYz1Z_T1UY/f015`; 2x crop `crops-01/ScYz1Z_T1UY-f015-kicad-dimension-2x.png` | likely |
| The footprint carrying both "19.05" and "18x17" outlines is of the kind drawn in Kailh Choc footprint libraries. | same frame | likely |
| Switches are low profile and mechanical: "We use these low-profile switches which allow us to make it thinner". The March 2026 unit has a switch with a lavender housing, two slots at one end, and an MX-type cross stem inside a round collar. The maker says each key is "a mechanical switch made out of the smooth plastic called POM". | maker, `K_bqsGX5qdg`, `Q6CKpc6AK0o`; `Q6CKpc6AK0o/f017`; `wLHIWHExL-k/f036` | confirmed (low profile, POM, cross stem) |
| The switch family is probably Kailh Choc V2 format (MX stem, Choc footprint), possibly one of the all-POM Choc V2 types. Exact model: not found. | inference from the two rows above | guess |
| The maker "will definitely offer different switches". Commenters say the shop offers switch or "key style" options without explanation. | maker comment on `4mGhEPTLoSA`; commenters on `v9_v6v359Tw`, `wLHIWHExL-k` | confirmed (intent) |
| Key backlight or RGB: none. "rgb is something we are on the fence about. We may potentially do it for V2". The footprint has an LED position that is not populated. | maker comment on `4mGhEPTLoSA`; `ScYz1Z_T1UY/f015` | confirmed |
| Keycaps are a custom design: square, low, straight tapered sides, a square concave dish, MX cross mount. Prototypes were resin printed (Elegoo Saturn 4 Ultra 16K). Production caps were planned as injection moulded. | maker, `qAuaOqLKj_Q`, `VipX8ReasHc`; `qAuaOqLKj_Q` frames 12 to 13, 28 to 29; `wLHIWHExL-k` frames 37 to 38 | confirmed |
| Two rotary encoders with push switch, through-hole, EC11-style: three signal pins on one side, two switch pins on the other, two mounting lugs. KiCad footprint name contains "RotaryEncoder_Switch". They are at the top right, side by side, references SW2 and SW4. The USB-C socket sits between them on the rear edge. | `S9c5WuorsgQ/f021`, `f044`; `ScYz1Z_T1UY/f014` | confirmed |
| Two round buttons below the display are SMD tactile switches. The May 2025 footprint name is "SW_Omron_B3FS" (SW3, SW5). The December 2025 board has two white square tactile parts in those positions. The caps are flat, slightly dished round buttons. | `ScYz1Z_T1UY/f014`; `S9c5WuorsgQ/f021`; `Nk6MD9QS8VA/f044` | confirmed |
| USB-C socket: mid-mount, through-hole shell tabs, on the rear edge. The footprint name starts "Type-C" and ends "M12" (a 16-pin TYPE-C-31-M-12 class part). | `ScYz1Z_T1UY/f014`; `S9c5WuorsgQ/f021` | likely |
| Knobs and buttons are plastic; everything else outside is aluminium ("fully out of aluminum besides the keycaps, knobs and buttons"). | maker comment on `qAuaOqLKj_Q` | confirmed |

### 2.8 PCB and assembly

| Fact | Source | Confidence |
| --- | --- | --- |
| The PCB is designed in KiCad. Revision silkscreen seen: "GLYF V4 2025 PROTA DESIGNS" with the joke line "This should work" -Noah. | `S9c5WuorsgQ/f044`, `f047`; maker, `YxNqUznpgjY` | confirmed |
| A horizontal dimension of 112.5000 mm is drawn above and below the board in the May 2025 layout. It is most plausibly the PCB width. Check: 4 x 19.05 = 76.2 mm of keys plus a right column of about 33 mm plus edge margins. | `ScYz1Z_T1UY/f015` | likely |
| Board outline: one rectangle with rounded corners, a notch on the rear edge at the USB-C socket, a slot for the display FPC, four plated mounting holes around the key field plus others near the edges. Black solder mask. | `kOclb0i9bug/f001`; `S9c5WuorsgQ/f020` | confirmed |
| Component placement: all SMD parts, hot-swap sockets, module, FPC connector, coin holder and battery connector are on the bottom side. Encoders, the two tactile buttons, switches and the display are on the top side. | `S9c5WuorsgQ/f020` to `f023`; `kOclb0i9bug/f017` | confirmed |
| The board is assembled by JLCPCB (order number prefix "SMT0251107", one-sided "bottom" SMT), then the maker hand-solders the rest. The Holyiot module is in the JLCPCB placement. | `kOclb0i9bug/f008`; maker, `S9c5WuorsgQ` | confirmed |
| Five-board order cost, November 2025: bare PCB USD 73.92 (engineering 24.00, colour 7.60, board 5.10, material type 3.38, minimum via hole 16.50, 4-wire Kelvin test 16.34, confirm file 1.00). Assembly USD 210.74 (setup 50.00, stencil 15.78, components 58.74, extended component fee 54.00, SMT 3.22, hand soldering 3.50, manual assembly 1.10, fixture 15.71, packaging 0.47, advanced options 7.86, confirm placement 0.43). Shipping 55.82, customs duties and taxes 151.67, coupon -15.00, PayPal fee 2.39, sales tax 24.34. Total USD 503.88. | `kOclb0i9bug/f016`, `f022`, frames 28 to 40 | confirmed |
| The "minimum via hole" and "material type" surcharges show a non-default stack-up or drill size. A commenter in May 2025 judged the earlier board to be two layers. Layer count of the final board: not found. | `kOclb0i9bug/f016`; commenter on `ScYz1Z_T1UY` | guess |
| The maker tests new power circuits on self-made breakout boards and perfboard before ordering assembled boards. | maker, `ScYz1Z_T1UY` | confirmed |

## 3. Mechanics

| Fact | Source | Confidence |
| --- | --- | --- |
| The case is two CNC-machined aluminium shells, bead-blasted and anodised black. Material is 6061 ("aerospace grade aluminum just means 6061 or 6063"; "It'll be the 6061"). | maker, `hBXO5tvxVr8`, `piNJL6_wltM`; maker, TikTok `7557776173275598110` | confirmed |
| The top shell is one part that includes the switch plate: 16 square switch openings in a recessed field, two encoder holes with raised ring bosses, a display pocket with an FPC notch, and two round button holes. There is no separate plate. | `Q6CKpc6AK0o/f035`, `f038`; `hBXO5tvxVr8` frames 25 to 26; `wLHIWHExL-k/f035` | confirmed |
| The bottom shell is a tray with stepped internal pockets (a deeper rectangular pocket under the key field for the battery, shallower ledges), screw bosses in the corners and notches on the rear wall for the USB-C socket and the slide switch. | `LyKoZR8Q888/f015`, `f019`; crop `crops-01/LyKoZR8Q888-f012-015-019-021.jpg` | confirmed |
| The underside has an integrated wedge at the rear that tilts the pad. The wedge is sculpted with concave scoops at both rear corners. Four pill-shaped silicone feet sit in milled slots, two on the wedge and two at the front. | `Q6CKpc6AK0o/f052`, `f057`; `4mGhEPTLoSA/f018`; `Nk6MD9QS8VA` frames 39 to 41 | confirmed |
| A caliper on one silicone foot reads 24.04 mm, taken as the foot length. The feet are custom-moulded silicone delivered on a strip. | `4mGhEPTLoSA/f015`; crop `crops-01/4mGhEPTLoSA-f015-foot-calipers-2x.png` | likely |
| The Fusion side view ("Mock Design") shows the profile: a thin top shell, a thicker bottom shell, the wedge growing toward the rear, keycaps standing proud of the top face and the knobs about one cap-height taller. | `Q6CKpc6AK0o/f057` | confirmed |
| Rear edge, left to right seen from behind: USB-C opening, then the slide power switch slot. Both are on the rear wall near the encoder end. | `Nk6MD9QS8VA/f042`, `f043`; `Q6CKpc6AK0o/f017` | confirmed |
| Weight: "265 grams" (on-screen text while the maker says "With it being so heavy, it just feels amazing in the hands"). | maker, `Nk6MD9QS8VA/f047` | confirmed |
| Thickness: no figure in any video. The shop page claims 19 mm. | shop page (not a video source) | not found in video |
| Overall footprint: no figure stated. From a near-frontal photo the body is 610 by 460 pixels (ratio 1.33) and the key pitch is about 100 pixels. With 19.05 mm pitch that gives about 116 by 88 mm. With the 31.2 mm lens as scale it gives about 125 by 94 mm. A 112.5 mm PCB plus walls supports roughly 118 to 120 mm width and 88 to 91 mm depth. | `Q6CKpc6AK0o/f059`; `ScYz1Z_T1UY/f015` | guess (needs the measurement agent) |
| A caliper frame on the top shell reads 10.30 mm. The measured feature cannot be identified from the frame. | `hBXO5tvxVr8/f027` | not usable |
| A darker "gunmetal" or grey top face appears in some January to March 2026 shots next to black units. A second colour is possible. | `Nk6MD9QS8VA/f044`; TikTok `7617023441199287582` | guess |
| The "dock" or "base plate with a silver block" in the hero render is a second copy of the pad shown from below, with its wedge and feet visible. No dock product is mentioned anywhere. | `CqwCjghqUu0/f018`; `LyKoZR8Q888` frames 8 to 9 | likely |
| Case supplier: a Chinese CNC vendor found through Alibaba, contact named "Susan". Samples took about two weeks. The machine in the vendor footage is a Taikan mill. Process: CNC, sandblast (grit chosen with the vendor), black anodise. | maker, `hBXO5tvxVr8`, `LyKoZR8Q888`, `8WrTUNELp2U` at 29:20 | confirmed |
| Cost driver named by the maker: number of machining set-ups and cuts, not the material. | maker, `piNJL6_wltM` | confirmed |
| The tempered cover glass arrives bonded to the LCD and sits in the top-shell pocket. A red pull tab on the protective film is visible on fresh prototypes. | maker, `Kp9UA2LNt6g`; `LyKoZR8Q888` frames 25 to 29 | confirmed |
| The maker will not sell a print-it-yourself kit ("assembling the electronics will make it far less accessible"), later softened to "We could potentially do this". Printed Pad STL and F3D files are free on the maker's Discord. | maker comments on `qAuaOqLKj_Q`, `LyKoZR8Q888`, `ugj16Tmrbyc` | confirmed |

## 4. Prototype history (useful for our own prototype plan)

| Stage | What it was | Source | Confidence |
| --- | --- | --- | --- |
| V1, October 2024 | 4 x 4 keys on a custom PCB with a hobby TFT breakout and tall encoders, QMK/VIA firmware. No Bluetooth, too little storage, pixelated screen. | `9dxC99HDVH0`; `CqwCjghqUu0` frames 1 to 2 | confirmed |
| V2, December 2024 to January 2025 | 3D-printed slim case, custom keycaps, new PCB that did not work, replaced by a dev kit typing over Bluetooth. Display brought up with LVGL. | `rTf2K0mlvSk`, `kTnqYrpr2v8`, `wY692-INdOE` | confirmed |
| V3, March to May 2025 | 3D-printed case, LCD, two encoders, low-profile switches, plug-in nRF dev board, battery, first wireless typing. Power-path error fixed. | `Wt_-N3kfbMI`, `Z8-k1frnIJM`, `wIC3IPEvYTs` | confirmed |
| Metal samples, June and October 2025 | Top shell first (June), then both shells from the finished "GLYF MOCK v24" Fusion design (October). | `hBXO5tvxVr8`, `LyKoZR8Q888` | confirmed |
| Integrated PCB, November to December 2025 | Board with the nRF5340 module, charger, gauge, RTC, NOR flash; firmware still to be written for it on 2025-12-30. | `kOclb0i9bug`, `S9c5WuorsgQ` | confirmed |
| Working metal units, January to March 2026 | Units with the square LCD, shown at the Founders, Inc. "Artifact" programme in San Francisco. | `Nk6MD9QS8VA`, `wLHIWHExL-k`, `Q6CKpc6AK0o` | confirmed |

The maker says there were four prototypes before the final look and that the case was redesigned three times in six months (`6XtP_ieaD8k`, `Pq1GoeAX_go`).

## 5. Price and dates

| Fact | Source | Confidence |
| --- | --- | --- |
| July 2025: planned price "about $170". | maker comment on `K_bqsGX5qdg` | confirmed |
| Pre-orders opened 2025-10-14 at 12:30 PST on the maker's own shop at USD 189 with free worldwide shipping. Kickstarter was rejected on purpose. | maker comments on `LyKoZR8Q888`, `piNJL6_wltM`, `CqwCjghqUu0` | confirmed |
| From 2025-11-21 the maker quotes USD 159 (a Black Friday deal is mentioned on 2025-11-25). Commenters still cite about USD 160 in December 2025 and January 2026. | maker comments on `uA8i7Z0LtXg`, `v9_v6v359Tw`; commenters on `Qzn6t-ihyvc`, `LHH8dsOPqco` | confirmed |
| March 2025 forecast by the maker: release "towards the end of this year" with shipping "not guaranteed until next year at the latest". | maker comment on `yAIwYPMENj4` | confirmed |
| The most common complaint in comments is the price. The second is the choice of one side display over per-key displays (top comment on `Q6CKpc6AK0o`, 75 likes). | `digest-01/comments.txt` | confirmed |

## 6. Design implications for worxpad (derived, not maker statements)

1. The reference architecture is: Nordic BLE SoC on a pre-certified module, ZMK, SPI LCD with LVGL, external SPI NOR flash for icon assets, I2C fuel gauge, I2C RTC with its own backup cell, power-path charger, slide switch, USB-C. All of it is one two-sided board with every SMD part on the bottom, which suits one-sided JLCPCB assembly.
2. The display that fits this layout is a 1.4 inch 240 x 240 panel under a 31.2 mm square cover lens about 1.1 mm thick. Total module depth is about 3 mm.
3. The 19.05 mm key pitch, a board about 112.5 mm wide and a body near 120 by 90 mm fit a 180 mm printer bed with room to spare.
4. The top shell with integrated plate needs machining from both faces. The bottom shell needs a sculpted wedge. The maker names set-up count as the cost driver, so a flat bottom with a separate bolt-on foot would be cheaper to machine.
5. The maker's five-board prototype order shows that extended parts and import duties, not the bare board, dominate small JLCPCB runs.

---

## 7. Best frames for the measurement agent

All paths are under `/home/worxbend/Projects/prota-clone/research/_cache/youtube/`. Frames are 720 x 1280 unless noted.

| Path | What it shows |
| --- | --- |
| `crops-01/sr0MIYEi678-f010-lcd-drawing-2x.png` | Supplier drawing of the 1.4 inch 240 x 240 LCD with cover lens, all dimensions readable. |
| `crops-01/ScYz1Z_T1UY-f015-kicad-dimension-2x.png` | KiCad key field with "19.05 spacing" labels and a 112.5000 mm dimension. |
| `crops-01/ScYz1Z_T1UY-f014-kicad-2x.png` | KiCad right column: USB-C, two encoders, module, FPC connector, RTC, two tactile buttons, part values. |
| `crops-01/S9c5WuorsgQ-f044-kicad-2x.png` | KiCad V4 routed right column with silkscreen "GLYF V4 2025 PROTA DESIGNS". |
| `frames-01/S9c5WuorsgQ/f023.jpg` | Bottom side of the assembled PCB: Holyiot nRF5340 module, FPC connector, coin holder, charger area, reference designators. |
| `frames-01/S9c5WuorsgQ/f020.jpg` | Bottom side, key field: 16 hot-swap sockets, diodes, mounting holes. |
| `frames-01/S9c5WuorsgQ/f021.jpg` | Top side, right column: two encoders, USB-C between them, FPC slot, two tactile buttons. |
| `frames-01/S9c5WuorsgQ/f060.jpg` | Pouch battery being plugged into the board, for battery size against key pitch. |
| `frames-01/S9c5WuorsgQ/f006.jpg` | Metal unit above the 3D-printed prototype, both face on. |
| `frames-01/kOclb0i9bug/f001.jpg` | KiCad 3D view of the whole PCB bottom side with outline and hole pattern. |
| `crops-01/kOclb0i9bug-f008-010-017-019.jpg` | JLCPCB 3D viewer: bottom side close-up and top side with encoder model. |
| `frames-01/Q6CKpc6AK0o/f059.jpg` | Finished unit held face on to the camera: best frame for the top-view proportions. |
| `frames-01/Q6CKpc6AK0o/f024.jpg` | Close-up of display window, knobs and one round button on a real unit. |
| `frames-01/Q6CKpc6AK0o/f035.jpg` | Inside face of the bare top shell with integrated plate. |
| `frames-01/Q6CKpc6AK0o/f038.jpg` | Top shell and bottom shell held together edge on, showing wall and plate thickness. |
| `frames-01/Q6CKpc6AK0o/f057.jpg` | Fusion side profile of the full assembly ("Mock Design"). |
| `frames-01/Q6CKpc6AK0o/f052.jpg` | Underside rear corner: sculpted wedge and a pill-shaped foot. |
| `frames-01/Q6CKpc6AK0o/f017.jpg` | One keycap removed: low-profile switch with cross stem; rear edge cut-outs. |
| `crops-01/Nk6MD9QS8VA-f042-043-044-047.jpg` | Rear edge with USB-C and slide switch (two angles), grey-faced unit, "265 grams" caption. Source frames are 1280 x 720. |
| `crops-01/wLHIWHExL-k-f032-034-035-036.jpg` | Unit at an angle, both bare shells side by side on a table (two angles), switch held edge on. Source frames are 1280 x 720. |
| `crops-01/LyKoZR8Q888-f012-015-019-021.jpg` | Fusion underside view, raw machined bottom shell inside, anodised bottom shell inside, bottom shell outside. |
| `crops-01/LyKoZR8Q888-f025-026-027-029.jpg` | Assembled metal prototype: low side view, end view, underside with four feet, face at an angle. |
| `crops-01/4mGhEPTLoSA-f012-018-019-020.jpg` | Fusion underside with feet, printed bottom with feet fitted, side views on a desk. |
| `crops-01/4mGhEPTLoSA-f015-foot-calipers-2x.png` | Caliper on a silicone foot reading 24.04 mm. |
| `crops-01/K_bqsGX5qdg-f008-010-018-019.jpg` | Prototype with one cap off, thickness against an MX numpad, USB-C on the rear edge, dev board overhang. |
| `frames-01/qAuaOqLKj_Q/f012.jpg` | CAD render of the keycap shape. |
| `frames-01/CqwCjghqUu0/f018.jpg` | Marketing render that shows a second unit from below behind the first. |
| `crops-01/Z8-k1frnIJM-f017-power-diagram.png` | Maker's power-switch diagram: battery, slide switch, MOSFET, nice!nano. |
| `crops-01/Kp9UA2LNt6g-f031-lcd-fpc-3x.png` | Rejected early LCD sample with glass, FPC marking ENH-TV0144006A. |
| `sheets-01/<id>.jpg` | One contact sheet per downloaded YouTube video, nine frames per row, one frame per second. |
| `sheets-03/<tiktok id>.jpg` | Contact sheets for seven TikTok-only videos. |

---

## 8. Sources read

### 8.1 Long-form videos (full description, subtitles and comments read)

| Video | Channel | Date | Views | Length | Notes |
| --- | --- | --- | --- | --- | --- |
| `8WrTUNELp2U` "NASA Interns turned Hardware Founders / Shop Talk with Autodesk Fusion" | Autodesk Fusion | 2025-10-16 | 1,674 | 42:22 | Interview with both founders. The description lists chapters and states "ZMK firmware, Bluetooth, media/time widgets; pre-orders open Oct 14". Two comments, neither technical. Transcript: `meta-02/8WrTUNELp2U.txt`. |
| `Nk6MD9QS8VA` "We Made a Device that will Replace Your Keyboard" | PROTA | 2026-01-31 | 1,226 | 0:57 | Demo of a working metal unit in Premiere Pro. Description: a general pitch for video editors with a link to the shop; no specifications. Four comments, no maker replies. |
| `wLHIWHExL-k` "We Built the Best Macro Pad in the World" | PROTA | 2026-02-12 | 12,601 | 0:55 | Shows both bare shells, keycap CAD and the configurator. Description: pre-orders open, live demo at "Artifact Festival at Founders Inc." Thirteen comments, no maker replies. |
| `PJ_84kYPAT4` "PROTA Macro-pad Animation" | supnovaco | 2025-02-21 | 94 | 0:16 | Fan-made Blender animation of the Printed Pad. No technical content. |
| `dvbwprZH9y8` "Why Every Designer & Creator Needs THIS Macropad in 2026" | Peter Georgiou | 2025-12-20 | 9,633 | 2:59 | Read and rejected: it is about a different product (Framer Creator Micro by Work Louder). |

### 8.2 Official shorts from the GLYF period (2024-10 onward)

Shorts have empty descriptions. Titles are shown without emoji. The view counts are those reported on 2026-11-13. Maker replies are collected with the question they answer in `digest-01/maker-comments-glyf-era.txt`. Pinned maker comments in this period only say "Check out the Printed Pad through the link in our bio" or explain what a macro pad is.

| Date | Video id | Title | Views | Length (s) | Subtitles | Comments read | Maker comments |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-10-11 | `MEvG5BgtNbg` | What do you guys want to see next? #smallbusiness #techtok #macropad #originstory #keyboa | 23655 | 41 | yes | 27 | 3 |
| 2024-10-21 | `9dxC99HDVH0` | What should we name it? #macropad #smallbusiness #techtok #prototype | 12784 | 41 | yes | 22 | 2 |
| 2024-11-05 | `Kp9UA2LNt6g` | Sorry to keep y'all waiting #macropad #smallbusiness #techtok #prototype | 16987 | 50 | yes | 12 | 1 |
| 2024-11-15 | `-CReF2KOL-U` | What do you want to see next? #macros #macropad #productivityhacks #techtok #techtips | 9657 | 32 | yes | 13 | 2 |
| 2024-11-21 | `pDZKl6kk-4M` | Simple yet sweet #macros #macropad  #productivityhacks #techtok #techtips #computeraccess | 31786 | 25 | yes | 16 | 1 |
| 2024-11-22 | `SMFDarLmCZg` | Don't mind the eyeroll #fusion360 #macros #macropad #productivityhacks #techtok #techtips | 19051 | 38 | yes | 14 | 1 |
| 2024-12-04 | `hFRq07rrJm4` | Who needs reindeer when you've got us? #macropad #smallbusiness #keyboard #wholesome #sh | 2594 | 43 | no | 3 | 0 |
| 2024-12-07 | `irNT4iMduPY` | Spreading Christmas joy one package at a time #christmas #macropad #handdelivered #smallbu | 2867 | 34 | yes | 3 | 0 |
| 2024-12-15 | `rTf2K0mlvSk` | Designing is our life force#macropad #smallbusiness #tech #techtok #prototype #processvid | 12325 | 40 | yes | 12 | 2 |
| 2024-12-22 | `PZ920nm7d2s` | Prototype 3 Complete #macropad #smallbusiness #tech #techtok #prototype #processvideo | 3984 | 17 | no | 10 | 1 |
| 2025-01-05 | `dlu_OGiPj2I` | The secret to saving HOURS every week is here! #productivityhacks #tech macropad #smallbus | 4935 | 48 | yes | 8 | 2 |
| 2025-01-07 | `WAhTKr1eSoI` | Speed, Customization, and Focus  #productivityhacks #tech #macropad #smallbusiness | 3772 | 38 | yes | 3 | 0 |
| 2025-01-08 | `kTnqYrpr2v8` | How do you think it took us to figure this out? #smallbusiness #tech #prototype #processv | 54301 | 46 | yes | 33 | 5 |
| 2025-01-11 | `2SQ10PToz5o` | All in a days work #dayinthelife #tech #smallbusiness #macropad #mechanicalkeyboard #tech | 124338 | 41 | yes | 46 | 5 |
| 2025-01-12 | `GAfVZWfzXnw` | If you could make anything what would it be? #pcb #tech #macropad #techtok #prototype #diy | 32565 | 44 | yes | 30 | 6 |
| 2025-01-14 | `LsfwSjNqi6Q` | Is this what you imagined the process to look like?#pcb #tech #macropad #techtok #prototy | 17071 | 51 | yes | 11 | 0 |
| 2025-01-17 | `U4XxXpSQi9M` | Ladies he's single btw#smallbusiness #macropad #tech #techtok #blogpost #behindthescenes | 23389 | 47 | yes | 12 | 0 |
| 2025-01-19 | `hEVKs306QLg` | It's all part of the process :) #prototype #macropad #mechanicalkeyboard #tech #techtok #p | 36912 | 43 | yes | 30 | 3 |
| 2025-01-22 | `BCKQ38nhzlk` | Printed Pad? #tech #macropad #techtok #smallbusiness #mechanicalkeyboard | 39464 | 38 | yes | 29 | 3 |
| 2025-01-26 | `-PEtvLqK1G0` | Gotta love 3D Printers#3dprinting #macropad #3dprint #3dprinter #tech #mechanicalkeyboard | 21643 | 41 | yes | 15 | 1 |
| 2025-01-29 | `75UdmK6n1AU` | Failing is what makes us stronger#smallbusiness #macropad #tech #progress #entrepreneur | 9211 | 51 | yes | 14 | 0 |
| 2025-01-31 | `wY692-INdOE` | I guess he likes the new macro pad :) #macropad #mechanicalkeyboard #tech #prototype #tech | 13148 | 32 | yes | 25 | 1 |
| 2025-02-02 | `gDomSar2V6E` | 3D Printing is a game changer#3dprinting #3dprinter #macropad #mechanicalkeyboard #smallb | 32456 | 23 | no | 19 | 1 |
| 2025-02-05 | `eqzRX2Y0rOg` | Did you know?#apple #tech #techtok #prototype #macropad #mechanicalkeyboard | 13141 | 29 | yes | 13 | 1 |
| 2025-02-09 | `YxNqUznpgjY` | Hello to me 1 year from today #3dmodeling #tech #circuitdesign #pcb #marketing #smallbusi | 14401 | 39 | yes | 13 | 1 |
| 2025-02-11 | `d4oJirvqhvY` | Here's the secret to packaging #smallbusiness #packaging #macropad #tech #mechanicalkeyboa | 11673 | 43 | yes | 9 | 0 |
| 2025-02-18 | `8m8pGzwhyao` | Which one's your favorite?#mechanicalkeyboard #tech #macropad #keyboard #techtok | 12662 | 34 | yes | 16 | 0 |
| 2025-02-21 | `PJ_84kYPAT4` | PROTA Macro-pad Animation | 94 | 16 | no | 2 | 1 |
| 2025-02-22 | `SVFJb6qEKMQ` | Would you buy one? #macropad #smallbusiness #tech #techtok #prototype #processvideo | 12744 | 39 | yes | 33 | 2 |
| 2025-02-24 | `Hzb1XL3zzrw` | What do you want to see next?#smallbusiness #macropad #tech #techtok #prototype #coding | 15504 | 46 | yes | 14 | 0 |
| 2025-02-26 | `wuogE5Xhh_k` | Who's down to build one#mechanicalkeyboard #smallbusiness #tech #setup #diy #techtok | 211280 | 30 | yes | 51 | 2 |
| 2025-03-01 | `qVLKbG08s8E` | What shortcuts would you put on it?#tech #macropad #techtok #smallbusiness #mechanicalkey | 16825 | 20 | yes | 15 | 3 |
| 2025-03-06 | `A3ifA8_PRJc` | What would you make? #3dmodeling #tech #circuitdesign #pcb #marketing #smallbusiness | 7983 | 45 | yes | 6 | 0 |
| 2025-03-07 | `TZLxTVbzH28` | This is not sponsored but I'm not opposed  @JLCPCB  #electronics #jlcpcb #tech #techtok # | 3343 | 36 | yes | 9 | 2 |
| 2025-03-09 | `9WgWnIbsQE8` | What would you make?#3dprinting #3dprinter #3dmodelling #tech #smallbusiness #fusion360 | 14228 | 36 | yes | 12 | 1 |
| 2025-03-13 | `bLpNX4Z4wvo` | What would you use it for? #tech #macropad #techtok #smallbusiness #mechanicalkeyboard | 25335 | 25 | yes | 19 | 1 |
| 2025-03-17 | `Pq1GoeAX_go` | What do you think?#macropad #smallbusiness #tech #techtok #prototype #processvideo | 10515 | 27 | yes | 8 | 1 |
| 2025-03-21 | `EiwzHhIsQKA` | Just start! #smallbusiness #originstory #techcompany #macropad #techtok #startup | 13670 | 55 | no | 15 | 2 |
| 2025-03-22 | `YIxPZJ1_lFs` | Don't give up.#smallbusiness #apple #techcompany #macropad #techtok #stevejobs | 4745 | 57 | yes | 5 | 0 |
| 2025-03-22 | `-nbTXRa3Whg` | Comment what you want to see next! #macros #macropad #tech #techtok #computerscience #codi | 18435 | 19 | yes | 17 | 0 |
| 2025-03-24 | `wMVHpqQajqc` | Yes each one is made by hand :)#asmr #tech #macropad #techtok #smallbusiness #mechanicalke | 7946 | 46 | no | 11 | 0 |
| 2025-03-26 | `yAIwYPMENj4` | Yes each one is packed by hand :)#asmr #tech #macropad #techtok #smallbusiness #mechanical | 9600 | 33 | no | 15 | 2 |
| 2025-03-29 | `YDbXE55F5L4` | Comment what you want to see next! #macros #macropad #tech #techtok #pcb #pcbdesign #elect | 12469 | 22 | yes | 5 | 0 |
| 2025-03-29 | `Q0jl11n2_AY` | Hit subscribe to see the full video #technology #techtok #relatable #macropad #prototype | 15615 | 10 | no | 13 | 2 |
| 2025-03-31 | `Wt_-N3kfbMI` | It's finally wireless#macropad #smallbusiness #tech #techtok #prototype #processvideo | 18507 | 37 | yes | 28 | 10 |
| 2025-04-02 | `LWd2-QYQFss` | What would you want as a widget?#macropad #smallbusiness #tech #techtok #prototype #proce | 19414 | 24 | yes | 21 | 2 |
| 2025-04-05 | `L4MqWy5PSd0` | This is a macro pad#smallbusiness #originstory #techcompany #macropad #techtok #startup | 36542 | 30 | yes | 16 | 3 |
| 2025-04-10 | `ugj16Tmrbyc` | It's possible #smallbusiness #originstory #techcompany #macropad #techtok #startup | 27345 | 46 | no | 22 | 5 |
| 2025-04-14 | `Z8-k1frnIJM` | Oops#macropad #smallbusiness #tech #techtok #prototype #processvideo | 5099 | 39 | yes | 4 | 0 |
| 2025-04-25 | `leZ12XkvpGw` | This is a macro pad #tech #mechanicalkeyboard #techcompany #macropad #techtok #startup | 117087 | 24 | yes | 17 | 0 |
| 2025-05-05 | `ScYz1Z_T1UY` | PCB Prototype Testing #pcbdesign #engineering #electronics #engineeringstudent | 104672 | 35 | yes | 40 | 6 |
| 2025-05-07 | `rpSo1C1WWrg` | Link in bio #tech #macropad #techtok #smallbusiness #mechanicalkeyboard | 57410 | 42 | yes | 21 | 1 |
| 2025-05-10 | `-cXreOmXRGo` | No More Dirty Floors #engineer #solidworks #mechanicaldesign #gym #engineering #3dprintin | 21411 | 24 | yes | 4 | 0 |
| 2025-05-12 | `wIC3IPEvYTs` | Prototype complete #electronics #mechanicalkeyboard #engineering #engineeringstudent #tec | 29319 | 11 | no | 17 | 4 |
| 2025-05-13 | `C9qxMbhROOI` | technologia #tech #macropad #techtok #smallbusiness #mechanicalkeyboard | 38507 | 10 | no | 7 | 0 |
| 2025-06-24 | `hBXO5tvxVr8` | I can't wait for the final! #macropad #smallbusiness #tech #productdesigner #cncmachining | 165387 | 34 | yes | 40 | 5 |
| 2025-06-25 | `4mGhEPTLoSA` | One step closer#macropad #smallbusiness #tech #productdesign #prototype #productdesigner | 26390 | 26 | yes | 10 | 1 |
| 2025-06-27 | `7yenLU0Odwo` | Thankful for everything that happened#college #computerscience #tech #smallbusiness #busi | 13683 | 58 | yes | 7 | 0 |
| 2025-07-01 | `K_bqsGX5qdg` | Where would you go?#macropad #smallbusiness #tech #productdesign #prototype #mechanicalke | 36439 | 33 | yes | 23 | 4 |
| 2025-07-04 | `VipX8ReasHc` | This resin 3D is so nice#3dprinting #resin3d #elegoo #saturn4ultra16k #tech @ElegooOffici | 12702 | 27 | yes | 7 | 1 |
| 2025-07-10 | `-wnISw4TIIk` | Prototypes coming soon #3dprinting #resin3d#elegoo #saturn4ultra16k #tech @ElegooOfficial | 16516 | 19 | no | 7 | 0 |
| 2025-07-19 | `qAuaOqLKj_Q` | We are so close to launching#3dprinting #resin3d #elegoo #saturn4ultra16k #prototype #tec | 90896 | 35 | yes | 62 | 17 |
| 2025-10-04 | `Lgr_0N7SrDY` | Your move @elgato  #macropad #streamdeck #mechanicalkeyboard #apple #edits | 11450 | 13 | yes | 13 | 4 |
| 2025-10-09 | `LyKoZR8Q888` | Available for Pre-Order Oct. 14th #macropad #mechanicalkeyboard #prototype #tech #cncmach | 14004 | 35 | yes | 14 | 2 |
| 2025-10-09 | `n7dKidp2OQE` | Chat did we cook? #macropad #apple #tech #mechanicalkeyboard #blender3d | 8073 | 18 | no | 15 | 4 |
| 2025-10-11 | `CqwCjghqUu0` | 2 years of development in one video #macropad #mechanicalkeyboard #tech #techtok #proto | 185941 | 20 | yes | 71 | 11 |
| 2025-10-14 | `6XtP_ieaD8k` | 2 Years and we Launch Tommorow #macropad #mechanicalkeyboard #prototype #tech #smallbusine | 13815 | 28 | yes | 15 | 5 |
| 2025-10-17 | `_7-Ndv3M_C4` | You're at the heart of our story | 13650 | 24 | no | 12 | 0 |
| 2025-10-21 | `piNJL6_wltM` | iPhone and sodacan approved #macropad #smallbusiness #tech #productdesigner #cncmachining | 34414 | 42 | yes | 24 | 2 |
| 2025-11-13 | `sr0MIYEi678` | $501 JUST TO MAKE 5 PIECES#macropad #mechanicalkeyboard #prototype #tech #techtok #manufa | 15473 | 28 | yes | 14 | 3 |
| 2025-11-14 | `kOclb0i9bug` | The more you know#macropad #pcbdesign #prototype #tech #techtok #pcb | 53410 | 45 | yes | 23 | 3 |
| 2025-11-18 | `j2515IN0vLo` | Hello me 2 years agoGet Autodesk Fusion #3dmodeling #tech #3dprinting #macropad #autodesk | 63405 | 46 | yes | 18 | 2 |
| 2025-11-21 | `uA8i7Z0LtXg` | Your wish is our command #macropad #techtok #electronics #mechanicalkeyboard #tech | 21715 | 12 | no | 24 | 8 |
| 2025-11-23 | `77L_fMnvAtk` | It's been an amazing journey so far #macropad #originstory #smallbusiness #startup #3dpri | 12274 | 49 | no | 11 | 0 |
| 2025-11-25 | `v9_v6v359Tw` | He's building our customization software #startup #engineering #tech  #softwareengineering | 60203 | 50 | yes | 35 | 4 |
| 2025-11-30 | `kCYgEIreAjg` | Forgot to mention it also has Bluetooth#foryou #macropad #elgato #tech #desksetup | 8103 | 11 | yes | 9 | 1 |
| 2025-12-04 | `Qzn6t-ihyvc` | I'll wait #macropad #techtok #mechanicalkeyboard #electronics #tech | 18554 | 16 | no | 27 | 4 |
| 2025-12-20 | `dvbwprZH9y8` | Why Every Designer & Creator Needs THIS Macropad in 2026 | 9633 | 179 | yes | 7 | 0 |
| 2025-12-30 | `lYW8Di9Q9So` | Meet Glyf: The device for creative and enterprise software to speed up digital workflows | 9616 | 6 | no | 0 | 0 |
| 2025-12-30 | `S9c5WuorsgQ` | Explaining how our newest pcb works #engineering #diy #tech #pcb #pcbdesign #prototype #ma | 33498 | 69 | yes | 9 | 1 |
| 2025-12-31 | `LHH8dsOPqco` | Want to know what it is? Check the link in our bio#tech #diy #prototype #asmr #macropad # | 12385 | 33 | no | 9 | 0 |
| 2026-01-05 | `MRxn-_TBt60` | Maybe not? #macropad #techtok #desksetup #streamdeck #tech | 14788 | 12 | yes | 29 | 8 |
| 2026-01-14 | `fSOHsMyMF1w` | We've got a lot of work ahead of us @fdotinc #foundersinc #startup #sanfrancisco #macropa | 13661 | 72 | yes | 7 | 2 |
| 2026-01-31 | `Nk6MD9QS8VA` | We Made a Device that will Replace Your Keyboard | 1226 | 57 | yes | 4 | 0 |
| 2026-02-12 | `wLHIWHExL-k` | We Built the Best Macro Pad in the World | 12601 | 55 | yes | 13 | 0 |
| 2026-03-05 | `Q6CKpc6AK0o` | Why these stream deck sounds so mushy #macropad #techtok #desksetup #streamdeck | 23309 | 59 | yes | 20 | 0 |

Older official videos read for context (66, all about keycap trays or the Printed Pad): `Fot8VzsgpQE`, `jqs5ICIaEHs`, `gM12Hj_y_ho`, `zQPC6Usu-eg`, `TktuD66eF-E`, `VKLLEFus3q4`, `lGJI6ThC_mA`, `jTnEIk54t8s`, `4exuQcAxxgM`, `SUEj78B8pM0`, `RdZGecWwNS0`, `5LpQBljoaY4`, `SkIvPcOhu9M`, `6maZrypmO7w`, `CTGYPcJQd9s`, `yx5NvDaqgX0`, `UbVkEtM2RxE`, `zmJvN4MvpzU`, `C_zwTXrcyEs`, `frKLLsDPFLo`, `-2W205U2IFs`, `z4Y5nFAHhig`, `jRfcfe_5I6o`, `1AxL2tSuE0w`, `qD3ZFAeTQ0I`, `rOcAmSUfcmA`, `e0h61Rklc_c`, `2V2j_wKRThg`, `QAoHt4obquE`, `Zqk4xhsj_Q0`, `aONQzL2isYE`, `ZPYCEvThUvA`, `ns9COOb-rIA`, `Q-2ZDkiC3sc`, `uImxk7PgNjU`, `eZv_OupLQkw`, `A0KCd4ABZzU`, `Q2tTNwO3_N0`, `AJ-kcK8Ldv8`, `6EGI4ZDqFqQ`, `0dSNXTyx3fQ`, `BkEGsrLkysY`, `qWUUs5PFe6g`, `pX0UHUrg1Is`, `0lPS5qmvaFw`, `1AG8Ugvqt-w`, `MDaeB28T_UE`, `3w1c4LM5u14`, `9k8XE6kn_GU`, `i42QIi-8eSA`, `iSp6BYpL3ss`, `7VAhNaNBCPk`, `dfxIYt_UTjU`, `nwt3pCxAG5U`, `r_yeIR0z4QI`, `OFY80bI6IIw`, `VVzorrFCozg`, `PhT-Yvm8JK4`, `JzehcfFaTVE`, `kMZ-0xxp3R0`, `hSpxZs5k-r8`, `uN9ZiunZy_U`, `ENDWKx692B0`, `jyPOA5Vsb60`, `vLeyDckQK9I`, `pytmxV8KJAE`.

### 8.3 TikTok

The full post list with dates, view counts and captions is in `social-01/tiktok-protadesigns.jsonl` (201 posts, 2023-05-01 to 2026-03-14). Seven posts that have no YouTube copy were downloaded and viewed:

| TikTok id | Date | Caption | Content |
| --- | --- | --- | --- |
| `7617023441199287582` | 2026-03-14 | "Just a fraction of its power btw" | Finished unit driving Premiere Pro: zoom, volume, copy and paste, play, undo and redo, link clips. |
| `7602395637484752159` | 2026-02-02 | "Good design can go a long way" | Prototype one, prototype two and the metal unit in sequence. |
| `7591818241400507679` | 2026-01-05 | "damn..." | Reply to a "$159" price complaint using the launch renders. |
| `7557263230071033118` | 2025-10-04 | "Follow for more updates!" | Two-minute firmware talk: normal widgets, system widgets, system layers. |
| `7557776173275598110` | 2025-10-05 | "Follow for more content like this" | States 6061 aluminium. |
| `7468152834417085727` | 2025-02-06 | "Would you get this macro pad?" | Printed Pad only. |
| `7462955956545047838` | 2025-01-23 | "Prototype vs Product" | Printed Pad only. |

Six TikTok posts dated 2025-11-12 are clips of the Autodesk interview and add nothing to the full video.

### 8.4 Other

- LCSC product data for part numbers C107410 (DS3231MZ+TRL, SOIC-8) and C11702 (1 kOhm 0402 resistor), both read from the JLCPCB order frame `kOclb0i9bug/f008`. Queried at `https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=C107410`.
- The two owner screenshots in `research/_cache/user/` were viewed for comparison with the video frames.

### 8.5 Cache layout

| Directory | Content |
| --- | --- |
| `search-01` to `search-04` | Raw yt-dlp search results (JSON lines), 38 queries. |
| `channel-01` | Channel tab listings. |
| `meta-01`, `meta-02` | Per-video info JSON with comments, and VTT subtitles, for 152 + 1 videos. |
| `digest-01` | `videos.txt` (all subtitles by date), `comments.txt` (all comments), `maker-comments-glyf-era.txt`. |
| `video-01`, `video-02`, `video-03` | Downloaded video files: 46 YouTube videos at 720p, the interview at 480p, 7 TikTok videos. |
| `frames-01`, `frames-03`, `frames-04` | Extracted frames: one per second for shorts, selected timestamps for the interview. |
| `sheets-01`, `sheets-03` | Contact sheets. |
| `crops-01` | Enlarged crops and small montages of the most informative frames. |
| `social-01` | TikTok account listing and probe results for Instagram and Vimeo. |

## 9. What could not be reached or was not done

- Instagram: `yt-dlp` cannot list the account `protadesigns` without a login ("Unable to extract data"). Instagram Reels were not read. They are probably the same clips as TikTok.
- Vimeo: the search page returns HTTP 403 to `yt-dlp`. No Vimeo source was found by other means.
- TikTok comments: `yt-dlp` does not fetch TikTok comments. Only captions, subtitles and video frames were read for TikTok.
- YouTube subtitles: ten videos hit HTTP 429 on the first pass and were fetched again one at a time. All 152 videos now have metadata. Videos without speech have no subtitles.
- Comments were capped at 300 per video. Only `hSpxZs5k-r8` (5.3 million views, a Printed Pad origin story) reached the cap.
- Forty-six of about ninety GLYF-period shorts were downloaded for frames. The rest are talking-head, motivational or Printed Pad clips according to their subtitles. They were not viewed frame by frame.
- Video was limited to 720p as instructed. Small silkscreen text and part markings are at the limit of legibility. A 1080p pull of `S9c5WuorsgQ`, `ScYz1Z_T1UY` and `kOclb0i9bug` would let more part values be read.
- The interview frames (480p) show the prototypes on the table too small to add detail.
- The maker's blog posts (on the shop site under "updates" or "support"), the Discord server and the Reddit thread where the maker posted the schematic were not read. They are outside the video scope and are listed as leads.
- Not found in any video source: battery capacity, battery life, Bluetooth version, display controller part, NOR flash part and size, charger part, exact switch model, exact outer dimensions, PCB layer count, any 2.4 GHz dongle, any dock.
