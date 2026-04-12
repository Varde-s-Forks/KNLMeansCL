# KNLMeansCL

**KNLMeansCL** is an optimized OpenCL implementation of the Non-local means de-noising algorithm.

The NLMeans filter, originally proposed by Buades et al., is a very popular filter for the removal of white Gaussian noise, due to its simplicity and excellent performance.
The strength of this algorithm is to exploit the repetitive character of the image in order to de-noise the image unlike conventional de-noising algorithms,
which typically operate in a local neighbourhood.

## Installation

Pre-compiled wheels are available on PyPI for:

- **Windows**: x86_64
- **Linux**: x86_64 and aarch64
- **macOS**: x86_64 and arm64 (15.0+)

```bash
pip install vapoursynth-knlmeanscl
```

## Documentation

Detailed documentation and usage examples are available on the upstream **[Wiki](https://github.com/Khanattila/KNLMeansCL/wiki)**.

## Compilation

To compile **KNLMeansCL**, you will need:

- **[uv](https://github.com/astral-sh/uv)**
- **C++14 Compiler**
- **OpenCL SDK**
- **Boost**

### Windows

The easiest way to compile on Windows is using **[vcpkg](https://github.com/microsoft/vcpkg)** for dependencies:

1.  **Install dependencies**:
    ```powershell
    vcpkg install --triplet x64-windows-static boost-filesystem boost-system opencl pkgconf
    ```
2.  **Build**:
    ```powershell
    # Replace path/to/vcpkg_installed with your actual installation path
    $vcpkgRoot = "path/to/vcpkg_installed/x64-windows-static"
    $env:LIB = "$vcpkgRoot/lib;$env:LIB"
    $env:INCLUDE = "$vcpkgRoot/include;$env:INCLUDE"
    $env:PKG_CONFIG_PATH = "$vcpkgRoot/lib/pkgconfig"
    $env:BOOST_ROOT = "$vcpkgRoot"
    $env:MESON_ARGS = "-Db_vscrt=mt -Denable_avs=false -Dstatic=true"
    uv build --wheel
    ```

### Linux

Install development packages via your package manager:

- **Ubuntu/Debian**: `apt install ocl-icd-opencl-dev libboost-system-dev libboost-filesystem-dev pkg-config`
- **Fedora/RHEL**: `dnf install ocl-icd-devel boost-devel pkgconf-pkg-config`

Then build:

```bash
export MESON_ARGS="-Denable_avs=false -Dstatic=true"
uv build --wheel
```

### macOS

Using **vcpkg**:

1.  **Install dependencies**:
    ```bash
    vcpkg install --triplet arm64-osx boost-filesystem boost-system opencl pkgconf
    ```
2.  **Build**:
    ```bash
    export MESON_ARGS="-Denable_avs=false -Dstatic=true"
    export PKG_CONFIG_PATH="path/to/vcpkg_installed/arm64-osx/lib/pkgconfig"
    export BOOST_ROOT="path/to/vcpkg_installed/arm64-osx"
    uv build --wheel
    ```

The resulting wheel will be located in the `dist/` directory.
