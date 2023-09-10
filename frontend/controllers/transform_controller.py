from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from js import JsDomElement


class Transforms(TypedDict):
    """
    A TypedDict for defining the transform properties to be applied to a DOM element.

    Attributes
    ----------
    rotate : str | None
        A string representing the rotation transformation or None if not set.
    scale : str | None
        A string representing the scale transformation or None if not set.
    """

    rotate: str | None
    scale: str | None


class TransformController:
    """
    A controller for managing and applying transformations to a DOM element.

    This controller provides an interface to apply transformations like rotation and scaling
    to a DOM element without overwriting each other.

    Attributes
    ----------
    element : JsDomElement
        The DOM element that the transformations will be applied to.
    transforms : Transforms
        A dictionary holding the transform functions and their values.
    """

    def __init__(self, element: JsDomElement) -> None:
        """
        Initialize the TransformController with the provided DOM element.

        Parameters
        ----------
        element : JsDomElement
            The DOM element to which the transformations will be applied.
        """
        self.element: JsDomElement = element
        self.transforms: dict[str, str] = {}

    def destroy(self) -> None:
        """Remove the transform property from the element styles."""
        self.element.style.removeProperty("transform")

    def transform(self) -> None:
        """Apply all stored transforms to the element."""
        transform_str = " ".join(self.transforms.values())
        self.element.style.transform = transform_str

    def rotate(self, degrees: float) -> None:
        """
        Rotate the element by the given number of degrees.

        This method updates the rotation transform and applies it to the element.

        Parameters
        ----------
        degrees : float
            The number of degrees by which the image should be rotated.
        """
        self._current_rotation = degrees % 360

        self.transforms["rotate"] = f"rotate({self._current_rotation}deg)"
        self.transform()

    def scale(self, factor: float) -> None:
        """
        Scale the element by the given factor.

        This method updates the scale transform and applies it to the element.

        Parameters
        ----------
        factor : float
            The scaling factor.
        """
        self.transforms["scale"] = f"scale({factor})"
        self.transform()
