# Building the aarch64 runtime

The runtime in `rejuvenation14/runtime/` is enumag/mkxp-z at commit
`afce4ce68404fb19383e00fe415b86dcc3aa214c` (the engine Rejuvenation V14 ships
with, version string `2.4.2/afce4ce`), built natively for aarch64 Linux with
the fork's own Linux build (`linux/Makefile`, then Meson and Ninja).

## Requirements

- An arm64 machine with Docker. The scripts use the Docker context `colima`
  (Colima on an Apple Silicon Mac). On an arm64 Linux host, remove
  `--context colima` from `build/rebuild.sh`.
- The reference build ran in Colima with 6 CPUs and 8 GB RAM.

## Build

```sh
runtime-build/build/rebuild.sh
```

This builds the image from `build/Dockerfile` (Ubuntu 22.04 arm64, pinned by
digest; Meson 1.5.2, CMake 3.31.6), then runs `build/build.sh` in it:

1. Clone enumag/mkxp-z and check out `afce4ce`.
2. `build/prefetch-locked.py` checks out every dependency at the commit in
   `build/source-locks.json`.
3. `build/patch-build.py` adapts `linux/Makefile` for aarch64 (see "Differences from the fork's
   official Linux build").
4. Apply `patches/0001-open-all-gamecontrollers.patch` and
   `patches/0002-ignore-inactive-controller-axis-noise.patch`.
5. Build the dependencies and the engine (`-Dworkdir_current=true`).
6. `build/check-controllers.py` runs the controller event handling against SDL
   virtual joysticks.
7. `build/package.py` collects the engine, its libraries, Ruby's standard
   library with native extensions, `cacert.pem` and all license texts.

The output lands in `runtime-build/` and as `build/runtime-aarch64.tar.gz`,
which `tools/make-release.sh` puts into the release zip.

## Differences from the fork's official Linux build

- Native aarch64 instead of x86_64, and a plain folder instead of an AppImage.
- SDL is built with Wayland, joystick, game controller and HIDAPI support.
  X11 and KMSDRM are off, so the runtime needs a Wayland compositor (ROCKNIX
  runs Sway). OpenGL, EGL and Mesa come from the device.
- Ruby (`mkxp-z/ruby`, branch `mkxp-z-3.1.3`) is built with loadable native
  extensions, packaged as `stdlib-aarch64-linux/`.
- Every ELF gets a `$ORIGIN`-relative RUNPATH, so no `LD_LIBRARY_PATH` is needed.
- Wayland, xkbcommon, libdecor, udev, D-Bus, PulseAudio and ALSA are left to
  the system. Bundling Ubuntu's Wayland client broke Mesa's EGL on ROCKNIX.
- Discord support is not built (the game's Discord module is x86_64 only; the
  port replaces it with a stub).

## Controller patches

- `0001` opens every connected game controller instead of only device index 0,
  and makes the last used one the active controller.
- `0002` stops an idle controller's stick noise from overwriting the active
  controller's axes.

## Checking a build on the device

`tools/check-odin.sh` inside the runtime folder prints the host, the resolved
libraries (`ldd`), and runs Ruby checks for zlib, JSON, digest, libffi and
encodings:

```sh
sh rejuvenation14/runtime/tools/check-odin.sh
```

See `SOURCE.md` for the exact source of every bundled component.
