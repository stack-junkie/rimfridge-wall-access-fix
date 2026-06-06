# RimFridge Wall Access Fix v0.1.0-alpha.0

RimWorld 1.6 compatibility patch for `RimFridge: Now with Shelves!`.

- Version: `0.1.0-alpha.0`
- Package ID: `ckvam.rimfridge.wallaccessfix`
- Live install target: `C:\Program Files (x86)\Steam\steamapps\common\RimWorld\Mods\RimFridgeWallAccessFix`
- Source repo target: `C:\Users\ckvam\Documents\Development\02 Projects\RimWorld Mods\RimFridgeWallAccessFix`

## What It Fixes

- Pawns trying to path `OnCell` to items stored inside RimFridge wall fridges.
- `Resolved path returned no nodes` loops for wall-fridge contents, including skull extraction and recreation/drug/food items.
- Humanlike corpses remain allowed in wall fridges; this mod fixes access/pathing rather than storage filters.
- Defensive null guards for RimFridge temperature and heat transfer methods when room data is missing or stale.

## Build

```powershell
scripts\build.cmd
```

The build writes:

```text
mod\1.6\Assemblies\RimFridgeWallAccessFix.dll
```

## Install Locally

```powershell
scripts\install_local.cmd
```

This copies `mod\` into RimWorld's local `Mods` folder and preserves `About\PublishedFileId.txt` if it already exists.

## Release Guardrails

```powershell
scripts\run_python.cmd scripts\sync_version.py --check
scripts\run_python.cmd scripts\check_release_metadata.py --staged
```

Use `scripts\bump_version.py` for version bumps, then add the matching `CHANGELOG.md` entry before committing.
