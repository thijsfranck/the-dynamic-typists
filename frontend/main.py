import asyncio
from typing import TYPE_CHECKING

from controllers import App
from js import document
from pyodide.ffi.wrappers import add_event_listener

if TYPE_CHECKING:
    from pyodide.ffi import JsDomElement


async def main() -> None:
    """Run the initial logic.

    This is a function as top-level await was removed in pyodide.
    """
    image_body: JsDomElement = document.getElementById("image-body")
    confirm_button: JsDomElement = document.getElementById("confirm-button")
    refresh_button: JsDomElement = document.getElementById("refresh-button")

    app = App(image_body)
    await app.load_captcha()

    add_event_listener(confirm_button, "click", lambda _: app.print_solution())
    add_event_listener(refresh_button, "click", lambda _: app.reset())


asyncio.ensure_future(main())  # noqa: RUF006
