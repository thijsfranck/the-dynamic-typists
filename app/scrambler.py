"""Scrambler module."""
from picture import Picture


class Scrambler:
    """Scrambler class."""

    def scramble_rows(self, picture: Picture) -> Picture:
        """Split an Image up into rows an rearranges them."""
        raise NotImplementedError

    def scramble_grid(self, picture: Picture) -> Picture:
        """Split an Image up into tiles an rearranges them."""
        raise NotImplementedError

    def scramble_circle(self, picture: Picture) -> Picture:
        """Split an Image up into circular tiles an rearranges them."""
        raise NotImplementedError
