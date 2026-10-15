# mujoco-stubs

[![PyPI Python Version][pypi-versions-badge]][pypi]
[![PyPI version][pypi-badge]][pypi]

[pypi-versions-badge]: https://img.shields.io/pypi/pyversions/mujoco-stubs
[pypi-badge]: https://img.shields.io/pypi/v/mujoco-stubs
[pypi]: https://pypi.org/project/mujoco-stubs/

An unofficial stub-only package providing type hints for [MuJoCo](https://github.com/google-deepmind/mujoco), a physics engine for robotics and biomechanics.

The stubs were generated from MuJoCo 3.9.0 using [pybind11-stubgen](https://github.com/pybind/pybind11-stubgen) and corrected with the generation scripts in this repository. They are a best-effort aid to type checking and autocompletion, and may be incomplete or inaccurate. Consult the [official MuJoCo documentation](https://mujoco.readthedocs.io/en/stable/) for runtime behavior.

## Usage

Python 3.10 or newer is required. Install from PyPI:

```bash
pip install mujoco-stubs
```

This installs the stubs and their typing dependencies without installing or
constraining MuJoCo. To also install a compatible MuJoCo runtime, use the extra:

```bash
pip install "mujoco-stubs[mujoco]"
```

The extra requires `mujoco>=3.9.0,<3.10.0` and may change the installed MuJoCo
version to satisfy that range. Type checkers that support
[PEP 561](https://peps.python.org/pep-0561/#stub-only-packages) discover the stubs
automatically when your code imports `mujoco`.

The package is partial. Graphics typing focuses on `Renderer`, viewer handles,
and public `GLContext` operations. Direct OpenGL/EGL/CGL bindings and internal
modules such as `mujoco._simulate` and the `gl_context` backend selectors remain
partially or wholly uncovered.

The stubs have been audited on both macOS (CGL) and Linux with EGL libraries
available. Windows runtime auditing is not yet covered.

## Versioning

The version of this package follows `{mujoco_version}.{stub_revision}`. For example, `3.9.0.1` is
stub revision 1 generated from MuJoCo 3.9.0; `3.9.0.2` would contain further stub
corrections. This release targets the MuJoCo 3.9 series. The optional `mujoco`
extra enforces that version range; a plain installation leaves runtime version
selection to you. The stub version number alone does not constrain MuJoCo.

## Development

With [uv](https://docs.astral.sh/uv/) installed, run the package validation:

```bash
uv run --locked --python 3.12 python scripts/validate.py
```

If you use [just](https://just.systems/), `just validate` runs the same checks,
`just lint` checks the validation code, and `just build` builds distributions.

`just audit` runs mypy's `stubtest` with [commented allowlists](https://github.com/horizon-blue/mujoco-stubs/blob/main/tests/runtime/allowlist.txt)
for known native-binding differences and partial coverage.

## License

Licensed under [Apache-2.0](https://github.com/horizon-blue/mujoco-stubs/blob/main/LICENSE).
See [NOTICE](https://github.com/horizon-blue/mujoco-stubs/blob/main/NOTICE) for
MuJoCo and dm_control attribution and the origin of the generated declarations.
