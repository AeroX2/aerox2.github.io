"""Convert a Sky130 GDS into a lightweight, layered GLB visualization.

The routing geometry is rasterized once into transparent textures and placed on
separated planes. This preserves the real layout while avoiding hundreds of
thousands of browser-side polygon meshes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import gdstk
import numpy as np
from PIL import Image, ImageDraw
import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals


LAYERS = [
    (65, 20, "diffusion", (73, 214, 153, 210)),
    (66, 20, "polysilicon", (244, 114, 182, 215)),
    (67, 20, "local-interconnect", (76, 201, 240, 220)),
    (68, 20, "metal-1", (78, 146, 255, 225)),
    (69, 20, "metal-2", (157, 112, 255, 225)),
    (70, 20, "metal-3", (255, 190, 74, 230)),
    (71, 20, "metal-4", (255, 103, 87, 235)),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("gds", type=Path)
    parser.add_argument("glb", type=Path)
    parser.add_argument("poster", type=Path)
    parser.add_argument("--long-edge", type=int, default=1536)
    return parser.parse_args()


def rasterize_layer(
    polygons: list[gdstk.Polygon],
    bounds: tuple[tuple[float, float], tuple[float, float]],
    size: tuple[int, int],
    color: tuple[int, int, int, int],
) -> Image.Image:
    (x_min, y_min), (x_max, y_max) = bounds
    width, height = size
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    x_scale = (width - 1) / (x_max - x_min)
    y_scale = (height - 1) / (y_max - y_min)
    for polygon in polygons:
        points = [
            (
                round((float(x) - x_min) * x_scale),
                round((y_max - float(y)) * y_scale),
            )
            for x, y in polygon.points
        ]
        if len(points) >= 3:
            draw.polygon(points, fill=color)
    return image


def textured_plane(
    width: float,
    depth: float,
    elevation: float,
    image: Image.Image,
    name: str,
) -> trimesh.Trimesh:
    vertices = np.array(
        [
            [-width / 2, elevation, -depth / 2],
            [width / 2, elevation, -depth / 2],
            [width / 2, elevation, depth / 2],
            [-width / 2, elevation, depth / 2],
        ],
        dtype=np.float32,
    )
    faces = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    uv = np.array([[0, 1], [1, 1], [1, 0], [0, 0]], dtype=np.float32)
    material = PBRMaterial(
        name=name,
        baseColorTexture=image,
        baseColorFactor=[255, 255, 255, 255],
        metallicFactor=0.15,
        roughnessFactor=0.6,
        alphaMode="BLEND",
        doubleSided=True,
    )
    return trimesh.Trimesh(
        vertices=vertices,
        faces=faces,
        visual=TextureVisuals(uv=uv, material=material),
        process=False,
    )


def main() -> None:
    args = parse_args()
    library = gdstk.read_gds(args.gds)
    top_cells = library.top_level()
    if len(top_cells) != 1:
        raise RuntimeError(f"Expected one top-level cell, found {len(top_cells)}")

    cell = top_cells[0]
    bounds = cell.bounding_box()
    if bounds is None:
        raise RuntimeError("GDS contains no geometry")

    (x_min, y_min), (x_max, y_max) = bounds
    gds_width = x_max - x_min
    gds_height = y_max - y_min
    if gds_width >= gds_height:
        texture_width = args.long_edge
        texture_height = round(args.long_edge * gds_height / gds_width)
    else:
        texture_height = args.long_edge
        texture_width = round(args.long_edge * gds_width / gds_height)
    texture_size = (max(texture_width, 1), max(texture_height, 1))

    flattened = cell.get_polygons(apply_repetitions=True, include_paths=True)
    by_layer: dict[tuple[int, int], list[gdstk.Polygon]] = {}
    for polygon in flattened:
        by_layer.setdefault((polygon.layer, polygon.datatype), []).append(polygon)

    scene = trimesh.Scene()
    plane_width = 2.0 * gds_width / gds_height
    plane_depth = 2.0
    layer_images: list[Image.Image] = []

    substrate = trimesh.creation.box(extents=[plane_width * 1.025, 0.07, plane_depth * 1.025])
    substrate.apply_translation([0, -0.055, 0])
    substrate.visual.material = PBRMaterial(
        name="silicon-substrate",
        baseColorFactor=[20, 31, 45, 255],
        metallicFactor=0.15,
        roughnessFactor=0.72,
    )
    scene.add_geometry(substrate, node_name="silicon-substrate")

    for index, (layer, datatype, name, color) in enumerate(LAYERS):
        polygons = by_layer.get((layer, datatype), [])
        if not polygons:
            continue
        image = rasterize_layer(polygons, bounds, texture_size, color)
        layer_images.append(image)
        elevation = 0.015 + index * 0.055
        scene.add_geometry(
            textured_plane(plane_width, plane_depth, elevation, image, name),
            node_name=name,
        )

    if not layer_images:
        raise RuntimeError("None of the configured Sky130 layers were found")

    poster = Image.new("RGBA", texture_size, (12, 17, 25, 255))
    for image in layer_images:
        poster = Image.alpha_composite(poster, image)
    poster = poster.convert("RGB")

    args.glb.parent.mkdir(parents=True, exist_ok=True)
    args.poster.parent.mkdir(parents=True, exist_ok=True)
    scene.export(args.glb, file_type="glb")
    poster.save(args.poster, "WEBP", quality=88, method=6)

    print(f"Top cell: {cell.name}")
    print(f"GDS polygons: {len(flattened):,}")
    print(f"Layer textures: {len(layer_images)} at {texture_size[0]}x{texture_size[1]}")
    print(f"GLB: {args.glb} ({args.glb.stat().st_size:,} bytes)")
    print(f"Poster: {args.poster} ({args.poster.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
