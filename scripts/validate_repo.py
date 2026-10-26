#!/usr/bin/env python3
"""Validate both plugin formats and every bundled skill without third-party packages."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PLUGINS_ROOT = ROOT / "plugins"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
CODEX_MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"

SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
SKILL_DESCRIPTION_LIMIT = 1024
CODEX_SKILL_KEYS = {"allowed-tools", "description", "license", "metadata", "name"}
INSTALL_POLICIES = {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}
AUTH_POLICIES = {"ON_INSTALL", "ON_USE"}
LOCAL_PLUGIN_NAMES = {"ai-os"}
RESOURCE_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"((?:references|scripts|assets|templates)/[A-Za-z0-9_. /-]+\.[A-Za-z0-9]+)"
)
PLUGIN_RESOURCE_RE = re.compile(
    r"\$\{CLAUDE_PLUGIN_ROOT\}/([A-Za-z0-9_. /-]+\.[A-Za-z0-9]+)"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
AI_OS_SKILL_NAMES = (
    "build-context",
    "build-os",
)
AI_OS_SKILL_PATTERN = "|".join(re.escape(name) for name in AI_OS_SKILL_NAMES)
CLAUDE_NAMESPACED_INVOCATION_RE = re.compile(
    rf"/ai-os:(?:<name>|{AI_OS_SKILL_PATTERN})"
)
CODEX_NAMESPACED_INVOCATION_RE = re.compile(
    rf"\$ai-os:(?:<name>|{AI_OS_SKILL_PATTERN})"
)
CLAUDE_SHORT_PRIMARY_RE = re.compile(
    rf"\bClaude(?: Code)?\b(?:(?!\n\n).){{0,240}}"
    rf"`/(?!ai-os:)(?:<name>|{AI_OS_SKILL_PATTERN})`",
    re.IGNORECASE | re.DOTALL,
)
SHORT_FORM_CLAIM_RE = re.compile(
    rf"\bshort form\b(?:(?!\n\n).){{0,160}}"
    rf"`/(?!ai-os:)(?:<name>|{AI_OS_SKILL_PATTERN})`",
    re.IGNORECASE | re.DOTALL,
)
SHORT_COMMAND_BULLET_RE = re.compile(
    rf"^\s*>?\s*-\s+`/(?!ai-os:)(?:{AI_OS_SKILL_PATTERN})`\s+(?:\u2014|-)",
    re.MULTILINE,
)
LOCAL_ONLY_PROMISE_RE = re.compile(
    r"(?:\b(?:nothing|no\s+(?:data|information|content)|everything)\b"
    r"[^\n.]{0,100}\b(?:leaves?|is\s+sent|gets?\s+sent|stays?)\b"
    r"[^\n.]{0,80}\b(?:machine|computer|device|local)\b|"
    r"\b(?:100%|entirely|completely)\s+local\b)",
    re.IGNORECASE,
)
MULTILINE_COMMAND_WRITE_RE = re.compile(
    r"(?:\bcat\s+(?:>>|>)\s*[^\n]+<<-?\s*['\"]?"
    r"[A-Za-z_][A-Za-z0-9_]*['\"]?|"
    r"\b(?:Add-Content|Set-Content)\b[^\n]*-Value\s+@[\"'])",
    re.IGNORECASE,
)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.counts = {"json": 0, "plugins": 0, "skills": 0, "shell": 0, "python": 0}

    def error(self, path: Path | str, message: str) -> None:
        try:
            label = str(Path(path).resolve().relative_to(ROOT))
        except (ValueError, OSError):
            label = str(path)
        self.errors.append(f"{label}: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--packaging-only",
        action="store_true",
        help="Validate marketplaces and plugin manifests, but skip skill and script checks.",
    )
    parser.add_argument(
        "--base-ref",
        default=os.environ.get("VALIDATE_BASE_REF"),
        help=(
            "Git ref to compare for plugin version-bump checks. "
            "Defaults to VALIDATE_BASE_REF when set."
        ),
    )
    return parser.parse_args()


def load_json(path: Path, result: Validation) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.error(path, "missing JSON file")
        return None
    except (OSError, json.JSONDecodeError) as exc:
        result.error(path, f"invalid JSON ({exc})")
        return None
    result.counts["json"] += 1
    if not isinstance(payload, dict):
        result.error(path, "top level must be a JSON object")
        return None
    return payload


def nonempty_string(payload: dict[str, Any], key: str) -> bool:
    return isinstance(payload.get(key), str) and bool(payload[key].strip())


def valid_https_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def resolve_inside(base: Path, raw: Any) -> Path | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    candidate = PurePosixPath(raw.replace("\\", "/"))
    if candidate.is_absolute() or any(part in {"", ".."} for part in candidate.parts):
        return None
    resolved = (base / candidate.as_posix()).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return None
    return resolved


def validate_all_json(result: Validation) -> None:
    for path in sorted(ROOT.rglob("*.json")):
        if ".git" in path.parts:
            continue
        load_json(path, result)


def validate_claude_marketplace(result: Validation) -> dict[str, Path]:
    payload = load_json(CLAUDE_MARKETPLACE, result)
    local_plugins: dict[str, Path] = {}
    if payload is None:
        return local_plugins
    if payload.get("name") != "nelk-onboarding":
        result.error(CLAUDE_MARKETPLACE, "marketplace name must be `nelk-onboarding`")
    entries = payload.get("plugins")
    if not isinstance(entries, list):
        result.error(CLAUDE_MARKETPLACE, "`plugins` must be an array")
        return local_plugins
    names: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            result.error(CLAUDE_MARKETPLACE, f"plugins[{index}] must be an object")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            result.error(CLAUDE_MARKETPLACE, f"plugins[{index}].name must be non-empty")
            continue
        if name in names:
            result.error(CLAUDE_MARKETPLACE, f"duplicate plugin `{name}`")
        names.add(name)
        source = entry.get("source")
        if isinstance(source, str):
            plugin_root = resolve_inside(ROOT, source)
            if plugin_root is None or not plugin_root.is_dir():
                result.error(CLAUDE_MARKETPLACE, f"plugin `{name}` has a missing local source")
            else:
                local_plugins[name] = plugin_root
        elif isinstance(source, dict):
            # Remote pointers must clone over anonymous HTTPS: the `github` shorthand
            # resolves to an SSH URL, which fails on machines without GitHub SSH keys.
            kind = source.get("source")
            url = source.get("url")
            if kind == "github" and isinstance(source.get("repo"), str):
                result.error(
                    CLAUDE_MARKETPLACE,
                    f"plugin `{name}` uses the `github` source (clones over SSH; "
                    'students can\'t) — use {"source": "url", "url": "https://github.com/<owner>/<repo>.git"}',
                )
            elif kind not in ("url", "git-subdir") or not isinstance(url, str) or not url.startswith("https://"):
                result.error(CLAUDE_MARKETPLACE, f"plugin `{name}` has an invalid remote source")
        else:
            result.error(CLAUDE_MARKETPLACE, f"plugin `{name}` has an invalid source")
    if set(local_plugins) != LOCAL_PLUGIN_NAMES:
        result.error(
            CLAUDE_MARKETPLACE,
            f"local plugin set must be {sorted(LOCAL_PLUGIN_NAMES)}, got {sorted(local_plugins)}",
        )
    return local_plugins


def validate_codex_marketplace(result: Validation) -> dict[str, Path]:
    payload = load_json(CODEX_MARKETPLACE, result)
    local_plugins: dict[str, Path] = {}
    if payload is None:
        return local_plugins
    if payload.get("name") != "nelk-onboarding":
        result.error(CODEX_MARKETPLACE, "marketplace name must be `nelk-onboarding`")
    interface = payload.get("interface")
    if not isinstance(interface, dict) or not nonempty_string(interface, "displayName"):
        result.error(CODEX_MARKETPLACE, "interface.displayName must be non-empty")
    entries = payload.get("plugins")
    if not isinstance(entries, list):
        result.error(CODEX_MARKETPLACE, "`plugins` must be an array")
        return local_plugins
    names: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            result.error(CODEX_MARKETPLACE, f"plugins[{index}] must be an object")
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not name:
            result.error(CODEX_MARKETPLACE, f"plugins[{index}].name must be non-empty")
            continue
        if name in names:
            result.error(CODEX_MARKETPLACE, f"duplicate plugin `{name}`")
        names.add(name)
        policy = entry.get("policy")
        if not isinstance(policy, dict):
            result.error(CODEX_MARKETPLACE, f"plugin `{name}` is missing policy")
        else:
            if policy.get("installation") not in INSTALL_POLICIES:
                result.error(CODEX_MARKETPLACE, f"plugin `{name}` has invalid installation policy")
            if policy.get("authentication") not in AUTH_POLICIES:
                result.error(CODEX_MARKETPLACE, f"plugin `{name}` has invalid authentication policy")
        if not nonempty_string(entry, "category"):
            result.error(CODEX_MARKETPLACE, f"plugin `{name}` is missing category")
        source = entry.get("source")
        if not isinstance(source, dict):
            result.error(CODEX_MARKETPLACE, f"plugin `{name}` source must be an object")
            continue
        source_kind = source.get("source")
        if source_kind == "local":
            plugin_root = resolve_inside(ROOT, source.get("path"))
            if plugin_root is None or not plugin_root.is_dir():
                result.error(CODEX_MARKETPLACE, f"plugin `{name}` has a missing local source")
            else:
                local_plugins[name] = plugin_root
        elif source_kind == "url":
            if not valid_https_url(source.get("url")):
                result.error(CODEX_MARKETPLACE, f"plugin `{name}` remote URL must use https")
            if not nonempty_string(source, "ref"):
                result.error(CODEX_MARKETPLACE, f"plugin `{name}` remote source is missing ref")
        else:
            result.error(CODEX_MARKETPLACE, f"plugin `{name}` has unsupported source kind")
    if set(local_plugins) != LOCAL_PLUGIN_NAMES:
        result.error(
            CODEX_MARKETPLACE,
            f"local plugin set must be {sorted(LOCAL_PLUGIN_NAMES)}, got {sorted(local_plugins)}",
        )
    return local_plugins


def validate_claude_manifest(plugin_root: Path, result: Validation) -> dict[str, Any] | None:
    path = plugin_root / ".claude-plugin" / "plugin.json"
    payload = load_json(path, result)
    if payload is None:
        return None
    for key in ("name", "version", "description", "homepage"):
        if not nonempty_string(payload, key):
            result.error(path, f"`{key}` must be a non-empty string")
    if payload.get("name") != plugin_root.name:
        result.error(path, "manifest name must match the plugin folder")
    version = payload.get("version")
    if isinstance(version, str) and SEMVER_RE.fullmatch(version) is None:
        result.error(path, "version must use strict semantic versioning")
    author = payload.get("author")
    if not isinstance(author, dict) or not nonempty_string(author, "name"):
        result.error(path, "author.name must be non-empty")
    return payload


def validate_codex_manifest(plugin_root: Path, result: Validation) -> dict[str, Any] | None:
    path = plugin_root / ".codex-plugin" / "plugin.json"
    payload = load_json(path, result)
    if payload is None:
        return None
    allowed = {
        "id", "name", "version", "description", "skills", "apps", "mcpServers",
        "interface", "author", "homepage", "repository", "license", "keywords",
    }
    for key in sorted(set(payload) - allowed):
        result.error(path, f"unsupported manifest field `{key}`")
    for key in ("name", "version", "description"):
        if not nonempty_string(payload, key):
            result.error(path, f"`{key}` must be a non-empty string")
    if payload.get("name") != plugin_root.name:
        result.error(path, "manifest name must match the plugin folder")
    version = payload.get("version")
    if isinstance(version, str) and SEMVER_RE.fullmatch(version) is None:
        result.error(path, "version must use strict semantic versioning")
    author = payload.get("author")
    if not isinstance(author, dict) or not nonempty_string(author, "name"):
        result.error(path, "author.name must be non-empty")
    elif "url" in author and not valid_https_url(author["url"]):
        result.error(path, "author.url must be an absolute https URL")
    for key in ("homepage", "repository"):
        if key in payload and not valid_https_url(payload[key]):
            result.error(path, f"{key} must be an absolute https URL")
    skills_path = resolve_inside(plugin_root, payload.get("skills"))
    if skills_path != (plugin_root / "skills").resolve() or not skills_path.is_dir():
        result.error(path, "skills must resolve to the plugin's `skills/` directory")
    if "mcpServers" in payload:
        mcp_path = resolve_inside(plugin_root, payload["mcpServers"])
        if mcp_path != (plugin_root / ".mcp.json").resolve() or not mcp_path.is_file():
            result.error(path, "mcpServers must resolve to the plugin's `.mcp.json`")
    interface = payload.get("interface")
    if not isinstance(interface, dict):
        result.error(path, "interface must be an object")
    else:
        for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
            if not nonempty_string(interface, key):
                result.error(path, f"interface.{key} must be non-empty")
        capabilities = interface.get("capabilities")
        if not isinstance(capabilities, list) or not all(
            isinstance(item, str) and item.strip() for item in capabilities
        ):
            result.error(path, "interface.capabilities must be an array of strings")
        prompts = interface.get("defaultPrompt")
        if not isinstance(prompts, list) or not prompts or len(prompts) > 3:
            result.error(path, "interface.defaultPrompt must contain one to three prompts")
        elif not all(isinstance(item, str) and 0 < len(item) <= 128 for item in prompts):
            result.error(path, "each default prompt must be a non-empty string of at most 128 characters")
        if "brandColor" in interface and (
            not isinstance(interface["brandColor"], str)
            or HEX_RE.fullmatch(interface["brandColor"]) is None
        ):
            result.error(path, "interface.brandColor must use #RRGGBB")
        for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
            if key in interface and not valid_https_url(interface[key]):
                result.error(path, f"interface.{key} must be an absolute https URL")
        for key in ("composerIcon", "logo", "logoDark"):
            if key in interface:
                asset = resolve_inside(plugin_root, interface[key])
                if asset is None or not asset.is_file():
                    result.error(path, f"interface.{key} points to a missing asset")
        screenshots = interface.get("screenshots", [])
        if not isinstance(screenshots, list):
            result.error(path, "interface.screenshots must be an array")
        else:
            for screenshot in screenshots:
                asset = resolve_inside(plugin_root, screenshot)
                if asset is None or not asset.is_file() or asset.suffix.lower() != ".png":
                    result.error(path, f"invalid screenshot asset `{screenshot}`")
    if "[TODO:" in json.dumps(payload):
        result.error(path, "manifest contains an unfinished TODO placeholder")
    result.counts["plugins"] += 1
    return payload


def validate_plugins(
    claude_plugins: dict[str, Path], codex_plugins: dict[str, Path], result: Validation
) -> dict[str, str]:
    versions: dict[str, str] = {}
    if claude_plugins != codex_plugins:
        result.error("marketplaces", "Claude and Codex local plugin paths do not match")
    for name, plugin_root in sorted(codex_plugins.items()):
        claude = validate_claude_manifest(plugin_root, result)
        codex = validate_codex_manifest(plugin_root, result)
        if claude is not None and codex is not None and claude.get("version") != codex.get("version"):
            result.error(plugin_root, "Claude and Codex manifest versions must match")
        if codex is not None and "mcpServers" in codex:
            result.error(plugin_root, "no plugin should declare MCP servers — /ai-os:connect adds them to the user's own config")
        if codex is not None:
            version = codex.get("version")
            if isinstance(version, str) and SEMVER_RE.fullmatch(version):
                versions[name] = version
    return versions


def compare_semver(left: str, right: str) -> int:
    """Return -1, 0, or 1 using SemVer precedence (build metadata is ignored)."""

    def parts(version: str) -> tuple[tuple[int, int, int], list[str] | None]:
        without_build = version.split("+", 1)[0]
        core, separator, prerelease = without_build.partition("-")
        major, minor, patch = (int(value) for value in core.split("."))
        return (major, minor, patch), prerelease.split(".") if separator else None

    left_core, left_pre = parts(left)
    right_core, right_pre = parts(right)
    if left_core != right_core:
        return 1 if left_core > right_core else -1
    if left_pre is None or right_pre is None:
        if left_pre is right_pre:
            return 0
        return 1 if left_pre is None else -1
    for left_id, right_id in zip(left_pre, right_pre):
        if left_id == right_id:
            continue
        left_numeric = left_id.isdigit()
        right_numeric = right_id.isdigit()
        if left_numeric and right_numeric:
            return 1 if int(left_id) > int(right_id) else -1
        if left_numeric != right_numeric:
            return -1 if left_numeric else 1
        return 1 if left_id > right_id else -1
    if len(left_pre) == len(right_pre):
        return 0
    return 1 if len(left_pre) > len(right_pre) else -1


def git_run(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def base_manifest_version(base_commit: str, manifest_path: Path) -> str | None:
    relative = manifest_path.relative_to(ROOT).as_posix()
    process = git_run(["show", f"{base_commit}:{relative}"])
    if process.returncode:
        return None
    try:
        payload = json.loads(process.stdout)
    except json.JSONDecodeError:
        return ""
    if not isinstance(payload, dict):
        return ""
    version = payload.get("version")
    if version is None:
        # Legacy Claude plugins may validly predate explicit SemVer. Introducing
        # the first paired Claude/Codex version is itself the release boundary.
        return None
    return version if isinstance(version, str) else ""


def validate_version_bumps(
    plugins: dict[str, Path],
    current_versions: dict[str, str],
    base_ref: str | None,
    result: Validation,
) -> None:
    """Require a newer paired manifest version when a plugin payload changed."""

    if not base_ref:
        return
    if shutil.which("git") is None:
        result.error("version bump guard", "git is required when --base-ref is supplied")
        return
    resolved = git_run(["rev-parse", "--verify", f"{base_ref}^{{commit}}"])
    if resolved.returncode:
        result.error("version bump guard", f"cannot resolve base ref `{base_ref}`")
        return
    base_commit = resolved.stdout.strip()
    for name, plugin_root in sorted(plugins.items()):
        relative_root = plugin_root.relative_to(ROOT).as_posix()
        changed = git_run(["diff", "--name-only", base_commit, "--", relative_root])
        untracked = git_run(
            ["ls-files", "--others", "--exclude-standard", "--", relative_root]
        )
        if changed.returncode or untracked.returncode:
            detail = changed.stderr.strip() or untracked.stderr.strip() or "git diff failed"
            result.error(plugin_root, f"could not compare payload with `{base_ref}` ({detail})")
            continue
        if not changed.stdout.strip() and not untracked.stdout.strip():
            continue

        base_versions: set[str] = set()
        for manifest_path in (
            plugin_root / ".claude-plugin" / "plugin.json",
            plugin_root / ".codex-plugin" / "plugin.json",
        ):
            base_version = base_manifest_version(base_commit, manifest_path)
            if base_version is None:
                continue
            if not base_version or SEMVER_RE.fullmatch(base_version) is None:
                result.error(
                    plugin_root,
                    f"base manifest at `{base_ref}` has an invalid version",
                )
                base_versions.clear()
                break
            base_versions.add(base_version)
        if not base_versions:
            # A plugin that did not exist at the base has no prior release to bump.
            continue
        current_version = current_versions.get(name)
        if current_version is None:
            continue
        stale_versions = sorted(
            version for version in base_versions if compare_semver(current_version, version) <= 0
        )
        if stale_versions:
            result.error(
                plugin_root,
                "payload changed since "
                f"`{base_ref}`, but version `{current_version}` is not newer than "
                f"base version(s) {', '.join(stale_versions)}",
            )


def parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return ""
    if raw in {"true", "false"}:
        return raw == "true"
    if raw in {"null", "~"}:
        return None
    if raw[0:1] in {"\"", "'"}:
        try:
            return ast.literal_eval(raw)
        except (SyntaxError, ValueError):
            return raw[1:-1]
    return raw


def parse_frontmatter(path: Path, result: Validation) -> tuple[dict[str, Any], str] | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        result.error(path, f"cannot read skill ({exc})")
        return None
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        result.error(path, "must start with YAML frontmatter")
        return None
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration:
        result.error(path, "frontmatter is not closed")
        return None
    fields: dict[str, Any] = {}
    index = 1
    while index < end:
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#"):
            index += 1
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            index += 1
            continue
        key, raw = line.split(":", 1)
        key = key.strip()
        if key in fields:
            result.error(path, f"frontmatter repeats `{key}`")
        raw = raw.strip()
        if raw in {">", ">-", ">+", "|", "|-", "|+"}:
            block: list[str] = []
            index += 1
            while index < end and (not lines[index].strip() or lines[index].startswith((" ", "\t"))):
                block.append(lines[index].strip())
                index += 1
            if raw.startswith(">"):
                fields[key] = re.sub(r"\s+", " ", " ".join(block)).strip()
            else:
                fields[key] = "\n".join(block).strip()
            continue
        fields[key] = parse_scalar(raw)
        index += 1
    body = "\n".join(lines[end + 1 :]).strip()
    return fields, body


def validate_agent_yaml(skill_root: Path, result: Validation) -> None:
    path = skill_root / "agents" / "openai.yaml"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    for field in ("display_name", "short_description"):
        if re.search(rf"^\s+{field}:\s*\S", text, re.MULTILINE) is None:
            result.error(path, f"interface.{field} must be non-empty")
    policy_match = re.search(r"^\s+allow_implicit_invocation:\s*(true|false)\s*$", text, re.MULTILINE)
    if policy_match is None:
        result.error(path, "policy.allow_implicit_invocation must be a boolean")


def validate_skill_references(skill_root: Path, text: str, result: Validation) -> None:
    for match in RESOURCE_RE.finditer(text):
        raw = match.group(1).strip().rstrip(".,:;)")
        candidate = (skill_root / raw).resolve()
        sibling_candidates = list((skill_root.parent).glob(f"*/{raw}"))
        if not candidate.is_file() and not any(path.is_file() for path in sibling_candidates):
            result.error(skill_root / "SKILL.md", f"referenced resource is missing: `{raw}`")
    plugin_root = skill_root.parent.parent
    for match in PLUGIN_RESOURCE_RE.finditer(text):
        raw = match.group(1).strip().rstrip(".,:;)")
        candidate = (plugin_root / raw).resolve()
        if not candidate.is_file():
            result.error(skill_root / "SKILL.md", f"plugin-root resource is missing: `{raw}`")


def validate_skills(result: Validation) -> None:
    for path in sorted(PLUGINS_ROOT.glob("*/skills/*/SKILL.md")):
        parsed = parse_frontmatter(path, result)
        if parsed is None:
            continue
        fields, body = parsed
        for key in sorted(set(fields) - CODEX_SKILL_KEYS):
            result.error(path, f"unsupported Codex frontmatter field `{key}`")
        name = fields.get("name")
        if not isinstance(name, str) or not name:
            result.error(path, "frontmatter.name must be non-empty")
        else:
            if name != path.parent.name:
                result.error(path, "frontmatter.name must match the skill folder")
            if len(name) > 64 or NAME_RE.fullmatch(name) is None:
                result.error(path, "frontmatter.name must be <=64 characters in lowercase hyphen-case")
        description = fields.get("description")
        if not isinstance(description, str) or not description:
            result.error(path, "frontmatter.description must be non-empty")
        elif len(description) > SKILL_DESCRIPTION_LIMIT:
            result.error(
                path,
                f"frontmatter.description is {len(description)} characters; maximum is {SKILL_DESCRIPTION_LIMIT}",
            )
        if not body:
            result.error(path, "skill body must not be empty")
        text = path.read_text(encoding="utf-8")
        validate_skill_references(path.parent, text, result)
        validate_agent_yaml(path.parent, result)
        result.counts["skills"] += 1


def validate_ai_os_contracts(result: Validation) -> None:
    """Check the shared runtime bootstrap, invocation copy, and unsafe promises."""

    skill_paths = sorted((PLUGINS_ROOT / "ai-os" / "skills").glob("*/SKILL.md"))
    for path in skill_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        missing = [
            marker
            for marker in ("shared/runtime.md", "PLUGIN_ROOT", "HOST_RUNTIME")
            if marker not in text
        ]
        if missing:
            result.error(
                path,
                "missing supported-runtime bootstrap marker(s): " + ", ".join(missing),
            )
        if LOCAL_ONLY_PROMISE_RE.search(text):
            result.error(
                path,
                "contains an absolute local-only privacy promise; describe the specific "
                "local file operation without promising what connected tools do",
            )
        if MULTILINE_COMMAND_WRITE_RE.search(text):
            result.error(
                path,
                "contains a shell/PowerShell multiline write pattern that is unsafe for "
                "user-provided content; use the active host's file-edit capability",
            )

    shared_privacy_paths = sorted((PLUGINS_ROOT / "ai-os" / "shared").glob("*.md"))
    shared_privacy_paths.append(
        PLUGINS_ROOT / "ai-os" / "skills" / "build-os" / "file-templates.md"
    )
    for path in shared_privacy_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            result.error(path, f"cannot read shared AI OS guidance ({exc})")
            continue
        if LOCAL_ONLY_PROMISE_RE.search(text):
            result.error(
                path,
                "contains an absolute local-only privacy promise; distinguish local file "
                "storage from processing under the active AI provider's terms",
            )

    invocation_paths = (
        ROOT / "README.md",
        PLUGINS_ROOT / "ai-os" / "shared" / "runtime.md",
        PLUGINS_ROOT / "ai-os" / "skills" / "build-context" / "SKILL.md",
        PLUGINS_ROOT / "ai-os" / "skills" / "build-os" / "SKILL.md",
    )
    for path in invocation_paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            result.error(path, f"cannot read invocation contract ({exc})")
            continue
        if CLAUDE_NAMESPACED_INVOCATION_RE.search(text) is None:
            result.error(path, "missing a canonical Claude `/ai-os:<skill>` invocation")
        if CODEX_NAMESPACED_INVOCATION_RE.search(text) is None:
            result.error(path, "missing a canonical Codex `$ai-os:<skill>` invocation")
        if (
            CLAUDE_SHORT_PRIMARY_RE.search(text)
            or SHORT_FORM_CLAIM_RE.search(text)
            or SHORT_COMMAND_BULLET_RE.search(text)
        ):
            result.error(
                path,
                "presents an unnamespaced Claude course command as the primary invocation; "
                "use `/ai-os:<skill>`",
            )


def validate_markdown_links(result: Validation) -> None:
    for path in sorted(ROOT.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for raw in MARKDOWN_LINK_RE.findall(text):
            target = raw.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            candidate = (path.parent / target).resolve()
            if not candidate.exists():
                result.error(path, f"Markdown link points to missing path `{raw}`")


def validate_scripts(result: Validation) -> None:
    bash = shutil.which("bash")
    for path in sorted(ROOT.rglob("*.sh")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "${{" in text:
            result.error(path, "contains GitHub-expression syntax inside a shell substitution")
        if bash is None:
            result.error(path, "bash is required for shell syntax validation")
        else:
            process = subprocess.run([bash, "-n", str(path)], capture_output=True, text=True)
            if process.returncode:
                result.error(path, f"shell syntax failed: {process.stderr.strip()}")
        result.counts["shell"] += 1
    for path in sorted(ROOT.rglob("*.py")):
        if ".git" in path.parts:
            continue
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
        except (OSError, SyntaxError) as exc:
            result.error(path, f"Python syntax failed: {exc}")
        result.counts["python"] += 1


def main() -> int:
    args = parse_args()
    result = Validation()
    validate_all_json(result)
    claude_plugins = validate_claude_marketplace(result)
    codex_plugins = validate_codex_marketplace(result)
    versions = validate_plugins(claude_plugins, codex_plugins, result)
    validate_version_bumps(codex_plugins, versions, args.base_ref, result)
    if not args.packaging_only:
        validate_skills(result)
        validate_ai_os_contracts(result)
        validate_markdown_links(result)
        validate_scripts(result)
    if result.errors:
        print(f"Validation failed with {len(result.errors)} error(s):", file=sys.stderr)
        for error in result.errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(
        "Validation passed: "
        f"{result.counts['plugins']} Codex plugins, "
        f"{result.counts['skills']} skills, "
        f"{result.counts['json']} JSON reads, "
        f"{result.counts['shell']} shell scripts, "
        f"{result.counts['python']} Python scripts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
