# Assembly

How to turn an assembled board from JLCPCB, the case parts and the hand-fitted parts into a worxpad. The bare
board is tested before anything is soldered or closed. The case build order is decision
[D28](decisions.md#d28-build-order-cell-orientation-and-lead); this page adds the bench tests around it.

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
- 0.3 mm insulating sheet, the lens adhesive ring, the black tape frame, the display foam pad and the battery
  foam pad.

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

1. Short each socket's two contacts with tweezers: the key reports. With the firmware's keymap
   ([keymap.md](keymap.md)) every position must give its own code.
2. Press both buttons and both knob pushes.
3. Turn both encoders. If one counts backwards, swap A and B in the firmware, not on the board.

## 6. Test the display on the bench

1. Insert the panel's flex into J2 (contact side as the connector drawing shows) and close the latch.
2. Power on: the status screen must show. A flipped image or an 80-line offset is a firmware setting
   ([firmware/README.md](../firmware/README.md)).
3. Open the latch and take the panel out again; it goes into the top shell first in step 8.

## 7. Check the cell

1. Measure the cell plug before it ever touches the board: pin 1 must be positive (power 7.4). Reversed
   plugs exist; the AO3401A protects the board, but do not rely on it.
2. Measure the lead length: 19 to 60 mm from the PCM to the plug (D28). The value in `board.toml` (50 mm) is
   a guess. Do not fit a cell whose lead is outside the range.
3. Plug it in on the bench, USB unplugged, switch on: the board runs from the cell. Plug USB: /CHG (TP7) goes low and
   the charge current is about 400 mA (362 to 443 mA by the data sheet). Unplug the cell again.

## 8. Build the case (D28)

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
7. Deck down on the mat. Lay the 0.3 mm insulating sheet over the sockets, lay the cell on it inside the pocket
   outline with the PCM end toward +X (toward the connector), plug the lead into J3 and dress the loop in the
   relief.
8. Slide the RF insert into the bottom-shell slot from above. Place the foam pad on the pocket floor. Stick the
   four feet into their pockets.
9. Lower the bottom shell over the cell. Fit C1 and C2 (M2 x 6) from below.
10. Deck up. Fit K1 to K4 (M1.6 x 5) from the top, then the keycaps. Put the 1.10 mm shim on the plinth, rest
    each knob on it under light finger pressure, tighten the M2 set screw lightly on the shaft flat, and pull
    the shim out. The knob must click and return.

## 9. Final test

1. Every key, both knobs (turn and push), both buttons.
2. USB: the board enumerates; the charge mark shows on the screen.
3. Bluetooth: pair with one host, then a second profile.
4. Radio range: the acceptance test of mcu-radio 7.3.4 on the first aluminium unit (README "Before you
   order", item 4). Record the antenna inset from step 1 next to the result.
5. Reset: a pin through the floor pinhole presses SW17.

## To open it again

Run D28 backward. Unit underside up, remove C1 and C2 and lift the bottom shell: the cell stays lying on the PCB.
**Unplug the cell first**, then anything else. To change a switch, take the cell out and put the top shell with
the PCB on the insertion jig (D26).
