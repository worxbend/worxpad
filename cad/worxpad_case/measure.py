"""Checks that measure the finished solids instead of trusting how they were built.

Each function returns a number or rows of `{"name", "value", "limit", "kind", "unit", "ok"}`; `kind` says
whether the limit is a minimum or a maximum. `row`, `thinnest_wall`, `soundness_faults`,
`sharp_internal_corners`, `unreachable_area` and `uncut_area` are copied from the macropad case (same owner);
the concave-radius rule, the ray probes and the bed checks are new here.
"""

from math import cos, pi, sin  # noqa: F401 (cos, sin used by the copied corner probe)

import numpy as np
import trimesh
from build123d import GeomType, Part, Vector
from OCP.BRepTools import BRepTools
from scipy.ndimage import binary_dilation, binary_opening, grey_closing

from .raster import DEPTH_MAP_SIZE, Material, mesh_of, rasterise
from .spec import CASE

WALL_SAMPLES = 3000  # surface points probed per part
WALL_MESH_TOLERANCE = 0.1
FACING_COSINE = -0.9  # two faces count as one wall when they are within about 25 degrees of parallel
RAYS_PER_BATCH = 200
RAY_START = 1e-4  # mm below the surface, so a ray does not hit the face it starts on
PROBE = 0.02  # mm; how far from an edge the corner probes sit
PROBES_PER_EDGE = 8
REACH_STEP = 0.25  # mm; how far off a face the tool-access probe sits
REACH_TOLERANCE = 0.05
UNDERCUT_NOISE = 5.0  # mm^2; slivers along edges that the height map cannot resolve
TOOL_CELL = 0.1  # mm; grid of the height map the tool is run over
TOOL_GRID_SLACK = 1  # cells taken off the tool radius, so a pocket corner of exactly that radius passes
UNCUT_HEIGHT = 0.1  # mm of material left standing before a cell counts as not cut
UNCUT_NOISE = 0.3  # mm^2; one sharp corner in a 3 mm pocket already leaves 0.48
SLOPED = (0.05, 0.995)  # |normal Z| of a face a flat end mill does not cut: chamfers and tapers
ANY_MATERIAL = Material((0.5, 0.5, 0.5))
HALF_TURN = pi - 0.02  # an arc this wide or wider is a drilled hole (full or cut in half by a slot), not a corner
FLOOR_FACING = -0.85  # faces whose normal points this far down are floors seen from below (ramp, slope, scoops)
FLOOR_SAMPLES = 6000


def row(name: str, value: float, limit: float, kind: str = "min", unit: str = "mm") -> dict:
    ok = value >= limit - 1e-6 if kind == "min" else value <= limit + 1e-6
    return {"name": name, "value": round(float(value), 3), "limit": limit, "kind": kind, "unit": unit, "ok": bool(ok)}


def thinnest_wall(part: Part) -> float:
    """Smallest distance through the material between two roughly parallel faces, from `WALL_SAMPLES`
    surface points chosen by area with a fixed seed. A sample can miss a very small thin spot."""
    vertices, triangles = part.tessellate(WALL_MESH_TOLERANCE, 0.3)
    mesh = trimesh.Trimesh([tuple(vertex) for vertex in vertices], triangles, process=False)
    points, source = trimesh.sample.sample_surface(mesh, WALL_SAMPLES, seed=0)
    inward = -mesh.face_normals[source]
    thinnest = np.inf
    for start in range(0, len(points), RAYS_PER_BATCH):
        chosen = slice(start, start + RAYS_PER_BATCH)
        distance, struck = _first_hit(points[chosen] + inward[chosen] * RAY_START, inward[chosen], mesh.triangles)
        found = np.isfinite(distance)
        facing = (mesh.face_normals[struck] * inward[chosen]).sum(axis=1) > -FACING_COSINE
        thinnest = min(thinnest, distance[found & facing].min(initial=np.inf) + RAY_START)
    return float(thinnest)


def _first_hit(origins: np.ndarray, directions: np.ndarray, triangles: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Moller-Trumbore for every ray against every triangle: distance to the first hit and its triangle."""
    corner = triangles[None, :, 0]
    edge_1 = triangles[None, :, 1] - corner
    edge_2 = triangles[None, :, 2] - corner
    ray = directions[:, None, :]
    p_vector = np.cross(ray, edge_2)
    determinant = (edge_1 * p_vector).sum(axis=2)
    with np.errstate(divide="ignore", invalid="ignore"):
        inverse = 1.0 / determinant
        t_vector = origins[:, None, :] - corner
        u = (t_vector * p_vector).sum(axis=2) * inverse
        q_vector = np.cross(t_vector, edge_1)
        v = (ray * q_vector).sum(axis=2) * inverse
        distance = (edge_2 * q_vector).sum(axis=2) * inverse
        hit = (np.abs(determinant) > 1e-12) & (u >= 0) & (v >= 0) & (u + v <= 1) & (distance > 1e-3)
    distance = np.where(hit, distance, np.inf)
    nearest = distance.argmin(axis=1)
    return distance[np.arange(len(origins)), nearest], nearest


def soundness_faults(part: Part) -> int:
    """How many things are wrong with a part as one body: every solid besides the one expected,
    an invalid shape, no volume. A boolean that went wrong shows up as one of these."""
    return abs(len(part.solids()) - 1) + (not part.is_valid) + (part.volume <= 0)


def sharp_internal_corners(part: Part) -> int:
    """Vertical edges where two pocket walls meet without a radius: a round tool cannot cut them.
    Probe points on a small circle around each vertical edge; in an internal corner most are in material."""
    sharp = 0
    for edge in part.edges().filter_by(GeomType.LINE):
        start, end = edge.position_at(0), edge.position_at(1)
        if edge.length < 0.05 or abs(start.X - end.X) > 1e-6 or abs(start.Y - end.Y) > 1e-6:
            continue
        middle = edge.position_at(0.5)
        in_material = sum(
            part.is_inside(middle + Vector(PROBE * cos(angle), PROBE * sin(angle), 0))
            for angle in (2 * pi * (step + 0.5) / PROBES_PER_EDGE for step in range(PROBES_PER_EDGE))
        )
        sharp += in_material > PROBES_PER_EDGE * 0.6
    return sharp


def _is_full_turn(face) -> bool:
    """The face runs the whole way round its axis (a hole), whatever its ends look like."""
    u_min, u_max, _, _ = BRepTools.UVBounds_s(face.wrapped)
    return u_max - u_min > 2 * pi - 1e-6


def face_radius(face) -> float:
    """Radius of a vertical cylinder face, from its axis; build123d leaves `radius` empty on some trimmed faces."""
    axis = face.axis_of_rotation
    on_face = face.position_at(0.5, 0.5)
    return Vector(on_face.X - axis.position.X, on_face.Y - axis.position.Y, 0).length


def unreachable_area(part: Part, skip: list[tuple[float, float, float]] = (),
                     only: list[tuple[float, float, float]] | None = None) -> float:
    """Area in mm^2 that a tool coming straight down or straight up cannot see: an undercut.
    A point just off each face is tested against the height of the material above and below it."""
    mesh = mesh_of(part, ANY_MATERIAL)
    triangles = mesh.triangles
    flat_normal = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    area = np.linalg.norm(flat_normal, axis=1) / 2
    keep = area > 1e-12  # sliver triangles have no normal
    triangles, flat_normal, area = triangles[keep], flat_normal[keep], area[keep]
    probe = triangles.mean(axis=1) + flat_normal / (2 * area[:, None]) * REACH_STEP
    low = triangles.reshape(-1, 3).min(axis=0)[:2] - 1.0
    cells_per_mm = (DEPTH_MAP_SIZE - 1) / (triangles.reshape(-1, 3).max(axis=0)[:2] + 1.0 - low).max()
    size = (DEPTH_MAP_SIZE, DEPTH_MAP_SIZE)
    cells = (triangles[..., :2] - low) * cells_per_mm
    _, _, top_height = rasterise(cells, triangles[..., 2], size, cull_back_faces=False)
    _, _, bottom_depth = rasterise(cells, -triangles[..., 2], size, cull_back_faces=False)
    column, row_number = np.clip(np.rint((probe[:, :2] - low) * cells_per_mm).astype(int), 0, DEPTH_MAP_SIZE - 1).T
    open_above = top_height[row_number, column] <= probe[:, 2] + REACH_TOLERANCE
    open_below = -bottom_depth[row_number, column] >= probe[:, 2] - REACH_TOLERANCE
    counted = np.ones(len(probe), dtype=bool)
    for x, y, radius in skip:  # features cut in another setup (model coordinates)
        counted &= (probe[:, 0] - x) ** 2 + (probe[:, 1] - y) ** 2 > radius ** 2
    if only is not None:
        wanted = np.zeros(len(probe), dtype=bool)
        for x, y, radius in only:
            wanted |= (probe[:, 0] - x) ** 2 + (probe[:, 1] - y) ** 2 <= radius ** 2
        counted &= wanted
    return float(area[~open_above & ~open_below & counted].sum())


def uncut_area(part: Part, tool_diameter: float, skip: list[tuple[float, float, float]] = (),
               only: list[tuple[float, float, float]] | None = None) -> dict[str, float]:
    """Area in mm^2 a flat end mill of `tool_diameter` cannot cut, coming straight down ("above") and
    straight up ("below"). The tool is lowered over a height map of the part: wherever it stops more
    than `UNCUT_HEIGHT` short of the surface, a corner is too tight or a slot too narrow. Sloped faces
    are left out (a chamfer mill cuts them), and so are round holes smaller than the tool (drilled)."""
    triangles = mesh_of(part, ANY_MATERIAL).triangles
    flat_normal = np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])
    steepness = np.abs(flat_normal[:, 2]) / np.maximum(np.linalg.norm(flat_normal, axis=1), 1e-12)
    is_sloped = (steepness > SLOPED[0]) & (steepness < SLOPED[1])
    border = tool_diameter / 2 + 1.0
    low = triangles.reshape(-1, 3).min(axis=0)[:2] - border
    columns, rows = np.ceil((triangles.reshape(-1, 3).max(axis=0)[:2] + border - low) / TOOL_CELL).astype(int)
    cells = (triangles[..., :2] - low) / TOOL_CELL
    radius = round(tool_diameter / 2 / TOOL_CELL) - TOOL_GRID_SLACK
    across = np.arange(-radius, radius + 1)
    tool = across[:, None] ** 2 + across[None, :] ** 2 <= radius ** 2
    drilled = _drilled_cells(part, tool_diameter, low, (rows, columns))
    row, column = np.indices((rows, columns))
    cell_x, cell_y = low[0] + (column + 0.5) * TOOL_CELL, low[1] + (row + 0.5) * TOOL_CELL
    for x, y, radius in skip:  # model coordinates of features cut in another setup
        drilled |= (cell_x - x) ** 2 + (cell_y - y) ** 2 <= radius ** 2
    if only is not None:  # count only the features this setup is for
        wanted = np.zeros((rows, columns), dtype=bool)
        for x, y, radius in only:
            wanted |= (cell_x - x) ** 2 + (cell_y - y) ** 2 <= radius ** 2
        drilled |= ~wanted
    found = {}
    for side, toward_tool in (("above", 1.0), ("below", -1.0)):
        nearest, _, height = rasterise(cells, toward_tool * triangles[..., 2], (int(columns), int(rows)), cull_back_faces=False)
        has_material = nearest >= 0
        height = np.where(has_material, height, height[has_material].min() - 1.0)  # the tool may pass beside the part
        left_standing = grey_closing(height, footprint=tool) - height > UNCUT_HEIGHT
        chamfered = binary_dilation(has_material & is_sloped[np.where(has_material, nearest, 0)], iterations=2)
        # Opening drops the lines one or two cells wide that the grid leaves along edges; a real fault is wider.
        faults = binary_opening(left_standing & ~chamfered & ~drilled, structure=np.ones((3, 3), dtype=bool))
        found[side] = float(faults.sum() * TOOL_CELL ** 2)
    return found


def _drilled_cells(part: Part, tool_diameter: float, low: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    """Cells inside vertical round holes smaller than the tool: those are drilled, not milled."""
    row, column = np.indices(shape)
    x, y = low[0] + (column + 0.5) * TOOL_CELL, low[1] + (row + 0.5) * TOOL_CELL
    drilled = np.zeros(shape, dtype=bool)
    for face in part.faces().filter_by(GeomType.CYLINDER):
        axis = face.axis_of_rotation
        if abs(axis.direction.Z) > 0.999 and face_radius(face) < tool_diameter / 2 and _is_full_turn(face):
            drilled |= (x - axis.position.X) ** 2 + (y - axis.position.Y) ** 2 <= (face_radius(face) + 2 * TOOL_CELL) ** 2
    return drilled


# ---------------------------------------------------------------------------------------------------------
# New here
# ---------------------------------------------------------------------------------------------------------
def concave_arcs(part: Part) -> list[dict]:
    """Every concave vertical arc wall that a mill cuts (not a drilled hole): radius, depth (the face height)
    and where it is, in board coordinates."""
    found = []
    for face in part.faces().filter_by(GeomType.CYLINDER):
        axis = face.axis_of_rotation
        if abs(axis.direction.Z) < 0.999:
            continue
        on_face = face.position_at(0.5, 0.5)
        toward_axis = Vector(axis.position.X - on_face.X, axis.position.Y - on_face.Y, 0)
        if toward_axis.length < 1e-9 or part.is_inside(on_face + toward_axis.normalized() * PROBE):
            continue  # material on the axis side: an outside corner
        height = face.bounding_box().size.Z
        radius = Vector(on_face.X - axis.position.X, on_face.Y - axis.position.Y, 0).length
        if height < 1e-6 or face.area / (radius * height) >= HALF_TURN:
            continue
        found.append({"radius": radius, "depth": height, "x": round(axis.position.X, 2),
                      "y": round(-axis.position.Y, 2), "z": round(face.bounding_box().min.Z, 2)})
    return found


def radius_rule(arcs: list[dict]) -> tuple[list[dict], float]:
    """Arcs that break R >= depth / 10 + 0.5 (enclosure 5), and the smallest margin over all arcs."""
    margins = [arc["radius"] - (arc["depth"] * CASE.corner_rule_slope + CASE.corner_rule_offset) for arc in arcs]
    faults = [arc for arc, margin in zip(arcs, margins) if margin < -1e-6]
    return faults, min(margins, default=float("inf"))


def table_rule(arcs: list[dict], waivers: list[dict]) -> tuple[list[dict], list[dict]]:
    """Arcs deeper than 3 mm need R 1.5 (enclosure 5 table, D29). Returns the faults and the waived arcs."""
    faults, waived = [], []
    for arc in arcs:
        if arc["depth"] <= CASE.shallow_depth + 1e-6 or arc["radius"] >= CASE.table_radius - 1e-6:
            continue
        waiver = next((w for w in waivers if _inside(arc, w["span"])), None)
        (waived if waiver else faults).append(arc | ({"waiver": waiver["reason"]} if waiver else {}))
    return faults, waived


def _inside(arc: dict, span) -> bool:
    (x0, x1), (y0, y1) = span
    return x0 <= arc["x"] <= x1 and y0 <= arc["y"] <= y1


def tool_reach(arcs: list[dict]) -> float:
    """Deepest concave arc as a multiple of the tool that cuts it (diameter 2R)."""
    return max((arc["depth"] / (2 * arc["radius"]) for arc in arcs), default=0.0)


def _mesh(part: Part) -> trimesh.Trimesh:
    vertices, triangles = part.tessellate(WALL_MESH_TOLERANCE, 0.3)
    return trimesh.Trimesh([tuple(v) for v in vertices], triangles, process=False)


def material_along(part: Part, start: tuple[float, float, float], direction: tuple[float, float, float]) -> float:
    """Length of material a ray crosses from a point inside (or on) the part until it leaves, in mm. The start
    point is in board coordinates (Y toward the front)."""
    mesh = _mesh(part)
    origin = np.array([[start[0], -start[1], start[2]]], dtype=float)
    ray = np.array([[direction[0], -direction[1], direction[2]]], dtype=float)
    ray /= np.linalg.norm(ray)
    distance, _ = _first_hit(origin + ray * RAY_START, ray, mesh.triangles)
    return float(distance[0] + RAY_START)


def thinnest_floor(part: Part) -> tuple[float, tuple[float, float]]:
    """Smallest vertical thickness above every floor face seen from below (normal pointing down): a ray
    straight up from sampled points until it leaves the material. Returns the value and where (board X, Y)."""
    mesh = _mesh(part)
    facing_down = mesh.face_normals[:, 2] < FLOOR_FACING
    sub = trimesh.Trimesh(mesh.vertices, mesh.faces[facing_down], process=False)
    points, _ = trimesh.sample.sample_surface(sub, FLOOR_SAMPLES, seed=0)
    up = np.tile([0.0, 0.0, 1.0], (len(points), 1))
    thinnest, where = np.inf, (0.0, 0.0)
    for start in range(0, len(points), RAYS_PER_BATCH):
        chosen = slice(start, start + RAYS_PER_BATCH)
        distance, struck = _first_hit(points[chosen] + up[chosen] * RAY_START, up[chosen], mesh.triangles)
        # Count only rays that leave through a face looking up; a ray from the rim of a tilted foot pocket
        # grazes the pocket's own wall, which is no floor.
        distance = np.where(mesh.face_normals[struck][:, 2] > 0.5, distance, np.inf)
        index = int(np.argmin(distance))
        if distance[index] < thinnest:
            thinnest = float(distance[index] + RAY_START)
            where = (round(float(points[chosen][index][0]), 2), round(float(-points[chosen][index][1]), 2))
    return thinnest, where


def bed_contact(posed: Part, height: float = 0.05) -> float:
    """Area in mm^2 of the faces that lie on the bed (within `height` of the lowest point, facing down)."""
    low = posed.bounding_box().min.Z
    return float(sum(face.area for face in posed.faces()
                     if face.normal_at().Z < -0.999 and face.bounding_box().max.Z <= low + height))


def largest_extent(posed: Part) -> float:
    """Largest extent of the posed part, to compare with the bed."""
    size = posed.bounding_box().size
    return float(max(size.X, size.Y, size.Z))


def inside_convex_hull(points: list[tuple[float, float]], target: tuple[float, float]) -> float:
    """Signed distance in plan from `target` to the edge of the convex hull of `points`: positive inside,
    negative outside (the most negative edge distance, which is exact inside and a lower bound outside)."""
    hull = _convex_hull(sorted(set(points)))
    if len(hull) < 3:
        raise ValueError("a support hull needs at least three points that are not on one line")
    distances = []
    for (x0, y0), (x1, y1) in zip(hull, hull[1:] + hull[:1], strict=True):
        length = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        distances.append(((x1 - x0) * (target[1] - y0) - (y1 - y0) * (target[0] - x0)) / length)
    return float(min(distances))


def _convex_hull(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """Andrew's monotone chain, counter-clockwise, from points sorted by X then Y."""
    def half(sequence):
        chain = []
        for point in sequence:
            while len(chain) >= 2 and ((chain[-1][0] - chain[-2][0]) * (point[1] - chain[-2][1])
                                       - (chain[-1][1] - chain[-2][1]) * (point[0] - chain[-2][0])) <= 0:
                chain.pop()
            chain.append(point)
        return chain
    lower, upper = half(points), half(reversed(points))
    return lower[:-1] + upper[:-1]
