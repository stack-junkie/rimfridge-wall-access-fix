# Validation

Run from the repository root:

```powershell
scripts\run_python.cmd scripts\sync_version.py --check
scripts\build.cmd
```

For staged commits:

```powershell
scripts\run_python.cmd scripts\check_release_metadata.py --staged
```

For live game validation:

1. Run `scripts\install_local.cmd`.
2. Start RimWorld with Harmony, RimFridge, and this patch enabled.
3. Load a save with a corpse in a RimFridge wall fridge.
4. Confirm skull extraction reserves and completes.
5. Confirm the current `Player.log` has no repeated `Resolved path returned no nodes` errors for wall-fridge contents.
