#!/usr/bin/env python3
"""Static contract tests for the AI OS layout-aware skill suite."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AI_OS = ROOT / "plugins" / "ai-os"
SKILLS = AI_OS / "skills"
EXPECTED_PLUGINS = {
    "ai-os": ("1.0.1", 2),
}


class AiOsSkillContractTests(unittest.TestCase):
    def read_skill(self, name: str) -> str:
        return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")

    def test_every_owned_ai_os_skill_ends_with_self_improvement_loop(self) -> None:
        for path in sorted(SKILLS.glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8").rstrip()
            self.assertIn("## Self-Improvement Loop", text, path)
            self.assertTrue(
                text.rfind("## Self-Improvement Loop") > len(text) * 0.8,
                f"{path} must end with the loop",
            )
            self.assertTrue(text.endswith("only after explicit approval."), path)

    def test_build_os_is_root_v3_only(self) -> None:
        text = self.read_skill("build-os")
        for required in (
            "MASTER_PATH=<OS_ROOT>/AGENTS.md",
            "MEMORY_PATH=<OS_ROOT>/MEMORY.md",
            "ROOT_SIGNPOST=none",
            "SKILL_HOMES=[<OS_ROOT>/.agents/skills]",
            "SKILL_COMPAT_PATH=<OS_ROOT>/.claude/skills",
            "brand-new student workspace",
            "six context files",
            "Windows registry",
            "learning and memory policy",
        ):
            self.assertIn(required, text)
        for forbidden in (
            ".claude/CLAUDE.md",
            ".claude/LESSONS.md",
            "legacy migration",
            "upgrade in place",
            "@AGENTS.md",
            "Write to `<OS_ROOT>/CLAUDE.md`",
        ):
            self.assertNotIn(forbidden, text)
        self.assertIn("no root `CLAUDE.md`", text)

    def test_root_v3_templates_use_one_canonical_master_and_conditional_signposts(self) -> None:
        templates = (SKILLS / "build-os" / "file-templates.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Root `AGENTS.md` — canonical cross-harness master", templates)
        self.assertNotIn("@AGENTS.md", templates)
        self.assertNotIn("Write to `<OS_ROOT>/CLAUDE.md`", templates)
        self.assertIn("There is no root `CLAUDE.md` template", templates)
        self.assertIn("All paths are\nrelative to the AI OS root", templates)
        self.assertIn("Before a task about offers, pricing, or packaging", templates)
        self.assertIn("read `context/offers.md` in full", templates)
        self.assertNotIn("@context/", templates)

    def test_root_v3_template_has_memory_routing_and_execution_standards(self) -> None:
        templates = (SKILLS / "build-os" / "file-templates.md").read_text(
            encoding="utf-8"
        )
        for required in (
            "Read `MEMORY.md` in full at the start of every task.",
            "A rule for one workflow → the relevant `SKILL.md`.",
            "An execution mistake is not a new memory.",
            "Never duplicate an instruction across files.",
            "### Delegate execution",
            "When subagents are available, delegate substantial execution",
            "The main agent remains responsible",
            "Never claim completion without",
            "Keep reusable skills in `.agents/skills/`",
            "must not contain separate",
        ):
            self.assertIn(required, templates)

    def test_root_v3_instruction_and_skill_compatibility_stay_distinct(self) -> None:
        layout = (AI_OS / "shared" / "workspace-layout.md").read_text(
            encoding="utf-8"
        )
        build = self.read_skill("build-os")

        for text in (layout, build):
            self.assertIn("macOS", text)
            self.assertIn("Windows", text)
            self.assertIn("Linux", text)
            self.assertIn("only", text.lower())
            self.assertIn("v2.1.277", text)

        self.assertIn("| `ROOT_SIGNPOST` | none |", layout)
        self.assertIn("never flag it", layout)
        self.assertIn("never auto-delete it", layout)
        self.assertIn("Never symlink, junction, hard-link, or copy", build)
        self.assertIn("never add a `CLAUDE.md` loader", " ".join(build.split()))

        for name in ("build-context",):
            text = self.read_skill(name)
            self.assertIn("ROOT_SIGNPOST", text)
            self.assertIn("@AGENTS.md", text)
            self.assertIn("Remy or Mav", text)

    def test_layout_consumers_use_resolved_master_and_memory(self) -> None:
        for name in ("build-context",):
            text = self.read_skill(name)
            self.assertIn("shared/workspace-layout.md", text, name)
            self.assertIn("MASTER_PATH", text, name)
            self.assertIn("MEMORY_PATH", text, name)

    def test_context_narration_matches_each_layout(self) -> None:
        text = self.read_skill("build-context")
        self.assertIn("This layout keeps that knowledge in one shared brain", text)
        self.assertIn("tells the AI exactly which one to read", text)
        self.assertNotIn("load automatically every single session", text)
        self.assertIn("original-cohort explanation from `workspace-layout.md`", text)
        self.assertNotIn(
            "Back in Session 1, each of your business folders", text
        )

    def test_build_os_chimes_have_executable_safe_payloads(self) -> None:
        text = self.read_skill("build-os")
        for required in (
            'If `PROJECT_SETTINGS` is absent, use `{}`',
            "AI_OS_CHIME_ID=finish afplay",
            "AI_OS_CHIME_ID=question afplay",
            "$env:AI_OS_CHIME_ID='finish'",
            "$env:AI_OS_CHIME_ID='question'",
            "Media.SoundPlayer",
            "$env:CLAUDE_PROJECT_DIR",
            "Preserve every unrelated top-level",
            "no credentials",
        ):
            self.assertIn(required, text)

    def test_build_os_names_exact_host_plugin_cascade(self) -> None:
        text = self.read_skill("build-os")
        self.assertIn("ai-os@nelk-onboarding", text)
        for retired in ("tac-general", "tac-marketing", "the-ai-course"):
            self.assertNotIn(retired, text)
        self.assertIn("Never write Claude settings from Codex", text)

    def test_build_os_ledgers_every_created_path_immediately(self) -> None:
        text = self.read_skill("build-os")
        for required in (
            "Created-path transaction rule",
            "root file, context file, business/client",
            "before any other filesystem",
            "mutation",
            '[".claude", ".claude/.ai-os-progress.json"]',
            "After creating each root/context file",
            "append its relative path to `created_paths`",
            "If progress is absent and the only existing item",
            "interrupted zero-data bootstrap",
            "remove existing `created_paths` entries deepest-first",
            "preserve every\n   unlisted path",
        ):
            self.assertIn(required, text)

    def test_three_ai_os_manifests_match(self) -> None:
        paths = (
            AI_OS / "plugin.json",
            AI_OS / ".claude-plugin" / "plugin.json",
            AI_OS / ".codex-plugin" / "plugin.json",
        )
        versions = {json.loads(path.read_text())["version"] for path in paths}
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions, {"1.0.1"})

    def test_marketplaces_ship_exactly_the_first_party_plugins(self) -> None:
        for path in (
            ROOT / ".claude-plugin" / "marketplace.json",
            ROOT / ".agents" / "plugins" / "marketplace.json",
        ):
            payload = json.loads(path.read_text(encoding="utf-8"))
            names = {entry["name"] for entry in payload["plugins"]}
            self.assertEqual(names, set(EXPECTED_PLUGINS), path)
            self.assertEqual(len(payload["plugins"]), len(EXPECTED_PLUGINS), path)

    def test_first_party_plugin_versions_and_skill_counts_are_locked(self) -> None:
        plugin_dirs = {
            path.name for path in (ROOT / "plugins").iterdir() if path.is_dir()
        }
        self.assertEqual(plugin_dirs, set(EXPECTED_PLUGINS))

        for plugin_name, (
            expected_version,
            expected_skills,
        ) in EXPECTED_PLUGINS.items():
            plugin_root = ROOT / "plugins" / plugin_name
            manifests = (
                plugin_root / "plugin.json",
                plugin_root / ".claude-plugin" / "plugin.json",
                plugin_root / ".codex-plugin" / "plugin.json",
            )
            versions = {
                json.loads(path.read_text(encoding="utf-8"))["version"]
                for path in manifests
            }
            self.assertEqual(versions, {expected_version}, plugin_name)
            skills = list((plugin_root / "skills").glob("*/SKILL.md"))
            self.assertEqual(len(skills), expected_skills, plugin_name)

    def test_breaking_public_command_rename_is_complete(self) -> None:
        public_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                ROOT / "README.md",
                *sorted(AI_OS.rglob("*.md")),
                *sorted(AI_OS.rglob("*.json")),
            )
        )
        for legacy in (
            "/ai-os:onboard",
            "$ai-os:onboard",
            "/ai-os:context",
            "$ai-os:context",
        ):
            self.assertNotIn(legacy, public_text)
        self.assertIn("/ai-os:build-os", public_text)
        self.assertIn("/ai-os:build-context", public_text)

        skill_names = {path.parent.name for path in SKILLS.glob("*/SKILL.md")}
        self.assertIn("build-os", skill_names)
        self.assertIn("build-context", skill_names)
        self.assertNotIn("onboard", skill_names)
        self.assertNotIn("context", skill_names)

    def test_build_os_contract_covers_location_light_context_and_proof(self) -> None:
        text = self.read_skill("build-os")
        for required in (
            "DEFAULT_OS_ROOT",
            "custom location",
            "sessions.onboard",
            'next_skill="build-context"',
            "15–20\nminutes",
            "What do you know about me and how should you work with me?",
            "at least two",
            "MEMORY.md",
        ):
            self.assertIn(required, text)
        self.assertIn("If it contains any file or folder, make no writes", text)
        self.assertIn("Preserve unrelated settings byte-for-byte", text)
        self.assertIn("Do not add an artificial entry to `MEMORY.md`", text)

    def test_build_context_reuses_legacy_state_without_repeating_answers(self) -> None:
        text = self.read_skill("build-context")
        for required in (
            "sessions.onboard",
            "sessions.context",
            "build-os",
            "Never re-ask",
            "MEMORY.md",
        ):
            self.assertIn(required, text)
        self.assertIn("an enduring lesson learned later", text)
        self.assertIn("Do not invent an entry", text)


if __name__ == "__main__":
    unittest.main()
