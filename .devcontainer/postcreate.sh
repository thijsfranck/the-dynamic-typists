#!/bin/sh

# Install dependencies
poetry install

# Install pre-commit hook
poetry run pre-commit install
