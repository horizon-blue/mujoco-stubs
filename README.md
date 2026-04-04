# mujoco-stubs

An unofficial stub-only package providing type hints for [MuJoCo](https://github.com/google-deepmind/mujoco), a physics engine for robotics and biomechanics.

The stubs files were automatically generated using [pybind11-stubgen](https://github.com/pybind/pybind11-stubgen).

The version of this stub package is set to match the version of MuJoCo it was generated from (e.g. for `mujoco==3.4.0`, the corresponding stub package is `mujoco-stubs==3.4.0`). However, since the stubs are auto-generated, they may not be perfectly accurate or complete. Use them as a reference, but always consult the official MuJoCo documentation for the most up-to-date and accurate information.

## Usage

To use the stubs, simply install the `mujoco-stubs` package alongside the `mujoco` package in your Python environment. For example:

```bash
pip install git+https://github.com/horizon-blue/mujoco-stubs.git
```

Type checkers that support [PEP 561](https://peps.python.org/pep-0561/#stub-only-packages) will automatically use the stubs when you import the `mujoco` package in your code. You can then benefit from improved type checking and autocompletion in your IDE.
