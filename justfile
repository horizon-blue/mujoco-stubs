# List the available local checks.
default:
    @just --list

# Build, inspect, install, and check the local package with all four type checkers.
validate:
    uv run --locked python scripts/validate.py

# Compare runtime bindings with stubs, allowing documented native/partial gaps.
audit:
    #!/usr/bin/env sh
    set -eu
    unset PYTHONPATH MYPYPATH VIRTUAL_ENV PYOPENGL_PLATFORM
    export PYTHONNOUSERSITE=1
    case "$(uname -s)" in
        Darwin) export MUJOCO_GL=cgl; platform=macos ;;
        Linux) export MUJOCO_GL=egl PYOPENGL_PLATFORM=egl; platform=linux ;;
        *) echo 'Runtime audit requires macOS (CGL) or Linux (EGL).' >&2; exit 1 ;;
    esac
    uv run --locked python -m mypy.stubtest mujoco \
        --mypy-config-file tests/runtime/mypy.ini \
        --allowlist tests/runtime/allowlist.txt \
        --allowlist "tests/runtime/allowlist-$platform.txt"

# Check the validation code and consumer examples without reformatting generated stubs.
lint:
    uv run --locked ruff check scripts tests
    uv run --locked ruff format --check scripts tests

# Build distributions for local inspection; nothing is uploaded.
build:
    uv build --force-pep517
