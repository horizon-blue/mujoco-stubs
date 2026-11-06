"""Check every installed batch field overload against real MuJoCo arrays."""

import ast
from importlib.metadata import distribution

import mujoco
import numpy as np
from mujoco import batch

# Exercise state, controls, sensors, equalities, and mocap alongside empty fields.
XML = """
<mujoco>
  <size nuserdata="3"/>
  <worldbody>
    <body name="target" mocap="true"/>
    <body name="ball">
      <freejoint/>
      <geom type="sphere" size="0.1"/>
    </body>
    <body name="arm" pos="1 0 0">
      <joint name="hinge"/>
      <geom type="capsule" size="0.1 0.3"/>
    </body>
  </worldbody>
  <equality><weld body1="ball" body2="target"/></equality>
  <actuator><motor joint="hinge"/></actuator>
  <sensor><jointpos joint="hinge"/></sensor>
</mujoco>
"""


def check_fields() -> None:
    """Compare complete Literal groups with empty and populated model results.

    Read the installed declarations instead of importing the generator, so an
    outdated or incorrect packaged mapping fails against the real API.
    """
    path = distribution("mujoco-stubs").locate_file("mujoco-stubs/batch.pyi")
    cls = next(
        n
        for n in ast.parse(path.read_text()).body
        if isinstance(n, ast.ClassDef) and n.name == "Batch"
    )
    mappings = {"bind": {}, "expand": {}, "expanded": {}}
    for method in cls.body:
        if not isinstance(method, ast.FunctionDef) or method.name not in mappings:
            continue
        annotation = method.args.args[1].annotation
        if ast.unparse(annotation) == "str":
            continue
        assert ast.unparse(annotation.value) == "typing.Literal"
        names = [ast.literal_eval(n) for n in annotation.slice.elts]
        returns = method.returns
        if method.name == "expanded":
            assert isinstance(returns, ast.BinOp) and isinstance(returns.op, ast.BitOr)
            assert ast.literal_eval(returns.right) is None
            returns = returns.left
        scalar = ast.unparse(returns.slice).removeprefix("np.")
        mapping = mappings[method.name]
        assert not mapping.keys() & set(names), f"Duplicate {method.name} fields"
        mapping.update(dict.fromkeys(names, np.dtype(scalar)))
    assert mappings["bind"].keys() == batch.DATA_FIELDS
    assert mappings["expand"].keys() == batch.MODEL_FIELDS
    assert mappings["expanded"] == mappings["expand"]
    for xml in ("<mujoco/>", XML):
        model = mujoco.MjModel.from_xml_string(xml)
        simulations = batch.Batch(model, 2, nthread=1, persistent=True)
        for name, fields in mappings.items():
            for field, dtype in fields.items():
                if name == "expand":
                    assert simulations.expanded(field) is None, field
                array = getattr(simulations, name)(field)
                assert array is not None, f"{name}({field!r})"
                assert array.dtype == dtype, (
                    f"{name}({field!r}): {array.dtype} != {dtype}"
                )
                if name == "expanded":
                    assert not array.flags.writeable, field
                    np.testing.assert_array_equal(array, simulations.expand(field))
    print(
        f"Batch dtypes: {len(mappings['bind'])} bind and "
        f"{len(mappings['expand'])} expand/expanded fields match on both models"
    )


if __name__ == "__main__":
    check_fields()
