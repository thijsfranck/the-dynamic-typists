"""Picture class contains template for picture based on Image from Pillow."""
from __future__ import annotations

import string
from random import choice
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFont

if TYPE_CHECKING:
    from app.tile import Tile


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

    def add_watermark(self) -> None:
        """Create a five digit code and add is as watermark into the picture."""
        text = ""
        for _ in range(5):
            text += choice(string.digits + string.ascii_lowercase)

        img_width, img_height = self.image.size

        fontsize = 175
        diff = 1
        old_width = 0
        while True:
            # find font size, so that text width matches the width of the picture
            font = ImageFont.truetype("arial.ttf", fontsize)
            font_left, font_top, font_right, font_bottom = font.getbbox(text)
            font_width = font_right + font_left
            font_height = font_bottom + font_top

            # diff must be dynamic, otherwise the code could get stuck in the loop
            old_width = font_width if old_width == 0 else old_width
            diff = max(diff, abs(old_width - font_width))
            old_width = font_width

            if img_width - diff <= font_width <= img_width:
                break

            # select next fontsize
            if font_width + diff < img_width:
                fontsize += 1
            elif font_width > img_width:
                fontsize -= 1

        x = img_width // 2 - font_width // 2
        y = img_height // 2 - font_height // 2

        # create watermark picture
        watermark = Image.new(mode="RGB", size=self.image.size)
        watermark_draw = ImageDraw.Draw(watermark)
        watermark_draw.text((x, y), text, fill=(192, 192, 192), font=font)
        watermark = watermark.rotate(90)

        # put watermark in the middle of the picture
        mask = Image.new(mode="L", size=self.image.size, color=50)
        self.image = Image.composite(watermark, self.image, mask=mask)

    def is_image_fixed(self) -> None:
        """Check if the scrambled tiles are put back to the original."""
        raise NotImplementedError
