from typing import TypedDict

Solution = list[int | float | tuple[int, float]]


class SolutionRequest(TypedDict):
    """Request body for when the user submits a solution to the server."""

    solution: Solution


class SolutionResponse(TypedDict):
    """Response body for when the user submits a solution to the server."""

    solved: bool
