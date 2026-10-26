# Workspace Layout Contract

This is the only compatibility contract for student workspace paths. Any AI OS
skill that reads or writes a student workspace must resolve this contract after
`runtime.md` and `platform.md`, then use the resolved variables below. Skills
must not repeat layout detection or hard-code master, memory, skill, progress,
or backup paths.

The bundled `workspace_layout.py` implements the same rules for deterministic
checks and tests. A host without Python applies this document directly with its
normal file-reading capability.

## Substantive-file test

A file is **substantive** when it contains durable user instructions or memory,
not just a heading, an import, or routing text that tells an agent to read
another file. Inspect contents; existence alone is not enough.

Before any write, classify all possible masters:

- `<OS_ROOT>/AGENTS.md`
- `<OS_ROOT>/CLAUDE.md`
- `<OS_ROOT>/.claude/CLAUDE.md`

If more than one is substantive, return `LAYOUT=mixed` and **stop before every
write**. Explain that competing employee handbooks exist and ask Remy or Mav
to sort it out with them. Never pick a winner, merge, rename, or create a backup.

If neither is substantive, return `LAYOUT=uninitialized`. Only onboarding may
create a layout, and onboarding requires a brand-new target.

## Supported shape: `root-v3` (default)

Detected when root `AGENTS.md` is substantive while root `CLAUDE.md` and
`.claude/CLAUDE.md` are absent or routing-only.

| Variable | Resolved path |
|---|---|
| `MASTER_PATH` | `<OS_ROOT>/AGENTS.md` |
| `MEMORY_PATH` | `<OS_ROOT>/MEMORY.md` |
| `ROOT_SIGNPOST` | none |
| `CONTEXT_DIR` | `<OS_ROOT>/context` |
| `SKILL_HOMES` | [`<OS_ROOT>/.agents/skills`] |
| `SKILL_COMPAT_PATH` | `<OS_ROOT>/.claude/skills` |
| `PROGRESS_PATH` | `<OS_ROOT>/.claude/.ai-os-progress.json` |
| `BACKUP_ROOT` | `<OS_ROOT>/.claude/backups/ai-os` |
| `CHIME_ROOT` | `<OS_ROOT>/.claude/sounds` |
| `PROJECT_SETTINGS` | `<OS_ROOT>/.claude/settings.json` |

Normal root-v3 health:

- root `AGENTS.md` is the only substantive master, is a regular file, and uses
  conditional, cross-harness source-map instructions;
- root `CLAUDE.md` is absent (new builds) or routing-only, such as the exact
  `@AGENTS.md` loader that earlier builds created;
- root `MEMORY.md` exists and uses the conservative approval policy;
- `.agents/skills/` is the one canonical physical skill home;
- `.claude/skills` is a directory link to `../.agents/skills` so Claude Code
  discovers that same physical tree;
- macOS/Linux use a relative filesystem symlink; Windows uses a directory
  junction;
- progress, chimes, project settings, and AI OS backups stay inside `.claude/`;
- business and client folders do not require nested guidance files.

### Root-v3 compatibility mechanisms — keep them separate

Root-v3 uses two different compatibility mechanisms because the hosts expose
two different capabilities:

1. **Instructions:** `AGENTS.md` is the one instructions file. Codex reads it
   directly, and Claude Code (v2.1.277 or later) reads it automatically when
   no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the OS
   folder or a parent folder. New builds create no root `CLAUDE.md`. This is
   the same on macOS, Windows, and Linux. Never make `AGENTS.md` a symlink,
   hard link, junction, or copied mirror.
2. **Skills:** `.agents/skills/` is the one physical tree. Claude Code does
   not discover skills there on its own, so `.claude/skills` points to it with a relative directory symlink on macOS/Linux or a directory
   junction on Windows.

Do not infer that the operating-system-specific skills-link rule also applies
to `AGENTS.md`. The instructions architecture is identical on every
supported operating system.

`ROOT_SIGNPOST` is none for root-v3: no skill creates, repairs, or writes a
root `CLAUDE.md`. Earlier builds created a real one-line `CLAUDE.md` containing
`@AGENTS.md`. That routing-only loader is still healthy root-v3: never flag it,
never auto-delete it, and never add content to it. A substantive root
`CLAUDE.md` alongside the substantive `AGENTS.md` is `mixed`. Writing skills
write durable instructions only to `MASTER_PATH`.

Do not link the whole `.claude` folder to `.agents`: those folders have
different host-specific responsibilities. Only `.claude/skills` points to the
canonical `.agents/skills` tree. Never create a copied fallback. Every build,
install, audit, and update must verify the link resolves to the canonical tree;
if the chosen filesystem cannot create that link, stop and offer a different OS
location rather than creating duplicate skills.

## Supported shape: `root-v2` (legacy)

Detected when root `CLAUDE.md` is substantive and `.claude/CLAUDE.md` is absent
or routing-only.

| Variable | Resolved path |
|---|---|
| `MASTER_PATH` | `<OS_ROOT>/CLAUDE.md` |
| `MEMORY_PATH` | `<OS_ROOT>/MEMORY.md` |
| `ROOT_SIGNPOST` | `<OS_ROOT>/AGENTS.md` |
| `CONTEXT_DIR` | `<OS_ROOT>/context` |
| `SKILL_HOMES` | [`<OS_ROOT>/.claude/skills`] |
| `SKILL_COMPAT_PATH` | none |
| `PROGRESS_PATH` | `<OS_ROOT>/.claude/.ai-os-progress.json` |
| `BACKUP_ROOT` | `<OS_ROOT>/.claude/backups/ai-os` |
| `CHIME_ROOT` | `<OS_ROOT>/.claude/sounds` |
| `PROJECT_SETTINGS` | `<OS_ROOT>/.claude/settings.json` |

Normal root-v2 health:

- root `CLAUDE.md` is the only substantive master;
- root `MEMORY.md` exists and uses the conservative approval policy;
- root `AGENTS.md` is a short signpost to `CLAUDE.md`, `MEMORY.md`, and
  `context/`;
- `.claude/skills/` is one real directory tree, never a symlink;
- progress, chimes, project settings, and AI OS backups stay inside `.claude/`;
- business and client folders do not require nested guidance files;
- `active/`, `.archive/`, `.agents/`, and per-folder guidance are not part of
  this shape.

## Supported shape: `cohort-v1`

Detected when `.claude/CLAUDE.md` is substantive and root `CLAUDE.md` is absent
or routing-only.

| Variable | Resolved path |
|---|---|
| `MASTER_PATH` | `<OS_ROOT>/.claude/CLAUDE.md` |
| `MEMORY_PATH` | substantive `<OS_ROOT>/.claude/MEMORY.md`, otherwise `<OS_ROOT>/.claude/LESSONS.md` |
| `ROOT_SIGNPOST` | `<OS_ROOT>/AGENTS.md` |
| `CONTEXT_DIR` | `<OS_ROOT>/context` |
| `SKILL_HOMES` | [`<OS_ROOT>/.claude/skills`, `<OS_ROOT>/.agents/skills`] |
| `SKILL_COMPAT_PATH` | none |
| `PROGRESS_PATH` | `<OS_ROOT>/.claude/.ai-os-progress.json` |
| `BACKUP_ROOT` | `<OS_ROOT>/.archive/ai-os-maintenance` |
| `CHIME_ROOT` | `<OS_ROOT>/.claude/sounds` |
| `PROJECT_SETTINGS` | `<OS_ROOT>/.claude/settings.json` |

For cohort-v1, `active/`, `.archive/`, `.agents/`, two complete real skill
copies, and nested `CLAUDE.md`/`AGENTS.md` guidance are valid and must not be
flagged merely for existing. Symlinks are never valid.

An existing `.claude/LESSONS.md` is supported for reading, but Spring Clean
must raise a health finding when it or liberal “save every correction” rules
remain. Repair is always approval-gated: back up through `BACKUP_ROOT`, rename
to `.claude/MEMORY.md`, update imports/signposts, and replace liberal rules with
the conservative policy. Never blind-rewrite custom content.

## Resolved-write gate

Every writing skill must:

1. Resolve the layout from substantive files.
2. Stop on `mixed` or `uninitialized` unless it is the new-workspace `build-os` flow.
3. Use only `MASTER_PATH`, `MEMORY_PATH`, `ROOT_SIGNPOST`, `CONTEXT_DIR`,
   `SKILL_HOMES`, `SKILL_COMPAT_PATH`, `PROGRESS_PATH`, `BACKUP_ROOT`,
   `CHIME_ROOT`, and `PROJECT_SETTINGS`. A variable resolved to none (such as
   root-v3 `ROOT_SIGNPOST`) means there is no file to create or update.
4. Preview user-content changes and obtain any approval required by the skill.
5. Back up unfamiliar or replaced content through `BACKUP_ROOT`.
6. Verify the write and re-run mixed-master detection.

## Windows and OneDrive

`OS_ROOT` comes from `platform.md`; never reconstruct it here. It may be the
registry-resolved Desktop default or a student-approved custom location. Join
all resolved relative paths to that exact root and quote paths containing
spaces. Later skills prefer a valid active workspace, cross-check the stored
`student.os_root`, then check only the Desktop default. They never broadly
search the machine for a custom OS.
