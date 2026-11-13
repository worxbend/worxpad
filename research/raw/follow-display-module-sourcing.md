# Follow-up: display module sourcing (240 x 240 panel, flex, backlight, cover lens)

Date: 2026-11-13
Key: `follow-display-module-sourcing`
Cache: `research/_cache/follow-display-module-sourcing/` (sub-directories `01-dlc`, `02-allshore`, `03-yousee`,
`04-stock-panels`, `05-search`, `06-lcsc`)

Confidence words: **confirmed** (stated by a maker or read from a primary drawing or datasheet), **likely**
(consistent indirect evidence), **guess**. "Not found" means the search was made and returned nothing usable.

## 0. Short answer

1. The reference panel is not a one-off custom glass. It is a standard 1.4 inch 240 x 240 IPS module with a
   28.0 x 31.35 x 1.65 mm outline and a 25.2 x 25.2 mm active area. A second maker (Shenzhen Yousee, part
   YX14011A) publishes a drawing with the same outline, glass size, viewing area, active area and thickness.
   Only the flex tail differs (15 pins instead of 20). The custom part of the GLYF order was the bonded cover lens
   and the 20-pin flex. (confirmed for the match of dimensions; likely for "same glass")
2. The flex mark `FPC-TFT014H030-A0` and the earlier mark `ENH-TV0144006A` return no hit in any reachable index.
   The vendor behind them is **not found**.
3. No shop was found that sells the bare 28.0 x 31.35 mm 1.4 inch panel in single units with a listed price.
   Yousee sells by quotation. DigiKey stocks a 1.4 inch 240 x 240 part (DLC0140AZP03SF-1, 49 pieces, USD 36.03),
   but its product photo shows a breakout board with a 2.54 mm header, not a bare plug-in panel.
4. The panel that can be bought today in single units, with a public drawing and a plug-in 0.5 mm flex, is the
   1.3 inch 240 x 240 ST7789V panel (26.16 x 29.22 x 1.5 mm, active area 23.4 x 23.4 mm, 24-pin flex,
   USD 7.90 at DisplayModule). It is smaller than the reference module in every direction, so it fits the same
   pocket and the same 31.2 mm lens.
5. A printed glass cover lens in single units: **not found**. Glass makers quote a minimum of 100 pieces. The
   practical routes are a lens bonded by the display vendor (the GLYF route, USD 210 for five) or the family
   convention of a 1.0 mm clear cast acrylic lens with a black mask on the underside.
6. Consequence for the design: keep the 31.2 mm square lens and the 38.6 mm control column. Size the pocket for
   the 28.0 x 31.35 mm module. Choose the flex connector only after the panel is chosen, because the three
   candidate flexes (15, 20 and 24 pins) have different pin tables.

## 1. Reference panel, restated from the cached drawing

Source: `research/_cache/youtube/crops-01/sr0MIYEi678-f010-lcd-drawing-2x.png`,
`research/_cache/social/tiktok-frames-hd-01/lcd_q_right.jpg`,
`research/_cache/official-site/03-media/files__P2P_4_LCD0.jpg`. Read again for this note. Confidence: confirmed
(the drawing), unless stated.

| Item | Value |
| --- | --- |
| Title text | 1.4 inch, 240 x RGB x 240, "ALL O'clock" |
| Cover lens | 31.20 +/- 0.1 mm square, four corners R2.00, 1.100 mm thick |
| Backlight (module) outline | 28.00 +/- 0.15 mm wide, 31.35 +/- 0.15 mm high |
| LCD glass | 27.20 x 29.93 mm |
| Viewing area | 25.80 x 25.80 mm |
| Active area | 25.20 x 25.20 mm |
| Offsets from lens edge (top and sides) | 1.60 mm to module, 2.00 mm to glass, 2.70 mm to viewing area, 3.00 mm to active area |
| Stack | lens 1.100 + OCA 0.200 + module 1.65 +/- 0.15 = 2.950 +/- 0.15 mm |
| Flex tail | 20 contacts, 0.50 mm pitch, 0.30 mm pad, 9.50 mm across contacts, 10.50 mm tail width, 3.50 mm contact length, 5.00 mm stiffener, 0.30 mm thick at the stiffener |
| Tail position | 17.30 +/- 0.5 mm below the module edge; 8.75 mm from each module side (8.75 + 10.50 + 8.75 = 28.00, so the tail is centred on the module) |

Derived, not printed on the drawing (confidence: confirmed arithmetic):

- The active area is centred in the lens (3.00 mm margin on all four sides).
- The module extends 1.75 mm past the lower lens edge (1.60 + 31.35 - 31.20). The case pocket under the lens
  must be open on the flex side by at least that much.
- The bare panels in the flex photo have no lens. The mark `FPC-TFT014H030-A0` is printed on the flex of the
  bare module, so the mark belongs to the display module maker, not to the lens bonder. (confirmed from the photo)

## 2. Flex-mark lookup

| Query | Where | Result |
| --- | --- | --- |
| `"TFT014H030"`, `"FPC-TFT014H030-A0"` | WebSearch (two queries) | No page contains the string. |
| `"ENH-TV0144006A"`, `"TV0144006A"`, `"ENH-TV"` | WebSearch (two queries) | No page contains the string. The search only surfaces generic Alibaba LCD suppliers. |
| The same five strings | html.duckduckgo.com | Blocked by a bot challenge page. No result. |
| `TFT014H030`, size 1.4 inch with 240 x 240 | panelook.com model search | Blocked by a slider verification page. No result. |

Conclusion: the vendor of the reference panel is **not found** from public sources. The mark reads as
"FPC, TFT, 0.14 (1.4 inch), H030, revision A0", which is a flex drawing number and not a catalogue part number
(guess). A flex drawing number is normally not indexed anywhere.

## 3. Same-glass module with a public datasheet: Yousee YX14011A

Source: https://www.directindustry.com/prod/shenzhen-yousee-technology-co-ltd/product-4621447-2851356.html and
the 20-page specification at
https://pdf.directindustry.com/pdf/shenzhen-yousee-technology-co-ltd/yousee-display-module-tft-lcd-yx14011a/4621447-1146135.html
(pages 4 to 8 cached as `03-yousee/yx14011a-p4b.jpg` to `p8b.jpg`; enlarged crop `03-yousee/crop-front.png`).
Confidence: confirmed (maker datasheet), unless stated.

| Item | YX14011A | Reference drawing |
| --- | --- | --- |
| Size, resolution | 1.4 inch, 240 (RGB) x 240, IPS, all o'clock | same |
| Module outline | 28 (W) x 31.35 (H) x 1.65 (T) mm, thickness tolerance +/- 0.05 | 28.00 x 31.35 x 1.65 mm, thickness tolerance +/- 0.15 |
| LCD glass | 27.2 x 29.93 mm | 27.20 x 29.93 mm |
| Viewing area | 25.8 x 25.8 mm | 25.80 mm |
| Active area | 25.2 x 25.2 mm, pixel pitch 0.105 mm | 25.20 mm |
| Edge offsets (top and sides, from module edge) | 0.4 mm to glass, 1.1 mm to viewing area, 1.4 mm to active area | 0.40, 1.10, 1.40 mm (after subtracting the 1.60 mm lens overhang) |
| Controller | ST7789V | ST7789V-compatible (firmware strings, `regulatory-software.md`) |
| Interface | 4-wire SPI only | SPI |
| Flex | 15 contacts, 0.5 mm pitch, 0.3 mm pad, 7 mm across contacts, 8 mm tail width, tail end 29.61 mm from the module edge, tail 10.00 mm from each module side (centred), 5 mm stiffener | 20 contacts, 10.50 mm wide, 17.30 mm long |
| Supply | VCC 2.8 to 3.6 V (3.3 V typical); IOVCC 1.65 to 3.6 V | not stated |
| Backlight | 3 white LEDs in parallel; Vf 3.3 V typical at 60 mA total (20 mA per LED) | not stated |
| Luminance | 1000 cd/m2 typical (maker claim), contrast 500, response 25 ms | not stated |
| Temperature | -20 to +80 C operating | not stated |

Pin table of the 15-pin flex (confirmed, page 6):

| Pin | Symbol | Function |
| --- | --- | --- |
| 1 | K | Backlight cathode |
| 2 to 5 | NC | Not connected |
| 6 | A | Backlight anode |
| 7 | VCC | Supply |
| 8, 9 | GND | Ground |
| 10 | SDA | Serial data in/out |
| 11 | SCL | Serial clock |
| 12 | CS | Chip select, active low |
| 13 | RS | Data (high) or command (low) |
| 14 | RST | Reset, active low |
| 15 | NC | Not connected |

Design notes printed on the Yousee drawing (confirmed):

- A lens or touch panel should keep at least 0.3 mm gap to the top of the polariser if it is not bonded.
- If the case has no foam gasket, the black-print window of the lens should be at most 0.6 mm per side larger
  than the active area. That gives a window of at most 26.4 mm. The reference lens uses the 25.8 mm viewing area.
- If the case has a foam gasket, the gasket should overlap the module by at least 0.5 mm per side.
- The rear face carries 0.05 mm black tape, and the drawing shows a double-sided foam tape of 0.5 mm.

Price and minimum order for YX14011A: **not found**. The listing has a quotation form only. The company page on
DirectIndustry returned HTTP 403 to the fetch tool.

## 4. Other 1.4 inch 240 x 240 modules found

| Part | Outline (mm) | Active area (mm) | Controller | Flex | Backlight | Buy | Source, confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Allshore ASI-T-1402A8SCN/A | 30.00 x 35.00 x 2.20 (metal frame with ears) | 25.20 x 25.20 | ST7789V2 | 20 contacts, 0.5 mm pitch, 9.5 mm across contacts, 10.5 mm wide, 3.5 mm contact, 5.0 mm stiffener, 0.30 mm thick, tail 27.55 mm long | 2 LEDs in series, 6.4 V typical (5.4 to 6.8 V) at 20 mA, 128 mW; 800 cd/m2 typical | Quotation only; price not found | Datasheet rev 1.0 (2020-03-13), archived copy cached at `02-allshore/ASIT1402A8SCN.pdf`; confirmed |
| DLC Display DLC0140AZP03SF-1 | not found (datasheet blocked) | 25.20 x 25.20 | ST7789V2 | Product photo shows a PCB breakout with an 8-pin 2.54 mm header (GND, VCC, SCL, SDA, RES, DC, CS, BLK) and silk "1.4' 240*240 TFT_LCD" | not found | DigiKey: 49 in stock, minimum 1, USD 36.03 (1), 29.335 (10), 25.4696 (100), maker lead time 10 weeks. RCS Components (Kyiv): 2,410.35 UAH without VAT (1), 1,889.51 UAH (10), to order, 21 to 31 days | DigiKey page JSON and photo cached in `01-dlc/`; RCS page in `04-stock-panels/rcs-dlc.html`; confirmed |
| HEM (Huarsun) LCM-T1D4HP-056C | 27.4 x 30.23 x 1.61 | 24.35 x 24.35 | ST7789P3 | not stated on the page | 3 LEDs, 60 mA typical (page says "serial" and "3.2 V", which do not agree; parallel is likely); 550 cd/m2 | Quotation only | https://www.hemlcd.com/products/tft/small-and-medium-size/lcm-t1d4hp-056c.html; confirmed (page), guess (LED wiring) |

Two facts from this table matter:

- "1.4 inch 240 x 240" is not one mechanical part. At least three outlines exist (28.0 x 31.35, 27.4 x 30.23,
  30 x 35 framed) and two active areas (25.2 and 24.35 mm). A substitute must be checked against the drawing.
- Backlight wiring differs between vendors: three LEDs in parallel at about 3.3 V and 60 mA (Yousee), or two LEDs
  in series at 6.4 V and 20 mA (Allshore). A series backlight needs a boost driver. The backlight of the GLYF
  reference panel is **not found**.

### 20-pin pin table of the Allshore module (reference only)

The tail geometry of the Allshore flex (20 contacts, 9.5 mm, 10.5 mm, 3.5 mm, 5.0 mm, 0.30 mm) equals the tail
geometry on the GLYF drawing. That is the generic geometry of any 20-way 0.5 mm flex, so it does not prove that
the pin table is the same. Confidence that the GLYF flex uses this pin table: guess.

| Pin | Symbol | Function (datasheet wording, shortened) |
| --- | --- | --- |
| 1 | LEDA | Backlight anode |
| 2 | LEDK | Backlight cathode |
| 3 | VDD | Supply, 2.4 to 3.3 V (2.8 V typical) |
| 4 | GND | Ground |
| 5 | IMX | Interface select (IM1 and IM2 shorted): 0 = 8-bit parallel, 1 = 4-line SPI |
| 6 | SDA | SPI data |
| 7 | /CS | Chip select, active low |
| 8 | RESET | Reset, active low |
| 9 | RD | Read strobe (parallel); tie to VDD or GND if unused |
| 10 | WR | Write strobe (parallel); data/command select in 4-line SPI |
| 11 | RS | Register select (parallel). In 4-line SPI the ST7789 uses this pad as the serial clock; the Allshore table does not say so. |
| 12 to 19 | D7 to D0 | Parallel data; unused in SPI |
| 20 | GND | Ground |

## 5. Stock 240 x 240 substitutes with a plug-in flex

### 5.1 1.3 inch, 24-pin plug-in flex (recommended prototype panel)

Source: https://www.displaymodule.com/products/1-3-inch-ips-display-240x240-with-spi, product JSON
(`04-stock-panels/dm-1-3-inch-ips-display-240x240-with-spi.js`), datasheets `DM-TFT13-377P24.pdf` (maker part
LH133T-IF05) and `DM-TFT13-377panel.pdf`. Confidence: confirmed.

| Item | Value |
| --- | --- |
| Outline | 26.16 x 29.22 x 1.5 mm (maximum thickness) |
| Active area | 23.4 x 23.4 mm, pixel pitch 0.0975 mm |
| Controller | ST7789V (datasheet for ST7789VW linked by the seller) |
| Interface | 4-line SPI or 8-bit 8080, selected by pin 6 |
| Supply | VDD 2.4 to 3.3 V (2.8 V typical); VDDIO 1.65 to 3.3 V; 8 mA typical, 10 mA maximum |
| Backlight | 2 white LEDs in parallel, 30 to 40 mA at 2.8 to 3.0 V |
| Luminance | 250 cd/m2 (seller page) |
| Flex | 24 contacts, 0.5 mm pitch, plug-in; tail 12.8 +/- 0.5 mm from the module edge; 0.3 mm thick at the 4 mm stiffener; solder bump on the back up to 0.45 mm |
| Window advice | Case window 0.5 mm per side larger than the active area (24.4 mm) |
| Price, stock | USD 7.90 each for "Panel-24pin" (SKU DM-TFT13-377p24), listed as available, no minimum quantity shown |
| Other variants | "Panel-12pin" (SKU DM-TFT13-377p12, USD 7.90): the 12-pin flex is a solder-down tail ("solder joint height 0.4 mm max"), not a plug-in tail. "Module" on a PCB: USD 9.90. |

Pin table of the 24-pin flex and the wiring for 4-line SPI (confirmed, datasheet page 5):

| Pin | Symbol | SPI wiring |
| --- | --- | --- |
| 1 | LEDA | Backlight anode |
| 2 | LEDK | Backlight cathode |
| 3 | GND | Ground |
| 4 | VDD (2.8 V) | Supply, 2.5 to 3.3 V |
| 5 | VDDIO | I/O supply, 1.65 to 3.3 V |
| 6 | IM1/2 | Tie to VDDIO for SPI |
| 7 | RESET | Reset, active low |
| 8 | CS | Chip select, active low |
| 9 | D/C (parallel name) | Serial clock in SPI |
| 10 | WR (parallel name) | Data/command select in SPI |
| 11 | RD | Tie to ground |
| 12 | SDA | Serial data |
| 13 to 20 | DB0 to DB7 | Tie to ground |
| 21 | TE | Tearing-effect output (optional) |
| 22 | NC | Not connected |
| 23, 24 | GND | Ground |

Fit against the reference pocket: the 1.3 inch module is 1.84 mm narrower and 2.13 mm shorter than the 1.4 inch
module, and 0.15 mm thinner. It needs a locating frame or tape in a pocket made for 28.0 x 31.35 mm. Its flex
is 4.5 mm shorter than the reference flex (12.8 mm against 17.3 mm), so the slot and the bottom-side connector
must sit closer to the module edge, or the flex must fold back under the module.

### 5.2 1.54 inch, 12-pin plug-in flex

Source: https://dl.espressif.com/AE/esp-dev-kits/胶铁一体ZJY154KC-IF17.pdf (Zhengzhou Zhongjingyuan, version A,
2021-07-13; cached `04-stock-panels/ZJY154KC-IF17.pdf`). Confidence: confirmed.

| Item | Value |
| --- | --- |
| Outline | 31.52 +/- 0.1 x 33.72 +/- 0.1 x 1.9 +/- 0.1 mm |
| LCD glass, polariser | 30.12 x 33.12 mm; 29.72 x 30.12 mm |
| Active area | 27.72 x 27.72 mm, pixel pitch 0.1155 mm |
| Controller | ST7789V3, 4-line SPI only |
| Supply | 2.5 to 3.3 V (2.8 V typical), 8 mA typical, sleep 15 uA typical |
| Backlight | 3 white LEDs in parallel, 60 mA typical (90 mA maximum) at 2.8 to 3.2 V; 400 cd/m2 typical |
| Flex | 12 contacts, 0.5 mm pitch, 6.50 +/- 0.1 mm wide, 0.3 mm thick, tail 25.00 +/- 0.3 mm from the module edge |
| Pin table | 1 GND, 2 LEDK, 3 LEDA, 4 VDD, 5 GND, 6 GND, 7 D/C, 8 CS, 9 SCL, 10 SDA, 11 RESET, 12 GND |
| Window advice | Case window 0.3 mm per side larger than the active area |
| Price | not found (the maker sells through a Taobao shop named in the datasheet; resellers were not reachable) |

Fit: the module is 31.52 mm wide, which is wider than the 31.2 mm reference lens. With a 1.6 mm lens overhang per
side the lens grows to about 34.7 mm, and the walls of a 38.6 mm column shrink to about 1.95 mm per side. It fits,
but it changes the lens, the pocket and the proportions of the column.

### 5.3 LCSC and the JLCPCB parts library

Source: JLCPCB parts search API, queried 2026-11-13 (responses cached in `06-lcsc/jlc-q*.json`). Confidence:
confirmed for the day of the query.

- No 240 x 240 panel is in stock. The 240 x 240 entries are resold parts from Western distributors at zero stock:
  AZ Displays ATM0130B3 (1.3 inch, USD 18.62), AZ Displays ATM0154B1 (1.54 inch, USD 23.01), Focus Display
  E13RG62424LWAM450-N (USD 59.38), Focus Display E15RA-FW255-N (USD 38.00), Adafruit 3787 (USD 49.42).
- The in-stock small TFT panels are 320 x 240 parts of brand "HS" (2.0 to 3.2 inch).
- The display therefore cannot be a JLCPCB-assembled part. It is a hand-fitted item. Only the flex connector
  goes on the assembly bill of materials.
- The LCSC public search endpoint returned an error body ("The static resource is unavailable"), so LCSC was
  checked only through the JLCPCB library.

DigiKey lists AZ Displays ATM0130B3 (1.3 inch) with 366 in stock at USD 13.27 (seen in the "also evaluated" block
of the cached DigiKey page). Its drawing was not opened. Confidence: likely.

## 6. Comparison

| Candidate | Outline W x H x T (mm) | Active area (mm) | Flex | Backlight | Single-unit price | Fits 31.2 mm lens and 38.6 mm column |
| --- | --- | --- | --- | --- | --- | --- |
| GLYF reference (custom order) | 28.00 x 31.35 x 1.65, plus bonded 31.2 mm lens (2.95 total) | 25.2 | 20 x 0.5 mm, 17.3 mm long | not found | USD 42 each (USD 210 for five, with lens) | yes (definition) |
| Yousee YX14011A | 28 x 31.35 x 1.65 | 25.2 | 15 x 0.5 mm, 29.61 mm long | 3 LEDs parallel, 3.3 V, 60 mA | not found (quotation) | yes, same pocket |
| DisplayModule DM-TFT13-377p24 (1.3 inch) | 26.16 x 29.22 x 1.5 | 23.4 | 24 x 0.5 mm, 12.8 mm long | 2 LEDs parallel, 2.8 to 3.0 V, 30 to 40 mA | USD 7.90 | yes, with a locating frame; window 24.4 mm |
| ZJY154KC-IF17 (1.54 inch) | 31.52 x 33.72 x 1.9 | 27.72 | 12 x 0.5 mm, 25.0 mm long | 3 LEDs parallel, 2.8 to 3.2 V, 60 mA | not found | only with a lens of about 34.7 mm |
| DLC0140AZP03SF-1 (DigiKey) | not found | 25.2 | on a PCB with 2.54 mm header | not found | USD 36.03 | no (PCB breakout), unless the datasheet shows otherwise |
| Allshore ASI-T-1402A8SCN/A | 30.00 x 35.00 x 2.20 | 25.2 | 20 x 0.5 mm, 27.55 mm long | 2 LEDs series, 6.4 V, 20 mA | not found | no (frame is 35 mm high and 2.2 mm thick) |

## 7. Cover lens

| Route | Evidence | Minimum order | Confidence |
| --- | --- | --- | --- |
| Lens bonded by the display vendor (tempered glass, black print, OCA) | The GLYF maker paid USD 210 for five modules with bonded glass (`youtube.md`, `social.md`). The supplier drawing in section 1 is the result. | 5 pieces documented | confirmed |
| Printed tempered cover glass from a glass maker | Saida Glass product page "1mm black printed cover glass for TFT display screen": "Min.Order Quantity: 100 Piece/Pieces", FOB price range "US $0.5 - 9,999 / Piece", order by inquiry with a drawing. https://www.saidaglass.com/1mm-black-printed-cover-glass-for-tft-display-screen.html | 100 pieces | confirmed (page) |
| Other glass makers | CDTech: silk-screened lens minimum "from 100pcs" plus tooling fee. Elecrow custom screen: 300 to 500 pieces. Fuxin Glass: "low MOQ" samples, no number. Read from search summaries only; the pages were not opened. | 100 or more | likely |
| Printed glass lens in one to five pieces from a shop with a price list | Searched; nothing found. | **not found** | - |
| Clear cast acrylic, 1.0 mm, black mask on the underside | Family convention: `/home/worxbend/Projects/macropad/cad/README.md` lines 52, 123 and 351 specify a clear cast acrylic lens of 1.0 mm with a black mask on the underside, exported as `lens.dxf` and `lens_mask.dxf`. The sibling README marks the thickness as a guess. | 1 piece (laser cut or hand cut) | confirmed (convention), guess (supplier) |
| CNC-machined PMMA at JLCCNC | JLCCNC machines PMMA and offers transparent polishing; its guide advises walls above 1.5 to 2 mm (search summary of https://jlccnc.com/blog/acrylic-and-pmma-cnc-machining; the help article https://jlccnc.com/help/article/pmma-acrylic-cnc-machining lists material properties only, no thickness limit). | 1 piece | likely |

Conclusion for the lens:

- For the printed prototype and the first aluminium sample, use the family convention: a 31.2 x 31.2 mm, R2.0,
  1.0 mm clear cast acrylic lens with a black mask on the underside. The mask window is 25.8 mm for a 25.2 mm
  active area, or 24.4 mm for the 1.3 inch panel.
- A real printed-glass lens needs either a batch of 100 pieces from a glass maker or a quotation from the display
  vendor for a bonded lens. Both are quotation items, not catalogue items.
- Keep the lens recess depth as a parameter. Glass from the reference is 1.1 mm. Cast acrylic sheet is 1.0 mm.
  JLCCNC PMMA is likely to need 1.5 mm or more.

## 8. What this fixes in the design

1. **Lens and window.** Lens 31.2 x 31.2 mm with R2.0 corners. Lens recess 31.4 x 31.4 mm (family `lens_fit` of
   0.1 mm per side, `conventions.md`). Visible window 25.8 x 25.8 mm for the 1.4 inch panel. (confirmed inputs)
2. **Module pocket.** Under the lens, a pocket for 28.0 x 31.35 x 1.65 mm with clearance. The module starts
   1.60 mm below the upper lens edge and ends 1.75 mm past the lower lens edge. The flex leaves at the centre of
   the lower module edge. (confirmed arithmetic from the drawing)
3. **Control column.** 38.6 mm stays valid: 31.2 mm lens plus 3.7 mm per side. The 1.54 inch panel is the only
   candidate that would press on this number. (confirmed arithmetic)
4. **Depth.** Lens top to module back is 2.95 mm with the bonded glass. With a loose 1.0 mm acrylic lens, 0.13 mm
   tape and the 0.3 mm air gap advised by Yousee, the stack is about 1.0 + 0.3 + 1.65 = 2.95 mm as well. The
   1.3 inch panel is 1.5 mm thick, which gives 2.8 mm. (confirmed inputs, likely for the acrylic stack)
5. **Connector.** The pin count is not fixed by the reference. Choices: 24-way 0.5 mm for the 1.3 inch stock
   panel (buyable now), 15-way 0.5 mm for YX14011A (quotation), 20-way 0.5 mm for a custom copy of the reference
   (quotation, pin table unknown). All tails are 0.3 mm thick, so the same connector family fits. The slot
   position depends on the tail length: 12.8 mm (1.3 inch), 17.3 mm (reference), 29.61 mm (YX14011A).
6. **Backlight drive.** Design for a parallel white-LED backlight at about 3.0 to 3.3 V: 30 to 40 mA for the
   1.3 inch panel and 60 mA for the 1.4 inch and 1.54 inch panels at full brightness. A 3.3 V rail leaves little
   or no headroom over a 3.3 V LED, so the backlight will run below its rated current from that rail. A low-side
   switch with PWM and a series resistor is enough. Do not assume a parallel backlight for an unknown 1.4 inch
   panel: the Allshore part needs 6.4 V.
7. **Firmware.** Every candidate is an ST7789V-family 240 x 240 panel with 4-wire SPI. The reference firmware
   settings in `regulatory-software.md` (RGB565, inversion on, 20 MHz) apply to all of them. (likely)

## 9. Sources read

- Cached project files: `research/raw/youtube.md`, `social.md`, `official-site.md`, `regulatory-software.md`,
  `conventions.md`; the three reference images named in section 1; `/home/worxbend/Projects/macropad/cad/README.md`.
- https://www.directindustry.com/prod/shenzhen-yousee-technology-co-ltd/product-4621447-2851356.html
- https://pdf.directindustry.com/pdf/shenzhen-yousee-technology-co-ltd/yousee-display-module-tft-lcd-yx14011a/4621447-1146135.html (page images 4 to 8)
- https://www.digikey.com/en/products/detail/dlc-display-co-ltd/DLC0140AZP03SF-1/24764445 (page JSON and product photo)
- https://www.rcscomponents.kiev.ua/product/dlc0140azp03sf-1.html
- https://web.archive.org/web/20260203001938/https://www.allshore.com/portals/0/PDFs/ASIT1402A8Scna.pdf
- https://www.hemlcd.com/products/tft/small-and-medium-size/lcm-t1d4hp-056c.html
- https://www.displaymodule.com/products/1-3-inch-ips-display-240x240-with-spi and its two panel datasheets on cdn.shopify.com; https://www.displaymodule.com/products.json (catalogue listing)
- https://dl.espressif.com/AE/esp-dev-kits/胶铁一体ZJY154KC-IF17.pdf
- JLCPCB parts search API (`https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList/v2`), 14 keyword queries
- https://www.saidaglass.com/1mm-black-printed-cover-glass-for-tft-display-screen.html
- https://jlccnc.com/help/article/pmma-acrylic-cnc-machining
- WebSearch result summaries for the flex marks, 1.4 inch panels, cover glass makers and PMMA machining.

## 10. Not reached

- DLC0140AZP03SF-1 datasheet. The viewer page at dlcdisplay.com loads the PDF from a file host that answers
  HTTP 403 to a plain request. The outline, pin table and backlight of the DigiKey part are therefore unknown.
- panelook.com (slider verification) and html.duckduckgo.com (bot challenge). No second search index was available.
- buydisplay.com (HTTP 403 from a challenge page) for ER-TFT1.3 and ER-TFT1.54 panels.
- allshore.com directly (connection refused or timed out). The archived datasheet was used instead.
- alibaba.com and aliexpress.com product pages (empty body without a browser). No single-unit listing for a
  1.4 inch 240 x 240 bare panel could be read.
- LCSC public search endpoint (error body).
- Yousee company page on DirectIndustry (HTTP 403 to the fetch tool). Price, minimum order and lens-bonding
  service for YX14011A are unknown.
- Glass maker pages other than Saida (only search summaries were read).
