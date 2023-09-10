from __future__ import annotations

import math
from typing import TYPE_CHECKING, Literal

from js import document
from pyodide.ffi.wrappers import add_event_listener

if TYPE_CHECKING:
    from collections.abc import Callable

    from js import DragEvent, JsDomElement


DropBehavior = Literal["insert", "swap"]


class DragDropGridController:
    """Controller for managing a draggable and droppable grid of images.

    Attributes
    ----------
    root : JsDomElement
        The root element where the images are rendered in a grid.
    columns : int
        Number of columns in the grid.
    drop_behavior : DropBehavior
        Defines the behavior on drop: "insert" or "swap".
    _images : List[str]
        A list of base64 encoded image strings.
    """

    def __init__(
        self,
        root: JsDomElement,
        columns: int = 1,
        drop_behavior: DropBehavior = "insert",
    ) -> None:
        """Create a new `DragDropGridController` with the given options.

        Parameters
        ----------
        root:
            The root element in which the images will be rendered.
        columns:
            Number of columns in the grid. Defaults to 1.
        drop_behavior:
            Behavior on dropping an image. Can be either "insert" or "swap". Defaults to "insert".
        """
        self.root: JsDomElement = root
        self.columns: int = columns
        self.drop_behavior: DropBehavior = drop_behavior
        self._images: list[str] = []

    def render(self, images: list[str]) -> None:
        """
        Render the images in a grid inside the root element.

        Parameters
        ----------
        images : List[str]
            List of base64 encoded image strings to be rendered in the grid.
        """
        self._images = images
        self.root.classList.add("grid-container")
        self.root.style.setProperty("--columns", str(self.columns))

        for index, image in enumerate(self._images):
            grid_item_element = document.createElement("div")
            grid_item_element.classList.add("grid-item")
            grid_item_element.setAttribute("draggable", "true")
            grid_item_element.setAttribute("data-index", str(index))

            img_element = document.createElement("img")
            img_element.src = "data:image/png;base64," + image
            grid_item_element.appendChild(img_element)

            # Add event listeners
            add_event_listener(grid_item_element, "dragstart", self._on_drag_start)
            add_event_listener(grid_item_element, "dragenter", self._on_drag_enter)
            add_event_listener(grid_item_element, "dragover", self._on_drag_over)
            add_event_listener(grid_item_element, "dragleave", self._on_drag_leave)
            add_event_listener(grid_item_element, "dragend", self._on_drag_end)
            add_event_listener(grid_item_element, "drop", self._on_drop)

            self.root.appendChild(grid_item_element)

    def destroy(self) -> None:
        """Remove the grid and all child elements from the root, resetting its styles."""
        self.root.classList.remove("grid-container")
        self.root.style.removeProperty("--columns")

        while element := self.root.firstChild:
            self.root.removeChild(element)

    def reset(self) -> None:
        """Reset the grid to its original state."""
        self.destroy()
        self.render(self._images)

    @property
    def solution(self) -> list[int]:
        """
        Get the current order of images in the grid.

        Returns
        -------
        List[int]
            List of indices representing the current order of images in the grid.
        """
        return [int(child.getAttribute("data-index")) for child in list(self.root.children)]

    def _on_drag_start(self, event: DragEvent) -> None:
        """
        Handle the drag start event.

        This method highlights the dragged item and potential drop targets.

        Parameters
        ----------
        event : DragEvent
            The event object associated with the drag start action.
        """
        source = event.target.closest(".grid-item")
        source_index = list(self.root.children).index(source)

        event.dataTransfer.setData("sourceIndex", str(source_index))
        event.dataTransfer.dropEffect = "move"

        # Set up drag image on a canvas to ensure it's the right size
        image_element = source.getElementsByTagName("img")[0]

        ctx = document.createElement("canvas").getContext("2d")
        ctx.canvas.width = image_element.width
        ctx.canvas.height = image_element.height

        # Rotate the preview image if the parent element is rotated
        if source.hasAttribute("data-angle"):
            angle = float(source.getAttribute("data-angle"))

            # Rotate the image around its center
            ctx.translate(image_element.width / 2, image_element.height / 2)
            ctx.rotate(angle * math.pi / 180)
            ctx.translate(-image_element.width / 2, -image_element.height / 2)

        ctx.drawImage(image_element, 0, 0, image_element.width, image_element.height)
        event.dataTransfer.setDragImage(ctx.canvas, 0, 0)

        # Highlight the current dragged element
        source.classList.add("dragged")

        # Highlight potential drop targets
        for child in self.root.children:
            if child != source:
                child.classList.add("drop-target")

    def _on_drag_enter(self, event: DragEvent) -> None:
        """
        Handle the drag enter event.

        Highlights the drop target when an element is dragged over it.

        Parameters
        ----------
        event : DragEvent
            The event object associated with the drag enter action.
        """
        event.preventDefault()
        target = event.target.closest(".grid-item")
        if target and not target.classList.contains("dragged"):
            target.classList.add("over")

    def _on_drag_over(self, event: DragEvent) -> None:
        """
        Handle the drag over event.

        Ensures the drag event is captured and can be used for dropping.

        Parameters
        ----------
        event : DragEvent
            The event object associated with the drag over action.
        """
        event.preventDefault()

    def _on_drag_leave(self, event: DragEvent) -> None:
        """
        Handle the drag leave event.

        Removes the highlight from the drop target when the dragged element leaves it.

        Parameters
        ----------
        event : DragEvent
            The event object associated with the drag leave action.
        """
        target = event.target.closest(".grid-item")
        if target and not target.contains(event.relatedTarget):
            target.classList.remove("over")

    def _on_drag_end(self, event: DragEvent) -> None:
        """
        Handle the drag end event.

        Cleans up classes and styles that were added for drag visualization.

        Parameters
        ----------
        event : DragEvent
            The event object associated with the drag end action.
        """
        event.preventDefault()
        for child in self.root.children:
            child.classList.remove("dragged", "drop-target", "over")

    def _on_drop(self, event: DragEvent) -> None:
        """
        Handle the drop event.

        Reorders the grid items based on the drop behavior, either "insert" or "swap".

        Parameters
        ----------
        event : DragEvent
            The event object associated with the drop action.
        """
        event.preventDefault()

        children = list(self.root.children)

        for child in children:
            child.classList.remove("dragged", "drop-target", "over")

        source_index = int(event.dataTransfer.getData("sourceIndex"))
        source = children[source_index]
        target = event.target.closest(".grid-item")
        target_index = children.index(target)

        if source_index == target_index:
            return

        # Helper function to insert or append
        def insert_or_append(element: JsDomElement, reference: JsDomElement | None) -> None:
            if reference is not None:
                self.root.insertBefore(element, reference)
            else:
                self.root.appendChild(element)

        def handle_insert() -> None:
            # If dragging from left to right
            if source_index < target_index:
                insert_or_append(source, target.nextSibling)
            # If dragging from right to left
            else:
                self.root.insertBefore(source, target)

        def handle_swap() -> None:
            source_next_sibling = source.nextSibling
            target_next_sibling = target.nextSibling

            # If source is right before target
            if source_next_sibling == target:
                self.root.insertBefore(target, source)
            # If target is right before source
            elif target_next_sibling == source:
                self.root.insertBefore(source, target)
            else:
                insert_or_append(source, target_next_sibling)
                insert_or_append(target, source_next_sibling)

        drop_behaviors: dict[DropBehavior, Callable[[], None]] = {
            "insert": handle_insert,
            "swap": handle_swap,
        }

        drop_behaviors[self.drop_behavior]()
