# FastAPI functions are better off without explicit return types.
# ruff: noqa: ANN201

import base64
import itertools
import random
from io import BytesIO
from os import getenv
from pathlib import Path
from typing import Annotated, Literal
from uuid import uuid4

from fastapi import Cookie, FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from PIL import Image
from pydantic import BaseModel, ConfigDict

from protocol import SolutionRequest, SolutionResponse, TilesResponse

from .picture import Picture
from .scrambler import scramble_circle, scramble_grid, scramble_rows
from .solver import solve_rows, solve_tiles

APP = FastAPI(debug=not bool(getenv("PRODUCTION")))
RESOURCES = Path("./app/resources")
GLOBS = {"*.png", "*.jpg", "*.jpeg", "*.gif", "*.avif", "*.webp"}


class SessionData(BaseModel):
    """
    Represents session-specific data for each user's CAPTCHA challenge.

    Attributes
    ----------
    picture : Picture
        The original Picture object used to generate the tiles.
    scrambler : Literal["rows", "grid", "circle"]
        The type of CAPTCHA challenge (rows, grid, or circle).
    session_id : str
        The unique identifier for the user's session.
    tiles_b64 : list[str]
        The base64-encoded image tiles for the CAPTCHA.
    """

    picture: Picture
    scrambler: Literal["rows", "grid", "circle"]
    session_id: str
    tiles_b64: list[str]

    model_config = ConfigDict(arbitrary_types_allowed=True)  # For compatibility with Picture class


# Initial version, in-memory dictionary for storing the tiles.
SESSIONS: dict[str, SessionData] = {}


def random_image() -> Path:
    """
    Choose and return a random image path from the resource directory.

    Returns
    -------
    Path
        The path to a randomly selected image.
    """
    images = list(itertools.chain(*(list(RESOURCES.glob(glob)) for glob in GLOBS)))
    return random.choice(images)


def image_base64(image: Image.Image) -> str:
    """
    Convert an Image object to its base64 representation.

    Parameters
    ----------
    image : Image.Image
        The PIL Image object to be encoded.

    Returns
    -------
    str
        The base64-encoded string of the image.
    """
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


@APP.get("/api/tiles")
async def get_tiles(response: Response, session_id: Annotated[str | None, Cookie()] = None):
    """
    Handle requests for a new set of CAPTCHA tiles.

    If a previous session ID is provided and exists, the corresponding session data is overwritten.
    Returns a random CAPTCHA type (rows, grid, or circle) and the associated tiles.

    Parameters
    ----------
    response : Response
        FastAPI's response object used to set cookies.
    session_id : str, optional
        The existing session ID, if any. Defaults to None.

    Returns
    -------
    TilesResponse
        A dictionary containing the CAPTCHA type and its associated image tiles.
    """
    if session_id is not None and session_id in SESSIONS:
        del SESSIONS[session_id]

    image_path = random_image()
    picture = Picture(str(object=image_path))

    scrambler = random.choice(["rows", "grid"])

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
    tiles_b64 = [image_base64(picture.tiles[index].image) for index in picture.tile_order]

    # Create a session and store it.
    session_id = str(uuid4())

    SESSIONS[session_id] = SessionData(
        picture=picture,
        scrambler=scrambler,
        session_id=session_id,
        tiles_b64=tiles_b64,
    )

    response.set_cookie(key="session_id", value=str(session_id))

    result: TilesResponse = {"type": scrambler, "tiles": tiles_b64}

    return result


@APP.post("/api/solution")
async def post_solution(
    request: SolutionRequest,
    session_id: Annotated[str | None, Cookie()] = None,
):
    # Check if session_id was provided
    if session_id is None:
        raise HTTPException(status_code=400, detail="Session ID missing in the request.")

    # Check if session exists for the given session_id
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found.")

    session_data = SESSIONS[session_id]

    solvers = {"rows": solve_rows, "grid": solve_tiles}

    # Check if the scrambler exists in solvers
    if session_data.scrambler not in solvers:
        raise HTTPException(status_code=500, detail=f"Invalid scrambler: {session_data.scrambler}")

    solver = solvers[session_data.scrambler]
    solution = solver(session_data.picture)

    print(solution)
    print(request["solution"])

    solved = request["solution"] == solution

    response: SolutionResponse = {
        "solved": solved,
    }

    return response


APP.mount("/", StaticFiles(directory="./frontend", html=True))
