---
name: connect
description: >-
  Connect ANY tool to the student's AI — both the
  Tools module of The AI Course ("the hands": connect email, calendar, docs/Drive, CRM
  and web tools department by department) AND the any-time way to connect one
  specific tool. Handles a bare tool name ("connect Airtable" — hunts the best
  route: the student's Composio hub FIRST whenever it's set up, then official
  vendor MCP, then community options), a pasted website or MCP URL (probed and
  wired up), a pasted GitHub repo (connector → connect it; skill → hand to the
  safe skill installer), and "what can I connect?" discovery. Every connection
  gets a safe read-only test and is recorded in context/working-style.md.
  Trigger on "tools module", "connect my tools/apps", "give my OS hands",
  "connect <app>", "connect the starter pack" (the recommended stack), a
  pasted MCP URL or GitHub repo to connect, "is there a connector/MCP for X",
  "what can I connect", or re-checking a connected app. Only for
  apps/tools/services — not connecting ideas or documents.
---

# /ai-os:connect — the hands (Tools module + connect any tool, any time)

**FIRST — bootstrap before reading shared files:** identify the active host from
session metadata. On Claude Code, set `CLAUDE_HOME` to
`${CLAUDE_CONFIG_DIR:-$HOME/.claude}` (Windows: non-empty
`%CLAUDE_CONFIG_DIR%`, otherwise `%USERPROFILE%\.claude`) and use the verified
`${CLAUDE_SKILL_DIR}` when available. On Codex, use the catalogue-provided
absolute path to this `SKILL.md` and resolve `CODEX_HOME`. If the direct path is
unavailable, search only the active host's `<CLAUDE_HOME>/plugins/cache/` or
`<CODEX_HOME>/plugins/cache/` for the enabled `ai-os` copy containing
`skills/connect/SKILL.md` and `shared/runtime.md`. Walk upward to the directory
containing `skills/` and `shared/runtime.md`, store it as `PLUGIN_ROOT`, verify
the active skill and neighbouring shared files, then read
`<PLUGIN_ROOT>/shared/runtime.md` followed by
`<PLUGIN_ROOT>/shared/interaction-contract.md`.

Then load these shared files (you'll use them throughout):
- `<PLUGIN_ROOT>/shared/platform.md` — host + OS detection and resolved paths.
- `<PLUGIN_ROOT>/shared/workspace-layout.md` — substantive layout detection and
  resolved master, memory, context, progress, and backup paths.
- `<PLUGIN_ROOT>/shared/progress-state.md` — resume and completion state.

This skill's own sibling reference files (same folder as this SKILL.md):
- `known-routes.md` — which door each app goes through (pinned routes, the
  Composio gateway, app-level vs machine-level doors, official vendor
  endpoints, add commands). Load it in EVERY mode.
- `guides/<tool>.md` — baked step-by-step recipes for the course's core
  stack (firecrawl, apify, perplexity, higgsfield, openrouter,
  chrome-devtools, playwriter, kie-ai, meta-ads) plus the aggregator hubs
  (composio, zapier) and the shared `guides/node-install.md`. In Quick
  Connect, a matching guide beats every other route — check for one FIRST.
- `quick-connect.md` — the ad-hoc playbook: input classifier, discovery
  ladder, URL/repo routes, discover mode, edge cases. Load for Quick
  Connect / Discover mode only.
- `mcp-safety.md` — endpoint probing, the trust review for unknown servers,
  the local-server path, secret-in-URL handling. Load whenever handling a
  pasted URL, a GitHub repo, or any server not on the pinned/official roster.

---

## Phase R — Route the request (always first)

This skill has TWO jobs: the guided **Tools module** of the course, and the
any-time **one-stop shop for connecting a specific tool**. Decide which the
student is asking for before anything else. First match wins:

1. **They named a target** — a specific app ("connect Airtable"), a pasted
   URL, or a GitHub repo → **Quick Connect**. Load `quick-connect.md` (+
   `mcp-safety.md` for URLs/repos/unknown servers) and follow it. A named
   tool with a baked guide in `guides/` routes straight through that guide
   (`quick-connect.md` §3 Step 0a). **The starter pack counts as a named
   target:** "starter pack" / "core stack" / "recommended stack" /
   "connect everything" → `guides/starter-pack.md`, which walks the whole
   recommended stack one tool at a time. Quick
   Connect is a utility, not a course session: it NEVER touches
   `sessions.connect.status`, skips the session machinery of Phases 0–2
   (progress gating, welcome, inventory) — though it still resolves the
   platform per Phase 0.1 first — and works even for a student who has never
   run onboarding.
2. **Discovery phrasing, no target** — "what can I connect?", "is there a
   connector for my CRM?", "find me connectors" → **Discover mode** in
   `quick-connect.md` §7, which feeds picks into Quick Connect one at a time.
3. **No target, module language or nothing specific** — "tools module",
   "connect my tools", "give my OS hands", or a bare `/ai-os:connect` → the
   **Tools module flow** below, starting at Phase 0 (which itself handles the
   already-complete case by offering: re-run / add one app / re-check).

Whichever mode runs: the secrets rule (Phase 1.2) is always live, every
connection ends with a read-only proof test, and every outcome lands in the
`## Tools` section of `context/working-style.md` (the tools legend built in
earlier sessions — there is no separate `tools.md`).

---

This is the Tools module. Build Your AI OS (`/ai-os:build-os`) built the
foundation. The Context module (`/ai-os:build-context`) gave it a brain. **This module gives it
hands** — the ability to actually reach into the student's real email,
calendar, documents, and other apps, instead of only knowing about them from
the interview.

Your job, in one line: **connect the apps → prove each one works with a safe read-only test → write down what's connected.** Teach the pattern the whole way through, so the student could connect a brand-new app next month without you.

---

## The core mental model (teach this first, and come back to it)

> "Up to now your OS has been a brilliant new hire who's read your whole handbook but has never been given a key to the building. Today we hand over the keys — to your email, your calendar, your documents. **Connecting an app is exactly like giving a new hire access to one company system.** You do it one system at a time, you check they can actually get in, and you write down what they now have access to."

Two things this analogy sets up, which you will lean on again and again:

1. **One key at a time.** We connect one app, test it, then move to the next. Never a batch.
2. **A key is access, never a password you hand over.** This leads straight into the secrets rule below — teach it early and mean it.

---

## Phase 0 — Pre-check, platform, and progress

Do all of this before talking to the student about tools.

### 0.1 Detect the platform
Follow `runtime.md` and `platform.md`, then resolve the layout through
`workspace-layout.md`. Store `LAYOUT`, `MASTER_PATH`, `MEMORY_PATH`,
`CONTEXT_DIR`, `PROGRESS_PATH`, and `BACKUP_ROOT`. On `mixed`, stop before
writes and ask Remy or Mav to sort it out with them. Quick Connect may continue only
as a connection utility without workspace writes when the student explicitly
chooses that. On `uninitialized`, the Tools module offers `build-os` first.

### 0.2 Read the progress file
Read `PROGRESS_PATH` with the active host's file-reading capability.

- **If it doesn't exist:** the student likely has not built their OS. Suggest the active host's `build-os` skill but let them choose whether to continue.
- **If `sessions.connect.status` is `"complete"`:** "Looks like you've already connected your tools. Want to run through it again, add a new app, re-check one, or leave it as-is?" Wait. (If they name one app to add, that's Quick Connect: switch to it per Phase R and leave the session state alone.)
- **If `sessions.connect.status` is `"in_progress"` with a `resume_state`:** offer to resume: "Last time we got partway through connecting your tools — we were on [phase / the tool you were mid-connecting]. Pick up from there, or start fresh?" Wait. If resume: restore and continue. If fresh: clear the resume state.

### 0.3 Check the prerequisites gently (don't hard-block)
Look at `sessions.onboard.status` and `sessions.context.status`.

- Ideal: both `"complete"`. Proceed normally.
- If the internal `sessions.onboard` entry isn't complete: as in 0.2, suggest the active host's `build-os` skill first but let them choose.
- If context isn't complete: "The Context module usually comes before this — it's where your OS learned which apps each part of your business uses. We can still connect tools now; I'll just ask you directly instead of reading it from your files. Want to carry on?" Wait.

### 0.4 Set the session to in_progress
Once you're proceeding, set `sessions.connect.status = "in_progress"`, set `started_at`, and write the file. Then move to Phase 1.

---

## Phase 1 — Welcome + the secrets rule (teach before doing)

### 1.1 The welcome
Deliver the mental model above in your own warm words. Set the shape and the time:

> "Here's how the next 20-ish minutes go. I'll show you which apps each part of your business uses, we'll agree on the order to connect them — highest-value first, usually email — and then we connect them one at a time. After each one, I run a quick, totally safe read-only check to prove it actually works. Nothing gets sent, posted, or changed. At the end I write a short file that records what's connected. You can stop and pick up later at any point."

### 1.2 The secrets rule — teach it as a habit, out loud
This is a required teaching beat. Say it clearly and explain the *why*, because the habit matters more than this one session:

> "One important habit before we start. When we connect an app, we're granting **access** — like giving a keycard to the building. We are **never** pasting in a password or a secret 'API key'. If any tool ever asks you to paste a key or password into our chat or into a file, don't. Two reasons: a key sitting in a chat or a file can be seen by anyone who opens it, and the proper connection method never needs it — the app logs you in through your browser, safely, and hands your OS a key it manages for you. So the rule is simple: **we ask for access, we never store keys.**"

Then flag the fallback so they're not surprised later: "If we ever hit an app that genuinely only offers a paste-in key, I'll stop and we'll set it up the safe way instead — I'll never write a secret into one of your files."

**Enforcement (non-negotiable, from the interaction contract):** if the student pastes an API key or password at any point in this session, do NOT store it, do NOT write it to any file, and do NOT echo it back. Say immediately: "I won't save that — you wouldn't want it sitting in a file where it could be seen. What I need is access to [tool], not the key itself. Let's connect it the safe way." Then guide them to the browser sign-in method.

---

## Phase 2 — Inventory: what does each department actually use?

**Teach first (2–3 sentences):**
> "Before we connect anything, let's list the apps your business actually runs on — matched to the parts of your business. No point connecting things you don't use. I'll start from what your OS already knows, then you fill the gaps."

### 2.1 Pull what's already known
You already have material — use it (show, don't ask):

1. Read `<CONTEXT_DIR>/working-style.md` first if it exists — its `## Tools`
   section is the `job → tool` legend. There is no separate `tools.md`.
2. Read `<CONTEXT_DIR>/business.md`, plus resolved `MASTER_PATH` and
   `MEMORY_PATH`, so the inventory respects existing instructions and does not
   duplicate approved memory.
3. If `working-style.md` doesn't exist (they skipped the earlier sessions), skip straight to asking.

### 2.2 Propose the inventory, department by department
Present a pre-filled list for them to react to, not a blank form. Map tools to departments so it's concrete. Example shape (fill with THEIR real departments and any tools you found):

> "Here's what I think your OS should be able to reach, by area:
> - **Marketing / content** → your email, maybe your calendar
> - **Sales / clients** → your CRM (you mentioned [name]), your email
> - **Operations** → your documents (Google Drive / the docs you keep)
> - **Research / lead-gen** → web tools for pulling data off websites (things like Apify or Firecrawl), if you do that
>
> Does that look right? Anything to add or cross off?"

Ask this as ONE question and wait. Keep it loose — the goal is a short, true list of apps, tagged by which department needs them.

### 2.3 The curriculum tool list (the pattern to walk, not a rigid script)
The course teaches literacy across these categories. Use them as your checklist for the inventory — but only connect what the student actually uses:

| Category | What it is, in plain words | Everyday examples (tool-agnostic) |
|---|---|---|
| **Email** | Reading and drafting the student's mail | Gmail, Outlook |
| **Calendar** | Seeing and prepping their schedule | Google Calendar, Outlook Calendar |
| **Docs / Drive** | Reaching their stored documents | Google Drive/Docs, Notion, OneDrive |
| **CRM** | Their customer / client records | HubSpot, Pipedrive, a Notion or Airtable database, "a spreadsheet" |
| **Web data tools** | Pulling data/content off websites | Apify, Firecrawl |

**The tool-agnostic promise:** you are teaching the *pattern* — how to connect any app and prove it works — not one product. Whatever the student names, the loop in Phase 4 is the same. If they use Outlook not Gmail, or a spreadsheet not a "real" CRM, that's fine — connect what they have.

### 2.4 Prioritise — highest value first
Once the list is agreed, propose the order and get a quick yes:

> "I'd connect these in this order — most useful first, so if we only get through two today you've got the big ones: **1) email, 2) [their most-used app], 3) …**. Email almost always earns the top spot — it's where most of your day already lives. Good with that order?"

Email first is the default. Wait for confirmation, then start connecting.

Save progress: record the agreed inventory + order into `resume_state`, write the file.

---

## Phase 3 — How connecting works in the active host

**Teach before the first connection (this is the conceptual core of the session).** Keep it plain:

> "Here's the actual mechanic. Your AI reaches an outside app through an adapter — like the keycard reader for that system. You connect it once, sign in through the browser, and then your OS can use the access you approved. I'll choose the safest path for each app."

Choose the path; never make the student decode host plumbing. The pinned
app-by-app routing (which app goes through which door) lives in
`known-routes.md` — consult it before deciding.

### Claude Code paths (`HOST_RUNTIME=claude`)

- **A — Anthropic-hosted connectors:** for Gmail, Google Calendar, and Microsoft 365 / Outlook when live inspection confirms them, use **claude.ai → Settings → Connectors** and browser sign-in.
- **B — the Composio gateway (add it during this session):** most other apps route through **Composio**, a one-stop connection hub. It is NOT pre-installed — add it once, directly into the student's own Claude config, so the connection belongs to them and survives any plugin change:

  ```bash
  claude mcp add --scope user --transport http composio https://connect.composio.dev/mcp
  ```

  Then inspect `/mcp` and complete the one-time browser sign-in (it creates the student's OWN free Composio account — no shared credentials). If the new server isn't visible in `/mcp` yet, save progress and have them restart Claude Code — it appears on the next start. After that, individual apps (Notion, HubSpot, Sheets, and so on) connect through Composio's live tools, each with its own browser sign-in. If the student wants AI image/video generation, add **Higgsfield** the same way: `claude mcp add --scope user --transport http higgsfield https://mcp.higgsfield.ai/mcp`.
- **C — direct fallback:** only when the first two routes do not cover the app, use `claude mcp add --scope user --transport http <name> <url>`, then inspect `/mcp` and complete browser authentication.

### Codex paths (`HOST_RUNTIME=codex`)

- **A — connector plugin:** inspect `/plugins` in CLI or **Settings → Plugins** in the IDE/app. For Gmail, Calendar, Drive, Slack, and similar apps, install/enable the appropriate connector plugin if it is available, authenticate through the browser, and start a **new session/chat** if the tools are not visible yet. Never send a Codex student to claude.ai Settings.
- **B — the Composio gateway (add it during this session):** it is NOT pre-installed — register it in the student's own Codex config: `codex mcp add composio --url https://connect.composio.dev/mcp` (and `codex mcp add higgsfield --url https://mcp.higgsfield.ai/mcp` only if they want AI media generation). Follow the live Codex auth prompt to complete the one-time browser sign-in, and start a **new session/chat** if the tools are not visible yet. Use Composio's live connection tool and returned browser URL for individual apps. Do not promise a `/mcp` panel in Codex.
- **C — direct fallback:** inspect `codex mcp list`; only when no gateway or connector-plugin route exists, use `codex mcp add <name> --url <url>`, complete the host's authentication flow, and re-check in a new session if needed.

**Important honesty note for you, the running agent:** the exact wording of menus, the precise `/mcp` panel layout, and which apps are on the Connectors page vs. need `claude mcp add` all change between Claude Code versions. **Do not recite steps from memory as if they're gospel.** Before you walk the student through their first connection:

1. Inspect the **active host** using only its paths above. For Claude, inspect `/mcp` and `claude mcp list`. For Codex, inspect installed plugin tools, `/plugins`, and `codex mcp list` as appropriate.
2. Composio and Higgsfield are NOT bundled with the plugin — this session adds them with the Path-B commands above. After adding, verify they actually show in the live inventory before walking the student through sign-in; never pretend they are present.
3. Adapt click-by-click wording to the live product. If a newly installed Codex plugin needs a new session, save progress before asking for it.

If something here doesn't match what the student sees, trust the live product and say so plainly: "The menu looks a little different on your version — no problem, here's the equivalent." Never insist on a path that isn't there.

---

## Phase 4 — Connect, ONE app at a time, verify each (the core loop)

For **each** app in the agreed order, run this exact loop. Never batch. Finish one fully before starting the next.

### Step 1 — Teach what this app unlocks (1–2 sentences)
> "First up: your email. Once this is connected, your OS can read your inbox — so it can draft replies, summarise what came in, pull out the important threads. Let's give it the key."

### Step 2 — Connect it (pick Path A or Path B for them)
- Decide A/B/C from the active host's live inventory. Never use a Claude panel or command in Codex.
- Walk them through it **one action at a time**, in their platform's terms, waiting after each:
  - **Claude:** use the Claude A/B/C actions above.
  - **Codex:** Path A uses the connector plugin browser and browser auth; Path B adds the gateway with `codex mcp add`, then uses its live auth prompt and connection link; Path C uses `codex mcp add <name> --url <url>`. Save progress and start a new session only when the added tool requires it.
- Keep the secrets rule live: if a browser sign-in appears, that's correct and safe. If anything asks them to paste a key into chat, stop and use the safe method.

### Step 3 — Verify with a SEND-NOTHING read test (mandatory)
This is the proof moment. **The test must only READ. Never send, post, create, update, or delete anything.** Run a tiny read and show the student the result so they see it working with their own eyes.

Safe read tests per category (adapt the exact tool to what's connected):

| App | Safe read-only test | What success looks like |
|---|---|---|
| **Email** | "List the subject lines of my 3 most recent emails." | Three real subject lines appear |
| **Calendar** | "What's on my calendar today (or this week)?" | Real event titles + times appear |
| **Docs / Drive** | "List 3 of my most recent documents by name." | Real file names appear |
| **CRM** | "Show me 3 recent contacts / deals by name." | Real records appear |
| **Web data tool** | A trivial read/health check (e.g. fetch the title of one public web page). | It returns without an auth error |

Say what you're doing and why, so they learn the habit:
> "Now the safe check. I'm going to *read* your three most recent email subject lines — nothing sent, nothing changed, just proving the key turns. Here's what came back: [results]. Recognise those? Then it's working."

**If the test fails:** troubleshoot briefly, calmly (see Phase 6). If it still fails after a quick try, don't let it block the session — note it as "attempted, not yet working" and move on. Better to connect three apps that work than get stuck on one.

### Step 4 — Note the result and move on
Record in the `## Tools` section of `working-style.md`: the app, whether it verified (✅ working / ⚠️ attempted, not working), the department(s) it serves, and any caveat the student mentioned ("CRM data is messy — don't fully trust it"). Update the progress `resume_state` and write the file. Then start Step 1 for the next app.

Repeat until the agreed list is done (or the student wants to stop — that's fine, the rest can be added later by re-running Claude `/ai-os:connect` or Codex `$ai-os:connect`).

---

## Phase 5 — Preview and update the Tools section of context/working-style.md

The tools legend already lives as the `## Tools` section of `context/working-style.md` (built in `/ai-os:build-os`, deepened in `/ai-os:build-context`). This session **upgrades that same section in place** from a plain "job → tool" legend into the live "what's connected" record — it does **not** create a separate `tools.md` file. If `working-style.md` doesn't exist (they skipped the earlier sessions), create it from the §4 template in `core-six-templates.md` — a PLUGIN reference file at `<PLUGIN_ROOT>/skills/build-context/core-six-templates.md`, NOT a file in the student's OS folder — with just the `## Tools` section filled.

**Teach first:**
> "Last thing: I'll update the tools legend in your `working-style.md` file — turning it into the record of what your OS can now reach. So every future session knows which apps are live, and later, when the Autopilot module puts suitable work on a schedule, it knows what can run on its own. I'll show it to you before I save anything."

### 5.1 Preview the section (never write without a yes)
Show the full proposed `## Tools` section in the chat and ask: "Here's what I'd save — look right?" Wait for the yes. Adjust if they want changes. Leave the rest of `working-style.md` (output prefs, hard rules, rhythms, timezone) untouched.

**Template for the `## Tools` section of
`<CONTEXT_DIR>/working-style.md`** (fill with real data):

```markdown
## Tools

The apps this OS can reach, what each is for, and how far to trust it.
Updated whenever tools are connected or changed. (The slim `job → tool`
version is mirrored in resolved `MASTER_PATH` under "My stack".)

### Connected and verified

| App | Category | Departments it serves | How it's connected | Status | Notes / caveats |
|---|---|---|---|---|---|
| Gmail | Email | marketing, sales | Connectors | ✅ verified <date> | Primary inbox: <address> |
| Google Calendar | Calendar | all | Connectors | ✅ verified <date> | Primary calendar only |
| Notion | Docs / CRM | operations | Composio | ✅ verified <date> | — |
| <Vendor tool> | <category> | <depts> | Official MCP (<endpoint>) | ✅ verified <date> | — |
| <Community tool> | <category> | <depts> | Local program (<owner/repo>) | ✅ verified <date> | Runs on this computer — the fragile kind |

### Connected but not yet verified

| App | Category | Departments | What happened |
|---|---|---|---|
| <CRM name> | CRM | sales | Connected but the read test failed — revisit. |

### Not connected (noted for later)

| App | Category | Why not / when |
|---|---|---|
| Firecrawl | Web data | Not used yet — connect if we start scraping. |

### The secrets rule (kept here as a reminder)

This OS is granted **access** to apps, never their passwords or API keys.
No secret keys are stored in these files. To add or re-check an app, ask to connect
it — access is always granted through a browser sign-in, never a pasted key.
```

**Never put an actual API key, token, password, or secret in this section.** It records *what* is connected and *how much to trust it* — never any credential. If you're ever unsure whether something is a secret, leave it out.

### 5.2 Write it
Update the `## Tools` section of `working-style.md` with the active host's safe
file-editing capability, carrying the rest forward unchanged. Preview and
update the slim map in `MASTER_PATH` in the same action. Never write connection
status to `MEMORY_PATH`. Read both changed files back before claiming success.

---

## Phase 6 — Troubleshooting (keep it short and calm)

When a connection or a read test fails, translate the problem into plain English first, then try one fix. Don't lecture, don't spiral. If a quick fix doesn't land, note it and move on — the session's success doesn't hinge on any single app.

| Symptom | Plain-English meaning | Quick fix |
|---|---|---|
| Sign-in window never opened | The browser handoff didn't fire | Retry using the active host's plugin/connection surface and confirm a default browser is set. |
| Composio shows "needs authentication" | The one-time switch-on has not happened | Use the live host's Composio authentication prompt; on Claude that may be `/mcp`, while Codex uses installed plugin tools / auth UI. |
| "This app isn't verified" in the browser | Google/Microsoft's standard caution screen | Click "Advanced" → "Go to [app]" to continue — it's expected for these sign-ins |
| Connected, but the read test finds nothing | Signed into the wrong account, or the wrong calendar/inbox | Check which account they signed in with; disconnect and reconnect with the right one |
| Email/calendar connection path is absent | The current host may use a separate connector plugin | Claude: inspect claude.ai Connectors. Codex: inspect `/plugins` or Settings → Plugins, authenticate, then start a new session if needed. |
| "Access denied" on Google | A locked-down work/school Google account | Try a personal Google account, or note it and move on |
| App asks to paste a key into chat | It's offering the unsafe path | Don't paste it. Note the app as "needs safe setup later" and continue — never store a key |
| App they use isn't connectable at all | No safe connection available yet | Note it in the `## Tools` section of `working-style.md` under "not connected"; the OS can still work with it manually |

Golden rule: a stuck tool is noted, not a dead end. Move on.

---

## Phase 7 — Verify the session + wrap up

### 7.1 Prove the whole thing works (don't wrap on faith)
End with one combined proof that shows the OS genuinely has hands now. Pick the highest-value connected app and do one more safe read that the student will recognise:
> "Let's see your OS actually use its new hands. Reading your three most recent email subjects one more time — [results]. That's your OS reaching your real inbox. A few weeks ago it only knew *about* your email; now it can actually read it."

### 7.2 Mark the session complete (per progress-state.md)
- Set `sessions.connect.status = "complete"`, set `completed_at`.
- Remove the `resume_state`.
- Set `sessions.connect.next_skill = null` — connect is the last plugin-delivered homework skill. The Skills module uses Claude's creator or Codex `$skill-creator`; the Autopilot module uses the active host's supported scheduling surface.
- Write the file.

### 7.3 Recap + point to the next session
Keep it warm and short. Cover: what's now connected (list them), the one habit that carries the secrets lesson ("we grant access, never hand over keys"), and the pointer forward:

> "That's the Tools module done — your OS has hands now. It can reach [the apps you connected], and every one passed a safe read-only check. Two things to carry forward: your OS gets **access** to apps, never their passwords — that habit keeps you safe. And if you ever add a new app, run [the active host's connect skill] again.
>
> Here's the big picture: your OS now has a **brain** and **hands**. Next up in the workshop: skills, the repeatable playbooks that teach it how you do things."

---

## Reference notes (internal — background facts for YOU; never read this section to a student)

Working facts behind the runtime-specific paths. Always trust the active host's live inventory over remembered wording.

1. **The routing decision is host-specific.** Claude uses its documented Connectors, Composio-gateway, and direct-add paths. Codex uses connector plugins, the gateway via `codex mcp add`, then direct `codex mcp add` as fallback. Never cross the UI or commands.

2. **Never recite menus from memory.** Panel wording, button labels, and click-paths shift between versions. On Claude, inspect the live `/mcp` panel or claude.ai Connectors page. On Codex, inspect installed plugin tools, `/plugins`, and the live connector/auth surface. Narrate only what is actually on screen.

3. **Routing facts live in `known-routes.md`** (sibling file — the single source of truth): the pinned app-by-app routes, the Composio gateway add commands (the plugin ships NO MCP servers; connections are added to the student's own user-scope config so they survive plugin changes), the official vendor endpoint roster, the direct-add commands per host, and the rube.app ban. Keys for API-key apps are entered on Composio's own connection page — never in chat. Do NOT restate endpoints here; read that file.

4. **The read-only test verbs.** Make sure each safe read test triggers a pure read on the app as connected today (e.g. "list my 3 recent emails" maps to a read tool, not a search-that-could-draft). When in doubt, pick the most obviously read-only phrasing.

5. **CRM reality.** Many students won't have a "real" CRM. The skill teaches it tool-agnostically: connect Notion/Airtable/Sheets as their CRM if that's what they actually use, or note "CRM = a spreadsheet, handled manually" and move on.

6. **Windows.** Do not assume either host's connector UI is identical across operating systems. Inspect the active host live and adapt per note 2.

## Self-Improvement Loop

After each run, propose a one-line skill update only if it would change what a
future run does. Edit this `SKILL.md` only after explicit approval.
