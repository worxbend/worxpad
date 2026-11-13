# SPDX-License-Identifier: MIT
# worxpad ZMK module sources (zephyr/module.yml -> cmake: firmware/zmk)

if(CONFIG_WORXPAD_STATUS_SCREEN)
  target_sources(app PRIVATE src/status_screen.c src/labels.c)
endif()

if(CONFIG_WORXPAD_DISPLAY_POWER)
  target_sources(app PRIVATE src/display_power.c)
endif()
