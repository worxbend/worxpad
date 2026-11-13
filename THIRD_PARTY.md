# Third-party material

worxpad is licensed under the GPL-3.0-or-later (code: [`LICENSE`](LICENSE)) and the CERN-OHL-S-2.0
(hardware: [`LICENSE-HARDWARE`](LICENSE-HARDWARE)). The material below comes from elsewhere. Nothing is copied
wholesale unless the table says so.

| Source | Licence | Used for | Where |
| --- | --- | --- | --- |
| worxboard (same owner), its tools/images.lock, tools/pull_images.sh and tools/kicad_env.sh | GPL-3.0-or-later | Pinned container images and KiCad library setup, adapted (library name, comments) | `tools/` |
| macropad (same owner), its .github/scripts/check_docs.py | none stated; same owner | Markdown path check, adapted (repository root, research notes) | `tools/check_docs.py` |
| Licence texts of worxboard (GPL-3.0, CERN-OHL-S-2.0) | verbatim licence texts | Copied unchanged | `LICENSE`, `LICENSE-HARDWARE` |
| Prota Designs GLYF | none; reference only | Facts and measurements from public pages, videos and firmware releases. No artwork, firmware, software, model or file is copied | `research/`, `docs/reference-device.md` |
| Part data sheets (u-blox, TI, Analog Devices, Winbond, Bourns, Omron, Hirose, HRO, JST, Kailh, DisplayModule and others) | as published by each maker | Numbers only (dimensions, ratings, pin tables), each cited in `research/components/` | `board.toml`, `docs/decisions.md` |

Planned and not yet used: ZMK (MIT), Zephyr (Apache-2.0), KiCad libraries (CC-BY-SA-4.0 with the KiCad library
exception), build123d (Apache-2.0). Add a row when the first file uses one.

Trademarks (GLYF, Prota Designs, Kailh, Choc, u-blox and others) belong to their owners. worxpad is not affiliated
with any of them.
