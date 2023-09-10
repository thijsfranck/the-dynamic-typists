import asyncio
from typing import TYPE_CHECKING

from controllers import App
from js import Event, document
from pyodide.ffi.wrappers import add_event_listener, remove_event_listener

if TYPE_CHECKING:
    from pyodide.ffi import JsDomElement


async def main() -> None:
    """Run the initial logic.

    This is a function as top-level await was removed in pyodide.
    """
    image_body: JsDomElement = document.getElementById("image-body")
    confirm_button: JsDomElement = document.getElementById("confirm-button")
    confirm_button_text: JsDomElement = document.getElementById("confirm-button-text")
    refresh_button: JsDomElement = document.getElementById("refresh-button")
    restart_button: JsDomElement = document.getElementById("restart-button")

    app = App(image_body)
    await app.load_captcha()

    is_loading_captcha = False
    is_posting_solution = False

    async def handle_load_captcha(_: Event) -> None:
        """
        Handle the load captcha event for the refresh button.

        When the user clicks the refresh button, this function is triggered. It requests the server
        to load a new captcha.

        While waiting for a response, a loading spinner is shown on the button. Once the response is
        received and the captcha is loaded, the loading spinner is removed.

        Parameters
        ----------
        _ : Event
            The event object, which is not used in this function but is typically passed by
            event handlers.

        Notes
        -----
        The function utilizes a nonlocal variable `is_loading_captcha` to prevent multiple
        concurrent requests when the user repeatedly clicks the button. This ensures that the
        application does not request another captcha until the previous one has been loaded.
        """
        nonlocal is_loading_captcha

        if is_loading_captcha:
            return

        is_loading_captcha = True
        refresh_button.classList.add("loading")

        try:
            await app.load_captcha()
        finally:
            is_loading_captcha = False
            refresh_button.classList.remove("loading")

        confirm_button_text.innerText = "CONFIRM"

        if confirm_button.classList.contains("solved"):
            confirm_button.classList.remove("solved")
            # Pyodide typings do not handle async event handlers, despite them working.
            add_event_listener(confirm_button, "click", handle_post_solution)  # type: ignore

    async def handle_post_solution(_: Event) -> None:
        """
        Handle the solution post event for the confirm button.

        When the user clicks the confirm button, this function is triggered. It sends the current
        solution to the server for validation. While waiting for a response, a loading spinner is
        shown on the button. Once the response is received, the button is updated to show whether
        the solution was correct or not.

        Parameters
        ----------
        _ : Event
            The event object, which is not used in this function but is typically passed by
            event handlers.

        Notes
        -----
        The function utilizes a nonlocal variable `is_posting_solution` to prevent multiple
        concurrent requests when the user repeatedly clicks the button. This ensures that the
        application does not send another request until the previous one has completed.

        If the solution is correct, the function updates the button's text to "SOLVED" and removes
        the event listener to prevent further submissions. If incorrect, the button's text is
        changed to "RETRY".
        """
        nonlocal is_posting_solution

        if is_posting_solution:
            return

        is_posting_solution = True
        confirm_button.classList.add("loading")

        solved = False

        try:
            solved = await app.post_solution()
        finally:
            is_posting_solution = False
            confirm_button.classList.remove("loading")

        if solved:
            confirm_button.classList.add("solved")
            confirm_button_text.innerText = "SOLVED"
            remove_event_listener(confirm_button, "click", handle_post_solution)  # type: ignore
        else:
            confirm_button_text.innerText = "RETRY"

    add_event_listener(confirm_button, "click", handle_post_solution)  # type: ignore
    add_event_listener(refresh_button, "click", handle_load_captcha)  # type: ignore
    add_event_listener(restart_button, "click", lambda _: app.reset())


asyncio.ensure_future(main())  # noqa: RUF006
