"""Convert the Phobos robot-dog URDF into an articulated browser-ready GLB.

Run with Blender so its STL importer and glTF exporter are available:

    blender --background --python tools/export-robodog-web.py -- robodog.urdf output.glb
"""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from math import radians
from pathlib import Path

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector


def script_args() -> tuple[Path, Path]:
    try:
        separator = sys.argv.index("--")
        source, destination = sys.argv[separator + 1 : separator + 3]
    except (ValueError, IndexError):
        raise SystemExit("Expected: -- input.urdf output.glb")
    return Path(source).resolve(), Path(destination).resolve()


def vector(text: str | None, fallback: tuple[float, float, float]) -> Vector:
    return Vector(tuple(float(value) for value in text.split()) if text else fallback)


def origin_matrix(element: ET.Element) -> Matrix:
    origin = element.find("origin")
    if origin is None:
        return Matrix.Identity(4)
    xyz = vector(origin.get("xyz"), (0.0, 0.0, 0.0))
    rpy = vector(origin.get("rpy"), (0.0, 0.0, 0.0))
    return Matrix.Translation(xyz) @ Euler(rpy, "XYZ").to_matrix().to_4x4()


def make_material(
    name: str,
    color: tuple[float, float, float, float],
    metallic: float,
    roughness: float,
) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.diffuse_color = color
    material.use_nodes = True
    shader = material.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = color
    shader.inputs["Metallic"].default_value = metallic
    shader.inputs["Roughness"].default_value = roughness
    return material


source, destination = script_args()
if not source.is_file():
    raise SystemExit(f"URDF source does not exist: {source}")

destination.parent.mkdir(parents=True, exist_ok=True)
robot = ET.parse(source).getroot()
if robot.tag != "robot":
    raise SystemExit(f"Expected a URDF robot root, found {robot.tag!r}")

bpy.ops.wm.read_factory_settings(use_empty=True)

blue = make_material("Printed blue", (0.035, 0.12, 0.42, 1.0), 0.08, 0.32)
aluminium = make_material("Machined aluminium", (0.52, 0.57, 0.62, 1.0), 0.72, 0.26)
rubber = make_material("Foot rubber", (0.025, 0.03, 0.04, 1.0), 0.0, 0.8)


def material_for(link_name: str) -> bpy.types.Material:
    if "foot" in link_name:
        return rubber
    if "_top_" in link_name or "_mid_" in link_name:
        return aluminium
    return blue


root = bpy.data.objects.new(robot.get("name", "robodog"), None)
bpy.context.collection.objects.link(root)

links: dict[str, bpy.types.Object] = {}
for link_element in robot.findall("link"):
    link_name = link_element.get("name")
    if not link_name:
        continue
    link = bpy.data.objects.new(link_name, None)
    bpy.context.collection.objects.link(link)
    links[link_name] = link

    for visual_index, visual in enumerate(link_element.findall("visual")):
        mesh = visual.find("geometry/mesh")
        if mesh is None or not mesh.get("filename"):
            continue
        mesh_path = (source.parent / mesh.get("filename")).resolve()
        if not mesh_path.is_file():
            raise SystemExit(f"Missing URDF mesh: {mesh_path}")

        result = bpy.ops.wm.stl_import(filepath=str(mesh_path))
        if "FINISHED" not in result:
            raise SystemExit(f"STL import failed for {mesh_path}: {result}")
        visual_object = bpy.context.active_object
        visual_object.name = visual.get("name") or f"{link_name}_visual_{visual_index}"
        visual_object.data.name = f"{visual_object.name}_mesh"
        visual_object.data.materials.append(material_for(link_name))
        visual_object.parent = link
        visual_object.matrix_parent_inverse = Matrix.Identity(4)
        visual_object.matrix_local = origin_matrix(visual)

        scale = vector(mesh.get("scale"), (1.0, 1.0, 1.0))
        visual_object.scale = scale
        mesh_data = visual_object.data
        editable_mesh = bmesh.new()
        editable_mesh.from_mesh(mesh_data)
        for face in editable_mesh.faces:
            face.smooth = True
        for edge in editable_mesh.edges:
            edge.smooth = len(edge.link_faces) == 2 and edge.calc_face_angle(0.0) < radians(32)
        editable_mesh.to_mesh(mesh_data)
        editable_mesh.free()

joints = robot.findall("joint")
child_links = {
    child.get("link")
    for joint in joints
    if (child := joint.find("child")) is not None
}
root_links = [link for name, link in links.items() if name not in child_links]
for link in root_links:
    link.parent = root
    link.matrix_parent_inverse = Matrix.Identity(4)
    link.matrix_local = Matrix.Identity(4)

for joint in joints:
    joint_name = joint.get("name")
    joint_type = joint.get("type")
    parent_element = joint.find("parent")
    child_element = joint.find("child")
    if not joint_name or parent_element is None or child_element is None:
        continue

    parent = links.get(parent_element.get("link", ""))
    child = links.get(child_element.get("link", ""))
    if parent is None or child is None:
        raise SystemExit(f"Unresolved links for joint {joint_name}")

    transform = origin_matrix(joint)
    if joint_type == "fixed":
        child.parent = parent
        child.matrix_parent_inverse = Matrix.Identity(4)
        child.matrix_local = transform
        continue

    if joint_type not in {"revolute", "continuous"}:
        raise SystemExit(f"Unsupported joint type {joint_type!r} for {joint_name}")

    pivot = bpy.data.objects.new(f"control__{joint_name}", None)
    bpy.context.collection.objects.link(pivot)
    pivot.empty_display_type = "ARROWS"
    pivot.parent = parent
    pivot.matrix_parent_inverse = Matrix.Identity(4)
    pivot.matrix_local = transform

    axis_element = joint.find("axis")
    axis = vector(
        axis_element.get("xyz") if axis_element is not None else None,
        (1.0, 0.0, 0.0),
    )
    limit = joint.find("limit")
    pivot["joint_axis"] = list(axis)
    if limit is not None:
        pivot["joint_lower"] = float(limit.get("lower", "0"))
        pivot["joint_upper"] = float(limit.get("upper", "0"))

    child.parent = pivot
    child.matrix_parent_inverse = Matrix.Identity(4)
    child.matrix_local = Matrix.Identity(4)

result = bpy.ops.export_scene.gltf(
    filepath=str(destination),
    export_format="GLB",
    export_yup=True,
    export_apply=False,
    export_animations=True,
    export_cameras=False,
    export_lights=False,
    export_extras=True,
)
if "FINISHED" not in result:
    raise SystemExit(f"glTF export failed: {result}")

print(
    f"Exported {len(links)} URDF links and "
    f"{sum(1 for joint in joints if joint.get('type') == 'revolute')} revolute joints "
    f"to {destination} ({destination.stat().st_size} bytes)"
)
