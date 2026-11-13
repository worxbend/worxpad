/*
 * SPDX-License-Identifier: MIT
 *
 * Short display labels for keymap bindings, made from the binding itself so that a keymap changed in
 * ZMK Studio shows its new functions without a rebuild.
 */

#pragma once

#include <stdbool.h>
#include <stddef.h>

#include <zmk/behavior.h>

/* True when the binding is &trans, so the caller looks at the layer below. */
bool worxpad_binding_is_transparent(const struct zmk_behavior_binding *binding);

/* Label for a key binding, such as "Undo", "Nav" or "BT2". */
void worxpad_binding_label(const struct zmk_behavior_binding *binding, char *buf, size_t len);

/* Label for a knob (sensor) binding: counter-clockwise function, then clockwise, as "Undo / Redo". */
void worxpad_sensor_label(const struct zmk_behavior_binding *binding, char *buf, size_t len);
