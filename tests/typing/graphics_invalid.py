"""Invalid classic graphics calls must be rejected by all four checkers."""

import mujoco
from mujoco import viewer

model = mujoco.MjModel.from_xml_string("<mujoco/>")


def wrong_key_callback(keycode: str) -> None:
    pass


callback: viewer.KeyCallbackType = wrong_key_callback  # expect-error


def invalid_graphics(renderer: mujoco.Renderer, handle: viewer.Handle) -> None:
    renderer.update_scene(model)  # expect-error
    handle.sync(state_only="yes")  # expect-error
    renderer.height = 240  # expect-error


mujoco.GLContext("320", 240)  # expect-error


def invalid_context(context: mujoco.GLContext) -> None:
    context.as_current(123)  # expect-error
