param(
    [string]$RimWorldDir = $(if ($env:RIMWORLD_DIR) { $env:RIMWORLD_DIR } else { "C:\Program Files (x86)\Steam\steamapps\common\RimWorld" })
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SourceMod = Join-Path $RepoRoot "mod"
$ModsDir = Join-Path $RimWorldDir "Mods"
$DestMod = Join-Path $ModsDir "RimFridgeWallAccessFix"

if (-not (Test-Path -LiteralPath $SourceMod)) {
    throw "Source mod folder not found: $SourceMod"
}

if (-not (Test-Path -LiteralPath $ModsDir)) {
    throw "RimWorld Mods folder not found: $ModsDir"
}

$resolvedMods = (Resolve-Path -LiteralPath $ModsDir).Path
$destParent = Split-Path -Parent $DestMod
if ((Resolve-Path -LiteralPath $destParent).Path -ne $resolvedMods) {
    throw "Refusing to install outside RimWorld Mods folder: $DestMod"
}

$publishedFileId = Join-Path $DestMod "About\PublishedFileId.txt"
$tempPublished = Join-Path $env:TEMP "RimFridgeWallAccessFix.PublishedFileId.txt"
$hadPublishedFileId = Test-Path -LiteralPath $publishedFileId
if ($hadPublishedFileId) {
    Copy-Item -LiteralPath $publishedFileId -Destination $tempPublished -Force
}

if (Test-Path -LiteralPath $DestMod) {
    Remove-Item -LiteralPath $DestMod -Recurse -Force
}

Copy-Item -LiteralPath $SourceMod -Destination $DestMod -Recurse -Force

if ($hadPublishedFileId) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $publishedFileId) | Out-Null
    Copy-Item -LiteralPath $tempPublished -Destination $publishedFileId -Force
}

Write-Host "[install] Wrote $DestMod"
