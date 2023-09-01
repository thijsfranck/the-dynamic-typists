from Picture import Picture


class Scrambler:
    def scramble_rows(self, picture: Picture) -> Picture:
        """Splits an Image up into rows an rearranges them."""
        raise NotImplementedError

    def scramble_grid(self, picture: Picture) -> Picture:
        """Splits an Image up into rows an rearranges them."""
        raise NotImplementedError

    def scramble_circle(self, picture: Picture) -> Picture:
        """Splits an Image up into rows an rearranges them."""
        raise NotImplementedError
