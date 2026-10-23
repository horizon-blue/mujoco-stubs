"""Representative MuJoCo calls checked statically and executed without rendering."""

import io
import sys
from typing import Any

import mujoco
import numpy as np
from mujoco import batch, viewer
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

# Texture data is exposed as a complete bytes buffer from MuJoCo 3.5 onward.
texture = spec.texture("pixels")
assert_type(texture.data, bytes)
texture.data = b"\x00\x7f\xff"
assert isinstance(texture.data, bytes)
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
    assert_type(context.make_current(), None)
    assert_type(context.free(), None)


# Enum arithmetic preserves the runtime distinction between int and float.
joint_kind = mujoco.mjtJoint.mjJNT_HINGE
assert_type(joint_kind + 2, int)
assert_type(joint_kind + 2.5, float)
assert_type(2 + joint_kind, int)
assert_type(2.5 + joint_kind, float)

# Native virtual filesystems can supply model files or be explicitly omitted.
with mujoco.MjVfs() as vfs:
    vfs["model.xml"] = b"<mujoco/>"
    assert_type(mujoco.MjModel.from_xml_path("model.xml", vfs=vfs), mujoco.MjModel)
assert_type(mujoco.MjSpec.from_string("<mujoco/>", vfs=None), mujoco.MjSpec)


# Batch simulations expose typed instance attributes and shared field views.
simulations = batch.Batch(model, nsim=2, nthread=2, persistent=True)
assert_type(simulations.model, mujoco.MjModel)
assert_type(simulations.state, NDArray[np.float64])
assert_type(simulations.warning, NDArray[np.int32])
assert_type(simulations.status, NDArray[np.int32])
assert_type(simulations.nsim, int)
assert_type(simulations.nthread, int)
assert_type(simulations.nstate, int)
assert_type(simulations.persistent, bool)
assert_type(simulations.error(0), str)
assert_type(batch.DATA_FIELDS, frozenset[str])
assert_type(batch.MODEL_FIELDS, frozenset[str])
assert simulations.state.dtype == np.float64
assert simulations.status.dtype == simulations.warning.dtype == np.int32
positions = simulations.bind("qpos")
assert_type(positions, NDArray[np.float64])
assert_type(simulations.qpos, NDArray[Any])
assert_type(simulations.bind(name="eq_active"), NDArray[np.float64])
assert_type(simulations.bind("ncon"), NDArray[np.int32])
assert_type(simulations.bind("bvh_active"), NDArray[np.bool_])
assert_type(simulations.bind("plugin_data"), NDArray[np.uint64])
assert_type(simulations.expand("geom_rgba"), NDArray[np.float32])
assert_type(simulations.expand("geom_group"), NDArray[np.int32])
assert_type(simulations.expand("jnt_limited"), NDArray[np.bool_])
assert_type(simulations.expand("body_sameframe"), NDArray[np.uint8])
assert_type(simulations.expand("plugin_attr"), NDArray[np.int8])
assert_type(simulations.expand(name="opt.iterations"), NDArray[np.int32])
assert_type(simulations.expand("opt.gravity"), NDArray[np.float64])
assert simulations.bind("eq_active").dtype == np.float64
assert data.eq_active.dtype == np.bool_


def check_dynamic_fields(data_field: str, model_field: str) -> None:
    """Runtime-selected names retain an unspecified dtype."""
    assert_type(simulations.bind(data_field), NDArray[Any])
    assert_type(simulations.expand(model_field), NDArray[Any])


check_dynamic_fields("qpos", "body_mass")
root_view = simulations.joint("root")
assert_type(root_view.id, int)
assert_type(root_view.name, str)
assert_type(root_view.qpos, NDArray[Any])
assert root_view.name == "root"
assert np.shares_memory(root_view.qpos, positions)

# Threaded stepping agrees with a real single-simulation MuJoCo loop.
reference = mujoco.MjData(model)
assert_type(simulations.step(nstep=3), None)
for _ in range(3):
    mujoco.mj_step(model, reference)
for row in positions:
    np.testing.assert_array_equal(row, reference.qpos)
selected: batch.Ids = [0]
assert_type(simulations.forward(ids=selected, stage=mujoco.mjtStage.mjSTAGE_POS), None)
assert_type(simulations.reset(keyframe=0), None)
simulations.step(ids=np.array([True, False]))
assert simulations.bind("time")[0] > simulations.bind("time")[1]

# Model expansion, snapshots, and caller-owned models retain their contracts.
masses = simulations.expand("body_mass")
assert_type(masses, NDArray[np.float64])
masses[:, 1] *= 1.1
assert_type(simulations.set_const(), None)
assert_type(simulations.get_model(0), mujoco.MjModel)
assert_type(simulations.get_data(0), mujoco.MjData)
model_out = mujoco.MjModel.from_xml_string(XML)
data_out = mujoco.MjData(model_out)
assert simulations.get_model(0, model=model_out) is model_out
assert simulations.get_data(0, data=data_out) is data_out
other_simulations = batch.Batch(model, nsim=2, nthread=1)
assert_type(other_simulations.set_models([model, model_out]), None)
assert_type(other_simulations.set_models(model), None)
assert_type(other_simulations.set_models(None), None)

record_item: batch.RecordItem = mujoco.mjtState.mjSTATE_QPOS
records = simulations.rollout(
    2, control_spec=mujoco.mjtState.mjSTATE_CTRL, record=["qpos", record_item]
)
assert_type(records, dict[batch.RecordItem, NDArray[Any]])
assert records["qpos"].shape == (2, 2, model.nq)
assert_type(
    simulations.rollout(2, record=["qpos"], out=records),
    dict[batch.RecordItem, NDArray[Any]],
)
jacp, jacr = simulations.jac(body=1, point=[0.0, 0.0, 0.0])
assert_type(jacp, NDArray[Any])
assert_type(jacr, NDArray[Any])
assert jacp.shape == jacr.shape == (2, 3, model.nv)
hits = simulations.ray(pnt=[0, 0, 1], vec=[0, 0, -1])
assert_type(hits, tuple[NDArray[Any], ...])
assert len(hits) == 2
assert hits[0].shape == hits[1].shape == (2, 1)
hits_with_normals = simulations.ray([0, 0, 1], [0, 0, -1], normal=True)
assert len(hits_with_normals) == 3
assert hits_with_normals[2].shape == (2, 1, 3)
error = batch.SimulationError(np.array([0], dtype=np.int32), "example", ncall=2)
assert_type(error.ids, NDArray[Any])
assert error.ids.tolist() == [0]
