/*
 * SPDX-License-Identifier: MIT
 *
 * Backlight dimming and panel sleep (mcu-radio record 7.7, hooks 1 and 2; power record 15).
 *
 * ZMK's blank-on-idle (CONFIG_ZMK_DISPLAY_BLANK_ON_IDLE, selected by WORXPAD_DISPLAY_POWER) stops the LVGL
 * tick and sends DISPOFF on idle, and sends DISPON and restarts the tick on activity. DISPOFF alone leaves the
 * ST7789V in normal mode drawing milliamperes, so this hook adds the rest: on idle the backlight goes off and
 * the panel goes to sleep-in (SLPIN) through its PM action; on activity the panel leaves sleep-in (SLPOUT),
 * gets DISPON again and the backlight returns to CONFIG_WORXPAD_BACKLIGHT_PERCENT.
 *
 * ZMK's work and this work both run on the display work queue, in an order that is not fixed. Sending DISPON
 * after SLPOUT here makes the panel end lit and awake in either order. The panel keeps its frame memory in
 * sleep-in (ST7789V data sheet 9.1.11). Not measured on a board.
 */

#include <errno.h>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/display.h>
#include <zephyr/drivers/led.h>
#include <zephyr/init.h>
#include <zephyr/logging/log.h>
#include <zephyr/pm/device.h>

#include <zmk/activity.h>
#include <zmk/display.h>
#include <zmk/event_manager.h>
#include <zmk/events/activity_state_changed.h>

LOG_MODULE_DECLARE(zmk, CONFIG_ZMK_LOG_LEVEL);

#define BACKLIGHT_NODE DT_NODELABEL(backlight)

static const struct device *const panel = DEVICE_DT_GET(DT_CHOSEN(zephyr_display));
static const struct device *const backlight = DEVICE_DT_GET(DT_PARENT(BACKLIGHT_NODE));
static const uint32_t backlight_index = DT_NODE_CHILD_IDX(BACKLIGHT_NODE);

/* -EALREADY means the panel is already in the asked state, which is not a fault. */
static void run_panel_action(enum pm_device_action action) {
    const int err = pm_device_action_run(panel, action);
    if (err != 0 && err != -EALREADY) {
        LOG_ERR("worxpad: panel PM action %d failed: %d", action, err);
    }
}

static void backlight_on(void) {
    const int err = led_set_brightness(backlight, backlight_index, CONFIG_WORXPAD_BACKLIGHT_PERCENT);
    if (err != 0) {
        LOG_ERR("worxpad: backlight brightness failed: %d", err);
    }
}

static void panel_sleep_cb(struct k_work *work) {
    ARG_UNUSED(work);
    const int err = led_off(backlight, backlight_index);
    if (err != 0) {
        LOG_ERR("worxpad: backlight off failed: %d", err);
    }
    run_panel_action(PM_DEVICE_ACTION_SUSPEND);
}

static void panel_wake_cb(struct k_work *work) {
    ARG_UNUSED(work);
    run_panel_action(PM_DEVICE_ACTION_RESUME);
    const int err = display_blanking_off(panel);
    if (err != 0) {
        LOG_ERR("worxpad: panel DISPON failed: %d", err);
    }
    backlight_on();
}

K_WORK_DEFINE(panel_sleep_work, panel_sleep_cb);
K_WORK_DEFINE(panel_wake_work, panel_wake_cb);

static int activity_listener(const zmk_event_t *eh) {
    const struct zmk_activity_state_changed *ev = as_zmk_activity_state_changed(eh);
    if (ev == NULL || !zmk_display_is_initialized()) {
        return ZMK_EV_EVENT_BUBBLE;
    }
    switch (ev->state) {
    case ZMK_ACTIVITY_ACTIVE:
        k_work_submit_to_queue(zmk_display_work_q(), &panel_wake_work);
        break;
    case ZMK_ACTIVITY_IDLE:
        k_work_submit_to_queue(zmk_display_work_q(), &panel_sleep_work);
        break;
    default:
        /* Deep sleep: ZMK suspends every device itself before System OFF. */
        break;
    }
    return ZMK_EV_EVENT_BUBBLE;
}

ZMK_LISTENER(worxpad_display_power, activity_listener);
ZMK_SUBSCRIPTION(worxpad_display_power, zmk_activity_state_changed);

static int backlight_init(void) {
    if (!device_is_ready(backlight)) {
        LOG_ERR("worxpad: backlight PWM not ready");
        return -ENODEV;
    }
    backlight_on();
    return 0;
}

SYS_INIT(backlight_init, APPLICATION, CONFIG_APPLICATION_INIT_PRIORITY);
