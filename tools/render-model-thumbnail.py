"""Render a clean project thumbnail from a GLB using Blender."""

from __future__ import annotations

import sys
from pathlib import Path

import bpy
from mathutils import Vector


def script_args() -> tuple[Path, Path]:
    try:
        separator = sys.argv.index("--")
        source, destination = sys.argv[separator + 1 : separator + 3]
    except (ValueError, IndexError):
        raise SystemExit("Expected: -- input.glb output.png")
    return Path(source).resolve(), Path(destination).resolve()


def point_camera(camera: bpy.types.Object, target: Vector) -> None:
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()


source, destination = script_args()
if not source.is_file():
    raise SystemExit(f"Model does not exist: {source}")

destination.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(source))

meshes = [item for item in bpy.context.scene.objects if item.type == "MESH"]
if not meshes:
    raise SystemExit("The GLB contains no renderable meshes")

ship_material = bpy.data.materials.new("Blueprint model material")
ship_material.diffuse_color = (0.09, 0.22, 0.52, 1.0)
ship_material.use_nodes = True
ship_shader = ship_material.node_tree.nodes.get("Principled BSDF")
ship_shader.inputs["Base Color"].default_value = (0.09, 0.22, 0.52, 1.0)
ship_shader.inputs["Metallic"].default_value = 0.08
ship_shader.inputs["Roughness"].default_value = 0.46
for item in meshes:
    item.data.materials.clear()
    item.data.materials.append(ship_material)

corners = [item.matrix_world @ Vector(corner) for item in meshes for corner in item.bound_box]
minimum = Vector((min(point.x for point in corners), min(point.y for point in corners), min(point.z for point in corners)))
maximum = Vector((max(point.x for point in corners), max(point.y for point in corners), max(point.z for point in corners)))
center = (minimum + maximum) / 2
size = maximum - minimum
span = max(size)

for item in meshes:
    item.select_set(True)

ground_material = bpy.data.materials.new("Blueprint grid surface")
ground_material.diffuse_color = (0.82, 0.86, 0.92, 1.0)
ground_material.use_nodes = True
ground_nodes = ground_material.node_tree.nodes
ground_links = ground_material.node_tree.links
ground_shader = ground_nodes.get("Principled BSDF")
ground_shader.inputs["Roughness"].default_value = 0.88

coordinates = ground_nodes.new("ShaderNodeTexCoord")
wave_x = ground_nodes.new("ShaderNodeTexWave")
wave_x.wave_type = "BANDS"
wave_x.bands_direction = "X"
wave_x.inputs["Scale"].default_value = 32.0
wave_x.inputs["Distortion"].default_value = 0.0
wave_y = ground_nodes.new("ShaderNodeTexWave")
wave_y.wave_type = "BANDS"
wave_y.bands_direction = "X"
wave_y.inputs["Scale"].default_value = 32.0
wave_y.inputs["Distortion"].default_value = 0.0

separate = ground_nodes.new("ShaderNodeSeparateXYZ")
combine_y = ground_nodes.new("ShaderNodeCombineXYZ")
ground_links.new(coordinates.outputs["Generated"], wave_x.inputs["Vector"])
ground_links.new(coordinates.outputs["Generated"], separate.inputs["Vector"])
ground_links.new(separate.outputs["Y"], combine_y.inputs["X"])
ground_links.new(combine_y.outputs["Vector"], wave_y.inputs["Vector"])

line_x = ground_nodes.new("ShaderNodeMath")
line_x.operation = "LESS_THAN"
line_x.inputs[1].default_value = 0.065
line_y = ground_nodes.new("ShaderNodeMath")
line_y.operation = "LESS_THAN"
line_y.inputs[1].default_value = 0.065
ground_links.new(wave_x.outputs["Fac"], line_x.inputs[0])
ground_links.new(wave_y.outputs["Fac"], line_y.inputs[0])

grid = ground_nodes.new("ShaderNodeMath")
grid.operation = "MAXIMUM"
ground_links.new(line_x.outputs[0], grid.inputs[0])
ground_links.new(line_y.outputs[0], grid.inputs[1])

grid_color = ground_nodes.new("ShaderNodeMixRGB")
grid_color.blend_type = "MIX"
grid_color.inputs[1].default_value = (0.82, 0.86, 0.92, 1.0)
grid_color.inputs[2].default_value = (0.63, 0.72, 0.84, 1.0)
ground_links.new(grid.outputs[0], grid_color.inputs[0])
ground_links.new(grid_color.outputs[0], ground_shader.inputs["Base Color"])

bpy.ops.mesh.primitive_plane_add(size=span * 4.5, location=(center.x, center.y, minimum.z - span * 0.035))
ground = bpy.context.active_object
ground.data.materials.append(ground_material)

bpy.ops.object.camera_add()
camera = bpy.context.active_object
camera.data.lens = 58
camera.data.clip_start = max(span / 1000, 0.001)
camera.data.clip_end = span * 100
direction = Vector((1.25, -1.55, 0.9)).normalized()
camera.location = center + direction * span * 1.85
point_camera(camera, center + Vector((0, 0, span * 0.01)))

bpy.ops.object.light_add(type="AREA", location=center + Vector((span * 1.0, -span * 1.0, span * 2.25)))
key = bpy.context.active_object
key.data.energy = 1150
key.data.shape = "DISK"
key.data.size = span * 1.4
point_camera(key, center)

bpy.ops.object.light_add(type="AREA", location=center + Vector((-span * 1.4, -span * 0.5, span * 1.15)))
fill = bpy.context.active_object
fill.data.energy = 320
fill.data.color = (0.68, 0.78, 1.0)
fill.data.size = span * 1.3
point_camera(fill, center)

bpy.ops.object.light_add(type="AREA", location=center + Vector((-span * 0.4, span * 1.5, span * 1.7)))
rim = bpy.context.active_object
rim.data.energy = 500
rim.data.color = (0.54, 0.69, 1.0)
rim.data.size = span * 1.0
point_camera(rim, center)

scene = bpy.context.scene
scene.camera = camera
scene.render.engine = "BLENDER_EEVEE_NEXT"
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = False
scene.render.resolution_x = 1400
scene.render.resolution_y = 800
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(destination)

scene.world = bpy.data.worlds.new("Thumbnail world")
scene.world.use_nodes = True
background = scene.world.node_tree.nodes.get("Background")
background.inputs["Color"].default_value = (0.82, 0.86, 0.92, 1.0)
background.inputs["Strength"].default_value = 0.52

scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = 0.7
bpy.ops.render.render(write_still=True)
print(f"Rendered {source} to {destination}")
