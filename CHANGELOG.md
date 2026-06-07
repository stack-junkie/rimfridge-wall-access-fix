# Changelog

This changelog tracks ckvam's compatibility patch, not upstream RimFridge history.

## [0.1.0-alpha.3] - 2026-06-07

- Added 1280x720 Workshop-ready image exports with black-bar padding while preserving source aspect ratios.
- Added the selected hero image to `mod/About/Preview.png` and a JPG fallback.
- Added a Workshop image manifest and synced the Workshop page field version through `scripts/sync_version.py`.

## [0.1.0-alpha.2] - 2026-06-07

- Added copy-ready Steam Workshop page fields, required-item guidance, initial change note, and image recommendations.
- Linked the Workshop upload checklist to the new page-field handoff.

## [0.1.0-alpha.1] - 2026-06-06

- Made the DLL build deterministic so pre-push validation does not leave a dirty compiled assembly.
- Rebuilt `RimFridgeWallAccessFix.dll` with the deterministic compiler setting.

## [0.1.0-alpha.0] - 2026-06-06

- Created `RimFridge Wall Access Fix` as a separate RimWorld 1.6 compatibility mod.
- Fixed wall-fridge stored-item pathing by converting `OnCell` access attempts to adjacent `Touch` access for items inside impassable RimFridge wall buildings.
- Kept humanlike corpse storage available in RimFridge wall fridges.
- Added an `ExtractSkull` reachability guard for humanlike corpses stored in wall fridges.
- Added defensive RimFridge temperature and heat-transfer guards for missing or stale room data.
- Added repo governance, version sync, release metadata checks, build/install scripts, and publish documentation.
