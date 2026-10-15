# Copyright 2023 DeepMind Technologies Limited
# SPDX-License-Identifier: Apache-2.0
# Generated from MuJoCo 3.16.0 and modified for mujoco-stubs; see NOTICE.

"""
Bindings for Apple CGL.
"""
from __future__ import annotations
import _ctypes
import ctypes as ctypes
from ctypes import c_int as GLint
from ctypes import c_void_p as CGLContextObj
from ctypes import c_void_p as CGLPixelFormatObj
import enum as enum
import typing
__all__: list[str] = ['CGLContextObj', 'CGLError', 'CGLOpenGLProfile', 'CGLPixelFormatAttribute', 'CGLPixelFormatObj', 'CGLReleaseContext', 'CGLReleasePixelFormat', 'GLint', 'ctypes', 'enum']
class CGLError(RuntimeError):
    pass
class CGLOpenGLProfile(enum.IntEnum):
    CGLOGLPVersion_Legacy = 4096
    CGLOGLPVersion_3_2_Core = 12800
    CGLOGLPVersion_GL3_Core = CGLOGLPVersion_3_2_Core
    CGLOGLPVersion_GL4_Core = 16640
class CGLPixelFormatAttribute(enum.IntEnum):
    '\n    CGLPixelFormatAttribute enum values.\n    '
    CGLPFAAllRenderers = 1
    CGLPFATripleBuffer = 3
    CGLPFADoubleBuffer = 5
    CGLPFAColorSize = 8
    CGLPFAAlphaSize = 11
    CGLPFADepthSize = 12
    CGLPFAStencilSize = 13
    CGLPFAMinimumPolicy = 51
    CGLPFAMaximumPolicy = 52
    CGLPFASampleBuffers = 55
    CGLPFASample = 56
    CGLPFAColorFloat = 58
    CGLPFAMultisample = 59
    CGLPFASupersample = 60
    CGLPFASampleAlpha = 61
    CGLPFARendererID = 70
    CGLPFANoRecovery = 72
    CGLPFAAccelerated = 73
    CGLPFAClosestPolicy = 74
    CGLPFABackingStore = 76
    CGLPFABackingVolatile = 77
    CGLPFADisplayMask = 84
    CGLPFAAllowOfflineRenderers = 96
    CGLPFAAcceleratedCompute = 97
    CGLPFAOpenGLProfile = 99
    CGLPFASupportsAutomaticGraphicsSwitching = 101
    CGLPFAVirtualScreenCount = 128
    CGLPFAAuxBuffers = 7
    CGLPFAAccumSize = 14
    CGLPFAAuxDepthStencil = 57
    CGLPFAStereo = 6
    CGLPFAOffScreen = 53
    CGLPFAWindow = 80
    CGLPFACompliant = 83
    CGLPFAPBuffer = 90
    CGLPFARemotePBuffer = 91
    CGLPFASingleRenderer = 71
    CGLPFARobust = 75
    CGLPFAMPSafe = 78
    CGLPFAMultiScreen = 81
    CGLPFAFullScreen = 54
def _make_checked(func):
    ...
CGLReleaseContext: _ctypes.CFuncPtr
CGLReleasePixelFormat: _ctypes.CFuncPtr
_CGL: ctypes.CDLL
_CGLChoosePixelFormat: _ctypes.CFuncPtr
_CGLCreateContext: _ctypes.CFuncPtr
_CGLErrorString: _ctypes.CFuncPtr
_CGLLockContext: _ctypes.CFuncPtr
_CGLReleaseContext: _ctypes.CFuncPtr
_CGLReleasePixelFormat: _ctypes.CFuncPtr
_CGLSetCurrentContext: _ctypes.CFuncPtr
_CGLUnlockContext: _ctypes.CFuncPtr
