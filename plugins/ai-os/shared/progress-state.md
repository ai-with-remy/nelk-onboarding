# Progress State Contract

Resolve `PLUGIN_ROOT` and `HOST_RUNTIME` from
`<PLUGIN_ROOT>/shared/runtime.md`, then resolve `PROGRESS_PATH` from
`<PLUGIN_ROOT>/shared/workspace-layout.md`. This file defines the shared
host-neutral progress state. Both supported layouts currently resolve progress
to `.claude/.ai-os-progress.json`; skills still use the variable, never the
literal path.

---

## Where the Progress File Lives

The progress file belongs inside the student's own OS folder — not inside the plugin directory. The plugin directory is read-only and gets replaced on update. The student's OS folder is permanent.

**Location:**

```
<OS root>/.claude/.ai-os-progress.json
```

Resolved paths:

| Platform | Full path |
|---|---|
| macOS | `/Users/<name>/Desktop/OS/.claude/.ai-os-progress.json` |
| Windows (OneDrive Desktop) | `C:\Users\<name>\OneDrive\Desktop\OS\.claude\.ai-os-progress.json` |
| Windows (plain Desktop) | `C:\Users\<name>\Desktop\OS\.claude\.ai-os-progress.json` |
| Custom location | `<student-approved absolute OS path>/.claude/.ai-os-progress.json` |

The `.claude/` folder is created by `/ai-os:build-os` as part of the OS spine. The progress file lives inside it so it's protected from casual browsing but still easy to find if something needs to be reset.

---

## Schema

The file is a single JSON object. Fields are documented below with their types and meanings.

```json
{
  "schema_version": 1,
  "student": {
    "name": "Sarah",
    "platform": "macos",
    "os_root": "/Users/sarah/Desktop/OS",
    "timezone": "Europe/Paris"
  },
  "sessions": {
    "onboard": {
      "status": "complete",
      "completed_at": "2026-07-13T14:32:00Z",
      "next_skill": "build-context",
      "sounds": "on"
    },
    "context": {
      "status": "in_progress",
      "started_at": "2026-07-15T10:05:00Z",
      "resume_state": {
        "phase": "core_six",
        "current_file": "voice-dna",
        "completed_files": ["business", "about-me"],
        "answers_captured": {
          "business_model": "1:1 coaching and group programs",
          "offers": "6-week group program at $2,800, 1:1 at $500/hr"
        }
      }
    },
    "connect": {
      "status": "not_started"
    }
  },
  "last_updated": "2026-07-15T10:22:00Z"
}
```

### Field reference

**`schema_version`** — integer. Increment if the schema changes. Skills check this and handle older versions gracefully.

**`student`** — global facts captured during `/ai-os:build-os` that every other skill reuses. Never ask for these again once captured.
- `name` — their first name (used for personalizing messages)
- `platform` — `"macos"` or `"windows"` (detected, not asked)
- `os_root` — the resolved absolute path to their OS folder (platform-specific)
- `timezone` — IANA timezone string (e.g. `"America/New_York"`) — captured in onboard Phase 2D and used later by the active host's scheduling surface. Never infer it.

**`sessions`** — one entry per guided course skill. The legacy internal keys
`onboard`, `context`, and `connect` remain stable even though the public first
two skills are now `build-os` and `build-context`. This preserves completed and
in-progress work from earlier plugin versions. Never migrate, duplicate, or
rename those keys merely to match the public commands.

Each session entry:
- `status` — `"not_started"` | `"in_progress"` | `"complete"`
- `started_at` — ISO 8601 timestamp when the session began (set on first meaningful interaction)
- `completed_at` — ISO 8601 timestamp when the session finished (set at wrap-up)
- `next_skill` — (on complete sessions only) the skill name to suggest next
- `resume_state` — (on in_progress sessions only) the per-skill state object (see below)

**`sessions.onboard.sounds`** — (`build-os` only) `"on"` | `"declined"` |
`"removed"` | `"unsupported"`. For Claude Code, `"on"` means the student
explicitly opted in and the tagged AI OS project-hook entries were installed;
`"declined"` means the student explicitly said no and no hook or sound change
was made; `"removed"` means previously installed tagged AI OS entries were
later removed without disturbing unrelated hooks. For Codex, set
`"unsupported"`: do not install Claude hooks or promise sounds. An absent value
means the choice has not been asked yet or comes from an older workspace. This
is durable session state, not part of `resume_state`.

**`sessions.onboard.plugins_enabled`** — (`build-os` only) Boolean retained for
compatibility with older completed students. It is not sufficient proof of the
current plugin set because earlier versions used it for retired bundles.

**`sessions.onboard.plugin_bundle_version`** — not used by this onboarding plugin.

**`sessions.context.import`** — (context only) records the optional "fold in old ChatGPT/Claude context" top-up offered at the very END of `/ai-os:build-context`, after the OS is already complete and verified. The small status object is stored in the local progress file; the surrounding conversation is still processed under the active AI provider's account and retention terms. It lets Remy see, per student, whether the feature earns its place. Shape: `{ offered, used, promoted, rejected, contradictions }`.
- `offered` — `true` once the bonus is offered (always, since the phase is reached).
- `used` — `true` only if the student actually did the top-up; `false` if they skipped the offer (the expected default path).
- `promoted` — integer count of items the student confirmed in the present tense and that were written into the real context files.
- `rejected` — integer count of items dropped (stale/junk + contradicted-then-corrected + declined adds).
- `contradictions` — integer count of pasted items that conflicted with what the student told the interview.
Like `sounds`, this is a *durable* session field, not part of `resume_state`. Absent = the top-up phase wasn't reached (e.g. an older run, or a session that ended before wrap-up).

**`last_updated`** — ISO 8601 timestamp. Updated every time the file is written.

### Per-skill resume state

The `resume_state` object is different for each skill because the resume point is different. Each skill defines what it needs to save. At minimum:

- `phase` — which major phase the student was in when they stopped
- The answers captured so far (so questions already answered don't get asked again)
- Any other state needed to continue without confusion

Examples:

```json
// build-os resume state (stored under sessions.onboard)
"resume_state": {
  "phase": "interview",
  "interview_section": "B",
  "current_question": "Q6",
  "answers": {
    "name": "Sarah",
    "role": "Business coach",
    "business_one_liner": "I help women leave corporate and start their own practice",
    "tech_level": "beginner"
  },
  "platform_detected": "macos",
  "os_root_confirmed": "/Users/sarah/Desktop/OS",
  "tree_proposed": false
}

// build-context resume state (stored under sessions.context)
"resume_state": {
  "phase": "core_six",
  "current_file": "voice-dna",
  "completed_files": ["business", "about-me"],
  "answers_captured": {
    "business_model": "1:1 coaching and group programs"
  }
}

// connect resume state
"resume_state": {
  "phase": "connecting",
  "inventory": ["email", "calendar", "drive"],
  "connected_so_far": ["email"],
  "current_tool": "calendar"
}
```

---

## The Contract Every Skill Follows

### On start

1. Read `PROGRESS_PATH` with the active host's file-reading capability.
2. If the file doesn't exist: create it with the default structure (all sessions `"not_started"`, no `student` facts yet). Write it immediately.
3. Check: is this skill already `"complete"`? If yes, tell the student: "Looks like you've already done this session. Want to run it again, or jump to [next skill]?"
4. Check: is this skill `"in_progress"` with a `resume_state`? If yes, offer to resume: "Looks like we got partway through this last time — we were on [phase / question]. Want to pick up from there, or start fresh?" Wait for their answer. If resume: restore from the saved state and continue. If fresh: clear the resume state and start from the beginning.
5. Check: what's been done so far? Use the `sessions` map to know what's already complete, what to suggest at the end.

### During the skill

Update the progress file at every meaningful checkpoint — not after every question, but at natural pause points (end of a phase, a file written, a section completed). The write should happen before moving to the next phase, not after.

Use the active host's safe file-editing capability to update the file. Always write the complete JSON object, not a partial fragment, and verify that it parses afterward.

### On completion

1. Set `status: "complete"` and `completed_at` for this session.
2. Remove the `resume_state` (no longer needed).
3. Set `next_skill` to the name of the skill the student should run next (see session chain below).
4. Write the updated file.
5. Then deliver the wrap-up message that points to the next skill.

### Reading and writing without the tools

If file capabilities are unavailable, use the detected platform's shell. Never require a capability by a host-specific display name.

```zsh
# macOS — read
cat "/Users/sarah/Desktop/OS/.claude/.ai-os-progress.json"

# macOS — write (pipe a variable containing JSON)
echo "$PROGRESS_JSON" > "/Users/sarah/Desktop/OS/.claude/.ai-os-progress.json"
```

```powershell
# Windows — read
Get-Content "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\.claude\.ai-os-progress.json"

# Windows — write
$progressJson | Set-Content "C:\Users\Sarah Johnson\OneDrive\Desktop\OS\.claude\.ai-os-progress.json"
```

Paths must use the resolved `PROGRESS_PATH`, cross-checked against the
`student.os_root` value, not hardcoded values.

---

## The Session Chain

Skills end by pointing to the next one. This is how a student who runs
`/ai-os:build-os` on Monday knows to run `/ai-os:build-context` after the next call.

| Internal session key | Public skill | Next skill to suggest |
|---|---|---|
| onboard | build-os | build-context |
| context | build-context | connect |
| connect | connect | none |

`connect` is the Tools module's guided skill. Later course modules teach
repeatable Skills and Autopilot using the active host's supported creation and
scheduling surfaces. There is no additional ai-os homework skill to point to
yet, so `connect` sets `next_skill = null`.

**Wrap-up language** (adapt per skill, keep the same structure):

> "Your OS foundation is built. The Context module gives it a deeper brain: we'll fill in the starting files properly without making you repeat what you already told me. When you're ready, run [the active host's build-context skill mention]."

Render cross-references from `runtime.md`: Claude Code uses the canonical
`/ai-os:<name>` form; Codex uses the verified `$ai-os:<name>` namespace or
`/skills` to select `ai-os:<name>`. Never give both host syntaxes in the same
student-facing instruction.

---

## Example: Full Progress File After the Context Module

```json
{
  "schema_version": 1,
  "student": {
    "name": "Marcus",
    "platform": "windows",
    "os_root": "C:\\Users\\Marcus Webb\\OneDrive\\Desktop\\OS",
    "timezone": "America/Chicago"
  },
  "sessions": {
    "onboard": {
      "status": "complete",
      "started_at": "2026-07-13T19:15:00Z",
      "completed_at": "2026-07-13T19:47:00Z",
      "next_skill": "build-context"
    },
    "context": {
      "status": "complete",
      "started_at": "2026-07-15T20:00:00Z",
      "completed_at": "2026-07-15T21:10:00Z",
      "next_skill": "connect",
      "import": {
        "offered": true,
        "used": true,
        "promoted": 2,
        "rejected": 5,
        "contradictions": 1
      }
    },
    "connect": {
      "status": "not_started"
    }
  },
  "last_updated": "2026-07-15T21:10:00Z"
}
```

---

## A Note on the File's Purpose

This file exists because earlier versions of the build had no persistence. A
student who got interrupted had to start over. For a 15–20 minute setup, that
is a real frustration, especially while their workspace is still being
created.

The progress file is intentionally lightweight. It stores only enough to know
where the student is and what has already been captured. The real durable state
lives at resolved `MASTER_PATH`, `MEMORY_PATH`, and in the context files. This
file is just the bookmark.
