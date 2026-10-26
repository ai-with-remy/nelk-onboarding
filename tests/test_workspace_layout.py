#!/usr/bin/env python3
"""Focused tests for the shared AI OS workspace-layout contract."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "plugins" / "ai-os" / "shared" / "workspace_layout.py"
FIXTURES_PATH = ROOT / "tests" / "fixtures" / "workspace-layouts.json"
SPEC = importlib.util.spec_from_file_location("workspace_layout", MODULE_PATH)
assert SPEC and SPEC.loader
workspace_layout = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = workspace_layout
SPEC.loader.exec_module(workspace_layout)


class WorkspaceLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp(prefix="ai-os-layout-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def make_fixture(self, name: str, root: Path | None = None) -> Path:
        root = root or self.temp_dir / "OS"
        for relative, content in self.fixtures[name].items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        if name == "root-v3":
            claude_skills = root / ".claude" / "skills"
            claude_skills.parent.mkdir(parents=True, exist_ok=True)
            claude_skills.symlink_to(Path("..") / ".agents" / "skills")
        return root

    def test_root_v3_end_to_end_paths_and_one_linked_skill_home(self) -> None:
        root = self.make_fixture("root-v3")
        layout = workspace_layout.require_writable(
            workspace_layout.resolve_layout(root)
        )

        self.assertEqual(layout.layout, "root-v3")
        self.assertEqual(layout.master_path, str((root / "AGENTS.md").resolve()))
        self.assertIsNone(layout.root_signpost)
        self.assertEqual(layout.memory_path, str((root / "MEMORY.md").resolve()))
        self.assertEqual(
            layout.skill_homes,
            [str((root / ".agents" / "skills").resolve())],
        )
        self.assertEqual(
            layout.skill_compat_path,
            str(root.resolve() / ".claude" / "skills"),
        )
        self.assertTrue((root / ".claude" / "skills").is_symlink())
        canonical = Path(layout.skill_homes[0]) / "example" / "SKILL.md"
        through_claude = Path(layout.skill_compat_path) / "example" / "SKILL.md"
        self.assertEqual(canonical.read_bytes(), through_claude.read_bytes())
        self.assertEqual(canonical.resolve(), through_claude.resolve())
        self.assertFalse((root / "CLAUDE.md").exists())
        self.assertEqual(
            workspace_layout.root_v3_instruction_compat_issues(root), []
        )

    def test_root_v3_without_claude_md_is_healthy(self) -> None:
        root = self.make_fixture("root-v3")
        self.assertFalse((root / "CLAUDE.md").exists())
        self.assertFalse((root / ".claude" / "CLAUDE.md").exists())

        layout = workspace_layout.resolve_layout(root)

        self.assertEqual(layout.layout, "root-v3")
        self.assertTrue(layout.writes_allowed)
        self.assertIsNone(layout.root_signpost)
        self.assertEqual(
            workspace_layout.root_v3_instruction_compat_issues(root), []
        )

    def test_root_v3_with_legacy_agents_loader_is_still_healthy(self) -> None:
        root = self.make_fixture("root-v3")
        (root / "CLAUDE.md").write_bytes(
            workspace_layout.LEGACY_ROOT_V3_CLAUDE_LOADER
        )

        layout = workspace_layout.resolve_layout(root)

        self.assertEqual(layout.layout, "root-v3")
        self.assertTrue(layout.writes_allowed)
        self.assertEqual(
            workspace_layout.root_v3_instruction_compat_issues(root), []
        )
        self.assertEqual((root / "CLAUDE.md").read_bytes(), b"@AGENTS.md\n")

    def test_root_v3_instruction_compat_rejects_linked_agents_or_claude(self) -> None:
        linked_agents = self.make_fixture("root-v3", self.temp_dir / "agents-link")
        (linked_agents / "HANDBOOK.md").write_bytes(
            (linked_agents / "AGENTS.md").read_bytes()
        )
        (linked_agents / "AGENTS.md").unlink()
        (linked_agents / "AGENTS.md").symlink_to("HANDBOOK.md")
        self.assertIn(
            "AGENTS.md must be a regular file, not a filesystem link",
            workspace_layout.root_v3_instruction_compat_issues(linked_agents),
        )

        linked_claude = self.make_fixture("root-v3", self.temp_dir / "claude-link")
        (linked_claude / "CLAUDE.md").symlink_to("AGENTS.md")
        self.assertIn(
            "CLAUDE.md, when present, must be a regular file, not a filesystem link",
            workspace_layout.root_v3_instruction_compat_issues(linked_claude),
        )

    def test_root_v2_end_to_end_paths_and_single_real_skill_home(self) -> None:
        root = self.make_fixture("root-v2")
        layout = workspace_layout.require_writable(
            workspace_layout.resolve_layout(root)
        )

        self.assertEqual(layout.layout, "root-v2")
        self.assertEqual(layout.master_path, str((root / "CLAUDE.md").resolve()))
        self.assertEqual(layout.memory_path, str((root / "MEMORY.md").resolve()))
        self.assertEqual(
            layout.progress_path,
            str((root / ".claude" / ".ai-os-progress.json").resolve()),
        )
        self.assertEqual(
            layout.skill_homes,
            [str((root / ".claude" / "skills").resolve())],
        )
        self.assertTrue(
            (Path(layout.skill_homes[0]) / "example" / "SKILL.md").is_file()
        )
        for name in (
            "about-me.md",
            "business.md",
            "offers.md",
            "ideal-customer-profile.md",
            "working-style.md",
            "voice-dna.md",
        ):
            self.assertTrue((root / "context" / name).is_file())
        self.assertTrue((root / "alex-co" / "marketing").is_dir())
        self.assertTrue((root / "clients" / "acme").is_dir())
        self.assertTrue((root / ".claude" / "sounds" / "finish.mp3").is_file())
        self.assertFalse(any((root / "alex-co").rglob("CLAUDE.md")))
        self.assertFalse(any((root / "clients").rglob("AGENTS.md")))
        self.assertFalse((root / ".agents").exists())
        self.assertFalse((root / "active").exists())
        self.assertFalse((root / ".archive").exists())

    def test_cohort_v1_before_and_after_memory_repair(self) -> None:
        before = self.make_fixture("cohort-v1-before", self.temp_dir / "before")
        before_layout = workspace_layout.resolve_layout(before)
        self.assertEqual(before_layout.layout, "cohort-v1")
        self.assertTrue(before_layout.memory_path.endswith(".claude/LESSONS.md"))
        self.assertEqual(len(before_layout.skill_homes), 2)

        after = self.make_fixture("cohort-v1-after", self.temp_dir / "after")
        after_layout = workspace_layout.resolve_layout(after)
        self.assertEqual(after_layout.layout, "cohort-v1")
        self.assertTrue(after_layout.memory_path.endswith(".claude/MEMORY.md"))
        self.assertEqual(len(after_layout.skill_homes), 2)

    def test_windows_onedrive_root_with_spaces(self) -> None:
        desktop = self.temp_dir / "Sarah Johnson" / "OneDrive" / "Desktop"
        root = workspace_layout.resolve_os_root(
            platform="windows",
            home=self.temp_dir / "Sarah Johnson",
            desktop=desktop,
        )
        self.make_fixture("root-v3", root)
        layout = workspace_layout.resolve_layout(root)

        self.assertEqual(layout.layout, "root-v3")
        self.assertIn("Sarah Johnson", layout.os_root)
        self.assertIn("OneDrive", layout.os_root)
        self.assertTrue(layout.progress_path.endswith(".claude/.ai-os-progress.json"))

    def test_custom_active_os_wins_over_desktop_default(self) -> None:
        desktop = self.temp_dir / "Desktop"
        default_root = self.make_fixture("root-v3", desktop / "OS")
        custom_root = self.make_fixture("root-v3", self.temp_dir / "Documents" / "OS")

        resolved = workspace_layout.resolve_existing_os_root(
            platform="macos",
            active_workspace=custom_root,
            home=self.temp_dir,
            desktop=desktop,
        )

        self.assertEqual(resolved, custom_root.resolve())
        self.assertNotEqual(resolved, default_root.resolve())

    def test_existing_root_checks_only_active_then_desktop_default(self) -> None:
        desktop = self.temp_dir / "Desktop"
        default_root = self.make_fixture("root-v3", desktop / "OS")
        unrelated = self.temp_dir / "Documents" / "Not An OS"
        unrelated.mkdir(parents=True)

        resolved = workspace_layout.resolve_existing_os_root(
            platform="macos",
            active_workspace=unrelated,
            home=self.temp_dir,
            desktop=desktop,
        )

        self.assertEqual(resolved, default_root.resolve())

    def test_active_workspace_stops_when_recorded_os_root_disagrees(self) -> None:
        desktop = self.temp_dir / "Desktop"
        active = self.make_fixture("root-v3", self.temp_dir / "Documents" / "OS")
        progress = active / ".claude" / ".ai-os-progress.json"
        progress.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "student": {"os_root": str(desktop / "OS")},
                }
            ),
            encoding="utf-8",
        )

        with self.assertRaises(workspace_layout.UnsafeLayoutError):
            workspace_layout.resolve_existing_os_root(
                platform="macos",
                active_workspace=active,
                home=self.temp_dir,
                desktop=desktop,
            )

    def test_mixed_substantive_masters_stop_before_writes(self) -> None:
        root = self.make_fixture("mixed")
        before = {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }
        layout = workspace_layout.resolve_layout(root)

        self.assertEqual(layout.layout, "mixed")
        self.assertFalse(layout.writes_allowed)
        with self.assertRaises(workspace_layout.UnsafeLayoutError):
            workspace_layout.require_writable(layout)
        after = {
            path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }
        self.assertEqual(before, after)

    def test_substantive_agents_and_claude_masters_are_mixed(self) -> None:
        root = self.temp_dir / "OS"
        root.mkdir()
        (root / "AGENTS.md").write_text(
            "# Canonical\n\nDurable cross-harness instructions.\n", encoding="utf-8"
        )
        (root / "CLAUDE.md").write_text(
            "# Competing\n\nDifferent durable Claude instructions.\n", encoding="utf-8"
        )

        layout = workspace_layout.resolve_layout(root)

        self.assertEqual(layout.layout, "mixed")
        self.assertFalse(layout.writes_allowed)

    def test_routing_only_master_does_not_create_false_mixed_state(self) -> None:
        root = self.make_fixture("cohort-v1-after")
        (root / "CLAUDE.md").write_text(
            "# Signpost\n\nRead `.claude/CLAUDE.md`.\n", encoding="utf-8"
        )
        layout = workspace_layout.resolve_layout(root)
        self.assertEqual(layout.layout, "cohort-v1")


if __name__ == "__main__":
    unittest.main()
