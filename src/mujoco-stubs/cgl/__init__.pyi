# Copyright 2023 DeepMind Technologies Limited
# SPDX-License-Identifier: Apache-2.0
# Generated from MuJoCo 4.0.0 and modified for mujoco-stubs; see NOTICE.

"""
An Apple CGL context for offscreen rendering on macOS.
"""
from __future__ import annotations
import _thread
import atexit as atexit
import contextlib as contextlib
import ctypes as ctypes
from mujoco.cgl.cgl import CGLOpenGLProfile as _PROFILE
from mujoco.cgl.cgl import CGLPixelFormatAttribute as _ATTRIB
import os as os
import threading as threading
import weakref as weakref
from . import cgl
__all__: list[str] = ['GLContext', 'atexit', 'cgl', 'contextlib', 'ctypes', 'os', 'threading', 'weakref']
class GLContext:
    """
    An EGL context for headless accelerated OpenGL rendering on GPU devices.
    """
    def as_current(self) -> contextlib.AbstractContextManager[None]:
        """
        Temporarily makes this context current, restoring any prior context.
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
_current_context: _thread._local
