"""Each marked line must produce an argument error in all four type checkers."""

from collections.abc import Hashable

import mujoco

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
