#!/usr/bin/env python3
"""Resolve supported AI OS workspace layouts without writing files."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


ROUTING_ONLY_RE = re.compile(
    r"^(?:"
    r"@[\w./\\-]+|"
    r"(?:before|first|always|please)?\s*(?:read|see|use|follow|load|look at)\b.*"
    r"(?:claude|agents|memory|lessons|context)[\w./\\ -]*\.md.*|"
    r"`?[\w./\\-]+\.md`?(?:\s*(?:is|are)\s+(?:the\s+)?(?:master|source of truth|signpost))?[.!]?"
    r")$",
    re.IGNORECASE,
)

# Earlier root-v3 builds wrote this one-line Claude loader. New builds write no
# root CLAUDE.md, but an existing loader stays healthy and is never removed.
LEGACY_ROOT_V3_CLAUDE_LOADER = b"@AGENTS.md\n"


@dataclass(frozen=True)
class Layout:
    layout: str
    os_root: str
    master_path: str | None
    memory_path: str | None
    root_signpost: str | None
    context_dir: str
    skill_homes: list[str]
    skill_compat_path: str | None
    progress_path: str
    backup_root: str
    chime_root: str
    project_settings: str
    writes_allowed: bool
    reason: str | None = None


class UnsafeLayoutError(RuntimeError):
    """Raised when a caller attempts to write to an unresolved workspace."""


def _meaningful_lines(text: str) -> list[str]:
    lines: list[str] = []
    in_frontmatter = False
    for index, raw in enumerate(text.splitlines()):
        line = raw.strip()
        if index == 0 and line == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line == "---":
                in_frontmatter = False
            continue
        if not line or line.startswith(("<!--", "#", ">")):
            continue
        if line in {"---", "```", "```markdown", "```text"}:
            continue
        line = re.sub(r"^[-*]\s+", "", line).strip()
        if line:
            lines.append(line)
    return lines


def is_substantive(path: Path) -> bool:
    """Return true only when a file contains more than imports/routing."""
    if not path.is_file():
        return False
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError):
        return True
    lines = _meaningful_lines(text)
    if not lines:
        return False
    return any(not ROUTING_ONLY_RE.fullmatch(line) for line in lines)


def root_v3_instruction_compat_issues(os_root: Path) -> list[str]:
    """Return deterministic health issues for root-v3 instructions.

    Root CLAUDE.md is optional: absent is healthy, and a routing-only file such
    as the legacy `@AGENTS.md` loader is also healthy.
    """
    root = os_root.resolve(strict=False)
    agents_path = root / "AGENTS.md"
    claude_path = root / "CLAUDE.md"
    issues: list[str] = []

    if agents_path.is_symlink():
        issues.append("AGENTS.md must be a regular file, not a filesystem link")
    elif not agents_path.is_file():
        issues.append("AGENTS.md is missing or is not a regular file")
    elif not is_substantive(agents_path):
        issues.append("AGENTS.md is not substantive")

    if claude_path.is_symlink():
        issues.append("CLAUDE.md, when present, must be a regular file, not a filesystem link")
    elif claude_path.exists() and is_substantive(claude_path):
        issues.append("CLAUDE.md, when present, must be routing-only")

    return issues


def resolve_os_root(
    *,
    platform: str,
    home: Path | None = None,
    desktop: Path | None = None,
) -> Path:
    """Resolve the Desktop/OS default, including Windows registry behavior."""
    home = home or Path.home()
    if desktop is not None:
        return desktop / "OS"
    if platform == "windows":
        if os.name == "nt":
            try:
                import winreg  # type: ignore[import-not-found]

                key_name = (
                    r"Software\Microsoft\Windows\CurrentVersion\Explorer"
                    r"\Shell Folders"
                )
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_name) as key:
                    value, _ = winreg.QueryValueEx(key, "Desktop")
                return Path(os.path.expandvars(value)) / "OS"
            except (OSError, ImportError):
                pass
        one_drive = home / "OneDrive" / "Desktop"
        return (one_drive if one_drive.is_dir() else home / "Desktop") / "OS"
    if platform in {"macos", "linux"}:
        return home / "Desktop" / "OS"
    raise ValueError(f"unsupported platform: {platform}")


def resolve_existing_os_root(
    *,
    platform: str,
    active_workspace: Path | None = None,
    home: Path | None = None,
    desktop: Path | None = None,
) -> Path | None:
    """Prefer a supported active OS, then check only the Desktop default."""
    if active_workspace is not None:
        active = active_workspace.resolve(strict=False)
        active_layout = resolve_layout(active)
        if active_layout.layout in {"root-v3", "root-v2", "cohort-v1"}:
            progress = Path(active_layout.progress_path)
            if progress.is_file():
                try:
                    payload = json.loads(progress.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, json.JSONDecodeError):
                    payload = {}
                stored = (payload.get("student") or {}).get("os_root")
                if isinstance(stored, str) and stored.strip():
                    recorded = Path(stored).expanduser().resolve(strict=False)
                    if recorded != active:
                        raise UnsafeLayoutError(
                            "active workspace does not match student.os_root"
                        )
            return active

    default = resolve_os_root(platform=platform, home=home, desktop=desktop)
    if resolve_layout(default).layout in {"root-v3", "root-v2", "cohort-v1"}:
        return default.resolve(strict=False)
    return None


def resolve_layout(os_root: Path) -> Layout:
    root = os_root.resolve(strict=False)
    agents_master = root / "AGENTS.md"
    claude_master = root / "CLAUDE.md"
    cohort_master = root / ".claude" / "CLAUDE.md"
    agents_is_substantive = is_substantive(agents_master)
    claude_is_substantive = is_substantive(claude_master)
    cohort_is_substantive = is_substantive(cohort_master)

    common = {
        "os_root": str(root),
        "context_dir": str(root / "context"),
        "progress_path": str(root / ".claude" / ".ai-os-progress.json"),
        "chime_root": str(root / ".claude" / "sounds"),
        "project_settings": str(root / ".claude" / "settings.json"),
    }

    substantive_masters = sum(
        (agents_is_substantive, claude_is_substantive, cohort_is_substantive)
    )
    if substantive_masters > 1:
        return Layout(
            layout="mixed",
            master_path=None,
            memory_path=None,
            skill_homes=[],
            skill_compat_path=None,
            backup_root=str(root / ".claude" / "backups" / "ai-os"),
            root_signpost=None,
            writes_allowed=False,
            reason="multiple instruction files are substantive",
            **common,
        )

    if agents_is_substantive:
        return Layout(
            layout="root-v3",
            master_path=str(agents_master),
            memory_path=str(root / "MEMORY.md"),
            skill_homes=[str(root / ".agents" / "skills")],
            skill_compat_path=str(root / ".claude" / "skills"),
            backup_root=str(root / ".claude" / "backups" / "ai-os"),
            root_signpost=None,
            writes_allowed=True,
            **common,
        )

    if claude_is_substantive:
        return Layout(
            layout="root-v2",
            master_path=str(claude_master),
            memory_path=str(root / "MEMORY.md"),
            skill_homes=[str(root / ".claude" / "skills")],
            skill_compat_path=None,
            backup_root=str(root / ".claude" / "backups" / "ai-os"),
            root_signpost=str(root / "AGENTS.md"),
            writes_allowed=True,
            **common,
        )

    if cohort_is_substantive:
        upgraded_memory = root / ".claude" / "MEMORY.md"
        lessons = root / ".claude" / "LESSONS.md"
        memory = upgraded_memory if is_substantive(upgraded_memory) else lessons
        return Layout(
            layout="cohort-v1",
            master_path=str(cohort_master),
            memory_path=str(memory),
            skill_homes=[
                str(root / ".claude" / "skills"),
                str(root / ".agents" / "skills"),
            ],
            skill_compat_path=None,
            backup_root=str(root / ".archive" / "ai-os-maintenance"),
            root_signpost=str(root / "AGENTS.md"),
            writes_allowed=True,
            **common,
        )

    return Layout(
        layout="uninitialized",
        master_path=None,
        memory_path=None,
        skill_homes=[],
        skill_compat_path=None,
        backup_root=str(root / ".claude" / "backups" / "ai-os"),
        root_signpost=None,
        writes_allowed=False,
        reason="no substantive supported master found",
        **common,
    )


def require_writable(layout: Layout) -> Layout:
    if not layout.writes_allowed:
        raise UnsafeLayoutError(layout.reason or f"unsafe layout: {layout.layout}")
    return layout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--os-root", type=Path)
    parser.add_argument("--platform", choices=("macos", "windows", "linux"))
    parser.add_argument("--home", type=Path)
    parser.add_argument("--desktop", type=Path)
    parser.add_argument("--require-writable", action="store_true")
    args = parser.parse_args(argv)

    if args.os_root is None:
        if args.platform is None:
            parser.error("--platform is required when --os-root is omitted")
        os_root = resolve_os_root(
            platform=args.platform,
            home=args.home,
            desktop=args.desktop,
        )
    else:
        os_root = args.os_root

    layout = resolve_layout(os_root)
    print(json.dumps(asdict(layout), indent=2))
    if args.require_writable and not layout.writes_allowed:
        print(layout.reason or "workspace is not writable", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
