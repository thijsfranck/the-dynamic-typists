from __future__ import annotations

from js import document

from .drag_rotation_controller import DragRotationController


class RotatingImagesController:
    """
    `RotatingImagesController` renders a set of images and allows each image to be rotated.

    This class provides methods for rendering the images, destroying them, resetting their state,
    and obtaining the current rotation of each image.

    Attributes
    ----------
    root : JsDomElement
        The HTML DOM element where the images are rendered.
    _controllers : List[DragRotationController]
        List of rotation controllers associated with each image.
    """

    def __init__(self, root: object) -> None:
        """
        Create a new `RotatingImagesController` instance.

        Parameters
        ----------
        root : JsDomElement
            The root element in which to render the images.
        """
        self.root: object = root
        self._controllers: list[DragRotationController] = []

    def render(self, images: list[str]) -> None:
        """
        Render the given images and attach RotationController instances to each image.

        Parameters
        ----------
        images : List[str]
            List of base64 encoded images.
        """
        self.root.classList.add("rotating-images")
        for image in images:
            img_element: object = document.createElement("img")
            img_element.src = f"data:image/png;base64,{image}"
            img_element.classList.add("rotatable-image")

            self._controllers.append(DragRotationController(img_element, rotation_steps=360))
            self.root.appendChild(img_element)

    def destroy(self) -> None:
        """Destroy each active controller and remove all child elements from the root element."""
        self.root.classList.remove("rotating-images")

        # Destroy each active controller
        while len(self._controllers):
            self._controllers.pop().destroy()

        # Remove all child elements from the root element
        while element := self.root.firstChild:
            self.root.removeChild(element)

    def reset(self) -> None:
        """Reset every active controller to its original state."""
        for controller in self._controllers:
            controller.reset()

    @property
    def solution(self) -> list[int]:
        """
        Get the current solution as a list of the degrees by which each element is rotated.

        Returns
        -------
        List[int] :
            List of rotation values in degrees.
        """
        return [controller.current_rotation for controller in self._controllers]
