# Flashing

Nothing on this page has been done on a worxpad board. No board exists yet. The steps follow the mcu-radio
record (`research/components/mcu-radio.md` 7.7) and the usb-io record (`research/components/usb-io.md` 6.5, 6.6).

## What runs on the board

| Part | What | Where it comes from |
| --- | --- | --- |
| Bootloader | Adafruit nRF52 UF2 bootloader 0.11.0, with the SoftDevice S140 v6 area below 0x26000 | flashed once over SWD |
| Application | ZMK, `firmware/dist/worxpad.uf2`, from 0x26000 | `make firmware`, then copied as a file |
| Settings | Bluetooth bonds and ZMK Studio keymap changes, 32 KB at 0xEC000 | written by the firmware |

The application layout is the one ZMK uses for the nice!nano, so the image also assumes that bootloader layout.

## First flash: the bootloader over SWD

Assumption, not yet done: the Adafruit bootloader has no worxpad board header. Before the first board arrives,
add one to a copy of the Adafruit_nRF52_Bootloader 0.11.0 source with:

- the status LED and the DFU or FRST button pins set to spare pins from `[pinmap_spare]` in `board.toml`, so
  the bootloader never drives a display, flash or matrix line;
- the reset pin P0.18 written to UICR PSELRESET (the application's `gpio-as-nreset` also writes it on first
  boot if it is still empty);
- the USB product name `worxpad`.

0.11.0 adds write protection of the MBR and bootloader and a jump to the application on USB disconnect. Neither
is tested with ZMK; 0.10.0 is the fallback.

Connect a probe to the TC2030-NL pads on the bottom face (SWDIO pad 2, SWCLK pad 4; module pads 44 and 43), with
the slide switch on and the cell or USB powering the board. Then, with nrfjprog:

```bash
nrfjprog --family NRF52 --recover
nrfjprog --family NRF52 --program worxpad_bootloader.hex --chiperase --verify
nrfjprog --family NRF52 --reset
```

`worxpad_bootloader.hex` stands for the bootloader and SoftDevice hex that the build above produces; it does
not exist yet. pyOCD or OpenOCD with any CMSIS-DAP probe work the same way.

## Updates: drag and drop over USB

1. Build: `make firmware` (or `bash firmware/build.sh`). It writes `firmware/dist/worxpad.uf2`.
2. Enter the bootloader, either way:
   - hold the left button and press row 4, column 4 (`&bootloader` on the System layer), or
   - press the reset button twice within 500 ms through the pinhole in the floor.
3. A USB drive appears. Copy `worxpad.uf2` onto it. The board restarts into the new firmware when the copy
   ends.

If the drive does not appear, the bootloader is missing or damaged; flash it again over SWD.

## Bluetooth

- Four profiles. Hold the left button and press row 2 to pick profile 1 to 4. A new profile advertises until a
  host pairs.
- To pair again with a host: pick its profile, then hold the left button and press row 3, column 3 (clear the
  bond), and remove the board on the host as well.
- The status bar shows the Bluetooth symbol and the profile number, grey while not connected, or USB.

## Checks before flashing

- `make test` runs `tools/check_pins.py`: the firmware pins against `board.toml`.
- `make firmware` must end with "wrote firmware/dist/worxpad.uf2". The memory summary from the last build is in
  [`firmware/README.md`](../firmware/README.md).
