# Hardware notes

What the worxpad board and case are, in words: the circuit, the pin map, the power tree, the layer stack and
the mechanical stack. The numbers come from [`board.toml`](../board.toml), `pcb/gen/circuit.py` and the
research records; this page repeats them for reading and is not a source of truth. If it disagrees with
`board.toml`, `board.toml` wins.

> **Nothing has been built.** No board has been made or powered, and no case has been milled or printed.

## Contents

- [Circuit, in words](#circuit-in-words)
- [Pin map](#pin-map)
- [Power tree](#power-tree)
- [Layer stack](#layer-stack)
- [Mechanical stack](#mechanical-stack)
- [Case](#case)

## Circuit, in words

- **Radio and MCU.** A u-blox BMD-340 module (nRF52840) on the bottom face, its trace antenna at the right board
  edge, 0.2 mm inside it (D24), over a metal-free bay in the case. The module runs in LV mode: VCC and VCCH both
  on 3V3. It has a 10 uF bulk capacitor, a 32.768 kHz crystal with two 20 pF C0G capacitors, pin reset on
  P0.18 from the reset button SW17 and the SWD pads, and SWD on a Tag-Connect TC2030-NL pad set.
- **Flash.** A 16 MB W25Q128JV on QSPI next to the QSPI pads (D8), for icons. The firmware only keeps it in deep
  power-down today.
- **Display.** A 1.3 inch 240 x 240 IPS panel (ST7789VW) on a 24-pin 0.5 mm FPC into a Hirose FH34SRJ on the
  top face. SPI on SPIM3. The backlight is switched low-side by an AO3400A with a 100 kOhm gate pull-down and a
  15 Ohm series resistor, driven by PWM.
- **USB.** An HRO TYPE-C-31-M-13C receptacle at the rear, 5.1 kOhm on CC1 and CC2, a USBLC6-2SC6 ESD array, then a
  0.75 A PTC. VBUS goes to the charger and to module pad 66 (USB PHY only; see D12).
- **Power.** A BQ24072 charger with power path (USB500 mode, about 400 mA charge), an AO3401A in the cell's
  positive line against reverse polarity, a JST PH battery header, a TPS7A02 3.3 V LDO whose enable is the slide
  switch SW18, and a MAX17048 fuel gauge on BAT, on I2C with 4.7 kOhm pull-ups to 3V3. An NTC on the PCB over
  the cell feeds the charger's TS pin.
- **Inputs.** 16 Choc V2 hot-swap sockets, two PEC12R encoders with push and two B3FS buttons in a 4 row x 5
  column `col2row` matrix with one 1N4148W per position. Column 4 holds the right encoder push (row 0), the left
  encoder push (row 1), the right button (row 2) and the left button (row 3) (D20). Encoder A and B go straight
  to GPIOs with internal pull-ups; 10 nF filter footprints are placed and not fitted (D36).

107 parts in `pcb/gen/circuit.py`: 61 machine-placed, 16 hand-fitted sockets, 4 not-fitted footprints, 26 pads,
holes and fiducials. The schematic: [schematic.pdf](images/pcb/schematic.pdf).

## Pin map

From `board.toml` `[pinmap]`; `tools/check_pins.py` checks it against the circuit and the firmware.

| Function | Pins |
|---|---|
| QSPI flash | P0.19 SCK, P0.17 CSN, P0.20 IO0, P0.21 IO1, P0.22 IO2, P0.23 IO3 |
| Display (SPIM3) | P0.13 SCK, P0.15 MOSI, P0.14 CS, P0.16 DC, P1.00 RESET |
| Backlight PWM | P0.24 |
| I2C to the gauge | P0.07 SDA, P0.11 SCL |
| Charger status | P0.03 /CHG, P0.04 /PGOOD |
| Gauge alert | P0.26 |
| Left encoder | P0.28 A, P0.30 B |
| Right encoder | P0.29 A, P0.31 B |
| Matrix rows (inputs, pull-down) | P1.12 ROW0, P1.13 ROW1, P1.14 ROW2, P1.15 ROW3 |
| Matrix columns (outputs) | P0.02 COL0, P0.25 COL1, P0.27 COL2, P1.05 COL3, P1.06 COL4 |
| Crystal | P0.00 XL1, P0.01 XL2 |
| Reset | P0.18 (gpio-as-nreset; button and SWD) |
| USB | D+, D-, VBUS (pad 66) |
| SWD | SWDIO (TC2030 pin 2), SWCLK (TC2030 pin 4) |
| Spare | P0.05, P0.06, P0.08, P0.09, P0.10, P0.12, P1.01, P1.02, P1.03, P1.04, P1.07 to P1.11 |

## Power tree

```
USB-C VBUS -> USBLC6 ESD -> 1206L075 PTC -> VBUS_SYS -+-> BQ24072 IN (USB500, ~400 mA charge)
                                                      +-> BMD-340 pad 66 (USB PHY only)
cell (PCM) -> AO3401A -> BAT -+-> BQ24072 BAT
                              +-> MAX17048
BQ24072 OUT = VSYS -> TPS7A02 IN, enable from slide switch SW18 -> 3V3
3V3 -> BMD-340 VCC and VCCH, flash, panel VDD and VDDIO, backlight through 15 Ohm, I2C pull-ups
```

| Rail | Range | Consumers |
|---|---|---|
| VBUS | 4.35 to 6.6 V at the charger; worst case 0.51 A in | charger, module USB PHY |
| BAT | 3.0 to 4.2 V | charger, gauge |
| VSYS | 3.0 to 4.5 V | LDO, slide switch |
| 3V3 | 3.3 V, 200 mA LDO; 21.6 uF nominal against the 22 uF limit (D14) | everything else |

Battery current, from research COMPONENTS 4.2 (estimates, nothing measured): off about 8 uA; deep sleep about
31 uA; connected idle with the display blanked about 54 uA with two firmware hooks; display lit with the
backlight at 25 % about 18 mA. Peak on 3V3 about 89 mA.

## Layer stack

4 layers, 1.6 mm, JLCPCB's default JLC04161H-7628 stack, 1 oz outer and 0.5 oz inner copper, ENIG.

| Layer | Use |
|---|---|
| F.Cu | signals, ground pour; top-face parts: J2, SW19, SW20, ENC1, ENC2 |
| In1.Cu | ground plane |
| In2.Cu | 3.3 V plane |
| B.Cu | signals, ground pour; every other part |

Tracks 0.10 mm signal and 0.30 mm or more supply; vias 0.3 / 0.6 mm. No copper of any kind on any layer in the
antenna keep-out (X 119.85 to 124.45, Y 42.90 to 63.10). No impedance was calculated; USB is full speed.
Board 120.65 x 80.30 mm, ordered in a frame panel of 135.65 x 95.30 mm (D23).

## Mechanical stack

Z from the deck (the top face of the top shell), negative downward, from `board.toml` `[stack]`:

| Z (mm) | Level |
|---|---|
| +12.00 | knob top |
| +4.40 | keycap top |
| 0.00 | deck; lens top flush |
| -1.95 | display web underside (0.80 mm web, D10) |
| -4.00 | plate top (switch plate lip, 1.15 mm in CNC) |
| -5.00 | split face between top and bottom shell |
| -6.20 / -7.80 | PCB top / bottom |
| -9.65 | hot-swap socket underside |
| -9.80 | module bottom |
| -10.25 | insulating sheet underside |
| -15.75 | cell bottom, with 0.5 mm swelling allowed |
| -15.95 | battery pocket floor top |
| -14.60 / -20.60 | underside at the front / at the wedge apex |

The case is 128.4 x 85.2 mm in plan, 20.6 mm tall at the wedge apex.

## Case

Two CNC 6061-T6 shells, bead blasted and black anodised. The top shell carries the deck, the key well and the
plate lip, the lens recess, the knob plinth and the button holes, and the C and G posts. The bottom shell
carries the wedge and ramp, the flank scoops, the battery pocket, the K posts, the rear USB-C and switch
notches, the reset pinhole, the foot pockets and the right-wall RF slot closed by a black POM insert. Screws:
4 x M1.6 K from the deck, 2 x M2 C from below, 2 x M2 G holding the PCB to the top shell and grounding it.
Model, checks and drawings: [cad/README.md](../cad/README.md). Order: [ordering-case.md](ordering-case.md).
