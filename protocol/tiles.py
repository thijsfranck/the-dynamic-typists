from typing_extensions import TypedDict


class TilesResponse(TypedDict):
    """A structured representation of the CAPTCHA challenge response.

    Represents the server's response to a request for a CAPTCHA challenge. The response
    contains the type of the CAPTCHA (determining the layout or nature of the challenge)
    and a list of image URIs that constitute the tiles for that challenge.

    Attributes
    ----------
    type : str
        The type of CAPTCHA challenge. This determines how the tiles should be
        arranged or manipulated. Examples include 'grid', 'rows', and 'circles'.
    tiles : list[str]
        A list of Base64-encoded image URIs that represent the individual tiles for
        the CAPTCHA challenge. These tiles are meant to be displayed or manipulated
        as per the challenge type.

    Example
    -------
    ```json
    {
        "type": "grid",
        "tiles": ["...", "..."]
    }
    ```
    """

    type: str
    tiles: list[str]
