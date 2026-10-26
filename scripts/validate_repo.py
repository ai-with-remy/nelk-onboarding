#!/usr/bin/env python3
"""Check the marketplace files, plugin manifests and skill front matter agree."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(ROOT)}: {exc}")
        return {}


claude_market = load(ROOT / ".claude-plugin/marketplace.json")
codex_market = load(ROOT / ".agents/plugins/marketplace.json")

for entry in claude_market.get("plugins", []):
    plugin_dir = (ROOT / entry["source"]).resolve()
    manifests = [
        plugin_dir / ".claude-plugin/plugin.json",
        plugin_dir / ".codex-plugin/plugin.json",
        plugin_dir / "plugin.json",
    ]
    versions = set()
    for manifest in manifests:
        data = load(manifest)
        if data.get("name") != entry["name"]:
            errors.append(f"{manifest.relative_to(ROOT)}: name should be {entry['name']!r}")
        versions.add(data.get("version"))
    if len(versions) != 1:
        errors.append(f"{entry['name']}: manifest versions differ {sorted(map(str, versions))}")

    codex_names = {p["name"] for p in codex_market.get("plugins", [])}
    if entry["name"] not in codex_names:
        errors.append(f"{entry['name']}: missing from .agents/plugins/marketplace.json")

    for skill_md in sorted((plugin_dir / "skills").glob("*/SKILL.md")):
        text = skill_md.read_text()
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not match:
            errors.append(f"{skill_md.relative_to(ROOT)}: missing front matter")
            continue
        name = re.search(r"^name:\s*(\S+)", match.group(1), re.M)
        if not name or name.group(1) != skill_md.parent.name:
            errors.append(f"{skill_md.relative_to(ROOT)}: name must match folder {skill_md.parent.name!r}")
        if "description:" not in match.group(1):
            errors.append(f"{skill_md.relative_to(ROOT)}: missing description")
        for bundled in ("templates.md", "voice-dna-base.md"):
            if bundled in text and not (skill_md.parent / bundled).exists():
                errors.append(f"{skill_md.relative_to(ROOT)}: bundled file {bundled} is missing")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("Marketplace, manifests and skills look consistent.")
