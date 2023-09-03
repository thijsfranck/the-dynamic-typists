from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from tile import Tile


class Picture:
    """Picture class."""

    def __init__(self, img_path: str) -> None:
        self.image: Image.Image = Image.open(img_path)
        self.is_solved: bool = False
        self.tiles: dict[int, Tile] = {}
        self.tile_order: list[int] = []
        self.scramble_type = None

    def save(self, img_path: str, scramble_type: str) -> None:
        """Save current tile arrangement as file."""
        new_image = Image.new(mode=self.image.mode, size=self.image.size)

        if scramble_type == "rows":
            for original_pos, new_pos in enumerate(self.tile_order):
                new_image.paste(self.tiles[new_pos].image, self.tiles[original_pos].position)

        if scramble_type == "tiles":
            for original_pos, new_pos in enumerate(self.tile_order):
                self.tiles[new_pos].image = self.tiles[new_pos].image.rotate(
                    self.tiles[new_pos].rotation,
                )
                new_image.paste(self.tiles[new_pos].image, self.tiles[original_pos].position)

        new_image.save(img_path)

    def is_image_fixed(self) -> None:
        """Check if the scrambled tiles are put back to the original."""
        raise NotImplementedError
