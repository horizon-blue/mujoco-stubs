# mujoco-stubs

An unofficial stub-only package providing type hints for [MuJoCo](https://github.com/google-deepmind/mujoco), a physics engine for robotics and biomechanics.

The stubs files were automatically generated using [pybind11-stubgen](https://github.com/pybind/pybind11-stubgen).

This release targets MuJoCo 3.4 and accepts `mujoco>=3.4.0,<3.5.0`, allowing patch releases within that series. However, since the stubs are auto-generated, they may not be perfectly accurate or complete. Use them as a reference, but always consult the official MuJoCo documentation for the most up-to-date and accurate information.

The package is partial. Graphics typing focuses on `Renderer`, viewer handles,
and public `GLContext` operations. Direct OpenGL/EGL/CGL bindings and internal
modules such as `mujoco._simulate` and `mujoco.gl_context` remain partially or
wholly uncovered.

In addition, the stubs have been audited on both macOS (CGL) and Linux with EGL libraries available. Windows runtime auditing is not yet covered.

## Usage

To use the stubs, simply install the `mujoco-stubs` package alongside the `mujoco` package in your Python environment. For example:

```bash
pip install git+https://github.com/horizon-blue/mujoco-stubs.git
```

Type checkers that support [PEP 561](https://peps.python.org/pep-0561/#stub-only-packages) will automatically use the stubs when you import the `mujoco` package in your code. You can then benefit from improved type checking and autocompletion in your IDE.

## Development

With [uv](https://docs.astral.sh/uv/) installed, run the package validation:

```bash
uv run --locked --python 3.12 python scripts/validate.py
```

If you use [just](https://just.systems/), `just validate` runs the same checks,
`just lint` checks the validation code, and `just build` builds distributions.

`just audit` runs mypy's `stubtest` with [commented allowlists](tests/runtime/allowlist.txt)
for known native-binding differences and partial coverage.
