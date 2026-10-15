# List the available local checks.
default:
    @just --list

# Build, inspect, install, and check the local package with all four type checkers.
validate:
    uv run --locked python scripts/validate.py

# Check the validation code and consumer examples without reformatting generated stubs.
lint:
    uv run --locked ruff check scripts tests
    uv run --locked ruff format --check scripts tests

# Build distributions for local inspection; nothing is uploaded.
build:
    uv build --force-pep517
