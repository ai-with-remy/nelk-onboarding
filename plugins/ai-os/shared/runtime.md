# Host Runtime Contract

Every `ai-os` skill supports both **Claude Code** and **Codex**. Resolve the
active host, the running skill directory, and the plugin root before reading
any other bundled file or touching the student's workspace.

## 0. Bootstrap before this file can be read

Every bundled `SKILL.md` carries the following minimal bootstrap. It must run
before the skill tries to read `runtime.md`:

1. Identify `HOST_RUNTIME` from the active session's host metadata. Do not infer
   it from installed executables.
2. Resolve the running skill location using the active host's native source:
   - **Claude Code:** when `${CLAUDE_SKILL_DIR}` is available, treat it as the
     absolute directory containing the active `SKILL.md` and verify that file
     exists. If it is absent, use the active skill path supplied by Claude's
     skill/plugin metadata when available.
   - **Codex:** use the absolute `SKILL.md` path supplied by the installed
     plugin catalogue, then take its parent directory.
3. Starting at that skill directory, walk upward to the first directory that
   contains `skills/`, `shared/runtime.md`, and `shared/workspace-layout.md`.
   Store it as `PLUGIN_ROOT`.
4. Verify the active `SKILL.md`,
   `<PLUGIN_ROOT>/shared/interaction-contract.md`, and
   `<PLUGIN_ROOT>/shared/workspace-layout.md`, then read this file.

`${CLAUDE_SKILL_DIR}` is Claude's preferred direct bootstrap, not a hard
cross-host dependency. Codex must never require it, and Claude must retain the
metadata/cache fallbacks below.

## 1. Resolve host configuration roots and cache fallbacks

Set these roots before any fallback search or global Claude/Codex path:

- **Claude Code, macOS/Linux:**
  `CLAUDE_HOME = ${CLAUDE_CONFIG_DIR:-$HOME/.claude}`.
- **Claude Code, Windows:** use `%CLAUDE_CONFIG_DIR%` when it is non-empty;
  otherwise use `%USERPROFILE%\.claude`.
- **Codex, macOS/Linux:** `CODEX_HOME = ${CODEX_HOME:-$HOME/.codex}`.
- **Codex, Windows:** use `%CODEX_HOME%` when non-empty; otherwise use
  `%USERPROFILE%\.codex`.

`CLAUDE_HOME` is the source of truth for Claude's user settings, global
guidance, global skills, plugin registry, and plugin cache. Never replace it
with a literal `~/.claude` or `%USERPROFILE%\.claude` later in a skill.

If the direct skill path cannot be verified, search **only the active host's**
plugin cache for an `ai-os` copy containing the active skill and
`shared/runtime.md`:

| Host | macOS / Linux cache | Windows cache |
|---|---|---|
| Claude Code | `<CLAUDE_HOME>/plugins/cache/` | `<CLAUDE_HOME>\plugins\cache\` |
| Codex | `<CODEX_HOME>/plugins/cache/` | `<CODEX_HOME>\plugins\cache\` |

Match the active skill name plus the enabled `ai-os` marketplace/plugin
identity. If several cached versions exist, use active plugin metadata to pick
the loaded version; do not guess by modification time. Verify the neighbouring
manifest, active `SKILL.md`, and `shared/runtime.md` before continuing. Never
silently fall across to the other host's cache.

Never show the student an unresolved placeholder such as `<PLUGIN_ROOT>`. If
the root still cannot be verified, explain that the
plugin copy is incomplete and ask them to reinstall the plugin, or ask Remy
or Mav for help.

All bundled paths elsewhere in this plugin are relative to `PLUGIN_ROOT`, for
example `<PLUGIN_ROOT>/shared/platform.md`.

## 2. Confirm the host independently from the operating system

Store one of:

- `HOST_RUNTIME = claude` when the active host identifies itself as Claude
  Code (or exposes Claude's plugin runtime metadata).
- `HOST_RUNTIME = codex` when the active host identifies itself as Codex (or
  exposes Codex host metadata / `CODEX_HOME`).

Use the active session's metadata and capabilities first. Do not decide merely
because a `claude` or `codex` executable happens to be installed; students may
have both. Ask “Are you using Claude Code or Codex right now?” only if the host
is genuinely ambiguous after the direct bootstrap and active-host cache checks.

Platform detection is separate: `DETECTED_OS` is `macos` or `windows`. A skill
therefore carries both values, such as `HOST_RUNTIME=codex` and
`DETECTED_OS=windows`.

## 3. Capability-neutral operations

Hosts expose different tool names. State the outcome, then use the available
capability:

- **Read a file:** use the host's file-reading capability; fall back to the
  platform shell only when needed.
- **Create or edit a file:** use the host's safe file-editing capability; write
  the complete intended content and preserve unrelated existing content.
- **Ask a choice:** use an interactive choice control when the host offers one;
  otherwise ask one plain-language question and wait.
- **Search files:** use the host's fast file-search capability; fall back to
  `rg` / `find` (macOS) or `Get-ChildItem` (Windows).
- **Browse a public page:** use the host's web-browsing capability. If it is not
  available, skip the optional lookup without treating that as a failure.

Never require a capability by a host-specific display name.

## 4. Canonical student workspace and signposts

Read `<PLUGIN_ROOT>/shared/workspace-layout.md` after platform detection. It is
the sole source of truth for supported workspace shapes, substantive-file
detection, mixed-master safety, and the resolved variables `MASTER_PATH`,
`MEMORY_PATH`, `ROOT_SIGNPOST`, `CONTEXT_DIR`, `SKILL_HOMES`, `SKILL_COMPAT_PATH`,
`PROGRESS_PATH`, `BACKUP_ROOT`, `CHIME_ROOT`, and `PROJECT_SETTINGS`.

`platform.md` resolves the OS root before this layout contract runs. The real
Desktop supplies the default, not a mandatory location. `build-os` may use an
approved custom path; later skills prefer a supported active workspace,
cross-check its stored `student.os_root`, then check only the Desktop default.
If neither is valid, ask the student to open their chosen OS folder. Never
broadly search the machine for it.

The default `root-v3` layout keeps the full cross-harness master at root
`AGENTS.md` with no root `CLAUDE.md`, memory at root `MEMORY.md`, one canonical
`.agents/skills/` tree, and a `.claude/skills` directory link to that same
tree. Legacy `root-v2` remains supported
with its substantive root `CLAUDE.md` and single `.claude/skills/` home. The
original `cohort-v1` layout also remains supported with a
substantive `.claude/CLAUDE.md`, `.claude/LESSONS.md` or upgraded
`.claude/MEMORY.md`, and two real skill homes. Do not repeat those compatibility
rules in individual skills.

Root-v3 needs no Claude loader: Claude Code (v2.1.277 or later) reads
`AGENTS.md` automatically when no `CLAUDE.md`, `.claude/CLAUDE.md`, or
`CLAUDE.local.md` exists in the workspace or a parent folder, and Codex reads it
natively. An older root-v3 OS may still have a routing-only `CLAUDE.md`
containing `@AGENTS.md`; it stays healthy and is never removed without
approval.

Every writing flow resolves the layout first and stops before writes when more
than one possible master is substantive. Compatibility loaders and signposts
contain routing only. Never create a root-v3 `CLAUDE.md` or duplicate the
master into one, and never use a filesystem link for root-v3 `AGENTS.md`. The
sole course-created link is the skills compatibility path described below:
`.claude/skills` points to canonical `.agents/skills`.

## 5. Skill locations and invocation

Workspace skill destinations come only from the resolved `SKILL_HOMES` array:

- `root-v3`: one complete physical tree in `.agents/skills/`; resolved
  `SKILL_COMPAT_PATH` is a Claude-facing directory link to that same tree;
- `root-v2`: one complete copy in `.claude/skills/`;
- `cohort-v1`: complete matching copies in `.claude/skills/` and
  `.agents/skills/`.

For root-v3, write only to the canonical home and verify the same file through
`SKILL_COMPAT_PATH`. The link is expected; copied fallback content is invalid.
Never create a second home for root-v2 or collapse cohort-v1's historical
dual-home layout. Global skill homes outside an OS remain host-specific.

For global skills outside a student OS, Claude's directory is
`<CLAUDE_HOME>/skills/` and Codex's directory is `<CODEX_HOME>/skills/`.

Invocation wording is runtime-specific:

| Action | Claude Code | Codex |
|---|---|---|
| Run a course skill | `/ai-os:<name>` | `$ai-os:<name>`; alternatively use `/skills` and select `ai-os:<name>` |
| Browse plugins | `/plugin` or Claude plugin commands | `/plugins` in CLI; **Settings → Plugins** in the IDE/app |
| Build a skill | Claude's built-in skill creator | `$skill-creator` |
| Schedule work | Claude's `/schedule` where available | **Scheduled tasks / Automations** where available; otherwise keep a manual run prompt |

When narrating a cross-runtime command, render only the active host's form.
Unnamespaced Claude aliases are legacy conveniences, not a guaranteed
interface; do not teach or depend on them. A slash command is not a portable
synonym for a Codex skill.

## 6. Plugin setup, updates, and recovery

Keep host configuration separate:

- Claude Code uses `<CLAUDE_HOME>/settings.json`,
  `<CLAUDE_HOME>/CLAUDE.md`, `<CLAUDE_HOME>/skills/`, Claude marketplace
  settings, and Claude plugin commands.
- Codex uses its plugin marketplace and plugin browser. Register a GitHub
  marketplace with `codex plugin marketplace add ai-with-remy/nelk-onboarding`, then use
  `/plugins` (CLI) or **Settings → Plugins** (IDE/app) to install or enable the
  bundles. Start a new Codex session/chat after install or enablement.

Never write Claude's `extraKnownMarketplaces` or `enabledPlugins` keys while
running in Codex, and never edit `~/.codex/config.toml` by guessing an
undocumented plugin shape. Preserve unrelated user configuration byte-for-byte.

## 7. Connections and MCP

- Claude Code: retain the live `/mcp`, `claude mcp ...`, and claude.ai
  Connectors paths documented in the `connect` skill.
- Codex: inspect installed plugin tools first. Use `/plugins` or
  **Settings → Plugins** for connector plugins and browser sign-in. Inspect
  direct servers with `codex mcp list`; add a direct HTTP server with
  `codex mcp add <name> --url <url>` only when a bundled or connector-plugin
  route is unavailable. Start a new session if newly installed tools are not
  visible yet.

Never tell a Codex student to use `/mcp`, `claude mcp`, or claude.ai Settings.
Never promise that a connector exists: inspect the live host, explain what is
actually available, and use a read-only verification after authentication.

## 8. Notification sounds

The bundled chime setup in this course is proven only for Claude Code's project
hooks. Install and promise it only when `HOST_RUNTIME=claude`.

When `HOST_RUNTIME=codex`, skip chime files and Claude hook configuration. Say
one accurate line during the build: “I’m leaving the Claude-only chimes off in
Codex, so I won’t promise notifications your current setup can’t deliver.” Do
not write `.claude/settings.json` merely for sounds, and do not invent Codex
hook event names or matchers.
