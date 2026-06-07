# Steam Workshop Page Fields

Use these fields for the `RimFridge Wall Access Fix` Workshop item.

## Upload Fields

- Title: `RimFridge Wall Access Fix`
- Visibility: `Public`
- Language: `English`
- Content folder: `C:\Program Files (x86)\Steam\steamapps\common\RimWorld\Mods\RimFridgeWallAccessFix`
- Primary preview image: `C:\Program Files (x86)\Steam\steamapps\common\RimWorld\Mods\RimFridgeWallAccessFix\About\Preview.png`
- Required items:
  - Harmony: `https://steamcommunity.com/sharedfiles/filedetails/?id=2009463077`
  - RimFridge: Now with Shelves!: `https://steamcommunity.com/sharedfiles/filedetails/?id=2898411376`
- Tags:
  - `Mod`
  - `1.6`

Steam's Workshop upload API updates title, description, visibility, tags, content, and the primary preview image as separate item fields. RimWorld `About.xml` dependencies are not enough by themselves for Workshop dependency prompts; add Harmony and RimFridge as Required Items on the Workshop page.

## Short Description

```text
Fixes RimFridge wall-fridge access/pathing loops while keeping humanlike corpse storage available.
```

## Description

```text
[h1]RimFridge Wall Access Fix[/h1]

Compatibility patch for [url=https://steamcommunity.com/sharedfiles/filedetails/?id=2898411376]RimFridge: Now with Shelves![/url].

[h2]What it fixes[/h2]
[list]
[*]Pawns trying to path onto impassable RimFridge wall-fridge cells to use stored items.
[*]Repeated "Resolved path returned no nodes" loops when jobs target wall-fridge contents.
[*]Skull extraction access for humanlike corpses stored in RimFridge wall fridges.
[*]Rare RimFridge temperature/heat null-reference cases when room data is missing or stale.
[/list]

[h2]What it does not change[/h2]
[list]
[*]Does not replace RimFridge.
[*]Does not add new fridges.
[*]Does not remove humanlike corpse storage from fridges.
[*]Does not change RimFridge storage filters except for fixing adjacent access/pathing behavior.
[/list]

[h2]Requirements[/h2]
[list]
[*][url=https://steamcommunity.com/sharedfiles/filedetails/?id=2009463077]Harmony[/url]
[*][url=https://steamcommunity.com/sharedfiles/filedetails/?id=2898411376]RimFridge: Now with Shelves![/url]
[/list]

[h2]Load order[/h2]
Load after Harmony and RimFridge.

[h2]Save compatibility[/h2]
Safe to add to an existing save.

Removal should be safe for saves, but any old wall-fridge pathing issue this patch fixed can return if the patch is removed while RimFridge remains active.

[h2]Tested[/h2]
Tested on RimWorld 1.6 with RimFridge wall fridges. Confirmed skull extraction from a humanlike corpse stored in a wall fridge completed successfully.

[h2]Version[/h2]
Patch version: 0.1.0-alpha.2

[h2]Source[/h2]
https://github.com/stack-junkie/rimfridge-wall-access-fix

[h2]Bug reports[/h2]
Please include:
[list]
[*]RimWorld version
[*]Patch version
[*]RimFridge version
[*]Mod list or Hugslib/RimPy export
[*]Steps to reproduce
[*]Player.log excerpt around the error
[/list]
```

## Initial Change Note

```text
Initial public Workshop release.

Fixes RimFridge wall-fridge pathing/access loops for stored items, including skull extraction from humanlike corpses stored in wall fridges. Keeps humanlike corpse storage available. Requires Harmony and RimFridge: Now with Shelves!
```

## Image Recommendations

Use real in-game screenshots as the main visual proof. Generated or abstract art would look less trustworthy for a compatibility patch.

### Primary Preview

- File: `mod\About\Preview.png`
- Format: PNG or JPG.
- Shape: 16:9 landscape.
- Working size: 1280x720, compressed small enough that Steam/RimWorld's uploader accepts it.
- Content: a clean RimWorld kitchen/dining-wall screenshot with a RimFridge wall fridge visible and a pawn standing beside it.
- Text overlay: `RimFridge Wall Access Fix` plus small `Requires RimFridge`.
- Avoid: gore-focused corpse imagery, crowded UI, red error spam, fake 3D renders, or art that hides what the mod actually touches.

### Extra Workshop Images

1. `Before / Problem`: a pawn/job targeting an item in a wall fridge, with a small caption like `Fixes wall-fridge access jobs`.
2. `After / Verified`: pawn adjacent to the wall fridge successfully using the stored item/corpse job.
3. `Dependencies`: a simple screenshot of the mod list order: Harmony, RimFridge, RimFridge Wall Access Fix.
4. `Scope`: a screenshot of wall fridges in a normal base layout with a caption: `No storage-filter removal; humanlike storage still allowed`.

Keep the first image clean and readable at thumbnail size. Put diagnostic details in secondary images or the description.

## Source Notes

- Steam Workshop uploads expose title, description, visibility, tags, content folder, and preview image as item fields: `https://partner.steamgames.com/doc/features/workshop/implementation?language=english`
- Steam preview images are set from an absolute local image path and suggested formats include JPG, PNG, and GIF: `https://partner.steamgames.com/doc/api/ISteamUGC?language=english`
- RimWorld `About.xml` dependencies warn in-game, but Workshop Required Items must be set separately: `https://rimworldwiki.com/wiki/Modding_Tutorials/About.xml`
