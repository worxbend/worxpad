"""Routes the placed board with router.py and writes the tracks and vias. Needs pcbnew.

The router works on the two outer layers. In1.Cu is the ground plane and In2.Cu the 3.3 V plane, so a pad
of either net only needs a via. Order (task brief and pcb/README.md net classes):

0. hand-placed ground vias, before any track: five in the charger's exposed pad (power 6.3) and a fence along
   both ends of the antenna keep-out (mcu-radio A3);
1. the USB pair from each J1 pad to the ESD pin on its side, while the board is empty;
2. VBUS and the ESD array's ground via, which sit between the USB pins of U6, then the rest of the pair;
3. the crystal nets, short, next to module pads 13 and 14;
4. the other supply nets at 0.30 mm (BAT_IN, BAT, VSYS, VBUS_SYS);
5. a way out of the module's pad field for every other module signal pad, nets from route_order.txt first;
6. one via to its plane for every ground and 3.3 V surface pad;
7. the remaining signals: route_order.txt first, then shortest first.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import pcbnew

import circuit
import layout
import schematic
from circuit import BAT, BAT_IN, BOARD_SPEC, GND, V3, VBUS, VBUS_SYS, VSYS
from router import BACK, BOTH_LAYERS, FRONT, Pad, Router, Rules

PLANE_NETS = (GND, V3)
USB_NETS = ("USB_DN", "USB_DP")
# J1's pads alternate B7 D-, A6 D+, A7 D-, B6 D+ along the row, so a tree that joins A7 to B7 walls A6 in.
# Each J1 pad gets its own track to the ESD pin on its side first (U6 is flow-through: 1 and 6 are D-, 3 and 4
# D+); the rest of each net then starts from the ESD pins. A6 runs up the middle, under U6's body.
USB_ENTRIES = (("USB_DN", "J1.B7", "U6.6"), ("USB_DN", "J1.A7", "U6.1"), ("USB_DP", "J1.A6", "U6.4"),
               ("USB_DP", "J1.B6", "U6.3"))
CRYSTAL_NETS = ("XL1", "XL2")
POWER_NETS = (VBUS, BAT_IN, BAT, VSYS, VBUS_SYS)
# Every module pad first gets a track out of this square around the module centre.
ESCAPE_DISTANCE = 5.4
LENGTH_LIMIT = {"XL1": 8.0, "XL2": 8.0}   # mm; the crystal sits next to pads 13 and 14 (mcu-radio 7.4)
USB_PAIR_MISMATCH_LIMIT = 2.0   # mm; full-speed USB tolerates far more, this only catches a detour
_KICAD_LAYER = {FRONT: pcbnew.F_Cu, BACK: pcbnew.B_Cu}
# Thermal vias in the BQ24072 exposed pad (1.6 mm square), as offsets from its centre: centre and four corners.
# Power 6.3 asks for at least five; TI SLUS810N 12.3 for "multiple vias" in the pad. At 0.5 mm the corner
# vias' copper ends at the pad edge and the holes keep 0.41 mm between them. Tented on the top face.
THERMAL_PAD = "U3.17"
THERMAL_VIA_OFFSETS = ((0.0, 0.0), (-0.5, -0.5), (0.5, -0.5), (-0.5, 0.5), (0.5, 0.5))
# Ground fence along the two ends of the RF keep-out (mcu-radio A3: "ground stitching vias along the border").
# The rows sit this far outside the keep-out, from its inner edge to the board edge clearance, at most
# STITCH_PITCH apart. The keep-out's long side is the board edge itself.
STITCH_OFFSET = 0.5
STITCH_PITCH = 1.5


@dataclass(frozen=True)
class Setup:
    rules: Rules
    head_start: tuple[str, ...] = ()   # nets that go first, from route_order.txt (build.py order)


@dataclass
class RoutingResult:
    router: Router
    unrouted: list[str] = field(default_factory=list)   # "NET: pad" for every pad left unconnected
    narrowed: list[str] = field(default_factory=list)   # supply pads joined with a signal-width track

    def report_lines(self) -> list[str]:
        router = self.router
        nets = sorted({track.net for track in router.tracks})
        lines = [
            f"tracks {len(router.tracks)}  vias {len(router.vias)}  "
            f"length {sum(t.length for t in router.tracks):.1f} mm  unrouted pads {len(self.unrouted)}",
            f"USB pair, connector to module: D+ {router.net_length('USB_DP'):.2f} mm, "
            f"D- {router.net_length('USB_DN'):.2f} mm",
            "",
            f"{'net':16} {'mm':>7} {'vias':>4}",
        ]
        for net in nets:
            vias = sum(via.net == net for via in router.vias)
            lines.append(f"{net:16} {router.net_length(net):7.2f} {vias:4}")
        lines += ["", "supply pads joined at signal width (0.10 mm):"] + (self.narrowed or ["none"])
        lines += ["", "unrouted:"] + (self.unrouted or ["none"])
        return lines


def _rect(box: pcbnew.BOX2I) -> tuple[float, float, float, float]:
    return tuple(pcbnew.ToMM(v) for v in (box.GetLeft(), box.GetTop(), box.GetRight(), box.GetBottom()))


def _hole_rect(pad: pcbnew.PAD) -> tuple[float, float, float, float]:
    x, y = pcbnew.ToMM(pad.GetPosition().x), pcbnew.ToMM(pad.GetPosition().y)
    radius = max(pcbnew.ToMM(pad.GetDrillSize().x), pcbnew.ToMM(pad.GetDrillSize().y)) / 2
    return x - radius, y - radius, x + radius, y + radius


def _load_obstacles(board: pcbnew.BOARD, router: Router) -> dict[str, list[Pad]]:
    """Feeds every pad, hole and keep-out to the router. Returns the pads by name ("U1.5"); a name can repeat."""
    pads: dict[str, list[Pad]] = {}
    for footprint in sorted(board.GetFootprints(), key=lambda fp: fp.GetReference()):
        for kicad_pad in footprint.Pads():
            if kicad_pad.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH:
                router.add_hole(_hole_rect(kicad_pad))
                continue
            layers = tuple(layer for layer in BOTH_LAYERS if kicad_pad.IsOnLayer(_KICAD_LAYER[layer]))
            name = f"{footprint.GetReference()}.{kicad_pad.GetNumber()}"
            net = schematic.circuit_net_name(kicad_pad.GetNetname())
            pad = Pad(name, net, _rect(kicad_pad.GetBoundingBox()), layers)
            router.add_pad(pad)
            pads.setdefault(name, []).append(pad)
        for zone in footprint.Zones():
            if zone.GetIsRuleArea() and zone.GetDoNotAllowTracks():
                _keep_copper_out(router, _rect(zone.GetBoundingBox()), BOTH_LAYERS)
    for x, y, radius, layer in layout.fiducial_keepouts(circuit.all_parts()):
        face = FRONT if layer == pcbnew.F_Cu else BACK
        _keep_copper_out(router, (x - radius, y - radius, x + radius, y + radius), (face,))
    return pads


def _keep_copper_out(router: Router, rect: tuple[float, float, float, float], layers: tuple[int, ...]) -> None:
    """No copper edge inside the rectangle: track centres stay half a track out, via centres a via radius out."""
    rules = router.rules
    for grow, track_layers in ((rules.via_diameter / 2 + rules.grid_allowance, ()),
                               (rules.track_width / 2 + rules.grid_allowance, layers)):
        left, top, right, bottom = rect
        router.add_keepout((left - grow, top - grow, right + grow, bottom + grow), track_layers)


def new_router() -> Router:
    """A router over the real outline: tongues, notch and R corners."""
    pcb = BOARD_SPEC["pcb"]
    router = Router(pcb["x1"] + 1.0, pcb["y1"] + 1.0, 0.0, layout.ROUTING_RULES)
    router.close_outside(layout.outline_points())
    notch = pcb["notches"][0]
    middle = ((notch["x0"] + notch["x1"]) / 2, (notch["y0"] + notch["y1"]) / 2)
    assert not router.is_open(FRONT, *middle), "the router lets copper into the USB notch"
    assert router.is_open(FRONT, 60.0, 40.0), "the router closed the middle of the board"
    return router


class _Plan:
    """The routing order. One method per stage; each appends what it could not connect."""

    def __init__(self, router: Router, pads: dict[str, list[Pad]], setup: Setup) -> None:
        self.router = router
        self.pads = pads
        self.head_start = setup.head_start
        self.unrouted: list[str] = []
        self.narrowed: list[str] = []
        self.fanned: set[str] = set()
        self.routed_nets: set[str] = set(PLANE_NETS)
        self.by_net: dict[str, list[Pad]] = {}
        for name in sorted(pads):
            for pad in pads[name]:
                if pad.net:
                    self.by_net.setdefault(pad.net, []).append(pad)

    def net(self, net: str, wide: bool = False) -> None:
        failed = self.router.route_net(net, self.by_net[net], wide)
        if wide and failed:   # a 0.30 mm track does not fit between module or VQFN pads
            self.narrowed += [f"{net}: {name}" for name in failed]
            failed = self.router.route_net(net, [pad for pad in self.by_net[net] if pad.name in failed])
            self.narrowed = [line for line in self.narrowed if line.split(": ")[1] not in failed]
        self.unrouted += [f"{net}: {name}" for name in failed]
        self.routed_nets.add(net)

    def ground_vias(self) -> None:
        """The hand-placed ground vias, on the empty board so that every track goes round them."""
        x, y = self.pads[THERMAL_PAD][0].centre
        for dx, dy in THERMAL_VIA_OFFSETS:
            self.router.add_via_in_pad(GND, x + dx, y + dy)
        for x, y in rf_stitch_points(self.router.rules):
            self.router.add_via(GND, x, y)

    def usb_entries(self) -> None:
        for net, connector_pad, esd_pad in USB_ENTRIES:
            if not self.router.route_pair(net, self.pads[connector_pad][0], self.pads[esd_pad][0]):
                self.unrouted.append(f"{net}: {connector_pad} to {esd_pad}")

    def usb_pair(self) -> None:
        """The pair from the ESD pins on: across U6 and on to module pads 67 and 68."""
        for net in USB_NETS:
            rest = [pad for pad in self.by_net[net] if not pad.name.startswith("J1.")]
            self.unrouted += [f"{net}: {name}" for name in self.router.route_net(net, rest)]
            self.routed_nets.add(net)

    def plane_fan_out(self, only: tuple[str, ...] = ()) -> None:
        """Every surface pad of a plane net (or only the named ones) gets a via, or a track to copper that has
        one. A pad that already has one is skipped by the router."""
        for net in PLANE_NETS:
            for pad in self.by_net[net]:
                if len(pad.layers) != 1 or (only and pad.name not in only) or pad.name in self.fanned:
                    continue   # through-hole pads touch the planes directly
                self.fanned.add(pad.name)
                if not (self.router.fan_out(net, pad, _anywhere, wide=True)
                        or self.router.fan_out(net, pad, _anywhere)):
                    self.unrouted.append(f"{net}: {pad.name} (no via to its plane)")

    def module_escapes(self) -> None:
        """Each remaining module signal gets a way out of the pad field, before the plane vias take the room
        round the module. The nets are finished later (signals)."""
        centre = circuit.module_centre()

        def turn(pad: Pad) -> tuple:
            first = self.head_start
            head_start = first.index(pad.net) if pad.net in first else len(first)
            depth = -max(abs(pad.centre[0] - centre[0]) / 7.5, abs(pad.centre[1] - centre[1]) / 5.1)
            return head_start, depth, pad.name

        module_pads = [pad for net in sorted(self.by_net) for pad in self.by_net[net]
                       if pad.name.startswith("U1.") and net not in self.routed_nets]
        for pad in sorted(module_pads, key=turn):
            if not self.router.has_escaped(pad):
                self.escape(pad, centre)

    def escape(self, pad: Pad, centre: tuple[float, float]) -> bool:
        escaped = self.router.escape(pad.net, pad, centre, ESCAPE_DISTANCE)
        if not escaped:
            self.unrouted.append(f"{pad.net}: {pad.name} (no way out of the module)")
        return escaped

    def signals(self) -> None:
        remaining = [net for net in self.by_net if net not in self.routed_nets]
        first = self.head_start
        for net in sorted(remaining, key=lambda name: (first.index(name) if name in first else len(first),
                                                        _spread(self.by_net[name]), name)):
            self.net(net)


def rf_keepout() -> tuple[float, float, float, float]:
    """The antenna keep-out from board.toml (left, top, right, bottom); layout.check_placement asserts that the
    module's rule area is this rectangle."""
    module = BOARD_SPEC["module"]
    right = BOARD_SPEC["pcb"]["x1"]
    half = module["keepout"]["length"] / 2
    return right - module["keepout"]["depth"], module["centre_y"] - half, right, module["centre_y"] + half


def rf_stitch_points(rules: Rules) -> list[tuple[float, float]]:
    """Grid points of the ground fence: one row STITCH_OFFSET above and one below the keep-out, evenly spaced
    from its inner edge to the last spot the board edge clearance leaves a via."""
    left, top, right, bottom = rf_keepout()
    last = right - rules.edge_clearance - rules.via_diameter / 2 - rules.grid_allowance
    gaps = math.ceil((last - left) / STITCH_PITCH)
    xs = [left + (last - left) * k / gaps for k in range(gaps + 1)]
    rows = (top - STITCH_OFFSET, bottom + STITCH_OFFSET)
    return [(_on_grid(x, rules), _on_grid(y, rules)) for y in rows for x in xs]


def _on_grid(value: float, rules: Rules) -> float:
    """Rounds down to the router grid. In X that moves away from the board edge; a row moves at most one pitch,
    and STITCH_OFFSET leaves the via copper outside the keep-out after that."""
    return round(math.floor(value / rules.pitch + 1e-6) * rules.pitch, 4)


def _anywhere(x: float, y: float) -> bool:
    """Both planes cover the whole board; the router's keep-outs already close the RF rule area."""
    return True


def _spread(pads: list[Pad]) -> float:
    """Half the perimeter of the box around the pads: a quick guess of the track length."""
    xs = [pad.centre[0] for pad in pads]
    ys = [pad.centre[1] for pad in pads]
    return max(xs) - min(xs) + max(ys) - min(ys)


def route(board: pcbnew.BOARD, setup: Setup) -> RoutingResult:
    """Plans every track and via. Nothing is written to the board; see write_copper."""
    router = new_router()
    plan = _Plan(router, _load_obstacles(board, router), setup)
    plan.ground_vias()
    plan.usb_entries()
    plan.net(VBUS, wide=True)   # U6 pin 5 and its ground pin 2 sit between the USB pins
    plan.plane_fan_out(only=("U6.2",))
    plan.usb_pair()
    for net in CRYSTAL_NETS:
        plan.net(net)
    for net in POWER_NETS[1:]:
        plan.net(net, wide=True)
    plan.module_escapes()
    plan.plane_fan_out()
    plan.signals()
    return RoutingResult(router, plan.unrouted, plan.narrowed)


def write_copper(board: pcbnew.BOARD, router: Router) -> None:
    for track in router.tracks:
        segment = pcbnew.PCB_TRACK(board)
        segment.SetStart(_point(*track.start))
        segment.SetEnd(_point(*track.end))
        segment.SetWidth(pcbnew.FromMM(track.width))
        segment.SetLayer(_KICAD_LAYER[track.layer])
        segment.SetNet(board.FindNet(schematic.board_net_name(track.net)))
        board.Add(segment)
    for via in router.vias:
        barrel = pcbnew.PCB_VIA(board)
        barrel.SetViaType(pcbnew.VIATYPE_THROUGH)
        barrel.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        barrel.SetPosition(_point(via.x, via.y))
        barrel.SetWidth(pcbnew.F_Cu, pcbnew.FromMM(router.rules.via_diameter))
        barrel.SetDrill(pcbnew.FromMM(router.rules.via_drill))
        barrel.SetNet(board.FindNet(schematic.board_net_name(via.net)))
        board.Add(barrel)


def _point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def check_sensitive_lengths(router: Router) -> None:
    for net, limit in LENGTH_LIMIT.items():
        length = router.net_length(net)
        assert 0 < length <= limit, f"{net} is {length:.2f} mm long, limit {limit} mm"
    mismatch = abs(router.net_length("USB_DP") - router.net_length("USB_DN"))
    assert mismatch <= USB_PAIR_MISMATCH_LIMIT, f"USB D+ and D- differ by {mismatch:.2f} mm"
