# mujoco-stubs

[![PyPI Python Version][pypi-versions-badge]][pypi]
[![PyPI version][pypi-badge]][pypi]
[![PyPI Types][pypi-types-badge]][pypi]

[pypi-versions-badge]: https://img.shields.io/pypi/pyversions/mujoco-stubs
[pypi-badge]: https://img.shields.io/pypi/v/mujoco-stubs
[pypi-types-badge]: https://img.shields.io/pypi/types/mujoco-stubs
[pypi]: https://pypi.org/project/mujoco-stubs/

An unofficial stub-only package providing type hints for [MuJoCo](https://github.com/google-deepmind/mujoco), a physics engine for robotics and biomechanics.

The project provides separate, version-matched stub releases for the MuJoCo
3.4–3.17 series. This release targets MuJoCo 3.17.0; for an older MuJoCo
installation, choose the corresponding stub release.

## Usage

Python 3.10 or newer is required. Install the latest stubs from PyPI:

```bash
pip install mujoco-stubs
```

This installs the stubs and their typing dependencies without installing or
constraining MuJoCo. To select stubs for an existing MuJoCo installation, choose
the matching version. For example, for MuJoCo 3.14.0:

```bash
pip install "mujoco-stubs==3.14.0.*"
```

The wildcard selects the latest stub revision for MuJoCo 3.14.0.

To install the latest stubs together with a compatible MuJoCo runtime, use the
extra:

```bash
pip install "mujoco-stubs[mujoco]"
```

The extra requires `mujoco>=3.17.0,<3.18.0` and may change the installed MuJoCo
version to satisfy that range. Type checkers that support
[PEP 561](https://peps.python.org/pep-0561/#stub-only-packages) discover the stubs
automatically when your code imports `mujoco`.

### Versioning

The version of this package follows `{mujoco_version}.{stub_revision}`. For example, `3.17.0.1` is
stub revision 1 generated from MuJoCo 3.17.0; `3.17.0.2` would contain further stub
corrections. This release targets the MuJoCo 3.17 series. The optional `mujoco`
extra enforces that version range; a plain installation leaves runtime version
selection to you. The stub version number alone does not constrain MuJoCo.

### Coverage and limitations

The package provides partial coverage of MuJoCo's Python API. The stubs are
produced with [pybind11-stubgen](https://github.com/pybind/pybind11-stubgen) and
corrected by the generation scripts in this repository. They may still be
incomplete or inaccurate; consult the
[official documentation](https://mujoco.readthedocs.io/en/stable/) for runtime
behavior.

Some dynamic array accesses retain an unspecified dtype. Array shapes and
writeability are not enforced by the annotations.

Graphics typing focuses on `Renderer`, viewer handles, and public `GLContext`
operations. Direct OpenGL/EGL/CGL bindings and internal modules such as
`mujoco._simulate` and the `gl_context` backend selectors remain partially or
wholly uncovered.

The stubs have been audited on macOS (CGL) and Linux with EGL libraries available.
They are expected to work on Windows, but have not yet been tested there.

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
