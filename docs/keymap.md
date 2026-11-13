# Default keymap

The default keymap lives in
[`firmware/zmk/boards/worxbend/worxpad/worxpad.keymap`](../firmware/zmk/boards/worxbend/worxpad/worxpad.keymap).
It is aimed at creative applications on Windows and Linux, so the shortcuts use Ctrl. On macOS, change Ctrl to
Cmd in ZMK Studio or in the host. Nothing here has run on a worxpad board.

## Controls

- 16 keys in a 4 x 4 grid. Row 1 is the rear row, column 1 the left column.
- Two knobs behind the display. Each knob turns and pushes.
- Two round buttons in front of the display.
- The **right button** steps through the layers: Edit, then Nav, then Media, then Edit again.
- Hold the **left button** for System. Release it to return to the layer you were on.

The display shows the active layer: knob functions at the top, the 16 key functions in the grid, and the
layer name, output and battery in the status bar. These labels come from the live keymap, so a change made in
ZMK Studio shows after the next layer change.

## Edit (layer 0)

| | Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- | --- |
| Row 1 | Esc | Undo (Ctrl+Z) | Redo (Ctrl+Shift+Z) | Save as (Ctrl+Shift+S) |
| Row 2 | Cut (Ctrl+X) | Copy (Ctrl+C) | Paste (Ctrl+V) | Delete |
| Row 3 | Shift | Ctrl | Alt | Space (pan tool in most editors) |
| Row 4 | Select all (Ctrl+A) | Find (Ctrl+F) | Tab (hide panels) | Enter |

| Control | Turn left | Turn right | Push |
| --- | --- | --- | --- |
| Left knob | Undo | Redo | Save (Ctrl+S) |
| Right knob | Zoom out (Ctrl+-) | Zoom in (Ctrl+=) | Fit (Ctrl+0) |
| Left button | | | hold: System |
| Right button | | | go to Nav |

## Nav (layer 1)

| | Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- | --- |
| Row 1 | Home | Up | End | Page up |
| Row 2 | Left | Down | Right | Page down |
| Row 3 | Shift | Ctrl | Alt | Tab |
| Row 4 | Backspace | Previous tab (Ctrl+Shift+Tab) | Next tab (Ctrl+Tab) | Enter |

| Control | Turn left | Turn right | Push |
| --- | --- | --- | --- |
| Left knob | Left (frame back in most timelines) | Right (frame forward) | Space (play) |
| Right knob | Up | Down | Enter |
| Left button | | | hold: System |
| Right button | | | go to Media |

## Media (layer 2)

| | Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- | --- |
| Row 1 | Previous track | Play/pause | Next track | Mute |
| Row 2 | Volume down | Volume up | Screen brightness down | Screen brightness up |
| Row 3 | F13 | F14 | F15 | F16 |
| Row 4 | F17 | F18 | F19 | F20 |

F13 to F20 send nothing that hosts use by default. Bind them to application actions in the host.

| Control | Turn left | Turn right | Push |
| --- | --- | --- | --- |
| Left knob | Volume down | Volume up | Mute |
| Right knob | Screen brightness down | Screen brightness up | Play/pause |
| Left button | | | hold: System |
| Right button | | | go to Edit |

## System (layer 3, hold the left button)

| | Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- | --- |
| Row 1 | go to Edit | go to Nav | go to Media | Unlock ZMK Studio |
| Row 2 | Bluetooth profile 1 | profile 2 | profile 3 | profile 4 |
| Row 3 | Previous profile | Next profile | Clear this profile's bond | Toggle USB / Bluetooth |
| Row 4 | Output to USB | Output to Bluetooth | Reset | Bootloader (UF2 drive) |

The knobs keep the function of the layer below. The knob pushes and the right button fall through as well.

## Changing the keymap

- **ZMK Studio:** connect over USB (or Bluetooth on hosts the Studio app supports), hold the left button and
  press row 1, column 4 to unlock, then edit. Changes are stored on the board. Knob turns cannot be changed in
  Studio; that is a ZMK limit.
- **Source:** edit the `.keymap` file, run `make pin-check` (it counts the bindings per layer), then
  `make firmware` and flash as in [flashing.md](flashing.md).
