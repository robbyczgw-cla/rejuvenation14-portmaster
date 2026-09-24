# Port patches

The game folder stays as downloaded. All changes live in `compat/` and in
`mkxp.json.in`. mkxp-z runs the files in `compat/preload/` before
`Data/Scripts.rxdata`, so each fix is in place before the game scripts load.

## compat/preload/rocknix_compat.rb

1. **Discord stub.** `Scripts/DiscordRichPresence.rb` runs `require 'discord'`,
   which finds `gems/discord.so`, an x86_64 library. The `LoadError` is a
   `ScriptError`, which the loader's bare `rescue` does not catch, so the
   script-loading thread dies. The preload puts `compat/rubylib/` first in `$:`.
   Ruby prefers `.rb` over `.so`, so `compat/rubylib/discord.rb` (a no-op
   module) loads instead.
2. **Fullscreen lock.** V14's Screen Size option (`SpriteResizer.rb`,
   `pbSetResizeFactor`) switches to a window and sets a window scale. On a
   handheld that fights the compositor and menus get drawn twice.
   `Graphics.fullscreen=` always sets fullscreen, `Graphics.scale=` and
   `Graphics.center` do nothing.
3. **Text entry default.** New settings get "Use Keyboard: Off", so name
   entry uses the letter grid, which works with a gamepad. Existing
   `Settings.dat` files keep their value, since loading them skips
   `initialize`.

## Developer preload

With `PORT_DEBUG=1`, the launcher also loads `compat/preload/rocknix_debug.rb`
if that file exists. The release does not contain it; it lives in the
development repository and dumps game state and runs test scripts.

## mkxp.json.in

Same game settings as V14's own `mkxp.json`, plus:

- `gameFolder`, `rubyLoadpath`, `preloadScript` with the port paths.
- `fullscreen`, `fixedAspectRatio`, `smoothScaling: 1` (512x384 to the panel, 4:3).
- `subImageFix: true`. 21 V14 tilesets are taller than 16384 px, the texture
  limit of the Adreno 740 under zink. This is the tested upload path for them.
- `enableReset: false`. Guide/Home would soft-reset the game.
- `midiSoundFont` points to ROCKNIX's `/usr/share/soundfonts/GeneralUser.sf2`.
  The healing jingle is a MIDI file.

## Launcher

- Builds `gamecontrollerdb.txt` from PortMaster's database plus the mappings
  EmulationStation generates. On ROCKNIX, InputPlumber grabs the built-in
  Odin 2 pad and presents it as a virtual DualSense, which SDL knows. The
  merged file covers setups where the raw "AYN Odin2 Gamepad" is visible.
- Saves go to `userdata/` through `XDG_DATA_HOME`.

## Runtime

See `runtime/BUILD.md`. Platform libraries (Wayland, xkbcommon, libdecor,
udev, dbus, PulseAudio, ALSA) come from the system. Bundled copies from the
build container broke Mesa's EGL.
