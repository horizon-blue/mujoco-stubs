# Copyright 2018 The dm_control Authors
# SPDX-License-Identifier: Apache-2.0
# Generated from MuJoCo 3.7.0 and modified for mujoco-stubs; see NOTICE.

"""
An EGL context for headless accelerated OpenGL rendering on GPU devices.
"""
from OpenGL import error
import atexit as atexit
import ctypes as ctypes
import os as os
from . import egl_ext
__all__: list[str] = ['EGL', 'EGL_ATTRIBUTES', 'EGL_DISPLAY', 'GLContext', 'PYOPENGL_PLATFORM', 'atexit', 'create_initialized_egl_device_display', 'ctypes', 'egl_ext', 'error', 'os']
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
def create_initialized_egl_device_display():
    """
    Creates an initialized EGL display directly on a device.
    """
EGL_ATTRIBUTES: tuple
EGL_DISPLAY = None
PYOPENGL_PLATFORM: str | None
EGL = egl_ext
