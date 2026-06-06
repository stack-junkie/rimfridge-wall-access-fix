from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_PATH = ROOT / "src" / "version.py"
SEMVER = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<pre>[0-9A-Za-z]+(?:\.[0-9A-Za-z]+)*))?$"
)


def read_version() -> str:
    content = VERSION_PATH.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise SystemExit("Could not find __version__ in src/version.py")
    return match.group(1)


def validate(version: str) -> re.Match[str]:
    match = SEMVER.match(version)
    if not match:
        raise SystemExit(f"Invalid semantic version: {version}")
    return match


def write_version(version: str) -> None:
    validate(version)
    content = VERSION_PATH.read_text(encoding="utf-8")
    content = re.sub(r'__version__\s*=\s*["\'][^"\']+["\']', f'__version__ = "{version}"', content)
    VERSION_PATH.write_text(content, encoding="utf-8", newline="\n")


def bump_alpha(current: str) -> str:
    match = validate(current)
    base = f"{match.group('major')}.{match.group('minor')}.{match.group('patch')}"
    pre = match.group("pre")
    if pre and pre.startswith("alpha."):
        parts = pre.split(".")
        if len(parts) == 2 and parts[1].isdigit():
            return f"{base}-alpha.{int(parts[1]) + 1}"
    return f"{base}-alpha.0"


def bump_stable(current: str, kind: str) -> str:
    match = validate(current)
    major = int(match.group("major"))
    minor = int(match.group("minor"))
    patch = int(match.group("patch"))
    if kind == "major":
        return f"{major + 1}.0.0"
    if kind == "minor":
        return f"{major}.{minor + 1}.0"
    if kind == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise SystemExit(f"Unsupported bump kind: {kind}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump semantic version from src/version.py")
    parser.add_argument("kind", choices=["alpha", "patch", "minor", "major", "set"])
    parser.add_argument("version", nargs="?", help="Explicit version for 'set'")
    args = parser.parse_args()

    current = read_version()
    if args.kind == "set":
        if not args.version:
            raise SystemExit("Usage: scripts\\run_python.cmd scripts\\bump_version.py set 0.1.0-alpha.1")
        next_version = args.version
        validate(next_version)
    elif args.kind == "alpha":
        next_version = bump_alpha(current)
    else:
        next_version = bump_stable(current, args.kind)

    write_version(next_version)
    print(f"[bump] {current} -> {next_version}")
    subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_version.py")], check=True)
    print("\nNext: add a matching CHANGELOG.md entry before committing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
