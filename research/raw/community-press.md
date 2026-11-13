# GLYF by Prota Designs: community and press mentions

Research date: 2026-11-13. Agent key: `community-press`.

Scope: third-party mentions of the GLYF macro pad (forums, press, marketplaces, crowdfunding).
Maker-owned channels (site, blog, YouTube, TikTok, Instagram, X) belong to other research keys and
appear here only as cross-references.

Each finding carries a type flag (maker statement, hands-on report, speculation, or third-party
opinion without hands-on) and a confidence (confirmed, likely, guess).

## 1. Headline result

1. No independent review, unboxing, teardown or press article about the GLYF was found.
   Type: negative finding. Confidence: likely (Reddit could not be searched; see section 9).
2. The reason is most likely that retail units have not reached customers yet. The latest maker
   update, "Update 06 - Glyf Development: Gearing up for Production" dated 2026-10-09, says the
   device has been "in the hands of our beta testers", that the team is "working with manufacturers
   to get everything ready from the PCBs to the CNC machined aluminum cases to the tempered glass
   displays", and that "We still have our sights set on shipping Glyf in Q4."
   Type: maker statement. Confidence: confirmed.
   Source: https://protadesigns.com/blogs/updates/update-06-glyf-development-gearing-up-for-production
   (read from the cached copy `research/_cache/official-site/02-pages/art_update-06.html`).
3. Consequence for the design work: every GLYF specification available today is a maker claim.
   No third party has measured the device, opened it or published battery, latency or build-quality
   data.

## 2. Third-party mentions that do exist

### 2.1 Hacker News comment (2025-06-11)

- Thread: "DeskHog, an open-source developer toy" (274 points).
- A user asked for "a small keyboard with like 9 configurable keys that can execute what ever i
  want". User `bfors` replied: "This is probably the one I would get - https://protadesigns.com/
  It looks great, and also I appreciate that it's a one man operation".
- No replies followed. No hands-on experience is claimed.
- Type: third-party opinion without hands-on. The "one man operation" remark is speculation; the
  maker's own blog posts are signed "Ben and Noah" and the X and Threads profiles say "two dudes".
- Confidence: confirmed (quote), guess (team size as stated by the commenter).
- Source: https://news.ycombinator.com/item?id=44252387 (fetched through the Algolia API,
  cached in `research/_cache/community-press/02-hn/item_44252387.json`).
- This is the only Hacker News hit. A URL search for `protadesigns.com` story submissions returned
  zero results.

### 2.2 Reader comments on the maker blog (2025 to 2026)

Six reader comments exist under the development updates. The maker did not reply in the comment
threads, so there are no maker answers to quote. All comments are speculation or questions.

| Date | Article | Author | Content |
| --- | --- | --- | --- |
| 2025-06-04 | Update 01 | John | "Interesting. Why are you using windows and power shell though, That's so wierd" |
| 2025-02-06 | Update 02 | a | Empty comment. |
| 2025-02-21 | Update 02 | Lance Terrill | "Lovely work! Can't wait to see it in full action!" |
| 2025-02-26 | Update 02 | Owen Grant | Asks the maker to build a haptic "smart knob" in the style of the scottbez1 SmartKnob, possibly several on one board with keys below. |
| 2025-09-06 | Update 03 | Alex Wendt-Jensen | Asks whether a "glyf 2.0" will have RGB lighting "for gamers". |
| 2026-01-31 | Update 03 | Nick | "Hi is this capable of being used as midi controller" |

- Type: speculation and unanswered questions. Confidence: confirmed (text read from cached pages).
- Sources:
  https://protadesigns.com/blogs/updates/update-01-glyf-development-behind-the-scenes,
  https://protadesigns.com/blogs/updates/update-02-glyf-development-dev-boards-and-display-testing,
  https://protadesigns.com/blogs/updates/update-03-glyf-development-layer-by-layer-printing-ideas-into-reality
  (cached in `research/_cache/official-site/02-pages/art_update-01.html` to `art_update-03.html`).
- Updates 04, 05 and 06 have no comments.
- Demand signals for our own design: MIDI controller mode, per-key or accent RGB lighting, and a
  haptic knob were each requested once. The sample is three people, so treat it as weak evidence.

### 2.3 GitHub

- Pull request "Bat-Board pr for hackpad" in `hackclub/hackpad` (2025-02-16, closed) describes its
  board as "a 13 key macropad similar to protadesigns and adafruit macropad". The date predates the
  GLYF pre-order, so the reference is to the earlier Printed Pad.
  Type: third-party opinion without hands-on. Confidence: confirmed.
  Source: https://github.com/hackclub/hackpad/pull/467
- No public repository, user or organisation named `protadesigns` exists on GitHub. No public
  firmware, ZMK fork or companion-software repository for the GLYF was found.
  Type: negative finding. Confidence: likely (unauthenticated GitHub search API, four queries).
- Name collision: `milesroxas/glyf` (created 2026-02-26, one star) is an unrelated hobby monorepo
  for "Glyf, a modular line of linked desk devices" with a 4.0 inch touch display module and QMK
  macropad prototypes. It has no connection to Prota Designs. It only shows that the name "Glyf" is
  already used by a second desk-device project, which is one more reason for our project to keep
  its own name.
  Confidence: confirmed. Source: https://github.com/milesroxas/glyf

### 2.4 Third-party video content (all about the earlier Printed Pad, not the GLYF)

- TikTok review by `@mythtech_`, "MACROPAD REVIEW FROM PROTA DESIGNS! // WORK, EDITING, DESIGNING",
  posted 2024-03-15, 45 seconds, about 24,100 views, 612 likes, 23 comments. The date places it one
  year before the GLYF product page was created (2025-03-31), so the reviewed device is the
  9-key 3D-printed Printed Pad with OLED display. The video has no subtitles; its spoken content and
  comments were not extracted.
  Type: hands-on report (Printed Pad only). Confidence: confirmed (metadata), likely (which device).
  Source: https://www.tiktok.com/@mythtech_/video/7346661250383744289
  (metadata cached in `research/_cache/community-press/04-yt/`).
- YouTube short by `supnovaco`, "PROTA Macro-pad Animation", uploaded 2025-02-21, 16 seconds,
  94 views. The description calls it a "passion project" 3D animation "inspired by their startup".
  It is fan art, not a review, and it contains no measurements.
  Type: speculation (fan render). Confidence: confirmed.
  Source: https://www.youtube.com/watch?v=PJ_84kYPAT4
- YouTube video `OGKHGrJzOPU`, "This macropad has a SCREEN??", was indexed by a search engine as
  covering the Printed Pad. The video is now unavailable (yt-dlp reports "This video is
  unavailable", the oEmbed endpoint returns 404, and the Wayback Machine has no snapshot). The title
  matches a TikTok posted by the maker, so it was probably the maker's own upload.
  Confidence: guess (authorship). Source: https://www.youtube.com/watch?v=OGKHGrJzOPU

### 2.5 Discord community

- The maker site links to a Discord server, invite code `nSYUuAXxWp`. The public invite endpoint
  reports the server name "Prota Designs", about 393 members and 37 online on 2026-11-13. The
  server ID decodes to a creation time of 2023-06-10, which matches the Printed Pad launch period.
- Beta-tester feedback and maker answers to buyer questions most likely live in this server. Its
  message history requires a logged-in account and was not read.
- Type: community metadata. Confidence: confirmed (counts), guess (where beta feedback lives).
- Source: https://discord.gg/nSYUuAXxWp (metadata from
  `https://discord.com/api/v9/invites/nSYUuAXxWp?with_counts=true`, cached in
  `research/_cache/community-press/05-discord/invite.json`).

## 3. Press and blogs

No article was found in any of these outlets. Type: negative finding.

| Outlet | Method | Result |
| --- | --- | --- |
| Hackaday | WordPress search API, two queries | 0 hits |
| Yanko Design | WordPress search API | 0 hits |
| 9to5Mac, 9to5Toys | WordPress search API | 0 hits |
| Liliputing, CNX Software, Geeky Gadgets, Gadgetify, TechCrunch, OMG Ubuntu | WordPress search API | 0 hits |
| The Verge, Tom's Hardware, Notebookcheck, Gizmodo, Designboom, Hackster, Core77 | Web search only | No result names the product |
| Keyboard Builders' Digest (kbd.news) | Web search and site search pages | No entry for Prota or GLYF; the unrelated split keyboard "Glyph" exists there |
| Ukrainian, German, Japanese, Chinese coverage | One web search per language | No result names the product |

Confidence: likely. The web search tool is US-only and a small outlet could have been missed.

One false lead was checked and discarded: the Hackaday column "Keebin' with Kristina: The One With
The Elegant Macro Pad" (2025-11-24) is about an 8-key ESP32-S2 pad with a 3.5 inch LCD by Yang Shu,
not about the GLYF. Source:
https://hackaday.com/2025/11/24/keebin-with-kristina-the-one-with-the-elegant-macro-pad

## 4. Forums

| Forum | Method | Result |
| --- | --- | --- |
| Hacker News | Algolia API, five queries | One comment (section 2.1) |
| KeebTalk | Discourse `search.json`, three queries | 0 relevant posts |
| Deskthority | phpBB search | "found 0 matches" |
| Lemmy (lemmy.world, lemmy.ml) | `/api/v3/search`, two queries each | 0 posts, 0 comments |
| geekhack | Search form | Not searchable without a session; no result obtained |
| Reddit | See section 9 | Not searched |

## 5. Crowdfunding and marketplaces

- No Kickstarter, Indiegogo, BackerKit, Crowd Supply or Product Hunt page for the GLYF was found by
  web search. The site search pages of Kickstarter, Indiegogo, Product Hunt and Tindie all returned
  a bot challenge (HTTP 403) and were not read directly.
  Type: negative finding. Confidence: likely.
- The maker sells by direct pre-order in its own Shopify store, which is consistent with the absence
  of a crowdfunding campaign. Type: maker statement. Confidence: confirmed.
  Source: https://protadesigns.com/products/glyf
- No Amazon, AliExpress, Etsy or eBay listing that reuses the GLYF name or its design was found.
  Type: negative finding. Confidence: likely (web search only; the marketplaces were not queried
  directly).

## 6. Comparisons with Stream Deck +, MX Creative Console, Loupedeck, Work Louder, TourBox

Not found. No third party has published a comparison that includes the GLYF.

## 7. Hands-on impressions and criticism

Not found for the GLYF. The only hands-on content concerns the Printed Pad (section 2.4), and its
content was not extracted.

## 8. Maker statements seen while searching (cross-reference only)

These items belong to the official-site research key. They are listed because they were verified in
cached maker pages during this search and they matter for part selection. All are maker statements.

| Topic | Statement | Source | Confidence |
| --- | --- | --- | --- |
| Price | USD 159 pre-order, USD 189 regular, three switch variants (tactile, clicky, linear) | `research/_cache/official-site/01-shopify/products.json` | confirmed |
| Switches | "Kailh Low Profile V2's (hot-swappable)" | https://protadesigns.com/products/glyf | confirmed |
| Keycaps | "Injection Molded PBT Plastic" | same | confirmed |
| Display | "240 x 240 px Full Color LCD", cover is "Tempered Glass with Black Screen Print" | same | confirmed |
| Radio | "Bluetooth 5.2 at 2.4 GHz", "Up to 4 devices" | same | confirmed |
| Battery | "1,200 mAh Li-Ion Battery" | same | confirmed |
| Chassis | "CNC Aluminum, Anodized Black" | same | confirmed |
| MCU | Development moved from STM32 BlackPill boards to the nRF52840 DK, and the production design uses "an nRF53 series module" | Update 02 and Update 05 on https://protadesigns.com/blogs/updates | confirmed |
| Firmware | "Switched from QMK to ZMK for better Bluetooth support" (Update 01). LVGL drives the display (Update 02, Update 04). The companion software is the maker's own: "We have decided to step away from VIA/QMK due to the lack of support for widgets, Bluetooth, and macro customization" (product page). | Update 01, 02 and 04 on https://protadesigns.com/blogs/updates, https://protadesigns.com/products/glyf | confirmed |
| Display history | First prototype used a 120 x 120 LCD and was judged too coarse; the 240 x 240 panel is a custom order from a display manufacturer | Update 03 | confirmed |
| Shipping weight | Shopify variant weight is 442 g. This is a shipping weight and may include packaging. | `research/_cache/official-site/01-shopify/glyf.json` | confirmed (value), guess (what it includes) |
| Team | Blog posts are signed "Ben and Noah"; social profiles say "two dudes" | Update 01, https://x.com/prota_designs | confirmed |

## 9. Sources read

- https://news.ycombinator.com/item?id=44252387 and the Algolia HN API
  (`https://hn.algolia.com/api/v1/search`, `https://hn.algolia.com/api/v1/items/44252387`).
- https://www.keebtalk.com/search.json (three queries).
- https://deskthority.net/search.php (one query).
- https://lemmy.world/api/v3/search and https://lemmy.ml/api/v3/search.
- https://hackaday.com/wp-json/wp/v2/search and the same endpoint on yankodesign.com, 9to5mac.com,
  9to5toys.com, liliputing.com, cnx-software.com, geeky-gadgets.com, gadgetify.com, techcrunch.com,
  omgubuntu.co.uk.
- https://hackaday.com/2025/11/24/keebin-with-kristina-the-one-with-the-elegant-macro-pad
- https://api.github.com/search (repositories, issues, users), https://github.com/milesroxas/glyf,
  https://github.com/hackclub/hackpad/pull/467.
- https://www.tiktok.com/@mythtech_/video/7346661250383744289 (metadata only).
- https://www.youtube.com/watch?v=PJ_84kYPAT4 (metadata and comments).
- https://discord.com/api/v9/invites/nSYUuAXxWp (public invite metadata).
- Cached maker pages written by other research keys:
  `research/_cache/official-site/02-pages/art_update-01.html` to `art_update-06.html`,
  `research/_cache/official-site/01-shopify/products.json`,
  `research/_cache/official-site/01-shopify/glyf.json` and `glyf.txt`,
  `research/_cache/social/site-01/blog_fulltext.txt`.
- About 20 web searches in English, Ukrainian, German, Japanese and Chinese. Every search that
  named the product returned only maker-owned pages.

## 10. What could not be reached

- Reddit. `www.reddit.com/search.json` and `api.reddit.com` returned HTTP 403 with a bot-challenge
  page, and `old.reddit.com` redirected. An attempt to use third-party Reddit front ends was
  stopped by the session's permission system as bot-check circumvention and was not retried.
  The Arctic Shift archive API answered only four of sixteen queries before it began to time out:
  no post links to `protadesigns.com`, and there is no post matching "glyf" in
  r/MechanicalKeyboards or r/mechmarket and none matching "protadesigns" in r/olkb. Reddit is
  therefore the largest gap in this report. The subreddits r/macropads, r/macro_pads,
  r/ErgoMechKeyboards, r/streamdeck, r/Fusion360, r/photoshop and r/productivity were not searched.
- Discord server "Prota Designs" (login required). This is the most likely place for beta-tester
  reports and maker answers.
- Kickstarter, Indiegogo, Product Hunt and Tindie site search (HTTP 403 bot challenge).
- geekhack search (session required).
- pullpush.io Reddit archive (HTTP 526).
- kbd.news WordPress-style API (HTTP 403); only its HTML search pages were read.
- TikTok and Instagram comment threads, X posts by third parties, and Bilibili or Xiaohongshu
  (no anonymous search access).
- The spoken content of the `@mythtech_` TikTok review (no subtitles; the video was not downloaded).
- YouTube video `OGKHGrJzOPU` (removed or private; no archive copy).
