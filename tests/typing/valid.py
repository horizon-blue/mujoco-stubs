"""Representative MuJoCo calls checked statically and executed without rendering."""

import mujoco
import numpy as np
from numpy.typing import NDArray
from typing_extensions import CapsuleType, assert_type

XML = """
<mujoco>
  <worldbody>
    <body name="ball">
      <freejoint/>
      <geom type="sphere" size="0.1"/>
    </body>
  </worldbody>
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

spec = mujoco.MjSpec.from_string(XML)
assert_type(spec, mujoco.MjSpec)
assert_type(spec.compile(), mujoco.MjModel)
orientation = spec.worldbody.add_geom().alt
sequence = mujoco.MjCharVec("xyz", 3)
assert_type(
    mujoco.MjSpec.resolve_orientation(False, sequence, orientation), list[float]
)
