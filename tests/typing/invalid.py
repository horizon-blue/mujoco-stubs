"""Each marked line must produce an argument error in all four type checkers."""

from collections.abc import Hashable

import mujoco
from mujoco import viewer

model = mujoco.MjModel.from_xml_string("<mujoco/>")
mujoco.MjData("not a model")  # expect-error
mujoco.mj_step(model, model)  # expect-error
mujoco.MjModel.from_xml_string(123)  # expect-error
mujoco.MjModel.from_xml_string("<mujoco/>", assets=123)  # expect-error

mujoco.mjtTimer("step")  # expect-error

spec = mujoco.MjSpec()
data = mujoco.MjData(model)
model.bind_scalar()  # expect-error
model.bind_scalar(None)  # expect-error
model.bind_scalar("ball")  # expect-error
model.bind_scalar(spec)  # expect-error
data.bind_scalar()  # expect-error
data.bind_scalar(None)  # expect-error
data.bind_scalar(spec.key("initial"))  # expect-error

spec.add_material(default="not a default")  # expect-error
spec.worldbody.add_frame(default=spec.default)  # expect-error

unhashable: Hashable = mujoco.MjContact()  # expect-error


def wrong_key_callback(keycode: str) -> None:
    pass


callback: viewer.KeyCallbackType = wrong_key_callback  # expect-error

model.bind()  # expect-error
data.bind()  # expect-error
spec.to_zip()  # expect-error
spec.to_zip(123)  # expect-error

data.bind(spec.key("initial"))  # expect-error
data.bind([spec.key("initial")])  # expect-error

# These native objects must come from loaders, builders, or existing views.
mujoco.MjModel()  # expect-error
mujoco.MjsBody()  # expect-error
mujoco.MjsGeom()  # expect-error
mujoco.MjsMaterial(object())  # expect-error
mujoco.MjsOrientation()  # expect-error


def invalid_graphics(renderer: mujoco.Renderer, handle: viewer.Handle) -> None:
    renderer.update_scene(model)  # expect-error
    handle.sync(state_only="yes")  # expect-error
    renderer.height = 240  # expect-error


mujoco.GLContext("320", 240)  # expect-error

mujoco.MjModel.from_xml_string("<mujoco/>", vfs=123)  # expect-error
