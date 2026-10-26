# Baked guide — Apify

Internal recipe for the running agent. Shared rules live in
`quick-connect.md` §3a. Never read this file to a student. (Students often
type "appify" — same tool.)

**What to say it is:** "Apify is a library of ready-made scrapers. Where
Firecrawl reads one page, Apify turns one page into thousands — every review
of a product, every post from an account, every listing on a board."

## Route

Run the aggregator check (§3a). **Apify IS covered by Composio.**

**Composio path (aggregator = Composio):**
1. "You can add this through Composio to make things easier — head to your
   Composio dashboard and log in to Apify there." Offer to kick off the
   sign-in from here (`COMPOSIO_MANAGE_CONNECTIONS` → browser link).
2. Composio's Apify connection takes an API key, entered on **Composio's own
   page — never in chat**: free account at apify.com, key from the Apify
   console (Settings → API & Integrations).
3. When they say it's connected, verify below.

**Direct path:** the official hosted server — browser sign-in, free plan
comes with monthly credits.

```bash
# Claude Code
claude mcp add --scope user --transport http apify https://mcp.apify.com
# Codex
codex mcp add apify --url https://mcp.apify.com
```

Restart the host if needed, then `/mcp` → authenticate (browser OAuth).

## Prove it (read-only, spends nothing)

Search the store, don't run anything: "Find me a scraper that pulls Google
reviews for a business." A list of real actors back = working. **Searching
is free; RUNNING a scraper spends their plan credits** — say that one line
before their first real run, and flag big scrapes before starting them.

## If it breaks

| Symptom | Meaning | Fix |
|---|---|---|
| Composio live but no Apify tools | App not connected inside Composio yet | Back to the dashboard — hub ≠ app |
| A run fails with a credits error | The free plan's monthly credits ran out | Wait for the reset or upgrade at apify.com — their choice, no pressure |
| A scraper returns partial data | Some sites resist scraping | Normal — try the store's most-used actor for that site instead |

## Record

`## Tools` row per §6. How connected = "Composio" or
"Official MCP (mcp.apify.com)".
