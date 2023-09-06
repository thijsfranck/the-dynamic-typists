# FastAPI functions are better off without explicit return types.
# ruff: noqa: ANN201

import base64
import itertools
import random
from io import BytesIO
from os import getenv
from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from PIL import Image

from .picture import Picture
from .scrambler import scramble_circle, scramble_grid, scramble_rows

APP = FastAPI(debug=not bool(getenv("PRODUCTION")))
RESOURCES = Path("./app/resources")
GLOBS = {"*.png", "*.jpg", "*.jpeg", "*.gif", "*.avif", "*.webp"}

# Initial version, in-memory dictionary for storing the tiles.
SOLUTIONS: dict[UUID, Picture] = {}


def random_image() -> Path:
    """Choose a random image from the resource directory."""
    images = list(itertools.chain(*(list(RESOURCES.glob(glob)) for glob in GLOBS)))
    return random.choice(images)


def image_base64(image: Image.Image) -> str:
    """Convert an image to base64."""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


@APP.get("/api/tiles")
async def get_tiles(response: Response, scrambler: str):
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

    # Get the images in order of scrambled tiles.
    image_uris = [image_base64(picture.tiles[index].image) for index in picture.tile_order]

    # Create a session and store it.
    session_id = UUID(int=random.getrandbits(128))
    SOLUTIONS[session_id] = picture
    response.set_cookie(key="session_id", value=str(session_id))

    return image_uris


APP.mount("/", StaticFiles(directory="./frontend", html=True))
