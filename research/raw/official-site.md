# Official site research: protadesigns.com (GLYF by Prota Designs)

Date of research: 2026-11-13.
Agent key: `official-site`.
Scope: the maker's own web presence (Shopify storefront, blog, policies, media, Wayback Machine history).
Cache root: `research/_cache/official-site/` (gitignored).

Confidence labels used below:

- **confirmed**: stated by the maker, or measured from a primary source such as a maker file or a maker screenshot.
- **likely**: consistent indirect evidence, for example a dimension scaled from a maker drawing.
- **guess**: an inference with weak support.
- **not found**: the site does not state it.

All measurements taken from renders or drawings are estimates. No vendor artwork, firmware, software or 3D model was copied into the repository.

## 1. Headline findings for the design

1. The production GLYF uses Kailh low-profile V2 switches in hot-swap sockets, a 240 x 240 px colour LCD under tempered glass, Bluetooth 5.2, a 1,200 mAh Li-ion cell and a CNC aluminium two-shell case. (confirmed, product page tech specs)
2. The production board uses an "nRF53 series module". Earlier prototypes used an nRF52833 chip-down design. The firmware is a private build on ZMK, Zephyr, the nRF Connect SDK and LVGL. (confirmed, blog updates 01, 02 and 05)
3. A vector top-view line drawing on the product page gives the plan proportions. With a 19.0 mm key pitch it scales to a body of about 120.0 x 84.9 mm. A maker CAD screenshot of a 2025 prototype shows a measured depth of 84.694 mm, which agrees. (likely)
4. The "19 mm" claim matches the height at the rear, measured from the foot bottom to the top face (about 18.8 mm). The case is a wedge: about 13.1 mm thick at the front edge and about 17.0 mm at the rear riser. Keycaps add about 5 mm and knobs add 12 to 14 mm. (likely, scaled from the side render)
5. The site has no 3D viewer asset. It has no dimension table, no device weight, no battery life figure, no MCU part number and no software download. (confirmed absent on 2026-11-13)
6. The site does not announce that shipping has started. On 2026-11-13 the product page still says "Pre-order Now" and "Shipping Early Q4 2026". (confirmed)

## 2. Company and legal

| Fact | Value | Source | Confidence |
| --- | --- | --- | --- |
| Trading name | PROTA DESIGNS / Prota Designs | `/meta.json`, Terms of Services | confirmed |
| Legal form | Not stated. The terms say only "This website is owned and operated by Prota Designs". | `/pages/terms-of-services` | not found |
| Location | Lake Elsinore, California, US | `/meta.json` | confirmed |
| Governing law | State of California, United States | `/pages/terms-of-services` | confirmed |
| Contact | business@protadesigns.com, contact form, Discord help-ticket channel | `/pages/refund-policy`, `/pages/terms-and-conditions`, `/pages/contact` | confirmed |
| People | "Ben | CEO" and "Noah | CTO". Blog authors are Ben Baybay and Noah Beidelman. | `/pages/about-us`, `/blogs/updates.atom` | confirmed |
| Background | "We were partners in a NASA internship". Self-funded: "No investors". | `/pages/about-us` | confirmed |
| Shopify shop id | 61911662649, `382195.myshopify.com`, currency USD | `/meta.json` | confirmed |
| Theme | "GLYF Launch", Shopify "Impact" theme 6.8.0 | `Shopify.theme` in page source | confirmed |
| Social | x.com/prota_designs, instagram.com/protadesigns, youtube.com/@PROTADESIGNS, tiktok.com/@protadesigns, discord.gg/nSYUuAXxWp | page footer | confirmed |
| Waitlist | "There are 2,031 people on the waitlist." The same number appears in the 2026-05-14 Wayback capture, so the counter is static. | `/pages/glyf-waitlist` | confirmed |

## 3. Catalogue and variant data

Source: `/products.json`, `/products/glyf.js`, `/products/glyf.json`, `/collections.json`. All confirmed.

The store has two published products and one collection ("All Products", handle `most-popular`).

### 3.1 GLYF (handle `glyf`, id 7879347142713)

- Description: "Aluminum Wireless Bluetooth Macro Pad with LCD and Two Rotary Encoders".
- Product type "Macro Pad". Vendor "PROTA DESIGNS". No tags. Template suffix `pre-order`.
- Record created 2025-03-31. Featured image uploaded 2025-09-10.
- One option, "Switches", with three values: Tactile, Clicky, Linear.
- There is no colour option. The only finish is anodised black.

| Variant | Id | Price | Compare-at | Grams | SKU | Barcode | Available |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tactile | 44388992614457 | 159.00 USD | 189.00 USD | 442 | empty | null | true |
| Clicky | 44388992647225 | 159.00 USD | 189.00 USD | 442 | empty | null | true |
| Linear | 44388992679993 | 159.00 USD | 189.00 USD | 442 | empty | null | true |

The 442 g value (442.1 g in `glyf.json`) is the Shopify shipping weight field. It most likely includes the box and the cable. The site does not state the bare device weight. (guess for the interpretation)

The UAH 7,331 price seen by the owner is the store's currency localisation of 159 USD.

### 3.2 Printed Pad (handle `printed-pad`, id 7018921852985)

This is the maker's earlier product. It matters only as design lineage.

- "3D Printed Macro Pad with OLED Display". 47.00 USD, compare-at 59.00 USD, 246 g shipping weight, sold out.
- 9 keys, 4 layers, "36 Reprogrammable Keys", "VIA & QMK Programmable", "5-Pin Hot-swappable", USB-C, PLA case, "Stores macros on the device up to 4KB".
- Switch options: Gateron Milky Yellow Pro (linear), Gateron KS-9 2.0 Brown (tactile), Gateron KS-9 2.0 Blue (clicky).

### 3.3 Hidden or accessory products

- No dock, keycap set, cable, case or other accessory product exists. Twenty-one plausible handles returned HTTP 404, and the predictive search returns only the two products. (confirmed absent)
- The Wayback Machine holds one capture of `/products/glyf-alpha-testing` from 2025-05-23. The live URL returns 404. The capture is the same product record under an earlier handle: it carries the same three variant ids. Its title was "Glyf (Alpha Testing)". It showed a "Coming Soon" image, a price of 0.00 USD, "OutOfStock" and a "Join Waitlist" link. It held no specifications. (confirmed)
- The second object in the hero and product renders is not a dock. It is a second GLYF shown upside down. It shows the underside, four stadium-shaped feet and the tilt riser. (likely, from the full-resolution product image)

## 4. Product copy with exact wording

### 4.1 Home page (`/`)

- "A Premium Macro Pad for Instant Shortcuts". "Automate your most used actions in your favorite apps".
- "Custom layers & macros", "Customizable icons", "Wired or wireless", "Windows • macOS • Linux".
- "$159", "Pre-order now", "Ships early Q4 2026", "Cancel anytime before shipping".
- "Aerospace Grade Aluminum". "Up to 256 Macros". "Multi-Device Pairing 4 Devices". "Ultra-Slim Design". "Personalized Widgets*". "Precision Control".
- Heading "Ultra-Slim Design" with the text "Just 19 mm thin."
- Heading "3+ Widgets*" with the text "Macros, time, music, and more to come." Further headings: "256 Icons", "16 Layers", "256 Macros".
- The asterisk footnote reads: "*Time & Media widgets TBD".
- "Aerospace-grade aluminum gives every press a premium weight and a solid feel in your hands."
- "Tempered glass keeps every detail crisp and smooth while adding the strength to stand up to everyday use."
- "Molded from POM plastic, the low-profile switches deliver a silky, satisfying feel with every press."
- Footer call to action: "*Shipping starting Q4 2026".

### 4.2 Product page (`/products/glyf`)

Badges: "Bluetooth & Wired", "Custom Macros", "Personalized Key Icons", "Interactive Screen", "Machined Aluminum", "Fast USA Shipping", "Worldwide Shipping".

Pre-order text: "Pre-order Now", "Shipping Early Q4 2026", and: "By clicking "Pre-order," I confirm that I'm purchasing an item that will ship at a later date and accept the terms and conditions of the pre-order process."

Feature sections, each given as heading and then body text:

- "Endless Macros". "GLYF has 16 layers, each with 16 keys. That's 256 customizable macros for all your shortcuts."
- "Your Workflow, Visualized". "Select or create custom icons that make every action clear."
- "Dynamic Widgets". "Customizable icons, time with custom wallpapers, plus media widget. (Time & Media TBD)"
- "Connected Your Way". "Take it anywhere with seamless Bluetooth and USB-C connectivity."
- "Precision in Every Turn". "Dual knobs give you smooth control over any setting."
- "Comfort in Every Press". "A new keycap shape and low-profile design made to feel, sound and look better."
- "Premium by Design". "Built with aerospace-grade aluminum for lasting quality."
- "Whats in the Box?" "You'll find GLYF, a USB-C to USB-C cable, and a Quick Start Guide."

Tech specs table, quoted in full (confirmed):

| Row | Value |
| --- | --- |
| Chassis | "CNC Aluminum | Anodized Black" |
| Switches | "Kailh Low Profile V2's (hot-swappable)" |
| Keycaps | "Injection Molded PBT Plastic" |
| Knobs | "Injection Molded PBT Plastic" |
| Screen Glass | "Tempered Glass with Black Screen Print" |
| Screen | "240 x 240 px Full Color LCD" |
| USB-C Connection | "USB-C to USB-C Cable Included" |
| Bluetooth Connection | "Bluetooth 5.2 at 2.4 GHz" |
| Bluetooth Capability | "Up to 4 devices" |
| Battery | "1,200 mAh Li-Ion Battery" |

FAQ (confirmed):

- Operating systems: "Windows, Linux, Android, MacOS, and iOS. Please note that certain widgets will not work on iOS and Android because our companion app is not available on these platforms."
- "Can I use VIA/QMK with it? For more customizability, we have developed our own custom software. We have decided to step away from VIA/QMK due to the lack of support for widgets, Bluetooth, and macro customization."
- "Can I use Glyf without software? Yes. Once you've set up your device using our software, all your macros and configurations will be stored directly on your GLYF ... However, please note that certain widgets may require software support to function."
- "Through our custom software, you will be able to either select or upload your own image for every macro."

### 4.3 Structured data

- JSON-LD `ProductGroup`, category "Keyboards", three variants at 159.00 USD, availability "InStock". There is no weight, size, GTIN or review field.
- Meta description equals the product description. Open Graph image is the 5000 x 5000 product render.

### 4.4 Specifications the site does not give

Each item below is **not found** on the site: overall width and depth, device weight, battery life, charge current or charge time, MCU part number, display size in inches, display controller, switch model numbers for the three options, key pitch, keycap profile name, knob encoder model, detent count, aluminium alloy number, warranty length, a 2.4 GHz dongle, RGB or backlight, and a software download link.

## 5. Engineering facts from the development blog

Source: `/blogs/updates.atom` (six articles). All statements are maker statements unless marked.

### 5.1 Timeline

| Date | Event | Source |
| --- | --- | --- |
| 2024-04-25 | Photo file date of the first LCD test on prototype 1. | Update 01 image filename |
| 2024-07-05 | Photo file date of the bootloader flashing on prototype 2. | Update 01 image filename |
| 2024-12-28 | Update 01. Two prototypes built. Move from QMK to ZMK. | blog |
| 2025-01-15 | Update 02. Display driver and LVGL tests. ZMK running on the nRF52840 DK. | blog |
| 2025-03-15 | Update 03. 240 x 240 LCD chosen. Low-profile switches and custom keycaps. | blog |
| 2025-03-31 | GLYF product record created in Shopify. | `products.json` |
| 2025-04-06 | Waitlist page created. | `pages.json` |
| 2025-05-23 | A `glyf-alpha-testing` product page existed. | Wayback CDX |
| 2025-09-29 | Pre-order terms pages created. | `pages.json` |
| 2025-10 | Pre-orders opened. | Wayback 2025-10-17, Update 04 |
| 2025-11-01 | Update 04. New widget system, UI router, file system on external flash. | blog |
| 2026-01 | Six weeks at Founders, Inc. in San Francisco ("Artifact"). Launch video on 2026-01-30. | Update 05 |
| 2026-03-09 | Update 05. "Final production hardware is complete". Beta test announced. | blog |
| 2026-10-09 | Update 06. Beta test finished. Production ramp. "Still on track to ship in Q4". | blog |

### 5.2 Prototype 1 (wired, 2024)

- "we made the first PCB based off the same hardware the Printed Pad uses and added two knobs, a screen, two buttons to control the screen, and more keys". (confirmed)
- The two extra buttons exist "to control the screen". This is the stated purpose of the two round buttons. (confirmed)
- Firmware was QMK with VIA. The LCD used SPI and QMK Quantum Painter. LVGL did not fit in the MCU flash. (confirmed)
- A later test used "example ST7735 driver code", so the first display used an ST7735 controller. (confirmed)
- Photos show MX-size switches, Kailh-style MX hot-swap sockets, a TQFP MCU, a USB-C socket at the rear edge, two EC11-size encoders, a red breakout LCD module and two 6 mm tactile buttons. (confirmed from photos; part identities are likely)

### 5.3 Prototype 2 (Bluetooth, 2024)

- "we decided to move Glyf to use ZMK firmware ... because ZMK firmware is optimized for Bluetooth microcontrollers". (confirmed)
- Added parts: "adding memory, a battery management system, an on and off switch, a GPIO expander, and pull up resistors". The design considerations also name "a real-time clock". (confirmed)
- "The battery management handles power coming in from the USB-C to charge the battery, the temperature of the battery, and the power supply coming out of the battery". (confirmed)
- "the Nordic microcontroller we chose for Glyf doesn't have a preinstalled bootloader". They flashed one with a Blue Pill running Black Magic Probe firmware. (confirmed)
- A terminal photo shows the file name `feather_nrf52833_express_bootloader-0.9.1_s140_7.3.0.hex` and the target "Nordic nRF52 M3/M4". Prototype 2 therefore used an nRF52833 with the Adafruit nRF52 UF2 bootloader and SoftDevice S140 7.3.0. (confirmed from the maker photo `files/20240705_172608.jpg`)
- KiCad screenshots of prototype 2 show the following. (confirmed that the items are visible; part identities are likely)
  - A 4 x 4 key matrix with one diode per key (D1 to D16) and footprints named "MX-NoLED".
  - A QFN Nordic chip with a chip antenna at the right board edge, beside the display and clear of the key area. The mirrored footprint text reads "ANT016008LCS2442MA1". This is a TDK 2.4 GHz chip antenna in a 1.6 x 0.8 mm case. (likely for the exact part)
  - A TSSOP package "U4" beside the MCU. This is the likely GPIO expander.
  - An SOIC-8 package. This is the likely external flash.
  - A crystal, a slide switch "S1" beside the USB-C socket, a tactile reset button "SW5", a 2-pin battery connector "J2", and a board cut-out below it.
  - Two encoder footprints whose names start with "RotaryEncoder" and contain "Switch". The encoders therefore have a push switch.
  - Two surface-mount tactile switch footprints for the round buttons. The partly hidden footprint names contain "Omron_B3" and end in "S". This fits the Omron B3FS series. (likely)
  - A 4-pin header "J3" between the two round buttons. Its purpose is not stated. A debug header is a guess.
  - Four plated mounting holes inside the key area, named "MountingHole_Pad".
- Update 03 says this prototype PCB "featured Alps Alpine rotary encoders". (confirmed)

### 5.4 Display selection

- The first glass-covered sample was a "120x120 LCD". The FPC label in the photo reads "ENH-TV0144006A". The connector tail is marked 1 to 8. (confirmed for the label; the "0144" suggests a 1.44 inch panel, guess)
- "the resolution of the screen was too low ... we found a manufacturer that could make a 240x240 LCD display that would fit perfectly with our design". (confirmed)
- The FPC label of the 240 x 240 sample reads "FPC-TFT014H030-A0". (likely; read from a photo at full resolution)
- The display is driven over SPI. On Zephyr the driver moved to the MIPI-DBI API. (confirmed, Update 02)
- Update 05: "We've also received our final screens, now featuring a tempered glass layer over the display". (confirmed)

### 5.5 Switches, keycaps and case

- "Welcome to the new age of low-profile switches. Choc switches walked so that Kailh low-profile switches could run! Fully made of POM, available in clicky, tactile, and linear options". (confirmed)
- The three switch images in Update 03 show a Kailh low-profile switch with an MX-style cross stem, two metal pins and a centre post. This is the Kailh Choc V2 family. (likely)
- The product page exploded render shows the same construction: cross stem, coil spring, centre post, two pins. (confirmed that it is visible)
- "We should design low-profile keycaps to match the switches". The keycaps were first resin printed for feel tests. The production keycaps are injection-moulded PBT. (confirmed)
- CAD screenshots list the bodies of the March 2025 design "Low Profile Improved Pad v17": Case (Top, Bottoms, Switch), Keycaps (16), Rotary Encoders (2), Buttons (2), LCD, Tempered Glass. (confirmed)
- The same screenshot shows a Fusion 360 measurement of **84.694 mm** between the two long outer faces of the top shell. This is the case depth (the direction of the four key rows). The two selected faces have loop lengths of 237.44 mm and 241.884 mm and areas of 467.743 mm2 and 441.475 mm2. Solving gives flat face lengths of about 114.6 mm and 117.2 mm. With the corner radii the case width is about 119 to 121 mm. (confirmed for 84.694 mm on the March 2025 prototype; likely for the width)
- "redesigning the inside geometry in SolidWorks to be easily machined out of aluminum". (confirmed)
- Update 05: "the case is now machined from cnc aerospace grade aluminum". "These will be the final version we use for production." (confirmed)

### 5.6 Production electronics (2026)

- "We've moved away from using a generic MCU board and instead adopted an nRF53 series module, which gives us better performance in a much more practical form factor. Its smaller size allows us to integrate everything directly onto the PCB". (confirmed, Update 05)
- The exact module is not named. (not found)
- Update 06: "We're working with manufacturers to get everything ready from the PCBs to the CNC machined aluminum cases to the tempered glass displays." (confirmed)

### 5.7 Firmware and software

- Stack: ZMK on Zephyr with the nRF Connect SDK, and LVGL 9 for the UI. SquareLine Studio was considered and dropped because it did not support LVGL 9 at that time. (confirmed, Updates 01 and 02)
- Widgets have two classes. Normal widgets: "the keymap widget, time widget, and media widget". System widgets: "the layer menu widget, widget menu widget, Bluetooth widget, and the settings widget". (confirmed, Update 04)
- A "widget-cycle button" steps through the enabled normal widgets in a user-set order. System widgets appear only on their own layer, for example the Bluetooth widget on the Bluetooth layer. (confirmed, Update 04)
- A "UI router system" routes all widget navigation and settings through one controller. (confirmed)
- A file system on external flash stores images and fonts. The stated reason is to leave "more room on the internal chip flash memory for firmware features". (confirmed)
- Icons are uploaded by the user through the companion software and assigned per key. (confirmed, Update 05)
- Macros are recorded from the keyboard, saved on the device and replayed. Encoder rotation is remappable. (confirmed, Update 05)
- Firmware update runs from the companion software. Development units are flashed with a hardware programmer. (confirmed, Update 05)
- The companion app exists for Windows, macOS and Linux only. (confirmed, product FAQ)
- The site has no download link, no manual, no documentation site and no source repository link. (confirmed absent)

## 6. Media inventory

All files are in `research/_cache/official-site/03-media/`. Shopify size suffixes were removed, so each URL is the full-resolution original. Base path for every entry: `https://protadesigns.com/cdn/shop/`. The machine-readable list is `research/_cache/official-site/media_urls.txt`.

### 6.1 GLYF product and home page stills

| File | Pixels | Content |
| --- | --- | --- |
| `files/prod_7c6895ff-3732-432d-bb54-e42f7affdd6c.png?v=1757540847` | 5000 x 5000 | Product image. Three-quarter top view. Behind it a second unit shows the underside: four stadium-shaped feet in shallow recesses and the rear riser with scooped flanks. No screws are visible. Display shows "Applications", "10:00", Bluetooth and battery icons, knob labels "Vol+ / Vol-" and "Nxt / Prv", and a 4 x 4 grid of application icons. |
| `files/heroprod_2.png?v=1765676724` | 3610 x 2160 | Hero, landscape. Same arrangement. Display shows "AU Fusion", "10:00", knob labels "Redo / Undo" and "Zoom+ / Zoom-", and a 4 x 4 grid of CAD tool icons. |
| `files/heroprod_1.png?v=1765672067` | 2160 x 3610 | Hero, portrait crop of the same scene. |
| `files/1_ab7debeb-767f-437d-8308-0a1bd7ac1f88.jpg?v=1757557210` | 4000 x 2000 | Front view, low angle. Keys left, knobs right rear, display with a clock widget ("Design", "11:00", "Fri, Sep 12", wallpaper), two low domed round buttons. Two front feet are visible. |
| `files/2_d50dca61-0ae3-4d3c-98de-c76b95fc43c8.jpg?v=1757557228` | 4000 x 2000 | Right side view. Buttons, display, knobs in a line. The shell split line and the rear riser are visible. |
| `files/3_2c90c273-fe8d-459b-8978-8c3d15af9203.jpg?v=1757557240` | 4000 x 2000 | Rear view. **USB-C port and a slide power switch on the rear edge**, both centred on the shell split line. The riser spans most of the width with concave ends. Two rear feet. |
| `files/4_1179c84d-587f-440e-906e-171f6b6413be.jpg?v=1757557250` | 4000 x 2000 | Left front three-quarter view. |
| `files/1_6426fca6-...jpg`, `files/2_6ba86080-...jpg`, `files/3_8ab8273d-...jpg`, `files/4_a80bcc40-...jpg` | 2000 x 4000 | Portrait crops of the four views above for mobile. |
| `files/Untitled_design_13.jpg?v=1759027972` and `files/Untitled_design_13_775c9e55-...jpg?v=1759027984` | 6500 x 2300 | Left side profile used for the "19 mm" claim. Best source for thickness. |
| `files/Untitled_design_14.jpg?v=1759028074` | 2700 x 7541 | The same side profile rotated for mobile. |
| `files/Desktop_Size_Grid_1_46ae2ac8-...jpg?v=1759548142` and `files/Mobile_Features_Grid_3_6896a433-...jpg?v=1759548182` | 3000 x 2000, 2000 x 3500 | Exploded view of the two aluminium shells from the rear. Top shell: integrated switch plate with 16 square cut-outs in a recessed key well, a display window with a glass ledge, two knob holes with raised conical bosses, two button holes. Bottom shell: a tray with internal pockets and two notches for the USB-C port and the slide switch. |
| `files/Untitled_design_10.jpg?v=1758683018` | 3000 x 3500 | Close view of the two shells on edge. Shows the riser profile and the tab notches. |
| `files/Untitled_design_11.jpg?v=1759027667` | 3000 x 3500 | Three stacked cover glasses with clock wallpapers. The glass has a wide black print border. |
| `files/2_93486fad-42cb-4bad-9493-b398f9209306.jpg?v=1758682139` | 3000 x 3500 | Exploded switch and keycap: keycap with cross mount, top housing, stem, spring, bottom housing with two pins and a centre post. |
| `files/Untitled_design_7_9d3b1358-...jpg?v=1758678421` and `files/Untitled_design_12.jpg?v=1759027789` | 3000 x 1900, 1975 x 3300 | Near-top views of the whole device. |
| `files/Untitled_design_16.jpg?v=1759034994` and `..._d01122bc-...jpg?v=1759034998` | 3000 x 3000 | Three display layouts stacked above the device: "AU Fusion", "Photoshop" ("Zoom+ / Zoom-", "Brsh+ / Brsh-"), "Excel" ("Redo / Undo", "Up / Down"). |
| `files/Untitled_design_17.jpg?v=1759036190` | 2000 x 1773 | Knob close-up. White tick marks around the knobs are overlay graphics. Display shows a "Spotify" media widget. |
| `files/Untitled_design_18.jpg?v=1759272612`, `files/Desktop_Size_Grid_3.jpg?v=1759277721`, `files/Mobile_Features_Grid_7.jpg?v=1759277650` | 4083 x 2000, 3000 x 2000, 2000 x 3500 | Three widget screens: keymap ("AU Fusion"), clock with wallpaper ("Video Editing", "10:00", "Tue, Oct 14", a USB icon in place of the Bluetooth icon), media ("Spotify", cover art, title, artist, pause icon, "-2:48"). |
| `files/Mobile_Features_Grid_6.jpg?v=1757536483` and `..._7a07b924-...jpg?v=1757536485` | 2000 x 3500 | Keycap beauty render. Square keycaps with a shallow rectangular dish. |
| `files/GLYFCABLESVG3.svg?v=1755130377` | vector | "What's in the box" line drawing: orthographic top view of the device and a USB-C to USB-C cable. Used for the plan measurements in section 7. |
| `files/1_f0ab69e6-...jpg` to `files/19.jpg`, `files/Untitled_design_4.jpg` | 300 x 300 | Twenty third-party application logo tiles for the "Works everywhere" carousel. Not relevant to the hardware. |

### 6.2 GLYF product page videos

All are short silent render loops, 24 fps. Each exists in a desktop and a mobile version.

| Files (`videos/c/vp/<id>/<id>.HD-...mp4`) | Size, length | Content |
| --- | --- | --- |
| `5288efd000c54dd0a22e4e4f23e3c59b` (720 x 720), `c5843f91a28c4e1db5811e256340c383` (616 x 1080) | 7.2 s | "Shortcuts Made Simple". Keys with overlaid shortcut text such as "Cmd + Options + Esc" and "Win + Shift + s". |
| `654b29ccd4aa4dc1805009d5c5b55ac3`, `cea4b06ea28c4dd786dd0767dfc477a3` (616 x 1080) | 14.0 s | "Your Workflow, Visualized". A scrolling library of monochrome line icons. |
| `6f66cafa8d604ab7a562a8c43dbbcf7b` (720 x 720), `103385dd927a4fc8abe861e658480e5f` (616 x 1080) | 4.8 s | "Connected Your Way". Rear view with the USB-C port and slide switch, with host device icons appearing above. |
| `df6e9ffece3e45f0a0486e3ed3f45109`, `e7c94491950b443bba46cac61135d525` (616 x 1080) | 6.2 s | "Precision in Every Turn". Knob close-up with animated tick marks. The media widget shows "Eye of the Storm". |
| `9cec11c64b994632a623300b303fb009`, `f79002e3d60346f5ae756e2057764058` (616 x 1080) | 6.2 s | "Comfort in Every Press". Side silhouette, then a single keycap rotating. |

### 6.3 Blog images

| File | Content |
| --- | --- |
| `files/frontpcb.png`, `files/back_pcb.png`, `files/topsld.png` (Update 01) | Prototype 1. Front with MX keycaps, two encoders, red LCD breakout, two tactile buttons. Back with hot-swap sockets, a TQFP MCU and a USB-C socket. |
| `files/20240425_120504_0923341b-...jpg` | Prototype 1 LCD test image. |
| `files/asdfjkasdfjkljasdfk.png`, `files/geradfasdfasdf.png` | Prototype 2 KiCad layout and 3D view. See section 5.3. |
| `files/20240705_172608.jpg` | Terminal photo with the nRF52833 bootloader file name. |
| `files/bluepill.png` | Blue Pill used as a debug probe, wired to prototype 2. |
| `files/Mini_Update_10.jpg`, `files/Mini_Update0.jpg` (Update 03) | Two glass-covered LCD samples with the FPC label "ENH-TV0144006A". A printed case with the sample fitted. |
| `files/P2P_4_LCD0.jpg` | Two 240 x 240 LCD samples with the FPC label "FPC-TFT014H030-A0". |
| `files/Screenshot_2025-03-15_165535.png` | Fusion 360 view of the first bulky case with MX keycaps. |
| `files/Part_20.jpg`, `files/Part_20_f9ac3461-...jpg` | Two prototype PCBs from the back. A printed prototype held in the hand. |
| `files/Screenshot_2025-03-15_171901.png`, `..._171734.png`, `..._171754.png` | Three Kailh low-profile switch product images (grey, black, dark green housings). |
| `files/Screenshot_2025-03-15_172123.png` | Fusion 360 view of "Low Profile Improved Pad v17" with the body list. |
| `files/Screenshot_2025-03-15_172244.png` | Fusion 360 view of "keycaps v2": 16 identical low keycaps with a dished top. |
| `files/best_upgrade0.jpg` | Printed low-profile prototype in the hand. |
| `files/Screenshot_2025-03-15_223917.png` | Fusion 360 measurement of 84.694 mm. See section 5.5. |
| `files/Screenshot_2025-10-31_195904.png` (Update 04) | Earlier home page hero: "The world's easiest way to master macros." |
| `files/artifactfestival.jpg` (Update 05) | Booth photo. A founder holds a unit. The sign reads "Move 3x faster in any software." |
| `articles/*.png|jpg` | Six article header images. The Update 06 header is the near-top product render. |

Embedded videos on the blog (YouTube ids, for the video research agent): `FC8CT-lUjvQ`, `8kk6UOHNkWg`, `AEPYk2L68G0`, `brxQ2vnSMzs`, `VzyTGfTZlpE`, `IaAfArGgowo`, `TKKm-nHWP4Q`, `KqhWx42rBqI`, `gmUwqF4LKXo`, `hvGEQ6V8Q90`, `l7_WagUqaJU`, `bP_OEk6QhI0` (old widget system), `CMcZaoDR8_s` (new widget system), `OhOzBamzcys` (removing widgets), `GsekCKWMDsI` (adding widgets), short `wv6qhc9iFxA`. The Printed Pad setup guide is `Yj0VQmUgzN0`.

Embedded posts: X posts by `ben_baybay` with status ids 2017126263744581642 (launch video, 2026-01-30), 2018810453137445308 (icon upload), 2019582172567597340 (comparison with Stream Deck), 2019883069185065242 (macro recording). Instagram reels `DBYO7BoRKXv`, `DD5iov1yJnn`, `DFeXk5QJXKZ`. Beta application form: `forms.gle/UCMDKHLhcwEUwXY6A`.

### 6.4 3D assets

No `glb`, `gltf`, `usdz`, Spline scene, `model-viewer` element or Sketchfab embed exists on any page. The product has one media item, and its type is `image`. (confirmed absent)

## 7. Measurements

### 7.1 Plan view from the vector line drawing

Source: `files/GLYFCABLESVG3.svg`. The drawing is an orthographic top view. Coordinates were read from the SVG geometry. The scale is not given, so one known length is needed.

Scale choice: the key pitch in the drawing is 114.95 units. A pitch of 19.0 mm gives a body depth of 84.94 mm. The maker's 2025 prototype measured 84.694 mm. A pitch of 19.05 mm gives 85.16 mm, and a pitch of 18.0 mm gives 80.47 mm. The 19.0 mm pitch is the best fit. All values below use 6.050 units per millimetre. Every value is **likely**, with an error of about 0.3 mm from the scale and the stroke width. The drawing is a marketing illustration, so small features may be simplified.

| Feature | Value |
| --- | --- |
| Body outline, width x depth | 120.0 x 84.9 mm |
| Width to depth ratio (scale independent) | 1.413 |
| Key pitch, both axes | 19.0 mm (assumed) |
| Keycap base footprint | 18.4 x 18.4 mm, so the gap between caps is 0.6 mm |
| Keycap top face | 12.0 x 12.0 mm |
| Key well, inner | 76.0 x 76.0 mm |
| Key well lip, outer | 78.0 x 78.0 mm |
| Wall between the left body edge and the key well lip | 3.5 mm. The same value applies at the front and the rear. |
| Centre of the top-left key from the left and rear edges | 14.0 mm, 13.5 mm |
| Control column width, key well lip to right edge | 38.6 mm |
| Knob centres from the right edge | 10.2 mm and 28.9 mm (centre spacing 18.6 mm) |
| Knob centres from the rear edge | 15.1 mm |
| Knob rings | 8.0 mm, 10.5 mm and 16.1 mm diameter. The 10.5 mm ring is the knob body. The 16.1 mm ring is the conical boss on the case. |
| Cover glass | 31.1 x 31.1 mm, corner radius about 2 mm |
| Cover glass position | 4.0 mm from the right edge, 26.9 mm to 58.0 mm from the rear edge |
| Round button rings | 10.3 mm and 12.4 mm diameter |
| Round button centres from the right edge | 10.2 mm and 28.9 mm, the same as the knobs |
| Round button centres from the front edge | 14.0 mm |

Display active area: in the widget render the wallpaper fills about 80 % of the glass width. That gives an active area of about 25 mm square, which is a diagonal of about 1.4 inches. The FPC label "TFT014" agrees with a 1.4 inch class panel. (guess)

### 7.2 Height from the side and rear renders

Source: `files/Untitled_design_13.jpg` (side, 6500 x 2300 px) and `files/3_2c90c273-...jpg` (rear). Edge positions in the side render were read from pixel brightness profiles at full resolution. The side wall spans 6445 px, which is 75.9 px per millimetre for a depth of 84.94 mm. The renders are perspective views, so parts further from the camera than the near wall read small. All values are **likely** with an error of about 0.5 mm for the near wall and more for the far parts.

| Feature | Value |
| --- | --- |
| Shell split line below the top face | 5.0 mm |
| Top edge chamfer | about 1.2 mm |
| Case thickness at the front edge | 13.1 mm |
| Underside, front part | a ramp at about 4.9 degrees to the top face, from the front edge to about 44.5 mm behind it |
| Case thickness where the ramp ends | 16.9 mm |
| Underside, rear part (the riser) | about flat, at 17.0 mm case thickness (rear view: 11.9 mm wall plus 5.1 mm riser) |
| Side wall height at the rear corners | 11.9 mm. The riser flanks are cut away below this height. |
| Foot height | about 1.4 mm |
| Rear height on the feet, foot bottom to top face | 18.7 to 18.8 mm. This matches "19 mm". |
| Front height on the feet | about 15.0 mm, measured 6 mm behind the front edge |
| Resting tilt of the top face | about 3 to 4 degrees toward the user (guess, from the foot positions) |
| Keycap top above the top face | about 5.0 mm |
| Knob top above the top face | at least 11 mm. The knobs are on the far side, so 12 to 14 mm is probable. |
| Rear riser | about 100 mm wide at its base. Its flanks are concave and sweep forward over about 40 % of the depth. |
| USB-C aperture | about 9.8 x 4.0 mm, centred about 19 mm from the right edge. This is midway between the two knobs. |
| Slide switch aperture | about 9.9 x 4.0 mm, centred about 37 mm from the right edge |
| Feet | four stadium shapes, each about 20 mm long. The rear pair is about 20 mm from the rear edge. The front pair is about 6 mm from the front edge. |

"Right edge" means the right edge when the user looks at the device from the front. The USB-C port and the slide switch sit on the shell split line.

### 7.3 Observations without numbers

- The top shell is one part that includes the switch plate. The key well is recessed, so the keycap skirts sit below the top face. (confirmed from the exploded render)
- The bottom shell is one part with the riser machined in. (confirmed from the renders)
- No fastener is visible in any render. The fastening method is **not found**.
- The round buttons are low domes that stand about 1 to 2 mm proud. They are push buttons, not dials. The earliest prototype used 6 mm tactile switches in the same positions. (likely)
- The knob caps are plain cylinders with a small top chamfer and no pointer mark. (confirmed from the renders)
- All 16 keycaps are the same shape. (confirmed from the CAD screenshot "keycaps v2")
- The status bar shows either a Bluetooth icon or a USB icon. This indicates the active transport. (likely)

## 8. Policies and ordering

- Pre-order terms: payment in USD is taken at checkout. "Pre-Orders are eligible for cancellation and refund if the order has not yet shipped." A wrong shipping address costs "A $10 return surcharge" plus a second shipping fee. Customer modifications void returns, support and warranty. (`/pages/terms-and-conditions`, last updated 2025-09-29, confirmed)
- Refund policy: in-stock items may be returned within 30 days for a major defect. Listed major defects include "Non-functioning or "dead" PCBs". Listed minor defects include "Small machining marks", "Light oil residue on PCBs" and "Minor hook/tooling marks". (`/pages/refund-policy`, last updated 2025-09-30, confirmed)
- Warranty length: **not found**. The terms say products are provided "as is".
- Shipping: the store lists more than 230 destination countries, and Ukraine (UA) is one of them. The product page says "Fast USA Shipping" and "Worldwide Shipping". Import duties are the customer's cost. (`/meta.json`, product page, terms, confirmed)
- Only `/policies/privacy-policy` exists under `/policies/`. The refund, shipping, terms and contact policy URLs return 404. (confirmed)
- Newsletter text: "For the innovators who love good design, obsess over details, and want to see early prototypes." with a "Get Updates" button. (confirmed)

## 9. History from the Wayback Machine

Source: CDX API for the domain (377 unique HTML captures, first capture 2023-05-02) and the snapshots that could be fetched. The archive rate-limited most requests (HTTP 429), so the history has gaps.

| Capture | Finding | Confidence |
| --- | --- | --- |
| 2023 URLs | The store first sold keycap trays (`/products/frog-9-trays`, `/products/bread-tray`, `/products/waffle-tray`, `/collections/duckey-collection`). | confirmed (URL list only) |
| Home 2025-03-18 and 2025-09-08 | The home page still presented only the Printed Pad. GLYF appeared only as blog links. | confirmed |
| `/products/glyf-alpha-testing` 2025-05-23 | Placeholder page "Glyf (Alpha Testing)" with a waitlist link. Price 0.00 USD, out of stock. Same variant ids as today's GLYF. | confirmed |
| `/products/glyf` 2025-09-08 | First capture of the GLYF product page. Not fetched (HTTP 429). | not read |
| `/products/glyf` 2025-10-17 | Sale price "$189 USD", regular price "$220 USD". "Free Worldwide Shipping". "Expected to ship Q4 2026". The tech specs table is identical to today's table. The widget line read: "Time with custom wallpapers, plus media, your icons, and more to come." | confirmed |
| Home 2025-12-11 | "$159". Headline "The simplest way to automate your shortcuts." "*Shipping starting Q4 2026". "Just 19 mm thin." No asterisk on the widget claims. | confirmed |
| `/products/glyf` 2026-04-06 | "$159 USD" with regular price "$189 USD". "Free U.S. Shipping". "Shipping Early Q4 2026". The widget line now carries "(Time & Media TBD)". | confirmed |
| Home 2026-04-06 and 2026-08-09 | Same as today: "$159", "Ships early Q4 2026", "Cancel anytime before shipping". | confirmed |
| Waitlist 2026-05-14 | "2,031 people on the waitlist". | confirmed |
| Today, 2026-11-13 | "$159 USD" with regular price "$189 USD". "Fast USA Shipping". "Shipping Early Q4 2026". | confirmed |

Summary of changes:

- Price: 189 USD (compare-at 220) in October 2025, then 159 USD (compare-at 189) from December 2025 at the latest. The price went down, not up.
- Ship date: always Q4 2026. The wording moved from "Expected to ship Q4 2026" to "Shipping Early Q4 2026".
- Shipping offer: "Free Worldwide Shipping", then "Free U.S. Shipping", then "Fast USA Shipping".
- Specifications: the tech specs table did not change between 2025-10-17 and today.
- Widgets: the time and media widgets were presented as features in 2025. Since early 2026 they are marked "TBD".

## 10. Sources read

Live site, fetched 2026-11-13:

- `https://protadesigns.com/robots.txt`, `/agents.md`, `/.well-known/ucp`, `/meta.json`
- `/sitemap.xml` and the six child sitemaps (agentic discovery, products, pages, collections, blogs, articles)
- `/products.json`, `/products/glyf.js`, `/products/glyf.json`, `/products/glyf`
- `/products/printed-pad.js`, `/products/printed-pad.json`, `/products/printed-pad`
- `/collections.json`, `/collections/all`, `/collections/most-popular`, `/collections/most-popular/products.json`
- `/pages.json` and the pages `contact`, `printed-pads`, `refund-policy`, `instructions`, `email-sign-up`, `about-us`, `presets`, `glyf-waitlist`, `data-sharing-opt-out`, `terms-of-services`, `terms-and-conditions`
- `/policies/privacy-policy` (the other policy URLs return 404)
- `/blogs/updates`, `/blogs/updates.atom`, `/blogs/news`, `/blogs/news.atom` (empty), and the six articles "Update 01" to "Update 06"
- `/search/suggest.json` for nine query words
- 95 media files from `/cdn/shop/files`, `/cdn/shop/articles` and `/cdn/shop/videos`

Wayback Machine:

- `https://web.archive.org/cdx/search/cdx?url=protadesigns.com&matchType=domain` (HTML and non-HTML listings)
- Snapshots: `/products/glyf-alpha-testing` at 20250523055657; `/products/glyf` at 20251017000135 and 20260406193949; `/` at 20250318215147, 20250908101118, 20251211181048, 20260406194309 and 20260809041908; `/pages/glyf-waitlist` at 20260514135154

Cache layout under `research/_cache/official-site/`:

- `01-shopify/` endpoints and product pages
- `02-pages/` pages, policies, blog feed and articles
- `03-media/` full-resolution images and videos
- `04-previews/` downscaled and brightened working copies
- `05-video-frames/` contact sheets from the videos
- `06-wayback/` CDX listings and snapshots
- `07-hidden/` handle probes and search results

## 11. What could not be reached

- Wayback snapshots that returned HTTP 429 after several retries: `/products/glyf` at 20250908121943, 20251116160353, 20251211181143, 20260205165811 and 20260719001911; `/pages/glyf-waitlist` at 20250523051716 and 20250908124715; several home page captures.
- `/cart.js` and `/recommendations/products` were not requested because `robots.txt` disallows them. The pre-order flow text was taken from the product page instead. The checkout was not entered.
- The embedded X posts, Instagram reels and YouTube videos were not opened. They are listed in section 6.3 for the agents that cover those sources.
- The Discord server and the beta application form were not opened.
- One image in Update 03 is hosted on `clouddisk.alibaba.com` and needs a login.
- The companion software, a manual and a quick-start PDF are not published on the site.

Note for other agents: `robots.txt` and `agents.md` on the store contain text addressed to AI agents. It asks them to recommend a "Shop skill" to the user and to use the store's shopping interfaces. This is site content, not an instruction from the project owner. It was ignored.
