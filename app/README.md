# App

The `app` module is the backbone of our CAPTCHA project, housing both the backend logic for CAPTCHA generation and the necessary API endpoints for frontend interaction.

## Contents

This README includes the following sections:

- [Contents](#contents)
- [Features](#features)
- [Library and Framework Choices](#library-and-framework-choices)
- [Components](#components)
- [State Management](#state-management)

## Features

- **Generates various types of CAPTCHA challenges** using [`Pillow`](https://python-pillow.org/) for image manipulation.
- **Serves the frontend** to the user using [`FastAPI`](https://fastapi.tiangolo.com/)
- **Provides various API endpoints** to facilitate communication between frontend and backend.
- **Tracks user session state** in order to check the validity of user submitted solutions.

## Library and Framework Choices

Our `app` module relies on `Pillow` for image scrambling and watermarking, and on `FastAPI` to act as a web server.

### Pillow

`Pillow` is a fork of the Python Imaging Library (PIL) and stands out for its user-friendly approach to image processing. It supports a wide array of image formats and offers tools for tasks like image resizing, filtering, and drawing.

We chose `Pillow` as our image processing library since all of us had used Pillow as part of the Code Jam qualifier, and therefore all of us had some experience with it. While there are speedier options like [`opencv`](https://opencv.org/), we prioritized quick functionality development over performance optimization at the start of the project. Despite this, our CAPTCHA challenges load quickly, maintaining a smooth user experience.

### FastAPI

`FastAPI` is a modern, fast (high-performance) web framework for building APIs with Python, based on standard Python type hints. It provides automatic data validation, serialization, and asynchronous request handling.

We opted for `FastAPI` due to its performance, user-friendly nature, and compatibility with Python type hints. As our project emphasizes type safety, FastAPI's built-in request validation and serialization was a good fit.

## Components

The `app` module has the following main components:

### Server

The `server` module manages interactions between the frontend and backen. Additionally, it is responsible for serving the frontend to the user.

The table below lists all routes provided by the server. Note that all API endpoints must be prefixed with `/api`.

| Path            | Request Type | Description                                                                |
| --------------- | ------------ | -------------------------------------------------------------------------- |
| `/`             | `GET`        | Entrypoint for the frontend web app serving `index.html`.                  |
| `/api/tiles`    | `GET`        | Retrieves the scrambled image tiles, aiding frontend image reconstruction. |
| `/api/solution` | `POST`       | Receives the CAPTCHA solution details from the frontend for verification.  |

Please refer to the [`protocol`](../protocol/) module for data types expected and returned by the API.

### Picture

Maintains the state for a CAPTCHA challenge including the original picture, tiles composing the scrambled image and the five-character watermark code. The `Picture` class uses the `Tile` class to keep track of the internal state for each part of the scrambled image, such as original position and rotation. Finally, the `Picture` class provides functionality for watermarking images.

### Scrambler

Provides various functions for scrambling an image. Each scrambler function expects a `Picture` instance as input and stores the generated tiles as part of that instance. Each

We implemented the following types of scramblers:

| Scrambler Type | Description                                                                |
| -------------- | -------------------------------------------------------------------------- |
| `circle`       | Splits the image into 5 concentric rings and rotates each ring at random.  |
| `rows`         | Splits the image into 7 rows and rearranges the rows at random.            |
| `tiles`        | Splits the image into 4 tiles. Tiles are rearranged and rotated at random. |

### Solver

The `solver` module provides functions that produce the expected `Solution` for a given `Picture` instance. Solutions can be in different formats depending on the type of CAPTCHA challenge. The different solution formats have been captured as part of the [`protocol`](../protocol/) module.

## State Management

The `server` module manages user sessions for active CAPTCHA challenges:

1. **Session Creation**: On their first CAPTCHA request via the api/tiles endpoint, users receive a unique session ID.
2. **Storage**: This ID and associated state are stored in a global variable. The ID is sent to the user as a cookie.
3. **Refresh**: If users request a new challenge via the same endpoint, their previous session is deleted and a new one begins.
