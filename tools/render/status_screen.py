"""Draw the 240 x 240 status screen the firmware shows on the Edit layer, for the display in the renders.

Run with the case venv (it has Pillow): `cad/.venv/bin/python tools/render/status_screen.py OUT.png`.

The layout, colours and label texts follow firmware/zmk/src/status_screen.c and labels.c; the key and knob
functions are read from the default keymap. This is a drawing of what the code should show, not a capture:
the firmware has never run on a panel. Two differences from the device: LVGL's symbol glyphs (Bluetooth, USB)
are written as text, and the status bar shows a sample state (Bluetooth profile 1 connected, 84 %).
"""

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
KEYMAP = REPO / "firmware/zmk/boards/worxbend/worxpad/worxpad.keymap"
LAYER = "edit"
FONTS = (  # LVGL's own Montserrat once the firmware workspace exists, else a common system font
    REPO / "firmware/.build/ws/modules/lib/gui/lvgl/scripts/built_in_font/Montserrat-Medium.ttf",
    Path("/usr/share/fonts/TTF/DejaVuSans.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
)

# Geometry and colours copied from status_screen.c
SCREEN_PX, KNOB_H, GRID_COLS, GRID_Y = 240, 40, 4, 44
CELL_W, CELL_H, CELL_GAP, CELL_RADIUS = 57, 38, 4, 6
STATUS_Y, SIDE_PAD = 212, 6
PAPER, CELL, INK, DIM, ACCENT = "#101418", "#252c34", "#e8ecef", "#8a96a3", "#4fb3bf"
SAMPLE_OUTPUT, SAMPLE_BATTERY = "BT 1", "84 %"

# The subset of labels.c `named` that the keymap uses, keyed by the &kp parameter as written in the keymap
LABELS = {
    "LC(Z)": "Undo", "LC(LS(Z))": "Redo", "LC(S)": "Save", "LC(LS(S))": "Save as", "LC(X)": "Cut",
    "LC(C)": "Copy", "LC(V)": "Paste", "LC(A)": "All", "LC(F)": "Find", "LC(N0)": "Fit", "LC(EQUAL)": "Zoom+",
    "LC(MINUS)": "Zoom-", "ESC": "Esc", "DEL": "Del", "BSPC": "Bksp", "TAB": "Tab", "ENTER": "Enter",
    "SPACE": "Space", "LSHFT": "Shift", "LCTRL": "Ctrl", "LALT": "Alt", "HOME": "Home", "END": "End",
    "PG_UP": "PgUp", "PG_DN": "PgDn", "C_VOL_UP": "Vol+", "C_VOL_DN": "Vol-", "C_BRI_UP": "Bri+",
    "C_BRI_DN": "Bri-",
}


def font_file() -> Path:
    for path in FONTS:
        if path.is_file():
            return path
    raise FileNotFoundError(f"no font found; tried {', '.join(map(str, FONTS))}")


def layer_block(keymap: str, layer: str) -> str:
    match = re.search(rf"\b{layer}\s*{{(.*?)\n\s*}};", keymap, re.DOTALL)
    if match is None:
        raise ValueError(f"layer {layer!r} not found in {KEYMAP}")
    return match.group(1)


def bindings(block: str, prop: str) -> list[list[str]]:
    """The bindings of one property as [behaviour, parameter, ...] lists."""
    match = re.search(rf"\b{prop}\s*=\s*<(.*?)>;", block, re.DOTALL)
    if match is None:
        raise ValueError(f"property {prop!r} not found in layer {LAYER!r}")
    return [entry.split() for entry in match.group(1).split("&") if entry.strip()]


def key_label(binding: list[str]) -> str:
    behaviour, *params = binding
    if behaviour != "kp":
        raise ValueError(f"no label rule for &{behaviour} on the {LAYER} layer")
    return LABELS.get(params[0], params[0])


def knob_label(binding: list[str]) -> str:
    """inc_dec_kp CW CCW is shown as 'CCW / CW', as worxpad_sensor_label does."""
    behaviour, clockwise, counter = binding
    if behaviour != "inc_dec_kp":
        raise ValueError(f"no label rule for sensor &{behaviour}")
    return f"{LABELS.get(counter, counter)} / {LABELS.get(clockwise, clockwise)}"


def knob_box(width: int, turn: str, push: str, font: dict) -> Image.Image:
    """One knob panel. Its labels are clipped at the panel edges (LV_LABEL_LONG_CLIP, centred), so a label
    wider than the panel loses both ends, as it would on the panel."""
    box = Image.new("RGB", (width, KNOB_H), PAPER)
    pen = ImageDraw.Draw(box)
    pen.text((width / 2, 2), turn, fill=ACCENT, font=font[16], anchor="mt")
    pen.text((width / 2, KNOB_H - 2), push, fill=DIM, font=font[12], anchor="mb")
    return box


def draw(out: Path) -> None:
    block = layer_block(KEYMAP.read_text(), LAYER)
    name = re.search(r'display-name\s*=\s*"([^"]+)"', block).group(1)
    keys = bindings(block, "bindings")
    knobs = bindings(block, "sensor-bindings")
    face = font_file()
    font = {size: ImageFont.truetype(str(face), size) for size in (12, 14, 16)}

    image = Image.new("RGB", (SCREEN_PX, SCREEN_PX), PAPER)
    pen = ImageDraw.Draw(image)
    half = (SCREEN_PX - CELL_GAP) // 2
    for knob, push_position in enumerate((16, 17)):
        box = knob_box(half, knob_label(knobs[knob]), f"push: {key_label(keys[push_position])}", font)
        image.paste(box, (knob * (half + CELL_GAP), 0))
    for position in range(GRID_COLS * GRID_COLS):
        col, row = position % GRID_COLS, position // GRID_COLS
        x, y = col * (CELL_W + CELL_GAP), GRID_Y + row * (CELL_H + CELL_GAP)
        pen.rounded_rectangle((x, y, x + CELL_W - 1, y + CELL_H - 1), CELL_RADIUS, fill=CELL)
        pen.text((x + CELL_W / 2, y + CELL_H / 2), key_label(keys[position]), fill=INK, font=font[14], anchor="mm")
    middle = STATUS_Y + (SCREEN_PX - STATUS_Y) / 2
    pen.text((SIDE_PAD, middle), name, fill=ACCENT, font=font[16], anchor="lm")
    pen.text((SCREEN_PX / 2, middle), SAMPLE_OUTPUT, fill=INK, font=font[16], anchor="mm")
    pen.text((SCREEN_PX - SIDE_PAD, middle), SAMPLE_BATTERY, fill=INK, font=font[16], anchor="rm")
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out)
    print(f"drew {out} with {face.name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: status_screen.py OUT.png", file=sys.stderr)
        sys.exit(2)
    draw(Path(sys.argv[1]))
