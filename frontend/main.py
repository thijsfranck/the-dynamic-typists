import asyncio

from controllers import App
from js import document
from pyodide.ffi.wrappers import add_event_listener


async def main() -> None:
    """Run the initial logic.

    This is a function as top-level await was removed in pyodide.
    """
    image_body: object = document.getElementById("image-body")
    confirm_button: object = document.getElementById("confirm-button")
    controller_select: object = document.getElementById("controller-select")
    refresh_button: object = document.getElementById("refresh-button")

    app = App(image_body)
    await app.set_controller(controller_select.value)

    add_event_listener(
        controller_select,
        "change",
        lambda event: app.set_controller(event.target.value),
    )
    add_event_listener(confirm_button, "click", lambda _: app.print_solution())
    add_event_listener(refresh_button, "click", lambda _: app.reset())


asyncio.ensure_future(main())  # noqa: RUF006
