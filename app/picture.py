from __future__ import annotations

import string
from random import choice
from typing import TYPE_CHECKING

from PIL import Image, ImageDraw, ImageFont, ImageStat

if TYPE_CHECKING:
    from app.tile import Tile


class Picture:
    """A picture holds information about an image and handles scrambling into tiles."""

    def __init__(self, img_path: str) -> None:
        """Create a new `Picture` with the given image.

        Parameters
        ----------
        img_path:
            The path to the image.
        """
        self.image: Image.Image = Image.open(img_path)
        self.tiles: dict[int, Tile] = {}
        self.tile_order: list[int] = []
        self.scramble_type: str | None = None
        self.code: str = ""
        self._generate_code()

    def add_watermark(self, text: str) -> None:
        """Create a five digit code and add it as a watermark into the picture.

        Parameters
        ----------
        text:
            The text to watermark.
        """
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
        watermark_draw.text((x, y), text, fill=(150, 150, 150), font=font)
        watermark = watermark.rotate(45)

        # chose contrast based on the originals image brightness
        watermark_contrast = int(self._get_brightness() * 0.8)

        # put watermark in the middle of the picture
        mask = Image.new(mode="L", size=self.image.size, color=watermark_contrast)
        self.image = Image.composite(watermark, self.image, mask=mask)

    def _get_brightness(self) -> int:
        """Get the average pixel brightness."""
        return int(ImageStat.Stat(self.image.convert("L")).mean[0])

    def _generate_code(self) -> None:
        """Generate a five digit code containing number and lower-case letters.

        The code is used as a solution for the CAPTCHA.
        """
        for _ in range(5):
            self.code += choice(string.digits + string.ascii_lowercase)
