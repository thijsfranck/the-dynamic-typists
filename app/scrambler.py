"""Scrambler module."""
import random

from picture import Picture
from PIL import Image, ImageDraw


class Scrambler:
    """Scrambler class."""

    def scramble_rows(self, picture: Picture) -> Picture:
        """Split an Image up into rows an rearranges them."""
        raise NotImplementedError

    def scramble_grid(self, picture: Picture) -> Picture:
        """Split an Image up into tiles an rearranges them."""
        raise NotImplementedError

    @classmethod
    def scramble_circle(cls, picture: Picture, num_tiles: int = 6) -> Picture:
        """Split an Image up into rings an rearranges them."""
        image = picture.image
        if image is not None:
            width, height = image.size
            center = (width // 2, height // 2)

            radiusvar = min(width, height) / (2 * num_tiles)

            result = Image.new("RGB", (width, height), (255, 255, 255))

            result.paste(image, (0, 0))
            result.paste(image, (width - image.width, 0))
            result.paste(image, (0, height - image.height))
            result.paste(image, (width - image.width, height - image.height))
            for i in range(num_tiles):
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

                angle = random.randint(0, num_tiles) * (360 / num_tiles)
                rotated_ring = image.rotate(angle, resample=Image.BILINEAR, center=center)

                result.paste(rotated_ring, mask=mask)
