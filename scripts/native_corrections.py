"""Normalize native MuJoCo stubs against the installed runtime.

Run under the interpreter containing the exact target MuJoCo version. The helper
imports native modules but never constructs models, data, or graphics contexts.
Edits use AST spans, preserving generated bodies and newly added parameters.
"""

import ast
import importlib
import io
import re
import tokenize
import types


class _Edits:
    def __init__(self, text: str):
        self.text = text
        self.starts = [0]
        for line in text.splitlines(keepends=True):
            self.starts.append(self.starts[-1] + len(line))
        self.edits: list[tuple[int, int, str]] = []

    def offset(self, line: int, col: int = 0) -> int:
        # Stub signatures are ASCII; account for possible Unicode docstrings.
        start = self.starts[line - 1]
        chars = self.text[start : self.starts[line]].encode()[:col].decode()
        return start + len(chars)

    def replace(self, node: ast.AST, value: str) -> None:
        self.edits.append(
            (
                self.offset(node.lineno, node.col_offset),
                self.offset(node.end_lineno, node.end_col_offset),
                value,
            )
        )

    def line(self, line: int, value: str) -> None:
        self.edits.append((self.starts[line - 1], self.starts[line], value))

    def apply(self) -> str:
        text = self.text
        end = len(text) + 1
        for start, stop, value in sorted(self.edits, reverse=True):
            if stop > end:
                raise ValueError("Overlapping correction edits")
            text = text[:start] + value + text[stop:]
            end = start
        ast.parse(text)
        return text


def _classes(body, path=()):
    for node in body:
        if isinstance(node, ast.ClassDef):
            yield path + (node.name,), node
            yield from _classes(node.body, path + (node.name,))


def _runtime_class(module, path):
    obj = module
    for name in path:
        obj = getattr(obj, name)
    return obj


def _overload(node):
    return any(
        ast.unparse(d) in {"typing.overload", "overload"} for d in node.decorator_list
    )


def _start(node):
    return min([node.lineno] + [d.lineno for d in node.decorator_list])


def _import(text, statement):
    if statement in text.splitlines():
        return text
    lines = text.splitlines(keepends=True)
    tree = ast.parse(text)
    # Insert before the first ordinary declaration and after __future__ imports.
    last_import = max(
        (
            n.end_lineno
            for n in tree.body
            if isinstance(n, (ast.Import, ast.ImportFrom))
        ),
        default=0,
    )
    lines.insert(last_import, statement + "\n")
    return "".join(lines)


def _deduplicate(text, module):
    edits = _Edits(text)
    for _, cls in _classes(ast.parse(text).body):
        groups = {}
        for node in cls.body:
            if isinstance(node, ast.FunctionDef) and _overload(node):
                groups.setdefault(node.name, []).append(node)
        for name, group in groups.items():
            unique = []
            keys = set()
            for node in group:
                key = (
                    ast.dump(node.args) + ast.dump(node.returns)
                    if node.returns
                    else ast.dump(node.args)
                )
                enum_index = (
                    module.endswith("_structs")
                    and name == "__getitem__"
                    and cls.name in {"_MjTimerStatList", "_MjWarningStatList"}
                    and any(
                        ast.unparse(a.annotation)
                        in {
                            "mujoco._enums.mjtTimer",
                            "mujoco._enums.mjtWarning",
                        }
                        for a in node.args.args
                        if a.annotation
                    )
                )
                if key in keys or enum_index:
                    edits.edits.append(
                        (
                            edits.starts[_start(node) - 1],
                            edits.starts[node.end_lineno],
                            "",
                        )
                    )
                else:
                    keys.add(key)
                    unique.append(node)
            if len(unique) == 1:
                for decorator in unique[0].decorator_list:
                    if ast.unparse(decorator) in {
                        "typing.overload",
                        "overload",
                    }:
                        edits.line(decorator.lineno, "")
    return edits.apply()


def normalize_native(module_name: str, text: str) -> str:
    """Repair generated native annotations using the matching installed runtime.

    Args:
        module_name: Fully qualified native module, such as ``mujoco._structs``.
        text: Fresh pybind11-stubgen output.

    Returns:
        Valid stub source with precise views, native binding, and constructors.

    Raises:
        ValueError: An unresolved generated native return cannot be mapped safely,
            or a novel bind signature needs review.
    """
    module_name = (
        module_name if module_name.startswith("mujoco.") else "mujoco." + module_name
    )
    module = importlib.import_module(module_name)
    # Upstream annotations contain a keyword identifier and invalid ordering.
    # Repair these exact native artifacts before parsing, retaining other args.
    text = re.sub(r"(?m)^    global: mujoco\._structs\.MjVisual\.Global\n", "", text)
    text = re.sub(
        r"(def resolve_orientation\([^\n]*sequence: MjCharVec) = None",
        r"\1",
        text,
    )
    lines = text.splitlines(keepends=True)
    for index, line in reversed(list(enumerate(lines))):
        if "def set_to_muscle(" not in line:
            continue
        # Native signatures can have an optional timeconst before required
        # tausmooth. Token boundaries preserve nested array annotations and
        # defaults introduced in 3.10, unlike splitting at every comma.
        depth = 0
        boundaries = []
        for token in tokenize.generate_tokens(io.StringIO(line.lstrip()).readline):
            if token.type != tokenize.OP:
                continue
            if token.string in "([{":
                depth += 1
                if depth == 1:
                    boundaries.append(token.end[1])
            elif token.string in ")]}":
                depth -= 1
                if depth == 0:
                    boundaries.append(token.start[1])
                    break
            elif token.string == "," and depth == 1:
                boundaries.extend([token.start[1], token.end[1]])
        declaration = line.lstrip()
        parameters = [
            declaration[a:b].strip()
            for a, b in zip(boundaries[::2], boundaries[1::2], strict=True)
        ]
        if (
            not parameters
            or len(parameters) < 3
            or not parameters[1].startswith("timeconst:")
            or " = " not in parameters[1]
            or not parameters[2].startswith("tausmooth:")
            or " = " in parameters[2]
        ):
            continue
        required = parameters[1].rsplit(" = ", 1)[0]
        first = line.replace(parameters[1], required, 1).replace(
            "= [-1.0, -1.0]", "= ..."
        )
        second = first.replace("self, " + required + ", ", "self, *, ", 1)
        indent = line[: len(line) - len(line.lstrip())]
        lines[index] = indent + "@typing.overload\n" + first
        lines.insert(
            index + 1, indent + "    ...\n" + indent + "@typing.overload\n" + second
        )
    text = "".join(lines)
    tree = ast.parse(text)
    edits = _Edits(text)
    need_never = False
    class_names = {path[-1] for path, _ in _classes(tree.body)}
    for path, cls in _classes(tree.body):
        live = _runtime_class(module, path)
        methods = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
        # pybind11's unavailable-constructor descriptor is distinct from its
        # real bound __init__ methods. This does not invoke native constructors.
        factory_only = isinstance(
            live.__init__, types.WrapperDescriptorType
        ) and not any(n.name == "__init__" for n in methods)
        if factory_only:
            need_never = True
            first = cls.body[0]
            if (
                isinstance(first, ast.Expr)
                and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)
            ):
                line = first.end_lineno
            else:
                line = cls.lineno
            indent = " " * (cls.col_offset + 4)
            edits.edits.append(
                (
                    edits.starts[line],
                    edits.starts[line],
                    indent
                    + "def __init__(self, _factory_only: Never, /) -> None:\n"
                    + indent
                    + '    """Instances are provided by MuJoCo; direct construction is unavailable."""\n',
                )
            )
        scalar_pairs = []
        scalar_nodes = [n for n in methods if n.name == "bind_scalar"]
        for method in methods:
            if (
                cls.name == "MjSpec"
                and method.name == "compile"
                and method.returns
                and ast.unparse(method.returns) == "typing.Any"
            ):
                edits.replace(method.returns, "mujoco._structs.MjModel")
            # C++ MjVfs annotations appear in loader parameters after 3.8.
            for argument in method.args.args + method.args.kwonlyargs:
                if not argument.annotation:
                    continue
                ellipses = [
                    n
                    for n in ast.walk(argument.annotation)
                    if isinstance(n, ast.Constant) and n.value is Ellipsis
                ]
                if ellipses and cls.name != "MjByteVec":
                    doc = getattr(live, method.name).__doc__ or ""
                    cpp = set(
                        re.findall(
                            r"\b"
                            + re.escape(argument.arg)
                            + r": mujoco::python::(\w+)",
                            doc,
                        )
                    )
                    if len(cpp) != 1:
                        raise ValueError(
                            f"Unresolved native parameter {path}.{method.name}.{argument.arg}"
                        )
                    native_name = cpp.pop()
                    specs_module = importlib.import_module("mujoco._specs")
                    if not isinstance(getattr(specs_module, native_name, None), type):
                        raise ValueError(f"Missing native spec class {native_name}")
                    for unresolved in ellipses:
                        edits.replace(unresolved, "mujoco._specs." + native_name)
                if (
                    cls.name == "MjSpec"
                    and method.name in {"from_file", "from_string"}
                    and argument.arg == "assets"
                    and "dict[" not in ast.unparse(argument.annotation)
                ):
                    for unresolved in ast.walk(argument.annotation):
                        if isinstance(unresolved, ast.Name) and unresolved.id == "dict":
                            edits.replace(unresolved, "dict[typing.Any, typing.Any]")
            if method.name == "bind_scalar":
                args = method.args.args
                if len(args) != 2:
                    raise ValueError(f"Review new bind_scalar signature: {path}")
                annotation = ast.unparse(args[1].annotation)
                match = re.fullmatch(r"mjs(\w+)_", annotation)
                if match:
                    annotation = "mujoco._specs.Mjs" + match[1]
                    edits.replace(args[1].annotation, annotation)
                    # The generated None default comes from a native pointer
                    # artifact; bind_scalar requires a real supported spec.
                    if (
                        method.args.defaults
                        and isinstance(method.args.defaults[-1], ast.Constant)
                        and method.args.defaults[-1].value is None
                    ):
                        default = method.args.defaults[-1]
                        annotation_end = edits.offset(
                            args[1].annotation.end_lineno,
                            args[1].annotation.end_col_offset,
                        )
                        edits.edits.append(
                            (
                                annotation_end,
                                edits.offset(
                                    default.end_lineno, default.end_col_offset
                                ),
                                "",
                            )
                        )
                suffix = annotation.rsplit(".", 1)[-1].removeprefix("Mjs")
                suffix = {"HField": "Hfield", "Key": "Keyframe"}.get(suffix, suffix)
                view = f"_{cls.name}{suffix}Views"
                if view not in class_names:
                    raise ValueError(f"Missing native view {view}")
                if (
                    method.returns is None
                    or isinstance(method.returns, ast.Constant)
                    and method.returns.value is Ellipsis
                ):
                    if method.returns is None:
                        raise ValueError("Missing bind_scalar return annotation")
                    edits.replace(method.returns, view)
                else:
                    view = ast.unparse(method.returns)
                scalar_pairs.append((annotation, view))
            elif (
                method.returns
                and isinstance(method.returns, ast.Constant)
                and method.returns.value is Ellipsis
            ):
                if cls.name == "MjByteVec":
                    edits.replace(method.returns, "typing.Any")
                elif cls.name == "MjModel" and method.name == "stat":
                    edits.replace(method.returns, "MjStatistic")
                else:
                    doc = getattr(live, method.name).__doc__ or ""
                    candidates = set(
                        re.findall(r"-> mujoco::python::(Mj\w+Views)", doc)
                    )
                    if len(candidates) != 1:
                        raise ValueError(
                            f"Unresolved native return: {path}.{method.name}"
                        )
                    view = "_" + candidates.pop()
                    if view not in class_names:
                        raise ValueError(f"Missing view class {view}")
                    edits.replace(method.returns, view)
            if cls.name == "MjByteVec":
                for node in ast.walk(method):
                    if (
                        isinstance(node, ast.Constant)
                        and node.value is Ellipsis
                        and node is not method.returns
                    ):
                        # Only replace ellipses inside annotations, never bodies.
                        if (
                            any(
                                node is sub
                                for arg in method.args.args
                                if arg.annotation
                                for sub in ast.walk(arg.annotation)
                            )
                            or method.returns
                            and any(node is sub for sub in ast.walk(method.returns))
                        ):
                            edits.replace(node, "typing.Any")
            for argument, default in (
                zip(
                    method.args.args[-len(method.args.defaults) :],
                    method.args.defaults,
                )
                if method.args.defaults
                else ()
            ):
                if (
                    argument.annotation
                    and isinstance(default, ast.Constant)
                    and default.value is None
                ):
                    current = ast.unparse(argument.annotation)
                    if current in {"MjsDefault", "MjsFrame"}:
                        edits.replace(argument.annotation, current + " | None")
                        if method.args.kwarg and method.args.kwarg.annotation is None:
                            edits.replace(
                                method.args.kwarg,
                                method.args.kwarg.arg + ": typing.Any",
                            )
            if cls.name == "MjSpec" and method.name == "to_zip":
                for decorator in method.decorator_list:
                    if ast.unparse(decorator) == "staticmethod":
                        edits.line(decorator.lineno, "")
        if scalar_nodes:
            binds = [n for n in methods if n.name == "bind"]
            if len(binds) != 1:
                # Idempotence: already-normalized overload group is retained.
                if not binds or not all(_overload(n) for n in binds):
                    raise ValueError("Review new bind overload shape")
                continue
            bind = binds[0]
            if (
                len(bind.args.args) != 2
                or bind.args.kwonlyargs
                or bind.args.vararg
                or bind.args.kwarg
                or bind.args.defaults
            ):
                raise ValueError("Review new bind arguments before replacing overloads")
            indent = " " * bind.col_offset
            first = bind.args.args[0].arg
            spec_parameter = bind.args.args[1].arg
            body = text[edits.starts[bind.lineno] : edits.starts[bind.end_lineno]]
            chunks = []
            for index, (annotation, view) in enumerate(scalar_pairs):
                chunks.append(
                    indent
                    + "@typing.overload\n"
                    + indent
                    + f"def bind({first}: {cls.name}, {spec_parameter}: {annotation}) -> {view}:\n"
                    + (body if index == 0 else indent + "    ...\n")
                )
            union = "typing.Union[" + ", ".join(a for a, _ in scalar_pairs) + "]"
            chunks.append(
                indent
                + "@typing.overload\n"
                + indent
                + f"def bind({first}: {cls.name}, {spec_parameter}: typing.Sequence[{union}]) -> mujoco._MjBind{cls.name.removeprefix('Mj')}:\n"
                + indent
                + "    ...\n"
            )
            edits.edits.append(
                (
                    edits.starts[_start(bind) - 1],
                    edits.starts[bind.end_lineno],
                    "".join(chunks),
                )
            )
    text = edits.apply()
    if need_never:
        text = _import(text, "from typing_extensions import Never")
    text = re.sub(
        r"(?m)^(\s*__hash__: typing.ClassVar\[None\] = None)$",
        r"\1  # type: ignore[assignment]  # Native type is unhashable.",
        text,
    )
    text = _deduplicate(text, module_name)
    if module_name.endswith("_structs"):
        text = _import(text, "import mujoco._specs")
    tree = ast.parse(text)
    # The generator emits Iterable parameters without importing their module.
    # Syntax checks cannot find this: retain the concrete annotation and supply
    # exactly the module it references.
    if any(
        isinstance(node, ast.Name) and node.id == "collections"
        for node in ast.walk(tree)
    ):
        text = _import(text, "import collections.abc")
    ast.parse(text)
    return text
