# SPDX-License-Identifier: MIT
# UF2 for the Adafruit nRF52 bootloader; nrfjprog for SWD on the TC2030 pads.
board_runner_args(nrfjprog "--nrf-family=NRF52" "--softreset")
include(${ZEPHYR_BASE}/boards/common/uf2.board.cmake)
include(${ZEPHYR_BASE}/boards/common/nrfjprog.board.cmake)
