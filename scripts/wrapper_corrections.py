"""Restore curated wrapper types while retaining each generated runtime surface.

Call ``normalize_wrapper`` inside the environment containing the MuJoCo version
being generated. This helper edits only supplied text and does not write files.
Native extension normalization and release headers belong to the caller.
"""

import ast
import importlib
import inspect
import re
from collections.abc import Callable


def _positions(text: str) -> list[int]:
    """Locate source lines for surgical edits without rewriting docstrings."""
    positions = [0]
    for line in text.splitlines(keepends=True):
        positions.append(positions[-1] + len(line))
    return positions


def _span(node: ast.AST, positions: list[int]) -> tuple[int, int]:
    """Get a node's source range in generated ASCII signatures."""
    return (
        positions[node.lineno - 1] + node.col_offset,
        positions[node.end_lineno - 1] + node.end_col_offset,
    )


def _apply(text: str, edits: list[tuple[int, int, str]]) -> str:
    """Apply nonoverlapping edits while preserving surrounding source bytes."""
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text


def _imports(text: str, statements: list[str]) -> str:
    """Add required imports after the docstring and any future imports."""
    tree = ast.parse(text)
    lines = text.splitlines(keepends=True)
    insertion = 0
    for node in tree.body:
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            insertion = node.end_lineno
        elif isinstance(node, ast.ImportFrom) and node.module == "__future__":
            insertion = node.end_lineno
        else:
            break
    missing = [
        statement + "\n"
        for statement in statements
        if statement not in text.splitlines()
    ]
    lines[insertion:insertion] = missing
    return "".join(lines)


def _repair_annotations(text: str, replacements: dict[str, str]) -> str:
    """Repair known malformed annotation leaves without touching signatures."""

    class Repair(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name) -> ast.AST:
            return (
                ast.parse(replacements[node.id], mode="eval").body
                if node.id in replacements
                else node
            )

        def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
            name = ast.unparse(node)
            return (
                ast.parse(replacements[name], mode="eval").body
                if name in replacements
                else self.generic_visit(node)
            )

        def visit_Call(self, node: ast.Call) -> ast.AST:
            if (
                ast.unparse(node.func) in ("ForwardRef", "typing.ForwardRef")
                and node.args
                and isinstance(node.args[0], ast.Constant)
            ):
                return self.visit(ast.parse(node.args[0].value, mode="eval").body)
            return self.generic_visit(node)

    positions = _positions(text)
    edits = []
    tree = ast.parse(text)
    annotations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.arg) and node.annotation is not None:
            annotations.append(node.annotation)
        elif (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.returns is not None
        ):
            annotations.append(node.returns)
        elif isinstance(node, ast.AnnAssign):
            annotations.append(node.annotation)
    for annotation in annotations:
        original = ast.dump(annotation)
        start, end = _span(annotation, positions)
        repaired = Repair().visit(annotation)
        if ast.dump(repaired) != original:
            edits.append((start, end, ast.unparse(repaired)))
    return _apply(text, edits)


def _annotate(
    text: str, rules: dict[tuple[str, str], tuple[str | None, dict[str, str]]]
) -> str:
    """Fill known missing types, retaining all generated parameters/defaults."""
    positions = _positions(text)
    edits = []
    for cls in ast.parse(text).body:
        if not isinstance(cls, ast.ClassDef):
            continue
        for method in cls.body:
            if not isinstance(method, ast.FunctionDef):
                continue
            returns, arguments = rules.get((cls.name, method.name), (None, {}))
            for argument in [
                *method.args.posonlyargs,
                *method.args.args,
                *method.args.kwonlyargs,
            ]:
                if argument.annotation is None and argument.arg in arguments:
                    start, end = _span(argument, positions)
                    edits.append((end, end, ": " + arguments[argument.arg]))
            if method.returns is None and returns is not None:
                # pybind11-stubgen emits one-line function headers, including
                # Python wrappers; fail explicitly if that assumption changes.
                line = text.splitlines()[method.lineno - 1]
                if not line.rstrip().endswith(":"):
                    raise ValueError(
                        f"Expected a single-line signature for {cls.name}.{method.name}"
                    )
                end = positions[method.lineno - 1] + line.rfind(":")
                edits.append((end, end, " -> " + returns))
    return _apply(text, edits)


def _aliases(text: str, module_name: str, names: set[str]) -> str:
    """Restore aliases from the matching Python source rather than object reprs."""
    module = importlib.import_module(module_name)
    source = inspect.getsource(module)
    expressions = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name, value = node.target.id, node.value
        elif (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            name, value = node.targets[0].id, node.value
        else:
            continue
        if name in names and value is not None:
            expression = ast.unparse(value)
            expression = re.sub(
                r"(?<![\w.])(Union|Sequence|Callable|Tuple|Optional)\b",
                r"typing.\1",
                expression,
            )
            expressions[name] = expression
    positions = _positions(text)
    edits = []
    for node in ast.parse(text).body:
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id in names
        ):
            name = node.target.id
            if name not in expressions:
                raise ValueError(f"No source alias for {module_name}.{name}")
            start = positions[node.lineno - 1]
            end = positions[node.end_lineno]
            edits.append(
                (start, end, f"{name}: typing.TypeAlias = {expressions[name]}\n")
            )
    return _apply(text, edits)


def _drop_members(text: str, class_name: str, names: set[str]) -> str:
    """Remove inherited implementation metadata accidentally materialized by generation."""
    positions = _positions(text)
    edits = []
    for cls in ast.parse(text).body:
        if isinstance(cls, ast.ClassDef) and cls.name == class_name:
            for node in cls.body:
                name = (
                    node.target.id
                    if isinstance(node, ast.AnnAssign)
                    and isinstance(node.target, ast.Name)
                    else getattr(node, "name", None)
                )
                if name in names:
                    start = min(
                        [
                            node.lineno,
                            *[d.lineno for d in getattr(node, "decorator_list", [])],
                        ]
                    )
                    edits.append((positions[start - 1], positions[node.end_lineno], ""))
    return _apply(text, edits)


def _exports(text: str, drop: set[str], add: set[str]) -> str:
    """Adjust only explicitly excluded machine-specific exports."""
    positions = _positions(text)
    for node in ast.parse(text).body:
        if (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.target, ast.Name)
            and node.target.id == "__all__"
        ):
            names = ast.literal_eval(node.value)
            names = sorted((set(names) - drop) | add)
            start, end = _span(node.value, positions)
            return _apply(text, [(start, end, repr(names))])
    return text


def _root(text: str) -> str:
    """Restore portable root reexports and the bind helper's concrete list type."""
    import mujoco

    text = re.sub(
        r"^from mujoco\.(?:cgl|egl|glfw) import GLContext$",
        "from mujoco.glfw import GLContext",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^from mujoco\.[\w.]+ import Renderer$",
        f"from {mujoco.Renderer.__module__} import Renderer",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^from \. import (?:cgl|egl)$", "from . import glfw", text, flags=re.MULTILINE
    )
    text = text.replace(
        "from . import gl_context\n", "import mujoco.gl_context as gl_context\n"
    )
    for name in ("HEADERS_DIR", "PLUGINS_DIR", "_SYSTEM"):
        text = re.sub(rf"^{name}: str = .*?$", f"{name}: str", text, flags=re.MULTILINE)
    text = re.sub(r"^(?:is_rosetta|proc_translated):.*\n", "", text, flags=re.MULTILINE)
    text = _exports(text, {"cgl", "egl", "is_rosetta", "proc_translated"}, {"glfw"})
    text = _aliases(text, "mujoco", {"MjStruct"})
    rules = {
        (name, "__getattr__"): ("list[typing.Any]", {})
        for name in ("_MjBindModel", "_MjBindData")
    }
    return _imports(_annotate(text, rules), ["import mujoco", "import typing"])


def _renderer(text: str) -> str:
    """Complete Renderer context management and result/property annotations."""
    rules = {}
    for name in (
        "__exit__",
        "disable_depth_rendering",
        "disable_segmentation_rendering",
        "enable_depth_rendering",
        "enable_segmentation_rendering",
        "update_scene",
    ):
        rules[("Renderer", name)] = ("None", {})
    rules[("Renderer", "__enter__")] = ("Self", {})
    rules[("Renderer", "__exit__")] = (
        "None",
        {
            "exc_type": "type[BaseException] | None",
            "exc_value": "BaseException | None",
            "traceback": "TracebackType | None",
        },
    )
    for name, annotation in {
        "height": "int",
        "width": "int",
        "model": "mujoco._structs.MjModel",
    }.items():
        rules[("Renderer", name)] = (annotation, {})
    text = _annotate(text, rules)
    text = text.replace(
        "from mujoco import gl_context\n", "import mujoco.gl_context as gl_context\n"
    )
    return _imports(
        text,
        [
            "import typing",
            "import numpy.typing",
            "from types import TracebackType",
            "from typing_extensions import Self",
        ],
    )


def _viewer(text: str) -> str:
    """Restore the public handle contract and real callable aliases."""
    import mujoco

    rules = {}
    for name in (
        "__init__",
        "clear_figures",
        "clear_images",
        "clear_texts",
        "close",
        "set_figures",
        "set_images",
        "set_texts",
        "sync",
        "update_hfield",
        "update_mesh",
        "update_texture",
    ):
        rules[("Handle", name)] = ("None", {})
    rules[("Handle", "__enter__")] = ("Self", {})
    rules[("Handle", "__exit__")] = (
        "None",
        {
            "exc_type": "type[BaseException] | None",
            "exc_val": "BaseException | None",
            "exc_tb": "TracebackType | None",
        },
    )
    properties = {
        "cam": "mujoco._structs.MjvCamera",
        "d": "mujoco._structs.MjData | None",
        "m": "mujoco._structs.MjModel | None",
        "opt": "mujoco._structs.MjvOption",
        "perturb": "mujoco._structs.MjvPerturb",
        "user_scn": "mujoco._structs.MjvScene | None",
        "viewport": f"{mujoco.MjrRect.__module__}.MjrRect | None",
        "lock": "contextlib.AbstractContextManager[None]",
    }
    for name, annotation in properties.items():
        rules[("Handle", name)] = (annotation, {})
    text = _annotate(text, rules)
    text = _aliases(
        text,
        "mujoco.viewer",
        {
            "CallbackType",
            "KeyCallbackType",
            "LoaderType",
            "_InternalLoaderType",
            "_LoaderWithPathType",
        },
    )
    text = _drop_members(text, "_MjPythonBase", {"__abstractmethods__", "_abc_impl"})
    text = text.replace(
        "class _MjPythonBase:\n", "class _MjPythonBase(metaclass=abc.ABCMeta):\n"
    )
    text = text.replace("from mujoco import _simulate\n", "")
    return _imports(
        text,
        [
            "import typing",
            "import numpy.typing",
            "from types import TracebackType",
            "from typing_extensions import Self",
        ],
    )


def _context(text: str) -> str:
    """Type the shared graphics-context methods without selecting a backend."""
    rules = {
        ("GLContext", name): ("None", {})
        for name in ("__del__", "__init__", "free", "make_current")
    }
    rules[("GLContext", "__init__")] = (
        "None",
        {"max_width": "int", "max_height": "int"},
    )
    return _annotate(text, rules)


def _cgl(text: str) -> str:
    """Use actual enum members, including aliases, instead of inherited methods."""
    module = importlib.import_module("mujoco.cgl.cgl")
    positions = _positions(text)
    edits = []
    for node in ast.parse(text).body:
        if isinstance(node, ast.ClassDef) and any(
            ast.unparse(base) == "enum.IntEnum" for base in node.bases
        ):
            cls = getattr(module, node.name)
            body = [f"class {node.name}(enum.IntEnum):\n"]
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
            ):
                body.append("    " + repr(node.body[0].value.value) + "\n")
            seen = {}
            for name, value in cls.__members__.items():
                assigned = seen.get(value.value, str(value.value))
                body.append(f"    {name} = {assigned}\n")
                seen.setdefault(value.value, name)
            edits.append(
                (positions[node.lineno - 1], positions[node.end_lineno], "".join(body))
            )
    return _apply(text, edits)


def _egl(text: str) -> str:
    """Keep the environment-selected platform optional and context dimensions typed."""
    text = re.sub(
        r"^PYOPENGL_PLATFORM: str(?: \| None)?(?: = .*)?$",
        "PYOPENGL_PLATFORM: str | None",
        text,
        flags=re.MULTILINE,
    )
    return _context(text)


def _egl_exports(text: str) -> str:
    """Reexport PyOpenGL's public objects instead of private generated classes."""
    text = re.sub(
        r"^from OpenGL\._opaque import \w+ as (\w+)$",
        r"from OpenGL.EGL import \1 as \1",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^from OpenGL\.raw\.EGL\._types import LP_c_int as (EGLAttrib\w*)$",
        r"from OpenGL.EGL import \1 as \1",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^(EGL_DEFAULT_DISPLAY|EGL_NO_CONTEXT|EGL_NO_DISPLAY|EGL_NO_SURFACE):[^\n]*$",
        r"from OpenGL.EGL import \1 as \1",
        text,
        flags=re.MULTILINE,
    )
    return re.sub(
        r"^(egl\w+): OpenGL\.(?:platform\.baseplatform|extensions)\.\w+$",
        r"from OpenGL.EGL import \1 as \1",
        text,
        flags=re.MULTILINE,
    )


def _rollout(text: str) -> str:
    """Bind names emitted from runtime annotations as well as repaired array types."""
    text = text.replace("from mujoco import _rollout\n", "")
    return _imports(
        text,
        ["import typing", "import collections.abc", "from numpy import typing as npt"],
    )


def normalize_wrapper(module_name: str, text: str) -> str:
    """Correct one generated wrapper using its matching installed MuJoCo.

    Args:
        module_name: Fully qualified module name, including ``mujoco`` itself.
        text: Fresh pybind11-stubgen output for that module.

    Returns:
        Parseable stub source retaining fresh signatures and documentation.
        Unsupported modules are returned unchanged.

    Raises:
        ValueError: A known source alias or expected generated shape is missing.
    """
    processors: dict[str, Callable[[str], str]] = {
        "mujoco": _root,
        "mujoco.__init__": _root,
        "mujoco.renderer": _renderer,
        "mujoco.rendering.classic.renderer": _renderer,
        "mujoco.viewer": _viewer,
        "mujoco.rollout": _rollout,
        "mujoco.glfw": _context,
        "mujoco.cgl": _context,
        "mujoco.cgl.cgl": _cgl,
        "mujoco.egl": _egl,
        "mujoco.egl.egl_ext": _egl_exports,
    }
    if module_name not in processors:
        return text
    # ctypes closures are invalid syntax; sanitize these before the first parse.
    text = re.sub(
        r"ctypes\.CDLL\.__init__\.<locals>\._FuncPtr", "_ctypes.CFuncPtr", text
    )
    text = text.replace("ctypes.CFUNCTYPE.<locals>.CFunctionType", "_ctypes.CFuncPtr")
    if module_name.startswith("mujoco.egl"):
        # Stubgen puts future imports after PyOpenGL imports. Stubs need no
        # runtime evaluation, and the curated EGL modules omit this import.
        text = text.replace("from __future__ import annotations\n", "")
    if "_ctypes.CFuncPtr" in text and "import _ctypes\n" not in text:
        text = _imports(text, ["import _ctypes"])
    # Drop generated object/address/path reprs. Alias repair reads source instead.
    text = re.sub(r"[ \t]+# value = .*", "", text)
    text = processors[module_name](text)
    replacements = {
        "NoneType": "None",
        "numpy.ndarray": "numpy.typing.NDArray[typing.Any]",
        "ArrayLike": "npt.ArrayLike",
        "mujoco._simulate.Simulate": "_Simulate",
    }
    if module_name == "mujoco.viewer":
        import mujoco

        replacements["mujoco._render.MjrRect"] = f"{mujoco.MjrRect.__module__}.MjrRect"
    text = _repair_annotations(text, replacements)
    ast.parse(text, feature_version=(3, 10))
    return text
