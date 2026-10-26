# Baked guide — Firecrawl

Internal recipe for the running agent. Shared rules (aggregator check, quiet
prerequisites, recording) live in `quick-connect.md` §3a — run them, don't
restate them. Never read this file to a student.

**What to say it is:** "Firecrawl reads web pages properly. Search finds
pages — Firecrawl gives your OS what's actually ON a page, clean: a
competitor's copy, a pricing page, a whole article."

## Route

Run the aggregator check (§3a). **Firecrawl IS covered by Composio.**

**Composio path (aggregator = Composio):**
1. Tell them, warmly: "You can add this through Composio to make things
   easier — head to your Composio dashboard and log in to Firecrawl there."
   Offer to kick off the sign-in from here too (the gateway's
   `COMPOSIO_MANAGE_CONNECTIONS` returns the browser link).
2. Composio's Firecrawl connection takes an API key, entered on **Composio's
   own page — never in chat**: they create a free account at firecrawl.dev
   and copy the key from their Firecrawl dashboard.
3. When they say it's connected, verify below.

**Direct path (no aggregator, or they prefer direct):** the official hosted
server. It works immediately with NO account on a rate-limited free tier; a
browser sign-in upgrades it later if they hit limits. Hosted server → both
doors apply (`known-routes.md` "Two doors"): app door with URL
`https://mcp.firecrawl.dev/v2/mcp` if they want it everywhere, or the
machine door:

```bash
# Claude Code
claude mcp add --scope user --transport http firecrawl https://mcp.firecrawl.dev/v2/mcp
# Codex
codex mcp add firecrawl --url https://mcp.firecrawl.dev/v2/mcp
```

Restart the host if it doesn't appear, then `/mcp` → authenticate only when
they want the full tier. NEVER the legacy key-in-URL form
(`mcp.firecrawl.dev/<key>/...`) — that's a password inside a link.

## Prove it (read-only)

Scrape ONE page they know — their own homepage beats example.com: "I'll read
your homepage and tell you the main headline." A real headline back = working.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| Rate-limit error on the direct path | The keyless free tier throttles | `/mcp` → sign in to Firecrawl, or just wait a minute |
| Composio is live but has no Firecrawl tools | The app isn't connected INSIDE Composio yet | Back to the dashboard — having the hub isn't the same as having the app |
| A scrape returns almost nothing | The page is login-walled or heavily scripted | Normal for some sites — try another page; logged-in pages are Playwriter's job |

## Record

`## Tools` row per §6. How connected = "Composio" or
"Official MCP (mcp.firecrawl.dev/v2/mcp)".
