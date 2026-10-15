"""
Extends OpenGL.EGL with definitions necessary for headless rendering.
"""
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
from OpenGL._opaque import EGLClientBuffer_pointer as EGLClientBuffer
from OpenGL._opaque import EGLConfig_pointer as EGLConfig
from OpenGL._opaque import EGLContext_pointer as EGLContext
from OpenGL._opaque import EGLDeviceEXT_pointer as EGLDeviceEXT
from OpenGL._opaque import EGLDisplay_pointer as EGLDisplay
from OpenGL._opaque import EGLImageKHR_pointer as EGLImage
from OpenGL._opaque import EGLImageKHR_pointer as EGLImageKHR
from OpenGL._opaque import EGLNativeDisplayType_pointer as EGLNativeDisplayType
from OpenGL._opaque import EGLNativeDisplayType_pointer as NativeDisplayType
from OpenGL._opaque import EGLNativePixmapType_pointer as NativePixmapType
from OpenGL._opaque import EGLNativePixmapType_pointer as EGLNativePixmapType
from OpenGL._opaque import EGLNativeWindowType_pointer as NativeWindowType
from OpenGL._opaque import EGLNativeWindowType_pointer as EGLNativeWindowType
from OpenGL._opaque import EGLOutputLayerEXT_pointer as EGLOutputLayerEXT
from OpenGL._opaque import EGLOutputPortEXT_pointer as EGLOutputPortEXT
from OpenGL._opaque import EGLStream_pointer as EGLStreamKHR
from OpenGL._opaque import EGLSurface_pointer as EGLSurface
from OpenGL._opaque import EGLSync_pointer as EGLSyncNV
from OpenGL._opaque import EGLSync_pointer as EGLSync
from OpenGL._opaque import EGLSync_pointer as EGLSyncKHR
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
from OpenGL.raw.EGL._types import wl_display
from OpenGL import wrapper
import _ctypes
import ctypes as ctypes
from ctypes import CFUNCTYPE as CALLBACK_TYPE
from ctypes import c_int as EGLNativeFileDescriptorKHR
from ctypes import c_int
from ctypes import c_int as EGLint
from ctypes import c_uint as EGLBoolean
from ctypes import c_uint as EGLenum
from ctypes import c_ulong as EGLScreenMESA
from ctypes import c_ulong as EGLuint64NV
from ctypes import c_ulong as EGLuint64KHR
from ctypes import c_ulong as EGLTime
from ctypes import c_ulong as EGLTimeKHR
from ctypes import c_ulong as EGLsizeiANDROID
from ctypes import c_ulong as EGLTimeNV
from ctypes import c_ulong as EGLModeMESA
from glfw import LP_c_int as EGLAttrib
from glfw import LP_c_int as EGLAttribKHR
__all__: list[str] = ['CALLBACK_TYPE', 'EGL', 'EGLAttrib', 'EGLAttribKHR', 'EGLBoolean', 'EGLClientBuffer', 'EGLClientPixmapHI', 'EGLConfig', 'EGLContext', 'EGLDeviceEXT', 'EGLDisplay', 'EGLError', 'EGLImage', 'EGLImageKHR', 'EGLModeMESA', 'EGLNativeDisplayType', 'EGLNativeFileDescriptorKHR', 'EGLNativePixmapType', 'EGLNativeWindowType', 'EGLOutputLayerEXT', 'EGLOutputPortEXT', 'EGLQuerier', 'EGLScreenMESA', 'EGLStreamKHR', 'EGLSurface', 'EGLSync', 'EGLSyncKHR', 'EGLSyncNV', 'EGLTime', 'EGLTimeKHR', 'EGLTimeNV', 'EGL_ALPHA_FORMAT', 'EGL_ALPHA_FORMAT_NONPRE', 'EGL_ALPHA_FORMAT_PRE', 'EGL_ALPHA_MASK_SIZE', 'EGL_ALPHA_SIZE', 'EGL_BACK_BUFFER', 'EGL_BAD_ACCESS', 'EGL_BAD_ALLOC', 'EGL_BAD_ATTRIBUTE', 'EGL_BAD_CONFIG', 'EGL_BAD_CONTEXT', 'EGL_BAD_CURRENT_SURFACE', 'EGL_BAD_DISPLAY', 'EGL_BAD_MATCH', 'EGL_BAD_NATIVE_PIXMAP', 'EGL_BAD_NATIVE_WINDOW', 'EGL_BAD_PARAMETER', 'EGL_BAD_SURFACE', 'EGL_BIND_TO_TEXTURE_RGB', 'EGL_BIND_TO_TEXTURE_RGBA', 'EGL_BLUE_SIZE', 'EGL_BUFFER_DESTROYED', 'EGL_BUFFER_PRESERVED', 'EGL_BUFFER_SIZE', 'EGL_CLIENT_APIS', 'EGL_CL_EVENT_HANDLE', 'EGL_COLORSPACE', 'EGL_COLORSPACE_LINEAR', 'EGL_COLORSPACE_sRGB', 'EGL_COLOR_BUFFER_TYPE', 'EGL_CONDITION_SATISFIED', 'EGL_CONFIG_CAVEAT', 'EGL_CONFIG_ID', 'EGL_CONFORMANT', 'EGL_CONTEXT_CLIENT_TYPE', 'EGL_CONTEXT_CLIENT_VERSION', 'EGL_CONTEXT_LOST', 'EGL_CONTEXT_MAJOR_VERSION', 'EGL_CONTEXT_MINOR_VERSION', 'EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT', 'EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT', 'EGL_CONTEXT_OPENGL_DEBUG', 'EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE', 'EGL_CONTEXT_OPENGL_PROFILE_MASK', 'EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY', 'EGL_CONTEXT_OPENGL_ROBUST_ACCESS', 'EGL_CORE_NATIVE_ENGINE', 'EGL_DEFAULT_DISPLAY', 'EGL_DEPTH_SIZE', 'EGL_DISPLAY_SCALING', 'EGL_DONT_CARE', 'EGL_DRAW', 'EGL_EXTENSIONS', 'EGL_FALSE', 'EGL_FOREVER', 'EGL_GL_COLORSPACE', 'EGL_GL_COLORSPACE_LINEAR', 'EGL_GL_COLORSPACE_SRGB', 'EGL_GL_RENDERBUFFER', 'EGL_GL_TEXTURE_2D', 'EGL_GL_TEXTURE_3D', 'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_X', 'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y', 'EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z', 'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_X', 'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Y', 'EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Z', 'EGL_GL_TEXTURE_LEVEL', 'EGL_GL_TEXTURE_ZOFFSET', 'EGL_GREEN_SIZE', 'EGL_HEIGHT', 'EGL_HORIZONTAL_RESOLUTION', 'EGL_IMAGE_PRESERVED', 'EGL_LARGEST_PBUFFER', 'EGL_LEVEL', 'EGL_LOSE_CONTEXT_ON_RESET', 'EGL_LUMINANCE_BUFFER', 'EGL_LUMINANCE_SIZE', 'EGL_MATCH_NATIVE_PIXMAP', 'EGL_MAX_PBUFFER_HEIGHT', 'EGL_MAX_PBUFFER_PIXELS', 'EGL_MAX_PBUFFER_WIDTH', 'EGL_MAX_SWAP_INTERVAL', 'EGL_MIN_SWAP_INTERVAL', 'EGL_MIPMAP_LEVEL', 'EGL_MIPMAP_TEXTURE', 'EGL_MULTISAMPLE_RESOLVE', 'EGL_MULTISAMPLE_RESOLVE_BOX', 'EGL_MULTISAMPLE_RESOLVE_BOX_BIT', 'EGL_MULTISAMPLE_RESOLVE_DEFAULT', 'EGL_NATIVE_RENDERABLE', 'EGL_NATIVE_VISUAL_ID', 'EGL_NATIVE_VISUAL_TYPE', 'EGL_NONE', 'EGL_NON_CONFORMANT_CONFIG', 'EGL_NOT_INITIALIZED', 'EGL_NO_CONTEXT', 'EGL_NO_DISPLAY', 'EGL_NO_RESET_NOTIFICATION', 'EGL_NO_SURFACE', 'EGL_NO_TEXTURE', 'EGL_OPENGL_API', 'EGL_OPENGL_BIT', 'EGL_OPENGL_ES2_BIT', 'EGL_OPENGL_ES3_BIT', 'EGL_OPENGL_ES_API', 'EGL_OPENGL_ES_BIT', 'EGL_OPENVG_API', 'EGL_OPENVG_BIT', 'EGL_OPENVG_IMAGE', 'EGL_PBUFFER_BIT', 'EGL_PIXEL_ASPECT_RATIO', 'EGL_PIXMAP_BIT', 'EGL_PLATFORM_DEVICE_EXT', 'EGL_READ', 'EGL_RED_SIZE', 'EGL_RENDERABLE_TYPE', 'EGL_RENDER_BUFFER', 'EGL_RGB_BUFFER', 'EGL_SAMPLES', 'EGL_SAMPLE_BUFFERS', 'EGL_SIGNALED', 'EGL_SINGLE_BUFFER', 'EGL_SLOW_CONFIG', 'EGL_STENCIL_SIZE', 'EGL_SUCCESS', 'EGL_SURFACE_TYPE', 'EGL_SWAP_BEHAVIOR', 'EGL_SWAP_BEHAVIOR_PRESERVED_BIT', 'EGL_SYNC_CL_EVENT', 'EGL_SYNC_CL_EVENT_COMPLETE', 'EGL_SYNC_CONDITION', 'EGL_SYNC_FENCE', 'EGL_SYNC_FLUSH_COMMANDS_BIT', 'EGL_SYNC_PRIOR_COMMANDS_COMPLETE', 'EGL_SYNC_STATUS', 'EGL_SYNC_TYPE', 'EGL_TEXTURE_2D', 'EGL_TEXTURE_FORMAT', 'EGL_TEXTURE_RGB', 'EGL_TEXTURE_RGBA', 'EGL_TEXTURE_TARGET', 'EGL_TIMEOUT_EXPIRED', 'EGL_TRANSPARENT_BLUE_VALUE', 'EGL_TRANSPARENT_GREEN_VALUE', 'EGL_TRANSPARENT_RED_VALUE', 'EGL_TRANSPARENT_RGB', 'EGL_TRANSPARENT_TYPE', 'EGL_TRUE', 'EGL_UNSIGNALED', 'EGL_VENDOR', 'EGL_VERSION', 'EGL_VERTICAL_RESOLUTION', 'EGL_VG_ALPHA_FORMAT', 'EGL_VG_ALPHA_FORMAT_NONPRE', 'EGL_VG_ALPHA_FORMAT_PRE', 'EGL_VG_ALPHA_FORMAT_PRE_BIT', 'EGL_VG_COLORSPACE', 'EGL_VG_COLORSPACE_LINEAR', 'EGL_VG_COLORSPACE_LINEAR_BIT', 'EGL_VG_COLORSPACE_sRGB', 'EGL_WIDTH', 'EGL_WINDOW_BIT', 'EGLenum', 'EGLint', 'EGLsizeiANDROID', 'EGLuint64KHR', 'EGLuint64NV', 'EXT', 'NativeDisplayType', 'NativePixmapType', 'NativeWindowType', 'VERSION', 'arrays', 'as_8_bit', 'c_int', 'constant', 'ctypes', 'ctypesloader', 'eglBindAPI', 'eglBindTexImage', 'eglChooseConfig', 'eglClientWaitSync', 'eglCopyBuffers', 'eglCreateContext', 'eglCreateImage', 'eglCreatePbufferFromClientBuffer', 'eglCreatePbufferSurface', 'eglCreatePixmapSurface', 'eglCreatePlatformPixmapSurface', 'eglCreatePlatformWindowSurface', 'eglCreateSync', 'eglCreateWindowSurface', 'eglDestroyContext', 'eglDestroyImage', 'eglDestroySurface', 'eglDestroySync', 'eglGetConfigAttrib', 'eglGetConfigs', 'eglGetCurrentContext', 'eglGetCurrentDisplay', 'eglGetCurrentSurface', 'eglGetDisplay', 'eglGetError', 'eglGetPlatformDisplay', 'eglGetPlatformDisplayEXT', 'eglGetProcAddress', 'eglGetSyncAttrib', 'eglInitialize', 'eglMakeCurrent', 'eglQueryAPI', 'eglQueryContext', 'eglQueryDevicesEXT', 'eglQueryString', 'eglQuerySurface', 'eglReleaseTexImage', 'eglReleaseThread', 'eglSurfaceAttrib', 'eglSwapBuffers', 'eglSwapInterval', 'eglTerminate', 'eglWaitClient', 'eglWaitGL', 'eglWaitNative', 'eglWaitSync', 'error', 'extensions', 'glInitEgl10VERSION', 'glInitEgl11VERSION', 'glInitEgl12VERSION', 'glInitEgl13VERSION', 'glInitEgl14VERSION', 'glInitEgl15VERSION', 'platform', 'raw_eglQueryString', 'wl_display', 'wrapper']
def eglQueryDevicesEXT(max_devices = 10):
    ...
EGLQuerier: OpenGL.raw.EGL._types._EGLQuerier  # value = <OpenGL.raw.EGL._types._EGLQuerier object>
EGL_ALPHA_FORMAT: OpenGL.constant.IntConstant  # value = EGL_ALPHA_FORMAT
EGL_ALPHA_FORMAT_NONPRE: OpenGL.constant.IntConstant  # value = EGL_ALPHA_FORMAT_NONPRE
EGL_ALPHA_FORMAT_PRE: OpenGL.constant.IntConstant  # value = EGL_ALPHA_FORMAT_PRE
EGL_ALPHA_MASK_SIZE: OpenGL.constant.IntConstant  # value = EGL_ALPHA_MASK_SIZE
EGL_ALPHA_SIZE: OpenGL.constant.IntConstant  # value = EGL_ALPHA_SIZE
EGL_BACK_BUFFER: OpenGL.constant.IntConstant  # value = EGL_BACK_BUFFER
EGL_BAD_ACCESS: OpenGL.constant.IntConstant  # value = EGL_BAD_ACCESS
EGL_BAD_ALLOC: OpenGL.constant.IntConstant  # value = EGL_BAD_ALLOC
EGL_BAD_ATTRIBUTE: OpenGL.constant.IntConstant  # value = EGL_BAD_ATTRIBUTE
EGL_BAD_CONFIG: OpenGL.constant.IntConstant  # value = EGL_BAD_CONFIG
EGL_BAD_CONTEXT: OpenGL.constant.IntConstant  # value = EGL_BAD_CONTEXT
EGL_BAD_CURRENT_SURFACE: OpenGL.constant.IntConstant  # value = EGL_BAD_CURRENT_SURFACE
EGL_BAD_DISPLAY: OpenGL.constant.IntConstant  # value = EGL_BAD_DISPLAY
EGL_BAD_MATCH: OpenGL.constant.IntConstant  # value = EGL_BAD_MATCH
EGL_BAD_NATIVE_PIXMAP: OpenGL.constant.IntConstant  # value = EGL_BAD_NATIVE_PIXMAP
EGL_BAD_NATIVE_WINDOW: OpenGL.constant.IntConstant  # value = EGL_BAD_NATIVE_WINDOW
EGL_BAD_PARAMETER: OpenGL.constant.IntConstant  # value = EGL_BAD_PARAMETER
EGL_BAD_SURFACE: OpenGL.constant.IntConstant  # value = EGL_BAD_SURFACE
EGL_BIND_TO_TEXTURE_RGB: OpenGL.constant.IntConstant  # value = EGL_BIND_TO_TEXTURE_RGB
EGL_BIND_TO_TEXTURE_RGBA: OpenGL.constant.IntConstant  # value = EGL_BIND_TO_TEXTURE_RGBA
EGL_BLUE_SIZE: OpenGL.constant.IntConstant  # value = EGL_BLUE_SIZE
EGL_BUFFER_DESTROYED: OpenGL.constant.IntConstant  # value = EGL_BUFFER_DESTROYED
EGL_BUFFER_PRESERVED: OpenGL.constant.IntConstant  # value = EGL_BUFFER_PRESERVED
EGL_BUFFER_SIZE: OpenGL.constant.IntConstant  # value = EGL_BUFFER_SIZE
EGL_CLIENT_APIS: OpenGL.constant.IntConstant  # value = EGL_CLIENT_APIS
EGL_CL_EVENT_HANDLE: OpenGL.constant.IntConstant  # value = EGL_CL_EVENT_HANDLE
EGL_COLORSPACE: OpenGL.constant.IntConstant  # value = EGL_COLORSPACE
EGL_COLORSPACE_LINEAR: OpenGL.constant.IntConstant  # value = EGL_COLORSPACE_LINEAR
EGL_COLORSPACE_sRGB: OpenGL.constant.IntConstant  # value = EGL_COLORSPACE_sRGB
EGL_COLOR_BUFFER_TYPE: OpenGL.constant.IntConstant  # value = EGL_COLOR_BUFFER_TYPE
EGL_CONDITION_SATISFIED: OpenGL.constant.IntConstant  # value = EGL_CONDITION_SATISFIED
EGL_CONFIG_CAVEAT: OpenGL.constant.IntConstant  # value = EGL_CONFIG_CAVEAT
EGL_CONFIG_ID: OpenGL.constant.IntConstant  # value = EGL_CONFIG_ID
EGL_CONFORMANT: OpenGL.constant.IntConstant  # value = EGL_CONFORMANT
EGL_CONTEXT_CLIENT_TYPE: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_CLIENT_TYPE
EGL_CONTEXT_CLIENT_VERSION: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_CLIENT_VERSION
EGL_CONTEXT_LOST: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_LOST
EGL_CONTEXT_MAJOR_VERSION: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_MAJOR_VERSION
EGL_CONTEXT_MINOR_VERSION: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_MINOR_VERSION
EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_OPENGL_COMPATIBILITY_PROFILE_BIT
EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT
EGL_CONTEXT_OPENGL_DEBUG: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_OPENGL_DEBUG
EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_OPENGL_FORWARD_COMPATIBLE
EGL_CONTEXT_OPENGL_PROFILE_MASK: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_OPENGL_PROFILE_MASK
EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_OPENGL_RESET_NOTIFICATION_STRATEGY
EGL_CONTEXT_OPENGL_ROBUST_ACCESS: OpenGL.constant.IntConstant  # value = EGL_CONTEXT_OPENGL_ROBUST_ACCESS
EGL_CORE_NATIVE_ENGINE: OpenGL.constant.IntConstant  # value = EGL_CORE_NATIVE_ENGINE
EGL_DEFAULT_DISPLAY: OpenGL._opaque.EGLNativeDisplayType_pointer  # value = <OpenGL._opaque.EGLNativeDisplayType_pointer object>
EGL_DEPTH_SIZE: OpenGL.constant.IntConstant  # value = EGL_DEPTH_SIZE
EGL_DISPLAY_SCALING: OpenGL.constant.IntConstant  # value = EGL_DISPLAY_SCALING
EGL_DONT_CARE: int = -1
EGL_DRAW: OpenGL.constant.IntConstant  # value = EGL_DRAW
EGL_EXTENSIONS: OpenGL.constant.IntConstant  # value = EGL_EXTENSIONS
EGL_FALSE: OpenGL.constant.IntConstant  # value = EGL_FALSE
EGL_FOREVER: OpenGL.constant.IntConstant  # value = EGL_FOREVER
EGL_GL_COLORSPACE: OpenGL.constant.IntConstant  # value = EGL_GL_COLORSPACE
EGL_GL_COLORSPACE_LINEAR: OpenGL.constant.IntConstant  # value = EGL_GL_COLORSPACE_LINEAR
EGL_GL_COLORSPACE_SRGB: OpenGL.constant.IntConstant  # value = EGL_GL_COLORSPACE_SRGB
EGL_GL_RENDERBUFFER: OpenGL.constant.IntConstant  # value = EGL_GL_RENDERBUFFER
EGL_GL_TEXTURE_2D: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_2D
EGL_GL_TEXTURE_3D: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_3D
EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_X: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_X
EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Y
EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_CUBE_MAP_NEGATIVE_Z
EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_X: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_X
EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Y: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Y
EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Z: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_CUBE_MAP_POSITIVE_Z
EGL_GL_TEXTURE_LEVEL: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_LEVEL
EGL_GL_TEXTURE_ZOFFSET: OpenGL.constant.IntConstant  # value = EGL_GL_TEXTURE_ZOFFSET
EGL_GREEN_SIZE: OpenGL.constant.IntConstant  # value = EGL_GREEN_SIZE
EGL_HEIGHT: OpenGL.constant.IntConstant  # value = EGL_HEIGHT
EGL_HORIZONTAL_RESOLUTION: OpenGL.constant.IntConstant  # value = EGL_HORIZONTAL_RESOLUTION
EGL_IMAGE_PRESERVED: OpenGL.constant.IntConstant  # value = EGL_IMAGE_PRESERVED
EGL_LARGEST_PBUFFER: OpenGL.constant.IntConstant  # value = EGL_LARGEST_PBUFFER
EGL_LEVEL: OpenGL.constant.IntConstant  # value = EGL_LEVEL
EGL_LOSE_CONTEXT_ON_RESET: OpenGL.constant.IntConstant  # value = EGL_LOSE_CONTEXT_ON_RESET
EGL_LUMINANCE_BUFFER: OpenGL.constant.IntConstant  # value = EGL_LUMINANCE_BUFFER
EGL_LUMINANCE_SIZE: OpenGL.constant.IntConstant  # value = EGL_LUMINANCE_SIZE
EGL_MATCH_NATIVE_PIXMAP: OpenGL.constant.IntConstant  # value = EGL_MATCH_NATIVE_PIXMAP
EGL_MAX_PBUFFER_HEIGHT: OpenGL.constant.IntConstant  # value = EGL_MAX_PBUFFER_HEIGHT
EGL_MAX_PBUFFER_PIXELS: OpenGL.constant.IntConstant  # value = EGL_MAX_PBUFFER_PIXELS
EGL_MAX_PBUFFER_WIDTH: OpenGL.constant.IntConstant  # value = EGL_MAX_PBUFFER_WIDTH
EGL_MAX_SWAP_INTERVAL: OpenGL.constant.IntConstant  # value = EGL_MAX_SWAP_INTERVAL
EGL_MIN_SWAP_INTERVAL: OpenGL.constant.IntConstant  # value = EGL_MIN_SWAP_INTERVAL
EGL_MIPMAP_LEVEL: OpenGL.constant.IntConstant  # value = EGL_MIPMAP_LEVEL
EGL_MIPMAP_TEXTURE: OpenGL.constant.IntConstant  # value = EGL_MIPMAP_TEXTURE
EGL_MULTISAMPLE_RESOLVE: OpenGL.constant.IntConstant  # value = EGL_MULTISAMPLE_RESOLVE
EGL_MULTISAMPLE_RESOLVE_BOX: OpenGL.constant.IntConstant  # value = EGL_MULTISAMPLE_RESOLVE_BOX
EGL_MULTISAMPLE_RESOLVE_BOX_BIT: OpenGL.constant.IntConstant  # value = EGL_MULTISAMPLE_RESOLVE_BOX_BIT
EGL_MULTISAMPLE_RESOLVE_DEFAULT: OpenGL.constant.IntConstant  # value = EGL_MULTISAMPLE_RESOLVE_DEFAULT
EGL_NATIVE_RENDERABLE: OpenGL.constant.IntConstant  # value = EGL_NATIVE_RENDERABLE
EGL_NATIVE_VISUAL_ID: OpenGL.constant.IntConstant  # value = EGL_NATIVE_VISUAL_ID
EGL_NATIVE_VISUAL_TYPE: OpenGL.constant.IntConstant  # value = EGL_NATIVE_VISUAL_TYPE
EGL_NONE: OpenGL.constant.IntConstant  # value = EGL_NONE
EGL_NON_CONFORMANT_CONFIG: OpenGL.constant.IntConstant  # value = EGL_NON_CONFORMANT_CONFIG
EGL_NOT_INITIALIZED: OpenGL.constant.IntConstant  # value = EGL_NOT_INITIALIZED
EGL_NO_CONTEXT: OpenGL._opaque.EGLContext_pointer  # value = <OpenGL._opaque.EGLContext_pointer object>
EGL_NO_DISPLAY: OpenGL._opaque.EGLDisplay_pointer  # value = <OpenGL._opaque.EGLDisplay_pointer object>
EGL_NO_RESET_NOTIFICATION: OpenGL.constant.IntConstant  # value = EGL_NO_RESET_NOTIFICATION
EGL_NO_SURFACE: OpenGL._opaque.EGLSurface_pointer  # value = <OpenGL._opaque.EGLSurface_pointer object>
EGL_NO_TEXTURE: OpenGL.constant.IntConstant  # value = EGL_NO_TEXTURE
EGL_OPENGL_API: OpenGL.constant.IntConstant  # value = EGL_OPENGL_API
EGL_OPENGL_BIT: OpenGL.constant.IntConstant  # value = EGL_OPENGL_BIT
EGL_OPENGL_ES2_BIT: OpenGL.constant.IntConstant  # value = EGL_OPENGL_ES2_BIT
EGL_OPENGL_ES3_BIT: OpenGL.constant.IntConstant  # value = EGL_OPENGL_ES3_BIT
EGL_OPENGL_ES_API: OpenGL.constant.IntConstant  # value = EGL_OPENGL_ES_API
EGL_OPENGL_ES_BIT: OpenGL.constant.IntConstant  # value = EGL_OPENGL_ES_BIT
EGL_OPENVG_API: OpenGL.constant.IntConstant  # value = EGL_OPENVG_API
EGL_OPENVG_BIT: OpenGL.constant.IntConstant  # value = EGL_OPENVG_BIT
EGL_OPENVG_IMAGE: OpenGL.constant.IntConstant  # value = EGL_OPENVG_IMAGE
EGL_PBUFFER_BIT: OpenGL.constant.IntConstant  # value = EGL_PBUFFER_BIT
EGL_PIXEL_ASPECT_RATIO: OpenGL.constant.IntConstant  # value = EGL_PIXEL_ASPECT_RATIO
EGL_PIXMAP_BIT: OpenGL.constant.IntConstant  # value = EGL_PIXMAP_BIT
EGL_PLATFORM_DEVICE_EXT: int = 12607
EGL_READ: OpenGL.constant.IntConstant  # value = EGL_READ
EGL_RED_SIZE: OpenGL.constant.IntConstant  # value = EGL_RED_SIZE
EGL_RENDERABLE_TYPE: OpenGL.constant.IntConstant  # value = EGL_RENDERABLE_TYPE
EGL_RENDER_BUFFER: OpenGL.constant.IntConstant  # value = EGL_RENDER_BUFFER
EGL_RGB_BUFFER: OpenGL.constant.IntConstant  # value = EGL_RGB_BUFFER
EGL_SAMPLES: OpenGL.constant.IntConstant  # value = EGL_SAMPLES
EGL_SAMPLE_BUFFERS: OpenGL.constant.IntConstant  # value = EGL_SAMPLE_BUFFERS
EGL_SIGNALED: OpenGL.constant.IntConstant  # value = EGL_SIGNALED
EGL_SINGLE_BUFFER: OpenGL.constant.IntConstant  # value = EGL_SINGLE_BUFFER
EGL_SLOW_CONFIG: OpenGL.constant.IntConstant  # value = EGL_SLOW_CONFIG
EGL_STENCIL_SIZE: OpenGL.constant.IntConstant  # value = EGL_STENCIL_SIZE
EGL_SUCCESS: OpenGL.constant.IntConstant  # value = EGL_SUCCESS
EGL_SURFACE_TYPE: OpenGL.constant.IntConstant  # value = EGL_SURFACE_TYPE
EGL_SWAP_BEHAVIOR: OpenGL.constant.IntConstant  # value = EGL_SWAP_BEHAVIOR
EGL_SWAP_BEHAVIOR_PRESERVED_BIT: OpenGL.constant.IntConstant  # value = EGL_SWAP_BEHAVIOR_PRESERVED_BIT
EGL_SYNC_CL_EVENT: OpenGL.constant.IntConstant  # value = EGL_SYNC_CL_EVENT
EGL_SYNC_CL_EVENT_COMPLETE: OpenGL.constant.IntConstant  # value = EGL_SYNC_CL_EVENT_COMPLETE
EGL_SYNC_CONDITION: OpenGL.constant.IntConstant  # value = EGL_SYNC_CONDITION
EGL_SYNC_FENCE: OpenGL.constant.IntConstant  # value = EGL_SYNC_FENCE
EGL_SYNC_FLUSH_COMMANDS_BIT: OpenGL.constant.IntConstant  # value = EGL_SYNC_FLUSH_COMMANDS_BIT
EGL_SYNC_PRIOR_COMMANDS_COMPLETE: OpenGL.constant.IntConstant  # value = EGL_SYNC_PRIOR_COMMANDS_COMPLETE
EGL_SYNC_STATUS: OpenGL.constant.IntConstant  # value = EGL_SYNC_STATUS
EGL_SYNC_TYPE: OpenGL.constant.IntConstant  # value = EGL_SYNC_TYPE
EGL_TEXTURE_2D: OpenGL.constant.IntConstant  # value = EGL_TEXTURE_2D
EGL_TEXTURE_FORMAT: OpenGL.constant.IntConstant  # value = EGL_TEXTURE_FORMAT
EGL_TEXTURE_RGB: OpenGL.constant.IntConstant  # value = EGL_TEXTURE_RGB
EGL_TEXTURE_RGBA: OpenGL.constant.IntConstant  # value = EGL_TEXTURE_RGBA
EGL_TEXTURE_TARGET: OpenGL.constant.IntConstant  # value = EGL_TEXTURE_TARGET
EGL_TIMEOUT_EXPIRED: OpenGL.constant.IntConstant  # value = EGL_TIMEOUT_EXPIRED
EGL_TRANSPARENT_BLUE_VALUE: OpenGL.constant.IntConstant  # value = EGL_TRANSPARENT_BLUE_VALUE
EGL_TRANSPARENT_GREEN_VALUE: OpenGL.constant.IntConstant  # value = EGL_TRANSPARENT_GREEN_VALUE
EGL_TRANSPARENT_RED_VALUE: OpenGL.constant.IntConstant  # value = EGL_TRANSPARENT_RED_VALUE
EGL_TRANSPARENT_RGB: OpenGL.constant.IntConstant  # value = EGL_TRANSPARENT_RGB
EGL_TRANSPARENT_TYPE: OpenGL.constant.IntConstant  # value = EGL_TRANSPARENT_TYPE
EGL_TRUE: OpenGL.constant.IntConstant  # value = EGL_TRUE
EGL_UNSIGNALED: OpenGL.constant.IntConstant  # value = EGL_UNSIGNALED
EGL_VENDOR: OpenGL.constant.IntConstant  # value = EGL_VENDOR
EGL_VERSION: OpenGL.constant.IntConstant  # value = EGL_VERSION
EGL_VERTICAL_RESOLUTION: OpenGL.constant.IntConstant  # value = EGL_VERTICAL_RESOLUTION
EGL_VG_ALPHA_FORMAT: OpenGL.constant.IntConstant  # value = EGL_VG_ALPHA_FORMAT
EGL_VG_ALPHA_FORMAT_NONPRE: OpenGL.constant.IntConstant  # value = EGL_VG_ALPHA_FORMAT_NONPRE
EGL_VG_ALPHA_FORMAT_PRE: OpenGL.constant.IntConstant  # value = EGL_VG_ALPHA_FORMAT_PRE
EGL_VG_ALPHA_FORMAT_PRE_BIT: OpenGL.constant.IntConstant  # value = EGL_VG_ALPHA_FORMAT_PRE_BIT
EGL_VG_COLORSPACE: OpenGL.constant.IntConstant  # value = EGL_VG_COLORSPACE
EGL_VG_COLORSPACE_LINEAR: OpenGL.constant.IntConstant  # value = EGL_VG_COLORSPACE_LINEAR
EGL_VG_COLORSPACE_LINEAR_BIT: OpenGL.constant.IntConstant  # value = EGL_VG_COLORSPACE_LINEAR_BIT
EGL_VG_COLORSPACE_sRGB: OpenGL.constant.IntConstant  # value = EGL_VG_COLORSPACE_sRGB
EGL_WIDTH: OpenGL.constant.IntConstant  # value = EGL_WIDTH
EGL_WINDOW_BIT: OpenGL.constant.IntConstant  # value = EGL_WINDOW_BIT
_eglQueryDevicesEXT: _ctypes.CFuncPtr  # value = <CFunctionType object>
eglBindAPI: OpenGL.platform.baseplatform.eglBindAPI  # value = <OpenGL.platform.baseplatform.eglBindAPI object>
eglBindTexImage: OpenGL.platform.baseplatform.eglBindTexImage  # value = <OpenGL.platform.baseplatform.eglBindTexImage object>
eglChooseConfig: OpenGL.platform.baseplatform.eglChooseConfig  # value = <OpenGL.platform.baseplatform.eglChooseConfig object>
eglClientWaitSync: OpenGL.platform.baseplatform.eglClientWaitSync  # value = <OpenGL.platform.baseplatform.eglClientWaitSync object>
eglCopyBuffers: OpenGL.platform.baseplatform.eglCopyBuffers  # value = <OpenGL.platform.baseplatform.eglCopyBuffers object>
eglCreateContext: OpenGL.platform.baseplatform.eglCreateContext  # value = <OpenGL.platform.baseplatform.eglCreateContext object>
eglCreateImage: OpenGL.platform.baseplatform.eglCreateImage  # value = <OpenGL.platform.baseplatform.eglCreateImage object>
eglCreatePbufferFromClientBuffer: OpenGL.platform.baseplatform.eglCreatePbufferFromClientBuffer  # value = <OpenGL.platform.baseplatform.eglCreatePbufferFromClientBuffer object>
eglCreatePbufferSurface: OpenGL.platform.baseplatform.eglCreatePbufferSurface  # value = <OpenGL.platform.baseplatform.eglCreatePbufferSurface object>
eglCreatePixmapSurface: OpenGL.platform.baseplatform.eglCreatePixmapSurface  # value = <OpenGL.platform.baseplatform.eglCreatePixmapSurface object>
eglCreatePlatformPixmapSurface: OpenGL.platform.baseplatform.eglCreatePlatformPixmapSurface  # value = <OpenGL.platform.baseplatform.eglCreatePlatformPixmapSurface object>
eglCreatePlatformWindowSurface: OpenGL.platform.baseplatform.eglCreatePlatformWindowSurface  # value = <OpenGL.platform.baseplatform.eglCreatePlatformWindowSurface object>
eglCreateSync: OpenGL.platform.baseplatform.eglCreateSync  # value = <OpenGL.platform.baseplatform.eglCreateSync object>
eglCreateWindowSurface: OpenGL.platform.baseplatform.eglCreateWindowSurface  # value = <OpenGL.platform.baseplatform.eglCreateWindowSurface object>
eglDestroyContext: OpenGL.platform.baseplatform.eglDestroyContext  # value = <OpenGL.platform.baseplatform.eglDestroyContext object>
eglDestroyImage: OpenGL.platform.baseplatform.eglDestroyImage  # value = <OpenGL.platform.baseplatform.eglDestroyImage object>
eglDestroySurface: OpenGL.platform.baseplatform.eglDestroySurface  # value = <OpenGL.platform.baseplatform.eglDestroySurface object>
eglDestroySync: OpenGL.platform.baseplatform.eglDestroySync  # value = <OpenGL.platform.baseplatform.eglDestroySync object>
eglGetConfigAttrib: OpenGL.platform.baseplatform.eglGetConfigAttrib  # value = <OpenGL.platform.baseplatform.eglGetConfigAttrib object>
eglGetConfigs: OpenGL.platform.baseplatform.eglGetConfigs  # value = <OpenGL.platform.baseplatform.eglGetConfigs object>
eglGetCurrentContext: OpenGL.platform.baseplatform.eglGetCurrentContext  # value = <OpenGL.platform.baseplatform.eglGetCurrentContext object>
eglGetCurrentDisplay: OpenGL.platform.baseplatform.eglGetCurrentDisplay  # value = <OpenGL.platform.baseplatform.eglGetCurrentDisplay object>
eglGetCurrentSurface: OpenGL.platform.baseplatform.eglGetCurrentSurface  # value = <OpenGL.platform.baseplatform.eglGetCurrentSurface object>
eglGetDisplay: OpenGL.platform.baseplatform.eglGetDisplay  # value = <OpenGL.platform.baseplatform.eglGetDisplay object>
eglGetError: OpenGL.platform.baseplatform.eglGetError  # value = <OpenGL.platform.baseplatform.eglGetError object>
eglGetPlatformDisplay: OpenGL.extensions.eglGetPlatformDisplay  # value = <OpenGL.extensions.eglGetPlatformDisplay object>
eglGetPlatformDisplayEXT: OpenGL.platform.baseplatform.eglGetPlatformDisplayEXT  # value = <OpenGL.platform.baseplatform.eglGetPlatformDisplayEXT object>
eglGetProcAddress: OpenGL.platform.baseplatform.eglGetProcAddress  # value = <OpenGL.platform.baseplatform.eglGetProcAddress object>
eglGetSyncAttrib: OpenGL.platform.baseplatform.eglGetSyncAttrib  # value = <OpenGL.platform.baseplatform.eglGetSyncAttrib object>
eglInitialize: OpenGL.platform.baseplatform.eglInitialize  # value = <OpenGL.platform.baseplatform.eglInitialize object>
eglMakeCurrent: OpenGL.platform.baseplatform.eglMakeCurrent  # value = <OpenGL.platform.baseplatform.eglMakeCurrent object>
eglQueryAPI: OpenGL.platform.baseplatform.eglQueryAPI  # value = <OpenGL.platform.baseplatform.eglQueryAPI object>
eglQueryContext: OpenGL.platform.baseplatform.eglQueryContext  # value = <OpenGL.platform.baseplatform.eglQueryContext object>
eglQueryString: OpenGL.platform.baseplatform.eglQueryString  # value = <OpenGL.platform.baseplatform.eglQueryString object>
eglQuerySurface: OpenGL.platform.baseplatform.eglQuerySurface  # value = <OpenGL.platform.baseplatform.eglQuerySurface object>
eglReleaseTexImage: OpenGL.platform.baseplatform.eglReleaseTexImage  # value = <OpenGL.platform.baseplatform.eglReleaseTexImage object>
eglReleaseThread: OpenGL.platform.baseplatform.eglReleaseThread  # value = <OpenGL.platform.baseplatform.eglReleaseThread object>
eglSurfaceAttrib: OpenGL.platform.baseplatform.eglSurfaceAttrib  # value = <OpenGL.platform.baseplatform.eglSurfaceAttrib object>
eglSwapBuffers: OpenGL.platform.baseplatform.eglSwapBuffers  # value = <OpenGL.platform.baseplatform.eglSwapBuffers object>
eglSwapInterval: OpenGL.platform.baseplatform.eglSwapInterval  # value = <OpenGL.platform.baseplatform.eglSwapInterval object>
eglTerminate: OpenGL.platform.baseplatform.eglTerminate  # value = <OpenGL.platform.baseplatform.eglTerminate object>
eglWaitClient: OpenGL.platform.baseplatform.eglWaitClient  # value = <OpenGL.platform.baseplatform.eglWaitClient object>
eglWaitGL: OpenGL.platform.baseplatform.eglWaitGL  # value = <OpenGL.platform.baseplatform.eglWaitGL object>
eglWaitNative: OpenGL.platform.baseplatform.eglWaitNative  # value = <OpenGL.platform.baseplatform.eglWaitNative object>
eglWaitSync: OpenGL.platform.baseplatform.eglWaitSync  # value = <OpenGL.platform.baseplatform.eglWaitSync object>
raw_eglQueryString: _ctypes.CFuncPtr  # value = <_FuncPtr object>
