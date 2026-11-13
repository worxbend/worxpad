# SPDX-License-Identifier: MIT
# Suppresses the duplicate unit-address warning for power, clock, acl and flash-controller, as ZMK's
# nRF52840 boards do.
list(APPEND EXTRA_DTC_FLAGS "-Wno-unique_unit_address_if_enabled")
