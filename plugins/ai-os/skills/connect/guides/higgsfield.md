# Baked guide — Higgsfield

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student.

**What to say it is:** "Claude can't draw — it has no image model of its
own. Higgsfield is the studio it calls instead: images, video, the creative
assets your content runs on."

## Route

**No aggregator check needed — Composio has no Higgsfield toolkit.** This
one is a hosted server with a browser sign-in, full stop — so offer BOTH
doors per `known-routes.md` "Two doors": the app door first for Claude
students (claude.ai → Settings → Connectors → Add custom connector, URL
`https://mcp.higgsfield.ai/mcp` — it then works on web, desktop, mobile AND
Claude Code; hand them the pre-filled link), or the machine door:

```bash
# Claude Code
claude mcp add --scope user --transport http higgsfield https://mcp.higgsfield.ai/mcp
# Codex
codex mcp add higgsfield --url https://mcp.higgsfield.ai/mcp
```

Then `/mcp` → authenticate (Codex: the live auth prompt) — a browser sign-in
to their own Higgsfield account (they create one at higgsfield.ai if they
don't have it). If the server isn't visible yet, restart the host — it
appears on the next start.

## Prove it (read-only, spends nothing)

Check the account, don't generate: "Show me my Higgsfield plan and credit
balance." Real numbers back = working. **Generating images/video spends
their Higgsfield credits** — one plain line about that before their first
real generation.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| Server not in `/mcp` after adding | Hosts load new servers at startup | Fully quit and reopen, then check again |
| Tools error with an auth message | The sign-in lapsed | `/mcp` → authenticate again — takes seconds |
| A generation fails with a credit error | Plan's credits ran out | Top up / upgrade at higgsfield.ai — their call |

## Record

`## Tools` row per §6. How connected =
"Official MCP (mcp.higgsfield.ai/mcp)".
