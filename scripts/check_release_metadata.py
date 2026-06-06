from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = "src/version.py"
CHANGELOG_FILE = "CHANGELOG.md"
MATERIAL_RE = re.compile(r"(\.cs|\.dll|\.xml|\.py|\.ps1|\.cmd|\.md|\.json|\.yml|\.yaml|\.txt)$", re.IGNORECASE)
RELEASE_ONLY = {"VERSION", VERSION_FILE, CHANGELOG_FILE}
SEMVER_RE = re.compile(r'__version__\s*=\s*["\']([^"\']+)["\']')


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def has_head() -> bool:
    result = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    return result.returncode == 0


def version_from_text(text: str) -> str | None:
    match = SEMVER_RE.search(text)
    return match.group(1) if match else None


def current_version() -> str:
    content = (ROOT / VERSION_FILE).read_text(encoding="utf-8")
    version = version_from_text(content)
    if not version:
        raise SystemExit("Could not read current version from src/version.py")
    return version


def version_at(ref: str) -> str | None:
    return version_from_text(git("show", f"{ref}:{VERSION_FILE}", check=False))


def is_material(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if normalized in RELEASE_ONLY:
        return False
    if normalized.startswith(".git/"):
        return False
    return bool(MATERIAL_RE.search(normalized))


def changelog_has(version: str, ref: str | None = None) -> bool:
    if ref:
        content = git("show", f"{ref}:{CHANGELOG_FILE}", check=False)
    else:
        content = (ROOT / CHANGELOG_FILE).read_text(encoding="utf-8")
    return f"## [{version}]" in content


def staged_files() -> list[str]:
    output = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    return [line.strip() for line in output.splitlines() if line.strip()]


def fail(message: str) -> int:
    print("")
    print("Release metadata check failed:")
    print(message)
    print("")
    print("Every material change needs a semantic version bump and CHANGELOG.md entry.")
    return 1


def check_staged() -> int:
    files = staged_files()
    material = [path for path in files if is_material(path)]
    if not material:
        print("  no material staged changes requiring release metadata")
        return 0

    missing = [path for path in [VERSION_FILE, CHANGELOG_FILE] if path not in files]
    if missing:
        return fail("Missing staged file(s): " + ", ".join(missing))

    new_version = current_version()
    if has_head():
        old_version = version_at("HEAD")
        if old_version == new_version:
            return fail(f"src/version.py is staged but version did not change from HEAD ({new_version}).")

    if not changelog_has(new_version):
        return fail(f"CHANGELOG.md does not contain a '## [{new_version}]' entry.")

    print(f"  release metadata present for v{new_version}")
    return 0


def commit_files(commit: str) -> list[str]:
    output = git("diff-tree", "--no-commit-id", "--name-only", "-r", "--root", commit)
    return [line.strip() for line in output.splitlines() if line.strip()]


def first_parent(commit: str) -> str | None:
    parents = git("rev-list", "--parents", "-n", "1", commit).split()
    return parents[1] if len(parents) > 1 else None


def check_commit(commit: str) -> int:
    files = commit_files(commit)
    material = [path for path in files if is_material(path)]
    if not material:
        return 0

    if VERSION_FILE not in files or CHANGELOG_FILE not in files:
        print(f"Commit {commit[:8]} has material changes but lacks {VERSION_FILE} and/or {CHANGELOG_FILE}.")
        return 1

    new_version = version_at(commit)
    if not new_version:
        print(f"Commit {commit[:8]} does not expose a readable version.")
        return 1

    parent = first_parent(commit)
    if parent:
        old_version = version_at(parent)
        if old_version == new_version:
            print(f"Commit {commit[:8]} did not bump version from parent ({new_version}).")
            return 1

    if not changelog_has(new_version, commit):
        print(f"Commit {commit[:8]} CHANGELOG.md lacks entry for {new_version}.")
        return 1

    return 0


def check_range(range_spec: str) -> int:
    commits = [line.strip() for line in git("rev-list", "--reverse", range_spec).splitlines() if line.strip()]
    failures = 0
    for commit in commits:
        failures += check_commit(commit)
    if failures:
        return fail(f"{failures} commit(s) failed release metadata checks.")
    print(f"  release metadata present for {len(commits)} commit(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Require version and changelog updates for material changes")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--staged", action="store_true")
    group.add_argument("--range", dest="range_spec")
    args = parser.parse_args()

    if args.staged:
        return check_staged()
    return check_range(args.range_spec)


if __name__ == "__main__":
    raise SystemExit(main())
