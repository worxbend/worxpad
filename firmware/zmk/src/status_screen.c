/*
 * SPDX-License-Identifier: MIT
 *
 * worxpad status screen on the 240 x 240 panel. The knobs sit behind the panel and the buttons in front
 * of it, so the knob functions go at the top:
 *
 *     +--------------------+--------------------+
 *     | left knob turn     | right knob turn    |   y 0 to 40
 *     | push: ...          | push: ...          |
 *     +----+----+----+----+---------------------+
 *     |    |    |    |    |                         4 x 4 key functions of the active layer,
 *     ... 4 x 4 ...                                 y 44 to 208, same order as the keys
 *     +-----------------------------------------+
 *     | Layer       BT2 / USB          84 %     |   y 212 to 240
 *     +-----------------------------------------+
 *
 * Labels come from the live keymap (labels.c), so ZMK Studio edits show after the next layer change.
 * No clock: the board has no time source until the host widget channel exists (mcu-radio 5.4).
 */

#include <stdio.h>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/logging/log.h>
#include <lvgl.h>

#include <zmk/battery.h>
#include <zmk/ble.h>
#include <zmk/display.h>
#include <zmk/display/status_screen.h>
#include <zmk/endpoints.h>
#include <zmk/event_manager.h>
#include <zmk/events/battery_state_changed.h>
#include <zmk/events/ble_active_profile_changed.h>
#include <zmk/events/endpoint_changed.h>
#include <zmk/events/layer_state_changed.h>
#include <zmk/events/usb_conn_state_changed.h>
#include <zmk/keymap.h>
#include <zmk/sensors.h>
#include <zmk/usb.h>

#include "labels.h"

LOG_MODULE_DECLARE(zmk, CONFIG_ZMK_LOG_LEVEL);

/* Geometry in pixels */
#define SCREEN_PX 240
#define KNOB_H 40
#define GRID_COLS 4
#define GRID_ROWS 4
#define GRID_Y 44
#define CELL_W 57
#define CELL_H 38
#define CELL_GAP 4
#define CELL_RADIUS 6
#define STATUS_Y 212
#define STATUS_H (SCREEN_PX - STATUS_Y)
#define SIDE_PAD 6

/* Colours: our own dark scheme */
#define COLOUR_PAPER 0x101418
#define COLOUR_CELL 0x252c34
#define COLOUR_INK 0xe8ecef
#define COLOUR_DIM 0x8a96a3
#define COLOUR_ACCENT 0x4fb3bf
#define COLOUR_WARN 0xe5534b

/* Battery level that turns the number red (power record 7.2: warn at 10 %) */
#define BATTERY_WARN_PERCENT 10

/* Period of the charger line poll while it runs (see charger_poll_cb) */
#define CHARGER_POLL_MS 1000

/* Keymap positions (matrix_transform in the board devicetree) */
#define GRID_KEYS (GRID_COLS * GRID_ROWS)
#define POS_LEFT_PUSH 16
#define POS_RIGHT_PUSH 17
#define KNOBS 2

#define LABEL_LEN 12
#define KNOB_LABEL_LEN 28
#define LAYER_NAME_LEN 16

BUILD_ASSERT(ZMK_KEYMAP_SENSORS_LEN == KNOBS, "the screen shows exactly two knobs");

/* ------------------------------------------------------------------------------------------------ */
/* Knob bindings per layer. ZMK keeps its sensor keymap private, so read it from the devicetree in the  */
/* same way keymap.c does. Studio cannot edit sensor bindings, so a compile-time copy stays correct.    */
/* ------------------------------------------------------------------------------------------------ */

#define SENSOR_ENTRY(idx, layer)                                                                   \
    {                                                                                              \
        .behavior_dev = DEVICE_DT_NAME(DT_PHANDLE_BY_IDX(layer, sensor_bindings, idx)),            \
        .param1 = COND_CODE_0(DT_PHA_HAS_CELL_AT_IDX(layer, sensor_bindings, idx, param1), (0),    \
                              (DT_PHA_BY_IDX(layer, sensor_bindings, idx, param1))),               \
        .param2 = COND_CODE_0(DT_PHA_HAS_CELL_AT_IDX(layer, sensor_bindings, idx, param2), (0),    \
                              (DT_PHA_BY_IDX(layer, sensor_bindings, idx, param2))),               \
    }

#define LAYER_SENSORS(layer)                                                                       \
    {COND_CODE_1(DT_NODE_HAS_PROP(layer, sensor_bindings),                                         \
                 (LISTIFY(DT_PROP_LEN(layer, sensor_bindings), SENSOR_ENTRY, (, ), layer)), ())}

static const struct zmk_behavior_binding knob_map[ZMK_KEYMAP_LAYERS_LEN][KNOBS] = {
    ZMK_KEYMAP_LAYERS_FOREACH_SEP(LAYER_SENSORS, (, ))};

/* ------------------------------------------------------------------------------------------------ */
/* Charger status lines (zephyr,user in the board devicetree)                                        */
/* ------------------------------------------------------------------------------------------------ */

static const struct gpio_dt_spec chg_line = GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), chg_gpios);
static const struct gpio_dt_spec pgood_line = GPIO_DT_SPEC_GET(DT_PATH(zephyr_user), pgood_gpios);

/* True while the charger reports power good and charging. A read error counts as not charging. */
static bool charging(void) {
    return gpio_pin_get_dt(&pgood_line) == 1 && gpio_pin_get_dt(&chg_line) == 1;
}

static int init_charger_lines(void) {
    int err = gpio_pin_configure_dt(&chg_line, GPIO_INPUT);
    if (err == 0) {
        err = gpio_pin_configure_dt(&pgood_line, GPIO_INPUT);
    }
    return err;
}

/* ------------------------------------------------------------------------------------------------ */
/* Screen objects                                                                                   */
/* ------------------------------------------------------------------------------------------------ */

static struct {
    lv_obj_t *knob_turn[KNOBS];
    lv_obj_t *knob_push[KNOBS];
    lv_obj_t *keys[GRID_KEYS];
    lv_obj_t *layer;
    lv_obj_t *output;
    lv_obj_t *battery;
} ui;

/* ------------------------------------------------------------------------------------------------ */
/* Layer view: layer name, knob functions, key functions                                            */
/* ------------------------------------------------------------------------------------------------ */

struct layer_view {
    char layer[LAYER_NAME_LEN];
    char knob_turn[KNOBS][KNOB_LABEL_LEN];
    char knob_push[KNOBS][LABEL_LEN];
    char keys[GRID_KEYS][LABEL_LEN];
};

/* Binding that a press at this position runs now: the highest active layer that is not &trans. */
static const struct zmk_behavior_binding *active_key_binding(uint32_t position) {
    for (int index = ZMK_KEYMAP_LAYERS_LEN - 1; index >= 0; index--) {
        const zmk_keymap_layer_id_t id = zmk_keymap_layer_index_to_id(index);
        if (id == ZMK_KEYMAP_LAYER_ID_INVAL || !zmk_keymap_layer_active(id)) {
            continue;
        }
        const struct zmk_behavior_binding *binding =
            zmk_keymap_get_layer_binding_at_idx(id, position);
        if (binding != NULL && binding->behavior_dev != NULL &&
            !worxpad_binding_is_transparent(binding)) {
            return binding;
        }
    }
    return NULL;
}

/* Knob binding a turn runs now: the highest active layer that has sensor bindings. */
static const struct zmk_behavior_binding *active_knob_binding(int knob) {
    for (int index = ZMK_KEYMAP_LAYERS_LEN - 1; index >= 0; index--) {
        const zmk_keymap_layer_id_t id = zmk_keymap_layer_index_to_id(index);
        if (id >= ZMK_KEYMAP_LAYERS_LEN || !zmk_keymap_layer_active(id)) {
            continue;
        }
        if (knob_map[id][knob].behavior_dev != NULL) {
            return &knob_map[id][knob];
        }
    }
    return NULL;
}

static struct layer_view layer_view_get(const zmk_event_t *eh) {
    ARG_UNUSED(eh);
    struct layer_view view;
    const char *name = zmk_keymap_layer_name(
        zmk_keymap_layer_index_to_id(zmk_keymap_highest_layer_active()));
    snprintf(view.layer, sizeof(view.layer), "%s", name != NULL ? name : "");

    const uint32_t push_position[KNOBS] = {POS_LEFT_PUSH, POS_RIGHT_PUSH};
    for (int knob = 0; knob < KNOBS; knob++) {
        worxpad_sensor_label(active_knob_binding(knob), view.knob_turn[knob], KNOB_LABEL_LEN);
        worxpad_binding_label(active_key_binding(push_position[knob]), view.knob_push[knob],
                              LABEL_LEN);
    }
    for (uint32_t key = 0; key < GRID_KEYS; key++) {
        worxpad_binding_label(active_key_binding(key), view.keys[key], LABEL_LEN);
    }
    return view;
}

static void layer_view_show(struct layer_view view) {
    lv_label_set_text(ui.layer, view.layer);
    for (int knob = 0; knob < KNOBS; knob++) {
        lv_label_set_text(ui.knob_turn[knob], view.knob_turn[knob]);
        lv_label_set_text_fmt(ui.knob_push[knob], "push: %s", view.knob_push[knob]);
    }
    for (int key = 0; key < GRID_KEYS; key++) {
        lv_label_set_text(ui.keys[key], view.keys[key]);
    }
}

ZMK_DISPLAY_WIDGET_LISTENER(worxpad_layer_view, struct layer_view, layer_view_show, layer_view_get)
ZMK_SUBSCRIPTION(worxpad_layer_view, zmk_layer_state_changed);

/* ------------------------------------------------------------------------------------------------ */
/* Output: USB, or the Bluetooth profile and whether it is connected                                */
/* ------------------------------------------------------------------------------------------------ */

struct output_view {
    struct zmk_endpoint_instance endpoint;
    bool connected;
};

static struct output_view output_view_get(const zmk_event_t *eh) {
    ARG_UNUSED(eh);
    return (struct output_view){
        .endpoint = zmk_endpoint_get_selected(),
        .connected = zmk_ble_active_profile_is_connected(),
    };
}

static void output_view_show(struct output_view view) {
    if (view.endpoint.transport == ZMK_TRANSPORT_NONE) {
        lv_label_set_text(ui.output, "no host");
        lv_obj_set_style_text_color(ui.output, lv_color_hex(COLOUR_DIM), LV_PART_MAIN);
        return;
    }
    if (view.endpoint.transport == ZMK_TRANSPORT_USB) {
        lv_label_set_text(ui.output, LV_SYMBOL_USB " USB");
        lv_obj_set_style_text_color(ui.output, lv_color_hex(COLOUR_INK), LV_PART_MAIN);
        return;
    }
    lv_label_set_text_fmt(ui.output, LV_SYMBOL_BLUETOOTH " %u",
                          (unsigned)view.endpoint.ble.profile_index + 1);
    lv_obj_set_style_text_color(ui.output, lv_color_hex(view.connected ? COLOUR_INK : COLOUR_DIM),
                                LV_PART_MAIN);
}

ZMK_DISPLAY_WIDGET_LISTENER(worxpad_output_view, struct output_view, output_view_show,
                            output_view_get)
ZMK_SUBSCRIPTION(worxpad_output_view, zmk_endpoint_changed);
ZMK_SUBSCRIPTION(worxpad_output_view, zmk_ble_active_profile_changed);

/* ------------------------------------------------------------------------------------------------ */
/* Battery: state of charge from the MAX17048, charging from the BQ24072 lines                       */
/* ------------------------------------------------------------------------------------------------ */

struct battery_view {
    uint8_t percent;
    bool charging;
};

static struct battery_view battery_view_get(const zmk_event_t *eh) {
    const struct zmk_battery_state_changed *ev = eh != NULL ? as_zmk_battery_state_changed(eh) : NULL;
    return (struct battery_view){
        .percent = ev != NULL ? ev->state_of_charge : zmk_battery_state_of_charge(),
        .charging = charging(),
    };
}

static void battery_view_show(struct battery_view view) {
    lv_label_set_text_fmt(ui.battery, "%s%u %%", view.charging ? LV_SYMBOL_CHARGE " " : "",
                          (unsigned)view.percent);
    const bool low = !view.charging && view.percent < BATTERY_WARN_PERCENT;
    lv_obj_set_style_text_color(ui.battery, lv_color_hex(low ? COLOUR_WARN : COLOUR_INK),
                                LV_PART_MAIN);
}

ZMK_DISPLAY_WIDGET_LISTENER(worxpad_battery_view, struct battery_view, battery_view_show,
                            battery_view_get)
ZMK_SUBSCRIPTION(worxpad_battery_view, zmk_battery_state_changed);
ZMK_SUBSCRIPTION(worxpad_battery_view, zmk_usb_conn_state_changed);

/*
 * /CHG and /PGOOD raise no ZMK event, and ZMK raises battery_state_changed only when the percentage moves, so
 * the end of a charge at 100 % or a /CHG edge just after plug-in would leave a stale mark. Poll the lines
 * while they can change: on USB power, and after unplugging until the mark is off. On battery alone the
 * lines cannot change, so the poll stops and costs nothing there.
 */
static void charger_poll_cb(struct k_work *work);
K_WORK_DELAYABLE_DEFINE(charger_poll, charger_poll_cb);

static void charger_poll_cb(struct k_work *work) {
    ARG_UNUSED(work);
    static bool shown;
    const bool now = charging();
    if (now != shown) {
        shown = now;
        worxpad_battery_view_cb(NULL);
    }
    if (now || zmk_usb_is_powered()) {
        k_work_schedule(&charger_poll, K_MSEC(CHARGER_POLL_MS));
    }
}

static int charger_poll_start(const zmk_event_t *eh) {
    ARG_UNUSED(eh);
    k_work_schedule(&charger_poll, K_NO_WAIT);
    return ZMK_EV_EVENT_BUBBLE;
}

ZMK_LISTENER(worxpad_charger_poll, charger_poll_start);
ZMK_SUBSCRIPTION(worxpad_charger_poll, zmk_usb_conn_state_changed);

/* ------------------------------------------------------------------------------------------------ */
/* Construction                                                                                     */
/* ------------------------------------------------------------------------------------------------ */

static lv_obj_t *panel(lv_obj_t *parent, int32_t x, int32_t y, int32_t w, int32_t h, uint32_t bg) {
    lv_obj_t *obj = lv_obj_create(parent);
    lv_obj_remove_flag(obj, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_pos(obj, x, y);
    lv_obj_set_size(obj, w, h);
    lv_obj_set_style_bg_color(obj, lv_color_hex(bg), LV_PART_MAIN);
    lv_obj_set_style_bg_opa(obj, LV_OPA_COVER, LV_PART_MAIN);
    lv_obj_set_style_radius(obj, CELL_RADIUS, LV_PART_MAIN);
    lv_obj_set_style_border_width(obj, 0, LV_PART_MAIN);
    lv_obj_set_style_pad_all(obj, 0, LV_PART_MAIN);
    return obj;
}

static lv_obj_t *text(lv_obj_t *parent, const lv_font_t *font, uint32_t colour, int32_t width) {
    lv_obj_t *obj = lv_label_create(parent);
    lv_obj_set_style_text_font(obj, font, LV_PART_MAIN);
    lv_obj_set_style_text_color(obj, lv_color_hex(colour), LV_PART_MAIN);
    lv_obj_set_width(obj, width);
    lv_obj_set_style_text_align(obj, LV_TEXT_ALIGN_CENTER, LV_PART_MAIN);
    lv_label_set_long_mode(obj, LV_LABEL_LONG_CLIP);
    lv_label_set_text(obj, "");
    return obj;
}

static void build_knob_row(lv_obj_t *screen) {
    const int32_t half = (SCREEN_PX - CELL_GAP) / 2;
    for (int knob = 0; knob < KNOBS; knob++) {
        lv_obj_t *box = panel(screen, knob * (half + CELL_GAP), 0, half, KNOB_H, COLOUR_PAPER);
        /* Montserrat 14: "Zoom- / Zoom+" on the stock Edit layer is 125 px at 16, wider than the box. */
        ui.knob_turn[knob] = text(box, &lv_font_montserrat_14, COLOUR_ACCENT, half);
        lv_obj_align(ui.knob_turn[knob], LV_ALIGN_TOP_MID, 0, 2);
        ui.knob_push[knob] = text(box, &lv_font_montserrat_12, COLOUR_DIM, half);
        lv_obj_align(ui.knob_push[knob], LV_ALIGN_BOTTOM_MID, 0, -2);
    }
}

static void build_key_grid(lv_obj_t *screen) {
    for (int key = 0; key < GRID_KEYS; key++) {
        const int32_t col = key % GRID_COLS;
        const int32_t row = key / GRID_COLS;
        lv_obj_t *cell = panel(screen, col * (CELL_W + CELL_GAP), GRID_Y + row * (CELL_H + CELL_GAP),
                               CELL_W, CELL_H, COLOUR_CELL);
        ui.keys[key] = text(cell, &lv_font_montserrat_14, COLOUR_INK, CELL_W);
        lv_obj_center(ui.keys[key]);
    }
}

static void build_status_bar(lv_obj_t *screen) {
    const int32_t third = (SCREEN_PX - 2 * SIDE_PAD) / 3;
    lv_obj_t *bar = panel(screen, 0, STATUS_Y, SCREEN_PX, STATUS_H, COLOUR_PAPER);

    ui.layer = text(bar, &lv_font_montserrat_16, COLOUR_ACCENT, third);
    lv_obj_set_style_text_align(ui.layer, LV_TEXT_ALIGN_LEFT, LV_PART_MAIN);
    lv_obj_align(ui.layer, LV_ALIGN_LEFT_MID, SIDE_PAD, 0);

    ui.output = text(bar, &lv_font_montserrat_16, COLOUR_INK, third);
    lv_obj_align(ui.output, LV_ALIGN_CENTER, 0, 0);

    ui.battery = text(bar, &lv_font_montserrat_16, COLOUR_INK, third);
    lv_obj_set_style_text_align(ui.battery, LV_TEXT_ALIGN_RIGHT, LV_PART_MAIN);
    lv_obj_align(ui.battery, LV_ALIGN_RIGHT_MID, -SIDE_PAD, 0);
}

lv_obj_t *zmk_display_status_screen(void) {
    if (init_charger_lines() != 0) {
        LOG_ERR("worxpad: charger status lines not configured");
    }

    /* ZMK gives a custom screen no theme: every object sets its own colours. */
    lv_obj_t *screen = lv_obj_create(NULL);
    lv_obj_remove_flag(screen, LV_OBJ_FLAG_SCROLLABLE);
    lv_obj_set_style_bg_color(screen, lv_color_hex(COLOUR_PAPER), LV_PART_MAIN);
    lv_obj_set_style_bg_opa(screen, LV_OPA_COVER, LV_PART_MAIN);

    build_knob_row(screen);
    build_key_grid(screen);
    build_status_bar(screen);

    worxpad_layer_view_init();
    worxpad_output_view_init();
    worxpad_battery_view_init();
    k_work_schedule(&charger_poll, K_NO_WAIT);
    return screen;
}
