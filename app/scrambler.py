"""Scramble has functions for scrambling images in different ways."""
import random
from random import choice, shuffle

from picture import Picture
from PIL import Image, ImageDraw
from tile import Tile


def scramble_rows(picture: Picture) -> None:
    """Split an Image up into rows an rearranges them."""
    num_tiles = 8
    image_size = picture.image.size
    tile_size = (image_size[0], int(image_size[1] / num_tiles))

    for y in range(num_tiles):
        co_ordinate = (0, tile_size[1] * y, tile_size[0], tile_size[1] * (y + 1))
        picture.tiles[y] = Tile(picture.image.crop(co_ordinate), (co_ordinate[0], co_ordinate[1]))

    picture.tile_order = list(picture.tiles.keys())
    shuffle(picture.tile_order)


def scramble_grid(picture: Picture, num_of_tiles: int = 4) -> None:
    """Split an Image up into tiles an rearranges them and rotates each tile randomly."""
    co_ordinates = [
        (0, 0, 512, 512),
        (512, 0, 1024, 512),
        (0, 512, 512, 1024),
        (512, 512, 1024, 1024),
    ]

    # Tile swap logic
    tile_order = [0, 1, 2, 3]
    swap_list = ["top", "left", "bottom", "right"]
    tile_rotations = [choice([90, 180, 270]) for _ in range(num_of_tiles)]
    _swap_order = []

    shuffle(swap_list)

    # Swap order can be used to keep track of swaps
    _swap_order = swap_list

    for current_choice in swap_list:
        if current_choice == "top":
            tile_order[0], tile_order[1] = tile_order[1], tile_order[0]

        if current_choice == "left":
            tile_order[0], tile_order[2] = tile_order[2], tile_order[0]

        if current_choice == "bottom":
            tile_order[2], tile_order[3] = tile_order[3], tile_order[2]

        if current_choice == "right":
            tile_order[1], tile_order[3] = tile_order[3], tile_order[1]

    # Order of tiles to be formed
    picture.tile_order = tile_order

    # Adding tiles for picture
    for tile in range(num_of_tiles):
        tile_img = picture.image.crop(co_ordinates[tile])
        tile_img = tile_img.rotate(tile_rotations[tile])
        picture.tiles[tile] = Tile(
            tile_img,
            (co_ordinates[tile][0], co_ordinates[tile][1]),
        )


def scramble_circle(picture: Picture) -> None:
    """Split an Image up into rows an rearranges them."""
    num_tiles = 6
    image = picture.image
    width, height = picture.image.size
    center = (width // 2, height // 2)
    radiusvar = min(width, height) / (2 * num_tiles)

    for i in range(num_tiles):
        ring = Image.new("RGBA", (width, height), (0, 0, 0, 0))

        inner_radius = radiusvar * i
        outer_radius = radiusvar * (i + 1)

        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse(
            [
                (center[0] - outer_radius, center[1] - outer_radius),
                (center[0] + outer_radius, center[1] + outer_radius),
            ],
            fill=255,
        )
        draw.ellipse(
            [
                (center[0] - inner_radius, center[1] - inner_radius),
                (center[0] + inner_radius, center[1] + inner_radius),
            ],
            fill=0,
        )

        angle = random.randint(0, num_tiles) * (360 // num_tiles)
        rotated_image = image.rotate(angle, resample=Image.BILINEAR, center=center)

        ring.paste(rotated_image.convert("RGBA"), (0, 0), mask.convert("L"))

        tile = Tile(ring, (0, 0), angle)

        picture.tiles[i] = tile

    picture.tile_order = list(picture.tiles.keys())
