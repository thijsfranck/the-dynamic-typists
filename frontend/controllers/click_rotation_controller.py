from typing import Any

from pyodide.ffi.wrappers import add_event_listener

from .rotation_controller import RotationController
from .transform_controller import TransformController


class ClickRotationController(RotationController):
    """
    `ClickRotationController` allows for rotating an element by clicking on it.

    The number of rotation steps defines how many discrete rotation angles the
    element can snap to, distributed evenly around the circle.

    Attributes
    ----------
    rotation_steps : int
        The number of discrete rotation angles the element can snap to.
    transform : TransformController
        The transform controller associated with the element that this controller manages.
    """

    def __init__(self, transform: TransformController, rotation_steps: int = 360) -> None:
        """
        Create a new `ClickRotationController` for the given `transform`.

        Parameters
        ----------
        transform : TransformController
            The transform controller associated with the element rotated by this instance.
        rotation_steps : int, optional
            The number of positions to which the element can snap during rotation, evenly
            divided around the circle. Defaults to 360.
        """
        super().__init__(transform, rotation_steps)
        add_event_listener(self.transform.element, "click", self._on_left_click)

    def _on_left_click(self, event: Any) -> None:
        """
        Handle the left-click event to rotate the element.

        Parameters
        ----------
        event : MouseEvent
            The mouse event associated with the click action.
        """
        event.preventDefault()
        self.step_clockwise()
