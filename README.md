# Rejuvenation V14 for ROCKNIX / PortMaster

Plays Rejuvenation V14, a free fan game, on aarch64 Linux handhelds. It uses the engine
the game ships with on PC, the enumag fork of mkxp-z, built for aarch64.

Tested on an AYN Odin 2 with ROCKNIX 20260901 and Rejuvenation 14.0.24.

> **Beta.** Tested on one device so far (AYN Odin 2). Test reports from other
> ROCKNIX devices are welcome as issues.

## Disclaimer

This is an unofficial, non-commercial fan project. It is not affiliated with,
endorsed by, or sponsored by Nintendo, Game Freak, Creatures, The Pokémon
Company, or the Rejuvenation team. All trademarks belong to their respective
owners; game names appear here only to identify the game this port runs.

This repository contains no game data, no game code, no music and no game
artwork; the only image is the Rejuvenation window icon compiled into the
engine binary, taken from the public enumag/mkxp-z source. It holds a
launcher, configuration, small compatibility scripts written for this port,
and the build recipe for the open source mkxp-z engine. Players
download Rejuvenation from its developers and supply it themselves.

Rights holders: if you want anything in this repository changed or removed,
open an issue and it will be handled promptly.

## Install

1. Download `rejuvenation14.zip` from the releases and unzip it into your
   ports folder (`/roms/ports/` on ROCKNIX). You get
   `Rejuvenation V14.sh` and a `rejuvenation14/` folder.
2. Download V14 from https://www.rebornevo.com/rejuvdown/ (Linux or Windows).
3. Copy everything inside that zip into `rejuvenation14/game/`.
4. Refresh the game list, then start "Rejuvenation V14" from Ports.

The first start takes about 20 seconds.

## Tested on

| Device | Firmware | Game version | Status |
|---|---|---|---|
| AYN Odin 2 (SM8550) | ROCKNIX 20260901 | 14.0.24 | Works: intro, maps, battles, video, save/load, updater, gamepad |

## Requirements

- ROCKNIX with PortMaster on an aarch64 device that runs the Sway (Wayland)
  desktop. The runtime is built for Wayland only; ArkOS, muOS, Knulli and
  other KMSDRM or X11 systems will not start it.
- Desktop OpenGL through Mesa (zink or a native driver). Devices limited to
  OpenGL ES are not supported.
- RAM: the game peaked at about 400 MB on the Odin 2 (intro and first areas).
  Later areas may need more; devices with 1 GB total are untested.

## Playing

Saves and settings go to `rejuvenation14/userdata/`. The in-game
updater works and installs official patches into `game/`.

Controls follow the game's own gamepad layout. Menu > Controls > View
Gamepad Defaults shows it; `rejuvenation14/README.md` lists it too. Every
connected controller works.

Quit with Menu > Quit Game.

Details, known issues and all port changes: `rejuvenation14/README.md` and
`rejuvenation14/PATCHES.md`.

## Building the release zip

```sh
tools/make-release.sh runtime-aarch64.tar.gz v1.0.0
```

The runtime tarball comes from `runtime-build/` (enumag/mkxp-z `2.4.2/afce4ce`
plus two controller patches). `runtime-build/BUILD.md` explains the build.

## Licenses

The port's own files (launcher, `compat/`, config template, tools) are MIT
licensed, see `LICENSE`. The runtime is mkxp-z, whose source is
GPL-2.0-or-later; the binary links OpenSSL (Apache-2.0) for the in-game
updater, so as mkxp-z's own README states, the compiled runtime is under
GPL-3.0. The licenses of it and its dependencies are in `rejuvenation14/runtime/licenses/` in the
release zip, and `runtime-build/SOURCE.md` lists the exact source of every
bundled component. The engine binary carries the Rejuvenation window
icon from the enumag/mkxp-z repository. Rejuvenation belongs to its
developers; all other trademarks belong to their owners.

## Credits

- Rejuvenation: the Rejuvenation team (rebornevo.com)
- mkxp-z: Roza and contributors; fork by enumag (Jáchym Toušek)
- First Rejuvenation port for PortMaster (V13.5): JanTrueno
