# Social and portfolio channels of Prota Designs: research notes

Date of research: 2026-11-13. Agent key: `social`.

Scope: public accounts of Prota Designs and its two founders, mined for facts about the GLYF macropad.
Nothing from the vendor (images, video, firmware, software, CAD) is copied into the repository. All downloads
are under `research/_cache/social/` (gitignored). Measurements below were read from the vendor's own
published screenshots and video frames.

Confidence scale: **confirmed** (stated by the maker or read directly from a primary source),
**likely** (consistent indirect evidence), **guess**.

Source shorthand used below:

- BLOG-01 … BLOG-06: the six "Update NN - Glyf Development" posts at `https://protadesigns.com/blogs/updates`
  (feed: `https://protadesigns.com/blogs/updates.atom`).
- TT-<date>: a TikTok post of `@protadesigns`, URL `https://www.tiktok.com/@protadesigns/video/<id>`;
  the id is given at first use. Speech was transcribed locally from the audio track.
- X-<id>: a post of `@ben_baybay`, URL `https://twitter.com/ben_baybay/status/<id>`.
- YT-<id>: a video of `https://www.youtube.com/@PROTADESIGNS`.

---

## 1. Accounts found

| Platform | Account | Status | Source | Confidence |
| --- | --- | --- | --- | --- |
| Instagram | `https://www.instagram.com/protadesigns/` (display name "PROTA") | Exists. Profile listing blocked (login wall). Three reels readable through yt-dlp. A screenshot inside TT-2025-10-08 shows 222 posts and 31.3K followers. | site footer; TT-2025-10-08 | confirmed |
| TikTok | `https://www.tiktok.com/@protadesigns` (display name "PROTA") | Fully listed: 201 posts, 2023-05-01 to 2026-03-14. No post after 2026-03-14. | site footer; yt-dlp listing | confirmed |
| YouTube | `https://www.youtube.com/@PROTADESIGNS` | 2 long videos, 148 shorts. Shorts mirror the TikTok posts. | site footer; yt-dlp listing | confirmed |
| X | `https://x.com/prota_designs` (company) | Exists. Timeline not readable without login (embed timeline returned zero entries). | site footer | confirmed |
| X | `https://x.com/ben_baybay` (founder) | Four posts readable through the public embed endpoint because the blog embeds them. | BLOG-05 | confirmed |
| Discord | `https://discord.gg/nSYUuAXxWp`, server "Prota Designs" | 393 members, 34 online on 2026-11-13. Server created 2023-06-10 (decoded from the server id). Invite created by user "Ben \| Prota Designs". Channel content needs a logged-in member. | Discord public invite API | confirmed |
| LinkedIn (company) | `https://www.linkedin.com/company/prota-designs` | "Macropads and more". 21 followers. Type: Partnership. Founded 2022. 2 employees listed. | public company page | confirmed |
| LinkedIn (people) | `https://www.linkedin.com/in/benbaybay`, `https://www.linkedin.com/in/noah-beidelman` | Exist. Blocked (HTTP 999). | company page links | confirmed (existence only) |
| Founders, Inc. | `https://f.inc/artifact/teams/prota-designs` | Team page: "A device to automate your most used shortcuts", booth number 52. | page fetch | confirmed |
| Threads, Facebook, Pinterest | handle `protadesigns` | Pages return only a script shell. Existence not determined. | direct probe | not found |
| Behance, Dribbble, Mastodon (mastodon.social), Linktree | handle `protadesigns` | HTTP 404. No account under that handle. | direct probe | confirmed (absent) |
| Bluesky | search for `protadesigns` | Zero actors returned by the public search API. | `public.api.bsky.app` | confirmed (absent) |
| ArtStation, Telegram | handle `protadesigns` | Generic landing pages, no profile data. | direct probe | not found |
| GitHub | `protadesigns`, `prota-designs`, `ProtaDesigns` | No such users. No public repository matches "glyf zmk". The firmware and the companion application are not published. | GitHub REST API | confirmed (absent) |
| Kickstarter | Printed Pad campaign (2023) | Mentioned by the maker. Kickstarter search returned HTTP 403. Campaign page not located. | TT-2023-08-06 caption | likely |

A YouTube channel named "ben designs" (`UCXYQapus0q4dBuV-6XKNGug`) appeared in search results. It publishes
graphics-software tutorials and is unrelated. It is a false lead.

---

## 2. People and company (public professional information only)

- **Company.** Prota Designs, "a California based tech company" (About page). Terms of Service are governed by
  California law. Contact address is `business@protadesigns.com`. Source: `https://protadesigns.com/pages/about-us`,
  `https://protadesigns.com/pages/terms-of-services`. Confidence: confirmed.
- **Legal entity.** A search-engine summary of `https://www.bizprofile.net/ca/sacramento/prota-designs-llc` states
  "Prota Designs LLC", Sacramento, California, incorporated 2024-09-03. The page itself returned HTTP 403, so this is
  second-hand. Confidence: likely.
- **Founders.** Ben Baybay (CEO; hardware, industrial design, video) and Noah Beidelman (CTO; firmware and companion
  software). The Founders, Inc. team page lists the full names "Ben Isaiah Cabato Baybay" and "Noah Brian Beidelman".
  Sources: About page; `https://f.inc/artifact/teams/prota-designs`; blog bylines. Confidence: confirmed.
- **Background.** The two met as "partners in a NASA internship leading a team of other engineers". They state that
  they are largely self-taught and that the company is self-funded with no investors. Source: About page.
  Confidence: confirmed (maker statement).
- **Team size.** Two people. Ben does the hardware and the case; Noah writes the firmware and the companion
  software alone ("Because I develop on my own", BLOG-05). Source: LinkedIn company page (2 employees); BLOG-05;
  TT-2025-11-25. Confidence: confirmed.
- **Accelerator.** The company worked from the Founders, Inc. campus in San Francisco for about five to six weeks
  from January 2026 in a programme called Artifact ("competing against 100 startups for $250,000 in funding",
  "200 founders for five weeks"). Sources: BLOG-05; TT-2026-01-14 (id 7595128314910592269). Confidence: confirmed.
- **Earlier products.**
  - 2023-05 to 2023-06: 3D-printed artisan keycap display trays ("Froggy-15 Tray"). Source: TikTok captions
    2023-05-01 to 2023-06-09. Confidence: confirmed.
  - 2023-08: "Printed Pad", a 3D-printed 3 x 3 macropad with one knob and an OLED, hot-swap MX switches, QMK and VIA.
    Launched on Kickstarter in August 2023 ("Launching Monday on Kickstarter", caption of 2023-08-06). Sold at
    USD 47 (regular USD 59) on the store. Each unit is assembled and packed by hand. Sources: TikTok captions;
    `https://protadesigns.com/products/printed-pad.json`; BLOG-01. Confidence: confirmed.
- **Sponsor relations.** Autodesk (Fusion; a "Shop Talk" podcast appearance, clips posted 2025-11-12) and Elegoo
  (a Saturn 4 Ultra 16K resin printer supplied to them, July 2025). Source: TikTok captions. Confidence: confirmed.

---

## 3. Development timeline of the GLYF

| Date | Event | Source | Confidence |
| --- | --- | --- | --- |
| 2024-04 (photo date) | Prototype 1: a wired board built on the Printed Pad hardware (STM32, QMK, VIA). 4 x 4 MX hot-swap keys, two encoders, a small SPI LCD on a red breakout, two tactile buttons "to control the screen". | BLOG-01, images `frontpcb`, `back_pcb` | confirmed |
| 2024-07 (photo date) | Prototype 2 PCB: first Bluetooth board. Bare Nordic nRF52 QFN with chip antenna. Bootloader flashed with a Blue Pill running Black Magic Probe. | BLOG-01 | confirmed |
| 2024-10-21 | First public teaser, "What should we name it?" | Instagram reel `DBYO7BoRKXv`; TT id 7428138707431017770 | confirmed |
| 2024-12-22 | "Prototype 3 complete": resin-printed low-profile keycaps on a printed case. | Instagram reel `DD5iov1yJnn`; BLOG-03 | confirmed |
| 2024-12-28 | BLOG-01: switch from QMK to ZMK announced. | BLOG-01 | confirmed |
| 2025-01-15 | BLOG-02: display driver tests on Blue Pill, Black Pill, then nRF52840 DK; LVGL 9; ZMK running on the DK. | BLOG-02 | confirmed |
| 2025-02-22 | Case redesigned "so it can be machined out of aluminum"; PCB gains Bluetooth, "a better charging system, and a built-in clock". | TT id 7474043910512184606 | confirmed |
| 2025-03-15 | BLOG-03: 240 x 240 LCD chosen over 120 x 120; move from MX to Kailh low-profile switches; custom keycaps. | BLOG-03 | confirmed |
| 2025-03-31 | First working wireless prototype soldered. | TT id 7487872979808865567 | confirmed |
| 2025-04-14 | Power fault on that board: a resistor in series with the battery at a MOSFET source pin gave 0.9 V instead of 3.3 V. | TT id 7493093082271862047 | confirmed |
| 2025-05-05 | New schematic verified on perfboard with breakout boards for small parts before ordering. | TT id 7500815296337415454 | confirmed |
| 2025-06-24 | First CNC aluminium samples arrive (machined, bead-blasted, anodised black). | TT id 7519406476465589535 | confirmed |
| 2025-06-25 | Custom silicone rubber feet designed and made; bottom shell goes to CNC next. | TT id 7519701128913685790 | confirmed |
| 2025-07-19 | Keycaps iterated on a resin printer; "the next step would be to injection mold these". | TT id 7528656908438277407 | confirmed |
| 2025-10-08 | Second set of metal samples ("two weeks ago I sent our finished design"). | TT id 7558905725280406798 | confirmed |
| 2025-10-14 | Pre-orders open on the store at 12:30 PST. USD 159 (regular USD 189). | TT id 7560951437434293535; `products/glyf.json` | confirmed |
| 2025-11-01 | BLOG-04: widget system, UI router, file system on external flash. | BLOG-04 | confirmed |
| 2025-11-13/14 | New PCB revision ordered: 5 assembled boards, USD 503.88 landed. Display samples with bonded glass: USD 210. | TT ids 7572019519800003870, 7572377900821777694 | confirmed |
| 2025-12-30 | That PCB arrives. Walk-through video shows the nRF5340 module, NOR flash, coin cell, charger. | TT id 7589532575031381279 | confirmed |
| 2026-01 to 2026-02 | Artifact residency at Founders, Inc. Launch video 2026-01-30. Icon upload (02-03) and runtime macro recording (02-06) shown working. | BLOG-05; X-2017126263744581642, X-2018810453137445308, X-2019883069185065242 | confirmed |
| 2026-03-09 | BLOG-05: "Final production hardware is complete". Beta test applications open. | BLOG-05 | confirmed |
| 2026-03-14 | Last TikTok post. No later post on TikTok or YouTube. | yt-dlp listings | confirmed |
| 2026-10-09 | BLOG-06: beta testing done; working with manufacturers on "PCBs", "CNC machined aluminum cases" and "tempered glass displays"; "still have our sights set on shipping Glyf in Q4". | BLOG-06 | confirmed |
| 2026-11-13 | Store still reads "Shipping Early Q4 2026" and pre-order. Waitlist page shows 2,031 people. No customer unboxing, review or teardown found on any channel searched. | `https://protadesigns.com/pages/glyf-waitlist`; searches | confirmed (for the channels reached) |

---

## 4. Electronics

### 4.1 Microcontroller and radio

- The final design uses "an nRF53 series module" instead of "a generic MCU board". Source: BLOG-05.
  Confidence: confirmed.
- The module on the December 2025 PCB is a **Holyiot nRF5340 module**. The shield can reads: "holyiot",
  "Chip: nRF5340", "FCC ID: 2ALGY21069", "Model: HOLYIOT-21069". Silkscreen beside it reads "HOLYIOT-21069-nRF5340".
  Reference designator U1. The module has castellated pads on three sides and its antenna end overhangs a board edge
  zone. Source: TT-2025-12-30 frames (`_cache/social/tiktok-frames-01/pcb_03_crop.jpg`). Confidence: confirmed.
- JLCPCB did not place the module. The board arrived with U1 empty and the maker soldered it by hot air
  ("ordering it partially assembled and then soldering some parts on"). Source: TT-2025-12-30. Confidence: confirmed.
- Maker reply on why not ESP32: "we use nrf. Esp would consume too much power and is not great for a product like
  this." Source: YouTube comment on YT-CqwCjghqUu0. Confidence: confirmed.
- History. Prototype 1: STM32 in LQFP (same MCU family as the Printed Pad), too little flash and RAM for LVGL.
  Prototype 2: bare nRF52 QFN; the bootloader file in the maker's terminal photo is
  `feather_nrf52833_express_bootloader-0.9.1_s140_7.3.0.hex`, so the chip was most probably an nRF52833.
  Development kit: nRF52840 DK. Prototypes of autumn 2025 carry a Pro-Micro-format nRF52840 board (silkscreen "nano")
  hanging off the side of the case. Sources: BLOG-01 image `20240705_172608`; BLOG-02; TT-2025-11-13 frames.
  Confidence: confirmed for the sequence, likely for "nRF52833".

### 4.2 Parts seen on the December 2025 board (bottom side, reference designators from silkscreen)

Source for this whole subsection: TT-2025-12-30 frames, 1080p. Confidence: confirmed for what is visible,
as marked for identifications.

- U1: nRF5340 module (above).
- U8: SOIC-8 next to the module. Maker: "NOR flash to store macro icons and larger images". Part number not
  readable. Confidence: confirmed (function), not found (part number).
- U2: small QFN with an inductor L1 beside it. Maker points at it for "This charging IC safely charges our battery
  and automatically manages power between the battery and an external power source", that is a charger with power
  path. Part number not readable. Confidence: likely (identification of U2), confirmed (function exists).
- A fuel gauge exists: "Extra chip communicating via i2c and connected to the battery" reads the state of charge.
  Source: maker reply on YT-CqwCjghqUu0. Candidate footprint: U3 (small DFN beside the battery connector).
  Confidence: confirmed (function), guess (which footprint).
- Real-time clock with backup cell: a through-hole coin-cell holder and the maker's words "a coin cell battery to
  continuously power the RTC components". The overlay names a **Panasonic ML1220** (rechargeable 3 V lithium).
  Confidence: confirmed.
- Battery connector: white 2-pin side-entry wire-to-board connector (JST style) beside U2. Pitch not readable.
  Confidence: confirmed (2-pin connector), not found (series).
- J2: FPC connector for the display on the bottom side, next to an oblong slot milled through the PCB. The display
  tail passes from the top side through the slot. The display drawing (section 5) specifies 20 pins at 0.5 mm.
  Confidence: confirmed.
- J3: 2 x 3 pad array near the board edge. Maker: "exposed points to flash the PCB later on" (SWD).
  Confidence: confirmed (function).
- SW1: SMD tactile switch. Maker: "a reset button". Confidence: confirmed.
- Slide switch at the rear edge near USB-C, side-actuated, with MOSFET Q1 next to it (power on/off).
  BLOG-01 lists "an on and off switch" among the Bluetooth additions. Confidence: confirmed.
- USB-C receptacle, mid-mount in a board-edge notch, centred between the two encoders at the rear edge.
  Resistors R14 and R15 beside it (CC pull-downs by position). Fuse F1 and a 6-pin SOT device U5 follow
  (ESD or protection by position). Confidence: confirmed (connector and position), guess (U5 function).
- U6 and U7: one SOIC-8 and one TSSOP near the reset button. BLOG-01 lists "a GPIO expander" and "memory" among the
  parts added for Bluetooth, and prototype 2 carried a TSSOP expander (U4 there). Confidence: likely (one of them is
  the GPIO expander), not found (part numbers).
- Diodes: one SOD-123-size diode per key (D1 to D16) plus D17 to D22 near the encoders and the lower edge, and
  D23, D24 near the USB input. The keys are in a diode matrix. Confidence: confirmed (per-key diodes),
  guess (role of D17 to D24).
- Hot-swap sockets for all 16 keys on the bottom side. Each key position has one large centre hole, one smaller
  offset peg hole and two contact holes. Confidence: confirmed.
- Encoders: two through-hole rotary encoders with push switch, metal body on a green base, references SW2 and SW4,
  at the rear edge on the top side. BLOG-03 names "Alps Alpine rotary encoders" for the March 2025 prototype.
  Confidence: confirmed (Alps Alpine in March 2025), likely (same family on the December 2025 board).
- The top side of the display area carries no components. Confidence: confirmed.
- Type of the two lower round buttons on the final board (tactile switch or key switch): not found.
  Prototype 1 used two 6 mm tactile switches there. BLOG-04 calls one of them the "widget-cycle button".

### 4.3 Battery

- Wired and battery operation with one LiPo on a 2-pin connector. Capacity and cell size are not stated anywhere.
  Not found.
- The video overlays a stock picture of a "UFX 653450 1200mAh" pouch cell while describing the battery connector.
  It is an illustration, not a statement of the fitted cell. Confidence: guess (as a hint of size class).
- Prototype 2 lessons (BLOG-01): the battery management "handles power coming in from the USB-C to charge the
  battery, the temperature of the battery, and the power supply coming out of the battery". Confidence: confirmed.

### 4.4 PCB manufacture and cost (maker's own order)

Source: TT-2025-11-14 (id 7572377900821777694), screen recordings of the order page. The maker confirms in a comment
"We ordered them assembled" in reply to a question about JLC prices; the fee names match JLCPCB's order form.
An earlier post tags `@JLCPCB` (2025-03-07). Confidence: confirmed (costs), likely (vendor is JLCPCB).

- Quantity 5. Bare boards USD 73.92: engineering fee 24.00, colour 7.60 (black solder mask), board 5.10,
  material type 3.38, minimum via hole size/diameter 16.50, 4-wire Kelvin test 16.34, confirm production file 1.00.
- Assembly USD 210.74: setup 50.00, stencil 15.78, components 58.74, extended components fee 54.00 (18 extended
  part types at 3.00), SMT assembly 3.22, hand-soldering labour 3.50, manual assembly 1.10, assembly fixture 15.71,
  packaging 0.47, advanced options 7.86, confirm parts placement 0.43.
- Merchandise total 284.66, shipping 55.82, customs duties and taxes 151.67, discount -15.00, PayPal fee 2.39,
  sales tax 24.34. Order total USD 503.88.
- Parts-list rows visible: `C107410` on an SOIC-8 footprint, `C11702` on 0402 footprints, bottom side.
- The delivered panel has break-off rails with tooling holes on the two short edges.
- The design tool is KiCad (BLOG-01 screenshots; footprint names such as `MX-NoLED`, `RotaryEncoder_Switch`,
  `MountingHole_Pad`). Confidence: confirmed.

---

## 5. Display

- Resolution history: 120 x 120 first (flex marked `ENH-TV0144006A`), rejected as too coarse for text and icons.
  Then 240 x 240. Source: BLOG-03. Confidence: confirmed.
- The 240 x 240 sample flex is marked `FPC-TFT014H030-A0`. Source: BLOG-03 image `P2P_4_LCD0`. Confidence: confirmed.
- **Module drawing shown on screen by the maker** (TT-2025-11-13, id 7572019519800003870, "210 dollars on a high
  resolution screen with tempered glass attached"). Read from 1080p frames
  (`_cache/social/tiktok-frames-hd-01/lcd_q_left_bottom.jpg`, `lcd_q_right.jpg`, `lcd_left.jpg`).
  Confidence: confirmed (the drawing), likely (that this is the production display; BLOG-05 says the final screens
  have "a tempered glass layer over the display").
  - Title text: `1.4"`, `240 x RGB x 240`, `ALL O' clock` (all viewing directions, that is IPS class).
  - Cover lens: 31.20 +/- 0.1 mm wide, 31.20 +/- 0.1 mm high, four corners R2.00, thickness 1.100 mm.
  - Backlight outline: 28.00 +/- 0.15 mm wide, 31.35 +/- 0.15 mm high.
  - LCD glass: 27.20 mm wide, 29.93 mm high.
  - Viewing area: 25.80 x 25.80 mm. Active area: 25.20 x 25.20 mm.
  - Offsets from the lens edge at the top and sides: 1.60 mm to backlight, 2.00 mm to LCD glass, 2.70 mm to viewing
    area, 3.00 mm to active area.
  - Stack: total thickness 2.950 +/- 0.15 mm = lens 1.100 + OCA 0.200 + LCM 1.65 +/- 0.15.
  - Flex tail: 20 contacts, 0.50 mm pitch, 0.30 mm pad width, contact strip 10.50 mm wide, 3.50 mm contact length,
    5.00 mm stiffener, 0.30 mm thick at the stiffener, tail length 17.30 +/- 0.5 mm below the module, left edge of
    the tail 8.75 mm from the module's left edge.
  - Notes on the drawing: black single-sided tape 0.05 mm on the non-reflective back face; 3M adhesive 0.15 mm in
    two strips on the lens overhang (for bonding the lens to the case); pull tabs for the liner.
- The display window on the machined top shell is close to square with rounded corners, which matches the square
  31.2 mm lens. The earlier assumption of a portrait panel is not supported by this drawing. Source: frames of
  TT-2026-03-05 (id 7613670866001415454). Confidence: likely.
- Controller IC: not stated. Early tests used an ST7735 driver on the 120 x 120 panel. BLOG-02 mentions Zephyr's
  move of display drivers to MIPI-DBI, which applies to the ST77xx family. Confidence: not found (240 x 240
  controller), guess (ST7789-class).
- Interface: SPI (BLOG-01: "the new LCD uses SPI"). Confidence: confirmed.
- Supplier: sourced through Alibaba (BLOG-03 embeds an image hosted on `clouddisk.alibaba.com`). Supplier name:
  not found. Confidence: likely (channel).
- One of the first two samples was faulty and the supplier's specification sheet was wrong, which cost weeks.
  Source: TT id 7457456843980393759. Confidence: confirmed.

---

## 6. Switches, keycaps, knobs, buttons

- Switches: "Kailh low-profile switches", "Fully made of POM, available in clicky, tactile, and linear options".
  The post contrasts them with Choc switches ("Choc switches walked so that Kailh low-profile switches could run").
  The three product images in BLOG-03 show a square low-profile housing with the "kailh" mark, a round stem with an
  MX-type cross, two contact pins and a large centre post. Source: BLOG-03. Confidence: confirmed.
- Identification: the form matches the Kailh low-profile full-POM series on the Choc V2 footprint (MX-cross stem,
  Choc-style hot-swap socket). Exact model names: not found. Confidence: likely.
- Store variants: Tactile, Clicky, Linear, all USD 159. Source: `products/glyf.json`. Confidence: confirmed.
- Hot-swap: yes ("are the keys hot swap?" - "Yes!"). Source: maker reply on YT-v9_v6v359Tw. Confidence: confirmed.
- A March 2026 close-up with one keycap removed shows a dark purple housing with the cross stem.
  Source: TT-2026-03-05 frames. Confidence: confirmed (appearance).
- Switch opening in the machined top shell: a caliper on an opening reads 14.06 mm in the sample-inspection clip.
  Source: TT-2025-06-24 frames (`_cache/social/tiktok-frames-hd-01/cal_sheet.jpg`). Confidence: likely.
- Keycaps: own design, low-profile, square with a shallow dish and a raised rim line, sides sloped. Designed in
  Fusion ("keycaps v2"), prototyped in resin (Elegoo Saturn 4 Ultra 16K). Production process intended: injection
  moulding. Sources: BLOG-03; TT-2025-07-19. Confidence: confirmed.
- Knobs: two cylindrical knobs on encoder shafts, each seated in a shallow circular dish cut into the top shell.
  Renders show a white index dot on each knob. Sources: TT-2026-03-05 and TT-2025-11-21 frames. Confidence: confirmed.
- Encoder functions are remappable like keys in the companion software since early 2026. Source: BLOG-05.
  Confidence: confirmed.
- Lower round buttons: two low round caps in round holes below the display. One is the widget-cycle button
  (BLOG-04). Layer, widget and Bluetooth selection happen on dedicated "system layers" with the knobs
  (TT id 7488570393620499742; TT-2025-10-04, id 7557263230071033118). Confidence: confirmed.

---

## 7. Case and mechanics

- Material: "6061 aerospace grade aluminum"; in another clip "aerospace grade aluminum just means 6061 or 6063
  aluminum". Sources: TT-2025-10-05 (id 7557776173275598110); TT-2025-10-21 (id 7563535884226678046).
  Confidence: confirmed (6061 stated first; alloy of production parts not independently verified).
- Process: CNC milled from billet, sandblasted to remove tool marks, then anodised black. Source: TT-2025-06-24.
  Confidence: confirmed.
- Vendor: a contract CNC shop reached through a sales contact shown as "Susin" ("Susan"); the shop footage shows a
  Taikan machining centre and a large anodising line. Company name: not found. Confidence: confirmed (process),
  not found (vendor name).
- Construction: two shells. The top shell is a thin plate-like part that contains the 16 square switch openings,
  two knob dishes, the display window and two round button holes. The bottom shell is a tray with a rib grid
  matching the key pitch. Source: TT-2026-03-05 frames. Confidence: confirmed.
- Tilt: the wedge is part of the bottom shell (a raised ramp at the rear with a pill-shaped recess), not a separate
  foot. A side view in Fusion shows a flat front section and a deeper rear section. Source: TT-2026-03-05 frames.
  Confidence: likely.
- Feet: custom-made silicone rubber feet, replacing the round stick-on feet of the Printed Pad. The first metal
  bottom had four round feet near the corners. Source: TT-2025-06-25. Confidence: confirmed.
- Rear edge: USB-C opening centred between the knobs and a slot for the power slide switch. Two slots are visible on
  the rear edge of the machined shell. Sources: TT-2025-12-30; TT-2026-03-05 frames. Confidence: likely.
- Cost driver stated by the maker: machining complexity, not the alloy ("More stuff to cut equals more expensive").
  The curved surfaces were kept "even if it cost us a little more to make". Sources: TT-2025-10-21; TT-2026-03-05.
  Confidence: confirmed.
- CAD: Autodesk Fusion for the design; BLOG-03 mentions redesigning inner geometry in SolidWorks for machining.
  Confidence: confirmed.
- **Measured dimension from the maker's CAD screenshot** (BLOG-03, image `Screenshot_2025-03-15_223917`, file
  "Low Profile Improved Pad v17", Fusion Measure panel): distance between the two long side faces = 84.694 mm.
  This is the depth across the four key rows of the March 2025 low-profile prototype. The same panel gives the
  selected side face as area 467.743 mm2 with loop length 237.44 mm, which solves to a face about 114.6 mm long and
  4.07 mm high. The overall width of that prototype (keys plus control column) is therefore about 115 to 117 mm
  including corner radii. Confidence: confirmed (84.694 mm on prototype v17), likely (about 115 mm width),
  guess (that the production case kept these values).
- Thickness: "19 mm thin" (store). Shipping weight field of the store variants: 442.1 g. Source:
  `https://protadesigns.com/products/glyf.json`. Confidence: confirmed (store values; the weight may include packaging).
- Layout proportions: 4 x 4 keys on the left; right column from rear to front is two knobs, display, two buttons.
  Unchanged since prototype 1. Confidence: confirmed.

---

## 8. Firmware and companion software

- Firmware base: ZMK on Zephyr, built inside the nRF Connect SDK. Chosen over QMK "because ZMK firmware is optimized
  for Bluetooth microcontrollers". Sources: BLOG-01; BLOG-02. Confidence: confirmed.
- The store text says the team stepped away from VIA and QMK "due to the lack of support for widgets, Bluetooth, and
  macro customization". Source: search snippet of `https://protadesigns.com/products/glyf`. Confidence: confirmed.
- Graphics: LVGL 9 (version 8 was tried first for SquareLine Studio compatibility and dropped). Source: BLOG-02.
  Confidence: confirmed.
- Companion software: a modified **ZMK Studio**. The screen recordings show the ZMK Studio header with added
  "Widgets" and device tabs, a bottom bar reading "(c) 2024 - The ZMK Contributors - About ZMK Studio - License NOTICE",
  tabs "Behaviors / Text / Encoders / Icon Library", and a "Runtime Macros" panel with "Record" and "Set Macro Delay".
  Sources: TT-2025-11-25 (id 7576513894936628511) frames; X-2018810453137445308; X-2019883069185065242; transcript of
  TT id 7474043910512184606 ("works in ZMK Studio"). Confidence: confirmed.
- A browser version and a downloadable version are both planned. Linux is supported. Source: maker replies on
  YT-v9_v6v359Tw. Confidence: confirmed (maker statement).
- Widgets. Normal widgets: keymap (icon grid), time, media. System widgets, shown automatically on their layer:
  layer menu, widget menu, Bluetooth, settings. Users can enable, disable and reorder normal widgets. A "UI router"
  centralises navigation and persistence. Sources: BLOG-04; TT-2025-10-04. Confidence: confirmed.
- Device-to-host protocol detail: on connect the device sends the full widget list with properties; widget order is
  sent separately on each update event. Source: TT-2025-11-25. Confidence: confirmed.
- Icons are stored as files on the external NOR flash through an LVGL file system, not as C arrays in firmware.
  Users upload their own icons. Source: BLOG-04; BLOG-05. Confidence: confirmed.
- Macros: recorded from the keyboard in the companion software, saved to the device, replayed by one key.
  Source: BLOG-05; X-2019883069185065242. Confidence: confirmed.
- Capacity claims: 16 layers of 16 keys (256 macros); four Bluetooth hosts. Source: store. Confidence: confirmed
  (maker claim).
- Firmware update: through the companion software over USB ("We transmit the data through usbc to program our
  boards"). Sources: BLOG-05; maker reply on YT-CqwCjghqUu0. Confidence: confirmed.
- Screen layout seen on working hardware (March 2026): top row with application or layer name at the left and
  settings and battery icons at the right; a second band with two knob legends, each an icon with two text lines
  such as "<Vol+ / >Vol-" and "<Zm+ / >Zm-"; then a 4 x 4 icon grid mirroring the keys. Source: TT-2026-03-05
  frames. Confidence: confirmed.

---

## 9. Points that matter for an original design in the same class

1. A module-based nRF5340 (or nRF52840) design with ZMK is the maker's own route; ZMK Studio already gives runtime
   keymap editing. The maker hand-soldered the radio module on prototypes instead of having it placed.
2. The power block is the part that failed twice for them (series resistor at the load switch; an earlier wiring
   fault). They now prove the power path on perfboard before ordering.
3. The display is a 1.4 inch 240 x 240 IPS module with a bonded 1.1 mm cover lens, 2.95 mm total, 20-pin 0.5 mm
   tail fed through a PCB slot to a bottom-side connector. Lens overhang is glued to the case with 0.15 mm tape.
4. Extras beyond a plain macropad: external NOR flash for icons, RTC with a rechargeable ML1220 backup cell,
   I2C fuel gauge, GPIO expander, hardware power switch, reset button, SWD pads.
5. Switches are Kailh low-profile full-POM on Choc-style hot-swap sockets with per-key diodes; opening about 14 mm.
6. A 5-piece JLCPCB assembled prototype run of this board cost USD 284.66 before shipping and duties, with 18
   extended parts.

---

## 10. Sources read

- `https://protadesigns.com/` (footer links), `/blogs/updates.atom` (six posts, full text),
  `/pages/about-us`, `/pages/contact`, `/pages/terms-of-services`, `/pages/terms-and-conditions`,
  `/pages/refund-policy`, `/pages/glyf-waitlist`, `/products/glyf.json`, `/products/printed-pad.json`.
- 23 images embedded in the blog posts (Shopify CDN), viewed and measured.
- TikTok `@protadesigns`: full listing of 201 posts (dates, captions, counters). 40 videos downloaded for
  transcription; frames examined for 20250331, 20250505, 20250624, 20250625, 20251008, 20251010, 20251113, 20251114,
  20251121, 20251125, 20251130, 20251230, 20260305.
- Instagram reels `DBYO7BoRKXv`, `DD5iov1yJnn`, `DFeXk5QJXKZ` (metadata only).
- X posts 2017126263744581642, 2018810453137445308, 2019582172567597340, 2019883069185065242 through
  `cdn.syndication.twimg.com` (text, counters, video at 720p).
- YouTube `@PROTADESIGNS`: listing of videos and shorts; comments with maker replies on `CqwCjghqUu0`,
  `hBXO5tvxVr8`, `kOclb0i9bug`, `v9_v6v359Tw`, `S9c5WuorsgQ`, `wLHIWHExL-k`, `Nk6MD9QS8VA`, `Q6CKpc6AK0o`.
- Discord invite metadata: `https://discord.com/api/v9/invites/nSYUuAXxWp?with_counts=true`.
- `https://www.linkedin.com/company/prota-designs/` (public view).
- `https://f.inc/artifact/teams/prota-designs`.
- Web searches for reviews, unboxings, forum threads, founder profiles and other platform accounts.

## 11. What could not be reached

- Instagram: profile grid, captions and comments (login wall). Only three reels known from blog embeds were read.
  One attempt to fetch the profile with a crawler user agent was refused by the local permission policy and was not
  repeated.
- X: timelines of `@prota_designs` and `@ben_baybay` (login wall; the embed timeline endpoint returned no entries).
  Only the four posts embedded in the blog were read. Replies to those posts were not readable.
- Discord: channel content (announcements, beta-tester discussion). This is the most probable place for
  beta-unit photos, battery capacity, final dimensions and shipping news.
- LinkedIn personal profiles (HTTP 999). Education and employment history were therefore not collected.
- TikTok comments (yt-dlp does not return them). Maker replies there were not read.
- Kickstarter (HTTP 403): the 2023 Printed Pad campaign page.
- `bizprofile.net` (HTTP 403): the company filing page. The incorporation date is second-hand.
- Reddit (HTTP 403): the maker says the prototype-2 schematic was posted to Reddit for help. The thread was not found.
- Threads, Facebook, Pinterest: script shells only.
- The Autodesk "Shop Talk" podcast episode with the founders was not located.
- No independent review, unboxing or teardown of a shipped unit was found. Shipment to customers is unconfirmed as
  of 2026-11-13.
