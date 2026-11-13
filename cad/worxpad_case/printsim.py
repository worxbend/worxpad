"""A layer-by-layer look at how a part prints without supports.

The part is cut into the layers a slicer would make. Each layer may only rest on the layer below,
a little past its edge, or bridge in a straight line between two places that do rest. Whatever is
left hangs from one side: a cantilever. This tells a bridge from a cantilever, which an overhang
test on single faces cannot do.

Copied from the macropad case (same owner). Changed here:
- Slicer support zones. A part printed with supports names the plan areas where the slicer builds them; a
  hanging cell over such an area is carried.
- Short ledges. A hanging cell within SHORT_REACH of a carried cell in its own layer hangs from that cell as a
  short cantilever, even when a straight run through it would also end on anchors. Without this a 1 mm ledge
  along a 30 mm wall counted as a 30 mm bridge. Cells farther out still need a bridge or count as cantilever.
"""

from dataclasses import dataclass

import numpy as np
from scipy.ndimage import distance_transform_edt, minimum_filter

from .raster import crossings, rasterise

LAYER = 0.2  # mm, layer height
CELL = 0.1  # mm, grid across a layer
# A layer may reach this many cells past the layer below: 0.3 mm per 0.2 mm layer, about 56 degrees
# from vertical. The design's 45 degree faces need two cells; the third absorbs the grid's rounding.
SUPPORT_REACH = 3
# Where in a layer its material is sampled, as a share of the layer height. Not one half: the model's
# horizontal faces lie on round heights, and a sample exactly on a face would be noise.
LAYER_SAMPLE = 0.37
SOUND_ANCHOR = 1.0  # mm; a bridge may start on a ledge no deeper than this
MARGIN = 4  # empty cells around the part
# Cells; keeps cell centres off the model's edges, which lie on round numbers, and off the diagonals
# of its square faces, which a single shift for both axes would leave on the centres.
GRID_SHIFT = (0.0137, 0.0291)
SHORT_REACH = 1.5  # mm; the cantilever limit of the checks (macropad, a guess: about three 0.45 mm lines)
MAX_BROKEN_COLUMNS = 1e-4  # share of grid columns the voxel count may get wrong before it is an error


@dataclass(frozen=True)
class PrintReport:
    longest_bridge: float  # mm
    deepest_cantilever: float  # mm, measured from the nearest place that is carried
    bridge_at: tuple[float, float, float]  # where the worst of each was found, in bed coordinates
    cantilever_at: tuple[float, float, float]


def layers_of(triangles: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The part as (layer, row, column) cells that hold material, and the bed coordinates of cell 0.

    `triangles` is (n, 3, 3) and must be a closed surface. A cell holds material when an odd number
    of surface crossings lie below its centre.
    """
    low = triangles.reshape(-1, 3).min(axis=0)
    high = triangles.reshape(-1, 3).max(axis=0)
    origin = np.array((low[0] - MARGIN * CELL, low[1] - MARGIN * CELL, low[2]))
    columns, rows = (np.ceil((high[:2] - origin[:2]) / CELL).astype(int) + MARGIN)
    count = int(np.ceil((high[2] - low[2]) / LAYER))
    cells = (triangles[..., :2] - origin[:2]) / CELL + GRID_SHIFT
    pixel, height = crossings(cells, triangles[..., 2], (int(columns), int(rows)))
    # Layer k is sampled at (k + LAYER_SAMPLE) * LAYER above the bed; a crossing counts for every sample above it.
    first_above = np.clip(np.ceil((height - origin[2]) / LAYER - LAYER_SAMPLE).astype(np.int64), 0, count)
    per_layer = rows * columns
    events = np.bincount(first_above * per_layer + pixel, minlength=(count + 1) * per_layer)
    events = (events & 1).astype(np.int8).reshape(count + 1, per_layer)
    broken = events.sum(axis=0) & 1 == 1  # a closed surface is crossed an even number of times
    if broken.mean() > MAX_BROKEN_COLUMNS:
        raise ValueError(f"{broken.mean():.2%} of the grid columns cross the surface an odd number of times")
    solid = np.bitwise_xor.accumulate(events[:count], axis=0).astype(bool)
    solid[:, broken] = False
    return solid.reshape(count, rows, columns), origin


def simulate(triangles: np.ndarray, support_triangles: np.ndarray | None = None) -> PrintReport:
    """Print the part layer by layer on a flat bed at its lowest Z.

    `support_triangles` (n, 3, 3), in the same bed pose, outline the plan areas where the slicer builds
    supports: every hanging cell inside their footprint is carried.

    Every cell gets an overhang depth: 0 when it is carried, else how far it hangs out, plus the depth
    of what it hangs from. A short ledge therefore still carries the wall above it, and that wall keeps
    the ledge's depth, while a slope that is too flat gets deeper with every layer.
    """
    solid, origin = layers_of(triangles)
    supported = _footprint(support_triangles, origin, solid.shape[1:]) if support_triangles is not None else None
    reach = _disc(SUPPORT_REACH)
    depth = np.where(solid[0], 0.0, np.inf)  # the bed carries the whole first layer
    worst_bridge, worst_cantilever = (0.0, (0, 0, 0)), (0.0, (0, 0, 0))
    for number in range(1, len(solid)):
        layer = solid[number]
        if not (layer & (depth != 0)).any():  # every cell stands on a carried cell
            depth = np.where(layer, 0.0, np.inf)
            continue
        inherited = minimum_filter(depth, footprint=reach, mode="constant", cval=np.inf)
        based = layer & np.isfinite(inherited)
        if supported is not None:
            inherited = np.where(supported, 0.0, inherited)
            based = layer & (np.isfinite(inherited) | supported)
        hanging = layer & ~based
        anchors = based & (inherited <= SOUND_ANCHOR)
        span = np.minimum(_bridge_span(hanging, anchors), _bridge_span(hanging.T, anchors.T).T)
        near = hanging & (distance_transform_edt(~based) * CELL <= SHORT_REACH) if based.any() else hanging & False
        bridged = hanging & ~near & np.isfinite(span)
        worst_bridge = max(worst_bridge, _largest(np.where(bridged, span, 0.0), number))
        depth = np.where(based, inherited, np.inf)
        depth[bridged] = 0.0
        cantilever = hanging & ~bridged
        if cantilever.any():
            distance, (row, column) = distance_transform_edt(~(based | bridged), return_indices=True)
            depth[cantilever] = (distance * CELL + depth[row, column])[cantilever]
        worst_cantilever = max(worst_cantilever, _largest(np.where(layer, depth, 0.0), number))
    return PrintReport(
        worst_bridge[0], worst_cantilever[0], _bed_position(worst_bridge[1], origin),
        _bed_position(worst_cantilever[1], origin),
    )


def _footprint(triangles: np.ndarray, origin: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    """Cells of the layer grid that lie under any of the triangles, seen from above."""
    cells = (triangles[..., :2] - origin[:2]) / CELL + GRID_SHIFT
    rows, columns = shape
    nearest, _, _ = rasterise(cells, triangles[..., 2], (int(columns), int(rows)), cull_back_faces=False)
    return nearest >= 0


def _disc(radius: int) -> np.ndarray:
    across = np.arange(-radius, radius + 1)
    return across[:, None] ** 2 + across[None, :] ** 2 <= radius ** 2


def _bridge_span(hanging: np.ndarray, anchors: np.ndarray) -> np.ndarray:
    """For each hanging cell, the length in mm of the straight run of hanging cells through it along
    a row, if that run ends on an anchor at both ends; infinite otherwise."""
    columns = hanging.shape[1]
    index = np.arange(columns)[None, :]
    before = np.maximum.accumulate(np.where(hanging, -1, index), axis=1)
    after = np.minimum.accumulate(np.where(hanging, columns, index)[:, ::-1], axis=1)[:, ::-1]
    starts_anchored = np.take_along_axis(anchors, np.clip(before, 0, columns - 1), axis=1) & (before >= 0)
    ends_anchored = np.take_along_axis(anchors, np.clip(after, 0, columns - 1), axis=1) & (after < columns)
    return np.where(hanging & starts_anchored & ends_anchored, (after - before - 1) * CELL, np.inf)


def _largest(values: np.ndarray, layer: int) -> tuple[float, tuple[int, int, int]]:
    row, column = np.unravel_index(values.argmax(), values.shape)
    return float(values[row, column]), (int(column), int(row), layer)


def _bed_position(cell: tuple[int, int, int], origin: np.ndarray) -> tuple[float, float, float]:
    column, row, layer = cell
    position = origin + ((column + 0.5) * CELL, (row + 0.5) * CELL, (layer + LAYER_SAMPLE) * LAYER)
    return tuple(round(float(value), 1) for value in position)
