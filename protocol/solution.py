from typing import TypedDict


class SolutionRequest(TypedDict):
    """Request body for when the user submits a solution to the server."""

    solution: list[int | float | tuple[int, float]]
