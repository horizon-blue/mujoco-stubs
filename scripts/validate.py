"""Check the built package as an installed consumer would see it.

Run with ``uv run --locked python scripts/validate.py`` (or ``just validate``).
The validation has two stages:

1. Build a wheel and source archive, inspect their contents, and check that
   rebuilding the source archive produces the same wheel contents.
2. Install the wheel into a temporary environment without MuJoCo, then enable
   its runtime extra, run a small MuJoCo example, and check valid and deliberately
   invalid usage with all four type checkers.

The project environment supplies the validation tools; the temporary environment
contains only the built package and its requested dependencies. This separation
helps expose packaging mistakes that an editable development install can hide.

Builds and installs may download dependencies through uv. Temporary files are
cleaned up on success or failure; built distributions are copied to ``dist/``
after the artifact checks, before consumer checks run. Nothing is uploaded.
"""

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import zipfile
from email.parser import BytesParser
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "mujoco-stubs"
CHECKERS = ("mypy", "pyright", "ty", "pyrefly")
# Match accidental machine paths and generated object reprs, not author metadata.
PRIVATE_CONTENT = re.compile(
    r"/(?:Users|home)/[\w.-]+/|[A-Z]:\\Users\\[\w.-]+\\"
    r"|# value = .*\bat 0x[0-9a-fA-F]{8,}"
    r"|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"
    r"|(?:gh[pousr]_|github_pat_|sk-proj-)[A-Za-z0-9_]{20,}"
)


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run an argument list directly, without a shell, and capture diagnostics.

    Keep PATH so commands use the project's validation tools, but remove import
    and environment overrides that could redirect them to unrelated packages.
    Return nonzero exit codes to the caller: negative typing tests expect them.
    """
    env = os.environ.copy()
    for name in (
        "PYTHONPATH",
        "MYPYPATH",
        "VIRTUAL_ENV",
        "TY_CONFIG_FILE",
        "PYREFLY_CONFIG",
    ):
        env.pop(name, None)
    env["PYTHONNOUSERSITE"] = "1"
    return subprocess.run(
        command, cwd=cwd, env=env, text=True, capture_output=True, check=False
    )


def require_success(command: list[str], cwd: Path) -> None:
    """Fail with the command's diagnostics when a build or runtime check fails."""
    result = run(command, cwd)
    if result.returncode:
        raise RuntimeError(f"{' '.join(command)}\n{result.stdout}{result.stderr}")


def read_wheel(path: Path) -> dict[str, bytes]:
    """Read wheel members without extracting them into the working tree."""
    with zipfile.ZipFile(path) as archive:
        return {
            name: archive.read(name)
            for name in archive.namelist()
            if not name.endswith("/")
        }


def check_content(files: dict[str, bytes]) -> None:
    """Inspect UTF-8 archive members for stray files and invalid stub syntax.

    The private-content patterns catch common generator leaks, such as local
    paths and object representations; they are not a comprehensive secret scan.
    Stub contents are parsed and compiled for validation, never executed.
    """
    for name, content in files.items():
        assert not any(part.startswith(".") for part in Path(name).parts), name
        text = content.decode("utf-8")
        assert not PRIVATE_CONTENT.search(text), (
            f"Potential private/generated data in {name}"
        )
        if name.endswith(".pyi"):
            # Keep the syntax compatible with the package's Python 3.10 minimum.
            ast.parse(text, filename=name, feature_version=(3, 10))
            # Compilation also catches errors the AST parser permits, such as
            # misplaced future imports, without executing the resulting code.
            compile(text, name, "exec", dont_inherit=True)


def check_wheel(path: Path, expected: dict[str, bytes]) -> dict[str, bytes]:
    """Verify stub payload, partial marker, metadata, and pure-Python packaging."""
    files = read_wheel(path)
    check_content(files)
    payload = {
        name: data for name, data in files.items() if name.startswith(f"{PACKAGE}/")
    }
    assert payload == expected, f"Unexpected stub payload in {path.name}"
    # PEP 561's partial marker lets checkers consult the runtime package for
    # modules this stub package does not cover.
    assert payload[f"{PACKAGE}/py.typed"] == b"partial\n"
    metadata_names = [name for name in files if name.endswith(".dist-info/METADATA")]
    assert len(metadata_names) == 1
    metadata_name = metadata_names[0]
    dist_info = metadata_name.rsplit("/", 1)[0]
    assert all(name.startswith((f"{PACKAGE}/", f"{dist_info}/")) for name in files)
    metadata = BytesParser().parsebytes(files[metadata_name])
    assert metadata["Name"] == PACKAGE
    assert metadata["License-Expression"] == "Apache-2.0"
    assert set(metadata.get_all("License-File", [])) == {"LICENSE", "NOTICE"}
    for name in ("LICENSE", "NOTICE"):
        assert files[f"{dist_info}/licenses/{name}"] == (ROOT / name).read_bytes()
    requirements = metadata.get_all("Requires-Dist", [])
    assert any(req.startswith("typing-extensions>=4.12") for req in requirements)
    assert "numpy" in requirements
    assert metadata.get_all("Provides-Extra", []) == ["mujoco"]
    assert [req for req in requirements if req.startswith("mujoco")] == [
        "mujoco>=3.4.0,<3.5.0 ; extra == 'mujoco'"
    ]
    wheel_metadata = BytesParser().parsebytes(files[f"{dist_info}/WHEEL"])
    assert wheel_metadata["Root-Is-Purelib"] == "true"
    assert "py3-none-any" in wheel_metadata.get_all("Tag", [])
    return files


def build_and_check(work: Path) -> Path:
    """Build both distribution formats and check their contents against source.

    Build outputs go in the disposable ``work`` directory. Return the direct wheel
    for consumer tests, and copy both distributions into ``dist/`` for inspection.
    These checks cover packaging; consumer tests run separately afterwards.
    """
    # Compare against the source files, not just a file count: missing,
    # unexpected, or altered stubs must all fail the packaging check.
    expected = {
        path.relative_to(ROOT / "src").as_posix(): path.read_bytes()
        for path in (ROOT / "src" / PACKAGE).rglob("*")
        if path.is_file()
    }
    assert all(name.endswith((".pyi", "/py.typed")) for name in expected)
    direct_dir = work / "direct"
    source_dir = work / "source"
    rebuilt_dir = work / "rebuilt"
    # Force the declared PEP 517 backend for every build. Otherwise uv's direct
    # build fast path can use a different backend version from the archive build.
    require_success(
        ["uv", "build", "--force-pep517", "--wheel", "--out-dir", str(direct_dir)], ROOT
    )
    require_success(
        ["uv", "build", "--force-pep517", "--sdist", "--out-dir", str(source_dir)], ROOT
    )
    (wheel,) = direct_dir.glob("*.whl")
    (sdist,) = source_dir.glob("*.tar.gz")
    with tarfile.open(sdist) as archive:
        source_files = {}
        for member in archive.getmembers():
            if member.isfile():
                stream = archive.extractfile(member)
                assert stream is not None
                source_files[member.name] = stream.read()
    check_content(source_files)
    source_payload = {
        name.split("/src/", 1)[1]: data
        for name, data in source_files.items()
        if f"/src/{PACKAGE}/" in name
    }
    assert source_payload == expected, "Source archive lost or changed stubs"
    # Rebuild from the archive outside the checkout, so omitted source files
    # cannot be supplied accidentally by the working tree.
    require_success(
        [
            "uv",
            "build",
            "--force-pep517",
            str(sdist),
            "--wheel",
            "--out-dir",
            str(rebuilt_dir),
        ],
        work,
    )
    (rebuilt,) = rebuilt_dir.glob("*.whl")
    direct_files = check_wheel(wheel, expected)
    rebuilt_files = check_wheel(rebuilt, expected)
    # Compare unpacked member bytes: ZIP timestamps and compression are not
    # meaningful differences in what a user installs.
    differences = [
        name
        for name in direct_files.keys() | rebuilt_files.keys()
        if direct_files.get(name) != rebuilt_files.get(name)
    ]
    if differences:
        details = "\n".join(
            f"{name}: {direct_files.get(name, b'')[:1000]!r} != {rebuilt_files.get(name, b'')[:1000]!r}"
            for name in differences
        )
        raise AssertionError(f"Wheel round-trip differs:\n{details}")
    destination = ROOT / "dist"
    destination.mkdir(exist_ok=True)
    shutil.copy2(wheel, destination / wheel.name)
    shutil.copy2(sdist, destination / sdist.name)
    print(
        f"Artifacts: {len(expected) - 1} stubs, partial marker, metadata, and sdist round-trip passed",
        flush=True,
    )
    return wheel


def checker_command(name: str, python: Path, filename: str) -> list[str]:
    """Select a project checker, but resolve imports in the consumer environment.

    ``python`` is the temporary environment's interpreter, not the interpreter
    running this script. Each checker has a different flag for this selection.
    Structured or concise output lets ``error_locations`` compare diagnostics.
    """
    executable = shutil.which(name)
    if executable is None:
        raise RuntimeError(f"Missing {name}; run this script with uv run --locked")
    options = {
        "mypy": ["--strict", "--no-incremental", "--python-executable", str(python)],
        "pyright": ["--pythonpath", str(python), "--outputjson"],
        "ty": ["check", "--python", str(python), "--output-format", "concise"],
        "pyrefly": [
            "check",
            "--preset",
            "strict",
            "--python-interpreter-path",
            str(python),
            "--output-format",
            "json",
        ],
    }
    return [executable, *options[name], filename]


def error_locations(name: str, output: str) -> list[tuple[str, int]]:
    """Normalize checker errors to filename and one-based line number.

    Ignore wording and diagnostic codes, which differ between checkers, but
    retain duplicate locations so unexpected extra errors still fail the test.
    Pyright uses zero-based lines; the other selected formats use one-based lines.
    """
    if name == "pyright":
        result = json.loads(output)
        assert result["summary"]["filesAnalyzed"] > 0, "Pyright did not check any files"
        return [
            (Path(item["file"]).name, item["range"]["start"]["line"] + 1)
            for item in result["generalDiagnostics"]
            if item["severity"] == "error"
        ]
    if name == "pyrefly":
        return [
            (Path(item["path"]).name, item["line"])
            for item in json.loads(output)["errors"]
            if item["severity"] == "error"
        ]
    return [
        (Path(match[0]).name, int(match[1]))
        for match in re.findall(
            r"^(.+\.py):(\d+):(?:\d+:)? error(?:\[|:)", output, re.MULTILINE
        )
    ]


def check_consumers(wheel: Path, work: Path) -> None:
    """Exercise the installed wheel with real runtime and static typing examples.

    Use the same Python version as the validation runner, with runtime dependency
    versions constrained by the project lockfile. Copy fixtures outside the repo
    so local sources cannot satisfy imports from an incorrectly packaged wheel.
    The valid fixture must execute and type-check; the invalid fixture is only
    type-checked and must report errors exactly where marked with ``expect-error``.
    """
    environment = work / "environment"
    require_success(["uv", "venv", "--python", sys.executable, str(environment)], work)
    python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    constraints = work / "constraints.txt"
    # Export runtime versions, excluding dev tools and the local project itself.
    # Constraints pin dependencies if requested by the wheel; they do not install
    # extra packages that could conceal a missing dependency declaration.
    require_success(
        [
            "uv",
            "export",
            "--locked",
            "--no-dev",
            "--extra",
            "mujoco",
            "--no-emit-project",
            "--no-hashes",
            "--output-file",
            str(constraints),
        ],
        ROOT,
    )
    install = [
        "uv",
        "pip",
        "install",
        "--python",
        str(python),
        "--constraint",
        str(constraints),
    ]
    require_success([*install, str(wheel)], work)
    # Plain installs must provide the typing dependencies without the runtime.
    require_success(
        [
            str(python),
            "-I",
            "-c",
            "import numpy.typing, typing_extensions; "
            "from importlib.util import find_spec; "
            "assert find_spec('mujoco') is None",
        ],
        work,
    )
    print("Plain install: typing dependencies present; MuJoCo absent", flush=True)
    require_success([*install, f"{PACKAGE}[mujoco] @ {wheel.as_uri()}"], work)
    # Check installed dependency metadata before interpreting typing failures.
    require_success(["uv", "pip", "check", "--python", str(python)], work)
    for path in (ROOT / "tests" / "typing").glob("*.py"):
        shutil.copy2(path, work / path.name)
    # Pyright's strict mode is configured in a file rather than a CLI flag.
    (work / "pyrightconfig.json").write_text(json.dumps({"typeCheckingMode": "strict"}))
    # Python's isolated mode ignores user site-packages and import overrides.
    # Run only the valid example; deliberately invalid calls are never executed.
    require_success([str(python), "-I", "valid.py"], work)
    expected = {
        ("invalid.py", number)
        for number, line in enumerate((work / "invalid.py").read_text().splitlines(), 1)
        if "# expect-error" in line
    }
    assert expected, "No negative cases were collected"
    for name in CHECKERS:
        valid = run(checker_command(name, python, "valid.py"), work)
        if valid.returncode or error_locations(name, valid.stdout):
            raise RuntimeError(
                f"{name} rejected the valid example:\n{valid.stdout}{valid.stderr}"
            )
        invalid = run(checker_command(name, python, "invalid.py"), work)
        # A nonzero exit alone could be a crash or an unrelated import error.
        # Require the checker's normal error exit and the exact marked locations.
        # A failed overload call can produce several diagnostics on the same line;
        # every marked call must fail, with no errors on unmarked lines.
        if (
            invalid.returncode != 1
            or set(error_locations(name, invalid.stdout)) != expected
        ):
            raise RuntimeError(
                f"{name} did not report exactly the expected errors:\n{invalid.stdout}{invalid.stderr}"
            )
        print(
            f"{name}: valid calls accepted; {len(expected)} invalid calls rejected",
            flush=True,
        )
    print("Runtime: model creation, stepping, arrays, and MjSpec passed", flush=True)


def main() -> None:
    """Run artifact checks, then isolated runtime and typing checks."""
    with TemporaryDirectory(prefix="mujoco-stubs-validation-") as directory:
        work = Path(directory)
        wheel = build_and_check(work)
        check_consumers(wheel, work)
    print("Local package validation passed. Artifacts are in dist/.")


if __name__ == "__main__":
    main()
