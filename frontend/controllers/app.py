from __future__ import annotations

from typing import TYPE_CHECKING

from pyodide.http import pyfetch

from .drag_drop_grid_controller import DragDropGridController
from .image_grid_controller import ImageGridController
from .rotating_images_controller import RotatingImagesController

if TYPE_CHECKING:
    from pyodide.ffi import JsDomElement

    from protocol import TilesResponse

Controller = ImageGridController | DragDropGridController | RotatingImagesController

CONTROLLER_FACTORIES: dict[str, type[Controller]] = {
    "grid": ImageGridController,
    "rows": DragDropGridController,
    "circles": RotatingImagesController,
}


async def fetch_tiles() -> TilesResponse:
    """
    Fetch tile images and their associated type for CAPTCHA challenges.

    This function makes an asynchronous request to the `/api/tiles` endpoint
    and retrieves a collection of tile images and their associated type. The response
    is structured to contain the tile type (e.g., 'grid', 'rows', 'circles') and the
    corresponding tile image URIs.

    Returns
    -------
    TilesResponse
        A dictionary containing the type of CAPTCHA and a list of image URIs.

    Raises
    ------
    RuntimeError
        If the request to the `/api/tiles` endpoint fails.
    """
    response = await pyfetch("/api/tiles")
    if not response.ok:
        # Need to properly handle errors
        msg = f"Failed to fetch images: {response.status} {await response.string()}"
        raise RuntimeError(msg)

    return await response.json()


class App:
    """
    The primary application controller managing the UI.

    Attributes
    ----------
    active_controller : Controller | None
        The currently active controller handling UI interactions.
        Can be None if no controller is set.
    root : JsDomElement
        The main DOM element that the app and its controllers interact with.
    """

    def __init__(self, root: JsDomElement) -> None:
        """
        Initialize a new instance of App.

        Parameters
        ----------
        root : JSDomElement
            The DOM element where the app will render the content.
        """
        self.active_controller: Controller | None = None
        self.root: JsDomElement = root

    async def load_captcha(self) -> None:
        """
        Load and display a CAPTCHA challenge using the appropriate controller.

        This method fetches a new CAPTCHA challenge from the server, which comprises a type
        (e.g., 'grid', 'rows', 'circles') and a set of associated tile images. Depending on
        the CAPTCHA type, it transitions to the corresponding controller and instructs it
        to render the fetched tiles.
        """
        captcha = await fetch_tiles()

        controller_name = captcha["type"]
        tiles = captcha["tiles"]

        self.set_controller(controller_name)

        if self.active_controller is not None:
            self.active_controller.render(tiles)

    def set_controller(self, controller_name: str) -> None:
        """
        Transition to the active controller identified by the provided name.

        This method will destroy the previously active controller (if any), fetch the required
        images, and then render the new controller using those images.

        Parameters
        ----------
        controller_name : str
            The identifier for the desired controller.
            Must match a key in the `controller_factories` dictionary.
        """
        if self.active_controller is not None:
            self.active_controller.destroy()

        if controller_name not in CONTROLLER_FACTORIES:
            return

        controller_factory = CONTROLLER_FACTORIES[controller_name]
        self.active_controller = controller_factory(self.root)

    def print_solution(self) -> None:
        """Display the solution of the currently active controller."""
        return

    def reset(self) -> None:
        """Restore the active controller to its original state."""
        if self.active_controller is not None:
            self.active_controller.reset()
