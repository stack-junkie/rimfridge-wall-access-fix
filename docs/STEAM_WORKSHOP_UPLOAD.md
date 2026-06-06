# Steam Workshop Upload

Use this checklist when publishing or updating the patch mod.

1. Build the DLL:

   ```powershell
   scripts\build.cmd
   ```

2. Install locally and test in RimWorld:

   ```powershell
   scripts\install_local.cmd
   ```

3. Confirm the mod loads after Harmony and RimFridge.

4. Confirm `Player.log` includes:

   ```text
   [RimFridge Wall Access Fix] Loaded.
   ```

5. Do not copy another mod's `PublishedFileId.txt` into this repo.

6. Keep the Workshop description clear that this is a compatibility patch and still requires RimFridge.

Report template:

```text
RimWorld version:
Patch version:
RimFridge version:
Mod list:
Save/new colony:
Steps to reproduce:
Player.log excerpt:
```
