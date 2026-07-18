import sys
from pathlib import Path

import bpy


def main() -> None:
    separator = sys.argv.index('--')
    args = sys.argv[separator + 1:]
    output = Path(args[0])
    inputs = [Path(value) for value in args[1:]]

    try:
        bpy.ops.preferences.addon_enable(module='io_scene_gltf2')
    except Exception:
        pass

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    for path in inputs:
        bpy.ops.wm.stl_import(filepath=str(path))

    meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    for obj in meshes:
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.select_set(True)
        obj.data.materials.clear()
        material = bpy.data.materials.new(name='Workshop blue')
        material.diffuse_color = (0.075, 0.16, 0.34, 1.0)
        material.metallic = 0.05
        material.roughness = 0.54
        obj.data.materials.append(material)

    output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(output),
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_draco_mesh_compression_enable=True,
    )


if __name__ == '__main__':
    main()
