from __future__ import annotations

import math
from typing import TYPE_CHECKING

from js import document
from pyodide.ffi.wrappers import add_event_listener

from .rotation_controller import RotationController

if TYPE_CHECKING:
    from pyodide.ffi import JsDomElement


class DragRotationController(RotationController):
    """
    `DragRotationController` allows for rotating an element by dragging with the mouse.

    It listens to mouse events on the associated element and translates mouse movements
    into rotation angles, with optional snap-to-grid functionality based on the number of
    rotation steps provided.

    Attributes
    ----------
    element : JsDomElement
        The HTML DOM element being rotated.
    _center : dict[str, int]
        The central point of the element being rotated.
    _is_rotating : bool
        A flag indicating if the user is actively dragging/rotating the element.
    """

    def __init__(self, element: JsDomElement, rotation_steps: int = 360) -> None:
        """
        Create a new `DragRotationController` for the given `element`.

        Parameters
        ----------
        element : JsDomElement
            The element rotated by this instance.
        rotation_steps : int, optional
            The number of positions to which the element can snap during rotation,
            evenly divided around the circle. Defaults to 360.
        """
        super().__init__(element, rotation_steps)

        self.element: JsDomElement = element
        self._center: dict[str, int] = {"x": 0, "y": 0}
        self._is_rotating: bool = False

        add_event_listener(self.element, "mousedown", self._on_mouse_down)
        add_event_listener(document, "mousemove", self._on_mouse_move)
        add_event_listener(document, "mouseup", self._on_mouse_up)

    def _on_mouse_down(self, event: object) -> None:
        """
        Enable the rotating state and set the current element center on left-click.

        Parameters
        ----------
        event : MouseEvent
            The mouse event triggered by the user.
        """
        event.preventDefault()

        bounding_rect = self.element.getBoundingClientRect()

        self._center["x"] = bounding_rect.left + bounding_rect.width / 2
        self._center["y"] = bounding_rect.top + bounding_rect.height / 2

        self._is_rotating = True
        self.element.classList.add("active")

    def _on_mouse_move(self, event: object) -> None:
        """
        Calculate the rotation angle based on the user's mouse movement and apply it to the element.

        Parameters
        ----------
        event : MouseEvent
            The mouse move event triggered by the user.
        """
        # Do nothing if the user is not actively rotating the element
        if not self._is_rotating:
            return

        dx: int = event.pageX - self._center["x"]
        dy: int = event.pageY - self._center["y"]

        angle_rad = math.atan2(dx, -dy)
        angle_deg = math.degrees(angle_rad)

        # Ensure the element rotates 360 degrees to avoid the image flipping
        if angle_deg < 0:
            angle_deg += 360

        degrees_per_step = 360 / self.rotation_steps

        # Snapping the angle to the nearest step
        angle_deg = round(angle_deg / degrees_per_step) * degrees_per_step

        self.rotate(angle_deg)

    def _on_mouse_up(self, _: object) -> None:
        """Disable the rotating state and remove applied styles."""
        if not self._is_rotating:
            return

        self._is_rotating = False
        self.element.classList.remove("active")
