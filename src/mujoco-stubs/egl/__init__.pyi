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
EGL_ATTRIBUTES: tuple  # value = (EGL_RED_SIZE, 8, EGL_GREEN_SIZE, 8, EGL_BLUE_SIZE, 8, EGL_ALPHA_SIZE, 8, EGL_DEPTH_SIZE, 24, EGL_STENCIL_SIZE, 8, EGL_COLOR_BUFFER_TYPE, EGL_RGB_BUFFER, EGL_SURFACE_TYPE, EGL_PBUFFER_BIT, EGL_RENDERABLE_TYPE, EGL_OPENGL_BIT, EGL_NONE)
EGL_DISPLAY = None
PYOPENGL_PLATFORM: str | None
EGL = egl_ext
