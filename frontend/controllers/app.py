from __future__ import annotations

from typing import Union

from .drag_drop_grid_controller import DragDropGridController
from .image_grid_controller import ImageGridController
from .rotating_images_controller import RotatingImagesController

Controller = Union[ImageGridController, DragDropGridController, RotatingImagesController]

CONTROLLER_FACTORIES: dict[str, type[Controller]] = {
    "grid": ImageGridController,
    "rows": DragDropGridController,
    "circles": RotatingImagesController,
}


def fetch_images() -> list[str]:
    """Return a list of mock images for testing."""
    return [
        "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
        "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
        "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
        "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
    ]


class App:
    """
    The primary application controller managing the UI.

    Attributes
    ----------
    active_controller : Controller | None
        The currently active controller handling UI interactions.
        Can be None if no controller is set.
    root : object
        The main DOM element that the app and its controllers interact with.
    """

    def __init__(self, root: object) -> None:
        """
        Initialize a new instance of App.

        Parameters
        ----------
        root : JSDomElement
            The DOM element where the app will render the content.
        """
        self.active_controller: Controller | None = None
        self.root: object = root

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

        images = fetch_images()
        self.active_controller.render(images)

    def print_solution(self) -> None:
        """Display the solution of the currently active controller."""
        return

    def reset(self) -> None:
        """Restore the active controller to its original state."""
        if self.active_controller is not None:
            self.active_controller.reset()
