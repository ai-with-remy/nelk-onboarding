# Baked guide — Composio (the aggregator hub)

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student.

**What to say it is:** "One hub that connects to 1,400+ apps. You log into
your apps through Composio once, and your OS reaches them all through a
single connection — one place to manage, re-check, and revoke everything."

This guide sets up the HUB itself. Individual apps connect INSIDE it
afterwards — through their own baked guides or the dashboard.

## Route

**Hosted server → two doors** (`known-routes.md` "Two doors"). Offer the app
door first for Claude students — it follows them everywhere:

- **App door (works on web, desktop, mobile AND Claude Code):** claude.ai →
  Settings → Connectors → Add custom connector — name `Composio`, URL
  `https://connect.composio.dev/mcp`. Hand them the pre-filled link (template
  in known-routes; if the form arrives empty, they fill those two fields
  manually).
- **Machine door (this computer only — and the only Codex option):**

  ```bash
  # Claude Code
  claude mcp add --scope user --transport http composio https://connect.composio.dev/mcp
  # Codex
  codex mcp add composio --url https://connect.composio.dev/mcp
  ```

Either door ends in the one-time browser sign-in (Claude: `/mcp` →
authenticate or the connector's Connect button; Codex: the live auth
prompt) — it creates the student's OWN free Composio account, no shared
credentials. Restart the host if the server isn't visible yet.
**NEVER anything referencing rube.app** — dead service.

Then record the aggregator answer per §3a:
`**Aggregator:** Composio — confirmed <date>` under the `## Tools` header.

## Connecting apps inside the hub

The hub being live is not the same as any app being connected. Per app:
the dashboard (app.composio.dev), or from here — `COMPOSIO_SEARCH_TOOLS`
says whether an app is covered and `COMPOSIO_MANAGE_CONNECTIONS` returns the
browser sign-in link. API-key apps enter the key on **Composio's own page,
never in chat**.

## Prove it (read-only, free)

Search the catalogue from here: `COMPOSIO_SEARCH_TOOLS` for an app they
actually use ("let's check yours is covered — what's your CRM?"). Real
results back = the hub is live.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| Shows "needs authentication" | The one-time sign-in hasn't happened | `/mcp` → authenticate (Codex: its auth prompt) |
| Added but not visible | Hosts load new servers at startup | Fully quit and reopen |
| An app's tools are missing | The app isn't connected INSIDE the hub | Dashboard or `COMPOSIO_MANAGE_CONNECTIONS` — hub ≠ app |

## Record

`## Tools` row per §6 for the hub itself, plus the `**Aggregator:**` line.
