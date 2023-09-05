from __future__ import annotations

from .click_rotation_controller import ClickRotationController
from .drag_drop_grid_controller import DragDropGridController


class ImageGridController(DragDropGridController):
    """
    Controller for an image grid that can be manipulated via drag and drop and can be rotated.

    Attributes
    ----------
    rotation_steps : int
        Number of rotation steps for each image.
    _controllers : List[RotationController]
        List of rotation controllers attached to each image in the grid.
    """

    def __init__(self, root: object, columns: int = 2, rotation_steps: int = 4) -> None:
        """
        Create a new `ImageGridController` instance.

        Parameters
        ----------
        root : JsDomElement
            The root element in which to render the images.
        columns : int, optional
            The number of columns in the grid. Defaults to 2.
        rotation_steps : int, optional
            The number of rotation steps for each image. Defaults to 4.
        """
        super().__init__(root, columns=columns, drop_behavior="swap")

        self.rotation_steps: int = rotation_steps
        self._controllers: list[ClickRotationController] = []

    def render(self, images: list[str]) -> None:
        """
        Render the grid with the provided images and attach rotation controllers to each element.

        Parameters
        ----------
        images : List[str]
            List of images to be rendered in the grid.
        """
        super().render(images)

        children = list(self.root.children)

        for child in children:
            controller = ClickRotationController(child, rotation_steps=self.rotation_steps)
            self._controllers.append(controller)

    def destroy(self) -> None:
        """Remove all grid items, destroy all controllers, and reset the root styles."""
        super().destroy()

        while len(self._controllers):
            self._controllers.pop().destroy()

    def reset(self) -> None:
        """Reset the grid to its initial state and reset rotations to default."""
        super().reset()
        for controller in self._controllers:
            controller.reset()

    @property
    def solution(self) -> list[tuple[int, int]]:
        """
        Provide the current solution as positions and rotations of images.

        Returns
        -------
        List[Tuple[int, int]]
            List of tuples where each tuple contains the position and rotation of each image.
            Each tuple is in the format (position, rotation).
        """
        children = list(self.root.children)
        return [
            (children.index(controller.element), controller.current_rotation)
            for controller in self._controllers
        ]
