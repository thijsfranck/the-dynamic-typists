"""Scrambler module."""
from picture import Picture
from random import shuffle

from tile import Tile


class Scrambler:
    """Scrambler class."""

    @classmethod
    def scramble_rows(cls, picture: Picture) -> None:
        """Split an Image up into rows an rearranges them."""
        num_tiles = 8
        image_size = picture.image.size
        tile_size = (image_size[0], int(image_size[1] / num_tiles))

        for y in range(num_tiles):
            x0, y0, x1, y1 = (0, tile_size[1] * y, tile_size[0], tile_size[1] * (y + 1))
            picture.tiles[y] = Tile(picture.image.crop((x0, y0, x1, y1)), (x0, y0))

        picture.tile_order = list(picture.tiles.keys())
        shuffle(picture.tile_order)

    def scramble_grid(self, picture: Picture) -> Picture:
        """Split an Image up into tiles an rearranges them."""
        raise NotImplementedError

    def scramble_circle(self, picture: Picture) -> Picture:
        """Split an Image up into circular tiles an rearranges them."""
        raise NotImplementedError
