# Copyright 2023 DeepMind Technologies Limited
# SPDX-License-Identifier: Apache-2.0
# Generated from MuJoCo 3.13.0 and modified for mujoco-stubs; see NOTICE.

"""
An Apple CGL context for offscreen rendering on macOS.
"""
from __future__ import annotations
import atexit as atexit
import ctypes as ctypes
from mujoco.cgl.cgl import CGLOpenGLProfile as _PROFILE
from mujoco.cgl.cgl import CGLPixelFormatAttribute as _ATTRIB
import os as os
from . import cgl
__all__: list[str] = ['GLContext', 'atexit', 'cgl', 'ctypes', 'os']
class GLContext:
    """
    An EGL context for headless accelerated OpenGL rendering on GPU devices.
    """
    def __del__(self) -> None:
        ...
    def __init__(self, max_width: int, max_height: int) -> None:
        ...
    def free(self) -> None:
        """
        Frees resources associated with this context.
        """
    def make_current(self) -> None:
        ...
