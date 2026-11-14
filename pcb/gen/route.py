"""Routes the placed board with router.py and writes the tracks and vias. Needs pcbnew.

The router works on the two outer layers. In1.Cu is the ground plane and In2.Cu the 3.3 V plane, so a pad
of either net only needs a via. Where the outer layers are full, a signal may take a short hop on In2.Cu at three
times the cost of an outer track, or on In1.Cu at four times (layout.ROUTING_RULES); the plane fill flows round
it. Both planes stay whole under the USB pair and the crystal (USB_REFERENCE_MARGIN), and the module's rule area
keeps every layer out of the antenna keep-out. Order (task brief, pcb/README.md net classes and its Routing section):

0. hand-placed ground vias, before any track: five in the charger's exposed pad (power 6.3) and a fence along
   both ends of the antenna keep-out (mcu-radio A3);
1. a track to a via for every signal pin of the parts in ESCAPE_PARTS (charger, LDO, gauge, display
   connector, flash, backlight FET), whose pins the supply tracks and the USB pair would otherwise seal in;
2. the crystal nets, short, next to module pads 13 and 14;
3. a way out for every other module signal pad, innermost first: a track out of the pad field from its outer
   ring, a via in the empty middle under the module from deeper in (module_escapes), in up to
   MODULE_ESCAPE_ROUNDS rounds;
4. one via to its plane for every ground and 3.3 V surface pad;
5. the USB pair from each J1 pad to the ESD pin on its side, VBUS, then the rest of the pair, mostly on F.Cu;
   the shorter of D+ and D- gets a meander when they differ by more than USB_PAIR_MISMATCH_LIMIT;
6. the other supply nets at 0.30 mm (BAT_IN, BAT, VSYS, VBUS_SYS);
7. the remaining signals: route_order.txt first, then shortest first;
8. rip-up and reroute: every pad still unconnected names the branches in its way (router.reach); they are
   taken off, the pad is joined, and their pads are joined again, for at most REPAIR_ROUNDS rounds. The
   copper of the nets in FIXED_NETS and every escape stays where it is; a try that leaves more pads unjoined
   is undone, and only the raised history costs stay;
9. a plane via that the inner-layer tracks cut off from its plane is moved into the plane (plane_islands);
10. the escapes' unused ends are cut off (router.prune_dangling), and every track is cut where another ends on its
    middle (router.split_at_junctions).

The escapes of stages 1 and 3 and the plane vias go in before the long nets on purpose: the long nets then go
round them, instead of the escapes finding their way out closed.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field

import pcbnew

import circuit
import layout
import schematic
from circuit import BAT, BAT_IN, BOARD_SPEC, GND, V3, VBUS, VBUS_SYS, VSYS
from router import BACK, FRONT, GROUND_INNER, INNER, Pad, Rect, Router, Rules

PLANE_NETS = (GND, V3)
# The inner layer of a plane net, checked for islands after routing (_Plan.plane_islands). Only 3.3 V: ground also
# has the pours on both outer layers, which join a ground via whatever happens on In1.Cu.
PLANE_LAYERS = {V3: INNER}
PLANE_ISLAND_ROUNDS = 3
# Signals with a track on the plane's layer this close (mm) to a cut-off plane via give way (_Plan.plane_islands).
PLANE_ISLAND_REACH = 2.0
# A step on a layer a net must keep off costs this many outer steps: the supply nets on both inner layers, the
# signals moved off a plane layer by plane_islands. check_sensitive_lengths fails on a supply track there.
OFF_LAYER_FACTOR = 1000
USB_NETS = ("USB_DN", "USB_DP")
# J1's pads alternate B7 D-, A6 D+, A7 D-, B6 D+ along the row, so a tree that joins A7 to B7 walls A6 in.
# Each J1 pad gets its own track to the ESD pin on its side first (U6 is flow-through: 1 and 6 are D-, 3 and 4
# D+); the rest of each net then starts from the ESD pins. A6 runs up the middle, under U6's body.
USB_ENTRIES = (("USB_DN", "J1.B7", "U6.6"), ("USB_DN", "J1.A7", "U6.1"), ("USB_DP", "J1.A6", "U6.4"),
               ("USB_DP", "J1.B6", "U6.3"))
CRYSTAL_NETS = ("XL1", "XL2")
POWER_NETS = (VBUS, BAT_IN, BAT, VSYS, VBUS_SYS)
# Copper that is never ripped up: the USB pair, the crystal and the supply nets go in first on purpose, and a
# supply net routed again late would lose its 0.30 mm width. A plane pad's fan-out may be ripped up: the pad then
# gets a new one (_push_through). The hand-placed ground vias are fixed in the router.
FIXED_NETS = (*USB_NETS, *CRYSTAL_NETS, *POWER_NETS)
# Rip-up rounds after the first pass; each round tries every pad that is still unconnected once.
REPAIR_ROUNDS = 12
# Ways one pad may try in a round: after each, the branches it crossed are ripped up and it searches again. A
# way that crosses more than REPAIR_MAX_CROSSINGS branches is not taken; ripped pads push through in turn, to
# REPAIR_DEPTH levels.
REPAIR_TRIES = 3
REPAIR_MAX_CROSSINGS = 2
REPAIR_DEPTH = 2
# Every module signal pad first gets a track out of the module's pad field, grown by this much (mm).
MODULE_ESCAPE_MARGIN = 1.0
# Rounds of module escapes: each new round starts again with the pads the round before left without a way.
MODULE_ESCAPE_ROUNDS = 6
# A module escape longer than this (mm) is not laid: it would run round its neighbours and wall them in.
MODULE_ESCAPE_LONGEST = 3.0
# Parts whose signal pins the later fixed copper would seal in: the charger, the LDO and the gauge, whose signal
# pins sit between supply pins, and the display connector, whose end pins sit beside the USB pair. Each signal pin
# gets a track to a via at least PIN_ESCAPE_LENGTH (mm) beyond the part's pads before any other net is routed.
ESCAPE_PARTS = ("U3", "U4", "U5", "J2", "U2", "Q1")
PIN_ESCAPE_LENGTH = 0.8
LENGTH_LIMIT = {"XL1": 8.0, "XL2": 8.0}   # mm; the crystal sits next to pads 13 and 14 (mcu-radio 7.4)
USB_PAIR_MISMATCH_LIMIT = 2.0   # mm; full-speed USB tolerates far more, this only catches a detour
_KICAD_LAYER = {FRONT: pcbnew.F_Cu, BACK: pcbnew.B_Cu, INNER: pcbnew.In2_Cu, GROUND_INNER: pcbnew.In1_Cu}
# No inner track this close to the USB pair's copper (mm, from its edge to the inner track's centre): three times
# the 0.21 mm prepreg to In2.Cu for the reference under a bottom track, plus the 0.2 mm zone clearance of the fill.
USB_REFERENCE_MARGIN = 0.9
# The pair from U6 to the module runs on F.Cu where it can: B.Cu carries the charger, gauge, flash and module pads,
# and a pair laid there first walls their pins in. A bottom step costs this many top steps.
USB_BACK_STEP_FACTOR = 3
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
    pad_count: dict[str, int] = {}
    for footprint in board.GetFootprints():
        for kicad_pad in footprint.Pads():
            pad_count[kicad_pad.GetNetname()] = pad_count.get(kicad_pad.GetNetname(), 0) + 1
    for footprint in sorted(board.GetFootprints(), key=lambda fp: fp.GetReference()):
        for kicad_pad in footprint.Pads():
            if kicad_pad.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH:
                router.add_hole(_hole_rect(kicad_pad))
                continue
            layers = tuple(layer for layer in router.rules.layers if kicad_pad.IsOnLayer(_KICAD_LAYER[layer]))
            name = f"{footprint.GetReference()}.{kicad_pad.GetNumber()}"
            net = _router_net(kicad_pad.GetNetname(), pad_count[kicad_pad.GetNetname()])
            pad = Pad(name, net, _rect(kicad_pad.GetBoundingBox()), layers)
            router.add_pad(pad)
            pads.setdefault(name, []).append(pad)
        for zone in footprint.Zones():
            if zone.GetIsRuleArea() and zone.GetDoNotAllowTracks():
                _keep_copper_out(router, _rect(zone.GetBoundingBox()), router.rules.layers)
    for x, y, radius, layer in layout.fiducial_keepouts(circuit.all_parts()):
        face = FRONT if layer == pcbnew.F_Cu else BACK
        _keep_copper_out(router, (x - radius, y - radius, x + radius, y + radius), (face,))
    return pads


def _router_net(board_net: str, pads: int) -> str:
    """The circuit net of a pad, and for an open pin that several pads share (the two solder tabs of J2 and of J3,
    both pad "MP") KiCad's own net name: KiCad counts such pads as one net, and DRC wants them joined."""
    if board_net.startswith(schematic.OPEN_PIN_NET_PREFIX) and pads > 1:
        return board_net
    return schematic.circuit_net_name(board_net)


def _board_net(net: str) -> str:
    """The board's name of a router net (see _router_net)."""
    return net if net.startswith(schematic.OPEN_PIN_NET_PREFIX) else schematic.board_net_name(net)


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
    """The routing order. One method per stage; each records what it could not connect."""

    def __init__(self, router: Router, pads: dict[str, list[Pad]], setup: Setup) -> None:
        self.router = router
        self.pads = pads
        self.head_start = setup.head_start
        self.failures: list[str] = []   # connections outside the net trees: the USB entries
        self.unreached: dict[str, list[str]] = {}   # net -> names of the pads its tree (or plane) does not reach
        self.narrowed: dict[str, list[str]] = {}   # supply net -> pads joined at signal width
        self.routed_nets: set[str] = set(PLANE_NETS)
        self.by_net: dict[str, list[Pad]] = {}
        for name in sorted(pads):
            for pad in pads[name]:
                if pad.net:
                    self.by_net.setdefault(pad.net, []).append(pad)

    @property
    def unrouted(self) -> list[str]:
        return self.failures + [f"{net}: {name}" for net in sorted(self.unreached) for name in self.unreached[net]]

    @property
    def narrowed_lines(self) -> list[str]:
        return [f"{net}: {name}" for net in sorted(self.narrowed) for name in self.narrowed[net]]

    def net(self, net: str, wide: bool = False) -> None:
        """Joins the net's pads, or the ones not joined yet. A supply net tries 0.30 mm first and stays off the
        inner layers, whose 15 um copper is too thin for its current."""
        if net in POWER_NETS:
            self.router.prefer_layers(net, {INNER: OFF_LAYER_FACTOR, GROUND_INNER: OFF_LAYER_FACTOR})
        failed = self.router.route_net(net, self.by_net[net], wide)
        if wide and failed:   # a 0.30 mm track does not fit between module or VQFN pads
            narrow = self.router.route_net(net, [pad for pad in self.by_net[net] if pad.name in failed])
            self.narrowed.setdefault(net, []).extend(name for name in failed if name not in narrow)
            failed = narrow
        self._record(net, failed)
        self.routed_nets.add(net)

    def _record(self, net: str, failed: list[str]) -> None:
        if failed:
            self.unreached[net] = failed
        else:
            self.unreached.pop(net, None)

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
                self.failures.append(f"{net}: {connector_pad} to {esd_pad}")

    def usb_pair(self) -> None:
        """The pair from the ESD pins on: across U6 and on to module pads 67 and 68."""
        for net in USB_NETS:
            self.router.prefer_layers(net, {BACK: USB_BACK_STEP_FACTOR})
            rest = [pad for pad in self.by_net[net] if not pad.name.startswith("J1.")]
            self._record(net, self.router.route_net(net, rest))
            self.routed_nets.add(net)
        self.match_usb_lengths()
        for net in USB_NETS:   # both planes stay whole under the pair: each is the reference of one outer layer
            for plane_layer in (INNER, GROUND_INNER):
                self.router.keep_layer_clear_near(net, plane_layer, USB_REFERENCE_MARGIN)

    def match_usb_lengths(self) -> None:
        """J1's alternating pads give D+ and D- different entry lengths. When they differ by more than
        USB_PAIR_MISMATCH_LIMIT, the shorter net gets a meander that brings it within half the limit, while the
        board round it is still empty. check_sensitive_lengths checks the result."""
        lengths = {net: self.router.net_length(net) for net in USB_NETS}
        shorter, longer = sorted(USB_NETS, key=lengths.get)
        gap = lengths[longer] - lengths[shorter]
        if gap > USB_PAIR_MISMATCH_LIMIT:
            self.router.lengthen(shorter, gap, USB_PAIR_MISMATCH_LIMIT / 2)

    def plane_fan_out(self) -> None:
        """Every surface pad of a plane net gets a via, or a track to copper that has one."""
        for net in PLANE_NETS:
            surface_pads = [pad for pad in self.by_net[net] if len(pad.layers) == 1]   # through-hole pads touch
            self._record(net, [pad.name for pad in surface_pads if not self._fan_out(net, pad)])   # the planes

    def _fan_out(self, net: str, pad: Pad) -> bool:
        return self.router.fan_out(net, pad, _anywhere, wide=True) or self.router.fan_out(net, pad, _anywhere)

    def module_escapes(self) -> None:
        """Each module signal pad (not of a fixed or plane net) gets a way out before the USB pair, the supply
        tracks and the plane vias take the room round the module. A pad on the field's outer ring gets a track out
        of the field; a pad deeper in gets a via in the empty middle under the module (`_empty_middle`), so that
        the vias do not fence the module in. The nets are finished later (signals)."""
        field = _bounds(self._part_pads("U1"))
        centre = ((field[0] + field[2]) / 2, (field[1] + field[3]) / 2)
        middle = _empty_middle(self._part_pads("U1"), centre)
        box = _grown(field, MODULE_ESCAPE_MARGIN)
        half_width, half_height = (field[2] - field[0]) / 2, (field[3] - field[1]) / 2

        def turn(pad: Pad) -> tuple:
            first = self.head_start
            head_start = first.index(pad.net) if pad.net in first else len(first)
            depth = max(abs(pad.centre[0] - centre[0]) / half_width, abs(pad.centre[1] - centre[1]) / half_height)
            return head_start, depth, pad.name

        module_pads = [pad for net in sorted(self.by_net) for pad in self.by_net[net]
                       if pad.name.startswith("U1.") and net not in (*FIXED_NETS, *PLANE_NETS)]
        order = sorted(module_pads, key=turn)   # innermost first: they have the fewest ways out
        saved = self.router.snapshot()
        best: tuple[tuple[int, int], list[Pad]] | None = None
        for _ in range(MODULE_ESCAPE_ROUNDS):
            walled, outside = self._escape_module_pads(order, field, middle, box)
            score = (len(walled), len(outside))
            if best is None or score < best[0]:
                best = (score, order)
            if not walled and not outside:
                return
            self.router.restore(saved)   # again, with the pads that found no way first
            order = walled + outside + [pad for pad in order if pad not in walled and pad not in outside]
        self._escape_module_pads(best[1], field, middle, box)   # the order that walled in the fewest pads

    def _escape_module_pads(self, order: list[Pad], field: Rect, middle: Rect,
                            box: Rect) -> tuple[list[Pad], list[Pad]]:
        """Escapes the pads in this order. Returns the pads left without any way out, and the deeper pads that
        found no room in the middle and took a track out of the field instead."""
        walled, outside = [], []
        for pad in order:
            if self.router.has_escaped(pad):
                continue
            if _on_outer_ring(pad, field):
                if not self._escape_out_of_field(pad, box):
                    walled.append(pad)
            elif not self.router.escape_to_via_inside(pad.net, pad, middle, MODULE_ESCAPE_LONGEST):
                (outside if self._escape_out_of_field(pad, box) else walled).append(pad)
        return walled, outside   # a walled-in pad is routed from scratch in signals()

    def _escape_out_of_field(self, pad: Pad, box: Rect) -> bool:
        """A track out of the module's pad field that ends on a via, or a plain track where no via fits: a plain
        end is easily closed in by the copper that later runs past it, a via is reached on any layer."""
        return (self.router.escape_to_via(pad.net, pad, box, MODULE_ESCAPE_LONGEST)
                or self.router.escape(pad.net, pad, box, MODULE_ESCAPE_LONGEST))

    def pin_escapes(self) -> None:
        """Each signal pad of the small parts in ESCAPE_PARTS gets a short way out of its part, before the supply
        tracks run round the part and seal its pins in (diagnosis in pcb/README.md, Routing)."""
        for reference in ESCAPE_PARTS:
            part_pads = self._part_pads(reference)
            box = _grown(_bounds(part_pads), PIN_ESCAPE_LENGTH)
            for pad in part_pads:
                if pad.net and pad.net not in (*PLANE_NETS, *POWER_NETS):
                    self.router.escape_to_via(pad.net, pad, box)

    def _part_pads(self, reference: str) -> list[Pad]:
        return [pad for name, pads in sorted(self.pads.items()) if name.startswith(f"{reference}.") for pad in pads]

    def signals(self) -> None:
        remaining = [net for net in self.by_net if net not in self.routed_nets]
        first = self.head_start
        for net in sorted(remaining, key=lambda name: (first.index(name) if name in first else len(first),
                                                        _spread(self.by_net[name]), name)):
            self.net(net)

    def repair(self) -> None:
        """Rip-up and reroute until every pad is joined, or for REPAIR_ROUNDS rounds."""
        for _ in range(REPAIR_ROUNDS):
            if not self.unreached:
                return
            for net in sorted(self.unreached):
                for name in list(self.unreached.get(net, ())):
                    if name in self.unreached.get(net, ()):   # an earlier rip-up may have joined it
                        self._clear_way(net, name)

    def _clear_way(self, net: str, name: str) -> None:
        """Joins one pad: the branches its way crosses are ripped up, and their pads pushed through in turn, to
        REPAIR_DEPTH levels. Kept only when no more pads are left unjoined than before; otherwise the board goes
        back as it was, and only the raised history costs remain, to send the next try elsewhere."""
        before = len(self.unrouted)
        saved = (self.router.snapshot(), {key: list(names) for key, names in self.unreached.items()},
                 {key: list(names) for key, names in self.narrowed.items()})
        touched: dict[str, list[str]] = {}
        self._push_through(net, [self._pad(net, name)], REPAIR_DEPTH, touched)
        if self.router.joined(net, self._pad(net, name)) and net in POWER_NETS:   # reach is signal width
            self.narrowed.setdefault(net, []).append(name)
        for other, names in touched.items():
            self._refresh(other, self.unreached.get(other, []) + names)
        if len(self.unrouted) > before:
            self.router.restore(saved[0])
            self.unreached, self.narrowed = saved[1], saved[2]

    def _push_through(self, net: str, pads: list[Pad], depth: int, touched: dict[str, list[str]]) -> None:
        """Joins the pads through `reach` (a plane pad through a new fan-out); at depth above 0, a way that
        crosses at most REPAIR_MAX_CROSSINGS branches rips them up and pushes their pads through one level down.
        Records every pad it handled."""
        touched.setdefault(net, []).extend(pad.name for pad in pads)
        if net in PLANE_NETS:   # a ripped fan-out: the pad gets a new one
            for pad in pads:
                if not self.router.joined(net, pad):
                    self._fan_out(net, pad)
            return
        for pad in pads:
            for _ in range(REPAIR_TRIES):
                if self.router.joined(net, pad):
                    break
                crossed = self.router.reach(net, pad)
                if not crossed or depth == 0 or len(crossed) > REPAIR_MAX_CROSSINGS:
                    break
                for other, lost in self.router.rip_up_crossings(crossed).items():
                    self._push_through(other, lost, depth - 1, touched)

    def plane_islands(self) -> None:
        """Tracks on the inner layers and rows of vias can cut a piece out of a plane; a plane via in that piece
        would join an island of the fill, not the plane. Each such via's fan-out is taken off and the pad fanned out
        again to a spot in the plane's main area (router.plane_area). Where no such spot is in reach, the signals
        with tracks on the plane's layer near the via are ripped up, kept off that layer and routed again. Up to
        PLANE_ISLAND_ROUNDS rounds; a pad that still has no spot keeps a via in the island, and DRC reports it."""
        for net, layer in PLANE_LAYERS.items():
            for _ in range(PLANE_ISLAND_ROUNDS):
                in_plane = self.router.plane_area(net, layer)
                stranded = [via for via in self.router.vias if via.net == net and not in_plane(via.x, via.y)]
                if not stranded:
                    break
                spots = {pad.name: (via.x, via.y)
                         for via in stranded for pad in self.router.rip_up_plane_vias(net, [via])}
                for pad in [self._pad(net, name) for name in spots]:
                    if self._fan_out_into(net, pad, in_plane):
                        continue
                    cutting = sorted(self.router.nets_near(layer, spots[pad.name], PLANE_ISLAND_REACH)
                                     - {*FIXED_NETS, *PLANE_NETS})
                    for other in cutting:
                        self.router.prefer_layers(other, {layer: OFF_LAYER_FACTOR})
                        self.router.rip_up(other)
                    if not (self._fan_out_into(net, pad, self.router.plane_area(net, layer))
                            or self._fan_out_into(net, pad, _anywhere)):
                        self._record(net, self.unreached.get(net, []) + [pad.name])
                    for other in cutting:
                        self.net(other)

    def _fan_out_into(self, net: str, pad: Pad, where: Callable[[float, float], bool]) -> bool:
        return self.router.fan_out(net, pad, where, wide=True) or self.router.fan_out(net, pad, where)

    def _pad(self, net: str, name: str) -> Pad:
        return next(pad for pad in self.by_net[net] if pad.name == name)

    def _refresh(self, net: str, names: list[str]) -> None:
        """Records which of the named pads the net's tree still does not reach."""
        self._record(net, [name for name in dict.fromkeys(names)
                           if not any(self.router.joined(net, pad) for pad in self.by_net[net] if pad.name == name)])


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


def _bounds(pads: list[Pad]) -> tuple[float, float, float, float]:
    return (min(pad.rect[0] for pad in pads), min(pad.rect[1] for pad in pads),
            max(pad.rect[2] for pad in pads), max(pad.rect[3] for pad in pads))


def _on_outer_ring(pad: Pad, field: tuple[float, float, float, float]) -> bool:
    """True for a pad whose edge is within one pad of the pad field's outline: it can leave the field directly."""
    left, top, right, bottom = field
    size = min(pad.rect[2] - pad.rect[0], pad.rect[3] - pad.rect[1])
    return (pad.rect[0] < left + size or pad.rect[1] < top + size or pad.rect[2] > right - size
            or pad.rect[3] > bottom - size)


def _empty_middle(pads: list[Pad], centre: tuple[float, float]) -> tuple[float, float, float, float]:
    """The largest rectangle round `centre` that no pad overlaps, grown side by side in 0.05 mm steps."""
    step = 0.05
    rect = [centre[0], centre[1], centre[0], centre[1]]

    def clear(candidate: list[float]) -> bool:
        return not any(pad.rect[0] < candidate[2] and candidate[0] < pad.rect[2] and pad.rect[1] < candidate[3]
                       and candidate[1] < pad.rect[3] for pad in pads)

    assert clear(rect), "a pad sits on the module centre"
    growing = [True] * 4
    while any(growing):
        for side in range(4):
            if growing[side]:
                candidate = list(rect)
                candidate[side] += -step if side < 2 else step
                growing[side] = clear(candidate)
                if growing[side]:
                    rect = candidate
    return rect[0], rect[1], rect[2], rect[3]


def _grown(rect: tuple[float, float, float, float], margin: float) -> tuple[float, float, float, float]:
    left, top, right, bottom = rect
    return left - margin, top - margin, right + margin, bottom + margin


def _spread(pads: list[Pad]) -> float:
    """Half the perimeter of the box around the pads: a quick guess of the track length."""
    xs = [pad.centre[0] for pad in pads]
    ys = [pad.centre[1] for pad in pads]
    return max(xs) - min(xs) + max(ys) - min(ys)


def route(board: pcbnew.BOARD, setup: Setup) -> RoutingResult:
    """Plans every track and via. Nothing is written to the board; see write_copper."""
    router = new_router()
    return route_pads(router, _load_obstacles(board, router), setup)


def route_pads(router: Router, pads: dict[str, list[Pad]], setup: Setup) -> RoutingResult:
    """The routing order on a router that already holds every obstacle. Needs no board."""
    router.freeze(FIXED_NETS)
    plan = _Plan(router, pads, setup)
    plan.ground_vias()
    plan.pin_escapes()
    for net in CRYSTAL_NETS:
        plan.net(net)
        for plane_layer in (INNER, GROUND_INNER):   # the crystal keeps whole planes under it, as the USB pair does
            router.keep_layer_clear_near(net, plane_layer, USB_REFERENCE_MARGIN)
    plan.module_escapes()
    plan.plane_fan_out()
    plan.usb_entries()
    plan.net(VBUS, wide=True)
    plan.usb_pair()
    for net in POWER_NETS[1:]:
        plan.net(net, wide=True)
    plan.signals()
    plan.repair()
    plan.plane_islands()
    router.prune_dangling(PLANE_NETS)
    router.split_at_junctions()
    return RoutingResult(router, plan.unrouted, plan.narrowed_lines)


def write_copper(board: pcbnew.BOARD, router: Router) -> None:
    for track in router.tracks:
        segment = pcbnew.PCB_TRACK(board)
        segment.SetStart(_point(*track.start))
        segment.SetEnd(_point(*track.end))
        segment.SetWidth(pcbnew.FromMM(track.width))
        segment.SetLayer(_KICAD_LAYER[track.layer])
        segment.SetNet(board.FindNet(_board_net(track.net)))
        board.Add(segment)
    for via in router.vias:
        barrel = pcbnew.PCB_VIA(board)
        barrel.SetViaType(pcbnew.VIATYPE_THROUGH)
        barrel.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        barrel.SetPosition(_point(via.x, via.y))
        barrel.SetWidth(pcbnew.F_Cu, pcbnew.FromMM(router.rules.via_diameter))
        barrel.SetDrill(pcbnew.FromMM(router.rules.via_drill))
        barrel.SetNet(board.FindNet(_board_net(via.net)))
        board.Add(barrel)


def _point(x: float, y: float) -> pcbnew.VECTOR2I:
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def check_sensitive_lengths(router: Router) -> None:
    """Crystal lengths, the USB pair's mismatch, and no supply track on an inner layer."""
    for net, limit in LENGTH_LIMIT.items():
        length = router.net_length(net)
        assert 0 < length <= limit, f"{net} is {length:.2f} mm long, limit {limit} mm"
    mismatch = abs(router.net_length("USB_DP") - router.net_length("USB_DN"))
    assert mismatch <= USB_PAIR_MISMATCH_LIMIT, f"USB D+ and D- differ by {mismatch:.2f} mm"
    inner = sorted({track.net for track in router.tracks
                    if track.net in POWER_NETS and track.layer not in (FRONT, BACK)})
    assert not inner, f"supply nets with tracks on an inner layer: {inner}"
