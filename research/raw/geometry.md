# GLYF geometry reconstruction from images

Date of research: 2026-11-13.
Agent key: `geometry`.
Scope: outer and inner geometry of the GLYF macro pad by Prota Designs, measured from maker images, maker video frames and maker drawings. No unit was handled.
Cache root: `research/_cache/geometry/` (gitignored). Scripts, overlay specs and overlays are listed in section 9.

Confidence labels:

- **confirmed**: stated by the maker, or read directly from a maker drawing with a scale that two maker sources fix.
- **likely**: measured from a maker render or a maker CAD video frame, with a cross-check from a second image.
- **guess**: derived from a stack-up, a single weak image, or reasoning.
- **not found**: no source gives it.

No vendor artwork, 3D model, firmware or software was copied into the repository. Every number in this file is a measurement or a calculation.

## 1. Headline results

1. The body is 120.4 x 85.2 mm in plan, with 2.0 mm vertical corner radii and a 1.0 mm chamfer on the top edge. (likely)
2. The key pitch is 19.05 mm in both axes. Choc spacing (18 x 17 mm) does not fit. (confirmed)
3. The maker's "19 mm" is the maximum body thickness: 19.2 mm at the wedge apex, measured square to the top face, without feet, keycaps or knobs. (likely)
4. The body is a wedge. It is 13.0 mm thick at the front edge and 12.0 mm at the rear wall. The underside is one flat ramp at 4.95 degrees that reaches 19.2 mm at 12.7 mm from the rear face, then a 29 degree slope back up to the rear wall. (likely)
5. On the desk the top face tilts 5.0 degrees toward the user. The top face is 14.9 mm above the desk at the front edge and 22.3 mm at the rear edge. The knob tops are 32.8 mm above the desk. (likely)
6. Keycap tops stand 4.4 mm above the top face. Knob tops stand 11.8 mm above it. The two round buttons stand 1.0 mm above it. (likely)
7. The display opening is a square 31.2 x 31.2 mm cover lens with 2.0 mm corner radii. The active area is 25.2 x 25.2 mm (1.4 inch, 240 x 240). The display is not portrait. (confirmed)
8. The case is two CNC shells split on a plane 5.0 mm below the top face. Four M2-class screws pass through the key well floor between key columns 1-2 and 3-4, hidden by the keycaps. (likely)
9. The object behind the pad in the hero render is a second pad lying upside down. There is no dock. (likely)

## 2. Sources used

Paths are relative to `research/_cache/`.

| Id | Source | Type | Used for |
| --- | --- | --- | --- |
| S1 | `official-site/03-media/files__GLYFCABLESVG3.svg` (`https://protadesigns.com/cdn/shop/files/GLYFCABLESVG3.svg?v=1755130377`) | Maker vector line drawing, orthographic top view, dated 2025-08-14 by its version stamp | All plan dimensions |
| S2 | `youtube/crops-01/sr0MIYEi678-f010-lcd-drawing-2x.png` (video `sr0MIYEi678`) | Supplier drawing of the display, shown on screen by the maker | Lens 31.20 mm, active area 25.20 mm, stack 2.95 mm. Scale reference 1 |
| S3 | `youtube/crops-01/ScYz1Z_T1UY-f015-kicad-dimension-2x.png` (video `ScYz1Z_T1UY`) | Maker KiCad layout frame | "19.05 spacing" label, 112.5 mm board dimension, mounting hole positions. Scale reference 2 |
| S4 | `geometry/yt-frames-01/Q6/t54_11.png` (video `Q6CKpc6AK0o` at 56.5 s, re-downloaded at 1080 x 1920) | Maker Fusion 360 side view, orthographic, file title "Mock Design" | All heights and the underside profile |
| S5 | `official-site/03-media/files__3_2c90c273-...jpg` (4000 x 2000) | Rear render, perspective | USB-C scale check, port positions, rear wall, rear feet |
| S6 | `official-site/03-media/files__Untitled_design_13.jpg` (6500 x 2300) | Left side render used for the "19 mm" claim, perspective | Cross-check of wall, split line, cap height |
| S7 | `official-site/03-media/files__1_ab7debeb-...jpg` (4000 x 2000) | Front render, perspective | Front wall, front feet |
| S8 | `official-site/03-media/files__Desktop_Size_Grid_1_46ae2ac8-...jpg` (3000 x 2000) | Exploded shell render | Key well depth, plate cut-outs, screw holes |
| S9 | `geometry/yt-frames-01/Ly/f019.png` (video `LyKoZR8Q888` at 18.5 s) | Photo of a real anodised bottom shell, inside | Screw bosses, wall, pockets |
| S10 | `geometry/yt-frames-01/Q6/t54_17.png` (video `Q6CKpc6AK0o` at 58 s) | Photo of a real unit, face on | Check that the real unit matches S1 |
| S11 | `user/site-hero-and-essentials.png`, `user/site-side-profile-19mm.png` | Owner screenshots | Orientation, the "dock" question |
| S12 | `research/raw/official-site.md`, `research/raw/youtube.md`, `research/raw/social.md`, `research/raw/regulatory-software.md` | Notes of the finder agents | Maker statements quoted below |
| S13 | `official-site/03-media/files__prod_7c6895ff-3732-432d-bb54-e42f7affdd6c.png` (5000 x 5000) | Product render: front unit plus a second unit upside down behind it, perspective | Foot plan shape and length, the "dock" question |
| S14 | `geometry/yt-frames-01/4m/f015.png` (video `4mGhEPTLoSA`, uploaded 2025-06-25) | Photo of a caliper on a moulded strip of silicone feet | Foot length cross-check |

Downloads made for this task: three maker shorts at 1080 x 1920 (`Q6CKpc6AK0o`, `LyKoZR8Q888`, `4mGhEPTLoSA`) in `geometry/yt-hd-01/`, and frames cut from them in `geometry/yt-frames-01/`.

## 3. Method

### 3.1 Coordinate system

- Plan origin: the rear left outer corner of the body, seen from above with the keys on the left. X runs to the right. Y runs toward the user (rear to front).
- Grid origin: the centre of the rear left key. Grid coordinates are given as (x, y) in the same directions.
- Heights are measured square to the top face. The top face (the "deck") is 0. Up is positive.
- "Right edge" is the edge beside the knobs.

### 3.2 Plan view

S1 is a hidden-line export of the CAD model. The keycap tops are centred on the keycap bases, so the view is orthographic. Stroke centre lines were read by rasterising the drawing at 8 pixels per unit and taking the centre of each bright run along chosen scan lines (`scripts/line_centres.py`). Element bounding boxes were read from the SVG geometry (`scripts/svg_bboxes.py`). Reading error is 0.06 units, which is 0.01 mm.

### 3.3 Heights

S4 is an orthographic CAD view. The proof is that the two knobs and the four keycap columns each collapse into one silhouette, and no top face is visible. The frame is a 1080 x 1920 video frame, so one pixel is 0.104 mm. Edges were located as the centroid of the brightness gradient along a row or column band (`scripts/edges.py`). Edge error is about 1.5 pixels, which is 0.16 mm.

### 3.4 Perspective renders

The renders S5 to S8 are perspective views. Three rules were applied.

1. A length is scaled only against a known length in the same plane. The near wall of each view carries the scale: body width 120.38 mm for S5 and S7, body depth 85.16 mm for S6.
2. The camera pitch was taken from the ratio of the vertical and horizontal scale on the near wall. For S5 the rear wall is 384.7 px high and 12.0 mm (from S4), against 32.24 px/mm horizontally. That gives a pitch of 5.1 degrees. The USB-C shell aspect ratio gives 6.4 degrees.
3. The camera distance was taken from a known size at a known depth. In S5 the 10.48 mm knobs, 15.1 mm behind the rear wall, read 328 px. That gives a distance of about 500 mm (range 415 to 640 mm). A point at depth d behind the near wall and height z projects to z cos(pitch) + d sin(pitch), reduced by D / (D + d).

The renders were used to check S4, not to replace it. Where they disagree with S4 the range in section 4 covers both.

### 3.5 Scale references and agreement

| Check | Reference A | Reference B | Result |
| --- | --- | --- | --- |
| S1 plan scale | Lens 31.20 mm (S2) spans 188.244 units: 6.0335 units/mm | Key pitch 19.05 mm (S3) spans 114.955 units: 6.0344 units/mm | Agree to 0.02 %. Scale used: 6.034 units/mm |
| S1 lens shape | Corner radius 12.04 units = 2.00 mm | S2 states "4-R2.00" | Agree |
| S1 cable sketch | Plug tip 54.0 units = 8.95 mm | USB-C shell 8.94 mm (receptacle) or 8.25 mm (plug) | Weak check. The cable is a sketch |
| S5 rear render | Body width 120.38 mm spans 3880.6 px: 32.24 px/mm | USB-C receptacle shell 8.94 mm spans 290.0 px: 32.44 px/mm | Agree to 0.6 %. The shell reads 8.99 x 3.26 mm at the body scale |
| S4 CAD side view | Body depth 85.16 mm spans 815.3 px: 9.574 px/mm | Key pitch 19.05 mm spans 181.93 px: 9.550 px/mm. Knob 10.48 mm spans 100.3 px: 9.57 px/mm | Agree to 0.25 % |
| S10 real unit | Local key pitch 155.7 px | Lens 249.2 px = 30.5 to 31.0 mm, cap top 126.6 px = 15.5 mm, lens to right edge 30.5 px = 3.8 mm | The real unit matches S1 within the photo error of 2 % |
| Maker CAD measurement | 84.694 mm depth, March 2025 prototype (`official-site.md` section 5.5) | 85.16 mm depth in S1 | Differ by 0.47 mm. The March 2025 design is an earlier revision |
| "19 mm thin" | Maker claim | 19.2 mm maximum body thickness in S4 | Agree. See section 6 |
| Standard keycap sizes | Keycap base 111.12 units square = 18.42 mm at the lens scale. MX-grid 1u caps are about 18 mm square (`https://deskthority.net/wiki/Keycap_size_by_keyboard`) | Choc-spaced 1u caps are 17.5 x 16.5 mm, not square (MBK, `https://splitkb.com/products/mbk-legend-ergo-ortho`) | The square 18.4 mm cap fits MX spacing only. Weak as a scale check, because cap sizes vary by about 0.5 mm between profiles |
| Mass | Maker states 265 g (`youtube.md`). Shopify shipping weight 442 g (`regulatory-software.md`) | Shell volume with 3.5 mm walls gives about 160 g of aluminium, plus about 115 g of board, cell, switches, caps, knobs and glass | Consistent. This is a plausibility check only (guess) |

### 3.6 MX spacing against Choc spacing

At the lens scale the pitch is 19.053 mm along X and 19.053 mm along Y. The X to Y pitch ratio is 1.0000. Choc spacing needs a ratio of 18 / 17 = 1.059, so it is rejected. An 18.0 mm square pitch would make the lens 29.5 mm, against 31.20 mm on the supplier drawing, so it is rejected too. The maker's KiCad footprint carries both "19.05 spacing" and "18x17 spacing" outlines, and the keys are tiled on the 19.05 outline (S3).

## 4. Dimension table

Each row gives the value, the low to high range, the source and the confidence. All values are millimetres unless marked.

### 4.1 Plan

| Dimension | Value | Range | Source and method | Confidence |
| --- | --- | --- | --- | --- |
| Overall width (X) | 120.4 | 120.1 to 120.7 | S1, 726.35 units | likely |
| Overall depth (Y) | 85.2 | 84.7 to 85.5 | S1, 513.86 units. Low end covers the 84.694 mm prototype | likely |
| Vertical corner radius | 2.0 | 1.9 to 2.1 | S1 corner arcs, 12.04 units. S4 shows the tangent line 2.0 mm from each end | likely |
| Top edge chamfer | 1.0 | 0.9 to 1.1 | S1 second outline, 6.0 units. S4 0.9 mm. S5 1.0 mm | likely |
| Bottom edge chamfer | 0.4 | 0.2 to 0.6 | S4, a line 2 to 4 px inside the underside silhouette | guess |
| Key pitch, X and Y | 19.05 | 19.03 to 19.07 | S1 and S3 | confirmed |
| Key field, cap edge to cap edge | 75.6 | 75.4 to 75.7 | S1 | likely |
| Key well, lip to lip | 78.15 x 78.15 | 78.0 to 78.3 | S1, 471.61 units | likely |
| Key well lip chamfer | 0.5 | 0.4 to 0.6 | S1, second line 3.0 units inside the lip | likely |
| Key well corner radius | 1.0 | 0.8 to 1.2 | S1 | likely |
| Wall between body edge and key well lip (left, rear, front) | 3.50 | 3.4 to 3.6 | S1, 21.12 units on all three sides | likely |
| Rear left key centre from left edge and rear edge | 14.00, 14.02 | 13.9 to 14.1 | S1 | likely |
| Control column width, well lip to right edge | 38.7 | 38.5 to 38.9 | S1 | likely |
| Body edges in grid coordinates | left -14.0, right +106.4, rear -14.0, front +71.1 | plus or minus 0.15 | S1 | likely |

The left 85.2 mm of the body is a square: the lens starts at X = 85.16 mm, which equals the body depth.

### 4.2 Heights and thickness

| Dimension | Value | Range | Source and method | Confidence |
| --- | --- | --- | --- | --- |
| Body thickness at the front edge | 13.0 | 12.8 to 13.2 | S4 ramp extrapolated to the front face: 12.94. S6: 13.1. S7: 12.8 | likely |
| Body thickness at the rear wall (wall height) | 12.0 | 11.8 to 12.2 | S4: 11.98. S5: 11.99. S6: 11.99 | likely |
| Maximum body thickness (wedge apex) | 19.2 | 18.6 to 19.3 | S4: 19.2. S5 gives 18.6 to 19.0 after pitch correction | likely |
| Height over keycaps, square to the top face, no feet | 23.6 | 22.8 to 23.9 | 19.2 + 4.4 | likely |
| Height over knobs, square to the top face, no feet | 31.0 | 30.1 to 31.4 | 19.2 + 11.8 | likely |
| Thickness over the rear feet | 20.8 | 20.0 to 21.0 | S4 foot bottom at 20.79. S5 gives 19.9 to 20.4 | likely |
| Thickness over the front feet | 15.5 | 15.0 to 15.7 | S4 foot bottom at 15.46 | likely |
| On the desk: top face at the front edge | 14.9 | 14.4 to 15.2 | Calculated from the two foot planes in S4 | likely |
| On the desk: top face at the rear edge | 22.3 | 21.6 to 22.6 | Calculated | likely |
| On the desk: highest keycap (rear row) | 25.5 at the cap centre, 26.2 at the rear edge of the cap top | 24.8 to 26.5 | Calculated | likely |
| On the desk: knob tops (overall height) | 32.8 | 32.0 to 33.5 | Calculated | likely |
| Shell split line below the top face | 5.0 | 4.8 to 5.1 | S4: 4.86. S5: 5.0. S6: 5.00. S7: 4.97 | likely |
| Bottom shell wall height, rear and front | 7.0 and 8.0 | plus or minus 0.3 | Wall height minus 5.0 | likely |
| Tilt of the top face on the desk (degrees) | 5.0 | 4.7 to 5.2 | S4: ramp 4.95 degrees, foot plane 4.97 degrees | likely |

### 4.3 Keys

| Dimension | Value | Range | Source and method | Confidence |
| --- | --- | --- | --- | --- |
| Keycap base, square | 18.4 | 18.3 to 18.5 | S1, 111.12 units | likely |
| Keycap top face, outer edge | 15.7 | 15.5 to 15.8 | S1, 94.75 units. S4 taper extrapolation 15.66. S10 15.5 | likely |
| Keycap top edge radius | 0.5 | 0.4 to 0.6 | S1 ring 3.0 units inside the top edge | likely |
| Keycap dish, square | 12.0 x 12.0 | 11.9 to 12.1 | S1, 72.37 units. Corner radius about 1.7 | likely |
| Dish depth | 0.6 | 0.3 to 1.0 | Not measurable. Estimate from the shading in the keycap render | guess |
| Gap between caps | 0.64 | 0.55 to 0.75 | S1, 3.875 units | likely |
| Keycap top above the top face | 4.4 | 4.2 to 4.6 | S4: 4.44. S6: 4.3 to 4.45 | likely |
| Keycap side angle from vertical (degrees) | 16.5 | 15 to 18 | S4: width 17.57 at 1.25 above the deck, 16.01 at 3.86 above | likely |
| Keycap total height | 4.6 | 4.4 to 5.2 | Side angle and base width put the cap base 0.1 to 0.2 below the deck | likely |
| Clearance, cap base to well wall | 0.8 | 0.7 to 0.9 | S1, measured to the foot of the lip chamfer | likely |
| Key well depth, deck to plate top | 3.7 | 3.3 to 4.2 | S8: 4.0 plus or minus 0.4. Stack: 5.0 shell minus 1.3 plate | guess |
| Plate thickness at the cut-outs | 1.3 | 0.9 to 1.5 | 5.0 minus well depth. Choc plates are 1.2 to 1.3 | guess |
| Switch cut-out | 13.9 x 13.9 | 13.7 to 14.1 | S8, 257.2 px at 18.55 px/mm. Corners have dog-bone reliefs | likely |

### 4.4 Knobs and round buttons

| Dimension | Value | Range | Source and method | Confidence |
| --- | --- | --- | --- | --- |
| Knob diameter | 10.5 | 10.3 to 10.6 | S1 ring 63.25 units = 10.48. S4 100.3 px = 10.48 | likely |
| Knob top flat diameter | 8.0 | 7.8 to 8.2 | S1 inner ring 48.37 units. The edge radius is 1.25 | likely |
| Knob top above the top face | 11.8 | 11.5 to 12.1 | S4: 11.83. S5 agrees within 0.15 | likely |
| Knob cap height | 9.1 | 8.8 to 9.4 | S4, from 2.7 to 11.8 above the deck | likely |
| Knob boss on the case, base diameter | 16.1 | 15.9 to 16.3 | S1 ring 97.25 units | likely |
| Knob boss height | 1.8 | 1.5 to 2.1 | S4. A 0.85 gap separates boss and knob | likely |
| Knob centres from the right edge | 10.27 and 28.96 | plus or minus 0.1 | S1 | likely |
| Knob centres from the rear edge | 15.10 | 15.0 to 15.2 | S1. S4 gives 15.15 | likely |
| Knob centre spacing | 18.68 | 18.6 to 18.8 | S1. It is not 19.05 | likely |
| Knob centres, grid coordinates | (77.42, 1.08) and (96.10, 1.08) | plus or minus 0.1 | S1. The knobs sit 1.08 in front of the rear key row centre line | likely |
| Round button cap diameter (skirt) | 12.3 | 12.2 to 12.5 | S1 rings 74.21 and 75.45 units: skirt 12.30 in a 12.50 hole | likely |
| Round button top face diameter | 10.3 | 10.2 to 10.4 | S1 ring 62.0 units | likely |
| Round button proud height | 1.0 | 0.7 to 1.2 | S5, cone band 30 px at 28.2 px/mm, pitch corrected | likely |
| Round button centres from the right edge | 10.27 and 28.96 | plus or minus 0.1 | S1. Same X as the knobs | likely |
| Round button centres from the front edge | 14.0 | 13.9 to 14.1 | S1 | likely |
| Round button centres, grid coordinates | (77.42, 57.14) and (96.10, 57.14) | plus or minus 0.1 | S1. They sit on the front key row centre line | likely |

### 4.5 Display

| Dimension | Value | Range | Source and method | Confidence |
| --- | --- | --- | --- | --- |
| Window (cover lens) width and height | 31.2 x 31.2 | 31.1 to 31.3 | S2 states 31.20 plus or minus 0.1. S1 gives 31.20 | confirmed |
| Lens corner radius | 2.0 | 1.9 to 2.1 | S2 and S1 | confirmed |
| Active area | 25.2 x 25.2 | 25.1 to 25.3 | S2. S10 shows the lit area at 25.2 | confirmed |
| Black border, lens edge to active area | 3.0 | 2.9 to 3.1 | S2 offsets 1.60, 2.00, 2.70, 3.00 from the lens edge. All four sides are equal | confirmed |
| Module thickness | 2.95 | 2.80 to 3.10 | S2: lens 1.10, adhesive 0.20, LCD module 1.65 | confirmed |
| Lens from the right edge | 4.0 | 3.9 to 4.1 | S1, 24.25 units | likely |
| Lens from the key well lip | 3.5 | 3.4 to 3.6 | S1 | likely |
| Lens from the rear edge, near and far side | 27.0 and 58.2 | plus or minus 0.1 | S1 | likely |
| Lens centre, grid coordinates | (86.76, 28.57) | plus or minus 0.1 | S1. It sits on the knob pair centre line and on the middle of the key grid | likely |
| Gap, knob boss to lens | 3.8 | 3.6 to 4.0 | S1 | likely |
| Gap, lens to button hole | 6.8 | 6.6 to 7.0 | S1 | likely |

### 4.6 Case

| Dimension | Value | Range | Source and method | Confidence |
| --- | --- | --- | --- | --- |
| Wall thickness, top shell | 3.5 | 3.3 to 3.6 | S1: well lip to outer face | likely |
| Wall thickness, bottom shell | 3.5 | 2.8 to 3.7 | S3: a 112.5 board in a 120.4 body leaves 3.94 per side. S9 rim reads 3 to 4 | guess |
| Bottom shell floor thickness | 1.8 | 1.2 to 2.5 | Mass estimate only | guess |
| Shell fasteners | 4 screws, M2 class | not applicable | S3: four "MountingHole_Pad" footprints, about 2.2 hole. S8: 3.6 holes in the well floor. S9: four bosses | likely |
| Screw positions, X from the left edge | 23.5 and 61.6 | plus or minus 0.3 | S3: exactly between columns 1-2 and 3-4 | likely |
| Screw positions, Y from the rear and front edges | 7.1 | 6.5 to 7.7 | S3: 6.5 to 7.3 beyond the outer row centres. S1 shows marks at 5.7 to 9.5 | likely |
| Printed circuit board width | 112.5 | not applicable | S3 dimension text | likely |

### 4.7 Underside, wedge and feet

| Dimension | Value | Range | Source and method | Confidence |
| --- | --- | --- | --- | --- |
| Ramp angle, underside to top face (degrees) | 4.95 | 4.7 to 5.2 | S4, straight within 1 px from 14 to 83 mm from the rear | likely |
| Wedge apex, distance from the rear face | 12.7 | 12 to 16 | S4 intersection of the ramp and the rear slope | likely |
| Rear slope angle to the top face (degrees) | 29 | 27 to 31 | S4, from 12.0 thick at the rear face to 19.2 at the apex | likely |
| Wedge height below the wall line | 7.2 | 6.6 to 7.3 | 19.2 minus 12.0 | likely |
| Wedge width at its base, rear | 94 | 92 to 100 | S5: 94.7 just above the bottom, 99.8 higher up | likely |
| Flank scoops | 13 wide per side at the rear, fading out about 43 from the rear face | plus or minus 3 | S5 and S4. The side wall stays 11.7 to 12.0 high along the scoop | likely |
| Feet, count and shape | 4, stadium (pill) shape, long axis along X, each in a milled pocket with a thin gap ring | not applicable | S5, S7, S13, video `4mGhEPTLoSA` | confirmed |
| Foot length (long axis along X) | 22.5 | 22.0 to 24.0 | Three methods, see the note below this table | likely |
| Foot width at its base (along Y) | 5.2 | 4.9 to 5.4 | S4 column scans across the rear foot: 4.99, 4.54, 3.78 and 2.82 wide at 1.36, 0.94, 0.52 and 0.21 above the foot bottom. S14: pill 5.4 wide at the strip scale | likely |
| Foot cross-section | Rounded, about 2.8 wide at 0.2 above the contact line | not applicable | S4, same scans. The foot is a domed bar, not a flat pad | likely |
| Foot proud height | 2.0 | 1.7 to 2.3 | S4: 2.06 on both feet. S5 gives 1.7 | likely |
| Rear feet centres | 18.2 from the rear face, 26.4 from each side edge | plus or minus 0.8 | S4 and S5 | likely |
| Front feet centres | 5.6 from the front face, 14.7 from each side edge | plus or minus 0.6 | S4 and S7 | likely |

Foot length method. The three readings agree within 1.5 mm.

1. S5 rear silhouette (`overlays-01/overlay-08-rear-foot-silhouette.png`). Only the lowest 0.7 mm of the rear foot shows below the wedge. Its width is 663.4, 641.9 and 606.9 px at 0.65, 0.40 and 0.14 mm above the foot bottom. At 31.1 px/mm (32.24 px/mm reduced by 0.965 for the 18.2 mm depth) that is 21.3, 20.6 and 19.5 mm. The domed ends shorten each slice. With the end profile taken equal to the S4 cross-section, the shortening is 1.2, 1.8 and 2.8 mm. The corrected lengths are 22.5, 22.4 and 22.3 mm. The earlier 20.4 mm (S5) and 20.8 mm (S7) readings were slices of this kind without the correction.
2. S13 plan view of the upside-down second unit (`overlays-01/overlay-07-feet-plan.png`). The two rear feet are 572 and 639 px long. Their centres are 1789.5 px apart, which is 67.6 mm (from S5). The mean foot length is 22.8 mm. The right foot is nearer the camera, so the mean is used.
3. S14 caliper photo, June 2025 foot sample. The caliper jaws grip the two edges of a moulded silicone strip that carries several pills side by side (crop `work-02/foot-strip-rot.png`). The 24.04 mm reading is the strip width. The pills run almost edge to edge, so the sample feet are 23 to 24 mm long. This sample predates the August 2025 drawing.

### 4.8 Ports

| Dimension | Value | Range | Source and method | Confidence |
| --- | --- | --- | --- | --- |
| USB-C aperture in the rear wall | 10.0 x 4.3, stadium | 9.8 to 10.3 x 4.1 to 4.5 | S5, 323.6 x 138.0 px | likely |
| USB-C centre from the right edge | 19.6 | 19.1 to 19.9 | S5: 19.35. The knob pair centre line is 19.62 | likely |
| USB-C centre below the top face | 5.0 | 4.8 to 5.2 | S5. The aperture is centred on the split line | likely |
| Slide switch aperture in the rear wall | 10.0 x 4.3, stadium | 9.8 to 10.3 x 4.1 to 4.5 | S5, 324.0 x 138.1 px | likely |
| Slide switch centre from the right edge | 37.5 | 37.0 to 38.0 | S5 | likely |
| Slide switch centre below the top face | 5.0 | 4.8 to 5.2 | S5 | likely |
| Centre spacing, USB-C to slide switch | 18.1 | 17.8 to 18.4 | S5, 584.1 px | likely |

### 4.9 Dock or base plate

There is no dock. The plate with the raised silver block in the hero render is a second pad lying upside down. Its size is the body size, 120.4 x 85.2 mm. The "raised block" is the wedge, 7.2 mm above the wall line, with its lit flank scoop. See section 7.7. (likely)

## 5. Underside profile

Source: S4. Thickness is measured square to the top face. Distance is from the rear face.

| Distance from rear (mm) | Thickness (mm) | Note |
| --- | --- | --- |
| 0.5 | 12.0 | Bottom of the rear wall |
| 3.2 | 13.8 | Rear slope |
| 5.3 | 14.9 | Rear slope |
| 7.3 | 16.2 | Rear slope |
| 9.4 | 17.4 | Rear slope |
| 11.5 | 18.6 | Rear slope |
| 12.7 | 19.2 | Apex |
| 18.2 | 18.7 (20.8 over the foot) | Rear foot centre |
| 25.1 | 18.1 | Ramp |
| 42.8 | 16.6 | Ramp |
| 63.7 | 14.8 | Ramp |
| 79.6 | 13.4 (15.5 over the foot) | Front foot centre |
| 85.2 | 12.9 | Front face, extrapolated |

The ramp follows thickness = 12.94 + 0.0866 x (distance from the front face).

## 6. What "19 mm" refers to

| Candidate | Value (mm) | Verdict |
| --- | --- | --- |
| Maximum body thickness, no feet, caps or knobs | 19.2 | Best match |
| Rear top edge above the desk, on feet | 22.3 | Too large |
| Front top edge above the desk, on feet | 14.9 | Too small |
| Thickness over the rear feet | 20.8 | Too large |
| Body plus keycaps | 23.6 | Too large |
| Overall height on the desk | 32.8 | Too large |

The claim most plausibly means the thickest point of the aluminium body. (likely)

`official-site.md` section 7.2 reports 17.0 mm at the rear riser and 18.8 mm on feet. Those values were read from the perspective side render without a pitch correction, and the wedge apex is hidden in shadow in that render. The orthographic CAD view replaces them.

## 7. Inferences

### 7.1 Switch family

Kailh Choc V2 class (PG1353 family): low profile, MX cross stem, Choc-type footprint. Confidence: likely.

Reasons:

1. The pitch is 19.05 mm, and the keycaps use an MX cross mount (real unit frame `youtube/frames-01/Q6CKpc6AK0o/f017.jpg`).
2. The maker's footprint carries "19.05 spacing" and "18x17 spacing" outlines, a large centre hole of about 5 mm and a third "MP" pad (S3). Those marks belong to Choc footprints.
3. The maker names the part "Kailh Low Profile V2's (hot-swappable)" and describes it as fully POM (`official-site.md`).
4. A full-height MX switch cannot fit. The cap top is 4.4 mm above the deck and the body is 13 mm thick at the front.
5. Choc V1 is excluded by the cross stem. Gateron low profile (KS-33) also has a cross stem, so geometry alone cannot exclude it. The maker's naming and the footprint do.

Exact switch model: not found.

### 7.2 Keycap profile

A custom uniform low-profile cap. All 16 caps are identical (S1). Base 18.4 mm, top 15.7 mm, height about 4.6 mm, side angle 16.5 degrees, a shallow 12 x 12 mm square dish, MX cross mount. The cap base sits level with the deck, and the skirt sinks into the key well when pressed. Confidence: likely.

No standard profile name applies. The nearest shop profiles are low uniform MX-mount caps for Choc V2 and Gateron low-profile switches. A match with any named profile was not checked.

### 7.3 Display panel candidates

The GLYF panel is a 1.4 inch 240 x 240 module with a bonded 31.2 mm lens (S2, confirmed). The firmware agent reports an ST7789V-compatible controller (`regulatory-software.md`).

Active areas below are calculated from the diagonal and the pixel count with square pixels. Datasheet values differ by up to 2 %. The envelope of the control column is: 31.7 mm maximum glass width (38.7 mm column minus two 3.5 mm walls) and 37.8 mm maximum glass height (41.8 mm between the knob bosses and the button holes minus two 2 mm gaps).

| Candidate | Active area W x H (mm) | Fits the 31.2 mm square lens | Fits the control column with a new lens |
| --- | --- | --- | --- |
| 1.4 in, 240 x 240 (GLYF) | 25.1 x 25.1 | Yes, 3.0 border | Yes |
| 1.47 in, 172 x 320 | 17.7 x 32.9 | No, 1.7 too tall | Yes, portrait, 7 border at the sides |
| 1.54 in, 240 x 240 | 27.7 x 27.7 | No, border would be 1.75 | Yes, tight: 2.0 border at the sides |
| 1.69 in, 240 x 280 | 27.9 x 32.6 | No | Yes, tight: 1.9 border at the sides, 2.6 top and bottom |
| 1.9 in, 170 x 320 | 22.6 x 42.6 | No | No, 4.8 too tall unless the buttons move |
| 2.0 in, 240 x 320 | 30.5 x 40.6 | No | No, too wide and too tall |
| AMOLED 1.64 in, 280 x 456 | 21.8 x 35.5 | No | Yes, 1.1 border top and bottom, so tight |
| AMOLED 1.78 in, 368 x 448 | 28.7 x 34.9 | No | Marginal, 1.5 border at the sides |
| AMOLED 1.91 in, 240 x 536 | 19.8 x 44.3 | No | No, too tall |

Confidence: likely for the fit verdicts. Module outline sizes, which are larger than the active area, were not checked against datasheets.

### 7.4 Bottom two round controls

They are push buttons, not dials. Confidence: confirmed.

Reasons:

1. The board has two SMD tactile switches in these positions, footprint name "SW_Omron_B3FS" (`youtube.md`).
2. The firmware has a 5 x 4 direct key matrix with 16 keys, 2 encoder pushes and 2 navigation buttons, and only two encoders (`regulatory-software.md`).
3. The caps stand 1.0 mm proud with a 1 mm chamfer and no grip surface (S1, S5).

### 7.5 Case split and fastening

Confidence: likely.

1. Two CNC shells meet on a flat plane 5.0 mm below the top face. The split line runs round all four walls (S4, S5, S6, S7).
2. The top shell is 5.0 mm tall. It carries the deck, the key well with the switch plate as its floor, the lens pocket with a through window and a flex notch, two knob bosses and two button holes (S8).
3. The bottom shell is a tray with the wedge machined in. Inside it has a deep pocket under the key field and shallower ledges (S9).
4. The USB-C and slide switch apertures are cut half into each shell (S5, S8).
5. Four screws enter from the top, through the key well floor, between key columns 1-2 and 3-4, about 7 mm from the rear and front edges. They pass through four board mounting holes (S3) into four bosses on the rear and front walls of the bottom shell (S9). The keycaps hide them: the gap between caps is 0.64 mm. No screw is visible on the underside or on the walls.
6. To open the unit, the keycaps beside the screws must come off first.

### 7.6 Antenna window

The GLYF has no dedicated antenna window. Confidence: likely for the absence, guess for the radio path.

1. Both shells are aluminium on every face. The non-metal openings are the 31.2 mm lens, two 12.5 mm button holes, two knob holes, the two rear apertures (10.0 x 4.3 mm each) and the anodised seam between the shells.
2. The radio module sits on the bottom side of the board at the right board edge, beside the lens, about 24 to 38 mm from the rear edge (KiCad 3D view `youtube/frames-01/kOclb0i9bug/f001.jpg` and board photo `youtube/frames-01/S9c5WuorsgQ/f023.jpg`). The glass is the nearest opening, so it is the most probable exit.
3. The lens overhang beyond the LCD is 1.6 mm at the sides, and the LCD has a metal backlight frame. The opening is small against the 125 mm wavelength.

Places where a clone of this shape could put a real window:

1. A longer cover glass with black print that extends past the LCD on one side, over a slot in the top shell. The right wall beside the lens is the natural place.
2. A plastic insert in the rear wall beside the USB-C port, as `prior-art.md` records for the Keychron Q1 Pro.
3. A slot in the bottom shell under a rear foot. The foot is about 22.5 x 5.2 mm and would hide it. Radiation toward the desk is the cost.

### 7.7 The "dock"

It is a second pad shown from below, not an accessory. Confidence: likely.

1. The plate has the same width as the pad once the depth difference is allowed for (S11).
2. It shows stadium-shaped feet in the four-foot pattern of section 4.7.
3. The "raised silver block" has the scooped flank of the wedge seen in the Fusion underside view (`geometry/yt-frames-01/Ly/f012.png`) and in the rear render S5.
4. The store lists no accessory product (`official-site.md`).
5. The full-resolution product render S13 shows the same object from a higher angle: a body underside with two pill feet on the ramp just in front of the wedge apex, the apex ridge, and the lit flank scoop at the rear corner.

### 7.8 Internal stack (derived)

All values are guesses. They follow from the measured heights and from a Choc V2 class switch, whose plate top lies 2.2 mm above the board.

| Level | Height (mm, deck = 0) |
| --- | --- |
| Keycap top | +4.4 |
| Deck and keycap base | 0 |
| Plate top (key well floor) | -3.7 |
| Plate underside and split plane | -5.0 |
| Board top | -5.9 |
| Board underside (1.6 mm board) | -7.5 |
| Hot-swap socket underside | -9.3 |
| Underside of the body at the front edge | -13.0 |
| Underside of the body at the apex | -19.2 |

At the front edge 3.7 mm remains for clearance and the floor. Under the rear half of the key field up to 9 mm remains, which is where the bottom shell has its deep pocket. A 1200 mAh pouch cell fits there.

The encoder shaft top is about 16 mm above the board top (knob top minus a 1.5 mm cap roof), which matches an EC11-type encoder with a 15 mm shaft. (guess)

## 8. Corrections to earlier notes

| Earlier value | Source | Value in this file | Reason |
| --- | --- | --- | --- |
| Pitch 19.0 mm, body 120.0 x 84.9 mm | `official-site.md` 7.1 | Pitch 19.05 mm, body 120.4 x 85.2 mm | The 31.20 mm lens fixes the scale independently |
| 17.0 mm at the rear riser, 18.8 mm on feet | `official-site.md` 7.2 | 19.2 mm at the apex, 20.8 mm over the rear feet | Orthographic CAD view. Pitch correction |
| Keycap top about 5.0 mm above the top face | `official-site.md` 7.2 | 4.4 mm | Orthographic CAD view, side render re-read |
| Knob top at least 11 mm | `official-site.md` 7.2 | 11.8 mm | Orthographic CAD view |
| Body about 116 x 88 mm or 125 x 94 mm | `youtube.md` | 120.4 x 85.2 mm | Hand-held photo against vector drawing |
| Fastening not found | `official-site.md` 7.3 | Four screws under the keycaps | S3, S8, S9 combined |
| One silicone foot measured at 24.04 mm | `youtube.md` | Foot about 22.5 x 5.2 mm. The 24.04 mm reading is the width of a moulded strip of feet | S14 shows the caliper jaws on the strip edges. Section 4.7 |

## 9. Overlays, specs and scripts

All paths are under `research/_cache/geometry/`.

| File | Content |
| --- | --- |
| `overlays-01/overlay-01-plan-svg.png` | S1 with column, row, lens, knob and body lines labelled in millimetres |
| `overlays-01/overlay-02-fusion-side-ortho.png` | S4 with deck, split, apex, cap top, knob top and feet lines |
| `overlays-01/overlay-03-rear-render.png` | S5 with body edges, apertures, knobs, feet, split and wall lines |
| `overlays-01/overlay-04-side-render.png` | S6 with cap top, top face, split and underside lines |
| `overlays-01/overlay-05-front-render.png` | S7 with feet, split and wall lines |
| `overlays-01/overlay-06-exploded-well.png` | S8 with well lip, well floor and cut-out lines |
| `overlays-01/overlay-07-feet-plan.png` | S13 with the ends of both rear feet and the scan rows |
| `overlays-01/overlay-08-rear-foot-silhouette.png` | S5 rear foot silhouette with its width at three heights |
| `specs-01/*.json` | One spec per overlay. Each lists every line position in source pixels. Specs 07 and 08 were written by hand, not by `make_specs.py` |
| `work-02/` | Crops for the foot check: caliper strip (`foot-strip-crop.png`, `foot-strip-rot.png`, `foot-pills-zoom.png`), S13 feet (`left-foot-zoom.png`, `right-foot-zoom.png`, `prod-underside-band.png`) and S5 foot (`s5-left-rear-foot.png`) |
| `scripts/svg_bboxes.py` | Bounding box of every element of an SVG file |
| `scripts/line_centres.py` | Stroke centres along one scan line of a rasterised line drawing |
| `scripts/edges.py` | Sub-pixel brightness edges along a row or column band |
| `scripts/make_specs.py` | The measured pixel positions, written out as overlay specs |
| `scripts/annotate.py` | Draws an overlay from a spec |
| `scripts/py.sh` | Runs a script with `python -I` and Pillow, numpy and svgpathtools from `uv` |
| `work-01/` | Rasters and crops made while measuring |

To rebuild the overlays, run `scripts/py.sh scripts/make_specs.py <cache root> specs-01 overlays-01`, then `scripts/py.sh scripts/annotate.py` on each spec. Specs 07 and 08 hold absolute image paths and are used as they are.

## 10. Not found and not checked

1. No unit was measured by hand. Every value is from maker images, and the shipped product may differ from the August 2025 drawing and from the "Mock Design" CAD file.
2. Not found: keycap dish depth, floor thickness, lens pocket depth, whether the lens is flush with the deck, screw thread and head type, foot thickness inside its recess, knob boss top diameter.
3. The key well depth and the plate thickness rest on one perspective render and a stack-up. Treat them as guesses.
4. The drawing S1 shows a small step in the rear wall of the key well beside the rear right key, about 8 mm long. Its purpose was not resolved.
5. Module outline sizes of the display candidates were not checked against datasheets.
6. The camera distance of the renders is known only to about 25 %. It affects the far features (feet, buttons) by up to 0.3 mm.
7. The foot length of 22.5 mm assumes that the domed foot ends have the same profile as the measured foot cross-section. A flatter end would bring the S5 value down toward 21.5 mm.
