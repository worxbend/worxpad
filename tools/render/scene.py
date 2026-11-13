"""Blender scene for the worxpad product renders. Run by tools/render_all.sh:

    flatpak run org.blender.Blender -b --factory-startup --python tools/render/scene.py -- \
        MESH_DIR SCREEN_PNG OUT_DIR VIEW [VIEW ...]

MESH_DIR holds manifest.json and the STL files from export_meshes.py (and pcb_step/ when the board STEP was
converted). VIEW is one of the keys of VIEWS; `turntable` writes numbered PNG frames to OUT_DIR/turntable/.
Cycles on the CPU. Materials are proposals for the look, not finishes anyone has ordered. Parts other than the
case are the reference shapes of cad/worxpad_case/components.py, not vendor models.
"""

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

MM = 0.001
SMOOTH_ANGLE = math.radians(35)
STILL_SIZE, STILL_SAMPLES = (1920, 1280), 64  # the denoiser does the rest; keeps the whole set near 15 minutes
TURNTABLE_SIZE, TURNTABLE_SAMPLES, TURNTABLE_FRAMES = (800, 536), 16, 72

# ---------------------------------------------------------------------------------------------------------
# Materials: name -> Principled BSDF inputs
# ---------------------------------------------------------------------------------------------------------
MATERIALS = {
    "anodised": {"Base Color": (0.018, 0.018, 0.02), "Metallic": 1.0, "Roughness": 0.42},  # bead-blasted black
    "pbt": {"Base Color": (0.005, 0.005, 0.0055), "Roughness": 0.6, "Specular IOR Level": 0.2},
    "black_plastic": {"Base Color": (0.006, 0.006, 0.0065), "Roughness": 0.45},
    "glass": {"Base Color": (1, 1, 1), "Roughness": 0.03, "IOR": 1.49, "Transmission Weight": 1.0},  # cast PMMA
    "lens_paint": {"Base Color": (0.004, 0.004, 0.004), "Roughness": 0.08},  # painted underside, seen through
    "panel_glass": {"Base Color": (0.003, 0.003, 0.004), "Roughness": 0.15},
    "soldermask": {"Base Color": (0.015, 0.12, 0.05), "Roughness": 0.35},
    "switch": {"Base Color": (0.05, 0.05, 0.055), "Roughness": 0.45},
    "steel": {"Base Color": (0.62, 0.62, 0.64), "Metallic": 1.0, "Roughness": 0.3},
    "black_oxide": {"Base Color": (0.05, 0.05, 0.05), "Metallic": 1.0, "Roughness": 0.4},
    "brass": {"Base Color": (0.78, 0.58, 0.28), "Metallic": 1.0, "Roughness": 0.3},
    "nylon": {"Base Color": (0.8, 0.78, 0.72), "Roughness": 0.55},
    "polyimide": {"Base Color": (0.55, 0.28, 0.03), "Roughness": 0.3},
    "foam": {"Base Color": (0.02, 0.02, 0.02), "Roughness": 0.95},
    "rubber": {"Base Color": (0.01, 0.01, 0.01), "Roughness": 0.85},
    "pouch": {"Base Color": (0.7, 0.71, 0.73), "Metallic": 0.9, "Roughness": 0.35},
    "pom": {"Base Color": (0.02, 0.02, 0.02), "Roughness": 0.4},
    "petg": {"Base Color": (0.86, 0.85, 0.81), "Roughness": 0.5, "Subsurface Weight": 0.08},  # light filament
    "floor": {"Base Color": (0.003, 0.003, 0.003), "Roughness": 0.35, "Specular IOR Level": 0.15},
}
PART_MATERIALS = {
    "top_shell": "anodised", "bottom_shell": "anodised", "knob_left": "anodised", "knob_right": "anodised",
    "keycaps": "pbt", "button_cap_left": "black_plastic", "button_cap_right": "black_plastic", "lens": "glass",
    "pcb": "soldermask", "switch_bodies": "switch", "switch_stems": "switch", "sockets": "black_plastic",
    "diodes": "black_plastic", "encoders": "steel", "encoder_shafts": "steel", "button_switches": "black_plastic",
    "display_module": "panel_glass", "display_flex": "polyimide", "display_foam": "foam", "fpc_connector": "nylon",
    "lens_tape": "foam", "module": "steel", "flash": "black_plastic", "usb_receptacle": "steel",
    "battery_connector": "nylon", "battery_plug": "nylon", "reset_button": "black_plastic",
    "power_switch": "steel", "power_parts": "black_plastic", "cell": "pouch", "insulation_sheet": "polyimide",
    "cell_foam": "foam", "k_screws": "black_oxide", "c_screws": "black_oxide", "g_screws": "black_oxide",
    "feet": "rubber", "rf_insert": "pom", "g_spacers": "petg", "inserts": "brass",
    "pcb_step_board": "soldermask", "pcb_step_parts": "black_plastic",
}
PRINTED = ("top_shell", "bottom_shell", "knob_left", "knob_right", "button_cap_left", "button_cap_right")

# Reference shapes that the KiCad STEP replaces when it carries part models
STEP_REPLACES = ("pcb", "sockets", "diodes", "module", "flash", "usb_receptacle", "battery_connector",
                 "reset_button", "power_switch", "power_parts", "fpc_connector", "encoders", "button_switches")

# Exploded view: lift along the unit's own Z in mm, by layer. Parts not listed stay with the PCB.
EXPLODED_LIFT = {
    "knob_left": 50, "knob_right": 50, "keycaps": 50, "button_cap_left": 45, "button_cap_right": 45,
    "lens": 45, "lens_tape": 45, "top_shell": 30, "display_module": 14, "display_flex": 14, "screen": 14,
    "insulation_sheet": -12, "cell": -22, "cell_foam": -24, "bottom_shell": -45, "rf_insert": -45,
    "feet": -60, "c_screws": -80,
}
EXPLODED_HIDDEN = ("k_screws", "g_screws", "battery_plug")


@dataclass
class View:
    variant: str = "cnc"
    background: tuple = (0.0, 0.0, 0.0)
    ambient: float = 0.06  # world light the camera does not see
    floor: bool = False
    exploded: bool = False
    direction: tuple = (0.55, 0.85, -0.55)  # camera looks along this, in the world frame
    up: tuple = (0.0, 0.0, 1.0)
    lens_mm: float = 85.0
    ortho: bool = False
    deck_frame: bool = False  # direction and up are in the unit's own frame (plan view of the tilted deck)
    focus: tuple = ()  # parts to frame; empty frames every visible part
    margin: float = 1.12
    lights: str = "studio"


VIEWS = {
    "hero": View(floor=True),
    "top": View(background=(0.16, 0.16, 0.17), ambient=0.25, direction=(0, 0, -1), up=(0, 1, 0), ortho=True,
                deck_frame=True, margin=1.06, lights="top"),
    "side": View(background=(0.55, 0.55, 0.56), ambient=0.35, direction=(1, 0, 0), up=(0, 0, 1), ortho=True,
                 margin=1.1, floor=False, lights="side"),
    "exploded": View(background=(0.035, 0.035, 0.04), ambient=0.25, exploded=True, direction=(0.5, 0.8, -0.42),
                     lens_mm=70, margin=1.05),
    "underside": View(background=(0.12, 0.12, 0.13), ambient=0.35, direction=(0.25, 0.45, 0.86), up=(0, 1, 0),
                      lens_mm=70, lights="below"),
    "closeup": View(floor=True, direction=(0.38, 0.7, -0.6), lens_mm=100, margin=1.08,
                    focus=("knob_left", "knob_right", "lens", "button_cap_left", "button_cap_right")),
    "fdm": View(variant="print", background=(0.035, 0.035, 0.04), ambient=0.2, floor=True),
    "turntable": View(floor=True, direction=(0.0, 0.92, -0.4), lens_mm=85, margin=1.18),
}


# ---------------------------------------------------------------------------------------------------------
# Scene building
# ---------------------------------------------------------------------------------------------------------
def material(name: str) -> bpy.types.Material:
    found = bpy.data.materials.get(name)
    if found is not None:
        return found
    made = bpy.data.materials.new(name)
    bsdf = made.node_tree.nodes["Principled BSDF"]
    for socket, setting in MATERIALS[name].items():
        bsdf.inputs[socket].default_value = (*setting, 1.0) if isinstance(setting, tuple) else setting
    return made


def lens_material(window: dict) -> bpy.types.Material:
    """Clear PMMA inside the mask window, painted black outside it (display 6.4). The test runs on the lens's
    own coordinates, which are the assembly frame in millimetres (the importer scales the object, not the mesh)."""
    made = bpy.data.materials.new("lens_masked")
    nodes, links = made.node_tree.nodes, made.node_tree.links
    output = nodes["Material Output"]
    nodes.remove(nodes["Principled BSDF"])
    clear, paint = (_bsdf(nodes, name) for name in ("glass", "lens_paint"))
    coords = nodes.new("ShaderNodeTexCoord")
    split = nodes.new("ShaderNodeSeparateXYZ")
    links.new(coords.outputs["Object"], split.inputs[0])
    inside = []
    for axis, centre in zip("XY", window["centre"], strict=True):
        offset = _math(nodes, links, "SUBTRACT", split.outputs[axis], float(centre))
        distance = _math(nodes, links, "ABSOLUTE", offset, 0.0)
        inside.append(_math(nodes, links, "LESS_THAN", distance, window["size"] / 2))
    both = _math(nodes, links, "MULTIPLY", inside[0], inside[1])
    mix = nodes.new("ShaderNodeMixShader")
    links.new(both, mix.inputs["Fac"])
    links.new(paint.outputs[0], mix.inputs[1])
    links.new(clear.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs["Surface"])
    return made


def _bsdf(nodes, name: str):
    node = nodes.new("ShaderNodeBsdfPrincipled")
    for socket, setting in MATERIALS[name].items():
        node.inputs[socket].default_value = (*setting, 1.0) if isinstance(setting, tuple) else setting
    return node


def _math(nodes, links, operation: str, first, second):
    """Math node on a socket and a second operand that is either a number or another socket."""
    node = nodes.new("ShaderNodeMath")
    node.operation = operation
    links.new(first, node.inputs[0])
    if isinstance(second, float):
        node.inputs[1].default_value = second
    else:
        links.new(second, node.inputs[1])
    return node.outputs[0]


def import_part(path: Path, name: str, root) -> bpy.types.Object:
    before = set(bpy.data.objects)
    bpy.ops.wm.stl_import(filepath=str(path), global_scale=MM)
    (part,) = set(bpy.data.objects) - before
    part.name = name
    clean = bmesh.new()
    clean.from_mesh(part.data)
    bmesh.ops.remove_doubles(clean, verts=clean.verts, dist=1e-4 * MM)
    clean.to_mesh(part.data)
    clean.free()
    part.data.shade_smooth()
    part.data.set_sharp_from_angle(angle=SMOOTH_ANGLE)
    part.parent = root
    return part


def screen_plane(rect: dict, image_path: Path, root) -> bpy.types.Object:
    """The panel's active area as an emitting plane textured with the status screen; image top toward +Y,
    the knob side."""
    (x0, x1), (y0, y1), z = rect["x"], rect["y"], rect["z"]
    corners = [(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)]
    mesh = bpy.data.meshes.new("screen")
    mesh.from_pydata([tuple(c * MM for c in corner) for corner in corners], [], [(0, 1, 2, 3)])
    uv = mesh.uv_layers.new()
    for loop, coord in zip(uv.data, ((0, 0), (1, 0), (1, 1), (0, 1)), strict=True):
        loop.uv = coord
    plane = bpy.data.objects.new("screen", mesh)
    bpy.context.collection.objects.link(plane)
    plane.parent = root
    made = bpy.data.materials.new("screen")
    nodes, links = made.node_tree.nodes, made.node_tree.links
    nodes.remove(nodes["Principled BSDF"])
    texture = nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images.load(str(image_path))
    texture.interpolation = "Closest"  # 240 pixels: show them as pixels
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Strength"].default_value = 1.6
    links.new(texture.outputs["Color"], emission.inputs["Color"])
    links.new(emission.outputs[0], nodes["Material Output"].inputs["Surface"])
    mesh.materials.append(made)
    return plane


def load_unit(mesh_dir: Path, variant: str, screen_png: Path):
    manifest = json.loads((mesh_dir / "manifest.json").read_text())
    pose = manifest["pose"]
    root = bpy.data.objects.new("unit", None)
    bpy.context.collection.objects.link(root)
    root.rotation_euler = (pose["rotation_x_rad"], 0.0, 0.0)
    root.location = Vector(pose["offset_mm"]) * MM
    data = manifest["variants"][variant]
    replaced = step_parts(mesh_dir, root)
    parts = {}
    for name, entry in data["parts"].items():
        if name in replaced:
            continue
        parts[name] = import_part(mesh_dir / entry["file"], name, root)
        parts[name].data.materials.append(part_material(name, variant, data))
    parts.update({obj.name: obj for obj in root.children if obj.name.startswith("pcb_step")})
    parts["screen"] = screen_plane(data["screen"], screen_png, root)
    return root, parts


def part_material(name: str, variant: str, data: dict) -> bpy.types.Material:
    if name == "lens":
        return lens_material(data["lens_window"])
    if variant == "print" and name in PRINTED:
        return material("petg")
    return material(PART_MATERIALS.get(name, "black_plastic"))


def step_parts(mesh_dir: Path, root) -> tuple:
    """Import the KiCad board when render_all.sh converted it; returns the reference shapes it replaces."""
    folder = mesh_dir / "pcb_step"
    if not (folder / "board.stl").is_file():
        return ()
    board = import_part(folder / "board.stl", "pcb_step_board", root)
    board.data.materials.append(material("soldermask"))
    if not (folder / "parts.stl").is_file():
        return ("pcb",)
    models = import_part(folder / "parts.stl", "pcb_step_parts", root)
    models.data.materials.append(material("black_plastic"))
    return STEP_REPLACES


# ---------------------------------------------------------------------------------------------------------
# World, floor, lights, camera
# ---------------------------------------------------------------------------------------------------------
def world(view: View) -> None:
    """The camera sees the background colour; the parts are lit by a neutral grey it does not see."""
    sky = bpy.data.worlds.new("sky")
    bpy.context.scene.world = sky
    nodes, links = sky.node_tree.nodes, sky.node_tree.links
    seen, light = nodes["Background"], nodes.new("ShaderNodeBackground")
    seen.inputs["Color"].default_value = (*view.background, 1.0)
    light.inputs["Color"].default_value = (view.ambient,) * 3 + (1.0,)
    path = nodes.new("ShaderNodeLightPath")
    mix = nodes.new("ShaderNodeMixShader")
    links.new(path.outputs["Is Camera Ray"], mix.inputs["Fac"])
    links.new(light.outputs[0], mix.inputs[1])
    links.new(seen.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], nodes["World Output"].inputs["Surface"])


def floor() -> None:
    bpy.ops.mesh.primitive_plane_add(size=4.0, location=(0.06, -0.04, 0.0))
    bpy.context.object.data.materials.append(material("floor"))


LIGHT_RIGS = {  # (name, location in m relative to the target, power W, size m)
    # Nothing sits along the hero camera's mirror direction (+X +Y, up), so the lens shows the screen.
    "studio": (("key", (-0.32, -0.28, 0.42), 7, 0.35), ("rim", (-0.30, 0.38, 0.18), 9, 0.25),
               ("fill", (0.40, -0.25, 0.12), 2, 0.5), ("top", (0.0, -0.25, 0.5), 3, 0.6)),
    "top": (("key", (-0.2, -0.25, 0.6), 6, 0.6), ("fill", (0.25, 0.2, 0.6), 3, 0.6)),
    "side": (("key", (-0.5, -0.3, 0.3), 8, 0.5), ("rim", (-0.3, 0.4, 0.25), 5, 0.4)),
    "below": (("key", (-0.25, -0.35, -0.45), 7, 0.5), ("fill", (0.3, 0.2, -0.4), 3, 0.5)),
}


def lights(rig: str, target: Vector) -> None:
    for name, offset, watts, size in LIGHT_RIGS[rig]:
        lamp = bpy.data.lights.new(name, "AREA")
        lamp.energy, lamp.size = watts, size
        lamp_object = bpy.data.objects.new(name, lamp)
        bpy.context.collection.objects.link(lamp_object)
        lamp_object.location = target + Vector(offset)
        aim(lamp_object, target - lamp_object.location, Vector((0, 0, 1)))


def aim(thing, direction: Vector, up: Vector) -> None:
    forward = direction.normalized()
    if abs(forward.dot(up.normalized())) > 0.999:
        up = Vector((0, 1, 0))
    right = forward.cross(up).normalized()
    true_up = right.cross(forward)
    thing.rotation_euler = Matrix((right, true_up, -forward)).transposed().to_euler()


def corners(objects) -> list[Vector]:
    bpy.context.view_layer.update()
    return [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]


def camera(view: View, objects, root) -> Vector:
    """Place a camera along view.direction so every corner of the framed parts' boxes fits, with a margin.
    Returns the target point (centre of the framed boxes)."""
    points = corners(objects)
    centre = Vector([(min(p[axis] for p in points) + max(p[axis] for p in points)) / 2 for axis in range(3)])
    frame = root.matrix_world.to_3x3() if view.deck_frame else Matrix.Identity(3)
    forward, up = (frame @ Vector(view.direction)).normalized(), frame @ Vector(view.up)
    lens = bpy.data.cameras.new("lens")
    eye = bpy.data.objects.new("camera", lens)
    bpy.context.collection.objects.link(eye)
    bpy.context.scene.camera = eye
    aim(eye, forward, up)
    right = forward.cross(up).normalized()
    true_up = right.cross(forward)
    width, height = bpy.context.scene.render.resolution_x, bpy.context.scene.render.resolution_y
    aspect = width / height
    offsets = [p - centre for p in points]
    if view.ortho:
        span_x = 2 * max(abs(o.dot(right)) for o in offsets)
        span_y = 2 * max(abs(o.dot(true_up)) for o in offsets)
        lens.type = "ORTHO"
        lens.ortho_scale = max(span_x, span_y * aspect) * view.margin
        distance = 1.0
    else:
        lens.lens, lens.sensor_fit, lens.sensor_width = view.lens_mm, "HORIZONTAL", 36.0
        tan_x = 18.0 / view.lens_mm / view.margin
        tan_y = tan_x / aspect
        distance = max(max(abs(o.dot(right)) / tan_x, abs(o.dot(true_up)) / tan_y) - o.dot(forward) for o in offsets)
    eye.location = centre - forward * distance
    lens.clip_start, lens.clip_end = 0.005, 10.0
    return centre


# ---------------------------------------------------------------------------------------------------------
# Render settings and views
# ---------------------------------------------------------------------------------------------------------
def settings(size: tuple, samples: int) -> None:
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces, scene.cycles.transmission_bounces = 8, 8
    scene.render.resolution_x, scene.render.resolution_y = size
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.look = "AgX - Medium High Contrast"


def clear() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def build(name: str, mesh_dir: Path, screen_png: Path):
    """Build one view's scene; returns the unit root and the camera target."""
    view = VIEWS[name]
    clear()
    turntable = name == "turntable"
    settings(TURNTABLE_SIZE if turntable else STILL_SIZE, TURNTABLE_SAMPLES if turntable else STILL_SAMPLES)
    root, parts = load_unit(mesh_dir, view.variant, screen_png)
    if view.exploded:
        for part_name, part in parts.items():
            part.location.z = EXPLODED_LIFT.get(part_name, 0.0) * MM
            part.hide_render = part_name in EXPLODED_HIDDEN
    world(view)
    if view.floor:
        floor()
    framed = [parts[n] for n in view.focus] if view.focus else [p for p in parts.values() if not p.hide_render]
    target = camera(view, framed, root)
    lights(view.lights, target)
    return root, target


def render_still(name: str, mesh_dir: Path, screen_png: Path, out_dir: Path) -> None:
    build(name, mesh_dir, screen_png)
    bpy.context.scene.render.filepath = str(out_dir / f"{name}.png")
    bpy.ops.render.render(write_still=True)
    print(f"rendered {out_dir / name}.png")


def render_turntable(mesh_dir: Path, screen_png: Path, out_dir: Path) -> None:
    """The unit turns once about a vertical axis through its centre under fixed lights and camera."""
    root, target = build("turntable", mesh_dir, screen_png)
    pivot = bpy.data.objects.new("pivot", None)
    bpy.context.collection.objects.link(pivot)
    pivot.location = (target.x, target.y, 0.0)
    bpy.context.view_layer.update()
    root.parent = pivot
    root.matrix_parent_inverse = pivot.matrix_world.inverted()
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 1, TURNTABLE_FRAMES
    bpy.context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"  # constant speed
    for frame, angle in ((1, 0.0), (TURNTABLE_FRAMES + 1, 2 * math.pi)):  # frame N+1 would repeat frame 1
        pivot.rotation_euler.z = angle
        pivot.keyframe_insert("rotation_euler", index=2, frame=frame)
    scene.render.use_persistent_data = True
    scene.render.filepath = str(out_dir / "turntable" / "frame_")
    bpy.ops.render.render(animation=True)
    print(f"rendered {TURNTABLE_FRAMES} turntable frames to {out_dir / 'turntable'}")


def main(arguments: list[str]) -> None:
    mesh_dir, screen_png, out_dir, *names = arguments
    unknown = [name for name in names if name not in VIEWS]
    if not names or unknown:
        raise SystemExit(f"usage: scene.py -- MESH_DIR SCREEN_PNG OUT_DIR VIEW...; views: {', '.join(VIEWS)}; "
                         f"unknown: {unknown}")
    for name in names:
        if name == "turntable":
            render_turntable(Path(mesh_dir), Path(screen_png), Path(out_dir))
        else:
            render_still(name, Path(mesh_dir), Path(screen_png), Path(out_dir))


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:])
