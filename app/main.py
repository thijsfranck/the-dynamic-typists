from pathlib import Path

from picture import Picture
from scrambler import Scrambler

if __name__ == "__main__":
    pic = Picture(str(Path.cwd() / "resources" / "pydis_logo.png"))
    Scrambler.scramble_rows(pic)
    pic.save(str(Path.cwd() / "resources" / "pydis_logo_scrambled.png"), "rows")

    tile_pic = Picture(str(Path.cwd() / "resources" / "stairs_josh_hild.jpg"))
    Scrambler.scramble_grid(tile_pic)
    tile_pic.save(str(Path.cwd() / "resources" / "stairs_josh_hild_scrambled.jpg"), "tiles")
