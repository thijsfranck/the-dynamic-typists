# Protocol

The `protocol` module standardizes API request and response types for our CAPTCHA project. Making the best use out of our full Python stack, we ensure type consistency across the backend and frontend. This allows the static type checker to identify breaking changes and protocol deviations, a crucial feature when frontend and backend are developed by different people.

## Design Choices

The protocol module focuses on detailed and user-friendly types. Each API endpoint has corresponding request and response types. All types are structured as JSON-compatible Python `dicts`. For compatibility with FastAPI, we use `TypedDict` from the `typing_extensions` module.

## Types

The table below outlines each API endpoint and its associated protocol types:

| API Endpoint   | File          | Request           | Response           |
| -------------- | ------------- | ----------------- | ------------------ |
| `api/solution` | `solution.py` | `SolutionRequest` | `SolutionResponse` |
| `api/tiles`    | `tiles.py`    | N/A               | `TilesResponse`    |

> **Note:** The "N/A" in the table indicates that the particular API endpoint does not have a request or response type associated with it.

## Usage

Protocol types can be imported directly from the `protocol` module as follows:

```python
from protocol import SolutionRequest, SolutionResponse
```
