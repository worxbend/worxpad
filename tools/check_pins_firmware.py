#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Firmware half of tools/check_pins.py: the ZMK board files against board.toml. Standard library only.

board.toml is the source of truth. The ZMK board definition repeats parts of it by hand:

- worxpad_nrf52840_zmk.dts: matrix, encoder, display, charger-line GPIOs; encoder steps; display clock and
  size; backlight PWM period; the matrix transform and the physical layout (Studio) positions,
- worxpad-pinctrl.dtsi: SPIM3, QSPI, TWIM and PWM pins (default and sleep states),
- worxpad.keymap: one binding per keymap position on every layer, two knob bindings where a layer has any,
- worxpad_nrf52840_zmk_defconfig: the 32.768 kHz crystal that P0.00/P0.01 carry.

tools/check_pins.py runs these checks after its circuit checks. Run alone: python3 tools/check_pins_firmware.py.

The devicetree is read with regular expressions, not a devicetree compiler. It understands the layout of
the files above and fails loudly when a node it needs is missing.
"""
from __future__ import annotations

import re
import sys
import tomllib
from collections.abc import Callable
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOARD_TOML = REPO / "board.toml"
BOARD_DIR = REPO / "firmware" / "zmk" / "boards" / "worxbend" / "worxpad"
DTS = BOARD_DIR / "worxpad_nrf52840_zmk.dts"
PINCTRL = BOARD_DIR / "worxpad-pinctrl.dtsi"
KEYMAP = BOARD_DIR / "worxpad.keymap"
DEFCONFIG = BOARD_DIR / "worxpad_nrf52840_zmk_defconfig"

# Pin-control function -> board.toml net.
PSEL_NET = {
    "SPIM_SCK": "LCD_SCK",
    "SPIM_MOSI": "LCD_MOSI",
    "QSPI_SCK": "QSPI_SCK",
    "QSPI_CSN": "QSPI_CSN",
    "QSPI_IO0": "QSPI_IO0",
    "QSPI_IO1": "QSPI_IO1",
    "QSPI_IO2": "QSPI_IO2",
    "QSPI_IO3": "QSPI_IO3",
    "TWIM_SDA": "I2C_SDA",
    "TWIM_SCL": "I2C_SCL",
    "PWM_OUT0": "BL_PWM",
}

# (devicetree node label, property) -> board.toml nets, one per <&gpioN pin flags> entry in order.
GPIO_NETS = {
    ("kscan", "row-gpios"): ["ROW0", "ROW1", "ROW2", "ROW3"],
    ("kscan", "col-gpios"): ["COL0", "COL1", "COL2", "COL3", "COL4"],
    ("encoder_left", "a-gpios"): ["ENC_L_A"],
    ("encoder_left", "b-gpios"): ["ENC_L_B"],
    ("encoder_right", "a-gpios"): ["ENC_R_A"],
    ("encoder_right", "b-gpios"): ["ENC_R_B"],
    ("mipi_dbi", "dc-gpios"): ["LCD_DC"],
    ("mipi_dbi", "reset-gpios"): ["LCD_RESET"],
    ("&spi3", "cs-gpios"): ["LCD_CS"],
    ("zephyr,user", "chg-gpios"): ["CHG_N"],
    ("zephyr,user", "pgood-gpios"): ["PGOOD_N"],
}

# GPIO nets of [pinmap] that no devicetree pin names, each with the place that covers it instead.
NOT_IN_DEVICETREE = {
    "GAUGE_ALRT_N": "unused: the ZMK MAX17048 driver polls the gauge",
    "XL1": "32.768 kHz crystal, CONFIG_CLOCK_CONTROL_NRF_K32SRC_XTAL",
    "XL2": "32.768 kHz crystal, CONFIG_CLOCK_CONTROL_NRF_K32SRC_XTAL",
    "RESET_N": "pin reset, &uicr gpio-as-nreset (P0.18 is fixed in silicon)",
}

PITCH_UNITS = 100  # physical layout units per key pitch
POSITION_NAMES = ["encoder_left_push", "encoder_right_push", "button_left", "button_right"]

Pin = str  # "P0.13"
Errors = list[str]


# --------------------------------------------------------------------------------------------------------
# Reading the firmware files
# --------------------------------------------------------------------------------------------------------
def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    return re.sub(r"//[^\n]*", "", text)


def node_body(text: str, name: str) -> str:
    """Body of the node `<name> {`, `<name>: <node> {` or `&<name> {`, braces matched."""
    pattern = rf"(?:^|\s)(?:{re.escape(name)}\s*:\s*[\w,@-]+|{re.escape(name)})\s*\{{"
    match = re.search(pattern, text)
    if match is None:
        raise ValueError(f"no devicetree node {name!r}")
    depth, start = 1, match.end()
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start:index]
    raise ValueError(f"unbalanced braces in node {name!r}")


def prop(body: str, name: str) -> str:
    match = re.search(rf"(?:^|[\s;]){re.escape(name)}\s*=\s*(.*?);", body, re.DOTALL)
    if match is None:
        raise ValueError(f"no property {name!r}")
    return match.group(1)


def int_prop(body: str, name: str) -> int:
    return int(prop(body, name).strip().strip("<>").strip(), 0)


def gpio_entries(value: str) -> list[tuple[Pin, str]]:
    """[(pin, flags)] from `<&gpio1 12 (FLAGS)>, ...`."""
    entries = re.findall(r"<\s*&gpio(\d)\s+(\d+)\s+(.*?)>", value, re.DOTALL)
    return [(f"P{port}.{int(pin):02d}", " ".join(flags.split())) for port, pin, flags in entries]


def psel_groups(pinctrl: str) -> dict[str, set[tuple[str, Pin]]]:
    """Pin-control state name -> {(function, pin)}."""
    body = node_body(pinctrl, "&pinctrl")
    groups = {}
    for match in re.finditer(r"(\w+)\s*:\s*\w+\s*\{", body):
        state = node_body(body, match.group(1))
        groups[match.group(1)] = {
            (function, f"P{port}.{int(pin):02d}")
            for function, port, pin in re.findall(r"NRF_PSEL\((\w+),\s*(\d),\s*(\d+)\)", state)
        }
    return groups


class Firmware:
    """The devicetree, pin control, keymap and defconfig text, comments stripped."""

    def __init__(self) -> None:
        self.dts = strip_comments(DTS.read_text())
        self.pinctrl = strip_comments(PINCTRL.read_text())
        self.keymap = strip_comments(KEYMAP.read_text())
        self.defconfig = DEFCONFIG.read_text()

    def gpio_sites(self) -> list[tuple[str, Pin, str]]:
        """[(net, pin, flags)] for every GPIO the devicetree names."""
        sites = []
        for (node, name), nets in GPIO_NETS.items():
            entries = gpio_entries(prop(node_body(self.dts, node), name))
            if len(entries) != len(nets):
                raise ValueError(f"{node} {name}: {len(entries)} pins, expected {len(nets)}")
            sites += [(net, pin, flags) for net, (pin, flags) in zip(nets, entries)]
        return sites

    def psel_sites(self) -> list[tuple[str, Pin]]:
        """[(net, pin)] for every pin-control default state."""
        sites = []
        for state, psels in psel_groups(self.pinctrl).items():
            if state.endswith("_default"):
                sites += [(PSEL_NET[function], pin) for function, pin in sorted(psels)]
        return sites

    def all_sites(self) -> list[tuple[str, Pin]]:
        return [(net, pin) for net, pin, _ in self.gpio_sites()] + self.psel_sites()


# --------------------------------------------------------------------------------------------------------
# Expected values from board.toml
# --------------------------------------------------------------------------------------------------------
def pin_of_net(board: dict) -> dict[str, Pin]:
    """Net -> module GPIO pin, for the GPIO rows of [pinmap] (keys "P0.xx" / "P1.xx")."""
    return {entry[0]: pin for pin, entry in board["pinmap"].items() if pin.startswith("P")}


def function_of_net(board: dict) -> dict[str, str]:
    return {entry[0]: entry[1] for pin, entry in board["pinmap"].items() if pin.startswith("P")}


def layout_units(mm: float, origin: float, pitch: float) -> int:
    """Physical-layout top-left coordinate of a 1u square centred at `mm`; key 0 centre is at `origin`."""
    return round((mm - origin) / pitch * PITCH_UNITS)


# --------------------------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------------------------
def check_gpio_pins(board: dict, fw: Firmware) -> Errors:
    expected = pin_of_net(board)
    errors = []
    for net, pin in fw.all_sites():
        if net not in expected:
            errors.append(f"{net}: not in board.toml [pinmap]")
        elif expected[net] != pin:
            errors.append(f"{net}: firmware {pin}, board.toml {expected[net]}")
    return errors


def check_every_net_used(board: dict, fw: Firmware) -> Errors:
    used = {net for net, _ in fw.all_sites()}
    return [
        f"{net} ({pin}): in board.toml [pinmap] but not in the firmware and not listed as covered elsewhere"
        for net, pin in pin_of_net(board).items()
        if net not in used and net not in NOT_IN_DEVICETREE
    ]


def check_covered_elsewhere(board: dict, fw: Firmware) -> Errors:
    errors = []
    nets = pin_of_net(board)
    for net in NOT_IN_DEVICETREE:
        if net not in nets:
            errors.append(f"{net}: listed as covered elsewhere but not in board.toml [pinmap]")
    if "CONFIG_CLOCK_CONTROL_NRF_K32SRC_XTAL=y" not in fw.defconfig:
        errors.append("XL1/XL2: the defconfig does not select the 32.768 kHz crystal")
    if nets.get("XL1") != "P0.00" or nets.get("XL2") != "P0.01":
        errors.append("XL1/XL2: the nRF52840 crystal pins are P0.00/P0.01")
    if "gpio-as-nreset" not in node_body(fw.dts, "&uicr"):
        errors.append("RESET_N: &uicr has no gpio-as-nreset")
    if nets.get("RESET_N") != "P0.18":
        errors.append("RESET_N: the nRF52840 pin reset is P0.18")
    return errors


def check_pins_unique(board: dict, fw: Firmware) -> Errors:
    seen: dict[Pin, str] = {}
    errors = []
    for net, pin in fw.all_sites():
        if pin in seen and seen[pin] != net:
            errors.append(f"{pin}: used for {seen[pin]} and {net}")
        seen.setdefault(pin, net)
    spare = set(board["pinmap_spare"]["pins"])
    errors += [f"{pin} ({net}): listed as spare in board.toml" for pin, net in seen.items() if pin in spare]
    return errors


def check_pulls(board: dict, fw: Firmware) -> Errors:
    """A [pinmap] function that names a pull must get that internal pull in the devicetree, and only then.

    Exception: the encoder lines, whose internal pull-ups come from the rotary-buttons record, not [pinmap].
    """
    functions = function_of_net(board)
    errors = []
    for net, pin, flags in fw.gpio_sites():
        function = functions.get(net, "")
        for words, flag in (("pull-up", "GPIO_PULL_UP"), ("pull-down", "GPIO_PULL_DOWN")):
            if words in function and flag not in flags:
                errors.append(f"{net} ({pin}): board.toml says {words}, devicetree flags are {flags!r}")
            if words not in function and flag in flags and not net.startswith("ENC_"):
                errors.append(f"{net} ({pin}): devicetree sets {flag}, board.toml names no {words}")
    return errors


def check_sleep_states(board: dict, fw: Firmware) -> Errors:
    groups = psel_groups(fw.pinctrl)
    errors = []
    for state, psels in groups.items():
        if state.endswith("_default"):
            sleep = state.removesuffix("_default") + "_sleep"
            if groups.get(sleep) != psels:
                errors.append(f"{sleep}: missing or not the same pins as {state}")
    return errors


def check_matrix(board: dict, fw: Firmware) -> Errors:
    kscan = node_body(fw.dts, "kscan")
    matrix = board["matrix"]
    errors = []
    direction = prop(kscan, "diode-direction").strip().strip('"')
    if direction != matrix["diode_direction"]:
        errors.append(f"diode-direction {direction}, board.toml {matrix['diode_direction']}")
    rows = [pin for pin, _ in gpio_entries(prop(kscan, "row-gpios"))]
    cols = [pin for pin, _ in gpio_entries(prop(kscan, "col-gpios"))]
    if rows != matrix["rows"]:
        errors.append(f"row-gpios {rows}, board.toml {matrix['rows']}")
    if cols != matrix["columns"]:
        errors.append(f"col-gpios {cols}, board.toml {matrix['columns']}")
    if "wakeup-source" not in kscan:
        errors.append("kscan is not a wakeup-source: keys could not wake the board from deep sleep")
    return errors


def expected_transform(board: dict) -> list[str]:
    """RC(row,col) per keymap position: the keys row by row, then the column-4 positions."""
    keys = board["keys"]
    grid = [f"RC({r},{c})" for r in range(keys["rows"]) for c in range(keys["columns"])]
    matrix_of = {
        "encoder_left_push": board["encoders"]["left"]["matrix"],
        "encoder_right_push": board["encoders"]["right"]["matrix"],
        "button_left": board["buttons"]["left"]["matrix"],
        "button_right": board["buttons"]["right"]["matrix"],
    }
    tail = []
    for name in POSITION_NAMES:
        match = re.fullmatch(r"C(\d)R(\d)", matrix_of[name])
        if match is None:
            raise ValueError(f"board.toml: {name} matrix {matrix_of[name]!r} is not CnRm")
        col, row = match.groups()
        tail.append(f"RC({row},{col})")
    return grid + tail


def check_transform(board: dict, fw: Firmware) -> Errors:
    found = re.findall(r"RC\(\s*\d+\s*,\s*\d+\s*\)", prop(node_body(fw.dts, "transform"), "map"))
    found = [item.replace(" ", "") for item in found]
    expected = expected_transform(board)
    return [] if found == expected else [f"matrix_transform map {found}, expected {expected}"]


def expected_layout(board: dict) -> list[tuple[int, int]]:
    keys = board["keys"]
    grid = [(c * PITCH_UNITS, r * PITCH_UNITS) for r in range(keys["rows"]) for c in range(keys["columns"])]
    parts = [board["encoders"]["left"], board["encoders"]["right"],
             board["buttons"]["left"], board["buttons"]["right"]]
    tail = [(layout_units(part["x"], keys["first_x"], keys["pitch"]),
             layout_units(part["y"], keys["first_y"], keys["pitch"])) for part in parts]
    return grid + tail


def check_physical_layout(board: dict, fw: Firmware) -> Errors:
    keys = prop(node_body(fw.dts, "layout"), "keys")
    attrs = re.findall(r"<&key_physical_attrs\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", keys)
    found = [(int(x), int(y)) for _, _, x, y in attrs]
    expected = expected_layout(board)
    return [] if found == expected else [f"physical layout {found}, expected {expected}"]


def check_encoders(board: dict, fw: Firmware) -> Errors:
    enc = board["encoders"]
    errors = []
    for side in ("left", "right"):
        steps = int_prop(node_body(fw.dts, f"encoder_{side}"), "steps")
        if steps != enc["steps"]:
            errors.append(f"encoder_{side} steps {steps}, board.toml {enc['steps']}")
    sensors = node_body(fw.dts, "sensors")
    triggers = int_prop(sensors, "triggers-per-rotation")
    if triggers != enc["triggers_per_rotation"]:
        errors.append(f"triggers-per-rotation {triggers}, board.toml {enc['triggers_per_rotation']}")
    order = re.findall(r"&(\w+)", prop(sensors, "sensors"))
    if order != ["encoder_left", "encoder_right"]:
        errors.append(f"sensor order {order}: the keymap and the screen expect left, then right")
    return errors


def check_display(board: dict, fw: Firmware) -> Errors:
    display = board["display"]
    lcd = node_body(fw.dts, "lcd")
    errors = []
    if int_prop(lcd, "mipi-max-frequency") != display["spi_mhz"] * 1_000_000:
        errors.append(f"mipi-max-frequency is not board.toml display.spi_mhz {display['spi_mhz']} MHz")
    for name, key in (("width", "width_px"), ("height", "height_px")):
        if int_prop(lcd, name) != display[key]:
            errors.append(f"panel {name} is not board.toml display.{key} {display[key]}")
    spi_dev = prop(node_body(fw.dts, "mipi_dbi"), "spi-dev").strip()
    if spi_dev != {"SPIM3": "<&spi3>"}.get(display["bus"]):
        errors.append(f"spi-dev {spi_dev}, board.toml display.bus {display['bus']}")
    pwms = prop(node_body(fw.dts, "backlight"), "pwms")
    period = re.search(r"PWM_USEC\((\d+)\)", pwms)
    if period is None or int(period.group(1)) != display["backlight"]["pwm_period_us"]:
        errors.append(f"backlight pwms {pwms!r}, board.toml period {display['backlight']['pwm_period_us']} us")
    return errors


def check_keymap(board: dict, fw: Firmware) -> Errors:
    positions = board["keys"]["rows"] * board["keys"]["columns"] + len(board["matrix"]["c4"])
    layers = re.findall(r"(\w+)\s*\{(.*?)\};", node_body(fw.keymap, "keymap"), re.DOTALL)
    errors = [] if layers else ["no layers in the keymap"]
    for name, layer in layers:
        bindings = re.search(r"\bbindings\s*=\s*<(.*?)>\s*;", layer, re.DOTALL)
        count = len(re.findall(r"&\w+", bindings.group(1))) if bindings else 0
        if count != positions:
            errors.append(f"layer {name}: {count} bindings, {positions} keymap positions")
        sensors = re.search(r"sensor-bindings\s*=\s*<(.*?)>\s*;", layer, re.DOTALL)
        if sensors and len(re.findall(r"&\w+", sensors.group(1))) != 2:
            errors.append(f"layer {name}: sensor-bindings must name both knobs")
    return errors


CHECKS: list[tuple[str, Callable[[dict, Firmware], Errors]]] = [
    ("firmware GPIO and pin-control pins match [pinmap]", check_gpio_pins),
    ("every [pinmap] GPIO net is in the firmware or covered elsewhere", check_every_net_used),
    ("crystal and reset pins covered by defconfig and &uicr", check_covered_elsewhere),
    ("no pin used twice, no spare pin used", check_pins_unique),
    ("internal pulls match [pinmap]", check_pulls),
    ("every pin-control default state has the same sleep state", check_sleep_states),
    ("matrix direction, rows and columns", check_matrix),
    ("matrix transform order", check_transform),
    ("physical layout positions", check_physical_layout),
    ("encoder steps, triggers and order", check_encoders),
    ("display bus, clock, size and backlight period", check_display),
    ("keymap binding counts", check_keymap),
]


def run(board: dict) -> int:
    """Run every firmware check, print one line each, return the number that failed."""
    fw = Firmware()
    failed = 0
    for title, check in CHECKS:
        try:
            errors = check(board, fw)
        except (ValueError, KeyError, AttributeError) as exc:
            errors = [f"could not run: {exc!r}"]
        print(f"{'ok  ' if not errors else 'FAIL'}  firmware: {title}")
        for error in errors:
            print(f"        {error}")
        failed += bool(errors)
    print(f"check_pins firmware: {len(CHECKS) - failed} of {len(CHECKS)} checks pass")
    return failed


if __name__ == "__main__":
    sys.exit(1 if run(tomllib.loads(BOARD_TOML.read_text())) else 0)
