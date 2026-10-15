"""Representative MuJoCo calls checked statically and executed without rendering."""

import io
import sys

import mujoco
import numpy as np
from mujoco import viewer
from numpy.typing import NDArray
from typing_extensions import CapsuleType, assert_type

XML = """
<mujoco>
  <worldbody>
    <body name="ball">
      <freejoint name="root"/>
      <geom name="ball" type="sphere" size="0.1"/>
    </body>
  </worldbody>
  <asset>
    <hfield name="terrain" nrow="2" ncol="2" size="1 1 1 .1"/>
    <texture name="pixels" type="2d" builtin="flat" width="1" height="1"/>
  </asset>
  <keyframe>
    <key name="initial"/>
  </keyframe>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(XML, assets={})
data = mujoco.MjData(model)
assert_type(model, mujoco.MjModel)
assert_type(data, mujoco.MjData)
assert_type(data.qpos, NDArray[np.float64])
assert_type(data.qvel, NDArray[np.float64])
assert_type(mujoco.mj_step(model, data), None)
assert data.time > 0
assert_type(mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "ball"), int)
assert_type(mujoco.mj_getCache(), CapsuleType)

# Named/indexed accessors and their aliases retain the concrete view fields.
assert_type(model.stat, mujoco.MjStatistic)
assert isinstance(model.stat, mujoco.MjStatistic)
assert_type(model.body("ball").mass, NDArray[np.float64])
assert_type(data.body(1).xpos, NDArray[np.float64])
assert_type(model.jnt(name="root").axis, NDArray[np.float64])
assert_type(data.joint(0).qpos, NDArray[np.float64])
assert_type(model.key("initial").qpos, NDArray[np.float64])
assert_type(model.keyframe(0).qvel, NDArray[np.float64])
assert_type(model.hfield("terrain").data, NDArray[np.float32])
assert np.shares_memory(data.jnt("root").qpos, data.qpos)

# Enum inputs remain valid through SupportsInt; slices retain their view type.
timer = mujoco.mjtTimer(int(mujoco.mjtTimer.mjTIMER_STEP))
warning = mujoco.mjtWarning(mujoco.mjtWarning.mjWARN_INERTIA)
assert_type(timer, mujoco.mjtTimer)
assert_type(warning, mujoco.mjtWarning)
assert_type(data.timer[timer], mujoco.MjTimerStat)
assert_type(data.timer[0], mujoco.MjTimerStat)
assert_type(data.timer[:1][timer], mujoco.MjTimerStat)
assert_type(data.warning[warning], mujoco.MjWarningStat)
assert_type(data.warning[0], mujoco.MjWarningStat)
assert_type(data.warning[:1][warning], mujoco.MjWarningStat)
assert isinstance(data.timer[timer], mujoco.MjTimerStat)
assert isinstance(data.warning[warning], mujoco.MjWarningStat)

spec = mujoco.MjSpec.from_string(XML)
assert_type(spec, mujoco.MjSpec)
spec_model = spec.compile()
spec_data = mujoco.MjData(spec_model)
assert_type(spec_model, mujoco.MjModel)

# Binding keeps the element-specific fields and exposes the compiled arrays.
body = spec.body("ball")
model_body = spec_model.bind_scalar(body)
data_body = spec_data.bind_scalar(spec=body)
assert_type(model_body.mass, NDArray[np.float64])
assert_type(data_body.xpos, NDArray[np.float64])
assert model_body.name == data_body.name == "ball"
assert np.shares_memory(model_body.mass, spec_model.body_mass)
assert np.shares_memory(data_body.xpos, spec_data.xpos)
joint = spec.joint("root")
assert_type(spec_model.bind_scalar(joint).axis, NDArray[np.float64])
assert_type(spec_data.bind_scalar(joint).qpos, NDArray[np.float64])
geom = spec.geom("ball")
assert_type(spec_model.bind_scalar(geom).size, NDArray[np.float64])
assert_type(spec_data.bind_scalar(geom).xpos, NDArray[np.float64])
assert_type(spec_model.bind_scalar(spec.key("initial")).qpos, NDArray[np.float64])
assert_type(spec_model.bind_scalar(spec.hfield("terrain")).data, NDArray[np.float32])

# Python functions attached to native classes still bind their first argument.
assert_type(spec_model.bind(body).mass, NDArray[np.float64])
assert_type(spec_data.bind(body).xpos, NDArray[np.float64])
assert len(spec_model.bind([body]).mass) == 1
assert len(spec_data.bind([body]).xpos) == 3
mujoco.MjModel.bind(spec_model, body)
mujoco.MjData.bind(spec_data, body)

orientation = spec.worldbody.add_geom().alt
sequence = mujoco.MjCharVec("xyz", 3)
assert_type(
    mujoco.MjSpec.resolve_orientation(False, sequence, orientation), list[float]
)

# Whole-buffer assignment and length work without converting std::byte scalars.
texture = spec.texture("pixels")
texture.data = b"\x00\x7f\xff"
assert_type(texture.data, mujoco.MjByteVec)
assert len(texture.data) == 3

# Omitting a builder default and passing None both select the native default.
builder = mujoco.MjSpec()
assert_type(builder.add_material(), mujoco.MjsMaterial)
assert_type(builder.add_material(default=None), mujoco.MjsMaterial)
body_builder = builder.worldbody.add_body(default=None)
assert_type(body_builder, mujoco.MjsBody)
assert_type(body_builder.add_site(default=None), mujoco.MjsSite)
frame_builder = body_builder.add_frame(default=None)
assert_type(frame_builder, mujoco.MjsFrame)
assert_type(frame_builder.add_body(default=None), mujoco.MjsBody)
assert_type(frame_builder.add_frame(default=None), mujoco.MjsFrame)

contact = mujoco.MjContact()
assert_type(contact.__hash__, None)
assert contact.__hash__ is None

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

archive = io.BytesIO()
mujoco.MjSpec.from_string(XML).to_zip(archive)
archive.seek(0)
restored_spec = mujoco.MjSpec.from_zip(archive)
assert_type(restored_spec, mujoco.MjSpec)
assert restored_spec.compile().nbody == spec_model.nbody
