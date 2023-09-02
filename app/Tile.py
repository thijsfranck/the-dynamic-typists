from dataclasses import dataclass

from PIL import Image


@dataclass
class Tile:
    """Represents one tile of a whole picture"""

    image: Image.Image
    """Tile as PIL.Image object"""
    position: tuple
    """The coordinates (x, y) of the tile in the original picture"""
    rotation: int = 0
    """The rotation of the tile in degrees"""
