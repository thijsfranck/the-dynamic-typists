from __future__ import annotations

from typing import Union

from controllers import DragDropGridController, ImageGridController, RotatingImagesController
from js import document
from pyodide.ffi.wrappers import add_event_listener

Controller = Union[ImageGridController, DragDropGridController, RotatingImagesController]

controller_factories: dict[str, type[Controller]] = {
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

        if controller_name not in controller_factories:
            return

        controller_factory = controller_factories[controller_name]
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


image_body: object = document.getElementById("image-body")
confirm_button: object = document.getElementById("confirm-button")
controller_select: object = document.getElementById("controller-select")
refresh_button: object = document.getElementById("refresh-button")

app = App(image_body)
app.set_controller(controller_select.value)

add_event_listener(
    controller_select,
    "change",
    lambda event: app.set_controller(event.target.value),
)
add_event_listener(confirm_button, "click", lambda _: app.print_solution())
add_event_listener(refresh_button, "click", lambda _: app.reset())
