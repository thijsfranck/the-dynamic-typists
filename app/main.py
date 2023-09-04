from pathlib import Path

from picture import Picture
from scrambler import Scrambler

if __name__ == "__main__":
    pic = Picture()
    pic.load(str(Path.cwd() / "resources" / "trevi_mark_neal.jpg"))
    Scrambler.scramble_circle(pic)
    pic.save(str(Path.cwd() / "resources" / "circle.jpg"), "circle")
