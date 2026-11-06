# Copyright 2018 The dm_control Authors
# SPDX-License-Identifier: Apache-2.0
# Generated from MuJoCo 4.0.0 and modified for mujoco-stubs; see NOTICE.

"""
An EGL context for headless accelerated OpenGL rendering on GPU devices.
"""
from OpenGL import error
import atexit as atexit
import contextlib as contextlib
import ctypes as ctypes
import os as os
from . import egl_ext
__all__: list[str] = ['EGL', 'EGL_ATTRIBUTES', 'EGL_DISPLAY', 'GLContext', 'PYOPENGL_PLATFORM', 'atexit', 'contextlib', 'create_initialized_egl_device_display', 'ctypes', 'egl_ext', 'error', 'os']
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
def _cuda_device_order(cuda_to_egl_device, cuda_devices):
    """
    Returns EGL devices ordered by CUDA_VISIBLE_DEVICES, if possible.
    """
def _get_cuda_to_egl_device_map(devices):
    """
    Returns a CUDA id to EGL device map, or None if it is unavailable.
    """
def _get_egl_device_cuda_id(device):
    """
    Returns the CUDA device id for an EGL device, if the driver exposes it.
    """
def _ordered_egl_devices(devices, cuda_to_egl_device, cuda_devices):
    """
    Returns EGL devices in CUDA order when possible.
    """
def _parse_cuda_device_ids(value):
    """
    Returns integer CUDA_VISIBLE_DEVICES entries, if they are parseable.
    """
def _select_egl_device(devices, cuda_to_egl_device, cuda_devices, device_id):
    """
    Selects an EGL device by CUDA id when possible, otherwise by index.
    """
def _terminate_display():
    """
    Terminates EGL_DISPLAY at exit and marks it as no longer usable.
    """
def create_initialized_egl_device_display():
    """
    Creates an initialized EGL display directly on a device.
    """
EGL_ATTRIBUTES: tuple
EGL_DISPLAY = None
PYOPENGL_PLATFORM: str | None
EGL = egl_ext
