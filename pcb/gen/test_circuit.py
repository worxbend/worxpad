"""Tests of the circuit data, the project footprints and the pin-map check. Plain Python, no KiCad.

    python3 -m unittest discover -s pcb/gen -p 'test_*.py'
"""

from __future__ import annotations

import copy
import math
import sys
import dataclasses
import importlib.util
import unittest

import circuit
import footprints

sys.path.insert(0, str(circuit.REPO_ROOT / "tools"))   # check_pins imports its firmware half from there
_spec = importlib.util.spec_from_file_location("check_pins", circuit.REPO_ROOT / "tools" / "check_pins.py")
check_pins = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_pins)

PARTS = circuit.all_parts()
BY_REF = {part.ref: part for part in PARTS}


class CircuitTest(unittest.TestCase):
    def test_every_part_has_a_footprint_and_every_fitted_part_a_jlcpcb_number(self) -> None:
        for part in PARTS:
            self.assertIn(part.footprint_key, circuit.FOOTPRINT, part.ref)
            if part.fitted and part.footprint_key not in circuit.NOT_A_PART:
                self.assertRegex(part.lcsc, r"^C\d+$", part.ref)

    def test_only_the_d9_parts_are_on_the_top_face(self) -> None:
        top = {part.footprint_key for part in PARTS if part.side == circuit.TOP}
        self.assertEqual(top - {"HOLE_NPTH4", "HOLE_G", "FIDUCIAL"}, {"FH34SRJ24", "B3FS", "PEC12R4"})

    def test_each_key_is_column_switch_diode_row(self) -> None:
        nets = circuit.nets_to_pads(PARTS)
        keys = circuit.BOARD_SPEC["keys"]
        for row in range(keys["rows"]):
            for column in range(keys["columns"]):
                index = row * keys["columns"] + column + 1
                switch, diode = BY_REF[f"SW{index}"], BY_REF[f"D{index}"]
                self.assertEqual(switch.nets["1"], circuit.column_net(column))
                self.assertEqual(diode.nets["1"], circuit.row_net(row), "cathode (pin 1) to the row")
                self.assertEqual(diode.nets["2"], switch.nets["2"], "anode (pin 2) to the switch")
                self.assertEqual(len(nets[switch.nets["2"]]), 2)
                self.assertEqual((switch.x, switch.y), circuit.key_centre(row, column))

    def test_twenty_matrix_positions(self) -> None:
        diodes = [part for part in PARTS if part.value == "1N4148W"]
        self.assertEqual(len(diodes), 20)
        self.assertEqual(len({part.nets["2"] for part in diodes}), 20)

    def test_encoder_filters_are_footprints_only(self) -> None:
        filters = [BY_REF[f"C{n}"] for n in range(13, 17)]
        self.assertTrue(all(not part.fitted and not part.machine_assembled and part.lcsc == "" for part in filters))
        self.assertEqual(sorted(part.nets["1"] for part in filters), ["ENC_L_A", "ENC_L_B", "ENC_R_A", "ENC_R_B"])

    def test_rail_capacitance_matches_d14(self) -> None:
        self.assertAlmostEqual(circuit.check_rail_capacitance(PARTS), 21.6)

    def test_an_extra_capacitor_on_3v3_is_caught(self) -> None:
        extra = circuit.Part("C99", "10uF", "C0603", nets={"1": circuit.V3, "2": circuit.GND})
        with self.assertRaises(AssertionError):
            circuit.check_rail_capacitance(PARTS + [extra])

    def test_a_single_pad_net_is_caught(self) -> None:
        stray = circuit.Part("R99", "100k", "R0402", nets={"1": "LONELY", "2": circuit.GND})
        with self.assertRaises(AssertionError):
            circuit.check_netlist(PARTS + [stray])

    def test_module_sits_inset_from_the_right_edge(self) -> None:
        module = circuit.BOARD_SPEC["module"]
        x, _ = circuit.module_centre()
        self.assertAlmostEqual(x + module["length"] / 2, circuit.BOARD_SPEC["pcb"]["x1"] - module["antenna_inset"])

    def test_reverse_fet_and_gauge_sit_after_the_fet(self) -> None:
        self.assertEqual(BY_REF["Q2"].nets, {"1": circuit.GND, "2": circuit.BAT, "3": circuit.BAT_IN})
        self.assertEqual(BY_REF["J3"].nets["1"], circuit.BAT_IN)
        self.assertEqual((BY_REF["U5"].nets["2"], BY_REF["U5"].nets["3"]), (circuit.BAT, circuit.BAT))


class FootprintTest(unittest.TestCase):
    def test_bmd340_has_68_pads_on_its_grid(self) -> None:
        positions = footprints.bmd340_pad_positions()
        self.assertEqual(len(positions), 68)
        self.assertEqual(positions["1"], (-2.85, 4.4))       # figure 2: pad 1 bottom left
        self.assertEqual(positions["45"], (-2.85, -4.4))     # top left, next to the antenna
        self.assertEqual(positions["30"], (5.95, -4.4))
        self.assertEqual(positions["68"], (6.85, -3.85))
        self.assertEqual(positions["54"], (4.15, 0.0))
        self.assertEqual(len(set(positions.values())), 68)

    def test_bmd340_pads_keep_their_spacing(self) -> None:
        """Copper to copper: 0.40 mm along the rows; 0.35 mm corner to corner between pads 32 and 28, the
        closest diagonal pair in figure 12."""
        points = list(footprints.bmd340_pad_positions().values())
        size, closest = footprints.BMD340_PAD, []
        for i, (x0, y0) in enumerate(points):
            for x1, y1 in points[i + 1:]:
                closest.append(math.hypot(max(abs(x0 - x1) - size, 0), max(abs(y0 - y1) - size, 0)))
        self.assertAlmostEqual(min(closest), math.hypot(0.25, 0.25), places=6)

    def test_rf_keepout_runs_from_the_edge_to_the_first_pad_column(self) -> None:
        module = circuit.BOARD_SPEC["module"]
        fp = footprints.bmd340()
        self.assertEqual(len(fp.zones), 1)
        first_column_edge = min(x for x, _ in footprints.bmd340_pad_positions().values()) - footprints.BMD340_PAD / 2
        self.assertAlmostEqual(first_column_edge, -module["length"] / 2 + module["antenna_strip"])
        self.assertIn(f"(xy {-module['length'] / 2 - module['antenna_inset']:g} ", fp.zones[0])

    def test_a_keepout_depth_that_is_not_strip_plus_inset_is_refused(self) -> None:
        original = circuit.BOARD_SPEC["module"]["keepout"]["depth"]
        try:
            circuit.BOARD_SPEC["module"]["keepout"]["depth"] = original + 0.1
            with self.assertRaises(AssertionError):
                footprints.bmd340()
        finally:
            circuit.BOARD_SPEC["module"]["keepout"]["depth"] = original

    def test_usb_pads_match_the_symbol_pin_names(self) -> None:
        pads = {pad.number for pad in footprints.usb_c_m13c().pads}
        self.assertEqual(pads - {"SH"}, set(footprints.USB_SIGNAL_PADS))
        self.assertTrue(set(BY_REF["J1"].nets) <= pads)

    def test_choc_socket_is_drawn_mirrored_from_board_toml(self) -> None:
        spec = circuit.BOARD_SPEC["keys"]["footprint"]
        pads = {pad.number: (pad.x, pad.y) for pad in footprints.choc_hotswap().pads if pad.number}
        (x2, y2), (x1, y1) = spec["socket_pads"]
        self.assertEqual(pads, {"1": (-x1, y1), "2": (-x2, y2)})

    def test_fpc_contact_1_at_plus_x_and_24_contacts(self) -> None:
        pads = [pad for pad in footprints.fh34srj_24().pads if pad.number != "MP"]
        self.assertEqual(len(pads), 24)
        self.assertEqual(max(pads, key=lambda pad: pad.x).number, "1")

    def test_every_project_footprint_name_matches_circuit(self) -> None:
        self.assertEqual(set(footprints.footprints()), {k for k, v in circuit.FOOTPRINT.items()
                                                        if v.startswith(circuit.LIBRARY + ":")})

    def test_every_circuit_pad_exists_in_its_project_footprint(self) -> None:
        made = footprints.footprints()
        for part in PARTS:
            if part.footprint_key in made:
                numbers = {pad.number for pad in made[part.footprint_key].pads}
                self.assertTrue(set(part.nets) <= numbers, f"{part.ref}: {set(part.nets) - numbers}")


class CheckPinsTest(unittest.TestCase):
    def _errors(self, board: dict, parts: dict | None = None) -> list[str]:
        errors: list[str] = []
        parts = parts or BY_REF
        for check in (check_pins.check_module, check_pins.check_matrix, check_pins.check_encoders,
                      check_pins.check_display):
            check(board, parts, errors)
        return errors

    def test_the_board_passes(self) -> None:
        self.assertEqual(self._errors(circuit.BOARD_SPEC), [])

    def test_a_moved_net_is_caught(self) -> None:
        board = copy.deepcopy(circuit.BOARD_SPEC)
        board["pinmap"]["P0.05"] = board["pinmap"].pop("P0.07")      # I2C_SDA to another pad
        board["pinmap_spare"]["pins"] = [p if p != "P0.05" else "P0.07" for p in board["pinmap_spare"]["pins"]]
        self.assertTrue(any("P0.05" in error for error in self._errors(board)))

    def test_a_fast_signal_on_a_slow_pin_is_caught(self) -> None:
        board = copy.deepcopy(circuit.BOARD_SPEC)
        board["module"]["low_frequency"]["pins"].append("P0.19")
        self.assertTrue(any("low-frequency" in error for error in self._errors(board)))

    def test_a_gpio_listed_twice_is_caught(self) -> None:
        board = copy.deepcopy(circuit.BOARD_SPEC)
        board["pinmap_spare"]["pins"].append("P0.02")
        self.assertTrue(any("exactly once" in error for error in self._errors(board)))

    def test_swapped_encoder_pins_are_caught(self) -> None:
        board = copy.deepcopy(circuit.BOARD_SPEC)
        left = board["encoders"]["left"]
        left["gpio_a"], left["gpio_b"] = left["gpio_b"], left["gpio_a"]
        self.assertTrue(any("encoders.left" in error for error in self._errors(board)))

    def test_a_wrong_fpc_pin_is_caught(self) -> None:
        parts = dict(BY_REF)
        nets = dict(parts["J2"].nets) | {"8": "LCD_DC", "10": "LCD_CS"}
        parts["J2"] = dataclasses.replace(parts["J2"], nets=nets)
        self.assertTrue(any("fpc_pins 8" in error for error in self._errors(circuit.BOARD_SPEC, parts)))

    def test_a_wrong_c4_assignment_is_caught(self) -> None:
        board = copy.deepcopy(circuit.BOARD_SPEC)
        board["buttons"]["left"]["matrix"] = "C4R2"
        self.assertTrue(any("buttons.left" in error for error in self._errors(board)))


if __name__ == "__main__":
    unittest.main()
