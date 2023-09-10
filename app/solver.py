from protocol import Solution

from .picture import Picture


def solve_rows(picture: Picture) -> Solution:
    """
    Compute the solution for the rows-scrambled CAPTCHA.

    For CAPTCHAs that are scrambled by rows, this function computes the solution
    based on the order of the tiles in the provided picture.

    Parameters
    ----------
    picture : Picture
        An instance of the Picture class representing the scrambled CAPTCHA.

    Returns
    -------
    Solution
        A list of indices representing the correct order of the tiles.
    """
    return [
        picture.tile_order.index(tile_position) for tile_position in range(len(picture.tile_order))
    ]


def solve_tiles(picture: Picture) -> Solution:
    """
    Compute the solution for the tile-rotated CAPTCHA.

    For CAPTCHAs where each tile is potentially rotated, this function computes the
    solution based on both the order and rotation of the tiles in the provided picture.

    Parameters
    ----------
    picture : Picture
        An instance of the Picture class representing the scrambled CAPTCHA.

    Returns
    -------
    Solution
        A list of tuples, where each tuple contains:
        - The index of the tile.
        - The rotation value of the tile.
    """
    return [
        (tile_position, float(picture.tiles[tile_position].rotation))
        for tile_position in picture.tile_order
    ]
