from random import choice, shuffle

from picture import Picture
from tile import Tile


class Scrambler:
    """Scramble a picture in different ways."""

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

    @classmethod
    def scramble_grid(cls, picture: Picture) -> None:
        """Split an Image up into tiles an rearranges them and rotates each tile randomly."""
        num_of_tiles = 4
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
        swap_order = []

        shuffle(swap_list)
        for current_choice in swap_list:
            swap_order.append(current_choice)
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
            picture.tiles[tile] = Tile(
                picture.image.crop(co_ordinates[tile]),
                (co_ordinates[tile][0], co_ordinates[tile][1]),
                tile_rotations[tile],
            )

    def scramble_circle(self, picture: Picture) -> Picture:
        """Split an Image up into rows an rearranges them."""
        raise NotImplementedError
