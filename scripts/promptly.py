#!/usr/bin/env python3
"""Build/install Promptly's native files. Expansion is performed by the host model."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import stat
import sys

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = {
    "codex": Path("codex/promptly/SKILL.md"),
    "claude": Path("claude/promptly/SKILL.md"),
    "opencode": Path("opencode/promptly.md"),
    "generic": Path("generic/promptly/SKILL.md"),
}


def render(root: Path = ROOT) -> dict[Path, bytes]:
    core = (root / "core/prompt.md").read_text(encoding="utf-8").strip()
    digest = hashlib.sha256((core + "\n").encode("utf-8")).hexdigest()
    result = {}
    for harness, entry in ENTRYPOINTS.items():
        template = (root / f"adapters/{harness}.md").read_text(encoding="utf-8")
        if template.count("{{CORE}}") != 1 or template.count("{{CORE_SHA256}}") != 1:
            raise ValueError(f"Invalid adapter template: {harness}")
        result[entry] = template.replace("{{CORE_SHA256}}", digest).replace(
            "{{CORE}}", core
        ).encode("utf-8")
    result[Path("codex/promptly/agents/openai.yaml")] = (
        root / "adapters/openai.yaml"
    ).read_bytes()
    return result


def is_link(path: Path) -> bool:
    if path.is_symlink():
        return True
    # lstat's reparse-point flag also covers Windows junctions on Python 3.10/3.11.
    try:
        return bool(getattr(path.lstat(), "st_file_attributes", 0)
                    & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))
    except FileNotFoundError:
        return False


def check_path(path: Path) -> None:
    # Do not silently follow a skill symlink or Windows junction when replacing files.
    for part in (path, *path.parents):
        if is_link(part):
            raise ValueError(f"Refusing linked installation path: {part}")
        if part != path and part.exists() and not part.is_dir():
            raise ValueError(f"Parent is not a directory: {part}")


def build(root: Path = ROOT, check: bool = False) -> list[str]:
    stale = []
    for relative, content in render(root).items():
        path = root / "bundles" / relative
        check_path(path)
        if path.is_file() and path.read_bytes() == content:
            continue
        stale.append(relative.as_posix())
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    return stale


def destination(harness: str, scope: str, project: Path, home: Path,
                environ: dict[str, str]) -> Path:
    if scope == "project":
        base = project.absolute()
        return base / {
            "codex": ".agents/skills/promptly",
            "claude": ".claude/skills/promptly",
            "opencode": ".opencode/commands",
            "generic": ".agents/skills/promptly",
        }[harness]
    if harness in {"codex", "generic"}:
        return home / ".agents/skills/promptly"
    if harness == "claude":
        return home / ".claude/skills/promptly"
    config = Path(environ.get("XDG_CONFIG_HOME") or home / ".config")
    if not config.is_absolute():
        raise ValueError("XDG_CONFIG_HOME must be an absolute path")
    return config / "opencode/commands"


def install(harness: str, dest: Path, *, force: bool = False,
            dry_run: bool = False, root: Path = ROOT) -> list[Path]:
    # Render from canonical sources so installation cannot accidentally use stale bundles.
    entry = ENTRYPOINTS[harness]
    source_base = entry.parent
    files = {
        dest / relative.relative_to(source_base): content
        for relative, content in render(root).items()
        if relative.is_relative_to(source_base)
    }
    changed = []
    # Preflight every file before the first write. Conflicts leave the whole install untouched.
    for path, content in files.items():
        check_path(path)
        if path.exists():
            if not path.is_file():
                raise ValueError(f"Not a regular file: {path}")
            if path.read_bytes() == content:
                continue
            if not force:
                raise ValueError(f"Existing file differs: {path}. Review it, then use --force.")
        changed.append(path)
    if dry_run:
        return changed
    for path in changed:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            backup = path.with_name(path.name + ".promptly-backup")
            index = 1
            while backup.exists() or is_link(backup):
                backup = path.with_name(path.name + f".promptly-backup.{index}")
                index += 1
            # Exclusive creation prevents overwriting an earlier backup.
            with backup.open("xb") as stream:
                stream.write(path.read_bytes())
        path.write_bytes(files[path])
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    builder = commands.add_parser("build", help="Regenerate native bundles from the core")
    builder.add_argument("--check", action="store_true", help="Fail on drift without writing")
    installer = commands.add_parser("install", help="Install a native adapter (no model calls)")
    installer.add_argument("harness", choices=ENTRYPOINTS)
    installer.add_argument("--scope", choices=("project", "user"), default="project")
    installer.add_argument("--project", type=Path, default=Path.cwd())
    installer.add_argument("--destination", type=Path,
                           help="Exact skill folder, or commands folder for OpenCode")
    installer.add_argument("--dry-run", action="store_true")
    installer.add_argument("--force", action="store_true",
                           help="Back up and replace differing Promptly files")
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            stale = build(check=args.check)
            if args.check and stale:
                print("Out-of-date bundles: " + ", ".join(stale), file=sys.stderr)
                return 1
            print("Bundles match canonical sources." if args.check else "Built native bundles.")
        else:
            dest = args.destination or destination(
                args.harness, args.scope, args.project, Path.home(), dict(os.environ)
            )
            dest = dest.expanduser().absolute()
            paths = install(args.harness, dest, force=args.force, dry_run=args.dry_run)
            verb = "Would write" if args.dry_run else "Wrote"
            for path in paths:
                print(f"{verb}: {path}")
            if not paths:
                print(f"Already up to date: {dest}")
    except (OSError, ValueError) as exc:
        print(f"Promptly: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
