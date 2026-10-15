"""Generate the covered MuJoCo API and apply reproducible typing corrections.

The installed MuJoCo must match the release being prepared. Raw generation keeps
its diagnostics visible; successful parsing alone does not establish correctness.
Run the consumer checks and platform runtime audit before accepting the output.
"""

import ast
import importlib.metadata
import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from native_corrections import normalize_native
from wrapper_corrections import normalize_wrapper

NATIVE = {
    "_callbacks",
    "_constants",
    "_enums",
    "_errors",
    "_functions",
    "_render",
    "_specs",
    "_structs",
}
WRAPPERS = {
    "__init__",
    "renderer",
    "rollout",
    "viewer",
    "glfw.__init__",
    "cgl.__init__",
    "cgl.cgl",
    "egl.__init__",
    "egl.egl_ext",
    "rendering.__init__",
    "rendering.classic.__init__",
    "rendering.classic.renderer",
}


def generate_raw(output: Path) -> None:
    """Run the pinned generator for the public modules available on this host."""
    import mujoco

    if importlib.metadata.version("pybind11-stubgen") != "2.5.5":
        raise RuntimeError("Generation requires pybind11-stubgen 2.5.5")
    modules = [
        "mujoco",
        "mujoco.glfw",
        "mujoco.renderer",
        "mujoco.rollout",
        "mujoco.viewer",
    ]
    if mujoco.Renderer.__module__ != "mujoco.renderer":
        modules.append(mujoco.Renderer.__module__)
    if sys.platform == "darwin":
        modules += ["mujoco.cgl", "mujoco.cgl.cgl"]
    elif sys.platform.startswith("linux"):
        modules += ["mujoco.egl", "mujoco.egl.egl_ext"]
    else:
        raise RuntimeError("Generation is currently supported on macOS and Linux")
    environment = dict(os.environ, PYTHONHASHSEED="0")
    for module in modules:
        subprocess.run(
            [sys.executable, "-m", "pybind11_stubgen", module, "-o", str(output)],
            check=True,
            env=environment,
        )


def normalize(raw: Path, output: Path) -> None:
    """Write only covered modules, retaining version-specific generated signatures."""
    version = importlib.metadata.version("mujoco")
    source = raw / "mujoco"
    if not source.is_dir():
        raise ValueError(f"Expected a mujoco directory inside {raw}")
    for path in sorted(source.rglob("*.pyi")):
        relative = path.relative_to(source)
        name = ".".join(relative.with_suffix("").parts)
        if name not in NATIVE | WRAPPERS:
            continue
        module = "mujoco." + name.removesuffix(".__init__")
        if name == "__init__":
            module = "mujoco"
        text = path.read_text()
        if name in NATIVE:
            text = normalize_native(module, text)
        else:
            text = normalize_wrapper(module, text)
        ast.parse(text, filename=str(relative), feature_version=(3, 10))
        compile(text, str(relative), "exec", dont_inherit=True)
        if name in {"rendering.__init__", "rendering.classic.__init__"}:
            spec = importlib.util.find_spec(module)
            copyright_line = (
                "2026 DeepMind Technologies Limited"
                if spec is not None and spec.origin is not None
                else "2026 Xiaoyan Wang"
            )
        elif name.startswith("egl"):
            copyright_line = "2018 The dm_control Authors"
        elif name.startswith("glfw"):
            copyright_line = "2017 The dm_control Authors"
        elif name.startswith("cgl"):
            copyright_line = "2023 DeepMind Technologies Limited"
        elif name == "_specs":
            copyright_line = "2024 DeepMind Technologies Limited"
        else:
            copyright_line = "2022 DeepMind Technologies Limited"
        header = (
            f"# Copyright {copyright_line}\n"
            "# SPDX-License-Identifier: Apache-2.0\n"
            f"# Generated from MuJoCo {version} and modified for mujoco-stubs; see NOTICE.\n\n"
        )
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(header + text)
    (output / "py.typed").write_text("partial\n")


def main(output: Path, *, raw: Path | None = None) -> None:
    """Generate corrected stubs into a separate directory for review.

    Args:
        output: Destination package directory. Existing covered files are replaced.
        raw: Previously generated raw output, containing a mujoco directory.
            Omit to run the pinned generator with the installed MuJoCo version.
            The raw files must come from that same version.

    Generate on macOS for CGL and on Linux with EGL libraries for EGL. Copy the
    two corrected EGL files from the Linux output into the macOS output to form
    the complete package; review the changes before replacing src/mujoco-stubs.
    """
    os.environ.setdefault("MUJOCO_GL", "cgl" if sys.platform == "darwin" else "egl")
    if sys.platform.startswith("linux"):
        os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
    output.mkdir(parents=True, exist_ok=True)
    if raw is not None:
        normalize(raw, output)
    else:
        with TemporaryDirectory(prefix="mujoco-stubgen-") as directory:
            source = Path(directory)
            generate_raw(source)
            normalize(source, output)


if __name__ == "__main__":
    from cyclopts import App

    app = App()
    app.default(main)
    app()
