# Assembly

How to turn an assembled board from JLCPCB, the case parts and the hand-fitted parts into a worxpad. The bare
board is tested before anything is soldered or closed. The case build order is decision
[D28](decisions.md#d28-build-order-cell-orientation-and-lead), steps 7 on as revised by
[D39](decisions.md#d39-cell-bonded-to-the-pocket-floor-top-assembly-lowered-onto-the-bottom-shell); this page adds
the bench tests around it.

> **Nobody has built one.** These steps follow the design files and the records. Nothing here has been tried
> on real parts. Where a step depends on a guess, it says so. Stop at the first step that does not behave as
> written, and record what you saw.

## What you need

- An assembled board, broken out of its frame ([ordering.md](ordering.md#when-the-boards-arrive)).
- 16 Kailh CPG135001S30 sockets, 16 switches, 16 keycaps, 2 button caps, the display panel, the lens, the cell
  and the case parts: [parts.md](parts.md), [bom-hand.csv](bom-hand.csv).
- Screws and feet: [cad/production/hardware.csv](../cad/production/hardware.csv).
- The printed switch insertion jig (D26) and a 1.10 mm fork shim for the knobs.
- A soldering iron, flux, a multimeter, a USB-C cable, a TC2030 cable and an SWD probe ([flashing.md](flashing.md)).
- A self-adhesive 0.3 mm insulating sheet (0.3 mm overall), the lens adhesive ring, the black tape frame, the
  display foam pad and 0.2 mm double-sided foam tape for the cell.

## What is already on the board

JLCPCB places 61 parts: everything on the bottom face except the sockets, plus J2, SW19, SW20 and the two
encoders on the top face. Left to you: the 16 sockets SW1 to SW16 (bottom face). The encoder filter capacitors
C13 to C16 stay empty (D36).

## 1. Check the bare board

1. Sand the tab nubs flush with the board edge. The board sits 0.30 mm from the left case wall.
2. Look at U1's antenna end under a loupe: it must not overhang the right edge. Write down the inset.
3. Look at the top face: J2 with contact 1 toward the right, both buttons and both encoders seated.
4. Measure resistance to GND (TP5 or TP6) from TP1 (VBUS_SYS), TP3 (VSYS), TP2 (BAT) and TP4 (3V3); `pcb/netlist.txt`
   lists every test pad. None may read as a short. Record the values; no expected value was computed.

## 2. First power, no cell

1. Slide switch off. Plug USB into a current-limited supply or a USB meter.
2. The charger's /PGOOD (TP8) goes low with USB present; nothing else should happen. The current should stay small
   (no figure was computed for this case).
3. Slide switch on. Measure 3V3 at TP4: 3.25 to 3.35 V (TPS7A02, +/-1.5 %, D13).
4. If the current jumps or 3V3 is wrong, unplug and stop.

## 3. First flash

Follow [flashing.md](flashing.md): the bootloader over SWD through the TC2030-NL pads, then the ZMK image over
USB. Neither has run on a board yet.

## 4. Solder the sockets

1. Board bottom face up. The socket pads have no paste.
2. Place each socket over its two holes, contacts on their pads, and solder both pads. Keep the solder flat:
   the eight sockets over the battery pocket sit 0.3 mm above the insulating sheet (keys 6.4).
3. Check each socket sits flat; a tilted socket meets the jig rib or the sheet.

## 5. Test the inputs

Use a key-event viewer on the host (for example evtest or wev on Linux), not an open application: most Edit
keys are shortcuts. The board starts on the Edit layer of the stock keymap ([keymap.md](keymap.md)). Row 1 is the
rear row, column 1 the left column. The display is not fitted yet, so the layer shows only in what the keys send.

1. Short each socket's two contacts with tweezers. On Edit every key sends its own report: Esc, Ctrl+Z,
   Ctrl+Shift+Z, Ctrl+Shift+S; Ctrl+X, Ctrl+C, Ctrl+V, Delete; Shift, Ctrl and Alt (modifier only, no key
   code), Space; Ctrl+A, Ctrl+F, Tab, Enter.
2. Push the left knob: Ctrl+S. Push the right knob: Ctrl+0.
3. Turn both knobs. Left knob to the right: Ctrl+Shift+Z; to the left: Ctrl+Z. Right knob to the right: Ctrl+=;
   to the left: Ctrl+-. If one is reversed, swap A and B in the firmware, not on the board.
4. The buttons send no key code; test them by the layer they select. Press the right button once, then row 1,
   column 2: Up arrow (Nav). Press the right button twice more, then row 1, column 2: Ctrl+Z (Edit again).
5. Hold the left button, short row 1, column 2 and release both: the board goes to Nav, so row 1, column 2 sends
   Up arrow. Hold the left button and short row 1, column 1 to return to Edit.

## 6. Test the display on the bench

1. Insert the panel's flex into J2 (contact side as the connector drawing shows) and close the latch.
2. Power on: the status screen must show. A flipped image or an 80-line offset is a firmware setting
   ([firmware/README.md](../firmware/README.md)).
3. Open the latch and take the panel out again; it goes into the top shell first in step 8.
4. Optional: repeat step 5 items 4 and 5 and watch the layer name in the status bar change.

## 7. Check the cell

1. Measure the cell plug before it ever touches the board: pin 1 must be positive (power 7.4). Reversed
   plugs exist; the AO3401A protects the board, but do not rely on it.
2. Measure the lead length: 19 to 60 mm from the PCM to the plug (D28). The value in `board.toml` (50 mm) is
   a guess. Do not fit a cell whose lead is outside the range. Plugging it in during step 8 item 9 needs
   more than the minimum (D39).
3. Plug it in on the bench, USB unplugged, switch on: the board runs from the cell. Plug USB: /CHG (TP7) goes low and
   the charge current is about 400 mA (362 to 443 mA by the data sheet). Unplug the cell again.

## 8. Build the case (D28, D39)

Prepare first: check the CNC parts as in [ordering-case.md](ordering-case.md#when-the-parts-arrive). For the
FDM print, press the heat-set inserts first ([printing.md](printing.md#inserts-and-screws)).

1. Bond the lens into the top-shell recess with the adhesive ring (display 6.4). Let it cure.
2. Top shell deck down on a soft mat. Fit the display panel and the tape frame against the web, flex toward the
   front.
3. Drop both button caps into their holes from below (rotary-buttons 6.6).
4. Hold the PCB top face toward the shell, insert the flex into J2 and close the latch.
5. Seat the PCB on the G posts; fit G1 and G2 (M2 x 4 pan head) from below.
6. Turn the assembly deck up onto the insertion jig and press in the 16 switches (D26). Never press a switch
   with the cell under the board.
7. Deck down on the mat. Stick the insulating sheet onto the socket bodies so that it covers the battery
   pocket outline.
8. Bottom shell open side up. Slide the RF insert into its slot from above, both keys into their reliefs. Bond
   the 0.2 mm double-sided foam tape to the pocket floor and peel its liner. Set the cell on it inside the pocket
   outline, PCM end toward +X (toward the connector) and the lead in the relief. Press it down with a flat hand,
   never with a fingertip or a tool.
9. Hold the top assembly deck up over the bottom shell, +X ends together, only as high as the lead allows. Push
   the plug into J3 along +X. Lower the top assembly and dress the loop in the relief, clear of the split face
   and the posts. The split faces must meet all round without force; if they do not, lift and dress the lead
   again. Never press the shells together over the lead. The working height the lead allows is not known; a lead
   near the 19 mm minimum may be too short for this step (D39, MEASURE on the first build).
10. Fit K1 to K4 (M1.6 x 5) from the top. Turn the unit underside up on the mat, fit C1 and C2 (M2 x 6) from
    below and stick the four feet into their pockets.
11. Deck up. Fit the keycaps. Put the 1.10 mm shim on the plinth, rest each knob on it under light finger
    pressure, tighten the M2 set screw lightly on the shaft flat, and pull the shim out. The knob must click and
    return.

## 9. Final test

1. Every key, both knobs (turn and push), both buttons, as in step 5; the display now shows the layer.
2. USB: the board enumerates; the charge mark shows on the screen.
3. Bluetooth: pair with one host, then a second profile.
4. Radio range: the acceptance test of mcu-radio 7.3.4 on the first aluminium unit (README "Before you
   order", item 4). Record the antenna inset from step 1 next to the result.
5. Reset: a pin through the floor pinhole presses SW17.

## To open it again

Run the build backward (D39). Unit underside up, remove C1 and C2; deck up, remove K1 to K4. Lift the top
assembly only as far as the lead allows: the cell stays bonded in the bottom shell. **Unplug the cell first**,
then anything else. To change a switch, put the top shell with the PCB on the insertion jig (D26); the cell stays
in the bottom shell, away from the board.
