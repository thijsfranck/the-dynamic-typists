#!/bin/sh

poetry run uvicorn app.server:APP --reload
