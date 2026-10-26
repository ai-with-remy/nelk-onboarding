#!/usr/bin/env python3
"""Validate plugins against the Agent Plugins Specification v1.0.0.

Checks every plugin root passed on the command line (or auto-discovered under
./plugins/ when none are given):

  - plugin.json exists at the plugin ROOT (not inside a client directory)
  - $schema is exactly the v1.0.0 plugin schema URL
  - name is present and matches the spec's character rules
  - no field outside the spec's closed top-level set
  - field types are correct; version is semver when present
  - skills/ exists and every immediate child has a regular SKILL.md
  - no skill is buried deeper than one level (clients must not recurse)
  - mcp.json, when present, uses the right $schema, valid server types,
    and plugin-relative paths that stay inside the plugin root

Exit 0 = conformant. Exit 1 = at least one violation.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"

# Closed schema: these are the ONLY permitted top-level fields.
ALLOWED = {
    "$schema", "name", "version", "description", "author",
    "homepage", "repository", "license", "keywords", "extensions",
}
AUTHOR_KEYS = {"name", "email", "url"}

# 1-64 chars, [a-z0-9-.], starts/ends alphanumeric, no "--" or ".."
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9]|-(?!-)|\.(?!\.))*[a-z0-9]$|^[a-z0-9]$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
NAMESPACE_RE = re.compile(r"^[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")
SERVER_TYPES = {"stdio", "streamable-http", "sse"}


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.plugins = 0
        self.skills = 0

    def error(self, where: Path | str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: Path | str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def load_json(path: Path, report: Report) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(rel(path), f"invalid JSON — {exc}")
        return None
    except OSError as exc:
        report.error(rel(path), f"unreadable — {exc}")
        return None
    if not isinstance(data, dict):
        report.error(rel(path), "top level must be a JSON object")
        return None
    return data


def check_name(value: str) -> str | None:
    if not 1 <= len(value) <= 64:
        return "name must be 1-64 characters"
    if not NAME_RE.match(value):
        return (
            "name must use only lowercase letters, digits, '-' and '.', "
            "start and end alphanumeric, with no '--' or '..'"
        )
    return None


def check_manifest(root: Path, report: Report) -> None:
    manifest_path = root / "plugin.json"
    if not manifest_path.is_file():
        report.error(rel(root), "missing plugin.json at the plugin root")
        return

    data = load_json(manifest_path, report)
    if data is None:
        return
    where = rel(manifest_path)

    schema = data.get("$schema")
    if schema is None:
        report.error(where, "missing required field '$schema'")
    elif schema != PLUGIN_SCHEMA:
        report.error(where, f"$schema must be '{PLUGIN_SCHEMA}' (got '{schema}')")

    name = data.get("name")
    if name is None:
        report.error(where, "missing required field 'name'")
    elif not isinstance(name, str):
        report.error(where, "'name' must be a string")
    else:
        problem = check_name(name)
        if problem:
            report.error(where, problem)
        elif name != root.name:
            report.warn(where, f"name '{name}' differs from directory '{root.name}'")

    for field in sorted(set(data) - ALLOWED):
        report.error(where, f"unknown top-level field '{field}' — schema is closed")

    for field in ("description", "homepage", "repository", "license"):
        if field in data and not isinstance(data[field], str):
            report.error(where, f"'{field}' must be a string")

    if "version" in data:
        version = data["version"]
        if not isinstance(version, str):
            report.error(where, "'version' must be a string")
        elif not SEMVER_RE.match(version):
            report.error(where, f"'version' should be semver (got '{version}')")

    if "keywords" in data:
        keywords = data["keywords"]
        if not isinstance(keywords, list) or not all(isinstance(k, str) for k in keywords):
            report.error(where, "'keywords' must be an array of strings")

    if "author" in data:
        author = data["author"]
        if not isinstance(author, dict):
            report.error(where, "'author' must be an object")
        else:
            for key in sorted(set(author) - AUTHOR_KEYS):
                report.error(where, f"unknown 'author' field '{key}'")
            for key, value in author.items():
                if not isinstance(value, str):
                    report.error(where, f"'author.{key}' must be a string")

    if "extensions" in data:
        extensions = data["extensions"]
        if not isinstance(extensions, dict):
            report.error(where, "'extensions' must be an object")
        else:
            for namespace in extensions:
                if not NAMESPACE_RE.match(namespace):
                    report.error(
                        where,
                        f"extension key '{namespace}' must be a reverse-domain namespace",
                    )


def check_skills(root: Path, report: Report) -> None:
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        report.warn(rel(root), "no skills/ directory — plugin ships no skills")
        return

    found = 0
    for child in sorted(skills_dir.iterdir()):
        if child.name.startswith("."):
            continue
        if not child.is_dir():
            report.warn(rel(child), "stray file in skills/ — only skill directories are read")
            continue
        skill_md = child / "SKILL.md"
        if skill_md.is_file():
            found += 1
            continue
        # A SKILL.md one level deeper is invisible to a conformant client.
        buried = [p for p in child.rglob("SKILL.md") if p.is_file()]
        if buried:
            report.error(
                rel(child),
                "no SKILL.md at this level, but one exists deeper — clients MUST NOT "
                f"recurse (found {rel(buried[0])})",
            )
        else:
            report.warn(rel(child), "directory in skills/ with no SKILL.md — ignored by clients")

    if found == 0:
        report.warn(rel(skills_dir), "skills/ contains no loadable skills")
    report.skills += found


def check_relative_path(value: str, root: Path, where: str, field: str, report: Report) -> None:
    if value.startswith("${PLUGIN_ROOT}") or value.startswith("${PLUGIN_DATA}"):
        return
    if not value.startswith("./"):
        report.error(where, f"{field} must be a bare command name or start with './' (got '{value}')")
        return
    resolved = (root / value).resolve()
    if not str(resolved).startswith(str(root.resolve())):
        report.error(where, f"{field} escapes the plugin root (got '{value}')")


def check_mcp(root: Path, report: Report) -> None:
    mcp_path = root / "mcp.json"
    if not mcp_path.is_file():
        return
    data = load_json(mcp_path, report)
    if data is None:
        return
    where = rel(mcp_path)

    if data.get("$schema") != MCP_SCHEMA:
        report.error(where, f"$schema must be '{MCP_SCHEMA}'")

    servers = data.get("mcpServers")
    if servers is None:
        report.error(where, "missing required field 'mcpServers'")
        return
    if not isinstance(servers, dict):
        report.error(where, "'mcpServers' must be an object")
        return

    for server_name, entry in servers.items():
        label = f"{where} [{server_name}]"
        if not isinstance(entry, dict):
            report.error(label, "server entry must be an object")
            continue
        server_type = entry.get("type")
        if server_type not in SERVER_TYPES:
            report.error(label, f"'type' must be one of {sorted(SERVER_TYPES)} (got '{server_type}')")
            continue
        if server_type == "sse":
            report.warn(label, "'sse' transport is deprecated — prefer 'streamable-http'")
        if server_type == "stdio":
            command = entry.get("command")
            if not isinstance(command, str) or not command:
                report.error(label, "stdio server requires a non-empty 'command'")
            elif "/" in command:
                check_relative_path(command, root, label, "'command'", report)
            if "cwd" in entry and isinstance(entry["cwd"], str):
                check_relative_path(entry["cwd"], root, label, "'cwd'", report)
            for key in ("args",):
                if key in entry and (
                    not isinstance(entry[key], list)
                    or not all(isinstance(v, str) for v in entry[key])
                ):
                    report.error(label, f"'{key}' must be an array of strings")
        else:
            url = entry.get("url")
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                report.error(label, "'url' must be an absolute http(s) URL")
            elif "#" in url:
                report.error(label, "'url' must not contain a fragment")


def discover(argv: list[str]) -> list[Path]:
    if argv:
        return [Path(a).resolve() for a in argv]
    plugins_dir = Path.cwd() / "plugins"
    if plugins_dir.is_dir():
        return sorted(p.resolve() for p in plugins_dir.iterdir() if p.is_dir())
    # Fall back to any immediate child directory that ships a skills/ dir.
    return sorted(
        p.resolve()
        for p in Path.cwd().iterdir()
        if p.is_dir() and not p.name.startswith(".") and (p / "skills").is_dir()
    )


def main(argv: list[str]) -> int:
    roots = discover(argv)
    if not roots:
        print("No plugin roots found.", file=sys.stderr)
        return 1

    report = Report()
    for root in roots:
        if not root.is_dir():
            report.error(str(root), "not a directory")
            continue
        report.plugins += 1
        check_manifest(root, report)
        check_skills(root, report)
        check_mcp(root, report)

    for warning in report.warnings:
        print(f"warning: {warning}")
    for error in report.errors:
        print(f"ERROR: {error}", file=sys.stderr)

    print(
        f"\nAgent Plugins v1.0.0 — checked {report.plugins} plugin(s), "
        f"{report.skills} skill(s): "
        f"{len(report.errors)} error(s), {len(report.warnings)} warning(s)"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
