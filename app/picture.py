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
        watermark = watermark.rotate(45)

        # put watermark in the middle of the picture
        mask = Image.new(mode="L", size=self.image.size, color=75)
        self.image = Image.composite(watermark, self.image, mask=mask)
