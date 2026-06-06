# Repository Instructions

This repo is the source of truth for `RimFridge Wall Access Fix`.

## Layout

- `mod/` mirrors the installable RimWorld mod folder.
- `mod/1.6/Source/` contains patch source.
- `mod/1.6/Assemblies/` contains the DLL RimWorld loads.
- `scripts/` contains Windows-first maintenance commands.
- `docs/` contains publish and validation handoffs.

## Release Discipline

- Treat `src/version.py` as the version source.
- Run `scripts\run_python.cmd scripts\sync_version.py --check` before committing.
- Every material change must bump the semantic version and add a `CHANGELOG.md` entry.
- Keep the compiled DLL in git when source changes; RimWorld loads it directly.
- Do not commit `mod/About/PublishedFileId.txt`.

## RimWorld Safety

- Keep this as a separate compatibility mod. Do not replace RimFridge.
- Preserve package ID `ckvam.rimfridge.wallaccessfix`.
- Keep `loadAfter` entries for Harmony and RimFridge.
- Use `scripts\install_local.cmd` to deploy into the live RimWorld `Mods` folder.
- When investigating live behavior, verify `ModsConfig.xml` and current `Player.log` instead of relying on stale errors.
