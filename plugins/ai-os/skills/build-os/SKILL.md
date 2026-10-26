---
name: build-os
description: >-
  Module 2 of The AI Course for brand-new students. Runs a short guided setup
  and builds a root-v3 AI operating system on the real Desktop or a chosen
  location: canonical root AGENTS.md (the one instructions file Claude Code
  and Codex both read), MEMORY.md, six context files, bespoke business/client
  folders, one canonical .agents/skills tree plus a .claude/skills compatibility
  link, progress, and supported notification
  chimes. Use for "build my OS", "set up my OS", "start the course", or
  "module 2".
---

# Build OS — Create the Foundation

This skill is exclusively for a brand-new student workspace. It creates only
the current root-v3 layout. It never converts, repairs, merges, or reorganizes
another workspace.

## Bootstrap and contracts

Identify `HOST_RUNTIME` from session metadata. Resolve the running skill and
walk upward to the plugin root containing `skills/`, `shared/runtime.md`, and
`shared/workspace-layout.md`. If direct metadata is unavailable, search only
the active host's verified plugin cache. Read, in order:

1. `<PLUGIN_ROOT>/shared/runtime.md`
2. `<PLUGIN_ROOT>/shared/interaction-contract.md`
3. `<PLUGIN_ROOT>/shared/platform.md`
4. `<PLUGIN_ROOT>/shared/workspace-layout.md`
5. `<PLUGIN_ROOT>/shared/progress-state.md`
6. `<PLUGIN_ROOT>/shared/interview-bank.md`

Load `<PLUGIN_ROOT>/shared/templates.md`,
`<PLUGIN_ROOT>/skills/build-os/file-templates.md`, and
`<PLUGIN_ROOT>/shared/voice-dna-base.md` only when their phase needs them.

Resolve `DETECTED_OS`, `HOME_DIR`, and the real `DESKTOP` (Windows registry
first, including OneDrive). Store `DEFAULT_OS_ROOT=<DESKTOP>/OS`. Do not set
the final `OS_ROOT` until the student accepts that default or chooses a custom
location in Phase 1. The new layout paths are then:

- `MASTER_PATH=<OS_ROOT>/AGENTS.md`
- `MEMORY_PATH=<OS_ROOT>/MEMORY.md`
- `ROOT_SIGNPOST=none` (no root `CLAUDE.md` is created)
- `CONTEXT_DIR=<OS_ROOT>/context`
- `SKILL_HOMES=[<OS_ROOT>/.agents/skills]`
- `SKILL_COMPAT_PATH=<OS_ROOT>/.claude/skills`
- `PROGRESS_PATH=<OS_ROOT>/.claude/.ai-os-progress.json`
- `BACKUP_ROOT=<OS_ROOT>/.claude/backups/ai-os`
- `CHIME_ROOT=<OS_ROOT>/.claude/sounds`
- `PROJECT_SETTINGS=<OS_ROOT>/.claude/settings.json`

Never link the whole `.agents`/`.claude` folders, create a copied second skills
tree, create a scratch/active or archive area, or create instruction files
inside business/client folders. `.agents/skills` is the one physical tree;
`.claude/skills` is only its Claude-facing directory link.

Keep the two compatibility mechanisms distinct:

- **Instructions are platform-independent:** create one substantive real file
  at `AGENTS.md` and no root `CLAUDE.md`. Codex reads `AGENTS.md` directly, and
  Claude Code (v2.1.277 or later) reads it automatically when no Claude
  instruction file (`CLAUDE.md`, `CLAUDE.local.md`, or a `CLAUDE.md` inside
  `.claude/`) sits in the OS folder or a parent folder.
  Never symlink, junction, hard-link, or copy `AGENTS.md`, and never add a
  `CLAUDE.md` loader.
- **Skills are platform-specific:** only `.claude/skills` uses a relative
  directory symlink on macOS/Linux or a directory junction on Windows to expose
  the one physical `.agents/skills` tree.

## Hard gates

- Ask one question at a time, with concrete examples.
- Explain a tree or file before previewing it.
- Preview every file containing the student's words and wait for approval.
- Create, list, and verify. Never claim a file/folder exists from intent alone.
- Save progress after every phase.
- No inbox, Drive, private-app, or broad machine scan. A public website supplied
  by the student is the only optional lookup.
- Built files are timeless: no course, session, plugin, or setup references.
- Preserve unrelated settings byte-for-byte.
- The public skill is `build-os`, but its progress entry remains
  `sessions.onboard` for compatibility with students who completed an earlier
  plugin version. Never rename or discard that internal key.

### Created-path transaction rule

`sessions.onboard.created_paths` is the rollback ledger, not an end-of-phase
summary. Store workspace-relative paths, including directories. Immediately
after **every** successful creation—root file, context file, business/client
folder, `.claude` directory, sound, backup, settings file, or temporary
sibling other than the progress writer's own atomic temp—append that path and
atomically write/parse `PROGRESS_PATH` **before any other filesystem
mutation**. Never add a path that existed before this attempt. When an
attempt-owned temporary path is removed, remove it from the ledger immediately.
The progress writer must use one deterministic same-directory temp and always
replace or remove it within that write operation; exempting that internal temp
avoids a recursive ledger write.

Before modifying a pre-existing file, create and verify its backup, record
`{path, backup_path}` under `sessions.onboard.modified_paths`, and write/parse
progress before the modification. This lets “start fresh” restore the original
instead of deleting it.

## Phase 0 — Detect the safe default

Before greeting, detect the platform, home directory, and real Desktop. Store
the proposed default as `DEFAULT_OS_ROOT`. Do not create, scan, or inspect a
target yet. Do not broadly search the computer for an existing OS.

## Phase 1 — Welcome, choose the location, and start durable progress

Explain: the OS is one folder that works like a highly trained project space,
with business context, working preferences, and future tools in one place.
Frame the short interview as briefing a new hire. It normally takes 15–20
minutes, should take no more than about 25 minutes, and can resume after an
interruption.

Show the detected default path and ask one choice:

> "I recommend building your OS at `[DEFAULT_OS_ROOT]` so it is easy to find.
> We can use that, or put a folder named `OS` somewhere else such as Documents.
> Which would you prefer?"

- If they accept the default, set `OS_ROOT=DEFAULT_OS_ROOT`.
- For a custom location, ask them to choose the parent folder or give the exact
  intended `OS` path. Normalize it to one absolute folder named `OS`, confirm
  the exact path back to them, and set `OS_ROOT` only after they approve it.
- The custom parent must already exist. Never create or choose a broad parent
  on the student's behalf, and never use a broad disk search to find one.
- If the active workspace is already that exact path, treat it as the chosen
  target. Otherwise, tell the student they will open it as the active workspace
  after the build.

After the location is chosen, run the brand-new target gate:

1. If `PROGRESS_PATH` records `sessions.onboard.status="in_progress"`, offer to
   resume or discard only this incomplete build attempt. Resume from its
   captured answers and confirmed tree. For “start fresh,” show the exact
   rollback: restore each `modified_paths` entry from its verified backup, then
   remove existing `created_paths` entries deepest-first. Delete a directory
   only when it is empty after its listed children are removed; preserve every
   unlisted path. Wait for approval, execute, verify, then restart Phase 1.
2. If progress is absent and the only existing item under `OS_ROOT` is an empty
   `.claude/` directory, treat it as an interrupted zero-data bootstrap—not a
   used workspace—and continue Phase 1 by creating the initial ledger.
3. Otherwise inspect `OS_ROOT` shallowly. If it does not exist or is empty,
   continue.
4. If it contains any file or folder, make no writes. Say this build flow is
   for a new empty OS and suggest asking Remy or Mav for a safe health check. Do not
   inspect, classify, move, rename, or overwrite its contents.

Ask if they are ready to begin only after the target passes this gate.

On yes:

1. Create `<OS_ROOT>/.claude/`.
2. Verify `.claude` with `ls -A` on macOS or `Get-ChildItem -Force` on Windows.
3. Write `PROGRESS_PATH` immediately with schema version 1, detected platform
   and `os_root`, all sessions `not_started`, and onboard `in_progress` with
   `started_at`, `layout: "root-v3"`, `created_paths` initialized to
   `[".claude", ".claude/.ai-os-progress.json"]`, and empty
   `modified_paths`. This first write is the transaction bootstrap.
4. Parse the JSON after writing.

## Phase 2 — Short, pre-filled foundation interview

Use the `[SCOPE: onboard-surface]` questions from `interview-bank.md`, Sections
A → B → C → D, to collect the required outputs. Never run context-deep
questions. Keep the final foundation complete while removing repetition:

- First use facts the student has already supplied in this conversation or an
  optional public website. Propose those facts and ask for correction instead
  of asking the underlying question again.
- If one answer covers a later field, record it and skip that later question.
- Skip client, brand, team, pricing, or tool follow-ups that are plainly not
  relevant. Record a short honest empty state instead of forcing detail.
- Keep examples short and tailored. Do not read the entire generic example
  bank when two or three relevant examples will make the question clear.
- Accept concise answers. Depth belongs in `/ai-os:build-context`.

### A — The person

Capture name/role, business one-liner, day-to-day work, expertise headline, and
technical comfort. Offer the website shortcut before asking for the business
description. If supplied, read only the public page, propose the facts found,
and let the student correct them. A single confirmation may populate several
fields when the page is clear.

### B — The business

Capture model, a light offer/pricing list, customer sketch, team, and one to
three ranked durable priorities. Ask currency the first time money appears and
reuse it.

### C — The workspace shape

Capture only relevant business areas, named clients, and distinct
brands/businesses. Draw a
small live ASCII tree using their names as answers arrive, explaining that
these answers become folders. Infer one recommended business/client tree from
`shared/templates.md`; never show archetype names or a template menu.

Do not ask about code experience, scan for folders, or offer to bring another
folder into the new OS. This flow builds new folders from interview answers
only.

### D — How they work

Capture output format, global/scope-specific hard rules, durable rhythms,
timezone, and a `job → tool` inventory. If one rhythm answer naturally covers
daily and weekly work, store both without asking twice. Inventory tools only;
connect nothing. Give beginners compact concrete examples, especially for
output and hard rules.

After each section update `PROGRESS_PATH.resume_state` with phase, section,
question, captured answers, and any known student fields. Parse after writing.

## Phase 3 — Confirm the business/client tree

Explain the proposed tree before showing it. Start broad, nest subtopics under
their parent, use lowercase hyphenated folder names, and use real business and
client names. Every business gets its own root folder. Separate distinct
businesses; group named clients logically. Create only folders that have a real
purpose.

Show only business/client folders. Do not add technical settings folders to
this preview. Iterate until confirmed, then save the complete folder list to
the progress file as the Phase 4 verification checklist.

## Phase 4 — Build root-v3

### 4.1 Create and verify the spine

Create only:

```text
OS/
├── .agents/
│   └── skills/                 (canonical editable skills)
├── .claude/
│   ├── skills -> ../.agents/skills
│   ├── sounds/                 (Claude chimes only)
│   └── .ai-os-progress.json
├── AGENTS.md                    (the one instructions file)
├── MEMORY.md
├── context/
└── [confirmed business/client folders]
```

Create `.agents/skills`, `context`, and every confirmed business/client folder.
After each create, list its parent, verify it appears, then append that exact
relative path to `created_paths` and write/parse progress before creating the
next path. The canonical skill home must be a real directory. Business/client
folders contain no generated guidance files.

Then create `SKILL_COMPAT_PATH` as a directory link to the canonical skill home:

- macOS/Linux: create the relative symlink `.claude/skills -> ../.agents/skills`;
- Windows: create a PowerShell directory junction from `.claude\skills` to the
  absolute `.agents\skills` path.

Ledger the link path immediately. Create a unique temporary probe file inside
`.agents/skills`, ledger it, read the exact marker through `.claude/skills`,
then remove and unledger the probe. Verify both paths resolve to the same
physical tree. If link creation or readback fails, remove only the attempted
link/probe, preserve the canonical directory, and stop. Offer a different OS
location; never create a copied fallback.

### 4.2 Notification chimes inside `.claude`

For `HOST_RUNTIME=codex`, set `sessions.onboard.sounds="unsupported"` and skip
sound files/settings; do not promise unsupported hooks.

For `HOST_RUNTIME=claude`, explain the two workspace-only chimes. If the student
objects, set `"declined"` and continue. Otherwise:

1. If `PROJECT_SETTINGS` is absent, use `{}` as the in-memory base; do not
   require or try to back up a missing file. If it exists, parse it, back it up
   under `<BACKUP_ROOT>/build-os-chimes/<UTC timestamp>/settings.json`, verify
   identical bytes, record the new backup paths in `created_paths`, and record
   the source/backup pair in `modified_paths` before editing.
2. Require the base `hooks` value (when present) to be an object and existing
   `Stop`/`PreToolUse` values (when present) to be arrays. On any other shape,
   leave settings untouched and mark chimes skipped.
3. Create `CHIME_ROOT`, then copy `finish.mp3`, `finish.wav`, and
   `question.wav` from `<PLUGIN_ROOT>/assets/sounds/` one at a time. Verify and
   ledger each directory/file before the next copy.
4. Deep-merge the platform payload below. Preserve every unrelated top-level
   key, event wrapper, matcher, and nested hook in order. Replace only a nested
   command carrying the same `AI_OS_CHIME_ID`; otherwise append its wrapper.
5. Write through a ledgered temporary sibling, parse, verify exactly one finish
   and one question tag, then replace. If settings did not exist, ledger
   `.claude/settings.json` immediately after creation. Remove the temporary
   path from `created_paths` once gone. Roll back on failure.
6. Set `sounds="on"` and parse progress.

**macOS payload:**

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "AI_OS_CHIME_ID=finish afplay -v 1.2 \"$CLAUDE_PROJECT_DIR/.claude/sounds/finish.mp3\""
      }]
    }],
    "PreToolUse": [{
      "matcher": "AskUserQuestion",
      "hooks": [{
        "type": "command",
        "command": "AI_OS_CHIME_ID=question afplay -v 1.6 \"$CLAUDE_PROJECT_DIR/.claude/sounds/question.wav\"",
        "async": true
      }]
    }]
  }
}
```

**Windows payload:**

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "powershell -NoProfile -Command \"$env:AI_OS_CHIME_ID='finish'; $p = Join-Path $env:CLAUDE_PROJECT_DIR '.claude\\sounds\\finish.wav'; (New-Object Media.SoundPlayer $p).PlaySync()\""
      }]
    }],
    "PreToolUse": [{
      "matcher": "AskUserQuestion",
      "hooks": [{
        "type": "command",
        "command": "powershell -NoProfile -Command \"$env:AI_OS_CHIME_ID='question'; $p = Join-Path $env:CLAUDE_PROJECT_DIR '.claude\\sounds\\question.wav'; (New-Object Media.SoundPlayer $p).PlaySync()\"",
        "async": true
      }]
    }]
  }
}
```

These commands contain no credentials and resolve only project-local sound
files at hook runtime.

Removal later is surgical: remove only tagged nested hooks and the three known
sound files the student approves.

### 4.3 Preview and write the knowledge files

Use `file-templates.md`.

1. Explain and preview root `AGENTS.md`: the canonical cross-harness master with
   the interview profile, tools, working preferences, operating principles,
   execution standards, learning and memory policy, and conditional source map.
   Each source-map entry must state the trigger, the action to read, and the
   exact relative path. Do not put Claude-only `@context/...` imports in this
   file.
2. Explain and preview root `MEMORY.md`: a near-empty place for enduring
   learning that could change a future chat. Mention the approval gate once;
   do not teach or demonstrate a memory workflow in this module.
3. Explain and preview the six interview-filled context files:
   `about-me.md`, `business.md`, `offers.md`,
   `ideal-customer-profile.md`, `working-style.md`, and `voice-dna.md`.

Write only after approval. After creating each root/context file, verify it,
append its relative path to `created_paths`, and write/parse progress before
writing the next file. Then read each back. Verify that `AGENTS.md`:

- tells the agent to read `MEMORY.md` at the start of every task;
- routes workflow rules to Skills, durable facts to Context, scoped information
  to its project/client folder, broad operating preferences to Memory, and
  system-level changes to `AGENTS.md`;
- never duplicates the same instruction across files;
- saves to Memory only when the owner directly confirmed an enduring,
  cross-task operating preference with no more specific home, no duplicate or
  sensitive information, and approved the exact actionable line;
- treats failure to follow an existing instruction as an execution mistake, not
  a new memory;
- delegates substantial independent execution when subagents are available,
  while keeping decisions, integration, and accountability with the main agent;
- requires direct evidence before claiming completion; and
- keeps one physical reusable Skills collection at `.agents/skills/`.

After `AGENTS.md` exists, run the instructions verification before creating
another knowledge file:

1. Verify `AGENTS.md` is a regular, substantive file and not a filesystem link
   or Windows reparse-point link.
2. Verify the OS folder has no `CLAUDE.md`, no `CLAUDE.local.md`, and no
   `CLAUDE.md` inside `.claude/`. Any of them would stop Claude Code reading
   `AGENTS.md` automatically.

If either check fails, stop before claiming the foundation is complete. Repair
only attempt-created files under the transaction ledger, then repeat both
checks. Do not substitute an instruction symlink, junction, copy, or
`CLAUDE.md` loader.

### 4.4 Keep the plugin updating

The running `ai-os` plugin comes from the public `nelk-onboarding`
marketplace and is the only plugin this onboarding uses. Do not install
community, remote, or other first-party plugin bundles.

Skip this phase when `plugins_enabled=true` is already present and the check
below verifies on the active host.

**Claude (`HOST_RUNTIME=claude`):**

1. Read `<CLAUDE_HOME>/plugins/known_marketplaces.json` and copy the
   `nelk-onboarding` source object verbatim. If
   `<CLAUDE_HOME>/settings.json` already has that marketplace, its existing
   source wins.
2. Parse `<CLAUDE_HOME>/settings.json` (or use `{}` when absent) and safely
   merge only `extraKnownMarketplaces` plus `enabledPlugins`, preserving every
   unrelated key and existing entry:

```json
{
  "extraKnownMarketplaces": {
    "nelk-onboarding": {
      "source": "<COPY THE EXISTING SOURCE OBJECT VERBATIM>",
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "ai-os@nelk-onboarding": true
  }
}
```

If no source exists in either file, skip only `extraKnownMarketplaces`; still
merge the `enabledPlugins` entry. Write atomically, parse, and verify
`autoUpdate` remains true without losing unrelated settings.

**Codex (`HOST_RUNTIME=codex`):** run `codex plugin marketplace list` and
confirm `nelk-onboarding` is present. Never write Claude settings from Codex
and never guess plugin keys in `~/.codex/config.toml`.

After host-specific verification, set `plugins_enabled=true`, then parse
progress.

### 4.5 Full verification

Use one deep listing and check every confirmed path:

- root `AGENTS.md` and `MEMORY.md`, with no root `CLAUDE.md`;
- all six context files;
- `.agents/skills/` as the one physical tree and `.claude/skills` as its
  verified directory link;
- progress JSON;
- every business/client folder;
- supported chime state and files/settings when enabled.

Also verify the canonical skill home is a real directory, the compatibility
path is a link to that exact directory, and there is no copied second tree or
generated instruction file inside business/client folders.
Verify separately that root `AGENTS.md` is the only instructions file on every
operating system and that no `CLAUDE.md` was created. Do not describe the
skills directory link as also applying to `AGENTS.md`.
Compare every live attempt-created path
against `created_paths`; any created artifact missing from the ledger is a
failed transaction and must be repaired before claiming done. Repair and
re-list before claiming done.

## Phase 5 — Fresh-session proof and wrap

Show the exact absolute `OS_ROOT` and have the student confirm the folder and
verified tree exist there. Then explain that the real proof must happen in a
genuinely fresh session, because the current interview conversation already
knows their answers.

Give only the active host's reopen steps. The student must:

1. Open the exact `OS_ROOT` as the workspace.
2. Start a new session or chat.
3. Ask: **“What do you know about me and how should you work with me?”**

Tell them what success looks like: the answer identifies who they are or their
role, what their work or business involves, and at least two preferences or
operating rules recorded in the new files. It must not depend on the interview
chat. In both Claude and Codex it proves native `AGENTS.md` loading.
Do not add an artificial entry to `MEMORY.md` or create a `CLAUDE.md` to make
the proof work. If the Claude answer does not know them, check the Claude Code version
first (automatic `AGENTS.md` reading needs v2.1.277 or later), then look for a
Claude instruction file of those three kinds in a parent folder of `OS_ROOT`; report what you find and suggest asking Remy or Mav rather than moving it.

Recap: root `AGENTS.md` is the one cross-harness handbook that Claude Code and
Codex both read, root `MEMORY.md` is conservative approved memory, `context/` is the business brain, business/client folders hold work,
and `.agents/skills/` is the one physical skill tree that Claude reaches through
the `.claude/skills` link.

Teach the one habit: always open the AI in the OS folder. Give only the active
host's exact reopen recipe using the resolved path.

Mark the internal `sessions.onboard` entry complete, remove resume state, set
`next_skill="build-context"`, and verify required student fields. Mention the
next skill without pushing them to run it now:

- Claude: `/ai-os:build-context`
- Codex: `$ai-os:build-context` or choose `ai-os:build-context` from `/skills`

## Self-Improvement Loop

After each run, propose a one-line skill update only if it would change what a
future run does. Edit this `SKILL.md` only after explicit approval.
