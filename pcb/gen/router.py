"""A small grid router. Pure Python, no KiCad import, so it can be tested anywhere.

The board is a grid of nodes (0.1 mm pitch) on the two outer copper layers, and optionally the inner layers
(`Rules.layers`) for short hops: a step there costs _INNER_STEP_FACTOR (3.3 V plane) or _GROUND_STEP_FACTOR (ground
plane) times as much, so they are used only where the outer layers are full. Vias go through every layer. Every
piece of copper
claims the nodes a track of another net must stay away from. A node claimed by one net is open to
that net only; a node claimed by two nets, by a hole or by the board edge is closed to all.
Routes are A* paths over 45 degree moves, with vias as moves between the layers.

Rip-up and reroute: after `freeze`, the router remembers the board without copper. A connection that finds no
free way can ask what stands in it (`reach`: the same search, but other nets' copper may be crossed at a price).
A net's tree is kept as branches, one per pad it joined, so that only the crossed branches (and the branches that
leave from them) are taken off (`rip_up_branch`) and routed again afterwards. Copper of the nets named fixed at
`freeze` is never crossed. Every crossing raises a history cost on its nodes, so that the next searches of all
nets keep away from spots that were fought over (negotiated congestion).

Coordinates are millimetres, top view, same as board.toml.
"""

from __future__ import annotations

import heapq
import math
from array import array
from dataclasses import dataclass
from typing import Callable, Iterable

FRONT, BACK, INNER, GROUND_INNER = 0, 1, 2, 3
BOTH_LAYERS = (FRONT, BACK)
_FREE = 0
_CLOSED = -1

_STEPS = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
_NO_HEADING = 8
_HEADINGS = 9
_STRAIGHT_COST = 10
_DIAGONAL_COST = 14
# Indexed by the heading change in 45 degree steps. Sharper than 90 degrees is not allowed.
_TURN_COST = (0, 3, 15)
_VIA_COST = 300  # a via costs as much as 3 mm of track
# Price of one node of another net's copper in a `blockers` search: crossing a 0.1 mm track costs about as much
# as two vias, so the search goes round or changes layer where it can, and crosses only where it must.
_CROSSING_COST = 100
# Added to a node's cost for every search that had to cross other copper there.
_HISTORY_STEP = 20
# The coarse map behind a second, longer search (see _find_way): cells of this many nodes a side (2: a track's
# claim, 4 nodes wide, always closes a whole cell, so the map does not jump walls), and that search may expand this
# many times as many nodes as the first. Its estimate is close, so it may be greedier: _GUIDED_GREED.
_COARSE = 2
_GUIDED_LIMIT_FACTOR = 10
_GUIDED_GREED = (2, 1)
_UNREACHABLE = 1 << 30
# A step on the inner layer costs this many outer steps: the inner layer is a plane, and every track there cuts it.
_INNER_STEP_FACTOR = 3
# The same on the ground plane layer, dearer still: it is the reference of every top track.
_GROUND_STEP_FACTOR = 4
# A pad of a plane net reaches for copper that already has a via only if that is this much nearer
# than a via of its own. Cheap, or the pads chain up into long bars that wall in their neighbours.
_OWN_VIA_COST = 40
# The distance still to go counts 1.5 times: far fewer nodes searched, for a slightly longer track.
_GREED = (3, 2)

Rect = tuple[float, float, float, float]  # left, top, right, bottom
Node = tuple[int, int, int]  # layer, column, row


@dataclass(frozen=True)
class Rules:
    pitch: float = 0.1
    track_width: float = 0.15
    wide_track_width: float = 0.3
    clearance: float = 0.15
    via_diameter: float = 0.6
    via_drill: float = 0.3
    edge_clearance: float = 0.3
    hole_clearance: float = 0.25
    # A track between two nodes can come this much closer to a corner than the nodes themselves.
    grid_allowance: float = 0.02
    # Vias stay out of pads, so solder does not wick into them.
    via_to_pad_gap: float = 0.05
    via_to_via_gap: float = 0.25
    # Nodes one search may expand before it gives up on a connection.
    search_limit: int = 3_000_000
    # Layers that carry tracks: FRONT and BACK, and INNER and GROUND_INNER where an inner plane may be cut for
    # short hops. Numbered from 0 without gaps.
    layers: tuple[int, ...] = BOTH_LAYERS


@dataclass(frozen=True)
class Pad:
    name: str  # "U1.5"
    net: str  # "" for a pad without a net
    rect: Rect
    layers: tuple[int, ...]

    @property
    def centre(self) -> tuple[float, float]:
        left, top, right, bottom = self.rect
        return (left + right) / 2, (top + bottom) / 2


@dataclass(frozen=True)
class Track:
    net: str
    layer: int
    start: tuple[float, float]
    end: tuple[float, float]
    width: float

    @property
    def length(self) -> float:
        return math.dist(self.start, self.end)


@dataclass(frozen=True)
class Via:
    net: str
    x: float
    y: float


@dataclass
class _Branch:
    """One connection of a net's tree: the copper from the tree to one pad."""
    pad: Pad
    nodes: set[tuple[int, int]]   # the path's nodes and the pad's
    tracks: list[Track]
    vias: list[Via]
    parent: int | None   # the branch the path leaves from; None: the net's first pad or its escape


@dataclass(frozen=True)
class _Snapshot:
    """What `Router.restore` puts back."""
    tracks: list[Track]
    vias: list[Via]
    trees: dict[str, set[tuple[int, int]]]
    roots: dict[str, set[tuple[int, int]]]
    branches: dict[str, dict[int, _Branch]]
    stubs: dict[tuple[str, Rect], tuple[str, set[tuple[int, int]]]]
    plane_trees: dict[str, set[tuple[int, int]]]


Crossing = tuple[str, int | None]   # a crossed net, and its crossed branch (None: its first pad or escape)


class Router:
    def __init__(self, width: float, height: float, corner_radius: float, rules: Rules = Rules()) -> None:
        self.rules = rules
        self.board_width, self.board_height = width, height
        self._pitch = rules.pitch
        self._columns = round(width / rules.pitch) + 1
        self._rows = round(height / rules.pitch) + 1
        node_count = self._columns * self._rows
        self._layers = rules.layers
        self._track_cells = [array("i", bytes(4 * node_count)) for _ in self._layers]
        self._via_cells = array("i", bytes(4 * node_count))
        self._net_ids: dict[str, int] = {}
        self._tree: dict[str, set[tuple[int, int]]] = {}  # copper already joined, per net: (layer, index)
        self._roots: dict[str, set[tuple[int, int]]] = {}  # the part of the tree that is no branch: its first pad
        self._branches: dict[str, dict[int, _Branch]] = {}
        self._branch_count = 0
        self._plane_tree: dict[str, set[tuple[int, int]]] = {}  # copper that already has a via to its plane
        self._plane_roots: dict[str, set[tuple[int, int]]] = {}  # the hand-placed vias' nodes, per plane net
        self._pad_centre: dict[tuple[int, int], tuple[float, float]] = {}
        # pad (name and place: two pads can share a name) -> net, nodes of its escape
        self._stubs: dict[tuple[str, Rect], tuple[str, set[tuple[int, int]]]] = {}
        self._pads: list[Pad] = []   # pads with a net, for prune_dangling
        self._fixed_items: set[int] = set()   # ids of escape tracks and vias: fixed copper of nets that are not
        self.tracks: list[Track] = []
        self.vias: list[Via] = []
        self._half_track = rules.track_width / 2
        self._via_radius = rules.via_diameter / 2
        self._track_reach = self._half_track + rules.clearance + rules.grid_allowance
        self._via_reach = self._via_radius + rules.clearance + rules.grid_allowance
        self._history = [array("i", bytes(4 * node_count)) for _ in self._layers]
        # Set by freeze(): the cells without any copper, the cells with only fixed copper, and the fixed nets.
        self._bare: tuple[list[array], array] | None = None
        self._fixed_cells: tuple[list[array], array] | None = None
        self._fixed_ids: set[int] = set()
        self._clear_layers: list[tuple[str, int, float]] = []   # (net, layer, reach), see keep_layer_clear_near
        self._default_step_factors = [{INNER: _INNER_STEP_FACTOR, GROUND_INNER: _GROUND_STEP_FACTOR}.get(layer, 1)
                                      for layer in self._layers]
        self._step_factors: dict[str, list[int]] = {}   # per net, see prefer_layers
        self._close_board_edge(corner_radius)

    # --- obstacles ----------------------------------------------------------------------------

    def add_pad(self, pad: Pad) -> None:
        owner = self._net_id(pad.net) if pad.net else _CLOSED
        if pad.net:
            self._pads.append(pad)
        for layer in pad.layers:
            self._claim_rect(self._track_cells[layer], pad.rect, self._track_reach, owner)
            if pad.net:
                for index in self._nodes_in(pad.rect):
                    self._pad_centre[(layer, index)] = pad.centre
        self._claim_rect(self._via_cells, pad.rect, self._via_reach, owner)
        self._claim_rect(self._via_cells, pad.rect, self._via_radius + self.rules.via_to_pad_gap, _CLOSED)

    def add_hole(self, rect: Rect) -> None:
        """A hole without copper: tracks and vias keep the hole clearance."""
        reach = self.rules.hole_clearance + self.rules.grid_allowance
        for layer in self._layers:
            self._claim_rect(self._track_cells[layer], rect, self._half_track + reach, _CLOSED)
        self._claim_rect(self._via_cells, rect, self._via_radius + reach, _CLOSED)

    def add_keepout(self, rect: Rect, layers: Iterable[int]) -> None:
        """No tracks on these layers inside the rectangle, and no vias."""
        for layer in layers:
            self._claim_rect(self._track_cells[layer], rect, 0.0, _CLOSED)
        self._claim_rect(self._via_cells, rect, 0.0, _CLOSED)

    def freeze(self, fixed_nets: Iterable[str]) -> None:
        """Ends the obstacles: pads, holes, keep-outs and outline are final, copper comes next. The copper of
        `fixed_nets` is never ripped up and never crossed by a `blockers` search."""
        assert self._bare is None, "the router is already frozen"
        assert not self.tracks and not self.vias, "freeze before the first copper"
        self._bare = ([array("i", cells) for cells in self._track_cells], array("i", self._via_cells))
        self._fixed_cells = ([array("i", cells) for cells in self._track_cells], array("i", self._via_cells))
        self._fixed_ids = {self._net_id(net) for net in fixed_nets}

    def rip_up(self, net: str) -> None:
        """Takes every track and via of the net off the board; its pads count as not joined again."""
        self._take_off_net(net)
        self._rebuild()

    def rip_up_branch(self, net: str, branch_id: int) -> list[Pad]:
        """Takes one branch of the net's tree off the board, with every branch that leaves from it. Returns the
        pads they had joined. A branch that is already gone returns nothing."""
        pads = self._take_off_branch(net, branch_id)
        self._rebuild()
        return pads

    def rip_up_crossings(self, crossings: Iterable[Crossing]) -> dict[str, list[Pad]]:
        """Takes the crossed branches off (a whole net where its first pad or escape was crossed), with one
        rebuild of the cells. Returns, per net, the pads no longer joined."""
        lost: dict[str, list[Pad]] = {}
        for net, branch_id in sorted(crossings, key=lambda crossing: (crossing[0], crossing[1] or 0)):
            if branch_id is None:
                lost[net] = self._take_off_net(net)
            else:
                lost.setdefault(net, []).extend(self._take_off_branch(net, branch_id))
        self._rebuild()
        return lost

    def snapshot(self) -> _Snapshot:
        """The copper and the trees as they are now, for `restore`."""
        return _Snapshot(list(self.tracks), list(self.vias), _copied(self._tree), _copied(self._roots),
                         {net: dict(branches) for net, branches in self._branches.items()}, dict(self._stubs),
                         _copied(self._plane_tree))

    def restore(self, snapshot: _Snapshot) -> None:
        """Puts the copper and the trees back as `snapshot` saw them. The history costs stay as they are."""
        self.tracks, self.vias = list(snapshot.tracks), list(snapshot.vias)
        self._tree = _copied(snapshot.trees)
        self._roots = _copied(snapshot.roots)
        self._plane_tree = _copied(snapshot.plane_trees)
        self._branches = {net: dict(branches) for net, branches in snapshot.branches.items()}
        self._stubs = dict(snapshot.stubs)
        # Copper that is gone may leave its id to a new object: only ids of copper that is back stay fixed.
        self._fixed_items &= {id(item) for item in (*self.tracks, *self.vias)}
        self._rebuild()

    def _take_off_net(self, net: str) -> list[Pad]:
        assert self._bare is not None, "rip-up needs a frozen router"
        assert self._net_id(net) not in self._fixed_ids, f"{net} is fixed"
        # The net's escapes and hand-placed vias are fixed: they stay, and its pads can still be reached by them.
        self.tracks = [track for track in self.tracks if track.net != net or id(track) in self._fixed_items]
        self.vias = [via for via in self.vias if via.net != net or id(via) in self._fixed_items]
        self._tree.pop(net, None)
        self._roots.pop(net, None)
        self._branches.pop(net, None)
        if net in self._plane_roots:
            self._plane_tree[net] = set(self._plane_roots[net])
        else:
            self._plane_tree.pop(net, None)
        return [pad for pad in self._pads if pad.net == net]

    def _take_off_branch(self, net: str, branch_id: int) -> list[Pad]:
        assert self._bare is not None, "rip-up needs a frozen router"
        assert self._net_id(net) not in self._fixed_ids, f"{net} is fixed"
        branches = self._branches.get(net, {})
        if branch_id not in branches:
            return []
        doomed = {branch_id}
        grew = True
        while grew:
            leaving = {key for key, branch in branches.items() if branch.parent in doomed}
            grew = not leaving <= doomed
            doomed |= leaving
        removed = [branches.pop(key) for key in sorted(doomed)]
        copper = {id(item) for branch in removed for item in (*branch.tracks, *branch.vias)}
        self.tracks = [track for track in self.tracks if id(track) not in copper]
        self.vias = [via for via in self.vias if id(via) not in copper]
        kept = [branch.nodes for branch in branches.values()]
        if net in self._roots:
            self._tree[net] = set(self._roots[net]).union(*kept)
        else:   # a plane net: its fan-outs
            self._plane_tree[net] = set(self._plane_roots.get(net, ())).union(*kept)
        return [branch.pad for branch in removed]

    def _rebuild(self) -> None:
        """Claims all copper again, starting from the bare board: a claim cannot be undone node by node."""
        bare_tracks, bare_vias = self._bare
        self._track_cells = [array("i", cells) for cells in bare_tracks]
        self._via_cells = array("i", bare_vias)
        self._fixed_cells = ([array("i", cells) for cells in bare_tracks], array("i", bare_vias))
        for clearance in self._clear_layers:
            self._close_near(*clearance)
        for track in self.tracks:
            self._claim_track(track)
        for via in self.vias:
            self._claim_via(via)

    def prefer_layers(self, net: str, step_factors: dict[int, int]) -> None:
        """Makes a step on the named layers cost that many times as much, for every later search of the net."""
        factors = list(self._default_step_factors)
        for layer, factor in step_factors.items():
            factors[layer] = factor
        self._step_factors[net] = factors

    def keep_layer_clear_near(self, net: str, layer: int, reach: float) -> None:
        """Closes the layer to every track within `reach` of the net's copper as it is now, also after any
        rip-up: for a plane that must stay whole under a sensitive net. The net must be fixed."""
        assert self._net_id(net) in self._fixed_ids, f"{net} must be fixed, or its copper could move"
        self._clear_layers.append((net, layer, reach))
        self._close_near(net, layer, reach)

    def _close_near(self, net: str, layer: int, reach: float) -> None:
        for track_cells, _ in (self._track_cells, self._via_cells), self._fixed_cells:
            cells = track_cells[layer]
            for track in self.tracks:
                if track.net == net:
                    self._claim_segment(cells, track.start, track.end, track.width / 2 + reach, _CLOSED)
            for via in self.vias:
                if via.net == net:
                    self._claim_rect(cells, (via.x, via.y, via.x, via.y), self._via_radius + reach, _CLOSED)

    def add_via(self, net: str, x: float, y: float) -> None:
        """A via placed by hand, already joined to its plane. The position is snapped to the grid."""
        assert self.via_fits(net, x, y), f"{net} via at ({x}, {y}) has no room"
        self._add_plane_via(net, self._index_at(x, y))

    def snapped(self, x: float, y: float) -> tuple[float, float]:
        """The grid node nearest to a point."""
        return self._xy(self._index_at(x, y))

    def via_fits(self, net: str, x: float, y: float) -> bool:
        return self._via_cells[self._index_at(x, y)] in (_FREE, self._net_id(net))

    def add_via_in_pad(self, net: str, x: float, y: float) -> None:
        """The same, inside a pad of its own net: for the vias in a chip's exposed pad. The via cells round a pad
        are closed to every via, so only the track cells are checked: the barrel crosses both outer layers, and
        on each one the spot must be free or already this net's copper."""
        index = self._index_at(x, y)
        owner = self._net_id(net)
        crowded = [layer for layer in self._layers if self._track_cells[layer][index] not in (_FREE, owner)]
        assert not crowded, f"{net} via in pad at ({x}, {y}) crowds other copper on layers {crowded}"
        self._add_plane_via(net, index)

    def _add_plane_via(self, net: str, index: int) -> None:
        """A via placed by hand: fixed copper, and a root of the net's plane tree."""
        self._fixed_items.add(id(self._commit_via(net, index)))
        nodes = {(layer, index) for layer in self._layers}
        self._plane_tree.setdefault(net, set()).update(nodes)
        self._plane_roots.setdefault(net, set()).update(nodes)

    def _index_at(self, x: float, y: float) -> int:
        return round(y / self._pitch) * self._columns + round(x / self._pitch)

    def _close_board_edge(self, corner_radius: float) -> None:
        track_inset = self.rules.edge_clearance + self._half_track + self.rules.grid_allowance
        via_inset = self.rules.edge_clearance + self._via_radius + self.rules.grid_allowance
        for cells, inset in [(cells, track_inset) for cells in self._track_cells] + [(self._via_cells, via_inset)]:
            self._close_outside_rounded_rectangle(cells, inset, corner_radius)

    def _close_outside_rounded_rectangle(self, cells: array, inset: float, corner_radius: float) -> None:
        pitch, width, height = self._pitch, self.board_width, self.board_height
        band = math.ceil(max(inset, corner_radius) / pitch) + 1
        for row in range(self._rows):
            y = row * pitch
            near_horizontal_edge = row < band or row >= self._rows - band
            columns = range(self._columns) if near_horizontal_edge else (
                list(range(band)) + list(range(self._columns - band, self._columns)))
            for column in columns:
                x = column * pitch
                # Distance into the board, measured from the rounded outline.
                dx = max(corner_radius - x, x - (width - corner_radius), 0.0)
                dy = max(corner_radius - y, y - (height - corner_radius), 0.0)
                if dx > 0 and dy > 0:
                    depth = corner_radius - math.hypot(dx, dy)
                else:
                    depth = min(x, width - x, y, height - y)
                if depth < inset:
                    cells[row * self._columns + column] = _CLOSED

    def close_outside(self, outline: list[tuple[float, float]]) -> None:
        """Closes every node outside a polygon board outline, or too close to its edge.

        For outlines that are not a rounded rectangle (tongues, notches). The polygon is a closed list of
        corners, arcs already cut into short segments. Nodes outside it are closed on every layer; nodes
        within the edge clearance of any of its sides are closed as the rounded rectangle's are.
        """
        track_inset = self.rules.edge_clearance + self._half_track + self.rules.grid_allowance
        via_inset = self.rules.edge_clearance + self._via_radius + self.rules.grid_allowance
        sides = list(zip(outline, outline[1:] + outline[:1], strict=True))
        for row in range(self._rows):
            inside = _inside_columns(sides, row * self._pitch, self._pitch, self._columns)
            base = row * self._columns
            for column in range(self._columns):
                if not inside[column]:
                    for cells in (*self._track_cells, self._via_cells):
                        cells[base + column] = _CLOSED
        for cells, inset in [(cells, track_inset) for cells in self._track_cells] + [(self._via_cells, via_inset)]:
            for start, end in sides:
                self._claim_segment(cells, start, end, inset, _CLOSED)

    def is_open(self, layer: int, x: float, y: float) -> bool:
        """True when a track of a new net could pass through the node nearest to the point."""
        return self._track_cells[layer][self._index_at(x, y)] == _FREE

    def _net_id(self, net: str) -> int:
        return self._net_ids.setdefault(net, len(self._net_ids) + 1)

    def _row_range(self, low: float, high: float) -> range:
        return range(max(0, math.ceil(low / self._pitch - 1e-9)),
                     min(self._rows - 1, math.floor(high / self._pitch + 1e-9)) + 1)

    def _column_range(self, low: float, high: float) -> range:
        return range(max(0, math.ceil(low / self._pitch - 1e-9)),
                     min(self._columns - 1, math.floor(high / self._pitch + 1e-9)) + 1)

    def _nodes_in(self, rect: Rect) -> list[int]:
        left, top, right, bottom = rect
        return [row * self._columns + column
                for row in self._row_range(top, bottom) for column in self._column_range(left, right)]

    def _claim_rect(self, cells: array, rect: Rect, reach: float, owner: int) -> None:
        """Claims every node closer than `reach` to the rectangle (or inside it)."""
        left, top, right, bottom = rect
        pitch, reach_squared = self._pitch, reach * reach + 1e-12
        for row in self._row_range(top - reach, bottom + reach):
            y = row * pitch
            dy = max(top - y, y - bottom, 0.0)
            base = row * self._columns
            for column in self._column_range(left - reach, right + reach):
                x = column * pitch
                dx = max(left - x, x - right, 0.0)
                if dx * dx + dy * dy <= reach_squared:
                    _claim(cells, base + column, owner)

    def _claim_segment(self, cells: array, start: tuple[float, float], end: tuple[float, float],
                       reach: float, owner: int) -> None:
        (x1, y1), (x2, y2) = start, end
        pitch, reach_squared = self._pitch, reach * reach
        span_x, span_y = x2 - x1, y2 - y1
        span_squared = span_x * span_x + span_y * span_y
        for row in self._row_range(min(y1, y2) - reach, max(y1, y2) + reach):
            y = row * pitch
            base = row * self._columns
            for column in self._column_range(min(x1, x2) - reach, max(x1, x2) + reach):
                x = column * pitch
                along = 0.0 if span_squared == 0 else max(
                    0.0, min(1.0, ((x - x1) * span_x + (y - y1) * span_y) / span_squared))
                dx, dy = x - (x1 + along * span_x), y - (y1 + along * span_y)
                if dx * dx + dy * dy < reach_squared:
                    _claim(cells, base + column, owner)

    # --- queries ------------------------------------------------------------------------------

    def _xy(self, index: int) -> tuple[float, float]:
        row, column = divmod(index, self._columns)
        return round(column * self._pitch, 4), round(row * self._pitch, 4)

    def pad_nodes(self, pad: Pad) -> set[tuple[int, int]]:
        indices = self._nodes_in(pad.rect)
        assert indices, f"{pad.name}: no grid node inside the pad"
        return {(layer, index) for layer in pad.layers for index in indices}

    def net_length(self, net: str) -> float:
        return sum(track.length for track in self.tracks if track.net == net)

    # --- routing ------------------------------------------------------------------------------

    def route_net(self, net: str, pads: list[Pad], wide: bool = False) -> list[str]:
        """Joins the pads into one tree, nearest pad first. Returns the names of pads it could not reach."""
        tree = self._tree.setdefault(net, set())

        def connect(pad: Pad) -> bool:
            routed = self._route_to_pad(net, tree, pad, wide)
            if routed is not None:
                self._join(net, pad, *routed)
            return routed is not None

        return self._grow_tree(net, pads, connect)

    def _grow_tree(self, net: str, pads: list[Pad], connect: Callable[[Pad], bool]) -> list[str]:
        """Seeds the net's tree with its first pad when it is empty, then connects the others nearest first."""
        tree = self._tree.setdefault(net, set())
        waiting = [pad for pad in pads if not tree & self.pad_nodes(pad)]
        if not tree:
            tree |= self._target_nodes(waiting.pop(0))
            self._roots[net] = set(tree)
        joined_centres = [pad.centre for pad in pads if pad not in waiting] or [pads[0].centre]
        unreached = []
        while waiting:
            nearest = min(waiting, key=lambda pad: min(math.dist(pad.centre, c) for c in joined_centres))
            waiting.remove(nearest)
            if connect(nearest):
                joined_centres.append(nearest.centre)
            else:
                unreached.append(nearest.name)
        return unreached

    def _join(self, net: str, pad: Pad, path: list[Node], copper: tuple[list[Track], list[Via]]) -> None:
        """Adds a committed path and the pad it reached (with its escape) to the net's tree, as a new branch."""
        tree = self._tree[net]
        pad_nodes = self._target_nodes(pad)
        start = self._indexed(path[:1]) or sorted(pad_nodes & tree)[:1]
        branches = self._branches.setdefault(net, {})
        parent = next((key for key, branch in branches.items() if branch.nodes.intersection(start)), None)
        nodes = set(self._indexed(path)) | pad_nodes
        tree.update(nodes)
        self._branch_count += 1
        branches[self._branch_count] = _Branch(pad, nodes, *copper, parent)

    def _target_nodes(self, pad: Pad) -> set[tuple[int, int]]:
        """The pad's nodes and those of its escape: a connection may end on either."""
        stub = self._stubs.get((pad.name, pad.rect))
        return self.pad_nodes(pad) | stub[1] if stub else self.pad_nodes(pad)

    def route_pair(self, net: str, first: Pad, second: Pad, wide: bool = False) -> bool:
        """One direct connection between two pads. It does not become part of the net's tree."""
        return self._route_to_pad(net, self.pad_nodes(first), second, wide) is not None

    def route_to_via(self, net: str, pads: list[Pad], via: Via, wide: bool = False) -> bool:
        """Joins the pads' copper to a via that is already there, on either layer."""
        sources = set().union(*(self.pad_nodes(pad) for pad in pads))
        target = Pad("via", net, (via.x, via.y, via.x, via.y), self._layers)
        return self._route_to_pad(net, sources, target, wide) is not None

    def _route_to_pad(self, net: str, sources: set[tuple[int, int]], target: Pad, wide: bool
                      ) -> tuple[list[Node], tuple[list[Track], list[Via]]] | None:
        """Writes the copper from any source node to the pad. Returns the path, empty if they already touch,
        and the copper written."""
        target_nodes = self._target_nodes(target)
        if sources & target_nodes:
            return [], ([], [])
        path = self._find_way(net, sources, target, wide, crossing=False)
        if path is None:
            return None
        return path, self._commit(net, path, wide)

    def _find_way(self, net: str, sources: set[tuple[int, int]], target: Pad, wide: bool,
                  crossing: bool) -> list[Node] | None:
        """A search toward the pad's rectangle first; when it gives up, a longer one that follows a coarse map
        of the board, for ways that run far round. None also when the coarse map shows no way at all."""
        target_nodes = self._target_nodes(target)
        path = self._search(net, sources, target_nodes.__contains__, self._distance_to(target), wide,
                            vias_allowed=True, crossing=crossing)
        if path is not None:
            return path
        guide = self._coarse_distances(net, target_nodes, crossing)
        if not any(guide(layer, *self._column_row(index)) < _UNREACHABLE for layer, index in sources):
            return None
        return self._search(net, sources, target_nodes.__contains__, guide, wide, vias_allowed=True,
                            crossing=crossing, limit=self.rules.search_limit * _GUIDED_LIMIT_FACTOR,
                            greed=_GUIDED_GREED)

    def _column_row(self, index: int) -> tuple[int, int]:
        row, column = divmod(index, self._columns)
        return column, row

    def _coarse_distances(self, net: str, target_nodes: set[tuple[int, int]],
                          crossing: bool) -> Callable[[int, int, int], int]:
        """Cost to go from every node to the target, measured on cells of _COARSE x _COARSE nodes. A cell is open
        on a layer when any of its nodes is open to the net, so the measure never says no where there is a way;
        a via fits where any node takes one. Unreachable cells cost _UNREACHABLE."""
        size = _COARSE
        columns, rows = self._columns, self._rows
        coarse_columns, coarse_rows = -(-columns // size), -(-rows // size)
        open_values = (_FREE, self._net_id(net))
        track_cells, via_cells = self._fixed_cells if crossing else (self._track_cells, self._via_cells)

        def open_map(cells: array) -> bytearray:
            opened = bytearray(coarse_columns * coarse_rows)
            for row in range(rows):
                line = cells[row * columns:(row + 1) * columns]
                base = (row // size) * coarse_columns
                for coarse_column in range(coarse_columns):
                    if not opened[base + coarse_column]:
                        chunk = line[coarse_column * size:(coarse_column + 1) * size]
                        if open_values[0] in chunk or open_values[1] in chunk:
                            opened[base + coarse_column] = 1
            return opened

        layer_open = [open_map(cells) for cells in track_cells]
        via_open = open_map(via_cells)
        cell_count = coarse_columns * coarse_rows
        distance = [array("i", [_UNREACHABLE]) * cell_count for _ in self._layers]
        queue = []
        for layer, index in target_nodes:
            row, column = divmod(index, columns)
            cell = (row // size) * coarse_columns + column // size
            if distance[layer][cell] != 0:
                distance[layer][cell] = 0
                queue.append((0, layer, cell))
        heapq.heapify(queue)
        factors = self._step_factors.get(net, self._default_step_factors)
        steps = [(dy * coarse_columns + dx, dx, size * (_DIAGONAL_COST if dx and dy else _STRAIGHT_COST))
                 for dx, dy in _STEPS]
        while queue:
            cost, layer, cell = heapq.heappop(queue)
            if cost > distance[layer][cell]:
                continue
            column = cell % coarse_columns
            for offset, dx, step in steps:
                neighbour = cell + offset
                if not (0 <= neighbour < cell_count and 0 <= column + dx < coarse_columns):
                    continue
                if layer_open[layer][neighbour] and cost + step * factors[layer] < distance[layer][neighbour]:
                    distance[layer][neighbour] = cost + step * factors[layer]
                    heapq.heappush(queue, (cost + step * factors[layer], layer, neighbour))
            if via_open[cell]:
                for other in self._layers:
                    if other != layer and layer_open[other][cell] and cost + _VIA_COST < distance[other][cell]:
                        distance[other][cell] = cost + _VIA_COST
                        heapq.heappush(queue, (cost + _VIA_COST, other, cell))

        def remaining(layer: int, column: int, row: int) -> int:
            return distance[layer][(row // size) * coarse_columns + column // size]

        return remaining

    def _distance_to(self, target: Pad) -> Callable[[int, int, int], int]:
        """Estimated cost from a node to the pad: 45 degree track, and a via when the pad is on the other layer."""
        left, top, right, bottom = (round(v / self._pitch) for v in target.rect)
        target_layers = target.layers

        def remaining(layer: int, column: int, row: int) -> int:
            dx = max(left - column, column - right, 0)
            dy = max(top - row, row - bottom, 0)
            estimate = _STRAIGHT_COST * max(dx, dy) + (_DIAGONAL_COST - _STRAIGHT_COST) * min(dx, dy)
            return estimate if layer in target_layers else estimate + _VIA_COST

        return remaining

    def reach(self, net: str, pad: Pad) -> set[Crossing] | None:
        """Joins the pad to the net's tree at signal width, or names the branches whose copper stands in the way.

        Searches as `route_net` does, but may cross the copper of nets that are not fixed, at a price per node.
        A way that crosses nothing is written and the pad joined: the result is empty. A way that crosses
        copper is not written; the result names the crossed branches, and the history cost rises on the crossed
        nodes. None: pads, holes, the outline or fixed copper wall the pad off. A net without copper (ripped up
        whole) starts its tree again from this pad: the result is empty."""
        assert self._bare is not None, "reach needs a frozen router"
        sources = self._tree.get(net)
        if not sources:   # the net was ripped up whole: this pad starts its tree again
            self._tree[net] = self._target_nodes(pad)
            self._roots[net] = set(self._tree[net])
            return set()
        target_nodes = self._target_nodes(pad)
        if sources & target_nodes:
            self._join(net, pad, [], ([], []))
            return set()
        path = self._find_way(net, sources, pad, wide=False, crossing=True)
        if path is None:
            return None
        open_to_net = (_FREE, self._net_id(net))
        crossed_nodes = [(layer, row * self._columns + column) for layer, column, row in path
                         if self._track_cells[layer][row * self._columns + column] not in open_to_net]
        crowded_vias = [index for (layer, index), (next_layer, _) in zip(self._indexed(path), self._indexed(path[1:]))
                        if layer != next_layer and self._via_cells[index] not in open_to_net]
        if not crossed_nodes and not crowded_vias:
            self._join(net, pad, path, self._commit(net, path, wide=False))
            return set()
        for layer, index in crossed_nodes:
            self._history[layer][index] += _HISTORY_STEP
        tracks, vias = self._copper(net, path, wide=False)
        # Nodes closed by copper that no single track or via comes near enough to name: treated as a wall.
        return self._crossed(net, tracks, vias) or None

    def _crossed(self, net: str, tracks: list[Track], vias: list[Via]) -> set[Crossing]:
        """Branches whose tracks or vias come closer to the given copper than the clearance plus one grid step."""
        rules = self.rules
        margin = rules.clearance + rules.grid_allowance + self._pitch
        via_gap = rules.via_diameter + rules.via_to_via_gap + self._pitch
        owner = {id(item): (other_net, key) for other_net, branches in self._branches.items()
                 for key, branch in branches.items() for item in (*branch.tracks, *branch.vias)}
        crossed = set()
        for other in self.tracks:
            if other.net == net or self._is_fixed(other):
                continue
            reach = other.width / 2 + margin
            if any(mine.layer == other.layer and _segment_gap(mine, other) < reach + mine.width / 2
                   for mine in tracks) or any(
                    _point_gap((via.x, via.y), other) < reach + self._via_radius for via in vias):
                crossed.add(owner.get(id(other), (other.net, None)))
        for other in self.vias:
            if other.net == net or self._is_fixed(other):
                continue
            spot = (other.x, other.y)
            if any(_point_gap(spot, mine) < self._via_radius + mine.width / 2 + margin for mine in tracks) or any(
                    math.dist(spot, (via.x, via.y)) < via_gap for via in vias):
                crossed.add(owner.get(id(other), (other.net, None)))
        return crossed

    def _indexed(self, path: list[Node]) -> list[tuple[int, int]]:
        return [(layer, row * self._columns + column) for layer, column, row in path]

    def escape(self, net: str, pad: Pad, box: Rect, longest: float = math.inf) -> bool:
        """Shortest way from a pad out of the rectangle `box` (a part's pad field, grown).

        The escape is fixed copper, never ripped up, and belongs to the pad: the rest of the net may end on it
        anywhere. The unused end is cut off by prune_dangling.
        """
        return self._escape(net, pad, box, None, longest)

    def escape_to_via(self, net: str, pad: Pad, box: Rect, longest: float = math.inf) -> bool:
        """The same, ending on a new via outside the box: the rest of the net then reaches the pad on any layer,
        however the copper laid later closes round the end of the escape."""
        net_id = self._net_id(net)
        return self._escape(net, pad, box, lambda index: self._via_cells[index] in (_FREE, net_id), longest)

    def _escape(self, net: str, pad: Pad, box: Rect, via_fits: Callable[[int], bool] | None,
                longest: float = math.inf) -> bool:
        left, top, right, bottom = (round(value / self._pitch) for value in box)

        def steps_to_go(column: int, row: int) -> int:
            if left <= column <= right and top <= row <= bottom:
                return 1 + min(column - left, right - column, row - top, bottom - row)
            return 0

        def is_outside(node: tuple[int, int]) -> bool:
            return via_fits is None and steps_to_go(*self._column_row(node[1])) == 0

        def via_fits_outside(index: int) -> bool:
            return steps_to_go(*self._column_row(index)) == 0 and via_fits(index)

        path = self._search(net, self.pad_nodes(pad), is_outside,
                            lambda layer, column, row: _STRAIGHT_COST * steps_to_go(column, row),
                            wide=False, vias_allowed=via_fits is None,
                            via_fits=via_fits_outside if via_fits else None)
        return self._keep_escape(net, pad, path, longest)

    def escape_to_via_inside(self, net: str, pad: Pad, area: Rect, longest: float = math.inf) -> bool:
        """A way from the pad to a new via inside `area`: for the pads deep in a module's pad field, whose nearest
        room for a via is the empty middle under the module. The via is fixed copper as an escape's is."""
        left, top, right, bottom = (round(value / self._pitch) for value in area)
        net_id = self._net_id(net)

        def steps_to_go(column: int, row: int) -> int:
            return max(left - column, column - right, top - row, row - bottom, 0)

        def via_fits_inside(index: int) -> bool:
            return steps_to_go(*self._column_row(index)) == 0 and self._via_cells[index] in (_FREE, net_id)

        path = self._search(net, self.pad_nodes(pad), lambda node: False,
                            lambda layer, column, row: _STRAIGHT_COST * steps_to_go(column, row),
                            wide=False, vias_allowed=False, via_fits=via_fits_inside)
        return self._keep_escape(net, pad, path, longest)

    def _keep_escape(self, net: str, pad: Pad, path: list[Node] | None, longest: float = math.inf) -> bool:
        """Writes an escape path as fixed copper that belongs to the pad; nothing when its tracks are longer than
        `longest` mm, since a long escape walls in its neighbours for good."""
        if path is None:
            return False
        if path[-1][0] < 0:   # the marker of a new via at the last node
            path.pop()
            layer, column, row = path[-1]
            path.append(((layer + 1) % len(self._layers), column, row))
        tracks, vias = self._copper(net, path, wide=False)
        if sum(track.length for track in tracks) > longest:
            return False
        self._fixed_items.update(id(item) for item in (*tracks, *vias))
        self._write(tracks, vias)
        nodes = set(self._indexed(path))
        for layer, column, row in path[1:]:
            if layer != path[0][0]:   # a via on the way reaches every layer
                nodes.update((other, row * self._columns + column) for other in self._layers)
        self._stubs[(pad.name, pad.rect)] = (net, nodes)
        return True

    def joined(self, net: str, pad: Pad) -> bool:
        """True when the pad is part of the net's tree, or has its way to the net's plane."""
        nodes = self.pad_nodes(pad)
        return bool(self._tree.get(net, set()) & nodes or self._plane_tree.get(net, set()) & nodes)

    def plane_area(self, net: str, layer: int) -> Callable[[float, float], bool]:
        """Where the net's plane on `layer` would be one piece: the largest 4-connected area of nodes open to the
        net whose four neighbours are open too. The fill keeps its clearance from other copper and needs a minimum
        width; dropping the nodes next to closed ones stands in for both, so a gap of one or two nodes between two
        vias does not count as a way through. Tracks on the layer and other nets' vias cut the area; a via of the
        net outside it would sit in an island of the fill. The bands kept clear of tracks (keep_layer_clear_near)
        are filled, so they do not count as cuts."""
        net_id = self._net_id(net)
        assert self._bare is not None, "plane_area needs a frozen router"
        cells = array("i", self._bare[0][layer])
        for track in self.tracks:
            if track.layer == layer:
                self._claim_segment(cells, track.start, track.end, track.width / 2 + self._track_reach,
                                    self._net_id(track.net))
        for via in self.vias:
            self._claim_rect(cells, (via.x, via.y, via.x, via.y), self._via_radius + self._track_reach,
                             self._net_id(via.net))
        columns, count = self._columns, self._columns * self._rows
        opened = bytearray(count)
        for index in range(columns + 1, count - columns - 1):
            if all(cells[node] in (_FREE, net_id) for node in (index, index - 1, index + 1, index - columns,
                                                                 index + columns)):
                opened[index] = 1
        label = array("i", bytes(4 * count))
        sizes = [0]
        for seed in range(count):
            if not opened[seed] or label[seed]:
                continue
            sizes.append(0)
            label[seed] = len(sizes) - 1
            stack = [seed]
            while stack:
                index = stack.pop()
                sizes[-1] += 1
                for neighbour in (index - 1, index + 1, index - columns, index + columns):
                    if opened[neighbour] and not label[neighbour]:
                        label[neighbour] = len(sizes) - 1
                        stack.append(neighbour)
        largest = max(range(len(sizes)), key=sizes.__getitem__)
        return lambda x, y: label[self._index_at(x, y)] == largest

    def nets_near(self, layer: int, point: tuple[float, float], reach: float) -> set[str]:
        """Nets with a track on the layer within `reach` mm of the point."""
        return {track.net for track in self.tracks if track.layer == layer and _point_gap(point, track) < reach}

    def rip_up_plane_vias(self, net: str, vias: list[Via]) -> list[Pad]:
        """Takes off the fan-outs (plane branches) that own these vias; returns the pads they had joined."""
        doomed = {id(via) for via in vias}
        branches = self._branches.get(net, {})
        keys = [key for key, branch in branches.items() if any(id(via) in doomed for via in branch.vias)]
        pads = [pad for key in keys for pad in self._take_off_branch(net, key)]
        self._rebuild()
        return pads

    def prune_dangling(self, plane_nets: Iterable[str]) -> None:
        """Cuts every track end that touches nothing of its net back to the last point that does, and drops
        vias that join copper on fewer than two layers, until nothing changes. Escapes that the rest of their
        net did not use to the end leave such ends. Plane nets are left alone: their vias join a plane."""
        skipped = set(plane_nets)
        nets = sorted({item.net for item in (*self.tracks, *self.vias)} - skipped)
        for net in nets:
            pads = [pad for pad in self._pads if pad.net == net]
            tracks = [track for track in self.tracks if track.net == net]
            vias = [via for via in self.vias if via.net == net]
            kept_tracks, kept_vias = _pruned(tracks, vias, pads)
            gone = {id(item) for item in (*tracks, *vias)}
            self.tracks = [track for track in self.tracks if id(track) not in gone] + kept_tracks
            self.vias = [via for via in self.vias if id(via) not in gone] + kept_vias

    def split_at_junctions(self) -> None:
        """Cuts every track where another track of its net and layer ends on its middle, so that each junction is
        two track ends meeting. KiCad joins a T either way, but its DRC calls an end on the middle of a track
        dangling. The last step: the branch bookkeeping of rip-up does not follow the cut tracks."""
        groups: dict[tuple[str, int], list[Track]] = {}
        for track in self.tracks:
            groups.setdefault((track.net, track.layer), []).append(track)
        self.tracks = [piece for group in groups.values() for piece in _split_group(group)]

    def has_escaped(self, pad: Pad) -> bool:
        return (pad.name, pad.rect) in self._stubs

    def fan_out(self, net: str, pad: Pad, plane_here: Callable[[float, float], bool], wide: bool = False) -> bool:
        """Short track from a surface pad to a new via into the net's plane, or to copper that has one. Each
        fan-out is a branch of the plane net, so a rip-up can take it off and fan the pad out again."""
        connected = self._plane_tree.setdefault(net, set())
        pad_nodes = self.pad_nodes(pad)
        if pad_nodes & connected:   # on copper that has its via already: a branch without copper
            self._add_plane_branch(net, _Branch(pad, pad_nodes, [], [], None), sorted(pad_nodes & connected)[:1])
            return True
        net_id = self._net_id(net)
        via_cells = self._via_cells

        def reaches_plane(node: tuple[int, int]) -> bool:
            return node in connected

        def via_fits(index: int) -> bool:
            return via_cells[index] in (_FREE, net_id) and plane_here(*self._xy(index))

        path = self._search(net, pad_nodes, reaches_plane, lambda *_: 0, wide, vias_allowed=False,
                            via_fits=via_fits)
        if path is None:
            return False
        ends_on_new_via = path[-1][0] < 0
        if ends_on_new_via:
            path.pop()
        tracks, vias = self._commit(net, path, wide)
        last_layer, last_column, last_row = path[-1]
        if ends_on_new_via:
            vias = vias + [self._commit_via(net, last_row * self._columns + last_column)]
        self._add_plane_branch(net, _Branch(pad, pad_nodes | set(self._indexed(path)), tracks, vias, None),
                               self._indexed(path[-1:]))
        return True

    def _add_plane_branch(self, net: str, branch: _Branch, end: list[tuple[int, int]]) -> None:
        """Files a fan-out under the branch whose copper it ends on (None: a hand-placed via or a new via)."""
        branches = self._branches.setdefault(net, {})
        branch.parent = next((key for key, other in branches.items() if other.nodes.intersection(end)), None)
        self._plane_tree[net].update(branch.nodes)
        self._branch_count += 1
        branches[self._branch_count] = branch

    def _search(self, net: str, sources: Iterable[tuple[int, int]], is_target: Callable[[tuple[int, int]], bool],
                remaining: Callable[[int, int, int], int], wide: bool, vias_allowed: bool,
                via_fits: Callable[[int], bool] | None = None, crossing: bool = False,
                limit: int | None = None, greed: tuple[int, int] = _GREED) -> list[Node] | None:
        """A* over (layer, node, heading). With `via_fits`, a node where a via fits is also a target,
        at the price of one via; the returned path then ends with a marker node on layer -1. With `crossing`,
        nodes closed only by copper that is not fixed are open at _CROSSING_COST each (see `blockers`)."""
        net_id = self._net_id(net)
        columns = self._columns
        node_count = columns * self._rows
        cells_by_layer = self._track_cells
        via_cells = self._via_cells
        history = self._history
        step_factors = self._step_factors.get(net, self._default_step_factors)
        fixed_tracks, fixed_vias = self._fixed_cells if crossing else (cells_by_layer, via_cells)
        offsets = [dy * columns + dx for dx, dy in _STEPS]
        open_to_net = (_FREE, net_id)
        neighbours = offsets if wide else []

        greed_numerator, greed_denominator = greed

        def greedy(estimate: int) -> int:
            return estimate * greed_numerator // greed_denominator

        best: dict[int, int] = {}
        parent: dict[int, int] = {}
        queue: list[tuple[int, int, int]] = []
        for layer, index in sorted(sources):
            state = (layer * node_count + index) * _HEADINGS + _NO_HEADING
            start_cost = self._cost_from_pad_centre(layer, index)
            best[state] = start_cost
            row, column = divmod(index, columns)
            queue.append((start_cost + greedy(remaining(layer, column, row)), start_cost, state))
        heapq.heapify(queue)
        via_marker_base = len(self._layers) * node_count * _HEADINGS
        layers = self._layers

        expansions = 0
        while queue:
            _, cost, state = heapq.heappop(queue)
            if state >= via_marker_base:
                return self._trace_back(parent, parent[state]) + [(-1, 0, 0)]
            if cost > best[state]:
                continue
            located, heading = divmod(state, _HEADINGS)
            layer, index = divmod(located, node_count)
            if is_target((layer, index)):
                return self._trace_back(parent, state)
            expansions += 1
            if expansions > (limit or self.rules.search_limit):
                return None
            cells = cells_by_layer[layer]
            fixed = fixed_tracks[layer]
            layer_factor = step_factors[layer]
            node_history = history[layer]
            for direction in range(8):
                if heading == _NO_HEADING:
                    turn_cost = 0
                else:
                    turn = (direction - heading) % 8
                    turn = min(turn, 8 - turn)
                    if turn > 2:
                        continue
                    turn_cost = _TURN_COST[turn]
                next_index = index + offsets[direction]
                crossing_cost = 0
                if cells[next_index] not in open_to_net or (
                        wide and any(cells[next_index + offset] not in open_to_net for offset in neighbours)):
                    if fixed[next_index] not in open_to_net or (
                            wide and any(fixed[next_index + offset] not in open_to_net for offset in neighbours)):
                        continue
                    crossing_cost = _CROSSING_COST
                step_cost = _DIAGONAL_COST if direction % 2 else _STRAIGHT_COST
                step_cost *= layer_factor
                next_cost = cost + step_cost + turn_cost + crossing_cost + node_history[next_index]
                next_state = (layer * node_count + next_index) * _HEADINGS + direction
                if next_cost < best.get(next_state, 1 << 60):
                    best[next_state] = next_cost
                    parent[next_state] = state
                    row, column = divmod(next_index, columns)
                    heapq.heappush(queue, (next_cost + greedy(remaining(layer, column, row)), next_cost, next_state))
            if via_fits is not None and via_fits(index):
                marker = via_marker_base + index
                if cost + _OWN_VIA_COST < best.get(marker, 1 << 60):
                    best[marker] = cost + _OWN_VIA_COST
                    parent[marker] = state
                    heapq.heappush(queue, (cost + _OWN_VIA_COST, cost + _OWN_VIA_COST, marker))
            if not vias_allowed or fixed_vias[index] not in open_to_net:
                continue
            via_crowded = via_cells[index] not in open_to_net
            for other in layers:
                if other == layer or fixed_tracks[other][index] not in open_to_net:
                    continue
                crowded = via_crowded or cells_by_layer[other][index] not in open_to_net
                if crowded and not crossing:
                    continue
                next_state = (other * node_count + index) * _HEADINGS + _NO_HEADING
                next_cost = cost + _VIA_COST + (_CROSSING_COST if crowded else 0)
                if next_cost < best.get(next_state, 1 << 60):
                    best[next_state] = next_cost
                    parent[next_state] = state
                    row, column = divmod(index, columns)
                    heapq.heappush(queue, (next_cost + greedy(remaining(other, column, row)), next_cost, next_state))
        return None

    def _cost_from_pad_centre(self, layer: int, index: int) -> int:
        """Start cost of a source node on a pad, so that a path leaves the pad as if from its centre."""
        centre = self._pad_centre.get((layer, index))
        if centre is None:
            return 0
        return round(_STRAIGHT_COST * math.dist(self._xy(index), centre) / self._pitch)

    def _trace_back(self, parent: dict[int, int], state: int) -> list[Node]:
        node_count = self._columns * self._rows
        path = []
        while True:
            layer, index = divmod(state // _HEADINGS, node_count)
            row, column = divmod(index, self._columns)
            path.append((layer, column, row))
            if state not in parent:
                break
            state = parent[state]
        path.reverse()
        return path

    def lengthen(self, net: str, extra: float, tolerance: float) -> bool:
        """Adds about `extra` mm (within `tolerance`) to the net by turning one straight track into a meander, for
        length matching. Tries the net's longest straight tracks first, the meander on either side, and writes
        it only where every node it passes is open to the net. Returns False when no track has room."""
        net_id = self._net_id(net)
        open_to_net = (_FREE, net_id)
        for track in sorted((t for t in self.tracks if t.net == net), key=lambda t: -t.length):
            for points in _meanders(track, extra, tolerance, self._pitch):
                nodes = [self._index_at(x, y) for x, y in _walk(points, self._pitch)]
                if all(self._track_cells[track.layer][index] in open_to_net for index in nodes):
                    self._replace_track(track, [Track(net, track.layer, a, b, track.width)
                                                for a, b in zip(points, points[1:])])
                    return True
        return False

    def _replace_track(self, old: Track, new: list[Track]) -> None:
        """Swaps one track for others that join the same ends, in the copper list and in the branch that owns it."""
        if id(old) in self._fixed_items:
            self._fixed_items.discard(id(old))
            self._fixed_items.update(id(item) for item in new)
        self.tracks = [item for item in self.tracks if item is not old]
        for branches in self._branches.values():
            for branch in branches.values():
                if any(item is old for item in branch.tracks):
                    branch.tracks = [item for item in branch.tracks if item is not old] + new
        self._write(new, [])

    # --- writing copper -----------------------------------------------------------------------

    def _commit(self, net: str, path: list[Node], wide: bool) -> tuple[list[Track], list[Via]]:
        """Adds the path's copper to the board and closes the nodes around it to other nets."""
        tracks, vias = self._copper(net, path, wide)
        self._write(tracks, vias)
        return tracks, vias

    def _write(self, tracks: list[Track], vias: list[Via]) -> None:
        for track in tracks:
            self._claim_track(track)
        for via in vias:
            self._claim_via(via)
        self.tracks += tracks
        self.vias += vias

    def _copper(self, net: str, path: list[Node], wide: bool) -> tuple[list[Track], list[Via]]:
        """The tracks and vias that draw a path."""
        width = self.rules.wide_track_width if wide else self.rules.track_width
        corners = self._corners(path)
        tracks, vias = [], []
        for (layer, start), (next_layer, end) in zip(corners, corners[1:]):
            if layer != next_layer:
                vias.append(Via(net, *start))
            elif start != end:
                tracks.append(Track(net, layer, start, end, width))
        return tracks, vias

    def _corners(self, path: list[Node]) -> list[tuple[int, tuple[float, float]]]:
        """The path as corner points, with a stub to the pad centre at each end that sits on a pad."""
        points = [(layer, (round(column * self._pitch, 4), round(row * self._pitch, 4)))
                  for layer, column, row in path]
        first_layer, first_column, first_row = path[0]
        last_layer, last_column, last_row = path[-1]
        first_centre = self._pad_centre.get((first_layer, first_row * self._columns + first_column))
        last_centre = self._pad_centre.get((last_layer, last_row * self._columns + last_column))
        if first_centre is not None and first_centre != points[0][1]:
            points.insert(0, (first_layer, first_centre))
        if last_centre is not None and last_centre != points[-1][1]:
            points.append((last_layer, last_centre))
        corners = [points[0]]
        for previous, current, following in zip(points, points[1:], points[2:]):
            same_layer = previous[0] == current[0] == following[0]
            if not (same_layer and _collinear(previous[1], current[1], following[1])):
                corners.append(current)
        if len(points) > 1:
            corners.append(points[-1])
        return corners

    def _commit_via(self, net: str, index: int) -> Via:
        via = Via(net, *self._xy(index))
        self._write([], [via])
        return via

    def _is_fixed(self, item: Track | Via) -> bool:
        return self._net_id(item.net) in self._fixed_ids or id(item) in self._fixed_items

    def _copper_cells(self, item: Track | Via) -> list[tuple[list[array], array]]:
        """The cell sets a piece of copper claims: always the live ones, and the fixed ones for fixed copper."""
        if self._fixed_cells is not None and self._is_fixed(item):
            return [(self._track_cells, self._via_cells), self._fixed_cells]
        return [(self._track_cells, self._via_cells)]

    def _claim_track(self, track: Track) -> None:
        owner = self._net_id(track.net)
        half_width = track.width / 2
        for track_cells, via_cells in self._copper_cells(track):
            self._claim_segment(track_cells[track.layer], track.start, track.end, half_width + self._track_reach,
                                owner)
            self._claim_segment(via_cells, track.start, track.end, half_width + self._via_reach, owner)

    def _claim_via(self, via: Via) -> None:
        owner = self._net_id(via.net)
        spot = (via.x, via.y, via.x, via.y)
        for track_cells, via_cells in self._copper_cells(via):
            for layer in self._layers:
                self._claim_rect(track_cells[layer], spot, self._via_radius + self._track_reach, owner)
            self._claim_rect(via_cells, spot, self._via_radius + self._via_reach, owner)
            self._claim_rect(via_cells, spot, self.rules.via_diameter + self.rules.via_to_via_gap, _CLOSED)


def _claim(cells: array, index: int, owner: int) -> None:
    current = cells[index]
    if current == _FREE:
        cells[index] = owner
    elif current != owner:
        cells[index] = _CLOSED


def _inside_columns(sides: list, y: float, pitch: float, columns: int) -> list[bool]:
    """Even-odd scanline of a polygon along one grid row: which columns lie inside."""
    crossings = sorted(x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                       for (x1, y1), (x2, y2) in sides if (y1 <= y < y2) or (y2 <= y < y1))
    inside = [False] * columns
    for left, right in zip(crossings[::2], crossings[1::2], strict=True):
        for column in range(max(0, math.ceil(left / pitch)), min(columns - 1, math.floor(right / pitch)) + 1):
            inside[column] = True
    return inside


def _copied(trees: dict[str, set[tuple[int, int]]]) -> dict[str, set[tuple[int, int]]]:
    return {net: set(nodes) for net, nodes in trees.items()}


_TOUCH = 1e-6   # mm: two points closer than this are one point


def _pruned(tracks: list[Track], vias: list[Via], pads: list[Pad]) -> tuple[list[Track], list[Via]]:
    """One net's copper without dangling track ends and without vias that join fewer than two layers."""
    tracks, vias = list(tracks), list(vias)
    changed = True
    while changed:
        changed = False
        for index, track in enumerate(tracks):
            others = tracks[:index] + tracks[index + 1:]
            start_touches = _touches(track.start, track.layer, others, vias, pads)
            end_touches = _touches(track.end, track.layer, others, vias, pads)
            if start_touches and end_touches:
                continue
            kept = _cut_back(track, others, vias, pads) if start_touches or end_touches else None
            tracks = others + ([kept] if kept else [])
            changed = True
            break
        layers_at = {id(via): {track.layer for track in tracks if _point_gap((via.x, via.y), track) < _TOUCH}
                     | {layer for pad in pads if _inside(pad.rect, (via.x, via.y)) for layer in pad.layers}
                     for via in vias}
        joining = [via for via in vias if len(layers_at[id(via)]) >= 2]
        changed = changed or len(joining) != len(vias)
        vias = joining
    return tracks, vias


def _touches(point: tuple[float, float], layer: int, tracks: list[Track], vias: list[Via], pads: list[Pad]) -> bool:
    return (any(track.layer == layer and _point_gap(point, track) < _TOUCH for track in tracks)
            or any(math.dist(point, (via.x, via.y)) < _TOUCH for via in vias)
            or any(layer in pad.layers and _inside(pad.rect, point) for pad in pads))


def _cut_back(track: Track, others: list[Track], vias: list[Via], pads: list[Pad]) -> Track | None:
    """The track from its end that touches other copper to the farthest point along it that also touches, or
    None when no such point lies beyond that end."""
    start, end = track.start, track.end
    if not _touches(start, track.layer, others, vias, pads):
        start, end = end, start
    span_x, span_y = end[0] - start[0], end[1] - start[1]
    span_squared = span_x * span_x + span_y * span_y

    def along(point: tuple[float, float]) -> float:
        return ((point[0] - start[0]) * span_x + (point[1] - start[1]) * span_y) / span_squared

    def on_track(point: tuple[float, float]) -> bool:
        return _point_gap(point, track) < _TOUCH

    stops = [along(point) for other in others if other.layer == track.layer
             for point in (other.start, other.end) if on_track(point)]
    stops += [along((via.x, via.y)) for via in vias if on_track((via.x, via.y))]
    stops += [_last_inside(pad.rect, start, end) for pad in pads if track.layer in pad.layers]
    farthest = max([stop for stop in stops if stop is not None] + [0.0])
    if farthest < _TOUCH:
        return None
    cut = (round(start[0] + span_x * farthest, 4), round(start[1] + span_y * farthest, 4))
    return Track(track.net, track.layer, start, cut, track.width)


def _split_group(tracks: list[Track]) -> list[Track]:
    """One net's tracks on one layer, each cut at every end of another that lies on its middle."""
    ends = {point for track in tracks for point in (track.start, track.end)}
    pieces = []
    for track in tracks:
        cuts = sorted((math.dist(track.start, point), point) for point in ends
                      if _point_gap(point, track) < _TOUCH and math.dist(point, track.start) > _TOUCH
                      and math.dist(point, track.end) > _TOUCH)
        corners = [track.start] + [point for _, point in cuts] + [track.end]
        pieces += [Track(track.net, track.layer, a, b, track.width) for a, b in zip(corners, corners[1:])]
    return pieces


def _inside(rect: Rect, point: tuple[float, float]) -> bool:
    left, top, right, bottom = rect
    return left - _TOUCH <= point[0] <= right + _TOUCH and top - _TOUCH <= point[1] <= bottom + _TOUCH


def _last_inside(rect: Rect, start: tuple[float, float], end: tuple[float, float]) -> float | None:
    """The largest fraction t of the way from start to end at which the point still lies in the rectangle."""
    low, high = 0.0, 1.0
    for axis in (0, 1):
        span = end[axis] - start[axis]
        near, far = rect[axis] - _TOUCH, rect[axis + 2] + _TOUCH
        if abs(span) < 1e-12:
            if not near <= start[axis] <= far:
                return None
            continue
        first, second = (near - start[axis]) / span, (far - start[axis]) / span
        low, high = max(low, min(first, second)), min(high, max(first, second))
    return high if low <= high else None


def _point_gap(point: tuple[float, float], track: Track) -> float:
    """Distance from a point to a track's centre line."""
    (x1, y1), (x2, y2) = track.start, track.end
    span_x, span_y = x2 - x1, y2 - y1
    span_squared = span_x * span_x + span_y * span_y
    along = 0.0 if span_squared == 0 else max(
        0.0, min(1.0, ((point[0] - x1) * span_x + (point[1] - y1) * span_y) / span_squared))
    return math.dist(point, (x1 + along * span_x, y1 + along * span_y))


def _segment_gap(first: Track, second: Track) -> float:
    """Distance between two tracks' centre lines; zero when they cross."""
    if _segments_cross(first.start, first.end, second.start, second.end):
        return 0.0
    return min(_point_gap(first.start, second), _point_gap(first.end, second),
               _point_gap(second.start, first), _point_gap(second.end, first))


def _segments_cross(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float],
                    d: tuple[float, float]) -> bool:
    def side(p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> float:
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    return side(a, b, c) * side(a, b, d) < 0 and side(c, d, a) * side(c, d, b) < 0


def _collinear(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> bool:
    return abs((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])) < 1e-9


# Meanders (Router.lengthen): legs this many grid steps apart, at least this many steps of plain track at each end.
_MEANDER_HALF_PERIOD = 3
_MEANDER_MARGIN = 3
_MEANDER_AMPLITUDES = range(2, 12)   # grid steps


def _meanders(track: Track, extra: float, tolerance: float, pitch: float) -> Iterable[list[tuple[float, float]]]:
    """Corner lists of meanders that replace a straight, on-grid track and add `extra` mm within `tolerance`:
    smallest amplitude first, each on both sides of the track. Nothing for a track that is not straight on the grid
    along an axis or a diagonal."""
    (x1, y1), (x2, y2) = track.start, track.end
    on_grid = all(abs(value / pitch - round(value / pitch)) < 1e-6 for value in (x1, y1, x2, y2))
    dx, dy = round((x2 - x1) / pitch), round((y2 - y1) / pitch)
    if not on_grid or not (dx == 0 or dy == 0 or abs(dx) == abs(dy)) or (dx, dy) == (0, 0):
        return
    sx, sy = (dx > 0) - (dx < 0), (dy > 0) - (dy < 0)
    step_length = pitch * math.hypot(sx, sy)
    steps = max(abs(dx), abs(dy))
    half = _MEANDER_HALF_PERIOD
    for amplitude in _MEANDER_AMPLITUDES:
        bump = 2 * amplitude * step_length
        count = round(extra / bump)
        if count < 1 or abs(count * bump - extra) > tolerance or 2 * half * count + 2 * _MEANDER_MARGIN > steps:
            continue
        first = (steps - 2 * half * count) // 2
        for side in (1, -1):
            nx, ny = -sy * side, sx * side

            def at(along: int, across: int) -> tuple[float, float]:
                return (round(x1 + (along * sx + across * nx) * pitch, 4),
                        round(y1 + (along * sy + across * ny) * pitch, 4))

            points = [track.start, at(first, 0)]
            for k in range(count):
                base = first + 2 * half * k
                points += [at(base, amplitude), at(base + half, amplitude), at(base + half, 0),
                           at(base + 2 * half, 0)]
            points.append(track.end)
            yield [p for p, q in zip(points, points[1:] + [None]) if p != q]


def _walk(points: list[tuple[float, float]], pitch: float) -> Iterable[tuple[float, float]]:
    """Every grid point along a polyline of on-grid axis and diagonal segments."""
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        steps = max(round(abs(x2 - x1) / pitch), round(abs(y2 - y1) / pitch))
        for k in range(steps + 1):
            yield x1 + (x2 - x1) * k / steps, y1 + (y2 - y1) * k / steps
