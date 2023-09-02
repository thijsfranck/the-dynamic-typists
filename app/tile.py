"""Tile module."""
from dataclasses import dataclass

from PIL import Image


@dataclass
class Tile:
    """Tile dataclass."""

    image: Image.Image
    rotation: int = 0
