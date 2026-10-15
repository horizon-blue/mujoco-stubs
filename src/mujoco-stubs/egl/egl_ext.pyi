# Copyright 2018 The dm_control Authors
# SPDX-License-Identifier: Apache-2.0
# Generated from MuJoCo 3.9.0 and modified for mujoco-stubs; see NOTICE.

"""
Extends OpenGL.EGL with definitions necessary for headless rendering.
"""
import _ctypes
from OpenGL import EGL
from OpenGL.EGL import EXT
from OpenGL.EGL import VERSION
from OpenGL.EGL.VERSION.EGL_1_0 import glInitEgl10VERSION
from OpenGL.EGL.VERSION.EGL_1_1 import glInitEgl11VERSION
from OpenGL.EGL.VERSION.EGL_1_2 import glInitEgl12VERSION
from OpenGL.EGL.VERSION.EGL_1_3 import glInitEgl13VERSION
from OpenGL.EGL.VERSION.EGL_1_4 import glInitEgl14VERSION
from OpenGL.EGL.VERSION.EGL_1_5 import glInitEgl15VERSION
from OpenGL._bytes import as_8_bit
from OpenGL.EGL import EGLClientBuffer as EGLClientBuffer
from OpenGL.EGL import EGLConfig as EGLConfig
from OpenGL.EGL import EGLContext as EGLContext
from OpenGL.EGL import EGLDeviceEXT as EGLDeviceEXT
from OpenGL.EGL import EGLDisplay as EGLDisplay
from OpenGL.EGL import EGLImage as EGLImage
from OpenGL.EGL import EGLImageKHR as EGLImageKHR
from OpenGL.EGL import NativeDisplayType as NativeDisplayType
from OpenGL.EGL import EGLNativeDisplayType as EGLNativeDisplayType
from OpenGL.EGL import NativePixmapType as NativePixmapType
from OpenGL.EGL import EGLNativePixmapType as EGLNativePixmapType
from OpenGL.EGL import NativeWindowType as NativeWindowType
from OpenGL.EGL import EGLNativeWindowType as EGLNativeWindowType
from OpenGL.EGL import EGLOutputLayerEXT as EGLOutputLayerEXT
from OpenGL.EGL import EGLOutputPortEXT as EGLOutputPortEXT
from OpenGL.EGL import EGLStreamKHR as EGLStreamKHR
from OpenGL.EGL import EGLSurface as EGLSurface
from OpenGL.EGL import EGLSync as EGLSync
from OpenGL.EGL import EGLSyncNV as EGLSyncNV
from OpenGL.EGL import EGLSyncKHR as EGLSyncKHR
from OpenGL import arrays
import OpenGL.constant
from OpenGL import constant
from OpenGL import error
from OpenGL import extensions
from OpenGL import platform
from OpenGL.platform import ctypesloader
from OpenGL.raw.EGL._errors import EGLError
import OpenGL.raw.EGL._types
from OpenGL.raw.EGL._types import EGLClientPixmapHI
from OpenGL.EGL import EGLAttrib as EGLAttrib
from OpenGL.EGL import EGLAttribKHR as EGLAttribKHR
from OpenGL.raw.EGL._types import wl_display
from OpenGL import wrapper
import ctypes as ctypes
from ctypes import CFUNCTYPE as CALLBACK_TYPE
from ctypes import c_int as EGLNativeFileDescriptorKHR
from ctypes import c_int as EGLint
from ctypes import c_int
from ctypes import c_uint as EGLenum
from ctypes import c_uint as EGLBoolean
from ctypes import c_ulong as EGLTimeKHR
from ctypes import c_ulong as EGLTime
from ctypes import c_ulong as EGLScreenMESA
from ctypes import c_ulong as EGLTimeNV
from ctypes import c_ulong as EGLsizeiANDROID
from ctypes import c_ulong as EGLuint64NV
from ctypes import c_ulong as EGLuint64KHR
from ctypes import c_ulong as EGLModeMESA
__all__: list[str] = ['CALLBACK_TYPE', 'EGL', 'EGLAttrib', 'EGLAttribKHR', 'EGLBoolean', 'EGLClientBuffer', 'EGLClientPixmapHI', 'EGLConfig', 'EGLContext', 'EGLDeviceEXT', 'EGLDisplay', 'EGLError', 'EGLImage', 'EGLImageKHR', 'EGLModeMESA', 'EGLNativeDisplayType', 'EGLNativeFileDescriptorKHR', 'EGLNativePixmapType', 'EGLNativeWindowType', 'EGLOutputLayerEXT', 'EGLOutputPortEXT', 'EGLQuerier', 'EGLScreenMESA', 'EGLStreamKHR', 'EGLSurface', 'EGLSync', 'EGLSyncKHR', 'EGLSyncNV', 'EGLTime', 'EGLTimeKHR', 'EGLTimeNV', 'EGL_ALPHA_FORMAT', 'EGL_ALPHA_FORMAT_NONPRE', 'EGL_ALPHA_FORMAT_PRE', 'EGL_ALPHA_MASK_SIZE', 'EGL_ALPHA_SIZE', 'EGL_BACK_BUFFER', 'EGL_BAD_ACCESS', 'EGL_BAD_ALLOC', 'EGL_BAD_ATTRIBUTE', 'EGL_BAD_CONFIG', 'EGL_BAD_CONTEXT', 'EGL_BAD_CURRENT_SURFACE', 'EGL_BAD_DISPLAY', 'EGL_BAD_MATCH', 'EGL_BAD_NATIVE_PIXMAP', 'EGL_BAD_NATIVE_WINDOW', 'EGL_BAD_PARAMETER', 'EGL_BAD_SURFACE', 'EGL_BIND_TO_TEXTURE_RGB', 'EGL_BIND_TO_TEXTURE_RGBA', 'EGL_BLUE_SIZE', 'EGL_BUFFER_DESTROYED', 'EGL_BUFFER_PRESERVED', 'EGL_BUFFER_SIZE', 'EGL_CLIENT_APIS', 'EGL_CL_EVENT_HANDLE', 'EGL_COLORSPACE', 'EGL_COLORSPACE_LINEAR', 'EGL_COLORSPACE_sRGB', 'EGL_COLOR_BUFFER_TYPE', 'EGL_CONDITION_SATISFIED', 'EGL_CONFIG_CAVEAT', 'EGL_CONFIG_ID', 'EGL_CONFORMANT', 'EGL_CONTEXT_CLIENT_TYPE', 'EGL_CONTEXT_CLIENT_VERSION', 'EGL_CONTEXT_LOST', 'EGL_CONTEXT_MAJOR_VERSION', 'EGL_CONTEXT_MINOR_VERSION', 'EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT', 'EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT', 'EGL_CONTEXT_OPENGL_DEBUG', 'EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE', 'EGL_CONTEXT_OPENGL_PROFILE_MASK', 'EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY', 'EGL_CONTEXT_OPENGL_ROBUST_ACCESS', 'EGL_CORE_NATIVE_ENGINE', 'EGL_DEFAULT_DISPLAY', 'EGL_DEPTH_SIZE', 'EGL_DISPLAY_SCALING', 'EGL_DONT_CARE', 'EGL_DRAW', 'EGL_EXTENSIONS', 'EGL_FALSE', 'EGL_FOREVER', 'EGL_GL_COLORSPACE', 'EGL_GL_COLORSPACE_LINEAR', 'EGL_GL_COLORSPACE_SRGB', 'EGL_GL_RENDERBUFFER', 'EGL_GL_TEXTURE_2D', 'EGL_GL_TEXTURE_3D', 'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_X', 'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y', 'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z', 'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_X', 'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Y', 'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Z', 'EGL_GL_TEXTURE_LEVEL', 'EGL_GL_TEXTURE_ZOFFSET', 'EGL_GREEN_SIZE', 'EGL_HEIGHT', 'EGL_HORIZONTAL_RESOLUTION', 'EGL_IMAGE_PRESERVED', 'EGL_LARGEST_PBUFFER', 'EGL_LEVEL', 'EGL_LOSE_CONTEXT_ON_RESET', 'EGL_LUMINANCE_BUFFER', 'EGL_LUMINANCE_SIZE', 'EGL_MATCH_NATIVE_PIXMAP', 'EGL_MAX_PBUFFER_HEIGHT', 'EGL_MAX_PBUFFER_PIXELS', 'EGL_MAX_PBUFFER_WIDTH', 'EGL_MAX_SWAP_INTERVAL', 'EGL_MIN_SWAP_INTERVAL', 'EGL_MIPMAP_LEVEL', 'EGL_MIPMAP_TEXTURE', 'EGL_MULTISAMPLE_RESOLVE', 'EGL_MULTISAMPLE_RESOLVE_BOX', 'EGL_MULTISAMPLE_RESOLVE_BOX_BIT', 'EGL_MULTISAMPLE_RESOLVE_DEFAULT', 'EGL_NATIVE_RENDERABLE', 'EGL_NATIVE_VISUAL_ID', 'EGL_NATIVE_VISUAL_TYPE', 'EGL_NONE', 'EGL_NON_CONFORMANT_CONFIG', 'EGL_NOT_INITIALIZED', 'EGL_NO_CONTEXT', 'EGL_NO_DISPLAY', 'EGL_NO_RESET_NOTIFICATION', 'EGL_NO_SURFACE', 'EGL_NO_TEXTURE', 'EGL_OPENGL_API', 'EGL_OPENGL_BIT', 'EGL_OPENGL_ES2_BIT', 'EGL_OPENGL_ES3_BIT', 'EGL_OPENGL_ES_API', 'EGL_OPENGL_ES_BIT', 'EGL_OPENVG_API', 'EGL_OPENVG_BIT', 'EGL_OPENVG_IMAGE', 'EGL_PBUFFER_BIT', 'EGL_PIXEL_ASPECT_RATIO', 'EGL_PIXMAP_BIT', 'EGL_PLATFORM_DEVICE_EXT', 'EGL_READ', 'EGL_RED_SIZE', 'EGL_RENDERABLE_TYPE', 'EGL_RENDER_BUFFER', 'EGL_RGB_BUFFER', 'EGL_SAMPLES', 'EGL_SAMPLE_BUFFERS', 'EGL_SIGNALED', 'EGL_SINGLE_BUFFER', 'EGL_SLOW_CONFIG', 'EGL_STENCIL_SIZE', 'EGL_SUCCESS', 'EGL_SURFACE_TYPE', 'EGL_SWAP_BEHAVIOR', 'EGL_SWAP_BEHAVIOR_PRESERVED_BIT', 'EGL_SYNC_CL_EVENT', 'EGL_SYNC_CL_EVENT_COMPLETE', 'EGL_SYNC_CONDITION', 'EGL_SYNC_FENCE', 'EGL_SYNC_FLUSH_COMMANDS_BIT', 'EGL_SYNC_PRIOR_COMMANDS_COMPLETE', 'EGL_SYNC_STATUS', 'EGL_SYNC_TYPE', 'EGL_TEXTURE_2D', 'EGL_TEXTURE_FORMAT', 'EGL_TEXTURE_RGB', 'EGL_TEXTURE_RGBA', 'EGL_TEXTURE_TARGET', 'EGL_TIMEOUT_EXPIRED', 'EGL_TRANSPARENT_BLUE_VALUE', 'EGL_TRANSPARENT_GREEN_VALUE', 'EGL_TRANSPARENT_RED_VALUE', 'EGL_TRANSPARENT_RGB', 'EGL_TRANSPARENT_TYPE', 'EGL_TRUE', 'EGL_UNSIGNALED', 'EGL_VENDOR', 'EGL_VERSION', 'EGL_VERTICAL_RESOLUTION', 'EGL_VG_ALPHA_FORMAT', 'EGL_VG_ALPHA_FORMAT_NONPRE', 'EGL_VG_ALPHA_FORMAT_PRE', 'EGL_VG_ALPHA_FORMAT_PRE_BIT', 'EGL_VG_COLORSPACE', 'EGL_VG_COLORSPACE_LINEAR', 'EGL_VG_COLORSPACE_LINEAR_BIT', 'EGL_VG_COLORSPACE_sRGB', 'EGL_WIDTH', 'EGL_WINDOW_BIT', 'EGLenum', 'EGLint', 'EGLsizeiANDROID', 'EGLuint64KHR', 'EGLuint64NV', 'EXT', 'NativeDisplayType', 'NativePixmapType', 'NativeWindowType', 'VERSION', 'arrays', 'as_8_bit', 'c_int', 'constant', 'ctypes', 'ctypesloader', 'eglBindAPI', 'eglBindTexImage', 'eglChooseConfig', 'eglClientWaitSync', 'eglCopyBuffers', 'eglCreateContext', 'eglCreateImage', 'eglCreatePbufferFromClientBuffer', 'eglCreatePbufferSurface', 'eglCreatePixmapSurface', 'eglCreatePlatformPixmapSurface', 'eglCreatePlatformWindowSurface', 'eglCreateSync', 'eglCreateWindowSurface', 'eglDestroyContext', 'eglDestroyImage', 'eglDestroySurface', 'eglDestroySync', 'eglGetConfigAttrib', 'eglGetConfigs', 'eglGetCurrentContext', 'eglGetCurrentDisplay', 'eglGetCurrentSurface', 'eglGetDisplay', 'eglGetError', 'eglGetPlatformDisplay', 'eglGetPlatformDisplayEXT', 'eglGetProcAddress', 'eglGetSyncAttrib', 'eglInitialize', 'eglMakeCurrent', 'eglQueryAPI', 'eglQueryContext', 'eglQueryDevicesEXT', 'eglQueryString', 'eglQuerySurface', 'eglReleaseTexImage', 'eglReleaseThread', 'eglSurfaceAttrib', 'eglSwapBuffers', 'eglSwapInterval', 'eglTerminate', 'eglWaitClient', 'eglWaitGL', 'eglWaitNative', 'eglWaitSync', 'error', 'extensions', 'glInitEgl10VERSION', 'glInitEgl11VERSION', 'glInitEgl12VERSION', 'glInitEgl13VERSION', 'glInitEgl14VERSION', 'glInitEgl15VERSION', 'platform', 'raw_eglQueryString', 'wl_display', 'wrapper']
def eglQueryDevicesEXT(max_devices = 10):
    ...
EGLQuerier: OpenGL.raw.EGL._types._EGLQuerier
EGL_ALPHA_FORMAT: OpenGL.constant.IntConstant
EGL_ALPHA_FORMAT_NONPRE: OpenGL.constant.IntConstant
EGL_ALPHA_FORMAT_PRE: OpenGL.constant.IntConstant
EGL_ALPHA_MASK_SIZE: OpenGL.constant.IntConstant
EGL_ALPHA_SIZE: OpenGL.constant.IntConstant
EGL_BACK_BUFFER: OpenGL.constant.IntConstant
EGL_BAD_ACCESS: OpenGL.constant.IntConstant
EGL_BAD_ALLOC: OpenGL.constant.IntConstant
EGL_BAD_ATTRIBUTE: OpenGL.constant.IntConstant
EGL_BAD_CONFIG: OpenGL.constant.IntConstant
EGL_BAD_CONTEXT: OpenGL.constant.IntConstant
EGL_BAD_CURRENT_SURFACE: OpenGL.constant.IntConstant
EGL_BAD_DISPLAY: OpenGL.constant.IntConstant
EGL_BAD_MATCH: OpenGL.constant.IntConstant
EGL_BAD_NATIVE_PIXMAP: OpenGL.constant.IntConstant
EGL_BAD_NATIVE_WINDOW: OpenGL.constant.IntConstant
EGL_BAD_PARAMETER: OpenGL.constant.IntConstant
EGL_BAD_SURFACE: OpenGL.constant.IntConstant
EGL_BIND_TO_TEXTURE_RGB: OpenGL.constant.IntConstant
EGL_BIND_TO_TEXTURE_RGBA: OpenGL.constant.IntConstant
EGL_BLUE_SIZE: OpenGL.constant.IntConstant
EGL_BUFFER_DESTROYED: OpenGL.constant.IntConstant
EGL_BUFFER_PRESERVED: OpenGL.constant.IntConstant
EGL_BUFFER_SIZE: OpenGL.constant.IntConstant
EGL_CLIENT_APIS: OpenGL.constant.IntConstant
EGL_CL_EVENT_HANDLE: OpenGL.constant.IntConstant
EGL_COLORSPACE: OpenGL.constant.IntConstant
EGL_COLORSPACE_LINEAR: OpenGL.constant.IntConstant
EGL_COLORSPACE_sRGB: OpenGL.constant.IntConstant
EGL_COLOR_BUFFER_TYPE: OpenGL.constant.IntConstant
EGL_CONDITION_SATISFIED: OpenGL.constant.IntConstant
EGL_CONFIG_CAVEAT: OpenGL.constant.IntConstant
EGL_CONFIG_ID: OpenGL.constant.IntConstant
EGL_CONFORMANT: OpenGL.constant.IntConstant
EGL_CONTEXT_CLIENT_TYPE: OpenGL.constant.IntConstant
EGL_CONTEXT_CLIENT_VERSION: OpenGL.constant.IntConstant
EGL_CONTEXT_LOST: OpenGL.constant.IntConstant
EGL_CONTEXT_MAJOR_VERSION: OpenGL.constant.IntConstant
EGL_CONTEXT_MINOR_VERSION: OpenGL.constant.IntConstant
EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT: OpenGL.constant.IntConstant
EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT: OpenGL.constant.IntConstant
EGL_CONTEXT_OPENGL_DEBUG: OpenGL.constant.IntConstant
EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE: OpenGL.constant.IntConstant
EGL_CONTEXT_OPENGL_PROFILE_MASK: OpenGL.constant.IntConstant
EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY: OpenGL.constant.IntConstant
EGL_CONTEXT_OPENGL_ROBUST_ACCESS: OpenGL.constant.IntConstant
EGL_CORE_NATIVE_ENGINE: OpenGL.constant.IntConstant
from OpenGL.EGL import EGL_DEFAULT_DISPLAY as EGL_DEFAULT_DISPLAY
EGL_DEPTH_SIZE: OpenGL.constant.IntConstant
EGL_DISPLAY_SCALING: OpenGL.constant.IntConstant
EGL_DONT_CARE: int = -1
EGL_DRAW: OpenGL.constant.IntConstant
EGL_EXTENSIONS: OpenGL.constant.IntConstant
EGL_FALSE: OpenGL.constant.IntConstant
EGL_FOREVER: OpenGL.constant.IntConstant
EGL_GL_COLORSPACE: OpenGL.constant.IntConstant
EGL_GL_COLORSPACE_LINEAR: OpenGL.constant.IntConstant
EGL_GL_COLORSPACE_SRGB: OpenGL.constant.IntConstant
EGL_GL_RENDERBUFFER: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_2D: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_3D: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_X: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_X: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Y: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Z: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_LEVEL: OpenGL.constant.IntConstant
EGL_GL_TEXTURE_ZOFFSET: OpenGL.constant.IntConstant
EGL_GREEN_SIZE: OpenGL.constant.IntConstant
EGL_HEIGHT: OpenGL.constant.IntConstant
EGL_HORIZONTAL_RESOLUTION: OpenGL.constant.IntConstant
EGL_IMAGE_PRESERVED: OpenGL.constant.IntConstant
EGL_LARGEST_PBUFFER: OpenGL.constant.IntConstant
EGL_LEVEL: OpenGL.constant.IntConstant
EGL_LOSE_CONTEXT_ON_RESET: OpenGL.constant.IntConstant
EGL_LUMINANCE_BUFFER: OpenGL.constant.IntConstant
EGL_LUMINANCE_SIZE: OpenGL.constant.IntConstant
EGL_MATCH_NATIVE_PIXMAP: OpenGL.constant.IntConstant
EGL_MAX_PBUFFER_HEIGHT: OpenGL.constant.IntConstant
EGL_MAX_PBUFFER_PIXELS: OpenGL.constant.IntConstant
EGL_MAX_PBUFFER_WIDTH: OpenGL.constant.IntConstant
EGL_MAX_SWAP_INTERVAL: OpenGL.constant.IntConstant
EGL_MIN_SWAP_INTERVAL: OpenGL.constant.IntConstant
EGL_MIPMAP_LEVEL: OpenGL.constant.IntConstant
EGL_MIPMAP_TEXTURE: OpenGL.constant.IntConstant
EGL_MULTISAMPLE_RESOLVE: OpenGL.constant.IntConstant
EGL_MULTISAMPLE_RESOLVE_BOX: OpenGL.constant.IntConstant
EGL_MULTISAMPLE_RESOLVE_BOX_BIT: OpenGL.constant.IntConstant
EGL_MULTISAMPLE_RESOLVE_DEFAULT: OpenGL.constant.IntConstant
EGL_NATIVE_RENDERABLE: OpenGL.constant.IntConstant
EGL_NATIVE_VISUAL_ID: OpenGL.constant.IntConstant
EGL_NATIVE_VISUAL_TYPE: OpenGL.constant.IntConstant
EGL_NONE: OpenGL.constant.IntConstant
EGL_NON_CONFORMANT_CONFIG: OpenGL.constant.IntConstant
EGL_NOT_INITIALIZED: OpenGL.constant.IntConstant
from OpenGL.EGL import EGL_NO_CONTEXT as EGL_NO_CONTEXT
from OpenGL.EGL import EGL_NO_DISPLAY as EGL_NO_DISPLAY
EGL_NO_RESET_NOTIFICATION: OpenGL.constant.IntConstant
from OpenGL.EGL import EGL_NO_SURFACE as EGL_NO_SURFACE
EGL_NO_TEXTURE: OpenGL.constant.IntConstant
EGL_OPENGL_API: OpenGL.constant.IntConstant
EGL_OPENGL_BIT: OpenGL.constant.IntConstant
EGL_OPENGL_ES2_BIT: OpenGL.constant.IntConstant
EGL_OPENGL_ES3_BIT: OpenGL.constant.IntConstant
EGL_OPENGL_ES_API: OpenGL.constant.IntConstant
EGL_OPENGL_ES_BIT: OpenGL.constant.IntConstant
EGL_OPENVG_API: OpenGL.constant.IntConstant
EGL_OPENVG_BIT: OpenGL.constant.IntConstant
EGL_OPENVG_IMAGE: OpenGL.constant.IntConstant
EGL_PBUFFER_BIT: OpenGL.constant.IntConstant
EGL_PIXEL_ASPECT_RATIO: OpenGL.constant.IntConstant
EGL_PIXMAP_BIT: OpenGL.constant.IntConstant
EGL_PLATFORM_DEVICE_EXT: int = 12607
EGL_READ: OpenGL.constant.IntConstant
EGL_RED_SIZE: OpenGL.constant.IntConstant
EGL_RENDERABLE_TYPE: OpenGL.constant.IntConstant
EGL_RENDER_BUFFER: OpenGL.constant.IntConstant
EGL_RGB_BUFFER: OpenGL.constant.IntConstant
EGL_SAMPLES: OpenGL.constant.IntConstant
EGL_SAMPLE_BUFFERS: OpenGL.constant.IntConstant
EGL_SIGNALED: OpenGL.constant.IntConstant
EGL_SINGLE_BUFFER: OpenGL.constant.IntConstant
EGL_SLOW_CONFIG: OpenGL.constant.IntConstant
EGL_STENCIL_SIZE: OpenGL.constant.IntConstant
EGL_SUCCESS: OpenGL.constant.IntConstant
EGL_SURFACE_TYPE: OpenGL.constant.IntConstant
EGL_SWAP_BEHAVIOR: OpenGL.constant.IntConstant
EGL_SWAP_BEHAVIOR_PRESERVED_BIT: OpenGL.constant.IntConstant
EGL_SYNC_CL_EVENT: OpenGL.constant.IntConstant
EGL_SYNC_CL_EVENT_COMPLETE: OpenGL.constant.IntConstant
EGL_SYNC_CONDITION: OpenGL.constant.IntConstant
EGL_SYNC_FENCE: OpenGL.constant.IntConstant
EGL_SYNC_FLUSH_COMMANDS_BIT: OpenGL.constant.IntConstant
EGL_SYNC_PRIOR_COMMANDS_COMPLETE: OpenGL.constant.IntConstant
EGL_SYNC_STATUS: OpenGL.constant.IntConstant
EGL_SYNC_TYPE: OpenGL.constant.IntConstant
EGL_TEXTURE_2D: OpenGL.constant.IntConstant
EGL_TEXTURE_FORMAT: OpenGL.constant.IntConstant
EGL_TEXTURE_RGB: OpenGL.constant.IntConstant
EGL_TEXTURE_RGBA: OpenGL.constant.IntConstant
EGL_TEXTURE_TARGET: OpenGL.constant.IntConstant
EGL_TIMEOUT_EXPIRED: OpenGL.constant.IntConstant
EGL_TRANSPARENT_BLUE_VALUE: OpenGL.constant.IntConstant
EGL_TRANSPARENT_GREEN_VALUE: OpenGL.constant.IntConstant
EGL_TRANSPARENT_RED_VALUE: OpenGL.constant.IntConstant
EGL_TRANSPARENT_RGB: OpenGL.constant.IntConstant
EGL_TRANSPARENT_TYPE: OpenGL.constant.IntConstant
EGL_TRUE: OpenGL.constant.IntConstant
EGL_UNSIGNALED: OpenGL.constant.IntConstant
EGL_VENDOR: OpenGL.constant.IntConstant
EGL_VERSION: OpenGL.constant.IntConstant
EGL_VERTICAL_RESOLUTION: OpenGL.constant.IntConstant
EGL_VG_ALPHA_FORMAT: OpenGL.constant.IntConstant
EGL_VG_ALPHA_FORMAT_NONPRE: OpenGL.constant.IntConstant
EGL_VG_ALPHA_FORMAT_PRE: OpenGL.constant.IntConstant
EGL_VG_ALPHA_FORMAT_PRE_BIT: OpenGL.constant.IntConstant
EGL_VG_COLORSPACE: OpenGL.constant.IntConstant
EGL_VG_COLORSPACE_LINEAR: OpenGL.constant.IntConstant
EGL_VG_COLORSPACE_LINEAR_BIT: OpenGL.constant.IntConstant
EGL_VG_COLORSPACE_sRGB: OpenGL.constant.IntConstant
EGL_WIDTH: OpenGL.constant.IntConstant
EGL_WINDOW_BIT: OpenGL.constant.IntConstant
_eglQueryDevicesEXT: _ctypes.CFuncPtr
from OpenGL.EGL import eglBindAPI as eglBindAPI
from OpenGL.EGL import eglBindTexImage as eglBindTexImage
from OpenGL.EGL import eglChooseConfig as eglChooseConfig
from OpenGL.EGL import eglClientWaitSync as eglClientWaitSync
from OpenGL.EGL import eglCopyBuffers as eglCopyBuffers
from OpenGL.EGL import eglCreateContext as eglCreateContext
from OpenGL.EGL import eglCreateImage as eglCreateImage
from OpenGL.EGL import eglCreatePbufferFromClientBuffer as eglCreatePbufferFromClientBuffer
from OpenGL.EGL import eglCreatePbufferSurface as eglCreatePbufferSurface
from OpenGL.EGL import eglCreatePixmapSurface as eglCreatePixmapSurface
from OpenGL.EGL import eglCreatePlatformPixmapSurface as eglCreatePlatformPixmapSurface
from OpenGL.EGL import eglCreatePlatformWindowSurface as eglCreatePlatformWindowSurface
from OpenGL.EGL import eglCreateSync as eglCreateSync
from OpenGL.EGL import eglCreateWindowSurface as eglCreateWindowSurface
from OpenGL.EGL import eglDestroyContext as eglDestroyContext
from OpenGL.EGL import eglDestroyImage as eglDestroyImage
from OpenGL.EGL import eglDestroySurface as eglDestroySurface
from OpenGL.EGL import eglDestroySync as eglDestroySync
from OpenGL.EGL import eglGetConfigAttrib as eglGetConfigAttrib
from OpenGL.EGL import eglGetConfigs as eglGetConfigs
from OpenGL.EGL import eglGetCurrentContext as eglGetCurrentContext
from OpenGL.EGL import eglGetCurrentDisplay as eglGetCurrentDisplay
from OpenGL.EGL import eglGetCurrentSurface as eglGetCurrentSurface
from OpenGL.EGL import eglGetDisplay as eglGetDisplay
from OpenGL.EGL import eglGetError as eglGetError
from OpenGL.EGL import eglGetPlatformDisplay as eglGetPlatformDisplay
from OpenGL.EGL import eglGetPlatformDisplayEXT as eglGetPlatformDisplayEXT
from OpenGL.EGL import eglGetProcAddress as eglGetProcAddress
from OpenGL.EGL import eglGetSyncAttrib as eglGetSyncAttrib
from OpenGL.EGL import eglInitialize as eglInitialize
from OpenGL.EGL import eglMakeCurrent as eglMakeCurrent
from OpenGL.EGL import eglQueryAPI as eglQueryAPI
from OpenGL.EGL import eglQueryContext as eglQueryContext
from OpenGL.EGL import eglQueryString as eglQueryString
from OpenGL.EGL import eglQuerySurface as eglQuerySurface
from OpenGL.EGL import eglReleaseTexImage as eglReleaseTexImage
from OpenGL.EGL import eglReleaseThread as eglReleaseThread
from OpenGL.EGL import eglSurfaceAttrib as eglSurfaceAttrib
from OpenGL.EGL import eglSwapBuffers as eglSwapBuffers
from OpenGL.EGL import eglSwapInterval as eglSwapInterval
from OpenGL.EGL import eglTerminate as eglTerminate
from OpenGL.EGL import eglWaitClient as eglWaitClient
from OpenGL.EGL import eglWaitGL as eglWaitGL
from OpenGL.EGL import eglWaitNative as eglWaitNative
from OpenGL.EGL import eglWaitSync as eglWaitSync
raw_eglQueryString: _ctypes.CFuncPtr
