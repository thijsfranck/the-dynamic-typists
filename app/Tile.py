from dataclasses import dataclass

from PIL import Image


@dataclass
class Tile:
    image: Image.Image
    rotation: int = 0
