/*
 * SPDX-License-Identifier: MIT
 *
 * Binding labels for the worxpad status screen. Behaviours are told apart by device name, taken from
 * the devicetree node labels in ZMK's behaviors.dtsi, so a renamed node falls back to its raw name.
 */

#include <stdio.h>
#include <string.h>

#include <zephyr/devicetree.h>
#include <zephyr/device.h>
#include <zephyr/sys/util.h>
#include <lvgl.h>

#include <zmk/keymap.h>

#include "labels.h"

/* keys.h defines one- and two-letter macros (A, C, UP, ...). It comes last so no later header sees them. */
#include <dt-bindings/zmk/bt.h>
#include <dt-bindings/zmk/outputs.h>
#include <dt-bindings/zmk/keys.h>

/* Device name of a behaviour node, or "" when ZMK left the node out (/omit-if-no-ref/). */
#define BEHAVIOR_NAME(node_label)                                                                  \
    COND_CODE_1(DT_NODE_EXISTS(DT_NODELABEL(node_label)),                                          \
                (DEVICE_DT_NAME(DT_NODELABEL(node_label))), (""))

struct usage_label {
    uint32_t usage; /* encoded as in a &kp parameter: modifiers in bits 24 to 31 */
    const char *text;
};

/* Chords and keys the default keymap uses, plus common ones. Anything else is spelled out below. */
static const struct usage_label named[] = {
    {LC(Z), "Undo"},
    {LC(LS(Z)), "Redo"},
    {LC(S), "Save"},
    {LC(LS(S)), "Save as"},
    {LC(X), "Cut"},
    {LC(C), "Copy"},
    {LC(V), "Paste"},
    {LC(A), "All"},
    {LC(F), "Find"},
    {LC(N0), "Fit"},
    {LC(EQUAL), "Zoom+"},
    {LC(MINUS), "Zoom-"},
    {LC(TAB), "Tab" LV_SYMBOL_RIGHT},
    {LC(LS(TAB)), LV_SYMBOL_LEFT "Tab"},
    {ESC, "Esc"},
    {DEL, "Del"},
    {BSPC, "Bksp"},
    {TAB, "Tab"},
    {ENTER, "Enter"},
    {SPACE, "Space"},
    {LSHFT, "Shift"},
    {LCTRL, "Ctrl"},
    {LALT, "Alt"},
    {LGUI, "Gui"},
    {HOME, "Home"},
    {END, "End"},
    {PG_UP, "PgUp"},
    {PG_DN, "PgDn"},
    {UP, LV_SYMBOL_UP},
    {DOWN, LV_SYMBOL_DOWN},
    {LEFT, LV_SYMBOL_LEFT},
    {RIGHT, LV_SYMBOL_RIGHT},
    {C_PREV, LV_SYMBOL_PREV},
    {C_PP, LV_SYMBOL_PLAY},
    {C_NEXT, LV_SYMBOL_NEXT},
    {C_MUTE, LV_SYMBOL_MUTE},
    {C_VOL_UP, "Vol+"},
    {C_VOL_DN, "Vol-"},
    {C_BRI_UP, "Bri+"},
    {C_BRI_DN, "Bri-"},
};

/* Keyboard page usage IDs (HID Usage Tables, page 0x07). */
#define USAGE_A 0x04
#define USAGE_Z 0x1D
#define USAGE_1 0x1E
#define USAGE_0 0x27
#define USAGE_F1 0x3A
#define USAGE_F12 0x45
#define USAGE_F13 0x68
#define USAGE_F24 0x73

/* Base key without modifiers: letter, digit or F key, else the page and usage in hex. */
static void base_key_label(uint32_t usage, char *buf, size_t len) {
    const uint32_t page = ZMK_HID_USAGE_PAGE(usage);
    const uint32_t id = ZMK_HID_USAGE_ID(usage);

    if (page == HID_USAGE_KEY && id >= USAGE_A && id <= USAGE_Z) {
        snprintf(buf, len, "%c", (char)('A' + (id - USAGE_A)));
    } else if (page == HID_USAGE_KEY && id >= USAGE_1 && id <= USAGE_0) {
        snprintf(buf, len, "%c", id == USAGE_0 ? '0' : (char)('1' + (id - USAGE_1)));
    } else if (page == HID_USAGE_KEY && id >= USAGE_F1 && id <= USAGE_F12) {
        snprintf(buf, len, "F%u", (unsigned)(id - USAGE_F1 + 1));
    } else if (page == HID_USAGE_KEY && id >= USAGE_F13 && id <= USAGE_F24) {
        snprintf(buf, len, "F%u", (unsigned)(id - USAGE_F13 + 13));
    } else {
        snprintf(buf, len, "%02X:%02X", (unsigned)page, (unsigned)id);
    }
}

static void usage_label(uint32_t encoded, char *buf, size_t len) {
    for (size_t i = 0; i < ARRAY_SIZE(named); i++) {
        if (named[i].usage == encoded) {
            snprintf(buf, len, "%s", named[i].text);
            return;
        }
    }

    const uint8_t mods = SELECT_MODS(encoded);
    char base[8];
    base_key_label(STRIP_MODS(encoded), base, sizeof(base));
    snprintf(buf, len, "%s%s%s%s%s", (mods & (MOD_LCTL | MOD_RCTL)) ? "C-" : "",
             (mods & (MOD_LSFT | MOD_RSFT)) ? "S-" : "", (mods & (MOD_LALT | MOD_RALT)) ? "A-" : "",
             (mods & (MOD_LGUI | MOD_RGUI)) ? "G-" : "", base);
}

static void bt_label(const struct zmk_behavior_binding *binding, char *buf, size_t len) {
    switch (binding->param1) {
    case BT_SEL_CMD:
        snprintf(buf, len, "BT%u", (unsigned)binding->param2 + 1);
        break;
    case BT_NXT_CMD:
        snprintf(buf, len, "BT" LV_SYMBOL_RIGHT);
        break;
    case BT_PRV_CMD:
        snprintf(buf, len, LV_SYMBOL_LEFT "BT");
        break;
    case BT_CLR_CMD:
        snprintf(buf, len, "BT clr");
        break;
    case BT_CLR_ALL_CMD:
        snprintf(buf, len, "Clr all");
        break;
    default:
        snprintf(buf, len, "BT?");
        break;
    }
}

static void out_label(const struct zmk_behavior_binding *binding, char *buf, size_t len) {
    switch (binding->param1) {
    case OUT_USB:
        snprintf(buf, len, LV_SYMBOL_USB);
        break;
    case OUT_BLE:
        snprintf(buf, len, LV_SYMBOL_BLUETOOTH);
        break;
    case OUT_TOG:
        snprintf(buf, len, "USB/BT");
        break;
    default:
        snprintf(buf, len, "Out?");
        break;
    }
}

static void layer_label(const struct zmk_behavior_binding *binding, char *buf, size_t len) {
    const char *name = zmk_keymap_layer_name((zmk_keymap_layer_id_t)binding->param1);
    if (name != NULL && name[0] != '\0') {
        snprintf(buf, len, "%s", name);
    } else {
        snprintf(buf, len, "L%u", (unsigned)binding->param1);
    }
}

static bool is(const struct zmk_behavior_binding *binding, const char *name) {
    return name[0] != '\0' && strcmp(binding->behavior_dev, name) == 0;
}

bool worxpad_binding_is_transparent(const struct zmk_behavior_binding *binding) {
    return binding->behavior_dev != NULL && is(binding, BEHAVIOR_NAME(trans));
}

void worxpad_binding_label(const struct zmk_behavior_binding *binding, char *buf, size_t len) {
    if (binding == NULL || binding->behavior_dev == NULL || is(binding, BEHAVIOR_NAME(none))) {
        snprintf(buf, len, "%s", "");
    } else if (is(binding, BEHAVIOR_NAME(kp))) {
        usage_label(binding->param1, buf, len);
    } else if (is(binding, BEHAVIOR_NAME(mo)) || is(binding, BEHAVIOR_NAME(to)) ||
               is(binding, BEHAVIOR_NAME(tog)) || is(binding, BEHAVIOR_NAME(sl))) {
        layer_label(binding, buf, len);
    } else if (is(binding, BEHAVIOR_NAME(bt))) {
        bt_label(binding, buf, len);
    } else if (is(binding, BEHAVIOR_NAME(out))) {
        out_label(binding, buf, len);
    } else if (is(binding, BEHAVIOR_NAME(bootloader))) {
        snprintf(buf, len, "Boot");
    } else if (is(binding, BEHAVIOR_NAME(sys_reset))) {
        snprintf(buf, len, "Reset");
    } else if (is(binding, BEHAVIOR_NAME(studio_unlock))) {
        snprintf(buf, len, "Studio");
    } else {
        snprintf(buf, len, "%s", binding->behavior_dev);
    }
}

void worxpad_sensor_label(const struct zmk_behavior_binding *binding, char *buf, size_t len) {
    if (binding == NULL || binding->behavior_dev == NULL) {
        snprintf(buf, len, "%s", "");
    } else if (is(binding, BEHAVIOR_NAME(inc_dec_kp))) {
        char ccw[12];
        char cw[12];
        usage_label(binding->param2, ccw, sizeof(ccw));
        usage_label(binding->param1, cw, sizeof(cw));
        snprintf(buf, len, "%s / %s", ccw, cw);
    } else {
        snprintf(buf, len, "%s", binding->behavior_dev);
    }
}
