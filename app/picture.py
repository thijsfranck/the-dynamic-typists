"""Picture class contains template for picture based on Image from Pillow."""
from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from .tile import Tile


class Picture:
    """Picture class has methods for saving PIL image formed from tiles.

    :param img_path: Used to provide image path to open image.
    """

    def __init__(self, img_path: str) -> None:
        self.image: Image.Image = Image.open(img_path)
        self.is_solved: bool = False
        self.tiles: dict[int, Tile] = {}
        self.tile_order: list[int] = []
        self.scramble_type = None

    def save(self, img_path: str) -> None:
        """Save current tile arrangement as file."""
        new_image = Image.new(mode=self.image.mode, size=self.image.size)

        for original_pos, new_pos in enumerate(self.tile_order):
            if self.scramble_type == "tiles":
                self.tiles[new_pos].image = self.tiles[new_pos].image.rotate(
                    self.tiles[new_pos].rotation,
                )
            elif self.scramble_type == "circle":
                scrambled_tile = self.tiles[new_pos]
                original_tile_position = self.tiles[original_pos].position
                transparent_tile = Image.new("RGBA", new_image.size, (0, 0, 0, 0))
                transparent_tile.paste(scrambled_tile.image.convert("RGBA"), original_tile_position)
                new_image = Image.alpha_composite(new_image.convert("RGBA"), transparent_tile)
            new_image.paste(self.tiles[new_pos].image, self.tiles[original_pos].position)

        new_image = new_image.convert(self.image.mode)
        new_image.save(img_path)

    def is_image_fixed(self) -> None:
        """Check if the scrambled tiles are put back to the original."""
        raise NotImplementedError
