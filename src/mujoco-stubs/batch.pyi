# Copyright 2026 DeepMind Technologies Limited
# SPDX-License-Identifier: Apache-2.0
# Generated from MuJoCo 3.17.0 and modified for mujoco-stubs; see NOTICE.

"""
Many simulations of one model, stepped on a thread pool.

Each simulation is its mjSTATE_INTEGRATION row; a call loads the row into an
MjData, runs, copies out the bound derived fields, and saves the row back, on
nthread threads including the caller's. Results are bit-identical to a loop over
one MjData per simulation at any thread count.

  batch = Batch(model, nsim=1024, nthread=8)
  qpos, ctrl, xpos = batch.bind('qpos'), batch.bind('ctrl'), batch.bind('xpos')
  for _ in range(1000):
    ctrl[:] = policy(qpos)
    batch.step()

bind() returns a live (nsim, ...) array. State fields (qpos, qvel, ctrl,
mocap_pos, ...) are views of the state rows: a write is the simulation's state
at its next call. Derived fields (xpos, sensordata, ...) are refreshed after
every call on a simulation, one substep behind the state after step(), as with
mj_step; a derived field bound between calls is zero until the next call.
joint(name), body(name), sensor(name) and the other named views slice the bound
and expanded fields per object, with the attributes of MjData's and MjModel's:
batch.joint('hinge').qpos is (nsim, 1), and batch.body('pole').mass = masses
writes per-simulation masses. set_models(models) runs each simulation on a model
of the caller's instead of expanding fields. get_model(sim) and get_data(sim)
materialize one simulation, to render it or to pass it to any function. Fields
are also attributes, as on MjData: batch.xpos binds xpos, and batch.ctrl = u
writes every simulation's controls. DATA_FIELDS and MODEL_FIELDS name the fields
bind() and expand() accept.

By default an MjData serves many simulations, so memory scales with threads;
only the fields a call computes are then meaningful, and a field it does not
compute (qfrc_inverse after step, quantities computed only for the sensors that
need them) holds another simulation's value. persistent=True keeps one MjData
per simulation instead, which every bound field then reflects, and is required
for models with sleep or IPC enabled. Likewise, engine plugins that keep state
outside plugin_state share it among the simulations a thread runs, unless the
batch is persistent.

The batch's threads run across simulations; the engine's thread pool
(mju_threadpool) runs within one, and the two do not combine. Physics callbacks
(mjcb_*) must be C functions, installed through ctypes: a Python function
installed as one makes the batch's calls raise ValueError.
"""
from __future__ import annotations
import numpy.typing
import copy as copy
import difflib as difflib
import functools as functools
import mujoco as mujoco
from mujoco import _batch
import numpy
import numpy as np
from numpy import typing as npt
import typing
from typing import Any
__all__: list[str] = ['Any', 'Batch', 'DATA_FIELDS', 'Ids', 'MODEL_FIELDS', 'RecordItem', 'SimulationError', 'copy', 'difflib', 'functools', 'mujoco', 'np', 'npt']
class Batch:
    """
    nsim simulations of a copy of model, on nthread threads (0: all CPUs).
    
      With persistent=True, the batch keeps one MjData per simulation.
    
      A Batch must not be used from several Python threads at once: its calls are
      serialized, but each reports its failures from status and error(), which the
      next call overwrites.
      
    """
    model: mujoco.MjModel
    state: npt.NDArray[np.float64]
    warning: npt.NDArray[np.int32]
    status: npt.NDArray[np.int32]
    @property
    def _data(self) -> mujoco.MjData: ...
    def __getattr__(self, name: str) -> numpy.typing.NDArray[typing.Any]:
        ...
    def __init__(self, model: mujoco._structs.MjModel, nsim: int, nthread: int = 0, persistent: bool = False) -> None:
        ...
    def __setattr__(self, name: str, value: typing.Any) -> None:
        ...
    def _check(self, ids: typing.Optional[numpy.typing.NDArray[typing.Any]], nfail: int) -> None:
        ...
    def _component(self, component: typing.Any) -> typing.Tuple[int, int]:
        ...
    def _expanded_values(self, name: str) -> typing.Optional[numpy.typing.NDArray[typing.Any]]:
        """
        A model field's read-only per-simulation values, None if not expanded.
        """
    def _model_of(self, sim: int) -> mujoco._structs.MjModel:
        """
        The model simulation sim runs on, but for its per-simulation fields.
        """
    def actuator(self, key: typing.Union[int, str]) -> _Named:
        ...
    @typing.overload
    def bind(
        self, name: typing.Literal[
            'bvh_active',
            'flex_hessian_valid',
        ]
    ) -> npt.NDArray[np.bool_]:
        ...
    @typing.overload
    def bind(
        self, name: typing.Literal[
            'M',
            'act',
            'act_dot',
            'actuator_force',
            'actuator_length',
            'actuator_moment',
            'actuator_velocity',
            'bvh_aabb_dyn',
            'cacc',
            'cam_xmat',
            'cam_xpos',
            'cdof',
            'cdof_dot',
            'cfrc_ext',
            'cfrc_int',
            'cinert',
            'crb',
            'ctrl',
            'cvel',
            'energy',
            'eq_active',
            'flexedge_J',
            'flexedge_hessian',
            'flexedge_length',
            'flexedge_velocity',
            'flexelem_aabb',
            'flexelem_krot',
            'flexvert_J',
            'flexvert_hessian',
            'flexvert_lambda',
            'flexvert_length',
            'flexvert_xpos',
            'geom_xmat',
            'geom_xpos',
            'history',
            'light_xdir',
            'light_xpos',
            'mocap_pos',
            'mocap_quat',
            'plugin_state',
            'qDeriv',
            'qH',
            'qHDiagInv',
            'qLD',
            'qLDiagInv',
            'qLU',
            'qacc',
            'qacc_smooth',
            'qacc_warmstart',
            'qfrc_actuator',
            'qfrc_adhesion',
            'qfrc_applied',
            'qfrc_bias',
            'qfrc_constraint',
            'qfrc_damper',
            'qfrc_fluid',
            'qfrc_gravcomp',
            'qfrc_inverse',
            'qfrc_passive',
            'qfrc_smooth',
            'qfrc_spring',
            'qpos',
            'qvel',
            'sensordata',
            'site_xmat',
            'site_xpos',
            'solver_fwdinv',
            'subtree_angmom',
            'subtree_com',
            'subtree_linvel',
            'ten_J',
            'ten_length',
            'ten_velocity',
            'time',
            'userdata',
            'wrap_xpos',
            'xanchor',
            'xaxis',
            'xfrc_applied',
            'ximat',
            'xipos',
            'xmat',
            'xpos',
            'xquat',
        ]
    ) -> npt.NDArray[np.float64]:
        ...
    @typing.overload
    def bind(
        self, name: typing.Literal[
            'body_awake',
            'body_awake_ind',
            'dof_awake_ind',
            'flexvert_conage',
            'moment_colind',
            'moment_rowadr',
            'moment_rownnz',
            'nA',
            'nJ',
            'ncon',
            'ne',
            'nefc',
            'nf',
            'nidof',
            'nisland',
            'nl',
            'parent_awake_ind',
            'plugin',
            'solver_niter',
            'solver_nnz',
            'ten_wrapadr',
            'ten_wrapnum',
            'tree_asleep',
            'tree_awake',
            'wrap_obj',
        ]
    ) -> npt.NDArray[np.int32]:
        ...
    @typing.overload
    def bind(
        self, name: typing.Literal[
            'plugin_data',
        ]
    ) -> npt.NDArray[np.uint64]:
        ...
    @typing.overload
    def bind(self, name: str) -> numpy.typing.NDArray[typing.Any]:
        """
        Return a live (nsim, ...) array over an MjData field.
        
            State fields are views of the rows, which hold mjtNum (float64 in the
            standard build), so eq_active binds as mjtNum rather than using MjData's field dtype.
            Other fields are outputs, copied out after every call, and read-only.
        
            Args:
              name: the MjData field, one of DATA_FIELDS.
        
            Returns:
              The (nsim, ...) array, cached so that each field is registered once.
            
        """
    def body(self, key: typing.Union[int, str]) -> _Named:
        ...
    def camera(self, key: typing.Union[int, str]) -> _Named:
        ...
    def equality(self, key: typing.Union[int, str]) -> _Named:
        ...
    def error(self, sim: int) -> str:
        """
        Message of the error simulation sim raised in its last call, or ''.
        """
    @typing.overload
    def expand(
        self, name: typing.Literal[
            'actuator_actearly',
            'actuator_actlimited',
            'actuator_ctrllimited',
            'actuator_forcelimited',
            'eq_active0',
            'flex_centered',
            'flex_flatskin',
            'flex_rigid',
            'flexedge_rigid',
            'jnt_actfrclimited',
            'jnt_actgravcomp',
            'jnt_limited',
            'light_active',
            'light_castshadow',
            'mat_texuniform',
            'tendon_actfrclimited',
            'tendon_limited',
        ]
    ) -> npt.NDArray[np.bool_]:
        ...
    @typing.overload
    def expand(
        self, name: typing.Literal[
            'cam_intrinsic',
            'cam_sensorsize',
            'flex_rgba',
            'flex_texcoord',
            'geom_rgba',
            'light_ambient',
            'light_attenuation',
            'light_bulbradius',
            'light_cutoff',
            'light_diffuse',
            'light_exponent',
            'light_intensity',
            'light_range',
            'light_softness',
            'light_specular',
            'mat_emission',
            'mat_metallic',
            'mat_reflectance',
            'mat_rgba',
            'mat_roughness',
            'mat_shininess',
            'mat_specular',
            'mat_texrepeat',
            'site_rgba',
            'tendon_rgba',
        ]
    ) -> npt.NDArray[np.float32]:
        ...
    @typing.overload
    def expand(
        self, name: typing.Literal[
            'actuator_acc0',
            'actuator_actrange',
            'actuator_armature',
            'actuator_biasprm',
            'actuator_cranklength',
            'actuator_ctrlrange',
            'actuator_damping',
            'actuator_dampingpoly',
            'actuator_delay',
            'actuator_dynprm',
            'actuator_forcerange',
            'actuator_gainprm',
            'actuator_gear',
            'actuator_length0',
            'actuator_lengthrange',
            'actuator_user',
            'body_gravcomp',
            'body_inertia',
            'body_invweight0',
            'body_ipos',
            'body_iquat',
            'body_margin',
            'body_mass',
            'body_pos',
            'body_quat',
            'body_subtreemass',
            'body_user',
            'bvh_aabb',
            'cam_fovy',
            'cam_ipd',
            'cam_mat0',
            'cam_pos',
            'cam_pos0',
            'cam_poscom0',
            'cam_quat',
            'cam_user',
            'dof_M0',
            'dof_armature',
            'dof_damping',
            'dof_dampingpoly',
            'dof_frictionloss',
            'dof_invweight0',
            'dof_length',
            'dof_solimp',
            'dof_solref',
            'efm0_L',
            'eq_data',
            'eq_solimp',
            'eq_solref',
            'flex_bending',
            'flex_damping',
            'flex_edgedamping',
            'flex_edgestiffness',
            'flex_friction',
            'flex_gap',
            'flex_margin',
            'flex_node',
            'flex_node0',
            'flex_radius',
            'flex_size',
            'flex_solimp',
            'flex_solmix',
            'flex_solref',
            'flex_stiffness',
            'flex_vert',
            'flex_vert0',
            'flex_vertmetric',
            'flexedge_invweight0',
            'flexedge_length0',
            'geom_aabb',
            'geom_adhesion',
            'geom_fluid',
            'geom_friction',
            'geom_gap',
            'geom_margin',
            'geom_pos',
            'geom_quat',
            'geom_rbound',
            'geom_size',
            'geom_solimp',
            'geom_solmix',
            'geom_solref',
            'geom_surfacevel',
            'geom_user',
            'jnt_actfrcrange',
            'jnt_axis',
            'jnt_margin',
            'jnt_pos',
            'jnt_range',
            'jnt_solimp',
            'jnt_solref',
            'jnt_stiffness',
            'jnt_stiffnesspoly',
            'jnt_user',
            'key_act',
            'key_ctrl',
            'key_mpos',
            'key_mquat',
            'key_qpos',
            'key_qvel',
            'key_time',
            'light_dir',
            'light_dir0',
            'light_pos',
            'light_pos0',
            'light_poscom0',
            'numeric_data',
            'opt.ccd_tolerance',
            'opt.density',
            'opt.gravity',
            'opt.impratio',
            'opt.ls_tolerance',
            'opt.magnetic',
            'opt.noslip_tolerance',
            'opt.o_friction',
            'opt.o_margin',
            'opt.o_solimp',
            'opt.o_solref',
            'opt.sleep_tolerance',
            'opt.timestep',
            'opt.tolerance',
            'opt.viscosity',
            'opt.wind',
            'pair_adhesion',
            'pair_friction',
            'pair_gap',
            'pair_margin',
            'pair_solimp',
            'pair_solref',
            'pair_solreffriction',
            'qpos0',
            'qpos_spring',
            'sensor_cutoff',
            'sensor_delay',
            'sensor_interval',
            'sensor_noise',
            'sensor_user',
            'site_pos',
            'site_quat',
            'site_size',
            'site_user',
            'tendon_actfrcrange',
            'tendon_armature',
            'tendon_damping',
            'tendon_dampingpoly',
            'tendon_frictionloss',
            'tendon_invweight0',
            'tendon_length0',
            'tendon_lengthspring',
            'tendon_margin',
            'tendon_range',
            'tendon_solimp_fri',
            'tendon_solimp_lim',
            'tendon_solref_fri',
            'tendon_solref_lim',
            'tendon_stiffness',
            'tendon_stiffnesspoly',
            'tendon_user',
            'tendon_width',
            'tuple_objprm',
            'wrap_prm',
        ]
    ) -> npt.NDArray[np.float64]:
        ...
    @typing.overload
    def expand(
        self, name: typing.Literal[
            'B_colind',
            'B_rowadr',
            'B_rownnz',
            'D_colind',
            'D_diag',
            'D_rowadr',
            'D_rownnz',
            'M_colind',
            'M_rowadr',
            'M_rownnz',
            'actuator_actadr',
            'actuator_actnum',
            'actuator_biastype',
            'actuator_ctrladr',
            'actuator_ctrlnum',
            'actuator_ctrlspec',
            'actuator_dyntype',
            'actuator_gaintype',
            'actuator_group',
            'actuator_history',
            'actuator_historyadr',
            'actuator_outadr',
            'actuator_outnum',
            'actuator_plugin',
            'actuator_trnid',
            'actuator_trntype',
            'body_bvhadr',
            'body_bvhnum',
            'body_conaffinity',
            'body_contype',
            'body_dofadr',
            'body_dofnum',
            'body_geomadr',
            'body_geomnum',
            'body_jntadr',
            'body_jntnum',
            'body_mocapid',
            'body_parentid',
            'body_plugin',
            'body_rootid',
            'body_treeid',
            'body_weldid',
            'cam_bodyid',
            'cam_mode',
            'cam_output',
            'cam_projection',
            'cam_resolution',
            'cam_targetbodyid',
            'dof_Madr',
            'dof_bodyid',
            'dof_jntid',
            'dof_parentid',
            'dof_simplenum',
            'dof_treeid',
            'efm0_L_colind',
            'efm0_L_rowadr',
            'efm0_L_rownnz',
            'efm0_dofid',
            'efmC_perm',
            'eq_obj1id',
            'eq_obj2id',
            'eq_objtype',
            'eq_type',
            'exclude_signature',
            'flex_activelayers',
            'flex_bendingadr',
            'flex_bvhadr',
            'flex_bvhnum',
            'flex_cellnum',
            'flex_conaffinity',
            'flex_condim',
            'flex_contype',
            'flex_dim',
            'flex_edge',
            'flex_edgeadr',
            'flex_edgeequality',
            'flex_edgeflap',
            'flex_edgenum',
            'flex_elem',
            'flex_elemadr',
            'flex_elemdataadr',
            'flex_elemedge',
            'flex_elemedgeadr',
            'flex_elemlayer',
            'flex_elemnum',
            'flex_elemtexcoord',
            'flex_group',
            'flex_interp',
            'flex_matid',
            'flex_nodeadr',
            'flex_nodebodyid',
            'flex_nodenum',
            'flex_passive',
            'flex_priority',
            'flex_selfcollide',
            'flex_shell',
            'flex_shelldataadr',
            'flex_shellnum',
            'flex_stiffnessadr',
            'flex_texcoordadr',
            'flex_vertadr',
            'flex_vertbodyid',
            'flex_vertedge',
            'flex_vertedgeadr',
            'flex_vertedgenum',
            'flex_vertnum',
            'flexedge_J_colind',
            'flexedge_J_rowadr',
            'flexedge_J_rownnz',
            'flexvert_J_colind',
            'flexvert_J_rowadr',
            'flexvert_J_rownnz',
            'geom_bodyid',
            'geom_conaffinity',
            'geom_condim',
            'geom_contype',
            'geom_dataid',
            'geom_group',
            'geom_matid',
            'geom_plugin',
            'geom_priority',
            'geom_type',
            'jnt_actuatorid',
            'jnt_bodyid',
            'jnt_dofadr',
            'jnt_group',
            'jnt_qposadr',
            'jnt_type',
            'light_bodyid',
            'light_mode',
            'light_targetbodyid',
            'light_texid',
            'light_type',
            'mapD2M',
            'mapM2D',
            'mapM2M',
            'mat_texid',
            'name_actuatoradr',
            'name_bodyadr',
            'name_camadr',
            'name_eqadr',
            'name_excludeadr',
            'name_flexadr',
            'name_geomadr',
            'name_hfieldadr',
            'name_jntadr',
            'name_keyadr',
            'name_lightadr',
            'name_matadr',
            'name_meshadr',
            'name_numericadr',
            'name_pairadr',
            'name_pluginadr',
            'name_sensoradr',
            'name_siteadr',
            'name_skinadr',
            'name_tendonadr',
            'name_texadr',
            'name_textadr',
            'name_tupleadr',
            'names_map',
            'numeric_adr',
            'numeric_size',
            'opt.ccd_iterations',
            'opt.cone',
            'opt.disableactuator',
            'opt.disableflags',
            'opt.enableflags',
            'opt.integrator',
            'opt.iterations',
            'opt.jacobian',
            'opt.ls_iterations',
            'opt.noslip_iterations',
            'opt.sdf_initpoints',
            'opt.sdf_iterations',
            'opt.solver',
            'pair_dim',
            'pair_geom1',
            'pair_geom2',
            'pair_signature',
            'plugin',
            'plugin_attradr',
            'plugin_stateadr',
            'plugin_statenum',
            'sensor_adr',
            'sensor_datatype',
            'sensor_dim',
            'sensor_history',
            'sensor_historyadr',
            'sensor_intprm',
            'sensor_needstage',
            'sensor_objid',
            'sensor_objtype',
            'sensor_plugin',
            'sensor_refid',
            'sensor_reftype',
            'sensor_type',
            'site_bodyid',
            'site_dataid',
            'site_group',
            'site_matid',
            'site_type',
            'ten_J_colind',
            'ten_J_rowadr',
            'ten_J_rownnz',
            'tendon_actuatorid',
            'tendon_adr',
            'tendon_group',
            'tendon_matid',
            'tendon_num',
            'tendon_treeid',
            'tendon_treenum',
            'text_adr',
            'text_size',
            'tree_bodyadr',
            'tree_bodynum',
            'tree_dofadr',
            'tree_dofnum',
            'tree_sleep_policy',
            'tuple_adr',
            'tuple_objid',
            'tuple_objtype',
            'tuple_size',
            'wrap_objid',
            'wrap_type',
        ]
    ) -> npt.NDArray[np.int32]:
        ...
    @typing.overload
    def expand(
        self, name: typing.Literal[
            'plugin_attr',
        ]
    ) -> npt.NDArray[np.int8]:
        ...
    @typing.overload
    def expand(
        self, name: typing.Literal[
            'body_sameframe',
            'body_simple',
            'geom_sameframe',
            'site_sameframe',
        ]
    ) -> npt.NDArray[np.uint8]:
        ...
    @typing.overload
    def expand(self, name: str) -> numpy.typing.NDArray[typing.Any]:
        """
        Give a model field per-simulation values; return them, (nsim, ...).
        
            Array fields are named as in MjModel, MjOption fields as 'opt.<name>'.
            bvh_aabb holds the bodies' bounding volumes, which precede the meshes'.
            After writing a field that mj_setConst reads, one of
            mujoco.MjModel._setconst_inputs or an MjOption field, call set_const() so
            that the constants derived from it follow.
        
            Args:
              name: the MjModel field, one of MODEL_FIELDS.
        
            Returns:
              The live (nsim, ...) array of per-simulation values.
            
        """
    def forward(self, ids: typing.Optional[npt.ArrayLike] = None, stage: int | mujoco.mjtStage = 3) -> None:
        """
        Compute the forward stages up to stage, by default mj_forward.
        """
    def geom(self, key: typing.Union[int, str]) -> _Named:
        ...
    def get_data(self, sim: int, data: typing.Optional[mujoco._structs.MjData] = None) -> mujoco._structs.MjData:
        """
        Simulation sim's state, and in a persistent batch its whole MjData.
        
            Derived fields are those of the simulation's last call in a persistent
            batch; otherwise run mj_forward with get_model(sim) to compute them.
        
            Args:
              sim: the simulation.
              data: an MjData with the batch's sizes to write into, or None for a new
                one.
        
            Returns:
              The data.
            
        """
    def get_model(self, sim: int, model: typing.Optional[mujoco._structs.MjModel] = None) -> mujoco._structs.MjModel:
        """
        Simulation sim's model: the batch's, with its per-simulation fields.
        
            With caller models set (set_models), a copy of simulation sim's model.
        
            Args:
              sim: the simulation.
              model: an MjModel with the sizes of simulation sim's model to write into,
                or None for a copy of that model. The batch shares that model's assets
                (meshes, textures and so on) and writes everything else.
        
            Returns:
              The model, for rendering or for any mj_ function.
            
        """
    def jac(self, body: npt.ArrayLike, point: npt.ArrayLike, ids: typing.Optional[npt.ArrayLike] = None) -> typing.Tuple[numpy.typing.NDArray[typing.Any], numpy.typing.NDArray[typing.Any]]:
        """
        Translational and rotational Jacobians of a world point on a body.
        
            Runs mj_kinematics and mj_comPos per simulation, from its state, then
            mj_jac; the state and bound fields are untouched. In a persistent batch the
            simulation's MjData keeps these kinematics, as get_data() shows, and its
            next step starts afresh rather than continuing.
        
            Args:
              body: body id, or one per simulation of the call, (n,).
              point: world-frame points, (3,) or (n, 3) for the n simulations of the
                call.
              ids: the simulations, or None for all.
        
            Returns:
              jacp, jacr: (n, 3, nv) each.
            
        """
    def joint(self, key: typing.Union[int, str]) -> _Named:
        ...
    def keyframe(self, key: typing.Union[int, str]) -> _Named:
        ...
    def light(self, key: typing.Union[int, str]) -> _Named:
        ...
    def material(self, key: typing.Union[int, str]) -> _Named:
        ...
    def numeric(self, key: typing.Union[int, str]) -> _Named:
        ...
    def pair(self, key: typing.Union[int, str]) -> _Named:
        ...
    def ray(self, pnt: npt.ArrayLike, vec: npt.ArrayLike, geomgroup: typing.Optional[npt.ArrayLike] = None, flg_static: bool = True, bodyexclude: npt.ArrayLike = -1, ids: typing.Optional[npt.ArrayLike] = None, normal: bool = False) -> typing.Tuple[numpy.typing.NDArray[typing.Any], ...]:
        """
        Intersect rays with each simulation's geoms, as mj_ray.
        
            Runs mj_kinematics (and mj_flex) per simulation, from its state; the state
            and bound fields are untouched. In a persistent batch the simulation's
            MjData keeps these kinematics, as get_data() shows, and its next step starts
            afresh rather than continuing.
        
            Args:
              pnt: ray origins, broadcast to (n, nray, 3) for the n simulations of the
                call: (3,) is one ray, (nray, 3) the same rays in every simulation.
              vec: ray directions, broadcast likewise.
              geomgroup: geom groups to include, (mjNGROUP,), or None for all.
              flg_static: whether to include static geoms.
              bodyexclude: body whose geoms a ray ignores, or -1; broadcast to (n,
                nray).
              ids: the simulations, or None for all.
              normal: whether to return the surface normal at each hit.
        
            Returns:
              dist, geomid: (n, nray) each; dist is -1 and geomid -1 for a miss. With
              normal, also the normals, (n, nray, 3), zero for a miss.
            
        """
    def reset(self, ids: typing.Optional[npt.ArrayLike] = None, keyframe: npt.ArrayLike = -1, stage: int | mujoco.mjtStage = 3) -> None:
        """
        Reset to the model's defaults or to keyframes, then compute stages.
        
            Writes to the reset simulations' state made before the call are discarded.
            By default the reset runs mj_forward; stage=mjSTAGE_NONE skips it, for a
            reset that is followed by writes to the state and a forward().
        
            Args:
              ids: the simulations, or None for all.
              keyframe: a keyframe for every simulation of the call, or one each, (n,);
                -1 for the model's defaults.
              stage: mjtStage, the stages to compute after the reset.
            
        """
    def rollout(self, nstep: int, control: typing.Optional[npt.ArrayLike] = None, control_spec: int | mujoco.mjtState = 64, record: typing.Sequence[typing.Union[str, int, mujoco._enums.mjtState]] = (('qpos',)), ids: typing.Optional[npt.ArrayLike] = None, out: typing.Optional[typing.Dict[typing.Union[str, int, mujoco._enums.mjtState], numpy.typing.NDArray[typing.Any]]] = None) -> typing.Dict[typing.Union[str, int, mujoco._enums.mjtState], numpy.typing.NDArray[typing.Any]]:
        """
        Advance each simulation by nstep substeps, recording after each.
        
            As mujoco.rollout: before substep k, the state components in control_spec
            are set from control, (n, nstep, ncontrol) for the n simulations of the
            call, or the inputs are left as they are when control is None. A simulation
            whose warning counters rise stops stepping, and its remaining records repeat
            its last ones.
        
            Args:
              nstep: number of substeps.
              control: (n, nstep, mj_stateSize(model, control_spec)) or None.
              control_spec: mjtState bits within mjSTATE_USER.
              record: MjData field names, or mjtState specs for state vectors. Fields
                are recorded with MjData's types, so eq_active is uint8 here though
                bind() gives it as mjtNum.
              ids: the simulations, or None for all.
              out: arrays to record into, by record item, of the shapes and dtypes this
                call returns; the items not in it get new arrays.
        
            Returns:
              A dict from each record item to its (n, nstep, ...) array.
            
        """
    def sensor(self, key: typing.Union[int, str]) -> _Named:
        ...
    def set_const(self, ids: typing.Optional[npt.ArrayLike] = None) -> None:
        """
        Run mj_setConst per simulation; derived fields become per-simulation.
        """
    def set_models(self, models: typing.Union[None, mujoco._structs.MjModel, typing.Sequence[mujoco._structs.MjModel]]) -> None:
        """
        Run simulation i on models[i] instead of the batch's model.
        
            Each model must give MjData the layout of the batch's model: the same sizes
            of everything MjData holds, as models compiled from one spec with different
            parameters, or with meshes of other shapes, do. The batch keeps them alive
            and reads them; set them again after editing one. Caller models replace
            per-simulation fields: expand() and set_const() raise while they are set,
            and set_models raises if fields are expanded. Named views read model
            attributes from each simulation's model.
        
            Args:
              models: an MjModel per simulation, one MjModel for all of them, or None
                for the batch's model.
            
        """
    def site(self, key: typing.Union[int, str]) -> _Named:
        ...
    def step(self, ids: typing.Optional[npt.ArrayLike] = None, nstep: int = 1, stage: int | mujoco.mjtStage = 0) -> None:
        """
        Advance each simulation by nstep calls to mj_step, then compute stages.
        
            As with mj_step, derived fields describe the state before the last substep.
            stage computes the forward stages up to it at the new state: mjSTAGE_VEL
            makes position- and velocity-dependent fields and sensors current, as
            mj_step1 does; mjSTAGE_ACC runs mj_forward, whose acceleration-dependent
            values use controls that will not be applied. A persistent batch continues
            its next step from those stages, so that mjSTAGE_VEL costs nothing extra.
        
            Args:
              ids: the simulations, or None for all.
              nstep: number of substeps.
              stage: mjtStage, the stages to compute at the new state.
            
        """
    def tendon(self, key: typing.Union[int, str]) -> _Named:
        ...
    @property
    def nsim(self) -> int:
        ...
    @property
    def nstate(self) -> int:
        ...
    @property
    def nthread(self) -> int:
        ...
    @property
    def persistent(self) -> bool:
        ...
class SimulationError(RuntimeError):
    """
    MuJoCo raised an error in some simulations of a call.
    
      Those simulations kept the state they had before the call, and the others ran
      to completion. ids lists them; Batch.error(i) has each message.
      
    """
    ids: npt.NDArray[typing.Any]
    def __init__(self, ids: numpy.typing.NDArray[typing.Any], message: str, ncall: typing.Optional[int] = None) -> None:
        ...
class _Named:
    """
    One object's slices of per-simulation fields, as MjData's and MjModel's.
    
      batch.joint('hinge').qpos is the part of batch.bind('qpos') that
      data.joint('hinge').qpos is of data.qpos, and batch.body('pole').mass the part
      of batch.expand('body_mass') that model.body('pole').mass is of
      model.body_mass. Data attributes bind their field. Model attributes read
      without expanding: the per-simulation values of a field that expand() or
      set_const() expanded, or else the model's value for every simulation,
      read-only unless expanded by expand(). Assignment expands the field and writes
      every simulation's value. Structural fields (addresses, counts, ids and types)
      are the same in every simulation and cannot be assigned. Equalities, pairs,
      materials, numerics and keyframes have only MjModel attributes.
      
    """
    @property
    def id(self) -> int: ...
    @property
    def name(self) -> str: ...
    _fields: typing.ClassVar[dict] = {}
    def __getattr__(self, attr: str) -> numpy.typing.NDArray[typing.Any]:
        ...
    def __init__(self, batch: Batch, kind: str, key: typing.Union[int, str], data: bool = True) -> None:
        ...
    def __setattr__(self, attr: str, value: typing.Any) -> None:
        """
        Write value to every simulation's slice: batch.joint('j').qpos = 0.5.
        """
    def _slice(self, attr: str, write: bool) -> numpy.typing.NDArray[typing.Any]:
        """
        The (nsim, ...) slice of attribute attr, writable if write.
        """
def _containing(obj: typing.Any, names: typing.FrozenSet[str], part: numpy.typing.NDArray[typing.Any]) -> typing.Optional[str]:
    """
    The field of obj among names whose memory holds the array part.
    """
def _did_you_mean(name: str, names: typing.Iterable[str]) -> str:
    """
    ' (did you mean ...?)' listing close matches of name among names, or ''.
    """
def _field_names() -> typing.Tuple[typing.FrozenSet[str], typing.FrozenSet[str]]:
    """
    The names bind() and expand() accept, as the batch's own tables decide.
    """
def _hint(name: str, names: typing.Iterable[str], model_hint: bool = False) -> str:
    """
    Where name belongs if it is a model or option field, else close matches.
    """
def _ids(ids: typing.Optional[npt.ArrayLike], nsim: int) -> typing.Optional[numpy.typing.NDArray[typing.Any]]:
    """
    Validated int32 ids from integer ids or a boolean mask; None for all.
    
      Shape, dtype, range, order and uniqueness are checked before narrowing to
      int32, so that no id is truncated or wrapped into a valid one.
    
      Args:
        ids: sorted unique integer ids, a boolean mask of shape (nsim,), or None.
        nsim: the number of simulations.
    
      Returns:
        The int32 ids, or None for all simulations.
      
    """
def _int32(x: npt.ArrayLike, shape: typing.Tuple[int, ...], lo: int, hi: int, name: str) -> numpy.typing.NDArray[typing.Any]:
    """
    Integers x in [lo, hi), broadcast to shape, checked, then as int32.
    """
def _not_bindable(data: mujoco._structs.MjData, name: str) -> ValueError:
    """
    The error for a name that bind() does not accept; data is a template.
    """
def _not_expandable(model: mujoco._structs.MjModel, name: str) -> ValueError:
    """
    The error for a name that expand() does not accept.
    """
def _output_error(name: str) -> ValueError:
    """
    The error for a write to an output, which every call overwrites.
    """
def _per_simulation(values: numpy.typing.NDArray[typing.Any], template: numpy.typing.NDArray[typing.Any]) -> numpy.typing.NDArray[typing.Any]:
    """
    (nsim, n) values of a model field as (nsim, *template.shape).
    
      bvh_aabb holds only the bodies' hierarchies, a prefix of the model's rows,
      possibly none of them, so the number of rows is taken from values.
    
      Args:
        values: the per-simulation values, one row of elements per simulation.
        template: the model's array of the field.
    
      Returns:
        values, reshaped.
      
    """
def _structural(field: str, part: numpy.typing.NDArray[typing.Any]) -> bool:
    """
    Whether model field holds addresses, counts, ids or types: structure.
    """
def _template(data: mujoco._structs.MjData, name: str) -> typing.Optional[numpy.typing.NDArray[typing.Any]]:
    """
    MjData field name as an array, an int scalar as a 0-d int32; else None.
    """
DATA_FIELDS: frozenset[str]
Ids: typing.TypeAlias = typing.Optional[npt.ArrayLike]
MODEL_FIELDS: frozenset[str]
RecordItem: typing.TypeAlias = typing.Union[str, int, mujoco.mjtState]
_COMPUTED_VIEWS: frozenset
_STATE_FIELDS: dict
