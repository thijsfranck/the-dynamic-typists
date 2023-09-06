# FastAPI functions are better off without explicit return types.
# ruff: noqa: ANN201

import base64
import itertools
import random
from io import BytesIO
from os import getenv
from pathlib import Path

from fastapi import FastAPI
from picture import Picture
from PIL import Image
from scrambler import scramble_circle, scramble_grid, scramble_rows

APP = FastAPI(debug=not bool(getenv("PRODUCTION")))
RESOURCES = Path("./resources")
GLOBS = {"*.png", "*.jpg", "*.jpeg", "*.gif", "*.avif", "*.webp"}


def random_image() -> Path:
    """Choose a random image from the resource directory."""
    images = list(itertools.chain(*(list(RESOURCES.glob(glob)) for glob in GLOBS)))
    return random.choice(images)


def convert_image(image: Image.Image) -> str:
    """Convert an image to a data:image URI."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"


@APP.get("/images")
async def get_images(scrambler: str):
    """Return a list of images."""
    image_path = random_image()
    picture = Picture(str(object=image_path))

    match scrambler:
        case "rows":
            scramble_rows(picture)
        case "grid":
            scramble_grid(picture)
        case "circle":
            scramble_circle(picture)
        case _:
            msg = "Scramble format is not implemented."
            raise RuntimeError(msg)

    tiles = [picture.tiles[index] for index in picture.tile_order]
    return {"tiles": [convert_image(tile.image) for tile in tiles]}
