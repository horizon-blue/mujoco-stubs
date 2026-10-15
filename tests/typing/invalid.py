"""Each marked line must produce an argument error in both type checkers."""

import mujoco

model = mujoco.MjModel.from_xml_string("<mujoco/>")
mujoco.MjData("not a model")  # expect-error
mujoco.mj_step(model, model)  # expect-error
mujoco.MjModel.from_xml_string(123)  # expect-error
mujoco.MjModel.from_xml_string("<mujoco/>", assets=123)  # expect-error
