# RimFridge Wall Access Fix

Local RimWorld 1.6 patch mod for `RimFridge: Now with Shelves!`.

- Patch version: `0.1.0-alpha.0`

## What it fixes

- Pawns trying to path `OnCell` to items stored inside RimFridge wall fridges.
- `Resolved path returned no nodes` loops for wall-fridge contents, including skull extraction and recreation/drug/food items.
- Humanlike corpses remain allowed in wall fridges; this mod fixes access/pathing rather than storage filters.
- Defensive null guards for RimFridge temperature and heat transfer methods when room data is missing or stale.

## Notes

This is a separate compatibility mod. It does not replace RimFridge and should load after Harmony and RimFridge.
