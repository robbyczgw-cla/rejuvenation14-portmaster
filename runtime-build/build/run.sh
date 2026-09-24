#!/bin/sh
# Invoke from the game directory. Environment changes apply only to mkxp-z.
set -eu
runtime_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec env \
  LD_LIBRARY_PATH="$runtime_dir/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" \
  RUBYLIB="$runtime_dir/stdlib:$runtime_dir/stdlib/aarch64-linux${RUBYLIB:+:$RUBYLIB}" \
  SSL_CERT_FILE="$runtime_dir/cacert.pem" \
  SDL_VIDEODRIVER=wayland \
  SDL_AUDIODRIVER=pulseaudio \
  ALSOFT_DRIVERS=pulse \
  SDL_VIDEO_WAYLAND_ALLOW_LIBDECOR=0 \
  "$runtime_dir/mkxp-z.aarch64" "$@"
