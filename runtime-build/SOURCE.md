# Source code for the bundled runtime

The release zip ships a compiled mkxp-z together with libraries under GPL,
LGPL and permissive licenses. mkxp-z's source is GPL-2.0-or-later; this build
links OpenSSL (Apache-2.0) for HTTPS, so the binary is distributed under
GPL-3.0, as described in mkxp-z's README. This file points to the
exact source of everything in `rejuvenation14/runtime/`.

## mkxp-z

- Upstream fork: https://github.com/enumag/mkxp-z at commit
  `afce4ce68404fb19383e00fe415b86dcc3aa214c`
- Changes on top: the two files in `patches/` (controller handling), applied
  by `build/build.sh`
- Build adaptations: `build/patch-build.py` (aarch64 build of the fork's
  Linux Makefile), documented in `BUILD.md`

## Dependencies

Every dependency is built from source at a pinned commit. `build/source-locks.json`
is the machine-readable list; `build/prefetch-locked.py` checks these commits out
before the build.

| Path in the build tree | Source | Commit |
|---|---|---|
| `.` | https://github.com/enumag/mkxp-z.git | `afce4ce68404` |
| `linux/downloads/aarch64/dbus` | https://gitlab.freedesktop.org/dbus/dbus | `958bf9db2100` |
| `linux/downloads/aarch64/fluidsynth` | https://github.com/FluidSynth/fluidsynth | `df432e151dca` |
| `linux/downloads/aarch64/fluidsynth/gcem` | https://github.com/kthohr/gcem.git | `012ae73c6d0a` |
| `linux/downloads/aarch64/fluidsynth/test/manual` | https://github.com/FluidSynth/testdata.git | `01d05b750667` |
| `linux/downloads/aarch64/fluidsynth/test/manual/SoundFont-Spec-Test` | https://github.com/mrbumpy409/SoundFont-Spec-Test | `0af09848d4d4` |
| `linux/downloads/aarch64/fluidsynth/test/manual/sf2/ANMP-data` | https://github.com/derselbst/ANMP-data | `28c09fec0f7a` |
| `linux/downloads/aarch64/fluidsynth/test/manual/sf2/GeneralUser-GS` | https://github.com/mrbumpy409/GeneralUser-GS | `d0fc360abafa` |
| `linux/downloads/aarch64/freetype` | https://github.com/mkxp-z/freetype2 | `4d8db130ea43` |
| `linux/downloads/aarch64/freetype/subprojects/dlg` | https://github.com/nyorain/dlg.git | `d142e646e263` |
| `linux/downloads/aarch64/libpng` | https://github.com/pnggroup/libpng | `2b978915d823` |
| `linux/downloads/aarch64/ogg` | https://github.com/xiph/ogg | `be05b13e98b0` |
| `linux/downloads/aarch64/openal` | https://github.com/kcat/openal-soft | `dc7d7054a5b4` |
| `linux/downloads/aarch64/openssl` | https://github.com/openssl/openssl | `c3cc0f1386b0` |
| `linux/downloads/aarch64/physfs` | https://github.com/icculus/physfs | `eb3383b532c5` |
| `linux/downloads/aarch64/pixman` | https://gitlab.freedesktop.org/pixman/pixman | `37216a32839f` |
| `linux/downloads/aarch64/ruby` | https://github.com/mkxp-z/ruby | `4d85560cf659` |
| `linux/downloads/aarch64/sdl2` | https://github.com/mkxp-z/SDL | `d3ac4c3742a4` |
| `linux/downloads/aarch64/sdl2_image` | https://github.com/mkxp-z/SDL_image | `d3c6d5963dbe` |
| `linux/downloads/aarch64/sdl2_image/external/dav1d` | https://github.com/libsdl-org/dav1d.git | `52d0c1f44eff` |
| `linux/downloads/aarch64/sdl2_image/external/jpeg` | https://github.com/libsdl-org/jpeg.git | `779556c0121c` |
| `linux/downloads/aarch64/sdl2_image/external/libavif` | https://github.com/libsdl-org/libavif.git | `a3e9315474de` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl` | https://github.com/libsdl-org/libjxl.git | `059943974d5a` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl/third_party/brotli` | https://github.com/libsdl-org/brotli.git | `2ae7ff838d1a` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl/third_party/brotli/research/esaxx` | https://github.com/hillbig/esaxx | `ca7cb332011e` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl/third_party/brotli/research/libdivsufsort` | https://github.com/y-256/libdivsufsort.git | `5f60d6f026c3` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl/third_party/googletest` | https://github.com/google/googletest | `0ea2d8f8fa16` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl/third_party/highway` | https://github.com/libsdl-org/highway.git | `a2104044ca07` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl/third_party/lcms` | https://github.com/mm2/Little-CMS | `65c63bf549d7` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl/third_party/lodepng` | https://github.com/lvandeve/lodepng | `48e5364ef48e` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl/third_party/sjpeg` | https://github.com/webmproject/sjpeg.git | `868ab558fad7` |
| `linux/downloads/aarch64/sdl2_image/external/libjxl/third_party/skcms` | https://skia.googlesource.com/skcms | `64374756e037` |
| `linux/downloads/aarch64/sdl2_image/external/libpng` | https://github.com/libsdl-org/libpng.git | `999173059e26` |
| `linux/downloads/aarch64/sdl2_image/external/libtiff` | https://github.com/libsdl-org/libtiff.git | `17461f1659d6` |
| `linux/downloads/aarch64/sdl2_image/external/libwebp` | https://github.com/libsdl-org/libwebp.git | `3bd82ea47820` |
| `linux/downloads/aarch64/sdl2_image/external/zlib` | https://github.com/libsdl-org/zlib.git | `f040d0cf7a55` |
| `linux/downloads/aarch64/sdl2_ttf` | https://github.com/mkxp-z/sdl_ttf | `0d5909ee2f1c` |
| `linux/downloads/aarch64/sdl_sound` | https://github.com/mkxp-z/SDL_sound | `cfb2533eb3ba` |
| `linux/downloads/aarch64/theora` | https://github.com/xiph/theora | `28fd5ec77f0a` |
| `linux/downloads/aarch64/uchardet` | https://gitlab.freedesktop.org/uchardet/uchardet | `ae6302a01608` |
| `linux/downloads/aarch64/vorbis` | https://github.com/xiph/vorbis | `0657aee69dec` |

## Libraries taken from Ubuntu 22.04 (arm64)

`rejuvenation14/runtime/lib/` also contains libraries copied from the Ubuntu
22.04 arm64 build container, not built from source. Their source is the Ubuntu
source package of the listed version (`apt-get source <source package>=<version>`
on Ubuntu 22.04, or https://launchpad.net/ubuntu/+source/<source package>).
`libruby.so.3.1` is built from the pinned `mkxp-z/ruby` source above.

| Library | Binary package | Source package | Version |
|---|---|---|---|
| `libapparmor.so.1` | `libapparmor1` | `apparmor` | `3.0.4-2ubuntu2.5` |
| `libFLAC.so.8` | `libflac8` | `flac` | `1.3.3-2ubuntu0.2` |
| `libgomp.so.1` | `libgomp1` | `gcc-12` | `12.3.0-1ubuntu1~22.04.3` |
| `libasyncns.so.0` | `libasyncns0` | `libasyncns` | `0.8-6build2` |
| `libbsd.so.0` | `libbsd0` | `libbsd` | `0.11.5-1` |
| `libcap.so.2` | `libcap2` | `libcap2` | `1:2.44-1ubuntu0.22.04.3` |
| `libffi.so.8` | `libffi8` | `libffi` | `3.4.2-4` |
| `libgcrypt.so.20` | `libgcrypt20` | `libgcrypt20` | `1.9.4-3ubuntu3.3` |
| `libgpg-error.so.0` | `libgpg-error0` | `libgpg-error` | `1.43-3` |
| `libmd.so.0` | `libmd0` | `libmd` | `1.0.4-1build1` |
| `libogg.so.0` | `libogg0` | `libogg` | `1.3.5-0ubuntu3` |
| `libsndfile.so.1` | `libsndfile1` | `libsndfile` | `1.0.31-2ubuntu0.2` |
| `libvorbis.so.0` | `libvorbis0a` | `libvorbis` | `1.3.7-1build2` |
| `libvorbisenc.so.2` | `libvorbisenc2` | `libvorbis` | `1.3.7-1build2` |
| `libX11-xcb.so.1` | `libx11-xcb1` | `libx11` | `2:1.7.5-1ubuntu0.3` |
| `libX11.so.6` | `libx11-6` | `libx11` | `2:1.7.5-1ubuntu0.3` |
| `libXau.so.6` | `libxau6` | `libxau` | `1:1.0.9-1build5` |
| `libxcb.so.1` | `libxcb1` | `libxcb` | `1.14-3ubuntu3` |
| `libcrypt.so.1` | `libcrypt1` | `libxcrypt` | `1:4.4.27-1` |
| `libXdmcp.so.6` | `libxdmcp6` | `libxdmcp` | `1:1.1.3-0ubuntu5` |
| `libyaml-0.so.2` | `libyaml-0-2` | `libyaml` | `0.2.2-1build2` |
| `libzstd.so.1` | `libzstd1` | `libzstd` | `1.4.8+dfsg-3build1` |
| `liblz4.so.1` | `liblz4-1` | `lz4` | `1.9.3-2build2` |
| `libopus.so.0` | `libopus0` | `opus` | `1.3.1-0.1build2` |
| `libsystemd.so.0` | `libsystemd0` | `systemd` | `249.11-0ubuntu3.22` |
| `liblzma.so.5` | `liblzma5` | `xz-utils` | `5.2.5-2ubuntu1.1` |
| `libz.so.1` | `zlib1g` | `zlib` | `1:1.2.11.dfsg-2ubuntu9.2` |

The license texts of all components are in `rejuvenation14/runtime/licenses/`
inside the release zip. `cacert.pem` is Ubuntu 22.04's `ca-certificates`
bundle (Mozilla CA list, MPL-2.0).

## Written offer

For three years after each release, the complete source archives used for that
release are available on request. Open an issue in this repository and they
will be provided at no charge beyond the cost of the transfer.
