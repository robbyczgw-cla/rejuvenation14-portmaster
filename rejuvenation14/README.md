# Rejuvenation V14 for ROCKNIX / PortMaster

Runs Rejuvenation V14 on aarch64 handhelds with the engine the game ships with:
the enumag fork of mkxp-z (`2.4.2/afce4ce`), built for aarch64. Tested on an
AYN Odin 2 (SM8550) with ROCKNIX 20260901.

The port contains no game files. Rejuvenation is free, and its developers
distribute it on their own site.

## Install

1. Download V14 from https://www.rebornevo.com/rejuvdown/. The Linux zip is the
   easiest to use. The Windows zip also works.
2. Copy everything from the zip (`Audio`, `Data`, `Fonts`, `Graphics`,
   `Scripts`, `Game.ini`, `mkxp.json`, `stdlib`, `gems`, ...) into
   `ports/rejuvenation14/game/`.
3. Start "Rejuvenation V14" from the Ports menu.

The first start takes about 20 seconds before the title screen shows.

## Updates

The in-game updater works. When the main menu shows "Update available", select
it. The game downloads the patch, writes it into `game/`, and exits. Start it
again. The port's own files sit outside `game/`, so updates never touch them.

A new full release (V15, for example) goes into `game/` the same way as the
first install. Saves stay where they are.

## Saves

`ports/rejuvenation14/userdata/`, in the subfolder the game creates there
(named after the game's window title).

`Game.rxdata` is save slot 1, `Game_2.rxdata` slot 2, and so on. `Settings.dat`
holds the options. Copy this folder to back up your progress.

Saves from the PC version (`Saved Games/Rejuv/` on Windows, the game's
folder under `~/.local/share/` on Linux) can be copied into that subfolder.

## Controls

Native gamepad input through SDL, no keyboard emulation. All connected pads
work at the same time; the one you touched last is the active one.

This is the game's own gamepad layout (Menu > Controls > View Gamepad
Defaults). Face buttons are listed by position, because the Odin, Xbox and
PlayStation pads label them differently.

| Button | Game |
|---|---|
| Bottom face button | Confirm, talk |
| Right face button | Cancel, open menu. Hold to skip text |
| Left face button | Registered item. Hold for the text log. Battle log in battle |
| Top face button | Mega, sort, misc |
| Start | Run toggle. Hold for smart travel. In battle: move details |
| Select | Speed-up toggle |
| L1 / R1 | Previous / next page. In battle: inspect self / foe |
| L2 (analog) | Speed-up while held, stronger the further you press |
| R2 (analog) | Run while held. R2 + L1/R1 skips 10 pages |
| L3 | Mute |
| R3 | Quick save |
| D-pad / left stick | Move |

Menu > Controls > Configure opens the key binding screen, which works with
the pad, so you can rebind buttons on the device. The in-game help lists
Guide as soft reset; the port turns that off.

Name entry uses the on-screen letter grid. You can switch to keyboard entry in
Options > Use Keyboard if a keyboard is attached.

To quit, use Menu > Quit Game. The game then asks whether to save; pick
"Don't Save" to leave your save file as it is.

## Known issues

- The Save Directory button in the main menu does nothing. It calls `xdg-open`,
  which ROCKNIX does not have. The save path is listed above.
- Discord activity is off. The game's Discord module exists only for x86_64.
- The game uses the system time for day and night. Set the time zone in the
  ROCKNIX settings.

## Files

- `game/` holds the game data (yours).
- `runtime/` holds mkxp-z and its libraries. `runtime/BUILD.md` documents how it was built.
- `compat/` holds the port's Ruby fixes, loaded before the game scripts. `PATCHES.md` lists them.
- `mkxp.json.in` is the engine config. The launcher writes `mkxp.json` from it on every start.
- `userdata/` holds saves and settings.
- `log.txt` holds the output of the last run.

## Credits

Rejuvenation by the Rejuvenation team (rebornevo.com).
mkxp-z by Roza and contributors, fork by enumag (Jáchym Toušek).
The first Rejuvenation port for PortMaster (V13.5) is by JanTrueno.
