project(
  'KNLMeansCL',
  'cpp',
  default_options: ['cpp_std=c++14', 'buildtype=release'],
  license: 'GPL-3',
  version: '1.1.1',
)

enable_vs = get_option('enable_vs')
enable_avs = get_option('enable_avs')

if not enable_vs and not enable_avs
  error('At least one of enable_vs or enable_avs must be true.')
endif

is_static = get_option('static')

opencl_dep = dependency('OpenCL', required: false)
if not opencl_dep.found()
  opencl_dep = meson.get_compiler('cpp').find_library('OpenCL')
endif
boost_dep = dependency('boost', modules: ['filesystem', 'system'], static: is_static)

link_args = []
if is_static and host_machine.system() == 'linux'
  link_args += ['-static-libgcc', '-static-libstdc++']
endif

common_deps = [opencl_dep, boost_dep]
if host_machine.system() == 'windows'
  cpp = meson.get_compiler('cpp')
  common_deps += cpp.find_library('cfgmgr32')
  common_deps += cpp.find_library('runtimeobject', required: false)
endif

# Shared sources (kernel + utilities) used by both plugins
shared_src = [
  'KNLMeansCL/NLMDefault.h',
  'KNLMeansCL/NLMKernel.cpp',
  'KNLMeansCL/NLMKernel.h',
  'KNLMeansCL/shared/common.cpp',
  'KNLMeansCL/shared/common.h',
  'KNLMeansCL/shared/ocl_utils.cpp',
  'KNLMeansCL/shared/ocl_utils.h',
  'KNLMeansCL/shared/startchar.cpp',
  'KNLMeansCL/shared/startchar.h',
]

lib_src = shared_src
lib_inc = []

if enable_vs
  py = import('python').find_installation(pure: false)

  r = run_command(
    py,
    '-c', 'import vapoursynth as vs; print(vs.get_include())',
    check: true,
  )
  lib_inc += include_directories(r.stdout().strip())
  lib_src += ['KNLMeansCL/NLMVapoursynth.cpp', 'KNLMeansCL/NLMVapoursynth.h']
endif

if enable_avs
  lib_inc += include_directories('KNLMeansCL/avisynth')
  lib_src += ['KNLMeansCL/NLMAvisynth.cpp', 'KNLMeansCL/NLMAvisynth.h']
endif

library(
  'KNLMeansCL',
  lib_src,
  include_directories: lib_inc,
  dependencies: common_deps,
  link_args: link_args,
  install: false,
)