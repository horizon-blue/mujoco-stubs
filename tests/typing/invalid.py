"""Each marked line must produce an argument error in all four type checkers."""

from collections.abc import Hashable

import mujoco
import numpy as np
from mujoco import batch, viewer
from numpy.typing import NDArray

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


batch.Batch("not a model", nsim=2)  # expect-error
batch.Batch(model, nsim="two")  # expect-error
simulations = batch.Batch(model, nsim=2)
simulations.bind(123)  # expect-error
simulations.joint(1.5)  # expect-error
simulations.step(ids=object())  # expect-error
simulations.step(nstep="two")  # expect-error
simulations.forward(stage="position")  # expect-error
simulations.expand(123)  # expect-error
simulations.set_models([data])  # expect-error
simulations.get_model(0, model=data)  # expect-error
simulations.get_data(0, data=model)  # expect-error
simulations.rollout(2, record=[object()])  # expect-error
simulations.ray([0, 0, 1], [0, 0, -1], normal="yes")  # expect-error
batch.SimulationError("0", "example")  # expect-error

simulations.joint("root").id = 0  # expect-error
simulations.joint("root").name = "other"  # expect-error

# A literal selects its actual dtype rather than the permissive str fallback.
wrong_positions: NDArray[np.int32] = simulations.bind("qpos")  # expect-error
wrong_active: NDArray[np.bool_] = simulations.bind("eq_active")  # expect-error
wrong_rgba: NDArray[np.float64] = simulations.expand("geom_rgba")  # expect-error
wrong_opt: NDArray[np.float64] = simulations.expand("opt.iterations")  # expect-error
