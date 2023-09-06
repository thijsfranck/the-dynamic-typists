#!/bin/sh

poetry run uvicorn server:APP --reload --port 3333
