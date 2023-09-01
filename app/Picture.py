from PIL import Image


class Picture:
    def __init__(self) -> None:
        self.image = None
        self.is_solved = False
        self.tiles = {}
        self.tile_order = []

    def load(self, img_path: str) -> None:
        """Loads an image from a file path.

        :param img_path: Absolute path to the image file
        """
        self.image = Image.open(img_path)

    def is_image_fixed(self) -> None:
        """Checks if the scrambled tiles are put back to the original."""
        raise NotImplementedError
