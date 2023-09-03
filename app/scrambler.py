from picture import Picture


class Scrambler:
    """Scramble a picture in different ways."""

    def scramble_rows(self, picture: Picture) -> None:
        """Split an Image up into rows an rearranges them."""
        raise NotImplementedError

    def scramble_grid(self, picture: Picture) -> None:
        """Split an Image up into tiles an rearranges them."""
        raise NotImplementedError

    def scramble_circle(self, picture: Picture) -> None:
        """Split an Image up into circular tiles an rearranges them."""
        raise NotImplementedError
