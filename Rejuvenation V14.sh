#!/bin/bash
# Rejuvenation V14 for ROCKNIX / PortMaster (aarch64)
# Runtime: mkxp-z (enumag fork, the engine V14 ships with), built for aarch64.
# Game data: official V14 Linux or Windows download, unpacked into rejuvenation14/game/.

XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

if [ -d "/opt/system/Tools/PortMaster/" ]; then
  controlfolder="/opt/system/Tools/PortMaster"
elif [ -d "/opt/tools/PortMaster/" ]; then
  controlfolder="/opt/tools/PortMaster"
elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
  controlfolder="$XDG_DATA_HOME/PortMaster"
else
  controlfolder="/roms/ports/PortMaster"
fi

source "$controlfolder/control.txt"
[ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
get_controls

GAMEDIR="/$directory/ports/rejuvenation14"
LOG="$GAMEDIR/log.txt"
cd "$GAMEDIR"
: > "$LOG"
exec > >(tee -a "$LOG") 2>&1

if [ ! -f "$GAMEDIR/game/Data/Scripts.rxdata" ]; then
  echo "Game files missing. Copy the contents of the official V14 download into $GAMEDIR/game/"
  pm_message "Rejuvenation: copy the V14 game files into ports/rejuvenation14/game/" 2>/dev/null
  sleep 5
  pm_finish
  exit 1
fi

# Never run two instances: both would play audio, only one gets input.
if pidof mkxp-z.aarch64 >/dev/null; then
  echo "Already running (pid $(pidof mkxp-z.aarch64))."
  exit 1
fi

# Launched over SSH there is no session environment; ES provides these.
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/var/run/0-runtime-dir}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-1}"
export SDL_VIDEODRIVER="${SDL_VIDEODRIVER:-wayland}"
export SDL_AUDIODRIVER="${SDL_AUDIODRIVER:-pulseaudio}"
export ALSOFT_DRIVERS=pulse
export SDL_VIDEO_WAYLAND_ALLOW_LIBDECOR=0
export SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS=1
# get_controls only writes pads that ES has mappings for; the built-in
# "AYN Odin2 Gamepad" was missing there and mkxp-z's own DB lacks it too.
# PortMaster's full DB first, ES-generated mappings last: SDL lets a later
# line replace an earlier one for the same GUID, so ES mappings win.
PADDB="$GAMEDIR/gamecontrollerdb.txt"
cat "$controlfolder/gamecontrollerdb.txt" "${SDL_GAMECONTROLLERCONFIG_FILE:-/dev/null}" > "$PADDB" 2>/dev/null
export SDL_GAMECONTROLLERCONFIG_FILE="$PADDB"
unset SDL_GAMECONTROLLERCONFIG
export SSL_CERT_FILE="$GAMEDIR/runtime/cacert.pem"
# Ruby loads its encoding DB (enc/encdb.so) during VM init, before mkxp-z
# applies rubyLoadpath. Without this, openssl fails with
# "unknown encoding name: binary" and the in-game updater breaks.
export RUBYLIB="$GAMEDIR/runtime/stdlib:$GAMEDIR/runtime/stdlib-aarch64-linux"

# Saves and settings go to userdata/ (outside game/, survives updates).
export XDG_DATA_HOME="$GAMEDIR/userdata"
mkdir -p "$XDG_DATA_HOME"

# mkxp-z reads mkxp.json from the working directory. Render it for this location.
# PORT_DEBUG=1 adds a developer preload, if one was copied into compat/preload/.
DEBUG_PRELOAD=""
if [ "${PORT_DEBUG:-}" = "1" ] && [ -f compat/preload/rocknix_debug.rb ]; then
  DEBUG_PRELOAD=", \"$GAMEDIR/compat/preload/rocknix_debug.rb\""
fi
sed -e "s#@PORTDIR@#$GAMEDIR#g" -e "s#@DEBUG_PRELOAD@#$DEBUG_PRELOAD#" mkxp.json.in > mkxp.json

# Zip extraction (PortMaster uses Python's zipfile) drops the executable bit.
chmod +x "$GAMEDIR/runtime/mkxp-z.aarch64"
pm_platform_helper "$GAMEDIR/runtime/mkxp-z.aarch64" >/dev/null 2>&1
./runtime/mkxp-z.aarch64
echo "EXIT CODE: $?"

pm_finish
