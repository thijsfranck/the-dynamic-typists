from pathlib import Path

from Picture import Picture
from Scrambler import Scrambler

if __name__ == "__main__":
    pic = Picture()
    pic.load(str(Path.cwd() / "resources" / "pydis_logo.png"))
    Scrambler.scramble_rows(pic)
    pic.save(str(Path.cwd() / "resources" / "pydis_logo_scrambled.png"))
