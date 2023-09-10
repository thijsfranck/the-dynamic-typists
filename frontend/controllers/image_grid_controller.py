from __future__ import annotations

from typing import TYPE_CHECKING

from .click_rotation_controller import ClickRotationController
from .drag_drop_grid_controller import DragDropGridController
from .transform_controller import TransformController

if TYPE_CHECKING:
    from js import JsDomElement


class ImageGridController:
    """
    Controller managing a grid of images that supports drag-and-drop and image rotation.

    The class integrates both the `DragDropGridController` for drag-and-drop capabilities and
    `ClickRotationController` for  click-to-rotate functionality. Each image in the grid can be
    rotated and repositioned within the grid.

    Attributes
    ----------
    root : JsDomElement
        The root DOM element wherein the grid will be rendered.
    columns : int
        Specifies the number of columns in the grid.
    rotation_steps : int
        Defines the number of distinct rotation positions an image can snap to.
    _grid_controller : DragDropGridController
        Controller responsible for handling drag and drop actions on the grid.
    _rotation_controllers : List[ClickRotationController]
        List of controllers managing the rotation for each individual image in the grid.
    """

    def __init__(self, root: JsDomElement, columns: int = 2, rotation_steps: int = 4) -> None:
        """
        Initialize the `ImageGridController`.

        Parameters
        ----------
        root : JsDomElement
            The root element where the grid will be rendered.
        columns : int, optional
            Number of columns for the grid layout. Defaults to 2.
        rotation_steps : int, optional
            Discrete rotation positions that an image can snap to. Defaults to 4.
        """
        self.root: JsDomElement = root
        self.columns: int = columns
        self.rotation_steps: int = rotation_steps
        self._images: list[str] = []
        self._grid_controller = DragDropGridController(root, columns=columns, drop_behavior="swap")
        self._rotation_controllers: list[ClickRotationController] = []

    def render(self, images: list[str]) -> None:
        """
        Render the images in the grid and assign rotation controllers to each image.

        Parameters
        ----------
        images : List[str]
            List of base64 encoded strings to be displayed in the grid.
        """
        self._images = images
        self._grid_controller.render(images)

        children = list(self.root.children)

        for child in children:
            child.classList.add("square")
            transform = TransformController(child)
            controller = ClickRotationController(transform, rotation_steps=self.rotation_steps)
            self._rotation_controllers.append(controller)

    def destroy(self) -> None:
        """Remove all grid items, destroy all controllers, and reset the root styles."""
        self._grid_controller.destroy()
        while len(self._rotation_controllers):
            controller = self._rotation_controllers.pop()
            controller.transform.destroy()
            controller.destroy()

    def reset(self) -> None:
        """Reset the grid to its initial state and reset rotations to default."""
        self.destroy()
        self.render(self._images)

    @property
    def solution(self) -> list[tuple[int, float]]:
        """
        Provide the current solution as positions and rotations of images.

        Returns
        -------
        List[Tuple[int, float]]
            List of tuples where each tuple contains the position and rotation of each image.
            Each tuple is in the format (position, rotation).
        """
        children = list(self.root.children)
        return [
            (children.index(controller.element), controller.current_rotation)
            for controller in self._rotation_controllers
        ]
