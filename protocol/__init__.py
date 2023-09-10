"""
The `protocol` module provides data model classes related to the CAPTCHA API.

These classes are designed for use by both frontend and backend applications.
"""
from .solution import (
    Solution,
    SolutionCodeRequest,
    SolutionCodeResponse,
    SolutionRequest,
    SolutionResponse,
)
from .tiles import TilesResponse

__all__ = [
    "Solution",
    "SolutionRequest",
    "SolutionResponse",
    "TilesResponse",
    "SolutionCodeRequest",
    "SolutionCodeResponse",
]
