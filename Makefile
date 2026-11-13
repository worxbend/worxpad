# Top-level tasks. `make help` lists them.
#
# spec-check, docs-check, pin-check and firmware have their scripts. Every other target calls a script that the
# builders still have to write; the target fails with "No such file" until it exists. The script paths below are the contract:
#   pcb/gen/build.py        PCB generator (place, route, schematic, fab, unit tests)
#   cad/build.py            case model (check, export, render, draw)
#   firmware/build.sh       ZMK build in the pinned image
#   tools/render_all.sh     every picture in docs/images/
#   tools/order_package.py  JLCPCB, PCBWay, JLCCNC and JLC3DP order packages
# When a builder adds a host-only check (pcb-test, cad-check, firmware host tests), add it to `test`.

NAME := worxpad
BOARD := pcb/kicad/$(NAME).kicad_pcb
BUILD := pcb/.build

# Images are pinned by digest in tools/images.lock; `bash tools/pull_images.sh <tag>` pulls and tags them.
KICAD_IMAGE := kicad/kicad:10.0.7
KICAD_FULL_IMAGE := kicad/kicad:10.0.7-full
DOCKER := docker run --rm --network none -u $$(id -u):$$(id -g) -e HOME=/tmp -e PYTHONHASHSEED=0 \
	-v $(CURDIR):/w -w /w
KICAD := $(DOCKER) $(KICAD_IMAGE) bash -c
KICAD_FULL := $(DOCKER) $(KICAD_FULL_IMAGE) bash -c
CAD_PYTHON := .venv/bin/python

.PHONY: help test spec-check docs-check pin-check pcb pcb-place pcb-check pcb-fab pcb-test cad cad-check firmware \
	renders order

help:
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/'

test: spec-check docs-check pin-check ## Everything that can be checked without Docker or hardware

spec-check: ## Arithmetic self-check of board.toml (holes, outline, overlaps, battery pocket, pins)
	python3 tools/check_spec.py

pin-check: ## Circuit and firmware pin maps against board.toml (tools/check_pins.py)
	python3 tools/check_pins.py

docs-check: ## Every file, picture and anchor named in a Markdown file exists
	python3 tools/check_docs.py

pcb: pcb-place pcb-check pcb-fab ## Regenerate the board, check it, write the order files (needs Docker)

pcb-place: ## board.toml -> schematic, placed and routed board (needs Docker; pcb/gen/build.py)
	$(KICAD) "bash tools/kicad_env.sh && python3 pcb/gen/build.py place"

pcb-check: ## DRC with schematic parity; fails on any violation or unconnected item (needs Docker)
	mkdir -p $(BUILD)
	$(KICAD) "bash tools/kicad_env.sh && kicad-cli pcb drc --severity-error --schematic-parity \
		--exit-code-violations --format json -o $(BUILD)/drc.json $(BOARD)"

pcb-fab: ## Gerbers, drill files, BOM and placement list -> pcb/fab/ (needs Docker; pcb/gen/build.py)
	$(KICAD) "bash tools/kicad_env.sh && python3 pcb/gen/build.py fab"

pcb-test: ## Netlist self-check and generator unit tests, no Docker (pcb/gen/build.py)
	python3 pcb/gen/build.py test

cad: ## Case: checks, STEP/STL/3MF exports, drawings (needs cad/.venv; cad/build.py)
	cd cad && $(CAD_PYTHON) build.py all

cad-check: ## Case checks only (needs cad/.venv; cad/build.py)
	cd cad && $(CAD_PYTHON) build.py check

firmware: ## ZMK build in the pinned zmk-build-arm image -> firmware/dist/ (firmware/build.sh)
	bash firmware/build.sh

renders: ## Case, PCB and UI pictures -> docs/images/ (tools/render_all.sh)
	KICAD_FULL='$(KICAD_FULL)' bash tools/render_all.sh

order: ## Order packages for JLCPCB, PCBWay, JLCCNC, JLC3DP (tools/order_package.py)
	python3 tools/order_package.py
