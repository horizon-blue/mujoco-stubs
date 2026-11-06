"""Check classic graphics interfaces with the full runtime installed."""

import sys
from typing import Any

import mujoco
from mujoco import viewer
from numpy.typing import NDArray
from typing_extensions import assert_type

model = mujoco.MjModel.from_xml_string("<mujoco/>")
data = mujoco.MjData(model)

if sys.platform == "darwin":
    from mujoco.cgl.cgl import CGLOpenGLProfile

    profile = CGLOpenGLProfile(0x3200)
    assert_type(profile, CGLOpenGLProfile)
    assert profile is CGLOpenGLProfile.CGLOGLPVersion_GL3_Core
    assert CGLOpenGLProfile(0x3200) is CGLOpenGLProfile.CGLOGLPVersion_3_2_Core


def key_callback(keycode: int) -> None:
    assert_type(keycode, int)


def load_model() -> tuple[mujoco.MjModel, mujoco.MjData]:
    return model, data


# Public callback aliases remain usable as annotations.
callback: viewer.KeyCallbackType = key_callback
loader: viewer.LoaderType = load_model
callback(32)
loaded_model, loaded_data = loader()
assert_type(loaded_model, mujoco.MjModel)
assert_type(loaded_data, mujoco.MjData)


def inspect_graphics(
    renderer: mujoco.Renderer,
    handle: viewer.Handle,
    context: mujoco.GLContext,
) -> None:
    """Type-check public graphics use without opening a window or GPU context."""
    with renderer as active_renderer:
        assert_type(active_renderer, mujoco.Renderer)
        assert_type(active_renderer.model, mujoco.MjModel)
        assert_type(active_renderer.width, int)
        assert_type(active_renderer.height, int)
        assert_type(active_renderer.scene, mujoco.MjvScene)
        assert_type(active_renderer.update_scene(data), None)
        assert_type(active_renderer.enable_depth_rendering(), None)
        assert_type(active_renderer.disable_depth_rendering(), None)
        assert_type(active_renderer.enable_segmentation_rendering(), None)
        assert_type(active_renderer.disable_segmentation_rendering(), None)
        assert_type(active_renderer.render(), NDArray[Any])
    with handle as active_handle:
        assert_type(active_handle, viewer.Handle)
        assert_type(active_handle.cam, mujoco.MjvCamera)
        assert_type(active_handle.opt, mujoco.MjvOption)
        assert_type(active_handle.perturb, mujoco.MjvPerturb)
        assert_type(active_handle.m, mujoco.MjModel | None)
        assert_type(active_handle.d, mujoco.MjData | None)
        assert_type(active_handle.user_scn, mujoco.MjvScene | None)
        assert_type(active_handle.viewport, mujoco.MjrRect | None)
        with active_handle.lock() as token:
            assert_type(token, None)
        assert_type(active_handle.sync(state_only=True), None)
    with context.as_current() as current:
        assert_type(current, None)
    assert_type(context.make_current(), None)
    assert_type(context.free(), None)
