param(
    [string]$RimWorldDir = $(if ($env:RIMWORLD_DIR) { $env:RIMWORLD_DIR } else { "C:\Program Files (x86)\Steam\steamapps\common\RimWorld" }),
    [string]$CompilerPath = $env:CSC_EXE,
    [string]$HarmonyDll = $env:HARMONY_DLL
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SourceFile = Join-Path $RepoRoot "mod\1.6\Source\RimFridgeWallAccessFix.cs"
$OutputDll = Join-Path $RepoRoot "mod\1.6\Assemblies\RimFridgeWallAccessFix.dll"
$ManagedDir = Join-Path $RimWorldDir "RimWorldWin64_Data\Managed"

function Resolve-ExistingPath {
    param([string[]]$Candidates)

    foreach ($candidate in $Candidates) {
        if ($candidate -and (Test-Path -LiteralPath $candidate)) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }

    return $null
}

function Get-RoslynCompiler {
    param([string]$RequestedPath)

    $candidate = Resolve-ExistingPath @(
        $RequestedPath,
        (Join-Path $env:TEMP "codex-roslyn\toolset-4.8.0\tasks\net472\csc.exe")
    )

    if ($candidate) {
        return $candidate
    }

    $toolsetRoot = Join-Path $env:TEMP "codex-roslyn"
    $packagePath = Join-Path $toolsetRoot "Microsoft.Net.Compilers.Toolset.4.8.0.nupkg"
    $extractPath = Join-Path $toolsetRoot "toolset-4.8.0"
    New-Item -ItemType Directory -Force -Path $toolsetRoot | Out-Null

    if (-not (Test-Path -LiteralPath $packagePath)) {
        Invoke-WebRequest -Uri "https://www.nuget.org/api/v2/package/Microsoft.Net.Compilers.Toolset/4.8.0" -OutFile $packagePath
    }

    if (-not (Test-Path -LiteralPath $extractPath)) {
        Expand-Archive -LiteralPath $packagePath -DestinationPath $extractPath -Force
    }

    $downloaded = Join-Path $extractPath "tasks\net472\csc.exe"
    if (-not (Test-Path -LiteralPath $downloaded)) {
        throw "Could not find Roslyn compiler at $downloaded"
    }

    return $downloaded
}

if (-not (Test-Path -LiteralPath $SourceFile)) {
    throw "Source file not found: $SourceFile"
}

if (-not (Test-Path -LiteralPath $ManagedDir)) {
    throw "RimWorld managed directory not found: $ManagedDir"
}

$CompilerPath = Get-RoslynCompiler -RequestedPath $CompilerPath

if (-not $HarmonyDll) {
    $HarmonyDll = Resolve-ExistingPath @(
        (Join-Path $RimWorldDir "Mods\Harmony\Current\Assemblies\0Harmony.dll"),
        (Join-Path $RimWorldDir "Mods\Harmony\1.6\Assemblies\0Harmony.dll"),
        (Join-Path $RimWorldDir "Mods\Harmony\Assemblies\0Harmony.dll"),
        (Join-Path $RimWorldDir "..\..\workshop\content\294100\2009463077\Current\Assemblies\0Harmony.dll"),
        (Join-Path $RimWorldDir "..\..\workshop\content\294100\2009463077\1.6\Assemblies\0Harmony.dll"),
        (Join-Path $RimWorldDir "..\..\workshop\content\294100\2009463077\Assemblies\0Harmony.dll")
    )
}

if (-not $HarmonyDll -or -not (Test-Path -LiteralPath $HarmonyDll)) {
    throw "Could not find 0Harmony.dll. Set HARMONY_DLL to its full path."
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $OutputDll) | Out-Null

$references = @(
    (Join-Path $ManagedDir "Assembly-CSharp.dll"),
    (Join-Path $ManagedDir "UnityEngine.dll"),
    (Join-Path $ManagedDir "UnityEngine.CoreModule.dll"),
    (Join-Path $ManagedDir "netstandard.dll"),
    $HarmonyDll
)

foreach ($reference in $references) {
    if (-not (Test-Path -LiteralPath $reference)) {
        throw "Reference not found: $reference"
    }
}

$args = @(
    "/nologo",
    "/target:library",
    "/langversion:latest",
    "/deterministic+",
    "/out:$OutputDll"
)

foreach ($reference in $references) {
    $args += "/reference:$reference"
}

$args += $SourceFile

& $CompilerPath @args
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "[build] Wrote $OutputDll"
