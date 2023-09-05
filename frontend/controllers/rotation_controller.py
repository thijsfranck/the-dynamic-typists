class RotationController:
    """
    `RotationController` provides basic functionality to handle the rotation of DOM elements.

    This controller allows rotation of an element through direct methods or via
    stepping mechanisms. The rotation can be set to snap at specific intervals,
    defined by the number of rotation steps.

    Attributes
    ----------
    element : JsDomElement
        The HTML DOM element being rotated.
    rotation_steps : int
        Number of positions to which the element can snap during rotation.
    _current_rotation : float
        The current rotation of the element in degrees.
    """

    def __init__(self, element: object, rotation_steps: int = 360) -> None:
        """
        Create a new `RotationController` for the given `element`.

        Parameters
        ----------
        element : JsDomElement
            The element rotated by this instance.
        rotation_steps : int, optional
            The number of positions to which the element can snap during rotation,
            evenly divided around the circle. Defaults to 360.
        """
        self.element: object = element
        self.rotation_steps: int = rotation_steps
        self._current_rotation: float = 0

    def destroy(self) -> None:
        """Remove object applied transformation from the target element."""
        self.element.style.removeProperty("transform")

    def reset(self) -> None:
        """Rotate the element back to its original orientation (0 degrees)."""
        self.rotate(0)

    def rotate(self, degrees: float) -> None:
        """
        Rotate the element by the given number of degrees.

        Parameters
        ----------
        degrees : int
            The number of degrees by which the image should be rotated.
        """
        self._current_rotation = degrees % 360
        self.element.style.transform = f"rotate({self._current_rotation}deg)"

    def step_clockwise(self) -> None:
        """
        Rotate the element one step in the clockwise direction.

        The size of the step is determined by dividing 360 by the number of rotation steps.
        """
        self.rotate(self._current_rotation + 360 / self.rotation_steps)

    def step_counter_clockwise(self) -> None:
        """
        Rotate the element one step in the counter-clockwise direction.

        The size of the step is determined by dividing 360 by the number of rotation steps.
        """
        self.rotate(self._current_rotation - 360 / self.rotation_steps)

    @property
    def current_rotation(self) -> float:
        """
        Get the current rotation of the element.

        Returns
        -------
        float
            The number of degrees by which the element is currently rotated, ranging from 0 to 360.
        """
        return self._current_rotation