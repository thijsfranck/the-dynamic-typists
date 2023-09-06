# Testing code, probably should be removed later?
from pathlib import Path

from picture import Picture
from scrambler import scramble_grid, scramble_rows

if __name__ == "__main__":
    pic = Picture(str(Path.cwd() / "resources" / "pydis_logo.png"))
    scramble_rows(pic)
    pic.save(str(Path.cwd() / "resources" / "pydis_logo_scrambled.png"))

    tile_pic = Picture(str(Path.cwd() / "resources" / "stairs_josh_hild.jpg"))
    scramble_grid(tile_pic)
    tile_pic.save(str(Path.cwd() / "resources" / "stairs_josh_hild_scrambled.jpg"))
