from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import Image


@dataclass
class Tile:
    """Represent one tile of a whole picture."""

    image: Image.Image
    """Tile as PIL.Image object"""
    position: tuple[int, int]
    """The coordinates (x, y) of the tile in the original picture"""
    rotation: int = 0
    """The rotation of the tile in degrees"""
