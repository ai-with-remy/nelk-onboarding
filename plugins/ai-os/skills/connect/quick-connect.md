# Quick Connect + Discover — connect ANY tool, any time

Internal playbook for the running agent. Loaded when `/ai-os:connect` routes to
**Quick Connect** or **Discover** mode (see Phase R in `SKILL.md`). Also load
`known-routes.md` and `mcp-safety.md` — they carry the routing facts and the
safety machinery this file leans on.

The interaction contract still governs everything here: one question at a
time, teach before doing, preview before writing, jargon ban, secrets rule.
Quick Connect is a **utility, not a course session** — it never touches
`sessions.connect.status`, and it works even for a student who has never run
onboarding (see "No OS folder" in the edge cases).

Your job in one line: **work out what they gave you → find the best route →
connect it → prove it with a read-only test → record it in the `## Tools`
section of `context/working-style.md`.**

---

## 1. Before any route: the duplicate check

Inspect the live inventory (Claude: `/mcp` + `claude mcp list`; Codex:
`codex mcp list` + installed plugin tools) and read the `## Tools` section of
`context/working-style.md` if it exists. If the tool is already connected, say
so and offer a **re-check** (run the read-only test again) instead of
reconnecting. Recheck passes → update the verified date in that `## Tools`
section and stop.

## 2. Classify the input

Run these in order — first match wins. (`mcp-safety.md` §1 — the
secret-in-input pre-check — runs before ALL of this.)

1. **GitHub repo** — `github.com/<owner>/<repo>` (including `/tree/...` links
   to a subfolder) or bare `owner/repo` shorthand → **REPO route** (§5).
2. **Any other URL** → **URL route** (§4).
3. **Anything else** — a tool name, a product, "my CRM" → **NAME route** (§3).
   If the name is ambiguous (multiple real products match, or it's a category
   like "my notes app"), ask ONE question with 2–4 named candidates and a
   one-line description each. Never guess between products.

## 3. NAME route — the discovery ladder

**Step 0a — baked guides first (before everything else).** Normalise the
name (lowercase; common aliases: "chrome dev tools" / "devtools" →
chrome-devtools, "appify" → apify, "kie" / "kie.ai" / "kie ai" → kie-ai,
"play writer" / "playwrite" → playwriter, "open router" → openrouter,
"higgs field" → higgsfield, "fire crawl" → firecrawl, "meta" /
"facebook ads" / "fb ads" / "instagram ads" → meta-ads, "starter pack" /
"core stack" / "recommended stack" / "connect everything" → starter-pack,
which sequences the whole recommended stack through the other guides). If
`guides/<slug>.md` exists in this skill folder, follow that guide exactly
per §3a and SKIP the ladder — the guide already encodes the aggregator
question, the right route per answer, the proof test, and the known failure
modes. The ladder below is for tools WITHOUT a baked guide.

**Step 0b — pinned routes.** Check the pinned table in `known-routes.md`.
If the tool is pinned (Gmail → Connectors, Notion → Composio, etc.), take that
route directly — no hunt. Anything touching rube.app is hard-ignored.

**Then walk the ladder in order — rung 1 is Composio, and it wins whenever
the student's Composio hub is live:**

1. **Composio toolkit** *(ALWAYS first when the Composio gateway is in the
   live inventory — do not hunt for an official vendor MCP before checking
   this rung; a real test connected Cal.com through a vendor server while
   the student's Composio hub, which covers Cal.com, sat there connected).*
   Check coverage the agent-readable way (`known-routes.md` — the
   coverage-check section): call the gateway's own `COMPOSIO_SEARCH_TOOLS`
   with the app name; the response says whether Composio covers the app,
   whether the student already has it connected, and that
   `COMPOSIO_MANAGE_CONNECTIONS` starts the browser sign-in. Covered →
   recommend Composio and stop the hunt: every connection lives in one hub
   the student already trusts, and no new server needs adding or
   trust-reviewing. Fall past this rung only if Composio doesn't cover the
   app, the Composio connection genuinely fails, or the student explicitly
   asks for the vendor's own connection. If the gateway is NOT installed:
   check the public catalogue instead (same section) and offer to add the
   gateway — but if the student doesn't want Composio, that's a legitimate
   choice: skip this rung without friction and say so respectfully.
2. **Official vendor-hosted MCP** *(the route when Composio is out of play —
   not installed and not wanted, no toolkit for this app, or the student
   prefers the vendor's own door)*. Web-search "<tool> MCP" and check the
   vendor's own docs. Accept an endpoint ONLY if it appears on the vendor's
   own domain or official docs — not a blog, not a third-party directory.
   **Probe it before recommending it** (`mcp-safety.md` §2) — endpoints rot;
   never recite one from memory.
3. **Host connector directory.** Claude: inspect the live claude.ai
   Connectors page. Codex: `/plugins` / Settings → Plugins. Only for apps
   that actually appear there.
4. **Community server (GitHub)** — first-class fallback, eyes open. Search
   for the most credible repo (the vendor's own org if possible; otherwise
   recent, maintained, widely used). If its README documents a hosted
   endpoint → URL route. If it's local-only → the local-server path
   (`mcp-safety.md` §4). Community servers ALWAYS get the trust review
   (`mcp-safety.md` §3).
5. **Nothing viable** → log it under "Not connected" in the `## Tools` section of `working-style.md` **with
   what you tried and today's date** (so a future run doesn't repeat the
   hunt), and offer the honest framing: "your OS can still work with this
   one — you'll be the hands for it, and we can re-check in a month or two;
   new connections appear all the time."

How to present a found route (teach, one beat). Composio-found:
> "Good news — [tool] connects through your Composio hub, the same door your
> other apps already use. One quick browser sign-in and it's live. Want me to
> wire it up?"

Vendor-found (only when Composio was out of play):
> "Good news — [tool] has an official connection, straight from the people
> who make it. That's their own front door. Want me to wire it up? Takes
> about a minute, and you'll sign in through your browser like normal."

## 3a. Running a baked guide

The `guides/` folder (sibling to this file) holds a step-by-step recipe per
core-stack tool — firecrawl, apify, perplexity, higgsfield, openrouter,
chrome-devtools, playwriter, kie-ai, meta-ads — plus the two aggregator hubs
themselves (composio, zapier) and `node-install.md`, the shared
quiet-prerequisite recipe. Hosted-server guides offer BOTH doors per
`known-routes.md` "Two doors" (app-level first for Claude students, machine
door as fallback). Inside a guide, these shared rules apply:

**The aggregator check** (run it only when the guide has a Composio path —
for tools Composio doesn't cover, the question is pointless friction). Ask
EVERY run — people change their minds — but let memory keep it quick:

- Read the `## Tools` section of `context/working-style.md` for an
  `**Aggregator:**` line.
- Line exists → one quick confirm: "Quick check — you're still running your
  app connections through Composio, right?" Yes → proceed on that path.
  Changed → update the line, route accordingly.
- No line → ask once, plainly: "Do you run your tool connections through a
  hub like Composio — one place that connects to lots of apps — or do you
  prefer connecting each tool directly?" (Zapier is a valid hub answer too.)
  Record it as one line right under the `## Tools` header:
  `**Aggregator:** Composio — confirmed <date>` (or `Zapier` / `none`).
- They name a hub they don't actually have set up yet → run that hub's own
  guide first (`guides/composio.md` / `guides/zapier.md`), then come back to
  the tool they originally asked for.
- **Composio + the guide has a Composio path** → the tool still needs its
  OWN connection inside Composio (having the hub is not having the app).
  Point them at the hub, warmly: "You can add this through Composio to make
  things easier — head to your Composio dashboard and log in to <tool>
  there." Offer to kick off the sign-in from here too (the gateway's
  `COMPOSIO_MANAGE_CONNECTIONS` returns the browser link). API-key apps
  enter the key on Composio's page, never in chat.
- **Zapier** → point them at their Zapier MCP configuration to enable the
  app and its actions there; verify the same way afterwards.
- **None / direct** → the guide's direct path.

**Local programs install their prerequisite quietly.** When a guide needs
Node, run `guides/node-install.md`: check silently; if it's missing, install
it with ONE line of narration — no ceremony, no options menu. Always
register local servers with the ABSOLUTE npx path (node-install §4) so the
connection survives however the host is launched.

**Everything else is unchanged:** the secrets rule, the read-only proof
test, the trust review for community servers, and recording per §6.

## 4. URL route — they pasted a link

1. **Probe it** (`mcp-safety.md` §2).
2. **Live MCP endpoint** (open or sign-in-gated) → connect it with the host's
   add command (`known-routes.md`), complete the browser sign-in, then trust
   review if it's not an official/pinned server, then verify (§6).
3. **HTML product page** (not an endpoint) → fetch it read-only and look for
   a documented MCP endpoint (a `/mcp` link, "Model Context Protocol" in
   docs, `/.well-known/oauth-protected-resource`). Found → probe → connect.
   Not found → extract the product name, tell the student what you're doing
   ("that link is the tool's homepage — let me find its actual connection
   point"), and run the NAME route (§3).
4. **`localhost` / private-IP URL** → that's a program running on their
   computer, not a cloud service; handle via the local-server framing
   (`mcp-safety.md` §4) — usually it means some other setup step already
   exists; ask what guide they're following.
5. **Dead** → say plainly what the probe found, then offer the NAME route
   hunt for the same tool.

## 5. REPO route — they pasted a GitHub repo

Inspect it READ-ONLY first — README + file tree via web fetch. Do NOT clone;
connect never needs the code locally except in the local-server path.

Then branch on what the repo actually is:

- **It contains `SKILL.md` (anywhere)** → it's a **skill** (a recipe card the
  AI follows), not an app connection. Say so plainly: "this one's a recipe
  card, not a key to an app — different installer, and ours security-scans it
  first." Hand off to the active host's `install-skill` skill with the exact
  repo (and subfolder, if the link pointed at one). install-skill owns its
  own quarantine + scan gate — never pre-approve, shortcut, or partially
  install on its behalf. If the repo holds BOTH a skill and a server, ask
  which they wanted (one question, both options named).
- **README documents a hosted/remote MCP endpoint** → happy path: extract the
  URL → URL route (§4). Many vendor repos are just the source code for an
  official hosted server — use the hosted one.
- **It's a local-only (stdio) server** — run instructions like `npx ...`,
  `node ...`, `python ...`, an MCP SDK in its manifest → the local-server
  path (`mcp-safety.md` §4), after re-checking rungs 1–3 of the ladder for a
  remote alternative for the same tool.
- **Monorepo with several servers** → list the candidates in plain English,
  ask ONE question about which they want.
- **None of the above** → be honest about what it is ("this repo looks like
  [X], not something we can connect") and offer the NAME-route hunt for the
  underlying product if there is one.
- **Private repo / 404** → they may need to be signed into GitHub or have
  access; use the machine's existing git/gh auth if present — never collect
  tokens in chat.

## 6. Verify + record (every route ends here)

Run the Tools module Phase 4 loop from `SKILL.md`, once, for this one tool:
teach what it unlocks (1–2 sentences) → connect → **SEND-NOTHING read test**
→ record. The read test picks the most obviously read-only tool the new
connection exposes ("list 3 recent...", "fetch one title") and shows the
student the real result.

- **Degraded tier:** if the server genuinely exposes no safe read-only tool
  (write-only servers exist), verification = the tool list loaded + the
  student accepted the trust review. Record it as
  `✅ connected — limited check (no read test available)` and say the same in
  plain English.
- **Recording:** update the `## Tools` section of
  `<OS_ROOT>/context/working-style.md` using the template in `SKILL.md`
  Phase 5 — preview the new row(s) before writing, never rewrite the rest of
  the file. Fill the "How it's connected" column (Connectors / Composio /
  official MCP + endpoint / community MCP + `owner/repo` / local program +
  `owner/repo`). Failed hunts go under "Not connected" with what was tried and
  the date.
- **No OS folder** (student has not run `build-os`): still connect and verify — then
  offer to create a minimal `context/working-style.md` with just the `## Tools`
  section holding this record, and mention `/ai-os:build-os` warmly,
  without blocking anything.

## 7. Discover mode — "what can I connect?"

When there's no specific target:

1. Read `context/working-style.md` (its `## Tools` section is the legend) and
   `context/business.md` where they exist, plus the live inventory — know
   what's already connected and what their business runs on.
2. Propose 3–5 candidate connections **mapped to their departments**, each
   with a one-line "what it unlocks" ("your bookkeeping folder mentions
   Stripe — connect it and your OS can pull your actual revenue numbers").
   Pre-fill from their real context; never present a generic catalogue dump.
3. One question: which (if any) shall we connect first?
4. Each accepted candidate runs through Quick Connect (§2 onward), one at a
   time — never batch.

If they have no context files, ask what apps their business runs on (with
examples, per the contract) and propose from that.

## 8. Edge cases

| Case | Handling |
|---|---|
| Ambiguous name | One question, 2–4 named candidates with one-liners |
| Tool has a baked guide in `guides/` | The guide wins over every other route, including pinned ones (§3 Step 0a) |
| Tool has BOTH an official MCP and a Composio toolkit | Composio gateway live → recommend Composio (one hub, one place to manage and revoke everything), mentioning the vendor's own door in one line for anyone who prefers direct. Gateway not installed and not wanted → recommend official. Student picks. |
| Dead / moved endpoint | Probe verdict in plain English, fall down the ladder, log the attempt + date |
| Anything referencing rube.app | Hard-ignore — dead service, even if search results still show it |
| Already connected | Offer re-check, not reconnect (§1) |
| Marketing page URL | Degrade to NAME route with the extracted product name (§4.3) |
| Write-only server | Degraded verification tier (§6) |
| Student pastes an API key mid-flow | The secrets-rule enforcement from `SKILL.md` Phase 1.2 applies verbatim — never store, never echo, redirect to the safe method |
| No web-search capability on this host | Say so, skip ladder rungs that need it, and lean on Composio + pinned routes |
| Codex parity | Every route has a Codex path: no claude.ai Connectors rung (use `/plugins`), `codex mcp add/list/remove`, live auth prompts instead of `/mcp`, new-session-after-add caveat. Never show a Claude panel or command to a Codex student. |
