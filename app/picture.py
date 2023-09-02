"""Picture module."""
from __future__ import annotations

from typing import TYPE_CHECKING

from PIL import Image

if TYPE_CHECKING:
    from tile import Tile


class Picture:
    """Picture class."""

    def __init__(self) -> None:
        self.image: Image.Image | None = None
        self.is_solved = False
        self.tiles: dict[int:Tile] = {}  # init so that autocomplete works
        self.tile_order = []

    def load(self, img_path: str) -> None:
        """Load an image from a file path.

        :param img_path: Absolute path to the image file
        """
        self.image = Image.open(img_path)

    def save(self, img_path: str) -> None:
        new_image = Image.new(mode=self.image.mode, size=self.image.size)
        for original_pos, new_pos in enumerate(self.tile_order):
            new_image.paste(self.tiles[new_pos].image, self.tiles[original_pos].position)
        new_image.save(img_path)

    def is_image_fixed(self) -> None:
        """Check if the scrambled tiles are put back to the original."""
        raise NotImplementedError
