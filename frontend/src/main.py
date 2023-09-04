import math

from js import document
from pyodide.ffi.wrappers import JsDomElement, add_event_listener


class RotationController:
    def __init__(self, element: JsDomElement, rotation_steps: int = 360) -> None:
        """
        Create a new `RotationController` for the given `element`.

        Parameters
        ----------
        - element (JsDomElement): The element rotated by this instance
        - rotation_steps (int): The number of positions to which the element can snap during rotation, evenly divided around the circle. Defaults to 360.
        """
        self.element: JsDomElement = element
        self.rotation_steps: int = rotation_steps
        self._current_rotation: int = 0

    def destroy(self):
        """Remove applied transformation from target element."""
        self.element.style.removeProperty("transform")

    def reset(self):
        """Rotate the element to 0 degrees."""
        self.rotate(0)

    def rotate(self, degrees: int):
        """
        Rotate the element by the given `degrees`.

        Parameters
        ----------
        - degrees (int): The number of degrees by which the image should be rotated (0 - 360)
        """
        self._current_rotation = degrees % 360
        self.element.style.transform = f"rotate({self._current_rotation}deg)"

    def step_clockwise(self):
        """Rotate the element one step in the clockwise direction."""
        self.rotate(self._current_rotation + 360 / self.rotation_steps)

    def step_counter_clockwise(self):
        """Rotate the element one step in the counter-clockwise direction."""
        self.rotate(self._current_rotation - 360 / self.rotation_steps)

    @property
    def current_rotation(self) -> int:
        """Return the number of degrees by which the element is currently rotated (0-360)."""
        return self._current_rotation


class DragRotationController(RotationController):
    def __init__(self, element: JsDomElement, rotation_steps: int = 360) -> None:
        """
        Create a new `DragRotationController` for the given `element`.

        Parameters
        ----------
        - element (JsDomElement): The element rotated by this instance
        - rotation_steps (int): The number of positions to which the element can snap during rotation, evenly divided around the circle. Defaults to 360.
        """
        super().__init__(element, rotation_steps)

        self.element: JsDomElement = element
        self._center: dict[str, int] = {"x": 0, "y": 0}
        self._is_rotating: bool = False

        add_event_listener(self.element, "mousedown", self._on_mouse_down)

    def _on_mouse_down(self, event):
        """Enable the rotating state and the current element center on left-click."""
        event.preventDefault()

        bounding_rect = self.element.getBoundingClientRect()

        self._center["x"] = bounding_rect.left + bounding_rect.width / 2
        self._center["y"] = bounding_rect.top + bounding_rect.height / 2

        self._is_rotating = True
        self.element.classList.add("active")

        add_event_listener(document, "mousemove", self._on_mouse_move)
        add_event_listener(document, "mouseup", self._on_mouse_up)

    def _on_mouse_move(self, event):
        """Calculate the rotation angle when the user moves their mouse while rotating the image."""
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

    def _on_mouse_up(self, _):
        """Disable the rotating state when the left mouse button is released."""
        self._is_rotating = False
        self.element.classList.remove("active")


class ClickRotationController(RotationController):
    def __init__(self, element: JsDomElement, rotation_steps: int = 360) -> None:
        """
        Create a new `ClickRotationController` for the given `element`.

        Parameters
        ----------
        - element (JsDomElement): The element rotated by this instance
        - rotation_steps (int): The number of positions to which the element can snap during rotation, evenly divided around the circle. Defaults to 360.
        """
        super().__init__(element, rotation_steps)
        add_event_listener(self.element, "click", self._on_left_click)

    def _on_left_click(self, event):
        """Handles the left-click event."""
        event.preventDefault()
        self.step_clockwise()


class RotatingImagesController:
    def __init__(self, root: JsDomElement) -> None:
        """
        Create a new `RotatingCirclesController` instance.

        Parameters
        ----------
        - root (JsDomElement): The root element in which to render the images
        """
        self.root: JsDomElement = root
        self._controllers: list[RotationController] = []

    def render(self, images: list[str]):
        """Render the given images and attach RotationController instances to each image.

        Parameters
        ----------
        - images (List[str]): List of base64 encoded images
        """
        self.root.classList.add("rotating-images")
        for image in images:
            img_element = document.createElement("img")
            img_element.src = f"data:image/png;base64,{image}"
            img_element.classList.add("rotatable-image")

            self._controllers.append(DragRotationController(img_element, rotation_steps=360))
            self.root.appendChild(img_element)

    def destroy(self):
        """Destroy each active controller and remove all child elements from the root element."""
        self.root.classList.remove("rotating-images")

        # Destroy each active controller
        while len(self._controllers):
            self._controllers.pop().destroy()

        # Remove all child elements from the root element
        while element := self.root.firstChild:
            self.root.removeChild(element)

    def reset(self):
        """Reset every active controller to its original state."""
        for controller in self._controllers:
            controller.reset()

    @property
    def solution(self):
        """The current solution as a list of the number of degrees by which each element is rotated."""
        return [controller.current_rotation for controller in self._controllers]


class DragDropGridController:
    def __init__(self, root: JsDomElement, columns: int = 1, drop_behavior: str = "insert") -> None:
        self.root: JsDomElement = root
        self.columns: int = columns
        self.drop_behavior: str = drop_behavior
        self._images: list[str] = []

    def render(self, images: list[str]):
        self._images = images
        self.root.classList.add("grid-container")
        self.root.style.setProperty("--columns", str(self.columns))

        for index, image in enumerate(self._images):
            grid_item_element = document.createElement("div")
            grid_item_element.classList.add("grid-item")
            grid_item_element.setAttribute("draggable", "true")
            grid_item_element.setAttribute("data-index", str(index))
            grid_item_element.innerText = str(index)

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

    def destroy(self):
        self.root.classList.remove("grid-container")
        self.root.style.removeProperty("--columns")

        while element := self.root.firstChild:
            self.root.removeChild(element)

    def reset(self):
        """Reset the grid to its original state."""
        self.destroy()
        self.render(self._images)

    @property
    def solution(self) -> list[int]:
        """
        Get the current order of images in the grid.

        Returns
        -------
        List[int]: The order of images as an array of indices.
        """
        return [int(child.getAttribute("data-index")) for child in list(self.root.children)]

    def _on_drag_start(self, event):
        source = event.target.closest(".grid-item")
        source_index = list(self.root.children).index(source)

        event.dataTransfer.setData("sourceIndex", str(source_index))
        event.dataTransfer.setDragImage(source.getElementsByTagName("img")[0], 0, 0)
        event.dataTransfer.dropEffect = "move"

        # Highlight the current dragged element
        source.classList.add("dragged")

        # Highlight potential drop targets
        for child in self.root.children:
            if child != source:
                child.classList.add("drop-target")

    def _on_drag_enter(self, event):
        event.preventDefault()
        target = event.target.closest(".grid-item")
        if target and not target.classList.contains("dragged"):
            target.classList.add("over")

    def _on_drag_over(self, event):
        event.preventDefault()

    def _on_drag_leave(self, event):
        target = event.target.closest(".grid-item")
        if target and not target.contains(event.relatedTarget):
            target.classList.remove("over")

    def _on_drag_end(self, event):
        event.preventDefault()
        for child in self.root.children:
            child.classList.remove("dragged", "drop-target", "over")

    def _on_drop(self, event):
        event.preventDefault()

        for child in self.root.children:
            child.classList.remove("dragged", "drop-target", "over")

        source_index = int(event.dataTransfer.getData("sourceIndex"))
        source = self.root.children[source_index]
        target = event.target.closest(".grid-item")
        target_index = list(self.root.children).index(target)

        if source_index == target_index:
            return

        def handle_insert():
            # If dragging from left to right
            if source_index < target_index:
                if target.nextSibling:
                    self.root.insertBefore(source, target.nextSibling)
                else:
                    self.root.appendChild(source)
            # If dragging from right to left
            else:
                self.root.insertBefore(source, target)

        def handle_swap():
            source_next_sibling = source.nextSibling
            target_next_sibling = target.nextSibling

            # If source is right before target
            if source_next_sibling == target:
                self.root.insertBefore(target, source)
            # If target is right before source
            elif target_next_sibling == source:
                self.root.insertBefore(source, target)
            else:
                self.root.insertBefore(source, target_next_sibling)
                self.root.insertBefore(target, source_next_sibling)

        drop_behaviors = {"insert": handle_insert, "swap": handle_swap}

        drop_behaviors[self.drop_behavior]()


class ImageGridController(DragDropGridController):
    def __init__(self, root: JsDomElement, columns: int = 2, rotation_steps: int = 4) -> None:
        """
        Create a new `ImageGridController` instance.

        Parameters
        ----------
        - root (JsDomElement): The root element in which to render the images.
        - columns (int): The number of columns in the grid. Defaults to 2.
        - rotation_steps (int): The number of rotation steps for each image. Defaults to 4.
        """
        super().__init__(root, columns=columns, drop_behavior="swap")

        self.rotation_steps = rotation_steps
        self._controllers = []

    def render(self, images: list[str]):
        """Render the grid with the provided images and attach rotation controllers to each element.

        Parameters
        ----------
        - images (List[str]): The images to be rendered.
        """
        super().render(images)

        children = list(self.root.children)

        for child in children:
            controller = ClickRotationController(child, rotation_steps=self.rotation_steps)
            self._controllers.append(controller)

    def destroy(self):
        """Remove all the grid items, destroy all rotation controllers and reset the root styles."""
        super().destroy()

        while len(self._controllers):
            self._controllers.pop().destroy()

    def reset(self):
        """Reset the grid to its initial state."""
        super().reset()
        for controller in self._controllers:
            controller.reset()

    @property
    def solution(self) -> list[tuple[int, int]]:
        """The current solution as a list of tuples that contain:
        - The current position of the element on the grid, and
        - The number of degrees by which each element is rotated.

        Returns
        -------
        List[Tuple[int, int]]: List of tuples describing the position and rotation of each element.
        """
        children = list(self.root.children)
        return [
            (children.index(controller.element), controller.current_rotation)
            for controller in self._controllers
        ]


image_body: JsDomElement = document.getElementById("image-body")
confirm_button: JsDomElement = document.getElementById("confirm-button")
controller_select: JsDomElement = document.getElementById("controller-select")
refresh_button: JsDomElement = document.getElementById("refresh-button")


controller_factories = {
    "grid": ImageGridController,
    "rows": DragDropGridController,
    "circles": RotatingImagesController,
}

active_controller = None


def fetch_images():
    return [
        "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
        "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
        "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
        "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII",
    ]


def set_controller(controller_name: str, root: JsDomElement):
    global active_controller

    if active_controller is not None:
        active_controller.destroy()

    active_controller = controller_factories[controller_name](root)

    images = fetch_images()

    active_controller.render(images)


add_event_listener(
    controller_select,
    "change",
    lambda event: set_controller(event.target.value, image_body),
)
add_event_listener(confirm_button, "click", lambda _: print(active_controller.solution))
add_event_listener(refresh_button, "click", lambda _: active_controller.reset())

set_controller(controller_select.value, image_body)
