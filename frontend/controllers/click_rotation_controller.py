from pyodide.ffi import JsDomElement
from pyodide.ffi.wrappers import add_event_listener

from .rotation_controller import RotationController


class ClickRotationController(RotationController):
    """
    `ClickRotationController` allows for rotating an element by clicking on it.

    The number of rotation steps defines how many discrete rotation angles the
    element can snap to, distributed evenly around the circle.

    Attributes
    ----------
    element : JsDomElement
        The HTML DOM element that this controller manages.
    rotation_steps : int
        The number of discrete rotation angles the element can snap to.
    """

    def __init__(self, element: JsDomElement, rotation_steps: int = 360) -> None:
        """
        Create a new `ClickRotationController` for the given `element`.

        Parameters
        ----------
        element : JsDomElement
            The element rotated by this instance.
        rotation_steps : int, optional
            The number of positions to which the element can snap during rotation, evenly
            divided around the circle. Defaults to 360.
        """
        super().__init__(element, rotation_steps)
        add_event_listener(self.element, "click", self._on_left_click)

    def _on_left_click(self, event: object) -> None:
        """
        Handle the left-click event to rotate the element.

        Parameters
        ----------
        event : MouseEvent
            The mouse event associated with the click action.
        """
        event.preventDefault()
        self.step_clockwise()
