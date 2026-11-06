# Copyright 2017 The dm_control Authors
# SPDX-License-Identifier: Apache-2.0
# Generated from MuJoCo 4.0.0 and modified for mujoco-stubs; see NOTICE.

"""
An OpenGL context created via GLFW.
"""
from __future__ import annotations
import contextlib as contextlib
import glfw as glfw
__all__: list[str] = ['GLContext', 'contextlib', 'glfw']
class GLContext:
    """
    An OpenGL context created via GLFW.
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
        ...
    def make_current(self) -> None:
        ...
